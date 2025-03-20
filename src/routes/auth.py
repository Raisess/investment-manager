from app.controllers import AuthController

controller = AuthController("auth", __name__)
routes = controller.router()

@routes.get("/auth/signin")
def authenticate():
  return controller.authenticate()


@routes.get("/auth/callback")
def callback():
  return controller.callback()


@routes.get("/auth/logout")
def logout():
  return controller.logout()
