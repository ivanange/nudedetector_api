from flask import Flask, request, jsonify
from mediavalidator import validate

app = Flask(__name__)


@app.post("/validate")
def validate_image():
    files = request.files.getlist("file")
    validation = validate(files)
    results = []
    for i, file in enumerate(files):
        results.append({"filename": file.filename, "valid": int(validation[i])})
    return jsonify(results)
