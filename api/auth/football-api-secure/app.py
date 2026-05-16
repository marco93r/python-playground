import sqlite3
from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

def init_db():
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            team TEXT NOT NULL,
            goals INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

init_db()

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "test-secret"
jwt = JWTManager(app)

USERS = {
    "admin": "password123"
}

@app.route('/login', methods = ['POST'])
def login():
    payload = request.json
    username = payload.get("username")
    password = payload.get("password")
    if username in USERS and USERS[username] == password:
        access_token = create_access_token(identity=username)
        return access_token, 200
    else:
        return {"error": "user or password incorrect"}, 401

@app.route('/players', methods = ['GET'])
def get_players():
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM players')
    rows = cursor.fetchall()
    conn.close()

    players = []

    for row in rows:
        players.append({
            "id": row[0],
            "name": row[1],
            "team": row[2],
            "goals": row[3]
        })

    return players, 200

@app.route('/players', methods = ['POST'])
@jwt_required()
def post_players():
    payload = request.json
    if "name" in payload and "team" in payload:
        name = payload["name"]
        team = payload["team"]
        goals = 0
        conn = sqlite3.connect('players.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO players (name, team, goals) VALUES (?, ?, ?)', (name, team, goals))
        conn.commit()
        
        player = {
            "id": cursor.lastrowid,
            "name": name,
            "team": team,
            "goals": goals
        }
        
        conn.close()
        return player, 201
    else:
        return {"error": "name and team required"}, 400
    
@app.route('/players/<int:id>', methods = ['DELETE'])
@jwt_required()
def delete_players(id):
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM players WHERE id = ?', [id])
    row = cursor.fetchone()
    if row:
        cursor.execute('DELETE FROM players WHERE id = ?', [id])
        conn.commit()
        conn.close()
        return {"message": "deleted"}, 200
    else:
        return {"error": "id not found"}, 404
    
@app.route('/players/<int:id>', methods = ['PUT'])
@jwt_required()
def update_players(id):
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM players WHERE id = ?', [id])
    row = cursor.fetchone()
    if row:
        cursor.execute('UPDATE players SET goals = goals + 1 WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return {"message": "updated"}, 200
    else:
        return {"error": "id not found"}, 404
    
if __name__ == '__main__':
    app.run(debug=True)