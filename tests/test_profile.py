from pathlib import Path
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))


class ProfileTests(unittest.TestCase):
    def test_calendar_year_windows_join_without_inventing_days(self):
        from datetime import date
        from fetch_github_activity import select_window
        years = [[{'date': '2025-12-31', 'count': 4}],
                 [{'date': '2026-01-01', 'count': 2}, {'date': '2026-01-02', 'count': 1}]]
        days = select_window(years, date(2025, 12, 31), date(2026, 1, 1))
        self.assertEqual([d['count'] for d in days], [4, 2])
        with self.assertRaises(ValueError):
            select_window(years[:1], date(2025, 12, 31), date(2026, 1, 1))

    def test_real_counts_and_invalid_calendar(self):
        from fetch_github_activity import parse_calendar
        html = '''<td class="ContributionCalendar-day" id="a" data-date="2026-01-31"></td>
        <td class="ContributionCalendar-day" id="b" data-date="2026-02-01"></td>
        <tool-tip for="a">1,234 contributions on January 31.</tool-tip>
        <tool-tip for="b">No contributions on February 1.</tool-tip>'''
        self.assertEqual(parse_calendar(html), [
            {'date': '2026-01-31', 'count': 1234}, {'date': '2026-02-01', 'count': 0}])
        for bad in [html.replace('No contributions', 'Unknown'),
                    html.replace('2026-02-01', '2026-02-02'),
                    html.replace('2026-02-01', '2026-01-31'), '']:
            with self.assertRaises(ValueError):
                parse_calendar(bad)

    def test_failure_preserves_cache(self):
        from fetch_github_activity import refresh
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'snapshot.json'
            p.write_text('previous snapshot', encoding='utf-8')
            def unavailable():
                raise OSError('offline')
            with self.assertRaises(OSError):
                refresh(p, unavailable)
            self.assertEqual(p.read_text(), 'previous snapshot')

    def test_same_data_does_not_rewrite(self):
        from fetch_github_activity import refresh
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'snapshot.json'
            data = {'days': [{'date': '2026-01-01', 'count': 2}]}
            refresh(p, lambda: data)
            stamp = p.stat().st_mtime_ns
            refresh(p, lambda: data)
            self.assertEqual(stamp, p.stat().st_mtime_ns)

    def test_monthly_totals(self):
        from render_readme_cards import monthly_totals
        self.assertEqual(monthly_totals([
            {'date': '2026-01-31', 'count': 5}, {'date': '2026-02-01', 'count': 2},
            {'date': '2026-02-02', 'count': 3}]), {'2026-01': 5, '2026-02': 5})

    def test_static_valid_deterministic_svg(self):
        from render_readme_cards import render
        with tempfile.TemporaryDirectory() as d:
            render(Path(d), None, static=True)
            files = list(Path(d).glob('*.svg'))
            self.assertEqual(len(files), 12)
            before = {p.name: p.read_bytes() for p in files}
            for p in files:
                self.assertIn('viewBox', ET.parse(p).getroot().attrib)
                self.assertNotIn('@keyframes', p.read_text(encoding='utf-8'))
                self.assertNotIn('<script', p.read_text(encoding='utf-8'))
            render(Path(d), None, static=True)
            self.assertEqual(before, {p.name: p.read_bytes() for p in files})

    def test_hero_embeds_portrait_and_uses_gray_surface(self):
        from render_readme_cards import render
        with tempfile.TemporaryDirectory() as d:
            render(Path(d), None, static=True)
            hero = (Path(d) / 'hero.svg').read_text(encoding='utf-8')
            self.assertIn('data:image/png;base64,', hero)
            self.assertIn('#eef0f3', hero)


if __name__ == '__main__':
    unittest.main()
