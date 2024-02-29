from enum import Enum
from flask import Flask, jsonify, request
from openai import prompt_gpt_bot
from utils import build_endpoint_data

app = Flask(__name__)


class Method(Enum):
    GET = "GET"
    POST = "POST"


@app.route("/")
def home():
    return (
        jsonify(
            {
                "status": "UP",
                "api_endpoints": [
                    build_endpoint_data(
                        name="home page", path="/", description="", method="GET"
                    ),
                    build_endpoint_data(
                        name="health",
                        path="/health",
                        description="",
                        method="GET",
                    ),
                    build_endpoint_data(
                        name="cv review",
                        path="/cv-review",
                        description="",
                        method="POST",
                    ),
                ],
            }
        ),
        200,
    )


@app.route("/health")
def health():
    response = jsonify({"success": True, "health": "UP"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 200


# Endpoint to create a new guide
@app.route("/cv-review", methods=["POST"])
def cv_review():
    try:
        cv_raw_text = request.json["cv_raw_text"]
        job_title = request.json["job_title"]
        job_description_text = request.json["job_description_text"]
        username = request.json["username"]
    except Exception as e:
        response = jsonify({"msg": "An error Occoured"})
        return response, 400
    bot_resp = prompt_gpt_bot(
        cv_raw_text=cv_raw_text,
        job_title=job_title,
        job_description_text=job_description_text,
        username=username,
    )
    response = jsonify({"msg": bot_resp})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
