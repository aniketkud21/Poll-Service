from fastapi import APIRouter

# Services
from services.question_service import QuestionService

from uuid import UUID

router = APIRouter()

@router.post('/')
def create_question(question_text: str, question_type: str, poll_id: UUID, order_index: int = 1):
    QuestionService.create_question(question_text, question_type, poll_id, order_index)
    return {'message': 'Question created successfully'}

@router.get('/')
def get_all_questions():
    return QuestionService.get_all_questions()

@router.get('/{question_id}')
def get_question_by_id(question_id: UUID):
    return QuestionService.get_question_by_id(question_id)

@router.put('/{question_id}')
def update_question(question_id: UUID, question_text: str, question_type: str, order_index: int | None = None):
    QuestionService.update_question(question_id, question_text, question_type, order_index)
    return {'message': 'Question updated successfully'}

@router.delete('/{question_id}')
def delete_question(question_id: UUID):
    QuestionService.delete_question(question_id)
    return {'message': 'Question deleted successfully'}