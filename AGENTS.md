# AGENTS.md

- 先读取 BIDS `dataset_description.json`、NIfTI header 和 JSON sidecar；不要从文件名推断 TR 或空间坐标。
- 时间轴统一放在最后一维；每次变换记录输入、输出、参数和软件版本。
- 不覆盖原始数据；衍生文件遵循 BIDS Derivatives 命名。
- 先运行对应小类 `pytest`，再运行 Notebook；失败时报告缺失依赖、数据或不适用条件。
- 只引用可追溯论文、官方文档和仓库；没有核验 commit hash 时明确写“未固定 commit”。
- 运动、DVARS、配准和覆盖率指标必须联合解释，不以单个阈值自动替代科学判断。
