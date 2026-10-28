// Reference excerpt from comp.html: voxel model, instanced mesh, blob shadow, hop path, idle moves, assembly.
// Depends on THREE, OM (motion.js), BLUE, Tw/Dw/Bw/Ew anchors and plane()/mkCanvas() helpers from comp.html.
// ───────── the whale (voxels)
const V = 0.088;
const VOX = []; // {x,y,z,col,part}
{
  const R = OM.rng(11), set = new Map(), K = (x, y, z) => x + ',' + y + ',' + z;
  const add = (x, y, z, part) => set.set(K(x, y, z), {x, y, z, part});
  for (let x = -7; x <= 8; x++) for (let y = 0; y <= 7; y++) for (let z = -4; z <= 4; z++) {
    const u = (x - 0.8) / 7.9, f = Math.pow(Math.max(0, 1 - Math.pow(Math.abs(u), 3.2)), 1 / 3.2) * (x < 0 ? 1 - 0.5 * (-x / 7) : 1);
    const cy = 3.4 + (x < -2 ? (-2 - x) * 0.18 : 0), hy = 3.5 * f, hz = 3.5 * f; if (hy < 0.6) continue;
    const p = 2.7; if (Math.pow(Math.abs(y - cy) / hy, p) + Math.pow(Math.abs(z) / hz, p) <= 1) add(x, y, z, 'body');
  }
  for (let x = -10; x <= -8; x++) for (let y = 4; y <= 5; y++) for (let z = -1; z <= 1; z++) if (!(Math.abs(z) === 1 && y === 5)) add(x, y + (x === -10 ? 1 : 0), z, 'tail');
  for (let z = -4; z <= 4; z++) { const lift = Math.abs(z) >= 3 ? 1 : 0; add(-11 - (Math.abs(z) >= 3 ? 1 : 0), 6 + lift, z, 'tail'); if (Math.abs(z) <= 2) add(-11, 5, z, 'tail'); }
  for (const s of [-1, 1]) { add(1, 1, s * 4, 'fin'); add(2, 1, s * 4, 'fin'); add(1, 0, s * 5, 'fin'); add(2, 0, s * 5, 'fin'); add(3, 0, s * 5, 'fin'); }
  const has = (x, y, z) => set.has(K(x, y, z));
  for (const v of set.values()) {
    if (has(v.x + 1, v.y, v.z) && has(v.x - 1, v.y, v.z) && has(v.x, v.y + 1, v.z) && has(v.x, v.y - 1, v.z) && has(v.x, v.y, v.z + 1) && has(v.x, v.y, v.z - 1)) continue;
    let col = new THREE.Color(BLUE);
    if (v.part === 'body' && v.y <= 1 && v.x > -3) col = new THREE.Color('#dfe6ff');
    if (v.part === 'body' && v.y === 2 && v.x >= 6 && Math.abs(v.z) <= 2) col = new THREE.Color('#1f2f8f');
    const sh = 0.93 + 0.12 * R() + (v.y >= 7 ? 0.06 : 0); col.multiplyScalar(sh);
    VOX.push({x: v.x, y: v.y, z: v.z, col, part: v.part, d: Math.hypot(v.x - 8, v.y - 3, v.z)});
  }
  // eyes: outermost voxels on each side, 2×2 at x 4..5, y 3..4, highlight top-front
  for (const sd of [-1, 1]) for (const x of [4, 5]) for (const y of [3, 4]) { let best = null; for (const v of VOX) if (v.x === x && v.y === y && Math.sign(v.z) === sd && (!best || Math.abs(v.z) > Math.abs(best.z))) best = v; if (best) { const hi = x === 5 && y === 4; best.col = new THREE.Color(hi ? '#ffffff' : '#070b18'); best.part = hi ? 'eyehi' : 'eye'; } }
  // spout voxels
  for (let j = 0; j < 5; j++) VOX.push({x: 3, y: 9, z: 0, col: new THREE.Color(j < 3 ? '#a9d4ff' : '#d8ecff'), part: 'spout', j, d: 0});
  const ds = VOX.map(v => v.d), dmax = Math.max(...ds); VOX.forEach(v => v.dn = v.d / dmax);
}
const whale = new THREE.Group(); scene.add(whale);
const vMesh = new THREE.InstancedMesh(new THREE.BoxGeometry(V * 0.93, V * 0.93, V * 0.93), new THREE.MeshStandardMaterial({roughness: .55, metalness: .05}), VOX.length);
vMesh.frustumCulled = false; VOX.forEach((v, i) => vMesh.setColorAt(i, v.col)); whale.add(vMesh);
const shadow = (() => { const c = mkCanvas(256, 256), g = c.getContext('2d'), gr = g.createRadialGradient(128, 128, 10, 128, 128, 126); gr.addColorStop(0, 'rgba(0,0,0,0.85)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(0, 0, 256, 256); const p = plane(1.9, 1.3, mkTex(c), {transparent: true}); p.material.depthWrite = false; scene.add(p); return p; })();

// whale path: hops between anchors that move with what they sit on
const WHALE_HOME = Tw(760, 560);
const HOPS = [
  {t0: 2.78, t1: 3.28, a: t => WHALE_HOME, b: t => Dw(0, t), h: 1.7, land: 'tile', i: 0},
  {t0: 3.38, t1: 3.62, a: t => Dw(0, t), b: t => Dw(1, t), h: 0.55, land: 'tile', i: 1},
  {t0: 3.72, t1: 3.96, a: t => Dw(1, t), b: t => Dw(2, t), h: 0.55, land: 'tile', i: 2},
  {t0: 4.04, t1: 4.38, a: t => Dw(2, t), b: t => Dw(3, t), h: 0.95, land: 'tile', i: 3, big: 1},
  {t0: 5.02, t1: 5.48, a: t => Dw(3, t), b: t => Bw(650, 62, t), h: 1.5, big: 1},
  {t0: 5.86, t1: ENTER_T, a: t => Bw(650, 62, t), b: t => Bw(1390, 62, t), h: 0.8, big: 1},
  {t0: 7.22, t1: 7.62, a: t => Bw(1390, 62, t), b: t => Bw(SRCH_X + 20, 205, t), h: 1.2, big: 1},
];
for (let j = 0; j < SRCH_HOPS; j++) { const t0 = SRCH_T0 + j * SRCH_DT; HOPS.push({t0, t1: t0 + 0.17, a: (k => t => Bw(k, 205, t))(j === 0 ? SRCH_X + 20 : srchX(2 * j) + 30), b: (k => t => Bw(k, 205, t))(srchX(2 * j + 2) + 30), h: 0.32, small: 1}); }
HOPS.push({t0: 9.55, t1: 9.95, a: t => Bw(srchX(16) + 30, 205, t), b: t => Bw(1150, 470, t), h: 0.9, big: 1});
HOPS.push({t0: 11.0, t1: 11.36, a: t => Bw(1150, 470, t), b: t => Bw(860, 300, t), h: 0.55});
HOPS.push({t0: 12.62, t1: FOLLOW_T, a: t => Bw(860, 300, t), b: t => Bw(1300, 545, t), h: 2.1, big: 2});
HOPS.push({t0: 13.72, t1: 13.98, a: t => Bw(1300, 545, t), b: t => Bw(1000, 400, t), h: 0.6});
HOPS.push({t0: 14.35, t1: 14.6, a: t => Bw(1000, 400, t), b: t => Bw(1000, 400, t), h: 0.45});
HOPS.push({t0: 15.3, t1: END_LAND, a: t => Bw(1000, 400, t), b: t => Ew(1660, 440), h: 3.0, big: 2});
const LANDS = HOPS.map(h => h.t1);
HOPS.forEach(h => { if (h.land === 'tile') DOCK_HITS.push([h.i, h.t1]); });
const ASM_T0 = 1.14, ASM_T1 = 1.88;
const facing = d => Math.atan2(-d.z, d.x);
const YAW_CAM = -Math.PI / 2;
const YK = [[0, YAW_CAM + 1.1], [2.05, YAW_CAM + 0.75], [2.3, YAW_CAM + 1.45], [2.55, YAW_CAM + 0.9]];
HOPS.forEach(h => { const d = h.b(h.t1).clone().sub(h.a(h.t0)); if (Math.hypot(d.x, d.z) > 0.05) YK.push([h.t0 - 0.12, facing(d)]); });
YK.push([6.5, YAW_CAM + 0.25], [10.7, YAW_CAM + 0.3], [11.4, YAW_CAM - 0.35], [12.33, facing(Bw(1300, 545, 13).sub(Bw(860, 300, 13)))]);
YK.push([14.1, YAW_CAM + 0.2], [16.25, -Math.PI + 0.55]);
YK.sort((a, b) => a[0] - b[0]);
function yawAt(t) {
  let i = 0; while (i + 1 < YK.length && YK[i + 1][0] <= t) i++;
  if (i === 0 && t < YK[0][0]) return YK[0][1];
  const prev = i > 0 ? YK[i - 1][1] : YK[0][1], cur = YK[i][1];
  let d = cur - prev; d = Math.atan2(Math.sin(d), Math.cos(d));
  return prev + d * ease.sineInOut(seg(t, YK[i][0], YK[i][0] + 0.2));
}
function whaleState(t) {
  let pos = WHALE_HOME.clone(), ground = WHALE_HOME.y, k = 1, air = 0, hop = null;
  for (const h of HOPS) {
    if (t >= h.t1) { pos = h.b(t); ground = pos.y; hop = null; continue; }
    if (t >= h.t0) { const a = h.a(t), b = h.b(t), u = seg(t, h.t0, h.t1); k = h.small ? ease.sineInOut(u) : ease.cubicInOut(u); pos = a.clone().lerp(b, k); ground = pos.y; air = Math.sin(Math.PI * ease.sineInOut(u)) * h.h; pos.y += air; hop = h; }
    break;
  }
  let sx = 1, sy = 1, pitch = 0;
  for (const tl of LANDS) { const im = OM.impact(t, tl, {sqx: 0.22, sqy: 0.3, decay: 8, omega: 24}); sx *= im.sx; sy *= im.sy; }
  for (const h of HOPS) { const a = seg(t, h.t0 - (h.big ? 0.14 : 0.07), h.t0), crouch = Math.sin(Math.PI * a) * (h.big ? 0.2 : 0.1); sy *= 1 - crouch; sx *= 1 + crouch * 0.6; }
  if (hop) { const u = seg(t, hop.t0, hop.t1); sy *= 1 + 0.12 * Math.sin(Math.PI * u); pitch = (0.5 - u) * (hop.small ? 0.4 : 0.9); }
  // assembly lands: squash
  const im = OM.impact(t, ASM_T1, {sqx: 0.18, sqy: 0.24}); sx *= im.sx; sy *= im.sy;
  return {pos, ground, air, sx, sy, pitch, yaw: yawAt(t)};
}
const BLINKS = [2.2, 6.85, 11.5, 14.9];
const PUFFS = [2.45, 14.1, 16.75];
const M4 = new THREE.Matrix4(), Q = new THREE.Quaternion(), E3 = new THREE.Euler(), P3 = new THREE.Vector3(), S3 = new THREE.Vector3();
function placeWhale(t) {
  const st = whaleState(t);
  whale.position.copy(st.pos); whale.rotation.set(0, st.yaw, 0); whale.rotateZ(st.pitch);
  whale.scale.set(st.sx, st.sy, st.sx); whale.updateMatrixWorld(true);
  const inv = whale.matrixWorld.clone().invert();
  const cur = Tw(PROMPT_X + TYPED.length * CH_W + 20, PROMPT_Y - 20).applyMatrix4(inv);
  const blink = BLINKS.some(b => t > b && t < b + 0.13);
  const wag = (1 - stillAt(t)) * Math.sin(t * 7.5) * 0.22 + (st.air > 0.05 ? Math.sin(t * 16) * 0.2 : 0);
  const idle = Math.sin(t * 3.1) * 0.35;
  VOX.forEach((v, i) => {
    let x = v.x, y = v.y + idle * clamp((v.x + 2) / 9, 0, 1) * 0, z = v.z, s = 1;
    if (v.part === 'tail' || (v.part === 'body' && v.x <= -6)) { const w = v.part === 'tail' ? 1 : 0.35, a = wag * w, px = -4, py = 4; const dx = x - px, dy = y - py; x = px + dx * Math.cos(a) - dy * Math.sin(a); y = py + dx * Math.sin(a) + dy * Math.cos(a); }
    if (v.part === 'fin') y += (1 - stillAt(t)) * Math.sin(t * 9 + v.z) * 0.25;
    let sY = 1; if ((v.part === 'eye' || v.part === 'eyehi') && blink) sY = 0.15;
    if (v.part === 'spout') {
      s = 0; for (const tp of PUFFS) { const tau = t - tp; if (tau > 0 && tau < 0.9) { const j = v.j; if (j < 3) { y = 9 + tau * 9 + j * 1.05 - tau * tau * 4; s = Math.max(0, 1 - tau / 0.9) * 1.1; z = 0; x = 3; } else { const sd = j === 3 ? -1 : 1; x = 3; y = 9 + 3 + tau * 6 - tau * tau * 10; z = sd * tau * 7; s = Math.max(0, 1 - tau / 0.9); } } }
    }
    P3.set(x * V, (y + 0.5) * V, z * V);
    if (t < ASM_T1 + 0.01) {
      if (t < ASM_T0) s = 0;
      else { const k = clamp(spring(t - ASM_T0 - v.dn * 0.42, 0.62, 15), 0, 1.25); P3.lerpVectors(cur, P3, k); s *= clamp(k, 0, 1) * (v.part === 'spout' ? 0 : 1); }
    }
    S3.set(s, s * sY, s); M4.compose(P3, Q.identity(), S3); vMesh.setMatrixAt(i, M4);
  });
  vMesh.instanceMatrix.needsUpdate = true;
  const vis = t >= ASM_T0;
  shadow.visible = vis; shadow.position.set(st.pos.x, st.ground + 0.004, st.pos.z); shadow.rotation.z = st.yaw;
  shadow.material.opacity = clamp(1 - st.air / 2.6, 0.15, 1) * 0.75 * clamp((t - ASM_T0) * 3, 0, 1);
  const sc = 1 + st.air * 0.25; shadow.scale.set(sc, sc, 1);
  return st;
}
