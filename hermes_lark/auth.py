from .config import get_config


def has_credentials():
    cfg = get_config()
    return bool(cfg["app_id"] and cfg["app_secret"])
