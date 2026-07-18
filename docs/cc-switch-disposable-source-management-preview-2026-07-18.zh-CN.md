# CC Switch 一次性来源管理预览 — 2026-07-18

## 结论

CC Switch 3.17.0 仍足以作为运行期 Skill 管理器候选。在一次性源码副本中，来源登记、来源启停、异源同目录冲突、选择性投影、备份、恢复和迁移快照合同均已通过；这既不授权真实迁移，也不证明真实迁移已经完成。

原版 Windows 测试边界存在缺陷：中央配置路径会识别 `CC_SWITCH_TEST_HOME`，但 Skill 服务仍有五处直接调用 `dirs::home_dir()`。因此未修改的测试套件出现一个真实失败，后续四项只是互斥锁中毒。仅在 `C:/tmp` 的诊断副本中把这些路径改为中央 home 解析后，官方七项 `skill_sync` 测试全部通过；本任务补充的一项一次性合同测试也验证了来源登记、禁用/启用持久化，以及在下载前返回 `SKILL_DIRECTORY_CONFLICT`。

## 证据边界

- 官方基线：`farion1231/cc-switch` 标签 `v3.17.0`，提交 `3d176b98cc0bfd151a42882e88ab59b62083b92f`。
- 下载的源码归档 SHA-256 为 `82273F854AB6C969BEC61AA9FB2BFFAB870B2988513071BCA18B3CDEEDFED947`。
- 临时隔离补丁与合同测试均未写入已安装产品或上游仓库。
- 真实共享 Skill 目录在测试前后的树哈希完全一致。
- 桌面进程锁定了真实数据库，因此不声称取得了整库前后哈希。

## 后续闸门

验收仍为 partial：当前活动投影仍没有来源仓记录，也没有运行来源型网络更新。真实 canary 需要单独授权，并绑定精确来源、备份、冲突、回滚和事后核对。原版 Windows 隔离缺陷如需向上游提 issue 或补丁，也属于另一次外部写授权。

后续回环来源更新夹具补齐了可丢弃成功路径，但同时确认 `update_skill` 不是原子事务，
并发现第二个 Windows 测试 Home 优先级缺陷。详见
`registry/cc-switch-disposable-source-update-and-recovery-review-2026-07-18.json`。

机器证据：`registry/cc-switch-disposable-source-management-preview-2026-07-18.json`。
