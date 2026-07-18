# CC Switch `handoff` 真实金丝雀执行——2026-07-18

## 结果

经用户授权，本次单 Skill 金丝雀通过 CC Switch 自身的来源下载、卸载备份、安装和投影
路径，把 `local:handoff` 转换为
`mattpocock/skills:skills/productivity/handoff`。Skill 总数保持 248，来源从 5 增至 6，
仍只对 Claude 和 Codex 启用。目标树精确采用 CC Switch 从 GitHub archive 得到的
`SKILL.md` 与 `agents/openai.yaml` 字节。

变更前已关闭 CC Switch。一致性数据库备份、独立 Skill 副本和前态清单保留在
`C:/tmp/cc-switch-handoff-canary-20260718`；CC Switch 还生成了可被自身恢复功能读取的
本地备份 `20260718_071018_handoff`。

## 失败关闭修正

第一次尝试被哈希闸门拒绝，因为预览使用 Windows Git checkout 的 CRLF 工作树字节，
而 CC Switch 实际安装 GitHub archive 的 LF 字节。闸门自动回滚来源登记、Skill 正文和
投影。随后证明两版在忽略换行差异后完全一致，按前态恢复原数据库元数据，并在不放宽
任何语义或安全检查的情况下，用 archive 字节哈希完成第二次执行。

## 后态与更新验证

其余 247 条 Skill、原有 5 条来源以及另外 14 张数据库表逐行不变。Claude、Codex 路径
仍是指向 CC Switch SSOT 的符号链接。CC Switch 来源更新检查没有为 `handoff` 报告更新，
证明新的来源身份和安装哈希已经进入真实更新链路。

同一次全局检查还报告 20 个其他更新信号，全部来自 `larksuite/cli`，本次没有执行任何
一个。它们进入候选复核通道，必须先固定来源 revision，并经过安全、质量、优劣、重叠、
冗余、重名和消费者影响审查。

## 后续同步与尚未越过的边界

用户随后授权 CC Switch 正常执行 WebDAV 同步。CC Switch 当前正在运行，并报告在
`2026-07-18T19:17:44+08:00` 完成本地同步。同步后审计确认来源型 `handoff` 身份、
精确正文、投影、无关 Skill 行和来源行均保持完整。观察到的运行态变化包括移除
`fetch`、`sequential-thinking`、`time` 三个 MCP 行、追加代理请求日志和推进会话日志
同步；用户已接受正常同步行为。

新会话 Skill 调用和跨设备内容相等性仍待验证。前态检查读取了含秘密的设置文件；秘密
没有写入仓库证据，仍建议在服务端另行轮换该凭据。

本次没有变更其他 Skill、Hook、MCP、Plugin、App、指令载体、消费者仓库、Git 提交或
远端 Git 状态。

机器证据：
`registry/cc-switch-handoff-real-canary-execution-2026-07-18.json`。
