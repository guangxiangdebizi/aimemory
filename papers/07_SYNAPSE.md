# SYNAPSE: Empowering LLM Agents with Episodic-Semantic Memory via Spreading Activation

## 基本信息

| 项目 | 内容 |
|------|------|
| **状态** | arXiv 预印本（2026.01） |
| **作者** | Hanqi Jiang, Junhao Chen, Yi Pan, Ling Chen 等 |
| **机构** | University of Georgia 等 |
| **arXiv** | https://arxiv.org/abs/2601.02744 |

## 为什么这篇重要

SYNAPSE 的核心不是“图检索”，而是把**检索本身**改写成一种认知动力学过程：
不是 top-k 命中，而是**激活、扩散、抑制、衰减**。

它试图解决两个向量检索的根本问题：
- **Contextual Tunneling**：只命中局部语义最像的点，跨跳关系丢失
- **Contextual Isolation**：不同时间和话题的记忆断开，无法联想式回忆

## 核心机制（原文技术细节）

### 1. 统一情景-语义图

SYNAPSE 把记忆组织为图 `G = (V, E)`，节点分成两类：

- **Episodic Nodes**
  - 表示一次具体交互
  - 形式为 `(c_i, h_i, τ_i)`
  - `c_i` 是文本内容
  - `h_i` 是 sentence encoder 产生的 embedding
  - `τ_i` 是时间戳

- **Semantic Nodes**
  - 表示抽象概念，如实体、偏好、主题
  - 每 **N = 5 turns** 触发一次 LLM 抽取

实现细节：
- episodic embedding 用 `all-MiniLM-L6-v2`
- semantic dedup 阈值 `τ_dup = 0.92`

### 2. 图怎么连边

图中有三类边：

1. **Temporal Edges**
   - 顺序连接相邻 episode
   - `v_t^e -> v_{t+1}^e`

2. **Abstraction Edges**
   - 把 episode 与窗口内抽出的 semantic concepts 双向连接
   - 形成“具体经历 -> 抽象概念”的桥梁

3. **Association Edges**
   - 连接 semantic node 之间的潜在相关性
   - 只保留高相似且进入 top-15 邻居的连接

论文附录里的增量构图算法里，Association Edge 的条件是：
- `sim(h_i, h_j) > 0.92`
- 且位于 `Top-15(N(i))`

### 3. 图的维护成本控制

论文没有回避扩图成本，而是明确加了约束：

- **每个节点最多保留 Top-15 incoming edges**
- 如果一个节点的激活长期低于 `ε = 0.01`
- 并持续 `W = 10` 个窗口
- 就归档到 disk

目标是把活跃图控制在：

```text
|V| <= 10,000
```

这就是它对“大图会不会爆”的第一层工程答案。

### 4. Spreading Activation 公式

#### 初始化：双触发锚点

query 进来后，不是只做 dense retrieval，而是先找 anchor set `T`：

- **Lexical Trigger**：BM25，抓显式实体
- **Semantic Trigger**：dense retrieval，抓概念相似

初始激活：

```text
a_i^(0) = α * sim(h_i, h_q),  if v_i in T
          0,                  otherwise
```

#### 扩散：考虑 fan effect

```text
u_i^(t+1) =
(1 - δ) a_i^(t) +
Σ_{j in N(i)} S * w_ji * a_j^(t) / fan(j)
```

其中：
- `S = 0.8` 是 spreading factor
- `fan(j) = deg_out(j)`，防止 hub 节点把激活泛滥传播
- 时间边权重：

```text
w_ji = exp(-ρ |τ_i - τ_j|)
```

- 论文默认 `ρ = 0.01`
- 语义边权重用 embedding similarity

#### 侧抑制（Lateral Inhibition）

高激活节点在 firing 前先压制竞争节点：

```text
û_i^(t+1) =
max(0, u_i^(t+1) - β * Σ competitor_gap)
```

默认只对 **M = 7** 个最高 potential 节点施加竞争。

#### 最终激活

```text
a_i^(t+1) = sigmoid(û_i^(t+1))
```

整个循环严格按：

```text
传播 -> 侧抑制 -> 非线性激活
```

论文说一般 **T = 3** 轮内就能稳定。

### 5. Triple Hybrid Retrieval

SYNAPSE 最终不是只看 activation score，而是三路融合：

1. 语义相似度
2. 扩散激活值
3. 结构化图信号

融合权重在主实验里设成：

```text
λ = {0.5, 0.3, 0.2}
```

分别对应：
- Semantic
- Activation
- Structural

## 实验结果（关键数字）

### LoCoMo 主结果（GPT-4o-mini）

| 方法 | Multi-Hop F1 | Temporal F1 | Open-Domain F1 | Single-Hop F1 | Adversarial F1 | Avg F1* |
|------|--------------|-------------|----------------|---------------|----------------|---------|
| A-Mem | 27.0 | 45.9 | 12.1 | 44.7 | 50.0 | 33.3 |
| Zep | 35.5 | 48.5 | 23.1 | 48.0 | 65.4 | 39.7 |
| **SYNAPSE** | **35.7** | **50.1** | **25.9** | **48.9** | **96.6** | **40.5** |

`Avg F1*` 按论文定义，不含 adversarial 类别。

最关键的亮点：
- **Temporal**：50.1，优于 A-Mem 的 45.9
- **Multi-Hop**：35.7，优于 A-Mem 的 27.0
- **Adversarial**：96.6，远高于 LoCoMo baseline 的 69.2

### 效率

| 方法 | Token / Query | Latency | Cost / 1k Queries | Avg F1* |
|------|----------------|---------|-------------------|---------|
| LoCoMo | ~16,910 | 8.2 s | $2.67 | 25.6 |
| MemGPT | ~16,977 | 8.5 s | $2.67 | 28.0 |
| MemoryOS | ~1,198 | 1.5 s | $0.30 | 38.0 |
| **SYNAPSE** | **~814** | **1.9 s** | **$0.24** | **40.5** |

结论很直接：
- 相比 full-context 方法，token 降了 **95%**
- 成本约便宜 **11x**
- 但 F1 反而更高

### 消融实验非常说明问题

论文里几个消融很有价值：
- 去掉 **Activation Dynamics**：平均 F1 从 **40.5 -> 30.5**
- 只用向量检索（Vectors Only）：掉到 **25.2**
- 去掉 **Node Decay**：Temporal F1 从 **50.1 -> 14.2**

这说明：
- 不是“有图就行”
- 也不是“有 embedding 就行”
- 真正起作用的是**动态图上的激活传播机制**

## 与本项目的关系

**相关度：⭐⭐⭐⭐**

如果我们的目标不是“把历史切块后 top-k 拼回来”，
而是做更像人类联想式回忆的系统，
SYNAPSE 是非常值得借鉴的路线：

- episodic node
- semantic node
- spreading activation
- lateral inhibition
- temporal decay

这五个组件拼起来，已经很像一个真正的动态记忆系统了。

## 待深入的问题

- [x] 图的构建和维护成本？→ 每 5 turns 做一次概念抽取，边限制为 top-15，低激活节点归档，活跃图控制在 10k 节点内
- [x] 扩散激活怎么做？→ 双触发初始化 + fan-effect 传播 + 侧抑制 + sigmoid 激活，默认 3 轮收敛
- [x] 侧抑制参数怎么调？→ 论文主配置使用 `M=7` 个竞争节点；消融显示去掉 inhibition 会明显放大 hallucination candidate
- [ ] 能否和 EM-LLM 的事件分割结合？→ 很可能可行，EM-LLM 负责把连续流切成事件，SYNAPSE 负责把事件组织成可激活图
