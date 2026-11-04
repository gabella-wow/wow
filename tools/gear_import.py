"""Gear up to level 30 for the spec cheat sheets -> data/gear30.json (content/spec_cheats.py reads it, the build has no network).

Two inputs, one schema. Nothing here goes to the network.

  1) Saved guide pages, until the client data (05.11):
       python tools/gear_import.py --pages <folder>
     One page per spec, saved by hand from the browser («HTML only»): <class>-<spec>.html (druid-balance.html,
     hunter-beast-mastery.html, ...). The same page of another site language may sit next to it as <class>-<spec>.<lang>.html
     (ru, de, fr, es, pt, it): the item names of that language are taken from it. Only facts are kept: item id, name, slot,
     required level, quality, stats, and where it comes from (boss and dungeon, quest and faction, profession). No text,
     no pictures. Items marked provenance "wowhead-forever-guide".
  2) The dump of the GabellaGear addon (tools/gear_dump), from 05.11:
       python tools/gear_import.py --addon "<WoW>/_forever_/WTF/Account/<account>/SavedVariables/GabellaGear.lua"
     The client gives the items (name in every dumped language, slot, levels, quality, stats); the sources are what the
     addon saw while playing (loot of a dungeon boss, quest rewards, recipes of the open profession window). The picks for
     each spec are made here by the spec's stat priority (content/spec_cheats.STATS). Items marked provenance "client-dump".
     Dump v2 (GabellaGear 2, 04.11) also keeps consumables, reagents and trade goods (no slot: left out of the specs here,
     read with addon_items()) and names the class and subclass iclass / isub (cls / sub of v1 are still read).

  --date YYYY-MM-DD   the day of the data (default today);  --fixture   test data (tests/fixtures): tests refuse it in data/.

Schema (data/gear30.json):
  {"schema": 1, "date": "2026-10-30", "fixture": false,
   "items": {"<id>": {"slot": "head|neck|shoulder|back|chest|wrist|hands|waist|legs|feet|finger|trinket|main|two|off|ranged",
                      "lvl": <required level 1-30 or null>, "il": <item level or null>, "q": <quality 0-5>,
                      "names": {"en": ..., "ru": ...}, "stats": {"int": 2, "spi": 2, ...}, "provenance": "..."}},
   "specs": {"<class>-<spec>": [{"id": <id>, "src": [{"kind": "drop", "boss": {names}, "dungeon": {names}},
                                                     {"kind": "quest", "quest": {names}, "faction": "alliance|horde|null"},
                                                     {"kind": "craft", "prof": "tailoring"}]}]}}
  Stat keys: str agi sta int spi armor sp (spell damage) hp (healing) mp5 hit crit def ap dps (percent stats as numbers)."""
import argparse, datetime, html as H, json, os, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, 'data', 'gear30.json')
LANGS = ('en', 'ru', 'de', 'fr', 'es', 'pt', 'it')
MAX_LVL = 30
SLOTS = ('head', 'neck', 'shoulder', 'back', 'chest', 'wrist', 'hands', 'waist', 'legs', 'feet', 'finger', 'trinket',
         'main', 'two', 'off', 'ranged')
# inventory type number (the game's, as in the item data of the pages) -> our slot; shirt, tabard, bags, ammo and relics are left out
INV = {1: 'head', 2: 'neck', 3: 'shoulder', 16: 'back', 5: 'chest', 20: 'chest', 9: 'wrist', 10: 'hands', 6: 'waist', 7: 'legs',
       8: 'feet', 11: 'finger', 12: 'trinket', 13: 'main', 21: 'main', 17: 'two', 14: 'off', 22: 'off', 23: 'off',
       15: 'ranged', 25: 'ranged', 26: 'ranged'}
INVTYPE = {'INVTYPE_HEAD': 1, 'INVTYPE_NECK': 2, 'INVTYPE_SHOULDER': 3, 'INVTYPE_CLOAK': 16, 'INVTYPE_CHEST': 5, 'INVTYPE_ROBE': 20,
           'INVTYPE_WRIST': 9, 'INVTYPE_HAND': 10, 'INVTYPE_WAIST': 6, 'INVTYPE_LEGS': 7, 'INVTYPE_FEET': 8, 'INVTYPE_FINGER': 11,
           'INVTYPE_TRINKET': 12, 'INVTYPE_WEAPON': 13, 'INVTYPE_WEAPONMAINHAND': 21, 'INVTYPE_2HWEAPON': 17, 'INVTYPE_SHIELD': 14,
           'INVTYPE_WEAPONOFFHAND': 22, 'INVTYPE_HOLDABLE': 23, 'INVTYPE_RANGED': 15, 'INVTYPE_THROWN': 25, 'INVTYPE_RANGEDRIGHT': 26}
# stat fields of the page item data -> our keys
WH_STATS = {'str': 'str', 'agi': 'agi', 'sta': 'sta', 'int': 'int', 'spi': 'spi', 'armor': 'armor', 'spldmg': 'sp', 'splpwr': 'sp',
            'splheal': 'hp', 'manargn': 'mp5', 'mlehitpct': 'hit', 'rgdhitpct': 'hit', 'splhitpct': 'hit', 'hitpct': 'hit',
            'mlecritstrkpct': 'crit', 'rgdcritstrkpct': 'crit', 'splcritstrkpct': 'crit', 'critstrkpct': 'crit', 'def': 'def',
            'defrtng': 'def', 'mleatkpwr': 'ap', 'atkpwr': 'ap', 'dps': 'dps', 'mledps': 'dps', 'rgddps': 'dps'}
# GetItemStats keys of the client -> our keys
CL_STATS = {'ITEM_MOD_STRENGTH_SHORT': 'str', 'ITEM_MOD_AGILITY_SHORT': 'agi', 'ITEM_MOD_STAMINA_SHORT': 'sta',
            'ITEM_MOD_INTELLECT_SHORT': 'int', 'ITEM_MOD_SPIRIT_SHORT': 'spi', 'RESISTANCE0_NAME': 'armor',
            'ITEM_MOD_SPELL_POWER_SHORT': 'sp', 'ITEM_MOD_SPELL_DAMAGE_DONE_SHORT': 'sp', 'ITEM_MOD_SPELL_HEALING_DONE_SHORT': 'hp',
            'ITEM_MOD_MANA_REGENERATION_SHORT': 'mp5', 'ITEM_MOD_POWER_REGEN0_SHORT': 'mp5', 'ITEM_MOD_HIT_RATING_SHORT': 'hit',
            'ITEM_MOD_HIT_SPELL_RATING_SHORT': 'hit', 'ITEM_MOD_CRIT_RATING_SHORT': 'crit', 'ITEM_MOD_CRIT_SPELL_RATING_SHORT': 'crit',
            'ITEM_MOD_DEFENSE_SKILL_RATING_SHORT': 'def', 'ITEM_MOD_ATTACK_POWER_SHORT': 'ap', 'ITEM_MOD_DAMAGE_PER_SECOND_SHORT': 'dps'}
# «Equip:» lines of the English tooltip the client stat table may miss (Classic-style items)
TIP_STATS = [(r'damage and healing done by magical spells and effects by up to (\d+)', ('sp', 'hp')),
             (r'healing done by spells and effects by up to (\d+)', ('hp',)),
             (r'chance to hit (?:with spells )?by (\d+)%', ('hit',)), (r'critical strike (?:with spells )?by (\d+)%', ('crit',)),
             (r'Restores (\d+) mana per 5 sec', ('mp5',)), (r'\+(\d+) Attack Power', ('ap',)), (r'Increased Defense \+(\d+)', ('def',))]
PROFS = {'blacksmithing': 164, 'leatherworking': 165, 'tailoring': 197, 'engineering': 202, 'enchanting': 333, 'alchemy': 171,
         'firstaid': 129, 'cooking': 185}
PROF_WORDS = {'blacksmithing': 'blacksmith', 'leatherworking': 'leatherwork', 'tailoring': 'tailor', 'engineering': 'engineer',
              'enchanting': 'enchant', 'alchemy': 'alchem', 'firstaid': 'first aid', 'cooking': 'cooking'}
SKILL_ID = {v: k for k, v in PROFS.items()}
LOC = {'enUS': 'en', 'enGB': 'en', 'ruRU': 'ru', 'deDE': 'de', 'frFR': 'fr', 'esES': 'es', 'esMX': 'es', 'ptBR': 'pt', 'itIT': 'it'}
NAME_KEY = {'en': 'name_enus', 'ru': 'name_ruru', 'de': 'name_dede', 'fr': 'name_frfr', 'es': 'name_eses', 'pt': 'name_ptbr', 'it': 'name_itit'}


# ---------- saved guide pages ----------

def gatherer(src):
    """Every WH.Gatherer.addData(type, env, {...}) of a page: {type: {id: data}} (1 npc, 3 item, 5 quest, 7 zone)."""
    out, dec = {}, json.JSONDecoder()
    for m in re.finditer(r'(?:WH\.)?Gatherer\.addData\(\s*(\d+)\s*,\s*\d+\s*,\s*', src):
        try:
            obj, _ = dec.raw_decode(src, m.end())
        except ValueError:
            continue
        if isinstance(obj, dict):
            out.setdefault(int(m.group(1)), {}).update({int(k): v for k, v in obj.items() if str(k).isdigit()})
    return out


def markup(src):
    """The guide body as tag markup: the string a page hands to WH.markup.printHtml, or else the rendered HTML turned into the same tags."""
    dec = json.JSONDecoder()
    for m in re.finditer(r'markup\.printHtml\(\s*', src):
        try:
            s, _ = dec.raw_decode(src, m.end())
        except ValueError:
            continue
        if isinstance(s, str) and len(s) > 200:
            return s
    body = src
    i = body.find('guide-body')
    if i >= 0:
        body = body[i:]
    body = re.sub(r'(?is)<(script|style)\b.*?</\1>', ' ', body)
    names = {}

    def link(m):
        kind, num, text = m.group(1), m.group(2), re.sub(r'<[^>]+>', '', m.group(3)).strip()
        if text:
            names[(kind, int(num))] = H.unescape(text)
        return f'[{kind}={num}]'
    body = re.sub(r'(?is)<a\b[^>]*href="[^"]*?/(item|npc|quest|zone|skill)=(\d+)[^"]*"[^>]*>(.*?)</a>', link, body)
    body = re.sub(r'(?i)<(/?)(h[1-4]|tr|td|th|table)\b[^>]*>', lambda m: f'[{m.group(1)}{m.group(2).lower().replace("th", "td")}]', body)
    body = re.sub(r'<[^>]+>', ' ', body)
    return H.unescape(body), names


def _txt(s):
    return re.sub(r'\s+', ' ', re.sub(r'\[/?[a-z0-9]+(?:[= ][^\]]*)?\]', ' ', s)).strip()


KIND_WORDS = (('drop', ('dungeon drop', 'dungeon loot', 'drops')), ('quest', ('quest reward', 'quest')), ('craft', ('crafted', 'craft', 'profession')))


def page_rows(src):
    """(kind, heading text, faction, row tags, row plain cells) for every table row with an item, in page order."""
    got = markup(src)
    text, anchor = (got, {}) if isinstance(got, str) else got
    kind, sub, rows = None, '', []
    for part in re.split(r'(\[h[1-4][^\]]*\].*?\[/h[1-4]\]|\[tr\].*?\[/tr\])', text, flags=re.S | re.I):
        if re.match(r'\[h[1-4]', part, re.I):
            level = int(part[2])
            title = _txt(part)
            low = title.lower()
            k = next((k for k, words in KIND_WORDS if any(w in low for w in words)), None)
            if level <= 2:                                         # a new part of the guide: one of the three tables or the end of them
                kind, sub = (k if k else 'stop' if kind else None), ''
            elif kind not in (None, 'stop'):
                sub = part
            continue
        if not part.lower().startswith('[tr]') or kind in (None, 'stop') or '[item=' not in part:
            continue
        cells = re.findall(r'\[td[^\]]*\](.*?)\[/td\]', part, flags=re.S | re.I) or [part]
        rows.append((kind, sub, cells))
    return rows, anchor


def faction_of(*texts):
    low = ' '.join(texts).lower()
    a, h = 'alliance' in low, 'horde' in low
    return 'alliance' if a and not h else 'horde' if h and not a else None


def prof_of(*texts):
    low = ' '.join(texts).lower()
    m = re.search(r'\[skill=(\d+)\]', low)
    if m and int(m.group(1)) in SKILL_ID:
        return SKILL_ID[int(m.group(1))]
    return next((p for p, w in PROF_WORDS.items() if w in low), None)


def names_of(kind, num, by_lang, anchor):
    """{lang: name} of an npc/quest/zone/item from the gatherer data of every saved language, then the link text."""
    t = {'npc': 1, 'item': 3, 'quest': 5, 'zone': 7}[kind]
    out = {}
    for lang, (g, _) in by_lang.items():
        d = g.get(t, {}).get(num) or {}
        n = d.get(NAME_KEY[lang]) or d.get('name_enus' if lang == 'en' else '') or (d.get('name') if lang == 'en' else None)
        if n:
            out[lang] = n
    if 'en' not in out and anchor.get((kind, num)):
        out['en'] = anchor[(kind, num)]
    return out


def item_of(num, by_lang, provenance):
    g = by_lang['en'][0] if 'en' in by_lang else next(iter(by_lang.values()))[0]
    d = g.get(3, {}).get(num)
    if not d:
        return None
    eq = d.get('jsonequip') or {}
    slot = INV.get(eq.get('slotbak') or eq.get('slot') or d.get('slot') or d.get('slotbak'))
    lvl = eq.get('reqlevel') or d.get('reqlevel')
    if not slot or (lvl and lvl > MAX_LVL):
        return None
    stats = {}
    for k, v in eq.items():
        if k in WH_STATS and isinstance(v, (int, float)) and v:
            stats[WH_STATS[k]] = max(stats.get(WH_STATS[k], 0), round(v, 1))
    return {'slot': slot, 'lvl': lvl or None, 'il': d.get('level') or eq.get('level') or None, 'q': d.get('quality', eq.get('quality', 1)),
            'names': names_of('item', num, by_lang, {}), 'stats': stats, 'provenance': provenance}


def from_pages(folder):
    """{spec: [entries]}, {id: item} from the saved guide pages of the folder."""
    files = {}
    for f in sorted(os.listdir(folder)):
        m = re.fullmatch(r'([a-z]+-[a-z-]+?)(?:\.([a-z]{2}))?\.html?', f)
        if m:
            files.setdefault(m.group(1), {})[m.group(2) or 'en'] = os.path.join(folder, f)
    items, specs = {}, {}
    for spec, by_file in files.items():
        by_lang = {}
        for lang, path in by_file.items():
            src = open(path, encoding='utf-8', errors='replace').read()
            by_lang[lang] = (gatherer(src), src)
        rows, anchor = page_rows(by_lang.get('en', next(iter(by_lang.values())))[1])
        got = {}
        for kind, sub, cells in rows:
            row = ' '.join(cells)
            ids = [int(x) for x in re.findall(r'\[item=(\d+)', row)]
            tag = lambda k, s=row + ' ' + sub: [int(x) for x in re.findall(rf'\[{k}=(\d+)', s)]  # noqa: E731
            if kind == 'drop':
                zone = tag('zone')
                boss = [int(x) for x in re.findall(r'\[npc=(\d+)', row)]
                plain = next((_txt(c) for c in cells if '[item=' not in c and _txt(c)), '')
                src = {'kind': 'drop', 'boss': names_of('npc', boss[0], by_lang, anchor) if boss else ({'en': plain} if plain else {}),
                       'dungeon': names_of('zone', zone[0], by_lang, anchor) if zone else ({'en': _txt(sub)} if _txt(sub) else {})}
            elif kind == 'quest':
                q = [int(x) for x in re.findall(r'\[quest=(\d+)', row)]
                plain = next((_txt(c) for c in cells if '[item=' not in c and _txt(c)), '')
                src = {'kind': 'quest', 'quest': names_of('quest', q[0], by_lang, anchor) if q else ({'en': plain} if plain else {}),
                       'faction': faction_of(row, sub)}
            else:
                src = {'kind': 'craft', 'prof': prof_of(row, sub)}
            for num in ids:
                if num not in items:
                    it = item_of(num, by_lang, 'wowhead-forever-guide')
                    if not it:
                        continue
                    items[num] = it
                e = got.setdefault(num, {'id': num, 'src': []})
                if src not in e['src']:
                    e['src'].append(src)
        specs[spec] = list(got.values())
    return specs, items


# ---------- SingleFile saves of the Wowhead level-30 class guides (30.10.2026) ----------
# These pages have no item data (scripts stripped): only the item id, the English name, the quality colour and the
# tables of the three parts (dungeon drops, quest rewards, crafted gear) plus world drops on some. So slot (except the
# Slot column of crafted tables), required level, item level, stats and ru names stay empty until the addon dump (05.11).
# Only links and short table cells are read: the guide's own text (advice, notes in brackets) is never kept.

SF_CLASSES = ('warrior', 'paladin', 'hunter', 'rogue', 'priest', 'shaman', 'mage', 'warlock', 'druid')
SF_FILE = re.compile(r'^Level 30 (.+?) (' + '|'.join(c.title() for c in SF_CLASSES) + r')\b.*?\((\d\d)\.(\d\d)\.(\d{4}) (\d\d)\D(\d\d)\D')
SF_PARTS = {'dungeon-drops': 'drop', 'quest-rewards': 'quest', 'crafted-items': 'craft', 'world-drop': 'world', 'reputation-items': 'rep'}
SF_SLOT = {'head': 'head', 'neck': 'neck', 'shoulder': 'shoulder', 'shoulders': 'shoulder', 'back': 'back', 'cloak': 'back',
           'chest': 'chest', 'wrist': 'wrist', 'hands': 'hands', 'waist': 'waist', 'legs': 'legs', 'feet': 'feet',
           'finger': 'finger', 'ring': 'finger', 'trinket': 'trinket', 'off-hand': 'off', 'off hand': 'off', 'shield': 'off'}
SF_SLOT_UNSURE = {'weapon', 'other'}                                  # a slot column that does not name one slot
SF_NOT_GEAR_SLOT = {'enchants', 'enchant', 'oil', 'consumables', 'food'}
SF_NOT_GEAR_PROF = {'cooking', 'alchemy'}
SF_NOT_GEAR_NAME = re.compile(r'^(Formula|Pattern|Plans|Recipe|Schematic|Manual):|Armor Kit$|\bOil$|\bElixir$|\bPotion$')
SF_DUNGEON = {'scarlet monastary': 'Scarlet Monastery', 'the stockades': 'The Stockade',
              'scarlet monastery graveyard': 'Scarlet Monastery: Graveyard', 'scarlet monastery - graveyard': 'Scarlet Monastery: Graveyard',
              'scarlet monastery (graveyard)': 'Scarlet Monastery: Graveyard'}
SF_TRASH = {'trash', 'zone drop'}


def _plain(s):
    s = re.sub(r'(?is)<(script|style|svg)\b.*?</\1>', ' ', s)
    return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()


def _links(s, kind):
    """[(id, text, quality)] of the links to /kind=<id> in an html piece."""
    out = []
    for m in re.finditer(r'(?is)<a\b([^>]*)href="?[^">]*?/' + kind + r'=(\d+)[^>]*>(.*?)</a>', s):
        q = re.search(r'\bq(\d)\b', m.group(1))
        out.append((int(m.group(2)), _plain(m.group(3)), int(q.group(1)) if q else None))
    return out


def _cell_lines(cell):
    """One table cell -> its lines (split at <br>): {'items', 'quests', 'zones', 'skills', 'spells', 'rest'}; rest = text outside links."""
    out = []
    for part in re.split(r'(?i)<br\s*/?>', cell):
        rest = re.sub(r'(?is)<a\b[^>]*>.*?</a>', ' \x00 ', part)
        d = {k: _links(part, k) for k in ('item', 'quest', 'zone', 'skill', 'spell')}
        d['rest'] = _plain(rest.replace('\x00', '|'))
        d['broken'] = [int(x) for x in re.findall(r'(?<![=/\w])item=(\d+)\]', _plain(rest))]   # «item=6687]»: a tag the page failed to render
        if any(d[k] for k in ('item', 'quest', 'zone', 'skill', 'spell', 'broken')) or d['rest'].strip(' |'):
            out.append(d)
    return out


def _bits(rest):
    """The text pieces around links: «| - Boss (note)» -> ['- Boss (note)']."""
    return [x.strip() for x in rest.split('|') if x.strip()]


def _strip_paren(s):
    """«Scorn (rare elite)» -> ('Scorn', ['rare elite'])."""
    notes = re.findall(r'\(([^)]*)\)', s)
    return re.sub(r'\s*\([^)]*\)', '', s).strip(' -–:'), notes


def _dungeon(name):
    n = re.sub(r'\s+', ' ', (name or '').strip(' :'))
    n = re.sub(r'\s+(Drops|Quests)$', '', n)
    return SF_DUNGEON.get(n.lower(), n)


def _faction(text):
    low = text.lower()
    if 'both factions' in low:
        return 'both'
    return 'alliance' if re.search(r'\balliance\b', low) and 'horde' not in low else 'horde' if re.search(r'\bhorde\b', low) and 'alliance' not in low else None


def sf_tables(sec):
    """A part of the page -> [(context, rows)] in order; context = the tab name or the text line ahead of the table
    («Blackfathom Deeps Drops:»), rows = [(is_header, [(td attrs, cell html)])]."""
    tabs = {m.group(1): _plain(m.group(2)) for m in re.finditer(r'(?is)<button\b[^>]*data-href="?#([\w-]+)[^>]*>(.*?)</button>', sec)}
    out, ctx = [], None
    pos = 0
    for m in re.finditer(r'(?is)<div\b[^>]*\bid="?tab-([\w-]+)[^>]*role="?tabpanel[^>]*>|<table\b.*?</table>', sec):
        between = sec[pos:m.start()]
        pos = m.end()
        lines = [x for x in (_plain(p) for p in re.split(r'(?i)<br\s*/?>|<div\b[^>]*>|</div>|<p\b[^>]*>', between)) if x]
        for line in lines:
            if re.search(r'(Drops|Quests|Quest Rewards):$', line):
                ctx = None if line.startswith('Notable') else _dungeon(line[:-1])
        if m.group(1) is not None:
            ctx = _dungeon(tabs.get(m.group(1), '')) or None
            continue
        rows = []
        for r in re.finditer(r'(?is)<tr\b([^>]*)>(.*?)(?=<tr\b|</tbody>|</table>)', m.group(0)):
            cells = [(c.group(1), c.group(2)) for c in re.finditer(r'(?is)<td\b([^>]*)>(.*?)(?=<td\b|$)', r.group(2))]
            head = 'data-background=black' in r.group(1).replace('"', '') and len(cells) > 1 and '<b>' in r.group(2) and '/item=' not in r.group(2)
            rows.append((head, cells))
        out.append((ctx, rows))
    return out


def sf_page(src):
    """One saved page -> ({part: [(src, [(id, name, q, slot)])]}, issues). Facts only."""
    issues, got = [], []
    parts = {}
    for m in re.finditer(r'(?i)<h2\b[^>]*\bid="?([\w-]+)', src):
        parts[m.group(1)] = m.start()
    order = sorted(parts.items(), key=lambda x: x[1])
    for i, (pid, start) in enumerate(order):
        kind = SF_PARTS.get(pid)
        if not kind:
            continue
        sec = src[start:order[i + 1][1] if i + 1 < len(order) else len(src)]
        for ctx, rows in sf_tables(sec):
            cols, sub, fac = [], None, None
            for head, cells in rows:
                if head:
                    cols = [_plain(c).lower() for _, c in cells]
                    continue
                if not cells:
                    continue
                lines = [_cell_lines(c) for _, c in cells]
                flat = [ln for cl in lines for ln in cl]
                if len(cells) == 1 or 'colspan' in cells[0][0]:            # a sub-heading row: dungeon, faction or profession
                    if any(ln['item'] for ln in flat):
                        issues.append(f'row without columns has items: {[x[0] for ln in flat for x in ln["item"]]}')
                        continue
                    text = _plain(cells[0][1])
                    skill = [x[0] for ln in flat for x in ln['skill']]
                    if kind == 'craft':
                        p = SKILL_ID.get(skill[0]) if skill else prof_of(text) if len(text) < 30 else None
                        if p or (skill and not p):
                            sub = p or f'skill-{skill[0]}'
                    elif kind == 'quest' and _faction(text) and len(text) < 20:
                        fac = _faction(text)
                    elif len(text) < 45:
                        sub = _dungeon(text)
                        if kind == 'quest':
                            fac = None
                    continue
                ci = next((j for j, c in enumerate(cols) if c in ('item', 'reward')), len(cells) - 1)
                if ci >= len(cells):
                    issues.append(f'row shorter than header: {_plain(" ".join(c for _, c in cells))[:40]}')
                    continue
                role = {c: j for j, c in enumerate(cols) if j != ci and j < len(cells)}
                item_lines = lines[ci]
                entries = []                                                       # [(id, name, q, extra)] of the row
                for ln in item_lines:
                    for x in ln['spell']:
                        issues.append(f'spell link instead of an item: spell {x[0]} {x[1]!r}')
                    for b in ln['broken']:
                        entries.append((b, None, None, {'broken_tag': True}))
                    bits = _bits(ln['rest'])
                    if not ln['item'] and not ln['broken'] and bits and not ln['spell']:
                        issues.append(f'{kind}: a row names items without a link: {bits[0][:40]!r}')
                    for j, (num, name, q) in enumerate(ln['item']):
                        extra = {}
                        if len(ln['item']) == 1 and bits:
                            b = bits[-1]
                            dash = re.match(r'^[-–]\s*(.+)$', b)
                            if dash:
                                extra['boss'] = _strip_paren(dash.group(1))[0]
                            elif re.match(r'^of the [A-Z]\w+$', b):
                                extra['suffix'] = b
                            elif re.fullmatch(r'\(([^)]*)\)', b) and kind == 'drop' and 'dungeon' in role and 'boss' not in role:
                                inner = b[1:-1]
                                if all(p.strip()[:1].isupper() for p in inner.split(',')) and not re.search(r'only|rare|BoE|technically|requires|crafter', inner):
                                    extra['bosses'] = [p.strip() for p in inner.split(',')]
                        if re.fullmatch(r'\(Item #\d+\)', name or ''):
                            issues.append(f'item {num}: no name on the page (shown as «Item #{num}»), left out')
                            continue
                        entries.append((num, name, q, extra))
                if not entries:
                    continue
                srcs = []
                if kind in ('drop', 'world'):
                    dg = None
                    if 'dungeon' in role:
                        dl = lines[role['dungeon']]
                        z = [x for ln in dl for x in ln['zone']]
                        txt = _plain(cells[role['dungeon']][1])
                        dg = (z[0][1], z[0][0]) if z else (txt, None)
                        if z and _bits(dl[0]['rest']):                         # «[zone=796 Scarlet Monastery] Graveyard»
                            dg = (f'{z[0][1]} {_bits(dl[0]["rest"])[0]}', z[0][0])
                        dg = (_dungeon(_strip_paren(dg[0])[0] + (' Graveyard' if '(Graveyard)' in dg[0] else '')), dg[1])
                    elif sub or ctx:
                        dg = (sub or ctx, None)
                    bosses = []
                    for key in ('boss', 'encounter'):
                        if key in role:
                            b = _strip_paren(_plain(cells[role[key]][1]))[0]
                            bosses = [x.strip() for x in re.split(r'\s+/\s*', b) if x.strip()]
                    for num, name, q, extra in entries:
                        bl = extra.get('bosses') or ([extra['boss']] if extra.get('boss') else bosses)
                        base = {'kind': 'drop'}
                        if kind == 'world':
                            base.update(boss={}, dungeon={}, world=True)
                            one = [dict(base)]
                        else:
                            d = {'en': dg[0]} if dg and dg[0] and dg[0].lower() != 'multiple' else {}
                            if dg and dg[1]:
                                d['zone'] = dg[1]
                            if dg and dg[0] and dg[0].lower() == 'multiple':
                                issues.append(f'item {num}: dungeon «Multiple», no dungeon kept')
                            one = []
                            for b in bl or [None]:
                                s = dict(base, boss={'en': b} if b and b.lower() not in SF_TRASH else {}, dungeon=d)
                                if b and b.lower() in SF_TRASH:
                                    s['trash' if b.lower() == 'trash' else 'zone_drop'] = True
                                one.append(s)
                        if extra.get('suffix'):
                            for s in one:
                                s['suffix'] = extra['suffix']
                        srcs.append(((num, name, q, None), one))
                elif kind == 'quest':
                    qcol = role.get('quest', 0 if ci else None)
                    groups = []
                    for ln in (lines[qcol] if qcol is not None else []):
                        f = _faction(ln['rest'])
                        qs = [{'id': x[0], 'en': x[1]} for x in ln['quest']]
                        if not qs:
                            nm = _strip_paren(' '.join(_bits(ln['rest'])))[0].strip(' /-')
                            if nm and nm != '-':
                                qs = [{'id': None, 'en': nm}]
                        if qs:
                            groups.append((qs, f if f in ('alliance', 'horde') else None))
                    dg = None
                    if 'dungeon' in role:
                        dg = _dungeon(_plain(cells[role['dungeon']][1]))
                    elif sub or ctx:
                        dg = sub or ctx
                    allq = [(qq, f) for qs, f in groups for qq in qs]
                    unsure = len(groups) > 1 and len(item_lines) > 1        # several quests and several items in one row
                    for e in entries:
                        one = []
                        for qq, f in allq or [({'id': None, 'en': None}, None)]:
                            s = {'kind': 'quest', 'quest': {'en': qq['en']} if qq.get('en') else {},
                                 'faction': f or (fac if fac in ('alliance', 'horde') else None)}
                            if qq.get('id'):
                                s['quest']['id'] = qq['id']
                            if dg:
                                s['dungeon'] = {'en': dg}
                            if unsure:
                                s['_unsure'] = True                            # from_singlefile keeps it only if another page pairs them
                            one.append(s)
                        srcs.append(((e[0], e[1], e[2], None), one))
                elif kind == 'craft':
                    label = _plain(cells[0][1]).lower() if ci else ''
                    prof = sub
                    slot = None
                    if 'profession' in role:
                        pl = lines[role['profession']]
                        sk = [x[0] for ln in pl for x in ln['skill']]
                        prof = SKILL_ID.get(sk[0]) if sk else prof_of(_plain(cells[role['profession']][1]))
                        label = ''
                    elif 'slot' in role:
                        if label in SF_NOT_GEAR_SLOT:
                            issues.append(f'not gear (slot «{label}»): items {[e[0] for e in entries]}')
                            continue
                        slot = SF_SLOT.get(label)
                        if not slot:
                            issues.append(f'slot «{label}» names no single slot: items {[e[0] for e in entries]}')
                    if prof in SF_NOT_GEAR_PROF:
                        issues.append(f'not gear ({prof}): items {[e[0] for e in entries]}')
                        continue
                    for num, name, q, extra in entries:
                        if name and SF_NOT_GEAR_NAME.search(name):
                            issues.append(f'not gear (name): item {num} {name!r}')
                            continue
                        srcs.append(((num, name, q, slot), [{'kind': 'craft', 'prof': prof if prof in PROFS else None}]))
                        if prof not in PROFS:
                            issues.append(f'item {num}: profession not recognised ({prof})')
                else:                                                          # reputation: no source kind for it in the schema
                    issues.append(f'reputation reward, left out (no such source kind): items {[e[0] for e in entries]}')
                    continue
                got += srcs
    return got, issues


def from_singlefile(folder):
    """{spec: [entries]}, {id: item}, {spec: file info}, [issues] from the SingleFile saves of the folder."""
    items, specs, files, issues = {}, {}, {}, []
    seen_name = {}
    for f in sorted(os.listdir(folder)):
        m = SF_FILE.match(f)
        if not m or not f.endswith(('.html', '.htm')):
            if f.endswith(('.html', '.htm')):
                issues.append(f'file not recognised: {f}')
            continue
        spec = f'{m.group(2).lower()}-{m.group(1).lower().replace(" ", "-")}'
        if spec in files:
            issues.append(f'{spec}: two files, kept {files[spec]["file"]}')
            continue
        files[spec] = {'file': f, 'saved': f'{m.group(5)}-{m.group(4)}-{m.group(3)} {m.group(6)}:{m.group(7)}'}
        src = open(os.path.join(folder, f), encoding='utf-8', errors='replace').read()
        rows, page_issues = sf_page(src)
        issues += [f'{spec}: {x}' for x in page_issues]
        got = {}
        for (num, name, q, slot), srcs in rows:
            if name is None:
                name = seen_name.get(num)
                issues.append(f'{spec}: item {num} written as plain text «item={num}]», name ' + (f'{name!r} from other pages' if name else 'unknown'))
            it = items.get(num)
            if it is None:
                it = items[num] = {'slot': slot, 'lvl': None, 'il': None, 'q': q, 'names': {'en': name} if name else {},
                                   'stats': {}, 'provenance': 'wowhead-forever-guide'}
            else:
                if slot and it['slot'] and slot != it['slot']:
                    issues.append(f'item {num}: slot {it["slot"]} and {slot} on different pages')
                it['slot'] = it['slot'] or slot
                if q is not None and it['q'] is not None and q != it['q']:
                    issues.append(f'item {num}: quality {it["q"]} and {q} on different pages')
                it['q'] = it['q'] if it['q'] is not None else q
                if name and it['names'].get('en') and name != it['names']['en']:
                    issues.append(f'item {num}: names {it["names"]["en"]!r} and {name!r} on different pages')
                if name and not it['names'].get('en'):
                    it['names']['en'] = name
            if name:
                seen_name.setdefault(num, name)
            e = got.setdefault(num, {'id': num, 'src': []})
            for s in srcs:
                if s not in e['src']:
                    e['src'].append(s)
        specs[spec] = list(got.values())
    # a row with several quests and several items says nothing on which quest gives which item: keep a quest only when
    # another page pairs that item with that quest in a row of its own; otherwise the source is «a quest» (dungeon kept)
    sure = {}
    for entries in specs.values():
        for e in entries:
            for s in e['src']:
                if s['kind'] == 'quest' and not s.get('_unsure') and s['quest'].get('id'):
                    sure.setdefault(e['id'], set()).add(s['quest']['id'])
    for spec, entries in specs.items():
        for e in entries:
            if not any(s.get('_unsure') for s in e['src']):
                continue
            keep, cand = [], []
            for s in e['src']:
                if not s.get('_unsure'):
                    keep.append(s)
                    continue
                cand.append(s['quest'].get('id'))
                if s['quest'].get('id') in sure.get(e['id'], ()):
                    keep.append({k: v for k, v in s.items() if k != '_unsure'})
            if not any(s['kind'] == 'quest' for s in keep):
                blank = {k: v for k, v in next(s for s in e['src'] if s.get('_unsure')).items() if k not in ('_unsure', 'quest')}
                keep.append({'kind': 'quest', 'quest': {}, **{k: v for k, v in blank.items() if k != 'kind'}, 'faction': None})
                issues.append(f'{spec}: item {e["id"]}: quest is one of {cand}, the page does not say which; kept as «a quest» without a name')
            else:
                issues.append(f'{spec}: item {e["id"]}: quest taken from another page that pairs them ({[s["quest"].get("id") for s in keep if s["kind"] == "quest"]} of {cand})')
            dedup = []
            for s in keep:
                if s not in dedup:
                    dedup.append(s)
            e['src'] = dedup
    return specs, items, files, list(dict.fromkeys(issues))


# ---------- the addon dump ----------

ARMOR_MAX = {'warrior': 3, 'paladin': 3, 'hunter': 2, 'shaman': 2, 'rogue': 2, 'druid': 2, 'mage': 1, 'priest': 1, 'warlock': 1}
WEAPONS = {'warrior': {0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 13, 15, 16, 18}, 'paladin': {0, 1, 4, 5, 6, 7, 8},
           'hunter': {0, 1, 2, 3, 6, 7, 8, 10, 13, 15, 18}, 'rogue': {2, 3, 4, 7, 13, 15, 16, 18}, 'priest': {4, 10, 15, 19},
           'shaman': {0, 1, 4, 5, 10, 13, 15}, 'mage': {7, 10, 15, 19}, 'warlock': {7, 10, 15, 19}, 'druid': {4, 5, 10, 13, 15}}
SHIELD = {'warrior', 'paladin', 'shaman'}
ROLE_W = {'tank': 'sta armor def str agi', 'heal': 'hp int spi mp5 crit', 'caster': 'sp hit crit int spi', 'str': 'dps hit crit str agi',
          'agi': 'dps hit agi crit'}
HEALERS = {'priest-holy', 'priest-discipline', 'paladin-holy', 'shaman-restoration', 'druid-restoration'}
TANKS = {'warrior-protection', 'paladin-protection'}
PCT = {'hit', 'crit'}


def weights(spec):
    """Stat weights of a spec from its priority in spec_cheats.STATS (first 1.0, then down); no order there: the role's."""
    from content import spec_cheats
    st = spec_cheats.STATS.get(spec)
    cls = spec.split('-')[0]
    if isinstance(st, tuple):
        keys = st[0].split()
    else:
        role = ('tank' if spec in TANKS else 'heal' if spec in HEALERS else 'caster' if cls in ('mage', 'warlock') or spec in
                ('priest-shadow', 'shaman-elemental', 'druid-balance') else 'agi' if cls in ('rogue', 'hunter') or spec == 'druid-feral' else 'str')
        keys = ROLE_W[role].split()
    keys = ['dps' if k == 'wd' else k for k in keys if k not in ('exp', 'haste')]
    w = {k: max(0.3, 1 - 0.15 * i) for i, k in enumerate(keys)}
    w.setdefault('sta', 0.1)
    return w


def score(it, w):
    s = 0.0
    for k, v in it['stats'].items():
        x = w.get(k, 0) * v
        s += x * 10 if k in PCT else x * 0.02 if k == 'armor' else x
    return s


def allowed(it, cls):
    c, sub = it.get('cls'), it.get('sub')
    if c == 4:                                                     # armor: cloth 1, leather 2, mail 3, plate 4, shield 6, misc 0
        if sub == 6:
            return cls in SHIELD
        return it['slot'] == 'back' or sub in (0, None) or sub <= ARMOR_MAX[cls]
    if c == 2:
        return sub in WEAPONS[cls]
    return True


def pick(spec, pool, per_slot=4):
    """The best item at its own required level for every slot (nothing at a lower level beats it), the last per_slot of them."""
    cls, w = spec.split('-')[0], weights(spec)
    out = []
    for slot in SLOTS:
        cand = sorted((it for it in pool.values() if it['slot'] == slot and allowed(it, cls) and score(it, w) > 0),
                      key=lambda it: (it['lvl'] or 0, -score(it, w)))
        best, keep = 0.0, []
        for it in cand:
            s = score(it, w)
            if s > best:
                best = s
                keep.append(it)
        out += keep[-per_slot:]
    return out


def tip_stats(lines, stats):
    for line in lines or ():
        for rx, keys in TIP_STATS:
            m = re.search(rx, line)
            if m:
                for k in keys:
                    stats.setdefault(k, int(m.group(1)))


def _by_id(t):
    """An int-keyed Lua table reads as a list or a dict: (key, value) pairs either way."""
    return t.items() if isinstance(t, dict) else ((i, v) for i, v in enumerate(t or [], 1) if v is not None)


def _read_db(path):
    sys.path.insert(0, os.path.join(HERE, 'tools'))
    from talent_import import parse_lua                       # the same SavedVariables reader as the talents
    return parse_lua(open(path, encoding='utf-8').read())['GabellaGearDB']


# item class of the client -> kind (0 consumable, 2 weapon, 4 armor, 5 reagent, 7 trade goods)
ICLASS = {0: 'consumable', 2: 'weapon', 4: 'armor', 5: 'reagent', 7: 'trade'}


def addon_items(path):
    """Every item of a dump, v1 or v2: {id: {kind, iclass, isub, slot (INVTYPE_* or None), lvl, il, q, icon (file id),
    names {lang}, stats {our keys}, tip {lang: [lines]}}}; for the item catalog and the icons of consumables."""
    db, out = _read_db(path), {}
    for num, d in _by_id(db.get('items')):
        c = d.get('iclass', d.get('cls'))
        stats = {CL_STATS[k]: round(v, 1) for k, v in (d.get('stats') or {}).items() if k in CL_STATS and v}
        out[int(num)] = {'kind': ICLASS.get(c), 'iclass': c, 'isub': d.get('isub', d.get('sub')), 'slot': d.get('slot') or None,
                         'lvl': d.get('req') or None, 'il': d.get('ilvl') or None, 'q': d.get('q', 1), 'icon': d.get('icon'),
                         'names': {LOC[loc]: n for loc, n in (d.get('name') or {}).items() if loc in LOC}, 'stats': stats,
                         'tip': {LOC[loc]: v for loc, v in (d.get('tip') or {}).items() if loc in LOC}}
    return out


def from_addon(path):
    db = _read_db(path)
    by_id = _by_id
    names = json.load(open(os.path.join(HERE, 'i18n', 'names.json'), encoding='utf-8'))
    prof_any = {n.lower(): p for p in PROFS for en in [p.title().replace('Firstaid', 'First Aid')] for n in [en, *names.get(en, {}).values()]}
    pool = {}
    for num, d in by_id(db.get('items')):
        slot = INV.get(INVTYPE.get(d.get('slot')))
        if not slot or (d.get('req') or 0) > MAX_LVL:
            continue
        stats = {}
        for k, v in (d.get('stats') or {}).items():
            if k in CL_STATS and v:
                stats[CL_STATS[k]] = round(v, 1)
        tip_stats((d.get('tip') or {}).get('enUS') or (d.get('tip') or {}).get('enGB'), stats)
        pool[int(num)] = {'id': int(num), 'slot': slot, 'lvl': d.get('req') or None, 'il': d.get('ilvl') or None, 'q': d.get('q', 1),
                          'names': {LOC[loc]: n for loc, n in (d.get('name') or {}).items() if loc in LOC}, 'stats': stats,
                          'provenance': 'client-dump', 'cls': d.get('iclass', d.get('cls')), 'sub': d.get('isub', d.get('sub'))}
    srcs = {}
    for num, recs in by_id(db.get('src')):
        out = []
        for r in (recs.values() if isinstance(recs, dict) else recs):
            nm = lambda x: {LOC[l]: v for l, v in (x or {}).items() if l in LOC}  # noqa: E731
            if r.get('kind') == 'drop':
                out.append({'kind': 'drop', 'boss': nm(r.get('name')), 'dungeon': nm(r.get('zone'))})
            elif r.get('kind') == 'quest':
                f = (r.get('faction') or '').lower()
                out.append({'kind': 'quest', 'quest': nm(r.get('name')), 'faction': f if f in ('alliance', 'horde') else None})
            elif r.get('kind') == 'craft':
                got = [prof_any.get((n or '').lower()) or prof_of(n or '') for n in (r.get('name') or {}).values()]
                out.append({'kind': 'craft', 'prof': next((p for p in got if p), None)})
        srcs[int(num)] = out
    from content.spec_cheats import CHEATS
    items, specs = {}, {}
    for c, s in CHEATS:
        spec = f'{c}-{s}'
        chosen = pick(spec, pool)
        specs[spec] = [{'id': it['id'], 'src': srcs.get(it['id'], [])} for it in chosen]
        for it in chosen:
            items[it['id']] = {k: v for k, v in it.items() if k not in ('id', 'cls', 'sub')}
    return specs, items


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--pages')
    g.add_argument('--addon')
    g.add_argument('--singlefile', help='folder of the SingleFile saves of the Wowhead level-30 class guides')
    ap.add_argument('--out', default=OUT)
    ap.add_argument('--date', default=datetime.date.today().isoformat())
    ap.add_argument('--fixture', action='store_true')
    ap.add_argument('--approve', action='store_true', help='Вячеслав accepted the data: the build shows the section')
    a = ap.parse_args()
    extra = {}
    if a.singlefile:
        specs, items, files, issues = from_singlefile(a.singlefile)
        extra = {'provenance': {'source': 'Wowhead Forever level-30 class guides (SingleFile saves, offline)', 'kind': 'wowhead-forever-guide',
                                'saved': '2026-10-30', 'temporary': 'временно до дампа аддона 05.11 (tools/gear_dump)',
                                'files': {k: files[k] for k in sorted(files)}},
                 'missing': ['slot: only crafted items with a Slot column', 'lvl', 'il', 'stats', 'names.ru'],
                 'issues': issues}
    else:
        specs, items = from_pages(a.pages) if a.pages else from_addon(a.addon)
    # specs with fewer than 6 slots: shown as they are with the mark «incomplete» (content/spec_cheats.GEAR_MIN_SLOTS, tests/test_guides.py)
    partial = sorted(k for k in specs if 0 < len({items[e['id']]['slot'] for e in specs[k]} - {None}) < 6)
    data = {'schema': 1, 'date': a.date, 'fixture': bool(a.fixture), 'approved': bool(a.approve), 'partial': partial, **extra,
            'items': {str(k): items[k] for k in sorted(items)}, 'specs': {k: specs[k] for k in sorted(specs)}}
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    for k in sorted(specs):
        slots = {items[e['id']]['slot'] for e in specs[k]} - {None}
        print(f'{k}: {len(specs[k])} items, {len(slots)} slots')
    if extra.get('issues'):
        print(f'{len(extra["issues"])} issues (see "issues" in the file)')
    print(f'{len(items)} items -> {a.out}')


if __name__ == '__main__':
    main()
