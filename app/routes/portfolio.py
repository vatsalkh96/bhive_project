from fastapi import APIRouter, Depends
from typing import List
from app.deps import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.portfolio_transaction import PortfolioTransactionResultSet
from app.schemas.portfolio import Portfolio
import app.crud.portfolio as portfolio_crud
from app.crud.user import get_current_user
from app.models.user import User

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])

@router.get("/{scheme_code}/transactions", response_model=PortfolioTransactionResultSet)
async def get_transactions(
    scheme_code: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await portfolio_crud.get_portfolio_transactions_for_user(user, scheme_code, db)

@router.get("/portfolio", response_model=Portfolio)
async def get_portfolio(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return await portfolio_crud.get_user_portfolio(user, db)
