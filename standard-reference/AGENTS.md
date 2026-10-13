# Code Agent 使用约定

先读 README、DATASET、reports/validation_summary.json 和小类证据限制。根目录23类分类是检索入口，公共实现位于 fmri_reference，Notebook用于教学和可复现验证。

- 不把本仓库数学/教学例视为成熟完整fMRI流水线。先判断原始BIDS或已处理derivatives，避免重复运动/畸变/滤波处理。
- 数据有版本、S3 VersionId、字节数、SHA256/annex校验；缺数据必须停止，不用合成输入伪装真实数据。
- RAS/LPS、mm/秒单位、qform/sform冲突与模板名称须审计；同网格不证明同空间，canonical不证明配准。
- 维度约定time x features；run、subject和split不混合；所有censor保留原index和物理时刻，padding必须附mask。
- raw DVARS与standardized DVARS分开，首卷FD/DVARS未定义；无真实运动参数则FD NOT_MEASURED。
- 未验证的组织mask不可称为WM/CSF；没有同步外周记录不可声称RETROICOR；单回波不可运行tedana。
- confounds+drift使用同一个设计矩阵，记录rank与代数dof。不要无限堆叠所有confound列、重复high-pass或把censor后的压缩时轴当均匀连续序列。
- tSNR/PSC应保留原始baseline；去均值后的tSNR没有原始解释。尺度是否保留神经振幅由任务决定。
- 阈值、频带、模板、处理顺序、mask和剔除规则在结果前固定。split按subject隔离；normalization拟合不能查看测试数据。
- 实测数学性质、真实数据演示、正式pipeline、科学最优结论四层必须独立报告。NOT_RUN/NOT_MEASURED/REVIEW_REQUIRED不能填零或改写为PASS。
- 源码与环境锁定分别看provenance/software.json、installed_versions.json、requirements-lock.txt、environment-freeze.txt。上游HEAD metadata不是执行版本。
- 运行python -m pytest -q以及python scripts/run_notebooks.py；新改动需按其科学风险验证。不要改动父仓库已暂存删除文件。
