# 文献索引

按发表 venue 分类整理。优先关注顶会/顶刊论文，预印本作为补充。

---

## 一、顶会论文（已正式发表）

### ICML（International Conference on Machine Learning）

| 论文 | 年份 | 笔记 | 核心关键词 |
|------|------|------|-----------|
| MEMORYLLM: Towards Self-Updatable Large Language Models | ICML 2024 | [笔记](01_MEMORYLLM.md) | 模型内生记忆、latent memory pool、self-update |
| M+: Extending MemoryLLM with Scalable Long-Term Memory | ICML 2025 | [笔记](05_M_Plus.md) | 可扩展长期记忆、co-trained retriever、160k+ retention |

### ICLR（International Conference on Learning Representations）

| 论文 | 年份 | 笔记 | 核心关键词 |
|------|------|------|-----------|
| EM-LLM: Human-inspired Episodic Memory for Infinite Context LLMs | ICLR 2025 | [笔记](02_EM-LLM.md) | 情景记忆、事件分割、贝叶斯惊奇、无限上下文 |

### AAAI（Association for the Advancement of Artificial Intelligence）

| 论文 | 年份 | 笔记 | 核心关键词 |
|------|------|------|-----------|
| MemoryBank: Enhancing LLMs with Long-Term Memory | AAAI 2024 | [笔记](03_MemoryBank.md) | 艾宾浩斯遗忘曲线、记忆衰减、长期陪伴 |
| GSW: Beyond Fact Retrieval — Episodic Memory for RAG | AAAI 2026 | [笔记](04_GSW.md) | 生成式语义工作空间、时空锚定、叙事表示 |

### ACL（Association for Computational Linguistics）

| 论文 | 年份 | 笔记 | 核心关键词 |
|------|------|------|-----------|
| EpMAN: Episodic Memory AttentioN for Generalizing to Longer Contexts | ACL 2025 | [笔记](06_EpMAN.md) | 情景记忆注意力、KV cache 重加权、长上下文泛化 |

---

## 二、顶刊论文

### Trends in Cognitive Sciences（认知科学顶刊）

| 论文 | 年份 | 笔记 | 核心关键词 |
|------|------|------|-----------|
| Towards Large Language Models with Human-Like Episodic Memory | 2025 | [笔记](11_HumanEpisodicReview.md) | 认知科学综述、MA-LLM vs 人类记忆、对齐标准 |

---

## 三、高影响力预印本（尚未正式发表 / venue 待确认）

| 论文 | 时间 | 笔记 | 核心关键词 |
|------|------|------|-----------|
| SYNAPSE: Episodic-Semantic Memory via Spreading Activation | 2026.01 | [笔记](07_SYNAPSE.md) | 扩散激活、动态图、侧抑制、时间衰减 |
| FadeMem: Biologically-Inspired Forgetting | 2026.01 | [笔记](08_FadeMem.md) | 生物遗忘、自适应衰减、双层记忆、45%存储压缩 |
| MemGPT: Towards LLMs as Operating Systems | 2023.10 | [笔记](09_MemGPT.md) | OS 式分页、虚拟上下文、Letta 框架 |
| SCM: Self-Controlled Memory Framework | 2023.04 | [笔记](10_SCM.md) | 记忆流、记忆控制器、即插即用 |

---

## 四、综述论文（快速了解全貌）

| 论文 | Venue / 时间 | 链接 | 侧重点 |
|------|-------------|------|--------|
| Memory in the LLM Era | arXiv 2026.04 | [arxiv](https://arxiv.org/abs/2604.01707) | 隐式/显式/智能体记忆统一框架 |
| Anatomy of Agentic Memory | arXiv 2025.02 | [arxiv](https://arxiv.org/abs/2602.19320) | Agent 记忆分类学 + 评估局限 |
| Memory for Autonomous LLM Agents | arXiv 2025.03 | [arxiv](https://arxiv.org/abs/2603.07670) | 五大记忆机制 + 前沿方向 |
| Continual Learning in LLMs | arXiv 2025.03 | [arxiv](https://arxiv.org/abs/2603.12658) | 持续学习方法论综述 |

---

## 五、按研究主题索引

### 主题 A：模型内生记忆（参数级）
- MEMORYLLM (ICML 2024) — latent memory pool
- M+ (ICML 2025) — 扩展至 160k+

### 主题 B：认知科学启发的记忆架构
- EM-LLM (ICLR 2025) — 情景记忆 + 事件分割
- MemoryBank (AAAI 2024) — 艾宾浩斯遗忘
- FadeMem (arXiv 2026) — 生物遗忘机制
- SYNAPSE (arXiv 2026) — 扩散激活
- 认知科学综述 (Trends Cogn. Sci. 2025)

### 主题 C：情景记忆与结构化表示
- GSW (AAAI 2026) — 语义工作空间
- EpMAN (ACL 2025) — 情景记忆注意力

### 主题 D：记忆系统架构
- MemGPT (arXiv 2023) — OS 式分层
- SCM (arXiv 2023) — 自控记忆框架
