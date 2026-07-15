# Agent Skills Curated

[English](README.md) | 简体中文

这是一个公开安全、跨 Agent 的权威仓库，负责经过审查的 Skill 正文、来源、治理证据、
能力拓扑和确定性发布清单。

## 仓库职责

本仓库治理可复用 Skill 从准入到批准发布的完整资产链，并作为面向 Agent 的中立生产者。
Codex 与 Claude 是当前已经刻画的消费侧实例，因为它们是维护者正在使用的环境；它们不
构成本仓模型边界。公开读者应从公开安全模板 `codex-user-config-template` 与
`claude-user-config-template` 开始理解消费侧结构；这两个模板展示的是更通用的
agent 环境迁移、云端同步/备份、验证和恢复模式。

## 本仓库提供什么

- `skills/` 中经过审查、可移植的 Skill 正文；
- 固定来源、许可证、来源证明、选择裁决和适配哈希；
- 安全、可移植性、重叠、生命周期和冲突证据；
- Skills、能力、关系、冲突和 Recipes 的权威 registry；
- 确定性的派生投影和 schema 1 发布清单。

当前批准发布包含 20 个 Skills、42 个文件：5 个来自
`addyosmani/agent-skills`，14 个来自 `mattpocock/skills`，1 个来自
`kepano/obsidian-skills`。它们都具备完整、固定的 Git 来源；原先来源不完整的
本地基线仅保留为非运行时历史证据。

## 战略定位

经过审查的 Skills 是 `YIYUAN-MERIDIAN` 更广资源治理漏斗中的首个末端 MVP。
它们是低负担、跨 Agent 的切入点，可以为内外部消费者携带指导、资源、脚本和
确定性检查；它们不是唯一可能的末端，也不把上游发现范围限制为 Skills。

本仓是多领域治理仓。人机协作短板只是一个以证据驱动的需求通道，不是本仓全部使命。
稳定原则是“复用优先于自制”：先建立需求证据，再比较原生、官方、运行时、单 Skill、
组合 Skill 和其它 Harness 替代方案；只有证明存在剩余缺口后，才允许进入适配或仓库自制。
发现数量、流行度或历史草案都不能单独证明缺口。

本仓要交付的是“决策就绪的外脑”，而不是越来越大的 inventory。消费方应获得经过治理的
少量路由、替代方案、冲突、证据边界和复查信号，而不是反复穷举未知 Skills；由此降低筛选、
路由、上下文和维护负担，让人主要投入创作与决策。本仓不宣称提高模型能力上限，也不把
某一 Agent 的验证结果泛化为所有 Agent 的一致行为。

稳定工序采用依赖图，而不是强制线性流水线：消费投影是可选分支，生命周期治理是跨阶段
回路，标准抽取只在重复证据成立时进入条件分支。上游雷达可以广泛发现，但候选信号必须在
本仓绑定需求、基线、精确来源固定、审查和验收后，才能影响精选决策。总控修订已经形成
明确的 owner 接受事件；当前 initiative 是仍待收口的 Round 02，而不是从历史步骤反推。

可靠性采用分层保障，而不是只依赖文本：instructions 与 rules 可以路由到 Skills 和
Recipes；脚本、schemas 与 validators 负责可机器检查的行为；消费侧控制和项目内置
硬标准仍属于更高权威的集成面。本仓可以从重复治理证据中提取可追溯的标准候选，
但不负责准入、发布或安装项目硬标准。用户配置仓在这条链路中只承担消费、验证和
反馈，不是跨项目调研或标准的长期托管位置；有边界的调研与标准候选包后续应交付到
`YIYUAN-CALIBRATION` 校准和保管，再由 `YIYUAN-ASSETS` 独立决定是否准入为项目硬标准。

战略目标到验收、验证和证据的稳定映射位于
`registry/program-acceptance-map.json`。局部或带日期的证据必须保持 partial 或
stale；仓库验证器通过不能证明当前 live Agent 状态。

## 本仓库不负责什么

本仓库不负责用户配置、认证、运行时记忆、Plugins、Apps、MCP 账号状态、安装权限
或 live 环境状态；不执行安装，不写入 `codex-user-config`、`claude-user-config`
这类私有消费配置仓，也不写入 live Agent 环境。
向 `YIYUAN-CALIBRATION` 交付材料属于另一项需要单独授权的跨仓事务，不是本仓验证或
发布流程可以顺带执行的隐含副作用。

本精选仓只治理第三方 Skill 正文和抽象、产品中立的能力分类，不治理、也不盘点官方、
运行时所有、内置或第一方 Skill 正文。它们只能作为带日期的重叠审查证据出现；这类
证据不是受管 inventory、仓库所有权或当前运行时可用性的证明。

来自 Agent、运行时、平台或工具生态的官方 Skills、能力包、workflow templates 或类似
公开能力包，可以作为带日期的“官方外部能力基线”记录。基线用于覆盖关系对照、缺口分析
和路由校准，不是受管 inventory。本仓用基线矩阵裁定 `covered`、`reference`、
`adapt-candidate` 或 `skip`；不会盲目导入官方仓库，也不会在未验证流程、资源、脚本、
触发描述和产物标准之前宣称完整覆盖。当前第一份基线实例是
`docs/anthropic-official-skills-coverage.md`。

## 与配对仓库的关系

依赖与权威方向保持单向：

```text
当前公开读者入口
  codex-user-config-template
  claude-user-config-template
    → 展示公开安全结构、占位值和用户自建指引

当前私有消费仓
  codex-user-config
  claude-user-config
    → 可消费固定且已审查的版本和 release manifest
    → 规划、备份、安装、验证和回滚受管 Skill 路径

agent-skills-curated
  → 负责已审查 Skill 正文、来源、拓扑、冲突、政策、审计和确定性清单
  → 不反向写入私有消费配置仓或 live Agent 环境
```

公开模板不包含维护者的私有配置、记忆、账号假设、偏好或本机状态；它们是外部用户理解
消费侧模式的公开入口。私有 Codex 与 Claude 配置仓是真实下游消费方，但普通公开用户
不需要访问它们。

消费侧模式是通用的，即使具体实现会因 agent 而异。未来其它 agent 或工具链只要完成
运行时文件、设置、记忆、hooks、工具、权限和恢复行为的映射，也可以拥有自己的公开模板
和私有 overlay。

消费仓不接管第三方 Skill 正文治理；精选仓不接管消费者侧安装或运行时集成。每个消费仓
负责自己的消费侧集成；本仓保持 agent 中立，不绑定任何单一 agent。

真实用户配置仓可能包含个人信息、偏好、记忆快照、账号假设、本地恢复策略或私有运行选择，
除非经过专门脱敏，否则应保持私有。如需公开配置示例，应另建 `codex-user-config-template`
或 `claude-user-config-template` 这类公开模板，使用占位值和用户自建指引，而不是复制私人仓库。

更宽的公开侧仓库家族由 `YIYUAN-MERIDIAN` 映射。该总入口可以映射本仓、
`resource-radar`、配置模板、书签分类仓和未来末端链路，但不拥有 Skill release
决策、manifest 或运行时安装。

## 能力分层与路由

三层资产不可混同：

1. 官方、运行时所有、内置或第一方 Skill 只能出现在带日期的重叠证据中；其正文和
   运行时身份都不是受管 inventory，不复制，也不在本仓发布；
2. 第三方候选必须经过来源固定、许可证、来源证明、安全、可移植性、重叠、适配和
   验证；批准前只留在来源、准入、选择和审计层，不得进入执行路径；
3. 只有 `status=approved` 的精选批准 Skill 才能进入 `skills/` 和清单。在 schema 1
   中，`registry/skills.json` 是批准发布清单，而不是候选积压。

仓库自制的缺口补位 Skill 只是候选来源，不是第四个发布层，也不是平台、运行时或厂商
第一方基线。它必须先有剩余缺口证据、替代方案比较、设计来源与许可证说明，并通过安全、
可移植性、重叠、验证和 owner 批准；在通过同一精选准入边界前始终不可执行。

配置仓拥有的 `capability-router` 是“能力决策路由器”，不是尽量选择 Skill 的
skill-router。候选决策包括原生推理、官方或运行时能力、精选 Skill、外部能力元数据、
Recipe/DAG、请求人工确认和无需 Skill。第三方候选不是可执行路由目标；高风险、歧义、
冲突、权限变化、写入、安装、删除、迁移、发布或回滚必须请求人工确认。

路由不只是任务入口的一次性判断。多步骤工作应在事件驱动的复判 checkpoint 重新评估：
阶段边界、新上下文、失败或阻塞、产生副作用动作前、切换能力类别前，以及最终验证前。
路由投影为这些 checkpoint 提供确定性策略输入；它不要求每个原子步骤都路由，也不证明
live 能力当前可用。

`capability-router` 是 **Codex 消费方**的能力决策机制，并非通用前置。调用链因消费 agent 而异：例如 Claude Code 每会话加载其指令文件、并将 Skills 与 MCP 工具直接呈现给模型，**不经 capability-router**。Codex 与 Claude 是第一批已刻画的消费链路，不是全部可能消费者。其它 agent 必须先形成证据化映射，才能在本仓描述其安装、路由或恢复行为。本仓只在结构上命名机制，保持 agent 中立、开放、兼容，**不得为任何单一 agent 的链路写死**。

Schema 2 的运行时覆盖通过结构契约保持产品中立：`runtime-resolved` 能力必须携带
`runtimeResolution: visible-capability-inventory`。该字段只命名解析机制，不命名产品、
厂商、所有者，也不假定任何 live 能力存在；消费者必须探测当前可见且已授权的能力清单。

## 目录结构

- `skills/`：精选批准的可移植 Skill 正文；
- `sources/`：不可变来源锁、许可证、选择和哈希；
- `registry/`：人工维护的拓扑与发布清单权威；
- `policies/`：准入、可移植性、安全、重叠和生命周期规则；
- `audits/`：来源级审查与证据；
- `docs/decisions/`：已经接受的治理决策，用于约束后续 contract 变更；
- `docs/official-external-capability-baselines.md`：官方外部能力基线的通用处理规则；
- `docs/anthropic-official-skills-coverage.md`：第一份官方基线实例的带日期覆盖矩阵；
- `docs/mvp02-preflight-readiness.md`：已被 bounded owner 批准消费的 MVP-02
  preflight 历史记录；
- `docs/mvp02-post-approval-execution-plan.md`：窄范围适配草案步骤的已执行计划；
  已停在 release 或 runtime 闸门之前；
- `docs/mvp02-adapted-draft-review.md`：非运行时适配草案审查证据；不是批准
  payload、不是路由、也不是 live install；
- `docs/mvp03-release-or-routing-preflight.md`：下一闸门预检与授权请求；不是
  release、routing、manifest 或 runtime 批准；
- `docs/mvp03-release-or-routing-review-template.md`：仅模板的候选审查契约；只有
  owner 批准后才能使用，不是候选裁决；
- `docs/mvp03-release-or-routing-approval-request.md`：MVP-03 候选审查的正式
  owner 授权请求；现在已被 bounded approval event 消费；
- `docs/mvp03-release-or-routing-candidate-review.md`：MVP-03 逐候选处置证据；
  不是 approved payload、不是 manifest、不是 routing，也不是 live install；
- `docs/mvp03-release-routing-execution.md`：owner 批准后的后续闸门；将两个
  候选合并进现有 approved Skill payload，将 `spec-driven-development` 建模为
  recipe/routing projection，并把 runtime install proof 交给消费仓执行；
- `docs/mvp06-lifecycle-feedback.md`：来自已验证消费仓安装结果的生命周期反馈，
  包含资源雷达去重元数据，以及下一批前先暂停观察的决策；
- `registry/program-acceptance-map.json`：稳定的战略目标、验收、验证和证据关系，
  并记录诚实的当前评估；
- `docs/curation-program-plan.md`：机器计划的人类投影、战略基线、交付生命周期和
  当前阶段收官对账状态；
- `docs/curation-harness-model.md`：持续策展闭环、首个末端 MVP、分层可靠性、
  多 Agent 消费边界和标准候选边界；
- `docs/round-lifecycle-contract.md`：迭代式策展轮次的计划、执行、验收和阶段性
  收官契约；
- `docs/round02-candidate-review-2026-07-02.md`：round-02 逐来源候选处置证据；
  不是 approved payload、不是 manifest、不是 routing，也不是本地 runtime sync；
- `docs/round02-obsidian-adaptation-gate.md`：Obsidian 子批次适配草案闸门；
  记录 open-format、CLI 与 Defuddle 处置，但不批准 payload、routing、manifest 或本地 sync；
- `docs/round02-pm-execution-adaptation-gate.md`：PM AI-shipping 与执行文档
  适配草案闸门；analytics、market/GTM、discovery、legal/privacy、script/tooling 组另行审查；
- `docs/round02-pm-analytics-adaptation-gate.md`：PM analytics 与 data-safety
  适配草案闸门；记录 analytics runtime-equivalence 与 synthetic data/SQL tooling
  处置，但不批准 payload、routing、manifest、执行或本地 sync；
- `docs/round02-pm-market-discovery-adaptation-gate.md`：PM market 与
  product-discovery 适配草案闸门；记录 strategy evidence 与 discovery research
  处置，但不批准 payload、routing、manifest、外部调研、参与者数据处理或本地 sync；
- `docs/round02-pm-toolkit-boundary-adaptation-gate.md`：PM toolkit 高边界
  适配草案闸门；记录 legal/privacy reference 与 personal-document/copyediting
  处置，但不批准 payload、routing、manifest、法律/合规声明、简历数据处理或本地 sync；
- `docs/round02-huashu-design-guidance-adaptation-gate.md`：Huashu design
  guidance 适配草案闸门；记录 design-direction 与 brand-asset provenance
  处置，但不批准 payload、routing、manifest、工具链、打包资产、外部媒体生成或本地 sync；
- `docs/round02-huashu-toolchain-media-adaptation-gate.md`：Huashu toolchain
  与 media 适配草案闸门；记录 HTML deck/export、voiceover/TTS 与打包资产再分发边界，
  但不批准 payload、routing、manifest、依赖安装、生成媒体、资产复用或本地 sync；
- `docs/round02-release-readiness-review.md`：Round-02 GitHub 侧 readiness
  review；汇总 3 个已审查来源和 7 个子闸门，但不批准 release payload、routing、
  manifest 变更、发布或本地 sync；
- `docs/round02-release-admission-review-template.md`：未来 owner 批准后才可使用的
  Round-02 release/admission review 模板契约；不是候选裁决，也不批准 payload、
  routing、manifest、install、发布或本地 sync；
- `docs/round02-release-admission-approval-request.md`：进入 Round-02
  release/admission 审查阶段所需的最小正式授权请求；现在已被有界 approval event
  消费，但仍阻断 payload、manifest、routing、live install、发布和本地 sync；
- `docs/round02-release-admission-candidate-review.md`：Round-02
  release/admission 候选逐项 disposition 证据；不是 approved payload、manifest、
  routing、publication 或本地 sync；
- `docs/round02-release-execution-approval-request.md`：下一道 GitHub-only
  approved-payload 与 routing 提案 gate 的正式授权请求；排除 adapter runtime、
  reference-only 晋升、已拒绝资产、发布、live install 和本地 sync；
- `docs/round02-approved-payload-routing-proposal-template.md`：未来 owner 批准后才可使用的
  Round-02 approved-payload/routing proposal 模板契约；不是 release execution，
  也不是本地 sync；
- `docs/round02-approved-payload-routing-proposal.md`：owner 已批准的 GitHub-only
  执行记录；准入 Obsidian 开放格式 payload，合并有边界的 Round-02 改进，更新
  routing/manifest/generated 投影，并继续阻止本地 sync；
- `docs/round02-local-runtime-sync-approval-request.md`：将已验证的 Round-02
  release payload 同步到本地 cc-switch、agents 和 Codex Skill 目录前所需的最小
  有界授权请求；不是 sync approval，也不是本地写入；
- `docs/round02-local-runtime-sync-execution.md`：已记录的本地 runtime sync
  执行结果；将 cc-switch hash 对齐到 Round-02 manifest，并记录 agents 与 Codex
  使用 Junction fallback 链接；
- `docs/round02-stage-closeout-review.zh-CN.md`：Round 02 逐项收口决策包；建议关闭
  本轮并暂停，先重基线 Round 03，但它本身不关闭轮次，也不授权远端推送；
- `docs/starred-capability-source-discovery.md`：用户 star 发现面的初筛，用于后续候选来源、
  基线、索引和排除项治理；
- `LICENSE`、`NOTICE` 与 `THIRD_PARTY_NOTICES.md`：仓库许可证、归属声明和第三方 Skill notice；
- `CONTRIBUTING.md`、`CODE_OF_CONDUCT.md` 与 `SECURITY.md`：公开贡献、社区协作和安全报告边界；
- `docs/license-policy.md`：仓库自有代码、文档、生成投影、第三方 Skill 正文和官方基线的分层许可证策略；
- `docs/public-private-boundary.md`：公开/私有发布边界和用户配置模板指引；
- `docs/sustainability.md`：成本姿态、赞助边界与 free-first 纪律；
- `generated/`：确定性派生投影，不是第二真相源；
- `registry/routing.json` 与 `registry/scenarios.json`：批准路由元数据和 105 场景
  结构化策略语料；
- `release-manifest.json`：批准 payload 的精确路径、大小和哈希；
- `scripts/`：只负责验证和确定性投影生成。

## 验证方式

```bash
python -B -m unittest discover -s tests -v
python -B scripts/build_release_manifest.py --check
python -B scripts/build_topology.py --check
python -B scripts/simulate_routing.py --all
python -B scripts/verify.py
```

验证覆盖 registry 契约、引用、派生文件一致性、来源证据、精确 payload、输入绑定的
路由投影、全部 27 个生命周期节点和 105 个确定性对抗场景。自然语言理解仍由 Agent
负责；模拟器验证归一化后的策略决策，不伪装成关键词分类器。它不会安装 Skill。

## 更新规则

每个上游版本都必须作为新的不可变准入：固定版本、保存许可证和来源证明、审查可执行
面、评估安全/可移植性/重叠、最小适配、验证、更新拓扑，最后才批准新的发布清单。
候选裁决可以是 `merge`、`adapter-only`、`recipe-only` 或 `reject`，但这些裁决本身
不等于运行时批准。

官方外部能力基线可以用于覆盖关系对照，但任何适配都仍需经过许可证、来源证明、安全、
可移植性、重叠和中立化审查。source-available 或 all-rights-reserved 的官方内容只能
作为 reference，除非另有明确授权路径。

用户 star 的仓库可以作为发现入口，但 star 不等于批准。一个来源可能被归类为官方基线、
第三方候选、发现索引、外部能力元数据、仅 reference 或 reject；在正常准入流程闭环前，
不得进入 `skills/`、manifest、generated routing projection 或 live 执行路径。

`resource-radar` 可以建议第三方 Skill 或能力来源。这些建议在本仓完成 intake、审查、适配、
验证、拓扑更新和 release-manifest 更新前，始终只是 advisory。

## 安全边界

- `generated/` 只是 registry 真相的派生投影；
- 候选内容或带日期的重叠证据不得被描述为已经安装或可以执行；
- 跨 Agent 可移植性不得削弱权限、安全、证据、许可证或真实环境限制；
- 安装、账号连接、外部写入和信任边界变化由消费者侧处理，并需适用的授权。

## 公开发布状态

本仓按公开安全原则设计，但公开可见不等于降低发布闸门。第三方再分发边界、来源证明、
私有 overlay 排除和赞助入口仍由仓库所有者作为发布决策单独控制。仓库自有代码和治理机制
采用 Apache-2.0；仓库自有文档和公开治理文本按
[`docs/license-policy.md`](docs/license-policy.md) 的分层策略治理。当前路径不需要 GitHub Pro
或 Team；只有当私有 Actions 分钟、组织治理或多人审查确实需要时，才考虑升级。
