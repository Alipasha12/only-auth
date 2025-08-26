from fastapi import FastAPI,Depends
from contextlib import asynccontextmanager
from .database.database import engine,Base,get_db
from .model.model import User
from .services.user import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas.user import UserCreate,Userlogin
from app.services.auth import AuthService

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:

        table_exists = await conn.run_sync(
            lambda sync_conn: engine.dialect.has_table(sync_conn, User.__tablename__)
        )
        if not table_exists:
            await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app=FastAPI(debug=True,lifespan=lifespan)

@app.get("/")
def welcome():
    return "hello"

@app.post("/register")
async def register(user_input : UserCreate, db : AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    await user_service.create_user(user_input)
    return "created"

@app.post("/login")
async def login(user_input: Userlogin , db : AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    result = await auth_service.login_by_email_or_username_and_password(user_input.email_or_username,user_input.password)
    return result