from datetime import datetime
import httpx

from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.learner import Learner
from app.models.interaction import InteractionLog
from app.models.item import ItemRecord
from app.settings import settings

async def fetch_items() -> list[dict]:
    url = f"{settings.autochecker_api_url}/api/items"
    auth_credentials = (settings.autochecker_email, settings.autochecker_password)

    async with httpx.AsyncClient() as client:
        response = await client.get(url, auth=auth_credentials)
        response.raise_for_status()
        data = response.json()
        return data


async def fetch_logs(since: datetime | None = None) -> list[dict]:
    url = f"{settings.autochecker_api_url}/api/logs"
    auth_credentials = (settings.autochecker_email, settings.autochecker_password)
    all_logs = []
    
    async with httpx.AsyncClient() as client:
        while True:
            params = {"limit": 500}
            
            if since is not None:
                if isinstance(since, datetime):
                    params["since"] = since.isoformat()
                else:
                    params["since"] = since

            response = await client.get(url, auth=auth_credentials, params=params)
            response.raise_for_status()
            
            data = response.json()
            logs_batch = data["logs"]
            
            all_logs.extend(logs_batch)

            if data["has_more"] is False:
                break
            
            last_log_in_batch = logs_batch[-1]
            since = last_log_in_batch["submitted_at"]

    return all_logs

async def load_items(items: list[dict], session: AsyncSession) -> int:
    new_items_count = 0
    
    # Создаем пустой словарь для связи: "короткое имя лабы" -> "объект из БД"
    lab_mapping = {} 

    # --- ШАГ 1: Обрабатываем лабораторные (labs) ---
    for item_data in items:
        if item_data["type"] == "lab":
            lab_short_id = item_data["lab"]
            lab_title = item_data["title"]

            query = select(ItemRecord).where(
                ItemRecord.type == "lab", 
                ItemRecord.title == lab_title
            )
            result = await session.exec(query)
            db_lab = result.first()

            if not db_lab:
                db_lab = ItemRecord(type="lab", title=lab_title)
                session.add(db_lab)
                new_items_count += 1
                await session.flush()

            lab_mapping[lab_short_id] = db_lab

    # --- ШАГ 2: Обрабатываем задачи (tasks) ---
    for item_data in items:
        if item_data["type"] == "task":
            lab_short_id = item_data["lab"]
            task_title = item_data["title"]
            
            parent_lab = lab_mapping.get(lab_short_id)
            if not parent_lab:
                continue 

            query = select(ItemRecord).where(
                ItemRecord.type == "task",
                ItemRecord.title == task_title,
                ItemRecord.parent_id == parent_lab.id
            )
            result = await session.exec(query)
            db_task = result.first()

            if not db_task:
                db_task = ItemRecord(
                    type="task", 
                    title=task_title, 
                    parent_id=parent_lab.id
                )
                session.add(db_task)
                new_items_count += 1
                await session.flush()

    # --- ШАГ 3: Финальное сохранение ---
    await session.commit()
    return new_items_count


async def load_logs(logs: list[dict], items_catalog: list[dict], session: AsyncSession) -> int:
    new_interactions_count = 0

    # --- ШАГ 1: Создаем словарь-шпаргалку для поиска названий ---
    item_title_lookup = {}
    for item in items_catalog:
        lab = item.get("lab")
        task = item.get("task")
        title = item["title"]
        item_title_lookup[(lab, task)] = title

    # --- ШАГ 2: Обрабатываем логи ---
    for log in logs:
        # 1. Ищем или создаем студента
        student_ext_id = log["student_id"]
        
        query_learner = select(Learner).where(Learner.external_id == student_ext_id)
        result_learner = await session.exec(query_learner)
        learner = result_learner.first()

        if not learner:
            learner = Learner(
                external_id=student_ext_id, 
                student_group=log.get("group")
            )
            session.add(learner)
            await session.flush() 

        # 2. Ищем предмет в базе
        lab_short = log.get("lab")
        task_short = log.get("task")
        
        item_title = item_title_lookup.get((lab_short, task_short))
        if not item_title:
            continue 

        query_item = select(ItemRecord).where(ItemRecord.title == item_title)
        result_item = await session.exec(query_item)
        item_record = result_item.first()

        if not item_record:
            continue

        # 3. Проверка на дубликаты
        log_ext_id = log["id"] 
        
        query_log = select(InteractionLog).where(InteractionLog.external_id == log_ext_id)
        result_log = await session.exec(query_log)
        existing_log = result_log.first()

        if existing_log:
            continue

        # 4. Создаем новую запись InteractionLog
        date_str = log["submitted_at"].replace("Z", "+00:00") 
        parsed_date = datetime.fromisoformat(date_str)

        new_interaction = InteractionLog(
            external_id=log_ext_id,
            learner_id=learner.id,
            item_id=item_record.id,
            kind="attempt",
            score=log.get("score"),
            checks_passed=log.get("passed"),
            checks_total=log.get("total"),
            created_at=parsed_date
        )
        
        session.add(new_interaction)
        new_interactions_count += 1

    # --- ШАГ 3: Финальное сохранение ---
    await session.commit()
    return new_interactions_count


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

async def sync(session: AsyncSession) -> dict:
    # --- ШАГ 1: Обновляем каталог ---
    raw_items = await fetch_items()
    await load_items(raw_items, session)

    # --- ШАГ 2: Ищем дату последнего лога ---
    query_last_date = select(func.max(InteractionLog.created_at))
    result_date = await session.exec(query_last_date)
    last_sync_date = result_date.first() 

    # --- ШАГ 3: Скачиваем новые логи ---
    raw_logs = await fetch_logs(since=last_sync_date)

    # --- ШАГ 4: Загружаем новые логи в базу ---
    new_records_count = await load_logs(raw_logs, raw_items, session)

    # --- ШАГ 5: Собираем статистику для отчета ---
    query_total = select(func.count(InteractionLog.id))
    result_total = await session.exec(query_total)
    total_records_count = result_total.first()

    return {
        "new_records": new_records_count,
        "total_records": total_records_count or 0
    }