from db.session import Session
from models.question import Question
from uuid import UUID
from datetime import datetime

class QuestionService:
    @staticmethod
    def create_question(question_text: str, question_type: str, poll_id: UUID, order_index: int | None = None):
        if order_index is None:
            order_index = 0

        with Session() as db:
            question = Question(
                question_text=question_text,
                question_type=question_type,
                order_index=order_index,
                poll_id=poll_id,
            )

            db.add(question)
            db.commit()
            db.refresh(question)
            return question

    @staticmethod
    def get_question_by_id(question_id: UUID) -> Question | None:
        with Session() as db:
            return db.query(Question).filter(Question.question_id == question_id).first()

    @staticmethod
    def get_all_questions() -> list[Question]:
        with Session() as db:
            return db.query(Question).all()

    @staticmethod
    def update_question(question_id: UUID, question_text: str, question_type: str, order_index: int | None) -> Question | None:
        with Session() as db:
            question = db.query(Question).filter(Question.question_id == question_id).first()
            if question is None:
                return None
            question.question_text = question_text
            question.question_type = question_type
            question.order_index = order_index
            db.commit()
            db.refresh(question)
            return question

    @staticmethod
    def delete_question(question_id: UUID) -> None:
        with Session() as db:
            question = db.query(Question).filter(Question.question_id == question_id).first()
            if question:
                db.delete(question)
                db.commit()
