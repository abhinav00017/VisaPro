from utils.backendopenai import BackendOpenAI
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

BackendOpenAI = BackendOpenAI(os.getenv('OPENAI_API_KEY'))

@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/newuser', methods=['GET','POST'])
def newUser():
    thread_id=BackendOpenAI.create_thread()
    print(thread_id)
    return f"<h1>Thread Id {thread_id}</h1>"

@app.route('/getuser', methods=['GET','POST'])
def getUser():
    thread_id=BackendOpenAI.get_thread('thread-id')
    print(thread_id)
    return f"<h1>Thread Id {thread_id}</h1>"


if __name__ == '__main__':
    app.run()
