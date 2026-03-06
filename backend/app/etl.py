from datetime import datetime
from app.models.learner import Learner
from app.models.interaction import InteractionLog
from sqlmodel import select, func
from app.models.item import ItemRecord 
import httpx

from datetime import datetime

from sqlmodel.ext.asyncio.session import AsyncSession

from app.settings import settings


# ---------------------------------------------------------------------------
# Extract — fetch data from the autochecker API
# ---------------------------------------------------------------------------


async def fetch_items() -> list[dict]:
  url = f"{settings.autochecker_api_url}/api/items"
  auth_credentials = (settings.autochecker_email, settings.autochecker_password)


  async with httpx.AsyncClient() as client:
    respone = await client.get(url, auth = auth_credentials)
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

# ---------------------------------------------------------------------------
# Load — insert fetched data into the local database
# ---------------------------------------------------------------------------


async def load_items(items: list[dict], session: AsyncSession) -> int:
    new_items_count = 0
    
    # Создаем пустой словарь. В нем мы будем хранить связь:
    # "короткое имя лабы из API" -> "готовый объект лабы из базы данных"
    # Например: {"lab-01": <ItemRecord id=5 title="Первая лаба">}
    lab_mapping = {} 

    # --- ШАГ 1: Обрабатываем лабораторные (labs) ---
    for item_data in items:
        if item_data["type"] == "lab":
            lab_short_id = item_data["lab"]
            lab_title = item_data["title"]

            # Ищем, нет ли уже такой лабы в нашей базе (чтобы не создавать дубликаты)
            # select(...) - это SQL-запрос: SELECT * FROM itemrecord WHERE type='lab' AND title='...'
            query = select(ItemRecord).where(
                ItemRecord.type == "lab", 
                ItemRecord.title == lab_title
            )
            result = await session.exec(query)
            db_lab = result.first() # Берем первое совпадение или None

            # Если такой лабы еще нет - создаем!
            if not db_lab:
                db_lab = ItemRecord(type="lab", title=lab_title)
                session.add(db_lab) # Добавляем в сессию
                new_items_count += 1
                
                # ВАЖНО: flush отправляет данные в БД, чтобы база выдала нашей лабе уникальный ID.
                # Но это еще не финальное сохранение (commit)!
                await session.flush()

            # Обязательно сохраняем лабу в наш словарь-шпаргалку для второго шага
            lab_mapping[lab_short_id] = db_lab

    # --- ШАГ 2: Обрабатываем задачи (tasks) ---
    for item_data in items:
        if item_data["type"] == "task":
            lab_short_id = item_data["lab"]
            task_title = item_data["title"]
            
            # Достаем родительскую лабу из нашего словаря-шпаргалки
            parent_lab = lab_mapping.get(lab_short_id)
            if not parent_lab:
                continue # Если родителя почему-то нет, просто пропускаем эту задачу

            # Снова ищем в базе: есть ли уже такая задача у этой лабы?
            query = select(ItemRecord).where(
                ItemRecord.type == "task",
                ItemRecord.title == task_title,
                ItemRecord.parent_id == parent_lab.id # Указываем ID родителя!
            )
            result = await session.exec(query)
            db_task = result.first()

            # Если задачи нет - создаем
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
    # Только сейчас все наши изменения реально записываются на жесткий диск базы данных.
    await session.commit()

    # Возвращаем количество созданных записей, как просили в задании
    return new_items_count
async def load_logs(
    logs: list[dict], items_catalog: list[dict], session: AsyncSession
) -> int:
    new_interactions_count = 0

    # --- ШАГ 1: Создаем словарь-шпаргалку для поиска названий ---
    # В логах есть только короткие имена (например, lab="lab-01", task="setup").
    # А в базе данных предметы лежат по их полному названию (title).
    # Делаем словарь, где ключ — это кортеж (lab, task), а значение — title.
    item_title_lookup = {}
    for item in items_catalog:
        lab = item.get("lab")
        task = item.get("task") # У лабораторных это поле будет None
        title = item["title"]
        item_title_lookup[(lab, task)] = title

    # --- ШАГ 2: Обрабатываем логи ---
    for log in logs:
        # 1. Ищем или создаем студента (Learner)
        student_ext_id = log["student_id"]
        
        query_learner = select(Learner).where(Learner.external_id == student_ext_id)
        result_learner = await session.exec(query_learner)
        learner = result_learner.first()

        # Если студента нет в базе — создаем его
        if not learner:
            learner = Learner(
                external_id=student_ext_id, 
                student_group=log.get("group")
            )
            session.add(learner)
            await session.flush() # Сразу получаем ID для студента

        # 2. Ищем предмет (ItemRecord) в базе
        lab_short = log.get("lab")
        task_short = log.get("task")
        
        # Достаем полное название из нашей шпаргалки
        item_title = item_title_lookup.get((lab_short, task_short))
        
        # Если в каталоге такого предмета не было, пропускаем лог
        if not item_title:
            continue 

        # Ищем предмет в БД по названию
        query_item = select(ItemRecord).where(ItemRecord.title == item_title)
        result_item = await session.exec(query_item)
        item_record = result_item.first()

        # Если в базе предмета нет (хотя должен быть после load_items), пропускаем
        if not item_record:
            continue

        # 3. Проверка на дубликаты (идемпотентность)
        log_ext_id = log["id"] # Уникальный ID самого лога из API
        
        query_log = select(InteractionLog).where(InteractionLog.external_id == log_ext_id)
        result_log = await session.exec(query_log)
        existing_log = result_log.first()

        # Если такой лог уже загружали ранее — просто пропускаем его
        if existing_log:
            continue

        # 4. Создаем новую запись InteractionLog
        # API присылает дату как строку ("2026-03-06T10:19:49Z"), 
        # а базе нужен объект datetime. Превращаем строку в дату:
        date_str = log["submitted_at"].replace("Z", "+00:00") # Заменяем Z для совместимости
        parsed_date = datetime.fromisoformat(date_str)

        new_interaction = InteractionLog(
            external_id=log_ext_id,
            learner_id=learner.id,     # Связываем с ID студента
            item_id=item_record.id,    # Связываем с ID задачи/лабы
            kind="attempt",
            score=log.get("score"),
            checks_passed=log.get("passed"),
            checks_total=log.get("total"),
            created_at=parsed_date     # Наша распарсенная дата
        )
        
        session.add(new_interaction)
        new_interactions_count += 1
        
        # Здесь можно делать flush, а можно и не делать, так как 
        # ID этого лога нам дальше в цикле не нужен. 
        # Достаточно просто добавить в сессию.

    # --- ШАГ 3: Финальное сохранение ---
    # Отправляем все новые логи и новых студентов в базу данных одним махом
    await session.commit()

    return new_interactions_count
# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


async def sync(session: AsyncSession) -> dict:
    # --- ШАГ 1: Обновляем каталог ---
    # Сначала скачиваем сырой каталог (список словарей) из интернета
    raw_items = await fetch_items()
    
    # Сразу загружаем/обновляем его в базе данных.
    # Результат (количество новых) нам тут не особо важен, поэтому не сохраняем его в переменную.
    await load_items(raw_items, session)

    # --- ШАГ 2: Ищем дату последнего лога ---
    # func.max() — это агрегатная функция SQL. Она просматривает всю колонку created_at 
    # и возвращает самое большое значение (то есть самую позднюю дату).
    query_last_date = select(func.max(InteractionLog.created_at))
    result_date = await session.exec(query_last_date)
    last_sync_date = result_date.first() 
    # Если таблица пустая (первый запуск), last_sync_date будет равен None.
    # Это идеально, потому что наш fetch_logs(since=None) тогда скачает всё с самого начала.

    # --- ШАГ 3: Скачиваем новые логи ---
    # Передаем найденную дату в API. Получаем сырой список только новых логов.
    raw_logs = await fetch_logs(since=last_sync_date)

    # --- ШАГ 4: Загружаем новые логи в базу ---
    # Передаем сырые логи и сырой каталог (чтобы внутри load_logs работала шпаргалка по названиям)
    new_records_count = await load_logs(raw_logs, raw_items, session)

    # --- ШАГ 5: Собираем статистику для отчета ---
    # func.count() — еще одна агрегатная функция SQL. Она просто считает количество строк (id).
    query_total = select(func.count(InteractionLog.id))
    result_total = await session.exec(query_total)
    total_records_count = result_total.first()

    # Возвращаем красивый словарь с итогами работы, как просили в задании
    return {
        "new_records": new_records_count,
        "total_records": total_records_count or 0 # or 0 на случай, если база вообще пустая
    }