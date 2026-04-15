from .tools_common import execute_openapi_tool


def feishu_calendar_list(start_time, end_time, calendar_id=None, access_token=None):
    query = {"start_time": start_time, "end_time": end_time}
    if calendar_id:
        query["calendar_id"] = calendar_id
    return execute_openapi_tool(
        "feishu_calendar_list",
        method="GET",
        path="/open-apis/calendar/v4/calendars/primary/events",
        query=query,
        access_token=access_token,
    )


def feishu_calendar_create_event(calendar_id, summary, start_time, end_time, description="", attendees=None, access_token=None):
    body = {
        "summary": summary,
        "description": description,
        "start_time": start_time,
        "end_time": end_time,
        "attendees": attendees or [],
    }
    return execute_openapi_tool(
        "feishu_calendar_create_event",
        method="POST",
        path=f"/open-apis/calendar/v4/calendars/{calendar_id}/events",
        body=body,
        access_token=access_token,
    )
