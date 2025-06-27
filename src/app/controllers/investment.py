import json
import html
import math
from datetime import datetime, timedelta

from __core.controller import Controller

from app.models import InvestmentModel, InvestmentChangeModel
from app.repositories import (
  InvestmentRepository,
  InvestmentChangeRepository,
  InvestmentRentabilityRepository,
  InvestmentSourceRepository,
  InvestmentTypeRepository,
  UserRepository,
)

class InvestmentController(Controller):
  def dashboard(self) -> str:
    user_id = self.session().get("user_id")
    if not user_id:
      return self.redirect("/")

    user_repository = UserRepository()
    user = user_repository.find_one({ "id": user_id })

    start_of_week = self.__start_of_week()
    investment_repository = InvestmentRepository()
    consolidated = investment_repository.consolidated(user_id, start_of_week)

    args = self.request().args()
    page = int(args.get("page")) if args.get("page") else 1
    limit = int(args.get("limit")) if args.get("limit") else 15

    if limit > 15:
      limit = 15

    max_page = math.ceil(consolidated.get("count") / limit)
    if page > max_page:
      page = max_page

    investments = investment_repository.find(user_id, start_of_week, page, limit)
    return self.render("/investment/dashboard", {
      "limit": limit,
      "page": page,
      "count": consolidated.get("count"),
      "investments": investments,
      "invested": round(consolidated.get("invested"), 2),
      "total": round(consolidated.get("total"), 2),
      "gain": round(consolidated.get("gain"), 2),
      "user": user,
    })

  def create_view(self) -> str:
    user_id = self.session().get("user_id")
    if not user_id:
      return self.redirect("/")

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
      return self.redirect("/")

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
      return self.redirect("/")

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
      return self.redirect("/")

    request = self.request()
    form = request.form()

    investment_repository = InvestmentRepository()
    investment = investment_repository.find_one(user_id, id)
    last_invested_value = investment.invested
    last_total_value = investment.total

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

    investment_change_repository = InvestmentChangeRepository()

    last_diff = last_total_value - last_invested_value
    today_diff = float(investment.total) - float(investment.invested)
    diff = today_diff - last_diff

    start_of_week = self.__start_of_week()
    last_investment_change = investment_change_repository.find_one(investment.id, start_of_week)
    if not last_investment_change:
      investment_change_repository.create(InvestmentChangeModel(
        investment_id=investment.id,
        change=diff,
      ))
    else:
      last_investment_change.change = diff
      investment_change_repository.update(last_investment_change.id, last_investment_change)

    return self.redirect("/investment/dashboard")

  def delete(self, id: str) -> None:
    user_id = self.session().get("user_id")
    if not user_id:
      return self.redirect("/")

    investment_repository = InvestmentRepository()
    investment_repository.remove_one(user_id, id)

    return self.redirect("/investment/dashboard")

  # @TODO: generate a new id and create a unique index to fail when
  # try to create the same investment twice
  def import_(self) -> None:
    user_id = self.session().get("user_id")
    if not user_id:
      return self.redirect("/")

    form = self.request().form()
    data = form.get("data")
    if not data:
      raise Exception("Invalid file content")

    investment_repository = InvestmentRepository()
    for item in json.loads(data):
      try:
        investment_repository.create(InvestmentModel(
          user_id=user_id,
          id=item.get("id"),
          type_id=item.get("type_id"),
          source_id=item.get("source_id"),
          name=html.escape(item.get("name")),
          invested=item.get("invested"),
          total=item.get("total"),
          maturity=item.get("maturity"),
          rentability_id=item.get("rentability_id"),
          rentability_number=item.get("rentability_number"),
        ))
      except:
        print(f"Failed to insert item: {item.get("id")} already exists")

    # @BUGFIX: already refreshing using javascript
    return self.redirect("/investment/dashboard")

  def export(self) -> None:
    user_id = self.session().get("user_id")
    if not user_id:
      return self.redirect("/")

    investment_repository = InvestmentRepository()
    investments = investment_repository.find(user_id)
    # @TODO: obfuscate some data: `user_id` and `id`
    dicts = [investment.to_dict() for investment in investments]

    date = datetime.now().strftime("%Y-%m-%d")
    return self.download(f"report_{date}.json", json.dumps(dicts))

  def __start_of_week(self) -> str:
    now = datetime.now()
    start_of_week = now - timedelta(days=now.weekday())
    start_of_week_iso = start_of_week.date().isoformat()
    return start_of_week_iso
