# 创意视频与个人 IP 技能库

用于 Agent 的宣传视频、头像和角色 IP 技能合集。每个 `skills/<名称>/` 是一个独立技能，可按需安装；原始压缩包保留在 `sources/original-zips/`，用于追溯，不是默认安装入口。

## 技能一览

| 技能 | 用途 | 状态与注意事项 |
| --- | --- | --- |
| [profile-promo](skills/profile-promo/) | 通用主页宣传动画的策划、分镜和制作 | 工作流技能，按项目选择渲染工具 |
| [promo-video-director](skills/promo-video-director/) | X、小红书、公众号、网站的体素吉祥物宣传片 | 19 秒横版模板；按需使用外部 Onetake，见下方授权说明 |
| [x-profile-3d-promo](skills/x-profile-3d-promo/) | 3D 主页介绍视频，横屏版本 | 原始实现含具体账号示例与沙盒环境假设，使用前改为自己的资料 |
| [x-profile-3d-video](skills/x-profile-3d-video/) | X 主页 3D 风格介绍视频，竖屏版本 | 原始实现含具体账号示例与沙盒环境假设，使用前改为自己的资料 |
| [personal-ip-kit](skills/personal-ip-kit/) | 从参考图建立独立角色档案，并复用到内容创作 | 通用技能，参考图由使用者提供 |
| [avatar-depth](skills/avatar-depth/) | 把照片或头像处理为立体风格头像 | 原技能附带 MIT 许可证 |
| [chibi-character-card](skills/chibi-character-card/) | 将人物、动物或设计制作成 Q 版角色卡 | 通用技能，参考图由使用者提供 |
| [soren-ip-illustrations](skills/soren-ip-illustrations/) | 基于 Soren 固定形象制作插图 | 专属角色技能；需自行提供已授权的原图和角色设定板 |

两个 X 技能是不同版本，分别保留；`promo-video-director` 中已整合 X、小红书、微信、网站、参考视频分析、沙盒设置与体素角色模块，避免再安装一组重复入口。23.5 秒弹出展示模板尚未整合成独立可安装技能，保存在 `sources/original-zips/make-popup-showcase-video.zip`。旧包中的说明、自动安装脚本和示例具有原环境假设，不保证安全或兼容，请先审阅再运行。

## 安装

克隆仓库后，将需要的整个技能目录复制到 Agent 的技能目录，例如 Codex：

```bash
git clone https://github.com/Eileenes/creative-skills.git
mkdir -p ~/.codex/skills
cp -R creative-skills/skills/personal-ip-kit ~/.codex/skills/
```

先检查目标目录是否已有同名技能，避免覆盖；也可改成其他技能目录名。不要只复制 `SKILL.md`，因为技能可能依赖旁边的脚本和参考文档。各技能的运行时依赖、素材和外部服务并不会随安装自动获得。Soren 专属技能的参考图片未公开，请在使用时自行提供。

## 运行和授权说明

本仓库保留各来源的许可状态，不给所有内容统一附加许可证。`avatar-depth` 的 [MIT 许可证](skills/avatar-depth/LICENSE) 仍然适用于该部分；其他未注明许可证的内容不因此获得额外授权。宣传模板使用外部 Onetake 时，需自行遵守适用版本的许可，详见 [依赖与授权](skills/promo-video-director/references/dependencies-and-license.md)。公开的 Soren 角色描述不等于授予他人使用该人物形象或品牌的权利。素材、平台标识、音乐等也需分别确认使用权。

旧 X 视频实现使用特定沙盒、浏览器与 Remotion 环境；宣传视频总技能的完整渲染、旧包中的脚本与跨平台抓取尚未在本仓库端到端验证。原始包和具体账号示例是历史资料，不应直接作为他人的个人数据使用。

来源、版本与整理边界见 [SOURCES.md](SOURCES.md)。
