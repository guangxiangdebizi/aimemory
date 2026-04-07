# GSW: Beyond Fact Retrieval — Episodic Memory for RAG with Generative Semantic Workspaces

## 基本信息

| 项目 | 内容 |
|------|------|
| **Venue** | AAAI 2026 + NeurIPS 2025 Workshop Spotlight |
| **arXiv** | https://arxiv.org/abs/2511.07587 |
| **代码** | https://github.com/roychowdhuryresearch/gsw-memory |

## 为什么这篇重要

传统 RAG 检索的是"相关片段"，但情景记忆要解决的是：
**同一个人、同一个地点、同一个事件类型在不同时空反复出现时，模型怎么区分并追踪它们。**

GSW 的核心不是做更强的向量检索，而是把长叙事压成一个**可更新的语义工作空间（workspace）**，
让模型存的是角色、状态、动作、时空关系，而不是原始 chunk。

## 核心架构（原文技术细节）

### 1. Operator：把文本 chunk 变成局部语义图

Operator 不是手写规则，也不是单独训练的小模型，**论文里直接用 GPT-4o 提示实现**。

具体流程：
- 先在 **chapter 级**做共指消解
- 再把每章切成**3 句一个 chunk、无重叠**
- 用温度 **0** 的 GPT-4o 对每个 chunk 抽取结构化语义

抽出来的不是普通三元组，而是一整套事件状态：
- **Actors**：参与实体
- **Roles**：实体在当前事件中的角色分布
- **States**：角色下的状态变化
- **Verbs / Valences**：动作及其导致的角色/状态转移
- **Time / Space**：时间和地点约束
- **Forward-falling Questions**：由当前局部事件自然引出的可回答问题

论文把单步 workspace 写成：

```text
M_n ~ p(A, R, S, V, T, X, Q | C_0:n)
```

也就是：给定到当前为止的上下文，workspace 存的是
实体 A、角色 R、状态 S、动作 V、时间 T、空间 X、以及可追问问题 Q 的联合分布。

### 2. Reconciler：把局部图递归并入全局工作空间

Reconciler 负责把新 chunk 的局部表示 `W_n` 和旧工作空间 `M_{n-1}` 融合成新的 `M_n`：

```text
P(M_n | C_0:n)
= Σ_{M_{n-1}, W_n}
  P(M_n | M_{n-1}, W_n)
  P(M_{n-1} | C_0:n-1)
  P(W_n | C_n)
```

它本质上是一个**状态空间更新**：
- Operator 负责 `C_n -> W_n`
- Reconciler 负责 `M_{n-1} + W_n -> M_n`

具体实现上：
- 也是通过 **GPT-4o prompt** 做
- 以**连续 chunk**为单位递归协调
- 论文实验里先把一章内所有 chunk 协调成**每章一个 reconciled GSW**
- 对实体的 **role / state / time / space** 全部加时间戳保存
- 如果某个实体触发了新的时空更新，会**传播到所有共享该时空节点的实体**
- 前面 Operator 产生的 forward-falling questions，也会在 Reconciler 阶段继续解析和补全

### 3. Query 阶段：不是直接检索 chunk，而是检索实体化摘要

问答时的流程也很关键：

1. 从 query 中抽取实体名
2. 用**字符串匹配**在当前 GSW 中找到对应节点
3. 从 workspace 为这些实体重建**情景摘要**
4. 对摘要做一次**语义重排**
5. 把 top 摘要交给 GPT-4o 生成最终答案

所以 GSW 的 retrieval 单位不是原始文档块，而是
**“以实体为中心、带时空上下文的情景摘要”**。

## 实验结果（关键数字）

### EpBench-200 数据规模

| 指标 | 数值 |
|------|------|
| 章节数 | 200 |
| 总 tokens | 102,870 |
| QA 数量 | 686 |
| 单个 query 最多关联章节 | 17 |

### EpBench-200 主结果

- **Overall Precision / Recall / F1 = 0.865 / 0.894 / 0.850**
- 在最难的 **6+ cues** 场景下，GSW 仍有：
  - **P = 0.891**
  - **R = 0.822**
  - **F1 = 0.834**
- 在这个 hardest case 上，相比 HippoRAG2，**Recall 高约 20%**

### EpBench-2000 扩展结果

10 倍规模数据下，GSW 仍保持领先：
- **Overall Precision / Recall / F1 = 0.830 / 0.796 / 0.773**
- 比最强 baseline 的整体 F1 仍高约 **15%**

### Token 效率

| 方法 | Avg. Tokens / Query | Avg. Cost / Query |
|------|---------------------|-------------------|
| Vanilla LLM | ~101,120 | ~$0.2528 |
| Embedding RAG | ~8,771 | ~$0.0219 |
| GraphRAG | ~7,340 | ~$0.0184 |
| HippoRAG2 | ~8,771 | ~$0.0219 |
| **GSW** | **~3,587** | **~$0.0090** |

也就是说：
- 相比最省 token 的 GraphRAG，GSW 再降 **51%**
- 相比 Embedding RAG / HippoRAG2，token 降幅接近 **59%**

## 人工评估（Operator 不是“看起来像对”，而是真的更可读）

论文专门做了一个**Operator 语义图的人类偏好评测**。

设置：
- 从 GDELT 抽取 5 类新闻情境：Crime & Justice、Economy、Firefighting、Healthcare、Tech Development
- 每篇文章切成 **3 句短上下文**
- 让人工在 Operator 输出和基线语义框架之间盲选

结果：
- 对 GLEN 的偏好率：**0.90 ~ 1.00**
- 对 BERT-SRL 的偏好率：**0.96 ~ 0.98**
- 对 FST 的偏好率：**0.70 ~ 0.94**

这说明 Operator 生成的语义图，不只是“能算”，而且在人看来也**更贴近叙事语义结构**。

## 与本项目的关系

**相关度：⭐⭐⭐⭐**

GSW 最值得借鉴的是：它把"情景记忆"明确建模成一个**持续更新的工作空间**。

和传统 RAG 相比，它更像是在做：
- 事件级表示
- 实体状态追踪
- 时空一致性维护
- 基于结构化摘要的问答

如果我们后面要做"episodic layer"，GSW 是目前最接近工程蓝图的一篇。

## 待深入的问题

- [x] Operator 和 Reconciler 的实现？→ 论文里两者都主要通过 GPT-4o prompt 实现，Operator 做局部语义图抽取，Reconciler 做递归状态更新
- [x] EpBench 详细数字？→ EpBench-200 上总体 F1=0.850，EpBench-2000 上总体 F1=0.773，query token 约 3,587
- [ ] 工作空间的长期容量管理？→ 论文没有显式遗忘/压缩机制，更多是“结构化表达减少 query token”，不是“主动控制 workspace 增长”
- [ ] 和 EM-LLM 的事件分割如何互补？→ 一个解决“事件怎么切”，一个解决“切完后怎么存成结构”
