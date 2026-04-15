from __future__ import annotations

from typing import Any

from .client import FeishuClient
from .errors import fail, ok
from .scopes import ensure_scope_for_tool

ALLOWED_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE"}


def execute_openapi_tool(tool_name: str, **kwargs):
    action = kwargs.get("action", "call")

    if action == "help":
        return ok(
            {
                "tool": tool_name,
                "protocol": {
                    "action": "call|help",
                    "method": "GET|POST|PUT|PATCH|DELETE",
                    "path": "OpenAPI path, must start with /",
                    "query": "object, optional",
                    "body": "object, optional",
                    "access_token": "optional token override",
                },
            }
        )

    if action != "call":
        return fail("invalid_argument", f"unsupported action: {action}", False)

    method = kwargs.get("method")
    path = kwargs.get("path")
    query = kwargs.get("query")
    body = kwargs.get("body")
    access_token = kwargs.get("access_token")

    if not isinstance(method, str) or not method.strip():
        return fail("invalid_argument", "method is required and must be string", False)
    if method.upper() not in ALLOWED_METHODS:
        return fail("invalid_argument", f"unsupported method: {method}", False)
    if not isinstance(path, str) or not path.startswith("/"):
        return fail("invalid_argument", "path is required and must start with '/'", False)
    if query is not None and not isinstance(query, dict):
        return fail("invalid_argument", "query must be an object", False)
    if body is not None and not isinstance(body, dict):
        return fail("invalid_argument", "body must be an object", False)

    scope_error = ensure_scope_for_tool(tool_name)
    if scope_error:
        return scope_error

    return FeishuClient().call_openapi(
        method=method,
        path=path,
        query=query,
        body=body,
        access_token=access_token,
    )
