from sqlalchemy.orm import Session
from models.option import Option

from uuid import UUID

class OptionRepository:

    @staticmethod
    def get_by_id(db: Session, option_id: UUID) -> Option | None:
        return (
            db.query(Option)
            .filter(Option.option_id == option_id)
            .first()
        )

    @staticmethod
    def get_all(db: Session) -> list[Option]:
        return db.query(Option).all()

    @staticmethod
    def create(db: Session, option: Option) -> Option:
        db.add(option)
        db.flush()
        return option

    @staticmethod
    def delete(db: Session, option: Option) -> None:
        db.delete(option)