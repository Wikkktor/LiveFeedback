from sqlalchemy.orm import Session

from core.exceptions import no_permission
from crud.base import CRUDBase
from models import Feedback, User
from schemas.feedback import FeedbackCreate, FeedbackUpdate, FeedbackInDB

from kafka.producer import send_to_kafka
from elastic import FeedbackElasticClient


class CRUDFeedback(CRUDBase[Feedback, FeedbackCreate, FeedbackUpdate]):
    def search(self, query: str | None = None) -> list[Feedback]:
        """Search for Feedback by query."""
        # Create some query for elastic search with fuzzy search
        body = (
            {
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["comment"],  # Adjust fields as needed
                        "fuzziness": "AUTO",
                    }
                }
            }
            if query
            else {}
        )
        results = FeedbackElasticClient().search_documents(body=body)
        return [hit["_source"] for hit in results["hits"]["hits"]]

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
        feedback_db: Feedback = super().create(db=db, obj_in=obj_in)
        send_to_kafka(
            model_type=self.model_name,
            action="create",
            payload=FeedbackInDB.model_validate(
                feedback_db, from_attributes=True
            ).model_dump(),
        )
        return feedback_db

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
        feedback_db: Feedback = super().update(db=db, db_obj=db_obj, obj_in=obj_in)
        send_to_kafka(
            model_type=self.model_name,
            action="update",
            payload=FeedbackInDB.model_validate(
                feedback_db, from_attributes=True
            ).model_dump(),
        )
        return feedback_db

    def remove(self, db: Session, *, feedback_id: int, current_user: User) -> Feedback:
        """Remove a Feedback."""
        feedback_db: Feedback = self.check_permission(
            db=db, current_user=current_user, feedback_id=feedback_id
        )
        db.delete(feedback_db)
        db.commit()
        send_to_kafka(
            model_type=self.model_name,
            action="delete",
            payload=FeedbackInDB.model_validate(
                feedback_db, from_attributes=True
            ).model_dump(),
        )
        return feedback_db


crud_feedback: CRUDFeedback = CRUDFeedback(Feedback)
