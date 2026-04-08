# 记忆巩固方向：Reconsolidation 评测任务设计

## 这份文件的目标

如果你做的是 `reconsolidation`，那就不能只拿普通 QA 来证明。

因为普通 QA 很可能只会告诉你：
- 系统能不能答对

但不会告诉你：
- 旧错误记忆有没有被修掉
- 抽象记忆能不能追溯来源
- 过粗抽象能不能被拆开

所以这份文件的目标是：

**把 reconsolidation 真正该测的任务单独定义出来。**

---

## 一、评测原则

Reconsolidation 的评测必须覆盖 4 个核心能力：

1. `Revision`
   新证据来了，能不能正确修订旧记忆
2. `Traceability`
   抽象记忆能不能追溯来源
3. `Granularity Repair`
   旧抽象太粗时，能不能纠正
4. `Stale Memory Suppression`
   旧版本是否会继续污染检索和回答

所以这里建议设计 5 类任务。

---

## 任务 1：Delayed Contradiction

### 测什么

测试系统遇到**延迟到来的反证**时，
能不能修订旧长期记忆，而不是继续同时保留冲突版本。

### 任务结构

#### Stage A

先给一串对话，让系统形成一个旧长期记忆。

例如：

```text
Session 1:
- 用户说最近很喜欢蓝色 UI
- 用户说蓝色看起来专业
```

系统可能形成：

```text
“用户喜欢蓝色界面”
```

#### Stage B

隔一段时间后，再给新证据：

```text
Session 4:
- 用户说现在已经不喜欢蓝色界面了
- 用户说蓝色让他想到旧系统
```

### 期望

系统应该：
- 修订旧记忆
- 让新版本成为 active version
- 压低或退役旧版本

### 核心指标

- `Revision Accuracy`
- `Stale Memory Rate`
- `Contradiction Persistence`

---

## 任务 2：Refinement After Over-Abstraction

### 测什么

测试系统是否能在后续证据到来后，修复过于粗糙的抽象。

### 任务结构

#### Stage A

先给有限证据，诱导系统形成粗抽象。

例如：

```text
- 用户说喜欢喝咖啡
- 用户经常点拿铁
```

系统可能形成：

```text
“用户喜欢咖啡”
```

#### Stage B

再给更细的限定：

```text
- 用户说只喜欢热咖啡
- 用户不喜欢冰咖啡
- 用户不喜欢太苦的美式
```

### 期望

系统能够：
- revise 或 split 旧记忆
- 形成更细粒度版本

### 核心指标

- `Refinement Accuracy`
- `Split Correctness`
- `Overgeneralization Error`

---

## 任务 3：Provenance Tracing

### 测什么

测试抽象长期记忆能不能追溯到其原始来源 episode。

### 任务结构

给系统一条长期记忆，然后问：

```text
你为什么认为用户不喜欢蓝色界面？
这条结论来自哪些历史经历？
```

### 期望

系统应该能返回：
- 支撑它的 episode
- 反证 episode
- 修订发生在哪次之后

### 核心指标

- `Provenance Recall`
- `Provenance Precision`
- `Version Chain Accuracy`

### 为什么重要

这是 reconsolidation 和普通 memory update 最大的区别之一。

没有这个任务，你的方法很容易退化成：

```text
只是更复杂的 update
```

---

## 任务 4：Stale Memory Suppression

### 测什么

测试系统在回答时，会不会继续调用已经被修订或退役的旧记忆。

### 任务结构

先让系统经历：
- 旧记忆形成
- 新证据修订

然后提问：

```text
用户现在偏好什么？
```

### 期望

系统不应该：
- 同时引用新旧冲突结论
- 默认使用旧版本

### 核心指标

- `Active-Version Retrieval Rate`
- `Retired-Memory Leakage Rate`
- `Response Consistency`

---

## 任务 5：Schema Revision

### 测什么

测试更高层 schema 在新 evidence 出现后，能不能被修订。

这比单条事实更新更难。

### 任务结构

#### Stage A

多次 episode 诱导系统形成 schema：

```text
- 用户多次选清淡食物
- 用户说不喜欢重口味
- 用户常点日料和沙拉
```

系统形成：

```text
“用户偏好清淡饮食”
```

#### Stage B

之后给反例或新模式：

```text
- 最近开始频繁吃火锅和烧烤
- 用户说冬天更偏好重口味食物
```

### 期望

系统能把旧 schema 从：

```text
全年稳定偏好
```

修订为：

```text
存在季节条件的偏好
```

### 核心指标

- `Schema Revision Accuracy`
- `Condition-Aware Abstraction`
- `Schema Staleness`

---

## 二、这些任务应该怎么组织数据

最稳的做法不是完全从零造 benchmark，而是：

```text
已有长对话 benchmark + 合成 reconsolidation 子任务
```

### 数据来源建议

#### 来源 1：LoCoMo

优点：
- 对话长
- 多事件
- 适合构造 delayed contradiction

#### 来源 2：LongMemEval

优点：
- 多 session
- 本来就有 update / temporal 类问题

#### 来源 3：合成数据

优点：
- 可精准控制：
  - 何时形成旧记忆
  - 何时出现反证
  - 何时需要 split / revise

---

## 三、建议的评测指标

这里给一版比较实用的指标集合。

## 3.1 主指标

### Revision Accuracy

定义：

```text
被正确修订的长期记忆数 / 应被修订的长期记忆数
```

### Stale Memory Rate

定义：

```text
回答或检索中仍使用旧错误版本的比例
```

### Traceability Score

定义：

```text
抽象记忆能否正确追溯其支持 episode 和反证 episode
```

### Split Correctness

定义：

```text
需要拆分的粗抽象中，被正确拆开的比例
```

### Active-Version Retrieval Rate

定义：

```text
检索时命中当前有效版本的比例
```

---

## 3.2 辅助指标

- `Retention`
- `Compression`
- `Consistency`
- `Response QA Accuracy`
- `Version Depth`
- `Revision Latency`

这些指标不是 reconsolidation 独有，但可以帮助补充说明。

---

## 四、baseline 该怎么测才公平

对同一个任务，baseline 的表现大概会是这样：

### No Consolidation

- retention 可能高
- stale memory 很严重
- contradiction 多

### Rule-based Consolidation

- 能去掉部分冗余
- 但 revision 常不稳定

### TiMem / LightMem / SimpleMem / PREMem

它们可能在：
- 普通 QA
- 压缩效率
- 层级组织

上表现很好。

但在下面这些任务上未必天然占优：
- delayed contradiction
- provenance tracing
- split correctness
- stale memory suppression

这正是你应该主打的战场。

---

## 五、一个最小实验表长什么样

### 表 1：Reconsolidation 核心任务

| 方法 | Revision Acc | Stale Rate | Traceability | Split Corr | Active-Version Retrieval |
|------|--------------|------------|--------------|------------|--------------------------|
| No Consolidation |  |  |  |  |  |
| Rule-based |  |  |  |  |  |
| TiMem |  |  |  |  |  |
| LightMem |  |  |  |  |  |
| PREMem |  |  |  |  |  |
| SimpleMem |  |  |  |  |  |
| FadeMem |  |  |  |  |  |
| Ours |  |  |  |  |  |

### 表 2：传统 benchmark 补充结果

| 方法 | LoCoMo | LongMemEval | Compression | Cost |
|------|--------|-------------|-------------|------|
| ...  |        |             |             |      |

这样你的论文就不会变成“只会做新指标，不会做传统任务”，也不会反过来只剩普通 QA。

---

## 六、评测设计里的一个关键原则

不要要求你的方法在所有任务上都绝对最强。

更合理的预期是：

```text
我们的 reconsolidation 方法，
在需要长期修订、抑制旧错误记忆、追踪抽象来源的任务上显著更强；
在普通事实问答上，至少不明显退化。
```

这个目标更现实，也更符合你的方法定位。

---

## 七、最小结论

如果把这份文件压成一句话，那就是：

**Reconsolidation 的评测重点，不是“记住没”，而是“记错以后能不能改，而且改完以后还能说清楚为什么这样改”。**

