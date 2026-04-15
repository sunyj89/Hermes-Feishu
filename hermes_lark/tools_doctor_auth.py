from __future__ import annotations

import json
import time
from typing import Any
from urllib.parse import quote

from .client import FeishuClient
from .config import get_config
from .errors import fail, ok
from .tools_common import execute_openapi_tool


def _get_open_domain(base_url: str | None = None) -> str:
    if base_url:
        return base_url.rstrip("/")
    cfg = get_config()
    host = cfg["base_url"]
    if "larksuite" in host:
        return "https://open.larksuite.com"
    return "https://open.feishu.cn"


def _build_auth_url(scopes: list[str], token_type: str = "user") -> str:
    cfg = get_config()
    app_id = cfg.get("app_id", "")
    if not app_id:
        return ""
    open_domain = _get_open_domain()
    scope_q = quote(",".join(scopes), safe=",:_")
    token_q = quote(token_type, safe="")
    return (
        f"{open_domain}/app/{app_id}/auth"
        f"?q={scope_q}&op_from=hermes-lark&token_type={token_q}"
    )


def _build_auth_card(auth_url: str, scopes: list[str], title: str = "Feishu Auth") -> dict[str, Any]:
    scope_lines = "\n".join(f"- `{s}`" for s in scopes) if scopes else "- `offline_access`"
    markdown = (
        "请点击按钮完成授权。\n\n"
        f"**申请权限**：\n{scope_lines}\n\n"
        "授权完成后，你可以继续对话让我重试刚才的操作。"
    )
    return {
        "schema": "2.0",
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": title},
            "template": "blue",
        },
        "body": {
            "elements": [
                {"tag": "markdown", "content": markdown},
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {"tag": "plain_text", "content": "前往授权"},
                            "type": "primary",
                            "multi_url": {
                                "url": auth_url,
                                "pc_url": auth_url,
                                "ios_url": auth_url,
                                "android_url": auth_url,
                            },
                            "value": {"hermes_action": "feishu_auth_open"},
                        }
                    ],
                },
            ]
        },
    }


def _build_doctor_card(report_markdown: str) -> dict[str, Any]:
    return {
        "schema": "2.0",
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": "Feishu Doctor"},
            "template": "turquoise",
        },
        "body": {
            "elements": [
                {"tag": "markdown", "content": report_markdown},
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {"tag": "plain_text", "content": "重新诊断"},
                            "type": "default",
                            "value": {"hermes_action": "feishu_doctor_recheck"},
                        }
                    ],
                },
            ]
        },
    }


def _send_interactive_card(
    client: FeishuClient,
    *,
    receive_id: str,
    receive_id_type: str = "chat_id",
    card: dict[str, Any],
    access_token: str | None = None,
):
    if receive_id_type not in {"chat_id", "open_id", "user_id", "union_id", "email"}:
        return fail("invalid_argument", f"unsupported receive_id_type: {receive_id_type}", False)

    return client.call_openapi(
        method="POST",
        path="/open-apis/im/v1/messages",
        query={"receive_id_type": receive_id_type},
        body={
            "receive_id": receive_id,
            "msg_type": "interactive",
            "content": json.dumps(card, ensure_ascii=False),
        },
        access_token=access_token,
    )


def feishu_auth(
    receive_id: str | None = None,
    receive_id_type: str = "chat_id",
    scopes: list[str] | None = None,
    token_type: str = "user",
    send_card: bool = True,
    access_token: str | None = None,
    action: str | None = None,
    **kwargs,
):
    if action == "help":
        return ok(
            {
                "tool": "feishu_auth",
                "params": [
                    "receive_id",
                    "receive_id_type",
                    "scopes",
                    "token_type",
                    "send_card",
                ],
            }
        )

    cfg = get_config()
    if not cfg.get("app_id"):
        return fail("missing_credentials", "FEISHU_APP_ID 未配置", False)

    requested_scopes = scopes or ["offline_access"]
    auth_url = _build_auth_url(requested_scopes, token_type=token_type)
    card = _build_auth_card(auth_url, requested_scopes)

    data: dict[str, Any] = {
        "auth_url": auth_url,
        "scopes": requested_scopes,
        "card": card,
        "send_card": bool(send_card),
    }

    if not send_card:
        return ok(data)

    if not receive_id:
        return fail("invalid_argument", "send_card=true 时必须提供 receive_id", False, data)

    client = FeishuClient()
    sent = _send_interactive_card(
        client,
        receive_id=receive_id,
        receive_id_type=receive_id_type,
        card=card,
        access_token=access_token,
    )
    if not sent.get("success"):
        return sent

    data["message"] = sent.get("data")
    return ok(data)


def feishu_oauth(**kwargs):
    return feishu_auth(**kwargs)


def feishu_oauth_batch_auth(
    receive_id: str | None = None,
    receive_id_type: str = "chat_id",
    scopes: list[str] | None = None,
    send_card: bool = True,
    access_token: str | None = None,
    action: str | None = None,
    **kwargs,
):
    if action == "help":
        return feishu_auth(action="help")

    requested = scopes or [
        "offline_access",
        "task:task:read",
        "task:task:write",
        "calendar:event:read",
        "calendar:event:write",
        "docx:document:readonly",
        "docx:document",
    ]
    return feishu_auth(
        receive_id=receive_id,
        receive_id_type=receive_id_type,
        scopes=requested,
        token_type="user",
        send_card=send_card,
        access_token=access_token,
    )


def feishu_doctor(
    receive_id: str | None = None,
    receive_id_type: str = "chat_id",
    send_card: bool = True,
    access_token: str | None = None,
    action: str | None = None,
    **kwargs,
):
    if action == "help":
        return ok(
            {
                "tool": "feishu_doctor",
                "params": ["receive_id", "receive_id_type", "send_card"],
            }
        )

    cfg = get_config()
    checks: list[dict[str, Any]] = []

    if not cfg.get("app_id") or not cfg.get("app_secret"):
        return fail("missing_credentials", "FEISHU_APP_ID / FEISHU_APP_SECRET 未配置", False)

    client = FeishuClient()

    token_probe = client._resolve_token(access_token)
    token_ok = token_probe[1] is None and bool(token_probe[0])
    checks.append({"name": "tenant_access_token", "ok": token_ok, "detail": token_probe[1]})

    probes = [
        ("contact_scopes", "GET", "/open-apis/contact/v3/scopes", None),
        ("task_tasklist", "GET", "/open-apis/task/v2/tasklists", {"page_size": "1"}),
        ("wiki_spaces", "GET", "/open-apis/wiki/v2/spaces", {"page_size": "1"}),
    ]

    for name, method, path, query in probes:
        r = client.call_openapi(method=method, path=path, query=query, access_token=access_token)
        checks.append({"name": name, "ok": bool(r.get("success")), "result": r})

    missing_scopes = []
    for c in checks:
        err = (c.get("result") or {}).get("error") or c.get("detail") or {}
        details = err.get("details") if isinstance(err, dict) else None
        if isinstance(details, dict):
            violations = details.get("error", {}).get("permission_violations", [])
            if isinstance(violations, list):
                for item in violations:
                    subject = item.get("subject") if isinstance(item, dict) else None
                    if subject:
                        missing_scopes.append(subject)

    missing_scopes = sorted(set(missing_scopes))

    lines = [
        f"- 检查时间: {int(time.time())}",
        f"- App ID: `{cfg.get('app_id')}`",
    ]
    for c in checks:
        icon = "✅" if c.get("ok") else "❌"
        lines.append(f"- {icon} `{c['name']}`")
    if missing_scopes:
        lines.append("\n**检测到缺失权限（来自飞书返回）**")
        lines.extend(f"- `{s}`" for s in missing_scopes)

    report = "\n".join(lines)
    card = _build_doctor_card(report)

    data = {"checks": checks, "missing_scopes": missing_scopes, "report_markdown": report, "card": card}
    if not send_card:
        return ok(data)

    if not receive_id:
        return fail("invalid_argument", "send_card=true 时必须提供 receive_id", False, data)

    sent = _send_interactive_card(
        client,
        receive_id=receive_id,
        receive_id_type=receive_id_type,
        card=card,
        access_token=access_token,
    )
    if not sent.get("success"):
        return sent

    data["message"] = sent.get("data")
    return ok(data)


def feishu_my_tool(**kwargs):
    # Compatibility placeholder from openclaw-lark inventory.
    return execute_openapi_tool("feishu_my_tool", **kwargs)


def my_oapi_tool(**kwargs):
    # Compatibility placeholder from openclaw-lark inventory.
    return execute_openapi_tool("my_oapi_tool", **kwargs)


def ask_user_form(**kwargs):
    # Compatibility placeholder from openclaw-lark inventory.
    return execute_openapi_tool("ask_user_form", **kwargs)


def my_tool(**kwargs):
    # Compatibility placeholder from openclaw-lark inventory.
    return execute_openapi_tool("my_tool", **kwargs)
