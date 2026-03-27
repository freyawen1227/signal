---
title: Anthropic 发布 Claude Haiku 4.5：编程性能媲美 Sonnet 4，成本仅三分之一
date: 2025-10-15
source: Anthropic
source_url: https://www.anthropic.com/news/claude-haiku-4-5
tags: [Claude, Anthropic, Haiku, 小模型, 混合推理, SWE-Bench]
---

# Anthropic 发布 Claude Haiku 4.5：编程性能媲美 Sonnet 4，成本仅三分之一

> **原文**: [Anthropic](https://www.anthropic.com/news/claude-haiku-4-5)

## 核心内容

- Anthropic 于 2025 年 10 月 15 日发布 Claude Haiku 4.5，定位「小而强」
- 编程性能与五个月前 SOTA 的 Sonnet 4 相当，价格仅为其三分之一
- SWE-Bench Verified 得分 73.3%，跻身全球顶级编程模型行列
- 引入混合推理模式：快速响应与扩展思考模式可切换
- 成为所有免费 Claude.ai 用户的默认模型

## 技术解读

### 技术突破点

**混合推理架构**

Haiku 4.5 作为混合推理系统运行，允许用户在两种响应模式之间选择：
- **快速模式**（默认）：直接快速回答查询
- **扩展思考模式**：模型在回答前分配额外时间进行深度思考

这是相对于 Haiku 3.5 的重大升级，后者完全不支持扩展思考功能。

**计算机使用能力提升**

在计算机使用任务上，Haiku 4.5 相比之前的模型有显著性能提升，使得更快速、响应更敏捷的应用成为可能。模型支持视觉理解，解锁了此前客户必须在性能和成本之间做选择的新用例。

**成本效率优化**

定价为每百万输入 token $1、每百万输出 token $5，在保持近前沿智能水平的同时实现了极具竞争力的成本结构。

### 横向对比

| 指标 | Claude Haiku 4.5 | Claude Sonnet 4 | 对比 |
|-----|------------------|-----------------|-----|
| SWE-Bench Verified | 73.3% | ~73% | 相当 |
| 输入价格 ($/M tokens) | $1 | $3 | 降低 67% |
| 输出价格 ($/M tokens) | $5 | $15 | 降低 67% |
| 扩展思考 | 支持 | 支持 | - |
| 计算机使用 | 支持 | 支持 | - |

### 对开发者/行业的影响

**多智能体架构的理想选择**

Sonnet 4.5 可以将复杂问题分解为多步骤计划，然后编排多个 Haiku 4.5 并行完成子任务。这种「大模型调度 + 小模型执行」的架构模式在成本和效果上取得了良好平衡。

**免费用户的智能升级**

Anthropic 将 Haiku 4.5 设为所有免费 Claude.ai 用户的默认模型，任何人都可以通过 Claude 网站或移动应用免费获得近前沿级别的智能服务。

**全平台可用性**

开发者可通过以下渠道使用 Haiku 4.5：
- Claude Developer Platform 原生支持
- Amazon Bedrock
- Google Cloud Vertex AI
- Microsoft Foundry
