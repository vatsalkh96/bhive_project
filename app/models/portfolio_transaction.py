from sqlalchemy import Column, Float, DateTime, ForeignKey, Integer, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid

class PortfolioTransaction(Base):
    __tablename__ = "portfolio_transaction"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    nav_on_purchase = Column(Float, nullable=False)
    nav_now = Column(Float, nullable=False)
    amount_invested = Column(Float, nullable=False)
    current_amount = Column(Float, nullable=False)
    units_purchased = Column(Float, nullable=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    scheme_code = Column(Integer, ForeignKey("scheme.scheme_code", ondelete="CASCADE"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="portfolio_transactions")  
    scheme = relationship("Scheme", back_populates="portfolio_transactions") 
