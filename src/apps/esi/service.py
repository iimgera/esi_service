import logging
from datetime import datetime, timezone, timedelta
from typing import Optional
from datetime import date

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.esi.model import EsiUser, EsiToken
from src.core.config import settings

logger = logging.getLogger(__name__)


class EsiService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.timeout = 15.0

    async def get_auth_token(self, code: str, code_verifier: str) -> Optional[dict]:
        url = f"{settings.ESI_URL}/connect/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": settings.ESI_CLIENT_ID,
            "client_secret": settings.ESI_CLIENT_SECRET,
            "code": code,
            "redirect_uri": settings.ESI_REDIRECT_URI,
            "code_verifier": code_verifier,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(url, headers=headers, data=data)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as exc:
                logger.error("Failed to get auth token: %s", exc.response.text)
            except httpx.RequestError as exc:
                logger.error("Network error while getting auth token: %s", exc)
        return None

    async def get_user_info(self, access_token: str) -> Optional[dict]:
        url = f"{settings.ESI_URL}/connect/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as exc:
                logger.error("Failed to get user info: %s", exc.response.text)
            except httpx.RequestError as exc:
                logger.error("Network error while getting user info: %s", exc)
        return None

    async def get_or_create_esi_user(self, user_info: dict) -> EsiUser:
        esi_id = user_info.get("sub")

        birth_date = user_info.get("birthdate")
        if isinstance(birth_date, str):
            try:
                birth_date = date.fromisoformat(birth_date)
            except ValueError:
                birth_date = None

        defaults = {
            "organization_tin": user_info.get("organization_tin"),
            "organization_name": user_info.get("organization_name"),
            "position_name": user_info.get("position_name"),
            "pin": user_info.get("pin"),
            "citizenship": user_info.get("citizenship"),
            "family_name": user_info.get("family_name"),
            "given_name": user_info.get("given_name"),
            "middle_name": user_info.get("middle_name"),
            "name": user_info.get("name"),
            "gender": user_info.get("gender"),
            "birth_date": birth_date,
            "email": user_info.get("email"),
            "phone": user_info.get("phone_number"),
        }

        result = await self.db.execute(select(EsiUser).where(EsiUser.esi_id == esi_id))
        esi_user = result.scalars().first()

        if esi_user:
            changed = False
            for field, value in defaults.items():
                if getattr(esi_user, field) != value:
                    setattr(esi_user, field, value)
                    changed = True
            if changed:
                await self.db.flush()
        else:
            esi_user = EsiUser(esi_id=esi_id, **defaults)
            self.db.add(esi_user)
            await self.db.flush()

        await self.db.commit()
        return esi_user

    async def save_esi_token(self, esi_user_id: int, auth_token: dict) -> None:
        expires_in_seconds = auth_token.get("expires_in", 0)
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in_seconds)

        token = EsiToken(
            esi_user_id=esi_user_id,
            token_type=auth_token.get("token_type", "Bearer"),
            token_value=auth_token.get("access_token"),
            expires_in=expires_at,
            refresh_token=auth_token.get("refresh_token", ""),
        )
        self.db.add(token)
        await self.db.commit()
