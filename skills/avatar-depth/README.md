# Avatar Depth · 头像立体化

上传自己的照片或已有头像，制作保留辨识度的立体风格头像，再通过自然语言修改配饰、背景和尺寸。

适用于支持 `SKILL.md`、参考图输入和图片生成/编辑工具的 Agent。**技能负责创作流程，实际生成依赖宿主的图像工具。** 输出是有3D质感的PNG/JPEG，不是可旋转的三维模型。没有生图工具的环境只能完成提示词。

## 安装

在支持技能安装的助手中发送：

> 请从 https://github.com/Eileenes/avatar-depth 安装 avatar-depth 技能，SKILL.md 在仓库根目录。

也可以下载 [Release 技能包](https://github.com/Eileenes/avatar-depth/releases/latest)，将其中的 `avatar-depth` 文件夹放到宿主的技能目录。在 Codex 中可以使用 `~/.codex/skills/avatar-depth/`，已有同名技能时先备份。不要把用户照片放到技能目录。

精确尺寸导出脚本需要 Python 3.10+ 与 Pillow。可在独立环境安装：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Windows 的环境解释器为 `.venv\Scripts\python.exe`。不需要为导出脚本配置生图API密钥；生图工具的可用性和费用由宿主决定。

## 使用

上传一张清晰图片后：

> 用 $avatar-depth 做一个微信头像，保留我的样子。

> 用 $avatar-depth 做800×800的软陶风头像，米白背景。

> 画面左肩加一只啃竹子的熊猫，右肩加一个迷你火锅，别遮住脸。

> 把胸前徽章换成九筒，保留刚才的肩部配饰和尺寸。

> 导出900×1200透明背景版，保留完整头发。

默认沿用原图设计增强体积感，也支持软陶公仔、精致3D卡通。新用户上传自己的图片后会以自己的图片为依据，不会继承别人的外貌。

## 尺寸与透明度

| 情况 | 行为 |
| --- | --- |
| 用户指定宽高 | 按指定像素导出，覆盖用途预设 |
| 微信头像未指定尺寸 | 640×640、实色背景PNG，这是实用预设，非官方唯一规格 |
| 通用头像未指定尺寸 | 1024×1024 |
| 源图与目标比例不同 | 默认等比缩放后留边，避免把脸拉长；可显式选择中央裁切 |
| PNG源图有透明度 | 默认保留alpha；实色底可显式指定 |
| 导出需要放大 | 默认拒绝，显式允许后仍注明放大不等于新增细节 |

从技能目录运行（其他目录请使用脚本绝对路径）：

```bash
python3 scripts/export_avatar.py master.png wechat.png --width 640 --height 640 --background '#fff6eb'
python3 scripts/export_avatar.py master.png portrait.png --width 900 --height 1200 --background transparent
python3 scripts/export_avatar.py master.png cropped.png --width 800 --height 800 --fit cover
```

`--background transparent` 只保留透明度或添加透明留边，不能把实色背景自动抠掉。抠图、补画和局部改图由图像工具完成。默认不覆盖现有输出；源图永远不能作为输出路径。最终报告实际尺寸、格式、透明度和是否放大。

## 连续编辑的约定

- 上一版成品作为当前编辑底图，保留已接受的配饰和徽章修改。
- “左/右”默认按观看者视角说明；明确指定人物自身方向时遵循用户。
- 脸部是视觉中心，配饰与人物统一材质、光照和比例。
- 徽章圆点等数量细节需要目视计数，不能只依赖提示词。
- 本地保存提示词与版本记录；公开技能包不包含用户照片、生成头像或个人路径。
- 图像模型可能产生身份或细节漂移。技能会检查并定向修正，不承诺逐像素不变或百分百相似。

## 验证

```bash
python3 -m unittest discover -s tests -v
```

自动测试覆盖尺寸、等比缩放、透明度、裁切、EXIF方向、文件保护和错误输入；图像审美和身份一致性仍需目视检查。

MIT License。版本：1.0.0。
