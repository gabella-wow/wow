"""Visit counters of the site (Worker report.gabella.site, path /c): day -> visits, visits with a saved character, share.
Reads KV RL through wrangler (you must be logged in: npx wrangler login). Run: python tools/read_counts.py [days=30]
Ratio for the 01.12 decision: char / visit >= 10%."""
import datetime, json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
NS = 'c19034f496a84055ba62d5dfde863575'   # KV RL, tools/report_error/wrangler.toml


def wrangler(*a):
    npx = shutil.which('npx') or shutil.which('npx.cmd')
    r = subprocess.run([npx, 'wrangler', *a], cwd=os.path.join(HERE, 'report_error'), capture_output=True, text=True, encoding='utf-8')
    if r.returncode:
        sys.exit(f'wrangler {a[0]} {a[1]}: {r.stderr.strip()[-400:]}')
    return r.stdout


def table(rows):
    """rows: {day: {'visit': n, 'char': n}} -> text lines."""
    out = [f'{"day":<12}{"visit":>8}{"char":>8}{"%":>8}']
    tv = tc = 0
    for day in sorted(rows):
        v, c = rows[day].get('visit', 0), rows[day].get('char', 0)
        tv, tc = tv + v, tc + c
        out.append(f'{day:<12}{v:>8}{c:>8}{(100 * c / v if v else 0):>7.1f}%')
    out.append(f'{"total":<12}{tv:>8}{tc:>8}{(100 * tc / tv if tv else 0):>7.1f}%')
    return out


def main():
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    since = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)).strftime('%Y-%m-%d')
    keys = json.loads(wrangler('kv', 'key', 'list', '--namespace-id', NS, '--prefix', 'cnt:', '--remote'))
    rows = {}
    for k in keys:
        _, day, kind = k['name'].split(':')
        if day >= since:
            rows.setdefault(day, {})[kind] = int(wrangler('kv', 'key', 'get', k['name'], '--namespace-id', NS, '--remote').strip() or 0)
    print('\n'.join(table(rows)))


if __name__ == '__main__':
    main()
