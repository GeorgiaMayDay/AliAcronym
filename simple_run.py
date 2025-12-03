""" Basic operations using Slack_sdk """

import os
import re

from flask import Flask, request
from slack_sdk import WebClient
from slack_bolt import App, Say
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

slack_token = os.environ["SLACKBOT_API_TOKEN"]
slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]

client = WebClient(token=slack_token)

bolt_app = App(token=slack_token, signing_secret=slack_signing_secret)
app = Flask(__name__)
# # Creating an instance of the Webclient class
client = WebClient(token=slack_token)

handler = SlackRequestHandler(bolt_app)

@bolt_app.message("hello ali")
def greetings(payload: dict, say: Say):
    """ This will check all the message and pass only those which has 'hello ali' in it """
    user = payload.get("user")
    say(f"Hi <@{user}>")

@bolt_app.message(re.compile("(hi|hello|hey) ali"))
def reply_in_thread(payload: dict):
    """ This will reply in thread instead of creating a new thread """
    response = client.chat_postMessage(channel=payload.get('channel'),
                                     thread_ts=payload.get('ts'),
                                     text=f"Hi<@{payload['user']}>")

@app.route("/ali_acronym/events", methods=["POST"])
def slack_events():
    """ Declaring the route where slack will post a request """
    return handler.handle(request)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

# try:
#     # Posting a message in #random channel
#     response = client.chat_postMessage(
#         channel="U09SR9R0BSB",
#         text="Bot's first message")
#
#     # Sending a message to a particular user
#     response = client.chat_postEphemeral(
#         channel="U09SR9R0BSB",
#         text="Hello USERID0000",
#         user="USERID0000")
#     print(response["channel"])
#
#     # Get basic information of the channel where our Bot has access
#     response = client.conversations_info(
#         channel="U09SR9R0BSB")
#
#     # Get a list of conversations
#     response = client.conversations_list()
#     print(response["channels"])
#
# except SlackApiError as e:
#     assert e.response["error"]
#     print(e.response["error"])