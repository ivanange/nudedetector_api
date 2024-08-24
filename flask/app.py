from flask import Flask, request, jsonify
from mediavalidator import validate
import serverless_wsgi

app = Flask(__name__)


@app.post("/validate")
def validate_image():
    files = request.files.getlist("file")
    if len(files) != 0:
        validation = validate(files)
    results = []
    for i, file in enumerate(files):
        results.append({"filename": file.filename, "valid": int(validation[i])})
    return jsonify(results)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)
