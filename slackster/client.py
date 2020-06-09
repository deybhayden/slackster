"""
Set of utilities for managing Slack connections etc.
"""
import os

from slack import WebClient
from slack.errors import SlackApiError


def get_web_client():
    """
    Return slack.WebClient instance as long as SLACK_TOKEN environment variable is set.
    """
    token = os.environ.get("SLACK_TOKEN")
    if not token:
        raise RuntimeError(
            "Set an environment variable named SLACK_TOKEN to use slackster."
        )

    return WebClient(token=token)


def get_conversation_roster(client, conversation_id):
    return client.conversations_info(channel=conversation_id, include_num_members=1)
