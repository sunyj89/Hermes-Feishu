from .errors import fail
from .tools_common import execute_openapi_tool


def feishu_doc_read(document_id, format="plain_text", access_token=None):
    return execute_openapi_tool(
        "feishu_doc_read",
        method="GET",
        path=f"/open-apis/docx/v1/documents/{document_id}",
        query={"format": format},
        access_token=access_token,
    )


def feishu_doc_append(document_id, text, access_token=None):
    return execute_openapi_tool(
        "feishu_doc_append",
        method="PATCH",
        path=f"/open-apis/docx/v1/documents/{document_id}/blocks/{document_id}",
        body={"append_text": text},
        access_token=access_token,
    )


def feishu_doc_replace_text(document_id, old_text, new_text, replace_all=False, access_token=None):
    if not old_text:
        return fail("invalid_argument", "old_text 不能为空", False)
    return execute_openapi_tool(
        "feishu_doc_replace_text",
        method="PATCH",
        path=f"/open-apis/docx/v1/documents/{document_id}",
        body={"old_text": old_text, "new_text": new_text, "replace_all": replace_all},
        access_token=access_token,
    )
