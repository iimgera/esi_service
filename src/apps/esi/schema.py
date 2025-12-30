from typing import Optional

from pydantic import BaseModel, EmailStr


class AuthCallBackRequest(BaseModel):
    code: str
    code_verifier: str


class AuthCallBackResponse(BaseModel):
    access_token: str
    esi_user_info: dict
    esi_user_id: int
