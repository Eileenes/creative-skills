---
name: x-profile-3d-promo
description: 把一个社交媒体主页（X / 小红书 / 公众号等）的截图做成"3D 主页介绍片"：暗色主页斜放在 3D 空间、头像里跳出 3D 小人、置顶内容立起展示 + 数字滚动、撕纸拼贴墙、Logo 收尾卡，带配乐音效。用户给出主页链接和/或参考视频、要求做"个人主页介绍片 / 账号宣传片 / 类似风格视频"时使用。
---

# X 主页 3D 介绍片制作方法

成片规格：1920×1080、30fps、30 秒（900 帧），H.264 + AAC。
技术栈：**浏览器截图（Playwright）→ AI 生图做 3D 形象 → 绿幕抠图 → Remotion（React + CSS 3D）做动画 → Python 合成音乐音效 → ffmpeg 合成**。
整个过程不用 Blender / AE，所有"3D"都是 CSS `perspective` + `transform-style: preserve-3d` 做出来的伪 3D。

---

## 0. 先拆参考视频（风格分析）

```bash
ffprobe -v error -show_entries format=duration:stream=width,height,r_frame_rate ref.mp4
ffmpeg -i ref.mp4 -vf "fps=2,scale=320:-1,tile=6x5" sheet%02d.png   # 每秒 2 帧拼成联系表
```

看联系表，把参考片拆成**分镜 + 特效清单**。本模板对应的参考风格：

| 段落 | 画面 | 关键特效 |
|---|---|---|
| ① 0–6s | 暗色主页截图像一块屏幕斜躺在黑色空间，镜头推近头像 | 3D 透视、镜头推拉+旋转、平板厚度、蓝色辉光 |
| ② 头像弹出 | 头像位置跳出一个 3D 小人 | 光圈闪烁、抛物线跳跃、彩纸爆开、落地挤压回弹、地面阴影 |
| ③ 7–13s | 置顶帖从地面立起，底座一圈青色霓虹框 | 卡片 rotateX 立起、扫光、霓虹呼吸、数字滚动 0→7.4K、描边大字 |
| ④ 14–21s | 米色撕纸拼贴墙：大红标签、数据卡、照片 | 撕纸锯齿边 clip-path、纸张噪点纹理、元素逐个"砸"进墙面、小人走过 |
| ⑤ 21–30s | 黑色反光地面上 3D Logo 升起，小人落到 Logo 上，左侧标签依次弹出 | 叠层挤出 Logo、旋转升起、名字/账号/口号贴纸弹入、打字机、皇冠 |
| 转场 | 每段之间 | 放大 + 模糊 + 提亮的"甩镜"转场 |

---

## 1. 抓取主页素材

X 未登录也能看公开主页，但会有登录弹窗遮挡，需要用脚本隐藏。

- **暗色模式**：加 cookie `night_mode=2`（域 `.x.com`）。
- **高清**：`newContext({ deviceScaleFactor: 2 })`，截图是 2 倍像素。
- **去遮挡**：在截图前把包含 "See xxx's full profile / Continue to X" 的元素 `display:none`（滚动后会重新出现，每次截图前都要再隐藏一次）。
- **截主页主栏**：`page.screenshot({clip:{x:331,y:0,width:600,height:1000}})`（视口 1400 宽时主栏的位置）。
- **截单条帖子**：`page.locator('article').nth(i).screenshot()`。
- **直接下原图**（比截图清晰）：
  - 头像：把 `..._normal.jpg` 改成 `..._400x400.jpg`
  - 横幅：`https://pbs.twimg.com/profile_banners/<id>/<ts>/1500x500`
  - 帖子图片：`https://pbs.twimg.com/media/<id>?format=jpg&name=large`
  - 页面里所有图片地址：`$$eval('img', els => els.map(e => e.src))`

脚本见 `scripts/grab_x_profile.js`。放进 `public/` 的素材：
`profile.png`（主页截图）、`tweet0.png`（置顶帖）、`avatar.jpg`、`banner.jpg`、`m1~m4.jpg`（帖子配图）、`figure.png`（3D 小人）。

同时记下文案数据：昵称、@账号、简介、帖子数 / 粉丝 / 关注、置顶帖浏览量。

---

## 2. 做 3D 小形象（"头像里蹦出来的小人"）

参考片里的小人是作者自己的 3D IP。没有现成 3D 模型的话，**用 AI 生图生成一张"盲盒手办风全身像"就够了**，因为视频里它始终正对镜头（billboard 广告牌原理），不需要真 3D 模型。

**提示词（把头像作为参考图输入）：**

> Turn this character into a full-body 3D chibi blind-box collectible figurine (Pop Mart / Pixar style). Keep the same face, hair, glasses… Big head, small body, wearing … Happy standing pose, one hand waving. Glossy vinyl toy material, soft studio lighting. Entire body visible from head to feet, centered, generous margin. **Plain solid pure green (#00FF00) chroma-key background**, no floor, no shadow, no text.

要点：
- **一定要纯绿背景**，方便抠图。AI 生图一般不能直接出透明 PNG。
- 全身入镜、四周留白，否则脚会被裁掉。
- 可多生成几个动作（挥手、比耶、跳跃），在不同段落轮换使用。

**抠图：**`python3 scripts/chroma_key.py figure_green.jpg public/figure.png`
原理：绿色程度 `d = G − max(R,B)` 转成透明度，再把边缘泛绿的部分压掉（去绿边），最后自动裁到人物边界。

> 想要更像参考片：用 Tripo / Meshy / Rodin 等"图生 3D"工具把这张图转成 .glb 模型，在 Blender 里绑动作、渲染成带透明通道的序列帧，再替换 `figure.png`，就能做出转身、走路等真正的 3D 动作。

---

## 3. 动画实现（Remotion + CSS 3D）

### 3.1 3D 舞台 / 摄像机
```tsx
<AbsoluteFill style={{perspective: 2000}}>
  <div style={{transformStyle:'preserve-3d',
    transform:`translate(960px,560px) scale(${s}) rotateX(${rx}deg) rotateZ(${rz}deg) translate(${-cx}px,${-cy}px)`}}>
    {/* 地面 = XY 平面，所有物体放在这里 */}
  </div>
</AbsoluteFill>
```
- `rotateX` = 俯仰角（越大越接近平视）；`rotateZ` = 绕竖直轴环绕；`scale` = 推拉；`cx,cy` = 镜头看向地面上的哪个点。
- 用关键帧函数 `kf(frame, [[帧, 值], ...])` + 缓动曲线 `bezier(0.65,0,0.35,1)` 给这 5 个参数打关键帧，镜头运动就出来了。

### 3.2 "立起来"的物体
躺在地面上的元素加 `rotateX(-90deg)`（`transformOrigin` 设在底边）就会垂直立起。从 0 → -90 用 spring 动画，就是"卡片从地面立起"。
小人/立牌再加 `rotateZ(-镜头rz)`，让它始终面朝镜头。

### 3.3 关键特效写法
| 特效 | 实现 |
|---|---|
| 平板厚度 | 同尺寸的深灰 div 叠 3 层，分别 `translateZ(-6/-12/-18px)` |
| 弹出 / 砸入 | `spring({damping:9~11, stiffness:180})`，同时做 scale 0.4→1 和 translateZ 260→0 |
| 跳跃 | `lift = 高度 * 4t(1−t)`（抛物线），落地后用 `|sin|` 做原地小跳，落地瞬间 scaleY 0.94 挤压 |
| 阴影 | 地面上一个模糊椭圆 `filter: blur(12px)`，小人越高阴影越小越淡 |
| 彩纸 | 36 个小矩形，随机角度向外扩散 + 重力下落 + 旋转 + 淡出 |
| 霓虹底座 | `border: 5px solid #34d6ff` + 多层 `box-shadow` 辉光，用 sin 做呼吸 |
| 扫光 | 卡片上叠一层斜向 `linear-gradient`，渐变位置随帧移动 |
| 数字滚动 | `interpolate(f,[55,140],[0,7400], easeOut)`，格式化成 `7.4K`；到点后做一次衰减抖动放大 |
| 描边大字 | `-webkit-text-stroke: 10px #0b1220; paint-order: stroke fill;` + 蓝色 `text-shadow` 做厚度 |
| 撕纸边 | `clip-path: polygon(...)`，四条边按伪随机数生成锯齿点 |
| 纸张质感 | SVG `feTurbulence` 噪点做成 data-uri 背景，用 `multiply` 混合 |
| 3D Logo | 14 层圆角方块逐层 `translateZ(3px)`，颜色由深到浅，最上层放 X 的 SVG |
| 地面倒影 | 把 Logo 组复制一份 `scaleZ(-1)` 放到地面下，地面用半透明渐变 |
| 甩镜转场 | 每段首尾 8 帧：`blur(18px) brightness(1.8) scale(1.25)` |
| 浮尘粒子 | 40 个小光点缓慢上飘 |
| 暗角 | 全屏 `radial-gradient` 四周压黑 |

完整代码在 `template/src/Video.tsx`，每一段是一个 Scene 组件（SceneA–D），在 `Main` 里用 `<Sequence from durationInFrames>` 串起来。

**换成你自己的账号时要改的地方：**
- 素材文件名（放 `public/`）
- 头像在截图中的位置 `AV = {x, y}`，以及截图在平板上的偏移
- 文案：Tag / StatCard / Counter 里的文字和数字
- 想调节奏就改每个 Sequence 的起止帧，以及各元素的 `pop(f, 起始帧)`

### 3.4 渲染
```bash
node render.cjs stills 30 100 300 560 760   # 先出关键帧静帧检查构图
node render.cjs video                         # 渲染完整视频 → out/video_noaudio.mp4
```
> 坑：如果环境里装的是 TypeScript 7（原生版，没有 JS API），Remotion 自带的 esbuild-loader 会报 `typescript.sys undefined`。`render.cjs` 通过 `webpackOverride` 给 loader 注入 `tsconfigRaw` 绕过了这个问题。正常环境用 `npx remotion render` 也可以。

---

## 4. 配乐与音效
`python3 scripts/make_audio.py` 用 numpy 合成 30 秒音频：
- 120 BPM 底鼓 + 反拍 hi-hat + 4 和弦 pad + 低音拨弦
- 音效按分镜时间点放：转场 whoosh、头像弹出 pop + 叮、数字滚动 tick、标签落下 thump

建议正式发布时换成有版权的 BGM，并按鼓点对齐转场。

## 5. 合成（⚠️ 一定要 -map）
Remotion 输出的 mp4 自带一条**静音音轨**，不指定 `-map` 的话 ffmpeg 会选中这条静音轨，导致成片没有声音：
```bash
ffmpeg -i out/video_noaudio.mp4 -i out/audio.wav \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -ac 2 -shortest final.mp4
# 检查一下确实有声音（mean_volume 不应是 -91dB）
ffmpeg -i final.mp4 -af volumedetect -vn -f null - 2>&1 | grep volume
```

---

## 6. 质检清单
- [ ] 截图里没有登录弹窗 / "See full profile" 遮挡
- [ ] 小人跳起时头没有出画面，落地时脚和阴影对齐
- [ ] 置顶卡片、拼贴墙上下没被裁掉
- [ ] 所有中文用的是粗体字体（Noto Sans SC Black），没有显示成方框（特殊符号如 𝕏 要换成 SVG）
- [ ] 成片有声音（volumedetect 检查）
- [ ] 数据（粉丝数、浏览量）是最新的

## 7. 变体
- **竖屏 9:16**（小红书 / 视频号 / 抖音）：Composition 改成 1080×1920，镜头 `scale` 调小，标签移到画面下方。
- **其他平台**：把 X 主页换成小红书 / B 站主页截图，Logo 换成平台图标即可，流程完全一样。
