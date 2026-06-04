from enum import Enum

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings


class CacheTypes(Enum):
    file = "file"
    redis = "redis"


class Config(BaseSettings):
    # Values can be overriden by envvars.

    USE_CACHE: bool = True
    CACHE_TYPE: CacheTypes = CacheTypes.file
    REDIS_CONNECTION_URL: str = ""
    FEATURE_GATING_ENABLED: bool = False
    ADMIN_API_KEY: str = ""

    @field_validator("USE_CACHE", mode="before")
    def validate_use_cache(cls, value):
        # Return default if value is an empty string
        if value == "":
            return True  # Default value for USE_CACHE
        return value

    @field_validator("CACHE_TYPE", mode="before")
    def validate_cache_type(cls, value):
        # Thanks https://stackoverflow.com/a/78157474
        if value == "":
            return "file"
        return value

    @field_validator("FEATURE_GATING_ENABLED", mode="before")
    def validate_feature_gating(cls, value):
        if value == "":
            return False
        return value

    @model_validator(mode="after")
    def validate_config(self):
        if self.FEATURE_GATING_ENABLED:
            if not self.REDIS_CONNECTION_URL:
                raise ValueError(
                    "REDIS_CONNECTION_URL required when FEATURE_GATING_ENABLED=true"
                )
            if not self.ADMIN_API_KEY:
                raise ValueError(
                    "ADMIN_API_KEY required when FEATURE_GATING_ENABLED=true"
                )

        match self.CACHE_TYPE:
            case CacheTypes.file:
                if self.REDIS_CONNECTION_URL and not self.FEATURE_GATING_ENABLED:
                    raise ValueError(
                        "REDIS_CONNECTION_URL provided when File cache selected. "
                        "To use Redis as a cache, set CACHE_TYPE=redis."
                    )
            case CacheTypes.redis:
                if not self.REDIS_CONNECTION_URL:
                    raise ValueError(
                        "REDIS_CONNECTION_URL not provided when Redis cache selected. "
                        "To use File cache, set CACHE_TYPE=file."
                    )
        return self
