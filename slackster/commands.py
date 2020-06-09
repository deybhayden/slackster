"""
Base file containing tools for building and composing Slackster commands.
"""
import os


def check_org_email_domain(email):
    domain = os.environ.get("ORG_EMAIL_DOMAIN")
    return email.endswith(domain)


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
                should_print_user = all(
                    [
                        not user_info["is_bot"],
                        not user_info["is_app_user"],
                        not user_info["deleted"],
                        check_org_email_domain(user_info["profile"]["email"]),
                    ]
                )

                if should_print_user:
                    formatted_user = (
                        "@"
                        + (
                            user_info["profile"]["display_name"]
                            or user_info["real_name"]
                        )
                        + (" *" if user_info["is_restricted"] else "")
                    )

                    print(formatted_user)
