# 用户星标新增来源预检

日期：2026-07-18
机器证据：`registry/user-starred-new-source-preflight-2026-07-18.json`

用户公开 GitHub 列表带来的 5 个新增来源，已对照当前 GitHub 元数据和本仓
既有证据完成预检。本轮没有下载、执行、安装或准入任何来源。

| 来源 | 当前角色 | 结论 |
| --- | --- | --- |
| `helloianneo/awesome-claude-code-skills` | 发现索引 | 作为非排他的线索表保留。它的评级和安装命令不是评审证据，每个子来源都要独立审查。 |
| `alchaincyf/huashu-design` | 单 Skill 加大型设计/媒体工具链 | 复用第二轮拆分结论，但当前版本已前进 10 个提交、变更 14 个文件；只在具体短板选中时做差量复核。 |
| `multica-ai/andrej-karpathy-skills` | 编码行为指导 | 仅作参考：内容有用但与现有链路高度重叠，而且 MIT 声明缺少根许可证文件和 GitHub 许可证元数据。 |
| `phuryn/pm-skills` | 68 个 Skill 的 PM 套件 | 复用第二轮套件拆分；当前版本前进 1 个提交、变更 27 个文件，不做整套准入。 |
| `vercel-labs/skills` | 跨 Agent 的 Skill CLI 与目录工具 | 只作为外部工具和路径映射基线，不是 Skill 正文候选；它与 CC Switch 重叠，不能借此复活已退役的自研 Manager。 |

这个结果不是继续盲目扩池，而是缩小下一步：去重索引中的子来源；只刷新
被具体短板选中的华枢或 PM 组件；把运营工具与 Skill 准入分开。当前有
2 个来源缺少完整的仓库级许可证证据，3 个来源的当前版本已经新于既有
评审证据。
