# MemGPT: Towards LLMs as Operating Systems

## 基本信息

| 项目 | 内容 |
|------|------|
| **状态** | arXiv 预印本（2023.10），后续工程化演化为 Letta |
| **作者** | Charles Packer, Sarah Wooders, Kevin Lin 等 |
| **机构** | UC Berkeley |
| **arXiv** | https://arxiv.org/abs/2310.08560 |
| **框架** | https://www.letta.com/ |

## 为什么这篇重要

MemGPT 的影响力不在于“检索效果最好”，而在于它第一次把 LLM 记忆系统说清楚成一个
**操作系统式的上下文管理问题**：

- context window = RAM
- 外部存储 = disk
- function call = 系统调用
- paging = 把外部内容换入/换出上下文

这个隐喻后来几乎成了 agent memory 的公共语言。

## 核心架构（原文技术细节）

### 1. Main Context 不是一整块，而是三段

MemGPT 的主上下文（main context）由三部分组成：

1. **System Instructions**
   - 只读
   - 描述控制流、内存层级、函数使用规则

2. **Working Context**
   - 可读写
   - 存当前人格、用户偏好、长期稳定事实

3. **FIFO Queue**
   - 滚动保存最近消息、系统消息、函数调用输入输出
   - 队首还有一个**递归摘要**
   - 用来概括已经被挤出队列的旧消息

也就是说，所谓“主上下文”本身已经分层了，不是把所有东西都混在一个 prompt 里。

### 2. 外部存储分成两类

论文区分：
- **Recall Storage**
  - 存完整对话消息历史
  - 适合把旧消息再读回来

- **Archival Storage**
  - 存任意长度的外部文本对象
  - 适合文档、知识库、长文本分析

在文档 QA 实验中，archival storage 的实现是：
- **PostgreSQL**
- `pgvector`
- **HNSW** 索引

也就是说，它不是抽象概念，是真按数据库做的。

### 3. 分页策略的具体实现：不是 LRU/LFU，而是“记忆压力 + 自主函数调用”

这是 MemGPT 最核心的工程细节。

#### Queue Manager 做什么

每次系统收到新消息时：
- 把用户输入和模型输出都写入 recall storage
- 把新内容 append 到 FIFO queue
- 触发下一次 LLM inference

#### 什么时候提醒“内存要爆了”

当 prompt token 超过底层模型 context window 的
**warning token count** 时：
- 论文示例给的是 **约 70% context window**
- Queue Manager 会插入一条 system message
- 提示 LLM 出现了 **memory pressure**
- 让它主动调用函数，把重要信息写进 working context 或 archival storage

#### 什么时候真正 flush

当 prompt token 超过 **flush token count** 时：
- 论文示例给的是 **约 100% context window**
- Queue Manager 会执行队列驱逐
- 例如驱逐 **50% context window** 对应的消息
- 并基于“旧递归摘要 + 被驱逐消息”生成一个新的递归摘要

被驱逐消息：
- 不再在当前上下文里
- 但仍完整保存在 recall storage
- 可以后续通过函数调用再读回

所以它的 paging 逻辑是：
**阈值触发的队列压缩 + 模型自主管理的显式换入/换出**

#### Function Chaining

MemGPT 支持一个特殊参数：

```text
request heartbeat=true
```

作用：
- 一次函数调用后，不立即返回给用户
- 继续触发下一轮 LLM 推理
- 让模型能连续执行多步检索 / 分页 / 追踪键值

这就是它能做 multi-step retrieval 的关键。

### 4. 文档检索是如何分页的

论文给了一个很直观的例子：

```text
archival_storage.search("nobel physics")
archival_storage.search("nobel physics", page=2)
```

含义是：
- 先取第一页结果
- 如果不够，再继续翻下一页
- 把分页结果逐步带回 main context

这正是“OS 式 paging”在 LLM 里的对应物。

### 5. 它不是被动检索器，而是自主管理控制流

MemGPT 的 completion token 会被解释成 function call。

这意味着模型可以自己决定：
- 什么时候 search archival storage
- 什么时候写 working context
- 什么时候把内容存到 archival storage
- 什么时候继续 heartbeat 以执行下一步操作

所以 MemGPT 不是“检索增强”，而是
**把 memory management 变成 agent policy**。

## 实验结果（关键数字）

### 长期对话：Deep Memory Retrieval

论文在多 session 对话上测了能否正确回忆很久以前的信息：

| 基座模型 | 原始 Accuracy | +MemGPT Accuracy |
|----------|---------------|------------------|
| GPT-3.5 Turbo | 38.7% | 66.9% |
| GPT-4 | 32.1% | 92.5% |
| GPT-4 Turbo | 35.3% | 93.4% |

说明 MemGPT 在跨 session consistency 上提升非常大。

### 文档 QA

论文结论是：
- 固定上下文 baselines 随检索文档数增加会因为截断而退化
- MemGPT 的表现基本不受文档总长度增长影响
- GPT-4 和 GPT-4 Turbo 上跑出的 MemGPT 曲线基本一致

### Nested KV Retrieval

论文还专门造了一个需要多跳追踪 key-value 的 nested KV 任务。

结论：
- **只有 MemGPT 能在超过 2 层嵌套后仍稳定完成任务**
- baseline 模型很难稳定做跨页、多跳、递归式查询

## 与本项目的关系

**相关度：⭐⭐⭐**

MemGPT 不是“类人记忆”的终点，因为它本质上还是外部存储 + 显式函数调用。

但它对工程设计非常有价值，尤其是：
- 上下文分层
- token-pressure 驱动的 paging
- function chaining
- 模型自主管理 memory flow

这些都很适合作为 agent memory controller 的起点。

## 待深入的问题

- [ ] LLM 自主管理记忆的可靠性？→ 论文显示有效，但也明确依赖底层模型的 function-calling 能力，GPT-3.5 明显弱于 GPT-4 系
- [x] 分页策略具体实现？→ `warning token count` 预警、`flush token count` 驱逐、递归摘要压缩、函数调用分页搜索，不是传统 LRU/LFU
- [ ] 后续 Letta 的工程化能力如何？→ 这属于论文之后的框架演化问题，和本文方法本身应分开看
