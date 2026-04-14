from .client import FeishuClient
from .errors import fail, ok


def feishu_doc_read(document_id, format="plain_text"):
    err = FeishuClient().ensure_ready()
    if err:
        return err
    return ok({"document_id": document_id, "format": format, "content": "TODO"})


def feishu_doc_append(document_id, text):
    err = FeishuClient().ensure_ready()
    if err:
        return err
    return ok({"document_id": document_id, "appended": len(text)})


def feishu_doc_replace_text(document_id, old_text, new_text, replace_all=False):
    if not old_text:
        return fail("invalid_argument", "old_text 不能为空", False)
    err = FeishuClient().ensure_ready()
    if err:
        return err
    return ok({"document_id": document_id, "replaced": 0, "replace_all": replace_all})
