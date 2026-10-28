# Creative Skills｜宣传视频与个人 IP 创作技能库

把主页、参考图片和角色设定，变成宣传视频、立体头像、Q 版角色卡和可持续使用的个人 IP 素材。这个仓库将相关的 Agent Skills 集中管理：你可以按任务安装其中一个，也可以组合使用。

**适合谁：** 想介绍自己的账号或产品、打造个人 IP、制作统一风格配图，或者为已有角色制作宣传片的创作者。

**它是什么：** 每个技能是一套写在 `SKILL.md` 中的工作流程，以及必要的参考资料、模板或脚本。支持 Agent Skills 的助手读取这些文件后，结合你的素材和当前可用工具完成任务。安装技能本身不会自动提供生图模型、视频渲染服务或 API 额度。

## 你可以得到什么

| 你的目标 | 使用技能 | 可以得到的成果 |
| --- | --- | --- |
| 先规划一条账号或网站介绍动画 | [profile-promo](skills/profile-promo/SKILL.md) | 结合主页、角色、平台和目标动作的制作话术、分镜或视频方案；环境具备时可继续制作成片 |
| 用体素吉祥物做账号或产品宣传片 | [promo-video-director](skills/promo-video-director/SKILL.md) | 默认 19 秒横版宣传片方案；具备渲染条件时可交付 MP4、关键帧预览和可复用配置 |
| 用主页截图制作 3D 风格横版介绍片 | [x-profile-3d-promo](skills/x-profile-3d-promo/SKILL.md) | 约 30 秒横屏介绍片的模板和制作流程，包含主页、头像、代表内容和片尾 |
| 为 X 主页制作竖屏短视频 | [x-profile-3d-video](skills/x-profile-3d-video/SKILL.md) | 约 30 秒竖屏介绍片的模板和制作流程，包含主页截图、置顶内容、拼贴墙和片尾 |
| 从一张参考图建立自己的 IP | [personal-ip-kit](skills/personal-ip-kit/SKILL.md) | 角色档案、角色设定与可按需扩展的头像、表情、Banner、文章插图及视频素材；可整理为素材包 |
| 把照片或头像做成立体风格 | [avatar-depth](skills/avatar-depth/SKILL.md) | 可按指定尺寸导出的立体风格头像图片，并支持局部修改和配饰 |
| 把人物、宠物或已有形象做成 Q 版 | [chibi-character-card](skills/chibi-character-card/SKILL.md) | 保留主体辨识特征的 Q 版角色设定卡，可包含三视图、表情、细节和配色 |
| 沿用 Soren 形象制作内容 | [soren-ip-illustrations](skills/soren-ip-illustrations/SKILL.md) | Soren 风格的头像、表情、封面或教程插图；需提供授权参考图 |

实际成果取决于你提供的资料、任务要求，以及助手能调用的生图、浏览器和渲染工具。图片是具有立体质感的二维素材，不等同于可旋转的三维模型。

## 如何使用

### 第一步：准备支持技能的助手

在支持读取 `SKILL.md` 的助手中使用，例如 Codex。创作图片需要支持参考图输入的生图或编辑工具；生成视频需要相应的素材、运行环境和渲染工具。无法调用这些工具时，可以先使用技能整理方案和提示词。

### 第二步：安装需要的技能

以 Codex 的用户级技能目录为例，在终端执行：

```bash
git clone https://github.com/Eileenes/creative-skills.git
mkdir -p ~/.codex/skills

# 示例：安装 personal-ip-kit；目标已存在时停止，避免覆盖
if [ -e "$HOME/.codex/skills/personal-ip-kit" ]; then
  echo "已存在 personal-ip-kit，请先比较或备份"
else
  cp -R creative-skills/skills/personal-ip-kit "$HOME/.codex/skills/"
fi
```

要安装其他技能，把命令中的 `personal-ip-kit` 换成上表里的技能名。**复制整个技能目录**，不要只复制 `SKILL.md`，因为它可能需要同目录的脚本、模板和参考资料。安装后如果当前会话没有识别新技能，重新打开会话，或直接向助手提供该技能的 `SKILL.md` 路径。

例如安装宣传视频导演时，将 `skills/promo-video-director` 整个目录复制到 `~/.codex/skills/promo-video-director`。使用其他支持技能的工具时，请按该工具要求选择安装目录。

### 第三步：提供素材并告诉助手目标

可以直接用自然语言，也可以用 `$技能名` 明确指定。以下示例可直接改写：

**制作个人 IP**：上传参考图，再说：

> 使用 $personal-ip-kit，根据这张图创建我的个人 IP。请保留发型、眼镜和衣服颜色，先做角色设定，再制作头像和一张文章配图。

**制作头像或角色卡**：上传照片、宠物图或已有形象，再说：

> 使用 $avatar-depth，把这张头像做成柔和的立体卡通风格，保留眼镜和发型，导出 1024×1024 图片。

> 使用 $chibi-character-card，把这只宠物制作成 Q 版角色设定卡，包含正侧背视图和几种表情。

**制作主页宣传视频**：提供主页链接或清晰截图、头像或角色参考、希望观众执行的动作，以及画幅和时长。例如：

> 使用 $profile-promo，为我的小红书主页设计一条 20 秒竖屏宣传片。用我提供的角色介绍主页，结尾引导观众关注；先给我分镜。

> 使用 $promo-video-director，为这个网站制作体素吉祥物宣传片。品牌色是橙色，结尾按钮写“了解更多”；请先展示关键帧，再制作视频。

> 使用 $x-profile-3d-video，根据我的 X 主页截图制作竖屏个人介绍短片，展示头像、置顶帖和账号名称。

需要横版主页介绍片时可指定 `$x-profile-3d-promo`；需要 Soren 配图时指定 `$soren-ip-illustrations`，并提供已授权的原始参考图和角色设定板。Soren 的参考图片没有放在公开仓库里。

## 一起使用：从角色到宣传片

1. 使用 `personal-ip-kit` 根据参考图建立角色档案和设定图。
2. 使用 `avatar-depth` 或 `chibi-character-card` 制作所需的头像或角色卡。
3. 使用 `profile-promo` 规划主页介绍的分镜、时长和目标动作。
4. 选择 `promo-video-director` 或适合横竖屏的 X 视频技能，结合角色素材制作预览和成片。

这些步骤可以分开使用。已有角色和主页资料时，可以直接从视频制作开始；不同技能的模板不会自动互通，具体适配需要助手根据素材和模板完成。

## 模板与运行条件

- `promo-video-director` 内含 X、小红书、微信公众号、网站、参考视频分析和体素角色等模块。默认模板为 **19 秒、1280×720、30 fps**；修改画幅、时长或剧情通常需要调整模板代码。
- `x-profile-3d-promo` 和 `x-profile-3d-video` 是分别面向横屏与竖屏的旧实现，使用浏览器截图、Remotion、Python 和 FFmpeg 等工具。它们带有原沙盒环境假设和具体账号示例，运行前需要适配环境并替换资料。
- 生图技能需要支持图片输入的生成或编辑工具；`personal-ip-kit` 和 `avatar-depth` 的部分辅助脚本还需要 Python 和 Pillow。具体安装方法见各技能文档。
- 23.5 秒的弹出展示视频模板目前保留在 [原始 ZIP](sources/original-zips/make-popup-showcase-video.zip) 中，还没有整理为独立可安装技能。原始 ZIP 供追溯使用；其中旧脚本和示例请先审阅再运行。
- 本仓库已检查技能结构和 IP、头像技能的现有测试；宣传视频的完整渲染和跨平台抓取尚未在此仓库端到端验证。

## 授权与来源

本仓库保留各来源的许可状态，没有给所有内容统一附加许可证。`avatar-depth` 保留其 [MIT 许可证](skills/avatar-depth/LICENSE)；其他未注明许可证的内容不因此获得额外授权。使用外部 Onetake 时，需自行遵守所用版本的许可，详见 [依赖与授权说明](skills/promo-video-director/references/dependencies-and-license.md)。平台标识、音乐和参考素材也应分别确认使用权；公开的 Soren 角色描述不等于授予他人使用该人物形象或品牌的权利。

原有独立仓库、导入版本与整理边界见 [SOURCES.md](SOURCES.md)。原始压缩包保存在 [sources/original-zips](sources/original-zips/)，用于追溯；它们不是默认安装入口，也不会随本仓库自动同步上游更新。
