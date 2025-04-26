from sqlalchemy import Column, Integer, String, Float, Date, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.schemas.scheme import SchemeType
from app.utils.helpers import utcnow

# class Scheme(Base):
#     __tablename__ = 'scheme'

#     scheme_code = Column(Integer, primary_key=True, unique=True, nullable=False)
#     isin_div_payout_isin_growth = Column(String(16), nullable=False)
#     isin_div_reinvestment = Column(String(16), nullable=False)
#     scheme_name = Column(String(64), nullable=False)
#     net_asset_value = Column(Float, nullable=False)
#     start_date = Column(Date, nullable=False)
#     scheme_type: SchemeType = Column(String(8), nullable=False)
#     scheme_category = Column(String(32), nullable=False)
#     mutual_fund_family = Column(String(64), nullable=False)

#     updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

#     portfolio_transactions = relationship('PortfolioTransaction', back_populates='scheme', cascade='all, delete-orphan')

#     @property
#     def needs_refresh(self):
#         if (utcnow() - self.updated_at).seconds > (60*60):
#             return True
#         return False


class Scheme(Base):
    __tablename__ = 'scheme'

    scheme_code = Column(Integer, primary_key=True, unique=True, nullable=False)
    isin_div_payout_isin_growth = Column(String(16), nullable=False)
    isin_div_reinvestment = Column(String(16), nullable=False)
    scheme_name = Column(String(128), nullable=False)
    net_asset_value = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False)
    scheme_type: SchemeType = Column(String(32), nullable=False)
    scheme_category = Column(String(128), nullable=False)
    mutual_fund_family = Column(String(128), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    portfolio_transactions = relationship('PortfolioTransaction', back_populates='scheme', cascade='all, delete-orphan')  # unchanged

    @property
    def needs_refresh(self):
        if (utcnow() - self.updated_at).seconds > (60*60):
            return True
        return False
