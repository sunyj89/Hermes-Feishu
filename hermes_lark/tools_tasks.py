from .tools_common import execute_openapi_tool


def feishu_task_list(page_size=20, assignee=None, completed=False, access_token=None):
    query = {"page_size": page_size, "completed": str(bool(completed)).lower()}
    if assignee:
        query["assignee"] = assignee
    return execute_openapi_tool(
        "feishu_task_list",
        method="GET",
        path="/open-apis/task/v2/tasks",
        query=query,
        access_token=access_token,
    )


def feishu_task_create(summary, due_time=None, assignee=None, description="", access_token=None):
    body = {"summary": summary, "description": description}
    if due_time:
        body["due_time"] = due_time
    if assignee:
        body["assignee"] = assignee
    return execute_openapi_tool(
        "feishu_task_create",
        method="POST",
        path="/open-apis/task/v2/tasks",
        body=body,
        access_token=access_token,
    )
