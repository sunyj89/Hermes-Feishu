from __future__ import annotations

from .config import get_config
from .errors import fail
from .capabilities import ALIAS_TOOL_NAMES, PARITY_TOOL_NAMES


TOOL_SCOPE_MAP = {
    # aliases
    "feishu_doc_read": ["docx:document:readonly"],
    "feishu_doc_append": ["docx:document"],
    "feishu_doc_replace_text": ["docx:document"],
    "feishu_calendar_list": ["calendar:event:readonly"],
    "feishu_calendar_create_event": ["calendar:event"],
    "feishu_task_list": ["task:task:readonly"],
    "feishu_task_create": ["task:task"],
    # parity tools
    "feishu_oauth": [],
    "feishu_oauth_batch_auth": [],
    "feishu_im_bot_image": ["im:message"],
    "feishu_im_user_fetch_resource": ["im:message:readonly"],
    "feishu_im_user_message": ["im:message"],
    "feishu_im_user_get_messages": ["im:message:readonly"],
    "feishu_im_user_get_thread_messages": ["im:message:readonly"],
    "feishu_im_user_search_messages": ["im:message:readonly"],
    "feishu_drive_file": ["drive:drive"],
    "feishu_doc_comments": ["docx:comment"],
    "feishu_doc_media": ["docx:document:readonly"],
    "feishu_create_doc": ["docx:document"],
    "feishu_fetch_doc": ["docx:document:readonly"],
    "feishu_update_doc": ["docx:document"],
    "feishu_search_doc_wiki": ["wiki:wiki:readonly"],
    "feishu_wiki_space": ["wiki:wiki"],
    "feishu_wiki_space_node": ["wiki:node"],
    "feishu_chat": ["im:chat"],
    "feishu_chat_members": ["im:chat:readonly"],
    "feishu_get_user": ["contact:user:readonly"],
    "feishu_search_user": ["contact:user:readonly"],
    "feishu_calendar_calendar": ["calendar:calendar"],
    "feishu_calendar_event": ["calendar:event"],
    "feishu_calendar_event_attendee": ["calendar:event"],
    "feishu_calendar_freebusy": ["calendar:calendar:readonly"],
    "feishu_task_task": ["task:task"],
    "feishu_task_subtask": ["task:task"],
    "feishu_task_comment": ["task:comment"],
    "feishu_task_section": ["task:section"],
    "feishu_task_tasklist": ["task:tasklist"],
    "feishu_sheet": ["sheets:spreadsheet"],
    "feishu_bitable_app": ["bitable:app"],
    "feishu_bitable_app_table": ["bitable:table"],
    "feishu_bitable_app_table_field": ["bitable:field"],
    "feishu_bitable_app_table_record": ["bitable:record"],
    "feishu_bitable_app_table_view": ["bitable:view"],
}


for _tool_name in PARITY_TOOL_NAMES + ALIAS_TOOL_NAMES:
    TOOL_SCOPE_MAP.setdefault(_tool_name, [])


def get_available_scopes() -> set[str] | None:
    raw = get_config().get("available_scopes", "")
    if not raw:
        return None
    normalized = raw.replace(";", ",").replace(" ", ",")
    values = {part.strip() for part in normalized.split(",") if part.strip()}
    return values or None


def ensure_scope_for_tool(tool_name: str):
    required = set(TOOL_SCOPE_MAP.get(tool_name, []))
    if not required:
        return None

    available = get_available_scopes()
    if available is None:
        return None

    missing = sorted(required - available)
    if missing:
        return fail(
            "permission_denied",
            f"scope precheck failed for {tool_name}, missing scopes: {', '.join(missing)}",
            False,
            {"required": sorted(required), "available": sorted(available), "missing": missing},
        )
    return None
