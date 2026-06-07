"""Discord OAuth2 authentication with guild-gated PDF access."""

import secrets
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

import jwt
from aiohttp_client_cache.session import CachedSession
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic_settings import BaseSettings

from create_book.vars import cache

DISCORD_API = "https://discord.com/api/v10"
COOKIE_NAME = "wpd_session"
STATE_COOKIE_NAME = "wpd_oauth_state"
MEMBERSHIP_CACHE_TTL = 1800


class AuthConfig(BaseSettings):
    DISCORD_AUTH_ENABLED: bool = True
    DISCORD_CLIENT_ID: str = ""
    DISCORD_CLIENT_SECRET: str = ""
    DISCORD_BOT_TOKEN: str = ""
    DISCORD_GUILD_ID: str = ""
    DISCORD_UNRESTRICTED_ACCESS_ROLE_ID: str = ""
    DISCORD_REDIRECT_URI: str = "http://localhost:5042/auth/discord/callback"
    JWT_SECRET: str = ""
    JWT_EXPIRY_SECONDS: int = 604800
    COOKIE_SECURE: bool = True


auth_config = AuthConfig()
auth_router = APIRouter(prefix="/auth")


def _auth_enabled() -> bool:
    return bool(auth_config.DISCORD_CLIENT_ID and auth_config.JWT_SECRET)


def create_jwt(discord_id: str, username: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "id": discord_id,
        "username": username,
        "iat": now,
        "exp": now + timedelta(seconds=auth_config.JWT_EXPIRY_SECONDS),
    }
    return jwt.encode(payload, auth_config.JWT_SECRET, algorithm="HS256")


def decode_jwt(token: str) -> dict | None:
    try:
        return jwt.decode(token, auth_config.JWT_SECRET, algorithms=["HS256"])
    except jwt.PyJWTError:
        return None


def _should_refresh(payload: dict) -> bool:
    exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    iat = datetime.fromtimestamp(payload["iat"], tz=timezone.utc)
    midpoint = iat + (exp - iat) / 2
    return datetime.now(timezone.utc) > midpoint


def _set_session_cookie(response, token: str):
    response.set_cookie(
        COOKIE_NAME,
        token,
        httponly=True,
        secure=auth_config.COOKIE_SECURE,
        samesite="lax",
        max_age=auth_config.JWT_EXPIRY_SECONDS,
        path="/",
    )


def get_current_user(request: Request) -> dict | None:
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        return None
    return decode_jwt(token)


async def fetch_guild_member(discord_id: str) -> dict | None:
    url = f"{DISCORD_API}/guilds/{auth_config.DISCORD_GUILD_ID}/members/{discord_id}"
    headers = {"Authorization": f"Bot {auth_config.DISCORD_BOT_TOKEN}"}
    async with CachedSession(cache=cache) as session:
        async with session.get(
            url, headers=headers, expire_after=MEMBERSHIP_CACHE_TTL
        ) as response:
            if response.status == 200:
                return await response.json()
            return None


async def check_guild_membership(discord_id: str) -> bool:
    return await fetch_guild_member(discord_id) is not None


def has_unrestricted_access(member: dict) -> bool:
    role_id = auth_config.DISCORD_UNRESTRICTED_ACCESS_ROLE_ID
    if not role_id:
        return False
    return role_id in member.get("roles", [])


async def require_pdf_access(request: Request, is_bulk: bool):
    if not auth_config.DISCORD_AUTH_ENABLED:
        return
    user = get_current_user(request)
    if not user:
        raise HTTPException(403, "Login required for PDF downloads")
    member = await fetch_guild_member(user["id"])
    if not member:
        raise HTTPException(403, "Guild membership required for PDF downloads")
    if is_bulk and not has_unrestricted_access(member):
        raise HTTPException(403, "Required role missing for bulk PDF downloads")


@auth_router.get("/discord/login")
def discord_login():
    if not _auth_enabled():
        raise HTTPException(503, "Discord auth not configured")
    state = secrets.token_urlsafe(32)
    params = {
        "client_id": auth_config.DISCORD_CLIENT_ID,
        "redirect_uri": auth_config.DISCORD_REDIRECT_URI,
        "response_type": "code",
        "scope": "identify",
        "state": state,
    }
    resp = RedirectResponse(f"{DISCORD_API}/oauth2/authorize?{urlencode(params)}")
    resp.set_cookie(
        STATE_COOKIE_NAME,
        state,
        httponly=True,
        secure=auth_config.COOKIE_SECURE,
        samesite="lax",
        max_age=300,
    )
    return resp


@auth_router.get("/discord/callback")
async def discord_callback(request: Request, code: str, state: str):
    if not _auth_enabled():
        raise HTTPException(503, "Discord auth not configured")

    saved_state = request.cookies.get(STATE_COOKIE_NAME)
    if not saved_state or state != saved_state:
        raise HTTPException(400, "Invalid state")

    async with CachedSession(cache=None) as session:
        async with session.post(
            f"{DISCORD_API}/oauth2/token",
            data={
                "client_id": auth_config.DISCORD_CLIENT_ID,
                "client_secret": auth_config.DISCORD_CLIENT_SECRET,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": auth_config.DISCORD_REDIRECT_URI,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        ) as token_response:
            if token_response.status != 200:
                raise HTTPException(502, "Failed to exchange code for token")
            token_data = await token_response.json()

        access_token = token_data["access_token"]

        async with session.get(
            f"{DISCORD_API}/users/@me",
            headers={"Authorization": f"Bearer {access_token}"},
        ) as user_response:
            if user_response.status != 200:
                raise HTTPException(502, "Failed to fetch user profile")
            user_data = await user_response.json()

    display_name = user_data.get("global_name") or user_data["username"]
    session_token = create_jwt(user_data["id"], display_name)

    resp = RedirectResponse("/")
    _set_session_cookie(resp, session_token)
    resp.delete_cookie(STATE_COOKIE_NAME)
    return resp


@auth_router.get("/me")
async def auth_me(request: Request):
    if not auth_config.DISCORD_AUTH_ENABLED:
        return {
            "logged_in": False,
            "auth_disabled": True,
            "has_pdf_access": True,
            "has_unrestricted_access": True,
        }

    user = get_current_user(request)
    if not user:
        return {"logged_in": False}

    member = await fetch_guild_member(user["id"])

    data = {
        "logged_in": True,
        "username": user["username"],
        "has_pdf_access": member is not None,
        "has_unrestricted_access": has_unrestricted_access(member) if member else False,
    }

    if _should_refresh(user):
        refreshed = create_jwt(user["id"], user["username"])
        resp = JSONResponse(data)
        _set_session_cookie(resp, refreshed)
        return resp

    return data


@auth_router.post("/logout")
def auth_logout():
    resp = JSONResponse({"logged_in": False})
    resp.delete_cookie(COOKIE_NAME, path="/")
    return resp
