# 微信公众号宣传片模块

输入：公众号任意文章链接，或名称、微信号、功能介绍和头像。默认终端词 wechat，主体 #07C160、肚皮 #dcf7e8。配置参考 examples/wechat.json。

可用 `python fetch_wechat_profile.py '<文章链接>' > profile.json` 解析公开文章。如果解析失败，检查页面内容，换用户给的其他链接或手填，不捏造资料。

profile 字段：platform=wechat、name、id、bio（数组）、avatar；可选 subject、verified、articles、followers。没有可靠数据就不填统计，不把“位朋友关注”写成公众号总粉丝数。gh_ 开头原始 ID 可以由用户提供准确微信号替换。

生成：`python init_config.py profile.json --typed 品牌词 --color '#07C160' --belly '#dcf7e8'`。

检查功能介绍换行、主体及认证依据、绿色“关注公众号”按钮、片尾“微信搜一搜”。画面是模板模拟的搜索和主页，不声称是实际网页录屏。其余步骤返回 production.md。
