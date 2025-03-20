from __core.controller import Controller

controller = Controller("routes", __name__)
routes = controller.router()

@routes.get("/")
def index():
  if controller.session().get("user_id"):
    return controller.redirect("/investment/dashboard")

  return controller.render("index")
