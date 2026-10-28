"""profile.json (from a fetch_* script) + a few choices → config.json
usage: python3 init_config.py profile.json --typed deepseek [--color "#4D6BFE"] [--tagline "..."] [--title "..."] [--cta "立即体验"] [--out config.json]
profile.json platform: x | xhs | wechat | web (from fetch_x_profile.sh / fetch_xhs_profile.sh / fetch_wechat_profile.py / fetch_web_page.sh)"""
import argparse, json
ap = argparse.ArgumentParser()
ap.add_argument("profile"); ap.add_argument("--typed", required=True, help="word typed in the terminal (product / brand)")
ap.add_argument("--color", default="#4D6BFE", help="mascot hex color"); ap.add_argument("--belly", default=None)
ap.add_argument("--tagline", default=None); ap.add_argument("--title", default=None); ap.add_argument("--footer", default=None)
ap.add_argument("--name", default=None, help="override display name (web pages often have odd titles)")
ap.add_argument("--cta", default=None, help="web only: button label, e.g. 立即体验 / Get started")
ap.add_argument("--out", default="config.json")
a = ap.parse_args(); p = json.load(open(a.profile))
if a.name: p["name"] = a.name
P = p.get("platform", "x")
bio = [b for b in p.get("bio", []) if b and b.strip()][:4] or [" "]
skip = {"bio", "loginWall", "pageTitle", "ogImage", "lastArticle"}
cfg = {k: v for k, v in p.items() if k not in skip and v not in (None, "")}
cfg.update(platform=P, bio=bio, typed=a.typed, mascot={"preset": "whale", "color": a.color},
           end={"title": a.title or p["name"], "tagline": a.tagline or (lambda t: t if len(t) <= 48 else t[:47] + "…")(" · ".join(bio[:2]))})
if a.belly: cfg["mascot"]["belly"] = a.belly
if a.footer: cfg["termFooter"] = a.footer
if a.cta: cfg["ui"] = {"follow": [a.cta, "✓ " + a.cta]}
if p.get("loginWall"): print("warn: 页面被登录墙挡住，资料可能不全——请向用户确认名字/简介/粉丝数/头像")
json.dump(cfg, open(a.out, "w"), ensure_ascii=False, indent=1)
print(f"wrote {a.out} (platform={P}); review bio/tagline/trends/stats, then: python3 build.py {a.out}")
