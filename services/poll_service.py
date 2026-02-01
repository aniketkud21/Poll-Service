from db.session import Session
from models.poll import Poll
from repositories.poll_repository import PollRepository
from uuid import UUID
from datetime import datetime, timedelta, timezone

DEFAULT_POLL_DURATION_DAYS = 7

class PollService:
    @staticmethod
    def create_poll(title: str, description: str | None, ends_at: datetime | None):
        if ends_at is None:
            ends_at = datetime.now(timezone.utc) + timedelta(days=DEFAULT_POLL_DURATION_DAYS)

        with Session() as db:
            repo = PollRepository(db)

            poll = Poll(
                title=title,
                description=description,
                ends_at=ends_at,
            )

            repo.create(poll)
            db.commit()
            return poll

    def get_poll_by_id(poll_id: UUID) -> Poll | None:
        with Session() as db:
            repo = PollRepository(db)
            return repo.get_by_id(poll_id)

    def get_all_polls() -> list[Poll]:
        with Session() as db:
            repo = PollRepository(db)
            return repo.list()
    def update_poll(poll_id: UUID, title: str, description: str | None, ends_at: datetime) -> Poll | None:
        with Session() as db:
            repo = PollRepository(db)
            poll = repo.get_by_id(poll_id)
            if poll is None:
                return None
            poll.title = title
            poll.description = description
            poll.ends_at = ends_at
            repo.update(poll)
            db.commit()
            return poll

    def delete_poll(poll_id: UUID) -> None:
        with Session() as db:
            repo = PollRepository(db)
            poll = repo.get_by_id(poll_id)
            if poll is None:
                return None
            repo.delete(poll)
            db.commit()
