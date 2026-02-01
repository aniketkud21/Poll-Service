from db.session import Session
from models.vote import Vote
from repositories.vote_repository import VoteRepository
from uuid import UUID
from datetime import datetime

class VoteService:
    @staticmethod
    def create_vote(vote: Vote):
        with Session() as db:
            repo = VoteRepository(db)

            vote = Vote(
                poll_id=poll_id,
                question_id=question_id,
                option_id=option_id,
            )

            repo.create(vote)
            db.commit()
            return vote

    def get_vote_by_id(vote_id: UUID) -> Vote | None:
        with Session() as db:
            repo = VoteRepository(db)
            return repo.get_by_id(vote_id)

    def get_all_votes() -> list[Vote]:
        with Session() as db:
            repo = VoteRepository(db)
            return repo.list()
    def update_vote(vote_id: UUID, poll_id: UUID, question_id: UUID, option_id: UUID) -> Vote | None:
        with Session() as db:
            repo = VoteRepository(db)
            vote = repo.get_by_id(vote_id)
            if vote is None:
                return None
            vote.poll_id = poll_id
            vote.question_id = question_id
            vote.option_id = option_id
            repo.update(vote)
            db.commit()
            return vote

    def delete_vote(vote_id: UUID) -> None:
        with Session() as db:
            repo = VoteRepository(db)
            vote = repo.get_by_id(vote_id)
            if vote is None:
                return None
            repo.delete(vote)
            db.commit()
