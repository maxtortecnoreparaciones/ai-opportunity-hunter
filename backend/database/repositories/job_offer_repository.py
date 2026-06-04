from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.models.job_offer import JobOffer


class JobOfferRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, offer: JobOffer) -> JobOffer:
        existing = await self.find_by_link(offer.link)
        if existing:
            return existing
        self.session.add(offer)
        await self.session.flush()
        return offer

    async def find_by_link(self, link: str) -> JobOffer | None:
        stmt = select(JobOffer).where(JobOffer.link == link)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_all(self) -> list[JobOffer]:
        stmt = select(JobOffer).order_by(JobOffer.encontrado_en.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def find_unanalyzed(self) -> list[JobOffer]:
        stmt = (
            select(JobOffer)
            .outerjoin("analyses")
            .where(JobOffer.id.notin_(select(JobOffer.id).join("analyses")))
            .order_by(JobOffer.encontrado_en.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def delete_all(self) -> int:
        stmt = delete(JobOffer)
        result = await self.session.execute(stmt)
        return result.rowcount
