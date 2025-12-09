""" Basic operations using Slack_sdk """
import logging
import os

from flask import Flask, request
from slack_bolt import App, Say
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_sdk import WebClient

from acronym_database.acronym_data import database
from formatters.slack_formatter import extract_acronym_description_text, extract_acronym_and_get_definition

slack_token = os.environ["SLACKBOT_API_TOKEN"]
slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]

client = WebClient(token=slack_token)

bolt_app = App(token=slack_token, signing_secret=slack_signing_secret)
app = Flask(__name__)
app.logger.setLevel(logging.INFO)
handler = SlackRequestHandler(bolt_app)

greetings = ["Hi", "hi", "hello", "Hello", "help", "Help"]


@bolt_app.event("app_mention")
def handle_app_mentions(body, say, logger):
    app.logger.info(body["event"]["text"])
    text = body["event"]["text"]
    parent_comment = body["event"]["ts"]
    channel = body["event"]["channel"]
    say(extract_acronym_description_text(text, database=database, logger=app.logger))

@bolt_app.command("/ali_explain")
def handle_acronym_command(ack, respond, command):
    ack()
    user_query = command['text']
    print(user_query)
    app.logger.info(command)
    for acronym_details in extract_acronym_and_get_definition(user_query, database, logger=app.logger):
        respond(acronym_details)


@bolt_app.event("message")
def handle_message_events(body, say, logger):
    logger.info(body)
    app.logger.info(body)
    user_msg = body["event"]["text"]
    if user_msg in greetings:
        say(f"Hi, I'm Ali Acronym, feel free to shoot me over some acronyms or jargon-landed paragraph and I'll try and decode it for you! \n You can also use the command /ali_explain for the same thing in any channel I'm in (sent only for your eyes :eyes:) or @ me in a thread and I'll give a public explanation of acronyms of jargon in the comment that spawned the thread")
    else:
        for acronym_details in extract_acronym_and_get_definition(user_msg, database, logger=app.logger):
            say(acronym_details)


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
