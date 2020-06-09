"""
Base file containing tools for building and composing Slackster commands.
"""


class SlacksterCommand:
    """
    Base class for slackster commands
    """

    def __init__(self, client, arguments):
        self.client = client
        self.name = arguments.command
        self.first_conversation_id = arguments.first_conversation_id
        self.second_conversation_id = arguments.second_conversation_id

    def run(self):
        """Perform command built from Slack CLI tool"""
        if self.name == "diff":
            self.perform_diff()

    def perform_diff(self):
        first_roster = self.client.get_conversation_members(self.first_conversation_id)
        second_roster = self.client.get_conversation_members(
            self.second_conversation_id
        )

        for user in first_roster:
            if user not in second_roster:
                user_info = self.client.get_user_info(user)["user"]
                formatted_user = (
                    (user_info["profile"]["display_name"] or user_info["real_name"])
                    + " (@"
                    + user_info["name"]
                    + ")"
                )

                print(formatted_user)
