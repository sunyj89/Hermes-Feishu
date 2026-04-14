def ok(data):
    return {"success": True, "data": data, "error": None}


def fail(code, message, retryable=False):
    return {
        "success": False,
        "data": None,
        "error": {
            "code": code,
            "message": message,
            "retryable": retryable,
        },
    }
