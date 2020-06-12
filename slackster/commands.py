"""
Base file containing tools for building and composing Slackster commands.
"""
import os


def check_org_email_domain(email):
    """
    Check passed email against ORG_EMAIL_DOMAIN for full organization members.
    """
    domain = os.environ.get("ORG_EMAIL_DOMAIN")
    return email.endswith(domain)


class SlacksterCommand:
    """
    Base class for slackster commands
    """

    def __init__(self, client, arguments):
        self.client = client
        self.name = arguments.command
        self.arguments = arguments

    def run(self):
        """Perform command built from Slack CLI tool"""
        if self.name == "diff":
            self.perform_diff()
        elif self.name == "archive":
            self.perform_archive()
        elif self.name == "prefix":
            self.perform_prefix_search()

    def perform_diff(self):
        """
        Print out members of first_conversation_id that aren't
        in the second_conversation_id.
        """
        first_roster = self.client.get_conversation_members(
            self.arguments.first_conversation_id
        )
        second_roster = self.client.get_conversation_members(
            self.arguments.second_conversation_id
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

    def perform_archive(self):
        """
        Archive channels with less than arguments.number of members upon confirmation.
        """
        channels = self.client.get_conversation_list()

        for channel in channels:
            if channel["num_members"] <= self.arguments.number:
                msg = "Going to archive {} ({} members). Type 'Yes' to continue. ".format(
                    channel["name"], channel["num_members"]
                )
                confirm = input(msg)
                if confirm.lower() == "yes":
                    self.client.archive_conversation(channel["id"])
                    print("Channel archived.")
                else:
                    print("Channel saved!")

    def perform_prefix_search(self):
        """
        Print channels with passed prefix string.
        """
        channels = self.client.get_conversation_list()
        results = []

        for channel in channels:
            if channel["name"].startswith(self.arguments.prefix):
                results.append((channel["num_members"], channel["name"]))

        print("Search results (most members first):\n")
        for (count, name) in sorted(results, key=lambda x: x[0], reverse=True):
            print("#{} with {} members".format(name, count))
