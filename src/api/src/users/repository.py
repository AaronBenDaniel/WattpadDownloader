from __future__ import annotations

import abc
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class FeatureGrant(BaseModel):
    expires_at: Optional[datetime] = None
    value: Optional[float] = None

    @property
    def is_active(self) -> bool:
        if self.expires_at is None:
            return True
        return datetime.now(timezone.utc) < self.expires_at


class UserRecord(BaseModel):
    id: UUID
    external_identifier: str = ""
    features: dict[str, FeatureGrant] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def active_features(self) -> list[str]:
        return [k for k, v in self.features.items() if v.is_active]

    def has_feature(self, feature: str) -> bool:
        grant = self.features.get(feature)
        return grant is not None and grant.is_active

    def feature_value(self, feature: str) -> float | None:
        grant = self.features.get(feature)
        if grant is None or not grant.is_active:
            return None
        return grant.value


class UserRepository(abc.ABC):
    @abc.abstractmethod
    async def create(
        self,
        features: dict[str, FeatureGrant] | None = None,
        external_identifier: str = "",
    ) -> UserRecord: ...

    @abc.abstractmethod
    async def get(self, user_id: UUID) -> UserRecord | None: ...

    @abc.abstractmethod
    async def get_by_external_identifier(
        self, external_identifier: str
    ) -> UserRecord | None: ...

    @abc.abstractmethod
    async def update(
        self,
        user_id: UUID,
        features: dict[str, FeatureGrant | None] | None = None,
        external_identifier: str | None = None,
    ) -> UserRecord | None: ...

    @abc.abstractmethod
    async def delete(self, user_id: UUID) -> bool: ...
