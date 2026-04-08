# 记忆巩固方向：开题汇报草案

## 题目暂定

`Provenance-Preserving Reconsolidation for Long-Term Memory in LLM Agents`

中文可表述为：

**面向 LLM Agent 长期记忆的可追溯重巩固机制研究**

---

## 1. 研究背景

当前 LLM Agent 的长期记忆研究已经从“能不能记”发展到“怎么记得更高效、更稳定”。

近两年代表性工作表明，研究重点正在快速演化：

- `TiMem` 强调时间层级巩固
- `LightMem` 强调 sleep-time 离线长期更新
- `PREMem` 强调存前推理
- `SimpleMem` 强调在线语义综合
- `FadeMem` 强调融合、冲突消解和遗忘

这说明“memory consolidation”本身已经不是空白方向。

但现有方法大多默认：

```text
记忆整理完成一次后，长期记忆就基本定型
```

这和真实长期记忆系统不一致。

在真实场景中，后续会不断出现：
- 新证据
- 冲突证据
- 更细条件
- 更高层解释

如果系统不能重新打开并修订旧长期记忆，就会积累：
- 过时记忆
- 错误抽象
- 长期冲突

因此，当前更值得推进的问题不是“再做一个 consolidation framework”，
而是：

**长期记忆在抽象形成之后，如何被可追溯地重新修订。**

这就是本课题关注的 `reconsolidation`。

---

## 2. 研究问题

本研究聚焦如下核心问题：

```text
当系统已经将多个 episode 巩固成长期记忆后，
若后续出现补充、反证或更细限定，
系统能否对已有长期记忆进行可追溯的修订，而不是简单追加？
```

具体研究 4 个子问题：

1. 新证据在什么条件下应触发 `reconsolidation`
2. 旧长期记忆应执行 `ADD / REVISE / SPLIT / MERGE / RETIRE / NOOP` 中哪种操作
3. 修订后的长期记忆如何保留 `provenance` 和 `revision history`
4. 检索阶段如何抑制旧版本，优先使用当前有效版本

---

## 3. 研究目标

本课题的目标不是单纯提升普通 QA 分数，
而是构建一个：

**可修订、可追溯、可版本化的长期记忆机制。**

目标拆解为：

### 目标 1：定义 reconsolidation 问题

把它从一般 memory update 中区分出来。

### 目标 2：提出可追溯 reconsolidation 框架

让长期记忆对象支持：
- provenance tracking
- support / contradiction evidence
- revision history

### 目标 3：设计评测任务

重点测：
- delayed contradiction
- stale memory suppression
- provenance tracing
- over-abstraction repair

### 目标 4：验证其相对现有工作的优势

尤其是在：
- 修订准确率
- 长期一致性
- 过时记忆抑制
- 抽象记忆可解释性

这些维度上取得明显提升。

---

## 4. 研究意义

## 4.1 理论意义

本研究把长期记忆从“静态条目集合”推进为“可演化对象集合”。

它与认知科学中的以下机制更一致：
- memory reconsolidation
- schema revision
- systems consolidation 后的再更新

因此它不是纯工程优化，而是对类人记忆建模的一步推进。

## 4.2 方法意义

现有方法主要研究：
- 写入
- 压缩
- 检索
- 遗忘

本研究进一步引入：
- 版本化长期记忆
- 基于证据的修订
- 抽象记忆的可追溯性

## 4.3 应用意义

对长期运行的 assistant / agent 来说，
这类机制有助于减少：
- 过时用户画像
- 错误偏好记忆
- 冲突长期知识
- 无法解释“为什么记成这样”的问题

---

## 5. 国内外研究现状

### 5.1 直接相关工作

#### TiMem

优点：
- 时间层级巩固
- 多粒度抽象

不足：
- 更关注层级组织，不关注后续修订和版本追踪

#### LightMem

优点：
- sleep-time 长期更新
- 高效率

不足：
- 更关注离线更新和成本，不关注抽象后的 revision

#### PREMem

优点：
- 存前推理
- 跨 session 关系建模

不足：
- 更接近 pre-storage reasoning，而非 post-storage reconsolidation

#### SimpleMem

优点：
- 在线语义综合
- 结构化压缩

不足：
- 更关注写入时高密度整合，不关注版本化长期修订

#### FadeMem

优点：
- 融合
- 冲突消解
- 遗忘

不足：
- 更接近 forgetting-aware fusion，不是系统性的 reconsolidation

### 5.2 当前缺口

现有工作尚未系统解决：

1. 抽象长期记忆如何被后续证据修订
2. 修订后的长期记忆如何保留版本链
3. 检索时如何抑制退役旧版本
4. 如何专门评测 reconsolidation，而非只测普通 QA

---

## 6. 核心思路

本课题拟提出一个 `provenance-preserving reconsolidation framework`。

核心对象不是普通 memory entry，而是：

```text
带 provenance、support、contradiction、revision_history 的长期记忆对象
```

系统流程包括：

1. 将新交互整理为 episode-level evidence
2. 检索可能受影响的旧长期记忆
3. 判断关系类型：
   - new
   - support
   - refine
   - contradict
   - over-generalized
4. 映射为结构性操作：
   - ADD
   - REVISE
   - SPLIT
   - MERGE
   - RETIRE
5. 维护长期记忆版本链
6. 在检索时优先激活当前有效版本

---

## 7. 方法创新点

本研究预期创新点包括：

### 创新点 1：问题定义创新

明确提出 `reconsolidation` 作为独立研究问题，
而不是普通 memory update 的附属过程。

### 创新点 2：长期记忆表示创新

提出带有：
- provenance_set
- support_set
- contradiction_set
- revision_history

的长期记忆对象。

### 创新点 3：结构性修订操作

不再只做追加或覆盖，而是引入：
- revise
- split
- retire

等更符合长期记忆演化的操作。

### 创新点 4：评测创新

设计专门针对 reconsolidation 的任务和指标。

---

## 8. 实验设计

### 8.1 评测任务

重点设计以下任务：

1. `Delayed Contradiction`
2. `Refinement After Over-Abstraction`
3. `Provenance Tracing`
4. `Stale Memory Suppression`
5. `Schema Revision`

### 8.2 评测指标

核心指标：
- Revision Accuracy
- Stale Memory Rate
- Traceability Score
- Split Correctness
- Active-Version Retrieval Rate

辅助指标：
- QA Accuracy
- Compression
- Consistency
- Retrieval Cost

### 8.3 对比方法

直接或间接对比：
- No Consolidation
- Rule-based Consolidation
- Recursive Summarization
- TiMem
- LightMem
- PREMem
- SimpleMem
- FadeMem

---

## 9. 可行性分析

### 可行性 1：文献基础已经具备

当前已经完成：
- 直接竞争工作拆解
- 不撞车题目收敛
- 问题定义
- 方法骨架
- 评测骨架

### 可行性 2：问题可以先做最小版本

第一版可以采用：
- rule-based candidate retrieval
- LLM-based relation judge
- versioned memory store

不需要一开始就引入复杂 RL 或大规模训练。

### 可行性 3：有现成 benchmark 可借用

可以利用：
- LoCoMo
- LongMemEval

并在其基础上构造 reconsolidation-specific 子任务。

---

## 10. 研究计划

### 阶段 1：补齐问题和方法细化

输出：
- formal problem formulation
- operation definition
- memory object schema

### 阶段 2：构建评测任务

输出：
- delayed contradiction set
- provenance tracing set
- stale-memory suppression set

### 阶段 3：实现 prototype

输出：
- episode builder
- versioned memory store
- reconsolidation controller
- retrieval-time resolver

### 阶段 4：实验与分析

输出：
- 主实验
- 消融实验
- 失败案例分析

### 阶段 5：论文写作

输出：
- 开题报告
- 论文初稿

---

## 11. 风险与应对

### 风险 1：问题容易被误解成普通 update

应对：
- 强调结构性重写
- 强调 provenance 和 version history

### 风险 2：普通 QA 提升不明显

应对：
- 主打 reconsolidation-specific 指标
- 明确方法定位不是所有任务通吃

### 风险 3：方法过重

应对：
- 先做最小 rule-based + LLM judge 版本
- 学习型策略后置

---

## 12. 预期结论

本研究预期证明：

1. 长期记忆不应被建模为一次性定型对象
2. `reconsolidation` 是长期 memory system 的必要能力
3. 引入 provenance-preserving revision 机制后，
   系统在长期一致性、错误修订和旧记忆抑制上优于单次 consolidation 方法

---

## 一句话收束

本课题不是再做一个“会整理记忆”的系统，
而是推动长期记忆研究从：

**“整理一次”**

走向：

**“整理后仍可修订，并且修订过程可追溯”**

