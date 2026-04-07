# SCM: Enhancing Large Language Model with Self-Controlled Memory Framework

## 基本信息

| 项目 | 内容 |
|------|------|
| **状态** | arXiv 预印本（2023.04），后版本发表于 DASFAA 2025 |
| **arXiv** | https://arxiv.org/abs/2304.13343 |
| **代码** | https://github.com/wbbeyourself/SCM4LLMs |

## 为什么这篇重要

SCM 虽然方法不复杂，但它很早就把一个后来非常重要的问题说清楚了：

**记忆系统真正需要控制器，不是只需要存储。**

也就是说，关键不只是“有 memory stream”，而是：
- 什么时候激活历史记忆
- 激活多少
- 原文还是摘要
- 当前 query 根本需不需要记忆

这就是 SCM 的价值。

## 核心架构（原文技术细节）

SCM 有三个部件：

1. **LLM Agent**
2. **Memory Stream**
3. **Memory Controller**

而且是 **plug-and-play** 的：
- 不改底层 LLM 结构
- 不要求微调 backbone

### 1. Memory Stream 存什么

每条 memory item 包含：
- interaction index
- observation
- system response
- memory summarization
- interaction embedding

embedding 的做法很具体：
- 把 **observation + system response** 拼起来
- 用 `text-embedding-ada-002` 编码

存储层则可以直接落在：
- Redis
- Pinecone 这类向量数据库

### 2. SCM 不是单一记忆，而是 activation memory + flash memory

论文明确区分两类记忆：

- **Activation Memory**
  - 长期记忆
  - 存相关历史

- **Flash Memory**
  - 短期记忆
  - 主要存前一轮 `T-1` 的实时上下文

一个 observation 进入后，SCM 的六步工作流是：

1. Input Acquisition
2. Memory Activation
3. Memory Retrieval
4. Memory Reorganization
5. Input Fusion
6. Response Generation

### 3. Memory Controller 的决策逻辑

这部分是论文最值得看的地方。

Controller 本身也是一个 LLM，
它不是学习一个隐式 policy，而是**显式自问两个问题**：

1. **当前输入需不需要激活历史记忆？**
2. **如果需要，摘要是否足够回答问题？**

也就是说，SCM 先做一个二段判断：
- `要不要检索`
- `检索后给原文还是摘要`

#### 第一步：是否需要记忆

论文用 prompt 让 controller 对当前输入输出：
- `yes (A)`
- `no (B)`

如果输出 `yes(A)`，才进入记忆检索。

#### 第二步：怎么给记忆排序

SCM 的 memory ranking 不是纯 embedding 相似度，
而是：

```text
rank_score = recency_score + relevance_score
```

其中：
- `recency_score`：越近期被访问过越高
- `relevance_score`：当前 query embedding 与 memory embedding 的 cosine similarity

然后取：

```text
top-k memories, where k in [3, 10]
```

#### 第三步：原文还是摘要

如果某条激活记忆太长，Controller 会再问一次：
**这条记忆的摘要能不能回答当前问题？**

触发条件也非常具体：
- 单条激活 memory 超过 **800 tokens**
- 且所有激活 memory 总长度超过 **2000 tokens**

这时才启动 summary gating。

如果判断“摘要够用”，就不再注入 full content，而只给 summary。

### 4. Memory Summarization 怎么做

论文在对话场景里，不直接用原始 observation / response 做 embedding，
而是先分别做摘要，再把：

- observation summary
- system response summary

拼接起来作为该条 interaction 的语义表示。

作者的理由是：
- user input 和 system response 长度差异可能很大
- 直接拿原文 embedding 会让某一侧信号压过另一侧

这点其实很实用，属于很典型的工程细节。

## 实验结果（关键数字）

### 长期对话

| 方法 | Answer Acc. | Memory Retrieval Recall | Single-turn Acc. | Multi-turn Acc. |
|------|-------------|-------------------------|------------------|-----------------|
| SCM turbo | 68.3 | 93.5 | 73.5 | 64.3 |
| **SCM davinci003** | **77.1** | **94.0** | **79.6** | **75.0** |

### 消融实验

| 变体 | 影响 |
|------|------|
| 去掉 memory controller | Answer Acc. 从 77.1 降到 59.3，Multi-turn 从 75.0 降到 49.4 |
| 去掉 flash memory | 只有小幅下降，说明它主要是局部辅助 |
| 去掉 activation memory | Retrieval Recall 直接变成 0，Multi-turn 也变成 0 |

论文原文总结得很直接：
- activation memory 是长期回忆的核心
- memory controller 的主要价值是**动态过滤 + 摘要选择**
- 没有 controller 时，会把检索结果粗暴拼接后再截断，信息损失严重

### 任务范围

SCM 不只做长期对话，还做：
- 书籍摘要
- 会议摘要

论文给的数据规模是：
- 单个实例长度从 **2 万 tokens 到 200 万 tokens**

这也是它为什么特别强调 controller 的原因：
没有控制器，根本不可能把这么长的记忆直接塞给 LLM。

## 与本项目的关系

**相关度：⭐⭐⭐**

SCM 很像一个早期版的 Memory Controller baseline：
- 没有复杂记忆图
- 没有 latent memory
- 也没有高级遗忘机制

但它非常清楚地展示了：
**controller 至少要做“是否检索 + 排序 + 摘要/原文选择”这三层决策。**

这对我们设计 Memory Controller 很有参考价值。

## 待深入的问题

- [x] Memory Controller 的决策逻辑？→ 不是单独训练策略网络，而是 prompt 驱动的 LLM controller，显式判断“要不要检索”和“摘要够不够”
- [ ] 和 MemGPT 的对比？→ SCM 更像“静态检索 + 控制器裁剪”，MemGPT 更像“外部存储 + 自主分页 + 函数控制流”
