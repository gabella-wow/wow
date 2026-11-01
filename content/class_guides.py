"""Гайды «Прокачка <класса> 1–60»: девять страниц guides/leveling-<класс>/.
Строка = t(ru, en, uk); de, es, fr, it, pl, pt берутся из i18n/<lang>.json по английской строке.
tx(ru, en, uk, de=…) — то же, но с явным переводом для языков, где английская строка в json значит другое
(например «Kick» — исключить игрока, а здесь заклинание Разбойника).
Таблица, где ячейка одинакова во всех языках (уровни, очки, названия Forever без перевода), хранит её простой строкой.
Названия способностей и талантов: ru — как в клиенте ruRU, de/es/fr/it/pt — из i18n/names.json, en/uk/pl — английские.
Источник текстов: docs/wow/specs/texts-2026-10-26-class-leveling (не в репо). Данные собраны скриптом, правятся здесь.
Блоки и разделы — как в докстринге guides.py. attach() подключает страницы к GUIDES, раздел «Прокачка по классам»
в гайде прокачки и плитку хаба."""
import re



def t(ru, en, uk):
    return {'ru': ru, 'en': en, 'uk': uk}


def tx(ru, en, uk, **other):
    """t() with the translations that must not come from the json (key already used for another meaning)."""
    return {'ru': ru, 'en': en, 'uk': uk, **other}


# Facts the beta shows and Blizzard has not confirmed (decision 26.10): one mark on all nine languages, in brackets after the claim.
BETA = {'ru': 'по данным беты', 'en': 'per beta data', 'uk': 'за даними бети', 'de': 'laut Beta-Daten', 'fr': 'd’après la bêta',
        'es': 'según los datos de la beta', 'pt': 'segundo os dados da beta', 'it': 'secondo i dati della beta', 'pl': 'wg danych z bety'}
BETA_TRAINER = {'ru': 'Уровни способностей у тренера — по данным беты.', 'en': 'Trainer ability levels: per beta data.',
                'uk': 'Рівні здібностей у тренера — за даними бети.', 'de': 'Fähigkeitsstufen beim Lehrer: laut Beta-Daten.',
                'fr': 'Niveaux des compétences chez l’instructeur : d’après la bêta.',
                'es': 'Niveles de las habilidades del instructor: según los datos de la beta.',
                'pt': 'Níveis das habilidades do instrutor: segundo os dados da beta.',
                'it': 'Livelli delle abilità dall’istruttore: secondo i dati della beta.',
                'pl': 'Levele zdolności u trenera: wg danych z bety.'}


def bt(d, n=1):
    """t()/tx() text with the beta mark in brackets before the period that ends sentence number n (at the end when there is none).
    The new languages take the json translation of the English text, so no new json keys are needed."""
    import langs
    out = {}
    for lang in langs.ALL:
        text = d.get(lang)
        if text is None:
            if lang in langs.OLD or langs.OV.get(lang) is None:
                continue
            text = langs.ov(d['en'], lang)
        ends = [m.start() for m in re.finditer(r'\.(?=\s|$)', text)]
        at = ends[n - 1] if len(ends) >= n else len(text)
        head = text[:at]
        out[lang] = (f'{head}, {BETA[lang]}' if head.endswith(')') else f'{head} ({BETA[lang]})') + text[at:]   # no nested brackets
    return out


CLASS_GUIDES = []
CLASSES = ('warrior', 'paladin', 'hunter', 'rogue', 'priest', 'shaman', 'mage', 'warlock', 'druid')   # порядок классов сайта

# Раздел «Прокачка по классам» в гайде прокачки и плитка хаба: новых строк сайта, поэтому переводы заданы здесь
CLASSES_TITLE = tx('Прокачка по классам', 'Leveling by class', 'Прокачування за класами',
                   de='Leveln nach Klasse', es='Subida de nivel por clase', fr='Progression par classe',
                   it='Livellamento per classe', pl='Levelowanie według klas', pt='Evolução por classe')
CLASSES_LEAD = tx('Отдельный гайд на каждый класс: какой спек качать, таланты по уровням, способности у тренера, ротация соло и в группе.',
                  'A separate guide for every class: which spec to level, talents by level, trainer abilities, and rotations for solo and group play.',
                  'Окремий гайд на кожен клас: який спек прокачувати, таланти за рівнями, здібності в тренера, ротація соло та в групі.',
                  de='Zu jeder Klasse ein eigener Guide: welche Skillung du levelst, Talente nach Stufe, Fähigkeiten beim Lehrer und Rotation solo und in der Gruppe.',
                  es='Una guía por clase: qué especialización subir, talentos por nivel, habilidades del instructor y rotación en solitario y en grupo.',
                  fr='Un guide par classe : quelle spécialisation monter, talents par niveau, compétences chez l’instructeur et rotation en solo et en groupe.',
                  it='Una guida per ogni classe: quale specializzazione livellare, talenti per livello, abilità dall’istruttore e rotazione da soli e in gruppo.',
                  pl='Osobny poradnik dla każdej klasy: którą specjalizację levelować, talenty według levelu, umiejętności u trenera i rotacja solo oraz w grupie.',
                  pt='Um guia por classe: qual especialização usar, talentos por nível, habilidades do instrutor e rotação solo e em grupo.')
CLASSES_TILE = tx('Спек, таланты и ротация для девяти классов', 'Spec, talents and rotation for all nine classes',
                  'Спек, таланти й ротація для дев’яти класів',
                  de='Skillung, Talente und Rotation für alle neun Klassen', es='Especialización, talentos y rotación de las nueve clases',
                  fr='Spécialisation, talents et rotation des neuf classes', it='Specializzazione, talenti e rotazione per tutte le nove classi',
                  pl='Specjalizacja, talenty i rotacja dla wszystkich dziewięciu klas', pt='Especialização, talentos e rotação das nove classes')
HUB_TILE = {'t': CLASSES_TITLE, 'd': CLASSES_TILE, 'href': 'guides/leveling/#classes', 'art': 'warrior'}   # hero_tierlist is the tier list's tile on the same hub


def _related(cid, labels):
    """End-of-page tiles: the class page, the leveling guide, the best race (anchor of the class), the tier list. 'd' is filled by attach()."""
    return [{'t': labels[0], 'd': None, 'href': f'classes/{cid}/', 'art': cid},
            {'t': labels[1], 'd': None, 'href': 'guides/leveling/', 'art': 'hero_dawn'},   # hero_leveling is this page's own hero
            {'t': labels[2], 'd': None, 'href': f'guides/best-race/#{cid}', 'art': 'hero_bestrace'},
            {'t': labels[3], 'd': None, 'href': 'guides/tier-list/', 'art': 'hero_tierlist'}]


# ---------- warrior ----------

CLASS_GUIDES.append({
    'slug': 'leveling-warrior', 'art': 'warrior', 'hero': 'hero_leveling', 'hub': False,
    'title': t('Прокачка Воина 1–60', 'Warrior Leveling 1–60', 'Прокачування Воїна 1–60'),
    'lead': tx('Воин качается медленнее всех классов: по оценке LFCarry, примерно на 12% дольше среднего. В Forever это заметно легче исправить: Защита со щитом получила больше Ярости и урона, а Победный раж лечит после каждого убийства.', 'Warrior is the slowest class to level: about 12% longer than average by LFCarry’s estimate. Forever makes that much easier to fix: Protection with a shield got more Rage and damage, and Victory Rush heals after every kill.', 'Воїн прокачується найповільніше з усіх класів: за оцінкою LFCarry, приблизно на 12% довше за середній показник. У Forever це набагато легше виправити: Захист зі щитом отримав більше Люті та шкоди, а Victory Rush лікує після кожного вбивства.', de='Der Krieger levelt am langsamsten aller Klassen: laut Schätzung von LFCarry etwa 12 % länger als der Durchschnitt. In Forever lässt sich das deutlich leichter ausgleichen: Schutz mit Schild bekam mehr Wut und Schaden, und Siegesrausch heilt nach jedem Kill.', es='El Guerrero es la clase que más tarda en subir: cerca de un 12 % más que la media, según LFCarry. En Forever es mucho más fácil compensarlo: Protección con escudo recibió más Ira y daño, y Ataque de la victoria cura tras cada muerte.', fr='Le Guerrier est la classe qui monte le plus lentement : environ 12 % de plus que la moyenne selon LFCarry. Dans Forever, c’est bien plus facile à corriger : Protection avec bouclier a gagné de la Rage et des dégâts, et Ivresse de la victoire soigne après chaque mort.', it='Il Guerriero è la classe che livella più lentamente: circa il 12% in più della media secondo LFCarry. In Forever è molto più facile rimediare: Protezione con scudo ha ottenuto più Rabbia e danno, e Victory Rush cura dopo ogni uccisione.', pl='Warrior leveluje najwolniej ze wszystkich klas: według szacunku LFCarry mniej więcej o 12% dłużej niż średnia. W Forever dużo łatwiej to nadrobić: Protection z tarczą dostał więcej Rage i obrażeń, a Victory Rush leczy po każdym zabójstwie.', pt='O Guerreiro é a classe que evolui mais devagar: cerca de 12% a mais do que a média, segundo o LFCarry. No Forever isso é bem mais fácil de corrigir: Proteção com escudo ganhou mais Raiva e dano, e Ímpeto da Vitória cura depois de cada morte.'),
    'tile': t('Защита, таланты по уровням и ротация', 'Protection, talents by level and rotation', 'Захист, таланти за рівнями та ротація'),
    'pills': [t('Спек: Защита', 'Spec: Protection', 'Спек: Захист'), t('Таланты 10–60', 'Talents 10–60', 'Таланти 10–60'), tx('По бете', 'Beta data', 'За бетою', de='Betadaten', fr='Données de la bêta', pt='Dados da beta')],
    'sources': [
        ('Icy Veins: Protection Warrior Leveling', 'https://www.icy-veins.com/wow-forever/protection-warrior-leveling'),
        ('Icy Veins: Fury Warrior Leveling', 'https://www.icy-veins.com/wow-forever/fury-warrior-leveling'),
        ('Mobalytics: Warrior Leveling 1-30', 'https://mobalytics.gg/wow-forever/classes/warrior-leveling-guide'),
        ('Warcraft Tavern: Warrior Leveling', 'https://www.warcrafttavern.com/forever/guides/warrior-leveling/'),
        ('Warcraft Tavern: Warrior Guide', 'https://www.warcrafttavern.com/forever/guides/warrior/'),
        ('Method: Warrior Leveling Guide and Talents', 'https://www.method.gg/wow-forever/wow-forever-warrior-leveling-guide-and-talents'),
    ],
    'sections': [
        {'id': 'spec', 'title': t('Какой спек качать', 'Which spec to level', 'Який спек прокачувати'), 'blocks': [
            ('text', [
                t('Качайте Защиту. Icy Veins и Mobalytics называют её лучшим спеком прокачки Воина в Forever: Реванш бьёт сильнее, чем в Classic, таланты ветки дают Ярость при блоке, а щит снижает урон, так что почти не нужно отдыхать между боями. Защита держит несколько врагов сразу и без смены талантов танкует подземелья.', 'Level Protection. Icy Veins and Mobalytics call it the best Warrior leveling spec in Forever: Revenge hits harder than in Classic, the tree’s talents give Rage on blocks, and the shield cuts incoming damage, so you hardly need to rest between fights. Protection holds several enemies at once and tanks dungeons without a respec.', 'Прокачуйте Захист. Icy Veins і Mobalytics називають його найкращим спеком прокачування Воїна у Forever: Revenge б’є сильніше, ніж у Classic, таланти гілки дають Лють під час блоку, а щит знижує шкоду, тож між боями майже не треба відпочивати. Захист утримує кількох ворогів одразу й без зміни талантів танкує підземелля.'),
                t('Источники спорят. Warcraft Tavern пишет, что традиционно качаются за Оружие, и считает все три ветки рабочими. Method советует Оружие с двуручным оружием в паре или тройке, а Защиту для соло. Icy Veins допускает Неистовство позже, когда собраны ключевые таланты и есть два хороших оружия.', 'The sources disagree. Warcraft Tavern says Warriors traditionally level as Arms and counts all three trees as workable. Method recommends Arms with a two-hander for a duo or trio, and Protection for solo. Icy Veins allows Fury later, once the key talents are in and you have two good weapons.', 'Джерела сперечаються. Warcraft Tavern пише, що традиційно качаються за Зброю, і вважає робочими всі три гілки. Method радить Зброю з дворучною зброєю в парі чи трійці, а Захист — для соло. Icy Veins допускає Лють пізніше, коли зібрано ключові таланти й є дві добрі зброї.'),
            ]),
            ('table', {'head': [tx('Спек', 'Spec', 'Спек', de='Skillung', es='Espec.', fr='Spé', it='Spec.', pl='Spec', pt='Espec.'), t('Когда брать', 'When to take it', 'Коли брати'), t('Минус', 'Downside', 'Мінус')], 'rows': [
                [t('Защита', 'Protection', 'Захист'), t('Соло и подземелья, весь путь до 60', 'Solo and dungeons, the whole way to 60', 'Соло та підземелля, увесь шлях до 60'), t('Блок щитом только с 16 уровня, до этого Реванш срабатывает редко', 'Shield Block only from level 16; before that Revenge procs rarely', 'Shield Block лише з 16 рівня, до цього Revenge спрацьовує рідко')],
                [t('Оружие', 'Arms', 'Зброя'), t('Группа или пара с лекарем', 'A group or a duo with a healer', 'Група або пара з цілителем'), t('Больше отдыха между боями', 'More rest between fights', 'Більше відпочинку між боями')],
                [t('Неистовство', 'Fury', 'Лють'), t('После 30–40, когда есть Шквал и Кровожадность', 'After 30–40, once you have Flurry and Bloodthirst', 'Після 30–40, коли є Flurry та Bloodthirst'), t('Два оружия, нужно качать навык обоих', 'Two weapons; you have to train the skill of both', 'Дві зброї, потрібно качати навичку обох')],
            ]}),
        ]},
        {'id': 'talents', 'title': t('Таланты по уровням', 'Talents by level', 'Таланти за рівнями'), 'blocks': [
            ('text', [
                t('Порядок Icy Veins для Защиты (обновлён 21.10). До 30 уровня его подтверждает бета. Уровни 31–60 на бете закрыты: это план источника по талантам Forever, проверим после старта 05.11.', 'Icy Veins order for Protection (updated Oct 21). The beta confirms it up to level 30. Levels 31–60 are closed on the beta: this is the source’s plan for Forever talents, and we will check it after the Nov 4–5 launch.', 'Порядок Icy Veins для Захисту (оновлено 21 жовтня). До 30 рівня його підтверджує бета. Рівні 31–60 у беті закриті: це план джерела щодо талантів Forever, перевіримо після старту 5 листопада.'),
            ]),
            ('table', {'head': [t('Уровни', 'Levels', 'Рівні'), t('Талант', 'Talent', 'Талант'), t('Очки', 'Points', 'Очки')], 'rows': [
                ['10–14', t('Специализация на щитах (Shield Specialization)', 'Shield Specialization', 'Shield Specialization'), '5'],
                ['15–17', t('Улучшенный реванш (Improved Revenge)', 'Improved Revenge', 'Improved Revenge'), '3'],
                ['18–19', t('Улучшенный удар грома (Improved Thunder Clap)', 'Improved Thunder Clap', 'Improved Thunder Clap'), '2'],
                ['20–21', t('Мастер защиты (Master of Defense)', 'Master of Defense', 'Master of Defense'), '2'],
                ['22', t('Улучшенный удар грома (Improved Thunder Clap)', 'Improved Thunder Clap', 'Improved Thunder Clap'), '3/3'],
                ['23', t('Ни шагу назад (Last Stand)', 'Last Stand', 'Last Stand'), '1'],
                ['24', t('Неукротимость (Defiance)', 'Defiance', 'Defiance'), '1'],
                ['25', t('Авангард (Vanguard)', 'Vanguard', 'Vanguard'), '1'],
                ['26–28', t('Улучшенный раскол брони (Improved Sunder Armor)', 'Improved Sunder Armor', 'Improved Sunder Armor'), '3'],
                ['29', t('Неукротимость (Defiance)', 'Defiance', 'Defiance'), '2'],
                ['30–32', t('Сосредоточенная ярость (Focused Rage)', 'Focused Rage', 'Focused Rage'), '3'],
                ['33', t('Оглушающий удар (Concussion Blow)', 'Concussion Blow', 'Concussion Blow'), '1'],
                ['34', t('Неукротимость (Defiance)', 'Defiance', 'Defiance'), '3/3'],
                ['35–39', 'Bastion', '5'],
                ['40', t('Сокрушение щитом (Shield Slam)', 'Shield Slam', 'Shield Slam'), '1'],
                ['41–45', t('Безжалостность (Cruelty)', 'Cruelty', 'Cruelty'), '5'],
                ['46–50', 'Lingering Rage', '5'],
                ['51', t('Пронзительный вой (Piercing Howl)', 'Piercing Howl', 'Piercing Howl'), '1'],
                ['52–55', t('Необузданный гнев (Unbridled Wrath)', 'Unbridled Wrath', 'Unbridled Wrath'), '4'],
                ['56', 'Raging Blows', '1'],
                ['57–60', t('Исступление (Enrage)', 'Enrage', 'Enrage'), '4'],
            ]}),
            ('tip', t('Mobalytics начинает иначе: до 16 уровня Улучшенное кровопускание 3/3 и Безжалостность 3/5, а на 16, когда появится Блок щитом, сброс талантов в Защиту. Перк Legacy Talented даёт таланты до 5 уровней раньше: порядок тот же, просто сдвиньте уровни.', 'Mobalytics starts differently: before level 16, Improved Rend 3/3 and Cruelty 3/5, then at 16, once Shield Block arrives, a respec into Protection. The Legacy Talented perk gives talents up to 5 levels earlier: the order is the same, just shift the levels.', 'Mobalytics починає інакше: до 16 рівня Improved Rend 3/3 і Cruelty 3/5, а на 16, коли з’явиться Shield Block, скидання талантів у Захист. Перк Legacy Talented дає таланти до 5 рівнів раніше: порядок той самий, просто зсуньте рівні.')),
        ]},
        {'id': 'abilities', 'title': t('Способности и тренер', 'Abilities and trainer', 'Здібності й тренер'), 'blocks': [
            ('text', [
                t('Ходите к тренеру каждые два уровня: новые ранги способностей важнее брони, особенно Боевой крик, Кровопускание и Реванш. Новый тип оружия сначала покачайте на слабых врагах: с низким навыком вы промахиваетесь.', 'Visit the trainer every two levels: new ability ranks matter more than armor, especially Battle Shout, Rend and Revenge. Level a new weapon type on weak enemies first: with low skill you miss.', 'Ходіть до тренера кожні два рівні: нові ранги здібностей важливіші за броню, особливо Battle Shout, Rend і Revenge. Новий тип зброї спершу прокачайте на слабких ворогах: з низькою навичкою ви промахуєтеся.'),
            ]),
            ('text', [BETA_TRAINER]),
            ('table', {'head': [t('Уровень', 'Level', 'Рівень'), t('Что взять', 'What to take', 'Що взяти'), tx('Зачем', 'Why', 'Навіщо', de='Wozu', es='Para qué', it='A cosa serve', pl='Po co', pt='Para quê')], 'rows': [
                ['4', t('Рывок, Кровопускание', 'Charge, Rend', 'Charge, Rend'), t('Вход в бой с Яростью и кровотечение', 'Open a fight with Rage, and a bleed', 'Вхід у бій з Люттю та кровотеча')],
                ['8', t('Подрезать сухожилия', 'Hamstring', 'Hamstring'), t('Замедлить бегущего врага', 'Slow a fleeing enemy', 'Уповільнити ворога, що тікає')],
                ['10', t('Оборонительная стойка, Провокация, Раскол брони, Кровавая ярость', 'Defensive Stance, Taunt, Sunder Armor, Bloodrage', 'Defensive Stance, Taunt, Sunder Armor, Bloodrage'), t('Стойка Защиты и Ярость вне боя', 'The Protection stance, and Rage outside combat', 'Стійка Захисту та Лють поза боєм')],
                ['12', t('Превосходство, Удар щитом', 'Overpower, Shield Bash', 'Overpower, Shield Bash'), t('Удар после уклонения, прерывание', 'A strike after a dodge, an interrupt', 'Удар після ухилення, переривання')],
                ['14', t('Реванш, Деморализующий крик', 'Revenge, Demoralizing Shout', 'Revenge, Demoralizing Shout'), t('Главный удар Защиты', 'The main Protection strike', 'Головний удар Захисту')],
                ['16', t('Блок щитом', 'Shield Block', 'Shield Block'), t('Делает Реванш постоянным', 'Makes Revenge available all the time', 'Робить Revenge постійним')],
                ['20', t('Победный раж, Рассекающий удар, Возмездие; древковое у тренера оружия', 'Victory Rush, Cleave, Retaliation; polearms from the weapon trainer', 'Victory Rush, Cleave, Retaliation; держакова зброя в тренера зброї'), t('Лечение после убийства, урон по нескольким целям', 'A heal after a kill, damage to several targets', 'Лікування після вбивства, шкода по кількох цілях')],
                ['24', t('Казнь', 'Execute', 'Execute'), t('Добивание', 'Finishing off', 'Добивання')],
                ['30', t('Стойка берсерка (задание), Перехват', 'Berserker Stance (quest), Intercept', 'Berserker Stance (завдання), Intercept'), t('Третья стойка', 'The third stance', 'Третя стійка')],
                ['36', t('Вихрь', 'Whirlwind', 'Whirlwind'), t('Урон по площади', 'Area damage', 'Шкода по площі')],
                ['40', t('Латы, верховая езда, вторая специализация', 'Plate, mounts, dual specialization', 'Лати, верхова їзда, друга спеціалізація'), t('Броня и второй набор талантов', 'Armor and a second set of talents', 'Броня й другий набір талантів')],
            ]}),
            ('steps', [
                {'t': t('Перед боем', 'Before the fight', 'Перед боєм'),
                 'd': t('Боевой крик, Кровавая ярость между врагами, чтобы не терять Ярость.', 'Battle Shout; Bloodrage between enemies so you don’t waste Rage.', 'Battle Shout, Bloodrage між ворогами, щоб не втрачати Лють.')},
                {'t': t('Вход', 'Opening', 'Вхід'),
                 'd': t('Рывок; с талантом Авангард рывок работает и в оборонительной стойке.', 'Charge; with Vanguard the charge works in Defensive Stance too.', 'Charge; з талантом Vanguard ривок працює й в оборонній стійці.')},
                {'t': t('В бою', 'In the fight', 'У бою'),
                 'd': t('Блок щитом перед ударом врага, Реванш при каждом срабатывании, Кровопускание, Раскол брони 2–3 раза; на двух и больше врагах Удар грома и Деморализующий крик.', 'Shield Block before an enemy strike, Revenge on every proc, Rend, Sunder Armor 2–3 times; against two or more enemies, Thunder Clap and Demoralizing Shout.', 'Shield Block перед ударом ворога, Revenge при кожному спрацьовуванні, Rend, Sunder Armor 2–3 рази; проти двох і більше ворогів Thunder Clap і Demoralizing Shout.')},
                {'t': t('После', 'After', 'Після'),
                 'd': t('Победный раж, если здоровье не полное; остаток Ярости сберегите на следующего врага.', 'Victory Rush if your health isn’t full; save leftover Rage for the next enemy.', 'Victory Rush, якщо здоров’я не повне; залишок Люті збережіть на наступного ворога.')},
            ]),
            ('text', [
                t('В подземелье угроза важнее экономии: Реванш, Раскол брони до 5 зарядов на боссе, Удар грома на группе, Провокация при потере цели. По Mobalytics (18.10), Деморализующий крик на бете не создавал угрозы из-за ошибки: не открывайте им бой. Удар героя и Рассекающий удар жмите только при лишней Ярости: удар не даёт Ярости за автоатаку.', 'In a dungeon, threat matters more than saving resources: Revenge, Sunder Armor up to 5 stacks on a boss, Thunder Clap on the group, Taunt when you lose a target. According to Mobalytics (Oct 18), Demoralizing Shout generated no threat on the beta because of a bug: don’t open a pull with it. Use Heroic Strike and Cleave only with spare Rage: the strike gives no Rage for the auto-attack.', 'У підземеллі загроза важливіша за економію: Revenge, Sunder Armor до 5 зарядів на босі, Thunder Clap на групу, Taunt, коли втрачаєте ціль. За Mobalytics (18 жовтня), Demoralizing Shout у бета-версії не створював загрози через помилку: не починайте ним бій. Heroic Strike і Cleave тисніть лише за зайвої Люті: удар не дає Люті за автоатаку.'),
            ]),
        ]},
        {'id': 'play', 'title': t('Соло, вдвоём, в группе', 'Solo, duo, group', 'Соло, удвох, у групі'), 'blocks': [
            ('tabs', [
                {'id': 'solo', 't': tx('Соло', 'Solo', 'Соло', es='En solitario', pt='Solo'), 'blocks': [('text', [t('Тяните по одному врагу. Несколько врагов разбирайте по одному, остальных замедляйте (Подрезать сухожилия). Держите бинты (Первая помощь), еду и зелья лечения: Победный раж лечит только после убийства. Против заклинателей и элементалей Защите тяжелее.', 'Pull one enemy at a time. Take several enemies one by one and slow the rest (Hamstring). Keep bandages (First Aid), food and healing potions: Victory Rush heals only after a kill. Protection has a harder time against casters and elementals.', 'Тягніть по одному ворогу. Кількох ворогів розбирайте по черзі, решту уповільнюйте (Hamstring). Майте бинти (Перша допомога), їжу та зілля лікування: Victory Rush лікує лише після вбивства. Проти заклиначів і елементалів Захисту важче.')])]},
                {'id': 'duo', 't': tx('Вдвоём', 'Duo', 'Удвох', de='Zu zweit', es='En pareja', fr='À deux', it='In coppia', pl='We dwoje', pt='Em dupla'), 'blocks': [('text', [t('Лучшая пара — лекарь или класс с самолечением. Боевой крик действует на группу, Раскол брони усиливает физический урон напарника. Если напарник тоже ближнего боя, Оружие с двуручным оружием убивает быстрее.', 'The best partner is a healer or a class with self-healing. Battle Shout buffs the group, and Sunder Armor boosts your partner’s physical damage. If your partner is also melee, Arms with a two-hander kills faster.', 'Найкраща пара — цілитель або клас із самолікуванням. Battle Shout діє на групу, Sunder Armor підсилює фізичну шкоду напарника. Якщо напарник теж б’є зблизька, Зброя з дворучною зброєю вбиває швидше.')])]},
                {'id': 'party', 't': t('Группа', 'Group', 'Група'), 'blocks': [('text', [t('Защита сразу готова танковать: таланты те же, что на прокачке. Скорость подземелий даёт хорошее оружие: урон Воина почти целиком от него.', 'Protection is ready to tank right away: the talents are the same as for leveling. Dungeon speed comes from a good weapon: a Warrior’s damage comes almost entirely from it.', 'Захист одразу готовий танкувати: таланти ті самі, що й на прокачуванні. Швидкість підземель дає добра зброя: шкода Воїна майже вся від неї.')])]},
            ]),
        ]},
        {'id': 'gear', 'title': t('Характеристики и снаряжение', 'Stats and gear', 'Характеристики та спорядження'), 'blocks': [
            ('text', [
                t('Урон Воина почти целиком от оружия, поэтому новое оружие важнее любой брони (Method). Для Защиты Mobalytics ставит силу (2 силы атаки за единицу), затем ловкость (крит) и выносливость для подземелий; дух ускоряет восполнение здоровья, но Защите он нужен меньше, чем Оружию. Быстрое одноручное лучше медленного: Реванш и Сокрушение щитом не зависят от урона оружия.', 'A Warrior’s damage comes almost entirely from the weapon, so a new weapon matters more than any armor (Method). For Protection, Mobalytics puts Strength first (2 attack power per point), then Agility (crit) and Stamina for dungeons; Spirit speeds up health regeneration, but Protection needs it less than Arms does. A fast one-hander beats a slow one: Revenge and Shield Slam don’t depend on weapon damage.', 'Шкода Воїна майже вся від зброї, тому нова зброя важливіша за будь-яку броню (Method). Для Захисту Mobalytics ставить на перше місце силу (2 сили атаки за одиницю), потім спритність (крит) і витривалість для підземель; дух прискорює відновлення здоров’я, але Захисту він потрібен менше, ніж Зброї. Швидка одноручна краща за повільну: Revenge і Shield Slam не залежать від шкоди зброї.'),
                t('Профессии: Горное дело и Кузнечное дело — точильные камни и снаряжение; Снятие шкур даёт деньги и стул в лагере (+2% крита). Пары под класс и объекты лагеря — в гайде по профессиям.', 'Professions: Mining and Blacksmithing for sharpening stones and gear; Skinning brings money and a stool at camp (+2% crit). Class pairings and camp objects are in the professions guide.', 'Професії: Гірництво і Ковальство — точильні камені та спорядження; Знімання шкур дає гроші й ослінчик у таборі (+2% крита). Пари під клас і об’єкти табору — у гайді з професій.'),
            ]),
        ]},
        {'id': 'forever', 'title': t('Чем Forever отличается от Classic', 'How Forever differs from Classic', 'Чим Forever відрізняється від Classic'), 'blocks': [
            ('table', {'head': [t('Что', 'What', 'Що'), t('В Forever', 'In Forever', 'У Forever')], 'rows': [
                [t('Ярость', 'Rage', 'Лють'), tx('Считается от скорости оружия, а не от урона. Криты дают на 100% больше Ярости (в ранней бете было 75%).', 'Based on weapon speed, not damage. Crits give 100% more Rage (it was 75% in the early beta).', 'Рахується від швидкості зброї, а не від шкоди. Криті дають на 100% більше Люті (у ранній беті було 75%).', de='Wird aus der Waffengeschwindigkeit berechnet, nicht aus dem Schaden. Krits geben 100 % mehr Wut (in der frühen Beta 75 %).', es='Se calcula según la velocidad del arma, no según el daño. Los críticos dan un 100 % más de Ira (75 % en la beta temprana).', fr='Calculée d’après la vitesse de l’arme, pas d’après les dégâts. Les critiques donnent 100 % de Rage en plus (75 % au début de la bêta).', it='Si calcola dalla velocità dell’arma, non dal danno. I critici danno il 100% di Rabbia in più (era il 75% nella prima beta).', pl='Liczony od szybkości broni, a nie od obrażeń. Krytyki dają o 100% więcej Rage (we wczesnej becie było 75%).', pt='Calculada pela velocidade da arma, não pelo dano. Críticos dão 100% a mais de Raiva (era 75% no início da beta).')],
                [t('Победный раж', 'Victory Rush', 'Victory Rush'), t('Есть с 20 уровня: 10% здоровья после убийства, откат 30 сек, жать в течение 20 сек. В Classic его не было.', 'Available from level 20: 10% of health after a kill, 30 sec cooldown, usable within 20 sec. It did not exist in Classic.', 'Є з 20 рівня: 10% здоров’я після вбивства, відкат 30 с, тиснути протягом 20 с. У Classic його не було.')],
                [t('Удар грома', 'Thunder Clap', 'Thunder Clap'), t('Работает в оборонительной стойке, его улучшение перенесено в ветку Защиты.', 'Works in Defensive Stance, and its improvement moved to the Protection tree.', 'Працює в оборонній стійці, його покращення перенесено в гілку Захисту.')],
                [t('Кровопускание', 'Rend', 'Rend'), t('Растёт от силы атаки и, как Раскол брони, сразу закрепляет врага за вами.', 'Scales with attack power and, like Sunder Armor, immediately ties the enemy to you.', 'Росте від сили атаки й, як Sunder Armor, одразу закріплює ворога за вами.')],
                [t('Боевой крик', 'Battle Shout', 'Battle Shout'), t('Улучшение стало базовым, талант не нужен.', 'The improvement became baseline; no talent needed.', 'Покращення стало базовим, талант не потрібен.')],
                [t('Новые таланты', 'New talents', 'Нові таланти'), t('Авангард, Мастер защиты, Gore Drinker, Кровавый азарт: в Classic их нет.', 'Vanguard, Master of Defense, Gore Drinker, Bloodthrill: not in Classic.', 'Vanguard, Master of Defense, Gore Drinker, Bloodthrill: у Classic їх немає.')],
                [t('Вторая специализация', 'Dual specialization', 'Друга спеціалізація'), t('С 40 уровня у тренера.', 'From level 40 at the trainer.', 'З 40 рівня в тренера.')],
            ]}),
        ]},
        {'id': 'faq', 'title': t('Вопросы', 'Questions', 'Питання'), 'blocks': [
            ('faq', [
                {'id': 'q1', 'q': t('Какой спек лучше для прокачки Воина в WoW Forever?', 'What is the best spec for leveling a Warrior in WoW Forever?', 'Який спек найкращий для прокачування Воїна у WoW Forever?'),
                 'a': [t('Защита: её советуют Icy Veins и Mobalytics. Warcraft Tavern и Method допускают Оружие, особенно в группе.', 'Protection: Icy Veins and Mobalytics recommend it. Warcraft Tavern and Method allow Arms, especially in a group.', 'Захист: його радять Icy Veins і Mobalytics. Warcraft Tavern і Method допускають Зброю, особливо в групі.')]},
                {'id': 'q2', 'q': t('Почему Воин качается медленно?', 'Why does the Warrior level slowly?', 'Чому Воїн прокачується повільно?'),
                 'a': [t('У него почти нет самолечения и контроля, и он зависит от оружия. В Forever это смягчают Победный раж и таланты Защиты, но по оценке LFCarry Воин всё равно примерно на 12% медленнее среднего.', 'It has almost no self-healing or control and depends on its weapon. In Forever, Victory Rush and the Protection talents soften that, but by LFCarry’s estimate the Warrior is still about 12% slower than average.', 'У нього майже немає самолікування та контролю, і він залежить від зброї. У Forever Victory Rush і таланти Захисту пом’якшують це, але за оцінкою LFCarry Воїн усе одно приблизно на 12% повільніший за середній показник.')]},
                {'id': 'q3', 'q': t('Нужен ли щит на прокачке?', 'Do I need a shield for leveling?', 'Чи потрібен щит на прокачуванні?'),
                 'a': [t('Для Защиты да: Блок щитом даёт стабильный Реванш. Mobalytics советует быстрое одноручное оружие: Реванш и Сокрушение щитом не зависят от урона оружия.', 'For Protection, yes: Shield Block gives a steady Revenge. Mobalytics recommends a fast one-handed weapon: Revenge and Shield Slam don’t depend on weapon damage.', 'Для Захисту так: Shield Block дає стабільний Revenge. Mobalytics радить швидку одноручну зброю: Revenge і Shield Slam не залежать від шкоди зброї.')]},
                {'id': 'q4', 'q': t('Когда брать Неистовство?', 'When should I take Fury?', 'Коли брати Лють?'),
                 'a': [t('Не раньше 30–40 уровня, когда есть Шквал, Кровожадность (40) и два хороших оружия. До этого Неистовство медленнее Защиты (Icy Veins).', 'Not before level 30–40, when you have Flurry, Bloodthirst (40) and two good weapons. Before that, Fury is slower than Protection (Icy Veins).', 'Не раніше 30–40 рівня, коли є Flurry, Bloodthirst (40) і дві добрі зброї. До цього Лють повільніша за Захист (Icy Veins).')]},
                {'id': 'q5', 'q': t('Можно ли держать два набора талантов?', 'Can I keep two talent sets?', 'Чи можна тримати два набори талантів?'),
                 'a': [t('Да, вторая специализация открывается на 40 уровне. Удобно: Защита для подземелий, второй набор под соло или PvP.', 'Yes, dual specialization opens at level 40. Handy: Protection for dungeons, the second set for solo or PvP.', 'Так, друга спеціалізація відкривається на 40 рівні. Зручно: Захист для підземель, другий набір для соло чи PvP.')]},
            ]),
        ]},
        {'id': 'related', 'title': t('Смотрите также', 'See also', 'Дивіться також'), 'blocks': [
            ('tiles', _related('warrior', [
                t('Воин', 'Warrior', 'Воїн'),
                tx('Прокачка 1–60', 'Leveling 1–60', 'Прокачування 1–60', fr='Monter de 1 à 60', it='Livellare 1–60', pt='Evoluir 1–60'),
                t('Лучшая раса', 'Best race', 'Найкраща раса'),
                t('Тир-лист', 'Tier list', 'Тір-лист'),
            ])),
        ]},
    ],
})

# ---------- paladin ----------

CLASS_GUIDES.append({
    'slug': 'leveling-paladin', 'art': 'paladin', 'hero': 'hero_leveling', 'hub': False,
    'title': t('Прокачка Паладина 1–60', 'Paladin Leveling 1–60', 'Прокачування Паладина 1–60'),
    'lead': t('Паладин качается в среднем темпе и почти не умирает: латы, лечение и щиты. В Forever у него новая способность Священный удар, а Освящение доступно у тренера с 20 уровня без талантов.', 'Paladin levels at an average pace and almost never dies: plate, heals and shields. In Forever it has a new ability, Holy Strike, and Consecration is available from the trainer at level 20 with no talents.', 'Паладин прокачується в середньому темпі й майже не помирає: лати, лікування та щити. У Forever він має нову здібність Holy Strike, а Consecration доступне в тренера з 20 рівня без талантів.'),
    'tile': t('Воздаяние, печати и таланты по уровням', 'Retribution, seals and talents by level', 'Відплата, печатки й таланти за рівнями'),
    'pills': [t('Спек: Воздаяние', 'Spec: Retribution', 'Спек: Відплата'), t('Таланты 10–60', 'Talents 10–60', 'Таланти 10–60'), tx('По бете', 'Beta data', 'За бетою', de='Betadaten', fr='Données de la bêta', pt='Dados da beta')],
    'sources': [
        ('Icy Veins: Retribution Paladin Leveling', 'https://www.icy-veins.com/wow-forever/retribution-paladin-leveling'),
        ('Mobalytics: Paladin Leveling 1-30', 'https://mobalytics.gg/wow-forever/classes/paladin-leveling-guide'),
        ('Warcraft Tavern: Paladin Leveling', 'https://www.warcrafttavern.com/forever/guides/paladin-leveling/'),
    ],
    'sections': [
        {'id': 'spec', 'title': t('Какой спек качать', 'Which spec to level', 'Який спек прокачувати'), 'blocks': [
            ('text', [
                t('Качайте Воздаяние. Его советуют Warcraft Tavern, Mobalytics и Icy Veins: хороший урон по одной цели, лечение из своей маны и защиты на крайний случай. Tavern советует вкладывать в Воздаяние первые 20–30 уровней, даже если потом вы хотите танковать.', 'Level Retribution. Warcraft Tavern, Mobalytics and Icy Veins all recommend it: good single-target damage, healing from your own mana and defensives for emergencies. Tavern suggests putting the first 20–30 levels into Retribution even if you want to tank later.', 'Прокачуйте Відплату. Її радять Warcraft Tavern, Mobalytics та Icy Veins: хороша шкода по одній цілі, лікування з власної мани та захист на крайній випадок. Tavern радить вкладати у Відплату перші 20–30 рівнів, навіть якщо згодом ви хочете танкувати.'),
                t('Учтите: 15.10 Воздаяние ослабили (Воитель Света 10/20/30% вместо 20/40/60%, Освящение меньше растёт от силы заклинаний). Для прокачки спек всё равно в числе сильных.', 'Note: Retribution was nerfed on Oct 15 (Champion of the Light 10/20/30% instead of 20/40/60%, Consecration scales less with spell power). For leveling it is still among the strong specs.', 'Зважайте: 15 жовтня Відплату послабили (Champion of the Light 10/20/30% замість 20/40/60%, Consecration менше росте від сили заклинань). Для прокачування спек усе одно серед сильних.'),
            ]),
            ('table', {'head': [tx('Спек', 'Spec', 'Спек', de='Skillung', es='Espec.', fr='Spé', it='Spec.', pl='Spec', pt='Espec.'), t('Когда брать', 'When to take it', 'Коли брати'), t('Минус', 'Downside', 'Мінус')], 'rows': [
                [t('Воздаяние', 'Retribution', 'Відплата'), t('Соло, весь путь до 60', 'Solo, the whole way to 60', 'Соло, увесь шлях до 60'), t('Нечем сбить заклинание врага и догнать бегущего', 'Nothing to interrupt an enemy spell or catch a runner', 'Нічим збити заклинання ворога й наздогнати того, хто тікає')],
                [t('Защита', 'Protection', 'Захист'), t('Бить сразу 3–4 врагов через Освящение, танковать подземелья', 'Hit 3–4 enemies at once with Consecration, tank dungeons', 'Бити одразу 3–4 ворогів через Consecration, танкувати підземелля'), t('Медленнее по одной цели', 'Slower on a single target', 'Повільніше по одній цілі')],
                [t('Свет через Шок небес', 'Holy through Holy Shock', 'Світло через Holy Shock'), t('С экипировкой на силу заклинаний', 'With spell power gear', 'Зі спорядженням на силу заклинань'), t('Раскрывается только с талантом Шок небес', 'Opens up only with the Holy Shock talent', 'Розкривається лише з талантом Holy Shock')],
            ]}),
        ]},
        {'id': 'talents', 'title': t('Таланты по уровням', 'Talents by level', 'Таланти за рівнями'), 'blocks': [
            ('text', [
                t('Порядок Icy Veins для Воздаяния (обновлён 17.10). До 30 уровня его подтверждает бета. Уровни 31–60 на бете закрыты: это план источника, проверим после старта 05.11.', 'Icy Veins order for Retribution (updated Oct 17). The beta confirms it up to level 30. Levels 31–60 are closed on the beta: this is the source’s plan, and we will check it after the Nov 4–5 launch.', 'Порядок Icy Veins для Відплати (оновлено 17 жовтня). До 30 рівня його підтверджує бета. Рівні 31–60 у беті закриті: це план джерела, перевіримо після старту 5 листопада.'),
            ]),
            ('table', {'head': [t('Уровни', 'Levels', 'Рівні'), t('Талант', 'Talent', 'Талант'), t('Очки', 'Points', 'Очки')], 'rows': [
                ['10–14', t('Благодарение (Benediction)', 'Benediction', 'Benediction'), '5'],
                ['15–16', t('Улучшенное правосудие (Improved Judgement)', 'Improved Judgement', 'Improved Judgement'), '2'],
                ['17', t('Приговор (Conviction)', 'Conviction', 'Conviction'), '1'],
                ['18–19', 'Holy Conduit', '2'],
                ['20', t('Печать повиновения (Seal of Command)', 'Seal of Command', 'Seal of Command'), '1'],
                ['21–22', t('Погоня за справедливостью (Pursuit of Justice)', 'Pursuit of Justice', 'Pursuit of Justice'), '2'],
                ['23–24', t('Освящённое правосудие (Sanctified Judgement)', 'Sanctified Judgement', 'Sanctified Judgement'), '2'],
                ['25', 'Sacred Arbiter', '1'],
                ['26', t('Освящённое правосудие (Sanctified Judgement)', 'Sanctified Judgement', 'Sanctified Judgement'), '3/3'],
                ['27–29', t('Подтверждение (Vindication)', 'Vindication', 'Vindication'), '3'],
                ['30', t('Покаяние (Repentance)', 'Repentance', 'Repentance'), '1'],
                ['31–33', t('Отмщение (Vengeance)', 'Vengeance', 'Vengeance'), '3'],
                ['34', t('Специализация на двуручном оружии (Two-Handed Weapon Specialization)', 'Two-Handed Weapon Specialization', 'Two-Handed Weapon Specialization'), '1'],
                ['35–37', t('Воитель Света (Champion of the Light)', 'Champion of the Light', 'Champion of the Light'), '3'],
                ['38–39', t('Специализация на двуручном оружии (Two-Handed Weapon Specialization)', 'Two-Handed Weapon Specialization', 'Two-Handed Weapon Specialization'), '3/3'],
                ['40', t('Изгиб Света (Twist of Light)', 'Twist of Light', 'Twist of Light'), '1'],
                ['41–42', 'Instrument of Law', '2'],
                ['43–47', t('Божественный интеллект (Divine Intellect)', 'Divine Intellect', 'Divine Intellect'), '5'],
                ['48–50', 'Improved Seals', '3'],
                ['51–52', t('Божественная сила (Divine Strength)', 'Divine Strength', 'Divine Strength'), '2'],
                ['53–55', t('Благоговение (Reverence)', 'Reverence', 'Reverence'), '3'],
                ['56–58', t('Божественная сила (Divine Strength)', 'Divine Strength', 'Divine Strength'), '5/5'],
                ['59–60', t('Приговор (Conviction)', 'Conviction', 'Conviction'), '3'],
            ]}),
            ('tip', t('Mobalytics (17.10) начинает с защиты и крита: Отражение 5/5, Приговор 5/5, затем Погоня за справедливостью (+15% к скорости) и Печать повиновения. Icy Veins сначала берёт экономию маны (Благодарение). Оба пути рабочие. Перк Legacy Talented даёт таланты до 5 уровней раньше.', 'Mobalytics (Oct 17) starts with defense and crit: Deflection 5/5, Conviction 5/5, then Pursuit of Justice (+15% speed) and Seal of Command. Icy Veins takes mana savings (Benediction) first. Both paths work. The Legacy Talented perk gives talents up to 5 levels earlier.', 'Mobalytics (17 жовтня) починає із захисту й крита: Deflection 5/5, Conviction 5/5, потім Pursuit of Justice (+15% до швидкості) і Seal of Command. Icy Veins спершу бере економію мани (Benediction). Обидва шляхи робочі. Перк Legacy Talented дає таланти до 5 рівнів раніше.')),
        ]},
        {'id': 'abilities', 'title': t('Способности и тренер', 'Abilities and trainer', 'Здібності й тренер'), 'blocks': [
            ('text', [BETA_TRAINER]),
            ('table', {'head': [t('Уровень', 'Level', 'Рівень'), t('Что взять', 'What to take', 'Що взяти'), tx('Зачем', 'Why', 'Навіщо', de='Wozu', es='Para qué', it='A cosa serve', pl='Po co', pt='Para quê')], 'rows': [
                ['1', t('Печать праведности, Свет небес, Аура благочестия', 'Seal of Righteousness, Holy Light, Devotion Aura', 'Seal of Righteousness, Holy Light, Devotion Aura'), t('Урон, лечение, броня', 'Damage, healing, armor', 'Шкода, лікування, броня')],
                ['4', t('Правосудие, Благословение могущества', 'Judgement, Blessing of Might', 'Judgement, Blessing of Might'), t('Правосудие и сила атаки', 'Judgement and attack power', 'Правосуддя та сила атаки')],
                ['6', t('Священный удар, Божественная защита', 'Holy Strike, Divine Protection', 'Holy Strike, Divine Protection'), t('Удар Светом, откат 10 сек', 'A Light strike, 10 sec cooldown', 'Удар Світлом, відкат 10 с')],
                ['8', t('Молот правосудия', 'Hammer of Justice', 'Hammer of Justice'), t('Оглушение, единственный контроль', 'A stun, the only control', 'Приголомшення, єдиний контроль')],
                ['10', t('Возложение рук, Благословение защиты, Печать ярости', 'Lay on Hands, Blessing of Protection, Seal of Fury', 'Lay on Hands, Blessing of Protection, Seal of Fury'), t('Спасение и печать танка', 'A rescue and the tank seal', 'Порятунок і печатка танка')],
                ['16', t('Аура воздаяния', 'Retribution Aura', 'Retribution Aura'), t('Урон тем, кто бьёт вас', 'Damage to those who hit you', 'Шкода тим, хто б’є вас')],
                ['20', t('Освящение, Экзорцизм, Вспышка Света, Благословение королей; древковое у тренера оружия', 'Consecration, Exorcism, Flash of Light, Blessing of Kings; polearms from the weapon trainer', 'Consecration, Exorcism, Flash of Light, Blessing of Kings; держакова зброя в тренера зброї'), t('Урон по площади и быстрое лечение', 'Area damage and a fast heal', 'Шкода по площі та швидке лікування')],
                ['32', t('Божественный щит', 'Divine Shield', 'Divine Shield'), t('Полная неуязвимость', 'Full invulnerability', 'Повна невразливість')],
                ['40', t('Скакун по заданию класса, вторая специализация', 'Class quest mount, dual specialization', 'Скакун за завданням класу, друга спеціалізація'), t('Езда без покупки скакуна', 'Riding without buying a mount', 'Їзда без купівлі скакуна')],
                ['44', t('Молот гнева', 'Hammer of Wrath', 'Hammer of Wrath'), t('Добивание', 'Finishing off', 'Добивання')],
            ]}),
            ('steps', [
                {'t': t('Перед боем', 'Before the fight', 'Перед боєм'),
                 'd': t('Благословение могущества и Аура воздаяния, печать на оружии: Печать повиновения с медленным двуручным, Печать праведности до 20 уровня или с одноручным.', 'Blessing of Might and Retribution Aura, a seal on your weapon: Seal of Command with a slow two-hander, Seal of Righteousness before level 20 or with a one-hander.', 'Blessing of Might і Retribution Aura, печатка на зброї: Seal of Command з повільною дворучною, Seal of Righteousness до 20 рівня або з одноручною.')},
                {'t': t('Вход', 'Opening', 'Вхід'),
                 'd': t('Правосудие на подходе, затем Священный удар.', 'Judgement on the approach, then Holy Strike.', 'Judgement на підході, далі Holy Strike.')},
                {'t': t('В бою', 'In the fight', 'У бою'),
                 'd': t('Правосудие и Священный удар по откату; печать обновляйте, только когда она кончается. На 2+ врагах Освящение, если они проживут 8 секунд: за это время оно наносит полный урон.', 'Judgement and Holy Strike on cooldown; refresh the seal only when it runs out. Against 2+ enemies, Consecration if they will live 8 seconds: that is how long it takes to deal full damage.', 'Judgement і Holy Strike за відкатом; печатку оновлюйте, лише коли вона закінчується. На 2+ ворогах Consecration, якщо вони проживуть 8 секунд: за цей час воно завдає повної шкоди.')},
                {'t': t('После', 'After', 'Після'),
                 'd': t('остаток маны потратьте на лечение (Свет небес) вместо еды.', 'spend leftover mana on healing (Holy Light) instead of eating.', 'залишок мани витратьте на лікування (Holy Light) замість їжі.')},
            ]),
            ('text', [
                t('Благословения в Forever длятся час. Держите Спасение (Salvation, 26 уровень) на всех, кроме танка: оно снижает угрозу. Ставьте ауру, которой нет у другого паладина. Защита танкует с Печатью ярости: её Правосудие провоцирует врага.', 'Blessings last an hour in Forever. Keep Blessing of Salvation (level 26) on everyone except the tank: it lowers threat. Pick the aura another Paladin doesn’t have. Protection tanks with Seal of Fury: its Judgement taunts the enemy.', 'Благословення у Forever тривають годину. Тримайте Blessing of Salvation (26 рівень) на всіх, крім танка: воно знижує загрозу. Ставте ауру, якої немає в іншого паладина. Захист танкує з Seal of Fury: її Правосуддя провокує ворога.'),
            ]),
        ]},
        {'id': 'play', 'title': t('Соло, вдвоём, в группе', 'Solo, duo, group', 'Соло, удвох, у групі'), 'blocks': [
            ('tabs', [
                {'id': 'solo', 't': tx('Соло', 'Solo', 'Соло', es='En solitario', pt='Solo'), 'blocks': [('text', [t('Мана — это и урон, и лечение. Воду меняйте примерно каждые 10 уровней, для серий врагов берите зелья маны. Мана восстанавливается через 5 секунд без заклинаний: жмите заклинания пачкой, потом бейте оружием. Опасный бой: Божественная защита или Благословение защиты на себя, потом лечение.', 'Mana is both damage and healing. Replace your water about every 10 levels, and take mana potions for chains of enemies. Mana regenerates after 5 seconds without casting: cast spells in a burst, then hit with the weapon. In a dangerous fight, Divine Protection or Blessing of Protection on yourself, then heal.', 'Мана — це і шкода, і лікування. Воду міняйте приблизно кожні 10 рівнів, для серій ворогів беріть зілля мани. Мана відновлюється через 5 секунд без заклинань: тисніть заклинання пачкою, потім бийте зброєю. Небезпечний бій: Divine Protection або Blessing of Protection на себе, потім лікування.')])]},
                {'id': 'duo', 't': tx('Вдвоём', 'Duo', 'Удвох', de='Zu zweit', es='En pareja', fr='À deux', it='In coppia', pl='We dwoje', pt='Em dupla'), 'blocks': [('text', [t('Паладин хорош с любым напарником: лечит его в паузах и даёт благословение. С классом дальнего боя берите Защиту и Освящение, чтобы держать врагов на себе.', 'Paladin is good with any partner: it heals them between pulls and gives a blessing. With a ranged class, take Protection and Consecration to keep enemies on you.', 'Паладин добрий з будь-яким напарником: лікує його в паузах і дає благословення. З класом дальнього бою беріть Захист і Consecration, щоб тримати ворогів на собі.')])]},
                {'id': 'party', 't': t('Группа', 'Group', 'Група'), 'blocks': [('text', [t('Можно танковать, лечить или бить. До 40 уровня одна специализация: выберите роль, которая нужна группе чаще.', 'You can tank, heal or deal damage. Until level 40 there is one specialization: choose the role the group needs more often.', 'Можна танкувати, лікувати або бити. До 40 рівня одна спеціалізація: оберіть роль, яка потрібна групі частіше.')])]},
            ]),
        ]},
        {'id': 'gear', 'title': t('Характеристики и снаряжение', 'Stats and gear', 'Характеристики та спорядження'), 'blocks': [
            ('text', [
                t('Воздаянию нужны сила и медленное тяжёлое двуручное оружие. Mobalytics даёт порядок для человека: сила > дух > ловкость > интеллект > выносливость; для нежити дух в конце, у неё есть Каннибализм. Защите и Свету Warcraft Tavern советует силу заклинаний и выносливость; Защите — быстрое оружие, Свету — одноручное с силой заклинаний.', 'Retribution needs Strength and a slow, heavy two-hander. Mobalytics gives this order for Human: Strength > Spirit > Agility > Intellect > Stamina; for Undead, Spirit goes last, since they have Cannibalize. For Protection and Holy, Warcraft Tavern recommends spell power and Stamina; a fast weapon for Protection, a one-hander with spell power for Holy.', 'Відплаті потрібні сила й повільна важка дворучна зброя. Mobalytics дає порядок для людини: сила > дух > спритність > інтелект > витривалість; для нежиті дух наприкінці, у неї є Канібалізм. Для Захисту й Світла Warcraft Tavern радить силу заклинань і витривалість; Захисту — швидку зброю, Світлу — одноручну з силою заклинань.'),
                t('Профессии: Кузнечное дело с Горным делом, чтобы делать себе латы и оружие (Tavern). Пары под класс и объекты лагеря — в гайде по профессиям.', 'Professions: Blacksmithing with Mining to make your own plate armor and weapons (Tavern). Class pairings and camp objects are in the professions guide.', 'Професії: Ковальство з Гірництвом, щоб виготовляти собі лати й зброю (Tavern). Пари під клас і об’єкти табору — у гайді з професій.'),
            ]),
        ]},
        {'id': 'forever', 'title': t('Чем Forever отличается от Classic', 'How Forever differs from Classic', 'Чим Forever відрізняється від Classic'), 'blocks': [
            ('table', {'head': [t('Что', 'What', 'Що'), t('В Forever', 'In Forever', 'У Forever')], 'rows': [
                [t('Священный удар', 'Holy Strike', 'Holy Strike'), t('Новый удар с 6 уровня, откат 10 сек.', 'A new strike from level 6, 10 sec cooldown.', 'Новий удар із 6 рівня, відкат 10 с.')],
                [t('Освящение', 'Consecration', 'Consecration'), t('Базовое у тренера с 20 уровня, в Classic это был талант.', 'Baseline from the trainer at level 20; in Classic it was a talent.', 'Базове в тренера з 20 рівня, у Classic це був талант.')],
                [t('Правосудие', 'Judgement', 'Judgement'), t('Больше не тратит печать.', 'No longer consumes the seal.', 'Більше не витрачає печатку.')],
                [t('Благословения', 'Blessings', 'Благословення'), t('Длятся 1 час (было 5 минут), Благословение королей стало базовым.', 'Last 1 hour (was 5 minutes), and Blessing of Kings became baseline.', 'Тривають 1 годину (було 5 хвилин), Blessing of Kings стало базовим.')],
                [t('Печать ярости', 'Seal of Fury', 'Seal of Fury'), t('Новая печать танка: Правосудие провоцирует врага.', 'A new tank seal: its Judgement taunts the enemy.', 'Нова печатка танка: Правосуддя провокує ворога.')],
                [t('Аура воздаяния', 'Retribution Aura', 'Retribution Aura'), t('Растёт от силы заклинаний.', 'Scales with spell power.', 'Росте від сили заклинань.')],
                [tx('Орда', 'Horde', 'Орда', pl='Horde'), t('Нежить может быть паладином, у неё своя стартовая зона.', 'Undead can be Paladins and have their own starting zone.', 'Нежить може бути паладином, у неї своя стартова зона.')],
                [t('Вторая специализация', 'Dual specialization', 'Друга спеціалізація'), t('С 40 уровня.', 'From level 40.', 'З 40 рівня.')],
            ]}),
        ]},
        {'id': 'faq', 'title': t('Вопросы', 'Questions', 'Питання'), 'blocks': [
            ('faq', [
                {'id': 'q1', 'q': t('Какой спек Паладина качать в WoW Forever?', 'Which Paladin spec should I level in WoW Forever?', 'Який спек Паладина прокачувати у WoW Forever?'),
                 'a': [t('Воздаяние: его советуют Warcraft Tavern, Mobalytics и Icy Veins. Защита хороша, если бить сразу нескольких врагов через Освящение.', 'Retribution: Warcraft Tavern, Mobalytics and Icy Veins recommend it. Protection is good if you hit several enemies at once with Consecration.', 'Відплату: її радять Warcraft Tavern, Mobalytics та Icy Veins. Захист хороший, якщо бити одразу кількох ворогів через Consecration.')]},
                {'id': 'q2', 'q': t('Какую печать держать?', 'Which seal should I use?', 'Яку печатку тримати?'),
                 'a': [t('Печать повиновения с медленным двуручным оружием, Печать праведности до 20 уровня или с одноручным. Священный удар и Печать повиновения растут от урона оружия, поэтому из двух похожих берите более медленное.', 'Seal of Command with a slow two-hander, Seal of Righteousness before level 20 or with a one-hander. Holy Strike and Seal of Command scale with weapon damage, so of two similar weapons take the slower one.', 'Seal of Command з повільною дворучною зброєю, Seal of Righteousness до 20 рівня або з одноручною. Holy Strike і Seal of Command ростуть від шкоди зброї, тому з двох схожих беріть повільнішу.')]},
                {'id': 'q3', 'q': t('Можно ли качаться за Свет?', 'Can I level as Holy?', 'Чи можна прокачуватися за Світло?'),
                 'a': [t('Можно: Warcraft Tavern называет такой Свет неожиданно сильным с экипировкой на силу заклинаний, но он раскрывается только после таланта Шок небес. Mobalytics и Icy Veins для соло советуют Воздаяние.', 'You can: Warcraft Tavern calls such a Holy surprisingly strong with spell power gear, but it opens up only after the Holy Shock talent. For solo, Mobalytics and Icy Veins recommend Retribution.', 'Можна: Warcraft Tavern називає такий Світло несподівано сильним зі спорядженням на силу заклинань, але він розкривається лише після таланту Holy Shock. Mobalytics та Icy Veins для соло радять Відплату.')]},
                {'id': 'q4', 'q': t('Ослабили ли Воздаяние?', 'Was Retribution nerfed?', 'Чи послабили Відплату?'),
                 'a': [t('Да, 15.10: Воитель Света и Освящение стали слабее. В тир-листе прокачки Паладин всё равно класс A.', 'Yes, on Oct 15: Champion of the Light and Consecration got weaker. In the leveling tier list Paladin is still an A class.', 'Так, 15 жовтня: Champion of the Light і Consecration стали слабшими. У тір-листі прокачування Паладин усе одно клас A.')]},
                {'id': 'q5', 'q': t('Где взять скакуна?', 'Where do I get a mount?', 'Де взяти скакуна?'),
                 'a': [t('На 40 уровне заданием класса, покупать скакуна не нужно.', 'At level 40 from a class quest; you don’t need to buy a mount.', 'На 40 рівні завданням класу, купувати скакуна не потрібно.')]},
            ]),
        ]},
        {'id': 'related', 'title': t('Смотрите также', 'See also', 'Дивіться також'), 'blocks': [
            ('tiles', _related('paladin', [
                t('Паладин', 'Paladin', 'Паладин'),
                tx('Прокачка 1–60', 'Leveling 1–60', 'Прокачування 1–60', fr='Monter de 1 à 60', it='Livellare 1–60', pt='Evoluir 1–60'),
                t('Лучшая раса', 'Best race', 'Найкраща раса'),
                t('Тир-лист', 'Tier list', 'Тір-лист'),
            ])),
        ]},
    ],
})

# ---------- hunter ----------

CLASS_GUIDES.append({
    'slug': 'leveling-hunter', 'art': 'hunter', 'hero': 'hero_leveling', 'hub': False,
    'title': t('Прокачка Охотника 1–60', 'Hunter Leveling 1–60', 'Прокачування Мисливця 1–60'),
    'lead': tx('Охотник — самый быстрый класс на прокачке, по оценке LFCarry, примерно на 8% быстрее среднего. Питомец держит врага, вы стреляете издалека. В Forever к нему добавились ястребы от таланта Призыв ястреба.', 'Hunter is the fastest class to level, about 8% faster than average by LFCarry’s estimate. The pet holds the enemy while you shoot from range. In Forever it gained hawks from the Summon Hawk talent.', 'Мисливець — найшвидший клас на прокачуванні, за оцінкою LFCarry, приблизно на 8% швидший за середній показник. Улюбленець утримує ворога, а ви стріляєте здалеку. У Forever до нього додалися яструби від таланту Summon Hawk.', de='Der Jäger ist die schnellste Klasse beim Leveln, laut Schätzung von LFCarry etwa 8 % schneller als der Durchschnitt. Der Begleiter hält den Gegner, du schießt aus der Ferne. In Forever kamen durch das Talent Summon Hawk Falken dazu.', es='El Cazador es la clase más rápida para subir de nivel, cerca de un 8 % más rápida que la media, según LFCarry. La mascota sujeta al enemigo y tú disparas desde lejos. En Forever se le añadieron halcones con el talento Summon Hawk.', fr='Le Chasseur est la classe la plus rapide à monter, environ 8 % de mieux que la moyenne selon LFCarry. Le familier retient l’ennemi pendant que vous tirez à distance. Dans Forever, des faucons se sont ajoutés grâce au talent Summon Hawk.', it='Il Cacciatore è la classe più veloce a livellare, circa l’8% più della media secondo LFCarry. L’animale trattiene il nemico mentre tu spari da lontano. In Forever si sono aggiunti i falchi con il talento Summon Hawk.', pl='Hunter to najszybsza klasa do levelowania, według szacunku LFCarry mniej więcej o 8% szybsza od średniej. Pet trzyma wroga, a wy strzelacie z daleka. W Forever doszły do tego jastrzębie z talentu Summon Hawk.', pt='O Caçador é a classe mais rápida para subir de nível, cerca de 8% mais rápida que a média, segundo o LFCarry. O pet segura o inimigo enquanto você atira de longe. No Forever ele ganhou falcões com o talento Summon Hawk.'),
    'tile': t('Повелитель зверей, питомец и таланты', 'Beast Mastery, pet and talents', 'Володіння звірами, улюбленець і таланти'),
    'pills': [t('Спек: Повелитель зверей', 'Spec: Beast Mastery', 'Спек: Володіння звірами'), t('Таланты 10–60', 'Talents 10–60', 'Таланти 10–60'), tx('По бете', 'Beta data', 'За бетою', de='Betadaten', fr='Données de la bêta', pt='Dados da beta')],
    'sources': [
        ('Icy Veins: Beast Mastery Hunter Leveling', 'https://www.icy-veins.com/wow-forever/beast-mastery-hunter-leveling'),
        ('Mobalytics: Hunter Leveling 1-30', 'https://mobalytics.gg/wow-forever/classes/hunter-leveling-guide'),
        ('Warcraft Tavern: Hunter Leveling', 'https://www.warcrafttavern.com/forever/guides/hunter-leveling/'),
        ('Warcraft Tavern: Best Hunter Pets', 'https://www.warcrafttavern.com/forever/guides/best-hunter-pets/'),
    ],
    'sections': [
        {'id': 'spec', 'title': t('Какой спек качать', 'Which spec to level', 'Який спек прокачувати'), 'blocks': [
            ('text', [
                t('Качайте Повелителя зверей. Здесь сходятся Warcraft Tavern, Mobalytics и Icy Veins: таланты усиливают питомца, он дольше живёт и держит угрозу, а вы почти не прерываетесь на отдых. В тир-листе прокачки это S.', 'Level Beast Mastery. Warcraft Tavern, Mobalytics and Icy Veins agree here: the talents strengthen the pet, it lives longer and holds threat, and you hardly stop to rest. In the leveling tier list it is S.', 'Прокачуйте Володіння звірами. Тут сходяться Warcraft Tavern, Mobalytics та Icy Veins: таланти підсилюють улюбленця, він довше живе й тримає загрозу, а ви майже не перериваєтеся на відпочинок. У тір-листі прокачування це S.'),
            ]),
            ('table', {'head': [tx('Спек', 'Spec', 'Спек', de='Skillung', es='Espec.', fr='Spé', it='Spec.', pl='Spec', pt='Espec.'), t('Когда брать', 'When to take it', 'Коли брати'), t('Минус', 'Downside', 'Мінус')], 'rows': [
                [t('Повелитель зверей', 'Beast Mastery', 'Володіння звірами'), t('Соло, весь путь до 60', 'Solo, the whole way to 60', 'Соло, увесь шлях до 60'), t('Мало урона по площади', 'Little area damage', 'Мало шкоди по площі')],
                [t('Стрельба', 'Marksmanship', 'Стрільба'), t('Группы и подземелья', 'Groups and dungeons', 'Групи та підземелля'), t('Соло медленнее; Одинокий волк без питомца на прокачке Tavern не советует', 'Slower solo; Tavern does not recommend Lone Wolf without a pet for leveling', 'Соло повільніше; Lone Wolf без улюбленця на прокачуванні Tavern не радить')],
                [t('Выживание', 'Survival', 'Виживання'), t('Любителям ближнего боя и ловушек', 'Fans of melee and traps', 'Тим, хто любить ближній бій і пастки'), t('На бете у талантов были ошибки', 'The talents had bugs on the beta', 'У беті таланти мали помилки')],
            ]}),
        ]},
        {'id': 'talents', 'title': t('Таланты по уровням', 'Talents by level', 'Таланти за рівнями'), 'blocks': [
            ('text', [
                t('Порядок Icy Veins (обновлён 17.10). Mobalytics (18.10) до 30 уровня берёт те же таланты в другом порядке. Уровни 31–60 на бете закрыты: это план источника, проверим после старта 05.11.', 'Icy Veins order (updated Oct 17). Mobalytics (Oct 18) takes the same talents up to level 30 in a different order. Levels 31–60 are closed on the beta: this is the source’s plan, and we will check it after the Nov 4–5 launch.', 'Порядок Icy Veins (оновлено 17 жовтня). Mobalytics (18 жовтня) до 30 рівня бере ті самі таланти в іншому порядку. Рівні 31–60 у беті закриті: це план джерела, перевіримо після старту 5 листопада.'),
            ]),
            ('table', {'head': [t('Уровни', 'Levels', 'Рівні'), t('Талант', 'Talent', 'Талант'), t('Очки', 'Points', 'Очки')], 'rows': [
                ['10–14', 'Deadly Aspects', '5'],
                ['15–16', t('Знание троп (Pathfinding)', 'Pathfinding', 'Pathfinding'), '2'],
                ['17–18', t('Улучшенное воскрешение питомца (Improved Revive Pet)', 'Improved Revive Pet', 'Improved Revive Pet'), '2'],
                ['19', t('Направленный огонь (Focused Fire)', 'Focused Fire', 'Focused Fire'), '1'],
                ['20', t('Звериная стремительность (Bestial Swiftness)', 'Bestial Swiftness', 'Bestial Swiftness'), '1'],
                ['21–24', t('Неудержимое неистовство (Unleashed Fury)', 'Unleashed Fury', 'Unleashed Fury'), '4'],
                ['25', t('Призыв ястреба (Summon Hawk)', 'Summon Hawk', 'Summon Hawk'), '1'],
                ['26', t('Неудержимое неистовство (Unleashed Fury)', 'Unleashed Fury', 'Unleashed Fury'), '5/5'],
                ['27–29', t('Свирепость (Ferocity)', 'Ferocity', 'Ferocity'), '3'],
                ['30', t('Устрашение (Intimidation)', 'Intimidation', 'Intimidation'), '1'],
                ['31–32', t('Беспрекословное послушание (Bestial Discipline)', 'Bestial Discipline', 'Bestial Discipline'), '2'],
                ['33–34', t('Свирепость (Ferocity)', 'Ferocity', 'Ferocity'), '5/5'],
                ['35–39', t('Бешенство (Frenzy)', 'Frenzy', 'Frenzy'), '5'],
                ['40', t('Звериный гнев (Bestial Wrath)', 'Bestial Wrath', 'Bestial Wrath'), '1'],
                ['41–45', 'Lethal Attacks', '5'],
                ['46–50', t('Верная цель (Careful Aim)', 'Careful Aim', 'Careful Aim'), '5'],
                ['51', t('Направленный огонь (Focused Fire)', 'Focused Fire', 'Focused Fire'), '2/2'],
                ['52–56', t('Тренировка стойкости (Endurance Training)', 'Endurance Training', 'Endurance Training'), '5'],
                ['57–58', t('Узы духа (Spirit Bond)', 'Spirit Bond', 'Spirit Bond'), '2'],
                ['59–60', t('Глаз ястреба (Hawk Eye)', 'Hawk Eye', 'Hawk Eye'), '2'],
            ]}),
            ('tip', t('Перк Legacy Talented даёт таланты до 5 уровней раньше: порядок тот же. По Mobalytics, Призыв ястреба позволяет держать двух ястребов сразу.', 'The Legacy Talented perk gives talents up to 5 levels earlier: the order is the same. According to Mobalytics, Summon Hawk lets you keep two hawks at once.', 'Перк Legacy Talented дає таланти до 5 рівнів раніше: порядок той самий. За Mobalytics, Summon Hawk дозволяє тримати двох яструбів одночасно.')),
        ]},
        {'id': 'pet', 'title': t('Питомец', 'Pet', 'Улюбленець'), 'blocks': [
            ('text', [
                bt(t('Приручение открывается на 10 уровне заданием класса в стартовой зоне. Warcraft Tavern советует для прокачки кошку (быстрые атаки, высокий урон) или кабана (крепче, Рывок быстро набирает угрозу). В Forever появилось новое семейство — лисы, у многих зверей новые способности. Питомец получает баффы лагеря, если призвать его у костра.', 'Taming opens at level 10 through a class quest in the starting zone. For leveling, Warcraft Tavern recommends a cat (fast attacks, high damage) or a boar (sturdier, Charge builds threat quickly). Forever added a new family, foxes, and many beasts have new abilities. The pet gets camp buffs if you summon it at the campfire.', 'Приборкання відкривається на 10 рівні завданням класу в стартовій зоні. Warcraft Tavern радить для прокачування кішку (швидкі атаки, висока шкода) або кабана (витриваліший, Charge швидко набирає загрозу). У Forever з’явилася нова родина — лисиці, а в багатьох звірів нові здібності. Улюбленець отримує бафи табору, якщо прикликати його біля багаття.'), 1),
            ]),
        ]},
        {'id': 'abilities', 'title': t('Способности и тренер', 'Abilities and trainer', 'Здібності й тренер'), 'blocks': [
            ('text', [BETA_TRAINER]),
            ('table', {'head': [t('Уровень', 'Level', 'Рівень'), t('Что взять', 'What to take', 'Що взяти'), tx('Зачем', 'Why', 'Навіщо', de='Wozu', es='Para qué', it='A cosa serve', pl='Po co', pt='Para quê')], 'rows': [
                ['4', t('Укус змеи, Дух обезьяны', 'Serpent Sting, Aspect of the Monkey', 'Serpent Sting, Aspect of the Monkey'), t('Яд на цель, уклонение вблизи', 'A poison on the target, dodge in melee', 'Отрута на ціль, ухилення зблизька')],
                ['6', t('Чародейский выстрел, Метка охотника', "Arcane Shot, Hunter's Mark", "Arcane Shot, Hunter's Mark"), t('Мгновенный выстрел', 'An instant shot', 'Миттєвий постріл')],
                ['8', t('Шокирующий выстрел', 'Concussive Shot', 'Concussive Shot'), t('Замедление', 'A slow', 'Уповільнення')],
                ['10', t('Приручение зверя (задание), Дух ястреба', 'Tame Beast (quest), Aspect of the Hawk', 'Tame Beast (завдання), Aspect of the Hawk'), t('Питомец и урон дальнего боя', 'A pet and ranged damage', 'Улюбленець і шкода здалеку')],
                ['12', t('Лечение питомца, Подрезать крылья', 'Mend Pet, Wing Clip', 'Mend Pet, Wing Clip'), t('Лечение зверя, уйти из ближнего боя', 'Heal the beast, get out of melee', 'Лікування звіра, вийти з ближнього бою')],
                ['18', t('Залп', 'Multi-Shot', 'Multi-Shot'), t('Несколько целей', 'Several targets', 'Кілька цілей')],
                ['20', t('Прицельный выстрел, Дух гепарда, Замораживающая ловушка; древковое у тренера оружия', 'Aimed Shot, Aspect of the Cheetah, Freezing Trap; polearms from the weapon trainer', 'Aimed Shot, Aspect of the Cheetah, Freezing Trap; держакова зброя в тренера зброї'), t('Сильный выстрел, скорость, контроль', 'A strong shot, speed, control', 'Сильний постріл, швидкість, контроль')],
                ['26', t('Быстрая стрельба', 'Rapid Fire', 'Rapid Fire'), t('Окно урона', 'A damage window', 'Вікно шкоди')],
                ['28', t('Ледяная ловушка', 'Frost Trap', 'Frost Trap'), t('Замедление по площади', 'An area slow', 'Уповільнення по площі')],
                ['30', t('Притвориться мертвым', 'Feign Death', 'Feign Death'), t('Сбросить бой', 'Drop combat', 'Скинути бій')],
                ['40', t('Дух стаи, верховая езда, вторая специализация', 'Aspect of the Pack, riding, dual specialization', 'Aspect of the Pack, верхова їзда, друга спеціалізація'), t('Скорость группы', 'Group speed', 'Швидкість групи')],
            ]}),
            ('steps', [
                {'t': t('Перед боем', 'Before the fight', 'Перед боєм'),
                 'd': t('Дух ястреба, питомец идёт к врагу первым и делает пару ударов.', 'Aspect of the Hawk; the pet goes at the enemy first and lands a couple of hits.', 'Aspect of the Hawk, улюбленець іде до ворога першим і завдає кілька ударів.')},
                {'t': t('Вход', 'Opening', 'Вхід'),
                 'd': t('Автоматическая стрельба, затем Укус змеи.', 'Auto Shot, then Serpent Sting.', 'Auto Shot, потім Serpent Sting.')},
                {'t': t('В бою', 'In the fight', 'У бою'),
                 'd': t('Призыв ястреба по откату, Прицельный выстрел и Быстрая стрельба по откату, Чародейский выстрел при лишней мане.', 'Summon Hawk on cooldown, Aimed Shot and Rapid Fire on cooldown, Arcane Shot when you have spare mana.', 'Summon Hawk за відкатом, Aimed Shot і Rapid Fire за відкатом, Arcane Shot за зайвої мани.')},
                {'t': t('Если враг пошёл на вас', 'If the enemy comes at you', 'Якщо ворог пішов на вас'),
                 'd': t('Подрезать крылья, Шокирующий выстрел или Ледяная ловушка, пока питомец не вернёт угрозу.', 'Wing Clip, Concussive Shot or Frost Trap until the pet takes the threat back.', 'Wing Clip, Concussive Shot або Frost Trap, доки улюбленець не поверне загрозу.')},
            ]),
            ('text', [
                t('Не стреляйте раньше танка: питомец и вы легко забираете угрозу. Замораживающая ловушка — надёжный контроль одной цели.', 'Don’t shoot before the tank: the pet and you take threat easily. Freezing Trap is reliable control of a single target.', 'Не стріляйте раніше за танка: улюбленець і ви легко забираєте загрозу. Freezing Trap — надійний контроль однієї цілі.'),
            ]),
        ]},
        {'id': 'play', 'title': t('Соло, вдвоём, в группе', 'Solo, duo, group', 'Соло, удвох, у групі'), 'blocks': [
            ('tabs', [
                {'id': 'solo', 't': tx('Соло', 'Solo', 'Соло', es='En solitario', pt='Solo'), 'blocks': [('text', [bt(t('Убивайте врагов по одному: питомец плохо держит нескольких, а урон по площади снимет угрозу с него. До 10 уровня питомца нет: стреляйте, отходите, вблизи добивайте врага (Удар ящера). Всегда держите запас стрел или пуль и воды. Если всё плохо — Притвориться мертвым, потом вернитесь с живым питомцем.', 'Kill enemies one at a time: the pet holds several poorly, and area damage will pull threat off it. Until level 10 you have no pet: shoot, step back, and finish the enemy in melee (Raptor Strike). Always keep a reserve of arrows or bullets and water. If it goes badly, Feign Death, then come back with the pet alive.', 'Убивайте ворогів по одному: улюбленець погано тримає кількох, а шкода по площі зніме з нього загрозу. До 10 рівня улюбленця немає: стріляйте, відходьте, зблизька добивайте ворога (Raptor Strike). Завжди майте запас стріл чи куль і воду. Якщо все погано — Feign Death, потім повертайтеся з живим улюбленцем.'), 2)])]},
                {'id': 'duo', 't': tx('Вдвоём', 'Duo', 'Удвох', de='Zu zweit', es='En pareja', fr='À deux', it='In coppia', pl='We dwoje', pt='Em dupla'), 'blocks': [('text', [t('С любым напарником: питомец может держать врага для пары без танка. Не отправляйте его на цель, которую танкует напарник.', 'With any partner: the pet can hold an enemy for a pair without a tank. Don’t send it at a target your partner is tanking.', 'З будь-яким напарником: улюбленець може тримати ворога для пари без танка. Не посилайте його на ціль, яку танкує напарник.')])]},
                {'id': 'party', 't': t('Группа', 'Group', 'Група'), 'blocks': [('text', [t('Дух стаи ускоряет группу в пути, но ошеломляет любого, по кому попадёт враг (Warcraft Tavern). В бою выключайте.', 'Aspect of the Pack speeds up the group on the road, but dazes anyone the enemy hits (Warcraft Tavern). Turn it off in combat.', 'Aspect of the Pack прискорює групу в дорозі, але ошелешує будь-кого, по кому влучить ворог (Warcraft Tavern). У бою вимикайте.')])]},
            ]),
        ]},
        {'id': 'gear', 'title': t('Характеристики и снаряжение', 'Stats and gear', 'Характеристики та спорядження'), 'blocks': [
            ('text', [
                t("Главное — оружие дальнего боя и запас патронов. Warcraft Tavern перечисляет оружие до 30 уровня: Barbaric Crossbow (13–16), Venomstrike (19–22), Naga Heartpiercer (22–29), Fallenroot Longbow (23–29), Quilboar Blaster (29–30), Master Hunter's Bow (30). Дух полезен с талантом Беспрекословное послушание: быстрее восполняет ману.", "The main thing is a ranged weapon and a supply of ammo. Warcraft Tavern lists weapons up to level 30: Barbaric Crossbow (13–16), Venomstrike (19–22), Naga Heartpiercer (22–29), Fallenroot Longbow (23–29), Quilboar Blaster (29–30), Master Hunter's Bow (30). Spirit is useful with the Bestial Discipline talent: it restores mana faster.", "Головне — зброя дальнього бою й запас набоїв. Warcraft Tavern перелічує зброю до 30 рівня: Barbaric Crossbow (13–16), Venomstrike (19–22), Naga Heartpiercer (22–29), Fallenroot Longbow (23–29), Quilboar Blaster (29–30), Master Hunter's Bow (30). Дух корисний із талантом Bestial Discipline: швидше відновлює ману."),
                t('Пары профессий под класс и объекты лагеря — в гайде по профессиям.', 'Profession pairings for the class and camp objects are in the professions guide.', 'Пари професій під клас і об’єкти табору — у гайді з професій.'),
            ]),
        ]},
        {'id': 'forever', 'title': t('Чем Forever отличается от Classic', 'How Forever differs from Classic', 'Чим Forever відрізняється від Classic'), 'blocks': [
            ('table', {'head': [t('Что', 'What', 'Що'), t('В Forever', 'In Forever', 'У Forever')], 'rows': [
                [t('Призыв ястреба', 'Summon Hawk', 'Summon Hawk'), t('Новый талант Повелителя зверей: ястребы бьют вместе с питомцем.', 'A new Beast Mastery talent: hawks attack together with the pet.', 'Новий талант Володіння звірами: яструби б’ють разом з улюбленцем.')],
                [t('Питомец', 'Pet', 'Улюбленець'), t('Получает 10% вашей силы атаки. Новое семейство: лисы.', 'Gets 10% of your attack power. A new family: foxes.', 'Отримує 10% вашої сили атаки. Нова родина: лисиці.')],
                [t('Ловушки', 'Traps', 'Пастки'), t('Ставятся в бою.', 'Can be set in combat.', 'Ставляться в бою.')],
                [t('Одинокий волк', 'Lone Wolf', 'Lone Wolf'), t('Новый талант Стрельбы: урон без питомца.', 'A new Marksmanship talent: damage without a pet.', 'Новий талант Стрільби: шкода без улюбленця.')],
                [t('Выживание', 'Survival', 'Виживання'), t('Может уходить в ближний бой: новые таланты Strider Kick, Expose Prey.', 'Can go into melee: new talents Strider Kick, Expose Prey.', 'Може йти в ближній бій: нові таланти Strider Kick, Expose Prey.')],
                [t('Выслеживание', 'Tracking', 'Вистежування'), t('Улучшенное выслеживание вместо талантов против отдельных типов врагов.', 'Improved tracking instead of talents against individual enemy types.', 'Покращене вистежування замість талантів проти окремих типів ворогів.')],
                [t('Вторая специализация', 'Dual specialization', 'Друга спеціалізація'), t('С 40 уровня.', 'From level 40.', 'З 40 рівня.')],
            ]}),
        ]},
        {'id': 'faq', 'title': t('Вопросы', 'Questions', 'Питання'), 'blocks': [
            ('faq', [
                {'id': 'q1', 'q': t('Какой спек Охотника лучший для прокачки в WoW Forever?', 'Which Hunter spec is best for leveling in WoW Forever?', 'Який спек Мисливця найкращий для прокачування у WoW Forever?'),
                 'a': [t('Повелитель зверей: его советуют Warcraft Tavern, Mobalytics и Icy Veins. Стрельба сильнее в группах.', 'Beast Mastery: Warcraft Tavern, Mobalytics and Icy Veins recommend it. Marksmanship is stronger in groups.', 'Володіння звірами: його радять Warcraft Tavern, Mobalytics та Icy Veins. Стрільба сильніша в групах.')]},
                {'id': 'q2', 'q': t('Какого питомца взять?', 'Which pet should I take?', 'Якого улюбленця взяти?'),
                 'a': [t('Для прокачки кошку или кабана (Warcraft Tavern). Кошка бьёт сильнее, кабан крепче.', 'For leveling, a cat or a boar (Warcraft Tavern). The cat hits harder, the boar is sturdier.', 'Для прокачування кішку або кабана (Warcraft Tavern). Кішка б’є сильніше, кабан витриваліший.')]},
                {'id': 'q3', 'q': t('Когда появляется питомец?', 'When do I get a pet?', 'Коли з’являється улюбленець?'),
                 'a': [bt(t('На 10 уровне, после задания класса в стартовой зоне.', 'At level 10, after the class quest in the starting zone.', 'На 10 рівні, після завдання класу в стартовій зоні.'), 1)]},
                {'id': 'q4', 'q': t('Нужен ли Охотнику бой вблизи?', 'Does a Hunter need melee?', 'Чи потрібен Мисливцю ближній бій?'),
                 'a': [t('На прокачке почти нет: питомец держит врага. Вблизи выручают Удар ящера, Подрезать крылья и Дух обезьяны.', 'Almost not while leveling: the pet holds the enemy. Raptor Strike, Wing Clip and Aspect of the Monkey help in melee.', 'На прокачуванні майже ні: улюбленець тримає ворога. Зблизька виручають Raptor Strike, Wing Clip та Aspect of the Monkey.')]},
                {'id': 'q5', 'q': t('Почему Охотник так быстро качается?', 'Why does a Hunter level so fast?', 'Чому Мисливець так швидко прокачується?'),
                 'a': [t('Он убивает почти без отдыха: питомец танкует, мана тратится мало. По LFCarry Охотник примерно на 8% быстрее среднего.', 'It kills with almost no rest: the pet tanks and mana is used sparingly. By LFCarry’s estimate, Hunter is about 8% faster than average.', 'Він убиває майже без відпочинку: улюбленець танкує, а мана витрачається мало. За LFCarry, Мисливець приблизно на 8% швидший за середній показник.')]},
            ]),
        ]},
        {'id': 'related', 'title': t('Смотрите также', 'See also', 'Дивіться також'), 'blocks': [
            ('tiles', _related('hunter', [
                t('Охотник', 'Hunter', 'Мисливець'),
                tx('Прокачка 1–60', 'Leveling 1–60', 'Прокачування 1–60', fr='Monter de 1 à 60', it='Livellare 1–60', pt='Evoluir 1–60'),
                t('Лучшая раса', 'Best race', 'Найкраща раса'),
                t('Тир-лист', 'Tier list', 'Тір-лист'),
            ])),
        ]},
    ],
})

# ---------- rogue ----------

CLASS_GUIDES.append({
    'slug': 'leveling-rogue', 'art': 'rogue', 'hero': 'hero_leveling', 'hub': False,
    'title': t('Прокачка Разбойника 1–60', 'Rogue Leveling 1–60', 'Прокачування Розбійника 1–60'),
    'lead': t('Разбойник качается в среднем темпе: сильный урон по одной цели и скрытность, но нет урона по площади и самолечения. В Forever энергия восстанавливается ровнее, а оружие можно выбирать свободнее.', 'Rogue levels at an average pace: strong single-target damage and stealth, but no area damage and no self-healing. In Forever energy regenerates more smoothly, and you can choose weapons more freely.', 'Розбійник прокачується в середньому темпі: сильна шкода по одній цілі й непомітність, але немає шкоди по площі та самолікування. У Forever енергія відновлюється рівніше, а зброю можна обирати вільніше.'),
    'tile': t('Бой, яды и таланты по уровням', 'Combat, poisons and talents by level', 'Бій, отрути й таланти за рівнями'),
    'pills': [t('Спек: Бой', 'Spec: Combat', 'Спек: Бій'), t('Таланты 10–60', 'Talents 10–60', 'Таланти 10–60'), tx('По бете', 'Beta data', 'За бетою', de='Betadaten', fr='Données de la bêta', pt='Dados da beta')],
    'sources': [
        ('Icy Veins: Combat Rogue Leveling', 'https://www.icy-veins.com/wow-forever/combat-rogue-leveling'),
        ('Mobalytics: Rogue Leveling 1-30', 'https://mobalytics.gg/wow-forever/classes/rogue-leveling-guide'),
        ('Warcraft Tavern: Rogue Leveling', 'https://www.warcrafttavern.com/forever/guides/rogue-leveling/'),
    ],
    'sections': [
        {'id': 'spec', 'title': t('Какой спек качать', 'Which spec to level', 'Який спек прокачувати'), 'blocks': [
            ('text', [
                t('Качайте Бой. Его советуют Mobalytics и Icy Veins: Ответный удар и защита талантами держат вас в бою без отдыха, а с 30 уровня Шквал клинков бьёт двух врагов сразу. В подземельях Бой тоже самый надёжный спек.', 'Level Combat. Mobalytics and Icy Veins recommend it: Riposte and defensive talents keep you in the fight without rest, and from level 30 Blade Flurry hits two enemies at once. In dungeons, Combat is also the most reliable spec.', 'Прокачуйте Бій. Його радять Mobalytics та Icy Veins: Riposte і захист талантами тримають вас у бою без відпочинку, а з 30 рівня Blade Flurry б’є двох ворогів одразу. У підземеллях Бій теж найнадійніший спек.'),
                t('Warcraft Tavern не выбирает одну ветку: Ликвидацию не советует для старта (сильна, когда есть Расправа, но хрупкая), Скрытность хороша на открытие из засады, но слабее в подземельях. Тир-лист прокачки ставит Разбойнику B за Ликвидацию или Бой.', 'Warcraft Tavern doesn’t pick one tree: it advises against Assassination as a start (strong once you have Mutilate, but fragile), and Subtlety is good for an ambush opener but weaker in dungeons. The leveling tier list gives Rogue a B for Assassination or Combat.', 'Warcraft Tavern не обирає одну гілку: Вбивство для старту не радить (сильне, коли є Mutilate, але тендітне), Непомітність добра для відкриття із засідки, але слабша в підземеллях. Тір-лист прокачування ставить Розбійнику B за Вбивство або Бій.'),
            ]),
            ('table', {'head': [tx('Спек', 'Spec', 'Спек', de='Skillung', es='Espec.', fr='Spé', it='Spec.', pl='Spec', pt='Espec.'), t('Когда брать', 'When to take it', 'Коли брати'), t('Минус', 'Downside', 'Мінус')], 'rows': [
                [t('Бой', 'Combat', 'Бій'), t('Соло и подземелья, весь путь до 60', 'Solo and dungeons, the whole way to 60', 'Соло та підземелля, увесь шлях до 60'), t('До 30 уровня (Шквал клинков) слаб против нескольких врагов', 'Weak against several enemies until level 30 (Blade Flurry)', 'До 30 рівня (Blade Flurry) слабкий проти кількох ворогів')],
                [t('Ликвидация', 'Assassination', 'Вбивство'), t('С 30 уровня, когда есть Расправа и кинжалы', 'From level 30, once you have Mutilate and daggers', 'З 30 рівня, коли є Mutilate і кинджали'), t('Меньше выживаемости', 'Less survivability', 'Менша виживаність')],
                [t('Скрытность', 'Subtlety', 'Непомітність'), t('Открытие из засады, PvP', 'An ambush opener, PvP', 'Відкриття із засідки, PvP'), t('Слабее в подземельях', 'Weaker in dungeons', 'Слабша в підземеллях')],
            ]}),
        ]},
        {'id': 'talents', 'title': t('Таланты по уровням', 'Talents by level', 'Таланти за рівнями'), 'blocks': [
            ('text', [
                t('Порядок Icy Veins для Боя (обновлён 17.10). Mobalytics (18.10) до 30 уровня почти тот же. Уровни 31–60 на бете закрыты: это план источника, проверим после старта 05.11.', 'Icy Veins order for Combat (updated Oct 17). Mobalytics (Oct 18) is almost the same up to level 30. Levels 31–60 are closed on the beta: this is the source’s plan, and we will check it after the Nov 4–5 launch.', 'Порядок Icy Veins для Бою (оновлено 17 жовтня). Mobalytics (18 жовтня) до 30 рівня майже той самий. Рівні 31–60 у беті закриті: це план джерела, перевіримо після старту 5 листопада.'),
            ]),
            ('table', {'head': [t('Уровни', 'Levels', 'Рівні'), t('Талант', 'Talent', 'Талант'), t('Очки', 'Points', 'Очки')], 'rows': [
                ['10–11', t('Улучшенный коварный удар (Improved Sinister Strike)', 'Improved Sinister Strike', 'Improved Sinister Strike'), '2'],
                ['12–14', t('Улучшенное потрошение (Improved Eviscerate)', 'Improved Eviscerate', 'Improved Eviscerate'), '3'],
                ['15–16', t('Точность (Precision)', 'Precision', 'Precision'), '2'],
                ['17–19', t('Отражение (Deflection)', 'Deflection', 'Deflection'), '3'],
                ['20', t('Ответный удар (Riposte)', 'Riposte', 'Riposte'), '1'],
                ['21', t('Точность (Precision)', 'Precision', 'Precision'), '3/3'],
                ['22–23', tx('Закалка (Endurance)', 'Endurance', 'Endurance', de='Durchhaltevermögen (Endurance)', es='Robustez (Endurance)', fr='Endurcissement (Endurance)', it='Vigore (Endurance)', pt='Resistência (Endurance)'), '2'],
                ['24', t('Молниеносные рефлексы (Lightning Reflexes)', 'Lightning Reflexes', 'Lightning Reflexes'), '1'],
                ['25', t('Безупречное исполнение (Flawless Execution)', 'Flawless Execution', 'Flawless Execution'), '1'],
                ['26–29', t('Специализация на бое двумя оружиями (Dual Wield Specialization)', 'Dual Wield Specialization', 'Dual Wield Specialization'), '4'],
                ['30', t('Шквал клинков (Blade Flurry)', 'Blade Flurry', 'Blade Flurry'), '1'],
                ['31–34', t('Круши-руби (Hack and Slash)', 'Hack and Slash', 'Hack and Slash'), '4'],
                ['35–36', t('Оружейное мастерство (Weapon Expertise)', 'Weapon Expertise', 'Weapon Expertise'), '2'],
                ['37–39', t('Агрессивность (Aggression)', 'Aggression', 'Aggression'), '3'],
                ['40', t('Выброс адреналина (Adrenaline Rush)', 'Adrenaline Rush', 'Adrenaline Rush'), '1'],
                ['41', t('Круши-руби (Hack and Slash)', 'Hack and Slash', 'Hack and Slash'), '5/5'],
                ['42', t('Специализация на бое двумя оружиями (Dual Wield Specialization)', 'Dual Wield Specialization', 'Dual Wield Specialization'), '5/5'],
                ['43–47', t('Злоба (Malice)', 'Malice', 'Malice'), '5'],
                ['48–50', t('Жестокость (Ruthlessness)', 'Ruthlessness', 'Ruthlessness'), '3'],
                ['51–52', t('Убийство (Murder)', 'Murder', 'Murder'), '2'],
                ['53', t('Неослабевающие удары (Relentless Strikes)', 'Relentless Strikes', 'Relentless Strikes'), '1'],
                ['54–57', t('Смертоносность (Lethality)', 'Lethality', 'Lethality'), '4'],
                ['58', t('Хладнокровие (Cold Blood)', 'Cold Blood', 'Cold Blood'), '1'],
                ['59–60', t('Тлетворные яды (Vile Poisons)', 'Vile Poisons', 'Vile Poisons'), '2'],
            ]}),
            ('tip', t('Mobalytics не берёт Молниеносные рефлексы и Безупречное исполнение: вместо них Улучшенный спринт и Специализация на бое двумя оружиями 5/5 до 30 уровня. Перк Legacy Talented даёт таланты до 5 уровней раньше.', 'Mobalytics does not take Lightning Reflexes and Flawless Execution: instead it takes Improved Sprint and Dual Wield Specialization 5/5 before level 30. The Legacy Talented perk gives talents up to 5 levels earlier.', 'Mobalytics не бере Lightning Reflexes і Flawless Execution: замість них Improved Sprint та Dual Wield Specialization 5/5 до 30 рівня. Перк Legacy Talented дає таланти до 5 рівнів раніше.')),
        ]},
        {'id': 'abilities', 'title': t('Способности и тренер', 'Abilities and trainer', 'Здібності й тренер'), 'blocks': [
            ('text', [BETA_TRAINER]),
            ('table', {'head': [t('Уровень', 'Level', 'Рівень'), t('Что взять', 'What to take', 'Що взяти'), tx('Зачем', 'Why', 'Навіщо', de='Wozu', es='Para qué', it='A cosa serve', pl='Po co', pt='Para quê')], 'rows': [
                ['1', t('Коварный удар, Потрошение, Незаметность', 'Sinister Strike, Eviscerate, Stealth', 'Sinister Strike, Eviscerate, Stealth'), t('Приём серии и завершающий удар', 'A combo point builder and a finisher', 'Прийом серії й завершальний удар')],
                ['4', t('Удар в спину', 'Backstab', 'Backstab'), t('Сильный удар кинжалом со спины', 'A strong dagger strike from behind', 'Сильний удар кинджалом у спину')],
                ['6', t('Парализующий удар', 'Gouge', 'Gouge'), t('Выиграть время на энергию или бинт', 'Buy time for energy or a bandage', 'Виграти час на енергію чи бинт')],
                ['8', t('Ускользание', 'Evasion', 'Evasion'), t('Спасение в бою', 'An escape in combat', 'Порятунок у бою')],
                ['10', t('Мясорубка, Ошеломление, Спринт', 'Slice and Dice, Sap, Sprint', 'Slice and Dice, Sap, Sprint'), t('Скорость атаки, контроль, бег', 'Attack speed, control, running', 'Швидкість атаки, контроль, біг')],
                ['12', tx('Пинок', 'Kick', 'Kick', de='Tritt', es='Patada', fr='Coup de pied', it='Calcio', pl='Kick', pt='Chute'), t('Прерывание', 'An interrupt', 'Переривання')],
                ['20', t('Яды (задание класса)', 'Poisons (class quest)', 'Отрути (завдання класу)'), t('Постоянная прибавка к урону', 'A permanent damage boost', 'Постійна надбавка до шкоди')],
                ['22', t('Исчезновение', 'Vanish', 'Vanish'), t('Выйти из боя', 'Leave combat', 'Вийти з бою')],
                ['26', t('Подлый трюк', 'Cheap Shot', 'Cheap Shot'), t('Оглушение из скрытности, 2 очка серии', 'A stun from stealth, 2 combo points', 'Приголомшення з непомітності, 2 бали серії')],
                ['30', t('Удар по почкам', 'Kidney Shot', 'Kidney Shot'), t('Оглушение в бою', 'A stun in combat', 'Приголомшення в бою')],
                ['34', t('Ослепление', 'Blind', 'Blind'), t('Убрать врага из боя', 'Take an enemy out of the fight', 'Прибрати ворога з бою')],
                ['40', t('Верховая езда, вторая специализация', 'Riding, dual specialization', 'Верхова їзда, друга спеціалізація'), '—'],
            ]}),
            ('steps', [
                {'t': t('Вход', 'Opening', 'Вхід'),
                 'd': t('обычно без скрытности, сразу Коварный удар: так быстрее. На сильном враге — Незаметность и Подлый трюк.', 'usually without stealth, straight to Sinister Strike: it is faster. On a strong enemy, Stealth and Cheap Shot.', 'зазвичай без непомітності, одразу Sinister Strike: так швидше. На сильному ворогу — Stealth і Cheap Shot.')},
                {'t': t('В бою', 'In the fight', 'У бою'),
                 'd': t('Коварный удар до 3–5 очков серии, Ответный удар после парирования.', 'Sinister Strike up to 3–5 combo points, Riposte after a parry.', 'Sinister Strike до 3–5 балів серії, Riposte після парирування.')},
                {'t': t('Завершение', 'Finishing', 'Завершення'),
                 'd': t('Потрошение при 3+ очках или если враг почти мёртв. Мясорубка — только против нескольких врагов подряд.', 'Eviscerate at 3+ points or when the enemy is nearly dead. Slice and Dice only against several enemies in a row.', 'Eviscerate при 3+ балах або якщо ворог майже мертвий. Slice and Dice — лише проти кількох ворогів поспіль.')},
                {'t': t('Если тяжело', 'If it’s hard', 'Якщо важко'),
                 'd': t('Парализующий удар, Удар по почкам, Ослепление, Ускользание; с 30 уровня на двух врагах Шквал клинков.', 'Gouge, Kidney Shot, Blind, Evasion; from level 30, Blade Flurry on two enemies.', 'Gouge, Kidney Shot, Blind, Evasion; з 30 рівня на двох ворогах Blade Flurry.')},
            ]),
            ('text', [
                t('В подземельях на элитных врагах и боссах: Быстродействующий яд в правой руке, Смертельный яд в левой (Mobalytics). На прокачке и в коротких боях — Быстродействующий яд на обоих оружиях. Пинок сбивает опасные заклинания.', 'In dungeons on elites and bosses: Instant Poison in the main hand, Deadly Poison in the off hand (Mobalytics). For leveling and short fights, Instant Poison on both weapons. Kick stops dangerous spells.', 'У підземеллях на елітних ворогах і босах: Instant Poison у правій руці, Deadly Poison у лівій (Mobalytics). На прокачуванні й у коротких боях — Instant Poison на обох зброях. Kick збиває небезпечні заклинання.'),
            ]),
        ]},
        {'id': 'play', 'title': t('Соло, вдвоём, в группе', 'Solo, duo, group', 'Соло, удвох, у групі'), 'blocks': [
            ('tabs', [
                {'id': 'solo', 't': tx('Соло', 'Solo', 'Соло', es='En solitario', pt='Solo'), 'blocks': [('text', [t('Качайте Первую помощь: Ослепление или Парализующий удар, потом бинт — это быстрее еды. Держите запас порошков: они нужны для Ослепление и Исчезновение. В скрытности вы медленнее: подходите к обычным врагам открыто. Взламывайте замки: сундуки и сейфы дают материалы для ядов.', 'Level First Aid: Blind or Gouge, then a bandage — it is faster than eating. Keep a stock of powders: you need them for Blind and Vanish. You are slower in stealth: approach ordinary enemies openly. Pick locks: chests and safes give materials for poisons.', 'Прокачуйте Перша допомога: Blind або Gouge, потім бинт — це швидше за їжу. Тримайте запас порошків: вони потрібні для Blind та Vanish. У непомітності ви повільніші: до звичайних ворогів підходьте відкрито. Зламуйте замки: скрині й сейфи дають матеріали для отрут.')])]},
                {'id': 'duo', 't': tx('Вдвоём', 'Duo', 'Удвох', de='Zu zweit', es='En pareja', fr='À deux', it='In coppia', pl='We dwoje', pt='Em dupla'), 'blocks': [('text', [t('С лекарем или танком Разбойник раскрывается: можно бить в спину. Ошеломление и Ослепление снимают лишних врагов из боя.', 'With a healer or a tank the Rogue comes into its own: you can hit from behind. Sap and Blind take extra enemies out of the fight.', 'З цілителем чи танком Розбійник розкривається: можна бити в спину. Sap і Blind прибирають зайвих ворогів із бою.')])]},
                {'id': 'party', 't': t('Группа', 'Group', 'Група'), 'blocks': [('text', [t('Урона по площади мало, зато много контроля. С 30 уровня Шквал клинков закрывает пары врагов.', 'There is little area damage, but a lot of control. From level 30, Blade Flurry covers pairs of enemies.', 'Шкоди по площі мало, зате багато контролю. З 30 рівня Blade Flurry закриває пари ворогів.')])]},
            ]),
        ]},
        {'id': 'gear', 'title': t('Характеристики и снаряжение', 'Stats and gear', 'Характеристики та спорядження'), 'blocks': [
            ('text', [
                t('Mobalytics ставит ловкость первой (сила атаки, крит, уклонение), затем дух (восполнение здоровья), силу и выносливость. Warcraft Tavern к 60 поднимает шанс крита выше ловкости. Меняйте оружие при первой возможности: от него зависит почти весь урон. Новый тип оружия покачайте на слабых врагах.', 'Mobalytics puts Agility first (attack power, crit, dodge), then Spirit (health regeneration), Strength and Stamina. By 60, Warcraft Tavern raises crit chance above Agility. Swap weapons at the first chance: almost all your damage depends on them. Train a new weapon type on weak enemies.', 'Mobalytics ставить спритність першою (сила атаки, крит, ухилення), потім дух (відновлення здоров’я), силу й витривалість. До 60 Warcraft Tavern піднімає шанс крита вище за спритність. Міняйте зброю за першої нагоди: від неї залежить майже вся шкода. Новий тип зброї прокачайте на слабких ворогах.'),
                t('Профессии: Первая помощь обязательна. Взлом замков качайте по пути: сундуки дают материалы для ядов. Пары под класс и объекты лагеря — в гайде по профессиям.', 'Professions: First Aid is a must. Level lockpicking along the way: chests give materials for poisons. Class pairings and camp objects are in the professions guide.', 'Професії: Перша допомога обов’язкова. Злам замків качайте по дорозі: скрині дають матеріали для отрут. Пари під клас і об’єкти табору — у гайді з професій.'),
            ]),
        ]},
        {'id': 'weapons', 'title': t('Оружие по спекам', 'Weapons by spec', 'Зброя за спеками'), 'blocks': [
            ('text', [
                t('Ликвидация и Скрытность обычно берут кинжалы, Бою подходит любое оружие (Warcraft Tavern).', 'Assassination and Subtlety usually take daggers, any weapon suits Combat (Warcraft Tavern).', 'Вбивство й Непомітність зазвичай беруть кинджали, Бою підходить будь-яка зброя (Warcraft Tavern).'),
            ]),
            ('table', {'head': [tx('Спек', 'Spec', 'Спек', de='Skillung', es='Espec.', fr='Spé', it='Spec.', pl='Spec', pt='Espec.'), t('Правая рука', 'Main hand', 'Права рука'), t('Левая рука', 'Off hand', 'Ліва рука'), t('Почему', 'Why', 'Чому')], 'rows': [
                [t('Бой', 'Combat', 'Бій'), t('Медленное, с большим уроном, любого типа', 'Slow, with high damage, any type', 'Повільна, з великою шкодою, будь-якого типу'), t('Быстрое, любого типа', 'Fast, any type', 'Швидка, будь-якого типу'),
                 t('Ответный удар и Коварный удар сильнее с медленным оружием в правой руке (Icy Veins), быстрое кладите в левую (Mobalytics). Круши-руби даёт бонус любому типу оружия, с мечом — шанс лишнего удара (Mobalytics).', 'Riposte and Sinister Strike hit harder with a slow main-hand weapon (Icy Veins); the fast one goes in the off hand (Mobalytics). Hack and Slash gives a bonus to every weapon type; with a sword, a chance for an extra hit (Mobalytics).', 'Riposte і Sinister Strike сильніші з повільною зброєю в правій руці (Icy Veins), швидку кладіть у ліву (Mobalytics). Hack and Slash дає бонус будь-якому типу зброї, з мечем — шанс зайвого удару (Mobalytics).')],
                [t('Ликвидация', 'Assassination', 'Вбивство'), t('Кинжал', 'Dagger', 'Кинджал'), t('Кинжал', 'Dagger', 'Кинджал'),
                 t('Расправа бьёт обоими оружиями и требует два кинжала (Icy Veins).', 'Mutilate strikes with both weapons and needs two daggers (Icy Veins).', 'Mutilate б’є обома зброями й потребує двох кинджалів (Icy Veins).')],
                [t('Скрытность', 'Subtlety', 'Непомітність'), t('Кинжал', 'Dagger', 'Кинджал'), t('Кинжал', 'Dagger', 'Кинджал'),
                 t('Внезапный удар и Удар в спину бьют кинжалом; без него открывайте Гарротой (Icy Veins). Сборка на кровотечение бьёт Кровоизлиянием (Warcraft Tavern).', 'Ambush and Backstab strike with a dagger; without one, open with Garrote (Icy Veins). The bleed build strikes with Hemorrhage (Warcraft Tavern).', 'Ambush і Backstab б’ють кинджалом; без нього відкривайте Garrote (Icy Veins). Збірка на кровотечу б’є Hemorrhage (Warcraft Tavern).')],
            ]}),
            ('text', [
                t('Бой с кинжалом: Удар в спину из-за спины, Внезапный удар из незаметности (Icy Veins). С хорошим кинжалом в правой руке Icy Veins советует Puncturing Wounds, у Mobalytics для кинжалов отдельная сборка. Мечи, топоры, булавы и кинжалы Бою подходят все (Mobalytics). Кулачное оружие тоже можно: его учат у тренера оружия (Warcraft Tavern).', 'Combat with a dagger: Backstab from behind, Ambush from Stealth (Icy Veins). With a good main-hand dagger, Icy Veins suggests Puncturing Wounds, and Mobalytics has a separate dagger build. Swords, axes, maces and daggers all suit Combat (Mobalytics). Fist weapons work too: you learn them from a weapon master (Warcraft Tavern).', 'Бій із кинджалом: Backstab з-за спини, Ambush з непомітності (Icy Veins). З добрим кинджалом у правій руці Icy Veins радить Puncturing Wounds, у Mobalytics для кинджалів окрема збірка. Мечі, сокири, булави й кинджали Бою підходять усі (Mobalytics). Кулачна зброя теж підходить: її вчать у тренера зброї (Warcraft Tavern).'),
            ]),
        ]},
        {'id': 'forever', 'title': t('Чем Forever отличается от Classic', 'How Forever differs from Classic', 'Чим Forever відрізняється від Classic'), 'blocks': [
            ('table', {'head': [t('Что', 'What', 'Що'), t('В Forever', 'In Forever', 'У Forever')], 'rows': [
                [t('Очки серии', 'Combo points', 'Бали серії'), t('Не сгорают при смене цели (Icy Veins, Mobalytics). Переходят ли на новую цель — источники спорят, проверим на старте.', 'Do not expire when you switch targets (Icy Veins, Mobalytics). Whether they carry over to the new target, the sources disagree; we will check at launch.', 'Не згоряють при зміні цілі (Icy Veins, Mobalytics). Чи переходять вони на нову ціль, джерела сперечаються, перевіримо на старті.')],
                [t('Энергия', 'Energy', 'Енергія'), t('Восстанавливается ровно, без рывков раз в 2 секунды.', 'Regenerates smoothly, without a jump every 2 seconds.', 'Відновлюється рівно, без ривків раз на 2 секунди.')],
                [t('Оружие', 'Weapons', 'Зброя'), t('Можно носить одноручные топоры. Круши-руби даёт бонус любому типу оружия: не надо менять таланты под оружие.', 'One-handed axes can be used. Hack and Slash gives a bonus to any weapon type: no need to change talents for your weapon.', 'Можна носити одноручні сокири. Hack and Slash дає бонус будь-якому типу зброї: не треба міняти таланти під зброю.')],
                [t('Новые способности', 'New abilities', 'Нові здібності'), t('Расправа и Отрава у Ликвидации.', 'Mutilate and Venom for Assassination.', 'Mutilate і Venom у Вбивства.')],
                [t('Яды', 'Poisons', 'Отрути'), t('Могут критовать. Складываются с точильными камнями и Тотемом неистовства ветра (Warcraft Tavern); Mobalytics пишет обратное про тотем — источники спорят.', 'Can crit. They stack with sharpening stones and Windfury Totem (Warcraft Tavern); Mobalytics writes the opposite about the totem: the sources disagree.', 'Можуть критувати. Складаються з точильними каменями та Windfury Totem (Warcraft Tavern); Mobalytics пише про тотем навпаки, джерела сперечаються.')],
                [t('Меткость', 'Hit chance', 'Влучання'), t('До 3% через талант (в Classic было 5%).', 'Up to 3% through a talent (it was 5% in Classic).', 'До 3% через талант (у Classic було 5%).')],
                [t('Вторая специализация', 'Dual specialization', 'Друга спеціалізація'), t('С 40 уровня.', 'From level 40.', 'З 40 рівня.')],
            ]}),
        ]},
        {'id': 'faq', 'title': t('Вопросы', 'Questions', 'Питання'), 'blocks': [
            ('faq', [
                {'id': 'q1', 'q': t('Какой спек Разбойника качать в WoW Forever?', 'Which Rogue spec should I level in WoW Forever?', 'Який спек Розбійника прокачувати у WoW Forever?'),
                 'a': [t('Бой: его советуют Mobalytics и Icy Veins. Warcraft Tavern не выделяет одну ветку, но не советует Ликвидацию для старта.', 'Combat: Mobalytics and Icy Veins recommend it. Warcraft Tavern doesn’t single out one tree, but advises against Assassination as a start.', 'Бій: його радять Mobalytics та Icy Veins. Warcraft Tavern не виділяє одну гілку, але не радить Вбивство для старту.')]},
                {'id': 'q2', 'q': t('Когда появляются яды?', 'When do poisons appear?', 'Коли з’являються отрути?'),
                 'a': [t('На 20 уровне, после задания класса.', 'At level 20, after the class quest.', 'На 20 рівні, після завдання класу.')]},
                {'id': 'q3', 'q': t('Почему Разбойник качается медленнее Охотника и Мага?', 'Why does the Rogue level slower than the Hunter and Mage?', 'Чому Розбійник прокачується повільніше за Мисливця й Мага?'),
                 'a': [t('У него почти нет урона по площади и самолечения. Выручают Первая помощь и Шквал клинков с 30 уровня.', 'It has almost no area damage or self-healing. First Aid and, from level 30, Blade Flurry help.', 'У нього майже немає шкоди по площі та самолікування. Виручають Перша допомога і з 30 рівня Blade Flurry.')]},
                {'id': 'q4', 'q': t('Какое оружие брать для Боя?', 'Which weapon should I take for Combat?', 'Яку зброю брати для Бою?'),
                 'a': [t('Любое: Круши-руби работает с любым типом. Быстрое оружие кладите в левую руку (Mobalytics).', 'Any: Hack and Slash works with any type. Put the fast weapon in the off hand (Mobalytics).', 'Будь-яку: Hack and Slash працює з будь-яким типом. Швидку зброю кладіть у ліву руку (Mobalytics).')]},
                {'id': 'q5', 'q': t('Сгорают ли очки серии при смене цели?', 'Do combo points expire when I switch targets?', 'Чи згоряють бали серії при зміні цілі?'),
                 'a': [t('Нет, остаются на прежней цели. Перенос на новую цель источники описывают по-разному: проверим после 05.11.', 'No, they stay on the previous target. The sources describe the transfer to a new target differently: we will check after Nov 4–5.', 'Ні, вони лишаються на попередній цілі. Перенесення на нову ціль джерела описують по-різному: перевіримо після 5 листопада.')]},
            ]),
        ]},
        {'id': 'related', 'title': t('Смотрите также', 'See also', 'Дивіться також'), 'blocks': [
            ('tiles', _related('rogue', [
                t('Разбойник', 'Rogue', 'Розбійник'),
                tx('Прокачка 1–60', 'Leveling 1–60', 'Прокачування 1–60', fr='Monter de 1 à 60', it='Livellare 1–60', pt='Evoluir 1–60'),
                t('Лучшая раса', 'Best race', 'Найкраща раса'),
                t('Тир-лист', 'Tier list', 'Тір-лист'),
            ])),
        ]},
    ],
})

# ---------- priest ----------

CLASS_GUIDES.append({
    'slug': 'leveling-priest', 'art': 'priest', 'hero': 'hero_leveling', 'hub': False,
    'title': t('Прокачка Жреца 1–60', 'Priest Leveling 1–60', 'Прокачування Жерця 1–60'),
    'lead': tx('Жрец качается чуть медленнее среднего, по оценке LFCarry примерно на 5%: всё упирается в ману. Зато он почти не умирает и нужен любой группе. Главное на прокачке — хороший жезл и бои без лишних заклинаний.', 'Priest levels a little slower than average, about 5% by LFCarry’s estimate: everything comes down to mana. But it almost never dies and every group needs one. The key to leveling is a good wand and fights without extra spells.', 'Жрець прокачується трохи повільніше за середній показник, за оцінкою LFCarry приблизно на 5%: усе впирається в ману. Зате він майже не помирає й потрібен будь-якій групі. Головне на прокачуванні — добра паличка й бої без зайвих заклинань.', de='Der Priester levelt etwas langsamer als der Durchschnitt, laut LFCarry etwa 5 %: Alles hängt am Mana. Dafür stirbt er fast nie und wird in jeder Gruppe gebraucht. Beim Leveln zählen ein guter Zauberstab und Kämpfe ohne überflüssige Zauber.', es='El Sacerdote sube algo más despacio que la media, cerca de un 5 % según LFCarry: todo depende del maná. Pero casi no muere y todo grupo lo necesita. Lo importante al subir de nivel es una buena varita y combates sin hechizos de más.', fr='Le Prêtre monte un peu plus lentement que la moyenne, d’environ 5 % selon LFCarry : tout dépend du mana. En revanche, il ne meurt presque jamais et tous les groupes en ont besoin. Ce qui compte en montée : une bonne baguette et des combats sans sorts superflus.', it='Il Sacerdote livella un po’ più lentamente della media, circa il 5% secondo LFCarry: tutto dipende dal mana. In compenso non muore quasi mai ed è richiesto da ogni gruppo. Per livellare contano una buona bacchetta e scontri senza incantesimi superflui.', pl='Priest leveluje się nieco wolniej od średniej, według LFCarry o około 5%: wszystko rozbija się o manę. Za to prawie nie umiera i każda grupa go potrzebuje. W levelowaniu liczy się dobra różdżka i walki bez zbędnych zaklęć.', pt='O Sacerdote evolui um pouco mais devagar que a média, cerca de 5%, segundo o LFCarry: tudo depende da mana. Em compensação quase não morre e todo grupo precisa de um. O que importa ao subir de nível é uma boa varinha e lutas sem feitiços desnecessários.'),
    'tile': t('Темная магия, жезл и таланты по уровням', 'Shadow, wand and talents by level', 'Темрява, паличка й таланти за рівнями'),
    'pills': [t('Спек: Темная магия', 'Spec: Shadow', 'Спек: Темрява'), t('Таланты 10–60', 'Talents 10–60', 'Таланти 10–60'), tx('По бете', 'Beta data', 'За бетою', de='Betadaten', fr='Données de la bêta', pt='Dados da beta')],
    'sources': [
        ('Icy Veins: Shadow Priest Leveling', 'https://www.icy-veins.com/wow-forever/shadow-priest-leveling'),
        ('Mobalytics: Priest Leveling 1-30', 'https://mobalytics.gg/wow-forever/classes/priest-leveling-guide'),
        ('Warcraft Tavern: Priest Leveling', 'https://www.warcrafttavern.com/forever/guides/priest-leveling/'),
    ],
    'sections': [
        {'id': 'spec', 'title': t('Какой спек качать', 'Which spec to level', 'Який спек прокачувати'), 'blocks': [
            ('text', [
                t('Качайте Темную магию, первые очки — в жезл. Так советуют Icy Veins и Mobalytics: Захват духа возвращает ману после убийства, Пытка разума замедляет врага, Объятия вампира даёт лечение от нанесённого урона.', 'Level Shadow, with the first points into the wand. Icy Veins and Mobalytics recommend this: Spirit Tap returns mana after a kill, Mind Flay slows the enemy, and Vampiric Embrace heals you from the damage you deal.', 'Прокачуйте Темряву, перші очки — у паличку. Так радять Icy Veins та Mobalytics: Spirit Tap повертає ману після вбивства, Mind Flay уповільнює ворога, Vampiric Embrace дає лікування від завданої шкоди.'),
                t('Источники спорят. Warcraft Tavern по умолчанию ставит Послушание с жезлом: оно надёжнее держит вас в живых, а Темная магия у них раскрывается только к 28 уровню и с силой заклинаний. Тир-лист прокачки даёт Жрецу C со звёздочкой: оценки от C до S.', 'The sources disagree. Warcraft Tavern defaults to Discipline with a wand: it keeps you alive more reliably, and their Shadow only opens up by level 28 and with spell power. The leveling tier list gives Priest a C with an asterisk: ratings range from C to S.', 'Джерела сперечаються. Warcraft Tavern за замовчуванням ставить Послух із паличкою: він надійніше тримає вас живим, а Темрява в них розкривається лише до 28 рівня й із силою заклинань. Тір-лист прокачування дає Жерцю C із зірочкою: оцінки від C до S.'),
            ]),
            ('table', {'head': [tx('Спек', 'Spec', 'Спек', de='Skillung', es='Espec.', fr='Spé', it='Spec.', pl='Spec', pt='Espec.'), t('Когда брать', 'When to take it', 'Коли брати'), t('Минус', 'Downside', 'Мінус')], 'rows': [
                [tx('Темная магия', 'Shadow', 'Темрява', es='Sombra'), t('Соло, весь путь до 60', 'Solo, the whole way to 60', 'Соло, увесь шлях до 60'), t('Мало маны до 40-х уровней (талант Облик Тьмы)', 'Little mana until the 40s (the Shadowform talent)', 'Мало мани до сорокових рівнів (талант Shadowform)')],
                [t('Послушание', 'Discipline', 'Послух'), t('Осторожная игра с жезлом, Исповедь с 30', 'Careful play with a wand, Penance from 30', 'Обережна гра з паличкою, Penance з 30'), t('Меньше урона', 'Less damage', 'Менше шкоди')],
                [t('Свет', 'Holy', 'Світло'), t('Если много подземелий', 'If you run a lot of dungeons', 'Якщо багато підземель'), t('Соло медленно: Tavern не советует качаться лекарем', 'Slow solo: Tavern does not recommend leveling as a healer', 'Соло повільно: Tavern не радить качатися цілителем')],
            ]}),
        ]},
        {'id': 'talents', 'title': t('Таланты по уровням', 'Talents by level', 'Таланти за рівнями'), 'blocks': [
            ('text', [
                t('Порядок Icy Veins для Темной магии (обновлён 17.10). Уровни 31–60 на бете закрыты: это план источника, проверим после старта 05.11.', 'Icy Veins order for Shadow (updated Oct 17). Levels 31–60 are closed on the beta: this is the source’s plan, and we will check it after the Nov 4–5 launch.', 'Порядок Icy Veins для Темряви (оновлено 17 жовтня). Рівні 31–60 у беті закриті: це план джерела, перевіримо після старту 5 листопада.'),
            ]),
            ('table', {'head': [t('Уровни', 'Levels', 'Рівні'), t('Талант', 'Talent', 'Талант'), t('Очки', 'Points', 'Очки')], 'rows': [
                ['10–11', t('Специализация на жезлах (Wand Specialization)', 'Wand Specialization', 'Wand Specialization'), '2'],
                ['12–16', t('Захват духа (Spirit Tap)', 'Spirit Tap', 'Spirit Tap'), '5'],
                ['17–18', t('Улучшенное слово Тьмы: Боль (Improved Shadow Word: Pain)', 'Improved Shadow Word: Pain', 'Improved Shadow Word: Pain'), '2'],
                ['19–21', t('Улучшенный взрыв разума (Improved Mind Blast)', 'Improved Mind Blast', 'Improved Mind Blast'), '3'],
                ['22', t('Пытка разума (Mind Flay)', 'Mind Flay', 'Mind Flay'), '1'],
                ['23–24', t('Улучшенная Пытка разума (Improved Mind Flay)', 'Improved Mind Flay', 'Improved Mind Flay'), '2'],
                ['25', t('Улучшенный взрыв разума (Improved Mind Blast)', 'Improved Mind Blast', 'Improved Mind Blast'), '4'],
                ['26', t('Средоточие Тьмы (Shadow Focus)', 'Shadow Focus', 'Shadow Focus'), '1'],
                ['27', t('Объятия вампира (Vampiric Embrace)', 'Vampiric Embrace', 'Vampiric Embrace'), '1'],
                ['28–31', 'Dark Inspiration', '4'],
                ['32–33', 'Devouring Contagion', '2'],
                ['34', 'Dark Inspiration', '5/5'],
                ['35–36', t('Плетение Тьмы (Shadow Weaving)', 'Shadow Weaving', 'Shadow Weaving'), '2'],
                ['37–41', t('Мрак (Darkness)', 'Darkness', 'Darkness'), '5'],
                ['42', t('Облик Тьмы (Shadowform)', 'Shadowform', 'Shadowform'), '1'],
                ['43–47', 'Twin Disciplines', '5'],
                ['48–50', t('Сила мысли (Mental Strength)', 'Mental Strength', 'Mental Strength'), '3'],
                ['51–53', t('Медитация (Meditation)', 'Meditation', 'Meditation'), '3'],
                ['54', t('Плетение Тьмы (Shadow Weaving)', 'Shadow Weaving', 'Shadow Weaving'), '3/3'],
                ['55–56', 'Early Demise', '2'],
                ['57–60', t('Средоточие Тьмы (Shadow Focus)', 'Shadow Focus', 'Shadow Focus'), '5/5'],
            ]}),
            ('tip', t('Mobalytics (22.10) до 30 уровня идёт почти так же, но не берёт Улучшенный взрыв разума и Dark Inspiration: вместо них Средоточие Тьмы 3/5, Предел Тьмы 2/2 и Плетение Тьмы 3/3. Если жезла к 10 уровню нет, первые 2 очка сразу в Темную магию. Перк Legacy Talented даёт таланты до 5 уровней раньше.', 'Mobalytics (Oct 22) goes almost the same way up to level 30, but does not take Improved Mind Blast and Dark Inspiration: instead Shadow Focus 3/5, Shadow Reach 2/2 and Shadow Weaving 3/3. If you have no wand by level 10, put the first 2 points straight into Shadow. The Legacy Talented perk gives talents up to 5 levels earlier.', 'Mobalytics (22 жовтня) до 30 рівня йде майже так само, але не бере Improved Mind Blast і Dark Inspiration: замість них Shadow Focus 3/5, Shadow Reach 2/2 і Shadow Weaving 3/3. Якщо палички до 10 рівня немає, перші 2 очки одразу в Темряву. Перк Legacy Talented дає таланти до 5 рівнів раніше.')),
        ]},
        {'id': 'abilities', 'title': t('Способности и тренер', 'Abilities and trainer', 'Здібності й тренер'), 'blocks': [
            ('text', [BETA_TRAINER]),
            ('table', {'head': [t('Уровень', 'Level', 'Рівень'), t('Что взять', 'What to take', 'Що взяти'), tx('Зачем', 'Why', 'Навіщо', de='Wozu', es='Para qué', it='A cosa serve', pl='Po co', pt='Para quê')], 'rows': [
                ['1', t('Кара, Малое исцеление, Слово силы: Стойкость', 'Smite, Lesser Heal, Power Word: Fortitude', 'Smite, Lesser Heal, Power Word: Fortitude'), t('Урон, лечение, выносливость', 'Damage, healing, Stamina', 'Шкода, лікування, витривалість')],
                ['4', t('Слово Тьмы: Боль', 'Shadow Word: Pain', 'Shadow Word: Pain'), t('Урон со временем', 'Damage over time', 'Шкода з часом')],
                ['5', t('Малый магический жезл (предмет)', 'Lesser Magic Wand (item)', 'Lesser Magic Wand (предмет)'), t('Урон без маны', 'Damage without mana', 'Шкода без мани')],
                ['6', t('Слово силы: Щит', 'Power Word: Shield', 'Power Word: Shield'), t('Щит от урона и сбития заклинаний', 'A shield against damage and spell pushback', 'Щит від шкоди та збивання заклинань')],
                ['8', t('Обновление, Уход в тень', 'Renew, Fade', 'Renew, Fade'), t('Лечение со временем, сброс угрозы', 'Healing over time, dropping threat', 'Лікування з часом, скидання загрози')],
                ['10', t('Взрыв разума; первое расовое заклинание', 'Mind Blast; the first racial spell', 'Mind Blast; перше расове заклинання'), t('Главный удар, откат 8 сек', 'The main strike, 8 sec cooldown', 'Головний удар, відкат 8 с')],
                ['12', t('Внутренний огонь', 'Inner Fire', 'Inner Fire'), t('Броня', 'Armor', 'Броня')],
                ['14', t('Ментальный крик', 'Psychic Scream', 'Psychic Scream'), t('Отогнать врагов страхом', 'Scare enemies away', 'Відлякати ворогів страхом')],
                ['20', t('Быстрое исцеление, Всепожирающая чума, Защита от страха; второе расовое', 'Flash Heal, Devouring Plague, Fear Ward; the second racial spell', 'Flash Heal, Devouring Plague, Fear Ward; друге расове'), t('Быстрое лечение, чума у любой расы', 'A fast heal, the plague for any race', 'Швидке лікування, чума в будь-якої раси')],
                ['30', t('Исповедь (талант Послушания)', 'Penance (a Discipline talent)', 'Penance (талант Послуху)'), t('Урон или лечение', 'Damage or healing', 'Шкода або лікування')],
                ['40', t('Верховая езда, вторая специализация', 'Riding, dual specialization', 'Верхова їзда, друга спеціалізація'), '—'],
            ]}),
            ('steps', [
                {'t': t('Перед боем', 'Before the fight', 'Перед боєм'),
                 'd': t('щит на себя (Слово силы: Щит): 30 секунд он поглощает урон и не даёт сбивать заклинания.', 'shield yourself (Power Word: Shield): for 30 seconds it absorbs damage and prevents spell pushback.', 'щит на себе (Power Word: Shield): 30 секунд він поглинає шкоду й не дає збивати заклинання.')},
                {'t': t('Вход', 'Opening', 'Вхід'),
                 'd': t('Взрыв разума, сразу Слово Тьмы: Боль.', 'Mind Blast, then Shadow Word: Pain right away.', 'Mind Blast, одразу Shadow Word: Pain.')},
                {'t': t('В бою', 'In the fight', 'У бою'),
                 'd': t('Пытка разума, пока враг идёт к вам; вблизи — щит или Ментальный крик.', 'Mind Flay while the enemy walks to you; up close, the shield or Psychic Scream.', 'Mind Flay, поки ворог іде до вас; зблизька — щит або Psychic Scream.')},
                {'t': tx('Добивание', 'Finishing', 'Добивання', de='Erledigen', fr='Achever', pl='Dobijanie'),
                 'd': t('при ~20% здоровья врага переходите на жезл. Мана восстанавливается через 5 секунд без заклинаний, а Захват духа срабатывает при убийстве.', 'at ~20% enemy health, switch to the wand. Mana regenerates after 5 seconds without casting, and Spirit Tap triggers on a kill.', 'при ~20% здоров’я ворога переходьте на паличку. Мана відновлюється через 5 секунд без заклинань, а Spirit Tap спрацьовує при вбивстві.')},
            ]),
            ('text', [
                t('Держите Слово силы: Стойкость на всей группе. В подземелье Жреца почти всегда просят лечить: на прокачке можно лечить и Темной магией, а с 40 уровня держать второй набор талантов под лечение.', 'Keep Power Word: Fortitude on the whole group. In a dungeon, a Priest is almost always asked to heal: while leveling you can heal with Shadow too, and from level 40 keep a second talent set for healing.', 'Тримайте Power Word: Fortitude на всій групі. У підземеллі Жерця майже завжди просять лікувати: на прокачуванні можна лікувати й Темрявою, а з 40 рівня тримати другий набір талантів під лікування.'),
            ]),
        ]},
        {'id': 'play', 'title': t('Соло, вдвоём, в группе', 'Solo, duo, group', 'Соло, удвох, у групі'), 'blocks': [
            ('tabs', [
                {'id': 'solo', 't': tx('Соло', 'Solo', 'Соло', es='En solitario', pt='Solo'), 'blocks': [('text', [t('Ищите улучшения жезла: Малый магический жезл с 5 уровня, Большой — около 13 (Icy Veins). Не тратьте ману на врага, которого добьёт жезл или Слово Тьмы: Боль. Ментальный крик может притянуть соседей: смотрите, куда побегут враги.', 'Look for wand upgrades: Lesser Magic Wand from level 5, Greater Magic Wand around 13 (Icy Veins). Don’t spend mana on an enemy the wand or Shadow Word: Pain will finish off. Psychic Scream can pull neighbors: watch where the enemies run.', 'Шукайте покращення палички: Lesser Magic Wand з 5 рівня, Greater Magic Wand близько 13 (Icy Veins). Не витрачайте ману на ворога, якого доб’є паличка чи Shadow Word: Pain. Psychic Scream може притягнути сусідів: дивіться, куди побіжать вороги.')])]},
                {'id': 'duo', 't': tx('Вдвоём', 'Duo', 'Удвох', de='Zu zweit', es='En pareja', fr='À deux', it='In coppia', pl='We dwoje', pt='Em dupla'), 'blocks': [('text', [t('Лучшая пара — любой класс ближнего боя: он держит врага, вы бьёте Тьмой и лечите. Щит на напарника перед боем экономит время.', 'The best partner is any melee class: it holds the enemy while you hit with Shadow and heal. A shield on your partner before the fight saves time.', 'Найкраща пара — будь-який клас ближнього бою: він тримає ворога, ви б’єте Темрявою й лікуєте. Щит на напарника перед боєм економить час.')])]},
                {'id': 'party', 't': t('Группа', 'Group', 'Група'), 'blocks': [('text', [t('Свет — для тех, кто много ходит в подземелья. Соло такой Жрец медленнее (Warcraft Tavern, Icy Veins).', 'Holy is for those who run a lot of dungeons. Solo, such a Priest is slower (Warcraft Tavern, Icy Veins).', 'Світло — для тих, хто багато ходить у підземелля. Соло такий Жрець повільніший (Warcraft Tavern, Icy Veins).')])]},
            ]),
        ]},
        {'id': 'gear', 'title': t('Характеристики и снаряжение', 'Stats and gear', 'Характеристики та спорядження'), 'blocks': [
            ('text', [
                t('Mobalytics: интеллект (запас маны), дух (восполнение), выносливость, сила заклинаний. Жезлы по Warcraft Tavern: Малый магический жезл (5), Большой магический жезл (13), Sizzle Stick (15), Gravestone Scepter (18), Wand of Eventide (27). Улучшение жезла на прокачке ценнее брони.', 'Mobalytics: Intellect (mana pool), Spirit (regeneration), Stamina, spell power. Wands per Warcraft Tavern: Lesser Magic Wand (5), Greater Magic Wand (13), Sizzle Stick (15), Gravestone Scepter (18), Wand of Eventide (27). A wand upgrade is worth more than armor while leveling.', 'Mobalytics: інтелект (запас мани), дух (відновлення), витривалість, сила заклинань. Палички за Warcraft Tavern: Lesser Magic Wand (5), Greater Magic Wand (13), Sizzle Stick (15), Gravestone Scepter (18), Wand of Eventide (27). Покращення палички на прокачуванні цінніше за броню.'),
                t('Пары профессий под класс и объекты лагеря — в гайде по профессиям.', 'Class profession pairings and camp objects are in the professions guide.', 'Пари професій під клас і об’єкти табору — у гайді з професій.'),
            ]),
        ]},
        {'id': 'forever', 'title': t('Чем Forever отличается от Classic', 'How Forever differs from Classic', 'Чим Forever відрізняється від Classic'), 'blocks': [
            ('table', {'head': [t('Что', 'What', 'Що'), t('В Forever', 'In Forever', 'У Forever')], 'rows': [
                [t('Расовые заклинания', 'Racial spells', 'Расові заклинання'), t('У каждой расы два своих заклинания жреца, на 10 и 20 уровнях.', 'Each race has two Priest spells of its own, at levels 10 and 20.', 'У кожної раси по два власні заклинання жерця, на 10 і 20 рівнях.')],
                [t('Всепожирающая чума и Защита от страха', 'Devouring Plague and Fear Ward', 'Devouring Plague і Fear Ward'), t('Доступны любой расе с 20 уровня.', 'Available to any race from level 20.', 'Доступні будь-якій расі з 20 рівня.')],
                [tx('Облик Тьмы', 'Shadowform', 'Shadowform', de='Schattengestalt', es='Forma de las Sombras', fr='Forme d’Ombre', it='Forma d’Ombra', pt='Forma de Sombra'), t('Переработан: шанс крита и заклинания Тьмы дешевле.', 'Reworked: crit chance, and Shadow spells cost less.', 'Перероблено: шанс крита, а заклинання Темряви дешевші.')],
                [tx('Новые таланты', 'New talents', 'Нові таланти', pt='Talentos novos'), t('Исповедь у Послушания, Молитва восстановления у Света, Улучшенная Пытка разума у Темной магии.', 'Penance for Discipline, Prayer of Mending for Holy, Improved Mind Flay for Shadow.', 'Penance у Послуху, Prayer of Mending у Світла, Improved Mind Flay у Темряви.')],
                [t('Жезлы', 'Wands', 'Палички'), t('Первые жезлы дают силу заклинаний.', 'The first wands give spell power.', 'Перші палички дають силу заклинань.')],
                [t('Эффекты со временем', 'Effects over time', 'Ефекти з часом'), t('Лечение и урон пересчитываются по ходу действия, а не фиксируются при касте.', 'Healing and damage are recalculated as the effect runs, not fixed at the cast.', 'Лікування й шкода перераховуються під час дії, а не фіксуються при касті.')],
                [t('Прикосновение вампира', 'Vampiric Touch', 'Vampiric Touch'), t('В Forever пока нет.', 'Not in Forever yet.', 'У Forever поки немає.')],
                [t('Вторая специализация', 'Dual specialization', 'Друга спеціалізація'), t('С 40 уровня.', 'From level 40.', 'З 40 рівня.')],
            ]}),
        ]},
        {'id': 'faq', 'title': t('Вопросы', 'Questions', 'Питання'), 'blocks': [
            ('faq', [
                {'id': 'q1', 'q': t('Какой спек Жреца качать в WoW Forever?', 'Which Priest spec should I level in WoW Forever?', 'Який спек Жерця прокачувати у WoW Forever?'),
                 'a': [t('Темную магию с талантами на жезл: так советуют Icy Veins и Mobalytics. Warcraft Tavern по умолчанию ставит Послушание.', 'Shadow with the wand talents: Icy Veins and Mobalytics recommend it. Warcraft Tavern defaults to Discipline.', 'Темряву з талантами на паличку: так радять Icy Veins та Mobalytics. Warcraft Tavern за замовчуванням ставить Послух.')]},
                {'id': 'q2', 'q': t('Зачем Жрецу жезл?', 'Why does a Priest need a wand?', 'Навіщо Жерцю паличка?'),
                 'a': [t('Он бьёт без маны. Добивая жезлом, вы восстанавливаете ману и получаете бонус за убийство от таланта Захват духа.', 'It deals damage without mana. Finishing with the wand restores mana and gives the kill bonus from the Spirit Tap talent.', 'Вона б’є без мани. Добиваючи паличкою, ви відновлюєте ману й отримуєте бонус за вбивство від таланту Spirit Tap.')]},
                {'id': 'q3', 'q': t('Когда появляется Облик Тьмы?', 'When does Shadowform appear?', 'Коли з’являється Shadowform?'),
                 'a': [t('Это талант на 40-х уровнях: у Icy Veins на 42 уровне, у Warcraft Tavern на 40.', 'It is a talent in the 40s: level 42 for Icy Veins, level 40 for Warcraft Tavern.', 'Це талант сорокових рівнів: в Icy Veins на 42 рівні, у Warcraft Tavern на 40.')]},
                {'id': 'q4', 'q': t('Можно ли качаться лекарем?', 'Can I level as a healer?', 'Чи можна качатися цілителем?'),
                 'a': [t('Можно, но соло медленно. Свет имеет смысл, если вы почти всё время в подземельях.', 'You can, but it is slow solo. Holy makes sense if you spend almost all your time in dungeons.', 'Можна, але соло повільно. Світло має сенс, якщо ви майже весь час у підземеллях.')]},
                {'id': 'q5', 'q': t('Почему Жрец качается медленнее?', 'Why does a Priest level slower?', 'Чому Жрець прокачується повільніше?'),
                 'a': [t('Всё упирается в ману, урона по площади нет. По оценке LFCarry примерно на 5% медленнее среднего.', 'Everything comes down to mana, and there is no area damage. By LFCarry’s estimate, about 5% slower than average.', 'Усе впирається в ману, шкоди по площі немає. За оцінкою LFCarry, приблизно на 5% повільніше за середній показник.')]},
            ]),
        ]},
        {'id': 'related', 'title': t('Смотрите также', 'See also', 'Дивіться також'), 'blocks': [
            ('tiles', _related('priest', [
                t('Жрец', 'Priest', 'Жрець'),
                tx('Прокачка 1–60', 'Leveling 1–60', 'Прокачування 1–60', fr='Monter de 1 à 60', it='Livellare 1–60', pt='Evoluir 1–60'),
                t('Лучшая раса', 'Best race', 'Найкраща раса'),
                t('Тир-лист', 'Tier list', 'Тір-лист'),
            ])),
        ]},
    ],
})

# ---------- shaman ----------

CLASS_GUIDES.append({
    'slug': 'leveling-shaman', 'art': 'shaman', 'hero': 'hero_leveling', 'hub': False,
    'title': t('Прокачка Шамана 1–60', 'Shaman Leveling 1–60', 'Прокачування Шамана 1–60'),
    'lead': t('Шаман качается в среднем темпе: сильный удар, лечение себя и Призрачный волк с 20 уровня. Главная трудность до 30 — мана. В Forever он впервые есть у Альянса: шаманом может быть дворф.', 'Shaman levels at an average pace: a strong strike, self-healing and Ghost Wolf from level 20. The main difficulty before 30 is mana. In Forever the Alliance has Shamans for the first time: a Dwarf can be one.', 'Шаман прокачується в середньому темпі: сильний удар, самолікування та Ghost Wolf з 20 рівня. Головна складність до 30 — мана. У Forever він уперше є в Альянсу: шаманом може бути дворф.'),
    'tile': t('Совершенствование, тотемы и таланты', 'Enhancement, totems and talents', 'Вдосконалення, тотеми й таланти'),
    'pills': [t('Спек: Совершенствование', 'Spec: Enhancement', 'Спек: Вдосконалення'), t('Таланты 10–60', 'Talents 10–60', 'Таланти 10–60'), tx('По бете', 'Beta data', 'За бетою', de='Betadaten', fr='Données de la bêta', pt='Dados da beta')],
    'sources': [
        ('Icy Veins: Enhancement Shaman Leveling', 'https://www.icy-veins.com/wow-forever/enhancement-shaman-leveling'),
        ('Mobalytics: Shaman Leveling 1-30', 'https://mobalytics.gg/wow-forever/classes/shaman-leveling-guide'),
        ('Warcraft Tavern: Shaman Leveling', 'https://www.warcrafttavern.com/forever/guides/shaman-leveling/'),
    ],
    'sections': [
        {'id': 'spec', 'title': t('Какой спек качать', 'Which spec to level', 'Який спек прокачувати'), 'blocks': [
            ('text', [
                t('Качайте Совершенствование. Здесь сходятся Warcraft Tavern, Mobalytics и Icy Veins, а порядок талантов у Mobalytics (24.10) и Icy Veins (17.10) до 30 уровня почти один. Удары оружием почти не тратят ману, Удар бури с 25 уровня даёт главный урон.', 'Level Enhancement. Warcraft Tavern, Mobalytics and Icy Veins agree here, and Mobalytics (Oct 24) and Icy Veins (Oct 17) have almost the same talent order up to level 30. Weapon strikes barely cost mana, and Stormstrike from level 25 provides the main damage.', 'Прокачуйте Вдосконалення. Тут сходяться Warcraft Tavern, Mobalytics та Icy Veins, а порядок талантів у Mobalytics (24 жовтня) та Icy Veins (17 жовтня) до 30 рівня майже однаковий. Удари зброєю майже не витрачають ману, Stormstrike з 25 рівня дає головну шкоду.'),
                t('Стихии рабочие, но Tavern пишет о нехватке маны и нестабильных срабатываниях. Исцеление для соло медленное: Tavern советует ждать второй специализации на 40 уровне.', 'Elemental works, but Tavern writes about a lack of mana and unstable procs. Restoration is slow for solo: Tavern advises waiting for dual specialization at level 40.', 'Стихії робочі, але Tavern пише про брак мани й нестабільні спрацьовування. Зцілення для соло повільне: Tavern радить зачекати на другу спеціалізацію на 40 рівні.'),
            ]),
            ('table', {'head': [tx('Спек', 'Spec', 'Спек', de='Skillung', es='Espec.', fr='Spé', it='Spec.', pl='Spec', pt='Espec.'), t('Когда брать', 'When to take it', 'Коли брати'), t('Минус', 'Downside', 'Мінус')], 'rows': [
                [t('Совершенствование', 'Enhancement', 'Вдосконалення'), t('Соло и подземелья, весь путь до 60', 'Solo and dungeons, the whole way to 60', 'Соло та підземелля, увесь шлях до 60'), t('Мана до 30 уровня, зависит от оружия', 'Mana before level 30, depends on the weapon', 'Мана до 30 рівня, залежність від зброї')],
                [t('Стихии', 'Elemental', 'Стихії'), t('Любителям дальнего боя', 'Fans of ranged combat', 'Любителям дальнього бою'), tx('Быстро кончается мана', 'Mana runs out fast', 'Мана швидко закінчується', de='Das Mana geht schnell aus')],
                [t('Исцеление', 'Restoration', 'Зцілення'), t('Как вторая специализация с 40', 'As a second specialization from 40', 'Як друга спеціалізація з 40'), t('Соло медленно', 'Slow solo', 'Соло повільно')],
            ]}),
        ]},
        {'id': 'talents', 'title': t('Таланты по уровням', 'Talents by level', 'Таланти за рівнями'), 'blocks': [
            ('text', [
                t('Порядок Icy Veins для Совершенствования (обновлён 17.10). Уровни 31–60 на бете закрыты: это план источника, проверим после старта 05.11.', 'Icy Veins order for Enhancement (updated Oct 17). Levels 31–60 are closed on the beta: this is the source’s plan, and we will check it after the Nov 4–5 launch.', 'Порядок Icy Veins для Вдосконалення (оновлено 17 жовтня). Рівні 31–60 у беті закриті: це план джерела, перевіримо після старту 5 листопада.'),
            ]),
            ('table', {'head': [t('Уровни', 'Levels', 'Рівні'), t('Талант', 'Talent', 'Талант'), t('Очки', 'Points', 'Очки')], 'rows': [
                ['10–14', t('Грохочущие удары (Thundering Strikes)', 'Thundering Strikes', 'Thundering Strikes'), '5'],
                ['15–17', t('Гибкость разума (Mental Dexterity)', 'Mental Dexterity', 'Mental Dexterity'), '3'],
                ['18–19', t('Улучшенный призрачный волк (Improved Ghost Wolf)', 'Improved Ghost Wolf', 'Improved Ghost Wolf'), '2'],
                ['20', 'Shamanistic Focus', '1'],
                ['21–23', t('Оружие стихий (Elemental Weapons)', 'Elemental Weapons', 'Elemental Weapons'), '3'],
                ['24', t('Предчувствие (Anticipation)', 'Anticipation', 'Anticipation'), '1'],
                ['25', t('Удар бури (Stormstrike)', 'Stormstrike', 'Stormstrike'), '1'],
                ['26–29', t('Шквал (Flurry)', 'Flurry', 'Flurry'), '4'],
                ['30–31', 'Improved Stormstrike', '2'],
                ['32', t('Spirit Weapons', 'Spirit Weapons', 'Spirit Weapons'), '1'],
                ['33–37', t('Приливная концентрация (Tidal Focus)', 'Tidal Focus', 'Tidal Focus'), '5'],
                ['38–40', t('Осознанность (Mindfulness)', 'Mindfulness', 'Mindfulness'), '3'],
                ['41–42', t('Улучшенная волна исцеления (Improved Healing Wave)', 'Improved Healing Wave', 'Improved Healing Wave'), '2'],
                ['43', t('Водный щит (Water Shield)', 'Water Shield', 'Water Shield'), '1'],
                ['44', t('Шквал (Flurry)', 'Flurry', 'Flurry'), '5/5'],
                ['45–46', t('Ментальная скорость (Mental Quickness)', 'Mental Quickness', 'Mental Quickness'), '2'],
                ['47–51', t('Оружие Водоворота (Maelstrom Weapon)', 'Maelstrom Weapon', 'Maelstrom Weapon'), '5'],
                ['52', t('Ярость Провидца (Rage of the Farseer)', 'Rage of the Farseer', 'Rage of the Farseer'), '1'],
                ['53–57', t('Конвекция (Convection)', 'Convection', 'Convection'), '5'],
                ['58–60', t('Опустошение Духов стихии (Elemental Devastation)', 'Elemental Devastation', 'Elemental Devastation'), '3'],
            ]}),
            ('tip', bt(t('Призрачный волк появляется только на 20 уровне. Mobalytics советует до 20 взять Улучшенный щит молний 2/2 и сбросить таланты на 20: на бете это стоило 1 серебряную, на старте будет 1 золотая. Перк Legacy Talented даёт таланты до 5 уровней раньше.', 'Ghost Wolf appears only at level 20. Mobalytics advises taking Improved Lightning Shield 2/2 before 20 and respeccing at 20: on the beta that cost 1 silver, at launch it will be 1 gold. The Legacy Talented perk gives talents up to 5 levels earlier.', 'Ghost Wolf з’являється лише на 20 рівні. Mobalytics радить до 20 взяти Improved Lightning Shield 2/2 і скинути таланти на 20: у беті це коштувало 1 срібний, на старті буде 1 золотий. Перк Legacy Talented дає таланти до 5 рівнів раніше.'), 2)),
        ]},
        {'id': 'abilities', 'title': t('Способности и тренер', 'Abilities and trainer', 'Здібності й тренер'), 'blocks': [
            ('text', [BETA_TRAINER]),
            ('table', {'head': [t('Уровень', 'Level', 'Рівень'), t('Что взять', 'What to take', 'Що взяти'), tx('Зачем', 'Why', 'Навіщо', de='Wozu', es='Para qué', it='A cosa serve', pl='Po co', pt='Para quê')], 'rows': [
                ['1', t('Оружие Камнедробителя, Молния', 'Rockbiter Weapon, Lightning Bolt', 'Rockbiter Weapon, Lightning Bolt'), t('Чары на оружие, вытягивать врагов', 'A weapon enchant, pulling enemies', 'Чари на зброю, витягувати ворогів')],
                ['4', t('Земной шок; задание на тотем земли', 'Earth Shock; the earth totem quest', 'Earth Shock; завдання на тотем землі'), t('Урон и прерывание', 'Damage and an interrupt', 'Шкода та переривання')],
                ['8', t('Щит молний, Тотем каменного когтя', 'Lightning Shield, Stoneclaw Totem', 'Lightning Shield, Stoneclaw Totem'), t('Урон атакующим, отвлечь врагов', 'Damage to attackers, distracting enemies', 'Шкода тим, хто атакує, відвернути ворогів')],
                ['10', t('Огненный шок, Оружие языка пламени, Тотем силы земли; задание на тотем огня (Опаляющий тотем)', 'Flame Shock, Flametongue Weapon, Strength of Earth Totem; the fire totem quest (Searing Totem)', 'Flame Shock, Flametongue Weapon, Strength of Earth Totem; завдання на тотем вогню (Searing Totem)'), t('Основной набор Совершенствования', 'The core Enhancement set', 'Основний набір Вдосконалення')],
                ['12', t('Кольцо огня', 'Fire Nova', 'Fire Nova'), t('Урон по площади от тотема огня', 'Area damage from the fire totem', 'Шкода по площі від тотема вогню')],
                ['20', t('Призрачный волк, Ледяной шок, Totemic Recall, Зов стихий; задание на тотем воды', 'Ghost Wolf, Frost Shock, Totemic Recall, Call of the Elements; the water totem quest', 'Ghost Wolf, Frost Shock, Totemic Recall, Call of the Elements; завдання на тотем води'), t('Скорость +40%, замедление, тотемы разом', '+40% speed, a slow, totems all at once', 'Швидкість +40%, уповільнення, тотеми одразу')],
                ['22', t('Проецирование тотемов', 'Totemic Projection', 'Totemic Projection'), t('Переставить тотемы', 'Reposition totems', 'Переставити тотеми')],
                ['26', t('Тотем источника маны, Тотем магмы', 'Mana Spring Totem, Magma Totem', 'Mana Spring Totem, Magma Totem'), t('Мана, урон по площади', 'Mana, area damage', 'Мана, шкода по площі')],
                ['28', t('Тотем языка пламени', 'Flametongue Totem', 'Flametongue Totem'), t('Тотем огня для группы', 'A fire totem for the group', 'Тотем вогню для групи')],
                ['30', t('Оружие неистовства ветра; задание на тотем воздуха', 'Windfury Weapon; the air totem quest', 'Windfury Weapon; завдання на тотем повітря'), t('Главные чары Совершенствования', 'The main Enhancement enchant', 'Головні чари Вдосконалення')],
                ['32', t('Тотем неистовства ветра', 'Windfury Totem', 'Windfury Totem'), t('Тотем для группы', 'A totem for the group', 'Тотем для групи')],
                ['40', t('Верховая езда, вторая специализация', 'Riding, dual specialization', 'Верхова їзда, друга спеціалізація'), '—'],
            ]}),
            ('steps', [
                {'t': t('Перед боем', 'Before the fight', 'Перед боєм'),
                 'd': t('Щит молний, чары на оружии: Оружие Камнедробителя или Оружие языка пламени, с 30 — Оружие неистовства ветра.', 'Lightning Shield, an enchant on the weapon: Rockbiter Weapon or Flametongue Weapon, and from 30 Windfury Weapon.', 'Lightning Shield, чари на зброї: Rockbiter Weapon або Flametongue Weapon, з 30 — Windfury Weapon.')},
                {'t': t('Вход', 'Opening', 'Вхід'),
                 'd': t('Огненный шок или Молния 1-го ранга, если врага надо вытянуть.', 'Flame Shock or rank 1 Lightning Bolt if you need to pull the enemy.', 'Flame Shock або Lightning Bolt 1-го рангу, якщо ворога треба витягнути.')},
                {'t': t('В бою', 'In the fight', 'У бою'),
                 'd': t('Удар бури по откату, сразу Земной шок, пока на враге висит ослабление от удара. Тотемы — только против элитных врагов.', 'Stormstrike on cooldown, then Earth Shock right away while the strike’s debuff is on the enemy. Totems only against elites.', 'Stormstrike за відкатом, одразу Earth Shock, поки на ворогу висить послаблення від удару. Тотеми — лише проти елітних ворогів.')},
                {'t': t('Мана', 'Mana', 'Мана'),
                 'd': t('все заклинания в начале боя, дальше бейте оружием: мана восстанавливается через 5 секунд без заклинаний. Лечение — Волна исцеления.', 'all spells at the start of the fight, then hit with the weapon: mana regenerates after 5 seconds without casting. Healing is Healing Wave.', 'усі заклинання на початку бою, далі бийте зброєю: мана відновлюється через 5 секунд без заклинань. Лікування — Healing Wave.')},
            ]),
            ('text', [
                t('На 3+ врагах Кольцо огня — самое выгодное по мане заклинание, Тотем магмы — только если враги проживут 15+ секунд (Mobalytics). Бафф тотемов в Forever действует на весь рейд. Земной шок сбивает опасные заклинания.', 'Against 3+ enemies, Fire Nova is the most mana-efficient spell, and Magma Totem only if the enemies will live 15+ seconds (Mobalytics). In Forever, totem buffs affect the whole raid. Earth Shock interrupts dangerous spells.', 'На 3+ ворогах Fire Nova — найвигідніше за маною заклинання, Magma Totem — лише якщо вороги проживуть 15+ секунд (Mobalytics). Бафи тотемів у Forever діють на весь рейд. Earth Shock збиває небезпечні заклинання.'),
            ]),
        ]},
        {'id': 'play', 'title': t('Соло, вдвоём, в группе', 'Solo, duo, group', 'Соло, удвох, у групі'), 'blocks': [
            ('tabs', [
                {'id': 'solo', 't': tx('Соло', 'Solo', 'Соло', es='En solitario', pt='Solo'), 'blocks': [('text', [t('Всегда носите воду: до 30 уровня мана кончается быстро. С талантом Удар бури ищите самое медленное двуручное оружие. Двуручные булавы и топоры откройте у тренера оружия как можно раньше (Icy Veins).', 'Always carry water: before level 30, mana runs out fast. With the Stormstrike talent, look for the slowest two-handed weapon. Open two-handed maces and axes at the weapon trainer as early as possible (Icy Veins).', 'Завжди носіть воду: до 30 рівня мана швидко закінчується. З талантом Stormstrike шукайте найповільнішу дворучну зброю. Дворучні булави й сокири відкрийте в тренера зброї якомога раніше (Icy Veins).')])]},
                {'id': 'duo', 't': tx('Вдвоём', 'Duo', 'Удвох', de='Zu zweit', es='En pareja', fr='À deux', it='In coppia', pl='We dwoje', pt='Em dupla'), 'blocks': [('text', [t('Тотемы усиливают и напарника: Тотем силы земли для ближнего боя, Тотем источника маны для заклинателя. Волна исцеления между боями закрывает лечение пары.', 'Totems strengthen your partner too: Strength of Earth Totem for melee, Mana Spring Totem for a caster. Healing Wave between fights covers the pair’s healing.', 'Тотеми підсилюють і напарника: Strength of Earth Totem для ближнього бою, Mana Spring Totem для заклинача. Healing Wave між боями закриває лікування пари.')])]},
                {'id': 'party', 't': t('Группа', 'Group', 'Група'), 'blocks': [('text', [t('Шаман нужен группе за тотемы: Тотем неистовства ветра с 32 уровня, Тотем источника маны, Тотем трепета против страха.', 'A group needs a Shaman for the totems: Windfury Totem from level 32, Mana Spring Totem, Tremor Totem against fear.', 'Шаман потрібен групі через тотеми: Windfury Totem з 32 рівня, Mana Spring Totem, Tremor Totem проти страху.')])]},
            ]),
        ]},
        {'id': 'gear', 'title': t('Характеристики и снаряжение', 'Stats and gear', 'Характеристики та спорядження'), 'blocks': [
            ('text', [
                t('По Mobalytics: сила (2 силы атаки) > интеллект (1 сила атаки с талантом, крит заклинаний, мана) > ловкость. Сила заклинаний у шамана на бете слабая: коэффициенты втрое ниже, чем у других классов. Оружие — самое медленное двуручное с максимальным уроном.', 'Per Mobalytics: Strength (2 attack power) > Intellect (1 attack power with the talent, spell crit, mana) > Agility. A Shaman’s spell power is weak on the beta: coefficients are three times lower than for other classes. The weapon is the slowest two-hander with the highest damage.', 'За Mobalytics: сила (2 сили атаки) > інтелект (1 сила атаки з талантом, крит заклинань, мана) > спритність. Сила заклинань у шамана в беті слабка: коефіцієнти втричі нижчі, ніж в інших класів. Зброя — найповільніша дворучна з максимальною шкодою.'),
                t('Лагерь (Mobalytics): лучшие объекты для Совершенствования — Mana Well (Алхимия), Lodestone (Горное дело), Fish Bowl (Рыбная ловля), Sharpening Wheel (Кузнечное дело), стул (Снятие шкур, +2% крита). Палатка Кожевничества даёт 5% отдыха. Пары под класс — в гайде по профессиям.', 'Camp (Mobalytics): the best objects for Enhancement are Mana Well (Alchemy), Lodestone (Mining), Fish Bowl (Fishing), Sharpening Wheel (Blacksmithing) and the stool (Skinning, +2% crit). The Leatherworking tent gives 5% rested. Class pairings are in the professions guide.', 'Табір (Mobalytics): найкращі об’єкти для Вдосконалення — Mana Well (Алхімія), Lodestone (Гірництво), Fish Bowl (Риболовля), Sharpening Wheel (Ковальство), ослінчик (Знімання шкур, +2% крита). Намет Шкіряництво дає 5% відпочинку. Пари під клас — у гайді з професій.'),
            ]),
        ]},
        {'id': 'forever', 'title': t('Чем Forever отличается от Classic', 'How Forever differs from Classic', 'Чим Forever відрізняється від Classic'), 'blocks': [
            ('table', {'head': [t('Что', 'What', 'Що'), t('В Forever', 'In Forever', 'У Forever')], 'rows': [
                [t('Альянс', 'Alliance', 'Альянс'), t('Дворф может быть шаманом.', 'A Dwarf can be a Shaman.', 'Дворф може бути шаманом.')],
                [t('Призрачный волк', 'Ghost Wolf', 'Ghost Wolf'), t('+40% к скорости бега. С талантом Улучшенный призрачный волк — мгновенно, в помещениях и в бою.', '+40% run speed. With the Improved Ghost Wolf talent it is instant, usable indoors and in combat.', '+40% до швидкості бігу. З талантом Improved Ghost Wolf — миттєво, у приміщеннях і в бою.')],
                [tx('Удар бури', 'Stormstrike', 'Stormstrike', de='Sturmschlag', es='Golpe de tormenta', fr='Courroux naturel', it='Assalto della Tempesta', pt='Ataque da Tempestade'), tx('Откат 8 сек (в Classic было 20), больше не вершина ветки.', '8 sec cooldown (it was 20 in Classic), no longer the top of the tree.', 'Відкат 8 с (у Classic було 20), більше не вершина гілки.', de='8 Sek. Abklingzeit (in Classic 20), nicht mehr die Spitze des Baums.', es='Reutilización de 8 s (en Classic, 20), ya no es la cima de la rama.', fr='Délai de récupération de 8 s (20 dans Classic), n’est plus le sommet de l’arbre.', it='Ricarica di 8 sec (in Classic era 20), non è più la cima del ramo.', pl='Cooldown 8 sek. (w Classic było 20), nie jest już szczytem drzewka.', pt='Recarga de 8 s (no Classic era 20), não é mais o topo da árvore.')],
                [t('Тотемы', 'Totems', 'Тотеми'), t('Зов стихий ставит до 4 тотемов разом, Проецирование тотемов переносит их. Баффы действуют на весь рейд.', 'Call of the Elements places up to 4 totems at once, Totemic Projection moves them. Buffs affect the whole raid.', 'Call of the Elements ставить до 4 тотемів одразу, Totemic Projection переносить їх. Бафи діють на весь рейд.')],
                [t('Кольцо огня', 'Fire Nova', 'Fire Nova'), t('Срабатывает вокруг вашего тотема огня.', 'Triggers around your fire totem.', 'Спрацьовує навколо вашого тотема вогню.')],
                [tx('Новые таланты', 'New talents', 'Нові таланти', pt='Talentos novos'), t('Оружие Водоворота, Ярость Провидца — личная версия Жажды крови, откат 3 мин.', 'Maelstrom Weapon, Rage of the Farseer: a personal version of Bloodlust, 3 min cooldown.', 'Maelstrom Weapon, Rage of the Farseer: особиста версія Bloodlust, відкат 3 хв.')],
                [t('Астральное возвращение', 'Astral Recall', 'Astral Recall'), t('Второй камень возвращения с откатом 15 мин.', 'A second hearthstone with a 15 min cooldown.', 'Другий камінь повернення з відкатом 15 хв.')],
                [t('Вторая специализация', 'Dual specialization', 'Друга спеціалізація'), t('С 40 уровня.', 'From level 40.', 'З 40 рівня.')],
            ]}),
        ]},
        {'id': 'faq', 'title': t('Вопросы', 'Questions', 'Питання'), 'blocks': [
            ('faq', [
                {'id': 'q1', 'q': t('Какой спек Шамана качать в WoW Forever?', 'Which Shaman spec should I level in WoW Forever?', 'Який спек Шамана прокачувати у WoW Forever?'),
                 'a': [t('Совершенствование: его советуют Warcraft Tavern, Mobalytics и Icy Veins.', 'Enhancement: Warcraft Tavern, Mobalytics and Icy Veins recommend it.', 'Вдосконалення: його радять Warcraft Tavern, Mobalytics та Icy Veins.')]},
                {'id': 'q2', 'q': t('Почему не хватает маны?', 'Why do I run out of mana?', 'Чому не вистачає мани?'),
                 'a': [t('Совершенствование до 30 уровня тратит много маны на шоки и тотемы. Жмите заклинания в начале боя, тотемы ставьте только на сильных врагов, носите воду.', 'Enhancement before level 30 spends a lot of mana on shocks and totems. Cast spells at the start of the fight, set totems only against strong enemies, and carry water.', 'Вдосконалення до 30 рівня витрачає багато мани на шоки й тотеми. Тисніть заклинання на початку бою, тотеми ставте лише на сильних ворогів, носіть воду.')]},
                {'id': 'q3', 'q': t('Когда появляется Призрачный волк?', 'When does Ghost Wolf appear?', 'Коли з’являється Ghost Wolf?'),
                 'a': [t('На 20 уровне. С талантом Улучшенный призрачный волк он мгновенный и работает в помещениях.', 'At level 20. With the Improved Ghost Wolf talent it is instant and works indoors.', 'На 20 рівні. З талантом Improved Ghost Wolf він миттєвий і працює в приміщеннях.')]},
                {'id': 'q4', 'q': t('Где взять тотемы?', 'Where do I get totems?', 'Де взяти тотеми?'),
                 'a': [bt(t('Заданиями класса: тотем земли на 4 уровне, огня на 10, воды на 20, воздуха на 30.', 'From class quests: the earth totem at level 4, fire at 10, water at 20, air at 30.', 'Завданнями класу: тотем землі на 4 рівні, вогню на 10, води на 20, повітря на 30.'), 1)]},
                {'id': 'q5', 'q': t('Может ли Шаман танковать?', 'Can a Shaman tank?', 'Чи може Шаман танкувати?'),
                 'a': [t('Mobalytics даёт советы для танка со щитом, а новый талант Spirit Weapons даёт парирование и угрозу. Насколько такой танк надёжен, станет ясно после старта.', 'Mobalytics gives tips for a shield tank, and the new Spirit Weapons talent gives parry and threat. How reliable such a tank is will become clear after launch.', 'Mobalytics дає поради для танка зі щитом, а новий талант Spirit Weapons дає парирування й загрозу. Наскільки надійний такий танк, стане ясно після старту.')]},
            ]),
        ]},
        {'id': 'related', 'title': t('Смотрите также', 'See also', 'Дивіться також'), 'blocks': [
            ('tiles', _related('shaman', [
                t('Шаман', 'Shaman', 'Шаман'),
                tx('Прокачка 1–60', 'Leveling 1–60', 'Прокачування 1–60', fr='Monter de 1 à 60', it='Livellare 1–60', pt='Evoluir 1–60'),
                t('Лучшая раса', 'Best race', 'Найкраща раса'),
                t('Тир-лист', 'Tier list', 'Тір-лист'),
            ])),
        ]},
    ],
})

# ---------- mage ----------

CLASS_GUIDES.append({
    'slug': 'leveling-mage', 'art': 'mage', 'hero': 'hero_leveling', 'hub': False,
    'title': t('Прокачка Мага 1–60', 'Mage Leveling 1–60', 'Прокачування Мага 1–60'),
    'lead': tx('Маг — один из самых быстрых классов на прокачке, по оценке LFCarry, примерно на 8% быстрее среднего. Сам делает себе еду и воду, замедляет и замораживает врагов. В Forever у Льда появились Ледяное копье и Ледяные пальцы.', 'Mage is one of the fastest classes to level, about 8% faster than average by LFCarry’s estimate. It conjures its own food and water, and slows and freezes enemies. In Forever, Frost gained Ice Lance and Fingers of Frost.', 'Маг — один із найшвидших класів на прокачуванні, за оцінкою LFCarry, приблизно на 8% швидший за середній показник. Сам робить собі їжу й воду, уповільнює та заморожує ворогів. У Forever у Льоду з’явилися Ice Lance і Fingers of Frost.', de='Der Magier gehört zu den schnellsten Klassen beim Leveln, laut Schätzung von LFCarry etwa 8 % schneller als der Durchschnitt. Er zaubert sich Essen und Wasser selbst und verlangsamt und gefriert Gegner. In Forever hat Frost Eislanze und Eisige Finger bekommen.', es='El Mago es una de las clases más rápidas para subir de nivel, cerca de un 8 % más rápida que la media, según LFCarry. Hace su propia comida y agua, y ralentiza y congela a los enemigos. En Forever, Escarcha recibió Lanza de hielo y Dedos de Escarcha.', fr='Le Mage est l’une des classes les plus rapides à monter, environ 8 % de mieux que la moyenne selon LFCarry. Il fabrique lui-même sa nourriture et son eau, ralentit et gèle les ennemis. Dans Forever, Givre a gagné Javelot de glace et Doigts de givre.', it='Il Mago è una delle classi più veloci a livellare, circa l’8% più della media secondo LFCarry. Si crea da solo cibo e acqua, rallenta e congela i nemici. In Forever Gelo ha ottenuto Lancia di Ghiaccio e Dita di Gelo.', pl='Mage to jedna z najszybszych klas do levelowania, według szacunku LFCarry mniej więcej o 8% szybsza od średniej. Sam robi sobie jedzenie i wodę, spowalnia i zamraża wrogów. W Forever Frost dostał Ice Lance i Fingers of Frost.', pt='O Mago é uma das classes mais rápidas para subir de nível, cerca de 8% mais rápida que a média, segundo o LFCarry. Ele cria a própria comida e água, e deixa os inimigos lentos e congelados. No Forever, Gélido ganhou Lança de Gelo e Dedos Glaciais.'),
    'tile': t('Лёд, Ледяное копьё и таланты по уровням', 'Frost, Ice Lance and talents by level', 'Лід, Ice Lance і таланти за рівнями'),
    'pills': [t('Спек: Лёд', 'Spec: Frost', 'Спек: Лід'), t('Таланты 10–60', 'Talents 10–60', 'Таланти 10–60'), tx('По бете', 'Beta data', 'За бетою', de='Betadaten', fr='Données de la bêta', pt='Dados da beta')],
    'sources': [
        ('Icy Veins: Frost Mage Leveling', 'https://www.icy-veins.com/wow-forever/frost-mage-leveling'),
        ('Mobalytics: Mage Leveling 1-30', 'https://mobalytics.gg/wow-forever/classes/mage-leveling-guide'),
        ('Warcraft Tavern: Mage Leveling', 'https://www.warcrafttavern.com/forever/guides/mage-leveling/'),
    ],
    'sections': [
        {'id': 'spec', 'title': t('Какой спек качать', 'Which spec to level', 'Який спек прокачувати'), 'blocks': [
            ('text', [
                t('Качайте Лёд. Это совет Warcraft Tavern, Mobalytics и Icy Veins: Ледяная стрела замедляет, Кольцо льда держит врага на месте, а Ледяное копье по замороженной цели бьёт в разы сильнее. Враги редко до вас добегают. В тир-листе прокачки это S.', 'Level Frost. This is the advice of Warcraft Tavern, Mobalytics and Icy Veins: Frostbolt slows, Frost Nova holds the enemy in place, and Ice Lance on a frozen target hits several times harder. Enemies rarely reach you. In the leveling tier list it is S.', 'Прокачуйте Лід. Це порада Warcraft Tavern, Mobalytics та Icy Veins: Frostbolt уповільнює, Frost Nova тримає ворога на місці, а Ice Lance по замороженій цілі б’є в рази сильніше. Вороги рідко до вас добігають. У тір-листі прокачування це S.'),
                t('Огонь тратит меньше маны, но зависит от критов. Тайная магия зависит от срабатываний и маны. Оба спека, по Tavern, лучше в подземельях, чем в открытом мире.', 'Fire costs less mana but depends on crits. Arcane depends on procs and mana. According to Tavern, both specs are better in dungeons than in the open world.', 'Вогонь витрачає менше мани, але залежить від критів. Тайна магія залежить від спрацьовувань і мани. За Tavern, обидва спеки кращі в підземеллях, ніж у відкритому світі.'),
            ]),
            ('table', {'head': [tx('Спек', 'Spec', 'Спек', de='Skillung', es='Espec.', fr='Spé', it='Spec.', pl='Spec', pt='Espec.'), t('Когда брать', 'When to take it', 'Коли брати'), t('Минус', 'Downside', 'Мінус')], 'rows': [
                [t('Лёд', 'Frost', 'Лід'), t('Соло и группы, весь путь до 60', 'Solo and groups, the whole way to 60', 'Соло та групи, увесь шлях до 60'), t('Нужна удача на срабатывания, много воды', 'Needs luck with procs, a lot of water', 'Потрібна вдача на спрацьовування, багато води')],
                [t('Огонь', 'Fire', 'Вогонь'), t('Подземелья, любителям критов', 'Dungeons, fans of crits', 'Підземелля, любителям критів'), t('Без крита урон проседает', 'Without crits, damage drops', 'Без крита шкода просідає')],
                [t('Тайная магия', 'Arcane', 'Тайна магія'), t('Подземелья, бурст', 'Dungeons, burst', 'Підземелля, бурст'), t('Быстро сжигает ману', 'Burns mana fast', 'Швидко спалює ману')],
            ]}),
        ]},
        {'id': 'talents', 'title': t('Таланты по уровням', 'Talents by level', 'Таланти за рівнями'), 'blocks': [
            ('text', [
                t('Порядок Icy Veins для Льда (обновлён 16.10). Уровни 31–60 на бете закрыты: это план источника, проверим после старта 05.11.', 'Icy Veins order for Frost (updated Oct 16). Levels 31–60 are closed on the beta: this is the source’s plan, and we will check it after the Nov 4–5 launch.', 'Порядок Icy Veins для Льоду (оновлено 16 жовтня). Рівні 31–60 у беті закриті: це план джерела, перевіримо після старту 5 листопада.'),
            ]),
            ('table', {'head': [t('Уровни', 'Levels', 'Рівні'), t('Талант', 'Talent', 'Талант'), t('Очки', 'Points', 'Очки')], 'rows': [
                ['10–14', t('Улучшенная ледяная стрела (Improved Frostbolt)', 'Improved Frostbolt', 'Improved Frostbolt'), '5'],
                ['15–17', t('Обморожение (Frostbite)', 'Frostbite', 'Frostbite'), '3'],
                ['18–19', t('Ледяные осколки (Ice Shards)', 'Ice Shards', 'Ice Shards'), '2'],
                ['20', t('Ледяное копье (Ice Lance)', 'Ice Lance', 'Ice Lance'), '1'],
                ['21–22', t('Заградительные стрелы (Missile Barrage)', 'Missile Barrage', 'Missile Barrage'), '2'],
                ['23', t('Направленная сила льда (Frost Channeling)', 'Frost Channeling', 'Frost Channeling'), '1'],
                ['24–26', t('Ледяные осколки (Ice Shards)', 'Ice Shards', 'Ice Shards'), '5/5'],
                ['27–29', t('Обледенение (Shatter)', 'Shatter', 'Shatter'), '3'],
                ['30', t('Ледяная глыба (Ice Block)', 'Ice Block', 'Ice Block'), '1'],
                ['31', t('Предел льда (Arctic Reach)', 'Arctic Reach', 'Arctic Reach'), '1'],
                ['32–33', t('Ледяные пальцы (Fingers of Frost)', 'Fingers of Frost', 'Fingers of Frost'), '2'],
                ['34–35', t('Направленная сила льда (Frost Channeling)', 'Frost Channeling', 'Frost Channeling'), '3/3'],
                ['36', t('Холодная хватка (Cold Snap)', 'Cold Snap', 'Cold Snap'), '1'],
                ['37–41', t("Зимняя стужа (Winter's Chill)", "Winter's Chill", "Winter's Chill"), '5'],
                ['42', t('Ледяная преграда (Ice Barrier)', 'Ice Barrier', 'Ice Barrier'), '1'],
                ['43–45', t('Улучшенный конус холода (Improved Cone of Cold)', 'Improved Cone of Cold', 'Improved Cone of Cold'), '3'],
                ['46', t('Предел льда (Arctic Reach)', 'Arctic Reach', 'Arctic Reach'), '2/2'],
                ['47–49', t('Испепеление (Incineration)', 'Incineration', 'Incineration'), '3'],
                ['50', t('Улучшенная снежная буря (Improved Blizzard)', 'Improved Blizzard', 'Improved Blizzard'), '1'],
                ['51–52', t('Вечная мерзлота (Permafrost)', 'Permafrost', 'Permafrost'), '2'],
                ['53–55', t('Точность стихии (Elemental Precision)', 'Elemental Precision', 'Elemental Precision'), '3'],
                ['56–58', t('Средоточие чар (Arcane Focus)', 'Arcane Focus', 'Arcane Focus'), '3'],
                ['59–60', t('Искусные чары (Arcane Subtlety)', 'Arcane Subtlety', 'Arcane Subtlety'), '2'],
            ]}),
            ('tip', t('Mobalytics (18.10) до 30 уровня не берёт Заградительные стрелы, Направленная сила льда и Ледяная глыба: вместо них Пронзающий лед 3/3 и Улучшенная снежная буря, а Ледяные пальцы — уже на 30. Перк Legacy Talented даёт таланты до 5 уровней раньше.', 'Mobalytics (Oct 18) does not take Missile Barrage, Frost Channeling and Ice Block before level 30: instead Piercing Ice 3/3 and Improved Blizzard, and Fingers of Frost already at 30. The Legacy Talented perk gives talents up to 5 levels earlier.', 'Mobalytics (18 жовтня) до 30 рівня не бере Missile Barrage, Frost Channeling і Ice Block: замість них Piercing Ice 3/3 та Improved Blizzard, а Fingers of Frost — уже на 30. Перк Legacy Talented дає таланти до 5 рівнів раніше.')),
        ]},
        {'id': 'abilities', 'title': t('Способности и тренер', 'Abilities and trainer', 'Здібності й тренер'), 'blocks': [
            ('text', [BETA_TRAINER]),
            ('table', {'head': [t('Уровень', 'Level', 'Рівень'), t('Что взять', 'What to take', 'Що взяти'), tx('Зачем', 'Why', 'Навіщо', de='Wozu', es='Para qué', it='A cosa serve', pl='Po co', pt='Para quê')], 'rows': [
                ['1', t('Огненный шар, Морозный доспех, Чародейский интеллект', 'Fireball, Frost Armor, Arcane Intellect', 'Fireball, Frost Armor, Arcane Intellect'), t('Урон до 4 уровня, броня, бафф', 'Damage until level 4, armor, a buff', 'Шкода до 4 рівня, броня, бафф')],
                ['4', t('Ледяная стрела, Сотворение воды', 'Frostbolt, Conjure Water', 'Frostbolt, Conjure Water'), t('Главное заклинание, своя вода', 'The main spell, your own water', 'Головне заклинання, своя вода')],
                ['6', t('Сотворение пищи, Огненный взрыв, Понимание', 'Conjure Food, Fire Blast, Comprehension', 'Conjure Food, Fire Blast, Comprehension'), t('Еда, мгновенный удар, чтение свитков', 'Food, an instant strike, reading scrolls', 'Їжа, миттєвий удар, читання сувоїв')],
                ['8', t('Превращение, Чародейские снаряды', 'Polymorph, Arcane Missiles', 'Polymorph, Arcane Missiles'), t('Контроль опасного врага', 'Control of a dangerous enemy', 'Контроль небезпечного ворога')],
                ['10', t('Кольцо льда', 'Frost Nova', 'Frost Nova'), t('Заморозить и отойти', 'Freeze and step away', 'Заморозити й відійти')],
                ['14', t('Чародейский взрыв', 'Arcane Explosion', 'Arcane Explosion'), t('Урон по площади вокруг себя', 'Area damage around you', 'Шкода по площі навколо себе')],
                ['20', t('Скачок, Прилив сил, Снежная буря, Щит маны, телепорт в столицу', 'Blink, Evocation, Blizzard, Mana Shield, a teleport to a capital city', 'Blink, Evocation, Blizzard, Mana Shield, телепорт до столиці'), t('Отступление, мана, урон по площади', 'Retreat, mana, area damage', 'Відступ, мана, шкода по площі')],
                ['24', t('Антимагия', 'Counterspell', 'Counterspell'), t('Прерывание', 'An interrupt', 'Переривання')],
                ['40', t('Порталы, Огненно-ледяная стрела, верховая езда, вторая специализация', 'Portals, Frostfire Bolt, riding, dual specialization', 'Портали, Frostfire Bolt, верхова їзда, друга спеціалізація'), '—'],
            ]}),
            ('steps', [
                {'t': t('Перед боем', 'Before the fight', 'Перед боєм'),
                 'd': t('Морозный доспех и Чародейский интеллект; Морозный доспех может вызвать Обморожение у атакующего.', 'Frost Armor and Arcane Intellect; Frost Armor can trigger Frostbite on an attacker.', 'Frost Armor і Arcane Intellect; Frost Armor може викликати Frostbite в атакуючого.')},
                {'t': t('Вход', 'Opening', 'Вхід'),
                 'd': t('Ледяная стрела с максимальной дистанции.', 'Frostbolt from maximum range.', 'Frostbolt з максимальної дистанції.')},
                {'t': t('В бою', 'In the fight', 'У бою'),
                 'd': t('Ледяная стрела; Ледяное копье, когда враг заморожен или сработали Ледяные пальцы. Подошёл вплотную — Кольцо льда и отойти; если она на откате — Конус холода.', 'Frostbolt; Ice Lance when the enemy is frozen or Fingers of Frost procs. If the enemy gets close, Frost Nova and step away; if it is on cooldown, Cone of Cold.', 'Frostbolt; Ice Lance, коли ворог заморожений або спрацювали Fingers of Frost. Підійшов упритул — Frost Nova і відійти; якщо вона на відкаті — Cone of Cold.')},
                {'t': tx('Добивание', 'Finishing', 'Добивання', de='Erledigen', fr='Achever', pl='Dobijanie'),
                 'd': t('жезлом: так мана копится к следующему врагу.', 'with the wand: that way mana builds up for the next enemy.', 'паличкою: так мана накопичується до наступного ворога.')},
            ]),
            ('text', [
                t('Соберите несколько врагов, заморозьте их (Кольцо льда), отойдите, дальше — Снежная буря; Конус холода даёт время отступить, Чародейский взрыв добивает. Урон по площади дорогой по мане, а в Forever он для прокачки ослаблен. В подземельях не начинайте раньше танка.', 'Gather several enemies, freeze them (Frost Nova), step away, then Blizzard; Cone of Cold buys time to retreat, and Arcane Explosion finishes them off. Area damage costs a lot of mana, and in Forever it is weakened for leveling. In dungeons, don’t start before the tank.', 'Зберіть кількох ворогів, заморозьте їх (Frost Nova), відійдіть, далі Blizzard; Cone of Cold дає час відступити, Arcane Explosion добиває. Шкода по площі дорога за маною, а у Forever для прокачування вона послаблена. У підземеллях не починайте раніше за танка.'),
            ]),
        ]},
        {'id': 'play', 'title': t('Соло, вдвоём, в группе', 'Solo, duo, group', 'Соло, удвох, у групі'), 'blocks': [
            ('tabs', [
                {'id': 'solo', 't': tx('Соло', 'Solo', 'Соло', es='En solitario', pt='Solo'), 'blocks': [('text', [t('Перед боем держите стопку еды и воды. Всегда оставляйте ману на Кольцо льда и Скачок: это ваш выход из плохого боя. Жезл возьмите как можно раньше: Малый магический жезл с 5 уровня (Icy Veins).', 'Before a fight, keep a stack of food and water. Always keep mana for Frost Nova and Blink: that is your way out of a bad fight. Get a wand as early as possible: Lesser Magic Wand from level 5 (Icy Veins).', 'Перед боєм тримайте стос їжі та води. Завжди лишайте ману на Frost Nova і Blink: це ваш вихід із поганого бою. Паличку візьміть якомога раніше: Lesser Magic Wand з 5 рівня (Icy Veins).')])]},
                {'id': 'duo', 't': tx('Вдвоём', 'Duo', 'Удвох', de='Zu zweit', es='En pareja', fr='À deux', it='In coppia', pl='We dwoje', pt='Em dupla'), 'blocks': [('text', [t('Делайте напарнику еду и воду. Превращение убирает одного врага из боя, пока вы вдвоём бьёте другого.', 'Conjure food and water for your partner. Polymorph takes one enemy out of the fight while the two of you hit the other.', 'Робіть напарнику їжу й воду. Polymorph прибирає одного ворога з бою, поки ви вдвох б’єте іншого.')])]},
                {'id': 'party', 't': t('Группа', 'Group', 'Група'), 'blocks': [('text', [t('Снежная буря и Чародейский взрыв легко снимают угрозу с танка: начинайте после него. С 20 уровня телепорт в столицу, с 40 — порталы для группы.', 'Blizzard and Arcane Explosion easily pull threat off the tank: start after them. From level 20, a teleport to a capital city; from 40, portals for the group.', 'Blizzard і Arcane Explosion легко знімають загрозу з танка: починайте після нього. З 20 рівня телепорт до столиці, з 40 — портали для групи.')])]},
            ]),
        ]},
        {'id': 'gear', 'title': t('Характеристики и снаряжение', 'Stats and gear', 'Характеристики та спорядження'), 'blocks': [
            ('text', [
                t('Mobalytics: сила заклинаний, интеллект (крит заклинаний и мана), дух, выносливость. Жезл возьмите как можно раньше. Покупайте реагенты: руны телепортации и лёгкие перья для заклинаний (Mobalytics). Камень маны и Прилив сил позволяют дольше обходиться без воды.', 'Mobalytics: spell power, Intellect (spell crit and mana), Spirit, Stamina. Get a wand as early as possible. Buy reagents: Rune of Teleportation and Light Feather for spells (Mobalytics). A Mana Gem and Evocation let you go longer without water.', 'Mobalytics: сила заклинань, інтелект (крит заклинань і мана), дух, витривалість. Паличку візьміть якомога раніше. Купуйте реагенти: Rune of Teleportation і Light Feather для заклинань (Mobalytics). Mana Gem і Evocation дозволяють довше обходитися без води.'),
                t('Пары профессий под класс и объекты лагеря — в гайде по профессиям.', 'Class profession pairings and camp objects are in the professions guide.', 'Пари професій під клас і об’єкти табору — у гайді з професій.'),
            ]),
        ]},
        {'id': 'forever', 'title': t('Чем Forever отличается от Classic', 'How Forever differs from Classic', 'Чим Forever відрізняється від Classic'), 'blocks': [
            ('table', {'head': [t('Что', 'What', 'Що'), t('В Forever', 'In Forever', 'У Forever')], 'rows': [
                [t('Лёд', 'Frost', 'Лід'), t('Новые таланты: Ледяное копье (в разы сильнее по замороженной цели), Ледяные пальцы.', 'New talents: Ice Lance (several times stronger against a frozen target), Fingers of Frost.', 'Нові таланти: Ice Lance (в рази сильніше по замороженій цілі), Fingers of Frost.')],
                [t('Огонь и Тайная магия', 'Fire and Arcane', 'Вогонь і Тайна магія'), t('Новые таланты Путь огня и Чародейская вспышка.', 'New talents Hotstreak and Arcane Blast.', 'Нові таланти Hotstreak і Arcane Blast.')],
                [t('Огненно-ледяная стрела', 'Frostfire Bolt', 'Frostfire Bolt'), t('С 40 уровня.', 'From level 40.', 'З 40 рівня.')],
                [t('Чародейская медитация', 'Arcane Meditation', 'Arcane Meditation'), t('До 50% восполнения маны в бою (было 15%).', 'Up to 50% mana regeneration in combat (it was 15%).', 'До 50% відновлення мани в бою (було 15%).')],
                [t('Урон по площади', 'Area damage', 'Шкода по площі'), t('Для прокачки ослаблен.', 'Weakened for leveling.', 'Для прокачування послаблена.')],
                [t('Понимание', 'Comprehension', 'Comprehension'), t('Новый навык с 6 уровня: чтение свитков.', 'A new skill from level 6: reading scrolls.', 'Нова навичка з 6 рівня: читання сувоїв.')],
                [t('Вторая специализация', 'Dual specialization', 'Друга спеціалізація'), t('С 40 уровня.', 'From level 40.', 'З 40 рівня.')],
            ]}),
        ]},
        {'id': 'faq', 'title': t('Вопросы', 'Questions', 'Питання'), 'blocks': [
            ('faq', [
                {'id': 'q1', 'q': t('Какой спек Мага качать в WoW Forever?', 'Which Mage spec should I level in WoW Forever?', 'Який спек Мага прокачувати у WoW Forever?'),
                 'a': [t('Лёд: его советуют Warcraft Tavern, Mobalytics и Icy Veins.', 'Frost: Warcraft Tavern, Mobalytics and Icy Veins recommend it.', 'Лід: його радять Warcraft Tavern, Mobalytics та Icy Veins.')]},
                {'id': 'q2', 'q': t('Можно ли качаться по площади, как в Classic?', 'Can I level by area damage as in Classic?', 'Чи можна прокачуватися по площі, як у Classic?'),
                 'a': [t('Можно, но урон по площади в Forever для прокачки ослаблен и дорогой по мане. Основной путь — бой по одному врагу: Ледяная стрела, Ледяное копье.', 'You can, but in Forever area damage is weakened for leveling and expensive in mana. The main route is fighting one enemy at a time: Frostbolt, Ice Lance.', 'Можна, але у Forever шкода по площі для прокачування послаблена й дорога за маною. Основний шлях — бій по одному ворогу: Frostbolt, Ice Lance.')]},
                {'id': 'q3', 'q': t('Когда появляется Ледяное копье?', 'When does Ice Lance appear?', 'Коли з’являється Ice Lance?'),
                 'a': [t('Это талант ветки Льда: Icy Veins берёт его на 20 уровне.', 'It is a Frost tree talent: Icy Veins takes it at level 20.', 'Це талант гілки Льоду: Icy Veins бере його на 20 рівні.')]},
                {'id': 'q4', 'q': t('Где Маг берёт еду и воду?', 'Where does a Mage get food and water?', 'Де Маг бере їжу й воду?'),
                 'a': [t('Делает сам: вода с 4 уровня, еда с 6.', 'It conjures them itself: water from level 4, food from level 6.', 'Робить сам: вода з 4 рівня, їжа з 6.')]},
                {'id': 'q5', 'q': t('Когда открываются телепорты и порталы?', 'When do teleports and portals open?', 'Коли відкриваються телепорти й портали?'),
                 'a': [t('Телепорт в столицу с 20 уровня, порталы для группы с 40.', 'A teleport to a capital city from level 20, portals for the group from 40.', 'Телепорт до столиці з 20 рівня, портали для групи з 40.')]},
            ]),
        ]},
        {'id': 'related', 'title': t('Смотрите также', 'See also', 'Дивіться також'), 'blocks': [
            ('tiles', _related('mage', [
                t('Маг', 'Mage', 'Маг'),
                tx('Прокачка 1–60', 'Leveling 1–60', 'Прокачування 1–60', fr='Monter de 1 à 60', it='Livellare 1–60', pt='Evoluir 1–60'),
                t('Лучшая раса', 'Best race', 'Найкраща раса'),
                t('Тир-лист', 'Tier list', 'Тір-лист'),
            ])),
        ]},
    ],
})

# ---------- warlock ----------

CLASS_GUIDES.append({
    'slug': 'leveling-warlock', 'art': 'warlock', 'hero': 'hero_leveling', 'hub': False,
    'title': t('Прокачка Чернокнижника 1–60', 'Warlock Leveling 1–60', 'Прокачування Чорнокнижника 1–60'),
    'lead': t('Чернокнижник качается в среднем темпе, но почти без отдыха: демон держит врага, эффекты тьмы убивают, а Жизнеотвод и Похищение жизни меняют здоровье на ману и обратно. В Forever эффекты со временем могут критовать.', 'Warlock levels at an average pace, but almost without rest: the demon holds the enemy, shadow effects do the killing, and Life Tap and Drain Life trade health for mana and back. In Forever, effects over time can crit.', 'Чорнокнижник прокачується в середньому темпі, але майже без відпочинку: демон тримає ворога, ефекти темряви вбивають, а Life Tap і Drain Life міняють здоров’я на ману й навпаки. У Forever ефекти з часом можуть критувати.'),
    'tile': t('Колдовство, демоны и таланты по уровням', 'Affliction, demons and talents by level', 'Прокляття, демони й таланти за рівнями'),
    'pills': [t('Спек: Колдовство', 'Spec: Affliction', 'Спек: Прокляття'), t('Таланты 10–60', 'Talents 10–60', 'Таланти 10–60'), tx('По бете', 'Beta data', 'За бетою', de='Betadaten', fr='Données de la bêta', pt='Dados da beta')],
    'sources': [
        ('Icy Veins: Affliction Warlock Leveling', 'https://www.icy-veins.com/wow-forever/affliction-warlock-leveling'),
        ('Mobalytics: Warlock Leveling 1-60', 'https://mobalytics.gg/wow-forever/classes/warlock-leveling-guide'),
        ('Warcraft Tavern: Warlock Leveling', 'https://www.warcrafttavern.com/forever/guides/warlock-leveling/'),
    ],
    'sections': [
        {'id': 'spec', 'title': t('Какой спек качать', 'Which spec to level', 'Який спек прокачувати'), 'blocks': [
            ('text', [
                t('Качайте Колдовство. Warcraft Tavern называет его самым плавным стартом, Icy Veins и Mobalytics дают для него гайды прокачки 1–60. Мгновенная Порча работает на бегу, можно вести двух врагов сразу, а пить почти не нужно.', 'Level Affliction. Warcraft Tavern calls it the smoothest start, and Icy Veins and Mobalytics both have 1–60 leveling guides for it. The instant Corruption works on the move, you can keep two enemies going at once, and you hardly need to drink.', 'Прокачуйте Прокляття. Warcraft Tavern називає його найплавнішим стартом, Icy Veins та Mobalytics дають для нього гайди прокачування 1–60. Миттєва Corruption працює на бігу, можна вести двох ворогів одразу, а пити майже не треба.'),
                t('Демонология тоже сильна: Mobalytics считает её равной Колдовству и более прощающей ошибки, Tavern — самой удобной после таланта Demonic Brand. Разрушение соло самое тяжёлое: нужно стоять и читать заклинания, зато оно сильно в подземельях.', 'Demonology is strong too: Mobalytics considers it equal to Affliction and more forgiving, and Tavern calls it the most convenient after the Demonic Brand talent. Destruction is the hardest for solo: you have to stand and cast, but it is strong in dungeons.', 'Демонологія теж сильна: Mobalytics вважає її рівною Прокляттю й поблажливішою до помилок, Tavern — найзручнішою після таланту Demonic Brand. Руйнування соло найважче: треба стояти й читати заклинання, зате воно сильне в підземеллях.'),
            ]),
            ('table', {'head': [tx('Спек', 'Spec', 'Спек', de='Skillung', es='Espec.', fr='Spé', it='Spec.', pl='Spec', pt='Espec.'), t('Когда брать', 'When to take it', 'Коли брати'), t('Минус', 'Downside', 'Мінус')], 'rows': [
                [t('Колдовство', 'Affliction', 'Прокляття'), t('Соло, весь путь до 60', 'Solo, the whole way to 60', 'Соло, увесь шлях до 60'), t('В коротких боях эффекты не успевают нанести урон', 'In short fights the effects don’t have time to deal damage', 'У коротких боях ефекти не встигають завдати шкоди')],
                [t('Демонология', 'Demonology', 'Демонологія'), t('Хочется, чтобы демон делал больше', 'You want the demon to do more', 'Хочеться, щоб демон робив більше'), t('Раскрывается к Demonic Brand', 'Opens up around Demonic Brand', 'Розкривається до Demonic Brand')],
                [t('Разрушение', 'Destruction', 'Руйнування'), t('Подземелья', 'Dungeons', 'Підземелля'), t('Соло медленно', 'Slow solo', 'Соло повільно')],
            ]}),
        ]},
        {'id': 'talents', 'title': t('Таланты по уровням', 'Talents by level', 'Таланти за рівнями'), 'blocks': [
            ('text', [
                t('Порядок Mobalytics «танк через Похищение жизни» (обновлён 23.10). Warcraft Tavern идёт тем же путём: сначала Улучшенная порча и Подавление, с 30 уровня таланты на Похищение жизни. Уровни 31–60 на бете закрыты: это план источника, проверим после старта 05.11.', 'The Mobalytics "tank through Drain Life" order (updated Oct 23). Warcraft Tavern goes the same way: first Improved Corruption and Suppression, and from level 30 talents for Drain Life. Levels 31–60 are closed on the beta: this is the source’s plan, and we will check it after the Nov 4–5 launch.', 'Порядок Mobalytics «танк через Drain Life» (оновлено 23 жовтня). Warcraft Tavern іде тим самим шляхом: спочатку Improved Corruption і Suppression, з 30 рівня таланти на Drain Life. Рівні 31–60 у беті закриті: це план джерела, перевіримо після старту 5 листопада.'),
            ]),
            ('table', {'head': [t('Уровни', 'Levels', 'Рівні'), t('Талант', 'Talent', 'Талант'), t('Очки', 'Points', 'Очки')], 'rows': [
                ['10–14', t('Улучшенная порча (Improved Corruption)', 'Improved Corruption', 'Improved Corruption'), '5'],
                ['15–17', t('Подавление (Suppression)', 'Suppression', 'Suppression'), '3'],
                ['18–19', t('Предел мрака (Grim Reach)', 'Grim Reach', 'Grim Reach'), '2'],
                ['20–21', 'Soul Harvest', '2'],
                ['22–24', 'Improved Drains', '3'],
                ['25–26', t('Сумерки (Nightfall)', 'Nightfall', 'Nightfall'), '2'],
                ['27–29', t('Сосредоточение Скверны (Fel Concentration)', 'Fel Concentration', 'Fel Concentration'), '3'],
                ['30–32', t('Вытягивание души (Soul Siphon)', 'Soul Siphon', 'Soul Siphon'), '3'],
                ['33–34', t('Пандемия (Pandemic)', 'Pandemic', 'Pandemic'), '2'],
                ['35–39', t('Власть над Тенями (Shadow Mastery)', 'Shadow Mastery', 'Shadow Mastery'), '5'],
                ['40', t('Пандемия (Pandemic)', 'Pandemic', 'Pandemic'), '3/3'],
                ['41–45', t('Нечестивая сила (Unholy Power)', 'Unholy Power', 'Unholy Power'), '5'],
                ['46–47', 'Demonic Energies', '2'],
                ['48–52', 'Malevolence', '5'],
                ['53–55', t('Fel Vitality', 'Fel Vitality', 'Fel Vitality'), '3'],
                ['56–57', t('Мастер призыва (Master Summoner)', 'Master Summoner', 'Master Summoner'), '2'],
                ['58–60', t('На выбор', 'Your choice', 'На вибір'), '3'],
            ]}),
            ('tip', t('Icy Veins (21.10) идёт иначе: Подавление с 10 уровня, Вытягивание жизни на 30, затем Демонология (талант Демоническое жертвоприношение на 41), вершина Колдовства — Смятие на 51, а таланты на Похищение жизни — только к 53–60. Выбирайте один путь и не смешивайте. Перк Legacy Talented даёт таланты с 5 уровня вместо 10.', 'Icy Veins (Oct 21) goes differently: Suppression from level 10, Siphon Life at 30, then Demonology (Demonic Sacrifice at 41), the top of Affliction, Wrack, at 51, and talents for Drain Life only by 53–60. Pick one path and don’t mix them. The Legacy Talented perk gives talents from level 5 instead of 10.', 'Icy Veins (21 жовтня) іде інакше: Suppression з 10 рівня, Siphon Life на 30, потім Демонологія (талант Demonic Sacrifice на 41), вершина Прокляття — Wrack на 51, а таланти на Drain Life — лише до 53–60. Обирайте один шлях і не змішуйте. Перк Legacy Talented дає таланти з 5 рівня замість 10.')),
        ]},
        {'id': 'abilities', 'title': t('Способности и тренер', 'Abilities and trainer', 'Здібності й тренер'), 'blocks': [
            ('text', [BETA_TRAINER]),
            ('table', {'head': [t('Уровень', 'Level', 'Рівень'), t('Что взять', 'What to take', 'Що взяти'), tx('Зачем', 'Why', 'Навіщо', de='Wozu', es='Para qué', it='A cosa serve', pl='Po co', pt='Para quê')], 'rows': [
                ['1', t('Призыв беса (задание), Стрела Тьмы, Жертвенный огонь, Шкура демона', 'Summon Imp (quest), Shadow Bolt, Immolate, Demon Skin', 'Summon Imp (завдання), Shadow Bolt, Immolate, Demon Skin'), t('Первый демон и урон', 'The first demon and damage', 'Перший демон і шкода')],
                ['4', t('Порча', 'Corruption', 'Corruption'), t('Главный эффект тьмы', 'The main shadow effect', 'Головний ефект темряви')],
                ['6', t('Жизнеотвод', 'Life Tap', 'Life Tap'), t('Здоровье в ману', 'Health into mana', 'Здоров’я в ману')],
                ['8', t('Страх, Bane of Agony', 'Fear, Bane of Agony', 'Fear, Bane of Agony'), t('Контроль и урон со временем', 'Control and damage over time', 'Контроль і шкода з часом')],
                ['10', t('Призыв демона Бездны (задание), Похищение души, Создание камня здоровья', 'Summon Voidwalker (quest), Drain Soul, Create Healthstone', 'Summon Voidwalker (завдання), Drain Soul, Create Healthstone'), t('Демон-танк, осколки души', 'The tank demon, soul shards', 'Демон-танк, уламки душі')],
                ['12', t('Канал здоровья', 'Health Funnel', 'Health Funnel'), t('Лечить демона', 'Heal the demon', 'Лікувати демона')],
                ['14', t('Похищение жизни', 'Drain Life', 'Drain Life'), t('Урон и лечение себя', 'Damage and self-healing', 'Шкода й самолікування')],
                ['20', t('Призыв суккуба (задание), Демонический доспех, Ритуал призывания, Проклятие стихий', 'Summon Succubus (quest), Demon Armor, Ritual of Summoning, Curse of the Elements', 'Summon Succubus (завдання), Demon Armor, Ritual of Summoning, Curse of the Elements'), t('Демон для урона, призыв группы', 'A damage demon, summoning the group', 'Демон для шкоди, виклик групи')],
                ['30', t('Призыв охотника Скверны (задание), Вытягивание жизни (талант)', 'Summon Felhunter (quest), Siphon Life (talent)', 'Summon Felhunter (завдання), Siphon Life (талант)'), t('Демон против заклинателей', 'A demon against casters', 'Демон проти заклиначів')],
                ['38', t('Похищение жизни 4-го ранга', 'Drain Life rank 4', 'Drain Life 4-го рангу'), t('Mobalytics: заметный скачок урона', 'Mobalytics: a noticeable damage jump', 'Mobalytics: помітний стрибок шкоди')],
                ['40', t('Скакун по заданию класса, вторая специализация', 'Class quest mount, dual specialization', 'Скакун за завданням класу, друга спеціалізація'), '—'],
            ]}),
            ('steps', [
                {'t': t('Вход', 'Opening', 'Вхід'),
                 'd': t('демон идёт первым и набирает угрозу.', 'the demon goes first and builds threat.', 'демон іде першим і набирає загрозу.')},
                {'t': t('Эффекты', 'Effects', 'Ефекти'),
                 'd': t('Bane of Agony, Порча, на долгоживущем враге ещё Жертвенный огонь; с 30 уровня Вытягивание жизни.', 'Bane of Agony, Corruption, and on a long-lived enemy Immolate too; from level 30, Siphon Life.', 'Bane of Agony, Corruption, на довгоживучому ворогу ще Immolate; з 30 рівня Siphon Life.')},
                {'t': t('В бою', 'In the fight', 'У бою'),
                 'd': t('жезл или Похищение жизни. Сработали Сумерки — мгновенная Стрела Тьмы.', 'the wand or Drain Life. If Nightfall procs, an instant Shadow Bolt.', 'паличка або Drain Life. Спрацював Nightfall — миттєвий Shadow Bolt.')},
                {'t': t('Ресурсы', 'Resources', 'Ресурси'),
                 'd': t('здоровья больше, чем маны — Жизнеотвод; маны больше — Похищение жизни. Не накладывайте эффекты на врага, который умрёт раньше, чем они пройдут.', 'more health than mana: Life Tap; more mana: Drain Life. Don’t apply effects to an enemy that will die before they tick through.', 'здоров’я більше, ніж мани — Life Tap; мани більше — Drain Life. Не накладайте ефекти на ворога, який помре раніше, ніж вони пройдуть.')},
            ]),
            ('text', [
                t('Наложите эффекты на первого, напугайте его (Страх) и бейте второго с демоном. Вернулся первый — снова Страх (Warcraft Tavern). В подземельях раздайте Камни здоровья перед входом.', 'Apply the effects to the first one, scare it (Fear) and hit the second with the demon. When the first returns, Fear again (Warcraft Tavern). In dungeons, hand out Healthstones before you go in.', 'Накладіть ефекти на першого, налякайте його (Fear) і бийте другого з демоном. Повернувся перший — знову Fear (Warcraft Tavern). У підземеллях роздайте Healthstone перед входом.'),
            ]),
        ]},
        {'id': 'play', 'title': t('Соло, вдвоём, в группе', 'Solo, duo, group', 'Соло, удвох, у групі'), 'blocks': [
            ('tabs', [
                {'id': 'solo', 't': tx('Соло', 'Solo', 'Соло', es='En solitario', pt='Solo'), 'blocks': [('text', [t('Демон по ситуации: демон Бездны держит врага, суккуб с 20 уровня бьёт сильнее (его советует Mobalytics), охотник Скверны — против заклинателей. Жезл сильный до 30-х уровней. Осколки души: Похищение души 1-го ранга, пока демон держит врага.', 'The demon depends on the situation: the Voidwalker holds the enemy, the Succubus hits harder from level 20 (Mobalytics recommends it), the Felhunter works against casters. The wand is strong through the 30s. Soul shards: rank 1 Drain Soul while the demon holds the enemy.', 'Демон за ситуацією: Voidwalker тримає ворога, Succubus з 20 рівня б’є сильніше (його радить Mobalytics), Felhunter — проти заклиначів. Паличка сильна до тридцятих рівнів. Уламки душі: Drain Soul 1-го рангу, поки демон тримає ворога.')])]},
                {'id': 'duo', 't': tx('Вдвоём', 'Duo', 'Удвох', de='Zu zweit', es='En pareja', fr='À deux', it='In coppia', pl='We dwoje', pt='Em dupla'), 'blocks': [('text', [t('Проклятие стихий усиливает магический урон напарника. демон Бездны может танковать для пары без танка.', 'Curse of the Elements boosts your partner’s magic damage. The Voidwalker can tank for a pair with no tank.', 'Curse of the Elements підсилює магічну шкоду напарника. Voidwalker може танкувати для пари без танка.')])]},
                {'id': 'party', 't': t('Группа', 'Group', 'Група'), 'blocks': [('text', [t('Камни здоровья и Ритуал призывания: в Forever камни встреч больше не призывают игроков, остаётся только ритуал. Держите для него лишние осколки.', 'Healthstones and Ritual of Summoning: in Forever, meeting stones no longer summon players, only the ritual does. Keep spare shards for it.', 'Healthstone і Ritual of Summoning: у Forever камені зустрічі більше не прикликають гравців, лишається тільки ритуал. Тримайте для нього зайві уламки.')])]},
            ]),
        ]},
        {'id': 'gear', 'title': t('Характеристики и снаряжение', 'Stats and gear', 'Характеристики та спорядження'), 'blocks': [
            ('text', [
                bt(t("Выносливость Чернокнижнику ценнее, чем другим заклинателям: чем больше здоровья, тем больше маны даёт Жизнеотвод (Warcraft Tavern). На 20 уровне — заданием Staff of Soran'ruk (+34 к урону от тьмы и огня, +14 выносливости) или Orb of Soran'ruk, для сферы нужны осколки из Blackfathom Deeps и Shadowfang Keep. Жезл — Gravestone Scepter (29 урона в секунду).", "Stamina is worth more to a Warlock than to other casters: the more health you have, the more mana Life Tap gives (Warcraft Tavern). At level 20, a quest gives Staff of Soran'ruk (+34 shadow and fire damage, +14 Stamina) or Orb of Soran'ruk; the orb needs shards from Blackfathom Deeps and Shadowfang Keep. The wand is Gravestone Scepter (29 damage per second).", "Витривалість Чорнокнижнику цінніша, ніж іншим заклиначам: що більше здоров’я, то більше мани дає Life Tap (Warcraft Tavern). На 20 рівні завданням — Staff of Soran'ruk (+34 до шкоди від темряви й вогню, +14 витривалості) або Orb of Soran'ruk, для сфери потрібні уламки з Blackfathom Deeps і Shadowfang Keep. Паличка — Gravestone Scepter (29 шкоди на секунду)."), 2),
                t('Профессии: Портняжное дело даёт персональное снаряжение на тьму за Merchant’s Favor. Пары под класс и объекты лагеря — в гайде по профессиям.', 'Professions: Tailoring gives personal shadow gear for Merchant’s Favor. Class pairings and camp objects are in the professions guide.', 'Професії: Кравецтво дає персональне спорядження на темряву за Merchant’s Favor. Пари під клас і об’єкти табору — у гайді з професій.'),
            ]),
        ]},
        {'id': 'forever', 'title': t('Чем Forever отличается от Classic', 'How Forever differs from Classic', 'Чим Forever відрізняється від Classic'), 'blocks': [
            ('table', {'head': [t('Что', 'What', 'Що'), t('В Forever', 'In Forever', 'У Forever')], 'rows': [
                [t('Проклятия', 'Curses', 'Прокляття'), t('Разделены на Бичи (урон) и Проклятия (польза): на цели может быть по одному каждого.', 'Split into Banes (damage) and Curses (utility): a target can have one of each.', 'Розділені на Banes (шкода) і Curses (користь): на цілі може бути по одному з кожного.')],
                [t('Эффекты со временем', 'Effects over time', 'Ефекти з часом'), t('Могут критовать. Лимита эффектов на цели нет (в Classic было 16).', 'Can crit. There is no limit on effects on a target (it was 16 in Classic).', 'Можуть критувати. Ліміту ефектів на цілі немає (у Classic було 16).')],
                [t('Осколки души', 'Soul shards', 'Уламки душі'), t('Похищение души может давать осколок с каждого тика.', 'Drain Soul can give a shard on every tick.', 'Drain Soul може давати уламок з кожного тіку.')],
                [t('Жизнеотвод', 'Life Tap', 'Life Tap'), t('Растёт от духа.', 'Scales with Spirit.', 'Росте від духу.')],
                [t('Демоны', 'Demons', 'Демони'), t('демон Бездны лучше держит угрозу, у демонов есть команда «Идти».', 'The Voidwalker holds threat better, and demons have a "Move to" command.', 'Voidwalker краще тримає загрозу, у демонів є команда «Іти».')],
                [t('Страх', 'Fear', 'Fear'), t('Дальность 20 м.', '20 yd range.', 'Дальність 20 м.')],
                [t('Призыв', 'Summoning', 'Виклик'), t('Камни встреч не призывают, только Ритуал призывания.', 'Meeting stones don’t summon, only Ritual of Summoning does.', 'Камені зустрічі не прикликають, лише Ritual of Summoning.')],
                [t('Камни огня и чар', 'Firestone and Spellstone', 'Firestone і Spellstone'), t('Стали маслами для оружия.', 'Became weapon oils.', 'Стали оліями для зброї.')],
                [t('Вторая специализация', 'Dual specialization', 'Друга спеціалізація'), t('С 40 уровня.', 'From level 40.', 'З 40 рівня.')],
            ]}),
        ]},
        {'id': 'faq', 'title': t('Вопросы', 'Questions', 'Питання'), 'blocks': [
            ('faq', [
                {'id': 'q1', 'q': t('Какой спек Чернокнижника качать в WoW Forever?', 'Which Warlock spec should I level in WoW Forever?', 'Який спек Чорнокнижника прокачувати у WoW Forever?'),
                 'a': [t('Колдовство: его советуют Warcraft Tavern, Mobalytics и Icy Veins. Демонология почти не уступает.', 'Affliction: Warcraft Tavern, Mobalytics and Icy Veins recommend it. Demonology is almost as good.', 'Прокляття: його радять Warcraft Tavern, Mobalytics та Icy Veins. Демонологія майже не поступається.')]},
                {'id': 'q2', 'q': t('Какого демона держать на прокачке?', 'Which demon should I keep while leveling?', 'Якого демона тримати на прокачуванні?'),
                 'a': [t('До 20 — демона Бездны, потом суккуба для урона (Mobalytics). демон Бездны надёжнее, если враги сильные.', 'The Voidwalker until 20, then the Succubus for damage (Mobalytics). The Voidwalker is more reliable if enemies are strong.', 'До 20 — Voidwalker, потім Succubus для шкоди (Mobalytics). Voidwalker надійніший, якщо вороги сильні.')]},
                {'id': 'q3', 'q': t('Где брать осколки души?', 'Where do I get soul shards?', 'Де брати уламки душі?'),
                 'a': [t('Похищение души на умирающем враге. В Forever осколок может падать с каждого тика.', 'Drain Soul on a dying enemy. In Forever a shard can drop on every tick.', 'Drain Soul на ворогу, що вмирає. У Forever уламок може випадати з кожного тіку.')]},
                {'id': 'q4', 'q': t('Почему таланты у разных сайтов такие разные?', 'Why are the talents so different on different sites?', 'Чому таланти на різних сайтах такі різні?'),
                 'a': [t('Mobalytics и Warcraft Tavern строят «танк через Похищение жизни» с 20-х уровней, Icy Veins откладывает это до 50-х и раньше берёт Демонологию. Оба пути рабочие.', 'Mobalytics and Warcraft Tavern build "tank through Drain Life" from the 20s, while Icy Veins postpones it to the 50s and takes Demonology earlier. Both paths work.', 'Mobalytics і Warcraft Tavern будують «танк через Drain Life» з двадцятих рівнів, Icy Veins відкладає це на п’ятдесяті й раніше бере Демонологію. Обидва шляхи робочі.')]},
                {'id': 'q5', 'q': t('Нужно ли покупать скакуна?', 'Do I need to buy a mount?', 'Чи треба купувати скакуна?'),
                 'a': [t('Нет, на 40 уровне скакуна даёт задание класса.', 'No, at level 40 a class quest gives you a mount.', 'Ні, на 40 рівні скакуна дає завдання класу.')]},
            ]),
        ]},
        {'id': 'related', 'title': t('Смотрите также', 'See also', 'Дивіться також'), 'blocks': [
            ('tiles', _related('warlock', [
                t('Чернокнижник', 'Warlock', 'Чорнокнижник'),
                tx('Прокачка 1–60', 'Leveling 1–60', 'Прокачування 1–60', fr='Monter de 1 à 60', it='Livellare 1–60', pt='Evoluir 1–60'),
                t('Лучшая раса', 'Best race', 'Найкраща раса'),
                t('Тир-лист', 'Tier list', 'Тір-лист'),
            ])),
        ]},
    ],
})

# ---------- druid ----------

CLASS_GUIDES.append({
    'slug': 'leveling-druid', 'art': 'druid', 'hero': 'hero_leveling', 'hub': False,
    'title': t('Прокачка Друида 1–60', 'Druid Leveling 1–60', 'Прокачування Друїда 1–60'),
    'lead': tx('Друид качается чуть медленнее среднего, по оценке LFCarry примерно на 5%: до 10 и 20 уровня у него нет обликов. Дальше кошка быстро убивает по одному, медведь держит толпу, а лечение и Походный облик с 30 уровня почти убирают простои.', 'Druid levels a little slower than average, about 5% by LFCarry’s estimate: it has no forms until levels 10 and 20. After that the cat kills quickly one at a time, the bear holds a crowd, and healing plus Travel Form from level 30 almost remove the downtime.', 'Друїд прокачується трохи повільніше за середній показник, за оцінкою LFCarry приблизно на 5%: до 10 і 20 рівня в нього немає форм. Далі кіт швидко вбиває по одному, ведмідь тримає натовп, а лікування та Travel Form з 30 рівня майже прибирають простої.', de='Der Druide levelt etwas langsamer als der Durchschnitt, laut LFCarry etwa 5 %: Bis Stufe 10 und 20 hat er keine Gestalten. Danach tötet die Katze schnell einzeln, der Bär hält eine Menge, und Heilung samt Reisegestalt ab Stufe 30 beseitigen fast alle Leerlaufzeiten.', es='El Druida sube algo más despacio que la media, cerca de un 5 % según LFCarry: hasta los niveles 10 y 20 no tiene formas. Después el gato mata rápido de uno en uno, el oso sujeta a una multitud, y la curación y Forma de viaje desde el nivel 30 casi eliminan los tiempos muertos.', fr='Le Druide monte un peu plus lentement que la moyenne, d’environ 5 % selon LFCarry : il n’a pas de formes avant les niveaux 10 et 20. Ensuite le chat tue vite un par un, l’ours retient la foule, et les soins et Forme de voyage dès le niveau 30 suppriment presque les temps morts.', it='Il Druido livella un po’ più lentamente della media, circa il 5% secondo LFCarry: fino ai livelli 10 e 20 non ha forme. Dopo, il gatto uccide in fretta uno alla volta, l’orso trattiene la folla, e le cure e Forma Celere dal livello 30 eliminano quasi del tutto i tempi morti.', pl='Druid leveluje się nieco wolniej od średniej, według LFCarry o około 5%: do levelu 10 i 20 nie ma form. Potem kot szybko zabija po jednym, niedźwiedź trzyma tłum, a leczenie i Travel Form od levelu 30 prawie likwidują przestoje.', pt='O Druida evolui um pouco mais devagar que a média, cerca de 5%, segundo o LFCarry: até os níveis 10 e 20 ele não tem formas. Depois, o gato mata rápido um de cada vez, o urso segura a multidão, e a cura e Forma de Viagem a partir do nível 30 quase eliminam os tempos parados.'),
    'tile': t('Сила зверя, облики и таланты по уровням', 'Feral, forms and talents by level', 'Сила звіра, форми й таланти за рівнями'),
    'pills': [t('Спек: Сила зверя', 'Spec: Feral', 'Спек: Сила звіра'), t('Таланты 10–60', 'Talents 10–60', 'Таланти 10–60'), tx('По бете', 'Beta data', 'За бетою', de='Betadaten', fr='Données de la bêta', pt='Dados da beta')],
    'sources': [
        ('Icy Veins: Feral Druid Leveling', 'https://www.icy-veins.com/wow-forever/feral-druid-leveling'),
        ('Mobalytics: Druid Leveling 1-30', 'https://mobalytics.gg/wow-forever/classes/druid-leveling-guide'),
        ('Warcraft Tavern: Druid Leveling', 'https://www.warcrafttavern.com/forever/guides/druid-leveling/'),
    ],
    'sections': [
        {'id': 'spec', 'title': t('Какой спек качать', 'Which spec to level', 'Який спек прокачувати'), 'blocks': [
            ('text', [
                t('Качайте Силу зверя и играйте кошкой. Это совет Warcraft Tavern, Mobalytics и Icy Veins: у кошки рано есть Крадущийся зверь и Порыв, урон по одной цели и лечение себя между боями. Против нескольких врагов переходите в медведя.', 'Level Feral and play the cat. This is the advice of Warcraft Tavern, Mobalytics and Icy Veins: the cat gets Prowl and Dash early, single-target damage and self-healing between fights. Against several enemies, switch to the bear.', 'Прокачуйте Силу звіра й грайте котом. Це порада Warcraft Tavern, Mobalytics та Icy Veins: у кота рано є Prowl і Dash, шкода по одній цілі та самолікування між боями. Проти кількох ворогів переходьте у ведмедя.'),
                t('Оценки темпа расходятся: тир-лист прокачки даёт Друиду A со звёздочкой (от C до A), потому что многие ключевые умения открываются после 30 уровня. Баланс всё время тратит ману и на урон, и на лечение. Исцеление на прокачке, по Mobalytics, неожиданно сильное, но медленнее кошки.', 'Pace estimates differ: the leveling tier list gives Druid an A with an asterisk (from C to A), because many key abilities open after level 30. Balance spends mana on both damage and healing all the time. Restoration while leveling is, per Mobalytics, surprisingly strong, but slower than the cat.', 'Оцінки темпу розходяться: тір-лист прокачування дає Друїду A із зірочкою (від C до A), бо багато ключових умінь відкривається після 30 рівня. Баланс увесь час витрачає ману і на шкоду, і на лікування. Зцілення на прокачуванні, за Mobalytics, несподівано сильне, але повільніше за кота.'),
            ]),
            ('table', {'head': [tx('Спек', 'Spec', 'Спек', de='Skillung', es='Espec.', fr='Spé', it='Spec.', pl='Spec', pt='Espec.'), t('Когда брать', 'When to take it', 'Коли брати'), t('Минус', 'Downside', 'Мінус')], 'rows': [
                [t('Сила зверя', 'Feral', 'Сила звіра'), t('Соло и подземелья, весь путь до 60', 'Solo and dungeons, the whole way to 60', 'Соло та підземелля, увесь шлях до 60'), t('Медленно до 20 уровня (Облик кошки)', 'Slow until level 20 (Cat Form)', 'Повільно до 20 рівня (Cat Form)')],
                [t('Баланс', 'Balance', 'Баланс'), t('Любителям дальнего боя', 'Fans of ranged combat', 'Любителям дальнього бою'), t('Мана и на урон, и на лечение', 'Mana for both damage and healing', 'Мана і на шкоду, і на лікування')],
                [t('Исцеление', 'Restoration', 'Зцілення'), t('Как вторая специализация с 40', 'As a second specialization from 40', 'Як друга спеціалізація з 40'), t('Мало урона соло', 'Little damage solo', 'Мало шкоди соло')],
            ]}),
        ]},
        {'id': 'talents', 'title': t('Таланты по уровням', 'Talents by level', 'Таланти за рівнями'), 'blocks': [
            ('text', [
                t('Порядок Icy Veins для Силы зверя (обновлён 18.10). Уровни 31–60 на бете закрыты: это план источника, проверим после старта 05.11.', 'Icy Veins order for Feral (updated Oct 18). Levels 31–60 are closed on the beta: this is the source’s plan, and we will check it after the Nov 4–5 launch.', 'Порядок Icy Veins для Сили звіра (оновлено 18 жовтня). Рівні 31–60 у беті закриті: це план джерела, перевіримо після старту 5 листопада.'),
            ]),
            ('table', {'head': [t('Уровни', 'Levels', 'Рівні'), t('Талант', 'Talent', 'Талант'), t('Очки', 'Points', 'Очки')], 'rows': [
                ['10–14', t('Свирепость (Ferocity)', 'Ferocity', 'Ferocity'), '5'],
                ['15–16', t('Жестокий удар (Brutal Impact)', 'Brutal Impact', 'Brutal Impact'), '2'],
                ['17–18', t('Feral Swiftness', 'Feral Swiftness', 'Feral Swiftness'), '2'],
                ['19', t('Животный инстинкт (Feral Instinct)', 'Feral Instinct', 'Feral Instinct'), '1'],
                ['20–21', t('Бешеное неистовство (Savage Fury)', 'Savage Fury', 'Savage Fury'), '2'],
                ['22–24', t('Shredding Attacks', 'Shredding Attacks', 'Shredding Attacks'), '3'],
                ['25', t('Переходящая сила (Shifting Power)', 'Shifting Power', 'Shifting Power'), '1'],
                ['26', 'Primal Bite', '1'],
                ['27', t('Звериная атака (Feral Charge)', 'Feral Charge', 'Feral Charge'), '1'],
                ['28–29', t('Животный инстинкт (Feral Instinct)', 'Feral Instinct', 'Feral Instinct'), '3'],
                ['30', t('Вожак стаи (Leader of the Pack)', 'Leader of the Pack', 'Leader of the Pack'), '1'],
                ['31–32', 'Improved Shifting Power', '2'],
                ['33–34', t('Острые когти (Sharpened Claws)', 'Sharpened Claws', 'Sharpened Claws'), '2'],
                ['35–36', 'Blood Frenzy', '2'],
                ['37–38', 'Natural Instinct', '2'],
                ['39', t('Удары хищника (Predatory Strikes)', 'Predatory Strikes', 'Predatory Strikes'), '1'],
                ['40', t('Берсерк (Berserk)', 'Berserk', 'Berserk'), '1'],
                ['41–45', 'Genesis', '5'],
                ['46–47', t("Предел сил Природы (Nature's Reach)", "Nature's Reach", "Nature's Reach"), '2'],
                ['48–49', "Nature's Majesty", '2'],
                ['50–51', t('Удары хищника (Predatory Strikes)', 'Predatory Strikes', 'Predatory Strikes'), '3/3'],
                ['52–56', 'Rend and Tear', '5'],
                ['57–60', t('Сердце дикой природы (Heart of the Wild)', 'Heart of the Wild', 'Heart of the Wild'), '4'],
            ]}),
            ('tip', t('Mobalytics (09.10, до патча 15.10) после Свирепость 5/5 берёт Сердце дикой природы 3/5, а Feral Swiftness — раньше: +30% к скорости в облике кошки, уклонение во всех обликах. Warcraft Tavern пропускает Shredding Attacks. Перк Legacy Talented даёт таланты до 5 уровней раньше.', 'Mobalytics (Oct 9, before the Oct 15 patch) takes Heart of the Wild 3/5 after Ferocity 5/5, and Feral Swiftness earlier: +30% speed in cat form, dodge in all forms. Warcraft Tavern skips Shredding Attacks. The Legacy Talented perk gives talents up to 5 levels earlier.', 'Mobalytics (9 жовтня, до патча 15 жовтня) після Ferocity 5/5 бере Heart of the Wild 3/5, а Feral Swiftness — раніше: +30% до швидкості у формі кота, ухилення в усіх формах. Warcraft Tavern пропускає Shredding Attacks. Перк Legacy Talented дає таланти до 5 рівнів раніше.')),
        ]},
        {'id': 'abilities', 'title': t('Способности и тренер', 'Abilities and trainer', 'Здібності й тренер'), 'blocks': [
            ('text', [BETA_TRAINER]),
            ('table', {'head': [t('Уровень', 'Level', 'Рівень'), t('Что взять', 'What to take', 'Що взяти'), tx('Зачем', 'Why', 'Навіщо', de='Wozu', es='Para qué', it='A cosa serve', pl='Po co', pt='Para quê')], 'rows': [
                ['1', t('Гнев, Знак дикой природы, Целительное прикосновение', 'Wrath, Mark of the Wild, Healing Touch', 'Wrath, Mark of the Wild, Healing Touch'), t('Урон, бафф, лечение', 'Damage, a buff, healing', 'Шкода, бафф, лікування')],
                ['4', t('Лунный огонь, Омоложение', 'Moonfire, Rejuvenation', 'Moonfire, Rejuvenation'), t('Мгновенный урон и лечение', 'Instant damage and healing', 'Миттєва шкода й лікування')],
                ['6', t('Шипы', 'Thorns', 'Thorns'), t('Урон тем, кто бьёт вас', 'Damage to those who hit you', 'Шкода тим, хто б’є вас')],
                ['8', t('Гнев деревьев', 'Entangling Roots', 'Entangling Roots'), t('Удержать врага', 'Hold an enemy', 'Утримати ворога')],
                ['10', t('Облик медведя (задание), Трепка, Устрашающий рев', 'Bear Form (quest), Maul, Demoralizing Roar', 'Bear Form (завдання), Maul, Demoralizing Roar'), t('Первый облик', 'The first form', 'Перша форма')],
                ['12', t('Восстановление, Оживление', 'Regrowth, Revive', 'Regrowth, Revive'), t('Лечение, воскрешение вне боя', 'Healing, out-of-combat resurrection', 'Лікування, воскресіння поза боєм')],
                ['14', t('Оглушить', 'Bash', 'Bash'), t('Оглушение', 'A stun', 'Приголомшення')],
                ['16', t('Размах; Водный облик (задание)', 'Swipe; Aquatic Form (quest)', 'Swipe; Aquatic Form (завдання)'), t('Урон по площади в медведе', 'Area damage in bear form', 'Шкода по площі у ведмедеві')],
                ['18', t('Волшебный огонь', 'Faerie Fire', 'Faerie Fire'), t('Вытянуть врага, не выходя из облика', 'Pull an enemy without leaving your form', 'Витягнути ворога, не виходячи з форми')],
                ['20', t('Облик кошки (задание), Когти, Крадущийся зверь, Разорвать, Полоснуть; древковое у тренера оружия', 'Cat Form (quest), Claw, Prowl, Rip, Shred; polearms from the weapon trainer', 'Cat Form (завдання), Claw, Prowl, Rip, Shred; держакова зброя в тренера зброї'), t('Главный облик прокачки', 'The main leveling form', 'Головна форма прокачування')],
                ['24', t('Глубокая рана', 'Rake', 'Rake'), t('Кровотечение', 'A bleed', 'Кровотеча')],
                ['26', t('Порыв', 'Dash', 'Dash'), t('Бег', 'Running', 'Біг')],
                ['30', t('Походный облик', 'Travel Form', 'Travel Form'), t('Скорость в пути за 10 уровней до скакуна', 'Travel speed 10 levels before a mount', 'Швидкість у дорозі за 10 рівнів до скакуна')],
                ['32', t('Свирепый укус', 'Ferocious Bite', 'Ferocious Bite'), t('Сильный завершающий удар', 'A strong finisher', 'Сильний завершальний удар')],
                ['40', t('Облик лютого медведя, Озарение, верховая езда, вторая специализация', 'Dire Bear Form, Innervate, riding, dual specialization', 'Dire Bear Form, Innervate, верхова їзда, друга спеціалізація'), '—'],
                ['44', t('Дубовая кожа', 'Barkskin', 'Barkskin'), t('Защита в бою', 'Defense in combat', 'Захист у бою')],
            ]}),
            ('steps', [
                {'t': t('Перед боем', 'Before the fight', 'Перед боєм'),
                 'd': t('Знак дикой природы и Шипы (Шипы держатся 10 минут); на сильного врага заранее Восстановление: лечение со временем 21 секунду продолжится в бою.', 'Mark of the Wild and Thorns (Thorns last 10 minutes); on a strong enemy, Regrowth in advance: the 21-second heal over time will keep going in combat.', 'Mark of the Wild і Thorns (Шипи тримаються 10 хвилин); на сильного ворога заздалегідь Regrowth: лікування з часом на 21 секунду триватиме й у бою.')},
                {'t': t('Вход', 'Opening', 'Вхід'),
                 'd': t('Волшебный огонь или Лунный огонь издалека, затем Когти; со спины — Полоснуть.', 'Faerie Fire or Moonfire from range, then Claw; from behind, Shred.', 'Faerie Fire або Moonfire здалеку, потім Claw; зі спини — Shred.')},
                {'t': t('В бою', 'In the fight', 'У бою'),
                 'd': t('Глубокая рана, при 4–5 очках серии Разорвать; на умирающего врага кровотечения не тратьте.', 'Rake, Rip at 4–5 combo points; don’t waste bleeds on a dying enemy.', 'Rake, при 4–5 балах серії Rip; на ворога, що вмирає, кровотечі не витрачайте.')},
                {'t': t('Несколько врагов', 'Several enemies', 'Кілька ворогів'),
                 'd': t('Облик медведя: Устрашающий рев, Размах по нескольким, Трепка по одному.', 'Bear Form: Demoralizing Roar, Swipe on several, Maul on one.', 'Bear Form: Demoralizing Roar, Swipe по кількох, Maul по одному.')},
            ]),
            ('text', [
                t('До 10 уровня: Лунный огонь на двух врагах, Омоложение на себя, Гнев при лишней мане, добивание оружием. Шипы с 6 уровня делают бой с двумя врагами выгодным (Mobalytics).', 'Until level 10: Moonfire on two enemies, Rejuvenation on yourself, Wrath with spare mana, finish with the weapon. Thorns from level 6 make a fight against two enemies worthwhile (Mobalytics).', 'До 10 рівня: Moonfire на двох ворогах, Rejuvenation на себе, Wrath за зайвої мани, добивання зброєю. Thorns з 6 рівня роблять бій із двома ворогами вигідним (Mobalytics).'),
            ]),
        ]},
        {'id': 'play', 'title': t('Соло, вдвоём, в группе', 'Solo, duo, group', 'Соло, удвох, у групі'), 'blocks': [
            ('tabs', [
                {'id': 'solo', 't': tx('Соло', 'Solo', 'Соло', es='En solitario', pt='Solo'), 'blocks': [('text', [t('Лечитесь вне боя и не стесняйтесь выйти из облика: смена облика снимает корни и замедления. Носите воду: облики тратят ману. Озарение позволяет тянуть дальше без питья.', 'Heal outside combat and don’t hesitate to leave your form: shifting breaks roots and slows. Carry water: forms cost mana. Innervate lets you keep pulling without drinking.', 'Лікуйтеся поза боєм і не соромтеся виходити з форми: зміна форми знімає корені та уповільнення. Носіть воду: форми витрачають ману. Innervate дозволяє тягнути далі без пиття.')])]},
                {'id': 'duo', 't': tx('Вдвоём', 'Duo', 'Удвох', de='Zu zweit', es='En pareja', fr='À deux', it='In coppia', pl='We dwoje', pt='Em dupla'), 'blocks': [('text', [t('Друид закрывает любую дыру пары: медведь танкует, кошка бьёт, в паузах лечит обоих. Вешайте Знак дикой природы и Шипы на напарника.', 'Druid fills any gap in a pair: the bear tanks, the cat hits, and in the pauses it heals both. Put Mark of the Wild and Thorns on your partner.', 'Друїд закриває будь-яку діру пари: ведмідь танкує, кіт б’є, у паузах лікує обох. Вішайте Mark of the Wild і Thorns на напарника.')])]},
                {'id': 'party', 't': t('Группа', 'Group', 'Група'), 'blocks': [('text', [t('Медведь танкует ранние подземелья, Mobalytics пишет, что их можно и лечить. Вожак стаи с 30 уровня усиливает и вас, и группу.', 'The bear tanks early dungeons, and Mobalytics writes that you can heal them too. Leader of the Pack from level 30 strengthens both you and the group.', 'Ведмідь танкує ранні підземелля, Mobalytics пише, що їх можна й лікувати. Leader of the Pack з 30 рівня підсилює і вас, і групу.')])]},
            ]),
        ]},
        {'id': 'gear', 'title': t('Характеристики и снаряжение', 'Stats and gear', 'Характеристики та спорядження'), 'blocks': [
            ('text', [
                t('Урон кошки и медведя в Forever растёт от оружия: берите оружие с максимальным уроном в секунду (Mobalytics). Warcraft Tavern отмечает для прокачки Wolfshead Helm, Manual Crowd Pummeler и комплект Embrace of the Viper из Wailing Caverns; Idol of Shifting Tides даёт задание на водный облик.', 'The cat’s and bear’s damage in Forever scales with the weapon: take the weapon with the highest damage per second (Mobalytics). For leveling, Warcraft Tavern notes Wolfshead Helm, Manual Crowd Pummeler and the Embrace of the Viper set from Wailing Caverns; Idol of Shifting Tides gives the quest for aquatic form.', 'Шкода кота й ведмедя у Forever росте від зброї: беріть зброю з максимальною шкодою на секунду (Mobalytics). Для прокачування Warcraft Tavern відзначає Wolfshead Helm, Manual Crowd Pummeler і комплект Embrace of the Viper з Wailing Caverns; Idol of Shifting Tides дає завдання на водну форму.'),
                t('Пары профессий под класс и объекты лагеря — в гайде по профессиям.', 'Class profession pairings and camp objects are in the professions guide.', 'Пари професій під клас і об’єкти табору — у гайді з професій.'),
            ]),
        ]},
        {'id': 'forever', 'title': t('Чем Forever отличается от Classic', 'How Forever differs from Classic', 'Чим Forever відрізняється від Classic'), 'blocks': [
            ('table', {'head': [t('Что', 'What', 'Що'), t('В Forever', 'In Forever', 'У Forever')], 'rows': [
                [t('Облики', 'Forms', 'Форми'), t('Урон кошки и медведя растёт от урона оружия, есть свой навык оружия. В облике можно пить зелья.', 'Cat and bear damage scales with weapon damage, and there is its own weapon skill. You can drink potions in form.', 'Шкода кота й ведмедя росте від шкоди зброї, є власна навичка зброї. У формі можна пити зілля.')],
                [t('Волшебный огонь и Природный захват', "Faerie Fire and Nature's Grasp", "Faerie Fire і Nature's Grasp"), t('Базовые у тренера, таланты не нужны.', 'Baseline from the trainer, no talents needed.', 'Базові в тренера, таланти не потрібні.')],
                [t('Гнев деревьев', 'Entangling Roots', 'Entangling Roots'), t('Работает в помещениях.', 'Works indoors.', 'Працює в приміщеннях.')],
                [t('Оружие', 'Weapons', 'Зброя'), bt(t('Древковое с 20 уровня.', 'Polearms from level 20.', 'Держакова з 20 рівня.'), 1)],
                [t('Оживление', 'Revive', 'Revive'), t('Новое: воскрешение вне боя с 12 уровня.', 'New: out-of-combat resurrection from level 12.', 'Нове: воскресіння поза боєм з 12 рівня.')],
                [tx('Восстановление', 'Regeneration', 'Відновлення', pl='Regeneracja'), t('Мана и энергия восстанавливаются ровно, без рывков раз в 2 секунды.', 'Mana and energy regenerate smoothly, without a jump every 2 seconds.', 'Мана й енергія відновлюються рівно, без ривків раз на 2 секунди.')],
                [t('Очки серии', 'Combo points', 'Бали серії'), t('По Mobalytics переходят на новую цель. Icy Veins (о разбойнике) пишет, что остаются на прежней: проверим на старте.', 'Per Mobalytics they carry over to the new target. Icy Veins (about the Rogue) writes that they stay on the previous one: we will check at launch.', 'За Mobalytics переходять на нову ціль. Icy Veins (про розбійника) пише, що лишаються на попередній: перевіримо на старті.')],
                [tx('Новые таланты', 'New talents', 'Нові таланти', pt='Talentos novos'), t('Берсерк, Переходящая сила, Primal Bite.', 'Berserk, Shifting Power, Primal Bite.', 'Berserk, Shifting Power, Primal Bite.')],
                [t('Вторая специализация', 'Dual specialization', 'Друга спеціалізація'), t('С 40 уровня.', 'From level 40.', 'З 40 рівня.')],
            ]}),
        ]},
        {'id': 'faq', 'title': t('Вопросы', 'Questions', 'Питання'), 'blocks': [
            ('faq', [
                {'id': 'q1', 'q': t('Какой спек Друида качать в WoW Forever?', 'Which Druid spec should I level in WoW Forever?', 'Який спек Друїда прокачувати у WoW Forever?'),
                 'a': [t('Силу зверя кошкой: так советуют Warcraft Tavern, Mobalytics и Icy Veins.', 'Feral as a cat: Warcraft Tavern, Mobalytics and Icy Veins recommend it.', 'Силу звіра котом: так радять Warcraft Tavern, Mobalytics та Icy Veins.')]},
                {'id': 'q2', 'q': t('Когда появляются облики?', 'When do the forms appear?', 'Коли з’являються форми?'),
                 'a': [bt(t('Медведь на 10 уровне (задание), водный облик на 16 (задание), кошка на 20 (задание), Походный облик на 30.', 'The bear at level 10 (quest), aquatic form at 16 (quest), the cat at 20 (quest), Travel Form at 30.', 'Ведмідь на 10 рівні (завдання), водна форма на 16 (завдання), кіт на 20 (завдання), Travel Form на 30.'), 1)]},
                {'id': 'q3', 'q': t('Кошка или медведь?', 'Cat or bear?', 'Кіт чи ведмідь?'),
                 'a': [t('Кошка против одного врага, медведь против нескольких (Icy Veins).', 'The cat against one enemy, the bear against several (Icy Veins).', 'Кіт проти одного ворога, ведмідь проти кількох (Icy Veins).')]},
                {'id': 'q4', 'q': t('Почему Друид медленный в начале?', 'Why is the Druid slow at the start?', 'Чому Друїд повільний на початку?'),
                 'a': [t('До 10 и 20 уровня нет обликов, приходится бить заклинаниями и тратить ману. После 20 темп заметно растёт.', 'There are no forms until levels 10 and 20, so you have to hit with spells and spend mana. After 20 the pace picks up noticeably.', 'До 10 і 20 рівня немає форм, доводиться бити заклинаннями й витрачати ману. Після 20 темп помітно зростає.')]},
                {'id': 'q5', 'q': t('Можно ли на одном Друиде танковать, лечить и бить?', 'Can one Druid tank, heal and deal damage?', 'Чи можна на одному Друїді танкувати, лікувати й бити?'),
                 'a': [t('Да. С 40 уровня вторая специализация позволяет держать, например, Силу зверя и Исцеление.', 'Yes. From level 40, dual specialization lets you keep, for example, Feral and Restoration.', 'Так. З 40 рівня друга спеціалізація дозволяє тримати, наприклад, Силу звіра та Зцілення.')]},
            ]),
        ]},
        {'id': 'related', 'title': t('Смотрите также', 'See also', 'Дивіться також'), 'blocks': [
            ('tiles', _related('druid', [
                t('Друид', 'Druid', 'Друїд'),
                tx('Прокачка 1–60', 'Leveling 1–60', 'Прокачування 1–60', fr='Monter de 1 à 60', it='Livellare 1–60', pt='Evoluir 1–60'),
                t('Лучшая раса', 'Best race', 'Найкраща раса'),
                t('Тир-лист', 'Tier list', 'Тір-лист'),
            ])),
        ]},
    ],
})

def attach(guides, hubs, order):
    """Connect the nine guides: tile texts of the related links, GUIDES, the «Прокачка по классам» section of the leveling guide."""
    by = {g['slug']: g for g in guides}
    hub = {h['slug']: h for h in hubs}
    desc = {'classes/': hub['classes']['tile'], 'guides/leveling/': by['leveling']['tile'],
            'guides/best-race/': by['best-race']['tile'], 'guides/tier-list/': by['tier-list']['tile']}
    tiles = []
    for g in CLASS_GUIDES:
        cid = g['slug'].removeprefix('leveling-')
        g['tile_art'] = cid                                  # «Другие гайды»: the class art, not nine copies of hero_leveling
        sec = g['sections'][-1]
        assert sec['id'] == 'related'
        for x in sec['blocks'][0][1]:
            x['d'] = desc['classes/' if x['href'].startswith('classes/') else x['href'].split('#')[0]]
        tiles.append({'t': sec['blocks'][0][1][0]['t'], 'd': g['tile'], 'href': f'guides/{g["slug"]}/', 'art': cid})
    guides.extend(CLASS_GUIDES)
    lv = by['leveling']['sections']
    sec = {'id': 'classes', 'title': CLASSES_TITLE,
           'blocks': [('text', [CLASSES_LEAD]), ('tiles', tiles)]}
    lv.insert(next(i for i, s in enumerate(lv) if s['id'] == 'pace') + 1, sec)
    guides.sort(key=lambda g: order.index(g['slug']))
