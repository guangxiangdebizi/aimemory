# 资源汇总

## 一、开源代码仓库

### 模型内生记忆
| 项目 | 论文 | 链接 | 说明 |
|------|------|------|------|
| MemoryLLM | MEMORYLLM + M+ (ICML'24/'25) | https://github.com/wangyu-ustc/MemoryLLM | 含 7B/8B/chat 版本 |

### 外部记忆系统
| 项目 | 论文 | 链接 | 说明 |
|------|------|------|------|
| Letta (MemGPT) | MemGPT | https://github.com/letta-ai/letta | OS 式记忆管理框架 |
| SCM4LLMs | SCM | https://github.com/wbbeyourself/SCM4LLMs | 自控记忆框架 |
| FadeMem | FadeMem | https://github.com/ChihayaAine/FadeMem | 生物启发遗忘 |
| GSW Memory | GSW | https://github.com/roychowdhuryresearch/gsw-memory | 生成式语义工作空间 |

### 记忆相关工具
| 项目 | 链接 | 说明 |
|------|------|------|
| Mem0 | https://github.com/mem0ai/mem0 | LLM 记忆层，工业级 |
| LangChain Memory | https://github.com/langchain-ai/langchain | 内置多种记忆模块 |
| LlamaIndex | https://github.com/run-llama/llama_index | 检索增强框架 |

---

## 二、论文直链

### 顶会论文（PDF）
| 论文 | Venue | 链接 |
|------|-------|------|
| MEMORYLLM | ICML 2024 | https://arxiv.org/abs/2402.04624 |
| M+ | ICML 2025 | https://proceedings.mlr.press/v267/wang25au.html |
| EM-LLM | ICLR 2025 | https://arxiv.org/abs/2407.09450 |
| MemoryBank | AAAI 2024 | https://arxiv.org/abs/2305.10250 |
| GSW | AAAI 2026 | https://arxiv.org/abs/2511.07587 |
| EpMAN | ACL 2025 | https://aclanthology.org/2025.acl-long.574/ |

### 顶刊论文
| 论文 | Venue | 链接 |
|------|-------|------|
| Human-Like Episodic Memory | Trends Cogn. Sci. 2025 | https://doi.org/10.1016/j.tics.2025.06.016 |

### 高影响力预印本
| 论文 | 时间 | 链接 |
|------|------|------|
| SYNAPSE | 2026.01 | https://arxiv.org/abs/2601.02744 |
| FadeMem | 2026.01 | https://arxiv.org/abs/2601.18642 |
| MemGPT | 2023.10 | https://arxiv.org/abs/2310.08560 |
| SCM | 2023.04 | https://arxiv.org/abs/2304.13343 |

### 综述论文
| 论文 | 时间 | 链接 |
|------|------|------|
| Memory in the LLM Era | 2026.04 | https://arxiv.org/abs/2604.01707 |
| Anatomy of Agentic Memory | 2025.02 | https://arxiv.org/abs/2602.19320 |
| Memory for Autonomous LLM Agents | 2025.03 | https://arxiv.org/abs/2603.07670 |
| Continual Learning in LLMs | 2025.03 | https://arxiv.org/abs/2603.12658 |

---

## 三、Benchmark 数据集

| 数据集 | 用途 | 使用论文 |
|--------|------|---------|
| LoCoMo | 长对话记忆评估 | SYNAPSE, FadeMem |
| LongBench | 长上下文理解 | EM-LLM |
| ∞-Bench | 超长上下文评估 | EM-LLM |
| EpBench | 情景记忆评估（100k-1M tokens） | GSW |
| Multi-Session Chat | 多轮对话记忆 | FadeMem |
| LTI-Bench | 长期交互评估 | FadeMem |
| MemoryAgentBench | Agent 记忆评估 | (ICLR 2026) |

---

## 四、Awesome List

| 名称 | 链接 | 说明 |
|------|------|------|
| awesome-long-term-memory | https://github.com/xiaowu0162/awesome-long-term-memory | 长期记忆论文合集，持续更新 |

---

## 五、关键概念速查

| 概念 | 英文 | 来源 | 简要说明 |
|------|------|------|---------|
| 情景记忆 | Episodic Memory | 认知科学 | 具体事件记忆，带时间地点 |
| 语义记忆 | Semantic Memory | 认知科学 | 抽象知识，不带时间 |
| 程序记忆 | Procedural Memory | 认知科学 | 技能和习惯 |
| 工作记忆 | Working Memory | 认知科学 | 当前活跃的短期记忆 |
| 记忆巩固 | Memory Consolidation | 认知科学 | 短期→长期的转化 |
| 事件分割 | Event Segmentation | 认知科学 | 连续经历切分为离散事件 |
| 艾宾浩斯遗忘曲线 | Ebbinghaus Forgetting Curve | 认知科学 | 记忆强度随时间指数衰减 |
| 扩散激活 | Spreading Activation | 认知科学 | 激活信号沿关联网络传播 |
| 侧抑制 | Lateral Inhibition | 神经科学 | 高激活节点抑制邻近低激活节点 |
| 贝叶斯惊奇 | Bayesian Surprise | 计算认知 | 信息流中的意外程度 |
| 灾难性遗忘 | Catastrophic Forgetting | 机器学习 | 学新知识时忘掉旧知识 |
| 持续学习 | Continual Learning | 机器学习 | 模型持续适应新数据 |
| 检索增强生成 | RAG | NLP | 检索外部知识辅助生成 |
| 参数高效微调 | PEFT / LoRA | NLP | 低成本微调模型 |
| 虚拟上下文管理 | Virtual Context Mgmt | MemGPT | OS 式信息换入换出 |
