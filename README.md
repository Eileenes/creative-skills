<div align="center">

# Creative Skills

### 从一张参考图，到你的头像、角色与内容。

为 AI 助手准备的创作技能合集：制作立体头像、Q 版角色卡、系列插图与宣传短片。<br />
8 个独立技能，按需安装；保留角色设定，让后续创作有据可循。

![Skills](https://img.shields.io/badge/skills-8-6366F1?style=flat-square)
![Images](https://img.shields.io/badge/image_skills-4-F59E0B?style=flat-square)
![Video](https://img.shields.io/badge/video_skills-4-EC4899?style=flat-square)
![Format](https://img.shields.io/badge/entry-SKILL.md-334155?style=flat-square)

**[下载合集](https://github.com/Eileenes/creative-skills/archive/refs/heads/main.zip)** · **[快速开始](#quick-start)** · **[选择技能](#skills)** · **[图片指南](docs/image-workflows.md)** · **[完整文档](docs/skill-guide.md)**

</div>

---

## 能做什么

| 头像与形象 | 角色与配图 | 宣传与视频 |
| --- | --- | --- |
| 照片转软陶、立体或 3D 卡通头像 | 人物、宠物、品牌角色设定 | 账号、网站与产品宣传片策划 |
| 配饰、背景与连续局部修改 | 三视图、表情、透明立绘 | 体素吉祥物与主页立体动效模板 |
| 指定像素尺寸导出 | 文章封面、Banner、教程插图 | 分镜、动画配置与渲染流程 |

每个技能提供创作流程、提示词或辅助工具。**实际出图需要宿主的图像生成／编辑能力；视频制作需要相应素材与渲染环境。** 安装合集不会自动安装模型或提供 API 额度。

<a id="quick-start"></a>

## 快速开始

### 1. 下载并选择技能

下载上方 ZIP 并解压，或者克隆仓库：

```bash
git clone https://github.com/Eileenes/creative-skills.git
cd creative-skills
```

首次使用可以从 `avatar-depth` 开始。无需安装即可让能读取本地文件的助手执行：

> 请读取这个仓库的 `skills/avatar-depth/SKILL.md`，按其中流程，把我上传的照片做成 800×800 的软陶头像，保留发型和眼镜，米白背景。

### 2. 长期使用时，安装整个技能目录

以 Codex 的默认用户技能目录为例，在合集根目录执行：

```bash
mkdir -p "$HOME/.codex/skills"
if [ -e "$HOME/.codex/skills/avatar-depth" ]; then
  echo "已有 avatar-depth，请先备份并比较版本"
else
  cp -R skills/avatar-depth "$HOME/.codex/skills/"
fi
```

其他技能使用下表中的对应目录。其他宿主使用各自的技能目录；如果未识别新技能，可重新打开会话或直接提供 `SKILL.md` 路径。**复制整个技能文件夹**，保留其参考资料和脚本。[已有安装的更新方法 →](docs/image-workflows.md#安装)

### 3. 上传参考图，说清目标

```text
使用 $avatar-depth，把这张头像做成软陶风，输出 800×800 PNG。

使用 $chibi-character-card，把这只猫做成角色卡，包含三视图和六种不同表情。

使用 $personal-ip-kit，为我的角色建立档案，再做一张文章封面和两张正文插图。
```

只需要一个技能就安装一个；同一角色的连续创作，请同时提供已接受的参考图和版本。

<a id="skills"></a>

## 选择技能

### 头像、角色与图片

| 技能 | 适合什么需求 | 主要交付 |
| --- | --- | --- |
| [**avatar-depth**](skills/avatar-depth) | 制作或修改一张立体、软陶、卡通头像 | 指定尺寸头像、局部修改与导出 |
| [**chibi-character-card**](skills/chibi-character-card) | 把人物、动物或 Logo 转成 Q 版设定 | 三视图、六种表情、细节与配色 |
| [**personal-ip-kit**](skills/personal-ip-kit) | 建立可持续使用的角色，为系列内容配图 | 角色档案、头像、立绘、表情、封面与插图 |
| [**soren-ip-illustrations**](skills/soren-ip-illustrations/SKILL.md) | 沿用 Soren 固定形象制作内容 | Soren 头像、表情、封面与教程插画 |

### 宣传与视频

| 技能 | 适合什么需求 | 模板／交付 |
| --- | --- | --- |
| [**profile-promo**](skills/profile-promo/SKILL.md) | 自由策划账号或网站宣传片 | 制作方案、分镜与时间线；具备环境后继续制作 |
| [**promo-video-director**](skills/promo-video-director/SKILL.md) | 体素吉祥物带观众浏览主页 | 默认 19 秒、720p、30fps 横屏模板 |
| [**x-profile-3d-promo**](skills/x-profile-3d-promo/SKILL.md) | 主页斜放、头像弹出、帖子立起 | 30 秒、1080p、30fps 横屏模板 |
| [**x-profile-3d-video**](skills/x-profile-3d-video/SKILL.md) | 通过集中配置制作 X 主页介绍片 | 可配置的 30 秒横屏模板；竖屏需适配 |

[查看每个技能的输入、步骤和示例 →](docs/skill-guide.md)

## 从角色到内容

**参考图 → 角色档案 → 头像／角色卡 → 封面与插图 → 宣传片**

用 `personal-ip-kit` 保存角色设定；按需用头像或角色卡技能扩展素材，再制作文章配图或交给视频技能策划。单张头像、角色卡、配图或视频任务均可独立开始。

技能之间没有自动数据同步，交接时需明确角色档案、参考图及已接受的成品。[查看完整图片工作流 →](docs/image-workflows.md)

## 使用条件与当前限制

| 场景 | 需要什么 | 当前状态 |
| --- | --- | --- |
| 图片创作 | 支持参考图的图片生成／编辑工具 | 技能不内置图像模型；无工具时只能整理提示词 |
| 头像导出、角色素材打包 | Python 3.10+、对应 `requirements.txt` 中的 Pillow | 辅助脚本及现有测试随技能提供 |
| 体素视频 | Three.js、浏览器、Python、FFmpeg、适用的 Onetake | Onetake 不随仓库分发；完整流程待端到端验证 |
| Remotion 视频 | Node.js、React/Remotion、浏览器、音频依赖、FFmpeg | 需替换示例和旧路径；完整渲染待端到端验证 |

- **角色一致性需要检查**：参考图与档案帮助保持特征，不保证每张图完全相同。
- **立体风格仍是图片**：头像和角色卡不等于可旋转、已绑定的三维模型。
- **横竖屏以代码为准**：`x-profile-3d-video` 的旧说明写竖屏，当前代码为横屏；详情见完整文档。
- **私人素材由使用者保存**：仓库不分发 Soren 私人参考图，也不附带用户照片、音色或凭据。

## 文档与维护

| 文档 | 内容 |
| --- | --- |
| [头像与图片指南](docs/image-workflows.md) | 安装、技能选择、角色交接、连续配图 |
| [技能详解与视频模板](docs/skill-guide.md) | 八个技能的详细用法、十份原始 ZIP 和模板限制 |
| [旧仓库迁移说明](docs/repository-migration.md) | 三个独立图片仓库的新入口、历史版本与更新方法 |
| [来源记录](SOURCES.md) | 导入版本、原始资料及整理边界 |

`avatar-depth`、`chibi-character-card`、`personal-ip-kit` 统一在本仓库维护，原技能名保持不变。`dsh-reel` 独立维护。

<details>
<summary><b>目录结构</b></summary>

```text
creative-skills/
├── README.md                 # 介绍、快速开始与选择指南
├── SOURCES.md                # 来源和导入版本
├── docs/                     # 图片流程、技能详解、迁移说明
├── skills/                   # 8 个可独立使用的技能
│   └── <skill>/
│       ├── SKILL.md          # 技能入口
│       └── ...               # 参考资料、脚本、素材或模板
└── sources/original-zips/     # 10 份历史资料快照
```

</details>

<details>
<summary><b>运行现有 Python 测试</b></summary>

在合集根目录建立虚拟环境，并安装两个技能的脚本依赖：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r skills/avatar-depth/requirements.txt -r skills/personal-ip-kit/requirements.txt
.venv/bin/python -m unittest discover -s skills/avatar-depth/tests -v
.venv/bin/python -m unittest discover -s skills/personal-ip-kit/tests -v
```

Windows 使用 `.venv\Scripts\python.exe`。测试覆盖头像尺寸与文件保护、角色管理和素材打包；不验证生图审美或视频成片质量。

</details>

遇到问题或想改进技能，可以[提交 Issue](https://github.com/Eileenes/creative-skills/issues)，注明技能名、宿主环境、操作步骤和预期结果；附图前请移除私人信息。

## 来源与授权

本仓库保留各来源的授权边界，**没有统一的全仓库许可证**。`avatar-depth` 保留 [MIT 许可证](skills/avatar-depth/LICENSE)；其余内容以各自来源说明为准，公开可见不等于获得额外授权。

原始 ZIP 是历史快照，不自动同步上游。Onetake、平台标识、音乐和参考素材分别遵循其许可条件；Soren 形象与品牌需获得相应授权。[查看来源与整理记录 →](SOURCES.md)
