# EpMAN: Episodic Memory AttentioN for Generalizing to Longer Contexts

## 基本信息

| 项目 | 内容 |
|------|------|
| **Venue** | ACL 2025 |
| **论文** | https://aclanthology.org/2025.acl-long.574/ |

## 为什么这篇重要

这篇和传统 RAG 最大的不同在于：
**它不是“检索后把内容塞回 prompt”，而是直接改 decoder 访问 KV cache 的方式。**

也就是说，记忆不是拼接到输入文本里，而是作为一种
**对原始 attention 的再加权机制**写进推理路径。

## 核心架构（原文技术细节）

### 1. Episodic Memory 的基本单元是 chunk，不是 token

EpMAN 把长上下文切成固定大小的 episodic entries。

论文实现里：
- 每个 entry = **256 tokens**
- 如果总长度为 `N`，则 chunk 数量为 `N_ep = N / 256`

先用一个 retriever / context encoder 对 chunk 做读写，
得到每个 chunk 的 episodic relevance 分数。

### 2. KV cache 重加权公式

核心不是重新生成上下文，而是用 chunk-level episodic attention 去重加权 decoder 对原始 KV cache 的访问。

论文给出的形式是：

```text
a_EpMAN = softmax(qK^T / √d_z) * (V * a_mem)
```

其中：
- `softmax(qK^T / √d_z)` 是标准 self-attention 分数
- `a_mem` 是 episodic attention
- `V * a_mem` 表示用 episodic 分数对 value 侧进行重加权

因为 `a_mem` 是 **chunk-level** 的，所以要先广播回 token 级。

如果一个 chunk 大小为 256，那么：

```text
a_mem[k*256 : (k+1)*256] = a_mem^chunk[k]
```

也就是：
- 先对 chunk 打分
- 再把 chunk 分数复制到该 chunk 内所有 token
- 最后用它去调制标准 attention

### 3. 训练时引入 noisy episodic attention，防止过拟合检索器

论文专门强调一点：
如果训练时永远把 top-K chunk 赋高权重，
decoder 会过拟合“检索器总是完美命中”的情况，
导致 OOD 长上下文泛化变差。

所以他们做了 **noisy training**：
- 训练时对 top-K chunk 的权重做随机扰动
- 实验中使用 **top-K = 5**
- 衰减斜率参数 **β = 0.2**
- 实际采用的采样区间是 **[1.0, 0.9]**

作用是：
- 让模型学会“主相关 chunk + 次相关 chunk”共同工作
- 不只依赖最相似的那一块

### 4. BroadAttn：推理时把相邻 chunk 一起带上

EpMAN 发现只看 top-K chunk 会出现信息截断问题：
- 主体在一个 chunk
- 属性、指代消解或后续描述在邻接 chunk

因此推理时提出 **BroadAttn**：
- 不只看 top-K chunk
- 还把这些 chunk 的**顺序邻居**一起纳入 attention

这比 NarrowAttn 更适合跨 chunk 的实体追踪和延迟共指。

### 5. 训练损失

训练时用了两部分 loss：

```text
L = E_D [ α log p(l | q, C) + log p(a | q, C, a_mem) ]
```

可理解为：
- 一部分让 episodic attention 学会定位相关 chunk
- 一部分是标准 next-token prediction

论文默认：
- `α = 0.1`

## 实验结果（关键数字）

### FactRecall-en

在 16k 到 256k 的长度范围里：
- `Dragon + Mistral-7B` 平均 recall = **71.7**
- `EpMAN (Noisy train + BroadAttn)` 平均 recall = **77.7**

而且在 256k 上仍能保持 **80.2**。

### MultiFieldQA-en-mixup

- `Dragon + Mistral-7B` 平均 = **69.7**
- `EpMAN (Noisy train + BroadAttn)` 平均 = **74.3**

### NITH / LooGLE 召回

简单 needle recall 任务上：
- `EpMAN (Uniform + BroadAttn)` 平均 = **78.6**
- `EpMAN (Noisy + BroadAttn)` 平均 = **75.9**

说明这种 attention-level coupling 对纯召回任务也稳定有效。

### top-K 选择

论文在 factrecall-en 上做了 top-K 消融：
- `top-K = 2` + noisy + BroadAttn：**83.2**
- `top-K = 3` + noisy + BroadAttn：**77.7**

也就是说，并不是 K 越大越好，
过多 chunk 反而会让 decoder 变“糊”。

## 计算开销（这是它和 RAG 最关键的现实问题）

论文专门测了 wall-clock：

| 方法 | 平均耗时 / sample |
|------|-------------------|
| DRAGON + baseline decoder | 1.76 s |
| **EpMAN (NarrowAttn)** | **1.45 s** |
| **EpMAN (BroadAttn)** | **2.17 s** |

作者的结论是：
- 额外的 noisy training 和 episodic reweighting 主要发生在**训练期**
- 推理期 NarrowAttn 和标准 RAG 基本同量级
- BroadAttn 稍慢，但不是数量级增加

## 与本项目的关系

**相关度：⭐⭐⭐⭐**

EpMAN 的真正价值不是“又一个长上下文技巧”，而是它给了一个方向：
**把 episodic retrieval 变成 attention bias，而不是 prompt 拼接。**

如果后面我们想做更内生的 episodic memory，
这类“KV cache 级再加权”会比传统 RAG 更接近目标。

## 待深入的问题

- [x] KV cache 重加权公式？→ 先得 chunk-level `a_mem`，再广播到 token 级，用它重加权标准 self-attention
- [x] 计算开销对比？→ NarrowAttn 平均 1.45s，baseline 1.76s，BroadAttn 2.17s，仍与 RAG 同量级
- [ ] 能否和 EM-LLM 的事件分割结合？→ 很自然，一个负责“怎么切事件”，一个负责“切完后怎么在 attention 层读取”
