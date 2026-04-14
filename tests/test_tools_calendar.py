from hermes_lark.tools_calendar import feishu_calendar_list


def test_calendar_list_missing_credentials(monkeypatch):
    monkeypatch.delenv("FEISHU_APP_ID", raising=False)
    monkeypatch.delenv("FEISHU_APP_SECRET", raising=False)
    r = feishu_calendar_list("2026-01-01T00:00:00Z", "2026-01-02T00:00:00Z")
    assert r["success"] is False
