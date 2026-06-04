from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.models.analysis import Analysis


class AnalysisRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, analysis: Analysis) -> Analysis:
        self.session.add(analysis)
        await self.session.flush()
        return analysis

    async def find_by_offer(self, job_offer_id: int) -> Analysis | None:
        stmt = select(Analysis).where(Analysis.job_offer_id == job_offer_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_top_scores(self, limit: int = 10) -> list[Analysis]:
        stmt = select(Analysis).order_by(Analysis.score.desc()).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
