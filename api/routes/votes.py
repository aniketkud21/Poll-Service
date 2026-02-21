from fastapi import APIRouter

# Services
from services.vote_service import VoteService

from uuid import UUID

router = APIRouter()

@router.post('/')
def create_vote(poll_id: UUID, question_id: UUID, option_id: UUID, user_id: UUID):
    VoteService.create_vote(poll_id, question_id, option_id, user_id)
    return {'message': 'Vote created successfully'}

@router.get('/')
def get_all_votes():
    return VoteService.get_all_votes()

@router.get('/{vote_id}')
def get_vote_by_id(vote_id: UUID):
    return VoteService.get_vote_by_id(vote_id)

@router.put('/{vote_id}')
def update_vote(vote_id: UUID, poll_id: UUID, question_id: UUID, option_id: UUID):
    VoteService.update_vote(vote_id, poll_id, question_id, option_id)
    return {'message': 'Vote updated successfully'}

@router.delete('/{vote_id}')
def delete_vote(vote_id: UUID):
    VoteService.delete_vote(vote_id)
    return {'message': 'Vote deleted successfully'}