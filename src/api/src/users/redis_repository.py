from uuid import UUID, uuid4

from redis.asyncio import Redis

from .repository import FeatureGrant, UserRecord, UserRepository


class RedisUserRepository(UserRepository):
    KEY_PREFIX = "wpd:user:"
    EXT_INDEX_PREFIX = "wpd:user:ext:"

    def __init__(self, redis: Redis):
        self._redis = redis

    def _key(self, user_id: UUID) -> str:
        return f"{self.KEY_PREFIX}{user_id}"

    def _ext_key(self, external_identifier: str) -> str:
        return f"{self.EXT_INDEX_PREFIX}{external_identifier}"

    async def create(
        self,
        features: dict[str, FeatureGrant] | None = None,
        external_identifier: str = "",
    ) -> UserRecord:
        user = UserRecord(
            id=uuid4(),
            features=features or {},
            external_identifier=external_identifier,
        )
        pipe = self._redis.pipeline()
        pipe.set(self._key(user.id), user.model_dump_json())
        if external_identifier:
            pipe.set(self._ext_key(external_identifier), str(user.id))
        await pipe.execute()
        return user

    async def get(self, user_id: UUID) -> UserRecord | None:
        data = await self._redis.get(self._key(user_id))
        if data is None:
            return None
        return UserRecord.model_validate_json(data)

    async def get_by_external_identifier(
        self, external_identifier: str
    ) -> UserRecord | None:
        uuid_str = await self._redis.get(self._ext_key(external_identifier))
        if uuid_str is None:
            return None
        return await self.get(
            UUID(uuid_str.decode() if isinstance(uuid_str, bytes) else uuid_str)
        )

    async def update(
        self,
        user_id: UUID,
        features: dict[str, FeatureGrant | None] | None = None,
        external_identifier: str | None = None,
    ) -> UserRecord | None:
        user = await self.get(user_id)
        if user is None:
            return None

        pipe = self._redis.pipeline()

        # None = "don't touch", "" = "clear it", other = "rename it"
        if (
            external_identifier is not None
            and external_identifier != user.external_identifier
        ):
            if user.external_identifier:  # delete old index key (skip if was empty)
                pipe.delete(self._ext_key(user.external_identifier))
            if external_identifier:  # create new index key (skip if clearing)
                pipe.set(self._ext_key(external_identifier), str(user.id))
            user.external_identifier = external_identifier

        if features is not None:
            merged = {**user.features, **features}
            user.features = {k: v for k, v in merged.items() if v is not None}

        pipe.set(self._key(user.id), user.model_dump_json())
        await pipe.execute()
        return user

    async def delete(self, user_id: UUID) -> bool:
        user = await self.get(user_id)
        if user is None:
            return False
        pipe = self._redis.pipeline()
        pipe.delete(self._key(user_id))
        if user.external_identifier:
            pipe.delete(self._ext_key(user.external_identifier))
        await pipe.execute()
        return True
