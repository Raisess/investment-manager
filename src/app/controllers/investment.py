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

    # --- Setup parameters ---

    args = self.request().args()
    page = int(args.get("page")) if args.get("page") else 1
    limit = int(args.get("limit")) if args.get("limit") else 15

    start_of_week = self.__start_of_week()
    start_of_month = self.__start_of_month()

    order_by = None
    order_by_arg = args.get("order") or args.get("order_by")
    if order_by_arg:
      _map = {
        "total": "total",
        "invested": "invested",
        "week_change": "fk_change",
      }
      order_by = _map.get(order_by_arg)

    # --- Setup parameters ---

    user_repository = UserRepository()
    user = user_repository.find_one({ "id": user_id })

    investment_repository = InvestmentRepository()
    consolidated = investment_repository.consolidated(user.id, start_of_week, start_of_month)

    if limit > 15:
      limit = 15

    max_page = math.ceil(consolidated.get("count") / limit)
    if page > max_page:
      page = max_page

    investments = investment_repository.find(user_id, start_of_week, page, limit, order_by)
    return self.render("/investment/dashboard", {
      "limit": limit,
      "page": page,
      "count": consolidated.get("count") or 0,
      "investments": investments,
      "invested": round(consolidated.get("invested") or 0, 2),
      "total": round(consolidated.get("total") or 0, 2),
      "total_gains": round((consolidated.get("total") or 0) - (consolidated.get("invested") or 0), 2),
      "monthly_gains": round(consolidated.get("monthly_gains") or 0, 2),
      "week_gains": round(consolidated.get("week_gains") or 0, 2),
      "user": user,
    })

  def chart(self, id: str) -> str:
    user_id = self.session().get("user_id")
    if not user_id:
      return self.redirect("/")

    user_repository = UserRepository()
    user = user_repository.find_one({ "id": user_id })

    investment_repository = InvestmentRepository()
    investements = investment_repository.find(user.id)
    investements_ids = [investement.id for investement in investements]

    investement_change_repository = InvestmentChangeRepository()
    # TODO: need to limit it to a limit that is visually good
    investement_changes = investement_change_repository.find(investements_ids)

    bar_labels = []
    for investement_change in investement_changes:
      if investement_change.created_at not in bar_labels:
        bar_labels.append(investement_change.created_at)

    bar_datasets = []
    doughnut_data = {}
    for investement in investements:
      filtered_changes_by_date = {}
      for investement_change in investement_changes:
        if investement_change.investment_id == investement.id:
          filtered_changes_by_date[investement_change.created_at] = round(investement_change.change, 2)

      for label in bar_labels:
        if not filtered_changes_by_date.get(label):
          filtered_changes_by_date[label] = 0

      filtered_changes_by_date = dict(sorted(filtered_changes_by_date.items()))
      bar_datasets.append({
        "label": investement.name,
        "data": list(filtered_changes_by_date.values()),
        "hidden": 0 if investement.id == id else 1,
        "backgroundColor": f"#{investement.fk_type.color}",
      })

      if not doughnut_data.get(investement.fk_type.name):
        doughnut_data[investement.fk_type.name] = {
          "color": f"#{investement.fk_type.color}",
          "total": investement.total,
        }
      else:
        doughnut_data[investement.fk_type.name]["total"] += investement.total

    doughnut_labels = list(doughnut_data.keys())
    doughnut_datasets = [{ "data": [], "backgroundColor": [] }]
    for item in list(doughnut_data.values()):
      doughnut_datasets[0]["backgroundColor"].append(item["color"])
      doughnut_datasets[0]["data"].append(item["total"])

    return self.render("/investment/chart", {
      "investment": investement,
      "user": user,
      "bar": {
        "labels": bar_labels,
        "datasets": bar_datasets,
      },
      "doughnut": {
        "labels": doughnut_labels,
        "datasets": doughnut_datasets,
      },
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

    if form.get("maturity") != "":
      investment.maturity = form.get("maturity")

    if form.get("rentability_type") != "None":
      investment.rentability_id = form.get("rentability_type")

    if form.get("rentability_type") != "None" and form.get("rentability_number") != "":
      investment.rentability_number = form.get("rentability_number")

    investment_repository.update(user_id, id, investment)

    start_of_week = self.__start_of_week()
    last_diff = last_total_value - last_invested_value
    today_diff = float(investment.total) - float(investment.invested)
    diff = today_diff - last_diff

    investment_change_repository = InvestmentChangeRepository()
    last_investment_change = investment_change_repository.find_one(investment.id, start_of_week)
    if not last_investment_change:
      investment_change_repository.create(InvestmentChangeModel(
        investment_id=investment.id,
        change=diff,
        created_at=start_of_week,
      ))
    else:
      last_investment_change.change += diff
      investment_change_repository.update(last_investment_change.id, last_investment_change)

    return self.redirect("/investment/dashboard")

  def delete(self, id: str) -> None:
    user_id = self.session().get("user_id")
    if not user_id:
      return self.redirect("/")

    investment_repository = InvestmentRepository()
    investment_repository.remove_one(user_id, id)

    return self.redirect("/investment/dashboard")

  def import_(self) -> None:
    user_id = self.session().get("user_id")
    if not user_id:
      return self.redirect("/")

    form = self.request().form()
    data = form.get("data")
    if not data:
      raise Exception("Invalid file content")

    investment_repository = InvestmentRepository()
    investment_change_repository = InvestmentChangeRepository()

    investments = []
    investments_changes = []
    for item in json.loads(data):
      investments.append(InvestmentModel(
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
        created_at=item.get("created_at"),
        updated_at=item.get("updated_at"),
      ))

      change_items = item.get("changes")
      if change_items and len(change_items) > 0:
        for change_item in change_items:
          investments_changes.append(InvestmentChangeModel(
            id=change_item.get("id"),
            investment_id=change_item.get("investment_id"),
            change=change_item.get("change"),
            created_at=change_item.get("created_at"),
          ))

    investment_repository.create_batch(investments)
    investment_change_repository.create_batch(investments_changes)
    # @BUGFIX: already refreshing using javascript
    return self.redirect("/investment/dashboard")

  def export(self) -> None:
    user_id = self.session().get("user_id")
    if not user_id:
      return self.redirect("/")

    investment_repository = InvestmentRepository()
    investments = investment_repository.find(user_id)

    investment_change_repository = InvestmentChangeRepository()
    investments_changes = investment_change_repository.find([investment.id for investment in investments])

    dicts = []
    for investment in investments:
      item = investment.to_dict()
      item["user_id"] = None
      item["changes"] = [investment_change.to_dict()
                         for investment_change in investments_changes
                         if investment_change.investment_id == item.get("id")]

      dicts.append(item)

    date = datetime.now().strftime("%Y-%m-%d")
    return self.download(f"report_{date}.json", json.dumps(dicts))

  def __start_of_week(self) -> str:
    now = datetime.utcnow()
    start_of_week = now - timedelta(days=now.weekday())
    start_of_week_iso = start_of_week.date().isoformat()
    return start_of_week_iso

  def __start_of_month(self) -> str:
    now = datetime.utcnow()
    # @NOTE: Sum 1 because 2026-10-05 - 05 days is 2026-10-00 == 2026-09-30 which is wrong
    start_of_month = now - timedelta(days=now.day) + timedelta(days=1)
    start_of_month_iso = start_of_month.date().isoformat()
    return start_of_month_iso
