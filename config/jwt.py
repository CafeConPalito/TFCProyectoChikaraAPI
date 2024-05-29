from fastapi.security import HTTPBearer
from jwt import encode, decode
from jwt import exceptions
from datetime import datetime, timedelta, timezone
from fastapi.responses import JSONResponse
from decouple import config

oauth2_scheme = HTTPBearer()

def parse_expire_date(hour: int):
    date = datetime.now(timezone.utc)
    new_date = date + timedelta(hours=hour)
    return new_date


def generate_token(data: dict):
    token = encode(payload={
        **data, "exp": parse_expire_date(config('EXPIRE_TIME', cast=int))
    }, key=config('KEY'),algorithm="HS256")
    return token


def validate_token(token, output=False):
    try:
        if output:
            return decode(token, key=config('KEY'), algorithms=["HS256"])
        decode(token, key=config('KEY'), algorithms=["HS256"])
    except exceptions.InvalidSignatureError:
        return JSONResponse(content={"message": "Invalid Token"},
                            status_code=401)
    except exceptions.DecodeError:
        return JSONResponse(content={"message": "Invalid Token"},
                            status_code=401)
    except exceptions.ExpiredSignatureError:
        return JSONResponse(content={"message": "Token Expired"},
                            status_code=401)
    
    
def get_user_id(token):
    return validate_token(token, True)["id_user"]
