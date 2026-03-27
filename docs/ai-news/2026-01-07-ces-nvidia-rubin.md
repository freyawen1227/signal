---
title: CES 2026：NVIDIA 发布 Rubin 平台，训练性能是 Blackwell 的 3.5 倍
date: 2026-01-07
source: NVIDIA Newsroom
source_url: https://nvidianews.nvidia.com/news/rubin-platform-ai-supercomputer
tags: [NVIDIA, CES 2026, Rubin, GPU, AI芯片]
---

# CES 2026：NVIDIA 发布 Rubin 平台，训练性能是 Blackwell 的 3.5 倍

> **原文**: [NVIDIA Newsroom](https://nvidianews.nvidia.com/news/rubin-platform-ai-supercomputer)

## 核心内容

- **六芯片极致协同设计**: Rubin 是 NVIDIA 首个"极致协同设计"AI 平台，集成 Vera CPU、Rubin GPU、NVLink 6 Switch、ConnectX-9 SuperNIC、BlueField-4 DPU、Spectrum-6 以太网交换机六款芯片
- **性能大幅跃升**: 相比 Blackwell，推理性能提升 5 倍，训练性能提升 3.5 倍，推理 Token 成本降低 10 倍，训练所需 GPU 数量减少 4 倍
- **已进入量产**: 黄仁勋宣布 Rubin 平台已全面投产，基于 Rubin 的产品将于 2026 年下半年通过合作伙伴发售

## 解读

### Rubin vs Blackwell 性能对比

| 指标 | Rubin 相对 Blackwell |
|------|---------------------|
| 推理性能 | 5 倍 |
| 训练性能 | 3.5 倍 |
| 推理 Token 成本 | 降低 10 倍 |
| 训练所需 GPU | 减少 4 倍 |
| HBM 带宽 | 22 TB/s（Blackwell 8 TB/s）|
| HBM 容量 | 288 GB（Blackwell 192 GB）|

### 六芯片协同架构

Rubin 平台的核心创新在于"极致协同设计"：

1. **Vera CPU**: Grace 的继任者，专为 AI 工作负载优化
2. **Rubin GPU**: 搭载 8 堆栈 HBM4 显存，带宽达 22 TB/s
3. **NVLink 6 Switch**: 高速 GPU 间互联
4. **ConnectX-9 SuperNIC**: 超级网卡
5. **BlueField-4 DPU**: 数据处理单元
6. **Spectrum-6 以太网交换机**: 网络基础设施

### 首批云服务商

2026 年首批部署 Vera Rubin 实例的云服务商：
- **超大规模**: AWS、Google Cloud、Microsoft Azure、OCI
- **NVIDIA 云合作伙伴**: CoreWeave、Lambda、Nebius、Nscale

### 黄仁勋的判断

> "Rubin 在恰当的时机到来，AI 计算需求——无论是训练还是推理——都在急剧增长。通过每年交付新一代 AI 超级计算机的节奏，以及六款新芯片的极致协同设计，Rubin 向 AI 的下一个前沿迈出了巨大一步。"

### 趋势分析

NVIDIA 坚持"年度迭代"节奏：Hopper -> Blackwell -> Rubin。每一代都实现数倍性能提升，但 Rubin 的特别之处在于：

1. **系统级优化**: 不只是 GPU 升级，而是整个计算栈的协同演进
2. **成本效率**: 10 倍的推理成本下降将大幅降低 AI 应用门槛
3. **命名致敬**: 以美国天文学家 Vera Rubin（暗物质研究先驱）命名，延续 NVIDIA 致敬科学家的传统

Rubin 平台的发布标志着 AI 基础设施进入"极致效率"时代，这将加速从大模型训练到 Agent 推理的全链路降本增效。
