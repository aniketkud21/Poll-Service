from fastapi import APIRouter

# Services
from services.option_service import OptionService

from uuid import UUID

router = APIRouter()

@router.post('/')
def create_option(option_text: str, order_index: int, question_id: UUID):
    OptionService.create_option(option_text, order_index, question_id)
    return {'message': 'Option created successfully'}

@router.get('/')
def get_all_options():
    return OptionService.get_all_options()

@router.get('/{option_id}')
def get_option_by_id(option_id: UUID):
    return OptionService.get_option_by_id(option_id)

@router.put('/{option_id}')
def update_option(option_id: UUID, option_text: str, order_index: int):
    OptionService.update_option(option_id, option_text, order_index)
    return {'message': 'Option updated successfully'}

@router.delete('/{option_id}')
def delete_option(option_id: UUID):
    OptionService.delete_option(option_id)
    return {'message': 'Option deleted successfully'}