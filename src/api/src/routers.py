from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from redis.exceptions import ConnectionError as RedisConnectionError

from create_book.config import Config
from users import FeatureGrant, UserRepository

config = Config()


def get_user_repo(request: Request) -> UserRepository | None:
    return getattr(request.app.state, "user_repo", None)


async def require_user_repo(
    repo: UserRepository | None = Depends(get_user_repo),
) -> UserRepository:
    if repo is None:
        raise HTTPException(501, "Feature gating is not enabled")
    return repo


async def verify_admin_key(x_api_key: str = Header(...)):
    if x_api_key != config.ADMIN_API_KEY:
        raise HTTPException(401, "Invalid API key")


class CreateUserRequest(BaseModel):
    features: dict[str, FeatureGrant] = {}
    external_identifier: str = ""


class UpdateUserRequest(BaseModel):
    features: dict[str, FeatureGrant | None] | None = None
    external_identifier: str | None = None


# --- Admin Router ---

admin_router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(verify_admin_key), Depends(require_user_repo)],
)


@admin_router.post("/users")
async def create_user(
    body: CreateUserRequest,
    repo: UserRepository = Depends(get_user_repo),
):
    """Create a new user with optional feature grants and external identifier.

    Body: {"features": {"pdf_download": {}, ...}, "external_identifier": "johndoe"}
    Returns: full UserRecord JSON.
    """
    user = await repo.create(body.features, body.external_identifier)
    return user.model_dump(mode="json")


@admin_router.get("/users/by-external/{external_identifier}")
async def get_user_by_external(
    external_identifier: str,
    repo: UserRepository = Depends(get_user_repo),
):
    """Look up a user by their external identifier (e.g. Discord username).

    Path param: external_identifier.
    Returns: full UserRecord JSON, or 404.
    """
    user = await repo.get_by_external_identifier(external_identifier)
    if user is None:
        raise HTTPException(404, "User not found")
    return user.model_dump(mode="json")


@admin_router.get("/users/{user_id}")
async def get_user(
    user_id: UUID,
    repo: UserRepository = Depends(get_user_repo),
):
    """Get a user by UUID.

    Path param: user_id (UUID).
    Returns: full UserRecord JSON, or 404.
    """
    user = await repo.get(user_id)
    if user is None:
        raise HTTPException(404, "User not found")
    return user.model_dump(mode="json")


@admin_router.put("/users/{user_id}")
async def update_user(
    user_id: UUID,
    body: UpdateUserRequest,
    repo: UserRepository = Depends(get_user_repo),
):
    """Partially update a user. Omitted fields are left unchanged.

    Path param: user_id (UUID).
    Body: {"features": {...}, "external_identifier": "..."}
      - Features are merged: new grants are added/overwritten, null removes a grant.
      - external_identifier: null = don't touch, "" = clear, other = rename.
    Returns: updated UserRecord JSON, or 404.
    """
    user = await repo.update(user_id, body.features, body.external_identifier)
    if user is None:
        raise HTTPException(404, "User not found")
    return user.model_dump(mode="json")


@admin_router.delete("/users/{user_id}", status_code=204)
async def delete_user(
    user_id: UUID,
    repo: UserRepository = Depends(get_user_repo),
):
    """Delete a user and their external identifier index.

    Path param: user_id (UUID).
    Returns: 204 on success, 404 if not found.
    """
    deleted = await repo.delete(user_id)
    if not deleted:
        raise HTTPException(404, "User not found")


# --- User Router ---

user_router = APIRouter()


@user_router.get("/user/features")
async def get_features(
    user_id: str | None = None,
    repo: UserRepository | None = Depends(get_user_repo),
):
    """Return a user's active feature names and external identifier.

    Query param: user_id (UUID string, optional).
    Returns: {"features": ["pdf_download", ...], "external_identifier": "..."}
      with Cache-Control: private, max-age=300.
    Degrades gracefully: returns empty features on invalid UUID or Redis failure.
    """
    features = []
    external_identifier = ""

    if repo and user_id:
        try:
            user = await repo.get(UUID(user_id))
            if user:
                features = user.active_features()
                external_identifier = user.external_identifier
        except ValueError:
            pass
        except RedisConnectionError:
            pass

    response = JSONResponse(
        {"features": features, "external_identifier": external_identifier}
    )
    response.headers["Cache-Control"] = "private, max-age=300"
    return response


# --- Activation Router ---

activation_router = APIRouter()


@activation_router.get("/activate/{user_id}")
async def activate(
    user_id: UUID,
    repo: UserRepository = Depends(require_user_repo),
):
    """Validate an activation link and redirect to the frontend activation page.

    Path param: user_id (UUID).
    Returns: 302 redirect to /activated?id={user_id}, or 404 if UUID is unknown.
    """
    user = await repo.get(user_id)
    if user is None:
        raise HTTPException(404, "Unknown activation link")

    return RedirectResponse(url=f"/activated?id={user_id}", status_code=302)
