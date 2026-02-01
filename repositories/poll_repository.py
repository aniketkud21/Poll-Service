from sqlalchemy.orm import Session
from models.poll import Poll
from uuid import UUID

class PollRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, poll: Poll) -> Poll:
        self.db.add(poll)
        self.db.flush()
        self.db.refresh(poll)
        return poll

    def get_by_id(self, poll_id: UUID) -> Poll | None:
        return (
            self.db
            .query(Poll)
            .filter(Poll.poll_id == poll_id)
            .first()
        )

    def list(self) -> list[Poll]:
        return self.db.query(Poll).all()

    def delete(self, poll: Poll) -> None:
        self.db.delete(poll)
