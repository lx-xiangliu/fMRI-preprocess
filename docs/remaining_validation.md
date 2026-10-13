# 仍需验证的科学范围

仓库结构、真实few-shot、基础可复用算法与数学测试可交付；完整成熟pipeline对比仍未完成，不能称为全部任务科学验证完成。

1. 在固定容器digest、FreeSurfer许可（如使用）、TemplateFlow校验和及完整BIDS验证下，运行fMRIPrep与AFNI/FSL对照，记录CPU小时、峰值内存与所有失败报告。当前未安装这些工具，不编造性能表。
2. 原始BOLD→真实运动参数→FD与standardized DVARS、非稳态标签、组织mask和aCompCor；目前缺这些产物，motion/非稳态/脑覆盖/组织去噪保持NOT_MEASURED或NOT_RUN。
3. nonlinear形态归一化、SDC和配准排除：当前SimpleITK教学刚体例不证明最佳配准。需要模板和脑提取、独立边界/覆盖检查、形变QC与人工裁决。
4. 生理噪声：从公开补充AOMIC获取记录并验证trigger与StartTime，再运行PhysIO/AFNI并对比。当前没有真实RETROICOR执行。
5. 非神经ICA：single-echo需真实AROMA特征/分类，多echo需完整echo/TE。PCA分解不能直接作为噪声回归。
6. Foundation-model输入：按subject/site分割，冻结阈值与每种合法预处理分支，比较跨受试者质量、神经/任务响应保真、可重复性和下游效用。仅两个run不能得到统计性最优推荐。

这些是具体数据/工具/实验依赖，不应让代理自动以synthetic、更多滤波或不合法数据替代。教学误差注入独立标记，绝非真实坏卷证据。
