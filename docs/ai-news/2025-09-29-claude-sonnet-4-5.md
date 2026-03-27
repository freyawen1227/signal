---
title: Anthropic 发布 Claude Sonnet 4.5：全球最强编程模型，推出 Claude Agent SDK
date: 2025-09-29
source: Anthropic
source_url: https://www.anthropic.com/news/claude-sonnet-4-5
tags: [Claude, Anthropic, Sonnet, 编程模型, Agent SDK, OSWorld, SWE-Bench]
---

# Anthropic 发布 Claude Sonnet 4.5：全球最强编程模型，推出 Claude Agent SDK

> **原文**: [Anthropic](https://www.anthropic.com/news/claude-sonnet-4-5)

## 核心内容

- Anthropic 于 2025 年 9 月 29 日发布 Claude Sonnet 4.5，Claude 4 系列最新成员
- 官方定位：「全球最强编程模型」「构建复杂智能体的最强模型」「最佳计算机使用模型」
- OSWorld 基准 61.4%（四个月前 Sonnet 4 为 42.2%），SWE-Bench Verified 77.2%（高配置达 82%）
- 同步推出 Claude Agent SDK，开发者可获得与 Claude Code 相同的智能体构建能力
- 展示超过 30 小时的持续任务专注能力

## 技术解读

### 技术突破点

**计算机使用能力的飞跃**

在 OSWorld 基准测试中，Sonnet 4.5 以 61.4% 的得分大幅领先。OSWorld 测试 AI 模型在真实计算机任务上的表现，包括网站导航、电子表格输入和桌面操作等。仅四个月前，Sonnet 4 以 42.2% 保持领先，这意味着近 50% 的相对性能提升。

**编程能力的新高度**

SWE-Bench Verified 得分 77.2%，使用简单脚手架（bash 和字符串替换文件编辑）在 10 次试验中取平均值。在高计算配置（并行尝试、拒绝采样、内部评分）下，模型可达 82.0%。

**超长任务专注能力**

模型展示了在复杂多步骤任务上保持超过 30 小时专注的能力。这种扩展注意力跨度对于需要长时间持续推理而不丢失上下文或犯错的自主智能体应用尤为重要。

### Claude Agent SDK

**与 Claude Code 同源的基础设施**

Claude Agent SDK 提供了与 Anthropic 一方产品（如 Claude Code）相同的基础设施和构建模块，使开发者能够创建具备以下能力的复杂 AI 智能体：
- 工具使用
- 文件创建
- 代码执行
- 上下文管理

**预构建企业级组件**

SDK 提供企业级 AI 智能体构建工具，包含预构建组件：
- 代码安全检查
- 代码审查
- 合同审查
- 会议摘要
- 财务报告
- 邮件自动化
- 发票处理

**解决关键技术挑战**

SDK 解决了内存管理、权限系统、多智能体协调等复杂挑战，让智能体能够自主处理复杂的多步骤任务。

### 横向对比

| 基准测试 | Claude Sonnet 4.5 | Claude Sonnet 4 | 提升 |
|---------|-------------------|-----------------|-----|
| OSWorld | 61.4% | 42.2% | +19.2% |
| SWE-Bench Verified | 77.2% | ~70% | +7%+ |
| SWE-Bench (高配置) | 82.0% | - | - |

### 对开发者/行业的影响

**无缝升级体验**

Anthropic 表示："我们建议所有用途升级到 Claude Sonnet 4.5。无论您通过我们的应用、API 还是 Claude Code 使用 Claude，Sonnet 4.5 都是即插即用的替代品，以相同价格提供大幅提升的性能。"

**定价与可用性**

- 定价：$3/百万输入 token，$15/百万输出 token
- 可用平台：Web、iOS、Android、Claude Developer Platform、Amazon Bedrock、Google Cloud Vertex AI

**智能体开发民主化**

Claude Agent SDK 的发布意味着任何开发者都可以利用 Anthropic 构建 Claude Code 所使用的相同工具和基础设施，这将大幅降低构建生产级 AI 智能体的门槛。
