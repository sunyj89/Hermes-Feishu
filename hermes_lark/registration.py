from .capabilities import ALIAS_TOOL_NAMES, PARITY_TOOL_NAMES
from .tools_calendar import feishu_calendar_create_event, feishu_calendar_list
from .tools_common import execute_openapi_tool
from .tools_docs import feishu_doc_append, feishu_doc_read, feishu_doc_replace_text
from .tools_tasks import feishu_task_create, feishu_task_list


_IMPLEMENTED_ALIAS_HANDLERS = {
    "feishu_doc_read": feishu_doc_read,
    "feishu_doc_append": feishu_doc_append,
    "feishu_doc_replace_text": feishu_doc_replace_text,
    "feishu_calendar_list": feishu_calendar_list,
    "feishu_calendar_create_event": feishu_calendar_create_event,
    "feishu_task_list": feishu_task_list,
    "feishu_task_create": feishu_task_create,
}


def _schema_for(tool_name):
    return {
        "name": tool_name,
        "description": f"hermes-lark tool: {tool_name}",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "call|help", "default": "call"},
                "method": {"type": "string", "description": "HTTP method for call"},
                "path": {"type": "string", "description": "Feishu OpenAPI path, starts with /"},
                "query": {"type": "object", "description": "query string object"},
                "body": {"type": "object", "description": "request JSON body"},
                "access_token": {"type": "string", "description": "optional token override"},
            },
            "required": [],
        },
    }


def _wrap_handler(name, fn):
    return lambda args, _fn=fn, **kw: _fn(**(args or {}))


def register_plugin(ctx):
    seen = set()

    for name in PARITY_TOOL_NAMES:
        if name in seen:
            continue
        seen.add(name)
        handler = _wrap_handler(name, lambda _tool=name, **args: execute_openapi_tool(_tool, **args))
        ctx.register_tool(
            name=name,
            toolset="hermes-feishu",
            schema=_schema_for(name),
            handler=handler,
            description="Hermes Feishu workspace tool",
            emoji="🪽",
        )

    for name in ALIAS_TOOL_NAMES:
        if name in seen:
            continue
        seen.add(name)
        alias_handler = _IMPLEMENTED_ALIAS_HANDLERS[name]
        ctx.register_tool(
            name=name,
            toolset="hermes-feishu",
            schema=_schema_for(name),
            handler=_wrap_handler(name, alias_handler),
            description="Hermes Feishu workspace tool (alias)",
            emoji="🪽",
        )
