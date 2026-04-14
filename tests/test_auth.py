from hermes_lark.auth import has_credentials


def test_has_credentials_false_when_missing(monkeypatch):
    monkeypatch.delenv("FEISHU_APP_ID", raising=False)
    monkeypatch.delenv("FEISHU_APP_SECRET", raising=False)
    assert has_credentials() is False
