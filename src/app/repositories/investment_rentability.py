from __core.plugins.database.sql.postgresql import PostgreSQL
from __core.repository import Repository

from app.models import InvestmentRentabilityModel

class InvestmentRentabilityRepository(Repository):
  def __init__(self):
    self.__table = "investment_rentabilities"
    self.__database = PostgreSQL()

  def find(self) -> list[InvestmentRentabilityModel]:
    results = self.__database.select(self.__table, {})
    return [InvestmentRentabilityRepository.__format(item) for item in results]

  @staticmethod
  def __format(data: dict) -> InvestmentRentabilityModel:
    return InvestmentRentabilityModel(
      id=data.get("id"),
      created_at=str(data.get("created_at")),
      updated_at=str(data.get("updated_at")),
      name=data.get("name"),
    )
