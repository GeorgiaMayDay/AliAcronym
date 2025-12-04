""" Basic operations using Slack_sdk """

import os
import re

from flask import Flask, request
from slack_sdk import WebClient
from slack_bolt import App, Say
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from acronym_analysis.acronym_identifier import identify_acronym

slack_token = os.environ["SLACKBOT_API_TOKEN"]
slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]

client = WebClient(token=slack_token)

bolt_app = App(token=slack_token, signing_secret=slack_signing_secret)
app = Flask(__name__)
# # Creating an instance of the Webclient class
client = WebClient(token=slack_token)

handler = SlackRequestHandler(bolt_app)


@bolt_app.event("app_mention")
def handle_app_mentions(body, say, logger):
    app.logger.info(body["event"]["text"])
    text = body["event"]["text"]
    acronyms = identify_acronym(text)
    if acronyms:
        say(f"I've identified:{acronyms} \n That's a nice acronym")
    else:
        say(f"I'm sorry I couldn't find an acronym in the string you sent me")

@bolt_app.command("/ali_explain")
def handle_acronym_command(ack, respond, command):
    ack()
    user_query = command['text']
    # thread_ts = command.get('thread_ts', command['ts'])
    print(user_query)
    app.logger.info(command)
    app.logger.info("Cheese")

    # Process the query (we'll implement this next)
    # response = generate_response(user_query, thread_ts)
    respond("TESTING")


@bolt_app.event("message")
def handle_message_events(body, say, logger):
    logger.info(body)
    app.logger.info(body)
    say(f"Hi I don't know you")

@app.route("/ali_acronym/events", methods=["POST"])
def slack_events():
    """ Declaring the route where slack will post a request """
    return handler.handle(request)

@app.route("/ali_acronym/install", methods=["GET"])
def install():
    return handler.handle(request)


@app.route("/ali_acronym/oauth_redirect", methods=["GET"])
def oauth_redirect():
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
