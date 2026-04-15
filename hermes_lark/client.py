from __future__ import annotations

from typing import Any

import requests

from .auth import TenantAccessTokenProvider, TokenError, has_credentials
from .config import get_config
from .errors import fail, map_feishu_business_error, map_http_error, ok


class FeishuClient:
    def __init__(self, config: dict[str, Any] | None = None, session: requests.Session | None = None):
        self.config = config or get_config()
        self.session = session or requests.Session()
        self.token_provider = TenantAccessTokenProvider(config=self.config, session=self.session)
        self.ready = has_credentials()

    def ensure_ready(self):
        if not self.ready:
            return fail("missing_credentials", "FEISHU_APP_ID / FEISHU_APP_SECRET 未配置", False)
        return None

    def _resolve_token(self, access_token: str | None) -> tuple[str | None, dict[str, Any] | None]:
        if access_token:
            return access_token, None
        try:
            return self.token_provider.get_token(), None
        except TokenError as exc:
            return None, exc.error_result
        except requests.RequestException as exc:
            return None, fail("network_error", f"failed to fetch tenant_access_token: {exc}", True)
        except ValueError as exc:
            return None, fail("invalid_response", f"invalid token response: {exc}", False)

    def call_openapi(
        self,
        *,
        method: str,
        path: str,
        query: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        access_token: str | None = None,
        timeout: int | None = None,
    ):
        err = self.ensure_ready()
        if err:
            return err

        token, token_err = self._resolve_token(access_token)
        if token_err:
            return token_err

        req_headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        }
        if headers:
            req_headers.update(headers)

        url = f"{self.config['base_url']}{path}"
        timeout_s = timeout or self.config["timeout_seconds"]

        try:
            resp = self.session.request(
                method=method.upper(),
                url=url,
                params=query,
                json=body,
                headers=req_headers,
                timeout=timeout_s,
            )
        except requests.RequestException as exc:
            return fail("network_error", str(exc), True)

        payload: Any
        try:
            payload = resp.json()
        except ValueError:
            payload = {"raw": resp.text}

        if resp.status_code >= 400:
            return map_http_error(resp.status_code, payload)

        if isinstance(payload, dict) and payload.get("code", 0) != 0:
            return map_feishu_business_error(payload.get("code"), payload.get("msg", ""), payload)

        return ok(
            {
                "status_code": resp.status_code,
                "headers": dict(resp.headers),
                "body": payload,
            }
        )
