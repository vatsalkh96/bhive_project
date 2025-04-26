from pydantic import BaseModel, ConfigDict
from uuid import UUID
import datetime

class PortfolioTransactionBase(BaseModel):
    nav_on_purchase: float
    nav_now: float
    amount_invested: float
    current_amount: float
    units_purchased: float
    user_id: UUID
    scheme_code: int

class PortfolioTransactionCreate(PortfolioTransactionBase):
    pass

class PortfolioTransactionResponse(PortfolioTransactionBase):
    id: UUID
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class PortfolioTransactionResultSet(BaseModel):
    data: list[PortfolioTransactionResponse]
    total: int