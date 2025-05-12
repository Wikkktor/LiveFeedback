from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from models import User

from crud import crud_feedback
from schemas.feedback import FeedbackCreate, FeedbackUpdate, FeedbackInDB
from api.deps import (
    get_db,
    get_current_user,
)

router = APIRouter()


@router.get(
    "/",
    response_model=list[FeedbackInDB],
    status_code=status.HTTP_200_OK,
)
def get_feedbacks(
    db: Session = Depends(get_db),
):
    """
    Retrieve all feedbacks
    """
    return crud_feedback.get_multi(db=db)


@router.get(
    "/me/",
    response_model=list[FeedbackInDB],
    status_code=status.HTTP_200_OK,
)
def get_my_feedbacks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve all feedbacks for the current user.
    """
    return crud_feedback.get_user_feedbacks(db=db, user_id=current_user.id)


@router.post(
    "/",
    response_model=FeedbackInDB,
    status_code=status.HTTP_201_CREATED,
)
def create_feedback(
    obj_in: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve all feedbacks for the current user.
    """
    return crud_feedback.create(db=db, obj_in=obj_in, current_user=current_user)


@router.put(
    "/{feedback_id}/",
    response_model=FeedbackInDB,
    status_code=status.HTTP_201_CREATED,
)
def update_feedback(
    feedback_id: int,
    obj_in: FeedbackUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve all feedbacks for the current user.
    """
    return crud_feedback.update(
        db=db, feedback_id=feedback_id, obj_in=obj_in, current_user=current_user
    )


@router.delete(
    "/{feedback_id}/",
    response_model=FeedbackInDB,
    status_code=status.HTTP_200_OK,
)
def delete_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve all feedbacks for the current user.
    """
    return crud_feedback.remove(
        db=db, feedback_id=feedback_id, current_user=current_user
    )
