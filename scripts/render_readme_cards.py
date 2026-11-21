"""Original, dependency-free SVG artwork for the GitHub profile."""
from collections import defaultdict
from datetime import date, timedelta
from html import escape
import base64
import json
import os
from pathlib import Path
import re

from fetch_github_activity import ROOT, validate_days, write_changed

THEMES = {
    'light': {'bg': '#eef0f3', 'ink': '#17283e', 'muted': '#4c6077',
              'line': '#d8e0ea', 'blue': '#175cd3', 'teal': '#087c80',
              'purple': '#6941c6', 'levels': ['#e1e7ef', '#9abcf2', '#5e92e0', '#2868c6', '#144392']},
    'dark': {'bg': '#111c2c', 'ink': '#edf3fc', 'muted': '#adbed3',
             'line': '#304158', 'blue': '#8bb9ff', 'teal': '#6ad3cb',
             'purple': '#c4b1ff', 'levels': ['#26354a', '#32598c', '#437ac2', '#77a9ec', '#b1d0ff']},
}


def monthly_totals(days):
    totals = defaultdict(int)
    for day in days:
        totals[day['date'][:7]] += day['count']
    return dict(sorted(totals.items()))


def text(x, y, value, size=18, fill='ink', weight=400, extra=''):
    return (f'<text x="{x}" y="{y}" class="{fill}" font-size="{size}" '
            f'font-weight="{weight}" {extra}>{escape(str(value))}</text>')


def portrait_uri():
    """Use the locally prepared portrait, or the image embedded in the committed hero."""
    prepared = ROOT / '.preview' / 'portrait-readme.png'
    if prepared.exists():
        return 'data:image/png;base64,' + base64.b64encode(prepared.read_bytes()).decode('ascii')
    existing = ROOT / 'cards' / 'hero.svg'
    if existing.exists():
        match = re.search(r'href="(data:image/png;base64,[A-Za-z0-9+/=]+)"',
                          existing.read_text(encoding='utf-8'))
        if match:
            return match.group(1)
    raise ValueError('No prepared portrait or generated hero available')


def svg(height, title, body, theme, static):
    colors = THEMES[theme]
    styles = ''.join(f'.{key}{{fill:{colors[key]}}}' for key in ('ink', 'muted', 'blue', 'teal', 'purple'))
    motion = '' if static else '''
    @keyframes appear {from {opacity:.45;transform:translateY(3px)} to {opacity:1;transform:none}}
    .enter {animation:appear .65s ease-out both}.later {animation-delay:.12s}
    @media(prefers-reduced-motion:reduce){.enter{animation:none!important;opacity:1!important;transform:none!important}}
    '''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="{height}" viewBox="0 0 640 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(title)}. Detailed text and source links accompany this image in the README.</desc>
<style>text{{font-family:Arial,Helvetica,sans-serif}}{styles}{motion}</style>
<rect x=".5" y=".5" width="639" height="{height-1}" rx="14" fill="{colors['bg']}" stroke="{colors['line']}"/>
{body}
</svg>
'''


def hero(theme, image_uri):
    c = THEMES[theme]
    body = text(30, 38, 'RESEARCH  /  ENGINEERING  /  DATA', 14, 'muted', 700)
    body += '<g class="enter">'
    body += text(28, 94, 'Henrique Rezer', 43, weight=700)
    body += text(28, 141, 'Mosquér', 43, weight=700)
    body += text(30, 184, 'Medical AI research.', 25, 'blue')
    body += text(30, 217, 'Applied AI engineering.', 25)
    body += '</g>'
    body += f'<image x="355" y="24" width="260" height="260" href="{image_uri}"/>'
    body += f'<path d="M30 305H610" stroke="{c["line"]}"/>'
    body += text(30, 333, 'PhD student · Computer Science · UFSC', 17, 'muted')
    return body


def pillar(index, label, heading, subtitle, color, theme):
    c = THEMES[theme]
    return (f'<path d="M1 24V92" stroke="{c[color]}" stroke-width="3"/>'
            + text(26, 33, f'0{index} / {label}', 15, color, 700)
            + '<g class="enter">' + text(26, 68, heading, 28, weight=700)
            + text(26, 96, subtitle, 17, 'muted') + '</g>'
            + text(590, 63, '↗', 30, color))


def activity(data, theme):
    c = THEMES[theme]
    if not data:
        return text(28, 42, 'ACTIVITY / AWAITING VERIFIED DATA', 16, 'muted', 700) + text(28, 100, 'No counts estimated.', 28) + text(28, 139, 'Run the collector to create a real snapshot.', 18, 'muted')
    days = data['days']
    totals = monthly_totals(days)
    body = text(28, 35, 'GITHUB / MONTHLY ACTIVITY', 15, 'muted', 700)
    body += text(28, 78, f'{sum(d["count"] for d in days):,}', 37, weight=700)
    body += text(200, 76, 'visible contributions', 20, 'muted')
    peak = max(max(totals.values()), 1)
    step = 580 / len(totals)
    for i, (month, value) in enumerate(totals.items()):
        x = 30 + i * step
        h = 105 * value / peak
        body += f'<rect class="enter" x="{x:.2f}" y="{217-h:.2f}" width="{step-10:.2f}" height="{max(h, 1):.2f}" rx="3" fill="{c["blue"]}"><title>{month}: {value}</title></rect>'
        body += text(round(x + (step-10)/2, 2), 236, month[5:], 12, 'muted', extra='text-anchor="middle"')
        body += text(round(x + (step-10)/2, 2), round(210-h, 2), value, 12, 'muted', extra='text-anchor="middle"')
    body += text(28, 266, f'{days[0]["date"]} — {days[-1]["date"]} · boundary months may be partial', 13, 'muted')
    body += text(28, 289, f'Observed {data["observed_on"]} UTC · today may be incomplete', 13, 'muted')
    return body


def contributions(data, theme):
    c = THEMES[theme]
    body = text(28, 36, 'GITHUB / DAILY ACTIVITY', 15, 'muted', 700)
    if not data:
        return body + text(28, 89, 'Calendar unavailable — no synthetic data.', 22)
    days = data['days']
    first = date.fromisoformat(days[0]['date'])
    offset = (first.weekday() + 1) % 7
    for i, day in enumerate(days):
        pos = i + offset
        count = day['count']
        level = 0 if count == 0 else 1 if count < 4 else 2 if count < 8 else 3 if count < 16 else 4
        x, y = 29 + (pos // 7) * 11, 59 + (pos % 7) * 13
        body += f'<rect x="{x}" y="{y}" width="8" height="10" rx="2" fill="{c["levels"][level]}"><title>{day["date"]}: {count} contributions</title></rect>'
    body += text(28, 173, f'{days[0]["date"]} — {days[-1]["date"]}', 14, 'muted')
    for i, label in enumerate(['0', '1–3', '4–7', '8–15', '16+']):
        x = 310 + i * 58
        body += f'<rect x="{x}" y="161" width="9" height="11" rx="2" fill="{c["levels"][i]}"/>'
        body += text(x+13, 171, label, 11, 'muted')
    return body


def render(output, data, static=False):
    if data:
        if data['username'] != 'Henriquerezer' or data['schema_version'] != 1:
            raise ValueError('Unexpected snapshot identity or schema')
        date.fromisoformat(data['observed_on'])
        validate_days(data['days'])
    image_uri = portrait_uri()
    for theme in THEMES:
        cards = {
            'hero': (350, 'Henrique Rezer Mosquér — Medical AI research and applied AI engineering', hero(theme, image_uri)),
            'research': (116, 'Research — Medical AI and computer vision', pillar(1, 'RESEARCH', 'Medical AI & computer vision', 'Models, experiments and evidence.', 'blue', theme)),
            'engineering': (116, 'Engineering — LLMs, RAG and AI systems', pillar(2, 'ENGINEERING', 'LLMs, RAG & AI systems', 'Connecting models to applications.', 'teal', theme)),
            'data': (116, 'Data — Machine learning and analytics', pillar(3, 'DATA', 'Machine learning & analytics', 'From data preparation to interpretation.', 'purple', theme)),
            'activity': (310, 'Monthly GitHub activity', activity(data, theme)),
            'contributions': (195, 'Daily GitHub contributions', contributions(data, theme)),
        }
        for name, (height, title, body) in cards.items():
            suffix = '-dark' if theme == 'dark' else ''
            write_changed(output / f'{name}{suffix}.svg', svg(height, title, body, theme, static))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / 'cards')
    args = parser.parse_args()
    snapshot = ROOT / 'data' / 'contributions.json'
    data = json.loads(snapshot.read_text(encoding='utf-8')) if snapshot.exists() else None
    render(args.output, data, static=os.getenv('STATIC') == '1')
    print('Rendered 12 SVGs' + (' (static)' if os.getenv('STATIC') == '1' else ''))
