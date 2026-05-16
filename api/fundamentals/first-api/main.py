from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def welcome():
    return {"message": "Welcome to my API!"}

@app.route('/hello')
def hello():
    return {"message": "Hello, World!"}

@app.route('/status')
def status():
    return {"status": "ok", "version": "1.0"}

@app.route('/echo', methods = ['POST'])
def echo():
    payload = request.json
    if "message" not in payload:
        return {"error": "message field required"}, 400
    else:
        return {"you sent": payload['message']}

if __name__ == '__main__':
    app.run(debug=True)