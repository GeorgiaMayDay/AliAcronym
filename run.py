""" Basic operations using Slack_sdk """
import logging
import os

import requests
from flask import Flask, request
from slack_bolt import App, Say
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from zappa.asynchronous import task
from acronym_database.acronym_data import database

from constants import help_msg
from formatters.slack_formatter import extract_acronym_and_get_definition, \
    friendly_response

slack_token = os.environ["SLACKBOT_API_TOKEN"]
slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]

client = WebClient(token=slack_token)

bolt_app = App(token=slack_token, signing_secret=slack_signing_secret)
app = Flask(__name__)
app.logger.setLevel(logging.INFO)
slackHandler = SlackRequestHandler(bolt_app)

greetings = ["Hi", "hi", "hello", "Hello", "help", "Help"]


@bolt_app.event("app_mention")
def handle_app_mentions(ack, body, say, logger):
    app.logger.info("Received this body: {}".format(body["event"]))
    try:
        parent_comment = body["event"]["thread_ts"]
        channel_id = body["event"]["channel"]

        result = client.conversations_history(channel=channel_id, oldest=parent_comment, inclusive=True, limit=1)
        parent_text = result["messages"][0]['text']

        app.logger.info("Found the parent thread")
        result = client.chat_postMessage(
            channel=channel_id,
            thread_ts=parent_comment,
            text=friendly_response(parent_text, logger, "mention"),)
        app.logger.info("posted reply: {}".format(result))
    except KeyError:
        say(help_msg)
    except SlackApiError as e:
        app.logger.error(e)
        say("Sorry, I'm having some connectivity issues. Please try again in a moment")
    ack()



@bolt_app.command("/ali_explain")
def handle_acronym_command(ack, respond, command):
    user_query = command['text']
    # request_url = command['response_url']
    app.logger.info(user_query)
    results = extract_acronym_and_get_definition(user_query, database)
    for acronym_details in results:
        respond(acronym_details)
    ack()

@bolt_app.event("message")
def handle_message_events(ack, body, say):
    user_msg = body["event"]["text"]
    user_channel = body["event"]["channel"]
    app.logger.info("I have received this message: {}".format(user_msg))
    if user_msg in greetings:
        say(help_msg)
    else:
        for acronym_details in extract_acronym_and_get_definition(user_msg, database, logger=app.logger):
            say(acronym_details)
    ack()


@app.route("/ali_acronym/events", methods=["POST"])
def slack_events():
    app.logger.info("The events handler was called")
    """ Declaring the route where slack will post a request """
    return slackHandler.handle(request)

@app.route("/ali_acronym/install", methods=["GET"])
def install():
    return slackHandler.handle(request)


@app.route("/ali_acronym/oauth_redirect", methods=["GET"])
def oauth_redirect():
    return slackHandler.handle(request)

@app.route("/", methods=["GET", "POST"])
def lambda_handler(event=None, context=None):
    app.logger.info("Lambda function invoked index()")

    return "We're Live and Happening here in the Studio"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)