from hermes_lark.scopes import TOOL_SCOPE_MAP
from hermes_lark.tools_common import execute_openapi_tool


def test_scope_map_contains_core_tools():
    assert "feishu_doc_read" in TOOL_SCOPE_MAP
    assert "feishu_calendar_create_event" in TOOL_SCOPE_MAP
    assert "feishu_chat" in TOOL_SCOPE_MAP


def test_scope_precheck_failed_returns_permission_denied(monkeypatch):
    monkeypatch.setenv("FEISHU_APP_ID", "app")
    monkeypatch.setenv("FEISHU_APP_SECRET", "secret")
    monkeypatch.setenv("FEISHU_AVAILABLE_SCOPES", "im:chat")

    result = execute_openapi_tool(
        "feishu_task_task",
        method="GET",
        path="/open-apis/task/v2/tasks",
    )
    assert result["success"] is False
    assert result["error"]["code"] == "permission_denied"
