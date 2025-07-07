from app.controllers import InvestmentController

controller = InvestmentController("investment", __name__)
routes = controller.router()

@routes.get("/investment/dashboard")
def dashboard():
  return controller.dashboard()


@routes.get("/investment/chart/<id>")
def chart(id: str):
  return controller.chart(id)


@routes.get("/investment/create")
def create_view():
  return controller.create_view()


@routes.post("/investment/create")
def create():
  return controller.create()


@routes.get("/investment/edit/<id>")
def edit_view(id: str):
  return controller.edit_view(id)


@routes.post("/investment/edit/<id>")
def edit(id: str):
  return controller.edit(id)


@routes.get("/investment/delete/<id>")
def delete(id: str):
  return controller.delete(id)


@routes.post("/investment/import")
def import_():
  return controller.import_()


@routes.get("/investment/export")
def export():
  return controller.export()
