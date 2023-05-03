from flask import Flask# , request
# from flask import jsonify
from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv()


@app.route('/')
def index():
    return 'success'


application = app
