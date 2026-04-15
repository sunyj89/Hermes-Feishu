from .tools_common import execute_openapi_tool


def feishu_bitable_app(**kwargs):
    return execute_openapi_tool("feishu_bitable_app", **kwargs)


def feishu_bitable_app_table(**kwargs):
    return execute_openapi_tool("feishu_bitable_app_table", **kwargs)


def feishu_bitable_app_table_field(**kwargs):
    return execute_openapi_tool("feishu_bitable_app_table_field", **kwargs)


def feishu_bitable_app_table_record(**kwargs):
    return execute_openapi_tool("feishu_bitable_app_table_record", **kwargs)


def feishu_bitable_app_table_view(**kwargs):
    return execute_openapi_tool("feishu_bitable_app_table_view", **kwargs)
