from .client import FeishuClient
from .errors import ok


def feishu_task_list(page_size=20, assignee=None, completed=False):
    err = FeishuClient().ensure_ready()
    if err:
        return err
    return ok({"page_size": page_size, "assignee": assignee, "completed": completed, "items": []})


def feishu_task_create(summary, due_time=None, assignee=None, description=""):
    err = FeishuClient().ensure_ready()
    if err:
        return err
    return ok({"summary": summary, "due_time": due_time, "assignee": assignee, "task_id": "TODO"})
