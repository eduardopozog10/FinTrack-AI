from sqlmodel import SQLModel


class UserRegister(SQLModel):
    full_name: str
    email: str
    password: str


class UserLogin(SQLModel):
    email: str
    password: str


class UserRead(SQLModel):
    id: int
    full_name: str
    email: str


class Token(SQLModel):
    access_token: str
    token_type: str