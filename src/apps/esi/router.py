from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.esi.service import EsiService
from src.apps.esi.schema import AuthCallBackRequest, AuthCallBackResponse
from src.dependencies.database import get_db

router = APIRouter()


@router.post("/esi_login", response_model=AuthCallBackResponse)
async def esi_login(
        payload: AuthCallBackRequest,
        db: AsyncSession = Depends(get_db)
):
    esi_service = EsiService(db)

    auth_token = await esi_service.get_auth_token(payload.code, payload.code_verifier)
    if not auth_token:
        raise HTTPException(status_code=500, detail="Failed to get auth token from ESI")

    access_token = auth_token.get("access_token")
    user_info = await esi_service.get_user_info(access_token)
    if not user_info:
        raise HTTPException(status_code=500, detail="Failed to get user info from ESI")

    if not user_info.get("sub"):
        raise HTTPException(status_code=500, detail="No 'sub' field in ESI user info")

    esi_user = await esi_service.get_or_create_esi_user(user_info=user_info)
    await esi_service.save_esi_token(esi_user_id=esi_user.id, auth_token=auth_token)

    return {
        "access_token": access_token,
        "esi_user_info": user_info,
        "esi_user_id": esi_user.id,
    }
