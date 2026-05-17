import sqlite3, bcrypt
from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

def init_db():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT NOT NULL,
            seen BOOLEAN DEFAULT FALSE,
            added_by TEXT NOT NULL
        )
        ''')
    conn.commit()
    conn.close()

init_db()

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "test-secret"
jwt = JWTManager(app)

@app.route('/register', methods = ['POST'])
def register():
    payload = request.json
    if "username" in payload and "password" in payload:
        username = payload.get("username")
        password = payload.get("password")
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        conn = sqlite3.connect('movies.db')
        cursor = conn.cursor()
        cursor.execute('SELECT username FROM users WHERE username = ?', [username])
        row = cursor.fetchone()
        if row:
            conn.close()
            return {"error": "username already taken"}, 400
        else:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed))
            conn.commit()
            conn.close()
            return {"message": "user " + username + " created"}, 200
    else:
        return {"error": "username and password required"}, 400
    
@app.route('/login', methods = ['POST'])
def login():
    payload = request.json
    username = payload.get("username")
    password = payload.get("password")
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, password FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()
    conn.close()
    if row and bcrypt.checkpw(password.encode(), row[1] if isinstance(row[1], bytes) else row[1].encode()):
        access_token = create_access_token(identity=username)
        return {"access_token": access_token}, 200
    else:
        return {"error": "unauthorized"}, 401

@app.route('/movies', methods = ["GET"])
def get_movies():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM movies')
    rows = cursor.fetchall()
    conn.close()

    movies = []

    for row in rows:
        movies.append({
            "id": row[0],
            "title": row[1],
            "genre": row[2],
            "seen": bool(row[3]),
            "added_by": row[4]
        })
    
    return movies, 200

@app.route('/movies', methods = ['POST'])
@jwt_required()
def post_movies():
    payload = request.json
    if "title" in payload and "genre" in payload:
        title = payload["title"]
        genre = payload["genre"]
        added_by = get_jwt_identity()
        conn = sqlite3.connect('movies.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO movies (title, genre, added_by) VALUES (?, ?, ?)', (title, genre, added_by))
        conn.commit()

        movie = {
            "id": cursor.lastrowid,
            "title": title,
            "genre": genre,
            "seen": False,
            "added_by": added_by
        }

        conn.close()
        return movie, 201
    else:
        return {"error": "required field missing"}, 400
    
@app.route('/movies/<int:id>', methods = ["DELETE"])
@jwt_required()
def delete_movies(id):
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM movies WHERE id = ?', [id])
    row = cursor.fetchone()
    if row:
        cursor.execute('DELETE FROM movies WHERE id = ?', [id])
        conn.commit()
        conn.close()
        return {"message": "deleted"}, 200
    else:
        return {"error": "id not found"}, 404
    
@app.route('/movies/<int:id>', methods = ["PUT"])
@jwt_required()
def put_movies(id):
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM movies WHERE id = ?', [id])
    row = cursor.fetchone()
    if row:
        cursor.execute('UPDATE movies SET seen = true WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return {"message": "updated"}, 200
    else:
        return {"error": "id not found"}, 404
    
@app.route('/movies/unseen', methods = ["GET"])
def get_unseen_movies():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM movies WHERE seen = false')
    rows = cursor.fetchall()
    conn.close()
    movies = []
    for row in rows:
        movies.append({
            "id": row[0],
            "title": row[1],
            "genre": row[2],
            "seen": bool(row[3]),
            "added_by": row[4]
        })
    
    return movies, 200

@app.route('/movies/stats', methods = ["GET"])
def get_stats():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            COUNT(*) as total,
            SUM(seen) as seen,
            SUM(NOT seen) as unseen
            FROM movies
        ''')
    row = cursor.fetchone()
    return {"total": row[0], "seen": row[1], "unseen": row[2]}
        
if __name__ == '__main__':
    app.run(debug=True)