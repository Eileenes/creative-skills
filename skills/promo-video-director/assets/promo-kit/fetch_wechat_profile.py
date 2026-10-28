"""公众号资料 ← 任意一篇该号的公开文章链接 (mp.weixin.qq.com/s/...). No browser needed.
usage: python3 fetch_wechat_profile.py "<article url>" > profile.json
公众号没有公开粉丝数：articles / followers 留空时片子里不显示统计；用户给了数字就手动填进 profile.json。"""
import html, json, re, subprocess, sys
u = sys.argv[1]
t = subprocess.run(["curl", "-sL", "--compressed", "--max-time", "60", "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36", u],
                   capture_output=True).stdout.decode("utf-8", "ignore")
def v(name):
    m = re.search(r'(?:var\s+)?\b' + name + r'\s*=\s*(?:htmlDecode\()?["\']([^"\']*)["\']', t)
    return html.unescape(m.group(1)) if m else ""
nick = v("nickname")
if not nick: sys.exit("未解析到公众号信息（可能是验证页/链接失效），请让用户换一篇文章链接或直接提供资料")
avatar = (v("round_head_img") or v("hd_head_img") or v("ori_head_img_url")).replace("http://", "https://")
sig = v("profile_signature")
print(json.dumps({"platform": "wechat", "name": nick, "id": v("alias") or v("user_name"), "bio": [sig] if sig else [],
                  "articles": None, "followers": None, "avatar": avatar, "banner": "", "lastArticle": v("msg_title")}, ensure_ascii=False, indent=1))
