# 记忆巩固方向：研究计划

## 先校正目标

原来最危险的版本是：

```text
“我们做一个异步巩固引擎，把短期记忆整理成长期记忆。”
```

这个说法现在太泛了。
因为：
- TiMem
- LightMem
- SimpleMem
- PREMem

都已经把这类故事讲掉了一大块。

所以现在的研究计划必须先做一件事：

**不要再把目标设成“做一个 consolidation system”，而要设成“解决 consolidation 里还没被讲透的一个关键子问题”。**

---

## 一、推荐的问题定义

在当前文献格局下，更稳的主问题是下面 3 选 1。

### 方案 A：可追溯的 reconsolidation

一句话：

**记忆不是整理一次就结束，而是随着新证据到来被重新整理，而且每次抽象都能追溯来源。**

为什么好：
- 和 TiMem / LightMem / PREMem / SimpleMem 拉开差异
- 比单次 consolidation 更有认知科学味道
- 可以和冲突更新、知识修订自然结合

### 方案 B：episodic -> semantic / procedural 转化

一句话：

**研究多个 episode 如何被巩固成稳定知识或可复用 procedure。**

为什么好：
- 这是认知上很核心，但现有 LLM memory 里很少被明确建模的部分
- 能和 CLS / schema theory 对接

### 方案 C：benchmark-first 的 consolidation

一句话：

**先把 consolidation 的评测问题立起来，再配一套简洁但严谨的方法。**

为什么好：
- 最不容易和方法工作撞车
- 即使后面别人又发新方法，你的 benchmark 价值仍在

---

## 二、不建议作为主线的题目

下面这些题目太容易做重：

- 单纯异步总结
- 单纯分层 memory tree
- 单纯 sleep-time update
- 单纯 topic-based consolidation
- 单纯短期到长期转存

这些最多可以做成你方法里的一个子模块，不能做 headline。

---

## 三、我建议你的主线

如果按“创新空间 + 风险 + 可写性”综合考虑，我建议优先做：

### 推荐主线：可追溯 reconsolidation

#### 核心问题

当系统先前已经把多个 episode 巩固成一条长期记忆后，
如果后续出现：
- 新证据
- 冲突证据
- 更高层解释

系统能否：
- 修订旧记忆
- 保留来源链
- 避免新旧版本互相打架

#### 核心贡献可以写成

1. 我们提出一个 `provenance-preserving reconsolidation` 框架
2. 每条长期记忆都显式绑定其来源 episode 集合
3. 当新证据到来时，系统不是简单追加，而是做 revision / merge / split
4. 我们定义一组专门评估 reconsolidation 的指标

这条线比“再做一个巩固引擎”更像论文问题。

---

## 四、方法草图

### 输入

短期记忆流：

```text
S = {e_1, e_2, ..., e_n}
```

每个 `e_i` 是 episode-level memory unit，包含：
- content
- timestamp
- entities
- source session
- confidence

### 长期记忆对象

长期记忆不只存内容，还要存来源：

```text
l_j = (
  abstract_memory,
  type,
  provenance_set,
  support_events,
  contradiction_events,
  revision_history
)
```

这里最关键的是：
- `provenance_set`
- `revision_history`

没有这两个字段，就很难做真正的 reconsolidation。

### 三类核心操作

#### 1. Consolidate

把多个短期事件压成一个长期记忆。

#### 2. Revise

当新证据和旧记忆冲突时，修订旧记忆。

#### 3. Split / Re-ground

如果原来的抽象记忆被证明混得太粗，就拆开并重新锚定来源。

---

## 五、和现有工作的明确差异化

### 相对 TiMem

TiMem 强在：
- temporal-hierarchical organization

你的差异：
- 不是只做层级组织
- 而是强调 `revision under later evidence`
- 并增加 `provenance-preserving` 机制

### 相对 LightMem

LightMem 强在：
- sleep-time consolidation
- 高效率

你的差异：
- 不把重点放在“离线更新”
- 而放在“抽象后如何被修订、追溯、纠错”

### 相对 SimpleMem

SimpleMem 强在：
- online semantic synthesis
- structured compression

你的差异：
- 不只是写入时综合压缩
- 而是强调“抽象后的长期记忆如何继续演化和修订”

### 相对 PREMem

PREMem 强在：
- pre-storage reasoning

你的差异：
- 你研究的是 post-storage / post-consolidation revision

### 相对 FadeMem

FadeMem 强在：
- fusion
- conflict resolution
- forgetting

你的差异：
- FadeMem 处理的是融合和衰减
- 你做的是更系统的 revision history 和 provenance-aware reconsolidation

---

## 六、阶段计划

## Phase 0：文献去重与定位（1 周）

目标：
- 把 TiMem / LightMem / SimpleMem / PREMem / FadeMem 彻底读透
- 明确哪些 claim 不能再说

交付物：
- 一页 related work 定位表
- 一页 “we are NOT doing X” 的排除表

## Phase 1：问题形式化（2 周）

你需要明确写出：

### 1. 对象定义

- episode
- consolidated memory
- provenance
- revision event

### 2. 操作定义

- merge
- abstract
- revise
- split
- retire

### 3. 优化目标

至少包括：

```text
Quality =
α * Retention
+ β * Consistency
+ γ * Compactness
+ δ * Traceability
+ ε * Revisability
```

其中 `Revisability` 是你比现有工作更有辨识度的部分。

交付物：
- Problem formulation 草稿
- 指标定义草稿

## Phase 2：benchmark 设计（2-3 周）

继续使用：
- LongMemEval
- LoCoMo
- LoCoMo-Plus

同时自建 3 个核心子任务：
- delayed contradiction
- abstraction faithfulness
- provenance tracing

交付物：
- 一个小规模开发集
- 一个论文主实验集

## Phase 3：baseline 落地（2-3 周）

优先实现：
- No Consolidation
- Rule-based Consolidation
- Recursive Summarization
- FadeMem-style subset

论文对照保留：
- TiMem
- LightMem
- SimpleMem
- PREMem

交付物：
- 可运行 baseline 框架
- 主实验脚本

## Phase 4：方法实现（3-4 周）

建议方法最小版本：

1. 事件级输入
2. consolidation graph / provenance graph
3. revision trigger
4. revise / split / merge 操作
5. retrieval 端读取最新有效版本

交付物：
- 最小可跑版本
- 初步实验结果

## Phase 5：分析与论文（3 周）

重点分析 4 件事：
- 压缩后为什么没丢关键事实
- 哪些情况下系统会修订旧记忆
- 哪些时候会错误抽象
- provenance 对调试和解释有什么帮助

---

## 七、投稿故事怎么写

比较稳的 paper story 是：

```text
现有 memory 方法已经开始做 consolidation，
但多把它视为单次压缩或层级归纳过程。
我们指出，真正长期运行的 agent memory 还需要 reconsolidation：
即在后续证据到来时，对已经抽象化的长期记忆进行可追溯修订。
为此，我们提出一个 provenance-preserving reconsolidation framework，
并构建针对 revision / traceability / abstraction faithfulness 的评测任务。
```

这个故事比“我们做了一个新的 consolidation engine”更不容易撞车。

---

## 八、风险与保底方案

### 风险 1：方法太复杂，做不完

保底：
- 先做 benchmark-first
- 方法只做 rule-based provenance reconsolidation

### 风险 2：赢不过 LightMem / TiMem

保底：
- 不主打整体 F1 全面超过
- 主打它们没测的维度：
  - revision accuracy
  - provenance traceability
  - stale-memory suppression

### 风险 3：reconsolidation 效果不明显

保底：
- 把论文重心转到新 benchmark 和新指标

---

## 九、最后一句话

你现在最应该避免的是：

**“拿一个 2024 年的巩固想法，在 2026 年重新包装。”**

最应该做的是：

**围绕当前已经出现的 TiMem / LightMem / SimpleMem，把问题进一步推进到它们还没真正解决的那一步。**

---

## 参考链接

- TiMem: https://arxiv.org/abs/2601.02845
- LightMem: https://arxiv.org/abs/2510.18866
- SimpleMem: https://arxiv.org/abs/2601.02553
- PREMem: https://arxiv.org/abs/2509.10852
- FadeMem: https://arxiv.org/abs/2601.18642
- LongMemEval: https://arxiv.org/abs/2410.10813
- LoCoMo: https://aclanthology.org/2024.acl-long.747/
