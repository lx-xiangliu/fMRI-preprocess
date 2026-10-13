# 统一真实数据

官方：[OpenNeuro ds000114 v1.0.2](https://openneuro.org/datasets/ds000114/versions/1.0.2)。dataset_description中的License=CC0，BIDSVersion=1.0.0rc2，公开匿名下载，无需注册。旧BIDS版本不代表通过当前validator；完整BIDS校验未运行。

主样本 sub-01，ses-test与ses-retest的fingerfootlips任务BOLD，共享继承的task JSON/events；ses-test T1w、DWI、bval/bvec。BOLD TR=2.5秒，SliceTiming存在；T1w、DWI是真实不同模态，当前DWI用于模态/输入验证而不进行DWI预处理。

官方数据Git tree、Git-annex哈希、冻结S3对象VersionId、URL、字节数、下载后SHA256与shape/zooms见 `provenance/data_manifest.json`。无脑组织分割、正式motion confounds、生理记录或多回波，不能假装这些输入存在。

本地原始数据约160MB，Git不提交NIfTI。`python scripts/download_data.py` 从固定对象下载并校验；data-manifest已验证后才能跑Notebook。若S3历史version不可用，停止并记录，不自动换最新版。

论文：[Gorgolewski et al. test-retest dataset](https://www.research.ed.ac.uk/files/8517189/A_test_retest_fMRI_dataset_for_motor_language_and_spatial_attention_functions.pdf)。下载/页证据见paper_manifest。

补充来源：AOMIC-PIOP1 ds003114可提供同步心肺记录；PIOP2 ds003115当前官方下载访问404；数据说明：[Snoek et al. 2021 DOI 10.1038/s41597-021-00870-6](https://www.nature.com/articles/s41597-021-00870-6)。主数据不适用tedana；可用公开多回波ds003592，需重新验证echo/TE、版本与许可证。补充来源当前未代替主数据，访问核查结果见supplemental_sources.json。
