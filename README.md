# AI Memory — 类人记忆机制研究与实现

## 项目定位

探索如何为大语言模型（LLM）构建**类人长期记忆系统**。

核心问题：Transformer 架构将"学习"和"推理"硬性分离——训练时学，推理时用，推理时不学。
这导致 LLM 天生没有"边用边记"的能力。本项目系统性地研究现有解决方案，并探索更接近人类认知架构的记忆机制。

## 研究方向

### 方向一：认知启发的外部记忆系统
基于认知科学（情景记忆、语义记忆、遗忘曲线、扩散激活）设计外部记忆架构，
使记忆的**写入、保留、遗忘、回忆**行为尽可能接近人类。

### 方向二：模型内生记忆能力
探索让模型参数本身具备持续学习、在线写入能力的前沿方法，
包括 self-updatable memory、latent memory pool、test-time training 等。

### 方向三：自适应记忆编排（Memory Controller）
训练专门的记忆调度模型，实现 query-conditioned adaptive memory assembly：
- 动态召回数量（非固定 top-k）
- 动态切片边界（非固定 chunk）
- 动态上下文完整度
- 记忆融合与压缩

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
