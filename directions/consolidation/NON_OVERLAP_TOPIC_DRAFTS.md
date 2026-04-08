# 记忆巩固方向：不撞车选题草案

## 这份文件怎么用

前一份文件告诉你：

**哪些工作已经占位了。**

这份文件告诉你：

**在这种情况下，你还能从哪里切进去，而且不容易和现有工作做重。**

---

## 先给结论

如果你的目标是：
- 不和现有工作大面积重叠
- 又保留“记忆巩固”这个核心主题

那我建议优先考虑这 4 个题目：

1. `可追溯 reconsolidation`
2. `episodic -> semantic schema induction`
3. `episodic -> procedural consolidation`
4. `benchmark-first consolidation`

---

## 选题 1：可追溯 reconsolidation

### 一句话题目

**不是只把记忆整理一次，而是在新证据出现后，重新修订旧抽象记忆，并保留来源链。**

### 为什么不容易撞车

- 不同于 TiMem 的层级时间组织
- 不同于 LightMem 的睡眠式离线更新
- 不同于 PREMem 的存前推理
- 不同于 SimpleMem 的写入时综合

它研究的是：

```text
抽象后的长期记忆怎么继续演化
```

### 核心问题

当系统已经把多个 episode 巩固成一条长期记忆后，
后面又来了：
- 新补充证据
- 反例
- 冲突证据
- 更好的解释

系统怎么做：
- revise
- split
- merge
- retire

### 最小方法草图

长期记忆对象里显式保存：
- `provenance_set`
- `support_events`
- `contradiction_events`
- `revision_history`

新证据进入后，不是简单 append，而是做：
- `revise`
- `split`
- `re-ground`

### 最适合的实验

- delayed contradiction
- stale memory correction
- provenance tracing
- revision accuracy

### 风险

- 需要你把“修订动作”定义清楚
- 比单次 consolidation 更复杂

### 推荐度

**最推荐**

---

## 选题 2：episodic -> semantic schema induction

### 一句话题目

**研究多个 episode 如何被巩固成稳定 schema，而不是只停留在 episodic storage。**

### 为什么不容易撞车

现有很多工作都在：
- 存 episode
- 找 episode
- 压 episode

但真正显式地研究：

```text
episode 怎么变成 schema
```

的还不多。

### 核心问题

给系统多次相关经历，例如：
- 多次选餐
- 多次旅游偏好
- 多次协作习惯

它能否归纳出：
- 稳定偏好
- 行为模式
- 高层规则

而且这个 schema 还能在后续被新 evidence 修正。

### 最小方法草图

1. 先收集 episodic clusters
2. 检测 recurring patterns
3. 归纳 schema candidates
4. 用后续 episode 做支持或反驳
5. 输出 semantic memory with confidence

### 最适合的实验

- pattern induction
- preference evolution
- schema precision / recall
- LongMemEval 的 update 类问题

### 风险

- schema 质量评估比普通 QA 更难

### 推荐度

**很推荐**

---

## 选题 3：episodic -> procedural consolidation

### 一句话题目

**不是把经历变成知识，而是把经历变成可复用 procedure。**

### 为什么不容易撞车

这条线和现有主流 memory paper 的重叠最小。

多数工作关注：
- factual memory
- preference memory
- profile memory

很少明确去建模：

```text
反复经历 -> 可复用操作经验
```

### 核心问题

如果系统多次经历类似问题：
- 调参失败后成功
- 某种检索策略在某类问题里好用
- 某类用户沟通套路反复有效

能否把这些具体 episode 提炼成：
- procedure
- heuristic
- reusable strategy

### 最小方法草图

1. 对 episode 做 task/outcome tagging
2. 聚合同类成功 / 失败轨迹
3. 提炼 procedure candidates
4. 在新任务上测试 transfer

### 最适合的实验

- task transfer
- success rate lift
- fewer repeated mistakes

### 风险

- benchmark 需要自己搭
- 更像长期方向，不是最省事的首发论文

### 推荐度

**中高**

---

## 选题 4：benchmark-first consolidation

### 一句话题目

**先把 consolidation 的评测问题立住，再配一个简洁方法。**

### 为什么不容易撞车

因为现在方法已经很多，但大家测的还是：
- QA
- retrieval
- long-context reasoning

真正专门测 consolidation 的标准还不够成熟。

### 核心问题

设计一个 benchmark，显式测：
- retention under compression
- abstraction faithfulness
- delayed revision
- provenance traceability
- schema induction

### 最小方法草图

1. 从 LoCoMo / LongMemEval 出发构造子任务
2. 定义 consolidation-specific metrics
3. 以 rule-based + provenance-aware baseline 开始

### 最适合的实验

它本身就是实验主轴。

### 风险

- 需要 benchmark 设计足够 convincing
- 方法贡献可能显得没那么 flashy

### 推荐度

**高，尤其适合保底**

---

## 四个题目的横向比较

| 题目 | 新颖度 | 工程难度 | 撞车风险 | 适合首发吗 | 我建议 |
|------|--------|----------|----------|-----------|-------|
| 可追溯 reconsolidation | 高 | 中高 | 低 | 是 | **首选** |
| episodic -> semantic schema induction | 高 | 中 | 低 | 是 | **次选** |
| episodic -> procedural consolidation | 高 | 高 | 很低 | 视资源而定 | 可做长期方向 |
| benchmark-first consolidation | 中高 | 中 | 很低 | 是 | 很稳 |

---

## 最不建议的 5 个题目

下面这些即使能做出来，也很容易被问“和已有工作差在哪”：

1. 纯 sleep-time consolidation
2. 纯 temporal memory tree
3. 纯 recursive summary memory
4. 纯 storage hierarchy + update
5. 纯 write-time synthesis

因为它们分别会逼近：
- LightMem
- TiMem
- Recursive Summarization
- Memory OS
- SimpleMem

---

## 如果你现在就要立项，我建议这样选

### 最稳的组合

主问题：
- `可追溯 reconsolidation`

副贡献：
- `ConsolidBench` 小规模子任务

这样你的论文结构会很顺：

1. 现有工作开始做 consolidation，但多是单次压缩或层级组织
2. 真正长期运行的系统还需要 reconsolidation
3. 我们提出 provenance-preserving reconsolidation
4. 我们额外定义专门评测 revision / traceability 的任务

### 次稳的组合

主问题：
- `episodic -> semantic schema induction`

副贡献：
- 可追溯抽象指标

这更偏认知科学故事。

---

## 直接可用的题目草案

### 草案 A

`Provenance-Preserving Reconsolidation for Long-Term Memory in LLM Agents`

### 草案 B

`From Episodes to Schemas: Traceable Semantic Consolidation for LLM Agent Memory`

### 草案 C

`ConsolidBench: Evaluating Compression, Revision, and Traceability in LLM Memory Consolidation`

### 草案 D

`Beyond Sleep-Time Updates: Revisable Long-Term Memory Consolidation for Conversational Agents`

---

## 最后一句话

你现在最该避免的不是“没想法”，而是：

**把一个已经有人做过的巩固故事，换个词再讲一遍。**

如果你真想不撞车，最好的办法不是把系统做得更复杂，
而是把问题定义推进一步：

- 从 consolidation 到 `reconsolidation`
- 从 summary 到 `traceable abstraction`
- 从 storage 到 `schema / procedure formation`

