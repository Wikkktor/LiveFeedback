from sqlalchemy.orm import Session

from core.exceptions import no_permission
from crud.base import CRUDBase
from models import Feedback, User
from schemas.feedback import FeedbackCreate, FeedbackUpdate


class CRUDFeedback(CRUDBase[Feedback, FeedbackCreate, FeedbackUpdate]):
    def check_permission(
        self, db: Session, current_user: User, feedback_id: int
    ) -> bool:
        """Check if the current user has permission to access the feedback."""
        feedback_db: Feedback = self.get_or_404(db=db, id=feedback_id)
        if feedback_db.user_id != current_user.id:
            raise no_permission()
        return feedback_db

    def get_user_feedbacks(self, db: Session, user_id: int) -> list[Feedback]:
        """Get a Feedback by user id."""
        return db.query(Feedback).filter(Feedback.user_id == user_id).all()

    def create(
        self, db: Session, *, obj_in: FeedbackCreate, current_user: User
    ) -> Feedback:
        """Create a new Feedback."""
        obj_in.user_id = current_user.id
        return super().create(db=db, obj_in=obj_in)

    def update(
        self,
        db: Session,
        *,
        feedback_id: int,
        obj_in: FeedbackUpdate,
        current_user: User,
    ) -> Feedback:
        """Update a Feedback."""
        db_obj: Feedback = self.check_permission(
            db=db, current_user=current_user, feedback_id=feedback_id
        )
        obj_in.user_id = current_user.id
        return super().update(db=db, db_obj=db_obj, obj_in=obj_in)

    def remove(self, db: Session, *, feedback_id: int, current_user: User) -> Feedback:
        """Remove a Feedback."""
        db_obj: Feedback = self.check_permission(
            db=db, current_user=current_user, feedback_id=feedback_id
        )
        db.delete(db_obj)
        db.commit()
        return db_obj


crud_feedback: CRUDFeedback = CRUDFeedback(Feedback)
