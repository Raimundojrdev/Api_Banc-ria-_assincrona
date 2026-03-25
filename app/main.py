from fastapi import FastAPI
from app.database.connection import engine
from app.database.connection import Base
from app.models.accounts import Account
from app.models.transaction import Transaction
from app.routes import auth

app = FastAPI(title="API Bancária")


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def on_startup():
    await create_tables()


app.include_router(auth.router)
