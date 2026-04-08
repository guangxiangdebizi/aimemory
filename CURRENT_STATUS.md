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
- 可插拔 relation judge 接口（`heuristic / prompt_stub / llm`）
- operation mapper
- retrieval-time resolver
- shared reconsolidation pipeline
- 3 个基础 baseline runner
- 最小 demo 脚本
- 最小 case-based evaluation suite
- `.env` 驱动的本地凭证管理

对应代码：
- [prototype/reconsolidation](prototype/reconsolidation)
- [run_reconsolidation.py](prototype/scripts/run_reconsolidation.py)
- [run_baselines.py](prototype/scripts/run_baselines.py)
- [run_eval_suite.py](prototype/scripts/run_eval_suite.py)
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

另外，当前已经能在一个小型 case 集上批量跑：
- `ours`
- `no_consolidation`
- `rule_based`
- `recursive_summary`

第一轮最小结果显示：
- `ours` 在 `behavior_hit` 上明显高于基础 baseline
- 在真实 LLM judge 下，当前最小集上达到 `6/6`
- `provenance_hit` 也已经体现出差异
- 但 `memory_hit` 仍然过粗，目前还只是原型级指标

---

## 现在还没完成什么

虽然结构已经很完整，但仍然有几块关键部分还没做完。

### 1. judge 已能调用真实 LLM，但还需要系统化评估

当前已经有：
- heuristic judge
- prompt stub
- OpenAI-compatible `LLMRelationJudge`

并且已通过 `.env` 从本地读取凭证。

但还缺：
- judge 稳定性分析
- prompt 消融
- 对不同模型的对比

### 2. 小评测集还太小

当前虽然已经有一个最小 `mini_reconsolidation_cases.jsonl`，
并扩到了 6 个 case，但数量仍远远不够。

正式论文至少还需要：
- delayed contradiction 集合
- provenance tracing 集合
- refinement / split 集合
- stale suppression 集合
- schema revision 更大样本

### 3. 还没有真正进入论文实验阶段

现在还在：
- 立题
- 搭骨架
- 做最小可运行原型
- 跑小型 case-based 评测
- 跑第一轮真实 LLM judge 结果

还没有到：
- 跑大 benchmark
- 做消融
- 出更完整的正式结果表

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

1. 扩充小型评测集到 50-100 条
   目标：让当前评测从 smoke test 升级成可分析结果

2. 改进评测指标
   目标：把当前粗糙的 `memory_hit` 换成更合理的语义匹配或 judge-based 指标

3. 跑第一轮正式对比实验
   目标：把当前最小 eval suite 升级成可写进论文的结果表

4. 接入公开 benchmark 子集验证
   目标：证明在公开任务上不退化

5. 做 judge / prompt / operation 的消融
   目标：把方法从“能跑”推进到“能分析”

### 已完成的关键里程碑

- `LLMRelationJudge` 已实现并接通 Databricks OpenAI-compatible endpoint
- `.env` 管理已接通，凭证不再硬编码
- 第一轮真实 judge 的最小结果已经跑出

### 当前最需要补强的部分

- 评测集规模
- 指标可信度
- 结果表可读性
- benchmark 外部验证

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
