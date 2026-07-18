# CC Switch `handoff` 真实金丝雀只读预览——2026-07-18

## 决策包

在本轮复核的 16 个现役上游原文替换候选中，`handoff` 是风险最低的第一只真实金丝雀。
它没有可执行面。相对当前本地正文，固定上游版本只增加
`disable-model-invocation: true`，把 `PRDs` 换成更通用的 `specs`，并新增 OpenAI
展示元数据且禁止隐式调用；没有删掉现有安全或能力分工边界。

固定来源为 MIT 许可的 `mattpocock/skills`，revision 是
`9603c1cc8118d08bc1b3bf34cf714f62178dea3b`。2026-07-18 观测时，远端 `main`
仍精确指向这个 revision。目标树只有 `SKILL.md` 和 `agents/openai.yaml`，没有脚本或
二进制文件。

第一次获授权执行按失败关闭中止后，本预览修正了目标哈希：Windows checkout 使用 CRLF
工作树字节，而 CC Switch 安装 GitHub archive 的 LF 字节；忽略换行差异后文件完全一致。
本次 CC Switch 事务以 archive 字节哈希为准，没有放宽语义或安全闸门。

## 前态与运行限制

真实条目是 `local:handoff`，只对 Claude 和 Codex 启用；两个消费目录都是指向 CC
Switch SSOT 的符号链接，解析后的 `SKILL.md` 哈希一致。真实数据库有 248 条 Skill、
5 条来源，尚未登记 `mattpocock/skills`。

数据库保存的本地内容哈希与当前 SSOT 不一致。由于它是本地行，这不会触发来源更新检查，
但它是真实前态漂移，迁移前不能静默“修正”。现有同名目录还会让来源安装失败关闭，
所以这是一笔“卸载—安装”的所有权转换，不是 `update_skill`。

CC Switch 只保存 `main`，下载的是会移动的 `refs/heads/main`，自身不能持久保存本次固定
commit。任何真实变更前都必须再次确认远端 `main` 仍等于已审 revision，否则中止。
自动更新继续禁止。

## 事务与回滚

变更前应暂停 CC Switch 写入，生成并验证可独立读取的数据库与 Skill 备份，重算真实
数据库行、目录树和投影哈希，并再次核对远端 revision。受限变更只会登记一个来源，
通过会生成备份的路径卸载 `local:handoff`，安装唯一的来源型 `handoff`，再只恢复原有
Claude、Codex 启用状态。

验收要求目标树哈希、来源型数据库行、符号链接投影全部精确命中，所有无关行不变，前态
备份持续可读。回滚只删除精确来源型行，恢复已验证的本地备份与原投影；只有确认没有其他
Skill 引用时才删除本次新增来源。数据库副本仅在写入仍暂停且应用级恢复失败时作为最后
手段，不能日常覆盖。

本文是当时供决策的只读预览。随后获授权的本地金丝雀另有独立执行证据；自动更新、外部
同步、提交和推送仍不属于本预览权限。

机器证据：
`registry/cc-switch-handoff-real-canary-readonly-preview-2026-07-18.json`。
