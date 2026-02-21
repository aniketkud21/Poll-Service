from sqlalchemy.orm import Session, joinedload

from models.poll import Poll
from models.question import Question

from uuid import UUID

class PollRepository:

    @staticmethod
    def get_by_id(db: Session, poll_id: UUID) -> Poll | None:
        return (
            db.query(Poll)
            .options(
                joinedload(Poll.questions)
                .joinedload(Question.options)
            )
            .filter(Poll.poll_id == poll_id)
            .first()
        )

    @staticmethod
    def get_all(db: Session) -> list[Poll]:
        return db.query(Poll).all()

    @staticmethod
    def create(db: Session, poll: Poll) -> Poll:
        db.add(poll)
        db.flush()  # important for nested inserts
        return poll

    @staticmethod
    def delete(db: Session, poll: Poll) -> None:
        db.delete(poll)