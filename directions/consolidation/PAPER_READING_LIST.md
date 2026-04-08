# 记忆巩固方向：补读论文清单

## 阅读目标

这份清单不是“看得越多越好”，而是：

**先把最容易和你做重的工作看透，再补理论和 benchmark。**

---

## 一、评分规则

为了避免“相关论文太多，看不过来”，这里给每篇一个简化权重分数。

总分 `100`，由 3 部分组成：

- `Directness 50%`
  这篇和 consolidation 有多直接
- `Venue 30%`
  顶刊顶会、正式 benchmark、还是预印本
- `Evidence 20%`
  是否有明确实验、代码、统一 benchmark 或可复现设置

你应该优先读：

1. `分数高`
2. `和你直接重叠`
3. `正式 venue`

---

## 二、第一梯队：必须先读，防止选题撞车

| 优先级 | 论文 | 分数 | Venue / 时间 | 为什么必须先读 | 读完要带走什么 |
|--------|------|------|--------------|----------------|---------------|
| S1 | **TiMem** | **91** | arXiv 2026.01 | 这是目前最像“巩固系统论文”的工作之一。直接做 temporal-hierarchical consolidation | 它的层级组织、抽象路径、检索配套机制，哪些已经把你的想法占了 |
| S2 | **LightMem** | **89** | ICLR 2026 Poster / arXiv 2025.10 | 明确提出 `sleep-time long-term consolidation`，而且效率结果很强 | 它怎样把在线和离线解耦；你不能再只讲“睡眠更新” |
| S3 | **SimpleMem** | **84** | arXiv 2026.01 | 最新版主打 `Online Semantic Synthesis`，已覆盖“写入时在线综合压缩” | 你不能再把“写入时把碎片合成高密度记忆”当新点 |
| S4 | **PREMem** | **83** | Findings EMNLP 2025 | 把复杂推理前移到 memory construction，是写入侧的强竞争者 | 存前 reasoning 和存后 consolidation 的边界该怎么划 |
| S5 | **Recursively Summarizing Enables Long-Term Dialogue Memory...** | **80** | Neurocomputing 2025 / arXiv 2023 | 最早的“递归摘要形成长期记忆”路线，不能忽略 | 它可以作为最朴素 baseline，也能帮你避免重复发明 |

---

## 三、第二梯队：高权重正式论文，虽然不完全叫 consolidation，但和你的方法强相关

| 优先级 | 论文 | 分数 | Venue / 时间 | 为什么要读 | 读完要带走什么 |
|--------|------|------|--------------|------------|---------------|
| A1 | **M+** | **84** | ICML 2025 | 短期到长期迁移的最强正式论文之一 | “转存”和“巩固”差在哪；你怎么把它写进 related work |
| A2 | **EM-LLM** | **83** | ICLR 2025 | 高质量事件边界是高质量巩固的上游 | 事件级巩固比固定 chunk 巩固更合理 |
| A3 | **GSW** | **82** | AAAI 2026 | Reconciler 本质上已经在做结构化整合 | 你能否把 GSW 视作“局部 consolidation”而不是 retrieval-only 方法 |
| A4 | **FadeMem** | **82** | arXiv 2026.01 | 融合、冲突消解、层迁移，最接近巩固 baseline | 你的方法若不超过它，论文很难成立 |
| A5 | **Memory OS of AI Agent** | **80** | EMNLP 2025 | 已经做了三层 memory 和动态更新 | 你不能只做 storage hierarchy；要有更强的 consolidation 定义 |
| A6 | **MemInsight** | **77** | EMNLP 2025 | 自动 memory augmentation，偏 retrieval enhancement | 看它如何处理结构化增强，不要把 augmentation 当成 consolidation |
| A7 | **Mem0** | **76** | arXiv 2025.04 | 工业界已经把 extraction / consolidation / retrieval 做成产品功能 | 工业定义的“consolidation”到底有多浅，和学术问题怎么区分 |
| A8 | **MemMachine** | **74** | arXiv 2026.04 | 它代表反方向：尽量保真、少做 lossy extraction | 可以作为你的负对照，提醒你别把 abstraction 做过头 |

---

## 四、第三梯队：理论与综述，决定你故事能不能讲稳

| 优先级 | 论文 / 资料 | 分数 | 类型 | 为什么要读 |
|--------|------------|------|------|-----------|
| T1 | **Towards LLMs with Human-Like Episodic Memory** | **90** | Trends in Cognitive Sciences 2025 | 这是你把 consolidation 讲成“认知对齐问题”的理论地基 |
| T2 | **Memory for Autonomous LLM Agents** | **88** | Survey, arXiv 2026.03 | 它已经把 `continual consolidation` 明确列为 open problem |
| T3 | **Memory in the Age of AI Agents** | **84** | Survey, arXiv 2025.12 | 帮你把 forms / functions / dynamics 讲清楚 |
| T4 | **Memory in the LLM Era** | **82** | Survey, arXiv 2026.04 | 提供统一框架和方法比较视角 |
| T5 | **Complementary Learning Systems (CLS)** | **86** | 认知理论 | 如果你要讲短期 episodic 到长期 semantic 的转化，这是核心理论支柱 |
| T6 | **Systems Consolidation** | **84** | 认知理论 | 支撑“记忆如何从具体经历变得更抽象、更稳定” |
| T7 | **Sleep and Memory Consolidation** | **83** | 认知理论 | 支撑离线 / sleep-time / replay 式整理 |
| T8 | **Schema Theory of Memory** | **81** | 认知理论 | 支撑“新记忆如何整合进已有知识框架” |

---

## 五、第四梯队：评测必读，不然你很容易做完不知道怎么证

| 优先级 | Benchmark / 论文 | 分数 | Venue / 时间 | 为什么要读 |
|--------|------------------|------|--------------|-----------|
| B1 | **LongMemEval** | **88** | ICLR 2025 | 五类长期记忆能力很实用，尤其是 update / abstention |
| B2 | **LoCoMo** | **86** | ACL 2024 | 目前最常用的长对话 memory benchmark |
| B3 | **LoCoMo-Plus** | **82** | arXiv 2026.02 | 开始测 latent constraints，适合更高层巩固能力 |
| B4 | **BEAM** | **79** | arXiv 2025.10 | 极长尺度测试，适合验证巩固和压缩能否撑住百万级上下文 |

---

## 六、你已经读过、但现在要用“巩固视角”重读的论文

| 已有笔记 | 这次重读只看什么 |
|---------|----------------|
| `05_M_Plus.md` | 短期到长期迁移是不是只是搬运，不是整理 |
| `02_EM-LLM.md` | 事件边界怎样作为 consolidation 的输入单元 |
| `04_GSW.md` | Reconciler 到底能不能视作局部结构化巩固 |
| `08_FadeMem.md` | 融合、冲突消解、双层迁移能否组成 baseline |
| `11_HumanEpisodicReview.md` | 巩固在整个人类记忆框架里的理论位置 |

---

## 七、最省时间的阅读顺序

### 第 1 周：先去重

1. TiMem
2. LightMem
3. SimpleMem
4. PREMem

目标：

搞清楚你当前直觉里的“异步整理系统”已经被做了多少。

### 第 2 周：补正式高权重论文

1. M+
2. EM-LLM
3. GSW
4. FadeMem
5. Memory OS

目标：

搞清楚现有顶会顶刊方法分别覆盖了巩固链条里的哪一段。

### 第 3 周：补理论

1. Human-like Episodic Memory 综述
2. Memory for Autonomous LLM Agents
3. CLS
4. Systems Consolidation
5. Sleep Consolidation

目标：

让你的故事从“系统工程想法”升级成“有认知理论支撑的问题”。

### 第 4 周：补 benchmark

1. LongMemEval
2. LoCoMo
3. LoCoMo-Plus
4. BEAM

目标：

明确现有 benchmark 测不到什么，从而知道要不要自己建 ConsolidBench。

---

## 八、最后一句话

对你现在最重要的不是“多看几篇 memory 论文”，而是：

**先把最像 consolidation 的那几篇看透，确认自己不会做成 TiMem / LightMem / PREMem / SimpleMem 的变体。**

---

## 链接

- TiMem: https://arxiv.org/abs/2601.02845
- LightMem: https://arxiv.org/abs/2510.18866
- SimpleMem: https://arxiv.org/abs/2601.02553
- PREMem: https://arxiv.org/abs/2509.10852
- Recursive Summarization: https://arxiv.org/abs/2308.15022
- M+: https://proceedings.mlr.press/v267/wang25au.html
- EM-LLM: https://proceedings.iclr.cc/paper_files/paper/2025/hash/c05144b635df16ac9bbf8246bbbd55ca-Abstract-Conference.html
- GSW: https://arxiv.org/abs/2511.07587
- FadeMem: https://arxiv.org/abs/2601.18642
- Memory OS: https://aclanthology.org/2025.emnlp-main.1318/
- MemInsight: https://aclanthology.org/2025.emnlp-main.1683/
- Mem0: https://arxiv.org/abs/2504.19413
- MemMachine: https://arxiv.org/abs/2604.04853
- LongMemEval: https://arxiv.org/abs/2410.10813
- LoCoMo: https://aclanthology.org/2024.acl-long.747/
- LoCoMo-Plus: https://arxiv.org/abs/2602.10715
- BEAM: https://arxiv.org/abs/2510.27246
