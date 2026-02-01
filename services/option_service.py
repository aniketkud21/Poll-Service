from db.session import Session
from models.option import Option
from repositories.option_repository import OptionRepository
from uuid import UUID

class OptionService:
    @staticmethod
    def create_option(option_text: str, order_index: int):
        with Session() as db:
            repo = OptionRepository(db)

            option = Option(
                option_text=option_text,
                order_index=order_index,
            )

            repo.create(option)
            db.commit()
            return option

    def get_option_by_id(option_id: UUID) -> Option | None:
        with Session() as db:
            repo = OptionRepository(db)
            return repo.get_by_id(option_id)

    def get_all_options() -> list[Option]:
        with Session() as db:
            repo = OptionRepository(db)
            return repo.list()
    def update_option(option_id: UUID, option_text: str, order_index: int) -> Option | None:
        with Session() as db:
            repo = OptionRepository(db)
            option = repo.get_by_id(option_id)
            if option is None:
                return None
            option.option_text = option_text
            option.order_index = order_index
            repo.update(option)
            db.commit()
            return option

    def delete_option(option_id: UUID) -> None:
        with Session() as db:
            repo = OptionRepository(db)
            option = repo.get_by_id(option_id)
            if option is None:
                return None
            repo.delete(option)
            db.commit()
