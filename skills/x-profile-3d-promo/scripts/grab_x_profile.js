const { chromium } = require('playwright');
(async () => {
  const b = await chromium.connectOverCDP(process.env.AGENT_BROWSER_CDP);
  const ctx = await b.newContext({viewport:{width:1400,height:1000},deviceScaleFactor:2});
  await ctx.addCookies([{name:'night_mode',value:'2',domain:'.x.com',path:'/'}]);
  const p = await ctx.newPage();
  await p.goto('https://x.com/Eileeness160708',{waitUntil:'domcontentloaded'});
  await p.waitForTimeout(9000);
  const hide = async()=>p.evaluate(()=>{ for(const e of document.querySelectorAll('*')){ if(e.children.length<40 && /See Soren’s full profile/.test(e.innerText||'') && e.getBoundingClientRect().height<400){ let x=e; while(x.parentElement && /See Soren’s full profile/.test(x.parentElement.innerText||'') && x.parentElement.getBoundingClientRect().height<500) x=x.parentElement; x.style.display='none'; break; } } });
  await hide(); await p.waitForTimeout(500);

  const tw = p.locator('article');
  for (const i of [0,5]){ await tw.nth(i).scrollIntoViewIfNeeded(); await p.waitForTimeout(1500); await hide(); await p.evaluate(()=>{for(const e of document.querySelectorAll("*")){const s=getComputedStyle(e); if((s.position==="fixed"||s.position==="sticky") && /full profile|Continue to X/.test(e.innerText||"")) e.style.display="none";}}); await p.waitForTimeout(400); await tw.nth(i).screenshot({path:`xv/public/tweet${i}.png`}); }
  await p.close(); await ctx.close(); process.exit(0);
})().catch(e=>{console.error(e);process.exit(1)});
