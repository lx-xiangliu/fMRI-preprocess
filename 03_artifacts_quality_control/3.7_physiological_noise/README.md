# 3.7_physiological_noise: 生理噪声

心脏/呼吸可混叠到 BOLD 频带，必须同步生理记录与扫描时刻。

## 使用条件与推荐

有外周记录时采用 PhysIO/RETROICOR 并检查 peak/trigger QC；无记录可用经解剖验证 CompCor，不能等同直接生理校正。

推荐是基于文献/官方文档的**条件建议**，不是在本仓库实验中选出的最优方法。

## 实现比较

| 实现 | 输入/前提 | 科学依据与限制 | 成本/兼容性 |
|---|---|---|---|
| PhysIO RETROICOR/RVT/HRV | 同步呼吸/心率和trigger、采集时间 | 多模型与同步QC | MATLAB/Neurodesk依赖，当前官方仓库位置需追踪 |
| AFNI 3dretroicor | 高频同步记录与slice时刻 | 成熟相位展开模型 | 缺记录不能从TR猜相位 |
| aCompCor | 可靠 WM/CSF mask | 无外周记录可用的代理 | 不应声称恢复真正心肺相位 |

## 标准步骤与参数

1. 使用根目录下载脚本取得 manifest 固定的真实样本，核对 SHA-256、mm affine 和秒单位 TR。
2. 阅读 `references.md` 的适用输入和版本记录；正式流水线参数须在下游结果前固定。
3. 运行 `few_shots/01_test.ipynb` 和 `02_retest.ipynb`。两例分别使用同一受试者的两次真实采集。
4. 查看 `results/<session>/metrics.json` 和 `comparison.png`，读 `evidence_status`、限制与原始索引；优化目标改变不是科学有效性证明。
5. 执行根目录 pytest。正式pipeline需另行输入完整confounds/组织mask/变换/生理记录，并验证报告。

## 输入、复用与验证

`src/reference.py` 导出公共 `phase_regressors` 为 `apply`。接口及校验见根 `fmri_reference/core.py`；数据加载、绘图与实验见 `fmri_reference/demo.py` 的 `physio` 分支。公共函数可直接复用；掩模、空间变换、频带、阈值、组件选择及扫描排除规则必须按数据和目标重新明确。

教学数据为原始任务BOLD，128个确定性EPI掩模内体素仅供时间信号演示；不是完整脑去噪流水线。所有参数如4mm、0.008Hz、50mm半径和最小段长5仅是明确示例，不能直接升级为全数据推荐。

## 错误实现与证据边界

主数据无生理记录；补充 AOMIC 可作为后续实测来源，当前真实生理校正 NOT_RUN。

Notebook 包含可运行的失败输入示例；缺输入会报错。不得静默替换数据、将缺失指标填0、把PCA脑信号称为aCompCor，或把采样间距统一称为解剖归一化。处理前后尺度单位可能不同，应读指标定义。

本小类完整成熟工具之间的同数据集端到端基准**未完成**。参见根 `reports/validation_summary.json` 和 `docs/remaining_validation.md`。
