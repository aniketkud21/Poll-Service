from sqlalchemy.orm import Session, joinedload
from models.question import Question

from uuid import UUID

class QuestionRepository:

    @staticmethod
    def get_by_id(db: Session, question_id: UUID) -> Question | None:
        return (
            db.query(Question)
            .options(
                joinedload(Question.options)
            )
            .filter(Question.question_id == question_id)
            .first()
        )

    @staticmethod
    def get_all(db: Session) -> list[Question]:
        return db.query(Question).all()

    @staticmethod
    def create(db: Session, question: Question) -> Question:
        db.add(question)
        db.flush()
        return question

    @staticmethod
    def delete(db: Session, question: Question) -> None:
        db.delete(question)