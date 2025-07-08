from __core.plugins.database.sql.postgresql import PostgreSQL
from __core.repository import Repository

from app.models import InvestmentChangeModel

class InvestmentChangeRepository(Repository):
  def __init__(self):
    self.__table = "investment_changes"
    self.__database = PostgreSQL()

  def create(self, data: InvestmentChangeModel) -> str:
    self.__database.insert(self.__table, data.to_dict())
    return data.id

  def create_batch(self, data: list[InvestmentChangeModel]) -> None:
    self.__database.batch_insert(self.__table, "id", [item.to_dict() for item in data])

  def update(self, id: str, new_data: InvestmentChangeModel) -> None:
    self.__database.update(self.__table, { "id": id }, new_data.to_dict())

  def find_one(self, investment_id: str, after_date: str) -> InvestmentChangeModel | None:
    results = self.__database.select(
      table=self.__table,
      limit=1,
      order_by={ "created_at": "desc" },
      where={
        "investment_id": investment_id,
        "created_at": (">=", after_date)
      },
    )
    return InvestmentChangeRepository.__format(results[0]) if len(results) == 1 else None

  def find(self, investment_ids: list[str]) -> list[InvestmentChangeModel]:
    results = self.__database.select(
      table=self.__table,
      order_by={ "created_at": "asc" },
      where={ "investment_id": investment_ids },
    )
    return [InvestmentChangeRepository.__format(item) for item in results]

  @staticmethod
  def __format(data: dict) -> InvestmentChangeModel:
    return InvestmentChangeModel(
      id=data.get("id"),
      investment_id=data.get("investment_id"),
      created_at=str(data.get("created_at")),
      change=float(data.get("change")),
    )
