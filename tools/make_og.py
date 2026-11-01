"""Share previews 1200x630 with the page title on the art: home (og-<lang>.jpg), guides, the classes/ and races/ sections
and tools (og/<slug>-<lang>.jpg). Rendered from HTML with the site fonts by headless Chrome, so the type matches the site.
Class and race cards (og/<class|race>-<lang>.jpg) and the builds-/leveling- guides of a class stand on the portrait of that class.
Run: python tools/make_og.py [slug ...] [--langs=de,fr] [--live] [--out=DIR]   (no args = all cards in every built language)
--live draws the post-launch line instead of the launch moment (a preview; the switch for the site is live.py); --out=DIR writes there."""
import json, os, re, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(ROOT, 'content'), ROOT]
from guides import HUB, GUIDES, HUBS  # noqa: E402

sys.path.insert(0, ROOT)
import langs  # noqa: E402
import live  # noqa: E402
from classes import CLASSES  # noqa: E402
import build_guides as BG  # noqa: E402
import build_talent_links as TL  # noqa: E402
from content import spec_cheats as SC  # noqa: E402

CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
LANGS = langs.LANGS
BRAND = 'Gabella'
REF = {'ru': 'Справочник', 'uk': 'Довідник', 'en': 'Reference', 'de': 'Kompendium', 'pl': 'Kompendium', 'fr': 'Référence',
       'es': 'Referencia', 'it': 'Compendio', 'pt': 'Referência'}   # the word of the header («Справочник» decision 27.10)
START = {'ru': 'Старт 05.11, 01:00 по Киеву', 'en': 'Launch Nov 4, 23:00 UTC', 'uk': 'Старт 05.11, 01:00 за Києвом',
         'de': 'Start 5. Nov., 00:00 MEZ', 'fr': 'Lancement 5 nov., 00 h 00 à Paris', 'es': 'Lanzamiento 5 nov., 00:00 en Madrid',
         'pt': 'Lançamento 4 nov., 20:00 em Brasília', 'it': 'Uscita 5 nov., ore 00:00', 'pl': 'Start 5 listopada, 00:00 w Polsce'}   # the moment, not a bare date; pl in local time like de/fr (as its description, 28.10 audit №9)
LIVE_LINE = {'ru': 'Уже в игре', 'en': 'Live now', 'uk': 'Уже в грі', 'de': 'Jetzt live', 'fr': 'Déjà en ligne', 'es': 'Ya disponible',
             'pt': 'Já no ar', 'it': 'Già online', 'pl': 'Już w grze'}   # replaces START after the launch night (live.py)
ROLES = {'ru': {'tank': 'Танк', 'heal': 'Лекарь', 'dps': 'Урон'}, 'uk': {'tank': 'Танк', 'heal': 'Цілитель', 'dps': 'Шкода'},
         'en': {'tank': 'Tank', 'heal': 'Healer', 'dps': 'Damage'}, 'de': {'tank': 'Tank', 'heal': 'Heiler', 'dps': 'Schaden'},
         'fr': {'tank': 'Tank', 'heal': 'Soigneur', 'dps': 'Dégâts'}, 'es': {'tank': 'Tanque', 'heal': 'Sanador', 'dps': 'Daño'},
         'pt': {'tank': 'Tanque', 'heal': 'Curandeiro', 'dps': 'Dano'}, 'it': {'tank': 'Tank', 'heal': 'Guaritore', 'dps': 'Danno'},
         'pl': {'tank': 'Tank', 'heal': 'Healer', 'dps': 'DPS'}}   # pl: the game terms the Polish pages use (Healer, class and race names stay English there)
JOIN = ' · '   # a bullet stays at the end of its line, never opens the next one
ROUTE = {'ru': 'Маршрут, сборка и темп прокачки', 'uk': 'Маршрут, збірка й темп прокачування', 'en': 'Route, build and leveling pace',
         'de': 'Route, Build und Leveltempo', 'fr': 'Parcours, build et rythme de leveling', 'es': 'Ruta, build y ritmo de nivelación',
         'pt': 'Rota, build e ritmo de evolução', 'it': 'Percorso, build e ritmo di livellamento', 'pl': 'Trasa, build i tempo levelowania'}
GAME = json.load(open(os.path.join(ROOT, 'assets', 'game.json'), encoding='utf-8'))
SIDE_RACE = {'warrior': 'human', 'paladin': 'human', 'hunter': 'nightelf', 'rogue': 'nightelf', 'priest': 'gnome', 'shaman': 'dwarf',
             'mage': 'gnome', 'warlock': 'gnome', 'druid': 'nightelf'}   # the Alliance portrait of each class (tools/make_build_cards.py POR)
EXACT = {'launch-day': {'ru': '04.11, 23:00 UTC · Киев 05.11, 01:00', 'en': 'Nov 4, 15:00 PST · 23:00 UTC',
                        'uk': 'Старт 04.11, 23:00 UTC · 15:00 PST', 'de': '5. November, 00:00 MEZ',
                        'fr': '5 novembre, minuit à Paris', 'es': '4 nov., 23:00 UTC · Madrid 00:00',
                        'pt': '4 de novembro, 20:00 em Brasília', 'it': '5 novembre, ore 00:00 in Italia',
                        'pl': '5 listopada, 00:00 w Polsce'}}   # the launch card names the moment (uk, pl: the lead already gives local time)
HOME = {'t': {l: 'WoW Forever' for l in langs.ALL},
        'd': {'ru': 'Legacy, тир-лист, конструктор группы, новости',
              'en': 'Legacy, tier list, group builder, news',
              'uk': 'Legacy, тір-лист, конструктор групи, новини',
              'de': 'Legacy, Tierliste, Gruppenplaner, News',
              'fr': 'Legacy, tier list, créateur de groupe, actus',
              'es': 'Legacy, tier list, creador de grupos, noticias',
              'pt': 'Legacy, tier list, montador de grupo, notícias',
              'it': 'Legacy, tier list, creatore di gruppi, notizie',
              'pl': 'Legacy, tier lista, kreator grupy, newsy'}}
TOOLS = {'t': {'ru': 'Состав группы', 'uk': 'Склад групи', 'en': 'Group builder', 'de': 'Gruppenplaner', 'fr': 'Créateur de groupe', 'es': 'Creador de grupos',
                'it': 'Creatore di gruppi', 'pt': 'Montador de grupo', 'pl': 'Kreator grupy'},   # a shared team link (tools/#t=) shows this card
         'd': {'ru': 'Рамки группы, рейдовая сетка, сравнение классов и рас, поиск',
               'en': 'Party frames, raid grid, class and race comparison, search',
               'uk': 'Рамки групи, рейдова сітка, порівняння класів і рас, пошук',
               'de': 'Gruppenrahmen, Schlachtzugsraster, Klassen- und Volksvergleich, Suche',
               'fr': 'Cadres de groupe, grille de raid, comparaison des classes et races, recherche',
               'es': 'Marcos de grupo, cuadrícula de banda, comparación de clases y razas, búsqueda',
               'pt': 'Quadros de grupo, grade de raide, comparação de classes e raças, busca',
               'it': 'Riquadri del gruppo, griglia d’incursione, confronto classi e razze, ricerca',
               'pl': 'Ramki grupy, siatka raidu, porównanie klas i ras, wyszukiwarka'}}
langs.fill([HUB, GUIDES, HUBS])
FOCUS = {'hero_dawn': '70%', 'hero_campfire': '88%'}   # horizontal crop of a landscape scene; the default is the right edge
NODATE = {'tier-list'}   # the beta snapshot is refreshed after launch: no launch date under the title
SKIP = set()            # a card that waits for its new scene; named on the command line it is rendered anyway


def core(lang):
    """class, race, spec and faction names in the language (the same tables the character block uses)"""
    return BG.hero_core(lang)


def spec_roles(cid, spec, lang):
    """«Урон», «Танк · Урон»: the roles of a spec on the class page (a guessed '?' role stays off the card)"""
    c = next(x for x in CLASSES if x['id'] == cid)
    sp = next(x for x in c['specs'] if re.sub(r'\W+', '-', x['en'].lower()) == spec)
    return JOIN.join(ROLES[lang][r] for r in sp['roles'] if not r.endswith('?'))


def cards():
    """(file name without -lang, art, title by lang, line under the title by lang, foot line by lang or None = the launch line)"""
    yield 'og', 'hero_dawn', HOME['t'], HOME['d'], None
    yield 'og/guides', HUB['hero'], HUB['title'], HUB['lead'], None
    N = {l: core(l) for l in LANGS}
    for g in GUIDES + HUBS:
        art = g.get('hero') or g['art']
        lead = g['lead']
        m = re.match(r'(builds|leveling)-(\w+)$', g['slug'])
        if m:                                              # a class guide: the portrait of the class, one short line
            art = f'{m[2]}-{SIDE_RACE[m[2]]}'
            lead = ({l: JOIN.join(N[l]['sn'][m[2]]) for l in LANGS} if m[1] == 'builds' else ROUTE)
        s = re.match(r'spec-([a-z]+)-([a-z-]+)$', g['slug'])
        if s:                                              # a spec guide (and the share page of a talent build, t/): class portrait, «Frost Mage»
            yield ('og/' + g['slug'], f'{s[1]}-{SIDE_RACE[s[1]]}', {l: TL.spec_name(s[1], s[2], l) for l in LANGS},
                   {l: f'{spec_roles(s[1], s[2], l)}. {SC.LEAD_TAIL[l]}' for l in LANGS}, None)
            continue
        yield 'og/' + g['slug'], art, g['title'], lead, None
    yield 'og/tools', 'hero_tools', TOOLS['t'], TOOLS['d'], None
    yield 'og/404', 'hero_dawn', {'xx': 'WoW Forever'}, {'xx': ''}, {'xx': 'gabella.site/wow'}   # one card for every language: the root 404.html is one page for all
    for c in CLASSES:
        roles = [r.rstrip('?') for r in c['roles']]
        yield ('og/' + c['id'], f'{c["id"]}-{SIDE_RACE[c["id"]]}', {l: N[l]['cn'][c['id']] for l in LANGS},
               {l: JOIN.join(N[l]['sn'][c['id']]) for l in LANGS}, {l: JOIN.join(ROLES[l][r] for r in roles) for l in LANGS})
    for rid, r in GAME['races'].items():
        yield ('og/' + r['slug'], r['slug'], {l: N[l]['rn'][rid] for l in LANGS},
               {l: JOIN.join(N[l]['cn'][c] for c in r['cls']) for l in LANGS}, {l: N[l]['fn'][r['f']] for l in LANGS})


def url(path):
    return 'file:///' + os.path.join(ROOT, path).replace('\\', '/')


def html(art, title, lead, lang, slug='', foot=None):
    assert os.path.isfile(os.path.join(ROOT, 'assets', 'art', f'{art}-1344.webp' if not art.startswith('hero_') else f'{art}-1440.webp')) or art == 'hero_campfire', f'no art {art}'
    wide = art.startswith('hero_')
    pic = (f'<img class="wide" src="{url(f"assets/art/{art}-1600.webp" if art == "hero_campfire" else f"assets/art/{art}-1440.webp")}">'
           if wide else
           f'<img class="blur" src="{url(f"assets/art/{art}-bg.webp")}"><img class="por" src="{url(f"assets/art/{art}-1344.webp")}">')
    fonts = ''.join(
        f'@font-face{{font-family:"{fam}";font-weight:400 700;src:url({url("assets/fonts/" + f)}) format("woff2");unicode-range:{rng}}}'
        for fam, base in (('Spectral SC', 'spectral-sc'), ('Golos Text', 'golos-text'))
        for f, rng in ((base + '-cyrillic.woff2', 'U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116'), (base + '-latin-ext.woff2', 'U+0100-02BA,U+1E00-1E9F'),
                       (base + '-latin.woff2', 'U+0000-00FF,U+2000-206F')))
    return f'''<!doctype html><meta charset="utf-8"><style>{fonts}
*{{margin:0;box-sizing:border-box}}
body{{width:1200px;height:630px;overflow:hidden;background:#050505;position:relative;font-family:"Golos Text";color:#efe9da;font-variant-numeric:lining-nums}}
img{{position:absolute;display:block}}
.wide{{inset:0;width:100%;height:100%;object-fit:cover;object-position:{FOCUS.get(art, '50%')} 50%}}
.blur{{inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.8)}}
.por{{right:0;top:-16px;width:760px;-webkit-mask-image:linear-gradient(90deg,transparent,#000 30%)}}
.shade{{position:absolute;inset:0;background:linear-gradient(90deg,#050505 0%,rgba(5,5,5,.92) 34%,rgba(5,5,5,.35) 62%,rgba(5,5,5,0) 80%),
  linear-gradient(0deg,rgba(5,5,5,.85) 0%,rgba(5,5,5,0) 36%)}}
.txt{{position:absolute;left:72px;top:0;bottom:0;width:620px;display:flex;flex-direction:column;justify-content:center;gap:24px}}
.brand{{position:absolute;left:72px;top:52px;display:flex;align-items:center;gap:22px;font:600 48px/1 "Spectral SC";color:#efe9da;letter-spacing:.04em;font-variant-numeric:lining-nums}}
.brand .ref{{color:#c9a54a;font-size:32px;letter-spacing:.06em;padding-left:22px;border-left:1px solid rgba(201,165,74,.45)}}
.brand img{{position:static;width:96px;height:96px;border-radius:50%}}
h1{{font:600 {'92' if len(title) <= 14 else '74'}px/1.02 "Spectral SC";letter-spacing:.02em;text-wrap:balance;font-variant-numeric:lining-nums}}
p{{font-size:30px;line-height:1.35;color:#c9c2b0;text-wrap:pretty;max-width:{"520" if wide else "600"}px}}
.start{{position:absolute;left:72px;bottom:56px;font:600 28px/1 "Spectral SC";letter-spacing:.03em;color:#c9a54a;font-variant-numeric:lining-nums}}
</style><body>{pic}<div class="shade"></div>
<div class="brand"><img src="{url('assets/logo.png')}" alt="">{BRAND}{f'<span class="ref">{REF[lang]}</span>' if lang != 'xx' else ''}</div>
<div class="txt"><h1>{title}</h1><p>{lead}</p></div>
<div class="start">{foot if foot is not None else '' if slug in NODATE else (LIVE_LINE[lang] if LIVE else EXACT.get(slug, START)[lang])}</div>
<div id="res" hidden></div>
<script>/* lay the text block out between the logo and the launch line: width first (Spectral is wide), then height */
document.fonts.ready.then(()=>{{   /* measure in Spectral, not in the fallback that is there before the font arrives */
const R=e=>e.getBoundingClientRect(),$=s=>document.querySelector(s),h=$('h1'),p=$('p'),br=$('.brand'),st=$('.start');
const px=()=>parseFloat(getComputedStyle(h).fontSize),LH=40.5,GAP=24;
const fits=()=>R(h).top>=R(br).bottom+GAP&&R(p).bottom<=R(st).top-GAP;
while(h.scrollWidth>h.clientWidth&&px()>40)h.style.fontSize=(px()-2)+'px';
while(!fits()&&px()>48)h.style.fontSize=(px()-2)+'px';
if(!fits()){{const sen=p.textContent.split(/(?<=[.!?])\\s+/);while(!fits()&&sen.length>1){{sen.pop();p.textContent=sen.join(' ')}}
 const w=p.textContent.split(' ');while(!fits()&&w.length>3){{w.pop();p.textContent=w.join(' ').replace(/[,;:\u2013-]$/,'')+'\u2026'}}}}
let right=0;for(const e of [h,p]){{const r=document.createRange();r.selectNodeContents(e);right=Math.max(right,r.getBoundingClientRect().right)}}
const box=e=>{{const r=R(e);return [r.left,r.top,r.right,r.bottom]}},bx={{brand:box(br),title:box(h),lead:box(p),start:box(st)}};
$('#res').textContent=JSON.stringify({{boxes:bx,right:right,font:px(),wide:h.scrollWidth>h.clientWidth,lines:Math.round(R(p).height/LH),block:R(p).bottom-R(h).top}})}})</script></body>'''


def chrome(src, *args):
    return subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                           '--force-device-scale-factor=1', '--window-size=1200,630', '--virtual-time-budget=3000', *args,
                           'file:///' + src.replace('\\', '/')], check=True, capture_output=True)


def check(res, out):
    """The laid-out boxes must stay inside the 48 px margins and keep 24 px between neighbours; otherwise stop and name the file."""
    bx, names = res['boxes'], ['brand', 'title', 'lead', 'start']
    bad = [f'{n} leaves the 48 px margin' for n in names if bx[n][0] < 48 or bx[n][1] < 48 or bx[n][2] > 1152 or bx[n][3] > 582]
    bad += [f'{a} and {b} are closer than 24 px' for i, a in enumerate(names) for b in names[i + 1:]
            if bx[a][0] < bx[b][2] and bx[b][0] < bx[a][2] and bx[a][1] < bx[b][3] + 24 and bx[b][1] < bx[a][3] + 24]
    if res['right'] > RIGHT_MAX:
        bad.append(f'text reaches x={res["right"]:.0f}, past the face line {RIGHT_MAX}')
    if res['wide']:
        bad.append('the longest word of the title does not fit the column')
    if bad:
        FAILS.append(f'{os.path.relpath(out, ROOT)}: ' + '; '.join(bad))


METRICS = {}
FAILS = []
RIGHT_MAX = 700   # no letter of the title or the line may reach past this x: the portrait starts there
LIVE, OUT = False, None


def shoot(page, out):
    with tempfile.TemporaryDirectory() as tmp:
        src, png = os.path.join(tmp, 'c.html'), os.path.join(tmp, 'c.png')
        with open(src, 'w', encoding='utf-8') as f:
            f.write(page)
        dom = chrome(src, '--dump-dom').stdout.decode('utf-8')          # the page lays itself out; read what it decided
        res = json.loads(re.search(r'<div id="res"[^>]*>(.*?)</div>', dom, re.S).group(1))
        check(res, out)
        METRICS[os.path.relpath(out, ROOT).replace('\\', '/')] = res
        chrome(src, f'--screenshot={png}')
        Image.open(png).convert('RGB').save(out, quality=82, optimize=True, progressive=True)


def main():
    global LIVE, OUT
    LIVE = live.LIVE or '--live' in sys.argv
    OUT = next((a[6:] for a in sys.argv[1:] if a.startswith('--out=')), None)
    only = {a for a in sys.argv[1:] if not a.startswith('--')}
    pick = next((a[8:].split(',') for a in sys.argv[1:] if a.startswith('--langs=')), LANGS)   # --langs=de,fr: only these
    jobs = []
    for name, art, title, lead, foot in cards():
        slug = name.split('/')[-1]
        if (only and slug not in only) or (not only and slug in SKIP):
            continue
        for lang in (l for l in (*pick, 'xx') if l in title):        # a one-language guide has one card
            out = os.path.join(OUT or os.path.join(ROOT, 'assets'), f'{name}.jpg' if lang == 'xx' else f'{name}-{lang}.jpg')
            os.makedirs(os.path.dirname(out), exist_ok=True)
            jobs.append((html(art, title[lang], lead[lang], lang, slug, foot and foot[lang]), out))
    with ThreadPoolExecutor(8) as ex:                         # one headless Chrome per card, eight at a time
        list(ex.map(lambda j: shoot(*j), jobs))
    print(len(jobs), 'cards')
    if FAILS:
        print(chr(10).join(FAILS))
        raise SystemExit(f'{len(FAILS)} cards do not fit')
    if os.environ.get('OG_REPORT'):
        with open(os.environ['OG_REPORT'], 'w') as f:
            json.dump(METRICS, f)


if __name__ == '__main__':
    main()
