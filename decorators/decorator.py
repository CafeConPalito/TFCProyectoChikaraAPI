from functools import wraps

from config.jwt import validate_token


def Security(required_roles: list= None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            token:str = kwargs.get("token") or args[1]
            validate_token(token, True)
            return func(*args, **kwargs)
        return wrapper
    return decorator