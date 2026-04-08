# 记忆巩固方向：Prototype 实现计划

## 目标

这份文档不讨论“论文故事”，只讨论：

**第一版 prototype 到底怎么做，做到什么程度就足够支撑论文早期实验。**

原则只有一个：

**先做能验证论文假设的最小系统，不做过早复杂化。**

---

## 一、第一版 prototype 的范围

第一版只实现 reconsolidation 最核心的 5 个能力：

1. episode-level evidence 构建
2. 长期记忆版本化存储
3. 候选旧记忆检索
4. reconsolidation 操作决策
5. 检索阶段抑制旧版本

第一版**不做**：
- RL
- 多模态
- 图神经网络
- 大规模训练
- 超复杂 scheduler

---

## 二、最小系统架构

```text
raw dialogue
  -> Episode Builder
  -> Candidate Retriever
  -> Relation Judge
  -> Operation Mapper
  -> Versioned Memory Store
  -> Retrieval-Time Resolver
```

这 6 个模块已经足够验证核心问题。

---

## 三、模块级落地

## 模块 1：Episode Builder

### 第一版做法

用轻量规则 + LLM 抽取：
- 每轮对话或每几轮合成一个 episode
- 提取：
  - content
  - entities
  - time
  - session_id
  - raw_span

### 输出格式

```json
{
  "episode_id": "e_0012",
  "content": "用户表示现在不喜欢蓝色界面，因为会想到旧系统。",
  "entities": ["用户", "蓝色界面", "旧系统"],
  "session_id": "s_04",
  "timestamp": "2026-04-08T10:20:00",
  "raw_span": [15, 18]
}
```

### 工程优先级

`P0`

---

## 模块 2：Versioned Memory Store

### 第一版做法

先不引入复杂数据库，直接：
- `SQLite + JSON` 或
- `JSONL + FAISS/Chroma`

长期记忆对象保留：
- memory_id
- version
- status
- memory_text
- provenance_set
- support_set
- contradiction_set
- revision_history

### 工程优先级

`P0`

---

## 模块 3：Candidate Retriever

### 第一版做法

采用混合召回：
- embedding similarity
- entity overlap
- lexical overlap

召回 top-k 候选旧记忆供后续判断。

### 为什么先这样做

因为你的论文关键不在 retriever 创新，
而在 reconsolidation 决策本身。

### 工程优先级

`P0`

---

## 模块 4：Relation Judge

### 第一版做法

先让 LLM 判断：

```text
NEW
SUPPORT
REFINE
CONTRADICT
OVERGENERALIZED
UNRELATED
```

输入：
- 新 episode
- 候选旧长期记忆
- 简短上下文

输出：
- 关系标签
- 简短解释

### 为什么它是第一版核心

这一步决定你是不是在做真正的 reconsolidation。

### 工程优先级

`P0`

---

## 模块 5：Operation Mapper

### 第一版做法

把关系标签映射到操作：

| Relation | Operation |
|----------|-----------|
| NEW | ADD |
| SUPPORT | update support_set |
| REFINE | REVISE |
| CONTRADICT | REVISE 或 RETIRE |
| OVERGENERALIZED | SPLIT |
| UNRELATED | NOOP |

### 后续可升级

第二版再考虑：
- learned controller
- uncertainty-aware decision

### 工程优先级

`P0`

---

## 模块 6：Retrieval-Time Resolver

### 第一版做法

回答问题时：
- 默认只检索 `status=active`
- 如果需要解释，再附带 provenance 和 revision history

### 工程优先级

`P1`

---

## 四、推荐技术栈

### 存储

- `SQLite`：版本化元数据
- `Chroma / FAISS`：向量检索

### LLM

第一版直接用现成 API 或强模型作为 judge：
- GPT-4o / Claude / Qwen API

### Embedding

- `text-embedding-3-large`
- 或开源 `bge-m3`

### 开发语言

- `Python`

### 数据格式

- `jsonl` for episodes
- `sqlite` for long-term memory objects

---

## 五、建议的目录结构

如果后面要开始写代码，建议新增：

```text
prototype/
├── data/
│   ├── raw/
│   ├── processed/
│   └── eval/
├── reconsolidation/
│   ├── episode_builder.py
│   ├── retriever.py
│   ├── relation_judge.py
│   ├── operation_mapper.py
│   ├── memory_store.py
│   └── resolver.py
├── scripts/
│   ├── build_dataset.py
│   ├── run_reconsolidation.py
│   └── evaluate.py
└── notebooks/
```

---

## 六、最小实验闭环

第一版 prototype 只需要跑通下面这个闭环：

### Step 1

准备小规模数据：
- 50-100 条多 session 对话
- 手工或半自动构造 delayed contradiction / refinement case

### Step 2

抽取 episode

### Step 3

形成初始长期记忆

### Step 4

喂入新证据，触发 reconsolidation

### Step 5

问：
- 用户现在偏好什么
- 为什么这么认为
- 哪条旧记忆已失效

### Step 6

记录指标：
- revision accuracy
- stale memory rate
- provenance traceability

只要这个闭环跑通，就已经足够支撑第一轮论文实验。

---

## 七、里程碑拆分

### Milestone 1：数据对象和存储打通

完成：
- episode schema
- memory object schema
- sqlite / json 存储

产出：
- 可读写版本化长期记忆库

### Milestone 2：关系判断和操作执行打通

完成：
- relation judge
- operation mapper
- revise / split / retire 执行逻辑

产出：
- reconsolidation 主循环可运行

### Milestone 3：评测闭环跑通

完成：
- delayed contradiction mini-set
- provenance tracing mini-set
- 指标脚本

产出：
- 第一轮结果表

### Milestone 4：基线对比

完成：
- no consolidation
- rule-based consolidation
- recursive summarization

产出：
- 论文早期对比结果

---

## 八、第一版最容易踩的坑

### 坑 1：一开始就试图做太强的全自动系统

解决：
- 先 rule-based + LLM judge

### 坑 2：把 update 和 reconsolidation 混掉

解决：
- 明确要求支持：
  - version chain
  - provenance
  - split / retire

### 坑 3：只看普通 QA

解决：
- 第一版就必须有：
  - delayed contradiction
  - provenance tracing

### 坑 4：把 retriever 做成主战场

解决：
- 先用简单混合召回
- 把创新预算留给 reconsolidation 本身

---

## 九、最小成功标准

第一版 prototype 不需要证明“全面最强”。

只要做到下面 4 条，就算成功：

1. 能维护版本化长期记忆
2. 能在延迟反证下正确修订旧记忆
3. 能追溯抽象记忆来源
4. 在 stale-memory suppression 上优于 no consolidation / rule-based baseline

---

## 十、一句话收束

Prototype 第一版的目标不是做一个完整产品，
而是做出一个足以证明下面这句话的系统：

**长期记忆如果被当成可修订对象来管理，会比“一次整理后静态存储”更稳定。**

