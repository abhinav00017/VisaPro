import os
import pathlib
# from dotenv import load_dotenv
from flask import Flask, request, session, abort, redirect, render_template, jsonify
from flask_session import Session
from functools import wraps
import requests
import json

from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

from utils.backendopenai import BackendOpenAI
from db.records import Records

# load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('GOOGLE_SECRET_KEY')
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

global email
records = Records()

client_secrets_file = os.path.join(
    pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="https://visapro.azurewebsites.net/callback"
)

BackendOpenAI = BackendOpenAI(os.getenv('OPENAI_API_KEY'))
threads = []


def login_is_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            kwargs['status']="loggedout"  # Authorization required
            return function(*args, **kwargs)
        else:
            global email
            email = session["email"]
            print(session)
            return function(*args, **kwargs)
    return wrapper


def login_to_home(function):
    def wrapper1(*args, **kwargs):
        print(session['email'])
        if "google_id" not in session:
            return redirect("/")
        else:
            return redirect("/protected_area")
    return wrapper1


@app.route("/save_user_data", methods=['POST'])
@login_is_required
def save_user_data(status=None):
    if status == "loggedout":
        return redirect("/")
    data = request.get_json()
    print(data)
    global email
    data['email'] = email
    print(records.create_record(data))
    return "Data Saved Successfully"


@app.route("/add_new_user_data")
@login_is_required
def add_new_user_data(status=None):
    if status == "loggedout":
        return redirect("/")
    return render_template('/frontend/Add_new_user_data.html')



@app.route("/threads")
@login_is_required
def thread(status=None):
    if status == "loggedout":
        return redirect("/")
    global email
    data = records.retrieve_record(email)
    print(data)
    if data == "None":
        return json.dumps({
            "threads_list": data["threads"]
        })
    return json.dumps({
        "threads_list": data["threads"]
    })


@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(
        session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    global email
    email = id_info.get("email")
    session["email"] = email
    return redirect("/home_screen")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/logout-successfull")


@app.route("/logout-successfull")
def logoutsuccessfull():
    return "Loggedout Successsfully <a href='/'><button>home</button></a>"

@app.route('/')
@login_is_required
def hello(status=None):
    if status == "loggedout":
        return render_template('/frontend/Login_landing.html')
    global email
    data = records.retrieve_record(email)
    if data == "None":
        return redirect("/add_new_user_data")
    return redirect('/home_screen')


@app.route("/home_screen")
@login_is_required
def home_screen(status=None):
    if status == "loggedout":
        return redirect("/")
    global email
    data = records.retrieve_record(email)
    if data == "None":
        return redirect("/add_new_user_data")
    return render_template('/frontend/Home_screen.html', name=session["name"])


@app.route('/add_thread', methods=['GET', 'POST'])
@login_is_required
def newUser(status=None):
    if status == "loggedout":
        return redirect("/")
    thread_data = BackendOpenAI.create_thread()
    print(thread_data)
    global email
    data = records.retrieve_record(email)
    if data != "None":
        data["threads"].append(thread_data)
    data['email'] = email
    print(records.update_record(data))
    return thread_data


@app.route('/add_user', methods=['POST'])
@login_is_required
def addUser(status=None):
    if status == "loggedout":
        return redirect("/")
    data = request.get_json()
    print(data)
    global email
    data['email'] = email
    print(records.create_record(data))
    return "true"



@app.route('/getuser', methods=['GET', 'POST'])
@login_is_required
def getUser(status=None):
    if status == "loggedout":
        return redirect("/")
    data = request.get_json()
    thread_id = data['thread_id']
    response_data = BackendOpenAI.get_thread(thread_id)
    print(response_data)
    return response_data


@app.route('/modifyuser', methods=['PUT'])
@login_is_required
def modifyUser(status=None):
    if status == "loggedout":
        return redirect("/")
    data = request.get_json()
    print(data)
    thread_id = data['thread_id']
    action = data['action']
    response_data = BackendOpenAI.modify_thread(thread_id, action)
    print(response_data)
    return f"<h1>Thread Id {response_data}</h1>"


@app.route('/deleteuser', methods=['DELETE'])
@login_is_required
def deleteUser(status=None):
    if status == "loggedout":
        return redirect("/")
    data = request.get_json()
    thread_id = data['thread_id']
    response_data = BackendOpenAI.delete_thread(thread_id)
    print(response_data)
    return f"<h1>Thread Id {response_data}</h1>"


@app.route('/chat', methods=['POST'])
@login_is_required
def chat(status=None):
    if status == "loggedout":
        return redirect("/")
    message = request.json.get('message')
    thread_id = request.json.get('threadId')
    response_data_1 = BackendOpenAI.query_inserstion(thread_id, message)
    print(response_data_1)
    response_data_2 = BackendOpenAI.run_thread(thread_id)
    print(response_data_2)
    response_data_3 = BackendOpenAI.run_thread_status(thread_id)
    while response_data_3['data'][0]['status'] != 'completed':
        print(response_data_3['data'][0]['status'],
              '----', response_data_3['data'][0]['id'])
        response_data_3 = BackendOpenAI.run_thread_status(thread_id)
    print(response_data_3)
    response_data_4 = BackendOpenAI.get_thread_response(thread_id)
    response_answer = response_data_4['data'][0]['content'][0]['text']['value']
    for i in threads:
        if i['id'] == thread_id:
            i['messages'].append({'sender': 'user', 'content': message})
            i['messages'].append(
                {'sender': 'assistant', 'content': response_answer})
    return jsonify({'response': response_answer, 'threadId': thread_id})


def load_chat(thread_id):
    # thread_id = request.json.get('threadId')
    thread = BackendOpenAI.get_thread_data(thread_id)
    print(thread)
    messages = []
    for message in thread['data']:
        messages.append({
            'id': message['id'],
            'sender': message['role'],
            'content': message['content'][0]['text']['value']
        })
    messages = messages[::-1]
    history = {
        'id': thread_id,
        'title': thread_id,
        'messages': messages
    }
    threads.append(history)
    print(threads)
    return jsonify(threads)



@app.route('/threads/<string:thread_id>', methods=['GET'])
def get_data(thread_id):
    global threads
    thread = None
    print("one ", threads)
    print(thread_id)
    if threads != []:
        thread = next((t for t in threads if t['id'] == thread_id), None)
    if thread == None:
        load_chat(thread_id)
        print("two ", threads)
        thread = next((t for t in threads if t['id'] == thread_id), None)
    print("three ", thread)
    if thread:
        return jsonify(thread)
    return jsonify({'error': 'Thread not found'}), 404


@app.route('/profile_page')
@login_is_required
def profile_page(status=None):
    if status == "loggedout":
        return redirect("/")
    global email
    data = records.retrieve_record(email)
    if data == "None":
        return redirect("/add_new_user_data")
    if data.get('phonenumber') == None:
        data['phonenumber'] = ''
    else:
        data['phonenumber'] = data.get('phonenumber')
    return render_template('/frontend/Profile.html', username=data['user_name'], email=email, country=data['country'], phonenumber=data['phonenumber'])


@app.route('/update_profile', methods=['POST'])
@login_is_required
def update_profile(status=None):
    if status == "loggedout":
        return redirect("/")
    update_data = request.get_json()
    global email
    data = records.retrieve_record(email)
    data['user_name'] = update_data['user_name']
    data['country'] = update_data['country']
    data['email'] = update_data['email']
    data['phonenumber'] = update_data['phonenumber']
    print(records.update_record(data))
    return {"status": "Profile Updated Successfully"}

# @login_is_required
# @app.route('/get_threads', methods=['GET'])
# def get_threads():
#     return {"thread_ids":[db.fetch_thread_id('database.csv', session["google_id"])]}


if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
