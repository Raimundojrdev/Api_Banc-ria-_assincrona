from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database.connection import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(
        Integer,
        primary_key=True,
    )
    type = Column(String)
    amount = Column(Float)
    account_id = Column(Integer, ForeignKey("accounts.id"))
