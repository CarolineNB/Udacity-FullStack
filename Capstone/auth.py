import json
import os
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen
AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
ALGORITHMS = os.environ.get('ALGORITHMS')
API_AUDIENCE = os.environ.get('Casts')

# AuthError Exception


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    if "Authorization" in request.headers:
        auth_header = request.headers["Authorization"]
        if auth_header:
            bearer_token_array = auth_header.split(' ')
            if bearer_token_array[0] and bearer_token_array[0].lower() \
                    == "bearer" and bearer_token_array[1]:
                return bearer_token_array[1]
    raise AuthError({
        'success': False,
        'code': 'invalid_header',
        'message': "JWT not found.",
        'error': 401
        }, 401)


def check_permissions(permission, payload):
    if "permissions" in payload:
        if permission in payload['permissions']:
            return True
    raise AuthError({
        'success': False,
        'code': 'unauthorized',
        'description': 'Permission Not Found in JWT!',
        'error': 401
    }, 401)


def verify_decode_jwt(token):
    # Get public key from Auth0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # Get the data in the header
    unverified_header = jwt.get_unverified_header(token)
    # Auth0 token should have a key id
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'success': False,
            'code': 'invalid_header',
            'description': 'Authorization malformed',
            'error': 401,
        }, 401)
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    # verify the token
    if rsa_key:
        try:
            # Validate the token using the rsa_key
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'success': False,
                'code': 'token_expired',
                'description': 'Token expired.',
                'error': 401,
            }, 401)
        except jwt.JWTClaimsError:
            raise AuthError({
                'success': False,
                'code': 'invalid_claims',
                'description': 'Incorrect claims. \
                        Please, check the audience and issuer.',
                'error': 401,
            }, 401)
        except Exception:
            raise AuthError({
                'success': False,
                'code': 'invalid_header',
                'description': 'Unable to parse authentication \
                        token.',
                'error': 400,
            }, 400)
    raise AuthError({
        'success': False,
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate \
                key.',
        'error': 400,
    }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
