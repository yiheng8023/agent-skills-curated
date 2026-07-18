# 分层可靠性投影对账

## 决策

本仓现在只在其声明范围内验证“分层可靠性”和“项目硬标准优先级”契约：这是
治理投影，不是实时运行效果证明。

最小充分链路为：

```text
instructions / rules
-> Skills / Recipes
-> scripts / schemas / validators
-> 消费方拥有的 Hook、CI 或 runtime controls
-> 项目拥有的硬标准
-> 证据与可问责的人类决策
```

不是每个任务都需要所有层。原生推理、无 Skill、无 Hook、无额外结构始终是合法
结果。只有证据证明存在实质缺口，而且收益高于上下文、控制、权限和维护成本时，
才增加更强的机制。

## 优先级边界

如果项目权威已经准入一项项目硬标准，那么与之冲突的通用 Skill 指导必须让位，
因为规范性裁决属于项目权威。本仓可以保留证据，并在未来形成非权威的标准候选
契约，但不能准入、发布或安装项目硬标准。

本对账验证 `acceptance.layered-reliability-model` 与
`acceptance.project-standard-precedence`。它不验证消费方映射、跨宿主行为、Hook
档位、标准候选成熟度或可运行的标准迁移级联。

## 有意推迟

硬标准抽取继续明确推迟。它必须先在独立来源、Agent 或宿主、任务类型和真实反馈
周期中证明稳定价值，再经过单独的项目权威决策。当前分层、字段和评审协议仍是
工作假设，不是过早固化的通用硬标准。

## 非动作

- 不实现 Skill、Recipe、Hook、CI、runtime 或硬标准；
- 不修改消费方、项目、release manifest 或 approved payload；
- 不跨仓写入，不提交，不推送。
