"""Create a local GitHub-width approximation without external packages."""
from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
readme = (ROOT / 'README.md').read_text(encoding='utf-8')
readme = re.sub(r'<a href="#[^"]+"><picture>.*?</picture></a>', '', readme, flags=re.S)
readme = re.sub(r'<picture>.*?</picture>', '', readme, flags=re.S)
readme = re.sub(r'<details>.*?</details>', '', readme, flags=re.S)
lines = []
table = []
for line in readme.splitlines():
    if line.startswith('|') and re.match(r'^\|\s*:?-{3}', line):
        continue
    if line.startswith('|'):
        cells = [x.strip() for x in line.strip('|').split('|')]
        cells = [re.sub(r'\[([^]]+)\]\(([^)]+)\)', lambda m: f'<a href="{escape(m[2])}">{escape(m[1])}</a>', cell) for cell in cells]
        cells = [re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', cell) for cell in cells]
        table.append('<tr>' + ''.join(f'<td>{cell}</td>' for cell in cells) + '</tr>')
        continue
    if table:
        lines.append('<table>' + ''.join(table) + '</table>')
        table = []
    if line.startswith('# '):
        lines.append(f'<h1>{escape(line[2:])}</h1>')
    elif line.startswith('## '):
        lines.append(f'<h2>{escape(line[3:])}</h2>')
    elif line.strip():
        line = re.sub(r'\[([^]]+)\]\(([^)]+)\)', lambda m: f'<a href="{escape(m[2])}">{escape(m[1])}</a>', line)
        line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
        line = re.sub(r'\*(.*?)\*', r'<em>\1</em>', line)
        lines.append(f'<p>{line}</p>')
if table:
    lines.append('<table>' + ''.join(table) + '</table>')
html = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{background:#f6f8fa;color:#1f2328;font:16px/1.55 system-ui;margin:0}main{box-sizing:border-box;max-width:896px;margin:24px auto;background:white;border:1px solid #d0d7de;border-radius:6px;padding:32px}img{display:block;width:100%;margin:12px 0}a{color:#0969da}p{margin:14px 0}h1{margin:20px 0}h2{margin:32px 0 12px}table{width:100%;border-collapse:collapse;margin:16px 0}td{border:1px solid #d0d7de;padding:8px;vertical-align:top}tr:nth-child(even){background:#f6f8fa}@media(max-width:640px){main{margin:0;padding:16px;border:0}table{display:block;overflow-x:auto}body{min-width:0}}</style><main>
<img src="static/hero.svg" alt="Profile hero">'''
for line in lines:
    if line.startswith('<h2>Selected projects'):
        html += ''.join(f'<img src="static/{name}.svg" alt="{name} card">' for name in ('research','engineering','data'))
    if line.startswith('<h2>GitHub activity'):
        html += '<img src="static/activity.svg" alt="Monthly activity"><img src="static/contributions.svg" alt="Contributions">'
    html += line
html += '</main></html>'
out = ROOT / '.preview' / 'index.html'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(html, encoding='utf-8')
print(out)
