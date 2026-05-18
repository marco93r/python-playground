from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session
import bcrypt
from jose import jwt

engine = create_engine('sqlite:///movie-api.db')

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    genre = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))

class UserLogin(BaseModel):
    username: str
    password: str

class MovieInput(BaseModel):
    title: str
    genre: str

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
        return {"message": "user " + user.username + " registered"}
    
@app.post('/login')
def login(body: UserLogin):
    with Session(engine) as session:
        user = session.query(User).filter(User.username == body.username).first()

        if not user or not bcrypt.checkpw(body.password.encode(), user.password if isinstance(user.password, bytes) else user.password.encode()):
            raise HTTPException(status_code=401, detail="unauthorized")
        
        token = jwt.encode({"sub": user.username}, SECRET_KEY, algorithm="HS256")
        return {"access_token": token}
    
@app.get('/movies')
def get_movies():
    with Session(engine) as session:
        movies = session.query(Movie).all()
        return [{"id": m.id, "title": m.title, "genre": m.genre, "owner_id": m.owner_id} for m in movies]
    
@app.post('/movies')
def post_movies(body: MovieInput, current_user_id: int = Depends(get_current_user)):
    with Session(engine) as session:
        movie = Movie(title=body.title, genre=body.genre, owner_id=current_user_id)
        session.add(movie)
        session.commit()
        session.refresh(movie)
        return {"id": movie.id, "title": movie.title, "genre": movie.genre}
    
@app.delete('/movies/{id}')
def delete_movies(id: int, current_user_id: int = Depends(get_current_user)):
    with Session(engine) as session:
        movie = session.query(Movie).filter(Movie.id == id).first()
        if not movie:
            raise HTTPException(status_code=404, detail="not found")
        elif movie.owner_id == current_user_id:
            session.delete(movie)
            session.commit()
            return {"message": "deleted"}
        else:
            raise HTTPException(status_code=403, detail="forbidden")