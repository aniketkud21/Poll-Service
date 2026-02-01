from db.session import Session
from models.question import Question
from repositories.question_repository import QuestionRepository
from uuid import UUID
from datetime import datetime

class QuestionService:
    @staticmethod
    def create_question(question_text: str, order_index: int):
        with Session() as db:
            repo = QuestionRepository(db)

            question = Question(
                question_text=question_text,
                order_index=order_index,
            )

            repo.create(question)
            db.commit()
            return question

    def get_question_by_id(question_id: UUID) -> Question | None:
        with Session() as db:
            repo = QuestionRepository(db)
            return repo.get_by_id(question_id)

    def get_all_questions() -> list[Question]:
        with Session() as db:
            repo = QuestionRepository(db)
            return repo.list()
    def update_question(question_id: UUID, question_text: str, order_index: int) -> Question | None:
        with Session() as db:
            repo = QuestionRepository(db)
            question = repo.get_by_id(question_id)
            if question is None:
                return None
            question.question_text = question_text
            question.order_index = order_index
            repo.update(question)
            db.commit()
            return question

    def delete_question(question_id: UUID) -> None:
        with Session() as db:
            repo = QuestionRepository(db)
            question = repo.get_by_id(question_id)
            if question is None:
                return None
            repo.delete(question)
            db.commit()
