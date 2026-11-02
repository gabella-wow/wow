"""«Нашёл ошибку»: the button and the dialog on the key data pages of all 9 languages, not on other pages; the Worker test
(tests/test_report_worker.mjs) in node. Run after python build.py: python tests/test_report_error.py"""
import os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from build import LANGS, page_dir  # noqa: E402
import report  # noqa: E402

KEY = ['classes/mage/', 'guides/builds/', 'guides/builds-warrior/', 'guides/spec-mage-fire/', 'guides/tier-list/',
       'guides/dungeons/', 'guides/dungeons/the-deadmines/', 'play/', 'talents/', 'talents/priest/']
NOT = ['', 'guides/faq/', 'races/orc/', 'tools/', 'privacy/']

results = []


def check(name, ok, why=''):
    results.append(f'{"ПРОЙДЕНО" if ok else "УПАЛО"} {name}' + ('' if ok else f': {why}'))


def page(lang, path):
    return open(os.path.join(ROOT, page_dir(lang, path), 'index.html'), encoding='utf-8').read()


check('9 languages in the texts', sorted(report.TX) == sorted(LANGS), sorted(report.TX))
check('every text filled, no Cyrillic outside ru/uk',
      all(all(x.strip() for x in t) and (l in ('ru', 'uk') or not re.search('[А-Яа-яЁёІіЇїЄє]', ''.join(t))) for l, t in report.TX.items()))
for path in KEY:
    bad = []
    for lang in LANGS:
        h = page(lang, path)
        btn = re.search(r'<p class="rep"><button class="rep-b" type="button" aria-haspopup="dialog" aria-controls="repDlg" data-v="\d{4}-\d\d-\d\d">([^<]+)</button></p>\s*<p class="dcta">', h)
        dlg = re.search(r'<dialog class="repd" id="repDlg" aria-labelledby="repT" data-l="(\w+)" data-u="https://report\.gabella\.site/"', h)
        main_end = h.find('</main>')
        if not btn or btn[1] != report.TX[lang][0]:
            bad.append(f'{lang}: button')
        elif not (0 < btn.start() < main_end):
            bad.append(f'{lang}: button outside <main>')
        if not dlg or dlg[1] != lang or h.count('id="repDlg"') != 1:
            bad.append(f'{lang}: dialog')
        elif dlg.start() < main_end:
            bad.append(f'{lang}: dialog inside <main>')
        if '.rep-b{' not in h or "getElementById('repDlg')" not in h or '<label for="repX">' not in h:
            bad.append(f'{lang}: styles/script/label')
    check(f'button + dialog on {path} x9', not bad, bad[:4])
for path in NOT:
    with_btn = [l for l in LANGS if 'rep-b' in page(l, path)]
    check(f'no button on {path or "home"}', not with_btn, with_btn)
check('wants(): the data pages only', all(map(report.wants, KEY)) and not any(map(report.wants, NOT + ['b/orc-warrior-arms/', 't/mage-fire/'])))
check('inject() twice changes nothing', report.inject(page('en', 'play/'), 'play/', 'en', '2026-11-01') == page('en', 'play/'))

node = shutil.which('node')
if not node:
    check('worker test', False, 'node not found')
else:
    r = subprocess.run([node, os.path.join(HERE, 'test_report_worker.mjs')], capture_output=True, text=True, encoding='utf-8')
    tail = (r.stdout + r.stderr).strip().splitlines()
    check('worker test (test_report_worker.mjs)', r.returncode == 0, '\n'.join(tail[-12:]))

print('\n'.join(results))
failed = [x for x in results if x.startswith('УПАЛО')]
print(f'УПАЛО report_error: {len(failed)} of {len(results)}' if failed else f'ПРОЙДЕНО report_error: {len(results)} checks')
sys.exit(1 if failed else 0)
