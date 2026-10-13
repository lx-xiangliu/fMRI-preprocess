# 实际验证结果
+
+数据：ds000114 sub-01 两次真实fingerfootlips BOLD（184卷/run，TR 2.5s），以及T1w/DWI。下载大小、annex校验和、S3 VersionId及SHA256均保留。
+
+- 46/46 Notebook执行成功；3类入口修正后重新执行受影响6份Notebook，结果合并保留。
+- 59项关键不变性/前提测试在原环境与独立干净环境通过。警告日志保留，未隐藏。CI状态需单独看GitHub，不能将本地PASS称为CI PASS。
+- z-score对照Nilearn最大误差8.89e-15，PSC最大误差2.85e-14（保守向上取整）。仅数学一致性，不代表科学最优。
+- 全EPI估计掩模：test 17210体素、retest 17258体素；stream DVARS与向量化误差0，tSNR误差<5.5e-12。流式时间约0.13-0.17s，仅本机未压缩输入小样本，不是跨工具性能结论。
+- 刚体MI配准已运行，图像已人工查看；低分辨率叠加仅教学，扫描仍REVIEW_REQUIRED。没有BBR/脑提取/SDC，不能自动接收扫描。
+
+明确未完成：正式FD、standardized DVARS、真实非稳态标签、独立解剖脑覆盖率、非线性标准化、SDC、真实RETROICOR、组织aCompCor、ICA-AROMA/tedana、下游Foundation Model效用与成熟工具端到端公平对照。缺失不赋值0。
+
+所有小类比较是基于官方代码/文档和代表论文的条件选择；不是同数据实验排名。源码读过的范围、PDF页审阅/失败和许可证metadata均在provenance。
+