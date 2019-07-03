import base64

from django.contrib.auth import authenticate
from django.http import HttpResponse


class BasicAuthMiddleware:
    """Middleware for Basic authentication"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user already authenticated or missing HTTP auth headers
        if not request.user.is_authenticated \
                and 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                if auth[0].lower() == "basic":
                    auth_string = base64.b64decode(auth[1]).decode()
                    uname, passwd = auth_string.split(':')
                    user = authenticate(username=uname, password=passwd)
                    if user is not None and user.is_active:
                        request.user = user

                        return self.get_response(request)

        response = HttpResponse()
        response.status_code = 401
        response['WWW-Authenticate'] = 'Basic realm="Basic Auth Protected"'
        return response
