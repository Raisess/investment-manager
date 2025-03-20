from __core.plugins.database.sql.postgresql import PostgreSQL
from __core.repository import Repository

from app.models import UserModel

class UserRepository(Repository):
  def __init__(self):
    self.__table = "users"
    self.__database = PostgreSQL()

  def create(self, data: UserModel) -> str:
    self.__database.insert(self.__table, data.to_dict())
    return data.id

  def update(self, id: str, new_data: UserModel) -> None:
    self.__database.update(self.__table, { "id": id }, new_data.to_dict())

  def find_one(self, filter: dict) -> UserModel | None:
    results = self.__database.select(self.__table, filter)
    return UserRepository.__format(results[0]) if len(results) > 0 else None

  @staticmethod
  def __format(data: dict) -> UserModel:
    return UserModel(
      id=data.get("id"),
      created_at=str(data.get("created_at")),
      updated_at=str(data.get("updated_at")),
      name=data.get("name"),
      email=data.get("email"),
      picture=data.get("picture"),
      status=data.get("status"),
    )
