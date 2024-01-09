import jwt
from rest_framework import authentication, exceptions
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)
        print(auth_data)
        if not auth_data:
            return None
        prefix, token = auth_data.decode("utf-8").split(" ") 
   
        try:
            payload = jwt.decode(token, settings.JWT_SECRET)
            user = User.objects.get(email=payload['email'])
            return (user, token)
        except jwt.DecodeError as identifier:
            raise exceptions.AuthenticationFailed(_('Token is invalid'))
        except jwt.ExpiredSignatureError as identifier:
            raise exceptions.ValidationError(_('Token has expired'))
        
        return super().authenticate(request)