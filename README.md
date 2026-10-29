# Creative Skills · 头像、角色配图与宣传视频

把参考图、个人主页和品牌资料，变成角色素材、头像、插画与宣传短片。

本仓库收录 **8 个可独立使用的 Agent 技能**，以及 **10 份原始资料 ZIP**。每个技能以 `SKILL.md` 为入口，按需附带脚本、提示词、动画模板和制作规范。适合交给能够读取技能文件、操作素材和运行代码的 AI 助手使用。

**这是一套创作工具和工作流程，不是安装后自动出片的软件。** 图片需要可用的生图或编辑能力；视频需要素材、浏览器和相应渲染环境。视频模板尚未在本仓库完成端到端渲染验证。

## 快速选择

本仓库是 `avatar-depth`、`chibi-character-card`、`personal-ip-kit` 的统一维护入口，三个技能仍可独立安装和调用。Soren 专属配图也在这里维护。

[图片创作流程与安装指南](docs/image-workflows.md) · [旧仓库迁移说明](docs/repository-migration.md)

### 头像、角色与图片

| 你想做什么 | 选择哪个技能 | 主要交付 |
| --- | --- | --- |
| 建立一个以后可以持续复用的个人、宠物或品牌角色 | [personal-ip-kit](skills/personal-ip-kit/SKILL.md) | 角色档案、设定图、头像、表情、封面及后续内容素材 |
| 把照片或现有头像做成立体、软陶或卡通头像 | [avatar-depth](skills/avatar-depth/SKILL.md) | 指定尺寸的头像图片 |
| 把人物、宠物或 Logo 做成 Q 版角色设定卡 | [chibi-character-card](skills/chibi-character-card/SKILL.md) | 三视图、表情、细节和配色组成的角色卡 |
| 沿用 Soren 的固定形象制作教程配图 | [soren-ip-illustrations](skills/soren-ip-illustrations/SKILL.md) | 头像、表情、封面和 AI 教程插画 |

### 宣传视频

| 你想做什么 | 选择哪个技能 | 主要交付 |
| --- | --- | --- |
| 自由设计账号或网站宣传片的角色、剧情、时长和画幅 | [profile-promo](skills/profile-promo/SKILL.md) | 制作话术、分镜；条件具备时继续制作视频 |
| 套用“方块鲸鱼带你浏览主页”的模板 | [promo-video-director](skills/promo-video-director/SKILL.md) | 默认 19 秒、720p、30fps 横屏视频、预览与配置 |
| 做“主页斜放、头像跳出、帖子立起”的介绍片 | [x-profile-3d-promo](skills/x-profile-3d-promo/SKILL.md) | 30 秒、1080p、30fps 横屏模板与制作流程 |
| 用集中配置文件制作同类 X 主页介绍片 | [x-profile-3d-video](skills/x-profile-3d-video/SKILL.md) | 可配置的 30 秒模板；当前代码仍为横屏，竖屏需适配 |

另有一个 **23.5 秒作品封面立体弹出模板**，保存在 [make-popup-showcase-video.zip](sources/original-zips/make-popup-showcase-video.zip)，尚未整理为独立可安装技能。

## 下载与使用

### 1. 获取仓库

```bash
git clone https://github.com/Eileenes/creative-skills.git
cd creative-skills
```

也可以在 GitHub 点击 **Code → Download ZIP**，解压后使用。

### 2. 让助手读取一个技能

不安装也可以直接告诉助手：

> 请读取这个仓库的 skills/avatar-depth/SKILL.md，按里面的流程把我上传的照片做成软陶头像。

希望长期使用时，把需要的**整个技能目录**复制到助手的技能目录。不要只复制 `SKILL.md`，它可能引用同目录的脚本、模板或参考文件。以下以 Codex 的用户技能目录为例，从仓库根目录执行：

```bash
mkdir -p "$HOME/.codex/skills"
if [ -e "$HOME/.codex/skills/avatar-depth" ]; then
  echo "avatar-depth 已存在，请先比较或备份，不直接覆盖"
else
  cp -R skills/avatar-depth "$HOME/.codex/skills/"
fi
```

安装其他技能时替换目录名即可。不需要一次安装全部技能；如果当前会话未识别新技能，重新打开会话或直接提供 `SKILL.md` 路径。其他助手使用各自的技能安装位置。

### 3. 提供素材和目标

图片任务通常提供参考图、用途、风格和尺寸。视频任务通常提供四类信息：

- **主页资料**：平台、链接或截图、昵称、简介及要展示的作品。
- **角色**：头像、角色参考图、已有 IP，或说明不需要角色。
- **目标动作**：关注、订阅、访问网站、了解作品等。
- **规格**：时长、横竖屏，以及是否需要配乐、旁白或多平台版本。

资料抓取受限时，可以直接提供截图和文字。没有提供的粉丝数、认证状态或作品成绩，不应由助手编造。

## 每个技能怎么用

### personal-ip-kit：创建并持续复用自己的角色

**能做什么**：从人物、宠物、动物、植物或物品参考图建立独立角色，再用同一角色制作头像、表情、文章 Banner、正文插图和视频素材。多个角色分别维护，避免混用特征。

**需要什么**：角色参考图、本次用途，以及必须保留的特征；续作时提供已有角色档案或已接受的成品。

**怎么做**：查看参考图 → 提炼识别特征 → 建立角色档案与设定 → 生成所需素材 → 检查角色一致性 → 保存提示词、版本与素材包。附带角色档案和打包脚本；图片生成依赖助手可用的生图工具。

> 使用 $personal-ip-kit，根据这张参考图建立我的个人 IP。保留发型、眼镜和服装配色，先做角色设定，再做一张头像和一张文章封面。

入口：[技能说明](skills/personal-ip-kit/SKILL.md) · [详细介绍](skills/personal-ip-kit/README.md)

### avatar-depth：照片和头像立体化

**能做什么**：增强原画的体积感，或转为软陶、公仔、3D 卡通风格；支持连续局部修改、肩部配饰和精确尺寸导出。

**需要什么**：照片或已有头像、目标风格、输出尺寸，以及希望保留或修改的细节。

**怎么做**：识别主体特征 → 生成或编辑头像 → 检查脸部、配饰和边缘 → 用导出脚本调整最终尺寸 → 检查小尺寸显示效果。尺寸导出脚本需要 Python 和 Pillow。

> 使用 $avatar-depth，把这张头像做成软陶风，保留眼镜和发型，米白背景，输出 800×800 PNG。

入口：[技能说明](skills/avatar-depth/SKILL.md) · [详细介绍](skills/avatar-depth/README.md)

### chibi-character-card：Q 版角色设定卡

**能做什么**：把真人、动物、头像、Logo 或已有角色制作成 Q 版设定卡，包含全身正侧背视图、细节、表情和配色。

**需要什么**：主体清晰的参考图；可指定角色名、服装、画幅和表情需求。

**怎么做**：提取关键识别点 → 设计 Q 版比例 → 补全正侧背面 → 制作有明显差异的表情 → 排版并检查角色一致性。参考图中未出现的身体、服装背面等会作为设计补全说明。

> 使用 $chibi-character-card，把这只猫做成 Q 版角色卡，保留花纹，包含三视图和六种不同表情。

入口：[技能说明](skills/chibi-character-card/SKILL.md) · [详细介绍](skills/chibi-character-card/README.md)

### soren-ip-illustrations：Soren 专属配图

**能做什么**：沿用固定 Soren 形象制作头像、透明表情、文章封面和 AI 教程插图，保持发型、眼镜、服装与胸章等特征。

**需要什么**：已授权的原始参考图和主角色设定板，以及本次画面的主题。公开仓库不附带私人参考图片。

**怎么做**：读取品牌手册 → 将实际参考图传入生图工具 → 按主题安排角色动作 → 检查身份特征、构图与文字 → 保存成品和提示词。这个技能面向 Soren；创建其他人的角色请使用 `personal-ip-kit`。

> 使用 $soren-ip-illustrations，沿用我提供的角色参考图，画一张“整理零散提示词”的教程插图，横版 16:9，右侧留标题位置。

入口：[技能说明](skills/soren-ip-illustrations/SKILL.md)

### profile-promo：自由策划主页宣传动画

**能做什么**：把“我是谁、我提供什么、希望观众做什么”编排成连续动画。平台、角色、剧情、时长和画幅可以自定义，也可以只输出完整制作话术或分镜。

**需要什么**：主页资料、角色素材或设定、目标动作、视频规格。

**怎么做**：整理事实与角色 → 分配每个镜头的信息和阅读时间 → 设计角色动作触发界面反馈 → 制作关键帧 → 实现动画、声音并渲染 → 检查成片。附带需求 JSON 模板与 `plan_timeline.py`，用于把节拍分配成整数帧；它不是现成的一键渲染器。

> 使用 $profile-promo，为我的小红书主页设计一条 20 秒竖屏宣传片，让我的猫咪角色介绍两篇代表作，结尾引导关注。先给分镜。

入口：[技能说明](skills/profile-promo/SKILL.md) · [输入准备](skills/profile-promo/references/inputs-and-options.md) · [制作与验收](skills/profile-promo/references/production-and-qa.md)

### promo-video-director：体素吉祥物宣传片总入口

**能做什么**：把 X、小红书、公众号或网站资料套入同一套体素吉祥物动画。默认剧情为：终端输入 → 鲸鱼聚合 → Dock → 浏览器搜索 → 主页 → 踩下关注或访问按钮 → 片尾。

**需要什么**：平台资料、头像或图片、品牌词、配色和结尾文案。支持参考片分析和体素角色设计模块。

**怎么做**：选择平台 → 创建独立项目 → 填写 `config.json` → 构建页面和素材 → 检查关键帧 → 生成音效、渲染视频 → 验收并交付。默认 19 秒、1280×720、30fps；改竖屏、剧情或角色形状需要调整模板代码。

从仓库根目录创建一个示例项目：

```bash
python3 skills/promo-video-director/scripts/prepare_project.py \
  --platform xhs \
  --output ./outputs/my-xhs-promo
```

输出目录必须尚不存在。该命令只复制模板和示例配置，不安装依赖、不生成成片。已有适用的 Onetake 安装时可增加 `--onetake /你的/onetake/路径`；随后替换示例资料，按制作说明完成构建、预览和渲染。

> 使用 $promo-video-director，为这个网站制作 19 秒横屏体素鲸鱼宣传片，品牌色是橙色，按钮写“立即体验”，结尾展示域名。

入口：[技能说明](skills/promo-video-director/SKILL.md) · [制作流程](skills/promo-video-director/references/production.md) · [依赖说明](skills/promo-video-director/references/dependencies-and-license.md)

### x-profile-3d-promo：横版立体主页介绍片

**能做什么**：用真实主页和帖子截图制作 30 秒横屏介绍片：主页斜放 → 头像人物弹出 → 帖子卡片立起与数字滚动 → 撕纸拼贴墙 → Logo 和口号收尾。

**需要什么**：主页截图、头像、置顶帖或代表内容、配图、文案；人物公仔图片可另外制作。

**怎么做**：浏览器采集或手动提供素材 → 准备透明人物图 → 在 Remotion 模板中替换素材和示例文案 → 检查静帧 → Python 合成音乐音效 → Remotion 渲染、FFmpeg 合成。当前代码规格为 1920×1080、30fps、900 帧。

这里的立体效果主要来自 React/CSS 透视、图层与图片，人物图片不是可自由旋转的三维模型。旧模板带有具体账号示例及沙盒路径，使用前需要替换和适配。

> 使用 $x-profile-3d-promo，根据我的主页截图和代表作品制作 30 秒横版介绍片，采用主页斜放、头像跳出、作品立起的风格。替换所有示例账号资料。

入口：[技能说明](skills/x-profile-3d-promo/SKILL.md)

### x-profile-3d-video：配置化 X 主页介绍模板

**能做什么**：制作同类主页、置顶帖、拼贴墙和 Logo 收尾动画；相比前一套，提供 `template/src/config.ts` 集中填写昵称、账号、标语、数据、照片和人物开关。

**需要什么**：X 主页截图、头像、帖子与配图、结尾文案和真实统计数据。

**怎么做**：准备素材 → 填写配置 → 预览四个场景 → 合成音频 → 渲染和检查视频。动画仍基于 Remotion 与 CSS 透视效果。

**当前已知问题**：原始 `SKILL.md` 写的是 1080×1920 竖屏，但实际 [Root.tsx](skills/x-profile-3d-video/template/src/Root.tsx) 配置为 **1920×1080 横屏**，渲染脚本未覆盖尺寸。ZIP、解压版和本仓库版本均存在此差异。需要竖屏时，应同时调整画布、场景布局、镜头和阅读区域，不能只改输出宽高。原始文档保留供追溯，以实际代码和预览为准。

> 使用 $x-profile-3d-video，根据我的 X 资料填写配置，先检查横屏模板。如果要输出 9:16，请重新适配构图并给我看关键帧。

入口：[技能说明](skills/x-profile-3d-video/SKILL.md) · [内容配置](skills/x-profile-3d-video/template/src/config.ts)

## 原始资料与内部模块

以下资料保留在 `sources/original-zips/`。整合版通常更适合作为日常入口；原始包适合追溯和参考，里面的旧沙盒命令需要按实际环境调整。

| 原始包 | 能干什么、怎么做 | 整理后的入口 |
| --- | --- | --- |
| [make-x-promo-video.zip](sources/original-zips/make-x-promo-video.zip) | 用 X 账号资料填写配置，生成搜索主页、踩下 Follow 的 19 秒动画 | [X 模块](skills/promo-video-director/references/make-x-promo-video.md) |
| [make-xhs-promo-video.zip](sources/original-zips/make-xhs-promo-video.zip) | 提供小红书主页链接或截图，展示昵称、主页与红色关注按钮 | [小红书模块](skills/promo-video-director/references/make-xhs-promo-video.md) |
| [make-wechat-promo-video.zip](sources/original-zips/make-wechat-promo-video.zip) | 从文章链接或手动资料整理公众号信息，生成绿色关注按钮版本 | [公众号模块](skills/promo-video-director/references/make-wechat-promo-video.md) |
| [make-web-promo-video.zip](sources/original-zips/make-web-promo-video.zip) | 提供网站地址、首屏截图和 CTA 文案，生成搜索网站、访问首页的版本 | [网站模块](skills/promo-video-director/references/make-web-promo-video.md) |
| [voxel-mascot.zip](sources/original-zips/voxel-mascot.zip) | 用 Three.js 程序化生成方块吉祥物，并添加摆尾、眨眼、跳跃、落地挤压和方块聚合动画 | [体素角色模块](skills/promo-video-director/references/voxel-mascot.md) |
| [analyze-reference-video.zip](sources/original-zips/analyze-reference-video.zip) | 对参考片抽帧、拼缩略图，再分析故事线、镜头、转场和运动节奏 | [参考片分析模块](skills/promo-video-director/references/analyze-reference-video.md) |
| [onetake-sandbox-setup.zip](sources/original-zips/onetake-sandbox-setup.zip) | 为旧 Linux 沙盒配置 Onetake、Three.js 和 Chromium 软件渲染环境 | [环境准备模块](skills/promo-video-director/references/onetake-sandbox-setup.md) |
| [make-popup-showcase-video.zip](sources/original-zips/make-popup-showcase-video.zip) | 23.5 秒、720p30 横屏：主页 → 头像变体素角色 → 两张作品封面分层立起 → 数据滚动 → Logo 与贴纸收尾 | 独立历史模板，未纳入总导演技能 |
| [promo-video-skills.zip](sources/original-zips/promo-video-skills.zip) | 将前述四个平台和三个辅助模块整合为统一制作流程与共用模板 | [promo-video-director](skills/promo-video-director/SKILL.md) |
| [x-profile-3d-video.zip](sources/original-zips/x-profile-3d-video.zip) | 带配置文件的 30 秒 Remotion 主页模板；注意上面的横竖屏差异 | [x-profile-3d-video](skills/x-profile-3d-video/SKILL.md) |

**弹出展示模板的用法**：解开外层 ZIP 和其中的 `showcase-video-kit.zip` → 准备平台资料、头像、两张代表作封面、展示数据与结尾两段标语 → 按包内示例填写 `config.json` → 适配依赖 → 构建并检查关键帧 → 渲染。支持 X、小红书和公众号皮肤，适合强调作品和成果的个人介绍片。

**重复关系**：小红书、公众号和网站原始包内的套件相同；角色、参考片分析、环境准备三个包内的套件也相同。外层文档分别说明不同用途。`make-x-promo-video/` 解压目录与对应 ZIP 相同，因此只保留一份原始归档。名为“个人媒体宣传视频prompt”的资料整理到了 `skills/profile-promo/`。

## 从角色到成片的组合方式

1. 用 `personal-ip-kit` 建立角色档案，已有角色时跳过。
2. 按需用 `avatar-depth` 制作头像，或用 `chibi-character-card` 制作角色卡。
3. 用 `profile-promo` 确定观众要看懂的信息、镜头顺序和结尾动作。
4. 选择体素模板、主页立体模板或独立弹出模板进行制作。
5. 检查关键帧、文字、声音和完整成片，保存源工程、配置和素材清单。

这些技能可以独立使用，模板之间不会自动互通。参考图和立体风格角色卡仍是二维图片，不等于已经完成三维建模、绑定和动作制作。

## 目录结构

```text
creative-skills/
├── README.md                 # 功能目录、安装与使用指南
├── SOURCES.md                # 来源和导入版本
├── docs/                     # 图片创作流程与旧仓库迁移说明
├── skills/                   # 8 个独立技能
│   └── <skill>/
│       ├── SKILL.md          # 助手入口
│       └── ...               # 按需附带 references、scripts、assets、template
└── sources/original-zips/     # 10 份原始资料归档
```

## 运行条件与当前状态

| 类别 | 需要的能力或依赖 | 当前边界 |
| --- | --- | --- |
| 头像、角色和插画 | 参考图查看、生图或图片编辑；部分导出脚本需要 Python/Pillow | 技能不内置图像模型；无工具时只能整理提示词和方案 |
| 自由宣传片策划 | 资料整理、时间线规划；实际制作另需动画与渲染能力 | `plan_timeline.py` 负责分配帧数，不负责渲染 |
| 体素宣传片 | Three.js、浏览器、Python、FFmpeg，以及适用的 Onetake 安装 | Onetake 未随仓库分发；完整渲染与跨平台抓取尚未端到端验证 |
| Remotion 主页模板 | Node.js、React/Remotion、浏览器、Python 音频依赖和 FFmpeg | 需补齐本地依赖、替换旧沙盒路径与示例素材；两份当前代码均为横屏 |
| 原始 ZIP | 包内说明所列工具与素材 | 保留旧实现；不能直接假定适用于当前电脑 |

主页、点击关注和粉丝数变化是**视频中的演示动画**，不会实际操作账号，也不代表真实涨粉。本仓库没有自动登录、发布到社交平台或执行关注的统一流程。

## 来源与授权

来源、导入版本和整理边界见 [SOURCES.md](SOURCES.md)。原始 ZIP 作为快照保留，不会自动同步上游更新。

本仓库未给全部内容统一附加许可证。`avatar-depth` 保留其 [MIT 许可证](skills/avatar-depth/LICENSE)；其他来源未注明许可证的内容，不因公开展示而获得额外授权。使用 Onetake 时，以实际安装版本及其许可证为准，详见 [依赖与授权说明](skills/promo-video-director/references/dependencies-and-license.md)。平台标识、音乐和参考素材分别遵守其使用条件。

Soren 的私人参考图不公开分发；角色描述公开不等于授权他人使用该人物形象或品牌。
