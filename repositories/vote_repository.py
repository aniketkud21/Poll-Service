from sqlalchemy.orm import Session
from models.vote import Vote
from uuid import UUID

class VoteRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, vote: Vote) -> Vote:
        self.db.add(vote)
        self.db.flush()
        self.db.refresh(vote)
        return vote

    def get_by_id(self, vote_id: UUID) -> Vote | None:
        return (
            self.db
            .query(Vote)
            .filter(Vote.vote_id == vote_id)
            .first()
        )

    def list(self) -> list[Vote]:
        return self.db.query(Vote).all()

    def delete(self, vote: Vote) -> None:
        self.db.delete(vote)
