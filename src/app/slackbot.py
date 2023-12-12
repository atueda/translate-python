from slack_sdk.web import WebClient

class SlackBot:
    """
    A class which builds slack messages

    Attributes
    ----------
    WELCOME_BLOCK : dict[str, Any]
        Welcome message block
    WELCOME_TEXT : str
        Welcome message in text form
    HELP_BLOCK : dict[str, Any]
        Help message block
    HELP_TEXT : str
        Help message text
    INVALID_FORMAT_BLOCK : dict[str, Any]
        Invalid format block
    INVALID_FORMAT_TEXT : str
        Invalied format text
    INVALID_LANGUAGE_BLOCK : dict[str, Any]
        Invalid language block
    INVALID_LANGUAGE_TEXT : str
        Invalid lanuage text
    INVALID_LANGUAGE_REACTION_BLOCK : dict[str, Any]
        Invalid language reaction block
    INVALID_LANGUAGE_REACTION_TEXT : str
        Invalid language reaction text
    DIVIDER_BLOCK : dict[str, Any]
        Divider block
    """

    WELCOME_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "Welcome to Slack! :wave: \n\n"
                "*You can use a translation bot. Use `!help` to view the commands.*"
            ),
        },
    }

    WELCOME_TEXT = """Welcome to Slack! :wave:
    
    You can use a translation bot. Use !help to view the commands."""

    HELP_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "*You can translate messages using the following methods:*"
            ),
        },
    }

    HELP_TEXT = """You can translate messages using the following methods: 
     
    1. Use commands to translate your messages
    You can translate messages by using !translate [en] or [jp] or [kr] [message] command.

    For example:
    Translate to English: !translate en このメッセージを翻訳します！
    Translate to Japanese: !translate jp Translate this message!
    Translate to Korean: !translate kr Translate this message!

    2. Use emoji reaction to translate your messages
    You can translate messages by using flags emoji :us: :jp: :kr:

    For example:
    Translate to English: !translate :us: このメッセージを翻訳します！
    Translate to Japanese: !translate :jp: Translate this message!
    Translate to Korean: !translate :kr: Translate this message!
    Or just use Find another reaction in the chat and choose flags :us: :jp: :kr:

    Note: This bot only supports English, Japanese and Korean :us: :jp: :kr:"""

    INVALID_FORMAT_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "The command you have inserted is invalid. Use `!help` to see all the valid commands."
            ),
        },
    }

    INVALID_FORMAT_TEXT = "The command you have inserted is invalid. Use '!help' to see all the valid commands."

    INVALID_LANGUAGE_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "You have used an unsupported language."
            ),
        },
    }

    INVALID_LANGUAGE_TEXT = "You have used an unsupported language."

    INVALID_LANGUAGE_REACTION_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "You have used an unsupported language flag. Currently supported flags are :us: :jp: :kr:"
            ),
        },
    }

    INVALID_LANGUAGE_REACTION_TEXT = "You have used an unsupported language flag. Currently supported flags are :us: :jp: :kr:"

    DIVIDER_BLOCK = {"type": "divider"}

    def __init__(self, channel: str):
        """
        Parameters
        ----------
        channel : str
            Channel ID to send messages to
        """
        self.channel = channel
        self.username = "workspacebot"
        self.timestamp = ""

    def get_message_payload(self, type: str = "welcome"):
        """Returns message based on type

        Parameters
        ----------
        type : str
            Message types (default is "welcome")

            Possible values "welcome", "help", "invalid_format", "invalid_language", "invalid_language_flag"
        """
        blocks = []
        text = ""
        if type == "welcome":
            blocks = [
                self.WELCOME_BLOCK,
            ]
            text = self.WELCOME_TEXT
        elif type == "help":
            blocks = [
                self.HELP_BLOCK,
                self.DIVIDER_BLOCK,
                *self.get_reaction_block(),
                self.DIVIDER_BLOCK,
                *self.get_command_block(),
            ]
            text = self.HELP_TEXT
        elif type == "invalid_format":
            blocks = [
                self.INVALID_FORMAT_BLOCK,
            ]
            text = self.INVALID_FORMAT_TEXT
        elif type == "invalid_language":
            blocks = [
                self.INVALID_LANGUAGE_BLOCK,
            ]
            text = self.INVALID_LANGUAGE_TEXT
        elif type == "invalid_language_flag":
            blocks = [
                self.INVALID_LANGUAGE_REACTION_BLOCK,
            ]
            text = self.INVALID_LANGUAGE_REACTION_TEXT

        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "blocks": blocks,
            "text": text,
        }

    def get_reaction_block(self):
        text = (
            "*1. Use `!translate [target language] [message]` command*\n"
            "You can quickly translate any message on Slack into Enlish, Japanese and Korean.\n\n"

            "*2. Add an flag emoji reaction to a message* :us: :jp: :kr:\n"
            "You can quickly translate any message on Slack with an emoji reaction."
        )
        return self.get_block(text)

    def get_command_block(self):
        text = (
            "*1. Use commands to translate your messages*\n"
            "You can translate messages by using `!translate [en] or [jp] or [kr] [message]` command.\n\n"
            "For example:\n"
            "Translate to English: `!translate en このメッセージを翻訳します！`\n"
            "Translate to Japanese: `!translate jp Translate this message!`\n"
            "Translate to Korean: `!translate kr Translate this message!`\n\n"

            "*2. Use emoji reaction to translate your messages*\n"
            "You can translate messages by using flags emoji :us: :jp: :kr:\n\n"
            "For example:\n"
            "Translate to English: !translate :us: このメッセージを翻訳します！\n"
            "Translate to Japanese: !translate :jp: Translate this message!\n"
            "Translate to Korean: !translate :kr: Translate this message!\n"
            "Or just use Find another reaction in the chat and choose flags :us: :jp: :kr:\n\n"

            "*Note: This bot only supports English, Japanese and Korean :us: :jp: :kr: *"
        )
        return self.get_block(text)

    @staticmethod
    def get_block(text):
        return [
            {"type": "section", "text": {"type": "mrkdwn", "text": text}},
        ]

def get_conversation(client: WebClient, channel_id: str, message_id: str):
    """Get the correct message_id / ts to add a reply to
    """

    # Get the oldest message from conversation thread
    result = client.conversations_replies(
        channel=channel_id,
        ts=message_id,
        inclusive=True,
        oldest=message_id,
        limit=1
    )

    message = result["messages"][0]
    text = message["text"]

    # Return thread_ts if reply (points to starting message)
    # and ts if starting message
    ts = message.get("thread_ts", message.get("ts"))

    # Return ts for overwriting text after commands
    message_ts = message.get("ts")

    return { "ts": ts, "text": text, "message_ts": message_ts }