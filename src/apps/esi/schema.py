from typing import Optional

from pydantic import BaseModel


class AuthCallBackRequest(BaseModel):
    code: str
    code_verifier: str


class EsiUserInfo(BaseModel):
    sub: str
    name: Optional[str] = None
    email: Optional[str] = None
    family_name: Optional[str] = None
    given_name: Optional[str] = None
    middle_name: Optional[str] = None
    organization_tin: Optional[str] = None
    organization_name: Optional[str] = None
    position_name: Optional[str] = None
    pin: Optional[str] = None
    citizenship: Optional[str] = None
    gender: Optional[str] = None
    birthdate: Optional[str] = None
    phone_number: Optional[str] = None


class AuthCallBackResponse(BaseModel):
    access_token: str
    esi_user_info: EsiUserInfo
    esi_user_id: int
