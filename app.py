import os
import main
import json
import requests
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App
from dotenv import find_dotenv, load_dotenv
from flask import Flask, request

import google.auth
import google.auth.transport.requests
creds, project = google.auth.default()
auth_req = google.auth.transport.requests.Request()
creds.refresh(auth_req)

load_dotenv(find_dotenv())
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
SLACK_BOT_USER_ID = os.environ["SLACK_BOT_USER_ID"]

app = App(token=SLACK_BOT_TOKEN)
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@app.event("message")
def handle_mentions(body, say):
    text = body["event"]["text"]
    mention = f"<@{SLACK_BOT_USER_ID}>"
    text = text.replace(mention, "").strip()
    response = main.sample_detect_intent(text)
    result = ""
    result += response['answer']
    result += "\n\nreference link:\n"
    for i in response['link']:
        result+= "\n- "+i
    # say(json.dumps(response, indent=4))
    say(result)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    request_json = request.get_json(silent=True)
    print(json.dumps(request_json, indent= 4))
    return handler.handle(request)

if __name__ == "__main__":
    flask_app.run()