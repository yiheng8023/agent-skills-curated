# Agent Capability Manager 基础切片实现证据

## 结论

`C:/Projects/agent-capability-manager` 已实现并在本地验证
`disposable-root-transaction-closure`。这证明的是可丢弃临时根内的事务安全
基础，不是完整生产 MVP，也不授权真实 Agent 配置写入。

## 已证明的链路

```text
inspect -> ownership -> plan -> lock -> backup -> apply
        -> verify -> receipt -> rollback / recover
```

- 计划只持久化意图，不创建目标文件。
- 外部或未知所有权阻止覆盖。
- apply、rollback、recover 共用目标锁。
- 计划、根身份、备份和前置摘要漂移均失败关闭。
- apply 与 rollback 的破坏性窗口都有持久恢复状态。
- SQLite journal 由触发器保证只追加。
- CLI 与 Rust 核心对同一检查产生完全一致的 JSON 决策。
- Windows Junction、大小写别名、锁文件和替换失败均有负向夹具。

## 最终验证

- Rust/Cargo 1.97.0 GNU：格式、34 项集成测试、Clippy 全部通过。
- 最低 Rust/Cargo 1.93.1 GNU：格式、同一组 34 项集成测试、Clippy
  全部通过。
- `cargo-deny 0.20.2`：advisories、bans、licenses、sources 全部通过且
  无白名单冗余警告。
- `cargo-audit 0.22.2`：扫描 76 个锁定依赖，未报告漏洞。
- `actionlint 1.7.12`：GitHub Actions 工作流语义检查通过。
- CI 固定 `actions/checkout` v6.0.2 与 `cargo-deny-action` v2.1.1 的完整
  提交 SHA，并固定 `cargo-audit 0.22.2`，不依赖可移动大版本标签。
- `Cargo.lock` SHA-256：
  `42daa3d866c107a8f7db2420e3a992fa60d63fae907bacbd86b629d36f507772`。

## 仓库与权限状态

- 分支：`main`。
- 提交：尚无提交。
- 远端：未配置。
- 未写真实 Codex、Claude、CC Switch 或其他 Agent 配置。
- 未改 Hook，未连接账号或遥测，未执行第三方 Skill，未提交、创建远端或
  推送。

Ubuntu CI 已在仓库中定义，但在没有另行授权提交和远端运行前尚未执行，
因此本记录不把“CI 配置存在”升级为“远端 CI 已通过”。

## 下一道门

下一阶段仍需单独确定真实 Agent 适配器的目标、权限、配置所有权、迁移、
回滚、平台夹具和验收面。在该门通过前，基础核心不得写入真实 Agent home。
