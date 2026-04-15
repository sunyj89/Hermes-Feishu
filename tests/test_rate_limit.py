from hermes_lark.client import FeishuClient


class DummyResp:
    def __init__(self, status_code, payload):
        self.status_code = status_code
        self._payload = payload
        self.headers = {}
        self.text = str(payload)

    def json(self):
        return self._payload


class FakeSession:
    def __init__(self, result_status):
        self.result_status = result_status

    def post(self, url, json, timeout):
        return DummyResp(
            200,
            {"code": 0, "msg": "ok", "tenant_access_token": "token_abc", "expire": 7200},
        )

    def request(self, **kwargs):
        return DummyResp(self.result_status, {"code": 999, "msg": "mock error"})


def test_429_is_retryable(monkeypatch):
    monkeypatch.setenv("FEISHU_APP_ID", "app")
    monkeypatch.setenv("FEISHU_APP_SECRET", "secret")

    c = FeishuClient(session=FakeSession(429))
    result = c.call_openapi(method="GET", path="/open-apis/im/v1/chats")
    assert result["success"] is False
    assert result["error"]["code"] == "rate_limited"
    assert result["error"]["retryable"] is True


def test_5xx_is_retryable(monkeypatch):
    monkeypatch.setenv("FEISHU_APP_ID", "app")
    monkeypatch.setenv("FEISHU_APP_SECRET", "secret")

    c = FeishuClient(session=FakeSession(503))
    result = c.call_openapi(method="GET", path="/open-apis/im/v1/chats")
    assert result["success"] is False
    assert result["error"]["code"] == "upstream_unavailable"
    assert result["error"]["retryable"] is True
