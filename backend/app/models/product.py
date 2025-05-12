from sqlalchemy import Column, Integer, String, DateTime, Numeric, func

from db.base_class import Base


class Product(Base):
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(256), nullable=False)
    slug = Column(String(256), nullable=False)
    description = Column(String(1000), nullable=True)

    price = Column(Numeric(10, 2), default=0)

    date_created = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        """Return a string representation of the user."""
        return f"<Product(id={self.id}, name={self.name})>"
