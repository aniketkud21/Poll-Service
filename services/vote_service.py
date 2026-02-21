from db.session import Session
from models.vote import Vote
from uuid import UUID

class VoteService:
    @staticmethod
    def create_vote(poll_id: UUID, question_id: UUID, option_id: UUID, user_id: UUID):
        with Session() as db:
            vote = Vote(
                poll_id=poll_id,
                question_id=question_id,
                option_id=option_id,
                user_id=user_id
            )

            db.add(vote)
            db.commit()
            db.refresh(vote)
            return vote

    @staticmethod
    def get_vote_by_id(vote_id: UUID) -> Vote | None:
        with Session() as db:
            return db.query(Vote).filter(Vote.vote_id == vote_id).first()

    @staticmethod
    def get_all_votes() -> list[Vote]:
        with Session() as db:
            return db.query(Vote).all()

    @staticmethod
    def update_vote(vote_id: UUID, poll_id: UUID, question_id: UUID, option_id: UUID) -> Vote | None:
        with Session() as db:
            vote = db.query(Vote).filter(Vote.vote_id == vote_id).first()
            if vote is None:
                return None
            vote.poll_id = poll_id
            vote.question_id = question_id
            vote.option_id = option_id
            db.commit()
            db.refresh(vote)
            return vote

    @staticmethod
    def delete_vote(vote_id: UUID) -> None:
        with Session() as db:
            vote = db.query(Vote).filter(Vote.vote_id == vote_id).first()
            if vote:
                db.delete(vote)
                db.commit()
