from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import models here to avoid circular import
from app.models import User, Scheme, PortfolioTransaction
