from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
import uuid
from app.utils.helpers import create_hash, verify_hash, utcnow
import datetime


class User(Base):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), default=func.now())

    email = Column(String(64), unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)

    first_name = Column(String(16), nullable=True)
    last_name = Column(String(16), nullable=True)
    
    last_login = Column(DateTime(timezone=True), default=func.now())

    portfolio_transactions = relationship('PortfolioTransaction', back_populates='user', cascade='all, delete-orphan')  


    def set_password(self, password: str):
        self.hashed_password = create_hash(password)
        
    def verify_password(self, password: str):
        return verify_hash(password, self.hashed_password)

    @property
    def needs_relogin(self)->bool:
        if self.last_login < (utcnow() - datetime.timedelta(days=7)):
            return True
        
        return False
