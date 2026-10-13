# 3.4_raw_residual_artifacts: 原始与残余伪影

畸变、鬼影、dropout 与残余噪声不能由单一指标或 z-score 去除。

## 使用条件与推荐

原始 MRIQC、校正流程报告和处理后 carpet/频谱分层审查；SDC 依赖 fieldmap/反向 PE 或有条件的 fieldmap-less 方法。

推荐是基于文献/官方文档的**条件建议**，不是在本仓库实验中选出的最优方法。

## 实现比较

| 实现 | 输入/前提 | 科学依据与限制 | 成本/兼容性 |
|---|---|---|---|
| MRIQC | 原始 BIDS BOLD/T1w | 多维 IQM+可视化 | 不自动证明可用/不可用 |
| fMRIPrep SDC | PE方向、readout和相位/反向PE | 物理/结构约束的畸变校正 | 信息缺失需报告不可用，不能编造 fieldmap |
| AFNI APQC | afni_proc 产物 | 交互质量审查及残余诊断 | 需成熟流程产物；原始DVARS不能验证校正成功 |

## 标准步骤与参数

1. 使用根目录下载脚本取得 manifest 固定的真实样本，核对 SHA-256、mm affine 和秒单位 TR。
2. 阅读 `references.md` 的适用输入和版本记录；正式流水线参数须在下游结果前固定。
3. 运行 `few_shots/01_test.ipynb` 和 `02_retest.ipynb`。两例分别使用同一受试者的两次真实采集。
4. 查看 `results/<session>/metrics.json` 和 `comparison.png`，读 `evidence_status`、限制与原始索引；优化目标改变不是科学有效性证明。
5. 执行根目录 pytest。正式pipeline需另行输入完整confounds/组织mask/变换/生理记录，并验证报告。

## 输入、复用与验证

`src/reference.py` 导出公共 `drift_basis` 为 `apply`。接口及校验见根 `fmri_reference/core.py`；数据加载、绘图与实验见 `fmri_reference/demo.py` 的 `artifacts` 分支。公共函数可直接复用；掩模、空间变换、频带、阈值、组件选择及扫描排除规则必须按数据和目标重新明确。

教学数据为原始任务BOLD，128个确定性EPI掩模内体素仅供时间信号演示；不是完整脑去噪流水线。所有参数如4mm、0.008Hz、50mm半径和最小段长5仅是明确示例，不能直接升级为全数据推荐。

## 错误实现与证据边界

示例仅真实 raw carpet 与简单漂移模型残差；SDC、鬼影指标未实测。

Notebook 包含可运行的失败输入示例；缺输入会报错。不得静默替换数据、将缺失指标填0、把PCA脑信号称为aCompCor，或把采样间距统一称为解剖归一化。处理前后尺度单位可能不同，应读指标定义。

本小类完整成熟工具之间的同数据集端到端基准**未完成**。参见根 `reports/validation_summary.json` 和 `docs/remaining_validation.md`。
