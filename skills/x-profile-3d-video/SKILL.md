---
name: x-profile-3d-video
description: 用 X(Twitter) 主页真实截图 + Remotion 代码动画，制作 30 秒竖屏 3D 风格个人介绍短片（主页平板翻转、头像弹出、置顶帖立起+浏览量滚动、撕纸拼贴墙、X Logo 收尾卡），自动合成配乐音效。当用户想“用我的 X 主页做一个类似的 3D 介绍视频/宣传片”时使用。
---

# X 主页 3D 介绍短片（Remotion 实做流程）

本 skill 是对一次真实制作过程的整理：**浏览器截图 + curl 下载素材 → Remotion 写动画 → numpy 合成音频 → ffmpeg 合并**。不依赖 AI 视频生成工具。

## 目录
```
SKILL.md
scripts/grab_x_profile.js   # 共享浏览器抓主页截图、帖子截图、头像/banner/配图链接
scripts/make_audio.py       # 生成 30s 配乐 + 转场/弹出/计数音效 -> out/audio.wav
scripts/chroma_key.py       # （可选）绿幕 3D 公仔抠图 -> figure.png
template/                   # Remotion 项目（1080x1920, 30fps, 900 帧）
  src/config.ts             # ★ 只改这里：昵称、账号、标语、数据、标签、照片
  src/Video.tsx, Root.tsx, index.ts
  render.cjs                # 打包+渲染+自动合成音频
  public/                   # 放素材（见第 2 步）
```

## 分镜 / 帧号（30fps）
| 场景 | 起始帧 | 秒 | 内容 |
|---|---|---|---|
| SceneA | 0 | 0–6.7 | 主页截图做成 3D 平板，镜头推近，头像弹出（useFigure 时公仔跳出） |
| SceneB | 200 | 6.7–13.7 | 置顶帖立起 + 霓虹底座 + 浏览量数字滚动 |
| SceneC | 410 | 13.7–21.2 | 撕纸拼贴墙：照片、三张数据卡、大红标签、描边标语 |
| SceneD | 635 | 21.2–30 | X Logo 收尾卡 + 昵称/定位标签逐个落下 + CTA |
场景之间用 Whip（甩镜）转场。修改时长后要同步改 `make_audio.py` 顶部的 WHOOSH/POPS/TICK_START/THUMPS 时间点。

## 步骤

### 0. （有参考视频时）先拆帧看节奏
```bash
ffmpeg -i ref.mp4 -vf fps=2,scale=270:-1 /data/ref/f_%03d.png
ffmpeg -i ref.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null - 2>&1 | grep pts_time   # 找切点
```
用 view_image 看关键帧，对照上面的分镜决定是否调整。

### 1. 复制模板
```bash
cp -r <skill>/template /data/xv && cd /data/xv && mkdir -p public stills out
```

### 2. 抓素材（共享浏览器）
先 `agent-browser skills get core`（bash browser:true）。X 主页未登录也可访问。
```bash
cd /data/xv && NODE_PATH=/vercel/sandbox/node_modules node <skill>/scripts/grab_x_profile.js <handle> public   # browser:true
```
产出：`public/profile.png`(1200x2000 暗色主页)、`tweet0.png`(置顶帖)…`tweet5.png`、`profile_info.json`（name/bio/计数/avatar/banner/media 链接）。
然后按 json 里的链接下载：
```bash
curl -sL "<avatar_url 把 _normal 换成 _400x400>" -o public/avatar.jpg
curl -sL "<banner_url>/1500x500" -o public/banner.jpg
curl -sL "<media_url>?name=medium" -o public/m1.jpg   # m1..m4（拼贴墙照片），article.jpg 可选
```
**必须 view_image 检查截图**：有无登录弹窗/"See xxx's full profile" 底栏遮挡（脚本已隐藏，X 改版时需更新选择器）、是否暗色、头像位置是否正确。

### 3. 填 config.ts
用 profile_info.json 和置顶帖内容填写：name、handle、cta、headline（一句话定位）、subline、slogan、photoTag、stats（帖子/粉丝/关注）、pinnedViews、pinnedTag、photos。截图参数不变时 `avatarCenter` 保持 `{x:168,y:504}`。

### 4.（可选）3D 公仔
用图像生成工具以头像为参考生成“盲盒风 3D 公仔、纯绿幕背景(#00FF00)、全身”，然后：
```bash
python3 <skill>/scripts/chroma_key.py fig_green.png public/figure.png
```
检查边缘无绿边后把 `useFigure: true`。否则用头像圆形亚克力立牌（默认）。

### 5. 出静帧检查
```bash
cd /data/xv && NODE_PATH=/vercel/sandbox/node_modules node render.cjs stills 110 300 560 820
```
逐张 view_image：文字有无溢出/重叠、镜头是否裁掉主体、头像对位、中文和 Logo 显示正常。

### 6. 音频 + 渲染 + 合成
```bash
cd /data/xv && python3 <skill>/scripts/make_audio.py          # -> out/audio.wav
NODE_PATH=/vercel/sandbox/node_modules node render.cjs video   # -> out/video_noaudio.mp4 + out/final.mp4，并打印音量
```
render.cjs 会自动执行 `ffmpeg -map 0:v:0 -map 1:a:0 ...`。确认打印的 mean_volume 约 -20dB 左右（不是 -91dB）。最后用 download_file_from_sandbox 交付 `out/final.mp4`。

## 质检清单
- [ ] 有声音（volumedetect mean ≈ -20dB）
- [ ] 截图无遮挡层、暗色、清晰（2x）
- [ ] 抽 4 帧检查文字不溢出、标签不与 Logo 重叠
- [ ] 数字滚动终值 = pinnedViews
- [ ] 时长 30s，1080x1920

## 踩坑记录
1. **TypeScript 7 没有 JS API**，Remotion 自带 esbuild-loader 读 tsconfig 会报错 → render.cjs 用 `webpackOverride` 注入 `tsconfigRaw`，不要用 `npx remotion render`。
2. **找不到模块**：在 /data 下运行要加 `NODE_PATH=/vercel/sandbox/node_modules`（以实际 node_modules 路径为准）。
3. **𝕏 字符显示为方框**：字体不支持，Logo 用 SVG 路径（模板已内置 XLogo 组件）。
4. **合成后无声**：Remotion 输出带静音音轨，ffmpeg 不加 `-map` 会选中它 → 必须 `-map 0:v:0 -map 1:a:0`。
5. **截图遮挡**：未登录时底部有 "See … full profile" 横幅/登录弹窗，需隐藏后再截。
6. **镜头裁切**：3D 旋转+推近时主体易出画，改 Video.tsx 中的 scale/translate 后务必重出静帧。
