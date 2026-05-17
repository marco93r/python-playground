from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase, Session

engine = create_engine('sqlite:///todos.db')

class Base(DeclarativeBase):
    pass

class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    done = Column(Boolean, default=False)

Base.metadata.create_all(engine)

class TodoInput(BaseModel):
    title: str

app = FastAPI()

@app.get('/todos')
def get_todos():
    with Session(engine) as session:
        todos = session.query(Todo).all()
        return [{"id": t.id, "title": t.title, "done": t.done} for t in todos]
    
@app.post('/todos', status_code=201)
def post_todos(body: TodoInput):
    with Session(engine) as session:
        todo = Todo(title=body.title, done=False)
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return {"id": todo.id, "title": todo.title, "done": todo.done}

@app.put('/todos/{id}')
def put_todos(id: int):
    with Session(engine) as session:
        todo = session.query(Todo).filter(Todo.id == id).first()
        if not todo:
            raise HTTPException(status_code=404, detail="not found")
        else:
            todo.done = True
            session.commit()
            session.refresh(todo)
            return {"id": todo.id, "title": todo.title, "done": todo.done}
        
@app.delete('/todos/{id}')
def delete_todos(id: int):
    with Session(engine) as session:
        todo = session.query(Todo).filter(Todo.id == id).first()
        if not todo:
            raise HTTPException(status_code=404, detail="not found")
        else:
            session.delete(todo)
            session.commit()
            return {"message": "deleted"}