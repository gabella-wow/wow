"""X2: site against the game. Compares the addon dumps of 05.11 with what the site shows. Reads only, writes nothing, no network.

    python tools/x2_verify.py --talents "<WoW>/_forever_/WTF/Account/<acc>/SavedVariables/GabellaTalents.lua" \
                              --gear "<WoW>/_forever_/WTF/Account/<acc>/SavedVariables/GabellaGear.lua" [--gear-specs a-b,c-d]
    python tools/x2_verify.py --selftest

Prints ПРОЙДЕНО / УПАЛО line by line; exit code 1 if anything failed, 0 if all passed.

Assumptions (the dump format comes from tools/talent_dump and tools/gear_dump, read with tools/talent_import.parse_lua):
 * GabellaTalentsDB[CLASS][locale] = {build, trees = [{info = {tabName, tabIconFileId, ...}, talents = [{name, icon (file id), row, col,
   maxRank, req = {row, col}}]}]}. The spec icon of the game is the tab icon info[2].
 * GabellaGearDB.items[id] = {name{locale}, slot (INVTYPE_*), req, q, ...} (the format gear_import.from_addon reads).
 * Talents are matched with the site tree (content/talents/<class>.json) by position (row, column), not by id.
 * "Spec icons": build.SPEC_ICON must have an entry for each of the 27 specs and the file must exist in the repo.
 * "Talents 31-60": talents.leveling() is run on the tree made from the DUMP; the order must be legal and cover levels 10-60,
   with 30 points on levels 31-60. mage and warlock are known to return None (see tests/test_talents.py): reported as УПАЛО.
 * "95 icons": the site has 95 of 464 talents without icon (26.10); after the import there must be 0 without icon on the site
   and 0 without an icon file id in the dump.
 * "Gear of 5 specs": by default every spec of data/gear30.json; --gear-specs narrows it to the five that matter.
   For each item of the site table: the id is in the dump, same slot, same required level, same quality.
A check whose dump is not given prints УПАЛО (нет дампа): nothing is guessed."""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'tools'))

OK, BAD = 'ПРОЙДЕНО', 'УПАЛО'


def _list(t):
    """A Lua table with int keys is read as a list or a dict: always give (key, value) pairs."""
    if isinstance(t, dict):
        return list(t.items())
    return [(i, v) for i, v in enumerate(t or [], 1) if v is not None]


def load_lua(path, root):
    from talent_import import parse_lua, from_traits
    db = parse_lua(open(path, encoding='utf-8').read()).get(root)
    if root == 'GabellaTalentsDB' and db:              # Forever dumps (C_Traits): positions -> rows and columns
        db = {c: {loc: (from_traits(d) if isinstance(d, dict) and d.get('api') == 'traits' and not d.get('grid') else d) for loc, d in by.items()}
              for c, by in db.items()}
    return db


def site_talents(cid):
    p = os.path.join(HERE, 'content', 'talents', f'{cid}.json')
    return json.load(open(p, encoding='utf-8')) if os.path.isfile(p) else None


def _base(by_locale):
    return by_locale.get('enUS') or by_locale.get('enGB') or next(iter(by_locale.values()))


# ---------- the checks: each returns a list of (ok, line) ----------

def check_spec_icons(talents_db, spec_icon, trees):
    out = []
    for cid, keys in trees.items():
        dump = (talents_db or {}).get(cid.upper())
        base = _base(dump) if dump else None
        for i, key in enumerate(keys):
            spec = f'{cid}-{key}'
            path = spec_icon.get(spec)
            problems = []
            if not path:
                problems.append('нет в build.SPEC_ICON')
            elif not os.path.isfile(os.path.join(HERE, path.replace('@@ROOT@@', '').lstrip('/'))):
                problems.append(f'файла нет: {path}')
            if base is None:
                problems.append('нет дампа класса')
            else:
                tr = _list(base.get('trees'))
                info = _list(tr[i][1].get('info')) if i < len(tr) else []
                if len(info) < 2 or not info[1][1]:
                    problems.append('в дампе нет значка вкладки')
            out.append((not problems, f'иконка спека {spec}: ' + ('есть, файл на месте, значок в дампе' if not problems else '; '.join(problems))))
    return out


def check_talents(talents_db, trees):
    out = []
    for cid, keys in trees.items():
        dump = (talents_db or {}).get(cid.upper())
        site = site_talents(cid)
        if not dump:
            out.append((False, f'таланты {cid}: нет дампа'))
            continue
        if not site:
            out.append((False, f'таланты {cid}: нет content/talents/{cid}.json'))
            continue
        base = _base(dump)
        dtrees = [v for _, v in _list(base.get('trees'))]
        diffs = []
        if len(dtrees) != len(site['trees']):
            diffs.append(f'деревьев {len(dtrees)} в дампе против {len(site["trees"])} на сайте')
        n = 0
        for dt, st in zip(dtrees, site['trees']):
            dpos = {(int(t['row']), int(t['col'])): t for _, t in _list(dt.get('talents'))}
            spos = {(t['r'], t['c']): t for t in st['talents']}
            n += len(dpos)
            for pos in sorted(set(dpos) | set(spos)):
                d, s = dpos.get(pos), spos.get(pos)
                if d is None or s is None:
                    diffs.append(f'{st["key"]} {pos}: {"нет в игре" if d is None else "нет на сайте"}')
                    continue
                if int(d['maxRank']) != s['m']:
                    diffs.append(f'{st["key"]} {pos} {s["n"].get("en")}: рангов {d["maxRank"]} в игре, {s["m"]} на сайте')
                en = s['n'].get('en')
                if en and d.get('name') and 'enUS' in dump and d['name'] != en:
                    diffs.append(f'{st["key"]} {pos}: название «{d["name"]}» в игре, «{en}» на сайте')
                dreq = tuple(int(x) for x in d['req']) if d.get('req') else None
                sreq = None
                if s.get('req'):
                    r = next((x for x in st['talents'] if x['id'] == s['req']), None)
                    sreq = (r['r'], r['c']) if r else None
                if dreq != sreq:
                    diffs.append(f'{st["key"]} {pos}: требование {dreq} в игре, {sreq} на сайте')
                if s.get('file') is not None and d.get('icon') and int(d['icon']) != int(s['file']):
                    diffs.append(f'{st["key"]} {pos}: файл значка {d["icon"]} в игре, {s["file"]} на сайте')
        out.append((not diffs, f'таланты {cid}: {n} узлов, ' + ('совпадают с игрой' if not diffs else f'расхождений {len(diffs)}, первые: ' + ' | '.join(diffs[:3]))))
    return out


def check_icons95(talents_db, trees):
    out = []
    total = bare = 0
    for cid in trees:
        site = site_talents(cid)
        if site:
            for tr in site['trees']:
                for t in tr['talents']:
                    total += 1
                    bare += t.get('icon') is None
    out.append((total > 0 and bare == 0, f'иконки талантов на сайте: без иконки {bare} из {total} (нужно 0)'))
    dn = dbare = 0
    for cid in trees:
        dump = (talents_db or {}).get(cid.upper())
        if dump:
            for _, tr in _list(_base(dump).get('trees')):
                for _, t in _list(tr.get('talents')):
                    dn += 1
                    dbare += not t.get('icon')
    out.append((dn > 0 and dbare == 0, f'значки в дампе: без файла {dbare} из {dn}' if dn else 'значки в дампе: нет дампа'))
    return out


def check_order(talents_db, trees):
    out = []
    try:
        import build_guides  # noqa: F401  (tests/test_talents.py does the same: attaches the guides' tree blocks)
    except Exception:
        pass
    import talents
    import talent_import
    for cid, spec in talents.LEVEL_SPEC.items():
        by = (talents_db or {}).get(cid.upper())
        if not by:
            out.append((False, f'порядок 31–60 {cid}-{spec}: нет дампа'))
            continue
        try:
            data = talent_import.convert(cid, by, site_talents(cid))   # English names by spell from the site (the dump may be ru only)
            b = talents.leveling(cid, spec, data)
        except Exception as e:                                     # a dump of a different shape must not hide the other checks
            out.append((False, f'порядок 31–60 {cid}-{spec}: ошибка разбора {type(e).__name__}: {e}'))
            continue
        if b is None:
            out.append((False, f'порядок 31–60 {cid}-{spec}: порядок гайда не ложится в дерево из игры (leveling = None)'))
            continue
        late = sum(add for _, add, a, bb in b['steps'] if a >= 31)
        ok = b['steps'][0][2] == 10 and b['steps'][-1][3] == 60 and late == 30
        out.append((ok, f'порядок 31–60 {cid}-{spec}: шаги {b["steps"][0][2]}–{b["steps"][-1][3]}, очков на 31–60: {late} (нужно 30)'))
    return out


def check_gear(gear_db, site_gear, only=None):
    from gear_import import INV, INVTYPE
    if not gear_db:
        return [(False, 'снаряжение: нет дампа')]
    items = {int(k): v for k, v in _list(gear_db.get('items'))}
    out = []
    for spec, rows in sorted((site_gear or {}).get('specs', {}).items()):
        if only and spec not in only:
            continue
        diffs = []
        for r in rows:
            sid = str(r['id'])
            s = site_gear['items'].get(sid) or {}
            d = items.get(int(r['id']))
            if d is None:
                diffs.append(f'{sid}: нет в дампе')
                continue
            if INV.get(INVTYPE.get(d.get('slot'))) != s.get('slot'):
                diffs.append(f'{sid}: ячейка {d.get("slot")} в игре, {s.get("slot")} на сайте')
            if s.get('lvl') is not None and (d.get('req') or 0) != s['lvl']:
                diffs.append(f'{sid}: уровень {d.get("req")} в игре, {s["lvl"]} на сайте')
            if s.get('q') is not None and d.get('q') != s['q']:
                diffs.append(f'{sid}: качество {d.get("q")} в игре, {s["q"]} на сайте')
        out.append((bool(rows) and not diffs, f'снаряжение {spec}: {len(rows)} предметов, ' + ('совпадают' if rows and not diffs else 'нет предметов' if not rows else f'расхождений {len(diffs)}, первые: ' + ' | '.join(diffs[:3]))))
    if not out:
        out.append((False, 'снаряжение: на сайте нет спеков для сверки'))
    return out


def run(talents_db, gear_db, spec_icon, site_gear, only=None):
    import talents
    trees = talents.TREES
    res = []
    res += check_spec_icons(talents_db, spec_icon, trees)
    res += check_talents(talents_db, trees)
    res += check_order(talents_db, trees)
    res += check_icons95(talents_db, trees)
    res += check_gear(gear_db, site_gear, only)
    return res


def report(res):
    for ok, line in res:
        print(f'{OK if ok else BAD}  {line}')
    bad = sum(not ok for ok, _ in res)
    print(f'Итого: {len(res) - bad} {OK}, {bad} {BAD}')
    return bad


# ---------- selftest ----------

def _synthetic(site):
    """A dump that says exactly what the site says (built from content/talents): the talent checks must pass on it."""
    import talents
    db = {}
    for cid, keys in talents.TREES.items():
        d = site_talents(cid)
        trees = []
        for i, tr in enumerate(d['trees']):
            byid = {t['id']: t for t in tr['talents']}
            tl = []
            for t in tr['talents']:
                x = {'name': t['n'].get('en', ''), 'icon': 100000 + len(tl), 'row': t['r'], 'col': t['c'], 'maxRank': t['m'], 'tip': []}
                if t.get('req'):
                    r = byid[t['req']]
                    x['req'] = [r['r'], r['c']]
                tl.append(x)
            trees.append({'info': [keys[i], 200000 + i], 'talents': tl})
        db[cid.upper()] = {'enUS': {'class': cid.upper(), 'locale': 'enUS', 'build': 'selftest', 'trees': trees}}
    return db


def selftest():
    import talents
    failures = []

    def expect(name, cond):
        print(f'{OK if cond else BAD}  selftest: {name}')
        if not cond:
            failures.append(name)

    # 1) empty dump: nothing passes, nothing crashes
    res = run({}, {}, {}, {'specs': {}, 'items': {}})
    expect('пустой дамп: все проверки УПАЛО', bool(res) and not any(ok for ok, _ in res))
    # 2) a dump equal to the site: names, ranks, requirements, cells match
    syn = _synthetic(None)
    res = check_talents(syn, talents.TREES)
    expect('дамп = сайт: таланты 9 классов ПРОЙДЕНО', len(res) == 9 and all(ok for ok, _ in res))
    res = check_icons95(syn, talents.TREES)
    expect('дамп с файлами значков: в дампе без файла 0', res[1][0])
    # 3) one changed rank must be caught
    syn['MAGE']['enUS']['trees'][0]['talents'][0]['maxRank'] += 1
    res = check_talents(syn, talents.TREES)
    expect('изменённый ранг пойман (mage УПАЛО)', [ok for ok, l in res if l.startswith('таланты mage')] == [False])
    # 4) fixture dump of the paladin (test data of the repo): parses and compares without exceptions
    fx = load_lua(os.path.join(HERE, 'tests', 'fixtures', 'talents', 'GabellaTalents.lua'), 'GabellaTalentsDB')
    res = check_talents(fx, {'paladin': talents.TREES['paladin']})
    expect('фикстура паладина читается (вердикт: ' + (OK if res[0][0] else BAD) + ', тестовые данные отличаются от сайта)', len(res) == 1)
    # 5) fixture gear dump against the fixture gear table
    gd = load_lua(os.path.join(HERE, 'tests', 'fixtures', 'gear_dump.lua'), 'GabellaGearDB')
    fixture_site = json.load(open(os.path.join(HERE, 'tests', 'fixtures', 'gear30.json'), encoding='utf-8'))
    res = check_gear(gd, fixture_site)
    print('  (фикстура снаряжения, сырые строки)'); [print('   ', l) for _, l in res]
    expect('фикстура снаряжения читается', len(res) >= 1)
    # 6) the gear check catches a missing item
    site = {'specs': {'x-y': [{'id': 900101}, {'id': 999}]}, 'items': {'900101': {'slot': 'head', 'lvl': 20, 'q': 2}, '999': {'slot': 'head', 'lvl': 1, 'q': 1}}}
    res = check_gear(gd, site)
    expect('отсутствующий предмет пойман', res[0][0] is False and '999: нет в дампе' in res[0][1])
    print(f'selftest: {"ПРОЙДЕНО" if not failures else "УПАЛО: " + ", ".join(failures)}')
    return 1 if failures else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--talents', help='GabellaTalents.lua (SavedVariables)')
    ap.add_argument('--gear', help='GabellaGear.lua (SavedVariables)')
    ap.add_argument('--gear-specs', help='comma list <class>-<spec>; default all specs of data/gear30.json')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    import build
    tdb = load_lua(a.talents, 'GabellaTalentsDB') if a.talents else None
    gdb = load_lua(a.gear, 'GabellaGearDB') if a.gear else None
    site_gear = json.load(open(os.path.join(HERE, 'data', 'gear30.json'), encoding='utf-8'))
    only = set(a.gear_specs.split(',')) if a.gear_specs else None
    return 1 if report(run(tdb, gdb, build.SPEC_ICON, site_gear, only)) else 0


if __name__ == '__main__':
    sys.exit(main())
