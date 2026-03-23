from pydantic import BaseModel


class AccountCreate(BaseModel):
    username: str
    password: str


class LoginData(BaseModel):
    username: str
    password: str


class DepositRequest(BaseModel):
    amount: float


class WithdrawRequest(BaseModel):
    amount: float
