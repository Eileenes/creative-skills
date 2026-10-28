"""config.json → config.js + assets.js (avatar/banner may be URLs or local paths).  usage: python3 build.py config.json"""
import base64, json, sys, urllib.request
cfg = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "config.json"))
P = cfg.setdefault("platform", "x")
need = {"x": ["handle", "following", "followers"], "xhs": ["followers"], "wechat": [], "web": ["url"]}.get(P)
if need is None: sys.exit("platform must be x | xhs | wechat | web")
need = need + ["name", "bio", "avatar", "typed", "mascot", "end"]
miss = [k for k in need if k not in cfg]
if miss: sys.exit(f"config missing: {miss}")
cfg.setdefault("verified", False); cfg.setdefault("link", ""); cfg.setdefault("joined", "")
rb = " · ".join(cfg["bio"][:2]); cfg.setdefault("resultBio", rb if len(rb) <= 40 else rb[:39] + "…")
cfg.setdefault("termTitle", f'{cfg.get("handle") or cfg["typed"]} — {cfg["typed"]} — zsh — 80×24'.lower())
cfg.setdefault("termFooter", {"x": "say hi on X →", "xhs": "来小红书找我 →", "wechat": "来公众号找我 →", "web": "come say hi →"}[P])
DEF = {"x": ([["Trending", "AI"], ["Technology", "#VibeCoding"], ["Trending", "three.js"]], [["three.js", "@threejs", "#2b3a67"], ["Notion", "@NotionHQ", "#4d6bfe"]]),
       "xhs": ([["热搜", "AI 工具测评"], ["热搜", "Vibe Coding"], ["热搜", "效率神器"]], [["AI 探索家", "小红书号：ai2025", "#ff6b81"], ["效率研究所", "小红书号：xiaolv", "#ffb3c1"]]),
       "wechat": ([["热搜", "AI 新工具"], ["热搜", "大模型"], ["热搜", "产品经理"]], [["AI 前线", "微信号：ai_front", "#07c160"], ["产品沉思录", "微信号：pmthink", "#2aae67"]]),
       "web": ([["相关", cfg["name"] + " 是什么"], ["相关", cfg["name"] + " 怎么用"], ["相关", cfg["name"] + " 官网"]], [["GitHub", "github.com", "#2b3a67"], ["Product Hunt", "producthunt.com", "#da552f"]])}[P]
cfg.setdefault("trends", DEF[0]); cfg.setdefault("whoToFollow", DEF[1])
cfg["mascot"].setdefault("belly", "#e6ecff")
if len(cfg["bio"]) > 4: print("warn: only the first 4 bio lines are shown")
for k in ("name",):
    if len(cfg[k]) > 18: print(f"warn: {k} is long ({len(cfg[k])} chars); check stills for overlap")
def data(src):
    raw = urllib.request.urlopen(urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read() if src.startswith("http") else open(src, "rb").read()
    mime = ("image/png" if raw[:4] == b"\x89PNG" else "image/webp" if raw[:4] == b"RIFF" else "image/gif" if raw[:3] == b"GIF"
            else "image/svg+xml" if raw.lstrip()[:1] == b"<" else "image/x-icon" if raw[:4] == b"\0\0\1\0" else "image/jpeg")
    return f"data:{mime};base64," + base64.b64encode(raw).decode()
if not cfg.get("banner"):  # no banner (common on 小红书/公众号): brand-tinted gradient
    from PIL import Image
    import io
    acc = {"x": (29, 155, 240), "xhs": (255, 36, 66), "wechat": (7, 193, 96), "web": (91, 108, 255)}[P]
    im = Image.new("RGB", (1500, 500)); px = im.load()
    for x in range(1500):
        k = x / 1499
        for y in range(500): px[x, y] = tuple(int(a * (0.55 + 0.45 * k) * (1 - y / 900)) for a in acc)
    b = io.BytesIO(); im.save(b, "PNG"); open("_banner.png", "wb").write(b.getvalue()); cfg["banner"] = "_banner.png"
def avatar():
    try: return data(cfg["avatar"])
    except Exception as e:  # e.g. favicon 404 → letter avatar
        print(f"warn: avatar failed ({e}); using a letter avatar")
        from PIL import Image, ImageDraw, ImageFont
        import io
        im = Image.new("RGB", (400, 400), cfg["mascot"]["color"]); d = ImageDraw.Draw(im)
        try: f = ImageFont.truetype("/usr/share/fonts/google-noto-cjk/NotoSansSC-Bold.otf", 220)
        except Exception: f = ImageFont.load_default()
        d.text((200, 200), cfg["name"][:1].upper(), fill="white", font=f, anchor="mm"); b = io.BytesIO(); im.save(b, "PNG")
        return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()
open("assets.js", "w").write(f'window.AVATAR="{avatar()}";window.BANNER="{data(cfg["banner"])}";')
open("config.js", "w").write("window.CFG=" + json.dumps(cfg, ensure_ascii=False) + ";")
print(f"wrote config.js + assets.js · platform={P} · {cfg['name']}")
