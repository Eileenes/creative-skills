# 环境与外部依赖模块

## 独立工作目录

使用当前技能绝对路径替换下文 SKILL_DIR；所有命令参数正常引用，路径允许中文及空格。

```sh
python3 "$SKILL_DIR/scripts/prepare_project.py" --platform xhs --output /absolute/path/to/new-film
```

工具不覆盖已有目录，不联网。它复制自己的模板，并将中性样例写成 config.json。替换演示资料后才能正式交付。每部视频一个目录。

## 运行依赖

需要 Python 3、Node/npm、ffmpeg/ffprobe；Python 环境需要 playwright、numpy、scipy、Pillow、matplotlib，参考分析可能需要 opencv-python。优先复用合适的现有环境，否则在作品目录创建 .venv 并安装。不要假定全局 pip 可用。

在工作目录安装 three@0.180.0 和 esbuild；保存 package-lock.json。用以下入口进行本地 IIFE 打包：

```js
import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/examples/jsm/geometries/RoundedBoxGeometry.js';
window.THREE = THREE;
window.THREEX = { RoundedBoxGeometry };
```

将其写入 three-entry.js，再运行 `npx esbuild three-entry.js --bundle --format=iife --minify --outfile=three.bundle.js`。不要在 HTML 里换成远程 ES module。

## Onetake

先读 dependencies-and-license.md。优先使用用户已有、授权适用的安装。没有安装且属于非商业用途时，可从 https://github.com/feitangyuan/onetake 获取免费版到作品目录 onetake/；记录实际 git revision。已有匹配版本锁时 checkout 该 revision；没有时先验证兼容性再记录，不将任意最新版本称为已兼容。

需要存在 lib/motion.js 和 scripts/{stills.py,render.py,verify_promo.py,sfx_palette.py}。可初始化时传 `--onetake /absolute/path/to/onetake`，脚本会链接依赖目录和 motion.js；已经初始化的项目也可以由代理在项目内建立等价链接。不修改外部安装。

macOS/Linux 默认使用 Playwright 管理的 Chromium（必要时 `python -m playwright install chromium`）。score.py 的 PROMO_CHROMIUM_PATH 和 PROMO_SOFTWARE_GL 仅控制音效事件采集，不会自动配置上游 stills/render 脚本。先检查它们当前版本的浏览器选项。

旧版 Notion 沙盒可能需要系统 Chromium + SwiftShader。确有需要时仅修改作品目录内可修改的依赖副本，按当前源码做有针对性的兼容调整，不对共享安装执行批量 sed。原附件中的 /data、/usr/local/bin/chromium、Linux sed -i 和专属上传下载工具不是跨平台要求。

## 首帧检查

查看 comp.html 的加载状态和浏览器控制台，确认 THREE、OM、config.js、assets.js 均加载成功。WebGL 必须保留 preserveDrawingBuffer；图片内联由 build.py 完成。中文字体用当前机器可用字体并查看实际字形，不能假定 Noto 字体存在。

渲染依赖属于用户机器上的环境，本仓库不打包浏览器、node_modules、Onetake 源码或生成成片。
