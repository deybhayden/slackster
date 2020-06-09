"""
Set of utilities for managing Slack connections etc.
"""
import os

from slack import WebClient


class SlacksterClient:
    """
    Helper class wrapper around Slack WebClient.
    """

    def __init__(self):
        """
        Return slack.WebClient instance as long as SLACK_TOKEN environment variable is set.
        """
        token = os.environ.get("SLACK_TOKEN")
        if not token:
            raise RuntimeError(
                "Set an environment variable named SLACK_TOKEN to use slackster."
            )

        self.web_client = WebClient(token=token)

    def get_conversation_info(self, conversation_id):
        """
        Get basic information from the conversation (public/private/group) id.
        """
        return self.web_client.conversations_info(
            channel=conversation_id, include_num_members=1
        )

    def get_conversation_members(self, conversation_id):
        """
        Get entire member list from the conversation (public/private/group) id.
        """
        response = self.web_client.conversations_members(channel=conversation_id)
        members = response["members"]
        cursor = response["response_metadata"].get("next_cursor")

        while cursor:
            response = self.web_client.conversations_members(
                channel=conversation_id, cursor=cursor
            )
            members.extend(response["members"])
            cursor = response["response_metadata"].get("next_cursor")

        return members

    def get_user_info(self, user_id):
        """
        Get basic information about the user.
        """
        return self.web_client.users_info(user=user_id)
