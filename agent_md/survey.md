# 任务：构建 fMRI 预处理标准参考代码仓库

## 1. 研究目标

针对 fMRI Foundation Model 的大规模预训练，系统调研现有 fMRI 预处理方法及其开源代码实现。

通过比较论文、官方工具、成熟开源项目和社区实践，筛选具有科学依据、经过验证、可复现且适合大规模数据处理的实现，最终构建一个供 Code Agent 长期参考和复用的标准代码仓库。

## 2. 研究范围

Category 1: Spatial Inconsistency（空间不一致）

1.1 Brain Shape（脑形态差异）

1.2 Brain Orientation（脑方向差异）

1.3 Voxel Spacing（体素间距差异）

1.4 Spatial Resolution（空间分辨率差异）

1.5 Spatial Coordinates（空间坐标系统差异）

Category 2: Temporal Inconsistency（时间不一致）

2.1 TR / Repetition Time（重复时间差异）

2.2 Sampling Rate（时间采样频率差异）

2.3 Time Points（时间点数量差异）

2.4 Scan Duration（扫描持续时间差异）

Category 3: Signal Artifacts & Quality Control（信号伪影与质量控制）

3.1 Head Motion / FD Abnormality（剧烈头动与 FD 异常）

3.2 Intensity Spikes / DVARS Abnormality（强度突变与 DVARS 异常）

3.3 Non-Steady-State Volumes & Short Valid Segments（非稳态与短有效片段）

3.4 Raw Signal Artifacts & Residual Artifacts（原始信号伪影与残余伪影）

3.5 Brain Coverage & Temporal SNR（脑覆盖率与 tSNR）

3.6 Registration Failure & Scan Exclusion（配准失败与扫描剔除）

3.7 Physiological Noise（生理噪声）

3.8 Scanner Drift（扫描仪信号漂移）

3.9 White Matter / CSF Confounds（白质与脑脊液干扰）

3.10 Other Non-Neural Components（其他非神经信号成分）

Category 4: Signal Scale Inconsistency（信号尺度不一致）

4.1 Mean（信号均值差异）

4.2 Variance（信号方差差异）

4.3 Signal Amplitude（信号振幅差异）

4.4 Dynamic Range（信号动态范围差异）



## 3. 文献与代码调研要求

针对每一个小类：

1. 尽可能全面地检索已有方法、代表论文以及 GitHub 官方代码仓库。
2. 优先考虑成熟工具及相关论文中的可复现实现，但不预设其一定最优。
3. 对比不同实现的科学正确性、适用前提、参数设置、鲁棒性、计算成本及兼容性。
4. 尽可能通过同一数据集上的实际实验验证不同实现，明确推荐方案的证据依据。
5. 对于存在争议或依赖具体数据条件的问题，保留多种正确方案，并说明选择条件。
6. 记录原始代码链接、Commit Hash、软件版本、许可证及对应论文。

禁止仅凭 GitHub Star 数量、项目知名度或模型主观判断确定最佳实现。

## 4. 统一参考数据集

选择一个**公开、可下载、包含 fMRI 和至少一种其他模态的多模态神经影像数据集**，优先选择 BIDS 组织的数据。

要求：
- 尽可能使用同一个数据集贯穿所有预处理示例。
- 优先选择同时包含结构 MRI、fMRI 及其他辅助模态或刺激信息的数据集。
- 提供官方下载地址、数据结构、访问条件及许可证。
- 使用少量真实样本完成 Few-shot 演示。
- 对不适用该数据集的操作，明确说明并寻找补充公开数据。

## 5. 代码仓库结构

严格采用 **大类 / 小类** 的两级分类结构。

每个小类至少包含：

- `README.md`：问题定义、科学原理、适用条件、推荐方法及注意事项。
- `references.md`：论文、官方文档、开源仓库及版本信息。
- `few_shots/`：多个可独立运行的 Jupyter Notebook（`.ipynb`）。
- `src/`：从 Notebook 提取的可复用 Python 实现。
- `tests/`：关键正确性测试与质量控制。
- `results/`：数值验证与可视化结果。

每个 Notebook 必须包含：真实数据输入、处理前状态、关键代码、处理后结果、可视化、定量质量指标，以及常见错误示例。

代码尽可能模块化、参数化，避免硬编码路径。

把这个仓库保存在这个父文件夹下面，传到 github 上面

## 6. Code Agent 复用要求

该仓库未来将作为 Code Agent 实现 fMRI 数据处理流水线时的核心参考资料。

因此每个小类需要明确：

1. 什么时候应该使用该方法。
2. 输入数据必须满足什么条件。
3. 标准处理步骤与参数选择依据。
4. 如何验证输出正确。
5. 哪些错误实现必须避免。
6. 哪些组件可以直接复用，哪些必须根据数据调整。

优先提供能够通过自动化测试的 Python 函数，Notebook 主要承担教学、演示和验证职责。

## 7. 最终交付

最终需要交付：

1. 完整的大类/小类仓库结构。
2. 每个小类的开源方法与代码对比报告。
3. 有明确证据支持的推荐实现及适用范围。
4. 基于真实多模态数据集的 Few-shot Notebook。
5. 可复用的 Python 模块、测试和环境配置。
6. 面向 Code Agent 的统一使用说明 `AGENTS.md`。

**质量约束：** 不得编造论文、仓库、测试结果或性能指标；区分已实际运行验证与仅通过代码审阅的方法。不能确定的技术结论必须标注证据不足。

优先保证科学正确性、代码可复现性与长期可维护性，再考虑执行效率。