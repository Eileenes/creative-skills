import sys, json, asyncio, os
sys.path.insert(0, "onetake/scripts")
from sfx_palette import *
from playwright.async_api import async_playwright
async def get():
    async with async_playwright() as p:
        launch_options = {}
        if os.environ.get("PROMO_CHROMIUM_PATH"):
            launch_options["executable_path"] = os.environ["PROMO_CHROMIUM_PATH"]
        if os.environ.get("PROMO_SOFTWARE_GL") == "1":
            launch_options["args"] = ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"]
        b = await p.chromium.launch(**launch_options)
        pg = await b.new_page(viewport={"width":1280,"height":720}); await pg.goto("file://" + __import__("os").path.abspath("comp.html") + ""); await pg.evaluate("window.__ready")
        ev = await pg.evaluate("window.__events()"); await b.close(); return ev
ev = asyncio.run(get()); json.dump(ev, open("events.json","w"))
s = Score(dur=19.0)
# soft pad bed: two detuned low sines swelling, ducked before the end
import numpy as np
n = int(SR*19); t = np.arange(n)/SR
bed = (np.sin(2*np.pi*110*t)+0.6*np.sin(2*np.pi*164.8*t)+0.4*np.sin(2*np.pi*220.5*t))*0.5
env = np.clip(t/1.5,0,1)*np.clip((18.8-t)/1.2,0,1)*(0.55+0.45*np.sin(2*np.pi*t/8)**2)
s.place(lp(bed*env, 900), t=0, gain=0.05, send=0.6)
notes = [523, 587, 659, 784, 880]
ki = 0
for e in ev:
    k, tt = e["kind"], e["t"]
    if k == "key": s.place(wood(1500 + 180*(ki%4), 0.07), t=tt, gain=0.16, send=0.15); ki += 1
    elif k == "whoosh": s.place(air(0.75, 200, 3200, 1.3, 0.7), t=tt, gain=0.45, send=0.5)
    elif k == "leap": s.place(air(0.4, 400, 2400, 1.5, 0.35), t=tt, gain=0.3, send=0.4)
    elif k == "hop": s.place(air(0.22, 700, 2600, 1.6, 0.3), t=tt, gain=0.12, send=0.3)
    elif k == "tile": s.place(wood(260, 0.14), t=tt, gain=0.5, send=0.3); s.place(glass(notes[ki%5], 0.5, 0.5), t=tt, gain=0.08, send=0.5); ki += 1
    elif k == "land": s.place(wood(200, 0.12), t=tt, gain=0.45, send=0.3); s.place(sub(70, 0.35), t=tt, gain=0.25)
    elif k == "land_small": s.place(wood(320, 0.08), t=tt, gain=0.22, send=0.2)
    elif k == "land_big": s.place(sub(55, 0.7), t=tt, gain=0.55, send=0.4); s.place(wood(160, 0.15), t=tt, gain=0.4)
    elif k == "window": s.place(air(0.5, 300, 1800, 1.2, 0.4), t=tt, gain=0.3, send=0.5); s.place(glass(392, 0.9, 0.6), t=tt+0.1, gain=0.1, send=0.6)
    elif k == "enter": s.place(wood(220, 0.12), t=tt, gain=0.4); s.place(glass(659, 0.8), t=tt+0.04, gain=0.12, send=0.6)
    elif k == "result": s.place(bubble(620, 0.22), t=tt, gain=0.25, send=0.4)
    elif k == "follow": s.place(glass(784, 1.2, 1.0), t=tt, gain=0.22, send=0.6); s.place(glass(1175, 1.0, 0.8), t=tt+0.09, gain=0.16, send=0.6)
    elif k == "tick": s.place(wood(1800, 0.06), t=tt, gain=0.15)
    elif k == "spout": s.place(bubble(480, 0.25), t=tt, gain=0.22, send=0.4); s.place(bubble(720, 0.2), t=tt+0.08, gain=0.15, send=0.4)
    elif k == "title": s.place(glass(523, 1.6, 0.7), t=tt, gain=0.16, send=0.7); s.place(glass(784, 1.6, 0.5), t=tt+0.12, gain=0.12, send=0.7)
s.write("sfx.wav")
print(len(ev), "events")
