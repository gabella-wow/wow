"""Тир-лист: «по бете» или «по живой игре» и дата данных — один переключатель в data/tierlist.json.
Отсюда берут текст, зависящий от статуса: title и description (seo.META), хвост лида, строка фактов первого экрана,
совет в «Как читать», подпись плитки и блок «Что изменилось» (нет заметок — нет блока).
Тексты со статусом и датой заданы здесь на всех 9 языках; тексты беты без даты остаются прежними строками
(их переводы уже в i18n/<lang>.json). Тестовая копия данных: переменная WF_TIERLIST=<путь к json>.
Порядок обновления после старта: docs/wow/TIERLIST-LIVE-RUNBOOK.md."""
import datetime, json, os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.environ.get('WF_TIERLIST') or os.path.join(HERE, 'data', 'tierlist.json')
ALL = ('ru', 'en', 'uk', 'de', 'fr', 'es', 'pt', 'it', 'pl')
SOURCES = ('beta', 'live')
MONTHS_EN = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')


def t(ru, en, uk):
    return {'ru': ru, 'en': en, 'uk': uk}


def load(path=None):
    with open(path or PATH, encoding='utf-8') as f:
        st = json.load(f)
    assert st['source'] in SOURCES, st['source']
    datetime.date.fromisoformat(st['date'])
    for c in st.get('changes', []):
        datetime.date.fromisoformat(c['date'])
        assert all((c['text'].get(l) or '').strip() for l in ALL), ('a change note needs all 9 languages', c)
    return st


def day(iso, lang):
    """'2026-11-06' -> the short date of the language: Nov 6 (en), 06.11. (de), 06.11 (the rest, as on the site)."""
    d = datetime.date.fromisoformat(iso)
    if lang == 'en':
        return f'{MONTHS_EN[d.month - 1]} {d.day}'
    return d.strftime('%d.%m') + ('.' if lang == 'de' else '')


# ---------- texts with the status and the date: all 9 languages ----------
# title ≤60 with the longest date (tests/test_tierlist_live.py); {m} the short mark, {d} the date
TITLE = {'ru': 'Тир-лист WoW Forever: PvE, PvP, прокачка ({m}, {d})',
         'en': 'WoW Forever Tier List: PvE, PvP, Leveling ({m}, {d})',
         'uk': 'Тір-лист WoW Forever: PvE, PvP, прокачка ({m}, {d})',
         'de': 'Tierliste WoW Forever: PvE, PvP, Leveln ({m}, {d})',
         'fr': 'Tier list WoW Forever : JcE, JcJ, progression ({m}, {d})',
         'es': 'Tier list WoW Forever: JcE, JcJ, subida ({m}, {d})',
         'pt': 'Tier list WoW Forever: PvE, PvP, evolução ({m}, {d})',
         'it': 'Tier list WoW Forever: PvE, PvP, leveling ({m}, {d})',
         'pl': 'Tier list WoW Forever: PvE, PvP, levelowanie ({m}, {d})'}
SHORT = {'beta': {'ru': 'бета', 'en': 'Beta', 'uk': 'бета', 'de': 'Beta', 'fr': 'bêta', 'es': 'beta', 'pt': 'beta', 'it': 'beta', 'pl': 'beta'},
         'live': {'ru': 'живая игра', 'en': 'Live', 'uk': 'жива гра', 'de': 'Live', 'fr': 'live', 'es': 'en vivo', 'pt': 'ao vivo', 'it': 'live', 'pl': 'live'}}
# the first item of the facts line under the lead
MARK = {'beta': {'ru': 'По бете, {d}', 'en': 'Beta data, {d}', 'uk': 'За бетою, {d}', 'de': 'Beta-Daten, {d}',
                 'fr': 'D’après la bêta, {d}', 'es': 'Datos de la beta, {d}', 'pt': 'Dados do beta, {d}',
                 'it': 'Dati della beta, {d}', 'pl': 'Dane z bety, {d}'},
        'live': {'ru': 'По живой игре, {d}', 'en': 'Live game data, {d}', 'uk': 'За живою грою, {d}', 'de': 'Live-Daten, {d}',
                 'fr': 'D’après le jeu en live, {d}', 'es': 'Datos del juego en vivo, {d}', 'pt': 'Dados do jogo ao vivo, {d}',
                 'it': 'Dati del gioco live, {d}', 'pl': 'Dane z gry na żywo, {d}'}}
# the last sentence of the lead in the live game (the beta one is the old sentence, LEAD_TAIL_BETA)
LEAD_TAIL_LIVE = {'ru': 'Срез живой игры на {d}.', 'en': 'A live game snapshot as of {d}.', 'uk': 'Зріз живої гри на {d}.',
                  'de': 'Stand der Live-Version: {d}', 'fr': 'Instantané du jeu en live au {d}.', 'es': 'Instantánea del juego en vivo al {d}.',
                  'pt': 'Retrato do jogo ao vivo em {d}.', 'it': 'Istantanea del gioco live al {d}.', 'pl': 'Stan gry na żywo z {d}.'}
DESC_LIVE = {'ru': 'Тир-лист WoW Forever по живой игре на {d}: лучшие классы и спеки для PvE, PvP и прокачки и что изменилось с беты.',
             'en': 'WoW Forever tier list from the live game as of {d}: best classes and specs for PvE, PvP and leveling, and what changed since the beta.',
             'uk': 'Тір-лист WoW Forever за живою грою на {d}: найкращі класи й спеціалізації для PvE, PvP і прокачування та що змінилося після бети.',
             'de': 'Tierliste für WoW Forever nach der Live-Version, Stand {d}: beste Klassen und Specs für PvE, PvP und Leveln, was sich seit der Beta änderte.',
             'fr': 'Tier list WoW Forever d’après le jeu en live au {d} : meilleures classes et spés en JcE, JcJ et progression, et ce qui a changé depuis la bêta.',
             'es': 'Tier list de WoW Forever según el juego en vivo al {d}: mejores clases y especializaciones para JcE, JcJ y subida, y qué cambió desde la beta.',
             'pt': 'Tier list do WoW Forever segundo o jogo ao vivo em {d}: melhores classes e especializações para PvE, PvP e evolução, e o que mudou desde o beta.',
             'it': 'Tier list di WoW Forever dal gioco live al {d}: migliori classi e specializzazioni per PvE, PvP e livellamento, e cosa è cambiato dalla beta.',
             'pl': 'Tier list WoW Forever według gry na żywo z {d}: najlepsze klasy i speki do PvE, PvP i levelowania oraz co zmieniło się od bety.'}
TIP_LIVE = {'ru': 'По живой игре, {d}: оценки источников после старта 5 ноября. Рейды откроются 09.12, их оценок пока нет.',
            'en': 'Live game data, {d}: source ratings after the Nov 4–5 launch. Raids open on Dec 9; there are no raid ratings yet.',
            'uk': 'За живою грою, {d}: оцінки джерел після старту 5 листопада. Рейди відкриються 9 грудня, їхніх оцінок поки немає.',
            'de': 'Live-Daten, {d}: Bewertungen der Quellen nach dem Start am 5. November. Raids öffnen am 09.12., Raid-Bewertungen gibt es noch nicht.',
            'fr': 'D’après le jeu en live, {d} : notes des sources après le lancement du 5 novembre. Les raids ouvrent le 09.12 ; pas encore de notes de raid.',
            'es': 'Datos del juego en vivo, {d}: valoraciones de las fuentes tras el lanzamiento del 5 de noviembre. Las bandas abren el 09.12; aún no hay valoraciones.',
            'pt': 'Dados do jogo ao vivo, {d}: avaliações das fontes após o lançamento de 5 de novembro. As raides abrem em 09.12; ainda não há avaliações de raide.',
            'it': 'Dati del gioco live, {d}: valutazioni delle fonti dopo il lancio del 5 novembre. I raid aprono il 09.12; non ci sono ancora valutazioni dei raid.',
            'pl': 'Dane z gry na żywo, {d}: oceny źródeł po starcie 5 listopada. Raidy ruszają 09.12, ocen raidów jeszcze nie ma.'}
TILE_LIVE = {'ru': 'Сильные классы и спеки по живой игре', 'en': 'Strong classes and specs from the live game',
             'uk': 'Сильні класи й спеціалізації за живою грою', 'de': 'Starke Klassen und Spezialisierungen nach Live-Daten',
             'fr': 'Les classes et spécialisations fortes d’après le jeu en live', 'es': 'Clases y especializaciones fuertes según el juego en vivo',
             'pt': 'Classes e especializações fortes segundo o jogo ao vivo', 'it': 'Classi e specializzazioni forti secondo il gioco live',
             'pl': 'Mocne klasy i specjalizacje według gry na żywo'}
CHANGES_H = {'ru': 'Что изменилось', 'en': 'What changed', 'uk': 'Що змінилося', 'de': 'Was sich geändert hat', 'fr': 'Ce qui a changé',
             'es': 'Qué ha cambiado', 'pt': 'O que mudou', 'it': 'Cosa è cambiato', 'pl': 'Co się zmieniło'}

# ---------- beta texts without a date: the old strings, translated by i18n/<lang>.json ----------
LEAD_TAIL_BETA = t('Это срез беты 30 уровня, обновим после старта 5 ноября.',
                   'This is a level 30 beta snapshot; we’ll update it after the Nov 4–5 launch.',
                   'Це зріз бети на 30 рівні, оновимо його після старту 5 листопада.')
DESC_BETA = t('Тир-лист WoW Forever: лучшие классы и спеки для PvE, PvP и прокачки по бете 30 уровня. Обновим после старта.',
              'WoW Forever tier list: best classes and specs for PvE, PvP and leveling from the level 30 beta. Updated after launch.',
              'Тір-лист WoW Forever: найкращі класи й спеціалізації для PvE, PvP і прокачування за бетою 30 рівня. Оновимо після старту.')
TIP_BETA = t('По бете. Бета шла с 17.09 по 23.10 на уровне 30: рейдов, полей боя и уровней 31–60 там не было. Обновим после старта 5 ноября.',
             'Beta data. The beta ran from Sep 17 to Oct 23 at level 30: no raids, battlegrounds or levels 31–60. We’ll update after the Nov 4–5 launch.',
             'За бетою. Бета тривала з 17 вересня по 23 жовтня на 30 рівні: рейдів, полів бою та рівнів 31–60 там не було. Оновимо після старту 5 листопада.')
TILE_BETA = t('Сильные классы и спеки по данным беты', 'Strong classes and specs by beta data', 'Сильні класи й спеціалізації за даними бети')
AFTER_BETA = t('Обновим после 05.11', 'Updated after Nov 4–5', 'Оновимо після 5 листопада')


def fmt(d9, iso):
    return {l: d9[l].format(d=day(iso, l)) for l in ALL}


def title(st=None):
    st = st or load()
    return {l: TITLE[l].format(m=SHORT[st['source']][l], d=day(st['date'], l)) for l in ALL}


def meta(st=None):
    """seo.META['guides/tier-list/']: (title, description)."""
    st = st or load()
    return title(st), (fmt(DESC_LIVE, st['date']) if st['source'] == 'live' else dict(DESC_BETA))


def lead(head, st=None):
    """The lead: the content sentences (head, ru/en/uk) + the status sentence. Beta: the old whole string (its translations
    are in i18n/<lang>.json). Live: all 9 languages, head's new languages by its English text (langs.ov: a missing one fails the build)."""
    st = st or load()
    if st['source'] == 'beta':
        return {l: head[l] + ' ' + LEAD_TAIL_BETA[l] for l in ('ru', 'en', 'uk')}
    import langs
    tail = fmt(LEAD_TAIL_LIVE, st['date'])
    return {l: (head[l] if l in head else langs.ov(head['en'], l)) + ' ' + tail[l] for l in ALL}


def pills(specs, st=None):
    st = st or load()
    return [fmt(MARK[st['source']], st['date']), specs] + ([dict(AFTER_BETA)] if st['source'] == 'beta' else [])


def tip(st=None):
    st = st or load()
    return fmt(TIP_LIVE, st['date']) if st['source'] == 'live' else dict(TIP_BETA)


def tile(st=None):
    st = st or load()
    return dict(TILE_LIVE) if st['source'] == 'live' else dict(TILE_BETA)


def changes_section(st=None):
    """«Что изменилось»: one line per note, newest first; None when there are no notes (no block, no contents entry)."""
    st = st or load()
    notes = sorted(st.get('changes', []), key=lambda c: c['date'], reverse=True)
    if not notes:
        return None
    from html import escape
    html = {l: '<ul class="tlchg">' + ''.join(f'<li><time datetime="{c["date"]}">{day(c["date"], l)}</time> {escape(c["text"][l])}</li>' for c in notes) + '</ul>'
            for l in ALL}
    return {'id': 'changes', 'title': dict(CHANGES_H), 'blocks': [('raw', html)]}
