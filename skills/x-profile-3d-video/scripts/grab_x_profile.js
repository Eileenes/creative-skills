// 抓取 X 主页素材（需在 browser:true 的 bash 中运行，用 AGENT_BROWSER_CDP 连接共享浏览器）
// 用法：node grab_x_profile.js <handle> <输出目录 public/>
const {chromium} = require('playwright');
const fs = require('fs');
const [handle, out = 'public'] = process.argv.slice(2);
if (!handle) { console.error('usage: node grab_x_profile.js <handle> <outDir>'); process.exit(1); }
(async () => {
  const b = await chromium.connectOverCDP(process.env.AGENT_BROWSER_CDP);
  const ctx = await b.newContext({viewport: {width: 1400, height: 1000}, deviceScaleFactor: 2});
  await ctx.addCookies([{name: 'night_mode', value: '2', domain: '.x.com', path: '/'}]); // 暗色模式
  const p = await ctx.newPage();
  await p.goto(`https://x.com/${handle}`, {waitUntil: 'domcontentloaded'});
  await p.waitForTimeout(9000);
  // 隐藏未登录时的 "See xxx's full profile / Continue to X" 遮挡层（滚动后会重现，每次截图前都要调用）
  const hide = () => p.evaluate(() => {
    for (const e of document.querySelectorAll('*')) {
      const t = e.innerText || '';
      if (/full profile|Continue to X/.test(t) && e.getBoundingClientRect().height < 500) {
        let x = e; while (x.parentElement && /full profile/.test(x.parentElement.innerText || '') && x.parentElement.getBoundingClientRect().height < 500) x = x.parentElement;
        x.style.display = 'none';
      }
    }
  });
  await hide(); await p.waitForTimeout(500);
  await p.screenshot({path: `${out}/profile.png`, clip: {x: 331, y: 0, width: 600, height: 1000}}); // 主栏 → 1200x2000
  // 资料与图片地址
  const info = await p.evaluate(() => {
    const txt = (s) => document.querySelector(s)?.innerText || '';
    const imgs = [...new Set([...document.images].map((i) => i.src))];
    return {
      name: txt('[data-testid="UserName"]').split('\n')[0],
      bio: txt('[data-testid="UserDescription"]'),
      following: txt('a[href$="/following"]'), followers: txt('a[href$="/verified_followers"], a[href$="/followers"]'),
      posts: (document.body.innerText.match(/([\d.,KM万]+)\s*(posts|帖子)/) || [])[1] || '',
      avatar: imgs.find((s) => s.includes('profile_images') && !s.includes('_normal'))?.replace(/_\d+x\d+/, '_400x400'),
      banner: imgs.find((s) => s.includes('profile_banners')),
      media: imgs.filter((s) => s.includes('/media/')).map((s) => s.replace(/format=\w+&name=\w+/, 'format=jpg&name=large')),
    };
  });
  // 单条帖子截图（第 0 条一般是置顶帖）
  const tw = p.locator('article'); const n = await tw.count(); info.tweets = [];
  for (let i = 0; i < Math.min(n, 6); i++) {
    try {
      await tw.nth(i).scrollIntoViewIfNeeded(); await p.waitForTimeout(1500); await hide(); await p.waitForTimeout(300);
      await tw.nth(i).screenshot({path: `${out}/tweet${i}.png`});
      info.tweets.push((await tw.nth(i).innerText()).replace(/\n/g, ' | ').slice(0, 200));
    } catch (e) {}
  }
  fs.writeFileSync(`${out}/profile_info.json`, JSON.stringify(info, null, 2));
  console.log(JSON.stringify(info, null, 2));
  await p.close(); await ctx.close(); process.exit(0);
})().catch((e) => { console.error(e); process.exit(1); });
