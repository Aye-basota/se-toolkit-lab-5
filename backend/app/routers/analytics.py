
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import select, func, case, col
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
# Прямые импорты из файлов твоих моделей
from app.models.item import ItemRecord
from app.models.interaction import InteractionLog
from app.models.learner import Learner

router = APIRouter()

async def get_lab_id(lab: str, session: AsyncSession) -> int:
    """Вспомогательная функция для поиска ID лабораторной по параметру 'lab'."""
    lab_title = lab.replace("-", " ").title()
    statement = select(ItemRecord.id).where(
        col(ItemRecord.title).contains(lab_title),
        ItemRecord.parent_id == None
    )
    result = await session.exec(statement)
    lab_id = result.first()
    
    if not lab_id:
        raise HTTPException(status_code=404, detail=f"Lab '{lab}' not found")
    return lab_id


@router.get("/scores")
async def get_scores(
    lab: str = Query(..., description="Lab identifier, e.g. 'lab-01'"),
    session: AsyncSession = Depends(get_session),
):
    """Score distribution histogram for a given lab."""
    lab_id = await get_lab_id(lab, session)
    
    # Распределяем оценки по 4 корзинам
    bucket_expr = case(
        (InteractionLog.score <= 25, "0-25"),
        (InteractionLog.score <= 50, "26-50"),
        (InteractionLog.score <= 75, "51-75"),
        else_="76-100"
    ).label("bucket")

    statement = (
        select(bucket_expr, func.count(InteractionLog.id).label("count"))
        .join(ItemRecord, InteractionLog.item_id == ItemRecord.id)
        .where(ItemRecord.parent_id == lab_id)
        .where(InteractionLog.score.isnot(None))
        .group_by("bucket")
    )
    
    results = await session.exec(statement)
    stats = {row.bucket: row.count for row in results}
    
    # Возвращаем все 4 корзины, даже если результат 0
    return [
        {"bucket": b, "count": stats.get(b, 0)} 
        for b in ["0-25", "26-50", "51-75", "76-100"]
    ]


@router.get("/pass-rates")
async def get_pass_rates(
    lab: str = Query(..., description="Lab identifier, e.g. 'lab-01'"),
    session: AsyncSession = Depends(get_session),
):
    """Per-task pass rates for a given lab."""
    lab_id = await get_lab_id(lab, session)
    
    statement = (
        select(
            ItemRecord.title.label("task"),
            func.round(func.avg(InteractionLog.score), 1).label("avg_score"),
            func.count(InteractionLog.id).label("attempts")
        )
        .join(InteractionLog, ItemRecord.id == InteractionLog.item_id)
        .where(ItemRecord.parent_id == lab_id)
        .group_by(ItemRecord.id, ItemRecord.title)
        .order_by(ItemRecord.title)
    )
    
    results = await session.exec(statement)
    return [
        {
            "task": row.task,
            "avg_score": float(row.avg_score) if row.avg_score is not None else 0.0,
            "attempts": row.attempts
        } 
        for row in results
    ]


@router.get("/timeline")
async def get_timeline(
    lab: str = Query(..., description="Lab identifier, e.g. 'lab-01'"),
    session: AsyncSession = Depends(get_session),
):
    """Submissions per day for a given lab."""
    lab_id = await get_lab_id(lab, session)
    
    statement = (
        select(
            func.date(InteractionLog.created_at).label("date"),
            func.count(InteractionLog.id).label("submissions")
        )
        .join(ItemRecord, InteractionLog.item_id == ItemRecord.id)
        .where(ItemRecord.parent_id == lab_id)
        .group_by(func.date(InteractionLog.created_at))
        .order_by(func.date(InteractionLog.created_at))
    )
    
    results = await session.exec(statement)
    return [
        {"date": str(row.date), "submissions": row.submissions} 
        for row in results
    ]


@router.get("/groups")
async def get_groups(
    lab: str = Query(..., description="Lab identifier, e.g. 'lab-01'"),
    session: AsyncSession = Depends(get_session),
):
    """Per-group performance for a given lab."""
    lab_id = await get_lab_id(lab, session)
    
    statement = (
        select(
            Learner.student_group.label("group"),
            func.round(func.avg(InteractionLog.score), 1).label("avg_score"),
            func.count(func.distinct(InteractionLog.learner_id)).label("students")
        )
        .join(InteractionLog, Learner.id == InteractionLog.learner_id)
        .join(ItemRecord, InteractionLog.item_id == ItemRecord.id)
        .where(ItemRecord.parent_id == lab_id)
        .group_by(Learner.student_group)
        .order_by(Learner.student_group)
    )
    
    results = await session.exec(statement)
    return [
        {
            "group": row.group,
            "avg_score": float(row.avg_score) if row.avg_score is not None else 0.0,
            "students": row.students
        } 
        for row in results
    ]