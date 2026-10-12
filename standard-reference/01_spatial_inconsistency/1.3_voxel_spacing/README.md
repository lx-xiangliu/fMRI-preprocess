# 1.3_voxel_spacing: 体素间距差异

不同采集的网格间距、视野、方向均可能变化。

## 使用条件与推荐

先确认坐标空间，再按完整目标 shape+affine 重采样；连续图像线性/样条、离散标签最近邻。降采样须评估抗混叠。

推荐是基于文献/官方文档的**条件建议**，不是在本仓库实验中选出的最优方法。

## 实现比较

| 实现 | 输入/前提 | 科学依据与限制 | 成本/兼容性 |
|---|---|---|---|
| NiBabel resample_to_output / resample_from_to | 已经建立世界坐标对应的 3D 图像 | 目标网格透明；参考实现适合单卷演示 | 不估计配准；4D 需按卷应用且保留时间 header |
| Nilearn resample_img | 正确 target_affine/shape | 可集成掩模与机器学习工作流 | force_resample/copy_header 需按版本固定 |
| ANTs apply transforms / FSL applywarp | 已估计的变换链 | 组合变换一次插值，适合正式流水线 | 变换方向和 RAS/LPS/FSL 约定需核对 |

## 标准步骤与参数

1. 使用根目录下载脚本取得 manifest 固定的真实样本，核对 SHA-256、mm affine 和秒单位 TR。
2. 阅读 `references.md` 的适用输入和版本记录；正式流水线参数须在下游结果前固定。
3. 运行 `few_shots/01_test.ipynb` 和 `02_retest.ipynb`。两例分别使用同一受试者的两次真实采集。
4. 查看 `results/<session>/metrics.json` 和 `comparison.png`，读 `evidence_status`、限制与原始索引；优化目标改变不是科学有效性证明。
5. 执行根目录 pytest。正式pipeline需另行输入完整confounds/组织mask/变换/生理记录，并验证报告。

## 输入、复用与验证

`src/reference.py` 导出公共 `resample_volume` 为 `apply`。接口及校验见根 `fmri_reference/core.py`；数据加载、绘图与实验见 `fmri_reference/demo.py` 的 `spacing` 分支。公共函数可直接复用；掩模、空间变换、频带、阈值、组件选择及扫描排除规则必须按数据和目标重新明确。

教学数据为原始任务BOLD，128个确定性EPI掩模内体素仅供时间信号演示；不是完整脑去噪流水线。所有参数如4mm、0.008Hz、50mm半径和最小段长5仅是明确示例，不能直接升级为全数据推荐。

## 错误实现与证据边界

重采样只统一网格，不能恢复原始分辨率；演示降采样未证明严格抗混叠。

Notebook 包含可运行的失败输入示例；缺输入会报错。不得静默替换数据、将缺失指标填0、把PCA脑信号称为aCompCor，或把采样间距统一称为解剖归一化。处理前后尺度单位可能不同，应读指标定义。

本小类完整成熟工具之间的同数据集端到端基准**未完成**。参见根 `reports/validation_summary.json` 和 `docs/remaining_validation.md`。
