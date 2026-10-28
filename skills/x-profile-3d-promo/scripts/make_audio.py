# 生成 120BPM 配乐 + 转场/弹出/计数/落字音效，输出 out/audio.wav（30 秒）
# 时间点按视频分镜修改：WHOOSH / POPS / TICK_START / THUMPS
import numpy as np, wave
sr=44100; T=30.0; n=int(sr*T); out=np.zeros(n); rng=np.random.default_rng(1)
WHOOSH=[0.0,6.4,13.4,20.9]; POPS=[2.07,7.67,23.1]; TICK_START=8.5; THUMPS=[23.8,24.3,24.9,25.4]
def add(sig,t,g=1.0):
    i=int(t*sr); e=min(n,i+len(sig)); out[i:e]+=sig[:e-i]*g
def env(L,a=0.005,d=0.2):
    t=np.arange(int(L*sr))/sr; return np.minimum(1,t/a)*np.exp(-t/d)
def sweep(L,f):
    t=np.arange(int(L*sr))/sr; return t, np.sin(2*np.pi*np.cumsum(f(t))/sr)
def kick(): t,s=sweep(0.35,lambda t:50+120*np.exp(-t/0.04)); return s*np.exp(-t/0.12)
def hat(): x=np.diff(rng.standard_normal(int(0.06*sr)),prepend=0); return x*env(0.06,0.001,0.015)*0.3
def pop(f0=500): t,s=sweep(0.18,lambda t:f0*(1+2*t/0.18)); return s*env(0.18,0.002,0.05)
def whoosh(L=0.6):
    x=rng.standard_normal(int(L*sr)); t=np.arange(len(x))/sr; y=np.zeros_like(x); a=0
    for i in range(len(x)):
        a+=(0.02+0.25*np.sin(np.pi*t[i]/L)**2)*(x[i]-a); y[i]=a
    return y*np.sin(np.pi*t/L)**1.5*1.6
def tick(): t=np.arange(int(0.03*sr))/sr; return np.sin(2*np.pi*2400*t)*env(0.03,0.0005,0.006)
def thump():
    t,s=sweep(0.4,lambda t:80+200*np.exp(-t/0.02)); return s*np.exp(-t/0.1)+rng.standard_normal(len(t))*np.exp(-t/0.02)*0.3
def chime():
    t=np.arange(int(1.2*sr))/sr; return sum(np.sin(2*np.pi*f*t)*np.exp(-t/0.35)/(k+1) for k,f in enumerate([1318,1760,2637]))*0.5
b=0.5; chords=[[220,277.2,329.6],[196,246.9,293.7],[174.6,220,261.6],[196,246.9,293.7]]; t=np.arange(n)/sr; pad=np.zeros(n)
for k in range(int(T/(4*b))+1):
    ch=chords[k%4]; s0=int(k*4*b*sr); s1=min(n,int((k+1)*4*b*sr)); tt=np.arange(max(0,s1-s0))/sr
    for f in ch: pad[s0:s1]+=np.sin(2*np.pi*f*tt)*0.05+np.sin(2*np.pi*f/2*tt)*0.03
    for j in range(4): add(np.sin(2*np.pi*ch[0]/2*np.arange(int(0.4*sr))/sr)*env(0.4,0.005,0.15)*0.25,k*4*b+j*b)
out+=pad*np.minimum(1,t/2)*np.minimum(1,(T-t)/1.5)
for k in range(int(T/b)):
    if 1.9<k*b<28.6: add(kick(),k*b,0.55); add(hat(),k*b+b/2,0.8)
for x in WHOOSH: add(whoosh(),max(0,x-0.1),0.35)
for x in POPS: add(pop(520),x,0.35); add(chime(),x+0.02,0.25)
for k in range(32): add(tick(),TICK_START+k*0.09,0.25)
for x in THUMPS: add(thump(),x,0.45)
out*=np.minimum(1,(T-t)/1.2); out=out/np.max(np.abs(out))*0.85
w=wave.open('out/audio.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
