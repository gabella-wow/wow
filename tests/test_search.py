"""Поиск по сайту: индекс есть на каждом языке, записи одинаковые по числу, каждая ведёт на собранную страницу и её якорь,
у каждого языка словарь других названий, вопросы и шесть популярных ссылок на свои записи, на всех страницах кнопка поиска
и скрипты с одной версией ?v=. Качество ответов — tests/test_search_queries.py. Запуск: python tests/test_search.py"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from langs import LANGS  # noqa: E402

import build  # noqa: E402
from content.guides import GUIDES  # noqa: E402

LIMITED = {s['id'] for g in GUIDES for s in g['sections'] if 'langs' in s}   # sections shown in some languages only

problems, sizes = [], {}
for lang in LANGS:
    data = json.load(open(os.path.join(ROOT, 'assets', 'search', f'{lang}.json'), encoding='utf-8'))
    rows, urls = data['i'], {r[2] for r in data['i']}
    if len(data['a']) < 150 or len(data['p']) != 6 or len(data['q']) < 9 or not data['s']:
        problems.append(f'{lang}: словари {len(data["a"])} названий, {len(data["p"])} популярных, {len(data["q"])} вопросов')
    problems += [f'{lang}: ссылка словаря без записи {u}' for u in [u for u, _ in data['q']] + [u for _, u in data['p']] if u not in urls]
    pre = build.page_dir(lang)
    sizes[lang] = sum(not build.only_lang(r[2].partition('#')[0][len(pre):]) and r[2].partition('#')[2] not in LIMITED
                      for r in rows)                             # one-language pages and ru/uk-only sections aside
    kinds = {k: sum(r[3] == k for r in rows) for k in range(4)}
    if kinds[0] < 31 or kinds[2] < 10 or kinds[3] < 35:
        problems.append(f'{lang}: мало записей {kinds}')
    for t, s, u, k, keys, x in rows:
        path, _, anchor = u.partition('#')
        page = os.path.join(ROOT, path, 'index.html')
        if not t.strip() or not os.path.exists(page):
            problems.append(f'{lang}: {t!r} -> {u}')
        elif anchor and f' id="{anchor}"' not in open(page, encoding='utf-8').read():
            problems.append(f'{lang}: нет якоря {u}')
if len(set(sizes.values())) != 1:
    problems.append(f'разное число записей: {sizes}')

pages = [p for p in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True)
         if not p.endswith('.src.html') and not re.search(r'(^|[\\/])(\.|node_modules|mock-)', os.path.relpath(p, ROOT))]
versions = set()
for p in pages:
    parts = os.path.relpath(p, ROOT).replace(os.sep, '/').split('/')
    if p == os.path.join(ROOT, '404.html') or parts[-1] == 'index.html' and len(parts) in (3, 4) and parts[-3] in ('b', 't'):   # the root 404 and the share pages b/<build>/, t/<class>-<spec>/ are light pages without the site chrome
        continue
    html = open(p, encoding='utf-8').read()
    v = re.findall(r'assets/search/search\.(?:js|css)\?v=(\w+)', html)
    if 'class="iconbtn srchbtn"' not in html or len(v) != 2:
        problems.append(f'нет поиска: {os.path.relpath(p, ROOT)}')
    versions |= set(v)
if len(versions) > 1:
    problems.append(f'разные версии поиска: {versions}')

# the examples under the home search field are answers, not the search again: real pages, the mage builds first (clarity audit 02.11, p.2)
for lang in LANGS:
    home = os.path.join(ROOT, build.page_dir(lang), 'index.html')
    hq = re.search(r'<p class="hq">(.*?)</p>', open(home, encoding='utf-8').read(), re.S)
    hrefs = re.findall(r'<a href="([^"]+)"', hq[1]) if hq else []
    if hrefs[:1] != ['guides/builds-mage/'] or len(hrefs) != 3 or 'data-q' in hq[1]:
        problems.append(f'{lang}: примеры поиска на главной {hrefs}')
    for h in hrefs:
        path, _, anchor = h.split('?')[0].partition('#')
        page = os.path.join(os.path.dirname(home), path, 'index.html')
        if not os.path.exists(page) or anchor and f' id="{anchor}"' not in open(page, encoding='utf-8').read():
            problems.append(f'{lang}: пример поиска ведёт в никуда {h}')

assert not problems, '\n'.join(problems[:20])
print('OK', len(LANGS), 'languages,', sizes['ru'], 'entries,', len(pages), 'pages')
