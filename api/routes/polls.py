from fastapi import APIRouter

# API Schemas
from api.schemas.poll import PollCreate, PollUpdate

# Services
from services.poll_service import PollService

from uuid import UUID

router = APIRouter()

@router.get('/')
def get_all_polls():
    return PollService.get_all_polls()

@router.get('/{poll_id}')
def get_poll_by_id(poll_id: UUID):
    return PollService.get_poll_by_id(poll_id)

@router.post('/')
def create_poll(poll: PollCreate):
    created_poll = PollService.create_poll(poll)
    return {
        "poll_id": created_poll.poll_id,
        "message": "Poll created successfully"
    }

@router.put('/{poll_id}')
def update_poll(poll_id: UUID, payload: PollUpdate):
    updated_poll = PollService.update_poll(poll_id, payload)
    return {
        "poll_id": updated_poll.poll_id,
        "message": "Poll updated successfully"
    }

@router.delete('/{poll_id}')
def delete_poll(poll_id: UUID):
    PollService.delete_poll(poll_id)
    return {'message': 'Poll deleted successfully'}