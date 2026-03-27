---
title: Kimi K2 Thinking 发布：超越 GPT-5 的开源思考模型
date: 2025-11-06
source: Moonshot AI
source_url: https://moonshotai.github.io/Kimi-K2/thinking.html
tags: [Kimi, Moonshot AI, 开源模型, 思考模型, SWE-Bench, 智能体]
---

# Kimi K2 Thinking 发布：超越 GPT-5 的开源思考模型

> **原文**: [Moonshot AI](https://moonshotai.github.io/Kimi-K2/thinking.html)

## 核心内容

- Moonshot AI 发布 Kimi K2 Thinking，成为目前最强开源思考模型
- 原生支持「边思考，边使用工具」能力，可执行 200-300 次连续工具调用
- SWE-Bench Verified 得分 71.3%，Humanity's Last Exam 得分 44.9%（超越 GPT-5 的 41.7%）
- 采用原生 INT4 量化，支持 256K 上下文窗口

## 技术解读

### 技术突破点

**原生思考智能体架构**

Kimi K2 Thinking 的核心创新在于将思考能力与工具使用能力深度融合。与传统的「先思考再行动」模式不同，K2 Thinking 实现了动态的 think -> search -> browser use -> think -> code 循环，能够持续生成和优化假设、验证证据、推理并构建连贯答案。

**长程工具调用能力**

模型能够执行 200-300 次连续工具调用，这得益于其长期规划和自适应推理能力。这种交织推理（interleaved reasoning）允许模型将模糊的开放性问题分解为清晰、可执行的子任务。

**高效量化技术**

K2 Thinking 采用原生 INT4 量化技术，在保持模型能力的同时实现了推理延迟和 GPU 内存占用的无损降低，这对于部署万亿参数级别的模型至关重要。

### 横向对比

| 基准测试 | Kimi K2 Thinking | GPT-5 | 提升幅度 |
|---------|------------------|-------|---------|
| Humanity's Last Exam | 44.9% | 41.7% | +3.2% |
| BrowseComp | 60.2% | - | - |
| SWE-Bench Verified | 71.3% | - | - |
| SWE-Multilingual | 61.1% | - | - |
| Terminal-Bench | 47.1% | - | - |

K2 Thinking 在多个关键基准上刷新了开源模型的记录，特别是在需要复杂推理和工具使用的任务上表现突出。

### 对开发者/行业的影响

**开源生态的里程碑**

这是首个在 Humanity's Last Exam 上超越闭源顶级模型的开源模型，标志着开源社区在 AI 能力上正在追平甚至超越闭源模型。

**智能体开发的新范式**

K2 Thinking 展示了思考模型在智能体场景下的巨大潜力。其原生工具调用能力使得开发者可以构建更加复杂和可靠的 AI 智能体系统。

**评估框架的重要性**

Moonshot AI 为 SWE-Bench 系列评估开发了内部评估框架，包含最小化工具集（bash、createfile、insert、view、strreplace、submit）和专门的系统提示，这为社区提供了可复现的评估标准。
