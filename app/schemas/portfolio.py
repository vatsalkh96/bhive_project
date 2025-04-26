from pydantic import BaseModel
from .scheme import FundFamily


class Investment(BaseModel):
    current_nav: float
    total_amount_invested: float
    total_current_amount: float
    total_units_purchased: float
    scheme_code: int
    scheme_name: str
    mutual_fund_family: FundFamily


class Portfolio(BaseModel):
    data: list[Investment]
    total: int