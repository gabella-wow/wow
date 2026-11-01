"""tools/news_latency.py on a fixture: a temporary git repo with two commits of data/official.json, issues and Pages builds.
No network. Run: python tests/test_news_latency.py"""
import json, os, subprocess, sys, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tools'))
import news_latency as nl  # noqa: E402


def run(d, *args, when=None):
    env = dict(os.environ, GIT_AUTHOR_NAME='t', GIT_AUTHOR_EMAIL='t@t', GIT_COMMITTER_NAME='t', GIT_COMMITTER_EMAIL='t@t')
    if when:
        env['GIT_COMMITTER_DATE'] = env['GIT_AUTHOR_DATE'] = when
    subprocess.run(['git', '-C', d, *args], check=True, capture_output=True, env=env)


with tempfile.TemporaryDirectory() as d:
    run(d, 'init', '-q')
    os.makedirs(os.path.join(d, 'data'))
    p = os.path.join(d, 'data', 'official.json')
    old = {'id': 'art-1', 'sha': 'aaaaaaaa11', 'at': '2026-10-30T17:01:00Z'}            # backlog: published a day later
    new = {'id': 'us-2', 'sha': 'bbbbbbbb22', 'at': '2026-11-01T10:00:00Z'}             # fresh post
    json.dump([old], open(p, 'w'))
    run(d, 'add', '.'); run(d, 'commit', '-qm', 'one', when='2026-10-31T17:30:59Z')
    json.dump([new, old], open(p, 'w'))
    run(d, 'add', '.'); run(d, 'commit', '-qm', 'two', when='2026-11-01T10:09:00Z')
    head = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()

    issues = [{'title': '[us-2@bbbbbbbb] Some post', 'created_at': '2026-11-01T10:04:00Z'},
              {'title': '[us-2@bbbbbbbb] duplicate later', 'created_at': '2026-11-01T10:30:00Z'},
              {'title': '[art-1@aaaaaaaa] Old', 'created_at': '2026-10-30T17:11:00Z'},
              {'title': 'not ours', 'created_at': '2026-11-01T10:00:00Z'}]
    builds = [{'commit': head, 'status': 'built', 'created_at': '2026-11-01T10:09:20Z', 'updated_at': '2026-11-01T10:10:30Z'},
              {'commit': 'zzz', 'status': 'errored', 'created_at': '2026-11-01T10:09:10Z', 'updated_at': '2026-11-01T10:09:15Z'}]

    c = nl.first_commits(d)
    assert set(c) == {('art-1', 'aaaaaaaa11'), ('us-2', 'bbbbbbbb22')}, c
    assert c[('us-2', 'bbbbbbbb22')][0] == nl.parse('2026-11-01T10:09:00Z')
    assert c[('art-1', 'aaaaaaaa11')][0] == nl.parse('2026-10-31T17:30:59Z')       # not re-dated by the second commit
    t = nl.task_times(issues)
    assert t['us-2'] == nl.parse('2026-11-01T10:04:00Z') and len(t) == 2   # earliest wins, foreign title skipped

    rows = nl.build_rows([old, new], c, t, builds)
    assert [r['id'] for r in rows] == ['us-2', 'art-1']                               # newest post first
    r = rows[0]
    assert (r['to_task'], r['to_commit'], r['commit_to_page'], r['to_page'], r['note']) == (4.0, 9.0, 1.5, 10.5, '')
    assert rows[1]['note'] == 'late' and rows[1]['page'] is None                  # no build in the fixture
    assert nl.page_time('nope', nl.parse('2026-11-01T10:09:00Z'), builds) == nl.parse('2026-11-01T10:10:30Z')   # first build after the commit
    assert nl.page_time('nope', nl.parse('2026-11-01T11:00:00Z'), builds) is None
    out = nl.render(rows)
    assert 'us-2' in out and '10.5' in out and 'ok' in out and 'late' in out and 'target post>page <= 15' in out, out

    # end to end, offline
    ip, bp = os.path.join(d, 'i.json'), os.path.join(d, 'b.json')
    json.dump(issues, open(ip, 'w')); json.dump(builds, open(bp, 'w'))
    assert nl.main(['--root', d, '--issues', ip, '--builds', bp]) == 0
print('ok news_latency')
