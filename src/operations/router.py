from http.client import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.operations.models import operation
from src.operations.schemas import OperationCreate

from fastapi_cache.decorator import cache

import time

router = APIRouter(
    prefix='/operations',
    tags=['Operation']
)

# @router.get('/long_operation')
# @cache(expire=60)
# def get_long_op():
#     time.sleep(2)
#     return 'Many many many data'

@router.get('/')
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        return {
            'status': 'success',
            'data': result.all(),
            'details': None
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': f'Error: {ex}'
        })

@router.post('/')
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        statement = insert(operation).values(**new_operation.dict())
        await session.execute(statement)
        await session.commit()

        return {
            'status': 'success',
            'data': new_operation.dict(),
            'details': None
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': f'Error: {ex}'
        })
