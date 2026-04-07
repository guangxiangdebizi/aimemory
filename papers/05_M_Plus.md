# M+: Extending MemoryLLM with Scalable Long-Term Memory

## 基本信息

| 项目 | 内容 |
|------|------|
| **Venue** | ICML 2025 (Poster) |
| **作者** | Yu Wang, Dmitry Krotov, Yuanzhe Hu 等 |
| **机构** | UC San Diego, IBM Research |
| **论文** | https://proceedings.mlr.press/v267/wang25au.html |
| **代码** | https://github.com/wangyu-ustc/MemoryLLM |

## 为什么这篇重要

这篇本质上是在回答 MEMORYLLM 最大的现实问题：
**如果 memory pool 迟早会被覆盖，那“长期记忆”到底怎么保住？**

M+ 的答案不是把 memory pool 再做大，而是把原来的随机丢弃 token
转存成一个**长期 latent memory**，再用一个专门训练过的检索器把它们拉回来。

所以它不是纯参数内记忆，也不是传统 RAG，
而是一个很明确的**“短期 latent pool + 长期 latent cache + 协同检索”**混合方案。

## 核心架构（原文技术细节）

### 1. 长期记忆结构：把被丢掉的 memory token 存起来

M+ 保留了 MEMORYLLM 原来的短期记忆池 `θ`，并新增长期记忆 `Θ`：

```text
short-term memory: θ = {θ_l}
long-term memory:  Θ = {Θ_l}
```

关键点：
- `Θ` 也是**按层存储**
- 每层长期记忆大小是可变的，但论文实现里设置了最大容量 **M = 150k**
- 原来 MEMORYLLM 在 update 时会随机丢掉 `K` 个 token
- M+ 不再直接丢弃，而是把这些被挤出的 token 写入 `Θ_l`

### 2. 与原 latent pool 的交互方式

#### Update 阶段

在短期 memory pool `θ_l` 更新时：
- 随机从 `θ_l` 中丢出 `K` 个 token
- 这些 token **不再销毁**，而是写入 `Θ_l`
- 新生成的 `K` 个 token 回填到短期池里

长期记忆里的每个 token 都附带一个 **age**，
这样在后续取回时可以按时间顺序重排。

当长期记忆达到上限 `M` 时：
- 删除 **age 最大** 的 token
- 也就是先淘汰最旧的长期 latent memory

#### Generation 阶段

生成时，在每一层都会：
- 从 `Θ_l` 中检索出 `K'` 个长期记忆 token
- 按 age 排序
- 与当前短期记忆 `θ_l` 拼接
- 一起被 query hidden states 通过 cross-attention 访问

论文 Stage 3 的配置是：

```text
短期记忆 θ_l      = 10,240 tokens
检索出的长期记忆   = 2,560 tokens
总 memory tokens   = 12,800
```

也就是说，它不是把总 memory 再做大，
而是在**固定 memory budget** 下，把一部分“短期 slot”替换成“按需取回的长期 slot”。

### 3. Co-trained Retriever：检索 hidden state，而不是检索文本块

M+ 的检索器不是 BM25，也不是普通向量库，
而是直接对**long-term hidden states**做检索。

结构上有两个投影器：
- `f_q`：query projector
- `f_k`：key projector

二者都是 **两层 MLP**。

做法：
- token 从 `θ_l` 被丢进 `Θ_l` 时，先经过 `f_k`，得到一个低维 key 向量
- 生成时，对当前 query hidden state 经过 `f_q`
- 用 `dot product(q, k)` 在 `Θ_l` 里找相关长期记忆

这比 KV-cache 系方法更关键的一点是：
**M+ 只需要每层做一次检索，而不是每个 head / 每层各检一次。**

### 4. Retriever 的训练目标

论文明确给了对比式目标。

先把文档切成 `x1, x2, ..., xn`：
- 把 `x1...x_{n-1}` 注入短期记忆
- 跟这些 chunk 相关的 memory token 记为 `θ+`
- 无关 token 记为 `θ-`
- 再对最后一个 chunk `x_n` 做前向，得到 hidden state `h_n`

训练目标：

```text
min_{f_q, f_k}  -log(p+) - log(1 - p-)

p+ = <f_q(h_n), f_k(θ+)>
p- = <f_q(h_n), f_k(θ-)>
```

也就是：
- 拉近 `h_n` 与相关 memory token `θ+`
- 推远 `h_n` 与无关 memory token `θ-`

这就是“co-trained retriever”的核心，不是后挂的检索模块。

### 5. 训练策略：在原三阶段上加了长期记忆阶段

M+ 仍然延续 MEMORYLLM 的 staged training，但第三阶段专门让模型学会读长期记忆。

#### Stage 1
- 学短期 memory 的 update / generate 机制

#### Stage 2
- 用更长文档继续训练长上下文能力
- 论文强调这一阶段会显著提升 long-context modeling

#### Stage 3
- 从 Stage 2 checkpoint 继续训练
- 引入长期记忆 `Θ`
- 让模型适应“10,240 短期 + 2,560 长期检索”的 mixed memory 结构
- 数据来自 SlimPajama 长文档，且与 Stage 2 用的实例不重复

## 实验结果（关键数字）

### 长期保留能力

- 原版 MEMORYLLM 的有效保留区间约 **16k-20k tokens**
- M+ 将其扩展到 **160k+ tokens**

在 retrieval quality 分析里：
- 当注入 **160k** tokens 时，长期记忆实际增长到 **81,276** 个条目
- ground-truth token 的召回大约 **30%**
- 随机检索的理论召回只有 **3%**（`2560 / 81276`）

### GPU 显存成本

| 方法 | GPU Memory Cost |
|------|------------------|
| Llama-3.1-8B-SnapKV | 32,574 MB |
| Llama-3.2-3B-128k | 30,423 MB |
| M+ | 21,178 MB |
| Llama-3.1-8B-16k | 19,239 MB |
| **M+ (offload)** | **17,973 MB** |

这说明：
- M+ 比 SnapKV / 128k 长上下文模型便宜很多
- 长期记忆**不会额外抬高 GPU 成本**
- CPU offload 后甚至能低于 16k baseline

### 推理延迟

论文在单张 H100 上测了 128k 输入：
- M+ 比 MemoryLLM 慢，主要慢在 retrieval
- 但 **M+ (offload)** 相比 M+ 只多 **1 秒**
- 对应大约 **3%** 的额外计算时间

### 长上下文理解

在 LongBook-QA / LongBook Event QA 上：
- M+ 在只使用 **12,800 memory tokens + 2,048 generation window** 的情况下持续优于基线
- 说明它不是靠 brute-force 加上下文，而是靠更有效的 memory access

## 与本项目的关系

**直接相关度：⭐⭐⭐⭐⭐**

M+ 特别值得借鉴的，不只是“能存更多”，而是它证明了下面这条路线成立：

- 短期 memory 用内生 latent pool
- 长期 memory 用按层 latent cache
- 中间用一个和模型共同训练的检索器桥接

这几乎就是“内生记忆系统可扩展化”的第一版工程答案。

## 待深入的问题

- [x] 长期记忆机制怎么实现？→ 被短期池随机挤出的 token 写入按层长期记忆 `Θ`，生成时再检索回 `K'=2560` 个 token 拼接到短期池
- [x] co-trained retriever 的训练目标？→ 对 `θ+ / θ-` 做对比式训练，拉近相关 hidden state 与相关 memory token，推远无关 token
- [x] 160k 是硬上限还是实验上限？→ 论文实现里长期记忆上限设为 `M=150k` 条目，因此 160k+ 是当前配置下的验证区间，不是理论极限
- [ ] 能否加入显式遗忘机制？→ 目前长期记忆主要按 age 淘汰，没有像 FadeMem 那样的“重要性衰减”
