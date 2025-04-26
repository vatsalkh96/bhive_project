from app.models import User, PortfolioTransaction
from sqlalchemy import select, func
from app.models.scheme import Scheme
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.portfolio import Portfolio
from app.schemas.portfolio_transaction import PortfolioTransactionCreate, PortfolioTransactionResponse, PortfolioTransactionResultSet

async def get_user_portfolio(user: User, db: AsyncSession) -> Portfolio:
    investments = (await db.execute(
        select(
            func.sum(PortfolioTransaction.amount_invested).label("total_amount_invested"),
            func.sum(PortfolioTransaction.current_amount).label("total_current_amount"),
            func.sum(PortfolioTransaction.units_purchased).label("total_units_purchased"),
            Scheme.scheme_code,
            Scheme.scheme_name,
            Scheme.mutual_fund_family,
            Scheme.net_asset_value.label("current_nav")
        )
        .join(Scheme, Scheme.scheme_code == PortfolioTransaction.scheme_code)
        .where(
            PortfolioTransaction.user_id == user.id
        )
        .group_by(
            Scheme.scheme_code,
            Scheme.scheme_name,
            Scheme.mutual_fund_family,
            Scheme.net_asset_value
        )
    )).all()

    total = (await db.execute(select(func.count(func.distinct(PortfolioTransaction.scheme_code))).where(PortfolioTransaction.user_id == user.id))).scalar()

    print("*********************** investments!! ")
    print(investments[0]._mapping)
    print("************ TOTAL")
    print(total)

    return Portfolio.model_validate({'data': [i._mapping for i in investments], 'total': total})


async def create_portfolio_transaction(
    user: User,
    db: AsyncSession, 
    transaction_in: PortfolioTransactionCreate,
) -> PortfolioTransactionResponse:
    
    db_transaction = PortfolioTransaction(
        user_id=user.id,
        scheme_code=transaction_in.scheme_code,
        nav_on_purchase=transaction_in.nav_on_purchase,
        nav_now=transaction_in.nav_now,
        amount_invested=transaction_in.amount_invested,
        current_amount=transaction_in.current_amount,
        units_purchased=transaction_in.units_purchased
    )

    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)

    return PortfolioTransactionResponse.model_validate(db_transaction)


async def get_portfolio_transactions_for_user(
    user: User,
    scheme_code: int,
    db: AsyncSession,
) -> PortfolioTransactionResultSet:
    
    transactions = (
        await db.execute(
            select(PortfolioTransaction)
            .where(PortfolioTransaction.user_id == user.id, PortfolioTransaction.scheme_code == scheme_code)
        )
    ).scalars().all()

    total = (await db.execute(select(func.count(1)).where(PortfolioTransaction.scheme_code == scheme_code))).scalar()

    print("TRANSATINS**********************************************************************")

    return {'data': transactions, 'total': total}
