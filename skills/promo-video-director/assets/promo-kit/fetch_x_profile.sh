#!/usr/bin/env bash
# Read a public X profile with agent-browser and print JSON for config.json
# (name, verified, bio lines, link, joined, following, followers, avatar, banner).
# Works logged-out (X renders without data-testid then) and logged-in.
# Run through bash with browser:true and a named AGENT_BROWSER_SESSION.  usage: bash fetch_x_profile.sh <handle> > profile.json
set -euo pipefail
H="${1#@}"
agent-browser open "https://x.com/$H" >/dev/null; agent-browser wait 6000 >/dev/null
agent-browser eval "(() => {
  const H = '$H', L = document.body.innerText.split('\n').map(s => s.trim()).filter(Boolean);
  const iH = L.findIndex(s => s.toLowerCase() === '@' + H.toLowerCase());
  const iJ = L.findIndex((s, i) => i > iH && /^Joined /.test(s));
  const name = (document.querySelector('h1')?.innerText || L[iH - 1] || H).trim();
  let mid = iH >= 0 && iJ > iH ? L.slice(iH + 1, iJ) : [];
  mid = mid.filter(s => !/^(Show translation|Translate bio|Follows you)$/.test(s));
  let link = '';
  if (mid.length && /^[^\s]+\.[a-z]{2,}(\/\S*)?$/i.test(mid[mid.length - 1])) link = mid.pop();
  const cnt = w => { const s = L.find(x => new RegExp('^[\\\\d.,]+[KM]? ' + w + '\$').test(x)); if (!s) return null; const v = s.split(' ')[0]; return /^[\\\\d,]+\$/.test(v) ? +v.replace(/,/g, '') : v; };
  let verified = false, e = document.querySelector('h1');
  for (let k = 0; e && k < 5 && !verified; k++, e = e.parentElement) verified = !!e.querySelector('[aria-label=\"Verified account\"], [data-testid=\"icon-verified\"]');
  const imgs = [...document.images].map(i => i.src);
  return JSON.stringify({ handle: H, name, verified, bio: mid, link, joined: iJ > 0 ? L[iJ] : '',
    following: cnt('Following'), followers: cnt('Followers'),
    avatar: (imgs.find(s => s.includes('profile_images')) || '').replace(/_(normal|bigger|200x200|x96)\./, '_400x400.'),
    banner: imgs.find(s => s.includes('profile_banners')) || '' }, null, 1); })()" | python3 -c "
import sys,json; d=json.loads(json.loads(sys.stdin.read()))
for k in ('following','followers'):
    v=str(d[k] or '').replace(',','')
    d[k]=int(v) if v.isdigit() else v
print(json.dumps(d,ensure_ascii=False,indent=1))"
