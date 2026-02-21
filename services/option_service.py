from db.session import Session
from models.option import Option
from uuid import UUID

class OptionService:
    @staticmethod
    def create_option(option_text: str, order_index: int, question_id: UUID):
        with Session() as db:
            option = Option(
                option_text=option_text,
                order_index=order_index,
                question_id=question_id,
            )

            db.add(option)
            db.commit()
            db.refresh(option)
            return option

    @staticmethod
    def get_option_by_id(option_id: UUID) -> Option | None:
        with Session() as db:
            return db.query(Option).filter(Option.option_id == option_id).first()

    @staticmethod
    def get_all_options() -> list[Option]:
        with Session() as db:
            return db.query(Option).all()

    @staticmethod
    def update_option(option_id: UUID, option_text: str, order_index: int) -> Option | None:
        with Session() as db:
            option = db.query(Option).filter(Option.option_id == option_id).first()
            if option is None:
                return None
            option.option_text = option_text
            option.order_index = order_index
            db.commit()
            db.refresh(option)
            return option

    @staticmethod
    def delete_option(option_id: UUID) -> None:
        with Session() as db:
            option = db.query(Option).filter(Option.option_id == option_id).first()
            if option:
                db.delete(option)
                db.commit()
