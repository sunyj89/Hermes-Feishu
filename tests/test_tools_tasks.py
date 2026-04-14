from hermes_lark.tools_tasks import feishu_task_create


def test_task_create_missing_credentials(monkeypatch):
    monkeypatch.delenv("FEISHU_APP_ID", raising=False)
    monkeypatch.delenv("FEISHU_APP_SECRET", raising=False)
    r = feishu_task_create("test")
    assert r["success"] is False
