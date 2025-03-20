import html

from __core.controller import Controller

from app.models import InvestmentModel
from app.repositories import (
  InvestmentRepository,
  InvestmentRentabilityRepository,
  InvestmentSourceRepository,
  InvestmentTypeRepository,
  UserRepository,
)

class InvestmentController(Controller):
  def dashboard(self) -> str:
    user_id = self.session().get("user_id")
    if not user_id:
      raise Exception("Not authenticated")

    user_repository = UserRepository()
    user = user_repository.find_one({ "id": user_id })

    investment_repository = InvestmentRepository()
    investments = investment_repository.find(user_id)

    invested = 0
    total = 0
    for item in investments:
      invested += item.invested
      total += item.total

    return self.render("/investment/dashboard", {
      "investments": investments,
      "invested": invested,
      "total": total,
      "user": user,
    })

  def create_view(self) -> str:
    user_id = self.session().get("user_id")
    if not user_id:
      raise Exception("Not authenticated")

    user_repository = UserRepository()
    user = user_repository.find_one({ "id": user_id })

    investment_rentability_repository = InvestmentRentabilityRepository()
    investment_rentabilities = investment_rentability_repository.find()

    investment_source_repository = InvestmentSourceRepository()
    investment_sources = investment_source_repository.find()

    investment_type_repository = InvestmentTypeRepository()
    investment_types = investment_type_repository.find()

    return self.render("/investment/create", {
      "investment_rentabilities": investment_rentabilities,
      "investment_sources": investment_sources,
      "investment_types": investment_types,
      "user": user,
    })

  def create(self) -> None:
    user_id = self.session().get("user_id")
    if not user_id:
      raise Exception("Not authenticated")

    request = self.request()
    form = request.form()

    investment_repository = InvestmentRepository()
    investment_repository.create(InvestmentModel(
      user_id=user_id,
      type_id=form.get("type"),
      source_id=form.get("source"),
      name=html.escape(form.get("name")),
      invested=form.get("invested"),
      total=form.get("total"),
      maturity=form.get("maturity") if form.get("maturity") != "" else None,
      rentability_id=form.get("rentability_type") if form.get("rentability_type") != "None" else None,
      rentability_number=form.get("rentability_number") if form.get("rentability_type") != "None" and form.get("rentability_number") != "" else None,
    ))

    return self.redirect("/investment/dashboard")

  def edit_view(self, id: str) -> str:
    user_id = self.session().get("user_id")
    if not user_id:
      raise Exception("Not authenticated")

    user_repository = UserRepository()
    user = user_repository.find_one({ "id": user_id })

    investment_repository = InvestmentRepository()
    investment = investment_repository.find_one(user_id, id)

    investment_rentability_repository = InvestmentRentabilityRepository()
    investment_rentabilities = investment_rentability_repository.find()

    investment_source_repository = InvestmentSourceRepository()
    investment_sources = investment_source_repository.find()

    investment_type_repository = InvestmentTypeRepository()
    investment_types = investment_type_repository.find()

    return self.render("/investment/edit", {
      "investment": investment,
      "investment_rentabilities": investment_rentabilities,
      "investment_sources": investment_sources,
      "investment_types": investment_types,
      "user": user,
    })

  def edit(self, id: str) -> None:
    user_id = self.session().get("user_id")
    if not user_id:
      raise Exception("Not authenticated")

    from datetime import datetime

    request = self.request()
    form = request.form()

    investment_repository = InvestmentRepository()
    investment = investment_repository.find_one(user_id, id)
    investment.updated_at = datetime.utcnow().isoformat()
    investment.name = html.escape(form.get("name"))
    investment.type_id = form.get("type")
    investment.source_id = form.get("source")
    investment.invested = form.get("invested")
    investment.total = form.get("total")
    investment.maturity = form.get("maturity") if form.get("maturity") != "" else None
    investment.rentability_id = form.get("rentability_type") if form.get("rentability_type") != "None" else None
    investment.rentability_number = form.get("rentability_number") if form.get("rentability_type") != "None" and form.get("rentability_number") != "" else None

    investment_repository.update(user_id, id, investment)
    return self.redirect("/investment/dashboard")

  def delete(self, id: str) -> None:
    user_id = self.session().get("user_id")
    if not user_id:
      raise Exception("Not authenticated")

    investment_repository = InvestmentRepository()
    investment_repository.remove_one(user_id, id)

    return self.redirect("/investment/dashboard")
