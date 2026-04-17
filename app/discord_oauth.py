from urllib.parse import urlencode
import requests
from flask import current_app


def get_authorization_url(state):
    params = {
        "client_id": current_app.config["DISCORD_CLIENT_ID"],
        "redirect_uri": current_app.config["DISCORD_REDIRECT_URI"],
        "response_type": "code",
        "scope": current_app.config["OAUTH_SCOPE"],
        "state": state,
        "prompt": "consent",
    }
    return f"{current_app.config['DISCORD_API_BASE_URL']}/oauth2/authorize?{urlencode(params)}"


def exchange_code(code):
    payload = {
        "client_id": current_app.config["DISCORD_CLIENT_ID"],
        "client_secret": current_app.config["DISCORD_CLIENT_SECRET"],
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": current_app.config["DISCORD_REDIRECT_URI"],
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(
        f"{current_app.config['DISCORD_API_BASE_URL']}/oauth2/token",
        data=payload,
        headers=headers,
    )
    response.raise_for_status()
    return response.json()


def fetch_user_info(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        f"{current_app.config['DISCORD_API_BASE_URL']}/users/@me", headers=headers
    )
    response.raise_for_status()
    return response.json()
