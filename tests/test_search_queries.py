"""Поиск по сайту на живых запросах: опечатки, название на чужом языке, сленг, вопросы новичка — на 9 языках.
Запрос верен, если нужная страница в первых трёх ответах. Движок — сам assets/search/search.js в node (tests/search_eval.js)
на собранном индексе. Запуск: python tests/test_search_queries.py [-v] [search.js [папка индекса]]  (-v: печатает и верные)
Ожидание: путь без языковой папки; 'x/' — страница x/ или её якорь (не глубже), 'x/#a' — ровно этот якорь, '' — главная."""
import json, os, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLASS = ['classes/', '#classes', 'tools/#picker', 'guides/tier-list/']           # «какой класс выбрать»: любой из выборов класса
START = ['guides/faq/#release', 'guides/faq/#dates']
PRICE = ['guides/faq/#price', 'guides/faq/#editions', 'guides/faq/#subscription']

Q = [
    # опечатки
    ('ru', 'палодин', ['classes/paladin/']), ('ru', 'чернокнижнек', ['classes/warlock/']), ('ru', 'друит', ['classes/druid/']),
    ('ru', 'разбийник', ['classes/rogue/']), ('ru', 'таурэн', ['races/tauren/']), ('ru', 'подземеля', ['guides/dungeons/']),
    ('ru', 'професии', ['guides/professions/']), ('ru', 'оргримар', ['races/orc/']), ('ru', 'шамаан', ['classes/shaman/']),
    ('en', 'wariror', ['classes/warrior/']), ('en', 'palladin', ['classes/paladin/']), ('en', 'warior', ['classes/warrior/']),
    ('en', 'orgrimar', ['races/orc/']), ('en', 'preist', ['classes/priest/']), ('en', 'rouge', ['classes/rogue/']),
    ('en', 'shamman', ['classes/shaman/']), ('en', 'proffesions', ['guides/professions/']), ('en', 'nigth elf', ['races/night-elf/']),
    ('en', 'warlok', ['classes/warlock/']),
    ('uk', 'чорнокнижнік', ['classes/warlock/']), ('uk', 'паладін', ['classes/paladin/']),
    ('de', 'kriger', ['classes/warrior/']), ('de', 'hexenmeiser', ['classes/warlock/']), ('fr', 'guerier', ['classes/warrior/']),
    ('fr', 'chasseurr', ['classes/hunter/']), ('es', 'guerero', ['classes/warrior/']), ('it', 'stregome', ['classes/warlock/']),
    ('pt', 'guereiro', ['classes/warrior/']), ('pl', 'wojownk', ['classes/warrior/']),
    # название на чужом языке и сленг
    ('ru', 'warrior', ['classes/warrior/']), ('ru', 'warlock', ['classes/warlock/']), ('ru', 'pally', ['classes/paladin/']),
    ('ru', 'mage', ['classes/mage/']), ('ru', 'night elf', ['races/night-elf/']), ('ru', 'rogue', ['classes/rogue/']),
    ('ru', 'хил', ['guides/tier-list/', '#classes', 'classes/priest/', 'classes/druid/', 'classes/shaman/', 'classes/paladin/']),
    ('ru', 'рога', ['classes/rogue/']), ('ru', 'лок', ['classes/warlock/']), ('ru', 'прист', ['classes/priest/']),
    ('ru', 'хант', ['classes/hunter/']), ('ru', 'шам', ['classes/shaman/']), ('ru', 'вар', ['classes/warrior/']),
    ('ru', 'данжи', ['guides/dungeons/']), ('ru', 'профы', ['guides/professions/']), ('ru', 'тирлист', ['guides/tier-list/']),
    ('ru', 'sfk', ['guides/dungeons/shadowfang-keep/', 'guides/dungeons/']), ('en', 'brd', ['guides/dungeons/']), ('de', 'brd', ['guides/dungeons/']),
    ('en', 'маг', ['classes/mage/']), ('en', 'воин', ['classes/warrior/']), ('en', 'ночной эльф', ['races/night-elf/']),
    ('en', 'pally', ['classes/paladin/']), ('en', 'lock', ['classes/warlock/']), ('en', 'tierlist', ['guides/tier-list/']),
    ('en', 'healer', ['guides/tier-list/', '#classes', 'classes/priest/', 'classes/druid/', 'classes/shaman/', 'classes/paladin/']),
    ('uk', 'warrior', ['classes/warrior/']), ('uk', 'воин', ['classes/warrior/']), ('uk', 'чернокнижник', ['classes/warlock/']),
    ('uk', 'хіл', ['guides/tier-list/', '#classes', 'classes/priest/', 'classes/druid/', 'classes/shaman/', 'classes/paladin/']),
    ('de', 'warrior', ['classes/warrior/']), ('de', 'rogue', ['classes/rogue/']), ('de', 'pally', ['classes/paladin/']),
    ('fr', 'warrior', ['classes/warrior/']), ('fr', 'rogue', ['classes/rogue/']), ('es', 'warlock', ['classes/warlock/']),
    ('es', 'rogue', ['classes/rogue/']), ('pt', 'priest', ['classes/priest/']), ('it', 'warlock', ['classes/warlock/']),
    ('pl', 'mage', ['classes/mage/']), ('pl', 'night elf', ['races/night-elf/']), ('de', 'маг', ['classes/mage/']),
    # вопросы новичка
    ('ru', 'какой класс выбрать', CLASS), ('ru', 'лучший класс для новичка', CLASS), ('ru', 'за кого играть', CLASS),
    ('ru', 'когда старт', START), ('ru', 'когда выйдет', START), ('ru', 'дата выхода', START),
    ('ru', 'есть ли русский язык', ['guides/faq/#language', 'guides/faq/#servers']), ('ru', 'лучшая раса для мага', ['guides/best-race/']),
    ('ru', 'подземелья 20 уровень', ['guides/dungeons/']), ('ru', 'сколько стоит', PRICE), ('ru', 'цена', PRICE),
    ('ru', 'как быстро качаться', ['guides/leveling/']), ('ru', 'когда рейды', ['guides/faq/#raids']),
    ('ru', 'какой максимальный уровень', ['guides/faq/#levels']),
    ('en', 'which class to choose', CLASS), ('en', 'best class for beginners', CLASS), ('en', 'what class should i play', CLASS),
    ('en', 'when does it start', START), ('en', 'release date', START), ('en', 'russian language', ['guides/faq/#servers']),
    ('en', 'best race for mage', ['guides/best-race/']), ('en', 'how much does it cost', PRICE),
    ('en', 'system requirements', ['guides/requirements/', 'guides/faq/#requirements']), ('en', 'how to level fast', ['guides/leveling/']),
    ('uk', 'який клас обрати', CLASS), ('uk', 'коли старт', START), ('uk', 'українська мова', ['guides/ukrainian/', 'guides/faq/#language']),
    ('uk', 'найкраща раса', ['guides/best-race/']),
    ('de', 'welche klasse soll ich spielen', CLASS), ('de', 'wann ist release', START), ('de', 'beste rasse', ['guides/best-race/']),
    ('de', 'was kostet', PRICE),
    ('fr', 'quelle classe choisir', CLASS), ('fr', 'date de sortie', START), ('fr', 'meilleure race', ['guides/best-race/']),
    ('es', 'que clase elegir', CLASS), ('es', 'fecha de lanzamiento', START), ('es', 'mejor raza', ['guides/best-race/']),
    ('pt', 'qual classe escolher', CLASS), ('pt', 'data de lançamento', START),
    ('it', 'quale classe scegliere', CLASS), ('it', 'data di uscita', START),
    ('pl', 'jaką klasę wybrać', CLASS), ('pl', 'data premiery', START),
]
# отложенный набор: написан после настройки словарей и под него не подгонялся; плюс то, что работало и до правок
RAID = ['guides/dungeons/', 'guides/faq/#raids']
SKY = ['races/skyborne-alliance/', 'races/skyborne-horde/', 'guides/faq/#skyborne']
HOLD = [
    ('ru', 'жрец', ['classes/priest/']), ('ru', 'паладин танк', ['classes/paladin/']), ('ru', 'варлак', ['classes/warlock/']),
    ('ru', 'охотнек', ['classes/hunter/']), ('ru', 'shadowfang keep', ['guides/dungeons/shadowfang-keep/', 'guides/dungeons/']), ('ru', 'крепость темного клыка', ['guides/dungeons/shadowfang-keep/', 'guides/dungeons/']),
    ('ru', 'рейд', RAID), ('ru', 'аддоны', ['guides/addons/']), ('ru', 'тир лист', ['guides/tier-list/']),
    ('ru', 'русский язык', ['guides/faq/#language']), ('ru', 'скайборн', SKY), ('ru', 'skyborne', SKY), ('ru', 'hunter', ['classes/hunter/']),
    ('ru', 'undead', ['races/undead/']), ('ru', 'gnome', ['races/gnome/']), ('ru', 'нужна ли подписка', ['guides/faq/#subscription']),
    ('ru', 'как занять имя', ['guides/faq/#reserve', 'guides/name-reservation/']), ('ru', 'требования к пк', ['guides/requirements/', 'guides/faq/#requirements']),
    ('ru', 'когда откроются рейды', ['guides/faq/#raids']), ('ru', 'палладин', ['classes/paladin/']), ('ru', 'прокачка мага', ['guides/leveling-mage/']),
    ('ru', 'билд воина', ['guides/builds-warrior/']), ('ru', 'билды паладина', ['guides/builds-paladin/']), ('ru', 'профессии', ['guides/professions/']),
    ('ru', 'цена', PRICE), ('ru', 'какой класс выбрать', CLASS),
    ('en', 'priest', ['classes/priest/']), ('en', 'paladin tank', ['classes/paladin/']), ('en', 'huntr', ['classes/hunter/']),
    ('en', 'druide', ['classes/druid/']), ('en', 'mage leveling', ['guides/leveling-mage/']), ('en', 'warrior build', ['guides/builds-warrior/']),
    ('en', 'addons', ['guides/addons/']), ('en', 'raid', RAID), ('en', 'subscription', ['guides/faq/#subscription']),
    ('en', 'free trial', ['guides/faq/#trial']), ('en', 'жрец', ['classes/priest/']), ('en', 'orc', ['races/orc/']),
    ('en', 'undaed', ['races/undead/']), ('en', 'deadmines', ['guides/dungeons/the-deadmines/', 'guides/dungeons/']), ('en', 'skyborne', SKY),
    ('en', 'reserve name', ['guides/faq/#reserve']), ('en', 'tier list', ['guides/tier-list/']), ('en', 'professions', ['guides/professions/']),
    ('en', 'price', PRICE),
    ('uk', 'мисливець', ['classes/hunter/']), ('uk', 'охотник', ['classes/hunter/']), ('uk', 'розбійнік', ['classes/rogue/']),
    ('uk', 'прокачування', ['guides/leveling/']), ('uk', 'рейди', RAID),
    ('de', 'jäger', ['classes/hunter/']), ('de', 'jager', ['classes/hunter/']), ('de', 'schurke', ['classes/rogue/']),
    ('de', 'hunter', ['classes/hunter/']), ('de', 'krieger leveln', ['guides/leveling-warrior/']), ('de', 'magier', ['classes/mage/']),
    ('de', 'priest', ['classes/priest/']), ('de', 'nachtelf', ['races/night-elf/']), ('de', 'night elf', ['races/night-elf/']),
    ('de', 'untoter', ['races/undead/']),
    ('fr', 'voleur', ['classes/rogue/']), ('fr', 'priest', ['classes/priest/']), ('fr', 'demoniste', ['classes/warlock/']),
    ('fr', 'warlock', ['classes/warlock/']), ('fr', 'elfe de la nuit', ['races/night-elf/']),
    ('es', 'picaro', ['classes/rogue/']), ('es', 'warrior', ['classes/warrior/']), ('es', 'chaman', ['classes/shaman/']),
    ('es', 'brujo', ['classes/warlock/']), ('es', 'sacerdote', ['classes/priest/']),
    ('pt', 'ladino', ['classes/rogue/']), ('pt', 'warrior', ['classes/warrior/']), ('pt', 'bruxo', ['classes/warlock/']), ('pt', 'xama', ['classes/shaman/']),
    ('it', 'ladro', ['classes/rogue/']), ('it', 'rogue', ['classes/rogue/']), ('it', 'sciamano', ['classes/shaman/']),
    ('it', 'warrior', ['classes/warrior/']), ('it', 'sacerdote', ['classes/priest/']),
    ('pl', 'kapłan', ['classes/priest/']), ('pl', 'łowca', ['classes/hunter/']), ('pl', 'czarnoksiężnik', ['classes/warlock/']),
    ('pl', 'warrior', ['classes/warrior/']), ('pl', 'krasnolud', ['races/dwarf/']),
]
LV = lambda c: [f'guides/leveling-{c}/']
BD = lambda c: [f'guides/builds-{c}/']
# третий набор (после проверки директора): связки «гайд + класс», транслит, английские слова кириллицей, опечатки в
# начале и середине, падежи; придуман до правок движка и замерен ДО/ПОСЛЕ. DIR — пять провалов из его проверки.
NEW = [
    # класс + гайд
    ('ru', 'билд на жреца', BD('priest')), ('ru', 'как качать охотника', LV('hunter')),
    ('ru', 'таланты разбойника', BD('rogue') + LV('rogue')), ('en', 'how to level a priest', LV('priest')),
    ('en', 'druid talents', BD('druid') + LV('druid')), ('de', 'schamane leveln', LV('shaman')),
    ('uk', 'білд воїна', BD('warrior')), ('uk', 'як прокачати чорнокнижника', LV('warlock')),
    ('ru', 'билды шамана', BD('shaman')), ('uk', 'таланти жерця', BD('priest') + LV('priest')),
    # транслит латиницей
    ('ru', 'okhotnik', ['classes/hunter/']), ('ru', 'razboinik', ['classes/rogue/']), ('ru', 'chernoknizhnik', ['classes/warlock/']),
    ('ru', 'prokachka maga', LV('mage')), ('ru', 'podzemelya', ['guides/dungeons/']), ('uk', 'myslyvets', ['classes/hunter/']),
    # английские слова кириллицей
    ('ru', 'ретрибушен', ['classes/paladin/'] + BD('paladin')), ('ru', 'протекшн воин', ['classes/warrior/'] + BD('warrior')),
    ('ru', 'энхансер', ['classes/shaman/'] + BD('shaman')), ('ru', 'хардкор', ['guides/legacy/', 'guides/faq/#modes']),
    ('en', 'аддоны', ['guides/addons/']),
    # опечатки в начале и середине
    ('ru', 'кожевнечество', ['guides/professions/']), ('ru', 'шоман', ['classes/shaman/']), ('ru', 'чирнокнижник', ['classes/warlock/']),
    ('en', 'enchnting', ['guides/professions/']), ('en', 'tailorng', ['guides/professions/']), ('de', 'schamanne', ['classes/shaman/']),
    ('ru', 'ночьной эльф', ['races/night-elf/']),
    # падежи
    ('uk', 'раса для мага', ['guides/best-race/', 'classes/mage/#races']), ('ru', 'подземелья для 30 уровня', ['guides/dungeons/']),
]
DIR = [  # провалы из проверки директора
    ('ru', 'как прокачать вара', LV('warrior')), ('ru', 'kak prokachat shamana', LV('shaman')),
    ('ru', 'алхемия', ['guides/professions/']), ('ru', 'что такое легаси', ['guides/legacy/']), ('uk', 'прокачка мисливця', LV('hunter')),
    # PvP (подсказки поиска 29.10: «wow forever pvp», «pvp system», «pvp gear», «pvp ranking»)
    ('en', 'wow forever pvp', ['guides/pvp/']), ('en', 'pvp gear', ['guides/pvp/']), ('en', 'pvp ranking', ['guides/pvp/']),
    ('ru', 'пвп', ['guides/pvp/']), ('ru', 'звания pvp', ['guides/pvp/']), ('uk', 'честь pvp', ['guides/pvp/']),
    ('de', 'pvp ehre', ['guides/pvp/']), ('pl', 'pvp honor', ['guides/pvp/']),
]
# слепой набор: написан после всех правок и замерен один раз, под него не подгонялось
BLIND = [
    ('ru', 'прокачка разбойника', LV('rogue')), ('ru', 'какие таланты взять магу', BD('mage') + LV('mage')),
    ('ru', 'кузнечное дело', ['guides/professions/']), ('ru', 'gnomeregan', ['guides/dungeons/']),
    ('ru', 'glubiny chernoi gory', ['guides/dungeons/']), ('ru', 'druid tank', ['classes/druid/'] + BD('druid')),
    ('ru', 'фрост маг', ['classes/mage/'] + BD('mage')), ('ru', 'скока стоит подписка', PRICE),
    ('ru', 'когда выходит игра', START), ('ru', 'травнечество', ['guides/professions/']),
    ('uk', 'прокачка шамана', LV('shaman')), ('uk', 'білди друїда', BD('druid')), ('uk', 'koly start', START),
    ('en', 'best race for warlock', ['guides/best-race/']), ('en', 'hunter pet', ['classes/hunter/'] + LV('hunter')),
    ('en', 'preist build', BD('priest')), ('de', 'beste klasse für anfänger', CLASS),
    ('fr', 'monter de niveau chasseur', LV('hunter')), ('es', 'talentos de brujo', BD('warlock') + LV('warlock')),
    ('pl', 'jak levelowac maga', LV('mage')), ('it', 'talenti sacerdote', BD('priest') + LV('priest')),
    ('pt', 'melhor raça para mago', ['guides/best-race/', 'classes/mage/#races']),
]
# второй слепой набор (после проверки 26.10: сленг классов в любом порядке, название игры как шум, «список» подземелий);
# написан до правок и замерен один раз после них
DUNG = ['guides/dungeons/']
BLIND2 = [
    ('ru', 'шам как прокачать', LV('shaman')), ('ru', 'дру танк', ['classes/druid/'] + BD('druid')), ('ru', 'хант билд', BD('hunter')),
    ('ru', 'лок соло', ['classes/warlock/'] + LV('warlock')), ('ru', 'дата выхода вов', START), ('ru', 'wow forever когда старт', START),
    ('ru', 'сколько стоит вов форевер', PRICE), ('ru', 'список подземелий', DUNG), ('ru', 'пал хил', ['classes/paladin/'] + BD('paladin')),
    ('ru', 'шп', ['classes/priest/'] + BD('priest')), ('en', 'raid list', DUNG + ['guides/faq/#raids']),
    ('en', 'wow forever release date', START), ('en', 'lock leveling', LV('warlock')), ('en', 'sham build', BD('shaman')),
    ('uk', 'вар прокачка', LV('warrior')), ('uk', 'коли реліз wow forever', START), ('de', 'dungeon liste', DUNG),
    ('de', 'pala build', BD('paladin')), ('fr', 'liste des donjons', DUNG), ('es', 'lista de mazmorras', DUNG),
]
# спеки на слух и сокращениями («протекшн воин», «прот вар», «холи пал»): страница класса или его билдов (якорь спека — лучше, но не обязателен)
def SP(c, a):
    return [f'classes/{c}/', f'guides/builds-{c}/', f'guides/builds-{c}/#{a}']
SPEC = [
    ('ru', 'протекшн воин', SP('warrior', 'protection')), ('ru', 'протекшн вар', SP('warrior', 'protection')),
    ('ru', 'прот вар', SP('warrior', 'protection')), ('ru', 'прот воин', SP('warrior', 'protection')),
    ('ru', 'протекшн', BD('warrior') + BD('paladin')), ('ru', 'протекшн паладин', SP('paladin', 'protection')),
    ('ru', 'прот пал', SP('paladin', 'protection')), ('ru', 'фури вар', SP('warrior', 'fury')), ('ru', 'арм вар', SP('warrior', 'arms')),
    ('ru', 'холи пал', SP('paladin', 'holy')), ('ru', 'ретрик', SP('paladin', 'retribution')), ('ru', 'рет пал', SP('paladin', 'retribution')),
    ('ru', 'диско прист', SP('priest', 'discipline')), ('ru', 'шадоу прист', SP('priest', 'shadow')),
    ('ru', 'ресто друид', SP('druid', 'restoration')), ('ru', 'ресто шам', SP('shaman', 'restoration')), ('ru', 'фери друид', SP('druid', 'feral')),
    ('ru', 'энх шам', SP('shaman', 'enhancement')), ('ru', 'элем шам', SP('shaman', 'elemental')),
    ('ru', 'бм хант', SP('hunter', 'beast-mastery')), ('ru', 'сурв хант', SP('hunter', 'survival')),
    ('ru', 'афлик лок', SP('warlock', 'affliction')), ('ru', 'дестро лок', SP('warlock', 'destruction')),
    ('ru', 'фаер маг', SP('mage', 'fire')), ('ru', 'комбат рога', SP('rogue', 'combat')),
    ('en', 'prot warrior', SP('warrior', 'protection')), ('en', 'prot war', SP('warrior', 'protection')), ('en', 'prot pal', SP('paladin', 'protection')),
    ('en', 'holy pal', SP('paladin', 'holy')), ('en', 'ret pal', SP('paladin', 'retribution')), ('en', 'disc priest', SP('priest', 'discipline')),
    ('uk', 'протекшн вар', SP('warrior', 'protection')), ('uk', 'прот воїн', SP('warrior', 'protection')), ('uk', 'холі пал', SP('paladin', 'holy')),
    ('de', 'prot krieger', SP('warrior', 'protection')), ('es', 'prot guerrero', SP('warrior', 'protection')),
]
DIR2 = [('ru', 'вор как качать', LV('rogue')), ('ru', 'когда релиз вов форевер', START), ('en', 'dungeon list', DUNG)]
# экипировка (разбор ясности 02.11, п.3): «что надеть», «шмот», «бис» -> блок «Экипировка 13–30» страницы спека; с классом — спека
# этого класса; «таланты мага» -> билд мага, а не калькулятор (п.2) — тут нужное должно быть ПЕРВЫМ (FIRST)
SPECS_ALL = sorted(d for d in os.listdir(os.path.join(ROOT, 'guides')) if d.startswith('spec-'))
# без класса годится и сборщик экипировки character/gear/ (04.11): он открывается под уровень и спек читателя
GEAR = lambda c='': [f'guides/{d}/#gear' for d in SPECS_ALL if d.startswith(f'spec-{c}')] + ([] if c else ['character/gear/'])
GEARQ = [
    ('ru', 'экипировка', GEAR()), ('ru', 'что надеть', GEAR()), ('ru', 'шмот', GEAR()), ('ru', 'бис', GEAR()),
    ('ru', 'экипировка мага', GEAR('mage')), ('ru', 'что надеть воину', GEAR('warrior')), ('ru', 'шмот на шамана', GEAR('shaman')),
    ('ru', 'бис рога', GEAR('rogue')), ('ru', 'таланты мага', BD('mage')),
    ('uk', 'екіпірування', GEAR()), ('uk', 'що вдягнути', GEAR()), ('uk', 'екіпіровка мага', GEAR('mage')), ('uk', 'таланти мага', BD('mage')),
    ('en', 'gear', GEAR()), ('en', 'what to wear', GEAR()), ('en', 'bis', GEAR()), ('en', 'mage gear', GEAR('mage')),
    ('en', 'best in slot warrior', GEAR('warrior')), ('en', 'mage talents', BD('mage')),
    ('de', 'ausrüstung', GEAR()), ('de', 'was anziehen', GEAR()), ('de', 'magier ausrüstung', GEAR('mage')), ('de', 'magier talente', BD('mage')),
    ('fr', 'équipement', GEAR()), ('fr', 'équipement mage', GEAR('mage')), ('es', 'equipo mago', GEAR('mage')),
    ('pt', 'equipamento', GEAR()), ('it', 'equipaggiamento', GEAR()), ('pl', 'ekwipunek', GEAR()), ('pl', 'mage talenty', BD('mage')),
]
KNOWN = set()   # запросы, которые пока не находят нужное: {(lang, query)}


def ok(url, lang, want):
    pre = '' if lang == 'ru' else lang + '/'
    rel = url[len(pre):] if url.startswith(pre) else url
    page, _, anchor = rel.partition('#')
    for w in want:
        wp, _, wa = w.partition('#')
        if page == wp and (not wa or anchor == wa):
            return True
    return False


def run(js=os.path.join(ROOT, 'assets', 'search', 'engine.js'), index=os.path.join(ROOT, 'assets', 'search')):
    node = shutil.which('node')
    if not node:
        print('SKIP: нет node')
        sys.exit(0)
    r = subprocess.run([node, os.path.join(ROOT, 'tests', 'search_eval.js'), js, index],
                       input=json.dumps([[l, q] for l, q, _ in Q + HOLD + NEW + DIR + BLIND + BLIND2 + DIR2 + SPEC + GEARQ]), capture_output=True, text=True, encoding='utf-8', check=True)
    return json.loads(r.stdout)


if __name__ == '__main__':
    res = run(*[a for a in sys.argv[1:] if not a.startswith('-')])   # [search.js [index dir]]: another engine, e.g. the old one
    sets = [('набор', Q), ('отложенный', HOLD), ('новый', NEW), ('директор', DIR), ('слепой', BLIND), ('слепой-2', BLIND2), ('директор-2', DIR2), ('спеки', SPEC), ('экипировка', GEARQ)]
    allq = [q for _, qs in sets for q in qs]
    good, bad, first = [], [], 0
    for (lang, q, want), urls in zip(allq, res):
        top = urls[:1] if (lang, q, want) in GEARQ else urls[:3]   # the gear set: the answer first
        (good if any(ok(u, lang, want) for u in top) else bad).append((lang, q, urls[:3]))
        first += bool(urls) and ok(urls[0], lang, want)
    if '-v' in sys.argv:
        for x in good:
            print('+', *x)
    for x in bad:
        print('-', *x)
    new = [b for b in bad if b[:2] not in KNOWN]
    keys = [(l, q) for l, q, _ in allq]
    per, at = [], 0
    for name, qs in sets:
        n = sum((l, q) in {g[:2] for g in good} for l, q, _ in qs)
        per.append(f'{name} {n}/{len(qs)}')
    print(', '.join(per) + f'; всего {len(good)}/{len(allq)} ({100 * len(good) // len(allq)}%), первым {first}')
    assert not new, f'не нашлось: {len(new)}'
