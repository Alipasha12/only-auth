from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.user import UserCreate
from sqlalchemy import select
from ..model.model import User
from sqlalchemy.exc import IntegrityError
from ..core.security import get_password_hash

class UserService():
    def __init__(self,db: AsyncSession):
        self.db: AsyncSession = db
    
    async def get_user_by_username(self, user_name: str) -> User | None:
            stmt = select(User).where(User.user_name == user_name)
            result = await self.db.execute(stmt)
            return result.scalars().first()

    async def get_user_by_email(self,email:str) -> User:
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()
    
    async def create_user(self,user_input : UserCreate):
        existing_user_by_username= await self.get_user_by_username(user_input.user_name)
        if existing_user_by_username:
            raise ValueError(f"user with this {user_input.user_name} is already exist!")
        existing_user_by_email= await self.get_user_by_email(user_input.email)
        if existing_user_by_email:
            raise ValueError(f"user with this {user_input.email} is already exist!")
        
        hashed_password = get_password_hash(user_input.password)
        user_input.password = hashed_password
        
        user_model = User(**user_input.model_dump())
        self.db.add(user_model)
        
        try:
            await self.db.commit()
            await self.db.refresh(user_model)
        except IntegrityError:
            await self.db.rollback()
            raise ValueError("username or email is already registered!")
        return user_model
        