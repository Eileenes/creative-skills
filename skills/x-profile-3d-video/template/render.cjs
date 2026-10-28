const path = require('path');
const fs = require('fs');
const {execFileSync} = require('child_process');
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
  // 合成音频：必须 -map 指定音轨，否则会选中 Remotion 自带的静音轨
  if (mode !== 'stills' && fs.existsSync('out/audio.wav')) {
    execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', 'out/video_noaudio.mp4', '-i', 'out/audio.wav', '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ac', '2', '-shortest', 'out/final.mp4']);
    const r = require('child_process').spawnSync('ffmpeg', ['-i', 'out/final.mp4', '-af', 'volumedetect', '-vn', '-f', 'null', '-'], {encoding: 'utf8'});
    console.log('\n' + (r.stderr.match(/mean_volume.*|max_volume.*/g) || []).join('\n'));
  }
  console.log('done'); process.exit(0);
})().catch((e) => { console.error(e); process.exit(1); });
