# GitHub 仓库配置证据

## 远端结果

2026-07-18 已确认 `yiheng8023/agent-skills-curated` 是以 `main` 为默认分支的
公开仓库，Issues、Projects、Discussions 已开启，Wiki 已关闭；仓库描述和 7 个
项目主题已经配置。合并策略与 `home-edge-bootstrap-public` 一致，本次没有改动
合并行为。

以下安全功能已通过 GitHub 官方 API 启用并回读：

- Vulnerability Alerts；
- Dependabot Security Updates，且未暂停；
- Secret Scanning；
- Secret Scanning Push Protection；
- 私下漏洞报告；
- CodeQL 默认设置。

CodeQL 已为 `actions` 与 `python` 返回 `configured` 和每周计划。首轮两份分析
已经针对远端 `main` 的精确 revision
`d0955bf7f7852b53955f843b20c69709b31459be` 完成：17 条 Actions 规则和 43 条
Python 规则均产生 0 个结果，告警 API 也返回 0。该结果只覆盖这个远端 revision，
不覆盖尚未推送的本地工作区。

## 社区与赞助边界

本地已经准备 PR/Issue 模板、支持文档、赞助文档和 `.github/FUNDING.yml`，但因
本任务不提交、不推送，它们尚未发布。GitHub 社区健康度因此仍为 85%，没有达到
参考仓的 100%；这是预期的本地/远端分离，不是模板生成失败。

赞助入口使用仓库所有者公开的 PayPal 链接，并引用参考仓中同一所有者公开的微信
与支付宝素材。赞助完全自愿，不购买 SLA、评审或发布优先级、治理例外或技术影响力。

## 验证边界

这是带日期的快照。GitHub 设置可能漂移，未来声称当前状态前必须重新查询。社区
健康度闭合需要另行授权提交和推送，再重新读取 profile；CodeQL 绿色状态必须绑定
被声明的精确 revision。当前结果覆盖远端 `main` 的 `d0955bf...`，本地领先 12 个
提交且仍有未发布改动，不能继承该结果。

本次没有发布仓库文件，没有修改分支规则或 Release，没有扩大认证 scope，也没有
修改 Agent、Hook、消费方或其他仓库。
