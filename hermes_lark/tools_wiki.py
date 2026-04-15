from .tools_common import execute_openapi_tool


def feishu_wiki_space(**kwargs):
    return execute_openapi_tool("feishu_wiki_space", **kwargs)


def feishu_wiki_space_node(**kwargs):
    return execute_openapi_tool("feishu_wiki_space_node", **kwargs)


def feishu_search_doc_wiki(**kwargs):
    return execute_openapi_tool("feishu_search_doc_wiki", **kwargs)
