"""Fetch only the publicly visible GitHub contribution calendar; no token required."""
from datetime import date, datetime, timedelta, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
USERNAME = 'Henriquerezer'


class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells = []
        self.tooltips = {}
        self.current = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'ContributionCalendar-day' in attrs.get('class', '').split():
            if attrs.get('data-date'):
                self.cells.append((attrs.get('id'), attrs['data-date']))
        if tag == 'tool-tip':
            self.current = attrs.get('for')
            self.tooltips[self.current] = ''

    def handle_data(self, data):
        if self.current is not None:
            self.tooltips[self.current] += data

    def handle_endtag(self, tag):
        if tag == 'tool-tip':
            self.current = None


def validate_days(days):
    if not days:
        raise ValueError('No calendar days found')
    previous = None
    for day in days:
        current = date.fromisoformat(day['date'])
        if type(day['count']) is not int or day['count'] < 0:
            raise ValueError('Invalid contribution count')
        if previous and current != previous + timedelta(days=1):
            raise ValueError('Duplicate or missing calendar date')
        previous = current


def parse_calendar(html):
    parser = CalendarParser()
    parser.feed(html)
    days = []
    for identifier, day in parser.cells:
        label = parser.tooltips.get(identifier, '').strip()
        match = re.match(r'^(No|\d{1,3}(?:,\d{3})+|\d+) contributions?\b', label, re.I)
        if not match:
            raise ValueError('Calendar tooltip missing or unrecognized')
        count = 0 if match[1].lower() == 'no' else int(match[1].replace(',', ''))
        days.append({'date': day, 'count': count})
    days.sort(key=lambda d: d['date'])
    validate_days(days)
    return days


def fetch_year(year):
    url = f'https://github.com/users/{USERNAME}/contributions?from={year}-01-01&to={year}-12-31'
    request = Request(url, headers={'User-Agent': 'Henriquerezer-profile/1.0',
                                    'Accept-Language': 'en-US'})
    for attempt in range(3):
        try:
            with urlopen(request, timeout=25) as response:
                html = response.read(4_000_001)
            if len(html) > 4_000_000:
                raise ValueError('Unexpected calendar response size')
            break
        except HTTPError as exc:
            if attempt == 2 or exc.code not in (429, 500, 502, 503, 504):
                raise
            retry = exc.headers.get('Retry-After', '')
            # Do not hammer the endpoint when a long cooldown is requested.
            if retry and (not retry.isdigit() or int(retry) > 15):
                raise
            time.sleep(int(retry) if retry else 2 ** (attempt + 1))
        except (URLError, TimeoutError):
            if attempt == 2:
                raise
            time.sleep(2 ** (attempt + 1))
    return parse_calendar(html.decode('utf-8'))


def select_window(calendars, start, end):
    days = sorted([d for calendar in calendars for d in calendar
                   if str(start) <= d['date'] <= str(end)], key=lambda d: d['date'])
    validate_days(days)
    if len(days) != (end - start).days + 1 or days[0]['date'] != str(start) or days[-1]['date'] != str(end):
        raise ValueError('Incomplete requested calendar window')
    return days


def fetch():
    end = datetime.now(timezone.utc).date()
    start = end - timedelta(days=364)
    days = select_window([fetch_year(year) for year in range(start.year, end.year+1)], start, end)
    return {'schema_version': 1, 'username': USERNAME,
            'source': f'https://github.com/users/{USERNAME}/contributions',
            'observed_on': str(end), 'scope': 'publicly visible calendar',
            'days': days}


def write_changed(path, text):
    payload = text.encode('utf-8')
    if path.exists() and path.read_bytes() == payload:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_bytes(payload)
    temporary.replace(path)
    return True


def refresh(path, loader=fetch):
    data = loader()  # Complete validation/fetch before touching the last good file.
    return write_changed(path, json.dumps(data, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    try:
        changed = refresh(ROOT / 'data' / 'contributions.json')
        print('Activity snapshot updated' if changed else 'Activity snapshot unchanged')
    except (OSError, ValueError, KeyError) as exc:
        print(f'Activity fetch failed ({type(exc).__name__}); previous snapshot preserved.', file=sys.stderr)
        sys.exit(1)
