from sqlalchemy.orm import Session
from models.question import Question
from uuid import UUID

class QuestionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, question: Question) -> Question:
        self.db.add(question)
        self.db.flush()
        self.db.refresh(question)
        return question

    def get_by_id(self, question_id: UUID) -> Question | None:
        return (
            self.db
            .query(Question)
            .filter(Question.question_id == question_id)
            .first()
        )

    def list(self) -> list[Question]:
        return self.db.query(Question).all()

    def delete(self, question: Question) -> None:
        self.db.delete(question)
