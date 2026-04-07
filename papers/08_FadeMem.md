# FadeMem: Biologically-Inspired Forgetting for Efficient Agent Memory

## 基本信息

| 项目 | 内容 |
|------|------|
| **状态** | arXiv 预印本（2026.01） |
| **作者** | Lei Wei, Xu Dong, Xiao Peng, Niantao Xie, Bin Wang |
| **机构** | 阿里巴巴国际数字商业、北京大学 |
| **arXiv** | https://arxiv.org/abs/2601.18642 |
| **代码** | https://github.com/ChihayaAine/FadeMem |

## 为什么这篇重要

MemoryBank 的遗忘主要是“时间过去了，强度下降”。

FadeMem 更进一步，把“该不该忘”拆成三个信号：
- 当前语义还重要吗
- 最近是不是经常被访问
- 它离现在已经多久了

所以它不只是艾宾浩斯曲线的工程版，而是一个**多因素、可迁移、可冲突处理**的 agent memory 方案。

## 核心机制（原文技术细节）

### 1. 双层记忆结构

每条记忆在时间 `t` 的表示为：

```text
m_i(t) = (c_i, s_i, v_i(t), τ_i, f_i)
```

其中：
- `c_i`：内容 embedding
- `s_i`：原始文本
- `v_i(t)`：当前记忆强度，范围 `[0, 1]`
- `τ_i`：创建时间
- `f_i`：访问频率

系统分成两层：
- **LML（Long-term Memory Layer）**
- **SML（Short-term Memory Layer）**

### 2. 三因素重要性分数

FadeMem 先算一条记忆的重要性 `I_i(t)`，再决定它该放哪层、忘多快：

```text
I_i(t) =
α * rel(c_i, Q_t) +
β * f_i / (1 + f_i) +
γ * recency(τ_i, t)
```

其中：
- `rel(c_i, Q_t)`：当前记忆与近期上下文 `Q_t` 的语义相关性
- `f_i / (1 + f_i)`：访问频率的饱和函数，避免“访问越多权重无限大”
- `recency(τ_i, t) = exp(-δ(t - τ_i))`

论文实现里又进一步把原始访问次数 `f_i` 替换成**时间衰减访问率**：

```text
f~_i = Σ_j exp(-κ (t - t_j))
```

也就是：
- 最近刚被访问的记忆更值钱
- 很久以前高频、但最近没用的记忆会自然降温

### 3. 记忆层迁移规则

```text
Layer(m_i) =
  LML, if I_i(t) >= θ_promote
  SML, if I_i(t) <  θ_demote
```

论文默认：
- `θ_promote = 0.7`
- `θ_demote = 0.3`

而且用了 hysteresis（`θ_promote > θ_demote`）避免记忆在两层之间来回抖动。

### 4. 生物启发遗忘曲线

记忆强度的衰减公式：

```text
v_i(t) = v_i(0) * exp(-λ_i * (t - τ_i)^β_i)
```

其中衰减率本身又受重要性调节：

```text
λ_i = λ_base * exp(-μ * I_i(t))
```

层级不同，衰减形状也不同：

```text
β_i = 0.8, if m_i in LML
β_i = 1.2, if m_i in SML
```

含义很直观：
- LML 是 **sub-linear decay**，忘得更慢、更平
- SML 是 **super-linear decay**，忘得更快

论文还给了 reinforcement 公式：

```text
v_i(t+) = v_i(t) + Δv * (1 - v_i(t)) * exp(-n_i / N)
```

即：
- 被重新访问时记忆会加强
- 但强化收益递减，符合 spacing effect

### 5. 半衰期是可解释的

在 `λ_base = 0.1` 且 `I_i(t) = 0` 的情况下，论文给出：
- **LML 半衰期约 11.25 天**
- **SML 半衰期约 5.02 天**

这已经不是“抽象遗忘”，而是能落到天级别时间常数。

### 6. 冲突消解：不是简单覆盖，而是四分类决策

对新记忆 `m_new`，先取语义相似集：

```text
S = {m_i : sim(c_new, c_i) > θ_sim}
```

然后让 LLM 判断与已有记忆的关系属于哪一种：
- **compatible**
- **contradictory**
- **subsumes**
- **subsumed**

不同类型对应不同更新：

#### Compatible

旧记忆保留，但因冗余被轻微降权：

```text
I_i = I_i * (1 - ω * sim(c_new, c_i))
```

#### Contradictory

更新型新信息会压制旧记忆：

```text
v_i(t) = v_i(t) * exp(-ρ * clip((τ_new - τ_i) / W_age, 0, 1))
```

#### Subsumes / Subsumed

通过 LLM 引导做合并，把更一般的记忆吸收更具体的记忆。

### 7. 记忆融合：不是摘要，而是带验证的聚类压缩

候选 cluster 的定义：

```text
C_k = {m_i : sim(c_i, c_k) > θ_fusion and |τ_i - τ_k| < T_window}
```

也就是必须同时满足：
- 语义相近
- 时间上接近

融合后的强度初始化：

```text
v_fused(0) = max_i v_i(t) + ε * var({v_i})
```

融合后的衰减还会变慢：

```text
ξ_fused = 1 / (1 + log |C_k|)
```

而且不是 LLM 说能融合就融合，论文还加了
**LLM verification + preservation threshold**
来检查信息是否真的保住，保不住就拒绝融合。

整个更新链写成：

```text
M_{t+Δt} = Fusion(Resolution(Decay(M_t, Δt) ∪ {m_new}))
```

## 实验结果（关键数字）

### LTI-Bench：遗忘和保留的平衡

| 方法 | Critical Facts | Contextual Info | Storage Used |
|------|----------------|-----------------|--------------|
| Fixed-16K | 50.2% | 44.8% | 100% |
| LangChain | 71.2% | 65.3% | 100% |
| Mem0 | 78.4% | 69.1% | 100% |
| MemGPT | 75.6% | 62.8% | 85.3% |
| **FadeMem** | **82.1%** | **71.0%** | **55.0%** |

重点结论：
- 关键事实保留率 **82.1%**
- 只用了 **55%** 存储
- 也就是实现了 **45% storage reduction**
- 高重要性记忆的衰减速度比 baseline 慢 **3-5x**
- 还有 **23%** 的低重要性记忆会因访问模式被提升到 LML

### 冲突消解（LTI-Bench，4075 个冲突）

| 方法 | Contradiction Acc/Cons | Update Acc/Cons | Overlap Acc/Cons |
|------|------------------------|-----------------|------------------|
| Mem0 | 62.3 / 71.4 | 84.7 / 82.3 | 45.6 / 73.8 |
| MemGPT | 58.7 / 68.9 | 81.2 / 79.6 | 51.3 / 75.4 |
| **FadeMem** | **66.2 / 78.0** | **87.1 / 86.5** | **53.4 / 76.8** |

论文还给了宏平均：
- **Macro Accuracy = 68.9%**
- **Macro Consistency = 80.4%**

### 跨数据集结果

| 方法 | MSC RP@10 | MSC TCS | LoCoMo F1 | LoCoMo FCR | SRR |
|------|-----------|---------|-----------|------------|-----|
| Fixed-16K | 58.7% | 0.71 | 5.17 | 78.9% | 0.00 |
| LangChain | 71.5% | 0.77 | 25.75 | 81.2% | 0.00 |
| Mem0 | 74.8% | 0.79 | 28.37 | 83.6% | 0.00 |
| MemGPT | 73.1% | 0.78 | 9.46 | 82.9% | 0.15 |
| **FadeMem** | **77.2%** | **0.82** | **29.43** | **85.9%** | **0.45** |

说明 FadeMem 不只是“省存储”，而是：
- 检索更准
- 时间一致性更强
- 多跳推理不降反升

## 实现配置（论文给的默认值）

- 冲突消解和融合模型：**GPT-4o-mini**
- embedding：**text-embedding-3-small**
- `λ_base = 0.1`
- `θ_promote = 0.7`
- `θ_demote = 0.3`
- `θ_fusion = 0.75`
- LML 最大容量：**1000**
- SML 最大容量：**500**

## 与本项目的关系

**相关度：⭐⭐⭐⭐**

FadeMem 最有价值的地方在于：它把“忘记”拆成了一个完整 pipeline，
而不是单独一条 decay 曲线。

它包含：
- importance scoring
- layer migration
- adaptive forgetting
- conflict resolution
- memory fusion

这五块组合起来，已经非常接近一个可运行的 agent forgetting layer。

## 待深入的问题

- [x] 三个衰减因素的权重怎么定？→ 通过验证集 grid search 选定，不是端到端可学习
- [x] 记忆融合怎么做？→ 先做时序-语义聚类，再让 GPT-4o-mini 做融合，并用 preservation threshold 验证信息是否保留
- [x] 冲突消解准确率？→ 宏平均 Acc 68.9%，Consistency 80.4%，其中 Update 类冲突最好（87.1 / 86.5）
- [ ] 和 MemoryBank 的直接对比？→ 论文主对比对象是 Mem0、MemGPT、LangChain，没有单独给出对 MemoryBank 的 head-to-head 实验
