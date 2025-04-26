import re

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


