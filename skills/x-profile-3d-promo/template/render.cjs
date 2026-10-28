const path = require('path');
const {bundle} = require('@remotion/bundler');
const {renderStill, renderMedia, selectComposition} = require('@remotion/renderer');
const override = (c) => {
  const walk = (rules) => rules && rules.forEach((r) => {
    const uses = Array.isArray(r.use) ? r.use : r.use ? [r.use] : [];
    uses.forEach((u) => { if (u && typeof u === 'object' && String(u.loader).includes('esbuild')) u.options = {...u.options, tsconfigRaw: {compilerOptions: {jsx: 'react-jsx'}}}; });
    if (r.loader && String(r.loader).includes('esbuild')) r.options = {...r.options, tsconfigRaw: {compilerOptions: {jsx: 'react-jsx'}}};
    walk(r.oneOf); walk(r.rules);
  });
  walk(c.module.rules);
  return c;
};
(async () => {
  const [mode, ...rest] = process.argv.slice(2);
  const serveUrl = await bundle({entryPoint: path.join(__dirname, 'src/index.ts'), webpackOverride: override, publicDir: path.join(__dirname, 'public')});
  const composition = await selectComposition({serveUrl, id: 'Main'});
  if (mode === 'stills') {
    for (const fr of rest) await renderStill({serveUrl, composition, frame: Number(fr), output: `stills/f${fr}.png`, chromiumOptions: {gl: 'angle'}});
  } else {
    await renderMedia({serveUrl, composition, codec: 'h264', outputLocation: 'out/video_noaudio.mp4', concurrency: 2, crf: 18, chromiumOptions: {gl: 'angle'}, onProgress: ({progress}) => { if (Math.round(progress * 100) % 10 === 0) process.stdout.write(`${Math.round(progress * 100)}% `); }});
  }
  console.log('done'); process.exit(0);
})().catch((e) => { console.error(e); process.exit(1); });
