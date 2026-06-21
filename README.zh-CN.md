# Agent Skills Curated

[English](README.md)

这是一个私有、跨 Agent 的 Skills 权威仓库，负责保存经过审查的 Skill 正文、来源、
重叠裁决、协作关系、安全证据和确定性的发布清单。

## 仓库职责

本仓库负责 Skills 及其治理，不负责用户配置、认证、运行时记忆、Plugins、Apps、
MCP 账号状态或安装权限。

`codex-user-config` 是启动与安装权威，只消费本仓库一个固定且已审查的版本：

```text
codex-user-config
  → 校验精选仓固定版本和发布清单
  → 规划、备份、安装、验证或回滚受管 Skills
agent-skills-curated
  → 保存 Skill 正文、来源、拓扑和发布证据
```

依赖保持单向；精选仓不会反向修改配置仓或在线 Agent 环境。

## 当前批准清单

当前发布包含 34 个 Skills、60 个文件：

- 29 个此前已经审查和中立化的本地 Skills，完整保存以支持跨环境迁移；
- 从 `addyosmani/agent-skills` 适配并新增 5 个能力：CI/CD、弃用迁移、
  可观测性、性能优化和生产发布。

其余 19 个上游 Skills 均有明确的合并、仅适配、仅配方或拒绝裁决。上游 Hook、
命令适配器、persona、脚本、CI、marketplace 配置和全局路由器均未进入安装面。

## 重叠与路由

语义相交并不可怕，未明确所有权才可怕。每个明显冲突组都在
`registry/conflicts.json` 中声明唯一默认所有者、适用条件和局部替代方案：

- `capability-router` 是唯一全局路由器；
- 精选 `tdd`、`diagnose`、`review` 是通用默认；
- 插件 Skills 只在明确进入对应插件工作流时生效；
- Codex Security 负责安全扫描，Product Design 负责产品设计，浏览器能力负责真实
  运行时控制。

不会再安装第三套 TDD、调试、评审、规划、前端、Git、安全或路由流程。

## 动态拓扑

Git 中的 `registry/` 是权威数据源，`scripts/build_topology.py` 生成目录、JSON
拓扑、Mermaid 图和场景路由表。稳定 ID 不受改名影响；关系覆盖顺序、条件、输入
输出、验证、协作、替代、回退、冲突和淘汰；复杂协作用条件化 Recipe/DAG 表达。

Neo4j 等图数据库以后可以消费生成结果，但不能成为第二份手工真相。

## 来源和安全边界

Addy 上游固定在提交 `17214a29c429a19f7a9607f2c06f9d650ea87eb0`，并保存
原始/适配哈希、MIT 声明、24 项裁决、安全报告、可移植性报告和重叠报告。

首版不包含任何上游可执行文件。安全验收发现的高风险 Hook 和 CI 面均不属于
五个新增 Skills 的必要依赖。“跨 Agent 通用”只移除不必要的产品耦合，不移除
安全、授权、许可证、证据或真实环境限制。

## 验证与更新

```bash
python scripts/build_topology.py --check
python scripts/verify.py
```

每次上游更新都必须作为新的不可变 intake：固定提交、审查差异和可执行面、重跑
安全/可移植性/重叠检查、更新全部裁决、逐个适配、重建拓扑和哈希，再发布新版本。

安装、备份和回滚由 `codex-user-config` 单向负责。
