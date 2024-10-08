from flask import Flask, request, jsonify
from mediavalidator import validate
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.post("/validate")
def validate_image():
    files = request.files.getlist("file")
    if len(files) != 0:
        validation = validate(files)
    results = []
    for i, file in enumerate(files):
        results.append({"filename": file.filename, "valid": int(validation[i])})

    response = jsonify(results)
    return response


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
