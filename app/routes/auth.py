from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.connection import get_db
from app.models.accounts import Account
from app.models.transaction import Transaction
from app.schemas.account import AccountCreate, LoginData, DepositRequest, WithdrawRequest
from app.core.security import hash_password, verify_password, create_token, get_current_user
import decimal


router = APIRouter()


# buscar conta
async def get_account_by_username(db: AsyncSession, username: str):
    result = await db.execute(
        select(Account).where(Account.username == username)
    )
    return result.scalar_one_or_none()


# REGISTER
@router.post("/register")
async def register(data: AccountCreate, db: AsyncSession = Depends(get_db)):
    existing = await get_account_by_username(db, data.username)

    if existing:
        raise HTTPException(status_code=409, detail="Usuário já existe")

    user = Account(
        username=data.username,
        password=hash_password(data.password)
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {"message": "Usuário registrado com sucesso"}


# LOGIN
@router.post("/login")
async def login(data: LoginData, db: AsyncSession = Depends(get_db)):
    user = await get_account_by_username(db, data.username)

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Senha incorreta")

    token = create_token(user.username)

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# DEPÓSITO
@router.post("/deposito")
async def deposit(
    data: DepositRequest,
    current_user: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Valor inválido")

    account = await get_account_by_username(db, current_user)

    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    try:
        account.balance = (account.balance or 0) + data.amount

        transaction = Transaction(
            type="deposit",
            amount=data.amount,
            account_id=account.id
        )

        db.add(transaction)

        await db.commit()
        await db.refresh(account)

    except Exception:
        await db.rollback()
        raise

    return {
        "message": "Depósito realizado",
        "new_balance": account.balance
    }


# SAQUE
@router.post("/saque")
async def withdraw(
    data: WithdrawRequest,
    current_user: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Valor inválido")

    account = await get_account_by_username(db, current_user)

    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    balance = account.balance or 0

    if data.amount > balance:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")

    try:
        account.balance = account.balance - decimal.Decimal(str(data.amount))

        transaction = Transaction(
            type="withdraw",
            amount=data.amount,
            account_id=account.id
        )

        db.add(transaction)

        await db.commit()
        await db.refresh(account)

    except Exception:
        await db.rollback()
        raise

    return {
        "message": "Saque realizado",
        "new_balance": account.balance
    }


# EXTRATO
@router.get("/extrato")
async def statement(
    current_user: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    account = await get_account_by_username(db, current_user)

    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    result = await db.execute(
        select(Transaction)
        .where(Transaction.account_id == account.id)
        .order_by(Transaction.id.desc())
    )

    transactions = result.scalars().all()

    return {
        "username": account.username,
        "balance": account.balance or 0,
        "transactions": transactions
    }
