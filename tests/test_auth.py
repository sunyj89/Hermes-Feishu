from hermes_lark.auth import TenantAccessTokenProvider, has_credentials


class DummyResp:
    def __init__(self, status_code, payload):
        self.status_code = status_code
        self._payload = payload

    def json(self):
        return self._payload


class FakeSession:
    def __init__(self):
        self.calls = 0

    def post(self, url, json, timeout):
        self.calls += 1
        return DummyResp(
            200,
            {"code": 0, "msg": "ok", "tenant_access_token": "token_abc", "expire": 120},
        )


def test_has_credentials_false_when_missing(monkeypatch):
    monkeypatch.delenv("FEISHU_APP_ID", raising=False)
    monkeypatch.delenv("FEISHU_APP_SECRET", raising=False)
    assert has_credentials() is False


def test_tenant_token_provider_caches_token_until_expire():
    now = [1000]
    cfg = {
        "app_id": "app",
        "app_secret": "secret",
        "base_url": "https://open.feishu.cn",
        "timeout_seconds": 20,
        "token_skew_seconds": 60,
    }
    session = FakeSession()
    provider = TenantAccessTokenProvider(config=cfg, session=session, now_fn=lambda: now[0])

    first = provider.get_token()
    second = provider.get_token()

    assert first == "token_abc"
    assert second == "token_abc"
    assert session.calls == 1

    now[0] = 1065
    third = provider.get_token()
    assert third == "token_abc"
    assert session.calls == 2
