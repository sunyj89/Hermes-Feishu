from __future__ import annotations

from typing import Any


def ok(data: Any) -> dict[str, Any]:
    return {"success": True, "data": data, "error": None}


def fail(code: str, message: str, retryable: bool = False, details: Any | None = None) -> dict[str, Any]:
    error = {
        "code": code,
        "message": message,
        "retryable": retryable,
    }
    if details is not None:
        error["details"] = details
    return {
        "success": False,
        "data": None,
        "error": error,
    }


def map_http_error(status_code: int, body: Any = None) -> dict[str, Any]:
    message = f"Feishu API request failed with HTTP {status_code}"
    if status_code == 401:
        return fail("auth_failed", message, False, body)
    if status_code == 403:
        return fail("permission_denied", message, False, body)
    if status_code == 404:
        return fail("not_found", message, False, body)
    if status_code == 409:
        return fail("conflict", message, False, body)
    if status_code == 429:
        return fail("rate_limited", message, True, body)
    if status_code >= 500:
        return fail("upstream_unavailable", message, True, body)
    return fail("http_error", message, False, body)


def map_feishu_business_error(code: Any, message: str, body: Any = None) -> dict[str, Any]:
    msg = message or "Feishu API business error"
    lowered = msg.lower()
    if "scope" in lowered or "permission" in lowered:
        return fail("permission_denied", msg, False, body)
    if "rate" in lowered or str(code) in {"429", "99991400"}:
        return fail("rate_limited", msg, True, body)
    if str(code) in {"99991663", "99991664"}:
        return fail("permission_denied", msg, False, body)
    return fail("upstream_error", msg, False, body)
