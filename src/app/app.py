import logging
from slack_bolt import App
from slack_sdk.web import WebClient
from ..event_handlers.flag_reactions import handle_flag_reactions
from ..event_handlers.commands import handle_commands
from ..event_handlers.team_join import handle_team_join
from dotenv import load_dotenv

# Load the environment from .env file
# Following variables are required:
# SLACK_BOT_TOKEN
# SLACK_USER_TOKEN
# SLACK_SIGNING_SECRET
# GOOGLE_APPLICATION_CREDENTIALS
load_dotenv()

# Initialize a Bolt for Python app
app = App()

# Handle team join event
@app.event("team_join")
def handle_team_join_event(event, client: WebClient):
    handle_team_join(event, client)
    # Other team join event handles
    

# Handle Reaction added events
@app.event("reaction_added")
def handle_added_reactions_event(event, client: WebClient):
    handle_flag_reactions(event, client)
    # Other reaction handlers

# Handle message events
@app.event("message")
def handle_message_event(event, client: WebClient):
    handle_commands(event, client)
    # Other message handlers

# Start server
def start_server():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.start(3000)