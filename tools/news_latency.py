"""Latency of the news chain: post of Blizzard -> task (issue of news-auto) -> commit in main -> built page.

Reads only: data/official.json and `git log` of the repository, plus (optionally) the issues and the Pages builds of
gabella-wow/wow from api.github.com. No other network, nothing is written, no workflow is started.
Times are UTC, minutes. Target: post -> page <= 15 min.

    python tools/news_latency.py                         # repo = this one, GitHub API for issues and builds
    python tools/news_latency.py --issues i.json --builds b.json   # offline (fixtures); no network at all
    python tools/news_latency.py --no-net                # post -> commit only
Token for the API (optional, 60 requests/hour without it): env GITHUB_TOKEN or GH_TOKEN.

A note published long after its post (backlog of the first live run) shows its real delay; the column `note` marks
it `late` when the commit came more than 60 min after the post; such rows are left out of the summary line."""
import argparse, json, os, re, subprocess, sys, urllib.request
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = 'gabella-wow/wow'
TARGET_MIN = 15
LATE_MIN = 60


def parse(ts):
    """ISO time with Z or an offset -> aware datetime (UTC)."""
    ts = ts.strip().replace('Z', '+00:00')
    d = datetime.fromisoformat(ts)
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def minutes(a, b):
    """b - a in minutes (1 decimal) or None."""
    return None if a is None or b is None else round((b - a).total_seconds() / 60, 1)


def git(root, *args):
    r = subprocess.run(['git', '-C', root, *args], capture_output=True, encoding='utf-8', errors='replace')
    if r.returncode:
        raise RuntimeError('git %s: %s' % (' '.join(args), r.stderr.strip()))
    return r.stdout


def entries_at(root, rev, path):
    """{id: sha} of data/official.json at a revision ({} if the file is absent there)."""
    try:
        data = json.loads(git(root, 'show', '%s:%s' % (rev, path)))
    except (RuntimeError, ValueError):
        return {}
    return {e['id']: e.get('sha') for e in data if isinstance(e, dict) and 'id' in e}


def first_commits(root, path='data/official.json', rev='HEAD'):
    """{(id, sha): committer time} of the commit in which the pair first appears in the file (oldest first walk)."""
    out = git(root, 'log', '--reverse', '--format=%H %cI', rev, '--', path).split('\n')
    seen, res, prev = set(), {}, {}
    for line in out:
        if not line.strip():
            continue
        h, ts = line.split(' ', 1)
        cur = entries_at(root, h, path)
        for i, s in cur.items():
            if (i, s) not in seen and prev.get(i) != s:
                seen.add((i, s))
                res[(i, s)] = (parse(ts), h)
        prev = cur
    return res


TITLE = re.compile(r'^\[(?P<id>[^@\]]+)@(?P<sha>[0-9a-f]+)\]')


def task_times(issues):
    """{id: earliest created_at} from issues of news-auto (title `[id@sha8] ...`). By id, not by sha: an edited post gets a new sha
    and a new issue `Правка: ...`, the first issue of the id is the moment we noticed the post."""
    res = {}
    for it in issues:
        m = TITLE.match(it.get('title', ''))
        if not m:
            continue
        k, t = m['id'], parse(it['created_at'] if 'created_at' in it else it['createdAt'])
        if k not in res or t < res[k]:
            res[k] = t
    return res


def page_time(commit_sha, commit_time, builds):
    """Finish time of the first successful Pages build that carries the commit: that very commit or, if the list has no such sha, the first one started within 30 min after it."""
    ok = [b for b in builds if b.get('status') == 'built']
    for b in ok:
        if b.get('commit') == commit_sha:
            return parse(b['updated_at'])
    later = sorted((parse(b['updated_at']), parse(b['created_at'])) for b in ok
                   if 0 <= minutes(commit_time, parse(b['created_at'])) <= 30)     # no exact match (old build list): a build within 30 min
    return later[0][0] if later else None


def build_rows(official, commits, tasks, builds):
    rows = []
    for e in official:
        key = (e['id'], str(e.get('sha', ''))[:8])
        full = next((v for (i, s), v in commits.items() if i == e['id'] and s and s[:8] == key[1]), None)
        post = parse(e['at'])
        task = tasks.get(e['id'])
        ctime, chash = full if full else (None, None)
        page = page_time(chash, ctime, builds) if ctime and builds is not None else None
        rows.append({'id': e['id'], 'post': post, 'task': task, 'commit': ctime, 'page': page,
                     'to_task': minutes(post, task), 'to_commit': minutes(post, ctime), 'to_page': minutes(post, page),
                     'commit_to_page': minutes(ctime, page),
                     'note': 'late' if (minutes(post, ctime) or 0) > LATE_MIN else ''})
    rows.sort(key=lambda r: r['post'], reverse=True)
    return rows


def fmt_t(t):
    return t.strftime('%d.%m %H:%M') if t else '-'


def fmt_m(m):
    return '-' if m is None else ('%.1f' % m)


def render(rows):
    head = ['id', 'post UTC', 'task UTC', 'commit UTC', 'page UTC', 'post>task', 'post>commit', 'commit>page', 'post>page', 'note']
    lines = [head]
    for r in rows:
        lines.append([r['id'], fmt_t(r['post']), fmt_t(r['task']), fmt_t(r['commit']), fmt_t(r['page']),
                      fmt_m(r['to_task']), fmt_m(r['to_commit']), fmt_m(r['commit_to_page']), fmt_m(r['to_page']),
                      r['note'] + ('' if r['to_page'] is None or r['note'] else (' ok' if r['to_page'] <= TARGET_MIN else ' >%d' % TARGET_MIN))])
    w = [max(len(str(l[i])) for l in lines) for i in range(len(head))]
    out = ['  '.join(str(c).ljust(w[i]) for i, c in enumerate(l)) for l in lines]
    fresh = [r['to_page'] for r in rows if r['to_page'] is not None and not r['note']]
    out.append('')
    out.append('fresh posts with a page time: %d%s; target post>page <= %d min'
               % (len(fresh), (', max %.1f, median %.1f' % (max(fresh), sorted(fresh)[len(fresh) // 2])) if fresh else '', TARGET_MIN))
    return '\n'.join(out)


def api(path):
    h = {'Accept': 'application/vnd.github+json', 'User-Agent': 'gabella-news-latency'}
    tok = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
    if tok:
        h['Authorization'] = 'Bearer ' + tok
    with urllib.request.urlopen(urllib.request.Request('https://api.github.com/repos/%s/%s' % (REPO, path), headers=h), timeout=30) as r:
        return json.loads(r.read())


def load(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--root', default=ROOT, help='repository (default: this one)')
    ap.add_argument('--official', default=None, help='official.json (default: <root>/data/official.json)')
    ap.add_argument('--issues', help='issues JSON (GitHub API format), offline')
    ap.add_argument('--builds', help='Pages builds JSON (GitHub API format), offline')
    ap.add_argument('--no-net', action='store_true', help='no GitHub API: only post > commit')
    a = ap.parse_args(argv)
    official = load(a.official or os.path.join(a.root, 'data', 'official.json'))
    commits = first_commits(a.root)
    issues, builds = None, None
    if a.issues:
        issues = load(a.issues)
    if a.builds:
        builds = load(a.builds)
    if not a.no_net:
        if issues is None:
            issues = []
            for page in range(1, 6):                      # up to 500 issues, newest first
                chunk = api('issues?labels=news-auto&state=all&per_page=100&page=%d' % page)
                issues += chunk
                if len(chunk) < 100:
                    break
        if builds is None:
            builds = api('pages/builds?per_page=100')
    rows = build_rows(official, commits, task_times(issues or []), builds)
    print(render(rows))
    return 0


if __name__ == '__main__':
    sys.exit(main())
