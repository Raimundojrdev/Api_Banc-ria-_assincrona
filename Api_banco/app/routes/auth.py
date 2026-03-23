from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.models.accounts import Account
from app.models.transaction import Transaction
from app.schemas.account import AccountCreate, LoginData, DepositRequest, WithdrawRequest
from app.core.security import hash_password, verify_password, create_token, get_current_user


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_account_by_username(db: Session, username: str):
    return db.query(Account).filter(Account.username == username).first()


@router.post("/register")
def register(data: AccountCreate, db: Session = Depends(get_db)):
    existing = db.query(Account).filter(Account.username == data.username).first()
    if existing:
        raise HTTPException(status_code=401, detail="Usuário já existe")

    user = Account(username=data.username, password=hash_password(data.password))
    db.add(user)
    db.commit()
    return {"message": "Usuário registrado com sucesso"}


@router.post("/login")
def login(data: LoginData, db: Session = Depends(get_db)):
    user = db.query(Account).filter(Account.username == data.username).first()

    if not user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Senha incorreta")

    token = create_token(user.username)

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/deposito")
async def deposit(data: DepositRequest, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="O valor do depósito deve ser maior que zero")

    account = get_account_by_username(db, current_user)
    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    account.balance = (account.balance or 0) + data.amount

    transaction = Transaction(type="deposit", amount=data.amount, account_id=account.id)
    db.add(transaction)
    db.add(account)
    db.commit()
    db.refresh(account)
    db.refresh(transaction)

    return {
        "message": "Depósito realizado com sucesso",
        "amount": data.amount,
        "new_balance": account.balance,
        "transaction_id": transaction.id
    }


@router.post("/saque")
async def withdraw(data: WithdrawRequest, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="O valor do saque deve ser maior que zero")

    account = get_account_by_username(db, current_user)
    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    balance = account.balance or 0
    if data.amount > balance:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")

    account.balance = balance - data.amount

    transaction = Transaction(type="withdraw", amount=data.amount, account_id=account.id)
    db.add(transaction)
    db.add(account)
    db.commit()
    db.refresh(account)
    db.refresh(transaction)

    return {
        "message": "Saque realizado com sucesso",
        "amount": data.amount,
        "new_balance": account.balance,
        "transaction_id": transaction.id
    }


@router.get("/extrato")
async def statement(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    account = get_account_by_username(db, current_user)
    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    transactions = db.query(Transaction).filter(Transaction.account_id == account.id).all()

    return {
        "username": account.username,
        "balance": account.balance or 0,
        "transactions": [
            {
                "id": tx.id,
                "type": tx.type,
                "amount": tx.amount,
                "account_id": tx.account_id
            }
            for tx in transactions
        ]
    }
