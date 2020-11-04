from flask import Flask, request
from flask_cors import CORS
from burrows import burrows

app = Flask(__name__)
CORS(app)

@app.route('/burrows', methods=['POST'])
def burrow():
    req_data = request.get_json()
    return burrows(req_data["disputedPaper"], req_data["disputedAuthor"])

app.run("127.0.0.1", 3000)