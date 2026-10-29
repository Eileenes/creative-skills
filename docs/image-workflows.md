# 头像与图片创作指南

## 先选一个技能

| 需求 | 技能 | 主要产物 |
| --- | --- | --- |
| 制作或修改一张头像 | [avatar-depth](../skills/avatar-depth/SKILL.md) | 立体、软陶、3D 卡通风格头像；指定尺寸 PNG/JPEG |
| 设计 Q 版人物、宠物或吉祥物 | [chibi-character-card](../skills/chibi-character-card/SKILL.md) | 三视图、六种表情、细节和配色组成的角色卡 |
| 建立可持续使用的角色，为文章系列配图 | [personal-ip-kit](../skills/personal-ip-kit/SKILL.md) | 角色档案、头像、立绘、表情、Banner、封面和正文插图 |
| 为已有的 Soren 固定形象制作内容 | [soren-ip-illustrations](../skills/soren-ip-illustrations/SKILL.md) | Soren 头像、表情、封面和 AI 教程插图 |

只做头像或角色卡时，可以直接使用对应技能。长期经营角色时，以 `personal-ip-kit` 的角色档案和已接受的参考图作为后续创作依据；Soren 技能只用于该固定角色。

## 安装

克隆合集或下载 GitHub ZIP，然后将需要的整个技能目录复制到助手支持的技能目录。以 Codex 为例，在合集根目录执行：

```bash
mkdir -p "$HOME/.codex/skills"
if [ -e "$HOME/.codex/skills/avatar-depth" ]; then
  echo "avatar-depth 已存在，请先备份并比较版本"
else
  cp -R skills/avatar-depth "$HOME/.codex/skills/"
fi
```

将两处 `avatar-depth` 路径和提示文字替换为所需技能名，即可安装其他技能。每个目录都是完整安装单元；不要只复制 `SKILL.md`，也不要把整个合集当成一个技能目录。要安装全部图片技能，分别复制上表四个目录。

已有独立仓库安装的用户，技能名和调用方式保持不变。备份旧目录中的自定义修改与私人素材后，再用合集内对应的完整目录更新。不要在旧 Git 仓库内直接更改远端地址为合集，两个仓库的根目录结构不同。

图片生成需要助手支持查看参考图及生成／编辑图片。安装技能不会安装图像模型。`avatar-depth` 和 `personal-ip-kit` 的辅助脚本需要 Python 3.10+ 和各自 `requirements.txt` 中的 Pillow；只制作 Q 版角色卡或 Soren 配图无需安装这两个技能的脚本依赖。

## 常见工作流

### 一张头像

上传照片或已有头像，指定风格、背景和尺寸：

> 使用 $avatar-depth，把这张照片做成 800×800 的软陶头像，保留发型和眼镜，米白背景。

后续修改以上一版已接受的成品为底图，例如更换肩部配饰或背景。最终交付时核对尺寸、透明度和小尺寸显示效果。

### 一张角色设定卡

> 使用 $chibi-character-card，把这只猫做成 Q 版角色卡，保留花纹，包含三视图、六种不同表情、细节和配色。

照片未展示的背面等内容属于设计补全。角色卡是二维设计参考，不是已完成的三维模型。

### 一个角色持续做系列图片

1. 使用 `personal-ip-kit`，从参考图建立独立角色档案与主设定。
2. 按需使用 `avatar-depth` 或 `chibi-character-card`，制作头像或角色卡；传入同一角色参考图。
3. 将接受的成品及其用途记入该角色的素材记录。
4. 继续使用 `personal-ip-kit`，提供文章或大纲，制作封面、Banner、正文插图和透明动作素材。
5. 检查角色一致性，保存提示词、版本与素材包。

技能之间没有自动数据同步；交接时需要明确角色档案、参考图和已接受的版本。私人照片及角色素材保存在使用者项目中，不提交到公共技能仓库。

### Soren 专属配图

> 使用 $soren-ip-illustrations，沿用我提供的 Soren 参考图，制作一张“整理提示词”的 16:9 教程插图，右侧留标题位置。

需要用户提供授权参考图和主设定。其他人物或品牌角色使用 `personal-ip-kit` 建档。

[返回总目录](../README.md)
