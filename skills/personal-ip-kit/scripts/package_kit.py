#!/usr/bin/env python3
"""Validate and package explicitly listed IP assets; never edit raster pixels."""
import argparse
import hashlib
import html
import json
from pathlib import Path, PurePosixPath
import shutil
import tempfile
from urllib.parse import quote
import zipfile

from PIL import Image


def build(source, plan_path, output):
    source, output = Path(source).resolve(), Path(output).absolute()
    archive = output.with_name(output.name + ".zip")
    if output.exists() or archive.exists():
        raise ValueError("Output directory or ZIP already exists; choose a new version.")
    plan = json.loads(Path(plan_path).read_text(encoding="utf-8"))
    if not isinstance(plan.get("name"), str) or not plan["name"].strip():
        raise ValueError("A nonempty name is required.")
    if not isinstance(plan.get("assets"), list) or not plan["assets"]:
        raise ValueError("At least one asset is required.")
    included = {}

    def collect(value):
        if not isinstance(value, str):
            raise ValueError("File paths must be strings.")
        p = PurePosixPath(value)
        if not value or p.is_absolute() or ".." in p.parts or "\\" in value:
            raise ValueError("Use relative paths within source: " + value)
        key = p.as_posix()
        if key in {".", "index.html", "manifest.json"}:
            raise ValueError("Reserved output path: " + key)
        local = (source / key).resolve()
        if not local.is_relative_to(source) or not local.is_file():
            raise ValueError("Missing file or path outside source: " + key)
        included[key] = local
        return key

    rows, ids, paths = [], set(), set()
    for item in plan["assets"]:
        identity = item.get("id")
        if not isinstance(identity, str) or not identity or identity in ids:
            raise ValueError("Asset ids must be unique nonempty strings.")
        ids.add(identity)
        path = collect(item["path"])
        if path in paths:
            raise ValueError("Duplicate asset path: " + path)
        paths.add(path)
        alpha = item.get("alpha")
        if not isinstance(alpha, bool):
            raise ValueError("alpha must be boolean: " + identity)
        refs = item.get("references")
        if not isinstance(refs, list) or not refs:
            raise ValueError("At least one reference is required: " + identity)
        row = dict(id=identity, title=str(item.get("title", identity)), path=path,
                   alpha=alpha, promptFile=collect(item["promptFile"]),
                   references=[collect(ref) for ref in refs])
        with Image.open(included[path]) as im:
            im.load()
            row.update(width=im.width, height=im.height, mode=im.mode)
            channel = im.convert("RGBA").getchannel("A")
            lo, hi = channel.getextrema()
            row["alphaRange"] = [lo, hi]
            row["fullyTransparentFraction"] = round(
                channel.histogram()[0] / (im.width * im.height), 6)
            if alpha and not (lo == 0 and hi > 0):
                raise ValueError("Expected transparent background and visible subject: " + path)
        rows.append(row)
    documents = [collect(value) for value in plan.get("documents", [])]
    esc = html.escape
    link = lambda value: esc(quote(value, safe="/"), quote=True)
    cards = []
    for row in rows:
        cards.append(
            '<article><div class="preview"><img loading="lazy" src="' + link(row["path"]) +
            '" alt="' + esc(row["title"], quote=True) + '"></div><div class="info"><h2>' +
            esc(row["title"]) + '</h2><p>' + str(row["width"]) + ' × ' +
            str(row["height"]) + (' · 透明 PNG' if row["alpha"] else '') +
            '</p><a download href="' + link(row["path"]) + '">下载图片 ↗</a></div></article>')
    doc_links = " · ".join('<a download href="' + link(p) + '">' +
                           esc(Path(p).name) + '</a>' for p in documents)
    page = """<!doctype html><html lang="zh-CN"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__NAME__ · IP 素材库</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#fff7ed;color:#30251f;
font-family:system-ui,-apple-system,sans-serif}main{max-width:1240px;margin:auto;padding:48px 24px}
h1{font-size:clamp(32px,6vw,64px);margin:12px 0}header p{line-height:1.8;color:#63564d}
nav{display:flex;gap:12px;flex-wrap:wrap;margin:24px 0 32px}
button,a{color:inherit}button{cursor:pointer;padding:10px 18px;border:1px solid #b8a899;
border-radius:30px;background:transparent;font:inherit}button[aria-pressed=true]{background:#30251f;color:#fff}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr));gap:24px}
article{border:1px solid #dfd1c1;border-radius:18px;overflow:hidden;background:#fffdf9}
.preview{height:300px;background:#efe4d6;overflow:hidden}
.preview img{display:block;width:100%;height:300px;object-fit:contain}
body[data-bg=dark] .preview{background:#26282d}
body[data-bg=check] .preview{background-color:#fff;background-image:conic-gradient(#ddd 25%,transparent 0 50%,#ddd 0 75%,transparent 0);background-size:24px 24px}
.info{padding:20px}h2{font-size:18px;margin:0}.info p{color:#756b64;font-size:14px}
footer{margin-top:40px;line-height:2}
</style><body data-bg="cream"><main><header><p>CHARACTER ASSET LIBRARY</p>
<h1>__NAME__</h1><p>__COUNT__ 张独立素材 · 点击下载原图 · 可切换背景检查透明边缘</p></header>
<nav aria-label="预览背景"><button data-value="cream" aria-pressed="true">奶油底</button>
<button data-value="dark" aria-pressed="false">深色底</button>
<button data-value="check" aria-pressed="false">棋盘格</button></nav>
<section class="grid">__CARDS__</section><footer>__DOCS__<br>
<a download href="manifest.json">下载文件清单</a></footer></main>
<script>document.querySelectorAll('button[data-value]').forEach(b=>b.onclick=()=>{
document.body.dataset.bg=b.dataset.value;
document.querySelectorAll('button[data-value]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));
});</script></body></html>"""
    # Replace template markers in one pass so user text cannot become another marker.
    import re
    values = {"NAME": esc(plan["name"]), "COUNT": str(len(rows)),
              "CARDS": "".join(cards), "DOCS": doc_links}
    page = re.sub(r"__(NAME|COUNT|CARDS|DOCS)__", lambda m: values[m[1]], page)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".ip-package-", dir=output.parent) as temporary:
        stage = Path(temporary) / "kit"
        stage.mkdir()
        hashes = {}
        for relative, original in sorted(included.items()):
            destination = stage / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(original, destination)
            hashes[relative] = hashlib.sha256(destination.read_bytes()).hexdigest()
        manifest = dict(name=plan["name"], version=str(plan.get("version", "1.0")),
                        assets=rows, documents=documents, sha256=hashes,
                        checks="File decoding, dimensions, alpha and hashes only; visual review is separate.")
        (stage / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        (stage / "index.html").write_text(page, encoding="utf-8")
        staged_zip = Path(temporary) / "kit.zip"
        with zipfile.ZipFile(staged_zip, "w", zipfile.ZIP_DEFLATED) as zf:
            for file in sorted(stage.rglob("*")):
                if file.is_file():
                    zf.write(file, output.name + "/" + file.relative_to(stage).as_posix())
        with zipfile.ZipFile(staged_zip) as zf:
            if zf.testzip() is not None:
                raise ValueError("ZIP verification failed.")
        # Reserve a new destination; never overwrite another run.
        output.mkdir()
        for child in stage.iterdir():
            shutil.move(str(child), str(output / child.name))
        with archive.open("xb") as target, staged_zip.open("rb") as origin:
            shutil.copyfileobj(origin, target)
    return dict(directory=str(output), archive=str(archive), assets=len(rows),
                transparentAssets=sum(row["alpha"] for row in rows), files=len(hashes))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True)
    parser.add_argument("--plan", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(build(args.source, args.plan, args.output), ensure_ascii=False))
    except (ValueError, KeyError, TypeError, OSError) as error:
        parser.exit(1, str(error) + "\n")
