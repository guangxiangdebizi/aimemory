# 当前进度总览

## 这个仓库现在在做什么

这个项目当前已经从“泛泛调研 LLM memory”推进到一个更明确的研究主线：

**围绕 `记忆巩固（consolidation）` 继续收敛，并进一步将核心论文问题锁定为 `provenance-preserving reconsolidation`。**

也就是：

- 不是只研究“怎么存记忆”
- 不是只研究“怎么检索记忆”
- 而是研究：

```text
已经被整理成长期记忆的内容，
在后续新证据到来后，
能不能被可追溯地修订、拆分、重写
```

---

## 为什么现在重点是 reconsolidation

因为 `consolidation` 本身已经不算空白。

当前直接竞争工作已经包括：
- TiMem
- LightMem
- PREMem
- SimpleMem
- FadeMem

所以现在如果还做：
- sleep-time consolidation
- temporal hierarchy
- pre-storage reasoning
- write-time synthesis

很容易和已有工作重叠。

因此项目已经明确把切口收缩为：

**`reconsolidation`：长期记忆在新证据下的可修订性。**

---

## 现在已经完成了什么

当前工作可以分成 3 层。

### 1. 研究问题层

已经完成：
- 论文池与认知架构梳理
- 记忆巩固方向筛选
- 直接竞争工作去重
- 不撞车题目收敛
- reconsolidation 正式问题定义

对应文档：
- [PROBLEM_STATEMENT.md](directions/consolidation/PROBLEM_STATEMENT.md)
- [DIRECT_COMPETITOR_COMPARISON.md](directions/consolidation/DIRECT_COMPETITOR_COMPARISON.md)
- [NON_OVERLAP_TOPIC_DRAFTS.md](directions/consolidation/NON_OVERLAP_TOPIC_DRAFTS.md)

### 2. 论文设计层

已经完成：
- 方法骨架
- 评测任务设计
- baseline / benchmark 梳理
- 开题汇报草案
- prototype 实现计划

对应文档：
- [METHOD_BLUEPRINT.md](directions/consolidation/METHOD_BLUEPRINT.md)
- [EVALUATION_TASKS.md](directions/consolidation/EVALUATION_TASKS.md)
- [BASELINE_AND_BENCHMARKS.md](directions/consolidation/BASELINE_AND_BENCHMARKS.md)
- [OPENING_REPORT.md](directions/consolidation/OPENING_REPORT.md)
- [IMPLEMENTATION_PLAN.md](directions/consolidation/IMPLEMENTATION_PLAN.md)

### 3. 原型系统层

已经完成：
- 第一版 `prototype/` 目录搭建
- episode-level evidence 构建
- versioned memory store
- candidate retriever
- relation judge（当前为轻量 heuristic 版本）
- operation mapper
- retrieval-time resolver
- 最小 demo 脚本

对应代码：
- [prototype/reconsolidation](prototype/reconsolidation)
- [run_reconsolidation.py](prototype/scripts/run_reconsolidation.py)
- [evaluate.py](prototype/scripts/evaluate.py)

---

## 当前 prototype 到什么程度了

当前原型已经可以跑通一个最小 reconsolidation 闭环：

1. 第 1 条证据进入长期记忆
2. 第 2 条证据触发 `REVISE`
3. 第 3 条证据再次触发 `REVISE`
4. 长期记忆保留版本链，只激活最新版本

当前验证结果表明：
- `active_count = 1`
- `revised_count = 2`

这说明第一版系统已经不是只会 `ADD`，
而是能表现出最基本的“长期记忆可修订”行为。

---

## 现在还没完成什么

虽然结构已经很完整，但仍然有几块关键部分还没做完。

### 1. judge 还只是原型级

当前 `relation_judge.py` 主要是 heuristic。

这适合：
- 跑通论文假设
- 验证数据结构是否合理

但还不适合：
- 做正式实验
- 做大规模评测

### 2. baseline 还没系统跑起来

目前还没有完整实现：
- No Consolidation
- Rule-based Consolidation
- Recursive Summarization baseline runner

### 3. 小评测集还太小

当前只有一个最小 `mini_reconsolidation_cases.jsonl`。

正式论文至少还需要：
- delayed contradiction 集合
- provenance tracing 集合
- refinement / split 集合

### 4. 还没有真正进入论文实验阶段

现在还在：
- 立题
- 搭骨架
- 做最小可运行原型

还没有到：
- 跑大 benchmark
- 做消融
- 出正式结果表

---

## 当前最核心的研究假设

项目现在实际在验证下面这个假设：

```text
如果把长期记忆建模成“可修订、可版本化、可追溯”的对象，
那么在延迟反证、抽象修正、旧记忆抑制这些任务上，
会优于只做单次 consolidation 的方法。
```

---

## 下一步会做什么

当前最合理的推进顺序是：

1. 把 `relation_judge` 改成可插拔接口
   目标：支持 heuristic / prompt / model judge 三种形式

2. 补一个小型评测集
   目标：覆盖
   - delayed contradiction
   - provenance tracing
   - over-abstraction refinement

3. 实现 3 个基础 baseline
   - No Consolidation
   - Rule-based Consolidation
   - Recursive Summarization

4. 跑第一轮对比实验
   目标不是全面最强，而是先验证：
   - revision accuracy
   - stale memory suppression
   - traceability

---

## 如果第一次进仓库，建议怎么读

### 如果你想先知道“现在研究问题是什么”

先读：
- [CURRENT_STATUS.md](CURRENT_STATUS.md)
- [PROBLEM_STATEMENT.md](directions/consolidation/PROBLEM_STATEMENT.md)

### 如果你想先知道“和别人差在哪”

先读：
- [DIRECT_COMPETITOR_COMPARISON.md](directions/consolidation/DIRECT_COMPETITOR_COMPARISON.md)
- [NON_OVERLAP_TOPIC_DRAFTS.md](directions/consolidation/NON_OVERLAP_TOPIC_DRAFTS.md)

### 如果你想先知道“准备怎么做”

先读：
- [METHOD_BLUEPRINT.md](directions/consolidation/METHOD_BLUEPRINT.md)
- [EVALUATION_TASKS.md](directions/consolidation/EVALUATION_TASKS.md)
- [IMPLEMENTATION_PLAN.md](directions/consolidation/IMPLEMENTATION_PLAN.md)

### 如果你想直接看代码

从这里开始：
- [prototype/README.md](prototype/README.md)
- [run_reconsolidation.py](prototype/scripts/run_reconsolidation.py)

---

## 一句话总结

这个项目当前不再是一个“LLM memory 资料仓库”，
而已经进入：

**围绕 `provenance-preserving reconsolidation` 立题、搭原型、准备实验的阶段。**

