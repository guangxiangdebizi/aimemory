# EM-LLM: Human-inspired Episodic Memory for Infinite Context LLMs

> 核对状态：已按论文 PDF 复核（2026-04-07）。

## 基本信息

| 项目 | 内容 |
|------|------|
| **Venue** | ICLR 2025 |
| **作者** | Zafeirios Fountas, Martin A. Benfeghoul, Adnan Oomerjee, Fenia Christopoulou, Gerasimos Lampouras, Haitham Bou-Ammar, Jun Wang |
| **机构** | Huawei Noah's Ark Lab, London; University College London |
| **论文页面** | https://proceedings.iclr.cc/paper_files/paper/2025/hash/c05144b635df16ac9bbf8246bbbd55ca-Abstract-Conference.html |
| **PDF** | https://proceedings.iclr.cc/paper_files/paper/2025/file/c05144b635df16ac9bbf8246bbbd55ca-Paper-Conference.pdf |
| **本地 PDF** | [02_EM-LLM.pdf](../_tmp_pdfs/02_EM-LLM.pdf) |
| **本地抽取文本** | [02_EM-LLM.txt](../_tmp_txt/02_EM-LLM.txt) |
| **代码** | https://github.com/em-llm/EM-LLM-model |

## 为什么这篇重要

**这是把“人类情景记忆 + 事件认知”真正落到长上下文 LLM 推理机制上的代表作。**

它的价值不只是“能做更长上下文”，而是把以下几个认知科学概念工程化了：

- 连续经验会被切成离散事件
- 事件边界通常出现在高 surprise 的位置
- 回忆不只是语义相似，还会带出时间相邻事件

而且这套方法**不需要微调**，直接在推理阶段工作。

## 核心架构（按原文）

EM-LLM 的三块核心机制分别是：

1. **surprise-based event segmentation**
2. **graph-theoretic boundary refinement**
3. **two-stage episodic retrieval**

### 1. 事件分割：不是泛泛的“不确定性变化”，而是显式 Bayesian surprise

论文把 token 级 surprise 定义为：

```text
-log P(x_t | x_1, ..., x_(t-1); θ)
```

也就是：当前真实 token 在已有上下文下的负对数似然。
token 越“出乎模型意料”，surprise 越高。

边界判定阈值不是固定常数，而是一个**滑动窗口自适应阈值**：

```text
T = μ_(t-τ:t) + γσ_(t-τ:t)
```

也就是说：

- 用过去一段窗口里的 surprise 均值和标准差估阈值
- `γ` 控制切分敏感度
- 某个 token 的 surprise 超过阈值，就把它当作潜在事件边界

这点很关键，因为它说明 EM-LLM 不是简单把“高困惑度”拿来硬切，而是做了**局部自适应**。

### 2. 边界精化：不是泛泛“社区检测”，而是对 key 相似图优化目标

初始边界出来以后，论文会再做一次 refinement。

具体做法：

- 取 attention head 的 key vectors
- 用 token 间 key similarity 构成加权邻接矩阵 `A`
- 再对候选边界做优化，让事件内部更紧、事件之间更分离

论文主要讨论两类 refinement objective：

- **modularity**
- **conductance**

复杂度写得很明确：整体 refinement 为 **O(nm)**，
其中 `n` 是序列长度，`m` 是处理 chunk size。

所以更准确的理解是：

> 它不是离线聚类整段文本，而是围绕 surprise 初始边界，对 KV 结构做局部图论精化。

### 3. 两阶段检索：Similarity Buffer + Contiguity Buffer

检索阶段也不是单纯 top-k 相似度召回。

第一阶段：

- 对每个事件选 representative tokens
- 当前 query 与这些代表向量做 `k-NN`
- 得到语义上最相关的 `k_s` 个事件

第二阶段：

- 再把这些事件在原始时间线上相邻的事件放进一个 **contiguity buffer**
- 这个 buffer 是 queue 结构，模拟 temporal contiguity / asymmetry

最终写法上，进入上下文的是：

```text
k = k_s + k_c
```

其中：

- `k_s` = similarity buffer
- `k_c` = contiguity buffer

论文还强调：**每一层都可以单独检索和 attend 不同事件**，不是整模型只检一次。

## 实验结果（关键数字）

### 1. 对 InfLLM 的主结果

论文 Table 1 中，LLaMA 3.1-8B 这一组最关键：

| Base LLM | 方法 | LongBench Avg. | Retrieve.KV | Retrieve.PassKey | Retrieve.Number |
|----------|------|----------------|-------------|------------------|-----------------|
| LLaMA 3.1 | InfLLM (4k+4k) | 51.1 | 81.0 | 100.0 | 100.0 |
| LLaMA 3.1 | **EM-LLM SM** | **51.3** | **90.2** | **100.0** | **100.0** |

这个表面看平均分增幅不大，但 retrieval 相关任务提升非常明显。

论文正文给出的总结更完整：

- 在 **5 个 base LLM** 上都比 InfLLM 更强
- 在 LongBench 各任务组里，覆盖 **80%** 的提升
- 对 InfLLM 的最大提升约为：
  - **retrieval 任务 up to 40%**
  - **QA 任务 up to 29.7%**

### 2. 对 RAG 和 Full-context 的比较

论文 Appendix A.2 / Table 9 给出更直观的数据。
在 LLaMA-3.1-8B 上：

| 方法 | LongBench Avg. | ∞-Bench Avg. |
|------|----------------|--------------|
| RAG | 36.44 | 58.97 |
| Full-context | 39.30 | 66.33 |
| **EM-LLM S** | **51.58** | **66.66** |

正文明确写到：

- LongBench 上相对 NV-Embed-v2 RAG 提升 **30.5%**
- ∞-Bench 上相对 RAG 提升 **11.5%**

### 3. 超长上下文能力

论文给出的强结果是：

- 在 **Passkey Retrieval** 上做到 **10.2M tokens** 仍可 100% 准确
- 作者把这作为 full-context 模型在计算上几乎不可行的对照

### 4. 人类对齐分析

这里也要说得准确一点。

论文不是“播客实验”这么简单，而是在人类标注的**音频事件边界数据**上比较不同切分方法：

- 基于 surprise 的方法（`S / SM / SC`）持续优于固定切分方法（`F / FM / FC`）
- 这说明 LLM 的 surprise signal 与人类感知到的事件边界存在明显对应关系

## 与本项目的关系

**直接相关度：⭐⭐⭐⭐⭐**

这篇对我们尤其关键，因为它把三件我们一直想做的事同时证明了：

1. **动态事件切分优于固定 chunk**
2. **检索应该同时利用语义关联和时间邻近**
3. **认知科学启发不只是叙事包装，真的能改善 LLM 长上下文行为**

## 关键局限

- **没有遗忘机制**：事件会持续累积，长期运行仍面临存储膨胀
- **超参数较多**：`γ`、buffer 大小、contiguity ratio 都会影响结果
- **boundary refinement 有额外开销**：虽然比 full attention 轻很多，但比纯 surprise 切分更复杂
- **仍是 retrieval-based memory**：不是模型内部写入式记忆

## 待深入的问题

- [x] surprise 到底怎么算？→ **是 token 级负对数似然，不是笼统“不确定性变化”**
- [x] 边界阈值是固定的吗？→ **不是，使用滑动窗口 `μ + γσ` 自适应阈值**
- [x] refinement 是做什么？→ **对 attention-key similarity 图优化 modularity / conductance**
- [ ] 如何引入遗忘或 consolidation，而不是事件一直堆积
- [ ] 能否把 EM-LLM 的事件单元作为 MEMORYLLM 的写入颗粒
- [ ] 两阶段检索能否和图记忆结构结合，避免只靠局部时序邻接
