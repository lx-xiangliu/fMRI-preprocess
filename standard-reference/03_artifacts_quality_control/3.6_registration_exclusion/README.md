# 3.6_registration_exclusion: 配准失败与剔除

优化器收敛、目标值下降与解剖配准正确不等价。

## 使用条件与推荐

检查 BOLD-T1 overlays、边界、模板变形和脑覆盖；保留失败日志并用预先规定规则裁决排除。

推荐是基于文献/官方文档的**条件建议**，不是在本仓库实验中选出的最优方法。

## 实现比较

| 实现 | 输入/前提 | 科学依据与限制 | 成本/兼容性 |
|---|---|---|---|
| fMRIPrep report + BBR | T1w分割及可用 BOLD reference | 解剖边界配准与综合报告 | 高成本，需人工/自动双重审查 |
| SimpleITK rigid MI 教学例 | 有效3D T1w/BOLD物理坐标 | 实现透明，可对比未经校正/刚体结果 | 当前不是 BBR 或非线性归一化，不能自动判PASS |
| FSL epi_reg / AFNI align_epi_anat | 结构脑mask与相应输入 | 成熟跨模态配准 | 需核对左右、畸变和切片覆盖 |

## 标准步骤与参数

1. 使用根目录下载脚本取得 manifest 固定的真实样本，核对 SHA-256、mm affine 和秒单位 TR。
2. 阅读 `references.md` 的适用输入和版本记录；正式流水线参数须在下游结果前固定。
3. 运行 `few_shots/01_test.ipynb` 和 `02_retest.ipynb`。两例分别使用同一受试者的两次真实采集。
4. 查看 `results/<session>/metrics.json` 和 `comparison.png`，读 `evidence_status`、限制与原始索引；优化目标改变不是科学有效性证明。
5. 执行根目录 pytest。正式pipeline需另行输入完整confounds/组织mask/变换/生理记录，并验证报告。

## 输入、复用与验证

`src/reference.py` 导出公共 `rigid` 为 `apply`。接口及校验见根 `fmri_reference/core.py`；数据加载、绘图与实验见 `fmri_reference/demo.py` 的 `registration` 分支。公共函数可直接复用；掩模、空间变换、频带、阈值、组件选择及扫描排除规则必须按数据和目标重新明确。

教学数据为原始任务BOLD，128个确定性EPI掩模内体素仅供时间信号演示；不是完整脑去噪流水线。所有参数如4mm、0.008Hz、50mm半径和最小段长5仅是明确示例，不能直接升级为全数据推荐。

## 错误实现与证据边界

MI刚体演示将实测；扫描排除状态 REVIEW_REQUIRED。

Notebook 包含可运行的失败输入示例；缺输入会报错。不得静默替换数据、将缺失指标填0、把PCA脑信号称为aCompCor，或把采样间距统一称为解剖归一化。处理前后尺度单位可能不同，应读指标定义。

本小类完整成熟工具之间的同数据集端到端基准**未完成**。参见根 `reports/validation_summary.json` 和 `docs/remaining_validation.md`。
