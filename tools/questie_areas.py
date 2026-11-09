"""Area ids of the dungeons for the in-game addon -> data/addon_dungeon_areas.json {English name of DUNGEONS (index.src.html): areaId}.
The ids are Questie's (QuestieDB/support/Forever/Zones/dungeons.lua of the Forever client, read only): the addon gets the area id of the
instance the player stands in. A dungeon is matched by its English name; a wing («Scarlet Monastery: Library», «Dire Maul: East») and the
two Blackrock Spire parts have the area of their instance as Questie knows it. No match (new Forever dungeons Questie has no area for)
is not written and is listed. Run: python tools/questie_areas.py [dungeons.lua]   (the file is committed; build.py does not run this)"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
LUA = r'C:\Program Files (x86)\World of Warcraft\_forever_\Interface\AddOns\QuestieDB\support\Forever\Zones\dungeons.lua'
OUT = os.path.join(ROOT, 'data', 'addon_dungeon_areas.json')
PARENT = {'Lower Blackrock Spire': 'Blackrock Spire', 'Upper Blackrock Spire': 'Blackrock Spire'}   # two parts of one Questie instance


def norm(s):
    return re.sub(r'[^a-z0-9]+', '', s.lower().replace('the ', ''))


def main(path=LUA):
    from content import dungeon_pages
    ents = re.findall(r'^\s*\[(\d+)\]\s*=\s*\{"([^"]+)"', open(path, encoding='utf-8').read(), re.M)
    by = {}
    for i, n in ents:
        by.setdefault(norm(n), int(i))    # the main id of a name (alternative area ids are listed after it in the file)
    _, order = dungeon_pages.registry()
    out, miss = {}, []
    for name in order:
        for cand in (name, PARENT.get(name), name.split(':')[0]):
            if cand and norm(cand) in by:
                out[name] = by[norm(cand)]
                break
        else:
            miss.append(name)
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(f'{len(out)} of {len(order)} dungeons have an area id; none for: {", ".join(miss)}')


if __name__ == '__main__':
    main(*sys.argv[1:])
