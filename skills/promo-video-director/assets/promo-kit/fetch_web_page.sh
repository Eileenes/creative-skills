#!/usr/bin/env bash
# Read any web page with agent-browser → JSON (title, description, icon, hero screenshot as banner) for init_config.py.
# Run through bash with browser:true and a named AGENT_BROWSER_SESSION.  usage: bash fetch_web_page.sh <url> > profile.json
set -euo pipefail
U="$1"; case "$U" in http*) ;; *) U="https://$U";; esac
agent-browser set viewport 1500 900 >/dev/null 2>&1 || true
agent-browser open "$U" >/dev/null; agent-browser wait 5000 >/dev/null
agent-browser screenshot "$PWD/_hero_full.png" >/dev/null
python3 -c "from PIL import Image; im=Image.open('_hero_full.png').convert('RGB'); w,h=im.size; im.crop((0,0,w,min(h,w//3))).resize((1500,500)).save('hero.png')"
agent-browser eval "(() => { const m = s => document.querySelector(s)?.content?.trim() || '';
  const icons = [...document.querySelectorAll('link[rel~=icon], link[rel=apple-touch-icon], link[rel=apple-touch-icon-precomposed]')]
    .map(l => ({href: l.href, s: parseInt((l.sizes && l.sizes.value) || '0') || (l.rel.includes('apple') ? 180 : 16)})).sort((a, b) => b.s - a.s);
  const title = m('meta[property=\"og:site_name\"]') || (document.title || '').split(/ [|–—-] /)[0].trim();
  const desc = m('meta[name=description]') || m('meta[property=\"og:description\"]');
  return JSON.stringify({ platform: 'web', url: location.origin + (location.pathname === '/' ? '' : location.pathname), name: title, pageTitle: document.title,
    bio: desc ? [desc] : [], avatar: (icons[0] && icons[0].href) || (location.origin + '/favicon.ico'), ogImage: m('meta[property=\"og:image\"]'), banner: 'hero.png' }, null, 1); })()" \
  | python3 -c "import sys,json; print(json.dumps(json.loads(json.loads(sys.stdin.read())),ensure_ascii=False,indent=1))"
