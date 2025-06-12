from __core.plugins.database.sql.postgresql import PostgreSQL
from __core.repository import Repository

from app.models import (
  InvestmentModel,
  InvestmentRentabilityModel,
  InvestmentSourceModel,
  InvestmentTypeModel,
)

class InvestmentRepository(Repository):
  def __init__(self):
    self.__table = "investments"
    self.__database = PostgreSQL()

  def create(self, data: InvestmentModel) -> str:
    self.__database.insert(self.__table, data.to_dict())
    return data.id

  def find(self, user_id: str) -> list[InvestmentModel]:
    query = f"""
      SELECT
        main_table.*,
        fk_type.name AS fk_type_name,
        fk_type.code AS fk_type_code,
        fk_type.color AS fk_type_color,
        fk_source.name AS fk_source_name,
        fk_source.code AS fk_source_code,
        fk_source.logo AS fk_source_logo,
        fk_rentability.name AS fk_rentability_name
      FROM {self.__table} AS main_table
        INNER JOIN investment_types AS fk_type ON fk_type.id = type_id
        INNER JOIN investment_sources AS fk_source ON fk_source.id = source_id
        LEFT OUTER JOIN investment_rentabilities AS fk_rentability ON fk_rentability.id = rentability_id
      WHERE user_id = %(user_id)s
      ORDER BY updated_at DESC;
    """
    results = self.__database.query(query, { "user_id": user_id })
    return [InvestmentRepository.__format(item) for item in results]

  def find_one(self, user_id: str, id: str) -> InvestmentModel | None:
    result = self.__database.select(self.__table, { "id": id, "user_id": user_id })
    return InvestmentRepository.__format(result[0]) if len(result) > 0 else None

  def update(self, user_id: str, id: str, new_data: InvestmentModel) -> None:
    self.__database.update(self.__table, { "id": id, "user_id": user_id }, new_data.to_dict())

  def remove_one(self, user_id: str, id: str) -> None:
    self.__database.delete(self.__table, { "id": id, "user_id": user_id })

  @staticmethod
  def __format(data: dict) -> InvestmentModel:
    return InvestmentModel(
      id=data.get("id"),
      created_at=str(data.get("created_at")),
      updated_at=str(data.get("updated_at")),
      user_id=data.get("user_id"),
      name=data.get("name"),
      invested=float(data.get("invested")),
      total=float(data.get("total")),
      maturity=str(data.get("maturity")) if data.get("maturity") else None,

      type_id=data.get("type_id"),
      fk_type=InvestmentTypeModel(
        name=data.get("fk_type_name"),
        code=data.get("fk_type_code"),
        color=data.get("fk_type_color"),
      ) if data.get("fk_type_code") and data.get("fk_type_color") else None,

      source_id=data.get("source_id"),
      fk_source=InvestmentSourceModel(
        name=data.get("fk_source_name"),
        code=data.get("fk_source_code"),
        logo=data.get("fk_source_logo") if data.get("fk_source_logo") else None,
      ),

      rentability_id=data.get("rentability_id"),
      rentability_number=str(data.get("rentability_number")),
      fk_rentability=InvestmentRentabilityModel(
        name=data.get("fk_rentability_name"),
      ) if data.get("rentability_id") else None,
    )
