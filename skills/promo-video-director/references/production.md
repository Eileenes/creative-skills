# 制作、预览与验收

所有命令在独立作品目录中执行，使用已准备的 Python 环境。下面参数对应模板预期接口，先查看安装版本 --help；若接口变化，适配后再运行。

## 构建和预览

```sh
python build.py config.json
python onetake/scripts/stills.py comp.html --width 1280 --height 720 --times 0.9,1.6,2.3,3.6,5.7,6.7,8.6,9.8,11.0,12.0,13.6,14.4,16.6,17.4,18.6 --cols 5 --out stills.png
```

查看 stills.png 并修复可见问题。默认模板同样要检查所有平台皮肤；编译通过不代表视觉正确。检查可读性、落点、关注前后状态和片尾。需要时额外截取出错时刻。仅改 config 后要重新 build。

用户要求预览确认时在此停止等待；完整出片已获授权且未要求确认时继续。不要调用旧 render.sh，因为它会在预览后直接开始后台渲染。

## 音效与成片

```sh
python score.py
python onetake/scripts/render.py comp.html --out promo.mp4 --sfx sfx.wav --width 1280 --height 720 --fps 30 --gpu --workers 2 --samples-max 10 --gap 12
python onetake/scripts/verify_promo.py promo.mp4
```

运行时间较长时使用当前执行环境提供的可追踪会话，保存日志并向用户报告有效进度；不能只看“后台进程已启动”就说出片成功。先根据当前环境选择 GPU 或软件渲染并确认可以抓到 WebGL 画面。不在超时后无条件清空已有帧；修改场景或配置后则不能复用旧帧冒充新渲染。

验证应包括 ffprobe 确认时长、尺寸、帧率和音轨；查看头尾及动作密集片段，检查黑帧、字体、遮挡、音效错位与明显削波。可用音频工具监听时实际试听。

旧说明把静止比例 rest 失败视为可忽略。这里不自动忽略：判断是固定风格与阈值不匹配，还是实际节奏问题。前者记录数值和理由，后者修正。不要为通过验收篡改检测器或声称失败项已通过。

## 交付

promo.mp4、stills.png、config.json；在工作目录 project-notes.md 写明素材来源、已知限制、渲染参数、依赖版本及验证结果。分享工程前剔除凭证、个人抓取数据、node_modules、浏览器和 Onetake/Pro 源码。外部依赖以安装说明保留。
