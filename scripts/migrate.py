#!/usr/bin/env python3
"""Re-apply the Universal Audiobooks rebrand after each upstream sync (idempotent)."""
from pathlib import Path
import os, base64, io, glob
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent

def main():
    REPL = [
        ('github.com/advplyr/audiobookshelf','github.com/yashhasan570/UniversalAudiobooks'),
        ('advplyr/audiobookshelf','yashhasan570/UniversalAudiobooks'),
        ('Audiobookshelf','Universal Audiobooks'),
    ]
    TEXT_EXTS = {'.js','.vue','.ts','.json','.yaml','.yml','.md','.html','.sh','.txt','.xml'}
    SKIP = {'.git','node_modules','scripts'}
    changed = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP]
        for fn in filenames:
            p = Path(dirpath)/fn
            if p.suffix.lower() not in TEXT_EXTS: continue
            try: s = p.read_text(encoding='utf-8')
            except Exception: continue
            o = s
            for a,b in REPL: s = s.replace(a,b)
            if s != o:
                p.write_text(s, encoding='utf-8'); changed += 1
    badge = ROOT/'scripts/icons/badge.png'
    n = 0
    if badge.exists():
        img = Image.open(badge).convert('RGBA')
        for t in glob.glob(str(ROOT/'client/static/*.png')) + glob.glob(str(ROOT/'client/static/*.ico')):
            p = Path(t)
            if p.name == 'favicon.ico':
                img.save(p, format='ICO', sizes=[(48,48),(32,32),(16,16)])
            else:
                ref = Image.open(p); w,h = ref.size
                canvas = Image.new('RGBA',(w,h),(0,0,0,0))
                inner = img.resize((w,h), Image.LANCZOS)
                canvas.paste(inner,(0,0),inner)
                canvas.save(p)
            n += 1
        buf = io.BytesIO()
        img.resize((512,512), Image.LANCZOS).save(buf, format='PNG')
        b64 = base64.b64encode(buf.getvalue()).decode()
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">'
               '<image width="512" height="512" href="data:image/png;base64,' + b64 + '"/></svg>')
        (ROOT/'client/static/icon.svg').write_text(svg)
        (ROOT/'images/banner.svg').write_text(svg)
        n += 2
    print(f'migrate: {changed} files swept, {n} icon files updated')

if __name__ == '__main__':
    main()
