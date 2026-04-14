# hermes-lark

`hermes-lark` 是一个 **Hermes Agent 原生插件**，用于把 openclaw-lark 的飞书能力迁移到 Hermes 插件机制中。

## 目标
- 与 `openclaw-lark@main` 的飞书能力保持功能对齐（MVP）
- 首发仅支持 **Feishu**
- MIT 开源协议

## 安装（仓库发布后）
```bash
hermes plugins install sunyj89/Hermes-Feishu
```

## 本地开发
```bash
python -m pytest tests/ -q
```

## 必要环境变量
- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`

> 详细能力映射见：`docs/capability-matrix.md`
