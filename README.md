# Translate Bot
Translate bot is a slack bot project that translate with Google API or DeepL API.

## Description
The translation bot translate the message reaction or the message in the specified format and in the language selected at the time of posting. 
Translate Bot Support English, Japanese and Korean

## Slack App Configuration

1. Navigate to [https://api.slack.com/apps/](https://api.slack.com/apps/) and select to **Create a Slack App**
2. Select to **From an app manifest** and select to add to one of your Development Slack Workspaces.
3. Retrieve the [manifest.yml](manifest.yml) and update the URL's to reflect your Application URL's, then paste into the prompted window, and submit through the remaining screens. The application URL is generated via either ngrok or ta-cloud-proxy.
4. Navigate to **Settings** > **Basic Information** and find **App Credentials**. Keep this page open as you'll need it in the next section.

## How to create googletoken.json
Google Translate API required Google service account.
Google service account info in `googletoken.json`

* Navigate to https://cloud.google.com/translate/docs/setup
* Activate Cloud Translation API
* Create Service Account
* Click Key Management
* Select Key tab and Add Key
* Select JSON format
* Copy downloaded JSON file to googletoken.json
* Select Project
* Enable billing

## How to create DeepL API
* Navigate to https://www.deepl.com/ja/pro-api?cta=header-pro-api/
* Sign up Account
* Select Start Free Trial or Upgrade 
* Navigate to https://www.deepl.com/account/summary and check Authentication Key for DeepL API

## Convert the example.env to an .env
Using information from your Google API Key and DeepL API Key & Slack configuration the example.env and convert to a .env

## Set Up and Install Python
execute below commands. `.env ,requirements.txt, googletoken.json` file locate in root folders
```
python3 -m venv env/ ./venv/Scripts/activate
pip install -r requirements.txt
pip install --upgrade deepl
```

## Start Running 
```
python3 main.py
```

## Start up ngrok

Generate a URL for your local developer environment using one of the options below:

-   Start up ngrok with `ngrok http 8080` if you have a paid account start with: `ngrok http 8080 -subdomain MY-URL`

## Install the Slack App

1. To install the application navigate to your application url followed by: `/slack/install`, e.g. `https://MY-URL.com/slack/install`
2. Install the application to the Development Workspace selected when initially created.
3. Note: installation via Org settings UI will not trigger a saving of tokens in DB, so use above link.

## Usage 
- The table below shows the Message that are supported by the bot.

| Message           | Description                                                                        |
|------------------------|------------------------------------------------------------------------------------|
| `!help`    | Usage of Translate Bot.                                 |
| `!translate [language] [message]`    | You can translate messages by using !translate [en] or [jp] or [kr] [message] command.            |


