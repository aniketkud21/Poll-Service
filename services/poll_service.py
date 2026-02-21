# Database
from db.session import Session

# API Schemas
from api.schemas.poll import PollCreate, PollUpdate

# DB Models
from models.poll import Poll
from models.question import Question
from models.option import Option

# Repositories/ Query Handlers
from repositories.poll_repository import PollRepository
from repositories.question_repository import QuestionRepository
from repositories.option_repository import OptionRepository

from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import joinedload

class PollService:

    @staticmethod
    def get_poll_by_id(poll_id: UUID) -> Poll | None:
        """
        Retrieve a poll by its ID with all nested questions and options.

        This method loads the full poll hierarchy using eager loading to avoid
        lazy loading issues after the session closes.

        Args:
            poll_id (UUID): Unique identifier of the poll.

        Returns:
            Poll | None: The poll if found, otherwise None.
        """
        with Session() as db:
            return PollRepository.get_by_id(db, poll_id)

    @staticmethod
    def get_all_polls() -> list[Poll]:
        """
        Retrieve all polls from the database.

        Returns:
            list[Poll]: List of all poll records.
        """
        with Session() as db:
            return PollRepository.get_all(db)

    @staticmethod
    def create_poll(payload: PollCreate):
        """
        Create a new poll along with its nested questions and options.

        This method constructs the full object tree in memory and persists
        it in a single transaction.

        Args:
            payload (PollCreate): Data for creating the poll.

        Returns:
            Poll: The created poll with nested questions and options.
        """
        with Session() as db:
            try:
                # Construct the nested model tree
                poll_model = Poll(
                    title=payload.title,
                    type=payload.poll_type,
                    description=payload.description,
                    status=payload.status,
                    ends_at=payload.ends_at,
                )

                for question_payload in payload.questions:
                    question_model = Question(
                        question_text=question_payload.question_text,
                        question_type=question_payload.question_type,
                        order_index=question_payload.order_index,
                    )
                    
                    for option_payload in question_payload.options:
                        option_model = Option(
                            option_text=option_payload.option_text,
                            order_index=option_payload.order_index,
                        )
                        question_model.options.append(option_model)
                    
                    poll_model.questions.append(question_model)

                db.add(poll_model)
                db.commit()
                db.refresh(poll_model)

                # Force load relationships to avoid DetachedInstanceError after session closure
                for q in poll_model.questions:
                    for o in q.options:
                        pass

                return poll_model

            except Exception as e:
                db.rollback()
                raise e

    @staticmethod
    def _update_poll_fields(poll, payload):
        if payload.title is not None:
            poll.title = payload.title

        if payload.description is not None:
            poll.description = payload.description

        if payload.status is not None:
            poll.status = payload.status

        if payload.ends_at is not None:
            poll.ends_at = payload.ends_at

    @staticmethod
    def _update_question(question, payload):
        question.question_text = payload.question_text
        question.question_type = payload.question_type
        question.order_index = payload.order_index

    @staticmethod
    def _create_question(poll, payload):
        question = Question(
            question_text=payload.question_text,
            question_type=payload.question_type,
            order_index=payload.order_index,
        )
        poll.questions.append(question)
        return question

    @staticmethod
    def _sync_questions(db, poll, question_payloads):
        existing_map = {q.question_id: q for q in poll.questions}
        incoming_ids = set()

        for question_payload in question_payloads:
            if question_payload.question_id:
                question = existing_map.get(question_payload.question_id)
                if not question:
                    continue

                incoming_ids.add(question.question_id)
                PollService._update_question(question, question_payload)

            else:
                question = PollService._create_question(poll, question_payload)
                db.flush()

            PollService._sync_options(db, question, question_payload.options)

        # delete removed questions
        for question in poll.questions[:]:
            if question.question_id not in incoming_ids:
                QuestionRepository.delete(db, question)

    @staticmethod
    def _sync_options(db, question, option_payloads):

        existing_map = {o.option_id: o for o in question.options}
        incoming_ids = set()

        for o_payload in option_payloads:

            if o_payload.option_id:
                option = existing_map.get(o_payload.option_id)
                if not option:
                    continue

                incoming_ids.add(option.option_id)
                option.option_text = o_payload.option_text
                option.order_index = o_payload.order_index

            else:
                option = Option(
                    option_text=o_payload.option_text,
                    order_index=o_payload.order_index,
                )
                question.options.append(option)

        # delete removed options
        for option in question.options[:]:
            if option.option_id and option.option_id not in incoming_ids:
                OptionRepository.delete(db, option)

    @staticmethod
    def update_poll(poll_id, payload: PollUpdate):
        """
        Update an existing poll and synchronize its nested questions and options.

        This performs a full sync operation:
        - Updates poll fields
        - Creates new questions/options
        - Updates existing ones
        - Deletes removed ones

        Args:
            poll_id (UUID): Poll identifier.
            payload (PollUpdate): Update payload.

        Returns:
            Poll | None: Updated poll if found, otherwise None.

        Raises:
            Exception: If transaction fails.
        """
        with Session() as db:
            try:
                poll = PollRepository.get_by_id(db, poll_id)
                
                if not poll:
                    return None

                PollService._update_poll_fields(poll, payload)
                PollService._sync_questions(db, poll, payload.questions)

                db.commit()
                db.refresh(poll)
                return poll

            except Exception:
                db.rollback()
                raise

    @staticmethod
    def delete_poll(poll_id: UUID) -> None:
        """
        Delete a poll by its ID.

        Args:
            poll_id (UUID): Poll identifier.

        Returns:
            None
        """
        with Session() as db:
            poll = PollRepository.get_by_id(db, poll_id)
            if poll:
                PollRepository.delete(db, poll)
                db.commit()