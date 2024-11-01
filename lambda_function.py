import json
import base64
import mediavalidator
import os

BASE_DIR = os.getenv("BASE_DIR", os.getenv("PYTHONPATH", ""))
mediavalidator.MODEL_PATH = BASE_DIR + mediavalidator.MODEL_PATH
mediavalidator.FEATURE_PATH = BASE_DIR + mediavalidator.FEATURE_PATH


def lambda_handler(event, context):
    data = json.loads(event["body"])
    files = data["files"]
    for file in files:
        with open("/tmp/" + file["filename"], "wb") as f:
            f.write(base64.b64decode(file["base64"]))

    validation = mediavalidator.validate(["/tmp/" + file["filename"] for file in files])
    results = []
    for i, file in enumerate(files):
        results.append({"filename": file["filename"], "valid": int(validation[i])})
        os.remove("/tmp/" + file["filename"])

    return {
        "statusCode": 200,
        "body": json.dumps(results),
    }
