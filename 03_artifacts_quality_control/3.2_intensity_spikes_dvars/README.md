# 3.2_intensity_spikes_dvars: 强度突变与 DVARS

DVARS 是相邻卷差的 RMS，raw/standardized DVARS 单位与定义不同。

## 使用条件与推荐

在明确掩模和处理阶段上计算并联看 carpet/FD；标准化 DVARS 用正式实现，阈值由方案指定。

推荐是基于文献/官方文档的**条件建议**，不是在本仓库实验中选出的最优方法。

## 实现比较

| 实现 | 输入/前提 | 科学依据与限制 | 成本/兼容性 |
|---|---|---|---|
| 直接 raw DVARS RMS | 同一掩模连续观测 | 定义可审计，首点未定义 | 强度单位依赖，当前仅128个示例体素 |
| MRIQC / fMRIPrep standardized DVARS | 运动校正与掩模/尺度模型 | 可比性更好 | raw 阈值不能直接套 standardized 值 |
| AFNI 3dDespike / spike regression | 任务设计/混杂与异常策略明确 | 提供局部/卷级不同处理 | 可能损伤真实任务响应，不默认修改所有尖峰 |

## 标准步骤与参数

1. 使用根目录下载脚本取得 manifest 固定的真实样本，核对 SHA-256、mm affine 和秒单位 TR。
2. 阅读 `references.md` 的适用输入和版本记录；正式流水线参数须在下游结果前固定。
3. 运行 `few_shots/01_test.ipynb` 和 `02_retest.ipynb`。两例分别使用同一受试者的两次真实采集。
4. 查看 `results/<session>/metrics.json` 和 `comparison.png`，读 `evidence_status`、限制与原始索引；优化目标改变不是科学有效性证明。
5. 执行根目录 pytest。正式pipeline需另行输入完整confounds/组织mask/变换/生理记录，并验证报告。

## 输入、复用与验证

`src/reference.py` 导出公共 `dvars` 为 `apply`。接口及校验见根 `fmri_reference/core.py`；数据加载、绘图与实验见 `fmri_reference/demo.py` 的 `dvars` 分支。公共函数可直接复用；掩模、空间变换、频带、阈值、组件选择及扫描排除规则必须按数据和目标重新明确。

教学数据为原始任务BOLD，128个确定性EPI掩模内体素仅供时间信号演示；不是完整脑去噪流水线。所有参数如4mm、0.008Hz、50mm半径和最小段长5仅是明确示例，不能直接升级为全数据推荐。

## 错误实现与证据边界

raw DVARS 已测，standardized DVARS 和异常卷排除结论未测。

Notebook 包含可运行的失败输入示例；缺输入会报错。不得静默替换数据、将缺失指标填0、把PCA脑信号称为aCompCor，或把采样间距统一称为解剖归一化。处理前后尺度单位可能不同，应读指标定义。

本小类完整成熟工具之间的同数据集端到端基准**未完成**。参见根 `reports/validation_summary.json` 和 `docs/remaining_validation.md`。
