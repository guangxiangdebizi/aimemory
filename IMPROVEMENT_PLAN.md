# 改进计划：从原型到论文实验

> 生成时间：2026-04-08
> 用途：直接交给 AI 对话作为行动指令

---

## 当前状态一句话

选题和设计文档已完备，原型可跑通最小闭环（ADD → REVISE → 版本链），但 **judge 是纯规则、评测集只有 6 条、没有可写进论文的实验结果**。

---

## 四个改进任务（按优先级排序）

### 任务 1：实现 LLM-based Relation Judge（最高优先级）

**为什么**：`relation_judge` 是系统心脏。当前 `HeuristicRelationJudge` 靠关键词匹配，只能跑通 demo，不能出论文结果。

**现状**：
- `prototype/reconsolidation/judges.py` 已有 `BaseRelationJudge` Protocol 和 `PromptStubRelationJudge` 占位
- `create_relation_judge()` 工厂函数已支持 mode 切换
- pipeline 已通过依赖注入接受 judge，改 judge 不需要改 pipeline

**要做的事**：
1. 在 `judges.py` 中新增 `LLMRelationJudge` 类，实现 `judge()` 方法
2. 调用 GPT-4o / Claude / Qwen API，输入 episode text + memory text
3. 输出 6 类标签之一：`NEW / SUPPORT / REFINE / CONTRADICT / OVERGENERALIZED / UNRELATED`
4. 用 few-shot prompt（3-5 个示例），不需要微调
5. 返回 `RelationDecision(relation=标签, explanation=LLM解释)`
6. 在 `create_relation_judge()` 中注册 `mode="llm"`
7. 在现有 6 条 case 上验证输出是否合理

**接口约束**（不要改）：
```python
class BaseRelationJudge(Protocol):
    def judge(self, episode: Episode, memory: MemoryVersion) -> RelationDecision: ...
```

**关键文件**：
- `prototype/reconsolidation/judges.py`（改这个）
- `prototype/reconsolidation/types.py`（Episode / MemoryVersion / RelationDecision 定义，只读参考）
- `prototype/reconsolidation/pipeline.py`（不需要改，已支持注入）

---

### 任务 2：扩充评测集到 50-100 条

**为什么**：当前 `mini_reconsolidation_cases.jsonl` 只有 6 条，统计上无意义，审稿人一看就拒。

**现状**：
- `prototype/scripts/build_dataset.py` 已能生成 4 类任务样例
- 4 类任务：`delayed_contradiction` / `refinement` / `provenance_tracing` / `schema_revision`
- 每条格式：`{case_id, task, expected_behavior, sessions, expected_active_memory}`

**要做的事**：
1. 每类任务扩充到 15-25 条，总计 60-100 条
2. 生成方式：用 LLM 批量生成草稿 → 人工审核过滤不合理的
3. 确保多样性：不同领域（饮食/工作/UI/社交/健康），不同矛盾强度
4. 新增 `stale_suppression` 任务类型（当前缺失），测试退役记忆是否泄漏
5. 输出到同一个 `data/eval/mini_reconsolidation_cases.jsonl`
6. 同步更新 `run_eval_suite.py` 中的 `_evaluate_case` 以支持新任务类型

**数据格式保持不变**：
```json
{
  "case_id": "delayed_contradiction_015",
  "task": "delayed_contradiction",
  "expected_behavior": "revise",
  "sessions": [["session1 turns..."], ["session2 turns..."]],
  "expected_active_memory": "期望的活跃记忆描述"
}
```

**关键文件**：
- `prototype/scripts/build_dataset.py`（改这个）
- `prototype/data/eval/mini_reconsolidation_cases.jsonl`（输出目标）
- `prototype/scripts/run_eval_suite.py`（可能需要小改以支持新任务类型）

---

### 任务 3：跑第一轮正式对比实验

**为什么**：这张结果表是论文命脉。没有它，方法到底行不行完全未知。

**前置条件**：任务 1（LLM judge）必须完成

**要做的事**：
1. 用 LLM judge 跑 4 种方法 × 全部评测集：
   - `ours`（ReconsolidationPipeline + LLM judge）
   - `no_consolidation`（全部 ADD，不合并）
   - `rule_based`（实体重叠规则合并）
   - `recursive_summary`（拼接摘要）
2. 计算 5 个核心指标：
   - **Revision Accuracy**：延迟反证后是否正确修订
   - **Stale Memory Rate**：检索结果中已退役记忆的比例
   - **Traceability Score**：活跃记忆是否保留来源 episode 链
   - **Split Correctness**：过度泛化是否被正确拆分
   - **Active-Version Retrieval Rate**：检索时是否优先返回最新版本
3. 输出第一张对比结果表（markdown 格式）
4. 分析结果，决定是调方法还是调评测

**关键文件**：
- `prototype/scripts/run_eval_suite.py`（主要改这个，补充指标计算）
- `prototype/reconsolidation/baselines.py`（3 个 baseline 已实现，检查是否需要调整）
- `prototype/reconsolidation/pipeline.py`（ours 方法，不需要改）

---

### 任务 4：接入公开 Benchmark 验证

**为什么**：只有自建评测集不够，需要在公开 benchmark 上证明"不退化"。

**前置条件**：任务 3 完成，自建评测集结果已出

**要做的事**：
1. 从 LoCoMo（ACL 2024）或 LongMemEval（ICLR 2025）中抽取子集
2. 筛选含知识更新/偏好变化的对话，构造 reconsolidation 测试场景
3. 跑 ours + baselines，补充一张"公开 benchmark 上不退化"的结果表
4. 重点证明：在需要修订的场景显著更强，在普通 QA 上至少持平

**关键参考**：
- `directions/consolidation/BASELINE_AND_BENCHMARKS.md`（已有详细 benchmark 分析）
- `directions/consolidation/EVALUATION_TASKS.md`（评测哲学和表结构设计）

---

## 关键原则

- **每天产出必须是代码或数据，不是文档**
- 任务 1 完成前不要碰任务 3
- 任务 2 可以和任务 1 并行
- 不要过早优化 retriever，创新预算留给 reconsolidation 本身
