from sqlmodel import Field, SQLModel
from typing import Optional
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

#if we want the class to be a table, specify table=True
#id, username, email, password are fields
#unique=True means the value cannot be repeated in another record
#Optional[int] is a type hint, so the database will provide the ID nd SQLModel understand that it starts as None but becomes a non-null integer.
class User(SQLModel, table=True):
    id: Optional[int] =  Field(default=None, primary_key=True)
    username:str = Field(index=True, unique=True)
    email:str = Field(index=True, unique=True)
    password:str

#the constructor of the USER class, used to make class instance
def __init__(self, username, email, password):
    self.username = username
    self.email = email
    self.set_password(password)

#method defined to hash user passwords
def set_password(self, password):
    self.password = password_hash.hash(password)

#returns a string rep of an instance of the model to the console
def __str__(self) -> str:
    return f"(User id={self.id}, userame={self.username}, email={self.email})"

