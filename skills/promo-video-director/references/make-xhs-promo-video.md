# 小红书宣传片模块

输入：小红书主页分享链接，或昵称、小红书号、简介、头像。默认终端词 xiaohongshu，主体 #FF2442、肚皮 #ffe3e8。配置参考 examples/xhs.json。

有兼容 agent-browser 时可用 `bash fetch_xhs_profile.sh '<链接>' > profile.json`，也可使用当前环境浏览器读取公开资料。出现登录墙或 name 为空时不要反复尝试，集中询问缺少的资料。

profile 字段：platform=xhs、name、id、bio（数组）、avatar、following、followers、likes；ip 有公开资料时填写。bio 最多四行。抓到“1千+”保留字符串，不反推准确粉丝数；只有已知数字才演示 +1。

生成：`python init_config.py profile.json --typed 品牌词 --color '#FF2442' --belly '#ffe3e8'`。

检查昵称搜索、小红书号、IP、关注/粉丝/获赞标签、红色关注按钮以及片尾“小红书搜索”。默认仍是横屏 720p，不因平台名自动声称支持竖屏。需要竖屏时进入定制模式。其余步骤返回 production.md。
