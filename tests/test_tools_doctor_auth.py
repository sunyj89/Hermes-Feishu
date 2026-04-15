from hermes_lark.tools_doctor_auth import feishu_auth, feishu_doctor, feishu_oauth_batch_auth


class DummyClient:
    def __init__(self):
        self.calls = []

    def _resolve_token(self, access_token=None):
        return "token_x", None

    def call_openapi(self, *, method, path, query=None, body=None, access_token=None, **kwargs):
        self.calls.append({
            "method": method,
            "path": path,
            "query": query,
            "body": body,
            "access_token": access_token,
        })
        if path == "/open-apis/contact/v3/scopes":
            return {"success": True, "data": {"body": {"code": 0, "msg": "ok"}}, "error": None}
        if path in {"/open-apis/task/v2/tasklists", "/open-apis/wiki/v2/spaces"}:
            return {
                "success": False,
                "data": None,
                "error": {
                    "code": "http_error",
                    "message": "Feishu API request failed with HTTP 400",
                    "retryable": False,
                    "details": {
                        "error": {
                            "permission_violations": [
                                {"subject": "task:tasklist:read"},
                            ]
                        }
                    },
                },
            }
        if path == "/open-apis/im/v1/messages":
            return {"success": True, "data": {"body": {"message_id": "om_1"}}, "error": None}
        return {"success": True, "data": {"body": {"code": 0}}, "error": None}


def test_feishu_auth_returns_card_without_sending(monkeypatch):
    monkeypatch.setenv("FEISHU_APP_ID", "cli_123")
    monkeypatch.setenv("FEISHU_APP_SECRET", "secret")

    result = feishu_auth(send_card=False, scopes=["offline_access", "task:task:read"])
    assert result["success"] is True
    assert result["data"]["auth_url"].startswith("https://open.feishu.cn/app/cli_123/auth")
    card = result["data"]["card"]
    assert card["schema"] == "2.0"


def test_feishu_auth_send_card_requires_receive_id(monkeypatch):
    monkeypatch.setenv("FEISHU_APP_ID", "cli_123")
    monkeypatch.setenv("FEISHU_APP_SECRET", "secret")

    result = feishu_auth(send_card=True)
    assert result["success"] is False
    assert result["error"]["code"] == "invalid_argument"


def test_feishu_oauth_batch_auth_sends_interactive_card(monkeypatch):
    monkeypatch.setenv("FEISHU_APP_ID", "cli_123")
    monkeypatch.setenv("FEISHU_APP_SECRET", "secret")
    monkeypatch.setattr("hermes_lark.tools_doctor_auth.FeishuClient", DummyClient)

    result = feishu_oauth_batch_auth(receive_id="oc_xxx", send_card=True)
    assert result["success"] is True
    body = result["data"]["message"]["body"]
    assert body["message_id"] == "om_1"


def test_feishu_doctor_builds_report_and_extracts_missing_scopes(monkeypatch):
    monkeypatch.setenv("FEISHU_APP_ID", "cli_123")
    monkeypatch.setenv("FEISHU_APP_SECRET", "secret")
    monkeypatch.setattr("hermes_lark.tools_doctor_auth.FeishuClient", DummyClient)

    result = feishu_doctor(send_card=False)
    assert result["success"] is True
    data = result["data"]
    assert "task:tasklist:read" in data["missing_scopes"]
    assert data["card"]["schema"] == "2.0"
    assert "Feishu Doctor" in data["card"]["header"]["title"]["content"]


def test_feishu_doctor_send_card(monkeypatch):
    monkeypatch.setenv("FEISHU_APP_ID", "cli_123")
    monkeypatch.setenv("FEISHU_APP_SECRET", "secret")
    monkeypatch.setattr("hermes_lark.tools_doctor_auth.FeishuClient", DummyClient)

    result = feishu_doctor(receive_id="oc_xxx", send_card=True)
    assert result["success"] is True
    assert result["data"]["message"]["body"]["message_id"] == "om_1"
