"""Guide data for the in-game addon -> assets/addon/gabella-guide.json (the addon turns it into Lua, players see it in the game).
Nothing is typed in here: every value comes from the data the site already shows.
  dungeons  DUNGEONS of index.src.html (content/dungeon_pages.registry): levels, entrance zone and side; Russian names from
            i18n/names.json (the ruRU client); url — the dungeon's own page (guides/dungeons/<slug>/), else the list guides/dungeons/
  dungeons_by_area  {areaId: url} for the addon, which knows the area id of the instance the player is in (Questie's ids, kept in
            data/addon_dungeon_areas.json by tools/questie_areas.py): the dungeon's url; the wings of one instance share the id
  levels    [{from, to, url}] the ranges of the route with the anchor of the hunter leveling guide (#lvl-<from>-<to>)
  route     the «Zone route» of guides/leveling/ (content/guides.py, build_guides.leveling_parts) in Russian as /play/ shows it;
            url — the step of that route on the page (#lvl-<side>-<from>-<to>), url_hunter — the same levels in the hunter leveling guide;
            the zones of a step are the zone names in its text (i18n/names_ids.json type "zone", plus the new Forever zones)
  gear      data/gear30.json, the list the spec pages and the gear planner (assets/gear/planner-<lang>.json) show, per GEAR_SPECS
  talents   the leveling order 10–60 of the class leveling guide as the builds page takes it: checked against the client tree
            (talents.leveling, content/talents/<class>.json), per TALENT_SPECS
No made-up data. A Russian name the client data lacks is null where the record has the English twin (en, zone_en) and the English
name in lists and source lines (as the Russian guide prints it). The sources have no uiMapID (names_ids.json keeps Wowhead zone ids,
another number): null and []. talentID is the game's id of the talent: tid of its tree node (tools/talent_import.py keeps the dump's
talentID, in Forever the C_Traits node id), null for a node without one. verified is true only for what was checked against the
game: gear of the client dump (provenance "client-dump") and talent
levels the class guide checked against the in-game tree (TALENTS_CHECKED); dungeon levels (guide sites, Blizzard published none)
and the route (a beta guideline) are false. version is a hash of the content: the same sources give the same file.
Run: python tools/export_addon.py  (build.py runs it on every build)"""
import hashlib, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import langs  # noqa: E402

OUT = os.path.join(ROOT, 'assets', 'addon', 'gabella-guide.json')
SITE = 'https://gabella.site/wow/'                          # absolute: the addon opens these links from the game (copy-paste or the launcher)
GEAR_SPECS = ('hunter-beast-mastery',)                     # data/gear30.json keys
TALENT_SPECS = (('hunter', 'beast-mastery'),)              # class and spec with a leveling order (talents.LEVEL_SPEC)
# levels of the leveling order the class guide checked against the in-game tree: hunter — the talents tip of guides/leveling-hunter/
# («checked against the in-game tree», 06.11); its levels 31–60 are the source's plan, to be checked (talents.UI lvnote)
TALENTS_CHECKED = {'hunter': 30}
# zones new in Forever: names_ids.json keeps Forever names without a type; the guide texts call these zones
FOREVER_ZONES = ('Zephras Isle', 'Riverglades', 'Shen’Dralas')
BETWEEN = re.compile(r'между\s[^,.;]*')                     # «Riverglades между Redridge и Burning Steppes»: a place on the map
SIDES = ('horde', 'alliance')


def _norm(name):
    return name.replace('’', "'")


def ru_name(en):
    """The ruRU client name of an English game name (i18n/names.json, either apostrophe), None when the client data has none."""
    for k in (en, _norm(en), en.replace("'", '’')):
        ru = (langs.NAMES.get(k) or {}).get('ru')
        if ru:
            return ru if ru != en else None
    return None


def shown(en):
    """A name as the Russian guide prints it: the client's Russian name, the English one when there is none."""
    return ru_name(en) or en


# ---------- dungeons ----------

def key_of(name):
    """ragefire_chasm: the English name in lower case, apostrophes dropped, any other run of non-letters one underscore."""
    return re.sub(r'[^a-z0-9]+', '_', re.sub(r"['’]", '', name.lower())).strip('_')


def side_of(side, both):
    """Who can run it: only the entrance side when the other cannot come (Ragefire Chasm, The Stockade: in a capital), else both."""
    return side if side and not both else 'both'


def dungeon_url(name):
    """The dungeon's own page when it has one (slug with hyphens, the JSON key has underscores), else the list of dungeons."""
    from content import dungeon_pages
    page = dungeon_pages.BY_NAME.get(name)
    return f'{SITE}guides/dungeons/{page["slug"]}/' if page else f'{SITE}guides/dungeons/'


def dungeons_by_area(ds):
    """{"718": url}: Questie's area id of an instance -> the page of its dungeon. Wings of one instance (Scarlet Monastery) have no
    pages of their own: all give the list url; ids sorted as numbers."""
    areas = json.load(open(os.path.join(ROOT, 'data', 'addon_dungeon_areas.json'), encoding='utf-8'))
    urls = {}
    for d in ds:
        if d['en'] in areas:
            urls.setdefault(areas[d['en']], set()).add(d['url'])
    return {str(a): (min(u) if len(u) == 1 else f'{SITE}guides/dungeons/') for a, u in sorted(urls.items())}


def dungeons():
    from content import dungeon_pages
    reg, order = dungeon_pages.registry()
    out = []
    for name in order:
        lo, hi, zone, _new, _other, side, both = reg[name]
        out.append({'key': key_of(name), 'en': name, 'ru': ru_name(name), 'min': lo, 'max': hi, 'zone_en': zone, 'zone_ru': ru_name(zone),
                    'uiMapID': None, 'side': side_of(side, both), 'entrance': side or None, 'url': dungeon_url(name), 'verified': False})
    keys = [d['key'] for d in out]
    assert len(set(keys)) == len(keys), keys
    return out


# ---------- route ----------

_ZONES = []


def zone_rx():
    """Zone names of i18n/names_ids.json (type "zone": cities and instances are zones too) and FOREVER_ZONES, apostrophes as '."""
    if not _ZONES:
        ids = json.load(open(os.path.join(ROOT, 'i18n', 'names_ids.json'), encoding='utf-8'))
        names = {_norm(k): k for k, v in ids.items() if v.get('type') == 'zone'}
        names.update({_norm(k): k for k in FOREVER_ZONES})
        alt = '|'.join(map(re.escape, sorted(names, key=len, reverse=True)))
        _ZONES.extend([re.compile(rf"(?<![A-Za-z'-])({alt})(?![A-Za-z'-])"), names])
    return _ZONES


def zones_of(text):
    """English names (as names_ids.json spells them) of the zones a route step sends you to, in order and once each: zone names
    bare or in [[form|English]] marks. A «между A и B» clause only places a zone on the map; a continent is not a zone."""
    rx, names = zone_rx()
    return list(dict.fromkeys(names[m] for m in rx.findall(BETWEEN.sub('', _norm(text)))))


def route():
    import build, build_guides
    from content.guides import lvl_id
    steps, _tip = build_guides.leveling_parts()
    out = {}
    for side in SIDES:
        out[side] = []
        for lo, hi, d in steps[side]:
            ru = d['ru'] if isinstance(d, dict) else d
            zones = zones_of(ru)
            out[side].append({'from': lo, 'to': hi, 'uiMapIDs': [], 'zones_ru': [shown(z) for z in zones], 'zones_en': zones,
                              'text_ru': build.ru_plain(ru), 'url': f'{SITE}guides/leveling/#{lvl_id(lo, hi, side)}',
                              'url_hunter': f'{SITE}guides/leveling-hunter/#{lvl_id(lo, hi)}', 'verified': False})
    return out


# ---------- gear ----------

def _named(x):
    """A boss, dungeon or quest of data/gear30.json as the Russian guide prints it (its own ru, else names.json, else English)."""
    x = x or {}
    return x.get('ru') or (shown(x['en']) if x.get('en') else None)


def source_of(srcs, keys):
    """The item source the addon shows, from the sources of one data/gear30.json entry (all of one kind): type, the name of the
    source as the Russian guide prints it (null for a world drop: it has none) and the DUNGEONS key of the dungeon, when it is a row."""
    from content import spec_cheats as SC
    kinds = {s['kind'] for s in srcs}
    if len(kinds) != 1:
        raise ValueError(f'one kind of source per item expected: {srcs}')
    kind, out = kinds.pop(), []
    for s in srcs:
        if kind == 'drop' and (s.get('boss') or s.get('dungeon')):
            dg = (s.get('dungeon') or {}).get('en')
            name = ' · '.join(x for x in (_named(s.get('boss')), _named(s.get('dungeon'))) if x)
            out.append(('boss', name, key_of(dg) if dg and key_of(dg) in keys else None))
        elif kind == 'drop' and s.get('world'):
            out.append(('world', None, None))
        elif kind == 'quest':
            out.append(('quest', _named(s.get('quest')), None))
        elif kind == 'craft':
            out.append(('recipe', SC.G_PROF.get(s.get('prof')), None))
        else:   # data/gear30.json has no vendor source yet: a new kind gets its type here, with its real fields
            raise ValueError(f'no addon source type for {s}')
    names = [n for _, n, _ in out if n]
    return {'type': out[0][0], 'ru': ' / '.join(dict.fromkeys(names)) or None, 'dungeon': next((k for _, _, k in out if k), None)}


def refined(iid, srcs, specs, keys):
    """A drop in a whole instance that is no DUNGEONS row («Scarlet Monastery») takes the exact dungeon another entry of the same
    item gives in the same zone id («Scarlet Monastery: Graveyard»), with that entry's boss: one fact of the item, kept per spec."""
    out = []
    for s in srcs:
        dg = s.get('dungeon') or {}
        if s['kind'] == 'drop' and dg.get('en') and key_of(dg['en']) not in keys and dg.get('zone'):
            same = [o for rows in specs.values() for e in rows if e['id'] == iid for o in e.get('src') or []
                    if o['kind'] == 'drop' and (o.get('dungeon') or {}).get('zone') == dg['zone'] and key_of(o['dungeon'].get('en') or '') in keys]
            best = next((o for o in same if o.get('boss')), same[0] if same else None)
            if best:
                s = dict(s, dungeon=best['dungeon'], boss=best.get('boss') or s.get('boss') or {})
        out.append(s)
    return out


def gear(spec, keys):
    """The spec's items in the order of its gear table (content/spec_cheats.gear_rows): slot, required level (null: none, as the
    page's «—»), the side when every source is a quest of one side (as the page's filter), verified for client-dump items."""
    from content import spec_cheats as SC
    data = SC.GEAR30
    out = []
    for e, it in SC.gear_rows(spec, data):
        srcs = refined(e['id'], e.get('src') or [], data.get('specs') or {}, keys)
        quests = [s for s in srcs if s['kind'] == 'quest']
        fac = (quests[0].get('faction') or '') if srcs and len(quests) == len(srcs) and len({s.get('faction') for s in quests}) == 1 else ''
        lv = it.get('lvl') or 0
        out.append({'slot': it['slot'], 'level': lv if lv > 1 else None, 'itemID': int(e['id']), 'ru': SC._name(it['names'], 'ru'),
                    'source': source_of(srcs, keys), 'side': fac or 'both', 'verified': it.get('provenance') == 'client-dump'})
    return out


# ---------- talents ----------

def talent_order(cid, spec):
    """One row per level 10–60: the talent the point goes to and its rank after it. Empty when the guide's order does not fit
    the tree (the builds page then shows no leveling tab either)."""
    import talents
    data = talents.load(cid)
    b = talents.leveling(cid, spec, data)
    if not b:
        return []
    checked = TALENTS_CHECKED.get(cid, 0) if data.get('client') else 0
    out, rank = [], {}
    for t, _add, a, z in b['steps']:
        for lv in range(a, z + 1):
            rank[t['id']] = rank.get(t['id'], 0) + 1
            out.append({'level': lv, 'talentID': t.get('tid'), 'spellID': (t.get('spells') or [None])[0], 'rank': rank[t['id']],
                        'ru': t['n'].get('ru') or t['n']['en'], 'verified': lv <= checked})
    return out


# ---------- the file ----------

def version_of(body):
    return hashlib.sha1(json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()[:12]


def payload():
    ds = dungeons()
    keys = {d['key'] for d in ds}
    rt = route()
    levels = [{'from': x['from'], 'to': x['to'], 'url': x['url_hunter']} for x in rt['alliance']]
    assert levels == [{'from': x['from'], 'to': x['to'], 'url': x['url_hunter']} for x in rt['horde']], 'the sides share the level ranges'
    body = {'dungeons': ds, 'dungeons_by_area': dungeons_by_area(ds), 'levels': levels, 'route': rt, 'gear': {s: gear(s, keys) for s in GEAR_SPECS},
            'talents': {f'{c}-{s}': talent_order(c, s) for c, s in TALENT_SPECS}}
    return {'version': version_of(body), **body}


def main():
    data = payload()
    text = json.dumps(data, ensure_ascii=False, indent=1) + '\n'
    old = open(OUT, encoding='utf-8').read() if os.path.isfile(OUT) else None
    if old != text:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        open(OUT, 'w', encoding='utf-8', newline='\n').write(text)
    n = lambda block: sum(map(len, data[block].values()))   # noqa: E731
    print(f'addon: v={data["version"]}, {len(data["dungeons"])} dungeons, {n("route")} route steps, {n("gear")} items, '
          f'{n("talents")} talent points', file=sys.stderr)


if __name__ == '__main__':
    main()
