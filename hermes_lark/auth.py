from __future__ import annotations

import time
from typing import Any

import requests

from .config import get_config
from .errors import map_feishu_business_error, map_http_error


class TokenError(RuntimeError):
    def __init__(self, error_result: dict[str, Any]):
        super().__init__(error_result["error"]["message"])
        self.error_result = error_result


def has_credentials() -> bool:
    cfg = get_config()
    return bool(cfg["app_id"] and cfg["app_secret"])


class TenantAccessTokenProvider:
    def __init__(self, config: dict[str, Any] | None = None, session: requests.Session | None = None, now_fn=None):
        self.config = config or get_config()
        self.session = session or requests.Session()
        self.now_fn = now_fn or time.time
        self._cached_token: str | None = None
        self._expire_at: float = 0

    def get_token(self, force_refresh: bool = False) -> str:
        now = self.now_fn()
        if not force_refresh and self._cached_token and now < self._expire_at:
            return self._cached_token

        endpoint = f"{self.config['base_url']}/open-apis/auth/v3/tenant_access_token/internal"
        resp = self.session.post(
            endpoint,
            json={"app_id": self.config["app_id"], "app_secret": self.config["app_secret"]},
            timeout=self.config["timeout_seconds"],
        )
        payload = resp.json()

        if resp.status_code >= 400:
            raise TokenError(map_http_error(resp.status_code, payload))

        if payload.get("code", 0) != 0:
            raise TokenError(map_feishu_business_error(payload.get("code"), payload.get("msg", ""), payload))

        token = payload.get("tenant_access_token")
        expire = int(payload.get("expire", 7200))
        skew = int(self.config.get("token_skew_seconds", 60))
        self._cached_token = token
        self._expire_at = max(now + expire - skew, now + 1)
        return token
