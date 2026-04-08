# 记忆巩固方向：Baseline 与 Benchmark 详细设计

## 先说一个现实判断

如果你现在做 consolidation 论文，最危险的不是“没 benchmark”，
而是：

**你选的 baseline 太弱，最后只是赢了几个过时方法。**

所以这个文件的目标是两件事：

1. 给出**应该优先对比的现有研究**
2. 区分哪些 benchmark 能测 consolidation，哪些只能间接测

---

## 一、Benchmark 应该怎么选

### 结论先行

目前**没有**一个被广泛接受、专门隔离测 `consolidation` 的标准 benchmark。

所以最稳妥的做法是：

```text
现有 benchmark 做下游验证
+ 自建 consolidation-specific 子任务做核心论证
```

---

## 二、推荐的 benchmark 组合

### B1. LongMemEval

| 项目 | 内容 |
|------|------|
| 论文 | LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory |
| Venue | ICLR 2025 |
| 适合度 | 很高 |
| 为什么重要 | 它显式覆盖 information extraction、multi-session reasoning、temporal reasoning、knowledge updates、abstention |

为什么适合 consolidation：
- 有 `knowledge update`
- 有 `temporal reasoning`
- 有多 session 结构

局限：
- 仍然主要测最终问答
- 不直接测“压缩后是否忠实”

### B2. LoCoMo

| 项目 | 内容 |
|------|------|
| 论文 | Evaluating Very Long-Term Conversational Memory of LLM Agents |
| Venue | ACL 2024 |
| 适合度 | 很高 |
| 为什么重要 | 目前最常见的长对话 memory benchmark，能测多跳、时间、对话长期一致性 |

为什么适合 consolidation：
- 长历史足够让“整理有没有用”体现出来
- 很适合看 episodic memory 的质量

局限：
- 本质上仍偏 downstream memory QA
- 不足以单独证明 consolidation 好

### B3. LoCoMo-Plus

| 项目 | 内容 |
|------|------|
| 论文 | LoCoMo-Plus: Beyond-Factual Cognitive Memory Evaluation Framework for LLM Agents |
| 时间 | arXiv 2026.02 |
| 适合度 | 中高 |
| 为什么重要 | 它开始测 latent constraints，不只测表层事实回忆 |

为什么适合 consolidation：
- 如果你的方法做 semantic abstraction，这个 benchmark 会更敏感

### B4. BEAM

| 项目 | 内容 |
|------|------|
| 论文 | Beyond a Million Tokens: Benchmarking and Enhancing Long-Term Memory in LLMs |
| 时间 | arXiv 2025.10 |
| 适合度 | 中 |
| 为什么重要 | 对极长上下文很有价值，适合测试压缩和巩固能否支撑更长尺度 |

为什么适合 consolidation：
- 如果你的方法强调“存储压缩后仍能保真”，BEAM 是很好的 stress test

---

## 三、现有 benchmark 覆盖不到什么

这部分正是你需要自建测试的理由。

现有 benchmark 很少直接测：

- 巩固后是否保留了所有关键源事实
- 抽象化是否可追溯到原始 episode
- 多条事件合并是否正确
- delayed contradiction 下旧记忆是否被正确重整
- episodic memory 是否成功转成 semantic / procedural memory

所以建议额外设计一组 `ConsolidBench` 子任务。

---

## 四、建议自建的 5 类 consolidation-specific 测试

### Task 1：Retention Under Compression

输入：
- 一批短期事件
- 其中包含可压缩冗余

目标：
- 巩固后存储更少
- 但关键事实仍能回答出来

核心指标：
- `Retention@Compression`

### Task 2：Conflict-Aware Reconsolidation

输入：
- 先给旧事件
- 再给延迟到来的新证据

目标：
- 测试系统会不会修正旧抽象记忆，而不只是继续追加

核心指标：
- `Revision Accuracy`
- `Stale Memory Rate`

### Task 3：Abstraction Faithfulness

输入：
- 多条具体 episode

目标：
- 看系统是否能产出高层抽象记忆
- 同时不胡编、不漏掉关键限制条件

核心指标：
- `Abstraction Faithfulness`
- `Detail Traceability`

### Task 4：Cross-Event Schema Induction

输入：
- 多次相似经历

目标：
- 看系统是否能从多个 episode 归纳出稳定 schema 或偏好规律

核心指标：
- `Schema Precision`
- `Schema Recall`

### Task 5：Proceduralization

输入：
- 多次问题解决 episode

目标：
- 看系统是否能把经历转成可复用 procedure / rule

核心指标：
- `Procedure Transfer Success`

---

## 五、baseline 不应该只放旧方法

建议把 baseline 分成 3 组，不然评审会说你挑软柿子捏。

### 组 1：经典弱 baseline

#### B0: No Consolidation

直接追加，不做整理。

作用：
- 下界

#### B1: Rule-based Consolidation

规则去重 + 时间分组 + LLM 摘要。

作用：
- 最朴素工程 baseline

#### B2: Recursive Summarization

按 session 或窗口递归产生摘要记忆。

作用：
- 历史强 baseline

---

### 组 2：最像 consolidation 的强 baseline

#### B3: PREMem

代表“把复杂 reasoning 前移到存储构建阶段”。

为什么必须比：
- 它已经开始占你的存储侧空间

#### B4: LightMem

代表：
- sensory filter
- short-term topic consolidation
- sleep-time long-term consolidation

为什么必须比：
- 它是最直接的 sleep-time consolidation 竞争者之一

#### B5: TiMem

代表：
- temporal-hierarchical consolidation
- 层级时间树

为什么必须比：
- 这是最像“系统化 consolidation 框架”的直接竞争对手

#### B6: SimpleMem

代表：
- semantic structured compression
- recursive consolidation

为什么必须比：
- 它已经把“异步递归整合”讲得很完整

#### B7: FadeMem

代表：
- 融合
- 冲突消解
- 双层迁移

为什么必须比：
- 它是最接近你已有材料库的强可复用 baseline

---

### 组 3：邻近强 baseline

#### B8: M+

代表短期到长期迁移，但不做真正整理。

作用：
- 证明“只迁移不巩固”不够

#### B9: Memory OS

代表层级存储与更新。

作用：
- 证明“只有 hierarchy 没有真正 consolidation”不够

#### B10: Mem0 / MemInsight / MemMachine

这组可以选 1-2 个有代码的系统作现实世界对照。

作用：
- 避免你的方法只对论文 baseline 有效，对工业 memory stack 无优势

---

## 六、推荐的主实验表结构

### 表 1：主结果

列：
- LongMemEval
- LoCoMo
- LoCoMo-Plus

行：
- B0 No Consolidation
- B1 Rule-based
- B2 Recursive Summarization
- B3 PREMem
- B4 LightMem
- B5 TiMem
- B6 SimpleMem
- B7 FadeMem
- B8 M+
- 你的方法

### 表 2：consolidation-specific 指标

列：
- Retention
- Compression
- Consistency
- Traceability
- Revision Accuracy
- Schema Induction

### 表 3：效率

列：
- ingestion cost
- consolidation cost
- retrieval latency
- token budget
- memory growth curve

---

## 七、如果代码拿不到，baseline 怎么办

这是很现实的问题。

建议分两层：

### 可完整复现层

- No Consolidation
- Rule-based
- Recursive Summarization
- FadeMem-style subset

### 论文结果对照层

- TiMem
- LightMem
- SimpleMem
- PREMem

写法上要诚实：

```text
我们对可复现 baseline 做统一环境复现；
对尚未开放完整实现的方法，报告原论文结果并做定性比较。
```

---

## 八、真正决定你论文是否成立的 4 个指标

如果只能盯最重要的 4 个，我建议是：

1. `Retention@FixedBudget`
2. `Revision Accuracy`
3. `Abstraction Faithfulness`
4. `Downstream QA / Multi-hop Gain`

因为这 4 个指标刚好对应 consolidation 的核心矛盾：
- 记住
- 压缩
- 修正
- 真能用

---

## 九、最后一句话

现在做 consolidation，baseline 不能再停留在：

**“不整理 / 简单摘要 / RAG”**

你必须把：
- TiMem
- LightMem
- SimpleMem
- PREMem
- FadeMem

至少作为**论文级比较对象**放进来，不然很容易被指出“没有和最直接相关工作比较”。

---

## 参考链接

- LongMemEval: https://arxiv.org/abs/2410.10813
- LoCoMo: https://aclanthology.org/2024.acl-long.747/
- LoCoMo-Plus: https://arxiv.org/abs/2602.10715
- BEAM: https://arxiv.org/abs/2510.27246
- PREMem: https://arxiv.org/abs/2509.10852
- LightMem: https://arxiv.org/abs/2510.18866
- TiMem: https://arxiv.org/abs/2601.02845
- SimpleMem: https://arxiv.org/abs/2601.02553
- FadeMem: https://arxiv.org/abs/2601.18642
- Memory OS: https://aclanthology.org/2025.emnlp-main.1318/
- Mem0: https://arxiv.org/abs/2504.19413
- MemInsight: https://aclanthology.org/2025.emnlp-main.1683/
- MemMachine: https://arxiv.org/abs/2604.04853
