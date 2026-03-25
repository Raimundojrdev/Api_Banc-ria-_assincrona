from sqlalchemy import Column, Integer, Numeric, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.database.connection import Base


class TransactionType(enum.Enum):
    deposit = "deposit"
    withdraw = "withdraw"
    transfer_in = "transfer_in"
    transfer_out = "transfer_out"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    type = Column(Enum(TransactionType), nullable=False)

    amount = Column(Numeric(10, 2), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    account_id = Column(
        Integer,
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    account = relationship("Account", back_populates="transactions")
