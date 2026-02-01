from fastapi import FastAPI
from services.poll_service import PollService
from services.question_service import QuestionService
from services.option_service import OptionService
from services.vote_service import VoteService
from datetime import datetime
from uuid import UUID

from db.init_db import init_db

app = FastAPI(title="Poll Service", description="Poll Service API", version="1.0.0")

@app.on_event("startup")
def on_startup():
    init_db()  # ✅ OK for now (dev / pre-Alembic)

@app.get('/')
def home():
    return {'message': 'Welcome to the Poll System'}

@app.get('/health')
def health():
    return {'message': 'OK'}

@app.post('/polls')
def create_poll(title: str, description: str | None, ends_at: datetime | None = None):
    PollService.create_poll(title, description, ends_at)
    return {'message': 'Poll created successfully'}

@app.get('/polls')
def get_all_polls():
    return PollService.get_all_polls()

@app.get('/polls/{poll_id}')
def get_poll_by_id(poll_id: UUID):
    return PollService.get_poll_by_id(poll_id)

@app.put('/polls/{poll_id}')
def update_poll(poll_id: UUID, title: str, description: str | None, ends_at: datetime):
    PollService.update_poll(poll_id, title, description, ends_at)
    return {'message': 'Poll updated successfully'}

@app.delete('/polls/{poll_id}')
def delete_poll(poll_id: UUID):
    PollService.delete_poll(poll_id)
    return {'message': 'Poll deleted successfully'}

@app.post('/questions')
def create_question(question_text: str, order_index: int):
    QuestionService.create_question(question_text, order_index)
    return {'message': 'Question created successfully'}

@app.get('/questions')
def get_all_questions():
    return QuestionService.get_all_questions()

@app.get('/questions/{question_id}')
def get_question_by_id(question_id: UUID):
    return QuestionService.get_question_by_id(question_id)

@app.put('/questions/{question_id}')
def update_question(question_id: UUID, question_text: str, order_index: int):
    QuestionService.update_question(question_id, question_text, order_index)
    return {'message': 'Question updated successfully'}

@app.delete('/questions/{question_id}')
def delete_question(question_id: UUID):
    QuestionService.delete_question(question_id)
    return {'message': 'Question deleted successfully'}

@app.post('/options')
def create_option(option_text: str, order_index: int):
    OptionService.create_option(option_text, order_index)
    return {'message': 'Option created successfully'}

@app.get('/options')
def get_all_options():
    return OptionService.get_all_options()

@app.get('/options/{option_id}')
def get_option_by_id(option_id: UUID):
    return OptionService.get_option_by_id(option_id)

@app.put('/options/{option_id}')
def update_option(option_id: UUID, option_text: str, order_index: int):
    OptionService.update_option(option_id, option_text, order_index)
    return {'message': 'Option updated successfully'}

@app.delete('/options/{option_id}')
def delete_option(option_id: UUID):
    OptionService.delete_option(option_id)
    return {'message': 'Option deleted successfully'}

@app.post('/votes')
def create_vote(poll_id: UUID, question_id: UUID, option_id: UUID):
    VoteService.create_vote(poll_id, question_id, option_id)
    return {'message': 'Vote created successfully'}

@app.get('/votes')
def get_all_votes():
    return VoteService.get_all_votes()

@app.get('/votes/{vote_id}')
def get_vote_by_id(vote_id: UUID):
    return VoteService.get_vote_by_id(vote_id)

@app.put('/votes/{vote_id}')
def update_vote(vote_id: UUID, poll_id: UUID, question_id: UUID, option_id: UUID):
    VoteService.update_vote(vote_id, poll_id, question_id, option_id)
    return {'message': 'Vote updated successfully'}

@app.delete('/votes/{vote_id}')
def delete_vote(vote_id: UUID):
    VoteService.delete_vote(vote_id)
    return {'message': 'Vote deleted successfully'}
