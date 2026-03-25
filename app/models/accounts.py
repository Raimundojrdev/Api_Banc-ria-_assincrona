from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Numeric
from app.database.connection import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(50), unique=True, nullable=False, index=True)

    password = Column(String(255), nullable=False)

    balance = Column(Numeric(10, 2), default=0, nullable=False)

    transactions = relationship(
        "Transaction",
        back_populates="account",
        cascade="all, delete-orphan"
    )
