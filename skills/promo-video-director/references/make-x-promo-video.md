# X 宣传片模块

输入：@handle 或主页链接；终端输入词可默认采用账号或品牌名。默认蓝色 #4D6BFE，浅色肚皮 #dfe6ff。读取工作目录 examples/x.json。

用可用浏览器读取显示名、简介、头像、横幅、关注/粉丝数；若已安装兼容的 agent-browser，可用 `bash fetch_x_profile.sh <handle> > profile.json`。先检查工具的实际输出格式，抓取失败则手动填资料。认证状态必须有依据。

profile 字段：platform=x、handle（不含 @）、name、bio（字符串数组）、avatar、banner、following、followers，可选 verified、link、joined。数字 followers 在动画里 N→N+1；“1.1M”这样的字符串不滚动，未知值写“—”。

生成：`python init_config.py profile.json --typed 品牌词 --color '#4D6BFE' --belly '#dfe6ff'`，然后检查 config.json。不要把 shell 占位词当作真实账号执行。

重点看搜索框的 @handle、主页认证和统计、Follow 按钮、片尾账号；显示名超过 18 字或 handle 很长时逐项检查溢出。其余步骤返回总技能与 production.md。
