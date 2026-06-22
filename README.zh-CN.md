# Agent Skills Curated

[English](README.md) | 简体中文

这是一个私有、跨 Agent 的权威仓库，负责经过审查的 Skill 正文、来源、治理证据、
能力拓扑和确定性发布清单。

## 仓库职责

本仓库治理可复用 Skill 从准入到批准发布的完整资产链，并作为
`codex-user-config` 的上游生产者；配置仓是运行时和用户配置的消费者。

## 本仓库提供什么

- `skills/` 中经过审查、可移植的 Skill 正文；
- 固定来源、许可证、来源证明、选择裁决和适配哈希；
- 安全、可移植性、重叠、生命周期和冲突证据；
- Skills、能力、关系、冲突和 Recipes 的权威 registry；
- 确定性的派生投影和 schema 1 发布清单。

当前批准发布包含 34 个 Skills、60 个文件：29 个已审查本地 Skills，以及从
`addyosmani/agent-skills` 跨 Agent 适配的 5 个 Skills。

## 本仓库不负责什么

本仓库不负责用户配置、认证、运行时记忆、Plugins、Apps、MCP 账号状态、安装权限
或 live 环境状态；不执行安装，不写入 `codex-user-config`，也不写入 live Agent
环境。

本精选仓只治理第三方 Skill 正文和抽象、产品中立的能力分类，不治理、也不盘点官方、
运行时所有、内置或第一方 Skill 正文。它们只能作为带日期的重叠审查证据出现；这类
证据不是受管 inventory、仓库所有权或当前运行时可用性的证明。

## 与配对仓库的关系

依赖与权威方向保持单向：

```text
codex-user-config
  → 消费固定且已审查的版本和 release manifest
  → 规划、备份、安装、验证和回滚受管 Skill 路径

agent-skills-curated
  → 负责已审查 Skill 正文、来源、拓扑、冲突、政策、审计和确定性清单
  → 不反向写入 codex-user-config 或 live Agent 环境
```

配置仓不接管第三方 Skill 正文治理；精选仓不接管消费者侧安装或运行时集成。

## 能力分层与路由

三层资产不可混同：

1. 官方、运行时所有、内置或第一方 Skill 只能出现在带日期的重叠证据中；其正文和
   运行时身份都不是受管 inventory，不复制，也不在本仓发布；
2. 第三方候选必须经过来源固定、许可证、来源证明、安全、可移植性、重叠、适配和
   验证；批准前只留在来源、准入、选择和审计层，不得进入执行路径；
3. 只有 `status=approved` 的精选批准 Skill 才能进入 `skills/` 和清单。在 schema 1
   中，`registry/skills.json` 是批准发布清单，而不是候选积压。

配置仓拥有的 `capability-router` 是“能力决策路由器”，不是尽量选择 Skill 的
skill-router。候选决策包括原生推理、官方或运行时能力、精选 Skill、外部能力元数据、
Recipe/DAG、请求人工确认和无需 Skill。第三方候选不是可执行路由目标；高风险、歧义、
冲突、权限变化、写入、安装、删除、迁移、发布或回滚必须请求人工确认。

## 目录结构

- `skills/`：精选批准的可移植 Skill 正文；
- `sources/`：不可变来源锁、许可证、选择和哈希；
- `registry/`：人工维护的拓扑与发布清单权威；
- `policies/`：准入、可移植性、安全、重叠和生命周期规则；
- `audits/`：来源级审查与证据；
- `generated/`：确定性派生投影，不是第二真相源；
- `release-manifest.json`：批准 payload 的精确路径、大小和哈希；
- `scripts/`：只负责验证和确定性投影生成。

## 验证方式

```bash
python -B -m unittest discover -s tests -v
python -B scripts/build_topology.py --check
python -B scripts/verify.py
```

验证覆盖 registry 契约、引用、派生文件一致性、来源证据和精确 payload，但不会安装
Skill。

## 更新规则

每个上游版本都必须作为新的不可变准入：固定版本、保存许可证和来源证明、审查可执行
面、评估安全/可移植性/重叠、最小适配、验证、更新拓扑，最后才批准新的发布清单。
候选裁决可以是 `merge`、`adapter-only`、`recipe-only` 或 `reject`，但这些裁决本身
不等于运行时批准。

## 安全边界

- `generated/` 只是 registry 真相的派生投影；
- 候选内容或带日期的重叠证据不得被描述为已经安装或可以执行；
- 跨 Agent 可移植性不得削弱权限、安全、证据、许可证或真实环境限制；
- 安装、账号连接、外部写入和信任边界变化由消费者侧处理，并需适用的授权。
