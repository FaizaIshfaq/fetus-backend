from rest_framework.authentication import TokenAuthentication, get_authorization_header
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions


class TokenException(exceptions.APIException):
    status_code = 401
    default_detail = {
        'response_code': 401,
        'response_message': _('Invalid/Expired Token.'),
        'data': None
    }
    default_code = 'invalid_token'

    def __init__(self, message=None):
        if message:
            self.default_detail['response_message'] = message
        super().__init__()


class UserTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            raise TokenException(_('Invalid token header. No credentials provided.'))

        if len(auth) == 1:
            raise TokenException(_('Invalid token header. No credentials provided.'))
        elif len(auth) > 2:
            raise TokenException(_('Invalid token header. Token string should not contain spaces.'))

        try:
            token = auth[1].decode()
        except UnicodeError:
            raise TokenException(_('Invalid token header. Token string should not contain invalid characters.'))

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise TokenException(_('Invalid token. User is not authenticated.'))

        if not token.user.is_active:
            raise TokenException(_('User inactive or deleted.'))

        if not token.user.is_authenticated or not token.user.is_logged_in:
            raise TokenException(_('User is not authenticated.'))

        return token.user, token
