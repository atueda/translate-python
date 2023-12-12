from slack_sdk.web import WebClient
from ..app.translator import translate_text, translation_mapper
from ..app.slackbot import SlackBot, get_conversation

def handle_flag_reactions(event, client: WebClient):
    """Handle flag reactions

    Handles slack reactions that have a flag and will translate the message
    to the language specified by the flag
    """
    type = event.get('item', {}).get('type')
    if type != 'message':
        return

    reaction = event.get('reaction')
    channel_id = event.get("item", {}).get("channel")
    message_id = event.get("item", {}).get("ts")

    conversation = get_conversation(client, channel_id, message_id)

    # Retrieve and validate language code
    language_code = ""
    try:
        language_code = translation_mapper[reaction]
    except KeyError:
        if 'flag' in reaction:
            slackbot = SlackBot(channel_id)
            message = slackbot.get_message_payload("invalid_language_flag")
            return client.chat_postMessage(**message | { "channel": channel_id, "thread_ts": conversation['ts'] })
        else:
            return

    # Get translated message
    message = translate_text(language_code, conversation["text"])

    # Post the translated message to same thread as the message is in
    client.chat_postMessage(
        channel=channel_id,
        thread_ts=conversation["ts"],
        text=message
    )