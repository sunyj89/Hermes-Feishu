from hermes_lark.registration import register_plugin


class DummyCtx:
    def __init__(self):
        self.tools = []

    def register_tool(self, **kwargs):
        self.tools.append(kwargs)


def test_register_plugin_registers_tools():
    ctx = DummyCtx()
    register_plugin(ctx)
    names = [t["name"] for t in ctx.tools]
    assert "feishu_doc_read" in names
    assert "feishu_calendar_list" in names
    assert "feishu_task_create" in names
