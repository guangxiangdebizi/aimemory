# 记忆巩固方向：Reconsolidation 问题定义

## 一句话版本

**现有 LLM memory 方法开始会“整理记忆”，但大多把整理看成一次性过程；我们要研究的是：已经被抽象化的长期记忆，在后续新证据到来时，能否被可追溯地修订、拆分、重锚定。**

---

## 1. 为什么现在要从 consolidation 进一步收敛到 reconsolidation

因为只说 `consolidation` 已经太宽了。

到 2026 年 4 月，下面这些路已经有人明显占位：

- `TiMem`：时间层级巩固
- `LightMem`：sleep-time 离线长期更新
- `PREMem`：存前推理与跨 session 关系构造
- `SimpleMem`：写入时在线语义综合
- `FadeMem`：融合、冲突消解、双层迁移、遗忘

这意味着，如果你继续把题目写成：

```text
我们提出一个新的 memory consolidation framework
```

审稿人很容易追问：

```text
和 TiMem / LightMem / PREMem / SimpleMem 到底差在哪？
```

所以现在更稳的做法不是继续讲“大巩固系统”，
而是把问题往前推进一步：

```text
记忆被整理后，后续还能不能被修订？
```

这一步就是 `reconsolidation`。

---

## 2. 什么叫 reconsolidation

最简单的人话版：

**记忆不是整理一次就定型，而是在后来遇到新证据时，会被重新打开、重新解释、重新写回。**

例如：

### 例子 1：偏好更新

旧记忆：
- “用户喜欢蓝色界面”

后来新证据：
- “用户最近明确说不喜欢蓝色界面”

普通 memory 系统经常会变成：
- 旧记忆还在
- 新记忆再加一条

于是长期库里出现冲突。

reconsolidation 的目标则是：
- 识别这不是简单新增，而是对旧抽象记忆的修订
- 保留修订链条
- 在后续检索时优先使用新版本

### 例子 2：抽象过头后纠正

系统先前根据几次对话抽象出：
- “用户喜欢咖啡”

后来发现其实更准确的是：
- “用户喜欢热咖啡，但不喜欢冰咖啡”

这说明旧抽象记忆不是完全错，而是**抽象得太粗**。

reconsolidation 要解决的就是：
- 能不能把粗抽象拆开
- 再重建成更精细、更正确的记忆

---

## 3. 为什么 reconsolidation 比普通 consolidation 更值得做

### 原因 1：它更接近真实长期记忆系统

真正长期运行的 memory system 不可能只整理一次。

因为现实交互一定会不断出现：
- 新证据
- 冲突证据
- 更晚揭示的原因
- 更高层抽象

如果系统只能：

```text
压缩一次 -> 存进去 -> 不再回头
```

那它迟早会积累：
- 过时抽象
- 错误泛化
- 自相矛盾的长期记忆

### 原因 2：它和现有直接竞争工作差异最清楚

现有系统大多已经覆盖：
- 怎么压缩
- 怎么分层
- 怎么离线更新
- 怎么在写入时综合

但“抽象后的长期记忆如何继续演化”这一步，仍然没有被明确做成主问题。

### 原因 3：它天然带来一组新的评测指标

普通 consolidation 常测：
- QA
- retrieval
- compression

reconsolidation 可以明确引入：
- `Revision Accuracy`
- `Stale Memory Rate`
- `Traceability`
- `Split / Merge Correctness`

这些指标更容易形成独立贡献。

---

## 4. 这个问题具体研究什么，不研究什么

## 研究什么

我们研究下面这个核心过程：

```text
旧长期记忆 + 新到证据 -> 是否需要修订？如何修订？修订后如何保持可追溯？
```

更具体地说，研究 4 个问题：

1. 什么情况下，新证据应该触发 reconsolidation，而不是简单追加
2. 旧长期记忆应该被 `revise / split / merge / retire` 中的哪一种操作处理
3. 修订后的长期记忆如何保留来源链和版本链
4. 检索阶段如何优先使用“当前有效版本”，而不是过时版本

## 不研究什么

这一步要说清楚，不然容易被认为和现有工作重叠。

### 我们不把下面这些作为主问题

- 不是单纯做 sleep-time update
- 不是单纯做 temporal memory tree
- 不是单纯做 recursive summarization
- 不是单纯做 pre-storage reasoning
- 不是单纯做 write-time semantic synthesis

也就是说：

```text
我们不是重新发明 TiMem / LightMem / PREMem / SimpleMem 的另一个版本
```

---

## 5. 问题形式化草图

### 5.1 输入

短期 episodic evidence 流：

```text
E = {e_1, e_2, ..., e_n}
```

其中每个 episode `e_i` 可以写成：

```text
e_i = (content, time, entities, source_session, confidence)
```

长期记忆集合：

```text
L = {l_1, l_2, ..., l_m}
```

### 5.2 长期记忆对象

和普通 memory entry 不同，这里每条长期记忆必须显式包含：

```text
l_j = (
  memory_text,
  memory_type,
  provenance_set,
  support_set,
  contradiction_set,
  revision_history,
  status
)
```

其中：
- `provenance_set`：这条记忆来自哪些原始 episode
- `support_set`：哪些证据支持它
- `contradiction_set`：哪些证据挑战它
- `revision_history`：它经历过哪些版本变更
- `status`：active / revised / retired

### 5.3 操作空间

给定新证据 `e_new` 和已有长期记忆 `l_j`，系统可以执行：

```text
ADD       新建
REVISE    修订旧记忆
SPLIT     将过粗抽象拆成多条
MERGE     将多条记忆合并
RETIRE    让旧版本退役
NOOP      不处理
```

### 5.4 目标

理想目标不是单一 accuracy，而是多目标优化：

```text
Quality =
α * Retention
+ β * Consistency
+ γ * Compactness
+ δ * Traceability
+ ε * Revisability
```

其中：
- `Retention`：关键信息没丢
- `Consistency`：长期库内部少冲突
- `Compactness`：不过度膨胀
- `Traceability`：抽象记忆能追溯来源
- `Revisability`：遇到新证据时能正确修订

---

## 6. 研究假设

如果你后面要做开题，这一节最重要。

### 假设 H1

**把长期记忆建模成“可修订对象”，会比一次性 consolidation 更能抑制过时记忆。**

### 假设 H2

**显式 provenance 会提升调试性、解释性，并降低错误抽象带来的长期污染。**

### 假设 H3

**在 delayed contradiction 和 knowledge update 场景里，reconsolidation 会明显优于 TiMem / LightMem / PREMem / SimpleMem 这类以单次整理为主的方法。**

### 假设 H4

**reconsolidation 的收益主要体现在“长期一致性”和“错误修正”上，而不一定体现在所有普通事实 QA 上。**

这点很重要，因为你不需要承诺“全指标吊打”，而是要承诺：

```text
在它真正应该强的任务上显著更强
```

---

## 7. 预期贡献可以怎么写

如果这个方向最后立题，比较稳的贡献写法是：

1. **问题贡献**
   我们将 LLM agent memory 中的 `reconsolidation` 明确提出为独立研究问题，而非单次 consolidation 的附属步骤。

2. **方法贡献**
   我们提出一个 `provenance-preserving reconsolidation` 框架，使长期记忆可以被修订、拆分、重锚定，并保留版本链。

3. **表示贡献**
   我们定义支持 `support / contradiction / revision history` 的长期记忆对象。

4. **评测贡献**
   我们构建针对 delayed revision、traceability、stale-memory suppression 的评测任务与指标。

---

## 8. 最适合的实验问题

reconsolidation 不应该只拿普通 QA 来证明。

最应该打的 4 类实验是：

### 8.1 Delayed Contradiction

旧记忆先形成，后来再给反证。

看系统能不能：
- 正确修订旧记忆
- 避免把旧错记忆继续当真

### 8.2 Abstraction Too Coarse

先故意让系统形成粗抽象，再补更多细节。

看系统能不能：
- split
- re-ground
- 生成更精确版本

### 8.3 Provenance Tracing

给出一条长期抽象记忆，追问：

```text
它是从哪些 episode 得出的？
```

看系统能不能回答。

### 8.4 Stale Memory Suppression

看检索时会不会继续拿出已经被修订或退役的旧版本。

---

## 9. 这个题目的真正风险

### 风险 1：问题太大

如果一上来就想把：
- revision
- split
- merge
- provenance
- benchmark
- retrieval

全做完，容易失控。

### 风险 2：reconsolidation 的收益不一定在通用 benchmark 上特别大

它最强的地方是：
- update
- correction
- consistency

不是所有普通问题都会体现优势。

### 风险 3：如果定义不够清楚，会被质疑成“只是更复杂的 memory update”

所以你后面一定要把 `reconsolidation != update` 说清楚。

一个简单区分是：

```text
update 更像追加或替换
reconsolidation 更像对已有抽象记忆的结构性重写
```

---

## 10. 为什么这个问题现在最值得推进

因为它刚好卡在一个很好的位置：

- 比“大而全 consolidation”更聚焦
- 比“纯 benchmark”更有方法味
- 比“纯工程 memory update”更有研究问题感
- 比 TiMem / LightMem / PREMem / SimpleMem 更不容易做重

换句话说：

**它不是最轻松的题，但它是当前最像“能立起来的题”的那个点。**

---

## 11. 接下来最该做什么

如果以 reconsolidation 继续推进，下一步最合理的是：

1. 先补一份 `METHOD_BLUEPRINT.md`
   把 `ADD / REVISE / SPLIT / RETIRE` 的触发条件和流程写清楚
2. 再补一份 `EVALUATION_TASKS.md`
   把 delayed contradiction / provenance tracing 的样例任务写出来
3. 最后再决定：
   是先做 benchmark-first
   还是先做最小 rule-based prototype

---

## 最后一句话

现在不是说：

```text
“我们终于找到一个 memory 方向”
```

而是：

```text
“我们已经把大方向收敛到了巩固，
并且在这个大方向里，把最值得立题的切口收缩到了 reconsolidation。”
```

