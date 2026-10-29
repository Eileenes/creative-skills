# 旧仓库迁移说明

头像与图片相关技能统一在 [Eileenes/creative-skills](https://github.com/Eileenes/creative-skills) 维护。技能名称、调用方式和独立安装能力保持不变。

## 保留与迁移

| 仓库 | 处理方式 | 新入口 |
| --- | --- | --- |
| `creative-skills` | 保留，作为统一维护入口 | [总目录](../README.md) |
| `avatar-depth` | 已有完整副本，可停止单独维护，建议归档 | [skills/avatar-depth](../skills/avatar-depth) |
| `chibi-character-card` | 已有完整副本，可停止单独维护，建议归档 | [skills/chibi-character-card](../skills/chibi-character-card) |
| `personal-ip-kit` | 已有完整副本，可停止单独维护，建议归档 | [skills/personal-ip-kit](../skills/personal-ip-kit) |
| `dsh-reel` | 继续独立维护，不参与此次整合 | [原仓库](https://github.com/Eileenes/dsh-reel) |

`soren-ip-illustrations` 已在合集内，没有需要移除的同名独立仓库。合集中的现有视频技能继续保留。

## 完整性核对

整理前逐一比对了三个独立仓库全部 Git 跟踪文件与合集对应目录，文件路径和内容完全一致；源提交见 [SOURCES.md](../SOURCES.md)。此次统一了 README 安装入口与使用指南，技能流程、辅助脚本、测试、参考资料及原有许可证均保留。

这次整合是文件与维护入口整合，未把旧仓库的 Git 提交历史、Issues 或 Releases 导入合集。检查时三个旧仓库没有开放的 Issues／PR；`avatar-depth` 和 `personal-ip-kit` 各有 `v1.0.0` Release，`chibi-character-card` 没有 Release。

建议归档三个旧仓库并保留迁移提示，这样历史版本与已有下载链接仍可访问。如果要彻底删除，应先另行备份 Git 历史、标签及 Release 附件，并更新外部安装链接；合集现有源文件副本不等于这些仓库元数据的备份。本次没有删除或归档任何仓库。

## 更新已有安装

从合集复制对应的完整技能目录；不要把整个合集克隆到原来的单技能目录。更新前保存个人改动和素材。具体步骤见 [安装指南](image-workflows.md)。
