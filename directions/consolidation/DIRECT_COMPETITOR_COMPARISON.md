# 记忆巩固方向：直接竞争工作逐篇拆解对比表

## 这份文件是干嘛的

这不是普通 reading list。

这份文件只回答一个问题：

**如果你现在做“记忆巩固”，最容易和哪些工作做重？到底重在哪？怎么避开？**

---

## 先看总表

| 工作 | 正式来源 | 时间 | 它的核心动作 | 和你做“巩固”有多重 | 现在最该警惕什么 |
|------|---------|------|-------------|-------------------|----------------|
| **TiMem** | arXiv | 2026-01-06 | 时间层级树 + 分层抽象 + 复杂度感知召回 | **极高** | 不要再做“层级时间树式巩固” |
| **LightMem** | ICLR 2026 | 2025-10 / 2026 | 预压缩 + topic-aware STM + sleep-time LTM update | **极高** | 不要只讲“离线睡眠巩固” |
| **PREMem** | Findings of EMNLP 2025 | 2025-11 | 存前推理 + 跨 session 关系建模 | **高** | 不要只讲“把推理前移到存储” |
| **SimpleMem** | arXiv | 2026-01-29 v3 | 语义压缩 + 在线语义综合 + 意图感知检索 | **中高** | 不要把“写入时在线综合”当新点 |
| **FadeMem** | arXiv | 2026-01 | 融合 + 冲突消解 + 双层迁移 + 遗忘 | **中高** | 不要只做“融合和冲突处理” |
| **Recursive Summarization** | Neurocomputing 2025 | 2023 / 2025 | 递归摘要形成长期对话记忆 | **中** | 不要只做“分段摘要再递归汇总” |

---

## 一个更精确的分工图

```text
原始对话流
  -> 预过滤/压缩
  -> 事件/片段组织
  -> 综合/抽象
  -> 长期存储
  -> 修订/冲突处理
  -> 检索/回答
```

现有工作大概占位如下：

| 环节 | 已有代表工作 |
|------|-------------|
| 预过滤/压缩 | LightMem, SimpleMem |
| 时间组织 | TiMem |
| 存前推理 | PREMem |
| 综合/抽象 | TiMem, LightMem, SimpleMem, Recursive Summarization |
| 修订/冲突处理 | FadeMem, PREMem（部分） |
| 高效召回 | TiMem, SimpleMem, LightMem |

所以你现在不能做的不是“巩固”，而是：

**不能只做这些已经有人做过一遍的巩固动作。**

---

## 1. TiMem

### 官方信息

- 标题: `TiMem: Temporal-Hierarchical Memory Consolidation for Long-Horizon Conversational Agents`
- 来源: arXiv
- 提交日期: `2026-01-06`
- 链接: https://arxiv.org/abs/2601.02845

### 它到底在做什么

最简单的人话版：

**把对话按时间做成一棵树，从细节一路往上整理成 profile。**

它的五层结构是：
- segment
- session
- day
- week
- profile

也就是说，它不是只存“某条记忆”，而是存“不同时间粒度下的记忆摘要”。

### 它强在哪里

1. 它把 `时间结构` 当一等公民，而不是普通 metadata。
2. 它已经明确把“memory consolidation”写进标题和方法主线。
3. 它的 story 很完整：
   - 时间层级组织
   - instruction-guided consolidation
   - complexity-aware recall
4. 它的 benchmark 也正对 LoCoMo / LongMemEval-S。

### 你最容易和它做重的地方

如果你做下面这些，很容易撞 TiMem：

- 时间树 / 层级时间记忆
- session/day/week/profile 这类多层抽象
- 按时间窗口结束触发高层巩固
- 基于 query complexity 选不同层级召回

### 和它不重的安全空间

相对 TiMem，更安全的空间是：

- `reconsolidation`
  不是只做一次层级抽象，而是后续证据到来时修订旧记忆
- `provenance`
  TiMem 强调层级和时间，不强调每条抽象记忆的来源追踪
- `revision / split`
  如果原先抽象错了，怎么拆开重建
- `episodic -> procedural`
  TiMem 更偏 persona / profile，不偏 procedure formation

### 一句话判断

**TiMem 已经占了“时间层级巩固系统”这条主赛道。**

---

## 2. LightMem

### 官方信息

- 标题: `LightMem: Lightweight and Efficient Memory-Augmented Generation`
- 来源: ICLR 2026 conference paper
- 公开版本: arXiv `2510.18866`
- 链接: https://arxiv.org/abs/2510.18866
- OpenReview PDF: https://openreview.net/pdf?id=oYHelQ3Edd

### 它到底在做什么

最简单的人话版：

**把 memory 系统拆成“感官预压缩 -> 短期主题整理 -> 睡眠期长期更新”。**

它特别像一个工程化得很强的三段式 memory pipeline：
- `Light1` 感官预压缩
- `Light2` topic-aware STM
- `Light3` sleep-time LTM update

### 它强在哪里

1. 离线更新故事讲得很顺。
2. 效率非常强，token 和 API 调用节省很明显。
3. 它已经明确提出：
   - reorganize
   - deduplicate
   - abstract
   - resolve inconsistencies
   - strengthen cross-knowledge connections

### 你最容易和它做重的地方

- “睡眠时间做巩固”
- “把在线和离线解耦”
- “先压缩再长期整理”
- “topic-aware 的短期整理，再进入长期记忆”

如果你的标题仍然是：

```text
An Asynchronous Sleep-Time Consolidation Engine for LLM Memory
```

那已经非常危险。

### 和它不重的安全空间

- `offline revision` 而不是 `offline update`
  它更强调离线更新和效率，不强调抽象后如何被修订
- `traceability`
  它强调效率，不强调每条长期记忆的来源链
- `benchmark-first consolidation metrics`
  它方法很强，但没有把 consolidation 指标体系独立立出来
- `semantic/procedural conversion`
  它主要还是长期 memory maintenance，不是显式知识化 / 技能化

### 一句话判断

**LightMem 已经占了“睡眠式离线巩固 + 极致效率”这条路线。**

---

## 3. PREMem

### 官方信息

- 标题: `Pre-Storage Reasoning for Episodic Memory: Shifting Inference Burden to Memory for Personalized Dialogue`
- 来源: Findings of EMNLP 2025
- 时间: `2025-11`
- 链接: https://aclanthology.org/2025.findings-emnlp.1204/

### 它到底在做什么

最简单的人话版：

**不是回答时再费劲推理，而是在存记忆前先把跨 session 的关系想清楚。**

它做了两件事：
- 把记忆分成 factual / experiential / subjective
- 在存前分析跨 session 的 evolution patterns

五类 evolution patterns 包括：
- extension / generalization
- accumulation
- specification / refinement
- transformation
- connection / implication

### 它强在哪里

1. 它不只是“摘要”，而是存前 reasoning。
2. 它已经在做跨 session 信息演化建模。
3. 它对小模型很友好，因为把复杂 reasoning 从回答阶段前移了。

### 你最容易和它做重的地方

- “存储前先建模跨 session 关系”
- “把多轮对话整理成结构化记忆片段”
- “从多个 session 中归纳变化模式”

如果你想做的是：

```text
把跨 session 的 evolution 提前在 memory construction 阶段做掉
```

那和 PREMem 的重叠会非常明显。

### 和它不重的安全空间

- `post-storage reconsolidation`
  PREMem 重在 pre-storage，你可以做 post-storage revision
- `provenance-preserving abstraction`
  PREMem 关注 reasoning memory fragment，不强调来源链审计
- `late evidence correction`
  PREMem 更像一次性构建 enriched memory，不是后验修订

### 一句话判断

**PREMem 已经占了“存前推理巩固”这条线。**

---

## 4. SimpleMem

### 官方信息

- 标题: `SimpleMem: Efficient Lifelong Memory for LLM Agents`
- 来源: arXiv
- 最新版本日期: `2026-01-29 (v3)`
- 链接: https://arxiv.org/abs/2601.02553

### 一个重要纠正

SimpleMem 现在的最新版主线，**不是**“离线递归巩固”。

它最新明确写的是三段：
- Semantic Structured Compression
- Online Semantic Synthesis
- Intent-Aware Retrieval Planning

所以更准确地说，它是：

**写入时的在线语义综合 + 结构化压缩系统。**

### 它到底在做什么

最简单的人话版：

**在记忆写进去的时候，就顺手把碎片融合成更高密度条目。**

例如：
- “用户要咖啡”
- “用户喜欢燕麦奶”
- “用户喜欢热饮”

会被在线综合成一条更完整的记忆。

### 它强在哪里

1. 它把“写入时综合”做得非常轻。
2. 它更像高信息密度 memory engineering。
3. 它在 token 效率上很强。

### 你最容易和它做重的地方

- 写入时就把碎片 merge 成统一记忆
- 以“减少碎片化”为主卖点
- 多视图 indexing + retrieval planning

### 和它不重的安全空间

- `async reconsolidation`
  它偏在线综合，不偏长期 revision
- `provenance / revision history`
  它关注压缩和高密度，不关注来源链和版本演化
- `semantic -> procedural conversion`
  它是 memory efficiency 路线，不是知识转化路线

### 一句话判断

**SimpleMem 占的是“在线综合压缩”这块，不是完整 reconsolidation。**

---

## 5. FadeMem

### 官方信息

- 标题: `FadeMem: Biologically-Inspired Forgetting for Efficient Agent Memory`
- 来源: arXiv
- 时间: `2026-01`
- 链接: https://arxiv.org/abs/2601.18642

### 它到底在做什么

最简单的人话版：

**不是重点研究“怎么整理成更高层知识”，而是研究“哪些记忆该留下、该合并、该衰减”。**

它已经覆盖的动作包括：
- importance scoring
- layer migration
- temporal-semantic clustering
- fusion with verification
- conflict resolution

### 它强在哪里

1. 冲突消解做得比很多系统细。
2. 融合不是瞎融，还带 preservation threshold。
3. 它是你最容易实现的强 baseline 之一。

### 你最容易和它做重的地方

- 只做融合
- 只做冲突处理
- 只做双层迁移
- 只做 importance-based decay + merge

### 和它不重的安全空间

- `reconsolidation as revision history`
- `traceable abstraction`
- `episodic -> semantic/procedural conversion`
- `benchmark-first consolidation metrics`

### 一句话判断

**FadeMem 不是你最大的 headline 竞争者，但一定是你最该认真打掉的 baseline。**

---

## 6. Recursive Summarization

### 官方信息

- 标题: `Recursively Summarizing Enables Long-Term Dialogue Memory in Large Language Models`
- 来源: arXiv 2023，后发表于 Neurocomputing 2025
- 链接: https://arxiv.org/abs/2308.15022

### 它到底在做什么

最简单的人话版：

**把长对话分段总结，再拿已有 summary 继续总结，形成滚动 memory。**

### 它强在哪里

1. 简单
2. 早
3. 很适合作为经典摘要型 baseline

### 你最容易和它做重的地方

- session summary
- hierarchical summary
- recursive summary memory

### 和它不重的安全空间

几乎所有更强的方向都和它不重，只要你不把“递归摘要”本身当创新点。

### 一句话判断

**它更多是历史基线，不是今天最危险的 direct competitor。**

---

## 最后的判断：真正的直接竞争顺位

如果按“最容易和你选题做重”的风险排序，我建议这样看：

1. `TiMem`
2. `LightMem`
3. `PREMem`
4. `SimpleMem`
5. `FadeMem`
6. `Recursive Summarization`

---

## 最后一句话

如果你现在还想做“记忆巩固”，最危险的不是没有方向，
而是你会不知不觉写成下面这些现成故事之一：

- TiMem 的时间层级版
- LightMem 的睡眠离线版
- PREMem 的存前推理版
- SimpleMem 的在线综合版

所以你下一步最安全的选题，必须明确写出：

**我不是在做哪一种现成故事。**

---

## 参考链接

- TiMem: https://arxiv.org/abs/2601.02845
- LightMem: https://arxiv.org/abs/2510.18866
- PREMem: https://aclanthology.org/2025.findings-emnlp.1204/
- SimpleMem: https://arxiv.org/abs/2601.02553
- FadeMem: https://arxiv.org/abs/2601.18642
- Recursive Summarization: https://arxiv.org/abs/2308.15022

