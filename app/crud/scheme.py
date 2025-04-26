from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import  select, func, orm
from app.models import User, Scheme
from app.schemas.scheme import FundFamily, SchemeCreate, SchemeQuery, SchemeType, SchemeResponseFull, SchemeResultSet, LatestSchemeResponse
from app.utils.exceptions import NotFoundException
from httpx import AsyncClient
from config import settings
from pydantic import TypeAdapter


async def fetch_latest_schemes_data(
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

    async with AsyncClient() as client:
        response = await client.get(settings.LATEST_MUTUALFUND_URL, headers=headers, params=params)
        if response.status_code != 200:
            return
        
        try:
            response_json = response.json()
            if not response_json:
                return
            
            return TypeAdapter(list[LatestSchemeResponse]).validate_python(response_json)
        
        except Exception:
            # Can add logging statements for visibility and error discovery
            return


async def get_schemes(user: User, db: AsyncSession, query_params: SchemeQuery) -> SchemeResultSet:
    schemes = (
        await db.execute(
            select(Scheme)
            .options(orm.load_only(Scheme.scheme_code, Scheme.mutual_fund_family, Scheme.scheme_name))
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
        latest_scheme_snapshot = await fetch_latest_schemes_data(scheme.scheme_type, scheme_code=scheme.scheme_code)

        if not latest_scheme_snapshot:
            return scheme

        for field, value in SchemeCreate.model_validate(latest_scheme_snapshot[0]).model_dump(exclude = {'scheme_code'}).items():
            # Can add some sanity check to see if the correct scheme code is returned or not. 
            setattr(scheme, field, value)

        await db.commit()
        await db.refresh(scheme)
    
    return SchemeResponseFull.model_validate(scheme)