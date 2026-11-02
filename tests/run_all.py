"""Все проверки одной командой (после python build.py): python tests/run_all.py [--live]"""
import glob, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
env = dict(os.environ, PYTHONUTF8='1')
runs = [[f] for f in sorted(glob.glob(os.path.join(HERE, 'test_*.py')))] + [[os.path.join(HERE, 'check_vhash.py')], [os.path.join(HERE, 'check_site.py')] + sys.argv[1:]]
failed = []
# Overflow check in headless Chrome (key pages x 9 languages x 2 widths); the full run: node tests/overflow_check.mjs --full
runs.append(['--node', os.path.join(HERE, 'overflow_check.mjs'), '--quick'])
# Narrow phones (audit X6): /play/ (no hero and a saved hero) and /classes/ x 9 languages x 320/360/375 x both themes —
# no sideways scroll, class cards one height, chips inside their column, «More» aria-expanded, search named without Ctrl K
runs.append(['--node', os.path.join(HERE, 'narrow_check.mjs')])
# Alignment check: the content of every button / chip / tab / badge in the middle of its frame, in pixels (full: --full)
runs.append(['--node', os.path.join(HERE, 'align_check.mjs'), '--quick'])
for args in runs:
    if args[0] == '--node':
        if not shutil.which('node'):
            print(f'FAIL {os.path.basename(args[1])}: node not found'); failed.append(args[1]); continue
        r = subprocess.run(['node'] + args[1:], env=env, capture_output=True, text=True, encoding='utf-8')
        args = args[1:]
    else:
        r = subprocess.run([sys.executable] + args, env=env, capture_output=True, text=True, encoding='utf-8')
    out = (r.stdout + r.stderr).strip().splitlines()
    print(f'{"OK  " if r.returncode == 0 else "FAIL"} {os.path.basename(args[0])}: {out[-1] if out else ""}')
    if r.returncode:
        failed.append(args[0])
        print('\n'.join(out[-15:]))
sys.exit(1 if failed else 0)
