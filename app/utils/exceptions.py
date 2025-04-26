import re

from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from starlette import status


class AppBaseException(Exception):
    """
    Base exception class for the project
    """

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = 'Something went wrong'
    payload = dict()

    def __init__(self, message: str | None = None, status_code: int | None = None, payload: dict | None = None):
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        if payload is not None:
            self.payload = payload

    def to_dict(self):
        rv = dict(self.payload)
        rv['message'] = self.message
        return rv


class BadRequestException(AppBaseException):
    """
    Exception if the resource is not well formed
    """

    status_code = status.HTTP_400_BAD_REQUEST


class ConflictException(AppBaseException):
    """
    Exception if the resource is being created while it already exists
    """

    status_code = status.HTTP_409_CONFLICT

    def __init__(self, message: str | None = None, field: str | None = None, value=None):
        if field and value:
            m = f'{field}: {value} already exists' if not message else message
            payload = {'detail': [{'msg': f'{field}: {value} already exists', 'type': 'already_exists'}]}
        elif message:
            m = message
            payload = {}
        else:
            raise NotImplementedError('message or field, value needs to provided')
        super().__init__(message=m, payload=payload)


class ExternalServiceException(AppBaseException):
    """
    External service not working
    """

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class NotFoundException(AppBaseException):
    """
    Exception if the request resource is not found
    """

    status_code = status.HTTP_404_NOT_FOUND


class UnprocessableEntityException(AppBaseException):
    """
    Exception if the parameter passed are not valid
    """

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


# class TooManyRequestsException(BaseException):
#     """
#     Exception if the parameter passed are not valid
#     """

#     status_code = status.HTTP_429_TOO_MANY_REQUESTS


class ForbiddenException(AppBaseException):
    """
    Exception if the resource is accessed without permission required
    """

    status_code = status.HTTP_403_FORBIDDEN


class UnauthorizedException(AppBaseException):
    """
    Exception if the resource is accessed without permission required
    """

    status_code = status.HTTP_401_UNAUTHORIZED


# class CannotModifyAttributeException(UnprocessableEntityException):
#     """
#     Exception if the parameter passed cannot be modified
#     """

#     def __init__(self, field: str, value):
#         message = f'{field} cannot be modified'
#         payload = {'detail': [{'loc': [field], 'msg': f'{field} cannot be modified', 'type': 'cannot_modify'}]}
#         super().__init__(message=message, payload=payload)


# class AttributeValueException(UnprocessableEntityException):
#     """
#     Exception if the parameter passed cannot be modified
#     """

#     def __init__(self, field: str, value, message: str | None = None):
#         if isinstance(value, dict) or isinstance(value, BaseModel) or isinstance(value, list):
#             field_value = 'the one provided'
#         else:
#             field_value = f'{value}'
#         message = f'{field} should not be {field_value}' if not message else message
#         payload = {'detail': [{'msg': f'{field} should not be {field_value}', 'type': 'value_error'}]}
#         super().__init__(message=message, payload=payload)


# async def sqlalchemy_exception_handler(request: Request, exc: IntegrityError):
#     # https://stackoverflow.com/questions/55133384/make-sqlalchemy-errors-more-user-friendly-and-detailed
#     if not exc.orig:
#         raise exc
#     pattern = r'^.*?Key\s+\((?P<key>.*)\)=\((?P<value>.*)\)\s+already\s+exists.*$'
#     match = re.match(pattern, re.sub(r'\n|\r', ' ', exc.orig.args[0]))
#     # raise exc.orig
#     if match and match.groups():
#         field, value = match.groups()
#         http_exc = ConflictException(field=field, value=value)
#         return JSONResponse(status_code=http_exc.status_code, content=http_exc.to_dict())
#     raise exc.orig


# def is_key_conflict_exception(exc: IntegrityError):
#     if not exc.orig:
#         raise exc
#     pattern = r'^.*?Key\s+\((?P<key>.*)\)=\((?P<value>.*)\)\s+already\s+exists.*$'
#     match = re.match(pattern, re.sub(r'\n|\r', ' ', exc.orig.args[0]))
#     if match and match.groups():
#         return True
#     return False


# async def app_exception_handler(request: Request, exc: BaseException):
#     return JSONResponse(status_code=exc.status_code, content=exc.to_dict())
