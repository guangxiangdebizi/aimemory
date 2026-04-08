# AI Memory — 类人记忆机制研究与实现

## 项目定位

探索如何为大语言模型（LLM）构建**类人长期记忆系统**。

核心问题：Transformer 架构将"学习"和"推理"硬性分离——训练时学，推理时用，推理时不学。
这导致 LLM 天生没有"边用边记"的能力。本项目系统性地研究现有解决方案，并探索更接近人类认知架构的记忆机制。

## 研究方向

### 方向 A：RL 驱动的记忆策略
研究如何让 agent 学会"什么时候记、什么时候删、什么时候更新、什么时候总结"，
把记忆管理从手工规则升级成可学习策略。

### 方向 B：记忆巩固
研究短期记忆如何在系统空闲时被整理、聚类、去重、冲突消解，并转化为更稳定的长期记忆。

### 方向 C：因果驱动检索
研究如何从"检索语义上相似的记忆"升级为"检索对当前决策真正有因果意义的记忆"。

### 方向 D：动态事件分割 + 结构化表示
研究如何先把连续经历切成合理事件，再把每个事件存成结构化对象，提升记忆质量和检索质量。

### 方向 E：多模态 / 具身记忆
研究 agent 如何记住自己看过什么、做过什么、走过哪里，以及这些经历如何支持后续行动。

## 项目结构

```
aimemory/
├── README.md                    # 项目总览（本文件）
├── papers/
│   ├── INDEX.md                 # 文献总索引（按顶会/顶刊/预印本分类）
│   ├── 01_MEMORYLLM.md          # MEMORYLLM — ICML 2024
│   ├── 02_EM-LLM.md             # EM-LLM — ICLR 2025
│   ├── 03_MemoryBank.md         # MemoryBank — AAAI 2024
│   ├── 04_GSW.md                # Generative Semantic Workspace — AAAI 2026
│   ├── 05_M_Plus.md             # M+ — ICML 2025
│   ├── 06_EpMAN.md              # EpMAN — ACL 2025
│   ├── 07_SYNAPSE.md            # SYNAPSE — arXiv 2026
│   ├── 08_FadeMem.md            # FadeMem — arXiv 2026
│   ├── 09_MemGPT.md             # MemGPT — arXiv 2023 / Letta
│   ├── 10_SCM.md                # SCM — arXiv 2023
│   └── 11_HumanEpisodicReview.md # 认知科学综述 — Trends in Cognitive Sciences 2025
├── architecture/
│   ├── COGNITIVE_MEMORY_ARCH.md # 类人记忆架构设计
│   └── COMPARISON.md            # 方案对比矩阵
├── directions/
│   ├── INDEX.md                 # 研究方向导读
│   ├── 01_RL_MEMORY_POLICY.md   # 方向 A：RL 驱动的记忆策略
│   ├── 02_MEMORY_CONSOLIDATION.md # 方向 B：记忆巩固
│   ├── 03_CAUSAL_RETRIEVAL.md   # 方向 C：因果驱动检索
│   ├── 04_EVENT_SEGMENTATION_PLUS_STRUCTURE.md # 方向 D：动态事件分割 + 结构化表示
│   ├── 05_MULTIMODAL_EMBODIED_MEMORY.md # 方向 E：多模态 / 具身记忆
│   └── consolidation/           # 方向 B 深入研究材料
│       ├── GAP_ANALYSIS.md      # 差距分析：当前缺什么
│       ├── RESEARCH_PLAN.md     # 研究计划：具体怎么做
│       ├── BASELINE_AND_BENCHMARKS.md # Baseline 与评测方案
│       ├── PAPER_READING_LIST.md # 补读论文清单
│       ├── DIRECT_COMPETITOR_COMPARISON.md # 直接竞争工作逐篇拆解
│       └── NON_OVERLAP_TOPIC_DRAFTS.md # 不撞车选题草案
└── references/
    └── RESOURCES.md             # 开源代码、数据集、工具汇总
```

## 核心论文速览

| # | 论文 | Venue | 年份 | 核心贡献 | 与本项目相关度 |
|---|------|-------|------|----------|---------------|
| 1 | MEMORYLLM | **ICML** 2024 | 2024 | 模型内嵌可自更新记忆池 | ⭐⭐⭐⭐⭐ |
| 2 | EM-LLM | **ICLR** 2025 | 2025 | 人类情景记忆启发的无限上下文 | ⭐⭐⭐⭐⭐ |
| 3 | MemoryBank | **AAAI** 2024 | 2024 | 艾宾浩斯遗忘曲线 + 记忆衰减 | ⭐⭐⭐⭐⭐ |
| 4 | GSW | **AAAI** 2026 | 2026 | 生成式语义工作空间 + 情景记忆 | ⭐⭐⭐⭐ |
| 5 | M+ | **ICML** 2025 | 2025 | MemoryLLM 扩展至 160k+ token | ⭐⭐⭐⭐⭐ |
| 6 | EpMAN | **ACL** 2025 | 2025 | 情景记忆注意力机制 | ⭐⭐⭐⭐ |
| 7 | SYNAPSE | arXiv | 2026 | 扩散激活 + 动态图记忆 | ⭐⭐⭐⭐ |
| 8 | FadeMem | arXiv | 2026 | 生物启发遗忘机制 | ⭐⭐⭐⭐ |
| 9 | MemGPT | arXiv / Letta | 2023 | OS 式虚拟上下文管理 | ⭐⭐⭐ |
| 10 | SCM | arXiv | 2023 | 自控记忆框架 | ⭐⭐⭐ |
| 11 | 认知科学综述 | **Trends Cogn. Sci.** | 2025 | 人类情景记忆 vs MA-LLM 差距分析 | ⭐⭐⭐⭐⭐ |

> ⭐⭐⭐⭐⭐ = 直接相关，必读；⭐⭐⭐⭐ = 高度相关；⭐⭐⭐ = 参考价值

## 阅读建议

**第一轮（建立认知框架）：**
1. 认知科学综述 → 理解人类记忆机制的核心特性
2. EM-LLM → 看认知科学如何落地到 LLM 架构
3. MEMORYLLM + M+ → 理解"模型内生记忆"的前沿进展

**第二轮（深入具体机制）：**
4. MemoryBank → 遗忘曲线的工程实现
5. FadeMem → 更精细的生物启发遗忘
6. SYNAPSE → 动态图 + 扩散激活检索
7. GSW → 情景记忆的结构化表示

**第三轮（系统设计参考）：**
8. MemGPT → 经典记忆分层架构
9. EpMAN → 注意力机制层面的记忆集成
10. SCM → 即插即用的记忆控制器设计
