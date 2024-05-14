from utils.backendopenai import BackendOpenAI
from flask import Flask, request
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
    return thread_id

@app.route('/getuser', methods=['GET','POST'])
def getUser():
    data = request.get_json()
    thread_id=data['thread_id']
    response_data=BackendOpenAI.get_thread(thread_id)
    print(response_data) 
    return response_data

@app.route('/modifyuser', methods=['PUT'])
def modifyUser():
    data = request.get_json()
    print(data)
    thread_id = data['thread_id']
    action = data['action']
    response_data = BackendOpenAI.modify_thread(thread_id, action)
    print(response_data)
    return f"<h1>Thread Id {response_data}</h1>"

@app.route('/deleteuser', methods=['DELETE'])
def deleteUser():
    data = request.get_json()
    thread_id = data['thread_id']
    response_data = BackendOpenAI.delete_thread(thread_id)
    print(response_data)
    return f"<h1>Thread Id {response_data}</h1>"

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    print(data)
    thread_id = data['thread_id']
    message = data['message']
    response_data_1 = BackendOpenAI.query_inserstion(thread_id, message)
    print(response_data_1)
    response_data_2 = BackendOpenAI.run_thread(thread_id)
    print(response_data_2)
    response_data_3 = BackendOpenAI.run_thread_status(thread_id)
    while response_data_3['data'][0]['status'] != 'completed':
        print(response_data_3['data'][0]['status'],'----',response_data_3['data'][0]['id'])
        response_data_3 = BackendOpenAI.run_thread_status(thread_id)
    print(response_data_3)
    response_data_4 = BackendOpenAI.get_thread_response(thread_id)
    return response_data_4['data'][0]['content'][0]['text']['value']

if __name__ == '__main__':
    app.run()
