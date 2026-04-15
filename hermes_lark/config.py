import os


def _get_int(name: str, default: int) -> int:
    raw = os.getenv(name, str(default))
    try:
        return int(raw)
    except ValueError:
        return default


def get_config():
    return {
        "app_id": os.getenv("FEISHU_APP_ID", "").strip(),
        "app_secret": os.getenv("FEISHU_APP_SECRET", "").strip(),
        "base_url": os.getenv("FEISHU_BASE_URL", "https://open.feishu.cn").rstrip("/"),
        "timeout_seconds": _get_int("FEISHU_TIMEOUT_SECONDS", 20),
        "token_skew_seconds": _get_int("FEISHU_TOKEN_SKEW_SECONDS", 60),
        "available_scopes": os.getenv("FEISHU_AVAILABLE_SCOPES", ""),
    }
