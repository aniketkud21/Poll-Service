from api.schemas.poll import PollCreate
from services.poll_service import PollService
import pytest

def test_create_poll(db_session):
    payload = PollCreate(
        title="Test Poll",
        poll_type="POLL",
        questions=[
            {
                "question_text": "Favorite language?",
                "question_type": "SINGLE_CHOICE",
                "order_index": 1,
                "options": [
                    {"option_text": "Python", "order_index": 1},
                    {"option_text": "Go", "order_index": 2},
                ]
            }
        ]
    )

    poll = PollService.create_poll(payload)

    assert poll.poll_id is not None
    assert len(poll.questions) == 1
    assert len(poll.questions[0].options) == 2
