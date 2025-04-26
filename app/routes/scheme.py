from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.deps import get_db, get_http_client
import app.crud.scheme as scheme_crud
from app.crud.user import get_current_user
from app.models import User
from app.schemas.scheme import SchemeResultSet, SchemeResponseFull, SchemeQuery

router = APIRouter(prefix='/scheme', tags=['Scheme'])

@router.get('', response_model=SchemeResultSet)
async def get_schemes(
    db: AsyncSession = Depends(get_db), 
    query_params: SchemeQuery = Depends(),
    user = Depends(get_current_user)
):
    return await scheme_crud.get_schemes(user, db, query_params)

@router.get('/{scheme_code}', response_model=SchemeResponseFull)
async def get_scheme(
    scheme_code: int, 
    user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    httpx_client: AsyncSession = Depends(get_http_client)
):
    return await scheme_crud.get_sceheme_by_code(user, db, scheme_code, httpx_client)
