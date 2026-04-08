# MemoryBank: Enhancing Large Language Models with Long-Term Memory

> 核对状态：已按论文 PDF 复核（2026-04-07）。

## 基本信息

| 项目 | 内容 |
|------|------|
| **Venue** | AAAI 2024（论文最早公开版本为 arXiv 2023） |
| **作者** | Wanjun Zhong, Lianghong Guo, Qiqi Gao, He Ye, Yanlin Wang |
| **机构** | Sun Yat-Sen University, Harbin Institute of Technology, KTH Royal Institute of Technology |
| **论文** | https://arxiv.org/abs/2305.10250 |
| **DOI** | https://doi.org/10.1609/AAAI.V38I17.29946 |
| **PDF** | https://arxiv.org/pdf/2305.10250.pdf |
| **本地 PDF** | [03_MemoryBank.pdf](../_tmp_pdfs/03_MemoryBank.pdf) |
| **本地抽取文本** | [03_MemoryBank.txt](../_tmp_txt/03_MemoryBank.txt) |
| **代码** | https://github.com/zhongwanjun/MemoryBank-SiliconFriend |

## 为什么这篇重要

**这是把“长期记忆 + 遗忘曲线 + 用户画像”一起落到 LLM 交互系统里的早期代表作。**

它重要的地方不只是“能记住历史对话”，而是明确把下面三件事组成一个系统：

- 记忆存储
- 记忆检索
- 记忆更新与遗忘

对我们来说，这篇论文最大的价值是：

> 它把“AI 记忆不仅要会存，还要会忘”这件事讲成了一个可实现的工程系统。

## 核心架构（按原文）

论文把 MemoryBank 拆成三块：

1. **memory storage**
2. **memory retrieval**
3. **memory updater**

### 1. Memory Storage：不只是聊天记录，还包括摘要和画像

MemoryBank 的存储不是单层对话日志，而是一个多层结构：

- **逐日对话记录**：按时间顺序保存多轮对话
- **daily event summary**：把当天对话压缩成事件摘要
- **global event summary**：再把多天摘要合成为全局摘要
- **daily personality insights**：从当天对话归纳用户性格与情绪
- **global personality summary**：进一步形成稳定用户画像

也就是说，它不是单纯“存原文”，而是显式做了：

- 时间组织
- 层级摘要
- 用户画像更新

### 2. Memory Retrieval：论文里是 DPR 风格 dense retrieval，不是模糊表述的“语义召回”

这里需要纠正一个常见误读。

论文写得很明确：它把 memory retrieval 视作一个**知识检索任务**，采用的是
类似 **Dense Passage Retrieval (DPR)** 的双塔 dense retrieval 流程：

- 每条对话 turn 或事件摘要作为一个 memory piece `m`
- 用 encoder `E(.)` 预编码成向量 `h_m`
- 把整库向量放进 **FAISS**
- 当前对话上下文 `c` 编码成 query 向量 `h_c`
- 再在 FAISS 里检索最相关记忆

在 SiliconFriend 的实现里，论文进一步写到：

- English embedding 用 **MiniLM**
- Chinese embedding 用 **Text2vec**
- 工程上借助 **LangChain + FAISS**

### 3. Memory Updating：艾宾浩斯遗忘曲线，但形式比很多二手总结更简单

论文采用的公式是：

```text
R = e^(-t / S)
```

其中：

- `R` = 记忆保留率
- `t` = 距离学习或上次强化的时间
- `S` = memory strength

最关键的原文细节是：

- `S` 被建模成**离散值**
- 一条记忆**首次出现时初始化为 1**
- 当该记忆在后续对话中被召回时，**S 加 1，同时 t 归零**

所以更准确的理解应该是：

> 论文里的 formalism 不是“LLM 先给每条记忆打 importance 分数”，而是用一个很简化的、基于是否被再次召回的 strength 变量来模拟强化与遗忘。

论文正文虽然口头上提到“less important”记忆更容易遗忘，但真正写进公式里的核心变量是：

- 时间 `t`
- strength `S`
- 是否被再次召回

## SiliconFriend：论文的主要落地场景

论文把 MemoryBank 实装成一个长期陪伴式聊天系统 **SiliconFriend**。

这里的几个关键事实值得保留：

- 支持 **ChatGPT / ChatGLM / BELLE**
- 对开源模型做了两阶段开发：
  - 先用 **38k psychological dialogues** 做心理陪伴领域适配
  - 再集成 MemoryBank
- 支持 **中英文双语**

所以这篇论文其实既是“记忆机制论文”，也是“长期陪伴 AI 系统论文”。

## 实验结果（关键数字）

### 1. 定量评测设置

论文的量化实验并不是标准公开 benchmark，而是作者自己构造的长期对话记忆测试：

- **10 天**对话历史
- **15 位**虚拟用户
- **194 个** probing questions
- 同时构造 **英文 / 中文** 两套 memory storage

评测指标是：

- Retrieval Accuracy
- Correctness
- Coherence
- Ranking Score

### 2. 定量结果

论文 Table 2 的核心结论是：

| 语言 | 模型 | Retrieval Acc. | Correctness | Coherence | Ranking |
|------|------|----------------|-------------|-----------|---------|
| English | SiliconFriend ChatGLM | 0.809 | 0.438 | 0.680 | 0.498 |
| English | SiliconFriend BELLE | 0.814 | 0.479 | 0.582 | 0.517 |
| **English** | **SiliconFriend ChatGPT** | **0.763** | **0.716** | **0.912** | **0.818** |
| Chinese | SiliconFriend ChatGLM | 0.840 | 0.418 | 0.428 | 0.510 |
| **Chinese** | **SiliconFriend BELLE** | **0.856** | **0.603** | **0.562** | **0.565** |
| Chinese | SiliconFriend ChatGPT | 0.711 | 0.655 | 0.675 | 0.758 |

读表时要注意：

- 检索准确率最高的不一定是整体最好模型
- English 上整体最强的是 **SiliconFriend ChatGPT**
- Chinese 上 **BELLE** 的 retrieval / correctness 结果更亮眼

### 3. 论文真正证明了什么

这篇论文更像是在证明：

- MemoryBank 可以让长期对话系统更会“记住用户”
- 可以形成用户画像并让回答更贴合历史关系
- 遗忘机制可以让系统更像“有记忆的陪伴体”

它**没有**像后来的长上下文论文那样，在标准长文 QA benchmark 上做大规模 head-to-head 对比。

## 与本项目的关系

**直接相关度：⭐⭐⭐⭐⭐**

这篇最适合作为我们“外部长期记忆 + 遗忘”路线的起点：

- 它把遗忘机制明确放进系统设计
- 它强调用户画像与事件摘要的层级组织
- 它给出了一个很清晰的 companion-memory 场景

如果我们以后做更通用的 agent memory，这篇可以作为“最早一代带遗忘的对话记忆系统”基线。

## 与 MEMORYLLM 的关键区别

| 维度 | MemoryBank | MEMORYLLM |
|------|-----------|-----------|
| 记忆位置 | 外部 memory storage | 模型 latent space 内部 |
| 检索方式 | DPR 风格 dense retrieval + FAISS | 直接 attend memory pool |
| 遗忘机制 | 显式 `R = e^(-t/S)` | 随机丢弃带来的指数衰减 |
| 可解释性 | 高 | 低 |
| 适用场景 | 长期对话 / 用户画像 / companion | 内生记忆 / 模型自更新 |

## 关键局限

- **评测偏场景化**：核心验证集中在 AI companion，而不是通用 benchmark
- **遗忘模型非常简化**：`S` 只是离散强度，远谈不上完整认知模型
- **删除阈值不够明确**：论文没有把“何时彻底删掉一条记忆”定义得很硬
- **检索质量强依赖 embedding 模型**：MiniLM / Text2vec / FAISS 选型都会影响表现

## 待深入的问题

- [x] 检索到底怎么做？→ **双塔 dense retrieval + FAISS，不是泛泛的语义匹配**
- [x] `S` 是不是“LLM 重要性评分”？→ **不是论文 formalism 的核心写法；论文正式机制是首次置 1、召回加 1**
- [x] 是否做了层级摘要和用户画像？→ **做了，而且是系统设计的一部分**
- [ ] 如果换成事件图结构，能否比“对话 turn / 摘要块”更稳
- [ ] 遗忘除了时间与重复召回，能否再引入情绪强度、任务价值、近期目标相关性
- [ ] 能否把这种显式外部遗忘机制与 EM-LLM 的事件切分结合起来
