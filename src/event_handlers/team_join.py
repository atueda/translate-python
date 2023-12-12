from ..app.slackbot import SlackBot

def handle_team_join(event, client):
    """Handle team join events

    Will send a welcome message to every user who joins the team
    """
    # Get the id of the Slack user associated with the incoming event
    user_id = event.get("user", {}).get("id")

    # Open a DM with the new user.
    response = client.conversations_open(users=user_id)
    channel = response["channel"]["id"]

    # Create a new onboarding tutorial.
    slackbot = SlackBot(channel)

    # Get the onboarding message payload
    message = slackbot.get_message_payload("welcome")

    # Post the onboarding message in Slack
    client.chat_postMessage(message)