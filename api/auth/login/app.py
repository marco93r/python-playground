from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask import Flask, request

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

@app.route('/protected', methods = ['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return {"message": "hello, " + current_user}, 200
    

if __name__ == '__main__':
    app.run(debug=True)