from .client import FeishuClient
from .errors import ok


def feishu_calendar_list(start_time, end_time, calendar_id=None):
    err = FeishuClient().ensure_ready()
    if err:
        return err
    return ok({"calendar_id": calendar_id, "start_time": start_time, "end_time": end_time, "items": []})


def feishu_calendar_create_event(calendar_id, summary, start_time, end_time, description="", attendees=None):
    err = FeishuClient().ensure_ready()
    if err:
        return err
    return ok({"calendar_id": calendar_id, "summary": summary, "event_id": "TODO", "attendees": attendees or []})
