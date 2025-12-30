from typing import Optional
from datetime import date

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.esi.model import EsiUser
from src.core.config import settings


class EsiService:
    """Class-based ESI Service for API calls and database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.timeout = 15.0

    async def get_auth_token(self, code: str, code_verifier: str) -> Optional[dict]:
        """Exchange authorization code for ESI access token."""
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
                print(f"[ESI ERROR] Failed to get auth token: {exc.response.text}")
            except httpx.RequestError as exc:
                print(f"[ESI ERROR] Network problem while getting auth token: {exc}")
        return None

    async def get_user_info(self, access_token: str) -> Optional[dict]:
        """Retrieve user information from ESI using access token."""
        url = f"{settings.ESI_URL}/connect/userinfo"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as exc:
                print(f"[ESI ERROR] Failed to get user info: {exc.response.text}")
            except httpx.RequestError as exc:
                print(f"[ESI ERROR] Network problem while getting user info: {exc}")
        return None

    # --------------------
    # DB Operations
    # --------------------
    async def get_or_create_esi_user(self, user_info: dict) -> EsiUser:
        """
        Get or create an ESI user in the database.
        Updates existing records only if fields have changed.
        """
        organization_tin = user_info.get("organization_tin")
        esi_id = user_info.get("sub")
        pin = user_info.get("pin")
        username = f"{esi_id}_{pin}" if pin else esi_id
        if organization_tin:
            username = f"{username}_{organization_tin}"

        # Normalize birth_date if provided
        birth_date = user_info.get("birthdate")
        if isinstance(birth_date, str):
            try:
                birth_date = date.fromisoformat(birth_date)
            except ValueError:
                birth_date = None

        defaults = {
            "organization_tin": organization_tin,
            "organization_name": user_info.get("organization_name"),
            "position_name": user_info.get("position_name"),
            "pin": pin,
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

        # Try to find an existing EsiUser
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
