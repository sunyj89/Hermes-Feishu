from .errors import fail
from .tools_docs import feishu_doc_read, feishu_doc_append, feishu_doc_replace_text
from .tools_calendar import feishu_calendar_list, feishu_calendar_create_event
from .tools_tasks import feishu_task_list, feishu_task_create


def _not_implemented(tool_name):
    def _handler(**kwargs):
        return fail("not_implemented", f"{tool_name} 尚未实现（骨架阶段）", False)
    return _handler


# 已有可调用占位实现（短名称）
_IMPLEMENTED_HANDLERS = {
    "feishu_doc_read": feishu_doc_read,
    "feishu_doc_append": feishu_doc_append,
    "feishu_doc_replace_text": feishu_doc_replace_text,
    "feishu_calendar_list": feishu_calendar_list,
    "feishu_calendar_create_event": feishu_calendar_create_event,
    "feishu_task_list": feishu_task_list,
    "feishu_task_create": feishu_task_create,
}


# openclaw-lark@main 扫描出的工具名（MVP parity-required）
_PARITY_TOOL_NAMES = [
    "feishu_oauth",
    "feishu_oauth_batch_auth",
    "feishu_im_bot_image",
    "feishu_im_user_fetch_resource",
    "feishu_im_user_message",
    "feishu_im_user_get_messages",
    "feishu_im_user_get_thread_messages",
    "feishu_im_user_search_messages",
    "feishu_drive_file",
    "feishu_doc_comments",
    "feishu_doc_media",
    "feishu_create_doc",
    "feishu_fetch_doc",
    "feishu_update_doc",
    "feishu_search_doc_wiki",
    "feishu_wiki_space",
    "feishu_wiki_space_node",
    "feishu_chat",
    "feishu_chat_members",
    "feishu_get_user",
    "feishu_search_user",
    "feishu_calendar_calendar",
    "feishu_calendar_event",
    "feishu_calendar_event_attendee",
    "feishu_calendar_freebusy",
    "feishu_task_task",
    "feishu_task_subtask",
    "feishu_task_comment",
    "feishu_task_section",
    "feishu_task_tasklist",
    "feishu_sheet",
    "feishu_bitable_app",
    "feishu_bitable_app_table",
    "feishu_bitable_app_table_field",
    "feishu_bitable_app_table_record",
    "feishu_bitable_app_table_view",
]

# 人类友好短名称（alias）
_ALIAS_TOOL_NAMES = list(_IMPLEMENTED_HANDLERS.keys())


def _schema_for(tool_name):
    return {
        "name": tool_name,
        "description": f"hermes-lark tool: {tool_name}",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    }


def register_plugin(ctx):
    seen = set()

    # 先注册 parity 工具（大部分是未实现占位）
    for name in _PARITY_TOOL_NAMES:
        if name in seen:
            continue
        seen.add(name)
        handler = _IMPLEMENTED_HANDLERS.get(name, _not_implemented(name))
        ctx.register_tool(
            name=name,
            toolset="hermes-feishu",
            schema=_schema_for(name),
            handler=lambda args, _fn=handler, **kw: _fn(**args),
            description="Hermes Feishu workspace tool",
            emoji="🪽",
        )

    # 再注册短名称 alias
    for name in _ALIAS_TOOL_NAMES:
        if name in seen:
            continue
        seen.add(name)
        handler = _IMPLEMENTED_HANDLERS[name]
        ctx.register_tool(
            name=name,
            toolset="hermes-feishu",
            schema=_schema_for(name),
            handler=lambda args, _fn=handler, **kw: _fn(**args),
            description="Hermes Feishu workspace tool (alias)",
            emoji="🪽",
        )
