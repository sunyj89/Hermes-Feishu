from hermes_lark.capabilities import ALIAS_TOOL_NAMES, PARITY_TOOL_NAMES
from hermes_lark.registration import register_plugin


class DummyCtx:
    def __init__(self):
        self.tools = []

    def register_tool(self, **kwargs):
        self.tools.append(kwargs)


def _get_tool(ctx, name):
    for tool in ctx.tools:
        if tool["name"] == name:
            return tool
    raise AssertionError(f"tool not found: {name}")


def test_register_plugin_registers_all_parity_and_alias_tools():
    ctx = DummyCtx()
    register_plugin(ctx)
    names = {t["name"] for t in ctx.tools}

    assert set(PARITY_TOOL_NAMES).issubset(names)
    assert set(ALIAS_TOOL_NAMES).issubset(names)


def test_parity_handlers_are_executable_and_not_not_implemented_text():
    ctx = DummyCtx()
    register_plugin(ctx)

    for name in PARITY_TOOL_NAMES:
        handler = _get_tool(ctx, name)["handler"]
        result = handler({"action": "help"})
        assert result["success"] is True
        assert "not_implemented" not in str(result).lower()


def test_parity_handler_validation_error_path():
    ctx = DummyCtx()
    register_plugin(ctx)

    handler = _get_tool(ctx, "feishu_chat")["handler"]
    result = handler({})
    assert result["success"] is False
    assert result["error"]["code"] == "invalid_argument"
