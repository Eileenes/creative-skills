import React from 'react';
import {AbsoluteFill, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, Easing} from 'remotion';

const FONT = "'Noto Sans SC','Noto Sans CJK SC',sans-serif";
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const ease = Easing.bezier(0.65, 0, 0.35, 1);

// keyframe helper: kf(frame, [[f, v], ...])
const kf = (f: number, pts: [number, number][]) =>
  interpolate(f, pts.map((p) => p[0]), pts.map((p) => p[1]), {...clamp, easing: ease});

const rand = (seed: number) => {
  const x = Math.sin(seed * 9301.17 + 49297.3) * 233280.5;
  return x - Math.floor(x);
};

// jagged torn-paper polygon
const torn = (seed: number, amp = 2.2, steps = 26) => {
  const pts: string[] = [];
  for (let i = 0; i <= steps; i++) pts.push(`${(i / steps) * 100}% ${rand(seed + i) * amp}%`);
  for (let i = 0; i <= steps / 3; i++) pts.push(`${100 - rand(seed + 50 + i) * amp * 0.6}% ${(i / (steps / 3)) * 100}%`);
  for (let i = steps; i >= 0; i--) pts.push(`${(i / steps) * 100}% ${100 - rand(seed + 100 + i) * amp}%`);
  for (let i = Math.floor(steps / 3); i >= 0; i--) pts.push(`${rand(seed + 150 + i) * amp * 0.6}% ${(i / (steps / 3)) * 100}%`);
  return `polygon(${pts.join(',')})`;
};

const NOISE = `url("data:image/svg+xml;utf8,${encodeURIComponent(
  `<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0.35  0 0 0 0 0.28  0 0 0 0 0.18  0 0 0 0.22 0'/></filter><rect width='300' height='300' filter='url(#n)'/></svg>`
)}")`;

const XLogo: React.FC<{size: number; color?: string; style?: React.CSSProperties}> = ({size, color = '#fff', style}) => (
  <svg width={size} height={size} viewBox="0 0 24 24" style={style}><path fill={color} d="M21.742 21.75l-7.563-11.179 7.056-8.321h-2.456l-5.691 6.714-4.54-6.714H2.359l7.29 10.776L2.25 21.75h2.456l6.035-7.118 4.818 7.118h6.191-.008zM7.739 3.818L18.81 20.182h-2.447L5.29 3.818h2.447z"/></svg>
);

const P3: React.CSSProperties = {position: 'absolute', transformStyle: 'preserve-3d'};

// ---------- Camera ----------
const Stage: React.FC<{rx: number; rz: number; s: number; cx: number; cy: number; ty?: number; children: React.ReactNode}> = ({rx, rz, s, cx, cy, ty = 0, children}) => (
  <AbsoluteFill style={{perspective: 2000, perspectiveOrigin: '50% 45%'}}>
    <div style={{...P3, left: 0, top: 0, width: 0, height: 0, transform: `translate(960px, ${560 + ty}px) scale(${s}) rotateX(${rx}deg) rotateZ(${rz}deg) translate(${-cx}px, ${-cy}px)`}}>
      {children}
    </div>
  </AbsoluteFill>
);

// ---------- Background ----------
const Backdrop: React.FC<{tint?: string}> = ({tint = '#121722'}) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 40%, ${tint} 0%, #07080c 55%, #000 100%)`}}>
      {new Array(40).fill(0).map((_, i) => {
        const x = rand(i) * 1920;
        const y = (rand(i + 7) * 1080 - f * (0.2 + rand(i + 3) * 0.6)) % 1080;
        return <div key={i} style={{position: 'absolute', left: x, top: (y + 1080) % 1080, width: 2 + rand(i + 9) * 3, height: 2 + rand(i + 9) * 3, borderRadius: 9, background: '#9fd7ff', opacity: 0.15 + rand(i + 4) * 0.25, filter: 'blur(1px)'}} />;
      })}
    </AbsoluteFill>
  );
};

const Vignette = () => (
  <AbsoluteFill style={{pointerEvents: 'none', background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,0.75) 100%)'}} />
);

// ---------- Avatar standee ----------
const AvatarDisc: React.FC<{size: number; ring?: number}> = ({size, ring = 10}) => (
  <div style={{width: size, height: size, borderRadius: '50%', background: '#fff', padding: ring, boxSizing: 'border-box', boxShadow: `0 0 0 ${ring * 0.6}px #ff6a3d, 0 18px 40px rgba(0,0,0,0.55), 0 0 60px rgba(255,120,60,0.45)`}}>
    <Img src={staticFile('avatar.jpg')} style={{width: '100%', height: '100%', borderRadius: '50%', display: 'block'}} />
  </div>
);

const Confetti: React.FC<{start: number; n?: number; spread?: number}> = ({start, n = 36, spread = 320}) => {
  const f = useCurrentFrame() - start;
  if (f < 0 || f > 40) return null;
  const colors = ['#ff5a36', '#ffd23f', '#3ddc97', '#4cc9f0', '#ffffff', '#b388ff'];
  return (
    <>
      {new Array(n).fill(0).map((_, i) => {
        const a = rand(i + 11) * Math.PI * 2;
        const v = 0.5 + rand(i + 23) * 0.5;
        const t = f / 40;
        const d = spread * v * (1 - Math.pow(1 - t, 3));
        const x = Math.cos(a) * d;
        const y = Math.sin(a) * d * 0.8 + t * t * 120;
        return <div key={i} style={{position: 'absolute', left: x, top: y, width: 14, height: 7, background: colors[i % colors.length], borderRadius: 2, opacity: 1 - t, transform: `rotate(${rand(i) * 360 + f * 12}deg)`}} />;
      })}
    </>
  );
};

// 3D figure standing on floor at (x,y); size = figure height
const Standee: React.FC<{x: number; y: number; size: number; lift?: number; bob?: number; spin?: number; scale?: number; confettiAt?: number; opacity?: number; tilt?: number}> = ({x, y, size, lift = 0, bob = 0, spin = 0, scale = 1, confettiAt, opacity = 1, tilt = 0}) => {
  const f = useCurrentFrame();
  const ph = Math.sin(f / 6);
  const b = bob ? Math.abs(ph) * bob : 0;
  const squash = bob ? 1 - 0.06 * Math.max(0, 1 - Math.abs(ph) * 4) : 1; // squash when touching floor
  const w = size * 0.52;
  const air = Math.min(1, (lift + b) / 300);
  return (
    <div style={{...P3, left: x, top: y, width: 0, height: 0, opacity}}>
      <div style={{position: 'absolute', left: -w * 0.55, top: -w * 0.16, width: w * 1.1, height: w * 0.32, borderRadius: '50%', background: 'rgba(0,0,0,0.7)', filter: 'blur(12px)', transform: `scale(${(1 - air * 0.5) * scale})`, opacity: 1 - air * 0.5}} />
      <div style={{...P3, left: 0, top: 0, transform: `translateZ(${lift + b}px) rotateZ(${spin}deg) rotateX(-90deg) rotateZ(${tilt}deg) scale(${scale * (2 - squash)}, ${scale * squash})`, transformOrigin: '0 0'}}>
        <Img src={staticFile('figure.png')} style={{position: 'absolute', left: -w / 2, top: -size, width: w, height: size, filter: 'drop-shadow(0 0 18px rgba(255,140,90,0.35))'}} />
        {confettiAt !== undefined ? <div style={{position: 'absolute', left: 0, top: -size * 0.6}}><Confetti start={confettiAt} /></div> : null}
      </div>
    </div>
  );
};

// ---------- Paper tag (2D overlay) ----------
const Tag: React.FC<{text: string; bg: string; color: string; size: number; seed: number; rot?: number; style?: React.CSSProperties; extra?: React.ReactNode}> = ({text, bg, color, size, seed, rot = 0, style, extra}) => (
  <div style={{position: 'absolute', transform: `rotate(${rot}deg)`, filter: 'drop-shadow(0 10px 14px rgba(0,0,0,0.55))', ...style}}>
    <div style={{clipPath: torn(seed, 4), background: bg, backgroundImage: NOISE, backgroundBlendMode: 'multiply', padding: `${size * 0.16}px ${size * 0.42}px`, fontFamily: FONT, fontWeight: 900, fontSize: size, lineHeight: 1.1, color, whiteSpace: 'nowrap', letterSpacing: 1}}>
      {text}
    </div>
    {extra}
  </div>
);

const pop = (f: number, at: number, fps: number, damping = 11) => spring({frame: f - at, fps, config: {damping, stiffness: 180, mass: 0.7}});

// ================= Scene A: profile slab =================
const NAV = ['主页', '探索', '通知', '私信', 'Grok', '书签', '个人资料', '更多'];
const SceneA: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const AV = {x: -239, y: -446};
  const rx = kf(f, [[0, 60], [75, 44], [150, 46], [200, 52]]);
  const rz = kf(f, [[0, -30], [75, -14], [150, -10], [200, -4]]);
  const s = kf(f, [[0, 0.5], [75, 1.15], [140, 1.25], [200, 0.95]]);
  const cx = kf(f, [[0, -80], [75, AV.x + 40], [140, AV.x + 60], [200, 120]]);
  const cy = kf(f, [[0, -150], [75, AV.y + 60], [140, AV.y + 80], [200, 520]]);
  const p = pop(f, 62, fps, 9);
  const jt = interpolate(f, [60, 95], [0, 1], clamp);
  const jz = 220 * 4 * jt * (1 - jt);
  const jx = 260 * jt, jy = 230 * jt;
  return (
    <AbsoluteFill>
      <Backdrop />
      <Stage rx={rx} rz={rz} s={s} cx={cx} cy={cy}>
        {/* slab thickness */}
        {[18, 12, 6].map((z) => (
          <div key={z} style={{...P3, left: -750, top: -900, width: 1500, height: 1800, borderRadius: 26, background: '#1b2029', transform: `translateZ(${-z}px)`}} />
        ))}
        <div style={{...P3, left: -750, top: -900, width: 1500, height: 1800, borderRadius: 26, background: '#000', overflow: 'hidden', boxShadow: '0 0 0 2px #2a313d, 0 0 120px rgba(80,160,255,0.18)'}}>
          <div style={{position: 'absolute', left: 0, top: 0, width: 360, height: 1800, borderRight: '1px solid #2f3336', padding: '40px 0 0 70px', boxSizing: 'border-box', fontFamily: FONT, color: '#e7e9ea'}}>
            <XLogo size={64} style={{marginBottom: 30}} />
            {NAV.map((t) => <div key={t} style={{fontSize: 34, fontWeight: t.includes('个人') ? 900 : 500, margin: '0 0 34px'}}>{t}</div>)}
            <div style={{marginTop: 20, width: 230, height: 72, borderRadius: 40, background: '#eff3f4', color: '#000', fontSize: 30, fontWeight: 800, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>发帖</div>
          </div>
          <Img src={staticFile('profile.png')} style={{position: 'absolute', left: 360, top: 0, width: 1080, height: 1800}} />
        </div>
        {/* glow ring flash on avatar */}
        <div style={{...P3, left: AV.x - 130, top: AV.y - 130, width: 260, height: 260, borderRadius: '50%', border: '8px solid #ffd2a8', boxShadow: '0 0 60px #ff8a4c, inset 0 0 40px #ff8a4c', opacity: interpolate(f, [56, 64, 84], [0, 1, 0], clamp), transform: `translateZ(2px) scale(${interpolate(f, [56, 84], [0.9, 1.5], clamp)})`}} />
        <Standee x={AV.x + jx} y={AV.y + jy} size={430} lift={jz} spin={-rz} scale={p} bob={f > 95 ? 14 : 0} tilt={interpolate(f, [62, 80, 95], [0, -8, 0], clamp)} confettiAt={66} opacity={f >= 60 ? 1 : 0} />
      </Stage>
      <Vignette />
    </AbsoluteFill>
  );
};

// ================= Scene B: pinned article stand =================
const Counter: React.FC<{value: string; unit: string; style: React.CSSProperties; scale: number}> = ({value, unit, style, scale}) => (
  <div style={{position: 'absolute', fontFamily: FONT, fontWeight: 900, display: 'flex', alignItems: 'baseline', gap: 10, transform: `scale(${scale}) rotate(-4deg)`, transformOrigin: 'left center', ...style}}>
    <span style={{fontSize: 120, color: '#fff', WebkitTextStroke: '10px #0b1220', paintOrder: 'stroke fill', textShadow: '0 8px 0 #1d9bf0, 0 16px 30px rgba(0,0,0,0.7)'}}>{value}</span>
    <span style={{fontSize: 54, color: '#fff', WebkitTextStroke: '7px #0b1220', paintOrder: 'stroke fill', textShadow: '0 5px 0 #1d9bf0'}}>{unit}</span>
  </div>
);

const SceneB: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const up = pop(f, 8, fps, 13);
  const rx = kf(f, [[0, 70], [60, 74], [210, 72]]);
  const rz = kf(f, [[0, -26], [210, 14]]);
  const s = kf(f, [[0, 0.55], [60, 0.7], [210, 0.78]]);
  const cyv = kf(f, [[0, 120], [210, 40]]);
  const n = interpolate(f, [55, 140], [0, 7400], {...clamp, easing: Easing.out(Easing.cubic)});
  const cScale = pop(f, 52, fps, 9);
  const bump = f > 140 ? 1 + 0.12 * Math.exp(-(f - 140) / 5) * Math.cos((f - 140) / 1.5) : 1;
  const tagP = pop(f, 150, fps, 10);
  const glow = 0.6 + 0.4 * Math.sin(f / 6);
  return (
    <AbsoluteFill>
      <Backdrop tint="#0f1a2a" />
      <Stage rx={rx} rz={rz} s={s} cx={0} cy={cyv} ty={230}>
        {/* floor */}
        <div style={{...P3, left: -1600, top: -1200, width: 3200, height: 2400, background: 'radial-gradient(ellipse at center, #141a24 0%, #07090d 60%, rgba(0,0,0,0) 75%)'}} />
        {/* neon base outline */}
        <div style={{...P3, left: -620, top: -40, width: 1240, height: 300, borderRadius: 10, border: '5px solid #34d6ff', boxShadow: `0 0 ${30 * glow}px #34d6ff, 0 0 ${80 * glow}px rgba(52,214,255,0.6), inset 0 0 40px rgba(52,214,255,0.35)`, opacity: interpolate(f, [10, 30], [0, 1], clamp)}} />
        {/* base slab */}
        <div style={{...P3, left: -560, top: 0, width: 1120, height: 200, background: 'linear-gradient(#2a2f38,#15181e)', borderRadius: 8, transform: 'translateZ(30px)', boxShadow: '0 0 0 2px #39414e'}} />
        {[10, 20].map((z) => <div key={z} style={{...P3, left: -560, top: 0, width: 1120, height: 200, background: '#0f1116', borderRadius: 8, transform: `translateZ(${z}px)`}} />)}
        {/* card standing */}
        <div style={{...P3, left: -520, top: 60, width: 0, height: 0, transform: `translateZ(30px) rotateX(${-90 * up}deg)`, transformOrigin: '0 0'}}>
          <div style={{position: 'absolute', left: 0, top: -808, width: 1040, height: 808, borderRadius: 18, overflow: 'hidden', background: '#000', boxShadow: '0 0 0 3px #2f3336, 0 30px 60px rgba(0,0,0,0.6)'}}>
            <Img src={staticFile('tweet0.png')} style={{width: 1040, height: 808, display: 'block'}} />
            <div style={{position: 'absolute', inset: 0, background: `linear-gradient(115deg, rgba(255,255,255,0) ${interpolate(f, [30, 90], [-20, 120], clamp)}%, rgba(255,255,255,0.22) ${interpolate(f, [30, 90], [-10, 130], clamp)}%, rgba(255,255,255,0) ${interpolate(f, [30, 90], [0, 140], clamp)}%)`}} />
          </div>
        </div>
        <Standee x={680} y={130} size={360} bob={18} scale={pop(f, 30, fps)} confettiAt={142} />
      </Stage>
      <Counter value={n >= 1000 ? (n / 1000).toFixed(1) + 'K' : Math.round(n).toString()} unit="浏览" scale={cScale * bump} style={{left: 1180, top: 770}} />
      <Tag text="梁山好汉 10/108" bg="#e24a3b" color="#fff" size={44} seed={7} rot={3} style={{left: 250, top: 120, transform: `scale(${tagP}) rotate(3deg)`}} />
      <Vignette />
    </AbsoluteFill>
  );
};

// ================= Scene C: paper collage diorama =================
const WallItem: React.FC<{at: number; z: number; style: React.CSSProperties; children: React.ReactNode}> = ({at, z, style, children}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = pop(f, at, fps, 10);
  return <div style={{...P3, ...style, opacity: p > 0.02 ? 1 : 0, transform: `translateZ(${z + (1 - p) * 260}px) scale(${0.4 + 0.6 * p}) ${style.transform || ''}`}}>{children}</div>;
};

const StatCard: React.FC<{num: string; label: string; seed: number; accent: string}> = ({num, label, seed, accent}) => (
  <div style={{clipPath: torn(seed, 3), background: '#f1e7d0', backgroundImage: NOISE, width: 250, height: 190, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', fontFamily: FONT, boxShadow: 'inset 0 0 30px rgba(120,90,40,0.25)'}}>
    <div style={{fontSize: 88, fontWeight: 900, color: '#16181c', lineHeight: 1}}>{num}</div>
    <div style={{fontSize: 34, fontWeight: 900, color: '#fff', background: accent, padding: '2px 14px', marginTop: 8}}>{label}</div>
  </div>
);

const SceneC: React.FC = () => {
  const f = useCurrentFrame();
  const shake = Math.sin(f / 9) * 0.6;
  const rx = kf(f, [[0, 76], [70, 80], [240, 78]]);
  const rz = kf(f, [[0, -22], [90, -4], [240, 9]]) + shake;
  const s = kf(f, [[0, 0.48], [80, 0.74], [240, 0.8]]);
  const W = 1640, H = 820;
  const walkX = kf(f, [[40, -760], [200, 600]]);
  const photos = ['m1.jpg', 'm2.jpg', 'm3.jpg', 'm4.jpg'];
  return (
    <AbsoluteFill>
      <Backdrop tint="#1a1610" />
      <Stage rx={rx} rz={rz} s={s} cx={0} cy={kf(f, [[0, 60], [240, 0]])} ty={150}>
        <div style={{...P3, left: -1500, top: -1100, width: 3000, height: 2200, background: 'radial-gradient(ellipse at center, #1c1a17 0%, #08080a 55%, rgba(0,0,0,0) 72%)'}} />
        {/* platform */}
        <div style={{...P3, left: -W / 2 - 40, top: -40, width: W + 80, height: 300, background: '#121318', boxShadow: '0 0 0 2px #2b2e36, 0 0 60px rgba(0,0,0,0.8)', transform: 'translateZ(2px)'}} />
        {/* wall standing at y=0 */}
        <div style={{...P3, left: -W / 2, top: 0, width: 0, height: 0, transform: 'rotateX(-90deg)', transformOrigin: '0 0'}}>
          <div style={{...P3, left: 0, top: -H, width: W, height: H}}>
            {/* back paper */}
            <div style={{position: 'absolute', inset: 0, clipPath: torn(3, 1.2, 40), background: '#efe5cc', backgroundImage: NOISE, boxShadow: 'inset 0 0 80px rgba(110,80,30,0.35)'}} />
            <div style={{position: 'absolute', left: 0, bottom: 0, width: W, height: 330, clipPath: torn(19, 6, 40), overflow: 'hidden'}}>
              <Img src={staticFile('banner.jpg')} style={{width: W, height: 330, objectFit: 'cover', filter: 'grayscale(0.6) sepia(0.35) contrast(1.1) brightness(0.85) hue-rotate(170deg) saturate(1.6)'}} />
            </div>
            <WallItem at={18} z={30} style={{left: 50, top: 50}}>
              <Tag text="AI 新工具测评" bg="#d93a2b" color="#fff" size={110} seed={31} rot={-3} style={{position: 'relative'}} />
            </WallItem>
            <WallItem at={34} z={18} style={{left: 80, top: 250}}>
              <Tag text="产品经理 | Vibe Coding 选手" bg="#16181c" color="#f1e7d0" size={46} seed={41} rot={1.5} style={{position: 'relative'}} />
            </WallItem>
            {photos.map((ph, i) => (
              <WallItem key={ph} at={50 + i * 9} z={20 + i * 12} style={{left: 960 + i * 150, top: 40 + (i % 2) * 40, transform: `rotate(${(i - 1.5) * 7}deg)`}}>
                <div style={{background: '#fff', padding: 10, paddingBottom: 34, boxShadow: '0 14px 30px rgba(0,0,0,0.45)'}}>
                  <Img src={staticFile(ph)} style={{width: 190, height: 290, objectFit: 'cover', display: 'block'}} />
                </div>
              </WallItem>
            ))}
            {[['395', '帖子', '#1d9bf0'], ['591', '粉丝', '#d93a2b'], ['324', '关注', '#16181c']].map(([num, lab, ac], i) => (
              <WallItem key={lab} at={90 + i * 10} z={40} style={{left: 90 + i * 290, top: 400, transform: `rotate(${(i - 1) * -3}deg)`}}>
                <StatCard num={num} label={lab} seed={60 + i * 9} accent={ac} />
              </WallItem>
            ))}
            <WallItem at={130} z={46} style={{left: 960, top: 470}}>
              <Tag text="1024 程序员节快乐！" bg="#f1e7d0" color="#d93a2b" size={56} seed={88} rot={-2} style={{position: 'relative'}} />
            </WallItem>
            <WallItem at={148} z={52} style={{left: 300, top: 680}}>
              <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 48, color: '#fff', WebkitTextStroke: '8px #111', paintOrder: 'stroke fill'}}>测评 AI 新工具，分享真实上手体验</div>
            </WallItem>
          </div>
        </div>
        <Standee x={walkX} y={170} size={320} bob={22} spin={Math.sin(f / 7) * 8} />
      </Stage>
      <Vignette />
    </AbsoluteFill>
  );
};

// ================= Scene D: logo stage + end card =================
const XBadge: React.FC<{size: number}> = ({size}) => (
  <>
    {new Array(14).fill(0).map((_, i) => (
      <div key={i} style={{position: 'absolute', left: -size / 2, top: -size, width: size, height: size, borderRadius: size * 0.24, background: i === 13 ? 'linear-gradient(145deg,#2a2f37,#050607)' : `rgb(${40 + i * 3},${44 + i * 3},${52 + i * 3})`, transform: `translateZ(${i * 3}px)`, display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: i === 13 ? 'inset 0 2px 0 rgba(255,255,255,0.25), 0 0 80px rgba(29,155,240,0.35)' : undefined}}>
        {i === 13 ? <XLogo size={size * 0.58} style={{filter: 'drop-shadow(0 5px 0 #8f99a8) drop-shadow(0 10px 18px rgba(0,0,0,0.6))'}} /> : null}
      </div>
    ))}
  </>
);

const SceneD: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const rise = pop(f, 6, fps, 12);
  const spin = interpolate(rise, [0, 1], [-200, 0]) + Math.sin(f / 30) * 6;
  const rx = kf(f, [[0, 68], [270, 74]]);
  const rz = kf(f, [[0, -16], [270, 6]]);
  const s = kf(f, [[0, 0.75], [60, 0.95], [270, 0.9]]);
  const drop = spring({frame: f - 44, fps, config: {damping: 8, stiffness: 120}});
  const BX = 380;
  const badgeH = 360;
  const t1 = pop(f, 80, fps), t2 = pop(f, 96, fps), t3 = pop(f, 116, fps), t4 = pop(f, 132, fps, 8);
  const crown = pop(f, 150, fps, 7);
  const typed = '@Eileeness160708'.slice(0, Math.max(1, Math.floor(interpolate(f, [100, 125], [1, 16], clamp))));
  const fadeOut = interpolate(f, [250, 270], [1, 0], clamp);
  const Group = (
    <div style={{...P3, left: BX, top: 0, width: 0, height: 0, transform: `translateZ(${interpolate(rise, [0, 1], [-420, 0])}px) rotateZ(${spin}deg) rotateX(-90deg)`, transformOrigin: '0 0'}}>
      <div style={{...P3, left: 0, top: 0, transform: 'translateZ(-21px)'}}><XBadge size={badgeH} /></div>
    </div>
  );
  return (
    <AbsoluteFill style={{opacity: fadeOut}}>
      <Backdrop tint="#151b26" />
      <Stage rx={rx} rz={rz} s={s} cx={120} cy={0} ty={170}>
        {/* reflection below floor */}
        <div style={{...P3, left: 0, top: 0, transform: 'scaleZ(-1)', opacity: 0.28}}>
          {Group}
        </div>
        {/* glossy floor */}
        <div style={{...P3, left: -1800, top: -1300, width: 3600, height: 2600, background: 'radial-gradient(ellipse at 60% 50%, rgba(46,52,64,0.82) 0%, rgba(14,16,22,0.9) 40%, rgba(0,0,0,0) 70%)'}} />
        <div style={{...P3, left: BX - 260, top: -120, width: 520, height: 240, borderRadius: '50%', background: 'radial-gradient(rgba(29,155,240,0.45), rgba(29,155,240,0) 70%)', opacity: rise}} />
        {Group}
        {/* avatar lands on top of badge */}
        <div style={{...P3, left: BX, top: 0, width: 0, height: 0, transform: `translateZ(${badgeH - 10 + (1 - drop) * 700}px)`, opacity: f > 44 ? 1 : 0}}>
          <Standee x={0} y={0} size={290} confettiAt={58} bob={f > 100 ? 10 : 0} />
        </div>
      </Stage>
      {/* end-card labels */}
      <div style={{position: 'absolute', left: 120, top: 330}}>
        <Tag text="Soren" bg="#f1e7d0" color="#16181c" size={120} seed={101} rot={-3} style={{left: 0, top: 0, transform: `scale(${t1}) rotate(-3deg)`, transformOrigin: 'left center'}}
          extra={<div style={{position: 'absolute', right: -40, top: -60, fontSize: 90, transform: `scale(${crown}) rotate(18deg)`}}>👑</div>} />
        <Tag text={typed} bg="#1d9bf0" color="#fff" size={50} seed={111} rot={2} style={{left: 40, top: 205, transform: `scale(${t2}) rotate(2deg)`, transformOrigin: 'left center'}} />
        <Tag text="AI 新工具测评" bg="#f1e7d0" color="#16181c" size={78} seed={121} rot={-1} style={{left: 0, top: 330, transform: `scale(${t3}) rotate(-1deg)`, transformOrigin: 'left center'}} />
        <Tag text="关注 Soren" bg="#d93a2b" color="#fff" size={78} seed={131} rot={2} style={{left: 560, top: 322, transform: `scale(${t4}) rotate(2deg)`, transformOrigin: 'left center'}} />
      </div>
      <Vignette />
    </AbsoluteFill>
  );
};

// ---------- transitions ----------
const Whip: React.FC<{children: React.ReactNode; dur: number}> = ({children, dur}) => {
  const f = useCurrentFrame();
  const inn = interpolate(f, [0, 8], [1, 0], clamp);
  const out = interpolate(f, [dur - 8, dur], [0, 1], clamp);
  const k = Math.max(inn, out);
  return (
    <AbsoluteFill style={{filter: `blur(${k * 18}px) brightness(${1 + k * 0.8})`, transform: `scale(${1 + out * 0.25 - inn * 0.08})`}}>
      {children}
    </AbsoluteFill>
  );
};

export const Main: React.FC = () => (
  <AbsoluteFill style={{background: '#000'}}>
    <Sequence from={0} durationInFrames={200}><Whip dur={200}><SceneA /></Whip></Sequence>
    <Sequence from={200} durationInFrames={210}><Whip dur={210}><SceneB /></Whip></Sequence>
    <Sequence from={410} durationInFrames={225}><Whip dur={225}><SceneC /></Whip></Sequence>
    <Sequence from={635} durationInFrames={265}><Whip dur={400}><SceneD /></Whip></Sequence>
  </AbsoluteFill>
);
