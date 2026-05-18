from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, Session
import bcrypt
from jose import jwt

engine = create_engine('sqlite:///book-library.db')

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    read = Column(Boolean)
    rating = Column(Integer)
    owner_id = Column(Integer, ForeignKey('users.id'))

class UserLogin(BaseModel):
    username: str
    password: str

class BookInput(BaseModel):
    title: str
    author: str
    read: bool = False

if __name__ == "__app__":
    Base.metadata.create_all(engine)

app = FastAPI()

SECRET_KEY = "test-secret"

def get_current_user(authorization: str = Header(None)):
    token = authorization.replace("Bearer ", "")
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    username = payload["sub"]
    with Session(engine) as session:
        user = session.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=401, detail="unauthorized")
        return user.id

@app.post('/register')
def register(body: UserLogin):
    with Session(engine) as session:

        existing = session.query(User).filter(User.username == body.username).first()
        if existing:
            raise HTTPException(status_code=400, detail="username already taken")
        
        hashed = bcrypt.hashpw(body.password.encode(), bcrypt.gensalt())

        user = User(username=body.username, password=hashed)
        session.add(user)
        session.commit()
        return {"message": "user registered"}
    
@app.post('/login')
def login(body: UserLogin):
    with Session(engine) as session:
        user = session.query(User).filter(User.username == body.username).first()

        if not user or not bcrypt.checkpw(body.password.encode(), user.password if isinstance(user.password, bytes) else user.password.encode()):
            raise HTTPException(status_code=401, detail="unauthorized")
        
        token = jwt.encode({"sub": user.username}, SECRET_KEY, algorithm="HS256")
        return {"access_token": token}
    
@app.get('/books')
def get_books():
    with Session(engine) as session:
        books = session.query(Book).all()
        return [{
            "id": b.id,
            "title": b.title,
            "author": b.author,
            "read": b.read,
            "owner_id": b.owner_id
            } for b in books]
    
@app.post('/books', status_code=201)
def post_books(body: BookInput, current_user_id: int = Depends(get_current_user)):
    with Session(engine) as session:
        book = Book(title=body.title, author=body.author, read=body.read, owner_id=current_user_id)
        session.add(book)
        session.commit()
        session.refresh(book)
        return {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "read": book.read
        }
    
@app.delete('/books/{id}')
def delete_books(id:int, current_user_id: int = Depends(get_current_user)):
    with Session(engine) as session:
        book = session.query(Book).filter(Book.id == id).first()
        if not book:
            raise HTTPException(status_code=404, detail="not found")
        elif book.owner_id == current_user_id:
            session.delete(book)
            session.commit()
            return {"message": "deleted"}
        else:
            raise HTTPException(status_code=403, detail="forbidden")
        
@app.put('/books/{id}')
def put_books(id:int, current_user_id: int = Depends(get_current_user)):
    with Session(engine) as session:
        book = session.query(Book).filter(Book.id == id).first()
        if not book:
            raise HTTPException(status_code=404, detail="not found")
        elif book.owner_id == current_user_id:
            book.read = True
            session.commit()
            return {"message": "updated"}
        else:
            raise HTTPException(status_code=403, detail="forbidden")
        
@app.get('/books/unread')
def get_unread_books():
    with Session(engine) as session:
        books = session.query(Book).filter(Book.read == False).all()
        return [{
            "id": b.id,
            "title": b.title,
            "author": b.author,
            "read": b.read,
            "owner_id": b.owner_id
            } for b in books]
    