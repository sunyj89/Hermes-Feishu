from hermes_lark.tools_docs import feishu_doc_replace_text


def test_replace_requires_old_text():
    r = feishu_doc_replace_text("doc_1", "", "new")
    assert r["success"] is False
    assert r["error"]["code"] == "invalid_argument"
