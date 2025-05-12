from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func

from db.base_class import Base


class Feedback(Base):
    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("user.id", ondelete="cascade"), index=True)
    product_id = Column(
        Integer, ForeignKey("product.id", ondelete="cascade"), index=True
    )
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)

    date_created = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        """Return a string representation of the user."""
        return f"<Feedback(id={self.id}>"
