# 记忆巩固方向：可视化研究地图

这份文件不是论文笔记。

它只做一件事：

**把“现有研究已经覆盖到哪”和“你还能往哪做”画成一张更直观的图。**

适合什么时候看：
- 脑子里已经有很多论文名字，但还是容易混
- 想快速判断哪些方向已经拥挤，哪些方向还能切
- 想把自己的研究点放到整张地图里看

---

## 图 1：大地图

```mermaid
flowchart TD
    A["LLM Long-Term Memory Research"] --> B["A. 写入 / 存储"]
    A --> C["B. 巩固 / 整理"]
    A --> D["C. 检索 / 回忆"]
    A --> E["D. 遗忘 / 衰减"]
    A --> F["E. 结构 / 具身"]

    C --> C1["已被明显覆盖的路线"]
    C --> C2["还可继续拓展的路线"]

    C1 --> C11["时间层级巩固<br/>TiMem"]
    C1 --> C12["sleep-time / 离线更新<br/>LightMem"]
    C1 --> C13["存前推理整理<br/>PREMem"]
    C1 --> C14["写入时在线综合<br/>SimpleMem"]
    C1 --> C15["融合 / 冲突消解 / 遗忘<br/>FadeMem"]
    C1 --> C16["递归摘要长期记忆<br/>Recursive Summarization"]

    C2 --> C21["可追溯 reconsolidation<br/>当前最值得收敛的主线"]
    C2 --> C22["episodic -> semantic schema induction"]
    C2 --> C23["episodic -> procedural consolidation"]
    C2 --> C24["benchmark / metric first consolidation"]
    C2 --> C25["causal / conflict-aware reconsolidation"]

    style C fill:#ffe9b3,stroke:#9a6a00,stroke-width:2px
    style C1 fill:#ffd6d6,stroke:#a33,stroke-width:1px
    style C2 fill:#d8f3dc,stroke:#2d6a4f,stroke-width:1px
    style C21 fill:#b7e4c7,stroke:#1b4332,stroke-width:3px
```

这张图要表达的其实很简单：

- “记忆巩固”不是无人区
- 但“可追溯 reconsolidation”还不是一个已经被完全堵死的位置
- 你现在最适合的不是重做一遍 TiMem / LightMem / PREMem
- 而是把问题往后推进一步：**长期记忆形成以后怎么继续演化**

---

## 图 2：把“你现在在做什么”单独拉出来

```mermaid
flowchart TD
    A["长期记忆形成后"] --> B{"新证据来了"}

    B -->|无关| C["NOOP / 不处理"]
    B -->|真的是新东西| D["ADD"]
    B -->|支持旧记忆| E["SUPPORT / strengthen"]
    B -->|补充条件| F["REVISE"]
    B -->|直接反证| G["REVISE or RETIRE"]
    B -->|说明旧抽象太粗| H["SPLIT / re-ground"]

    F --> I["生成新版本"]
    G --> I
    H --> J["拆成更细的记忆"]

    I --> K["旧版本保留在版本链里"]
    J --> K
    K --> L["检索时默认只用当前 active 版本"]
    K --> M["需要时可以回溯 provenance / 来源 episode"]

    style F fill:#d8f3dc,stroke:#2d6a4f,stroke-width:2px
    style G fill:#d8f3dc,stroke:#2d6a4f,stroke-width:2px
    style H fill:#d8f3dc,stroke:#2d6a4f,stroke-width:2px
    style K fill:#ffe9b3,stroke:#9a6a00,stroke-width:2px
```

这张图就是你当前研究问题的人话版：

**不是“怎么再存一条记忆”，而是“旧长期记忆遇到新证据后怎么被修订、拆分、退役，而且修订过程还能追溯”。**

---

## 图 3：现有研究和你的可拓展空间，放在一棵树里看

```mermaid
flowchart LR
    A["Memory Consolidation"] --> B["已经被讲得比较完整"]
    A --> C["仍然有空间"]

    B --> B1["时间组织"]
    B1 --> B11["TiMem"]

    B --> B2["离线巩固 / 睡眠更新"]
    B2 --> B21["LightMem"]

    B --> B3["存前推理"]
    B3 --> B31["PREMem"]

    B --> B4["在线语义综合"]
    B4 --> B41["SimpleMem"]

    B --> B5["融合 / 冲突 / 衰减"]
    B5 --> B51["FadeMem"]

    C --> C1["Post-storage reconsolidation"]
    C1 --> C11["revision under later evidence"]
    C1 --> C12["stale memory suppression"]
    C1 --> C13["active-version retrieval"]

    C --> C2["Traceable abstraction"]
    C2 --> C21["provenance-preserving memory object"]
    C2 --> C22["support / contradiction / revision history"]

    C --> C3["从经历到知识 / 规则"]
    C3 --> C31["schema induction"]
    C3 --> C32["proceduralization"]

    C --> C4["评测先行"]
    C4 --> C41["revision accuracy"]
    C4 --> C42["traceability"]
    C4 --> C43["abstraction faithfulness"]

    style A fill:#ffe9b3,stroke:#9a6a00,stroke-width:2px
    style B fill:#ffd6d6,stroke:#a33,stroke-width:1px
    style C fill:#d8f3dc,stroke:#2d6a4f,stroke-width:1px
    style C1 fill:#b7e4c7,stroke:#1b4332,stroke-width:3px
    style C2 fill:#b7e4c7,stroke:#1b4332,stroke-width:2px
```

---

## 图 4：如果你要继续收敛，最推荐怎么走

```mermaid
flowchart TD
    A["你当前的位置"] --> B["先别再讲泛泛 consolidation"]
    B --> C["把主问题定成<br/>provenance-preserving reconsolidation"]

    C --> D["方法层"]
    C --> E["评测层"]
    C --> F["论文定位层"]

    D --> D1["memory object: version + status + provenance"]
    D --> D2["relation judge: support / refine / contradict / overgeneralized"]
    D --> D3["operations: add / revise / split / retire"]
    D --> D4["resolver: retrieval-time active version only"]

    E --> E1["delayed contradiction"]
    E --> E2["stale memory suppression"]
    E --> E3["provenance tracing"]
    E --> E4["abstraction faithfulness"]

    F --> F1["不和 TiMem 比时间树"]
    F --> F2["不和 LightMem 比纯 sleep-time efficiency"]
    F --> F3["不和 PREMem 比存前 reasoning"]
    F --> F4["主打 post-storage revision + traceability"]

    style C fill:#b7e4c7,stroke:#1b4332,stroke-width:3px
    style D fill:#d8f3dc,stroke:#2d6a4f,stroke-width:1px
    style E fill:#d8f3dc,stroke:#2d6a4f,stroke-width:1px
    style F fill:#d8f3dc,stroke:#2d6a4f,stroke-width:1px
```

---

## 一句话读图指南

如果你只记住一句话，就记这个：

**现有论文已经覆盖了“怎么整理一次记忆”，你更值得做的是“整理后的长期记忆如何在后续新证据下继续被可追溯地修订”。**

---

## 你现在最适合继续补强的 4 个点

1. `reconsolidation object` 定义清楚
2. `revision / split / retire` 的触发条件清楚
3. `provenance` 怎么保存与读取清楚
4. 专门评测 `revision` 和 `traceability`，不要只测普通 QA

---

## 对应代表论文

- `TiMem`：时间层级巩固
- `LightMem`：sleep-time / 离线长期更新
- `PREMem`：存前推理整理
- `SimpleMem`：在线语义综合
- `FadeMem`：融合、冲突消解、衰减
- `Recursive Summarization`：递归摘要长期记忆

这些工作更多覆盖的是：
- 怎么整理
- 怎么压缩
- 怎么分层
- 怎么融合

你现在想继续往前推的是：
- 怎么修旧记忆
- 怎么保留版本链
- 怎么保留来源链
- 怎么压住 stale memory
