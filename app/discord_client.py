import requests
from flask import current_app


class DiscordAPIError(Exception):
    pass


class DiscordClient:
    def __init__(self, bot_token=None):
        self.bot_token = bot_token or current_app.config["DISCORD_BOT_TOKEN"]
        self.base_url = f"{current_app.config['DISCORD_API_BASE_URL']}/v10"
        self.headers = {
            "Authorization": f"Bot {self.bot_token}",
            "Content-Type": "application/json",
        }

    def send_embed(self, channel_id, embed_payload):
        url = f"{self.base_url}/channels/{channel_id}/messages"
        body = {"embeds": [embed_payload]}
        response = requests.post(url, json=body, headers=self.headers)
        self._check_response(response)
        return response.json()

    def update_embed(self, channel_id, message_id, embed_payload):
        url = f"{self.base_url}/channels/{channel_id}/messages/{message_id}"
        body = {"embeds": [embed_payload]}
        response = requests.patch(url, json=body, headers=self.headers)
        self._check_response(response)
        return response.json()

    def delete_message(self, channel_id, message_id):
        url = f"{self.base_url}/channels/{channel_id}/messages/{message_id}"
        response = requests.delete(url, headers=self.headers)
        if response.status_code not in (204, 404):
            self._check_response(response)
        return True

    def _check_response(self, response):
        if not response.ok:
            raise DiscordAPIError(
                f"Discord API error {response.status_code}: {response.text}"
            )
