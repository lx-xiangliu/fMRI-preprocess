# fMRI 预处理标准参考库

供fMRI Foundation Model数据处理代理检索：4大类 / 23小类，每类有方法比较、版本引用、两份独立真实Notebook、src、tests及实际results。优先科学前提、来源与可复现性，保留多种合法方案，不按stars选最佳。

**当前范围：真实数据教学与基础算法验证。成熟完整流水线的同数据集端到端对比未完成；不宣称最佳实现。** 实测汇总见 [验证报告](reports/validation_summary.json)，缺失范围见 [后续科学验证](docs/remaining_validation.md)。

## 运行

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements-lock.txt
pip install -e . --no-deps
python scripts/download_data.py
python -m pytest -q
python scripts/run_notebooks.py
```

交付运行使用Python 3.12及明确版本。`requirements-lock.txt`锁定直接依赖，`environment-freeze.txt`为实际运行环境完整快照；它来自继承的本机环境，干净环境重建结果见reports/clean_environment_pytest.txt；完整传递依赖锁见requirements-clean-lock.txt。本机完整包清单仅为运行证据，不是跨平台hermetic lock。

Notebook从库根目录或其子目录运行；也可设FMRI_REFERENCE_ROOT。执行器自动创建本地fmri-reference kernel，固定为当前Python。原始NIfTI和环境不入Git；执行Notebook及小型PNG/JSON结果入Git。

## 分类入口

- [1.1_brain_shape 脑形态差异](01_spatial_inconsistency/1.1_brain_shape/README.md)
- [1.2_brain_orientation 脑方向差异](01_spatial_inconsistency/1.2_brain_orientation/README.md)
- [1.3_voxel_spacing 体素间距差异](01_spatial_inconsistency/1.3_voxel_spacing/README.md)
- [1.4_spatial_resolution 空间分辨率差异](01_spatial_inconsistency/1.4_spatial_resolution/README.md)
- [1.5_spatial_coordinates 空间坐标差异](01_spatial_inconsistency/1.5_spatial_coordinates/README.md)
- [2.1_repetition_time TR 差异](02_temporal_inconsistency/2.1_repetition_time/README.md)
- [2.2_sampling_rate 采样率差异](02_temporal_inconsistency/2.2_sampling_rate/README.md)
- [2.3_time_points 时间点数量差异](02_temporal_inconsistency/2.3_time_points/README.md)
- [2.4_scan_duration 扫描时长差异](02_temporal_inconsistency/2.4_scan_duration/README.md)
- [3.1_head_motion_fd 头动与 FD 异常](03_artifacts_quality_control/3.1_head_motion_fd/README.md)
- [3.2_intensity_spikes_dvars 强度突变与 DVARS](03_artifacts_quality_control/3.2_intensity_spikes_dvars/README.md)
- [3.3_nonsteady_short_segments 非稳态与短有效片段](03_artifacts_quality_control/3.3_nonsteady_short_segments/README.md)
- [3.4_raw_residual_artifacts 原始与残余伪影](03_artifacts_quality_control/3.4_raw_residual_artifacts/README.md)
- [3.5_brain_coverage_tsnr 脑覆盖率与 tSNR](03_artifacts_quality_control/3.5_brain_coverage_tsnr/README.md)
- [3.6_registration_exclusion 配准失败与剔除](03_artifacts_quality_control/3.6_registration_exclusion/README.md)
- [3.7_physiological_noise 生理噪声](03_artifacts_quality_control/3.7_physiological_noise/README.md)
- [3.8_scanner_drift 扫描仪漂移](03_artifacts_quality_control/3.8_scanner_drift/README.md)
- [3.9_wm_csf_confounds 白质/脑脊液混杂](03_artifacts_quality_control/3.9_wm_csf_confounds/README.md)
- [3.10_other_non_neural 其他非神经成分](03_artifacts_quality_control/3.10_other_non_neural/README.md)
- [4.1_mean 均值差异](04_signal_scale_inconsistency/4.1_mean/README.md)
- [4.2_variance 方差差异](04_signal_scale_inconsistency/4.2_variance/README.md)
- [4.3_signal_amplitude 信号振幅差异](04_signal_scale_inconsistency/4.3_signal_amplitude/README.md)
- [4.4_dynamic_range 动态范围差异](04_signal_scale_inconsistency/4.4_dynamic_range/README.md)

## 证据与复用

- [数据与访问条件](DATASET.md)，data_manifest含冻结S3版本和校验。
- [Code Agent约定](AGENTS.md)：先判断输入前提，再选函数和验证；缺失不等于0。
- provenance/software.json：官方源码commit、release元数据、许可证；installed_versions是实际运行版本。
- provenance/source_review_manifest.json与paper_manifest.json：代码/PDF审阅范围，保留下载失败。
- reports/validation_summary.json：每Notebook执行状态、实际数值、未运行成熟工具与不足证据。

本仓库原创代码采用MIT；数据CC0，上游软件/论文保留各自许可。查看引用的FSL/PhysIO/SPM等许可与运行条件，不能把本库MIT传递给上游。

完整EPI掩模的流式QC及独立数值对照：`python scripts/full_qc.py`，结果见reports/full_mask_qc.json；未测峰值内存，演示运行时间不能代表成熟工具性能。未运行的fMRIPrep命令可由fmri_reference/pipelines.py构建，需要真实container digest与外部环境。
