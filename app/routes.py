import json
from app import app

@app.route('/')
def hello_world():
    return json.dumps({'text': 'Hello World!!!'})
