# CC Switch 真实来源与所有权对账——2026-07-18

已接受的方向仍然成立：复用 CC Switch 做运行管理，不再自研 Manager。但当前真实投影
尚未达到“来源保真、可按上游更新”的目标状态。

## 只读发现

共享 Agent Skill 根目录共有 73 个目录。其中 43 个解析到 CC Switch Skill 存储：
42 个符号链接、1 个目录联接。剩余 30 个是实体目录：27 个由 Lark schema 3 锁文件
声明；`capability-router`、`closure-contract`、`intent-contract` 与固定版本的
`codex-user-config` 完全一致。

真实 CC Switch 数据库包含 248 条 Skill 和 5 条来源仓记录。`enabled_codex` 标志不能
直接证明共享目录投影：248 条都被标记启用，但共享目录里只有 43 个 CC Switch 目标。
这 43 个当前目标中，42 个是 `local:*` 数据库记录，0 个带来源仓记录；
`obsidian-open-format-knowledge-files` 甚至没有对应数据库行。

旧 curated 事务声称的 19 个 Skills 全部符号链接到 CC Switch，并与本仓当前发布正文
逐目录完全一致。它们在 CC Switch 中全部是没有 Git 来源元数据的本地记录；这些正文是
两个已固定上游家族的审查后适配衍生物，不是上游逐字节原文。因为当前 curated 发布已经
越过旧事务版本，所以 19 个都与旧事务清单不同。

## 权威结论

CC Switch 的运行分发已经得到真实观测，但真实来源保真尚未成立：43 个当前投影中，
来源仓记录为 0。在逐个完成迁移审查前，本仓当前发布仍是这 19 个历史适配衍生物的正文
权威；CC Switch 拥有当前存储、启用和链接控制，但不拥有缺失的上游来源证明。

旧 curated 事务降级为历史安装、备份和路由证据；它不是当前正文权威，也不授权越过
CC Switch 链接执行回滚。未知、外部或生态管理内容继续默认冻结。

`acceptance.cc-switch-source-preserving-skill-pool` 从 `verified` 降为 `partial`：
策略和运行复用已经验证，真实来源迁移尚未验证。消费者映射与外部管理能力共存也继续
保持部分完成。

后续逐 Skill 的只读迁移复核已经为 19 个历史衍生物给出有边界的处置建议。独立的
CC Switch 可丢弃预览又验证了来源仓状态、冲突拒绝、选择性投影、备份、恢复和迁移快照
契约，同时发现上游 Windows 测试隔离缺陷：Skill 服务有 5 组路径绕过了
`CC_SWITCH_TEST_HOME`。只在解压源码中做诊断性修正后，上游 7 个 `skill_sync` 测试
全部通过。这仍不证明真实来源网络更新或真实迁移。

下一安全门是网络受控的可丢弃更新夹具，或另行精确授权的单 Skill 金丝雀迁移，并绑定
备份和回滚。本次对账与预览均未修改真实 CC Switch、Skill、Agent Home、Hook、事务、
备份、仓库、提交或远端。
