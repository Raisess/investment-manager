import json

from __core.env import Env
from __core.integration.http_client import HttpClient

HOST = "https://www.googleapis.com"
API_KEY = Env.Get("GOOGLE_API_KEY")

class GoogleService:
  @staticmethod
  def GetProfileInfo(access_token: str) -> dict:
    http = HttpClient(HOST)
    (_, response_text) = http.get(f"oauth2/v1/userinfo?alt=json&access_token={access_token}")
    return json.loads(response_text)
