# Migration from openclaw-lark to hermes-lark

## Why
- Hermes 使用 Python 插件机制（plugin.yaml + register(ctx)）
- 不依赖 openclaw/plugin-sdk

## Steps
1. 安装 hermes-lark
2. 配置 FEISHU_APP_ID / FEISHU_APP_SECRET
3. 按 capability matrix 对照能力与参数
