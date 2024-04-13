from rest_framework import exceptions, status
from django.http import Http404
from django.utils.translation import gettext_lazy as _

from rest_framework.response import Response


class UserException(exceptions.APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {
        'response_code': status.HTTP_403_FORBIDDEN,
        'response_message': _('User with provided token/id is not valid.'),
        'data': None
    }
    default_code = 'invalid_user'


def handle_exceptions(e, message):
    if isinstance(e, Http404):
        return Response({
            'response_code': status.HTTP_404_NOT_FOUND,
            'data': None,
            'response_message': _(message),
        }, status=status.HTTP_404_NOT_FOUND)
    if isinstance(e, UserException):
        return Response(
            e.default_detail,
            status=e.status_code
        )
    else:
        return Response({
            'response_code': status.HTTP_400_BAD_REQUEST,
            'data': None,
            'response_message': _('Something went wrong. Please try again later.'),
        }, status=status.HTTP_400_BAD_REQUEST)
