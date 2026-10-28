#!/usr/bin/env bash
# Read a 小红书 profile (share link from the app: 个人主页 → 分享 → 复制链接) with agent-browser → JSON for init_config.py.
# Logged-out pages often hit a login wall; then ask the user for name / 小红书号 / bio / counts / avatar instead.
# Run through bash with browser:true and a named AGENT_BROWSER_SESSION.  usage: bash fetch_xhs_profile.sh "<profile url>" > profile.json
set -euo pipefail
U="$1"
agent-browser open "$U" >/dev/null; agent-browser wait 6000 >/dev/null
agent-browser eval "(() => {
  const st = window.__INITIAL_STATE__ || {}, ud = (st.user && (st.user.userPageData?._value || st.user.userPageData)) || {};
  const bi = ud.basicInfo || {}, it = ud.interactions || [];
  const n = t => (it.find(x => x.type === t) || {}).count;
  const L = document.body.innerText.split('\n').map(s => s.trim()).filter(Boolean);
  const pick = re => (L.find(s => re.test(s)) || '');
  const num = w => { const s = L.find(x => new RegExp('^[\\\\d.万千+]+\\\\s*' + w + '\$').test(x)) || ''; return s.replace(w, '').trim(); };
  return JSON.stringify({ platform: 'xhs',
    name: bi.nickname || (document.title || '').replace(/ - 小红书\$/, ''),
    id: bi.redId || pick(/^小红书号/).replace(/^小红书号[：:]\s*/, ''),
    bio: (bi.desc || '').split('\n').filter(Boolean),
    ip: bi.ipLocation || pick(/^IP属地/).replace(/^IP属地[：:]\s*/, ''),
    following: n('follows') ?? num('关注'), followers: n('fans') ?? num('粉丝'), likes: n('interaction') ?? num('获赞与收藏'),
    avatar: bi.imageb || bi.images || ([...document.images].map(i => i.src).find(s => /sns-avatar/.test(s)) || ''),
    banner: '', loginWall: /登录后推荐更懂你的笔记|手机号登录/.test(document.body.innerText) && !bi.nickname }, null, 1); })()" | python3 -c "
import sys,json; d=json.loads(json.loads(sys.stdin.read()))
for k in ('following','followers','likes'):
    v=str(d[k] or '').replace(',','')
    d[k]=int(v) if v.isdigit() else v
print(json.dumps(d,ensure_ascii=False,indent=1))"
