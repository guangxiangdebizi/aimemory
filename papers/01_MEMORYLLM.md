# MEMORYLLM: Towards Self-Updatable Large Language Models

> 核对状态：已按论文 PDF 复核（2026-04-07）。

## 基本信息

| 项目 | 内容 |
|------|------|
| **Venue** | ICML 2024（PMLR 235） |
| **作者** | Yu Wang, Yifan Gao, Xiusi Chen, Haoming Jiang, Shiyang Li, Jingfeng Yang, Qingyu Yin, Zheng Li, Xian Li, Bing Yin, Jingbo Shang, Julian McAuley |
| **机构** | UC San Diego, Amazon, UCLA |
| **论文** | https://arxiv.org/abs/2402.04624 |
| **PDF** | https://arxiv.org/pdf/2402.04624.pdf |
| **本地 PDF** | [01_MEMORYLLM.pdf](../_tmp_pdfs/01_MEMORYLLM.pdf) |
| **本地抽取文本** | [01_MEMORYLLM.txt](../_tmp_txt/01_MEMORYLLM.txt) |
| **代码** | https://github.com/wangyu-ustc/MemoryLLM |
| **论文主干模型** | 基于 Llama2-7B；论文主体实验围绕 MemoryLLM-7B 展开 |

## 为什么这篇重要

**这是“模型内生记忆”路线最有代表性的正式顶会工作之一。**

它不是在模型外接一个向量库，而是直接把一个大规模、固定大小的 memory pool 嵌进 Transformer 的 latent space，
让模型在推理阶段通过前向传播把新知识写进记忆池。

对我们关心的问题来说，这篇论文回答的是：

- 能不能让 LLM 在部署后继续“写入”
- 写入之后能不能保留旧知识，而不是立刻覆盖
- 不改主模型权重的前提下，能不能让“会记住”成为模型本体能力

## 核心架构（按原文）

模型由两部分组成：

- **静态参数 φ**：Transformer 主体参数，部署后不变
- **动态参数 θ**：跨层 memory pool，负责推理时持续写入

### 记忆池结构

论文把记忆池放在 **每一层 Transformer** 中：

```text
θ ∈ R^(L × N × d)
L = 32, N = 7680, d = 4096
总记忆参数量约为 1.066B
```

生成阶段，输入 token 会 attend 到该层全部 memory tokens。
如果当前输入长度为 `n_x`，则 attention map 形状为：

```text
n_x × (n_x + N)
```

因此对 memory pool 大小是**线性复杂度**。

### Self-Update 机制

当新知识 `x_c` 到来时，MEMORYLLM 用 Transformer 自身做写入，而不是梯度更新 memory 参数。

每层 `l` 的流程是：

1. 从当前记忆池 `θ_l` 中取最后 `K` 个 memory tokens，记为 `e_θ^l`
2. 将 `e_θ^l` 与该层输入隐状态 `h_l` 拼接，送入 `φ_l`
3. 输出 `h_(l+1)` 的最后 `K` 个 hidden states 作为新记忆 `e_θ'^l`
4. 从旧记忆池 `θ_l` 中**随机丢弃 K 个 tokens**
5. 将保留下来的旧记忆左移，再把 `e_θ'^l` 填到右侧，形成新的 `θ'_l`

关键点：

- 写入是**前向传播生成新记忆 token**
- 被更新的不是主模型权重，而是 memory pool 内容
- 真正参与 self-update 的只是最后 `K` 个 memory tokens，而不是整池 `N` 个

### 遗忘分析

论文明确把该机制和艾宾浩斯式指数遗忘联系起来。

每次更新随机丢弃 `K` 个 memory tokens，统计意义上相当于以 `K / N` 的比例遗忘旧知识。
如果一段知识在 `N / K` 次更新前被写入，那么其保留率近似为：

```text
(1 - K/N)^(N/K)
```

当 `N/K → ∞` 时：

```text
lim (1 - K/N)^(N/K) = 1/e ≈ 36.8%
```

这给出了论文想强调的两个结论：

- `N` 越大，记忆池越大，遗忘越慢
- `K` 越小，压缩越强，每次写入破坏越少，遗忘越慢

### 训练策略

论文训练分三阶段：

1. **新知识写入训练**
   用 `(x1, x2)` 切分文档，先用 `x1` 更新 memory，再用更新后的 memory 预测 `x2`
2. **连续上下文理解训练**
   把长文档切成多段，前 `n-1` 段依次写入，最后一段用于预测
3. **抗遗忘训练**
   交替注入主文档与干扰文档，最后要求模型回忆主文档信息

论文报告的训练资源是 **8 x A100-80GB，训练 3 天**。

## 实验结果（关键数字）

### 1. Model Editing

论文在 ZsRE 和 CounterFact 上报告的核心结果如下：

| 方法 | ZsRE Score | CounterFact Score |
|------|------------|-------------------|
| Llama2-7B | 55.6 | 20.7 |
| ROME | 69.3 | 69.2 |
| **MemoryLLM-7B (w/ EF)** | **79.2** | **75.3** |

其中 `w/ EF` 表示已经把编辑事实写入 memory pool 之后的模型。

更细一点看：

- ZsRE 上 Efficacy = **99.8**
- ZsRE 上 Generalization = **96.7**
- CounterFact 上 Efficacy = **98.5**
- CounterFact 上 Generalization = **82.2**

这说明它在“把新事实写进去”这件事上是很强的。

### 2. 长上下文与保留能力

在 LongBench 上，论文报告：

- 在 6 个数据集里有 **4 个**优于基线
- 随着上下文长度增加，MemoryLLM 性能还会继续上升
- `qasper` 上相对吃亏，作者明确归因于训练主要用 C4，没有覆盖 arXiv 风格科学文本

### 3. 运行稳定性

这里要说精确一点：

- **摘要**写的是“nearly a million memory updates”
- **主实验图 6** 实际展示的是 **650,000 次更新** 之后没有明显退化

所以更稳妥的表述应该是：

> 论文实证图里验证了 65 万次更新的稳定性，摘要把整体能力描述为接近百万次更新仍无明显退化。

### 4. 推理资源

论文明确写到：

- 对比 16k 长上下文基线，7B 模型在 8 x A100-80GB 上都会 OOM
- 而 MEMORYLLM 推理可用 **1 张 48GB GPU** 或 **2 张 40GB GPU**
- 且推理资源需求**不随输入长度线性爆炸**

## 关键局限

- **记忆容量固定**：memory pool 是固定大小，不能无限增长
- **随机丢弃不看重要性**：重要知识和普通知识被等概率淘汰
- **主实验围绕 7B**：论文不是在更大模型规模上系统验证的
- **科学文本适配弱点暴露**：`qasper` 结果说明训练分布会显著影响记忆效果
- **记忆是 latent 级而非显式文本级**：可解释性弱，不像外部 memory 那样能直接检查每条记忆内容

## 与本项目的关系

**直接相关度：⭐⭐⭐⭐⭐**

这篇对我们的价值在于：

- 它证明了“记忆可以是模型内部的动态状态，而不是外挂数据库”
- 它把“写入”和“遗忘”都做成了可分析的机制
- 它给了一个很强的对照面：如果我们以后做外部情景记忆系统，就要明确自己相对 MEMORYLLM 的收益到底在哪里

## 待深入的问题

- [x] 写入到底是不是梯度更新？→ **不是**，是前向传播生成新 memory tokens
- [x] 遗忘是不是有数学解释？→ **有**，论文明确给了指数衰减分析
- [x] “近百万次更新”是否在图里直接验证？→ **图里直接验证的是 65 万次；摘要写法更宽**
- [ ] 随机丢弃能否替换为基于重要性的选择性淘汰
- [ ] 能否把 EM-LLM 的事件分割接到 MEMORYLLM 前面，用事件而不是固定片段做写入单元
- [ ] 能否做分层 memory pool，而不是所有记忆都在同一淘汰机制里竞争
