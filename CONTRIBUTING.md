# Contributing

## Development
```bash
python -m pytest tests/ -q
```

## Conventions
- 工具返回统一 JSON：success/data/error
- 不在 import 阶段进行网络调用
- 新增能力前先更新 docs/capability-matrix.md
