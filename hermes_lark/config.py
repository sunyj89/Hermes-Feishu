import os


def get_config():
    return {
        "app_id": os.getenv("FEISHU_APP_ID", ""),
        "app_secret": os.getenv("FEISHU_APP_SECRET", ""),
        "base_url": os.getenv("FEISHU_BASE_URL", "https://open.feishu.cn"),
        "timeout_seconds": int(os.getenv("FEISHU_TIMEOUT_SECONDS", "20")),
    }
