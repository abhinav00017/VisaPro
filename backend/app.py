import os
import pathlib
from dotenv import load_dotenv
from flask import Flask, request, session, abort, redirect
import requests

from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

from utils.backendopenai import BackendOpenAI

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('GOOGLE_SECRET_KEY')
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')

client_secrets_file = os.path.join(
    pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://localhost:5000/callback"
)

BackendOpenAI = BackendOpenAI(os.getenv('OPENAI_API_KEY'))

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper

def login_to_home(function):
    def wrapper1(*args, **kwargs):
        print(session)
        if "google_id" not in session:
            return redirect("/") 
        else:
            return redirect("/protected_area")

    return wrapper1
        

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
    print(id_info)
    print(type(id_info))
    print(session,type(session))
    return redirect("/protected_area")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/logout-successfull")

@app.route("/logout-successfull")
def logoutsuccessfull():
    return "Loggedout Successsfully <a href='/'><button>home</button></a>"


@app.route('/')
def hello():
    return "Hello, World! <a href='/login'><button>Login</button></a>"


@app.route("/protected_area")
@login_is_required
def protected_area():
    return f"Hello {session["name"]}! <br/> <a href='/logout'><button>Logout</button></a>"


@app.route('/newuser', methods=['GET', 'POST'])
def newUser():
    thread_id = BackendOpenAI.create_thread()
    return thread_id


@app.route('/getuser', methods=['GET', 'POST'])
def getUser():
    data = request.get_json()
    thread_id = data['thread_id']
    response_data = BackendOpenAI.get_thread(thread_id)
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
        print(response_data_3['data'][0]['status'],
              '----', response_data_3['data'][0]['id'])
        response_data_3 = BackendOpenAI.run_thread_status(thread_id)
    print(response_data_3)
    response_data_4 = BackendOpenAI.get_thread_response(thread_id)
    return response_data_4['data'][0]['content'][0]['text']['value']


if __name__ == '__main__':
    app.run()
