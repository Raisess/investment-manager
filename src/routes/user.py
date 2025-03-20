from app.controllers import UserController

controller = UserController("user", __name__)
routes = controller.router()

@routes.get("/user/post_auth")
def post_authentication():
  return controller.post_authentication()
