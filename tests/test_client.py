from hermes_lark.client import FeishuClient


def test_client_reports_missing_credentials(monkeypatch):
    monkeypatch.delenv("FEISHU_APP_ID", raising=False)
    monkeypatch.delenv("FEISHU_APP_SECRET", raising=False)
    c = FeishuClient()
    err = c.ensure_ready()
    assert err and err["success"] is False
    assert err["error"]["code"] == "missing_credentials"
