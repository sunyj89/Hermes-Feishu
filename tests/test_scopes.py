from hermes_lark.scopes import TOOL_SCOPE_MAP


def test_scope_map_contains_core_tools():
    assert "feishu_doc_read" in TOOL_SCOPE_MAP
    assert "feishu_calendar_create_event" in TOOL_SCOPE_MAP
