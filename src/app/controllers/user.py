from __core.controller import Controller

from app.models import UserModel
from app.repositories import UserRepository
from app.services.google import GoogleService

class UserController(Controller):
  def post_authentication(self) -> None:
    session = self.session()
    access_token = session.get("google_access_token")
    if not access_token:
      raise Exception("Not authenticated")

    google_profile_data = GoogleService.GetProfileInfo(access_token)

    user_repository = UserRepository()
    user = user_repository.find_one({ "email": google_profile_data.get("email") })
    if not user:
      user = UserModel(
        name=google_profile_data.get("name"),
        email=google_profile_data.get("email"),
        picture=google_profile_data.get("picture"),
        status=1
      )
      user_repository.create(user)

    session.add("user_id", user.id) 
    return self.redirect("/investment/dashboard")
