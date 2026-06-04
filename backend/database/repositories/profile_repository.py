from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.models.profile import Profile


class ProfileRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, profile: Profile) -> Profile:
        self.session.add(profile)
        await self.session.flush()
        return profile

    async def find_by_user(self, user_id: int) -> Profile | None:
        stmt = select(Profile).where(Profile.user_id == user_id).order_by(Profile.id.desc())
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, profile: Profile) -> Profile:
        await self.session.merge(profile)
        await self.session.flush()
        return profile
