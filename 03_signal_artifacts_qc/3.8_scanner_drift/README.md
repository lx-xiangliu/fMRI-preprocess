# Scanner Drift

## 问题定义

Estimate low-frequency scanner drift from global signal. 本小类面向大规模 BIDS fMRI 处理；所有自动修改都必须保留原始 affine、TR、输入文件和参数。

## 推荐做法

1. 先读取 BIDS/NIfTI header 与 JSON，不根据文件名猜测单位。
2. 在处理前保存形状、affine、NaN 数量和时间维度。
3. 使用 `src/` 中的函数执行单一、可审计的变换；需要重采样或回归时显式提供目标网格/模型。
4. 用 Few-shot Notebook 的定量指标检查输出，并将结果写入 `results/`。

## 适用条件与错误实现

输入必须是有效 NIfTI 或 NumPy 数组，时间轴约定为最后一维（除非函数签名另有说明）。禁止静默覆盖源数据、把 TR 当毫秒、在不同 affine 间直接拼接、或仅凭单一 QC 指标剔除扫描。短扫描、缺失 JSON、缺少生理记录时应报告“不适用”，而不是填入猜测值。

## 实现与证据

`src/scanner_drift.py` 是可复用的最小实现；`tests/` 覆盖确定性边界案例。Notebook 需要先下载真实 ds000114 数据后运行。本机验证状态记录在根目录 `VALIDATION.md`。
