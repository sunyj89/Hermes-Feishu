from .tools_common import execute_openapi_tool


def feishu_drive_file(**kwargs):
    return execute_openapi_tool("feishu_drive_file", **kwargs)


def feishu_doc_comments(**kwargs):
    return execute_openapi_tool("feishu_doc_comments", **kwargs)


def feishu_doc_media(**kwargs):
    return execute_openapi_tool("feishu_doc_media", **kwargs)
