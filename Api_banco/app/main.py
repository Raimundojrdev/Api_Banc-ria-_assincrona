from fastapi import FastAPI
from app.database.connection import Base, engine
from app.models import accounts, transaction
from app.routes import auth


Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Bancária")

app.include_router(auth.router, prefix="/auth")


@app.get("/")
def home():
    return {"message": "API rodando"}
