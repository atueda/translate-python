import os
from slack_sdk.web import WebClient
from ..app.translator import translate_text, translation_mapper
from ..app.slackbot import SlackBot, get_conversation
from google.api_core.exceptions import BadRequest

# Handle commands
def handle_commands(event, client: WebClient):
    """Handle slackbot commands
    
    Handles commands `!help` and `!translate` and sends users messages based on their input
    """
    text = event.get("text")

    if text and text.lower() == "!help":
        handle_help_command(event, client)
    elif text and text.lower().startswith("!translate"):
        handle_translate_command(event, client, text)

# Handle help
def handle_help_command(event, client: WebClient):
    """Handle help command sends user the help message"""
    channel_id = event.get("channel")
    message_id = event.get("ts")
    conversation = get_conversation(client, channel_id, message_id)

    slackbot = SlackBot(channel_id)
    message = slackbot.get_message_payload("help")

    client.chat_postMessage(**message | { "channel": channel_id, "thread_ts": conversation["ts"] })

# Handle translations
def handle_translate_command(event, client: WebClient, text: str):
    """Handle translate command if valid parameters
    
    Should be in format `!translate [language] [message]`
    """

    channel_id = event.get("channel")
    message_id = event.get("ts")

    conversation = get_conversation(client, channel_id, message_id)

    try:
        # Parse command
        [_, language, text_to_translate] = text.split(" ", 2)

        # Retrieve and validate language code
        language_code = ""
        try:
            language_code = translation_mapper[language]
        except KeyError:
            return handle_command_error(client, channel_id, conversation["ts"], 'INVALID_LANGUAGE')
            
        # Get translated message
        try:
            translation = translate_text(language_code, text_to_translate)

            # Overwrite translation command message
            client.chat_update(
                channel=channel_id,
                ts=conversation["message_ts"],
                text=text_to_translate,
                token=os.environ.get("SLACK_USER_TOKEN")
            )

            # Post the translated message to same thread as the message is in
            client.chat_postMessage(
                channel=channel_id,
                thread_ts=conversation["ts"],
                text=translation
            )
        except BadRequest:
            return handle_command_error(client, channel_id, conversation["ts"], 'INVALID_LANGUAGE')
        
    except ValueError:
        return handle_command_error(client, channel_id, conversation["ts"], 'INVALID_FORMAT')
        
# Handle command errors later
def handle_command_error(client, channel_id, ts, type):
    slackbot = SlackBot(channel_id)
    message = ""

    # Display error message to user only on valid error types
    if type == 'INVALID_FORMAT':
        message = slackbot.get_message_payload("invalid_format")
    elif type == 'INVALID_LANGUAGE':
        message = slackbot.get_message_payload("invalid_language")
    elif type == 'INVALID_LANGUAGE_FLAG':
        message = slackbot.get_message_payload("invalid_language_flag")
    else:
        return

    # Sends error message to user / conversation
    client.chat_postMessage(**message | { "channel": channel_id, "thread_ts": ts })