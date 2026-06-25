from __core.plugins.cache.memory import Memory
from __core.plugins.database.sql.sqlite import SQLite
from __core.repository import Repository

from app.models import InvestmentTypeModel

class InvestmentTypeRepository(Repository):
  def __init__(self):
    self.__table = "investment_types"
    self.__database = SQLite()
    self.__cache = Memory()

  def find(self) -> list[InvestmentTypeModel]:
    data = self.__cache.read_json("InvestmentTypeRepository::find")
    if data:
      return data

    results = self.__database.select(self.__table, {})
    data = [InvestmentTypeRepository.__format(item) for item in results]
    self.__cache.write_json("InvestmentTypeRepository::find", data)
    return data

  @staticmethod
  def __format(data: dict) -> InvestmentTypeModel:
    return InvestmentTypeModel(
      id=data.get("id"),
      created_at=str(data.get("created_at")),
      updated_at=str(data.get("updated_at")),
      name=data.get("name"),
      code=data.get("code"),
      color=data.get("color"),
    )
