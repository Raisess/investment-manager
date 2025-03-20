from __core.controller import Controller
from __core.env import Env
from __core.plugins.auth import GoogleOAuth2

APP_REDIRECT_HOST_BASE = Env.Get("APP_REDIRECT_HOST_BASE")
REDIRECT_URI = f"{APP_REDIRECT_HOST_BASE}/auth/callback"

class AuthController(Controller):
  def authenticate(self) -> None:
    auth_provider = GoogleOAuth2()
    authorization_url = auth_provider.get_authorization_url(REDIRECT_URI)
    return self.redirect(authorization_url)

  def callback(self) -> None:
    arguments = self.request().args()
    authorization_code = arguments.get("code") 

    auth_provider = GoogleOAuth2()
    token = auth_provider.get_authorized_token(REDIRECT_URI, authorization_code)
    self.session().add("google_access_token", token)
    return self.redirect("/user/post_auth")

  def logout(self) -> None:
    self.session().clear()
    return self.redirect("/")
