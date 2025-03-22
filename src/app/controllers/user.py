from __core.controller import Controller

from app.models import UserModel
from app.repositories import UserRepository
from app.services.google import GoogleService

class UserController(Controller):
  def post_authentication(self) -> None:
    session = self.session()
    access_token = session.get("google_access_token")
    if not access_token:
      return self.redirect("/")

    google_profile_data = GoogleService.GetProfileInfo(access_token)
    email = google_profile_data.get("email")
    session.add("temporary_email", email)

    user_repository = UserRepository()
    user = user_repository.find_one({ "email": email })
    if not user:
      user = UserModel(
        name=google_profile_data.get("name"),
        email=google_profile_data.get("email"),
        picture=google_profile_data.get("picture"),
        status=0,
      )
      user_repository.create(user)

    return self.redirect("/user/validate_auth")

  def validate_authentication(self) -> None:
    session = self.session()
    email = session.get("temporary_email")
    session.clear()

    user_repository = UserRepository()
    user = user_repository.find_one({ "email": email, "status": 1 })
    if not user:
      # @TODO: redirect to payment session
      raise Exception("Invalid user")

    session.add("user_id", user.id) 
    return self.redirect("/investment/dashboard")
