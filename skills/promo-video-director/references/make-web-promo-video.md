# 网站宣传片模块

输入：网址，或用户提供的截图和站点资料。默认主体 #4D6BFE，CTA“立即访问”；终端词取品牌名。配置参考 examples/web.json。

通过可用浏览器取标题、简介、图标和首屏截图；兼容 agent-browser 存在时可用 `bash fetch_web_page.sh '<网址>' > profile.json`，它会写 hero.png。必须查看截图，避免把错误页、Cookie 遮罩或空白页当作官网。遇验证码请用户提供截图，不绕过验证。

profile 字段：platform=web、url、name、bio（数组）、avatar、banner=hero.png。标题不适合展示时用 --name 覆盖。用 `python init_config.py profile.json --typed 品牌词 --name 展示名 --cta 立即体验` 生成配置。

可选 stats=[[值,标签],…] 与 roll 指定动画变化的数据项，-1 为不滚动；真实指标必须有依据，默认省略。hero.png 只是模板里的横幅，不能据此声称整页被精确复刻。

检查 URL、首屏截图的裁切、图标清晰度、CTA 和片尾域名。修改资料后回到 production.md。
