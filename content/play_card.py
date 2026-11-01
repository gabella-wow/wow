"""/play/: the card «My class at level N» on top of the character block (variant B of docs/wow/audit/2026-11-01-second-screen-review).
Nothing is written here by hand but the labels: every fact of the card is read from the data the site already shows elsewhere —
  talents  the order by level of guides/builds-<class>/ (talents.py): the leveling build 10–60 of the class leveling guide where it fits
           the tree, else the spec's own table (beta, up to 30);
  abilities the «Level / What to take» table of guides/leveling-<class>/ (content/class_guides.py);
  gear     data/gear30.json (content/spec_cheats.gear_rows, items with a required level 16–30); a spec whose own guide list had holes
           (items marked "pick", filled from other specs' lists) shows «no data yet» until the client dump of 05.11;
  dungeons the dungeon pages (content/dungeon_pages.py), their «Bosses in order» section has the tips by role.
data(lang, L, slugs) -> the P.card object of the page script (build_guides.play_data); tests/test_play_card.py checks it against the
sources and every link against the built pages."""
import re

import talents
from content import spec_cheats as SC
from content.class_guides import BETA_TRAINER

LANGS9 = ('ru', 'en', 'uk', 'de', 'fr', 'es', 'pt', 'it', 'pl')


def n9(*v):
    return dict(zip(LANGS9, v))


GEAR_LO, GEAR_HI = 16, 30                   # the required levels of data/gear30.json (16 the lowest, 30 the beta cap)

TX = {
    'head': n9('{c} на {n} уровне', '{c} at level {n}', '{c} на {n} рівні', '{c} auf Stufe {n}', '{c} au niveau {n}', '{c} en el nivel {n}',
               '{c} no nível {n}', '{c} al livello {n}', '{c} na poziomie {n}'),
    'tal': n9('Таланты', 'Talents', 'Таланти', 'Talente', 'Talents', 'Talentos', 'Talentos', 'Talenti', 'Talenty'),
    'talTo': n9('К {n} уровню', 'By level {n}', 'До {n} рівня', 'Bis Stufe {n}', 'Au niveau {n}', 'Hasta el nivel {n}', 'Até o nível {n}',
                'Fino al livello {n}', 'Do poziomu {n}'),
    'talFirst': n9('Первое очко талантов — на {n} уровне.', 'Your first talent point comes at level {n}.', 'Перше очко талантів — на {n} рівні.',
                   'Den ersten Talentpunkt gibt es auf Stufe {n}.', 'Le premier point de talent arrive au niveau {n}.',
                   'El primer punto de talento llega en el nivel {n}.', 'O primeiro ponto de talento vem no nível {n}.',
                   'Il primo punto talento arriva al livello {n}.', 'Pierwszy punkt talentu dostajesz na poziomie {n}.'),
    'next': n9('Дальше', 'Next', 'Далі', 'Als Nächstes', 'Ensuite', 'Después', 'Depois', 'Poi', 'Dalej'),
    'talWait': n9('Порядок после 30 уровня добавим после старта 05.11.', 'We will add the order after level 30 after the Nov 4–5 launch.',
                  'Порядок після 30 рівня додамо після старту 5 листопада.', 'Die Reihenfolge nach Stufe 30 ergänzen wir nach dem Start am 5. November.',
                  'L’ordre après le niveau 30 sera ajouté après le lancement du 5 novembre.',
                  'Añadiremos el orden después del nivel 30 tras el lanzamiento del 5 de noviembre.',
                  'Vamos adicionar a ordem depois do nível 30 após o lançamento em 5 de novembro.',
                  'Aggiungeremo l’ordine dopo il livello 30 dopo il lancio del 5 novembre.',
                  'Kolejność po 30 poziomie dodamy po starcie 5 listopada.'),
    'talAll': n9('Все таланты', 'All talents', 'Усі таланти', 'Alle Talente', 'Tous les talents', 'Todos los talentos', 'Todos os talentos',
                 'Tutti i talenti', 'Wszystkie talenty'),
    'ab': n9('Способности у тренера', 'Trainer abilities', 'Здібності в тренера', 'Fähigkeiten beim Lehrer', 'Compétences chez l’instructeur',
             'Habilidades del instructor', 'Habilidades do instrutor', 'Abilità dall’istruttore', 'Zdolności u trenera'),
    'abAll': n9('Все способности', 'All abilities', 'Усі здібності', 'Alle Fähigkeiten', 'Toutes les compétences', 'Todas las habilidades',
                'Todas as habilidades', 'Tutte le abilità', 'Wszystkie zdolności'),
    'gear': n9('Экипировка 16–30', 'Gear 16–30', 'Екіпірування 16–30', 'Ausrüstung 16–30', 'Équipement 16–30', 'Equipo 16–30',
               'Equipamento 16–30', 'Equipaggiamento 16–30', 'Ekwipunek 16–30'),
    'gearNow': n9('Можно надеть', 'Wearable now', 'Можна вдягнути', 'Jetzt tragbar', 'Portable maintenant', 'Puedes llevar ya', 'Já pode usar',
                  'Indossabile ora', 'Możesz założyć'),
    'gearSoon': n9('С {n} уровня', 'From level {n}', 'З {n} рівня', 'Ab Stufe {n}', 'Dès le niveau {n}', 'Desde el nivel {n}',
                   'A partir do nível {n}', 'Dal livello {n}', 'Od poziomu {n}'),
    'gearHole': n9('Данных пока нет: в гайдах беты список для этого спека неполный. Соберём его из клиента игры после 05.11.',
                   'No data yet: the beta guides give this spec an incomplete list. We will collect it from the game client after Nov 4–5.',
                   'Даних поки немає: у гайдах бети список для цього спеку неповний. Зберемо його з клієнта гри після 5 листопада.',
                   'Noch keine Daten: Die Beta-Guides haben für diese Skillung nur eine lückenhafte Liste. Wir lesen sie nach dem 5. November aus dem Spielclient aus.',
                   'Pas encore de données : les guides de la bêta donnent une liste incomplète pour cette spécialisation. Nous la tirerons du client du jeu après le 5 novembre.',
                   'Aún no hay datos: las guías de la beta dan una lista incompleta para esta especialización. La sacaremos del cliente del juego después del 5 de noviembre.',
                   'Ainda não há dados: os guias da beta trazem uma lista incompleta para esta especialização. Vamos tirá-la do cliente do jogo depois de 5 de novembro.',
                   'Ancora nessun dato: le guide della beta danno un elenco incompleto per questa specializzazione. Lo ricaveremo dal client del gioco dopo il 5 novembre.',
                   'Na razie brak danych: poradniki z bety mają dla tej specjalizacji niepełną listę. Zbierzemy ją z klienta gry po 5 listopada.'),
    'gearNone': n9('Предметов с уровнем до {n} в списке нет.', 'The list has no items up to level {n}.', 'Предметів із рівнем до {n} у списку немає.',
                   'Die Liste hat keine Gegenstände bis Stufe {n}.', 'La liste n’a aucun objet jusqu’au niveau {n}.', 'La lista no tiene objetos hasta el nivel {n}.',
                   'A lista não tem itens até o nível {n}.', 'L’elenco non ha oggetti fino al livello {n}.', 'Lista nie ma przedmiotów do poziomu {n}.'),
    'dg': n9('Подземелья', 'Dungeons', 'Підземелля', 'Dungeons', 'Donjons', 'Mazmorras', 'Masmorras', 'Spedizioni', 'Dungeony'),
    'role': n9('Ваша роль: {r}.', 'Your role: {r}.', 'Ваша роль: {r}.', 'Deine Rolle: {r}.', 'Votre rôle : {r}.', 'Tu rol: {r}.', 'Sua função: {r}.',
               'Il tuo ruolo: {r}.', 'Twoja rola: {r}.'),
    'dgTips': n9('Советы вашей роли на каждого босса:', 'Tips for your role on every boss:', 'Поради вашій ролі на кожного боса:',
                 'Tipps für deine Rolle bei jedem Boss:', 'Conseils pour votre rôle sur chaque boss :', 'Consejos para tu rol en cada jefe:',
                 'Dicas para sua função em cada chefe:', 'Consigli per il tuo ruolo su ogni boss:', 'Wskazówki dla twojej roli przy każdym bossie:'),
    'dgNone': n9('Страниц подземелий под этот уровень пока нет: подземелья — в списке ниже.',
                 'No dungeon pages for this level yet: the dungeons are in the list below.',
                 'Сторінок підземель під цей рівень поки немає: підземелля — у списку нижче.',
                 'Für diese Stufe gibt es noch keine Dungeon-Seiten: Die Dungeons stehen in der Liste unten.',
                 'Pas encore de pages de donjon pour ce niveau : les donjons sont dans la liste ci-dessous.',
                 'Aún no hay páginas de mazmorras para este nivel: las mazmorras están en la lista de abajo.',
                 'Ainda não há páginas de masmorras para este nível: as masmorras estão na lista abaixo.',
                 'Non ci sono ancora pagine di spedizioni per questo livello: le spedizioni sono nell’elenco qui sotto.',
                 'Na ten poziom nie ma jeszcze stron dungeonów: dungeony są na liście poniżej.'),
    'noSpec': n9('Выберите спек — покажем таланты и экипировку.', 'Pick a spec to see talents and gear.', 'Оберіть спек — покажемо таланти й екіпірування.',
                 'Wähle eine Skillung, um Talente und Ausrüstung zu sehen.', 'Choisissez une spécialisation pour voir les talents et l’équipement.',
                 'Elige una especialización para ver talentos y equipo.', 'Escolha uma especialização para ver talentos e equipamento.',
                 'Scegli una specializzazione per vedere talenti ed equipaggiamento.', 'Wybierz specjalizację, aby zobaczyć talenty i ekwipunek.'),
    'pickSpec': n9('Выбрать спек', 'Pick a spec', 'Обрати спек', 'Skillung wählen', 'Choisir la spécialisation', 'Elegir especialización',
                   'Escolher especialização', 'Scegli la specializzazione', 'Wybierz specjalizację'),
}


def _guide(guides, slug):
    return next((g for g in guides if g['slug'] == slug), None)


def abilities(guides, cid, L, lang):
    """[[level, what, why]] of the «Level / What to take» table of the class leveling guide."""
    g = _guide(guides, f'leveling-{cid}')
    sec = next(s for s in g['sections'] if s['id'] == 'abilities')
    tb = next(b for k, b in sec['blocks'] if k == 'table')
    return [[int(r[0]), L(r[1], lang), L(r[2], lang)] for r in tb['rows']]


def spec_rows(guides, cid, spec):
    """(talent cell, points) of the spec's talent table on guides/builds-<class>/ — the rows talents.render() draws the tree from."""
    from content.spec_builds import H_TAL
    g = _guide(guides, f'builds-{cid}')
    sec = next(s for s in g['sections'] if s['id'] == spec)
    tb = next(b for k, b in sec['blocks'] if k == 'table' and b['head'] is H_TAL)
    return [(r[0], r[1]) for r in tb['rows']]


def talent_steps(guides, cid, spec):
    """The order by level the builds page shows for the spec: (kind, steps, first level, perk ranks). kind 'lv' = the leveling build
    10–60 (tab #<spec>-leveling), 'gen' = the spec's own table (beta, the run to 30; a None talent is a «your pick» run)."""
    data = talents.load(cid)
    b = talents.leveling(cid, spec, data)
    if b:
        return 'lv', b['steps'], talents.FIRST_LEVEL, 0
    rows = spec_rows(guides, cid, spec)
    pk = talents.perk(data, rows)
    _, steps, _, _ = talents.plan(data, rows, talents.FIRST_LEVEL - pk)
    return 'gen', steps, talents.FIRST_LEVEL - pk, pk


def _src(src, lang, tr):
    """Where an item comes from, plain text: the dungeon (a drop or a dungeon quest), the quest, the profession, a world drop."""
    k = src.get('kind')
    if k == 'drop':
        return SC._name(src['dungeon'], lang) if src.get('dungeon') else SC.G_WORLD[lang] if src.get('zone_drop') or src.get('world') else ''
    if k == 'quest':
        if src.get('quest'):
            return f'{SC.G_QUEST[lang]}: {SC._name(src["quest"], lang)}'
        return SC._name(src['dungeon'], lang) if src.get('dungeon') else SC.G_QUEST[lang]
    if k == 'craft' and src.get('prof') in SC.G_PROF:
        return tr(SC.G_PROF[src['prof']], lang)
    return ''


def gear(key, lang, tr, items):
    """None when the spec's list had holes ("pick" items), else [[item id, faction, source]] for the items with a required level 16–30,
    in the order of the spec page's table; items[id] = [required level, slot, name, quality] is shared by all specs. The card shows the
    best item per slot up to the level, so of two items of one slot, level and faction only the first (table order) is kept."""
    rows = SC.gear_rows(key)
    if any(e.get('pick') for e, _ in rows):
        return None
    out, seen = [], set()
    for e, it in rows:
        lv = it.get('lvl') or 0
        if not GEAR_LO <= lv <= GEAR_HI:
            continue
        srcs = e.get('src') or []
        quests = [s for s in srcs if s['kind'] == 'quest']
        fac = (quests[0].get('faction') or '') if srcs and len(quests) == len(srcs) and len({s.get('faction') for s in quests}) == 1 else ''
        if (it['slot'], lv, fac) in seen:
            continue
        seen.add((it['slot'], lv, fac))
        where = ' · '.join(dict.fromkeys(x for x in (_src(s, lang, tr) for s in srcs) if x))
        items[str(e['id'])] = [lv, SC.GSLOT[it['slot']][lang], SC._name(it['names'], lang), int(it.get('q', 1))]
        out.append([int(e['id']), fac, where])
    return out


def data(lang, L, tr, guides, slugs, spec_ids, spec_roles, dungeon_links):
    """P.card: labels, per class the abilities and per spec the talents, gear and links; the dungeon pages by DUNGEONS index.
    Links are relative to the language home (HOME), anchors included; a page missing in this language: no link."""
    has = lambda s: s in slugs   # noqa: E731
    tx = {k: v[lang] for k, v in TX.items()}
    tx.update({'free': talents.UI['free'][lang], 'perk': talents.UI['perk'][lang], 'lvnote': talents.UI['lvnote'][lang],
               'beta': talents.UI['beta'][lang], 'gearBeta': SC.G_TEMP[lang], 'gearAll': SC.G_GO[lang], 'gearUp': SC.G_L60[lang],
               'abBeta': BETA_TRAINER[lang],
               'roles': {'tank': tr('Танк', lang), 'heal': tr('Лекарь', lang), 'dps': tr('Урон', lang)}})
    cls, items = {}, {}
    for cid, specs in spec_ids.items():
        c = {'ab': abilities(guides, cid, L, lang), 'abU': f'guides/leveling-{cid}/#abilities' if has(f'leveling-{cid}') else '', 'sp': {}}
        for i, spec in enumerate(specs):
            kind, steps, first, pk = talent_steps(guides, cid, spec)
            rank, st = {}, []
            for t, n, a, b in steps:
                if t is None:
                    st.append([a, b, '', n, 0, 0])
                    continue
                rank[t['id']] = rank.get(t['id'], 0) + n
                st.append([a, b, talents.tname(t, lang), n, rank[t['id']], t['m']])
            g = gear(f'{cid}-{spec}', lang, tr, items)
            c['sp'][spec] = {
                'k': kind, 'f': first, 'pk': pk, 'top': steps[-1][3] if steps else 0, 't': st,
                'r': spec_roles.get(cid, [[]] * 3)[i],
                'tU': (f'guides/builds-{cid}/#{spec}-leveling' if kind == 'lv' else f'guides/builds-{cid}/#{spec}') if has(f'builds-{cid}') else '',
                'g': g, 'gU': f'guides/spec-{cid}-{spec}/#gear' if has(f'spec-{cid}-{spec}') else '',
            }
        cls[cid] = c
    dg = {str(i): f'guides/dungeons/{s.rstrip("/")}/#bosses' for i, s in dungeon_links.items() if has(f'dungeons/{s.rstrip("/")}')}
    return {'tx': tx, 'cls': cls, 'it': items, 'dg': dg}


def spec_roles_of(src):
    """{class: [[roles of spec 1], …]} from the CLASSES of index.src.html (the same parse as build_guides.hero_json)."""
    roles = {}
    for m in re.finditer(r"\{ id:'(\w+)'[^\n]*\n\s*specs:\[(.*?)\],\n", src[src.index('const CLASSES = ['):src.index('const ROLE_RU')]):
        roles[m.group(1)] = [re.findall(r"'(tank|heal|dps)'", rs) for rs in re.findall(r"\['[^']*','[^']*',\[([^\]]*)\]\]", m.group(2))]
    return roles
