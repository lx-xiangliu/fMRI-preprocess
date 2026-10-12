# 1.1_brain_shape: 脑形态差异

个体解剖形态不同；规则网格 resize 无法建立解剖对应。

## 使用条件与推荐

跨个体体素模型可采用 T1w→模板的 ANTs SyN，再组合 EPI→T1w 变换一次重采样。原生空间/表面模型可以保留个体形态。

推荐是基于文献/官方文档的**条件建议**，不是在本仓库实验中选出的最优方法。

## 实现比较

| 实现 | 输入/前提 | 科学依据与限制 | 成本/兼容性 |
|---|---|---|---|
| fMRIPrep + ANTs SyN | T1w、模板、脑提取与 BOLD 配准 | 非线性解剖对应；需逐例报告和形变检查 | 成本高，缓存模板和解剖结果；避免每窗口重复配准 |
| FSL FLIRT + FNIRT | 成人 T1w 和匹配 FNIRT 模板/配置 | 成熟组合；初始化失败会传递到非线性阶段 | 参数及模板依赖强，FSL 许可证单独审查 |
| SPM segmentation + normalization | 合适的组织先验 | 组织分割驱动，病灶和发育样本需专门先验 | MATLAB/运行时依赖；不能把体素 resize 称为归一化 |

## 标准步骤与参数

1. 使用根目录下载脚本取得 manifest 固定的真实样本，核对 SHA-256、mm affine 和秒单位 TR。
2. 阅读 `references.md` 的适用输入和版本记录；正式流水线参数须在下游结果前固定。
3. 运行 `few_shots/01_test.ipynb` 和 `02_retest.ipynb`。两例分别使用同一受试者的两次真实采集。
4. 查看 `results/<session>/metrics.json` 和 `comparison.png`，读 `evidence_status`、限制与原始索引；优化目标改变不是科学有效性证明。
5. 执行根目录 pytest。正式pipeline需另行输入完整confounds/组织mask/变换/生理记录，并验证报告。

## 输入、复用与验证

`src/reference.py` 导出公共 `fmriprep_command` 为 `apply`。接口及校验见根 `fmri_reference/core.py`；数据加载、绘图与实验见 `fmri_reference/demo.py` 的 `shape` 分支。公共函数可直接复用；掩模、空间变换、频带、阈值、组件选择及扫描排除规则必须按数据和目标重新明确。

教学数据为原始任务BOLD，128个确定性EPI掩模内体素仅供时间信号演示；不是完整脑去噪流水线。所有参数如4mm、0.008Hz、50mm半径和最小段长5仅是明确示例，不能直接升级为全数据推荐。

## 错误实现与证据边界

非线性配准、脑提取、模板与形变 Jacobian 未实测；当前仅提供真实结构/功能输入审计。

Notebook 包含可运行的失败输入示例；缺输入会报错。不得静默替换数据、将缺失指标填0、把PCA脑信号称为aCompCor，或把采样间距统一称为解剖归一化。处理前后尺度单位可能不同，应读指标定义。

本小类完整成熟工具之间的同数据集端到端基准**未完成**。参见根 `reports/validation_summary.json` 和 `docs/remaining_validation.md`。

`apply`只构建digest固定的fMRIPrep命令，不启动容器；外部Docker/模板及质量控制未满足时不得声称配准已完成。
