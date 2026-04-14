from .auth import has_credentials
from .errors import fail


class FeishuClient:
    def __init__(self):
        self.ready = has_credentials()

    def ensure_ready(self):
        if not self.ready:
            return fail("missing_credentials", "FEISHU_APP_ID / FEISHU_APP_SECRET 未配置", False)
        return None
