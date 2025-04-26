import datetime
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select, func, orm
from app.models import User, Scheme
from app.schemas.scheme import FundFamily, SchemeQuery, SchemeType, SchemeResponseFull, SchemeResultSet, LatestSchemeResponse
from app.schemas.user import UserCreate, UserPatch, UserResponse
from app.schemas.auth import Login
from app.utils.helpers import create_hash
from fastapi import Depends, Header
from app.deps import get_db
from app.utils.exceptions import BadRequestException, NotFoundException, UnauthorizedException
from httpx import AsyncClient
from config import settings



async def fetch_latest_schemes_data(
    httpx_client: AsyncClient,
    scheme_type: SchemeType, 
    fund_family: FundFamily | None = None, 
    scheme_code: int | None = None, 
) -> LatestSchemeResponse | None:
    headers = {
        'x-rapidapi-key': settings.RAPIDAPI_KEY,
        'x-rapidapi-host': settings.LATEST_MUTUALFUND_HOST
    }
    params = {
        "Scheme_Type": scheme_type
    }

    if scheme_code:
        params['Scheme_Code'] = scheme_code

    if fund_family:
        params['Mutual_Fund_Family'] = fund_family

    response = await httpx_client.get(settings.LATEST_MUTUALFUND_URL, headers=headers, params=params)

    if response.status_code != 200:
        return
    
    try:
        response_json = await response.json()
        if not response_json:
            return
        
        return LatestSchemeResponse.model_validate(response_json)
    
    except Exception:
        # Can add logging statements for visibility and error discovery
        return


async def get_schemes(user: User, db: AsyncSession, query_params: SchemeQuery) -> SchemeResultSet:
    schemes = (
        await db.execute(
            select(Scheme)
            # .options(orm.load_only(Scheme.scheme_code, Scheme.mutual_fund_family, Scheme.scheme_name))
            .where(
                Scheme.mutual_fund_family == query_params.mutual_fund_family,
                Scheme.scheme_type == query_params.scheme_type
            )
            .limit(query_params.page_size)
            .offset((query_params.page-1)*query_params.page_size)
        )
    ).scalars().all()

    total = (
        await db.execute(
            select(func.count(1))
            .select_from(Scheme)
            .where(
                Scheme.mutual_fund_family == query_params.mutual_fund_family,
                Scheme.scheme_type == query_params.scheme_type
            )
        )
    ).scalar()

    return SchemeResultSet.model_validate({'data': schemes, 'total': total})


async def get_sceheme_by_code(user: User, db: AsyncSession, scheme_code: int, httpx_client: AsyncClient) -> SchemeResponseFull:
    scheme = (
        await db.execute(
            select(Scheme)
            .where(
                Scheme.scheme_code == scheme_code,
            )
        )
    ).scalar_one_or_none()

    if not scheme: 
        raise NotFoundException(f'Cannot find scheme: {scheme_code}')
    
    if scheme.needs_refresh:
        latest_scheme_snapshot = await fetch_latest_schemes_data(httpx_client, scheme.scheme_type, scheme_code=scheme.scheme_code)

        for field, value in latest_scheme_snapshot.model_dump(exclude = {'scheme_code'}):
            # Can add some sanity check to see if the correct scheme code is returned or not. 
            setattr(scheme, field, value)

        await db.commit()
        await db.refresh(scheme)
    
    return SchemeResponseFull.model_validate(scheme)