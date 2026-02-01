from sqlalchemy.orm import Session
from models.option import Option
from uuid import UUID

class OptionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, option: Option) -> Option:
        self.db.add(option)
        self.db.flush()
        self.db.refresh(option)
        return option

    def get_by_id(self, option_id: UUID) -> Option | None:
        return (
            self.db
            .query(Option)
            .filter(Option.option_id == option_id)
            .first()
        )

    def list(self) -> list[Option]:
        return self.db.query(Option).all()

    def delete(self, option: Option) -> None:
        self.db.delete(option)
