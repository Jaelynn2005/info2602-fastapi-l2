import typer
from app.database import create_db_and_tables, get_session, drop_all
from app.models import User
from fastapi import Depends
from sqlmodel import select
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

cli = typer.Typer()

@cli.command(help="Initialize the database with some data")
def initialize():
    with get_session() as db: # Get a connection to the database
        drop_all() # delete all tables
        create_db_and_tables() #recreate all tables
        bob = User(username='bob', email='bob@mail.com', password='bobpass') # Create a new user (in memory)
        db.add(bob) # Tell the database about this new data
        db.commit() # Tell the database persist the data
        db.refresh(bob) # Update the user (we use this to get the ID from the db)
        print("Database Initialized")

#retrieving a user by their username and printing it
@cli.command(help="Get a user by their username")
def get_user(username:str): #takes the username argument
    with get_session() as db:
        user = db.exec(select(User).where(User.username==username)).all()
        if not user:
            print(f'{username} not found')
            return
        print(user)

#retrieving all users in the db
@cli.command(help="Get all users in the database")
def get_all_users():
    with get_session() as db:
        all_users = db.exec(select(User)).all()
        if not all_users:
            print("Users not found")
        else:
            for user in all_users: #using a for loop to print each user one by one.
                print(user)

#updating user bob's email
@cli.command(help="Change a user's email")
def change_email(username: str, new_email:str):
    with get_session() as db:
        user = db.exec(select(User).where(User.username==username)).first()
        if not user:
            print(f'{username} not found. Failed to update email')
            return
        user.email = new_email
        db.add(user)
        db.commit()
        print(f"Updated {user.username}'s email to {user.email}")

#creating a new user
@cli.command(help="Create a new user")
def create_user(username: str, email:str, password: str):
    with get_session() as db:
        newuser = User(username=username, email=email, password=password)
        try: #contains the block that can throw an error
            db.add(newuser)
            db.commit()
        except IntegrityError as e: #states what error to look out for
            db.rollback() #the database can undo any erroneous operations and execute further queries.
            print("Username or email already taken.")
        else: #runs the code if the error do not occur.
            print(newuser)
#jacklyn and ronny was created
#jacklyn, jacklyn@yahoo.com, jacky
#ronny, ronny123@gmail.com, ronron45

#deleting a user
@cli.command(help="Delete a user by their username")
def delete_user(username: str):
    with get_session() as db:
        user = db.exec(select(User).where(User.username==username)).first()
        if not user:
            print(f'{username} not found. Failed to delete user')
            return
        db.delete(user)
        db.commit()
        print(f'{username} deleted.')
#jacklyn was deleted

#exercises
#ex1
@cli.command(help="Get a user by their username or email")
def get_user(username: str, email:str):
    with get_session() as db:
        user = db.exec(select(User).where(or_(User.username.ilike(f"%{username}%"),(User.email.ilike(f"%{email}%"))))).first()
        if not user:
            print("User not found")
        else:
            print(user)

#ex2
@cli.command(help="Get a list of users with pagination")
def get_user(limit: int=10, offset: int=0):
    with get_session() as db:
        user = db.exec(select(User).offset(offset).limit(limit)).all()
        if not user:
            print("Users not found")
        else:
            print(user)


if __name__ == "__main__":
    cli()