import sqlite3
from flask import Flask, request

def init_db():
    conn = sqlite3.connect('todos.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN DEFAULT FALSE
        )
    ''')
    conn.commit()
    conn.close()

init_db()

app = Flask(__name__)

@app.route('/todos', methods = ['GET'])
def get_todos():
    conn = sqlite3.connect('todos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM todos')
    rows = cursor.fetchall()
    conn.close()

    todos = []

    for row in rows:
        todos.append({
            "id": row[0],
            "title": row[1],
            "done": bool(row[2])
        })

    return todos, 200

@app.route('/todos', methods = ['POST'])
def post_todos():
    payload = request.json
    if "title" in payload:
        title = payload["title"]
        conn = sqlite3.connect('todos.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO todos (title, done) VALUES (?, ?)', (title, False))
        conn.commit()
        conn.close()
        
        todo = {
            "id": cursor.lastrowid,
            "title": title,
            "done": False
        }

        return todo, 201
    else:
        return {"error": "title required"}, 400
    
@app.route('/todos/<int:id>', methods = ['DELETE'])
def delete_todos(id):
    conn = sqlite3.connect('todos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM todos WHERE id = ?', [id])
    row = cursor.fetchone()
    if row:
        cursor.execute('DELETE FROM todos WHERE id = ?', [id])
        conn.commit()
        conn.close()
        return {"message": "deleted"}, 200
    else:
        return {"error": "id not found"}, 404
    
@app.route('/todos/<int:id>', methods = ['PUT'])
def update_todos(id):
    conn = sqlite3.connect('todos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM todos WHERE id = ?', [id])
    row = cursor.fetchone()
    if row:
        cursor.execute('UPDATE todos SET done = TRUE WHERE id = ?', [id])
        conn.commit()
        conn.close()
        return {"message": "updated"}, 200
    else:
        return {"error": "id not found"}, 404

if __name__ == '__main__':
    app.run(debug=True)
