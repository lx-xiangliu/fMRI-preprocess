# 来源核查与版本边界

检索日期2026-10-12，使用官方文档、PubMed论文记录、官方GitHub/GitLab代码、原始数据description及S3版本。并非PRISMA系统综述：没有声称穷尽全部实现。每类比较至少3种操作/实现策略，无法凭此确定科学最优。

## 论文与源码证据

PDF manifest保留403和TLS失败。CompCor官方主机镜像成功后保留原证书失败记录。PhysIO PDF第3-4页核查了模块流程、scan-timing同步与质量检查；AOMIC第10页明确历史fMRIPrep 1.4.1并列举部分元数据差异。因此历史预处理derivatives不能声称由当前25.x生成。PDF缓存不上传GitHub，manifest提供URL与校验。

`code_review_evidence.json`记录读过的关键源码范围；HEAD快照不等于本环境执行版本。MRIQC文档中DVARS涉及motion correction和强度缩放，本例raw DVARS无这些预处理，明确不直接比较绝对指标。

## 兼容性与许可证

原TAPAS代码仓库已归档/迁移，PhysIO当前官方入口单独记录。GitHub返回NOASSERTION表示未识别许可证，不代表无条件可重新分发；NiBabel和AFNI的真实许可证需看其许可文件。FSL不虚构GitHub镜像，其正式版本本机未安装；官方GitLab API当前限流429，commit保持未核实并保留失败。

HCP minimal pipelines与XCP-D均列为重要成熟参考。HCP的表面/CIFTI、畸变与结构输入依赖不同于普通单回波教学数据。XCP-D定位rest/pseudo-rest connectivity，官方不推荐将其通用去噪直接代替task GLM nuisance modeling；本主数据是任务BOLD，因此未直接套其rest默认参数。

## 数据补充

ds003114和ds003592官方description当前可读且CC0；ds003115当前S3/GitHub访问404，保留失败。补充来源未下载BOLD/physio样本、未执行相应方法，不能升级为已验证去噪。本主数据的NIfTI均通过annex大小/哈希与SHA256，数据版本不漂移。
