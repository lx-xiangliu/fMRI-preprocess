# fMRI Preprocessing Reference

一个面向 Code Agent 的 fMRI 预处理标准参考仓库，按“大类/小类”组织。每个小类包含科学说明、来源、可复用 Python 函数、测试、两个真实 BIDS 输入的 Few-shot Notebook 和结果目录。

## 统一数据集

Few-shot 默认使用 OpenNeuro `ds000114`（Faces，BIDS；包含功能 MRI、结构 MRI 和行为/刺激相关信息，具体模态与许可应以下载目录中的 `dataset_description.json` 和 README 为准）。官方下载入口：<https://openneuro.org/ds000114>；S3 入口：`s3://openneuro.org/ds000114`。下载后设置 `FMRI_BIDS_ROOT=/path/to/ds000114`。

## 安装与运行

```bash
conda activate base
python -m pip install -e .
pytest
```

Notebook 需要 `nibabel`, `numpy`, `matplotlib`, `jupyter`；在真实数据下载后逐个运行。所有结果必须保存到对应小类的 `results/`，不把未运行的结果写成性能结论。

## 证据边界

仓库区分“代码审阅/确定性单元测试”和“真实数据实验”。当前 `VALIDATION.md` 记录了 base 环境下 23 个测试和 46 个 Notebook 的实际运行；样本范围与限制也在那里说明。
