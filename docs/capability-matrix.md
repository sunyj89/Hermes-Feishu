# Capability Matrix (Frozen Baseline)

Source of truth: `openclaw-lark@main`  
Source repo: `https://github.com/larksuite/openclaw-lark`

> 状态字段：`parity-required` / `deferred` / `done`

## A. Metadata
- Baseline branch: `main`
- Baseline commit: `1e2a7422bdea69ab297657d448bc24c0cc88cfd7`
- Matrix updated at: `2026-04-14`
- Owner: `sunyj89`
- MVP policy: 覆盖 openclaw-lark 当前支持的全部 **Feishu** 能力

## B. Capability Rows (from openclaw-lark tool names)

| Domain | OpenClaw Tool Name | Hermes Tool Name (planned) | MVP Status | Notes |
|---|---|---|---|---|
| auth | feishu_oauth | feishu_oauth | parity-required | |
| auth | feishu_oauth_batch_auth | feishu_oauth_batch_auth | parity-required | |
| im | feishu_im_bot_image | feishu_im_bot_image | parity-required | |
| im | feishu_im_user_fetch_resource | feishu_im_user_fetch_resource | parity-required | |
| im | feishu_im_user_message | feishu_im_user_message | parity-required | |
| im | feishu_im_user_get_messages | feishu_im_user_get_messages | parity-required | |
| im | feishu_im_user_get_thread_messages | feishu_im_user_get_thread_messages | parity-required | |
| im | feishu_im_user_search_messages | feishu_im_user_search_messages | parity-required | |
| drive/doc | feishu_drive_file | feishu_drive_file | parity-required | |
| drive/doc | feishu_doc_comments | feishu_doc_comments | parity-required | |
| drive/doc | feishu_doc_media | feishu_doc_media | parity-required | |
| docs(mcp) | feishu_create_doc | feishu_create_doc | parity-required | |
| docs(mcp) | feishu_fetch_doc | feishu_fetch_doc | parity-required | |
| docs(mcp) | feishu_update_doc | feishu_update_doc | parity-required | |
| search | feishu_search_doc_wiki | feishu_search_doc_wiki | parity-required | |
| wiki | feishu_wiki_space | feishu_wiki_space | parity-required | |
| wiki | feishu_wiki_space_node | feishu_wiki_space_node | parity-required | |
| chat | feishu_chat | feishu_chat | parity-required | |
| chat | feishu_chat_members | feishu_chat_members | parity-required | |
| users | feishu_get_user | feishu_get_user | parity-required | |
| users | feishu_search_user | feishu_search_user | parity-required | |
| calendar | feishu_calendar_calendar | feishu_calendar_calendar | parity-required | |
| calendar | feishu_calendar_event | feishu_calendar_event | parity-required | |
| calendar | feishu_calendar_event_attendee | feishu_calendar_event_attendee | parity-required | |
| calendar | feishu_calendar_freebusy | feishu_calendar_freebusy | parity-required | |
| task | feishu_task_task | feishu_task_task | parity-required | |
| task | feishu_task_subtask | feishu_task_subtask | parity-required | |
| task | feishu_task_comment | feishu_task_comment | parity-required | |
| task | feishu_task_section | feishu_task_section | parity-required | |
| task | feishu_task_tasklist | feishu_task_tasklist | parity-required | |
| sheets | feishu_sheet | feishu_sheet | parity-required | |
| bitable | feishu_bitable_app | feishu_bitable_app | parity-required | |
| bitable | feishu_bitable_app_table | feishu_bitable_app_table | parity-required | |
| bitable | feishu_bitable_app_table_field | feishu_bitable_app_table_field | parity-required | |
| bitable | feishu_bitable_app_table_record | feishu_bitable_app_table_record | parity-required | |
| bitable | feishu_bitable_app_table_view | feishu_bitable_app_table_view | parity-required | |

## C. Hermes Short-Name Alias Layer (optional)

为了提升可读性，可在 `hermes-lark` 内增加 alias（保持对上表主工具名兼容）：
- `feishu_doc_read` → `feishu_fetch_doc`
- `feishu_doc_append` / `feishu_doc_replace_text` → `feishu_update_doc`
- `feishu_calendar_list` → `feishu_calendar_event`
- `feishu_calendar_create_event` → `feishu_calendar_event`
- `feishu_task_list` / `feishu_task_create` → `feishu_task_task`

## D. Error Mapping (draft)

| OpenClaw Error | Hermes error.code | retryable | Notes |
|---|---|---|---|
| permission denied | permission_denied | false | |
| rate limited | rate_limited | true | 需指数退避 |
| not found | not_found | false | |
| auth failed | auth_failed | false | |
| conflict | conflict | false | 幂等冲突 |

## E. Completion Checklist
- [x] 已填写 baseline commit SHA
- [x] 已罗列 openclaw-lark@main 全部 Feishu 工具名（按静态扫描）
- [ ] 每个能力补齐参数与 scope 映射
- [ ] parity-required 能力在 hermes_lark/ 已实现并有测试
- [ ] 发布前跑通真实 Feishu 环境联调
