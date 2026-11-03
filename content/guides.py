"""Гайды: тексты сразу на трёх языках. Строка = {'ru': …, 'en': …, 'uk': …}.
Названия игровых объектов на EN/UK английские. Факты — только из источников в 'sources'.
Блок = (тип, данные):
  ('text', [строка, …])                                 абзацы
  ('steps', [{'t': строка, 'd': строка}, …])           нумерованный список 1/2/3
  ('tiles', [{'t', 'd', 'href', 'art'}, …])            плитки с артом; href относительно корня гида, art = имя без размера
  ('play', {'h', 'd', 'go'})                           строка-ссылка на «В игре» (гайд «Прокачка»)
  ('table', {'head': [строка, …], 'rows': [[строка|str, …], …]})
  ('tabs', [{'id': 'alliance', 't': строка, 'blocks': [блок, …]}, …])
  ('faq', [{'id': 'release', 'q': строка, 'a': [строка, …], 'link': (строка, url)?}, …])   link — кнопка под ответом
  ('tip', строка)
  ('addons', {'head': [...], 'items': [{'n', 'd', 'url', 'langs'?}, …]})   строка аддона: имя, что делает, кнопка CurseForge
  ('raw', 'html')   только для живых частей, разметка с data-атрибутами для JS"""


def t(ru, en, uk):
    return {'ru': ru, 'en': en, 'uk': uk}


HUB = {
    'slug': '', 'art': 'hero_campfire', 'hero': 'hero_guides',
    'title': t('Гайды', 'Guides', 'Гайди'),
    'lead': t('Прокачка, подземелья, профессии, ответы на вопросы и новости WoW Forever.',
              'Leveling, dungeons, professions, answers and news for WoW Forever.',
              'Прокачка, підземелля, професії, відповіді на питання та новини WoW Forever.'),
}

GUIDES = []   # наполняется в задачах 3, 5, 6, 7, 9; каждый гайд дописывается ниже через GUIDES.append

NEWS = []     # записи «Новостей», шаблон и порядок выпуска: tools/news_watch.py + docs news-auto (задача news-auto с фактами поста)
# {'date': '2026-10-23', 'title': t(...), 'text': t(3–5 строк сути), 'so'?: t(что это значит для игрока), 'url': 'https://…' — первоисточник Blizzard,
#  'cls'?: 'all' | 'mage priest'} — cls: «касается вашего класса» для «Моего персонажа»
# На странице: заголовок + ОДНА строка — 'so', а без него 'text'. 'so' = что меняется для вас (дата, условие, действие),
#  а не «Подробности — в статье Blizzard»: вся запись и так ссылка на первоисточник.
from build import DISCORD_AT  # noqa: E402  (у каждого места ссылки своё приглашение)
from content import tierlist_live as TL  # noqa: E402  (тир-лист: «по бете» / «по живой игре» и дата, data/tierlist.json)
TL_STATUS = TL.load()

ORDER = ['name-reservation', 'launch-checklist', 'launch-day', 'leveling', 'leveling-warrior', 'leveling-paladin', 'leveling-hunter', 'leveling-rogue', 'leveling-priest', 'leveling-shaman', 'leveling-mage', 'leveling-warlock', 'leveling-druid', 'builds', 'builds-warrior', 'builds-paladin', 'builds-hunter', 'builds-rogue', 'builds-priest', 'builds-shaman', 'builds-mage', 'builds-warlock', 'builds-druid', 'spec-hunter-beast-mastery', 'spec-mage-frost', 'spec-paladin-protection', 'spec-priest-discipline', 'best-race', 'tier-list', 'pvp', 'legacy', 'dungeons', 'professions', 'addons', 'faq', 'glossary', 'requirements', 'server-status', 'news', 'ukrainian']   # порядок плиток на хабе и в «Другие гайды»


# ---------- FAQ: даты и наборы, режимы, имена, отличия от Era (переехали с главной) + частые вопросы ----------

GUIDES.append({
    'slug': 'faq', 'art': 'mage', 'hero': 'hero_faq', 'js': 'faq',
    'title': t('FAQ и даты', 'FAQ and dates', 'FAQ і дати'),
    'lead': t('Даты до и после релиза, цены и подписка, режимы и серверы, имена, графика и ответы на частые вопросы.',
              'Dates before and after release, prices and subscription, modes and servers, names, graphics and answers to common questions.',
              'Дати до й після релізу, ціни та підписка, режими та сервери, імена, графіка та відповіді на часті питання.'),
    'tile': t('Даты, наборы, режимы и ответы на вопросы', 'Dates, packs, modes and answers', 'Дати, набори, режими та відповіді'),
    'pills': [t('Релиз 05.11.2026', 'Release 04.11 / 05.11.2026', 'Реліз 05.11.2026'),
              t('Имена: 27.10 – 03.11', 'Names: 27.10 – 03.11', 'Імена: 27.10 – 03.11'),
              t('Рейды 09.12', 'Raids 09.12', 'Рейди 09.12')],
    'sources': [
        (t('ClassicWoW.gg: даты беты, имён, рейдов, отличия от Classic Era', 'ClassicWoW.gg: beta, names, raids, Classic Era differences',
           'ClassicWoW.gg: дати бети, імен, рейдів, відмінності від Classic Era'), 'https://classicwow.gg/forever'),
        (t('Icy Veins: время резерва имён по регионам', 'Icy Veins: name reservation times by region', 'Icy Veins: час резерву імен за регіонами'),
         'https://www.icy-veins.com/wow-forever/news/wow-forever-early-name-reservation-dates-amounts-and-times-revealed/'),
        (t('Icy Veins: время закрытия беты', 'Icy Veins: beta end time', 'Icy Veins: час закриття бети'),
         'https://www.icy-veins.com/wow-forever/news/wow-forever-beta-end-time-and-stress-test-starting-times-by-time-zone/'),
        (t('Warcraft Tavern: наборы и цены', 'Warcraft Tavern: editions and prices', 'Warcraft Tavern: набори та ціни'),
         'https://www.warcrafttavern.com/news/world-of-warcraft-forever-editions-skyborne-race-unlock-beta-access/'),
        (t('Warcraft Tavern: изменения беты от 15 октября', 'Warcraft Tavern: 15 October beta changes', 'Warcraft Tavern: зміни бети від 15 жовтня'),
         'https://www.warcrafttavern.com/forever/news/racial-class-ability-changes-in-the-wow-forever-beta/'),
        (t('Warcraft Tavern: расы', 'Warcraft Tavern: races', 'Warcraft Tavern: раси'), 'https://www.warcrafttavern.com/forever/guides/races/'),
        (t('Team Overpowered: имена и фамилии', 'Team Overpowered: names and surnames', 'Team Overpowered: імена та прізвища'),
         'https://teamoverpowered.com/forever/guides/name-reservation/'),
        (t('Battle.net: Forever, наборы, регионы', 'Battle.net: Forever, packs, regions', 'Battle.net: Forever, набори, регіони'),
         'https://eu.shop.battle.net/en-gb/product/world-of-warcraft-forever'),
        (t('Battle.net: цены подписки', 'Battle.net: subscription prices', 'Battle.net: ціни підписки'),
         'https://us.shop.battle.net/en-us/product/world-of-warcraft-subscription'),
        (t('Blizzard: старт и коды Invite-A-Friend', 'Blizzard: launch and Invite-A-Friend codes', 'Blizzard: старт і коди Invite-A-Friend'),
         'https://news.blizzard.com/en-us/article/24301508'),
        (t('Blizzard: режим RP-PvP к старту', 'Blizzard: RP-PvP mode for launch', 'Blizzard: режим RP-PvP до старту'),
         'https://us.forums.blizzard.com/en/wow/t/the-roleplay-pvp-ruleset-is-coming-to-wow-forever/2389502'),
        (t('Method: серверы и режимы', 'Method: servers and modes', 'Method: сервери та режими'),
         'https://www.method.gg/wow-forever/choosing-your-character-name-and-ruleset-in-wow-forever'),
        (t('Conquest Capped: Classic или Enhanced', 'Conquest Capped: Classic or Enhanced', 'Conquest Capped: Classic чи Enhanced'),
         'https://conquestcapped.com/guides/wow-forever/wow-forever-classic-look/'),
        # the home page list of sources lives here since 25.10 (the home has one line with a link)
        (t('Warcraft Tavern: комбинации рас и классов', 'Warcraft Tavern: race and class combinations', 'Warcraft Tavern: поєднання рас і класів'),
         'https://www.warcrafttavern.com/forever/guides/race-class-combos/'),
        (t('Method: все комбинации и способности рас', 'Method: all combinations and racial abilities', 'Method: усі поєднання та здібності рас'),
         'https://www.method.gg/wow-forever/all-class-and-race-combinations-in-world-of-warcraft-forever'),
        (t('Blizzard: система Legacy', 'Blizzard: Legacy system', 'Blizzard: система Legacy'), 'https://news.blizzard.com/en-gb/article/24307383'),
        (t('LFCarry: классы и темп прокачки', 'LFCarry: classes and leveling pace', 'LFCarry: класи та темп прокачування'), 'https://lfcarry.com/guides/wow-forever-classes'),
        ('Wowhead', 'https://www.wowhead.com/forever'),
    ],
    'sections': [
        {'id': 'dates', 'title': t('Даты', 'Dates', 'Дати'), 'blocks': [
            ('table', {'head': [t('Когда', 'When', 'Коли'), t('Событие', 'Event', 'Подія'), t('Что важно', 'What matters', 'Що важливо')], 'rows': [
                ['17.09 – 23.10', t('Закрытая бета', 'Closed beta', 'Закрита бета'),
                 t('Доступ был у владельцев наборов Epic и Collection. Бета завершилась 23.10 в 10:00 по тихоокеанскому времени. 08.10 в бету добавили [[Даларан|City of Dalaran]] и примерно на 20% больше опыта за врагов в подземельях.',
                   'Access was for Epic and Collection owners. The beta ended on 23.10 at 10:00 Pacific time. On 08.10 the beta got City of Dalaran and about 20% more experience for enemies in dungeons.',
                   'Доступ мали власники наборів Epic і Collection. Бета завершилася 23.10 о 10:00 за тихоокеанським часом. 08.10 у бету додали City of Dalaran і приблизно на 20% більше досвіду за ворогів у підземеллях.')],
                ['15.10', t('Крупный патч беты', 'Major beta patch', 'Великий патч бети'),
                 t('Переделаны способности рас (оружейные специализации заменены критами) и настроены почти все классы.',
                   'Racial abilities were reworked (weapon specializations replaced with crits) and almost all classes were tuned.',
                   'Переробили здібності рас (спеціалізації зброї замінили критами) і налаштували майже всі класи.')],
                ['27.10 – 03.11', t('Ранняя резервация имён', 'Early name reservation', 'Рання резервація імен'),
                 t('Идёт с 27.10 по 03.11 для владельцев Heroic, Epic и Collection. До трёх персонажей на аккаунт во всех режимах вместе, кто первым пришёл, тот и занял. Это не ранний доступ в игру. Старт по Киеву: Европа 27.10 в 19:00, Америка 27.10 в 22:00, Корея 28.10 в 00:00, Тайвань 28.10 в 01:00.',
                   'Runs from 27.10 to 03.11 for Heroic, Epic and Collection owners. Up to three characters per account across all modes, first come, first served. This is not early access to the game. Start in Kyiv time: Europe 27.10 at 19:00, the Americas 27.10 at 22:00, Korea 28.10 at 00:00, Taiwan 28.10 at 01:00.',
                   'Триває з 27.10 по 03.11 для власників Heroic, Epic і Collection. До трьох персонажів на акаунт у всіх режимах разом, хто перший прийшов, той і зайняв. Це не ранній доступ до гри. Старт за Києвом: Європа 27.10 о 19:00, Америка 27.10 о 22:00, Корея 28.10 о 00:00, Тайвань 28.10 о 01:00.')],
                [t('05.11', '04.11 / 05.11', '05.11'), t('Релиз WoW Forever', 'WoW Forever release', 'Реліз WoW Forever'),
                 t('Нужна подписка или игровое время. Forever — постоянная игра рядом с Retail и Classic, а не сезон. Старт в 15:00 по тихоокеанскому, это 23:00 UTC.',
                   'Requires a subscription or game time. Forever is a permanent game next to Retail and Classic, not a season. Launch is at 15:00 Pacific, which is 23:00 UTC.',
                   'Потрібна підписка або ігровий час. Forever — постійна гра поруч із Retail і Classic, а не сезон. Старт о 15:00 за тихоокеанським, це 23:00 UTC.')],
                ['09.12', t('Открываются рейды', 'Raids open', 'Відкриваються рейди'),
                 t('Barrow Deeps (10 игроков), Hyjal Summit (20), Onyxia’s Lair (40). До этого есть пять недель на прокачку и подземелья.',
                   'Barrow Deeps (10 players), Hyjal Summit (20), Onyxia’s Lair (40). Until then you have five weeks for leveling and dungeons.',
                   'Barrow Deeps (10 гравців), Hyjal Summit (20), Onyxia’s Lair (40). До цього є п’ять тижнів на прокачування та підземелля.')],
            ]}),
            ('text', [t('Старт 04.11 в 23:00 UTC, в Европе уже 05.11. По часовым поясам:', 'Launch is on 04.11 at 23:00 UTC, which is already 05.11 in Europe. By time zone:', 'Старт 04.11 о 23:00 UTC, в Європі вже 05.11. За часовими поясами:')]),
            ('table', {'head': [t('Где', 'Where', 'Де'), t('Старт', 'Launch', 'Старт')], 'rows': [
                [t('Лос-Анджелес', 'Los Angeles', 'Лос-Анджелес'), '04.11, 15:00'],
                [t('Нью-Йорк', 'New York', 'Нью-Йорк'), '04.11, 18:00'],
                [t('Сан-Паулу', 'São Paulo', 'Сан-Паулу'), '04.11, 20:00'],
                [t('UTC, Лондон, Лиссабон', 'UTC, London, Lisbon', 'UTC, Лондон, Лісабон'), '04.11, 23:00'],
                [t('Берлин, Париж, Мадрид, Рим, Варшава', 'Berlin, Paris, Madrid, Rome, Warsaw', 'Берлін, Париж, Мадрид, Рим, Варшава'), '05.11, 00:00'],
                [t('Киев', 'Kyiv', 'Київ'), '05.11, 01:00'],
                [t('Алматы', 'Almaty', 'Алмати'), '05.11, 04:00'],
                [t('Сидней', 'Sydney', 'Сідней'), '05.11, 10:00'],
            ]}),
        ]},
        {'id': 'editions', 'title': t('Цены и подписка', 'Prices and subscription', 'Ціни та підписка'), 'blocks': [
            ('text', [t('Forever входит в обычную подписку WoW или игровое время: одна подписка открывает WoW, Classic и Forever. Отдельно игру покупать не нужно.',
                        'Forever is included in the regular WoW subscription or game time: one subscription opens WoW, Classic and Forever. You do not buy the game separately.',
                        'Forever входить у звичайну підписку WoW або ігровий час: одна підписка відкриває WoW, Classic і Forever. Окремо гру купувати не потрібно.')]),
            ('table', {'head': [t('Подписка', 'Subscription', 'Підписка'), t('США, в месяц', 'US, per month', 'США, на місяць'), t('Европа, в месяц', 'Europe, per month', 'Європа, на місяць')], 'rows': [
                [t('1 месяц', '1 month', '1 місяць'), '$14.99', '€12.99'],
                [t('3 месяца', '3 months', '3 місяці'), '$13.99', '€11.99'],
                [t('6 или 12 месяцев', '6 or 12 months', '6 або 12 місяців'), '$12.99', '€10.99'],
            ]}),
            ('text', [t('Цены магазина Battle.net на 24.10, с НДС. В других валютах и регионах цена своя.',
                        'Battle.net shop prices as of 24.10, VAT included. Other currencies and regions have their own price.',
                        'Ціни магазину Battle.net на 24.10, з ПДВ. В інших валютах і регіонах ціна своя.')]),
            ('table', {'head': [t('Набор', 'Pack', 'Набір'), t('Цена', 'Price', 'Ціна'), t('Что даёт', 'What you get', 'Що дає')], 'rows': [
                ['Heroic Pack', '$29.99', t('Расу Скайборн, её стартовую зону и раннюю резервацию имён.',
                                            'The Skyborne race, its starting zone and early name reservation.',
                                            'Расу Скайборн, її стартову зону та ранню резервацію імен.')],
                ['Epic Pack', '$59.99', t('То же плюс 30 дней игрового времени: их начислят в день старта.',
                                          'The same plus 30 days of game time, added on launch day.',
                                          'Те саме плюс 30 днів ігрового часу: їх нарахують у день старту.')],
                ['Warcraft Forever Collection', '$79.99', t('Epic Pack плюс Warcraft III: Reforged с кампанией Forsaken Kingdom. Продаётся до 11.01.2027.',
                                                            'The Epic Pack plus Warcraft III: Reforged with the Forsaken Kingdom campaign. On sale until 11.01.2027.',
                                                            'Epic Pack плюс Warcraft III: Reforged з кампанією Forsaken Kingdom. Продається до 11.01.2027.')],
            ]}),
            ('text', [t('Остальные восемь рас и все девять классов докупать не нужно.',
                        'The other eight races and all nine classes do not need to be bought.',
                        'Решту восьми рас і всі дев’ять класів докуповувати не потрібно.')]),
            ('steps', [
                {'t': t('Неделя для друга', 'A week for a friend', 'Тиждень для друга'),
                 'd': t('К набору прилагается код Invite-A-Friend: по нему друг играет с 04.11 по 11.11 без подписки. Heroic даёт 1 код, Epic и Collection — 3. Коды приходят на почту с 20.10, к подарочным покупкам их нет.',
                        'A pack comes with Invite-A-Friend codes: with one, a friend plays from 04.11 to 11.11 without a subscription. Heroic gives 1 code, Epic and Collection give 3. Codes arrive by email from 20.10, gift purchases get none.',
                        'До набору додається код Invite-A-Friend: з ним друг грає з 04.11 по 11.11 без підписки. Heroic дає 1 код, Epic і Collection — 3. Коди приходять на пошту з 20.10, до подарункових покупок їх немає.')},
            ]),
        ]},
        {'id': 'language', 'langs': ('ru', 'uk', 'pl'),   # ru, uk и pl: язык клиента и аддоны перевода (pl: клиента нет, по магазину Battle.net)
         'title': {'ru': 'Играть на русском', 'uk': 'Грати українською', 'pl': 'Czy WoW Forever jest po polsku?'}, 'blocks': [
            ('raw', {
                'ru': '<p>У WoW Forever есть русский клиент. В лаунчере Battle.net откройте настройки игры и выберите язык «Русский». Русификатор не нужен.</p>'
                      '<p>Русская озвучка заданий, истории зон и книг — аддон Wayfarer — Russian VoiceOver. Работает только с русским клиентом. Запасной вариант — Russian Quests Voiceover.</p>'
                      '<p class="gbtns"><a class="btn ghost" href="https://www.curseforge.com/wow/addons/wayfarer-russian-voiceover" target="_blank" rel="noopener">Wayfarer на CurseForge ↗</a>'
                      '<a class="btn ghost" href="https://www.curseforge.com/wow/addons/wowvoice-classic" target="_blank" rel="noopener">Russian Quests Voiceover ↗</a></p>',
                'uk': '<p>Українського клієнта у WoW Forever немає. Українською грають з аддоном UA_Forever: він перекладає завдання, підказки й вікна поверх клієнта.</p>'
                      '<p class="gbtns"><a class="btn ghost" href="https://www.curseforge.com/wow/addons/ua-forever" target="_blank" rel="noopener">Відкрити на CurseForge ↗</a>'
                      '<a class="btn ghost" href="../ukrainian/">Як грати українською</a></p>',
                'pl': '<p>Nie. Sklep Battle.net podaje dla WoW Forever 10 wersji językowych: angielską, hiszpańską, portugalską (Brazylia), niemiecką, francuską, rosyjską, koreańską i chińską tradycyjną. Polskiej wśród nich nie ma.</p>'
                      '<p>W Polsce gra się na kliencie angielskim. Dlatego nazwy zadań, lochów i umiejętności podajemy tu po angielsku, tak jak w grze.</p>'
                      '<p class="gbtns"><a class="btn ghost" href="https://eu.shop.battle.net/en-gb/product/world-of-warcraft-forever" target="_blank" rel="noopener">Battle.net: języki gry ↗</a></p>',
            }),
        ]},
        {'id': 'modes', 'title': t('Режимы и серверы', 'Modes and servers', 'Режими та сервери'), 'blocks': [
            ('steps', [
                {'t': t('Обычный, PvP, RP и RP-PvP', 'Normal, PvP, RP and RP-PvP', 'Звичайний, PvP, RP і RP-PvP'),
                 'd': t('RP-PvP Blizzard добавила к старту 22.10, выбрать его можно уже при резерве имён. Hardcore запустят позже со своими правилами.',
                        'Blizzard added RP-PvP for launch on 22.10, and you can pick it as early as name reservation. Hardcore will launch later with its own rules.',
                        'RP-PvP Blizzard додала до старту 22.10, обрати його можна вже під час резерву імен. Hardcore запустять пізніше зі своїми правилами.')},
                {'t': t('Один сервер на режим', 'One server per mode', 'Один сервер на режим'),
                 'd': t('Реалмов нет: в каждом регионе по одному большому серверу на режим, нагрузку делят слои. Регионы: Америка и Океания, Европа, Корея, Тайвань.',
                        'There are no realms: each region has one large server per mode, and layers share the load. Regions: Americas and Oceania, Europe, Korea, Taiwan.',
                        'Реалмів немає: у кожному регіоні по одному великому серверу на режим, навантаження ділять шари. Регіони: Америка й Океанія, Європа, Корея, Тайвань.')},
                {'t': t('Режим выбирают один раз', 'The mode is chosen once', 'Режим обирають один раз'),
                 'd': t('Перенести персонажа в другой режим нельзя. Исключение — погибший персонаж Hardcore: он продолжает в другом режиме.',
                        'You cannot move a character to another mode. The exception is a Hardcore character who has died: it carries on in another mode.',
                        'Перенести персонажа в інший режим не можна. Виняток — загиблий персонаж Hardcore: він продовжує в іншому режимі.')},
                {'t': t('Группа только в одном режиме', 'Groups stay within one mode', 'Група лише в одному режимі'),
                 'd': t('Группироваться можно только внутри одного режима. В PvP при создании доступна одна фракция.',
                        'You can only group within one mode. In PvP only one faction is available at character creation.',
                        'Групуватися можна лише в межах одного режиму. У PvP під час створення доступна одна фракція.')},
            ]),
            ('tip', t('Договоритесь заранее: одна фракция, один режим, одни и те же дни на старт.',
                      'Agree in advance: one faction, one mode, the same days for launch.',
                      'Домовтеся заздалегідь: одна фракція, один режим, одні й ті самі дні на старт.')),
        ]},
        {'id': 'names', 'title': t('Имена и фамилии', 'Names and surnames', 'Імена та прізвища'), 'blocks': [
            ('steps', [
                {'t': t('Имя и фамилия', 'First name and surname', 'Ім’я та прізвище'),
                 'd': t('У каждого персонажа есть имя и фамилия.', 'Every character has a first name and a surname.',
                        'Кожен персонаж має ім’я та прізвище.')},
                {'t': t('Реалмов нет', 'No realms', 'Реалмів немає'),
                 'd': t('Полное имя должно быть уникальным во всём регионе. Одно имя у двоих возможно, если фамилии разные.',
                        'The full name must be unique across the whole region. Two players can share a first name if their surnames differ.',
                        'Повне ім’я має бути унікальним у всьому регіоні. Одне ім’я у двох можливе, якщо прізвища різні.')},
                {'t': t('Фамилию можно скрыть', 'The surname can be hidden', 'Прізвище можна приховати'),
                 'd': 'Esc → Options → Nameplates → My Secondary Name.'},
                {'t': t('Одна фракция в PvP', 'One faction in PvP', 'Одна фракція в PvP'),
                 'd': t('В PvP-режиме на аккаунте может быть только одна фракция.', 'In PvP mode an account can have only one faction.',
                        'У PvP-режимі на акаунті може бути лише одна фракція.')},
            ]),
            ('tip', t('Резерв имён открыт до 03.11. Подготовьте имя, фамилию и два-три запасных варианта: короткие имена разбирают первыми.',
                      'Name reservation is open until 03.11. Prepare a name, a surname and two or three backups: short names go first.',
                      'Резерв імен відкрито до 03.11. Підготуйте ім’я, прізвище й два-три запасні варіанти: короткі імена розбирають першими.')),
        ]},
        {'id': 'era', 'title': t('Чем Forever отличается от Classic Era', 'How Forever differs from Classic Era', 'Чим Forever відрізняється від Classic Era'), 'blocks': [
            ('table', {'head': [t('Тема', 'Topic', 'Тема'), t('Что в Forever', 'What Forever has', 'Що у Forever')], 'rows': [
                [t('Общее', 'General', 'Загальне'),
                 t('Eastern Kingdoms и Kalimdor, прокачка до 60. Постоянная игра, а не сезон. Нет летающих скакунов и нет масштабирования уровней, как и в Classic.',
                   'Eastern Kingdoms and Kalimdor, leveling to 60. A permanent game, not a season. No flying mounts and no level scaling, as in Classic.',
                   'Eastern Kingdoms та Kalimdor, прокачування до 60. Постійна гра, а не сезон. Немає літаючих скакунів і масштабування рівнів, як і в Classic.')],
                [t('Контент', 'Content', 'Контент'),
                 t('Новые зоны, задания, 9 новых подземелий, 2 новых рейда и Onyxia’s Lair, новое поле боя, новая раса Скайборн.',
                   'New zones, quests, 9 new dungeons, 2 new raids plus Onyxia’s Lair, a new battleground, the new Skyborne race.',
                   'Нові зони, завдання, 9 нових підземель, 2 нові рейди та Onyxia’s Lair, нове поле бою, нова раса Скайборн.')],
                [t('Классы и расы', 'Classes and races', 'Класи та раси'),
                 t('Обновлены таланты и способности классов, новые сочетания рас и классов, у рас убраны сопротивления и добавлены свои способности.',
                   'Class talents and abilities were updated, there are new race and class combinations, and races lost resistances and gained their own abilities.',
                   'Оновлено таланти та здібності класів, нові поєднання рас і класів, у рас прибрано опори й додано свої здібності.')],
                [t('Системы', 'Systems', 'Системи'),
                 t('Legacy, лагерь, опциональная трансмогрификация и выбор визуального стиля (Classic или современный), официальная поддержка геймпада.',
                   'Legacy, camp, optional transmog and a choice of visual style (Classic or modern), official gamepad support.',
                   'Legacy, табір, опціональна трансмогрифікація та вибір візуального стилю (Classic або сучасний), офіційна підтримка геймпада.')],
                [t('Предметы', 'Items', 'Предмети'),
                 t('Характеристики и предметы изменены, поэтому старые списки добычи из Classic ненадёжны.',
                   'Stats and items were changed, so old Classic loot lists are unreliable.',
                   'Характеристики та предмети змінено, тому старі списки здобичі з Classic ненадійні.')],
            ]}),
        ]},
        {'id': 'graphics', 'title': t('Classic или Enhanced', 'Classic or Enhanced', 'Classic чи Enhanced'), 'blocks': [
            ('text', [t('При первом входе игра предлагает набор настроек: Classic или Enhanced. Это только старт: экран выбора больше не появится, но каждую настройку можно поменять отдельно.',
                        'On first login the game offers a set of settings: Classic or Enhanced. It is only a starting point: the choice screen will not come back, but every setting can be changed on its own.',
                        'Під час першого входу гра пропонує набір налаштувань: Classic або Enhanced. Це лише старт: екран вибору більше не з’явиться, але кожне налаштування можна змінити окремо.')]),
            ('table', {'head': [t('Настройка', 'Setting', 'Налаштування'), 'Classic', 'Enhanced', t('Где поменять', 'Where to change', 'Де змінити')], 'rows': [
                [t('Модели персонажей', 'Character models', 'Моделі персонажів'), t('Обычные (SD)', 'Standard (SD)', 'Звичайні (SD)'), t('Высокой чёткости (HD)', 'High definition (HD)', 'Високої чіткості (HD)'),
                 t('Настройки графики', 'Graphics settings', 'Налаштування графіки')],
                [t('Цели заданий на карте', 'Quest objectives on the map', 'Цілі завдань на мапі'), t('Нет', 'Off', 'Ні'), t('Есть', 'On', 'Є'),
                 t('Фильтр карты мира', 'World map filter', 'Фільтр мапи світу')],
                [t('Одна общая сумка', 'One combined bag', 'Одна спільна сумка'), t('Нет', 'Off', 'Ні'), t('Есть', 'On', 'Є'),
                 t('Настройки управления', 'Controls settings', 'Налаштування керування')],
                [t('Трансмогрификация', 'Transmog', 'Трансмогрифікація'), t('Выключена', 'Off', 'Вимкнена'), t('Включена', 'On', 'Увімкнена'),
                 t('У трансмогрификатора в городе', 'At a transmogrifier in a city', 'У трансмогрифікатора в місті')],
                [t('Клавиши A и D', 'A and D keys', 'Клавіші A і D'), t('Поворот', 'Turn', 'Поворот'), t('Шаг в сторону', 'Strafe', 'Крок убік'),
                 t('Назначение клавиш', 'Key bindings', 'Призначення клавіш')],
                [t('Расположение интерфейса', 'Interface layout', 'Розташування інтерфейсу'), t('Классическое', 'Classic', 'Класичне'), t('По центру', 'Centred', 'По центру'),
                 t('Режим редактирования', 'Edit Mode', 'Режим редагування')],
            ]}),
            ('tip', t('Режим редактирования возвращает рамкам старые места, но не старый рисунок: классический вид интерфейса дают только аддоны.',
                      'Edit Mode puts the frames back in their old places, but not their old look: the classic interface art comes only with addons.',
                      'Режим редагування повертає рамкам старі місця, але не старий вигляд: класичний вигляд інтерфейсу дають лише аддони.')),
            ('tiles', [{'t': t('Аддоны и интерфейс', 'Addons and Interface', 'Аддони та інтерфейс'), 'd': t('Что работает, что встроено, как ставить', 'What works, what is built in, how to install', 'Що працює, що вбудовано, як ставити'), 'href': 'guides/addons/', 'art': 'hero_roster'}]),
        ]},
        {'id': 'questions', 'title': t('Частые вопросы', 'Common questions', 'Часті питання'), 'blocks': [
            ('raw', t('<label class="gsearch"><span class="sr">Поиск по вопросам</span><input type="search" id="faqQ" autocomplete="off" placeholder="Поиск по вопросам"></label><p class="note" id="faqNone" hidden>Ничего не нашлось. Попробуйте другое слово или поиск по сайту (Ctrl+K).</p>',
                      '<label class="gsearch"><span class="sr">Search questions</span><input type="search" id="faqQ" autocomplete="off" placeholder="Search questions"></label><p class="note" id="faqNone" hidden>Nothing found. Try another word or the site search (Ctrl+K).</p>',
                      '<label class="gsearch"><span class="sr">Пошук по питаннях</span><input type="search" id="faqQ" autocomplete="off" placeholder="Пошук по питаннях"></label><p class="note" id="faqNone" hidden>Нічого не знайшлося. Спробуйте інше слово або пошук по сайту (Ctrl+K).</p>')),
            ('faq', [
                {'id': 'release', 'q': t('Когда выходит WoW Forever?', 'When does WoW Forever launch?', 'Коли виходить WoW Forever?'),
                 'a': [t('В Европе 05.11.2026, в Америке 04.11.2026. Старт в 15:00 по тихоокеанскому, это 23:00 UTC.',
                         '04.11.2026 in the Americas, 05.11.2026 in Europe. Launch is at 15:00 Pacific, which is 23:00 UTC.',
                         'У Європі 05.11.2026, в Америці 04.11.2026. Старт о 15:00 за тихоокеанським, це 23:00 UTC.')]},
                {'id': 'subscription', 'q': t('Нужна ли подписка?', 'Do I need a subscription?', 'Чи потрібна підписка?'),
                 'a': [t('Да, подписка или игровое время, та же, что для WoW и Classic: от $14.99 или €12.99 в месяц, дешевле при оплате на 3–12 месяцев. Forever — постоянная игра рядом с Retail и Classic, а не сезон.',
                         'Yes, a subscription or game time, the same one as for WoW and Classic: from $14.99 or €12.99 a month, cheaper when paid for 3–12 months. Forever is a permanent game next to Retail and Classic, not a season.',
                         'Так, підписка або ігровий час, та сама, що для WoW і Classic: від $14.99 або €12.99 на місяць, дешевше при оплаті на 3–12 місяців. Forever — постійна гра поруч із Retail і Classic, а не сезон.')]},
                {'id': 'trial', 'q': t('Можно ли попробовать бесплатно?', 'Can I try it for free?', 'Чи безкоштовна WoW Forever?'),
                 'a': [t('Только по коду друга. Владелец набора получает коды Invite-A-Friend, по такому коду играют с 04.11 по 11.11 без подписки. Heroic даёт 1 код, Epic и Collection — 3.',
                         'Only with a friend’s code. Pack owners get Invite-A-Friend codes, and with one you play from 04.11 to 11.11 without a subscription. Heroic gives 1 code, Epic and Collection give 3.',
                         'Ні, потрібна підписка або ігровий час. Безкоштовно грають лише за кодом друга Invite-A-Friend: з ним — з 04.11 по 11.11 без підписки. Власник Heroic отримує 1 код, Epic і Collection — 3.')]},
                {'id': 'price', 'q': t('Сколько стоят наборы и нужны ли они?', 'How much are the packs, and do I need one?', 'Скільки коштують набори і чи потрібні вони?'),
                 'a': [t('Heroic Pack $29.99, Epic Pack $59.99, Warcraft Forever Collection $79.99. Набор нужен только ради расы Скайборн и ранней резервации имён: остальные восемь рас и все девять классов докупать не нужно.',
                         'Heroic Pack $29.99, Epic Pack $59.99, Warcraft Forever Collection $79.99. A pack is only needed for the Skyborne race and early name reservation: the other eight races and all nine classes do not need to be bought.',
                         'Heroic Pack $29.99, Epic Pack $59.99, Warcraft Forever Collection $79.99. Набір потрібен лише заради раси Скайборн і ранньої резервації імен: решту восьми рас і всі дев’ять класів докуповувати не потрібно.')]},
                {'id': 'reserve', 'q': t('Когда занимать имя?', 'When can I reserve a name?', 'Коли бронювати ім’я?'),
                 'a': [t('С 27.10 по 03.11, если у вас Heroic, Epic или Collection. До трёх персонажей на аккаунт, кто первым пришёл, тот и занял. Это не ранний доступ в игру.',
                         'From 27.10 to 03.11 if you own Heroic, Epic or Collection. Up to three characters per account, first come, first served. This is not early access to the game.',
                         'З 27.10 по 03.11, якщо у вас Heroic, Epic або Collection. До трьох персонажів на акаунт, хто перший прийшов, той і зайняв. Це не ранній доступ до гри.')],
                 'link': (t('Как занять имя', 'How to claim a name', 'Як зайняти ім’я'), '../name-reservation/')},
                {'id': 'surname', 'q': t('Зачем фамилия и можно ли взять то же имя, что у друга?', 'Why a surname, and can two people share a name?', 'Навіщо прізвище і чи можна взяти те саме ім’я, що в друга?'),
                 'a': [t('Реалмов нет, поэтому уникальным должно быть полное имя во всём регионе. Одно имя у двоих возможно, если фамилии разные. Фамилию можно скрыть: Esc → Options → Nameplates → My Secondary Name.',
                         'There are no realms, so the full name must be unique across the whole region. Two players can share a first name if their surnames differ. You can hide the surname: Esc → Options → Nameplates → My Secondary Name.',
                         'Реалмів немає, тому унікальним має бути повне ім’я у всьому регіоні. Одне ім’я у двох можливе, якщо прізвища різні. Прізвище можна приховати: Esc → Options → Nameplates → My Secondary Name.')]},
                {'id': 'skyborne', 'q': t('Что такое Скайборн?', 'What is Skyborne?', 'Що таке Скайборн?'),
                 'a': [t('Новая раса Forever, открывается любым из трёх наборов. Доступна обеим фракциям, фракция выбирается при создании. Обе ветки знают дарнасский, а стартовая зона Zephras Isle общая.',
                         'The new Forever race, unlocked by any of the three packs. Playable for both factions, the faction is chosen at character creation. Both branches know Darnassian and share the Zephras Isle starting zone.',
                         'Нова раса Forever, відкривається будь-яким із трьох наборів. Доступна за обидві фракції, фракцію обирають під час створення. Обидві гілки знають дарнаську, а стартова зона Zephras Isle спільна.')]},
                {'id': 'levels', 'q': t('До какого уровня качаться и где?', 'What is the level cap, and where do we level?', 'До якого рівня качатися і де?'),
                 'a': [t('До 60, в [[Восточных королевствах|Eastern Kingdoms]] и [[Калимдоре|Kalimdor]]. Летающих скакунов и масштабирования уровней нет, как и в Classic.',
                         'Up to 60, in the Eastern Kingdoms and Kalimdor. No flying mounts and no level scaling, as in Classic.',
                         'До 60, у Eastern Kingdoms і Kalimdor. Літаючих скакунів і масштабування рівнів немає, як і в Classic.')]},
                {'id': 'together', 'q': t('Можно ли играть вместе, если выбрали разные режимы?', 'Can we play together in different modes?', 'Чи можна грати разом, якщо обрали різні режими?'),
                 'a': [t('Нет: группироваться можно только внутри одного режима. Режимы на старте: обычный, PvP, RP и RP-PvP, Hardcore запустят позже. В PvP на аккаунте может быть только одна фракция.',
                         'No: you can only group within one mode. Modes at launch: Normal, PvP, RP and RP-PvP, Hardcore comes later. In PvP an account can have only one faction.',
                         'Ні: групуватися можна лише в межах одного режиму. Режими на старті: звичайний, PvP, RP і RP-PvP, Hardcore запустять пізніше. У PvP на акаунті може бути лише одна фракція.')]},
                {'id': 'group-choice', 'q': t('Какой регион, режим и фракцию выбрать, чтобы играть с друзьями?', 'Which region, mode and faction should we pick to play with friends?', 'Який регіон, режим і фракцію обрати, щоб грати з друзями?'),
                 'a': [t('Одни и те же на всех. Регионы разделены, межрегиональной игры нет, поэтому берите регион с лучшим пингом для большинства. Группа собирается только внутри одного режима, а Альянс и Орда не встают в одну группу ни в каком режиме. В PvP на аккаунте одна фракция, так что договоритесь о ней до резерва имён 27.10.',
                         'The same for everyone. Regions are separate and there is no cross-region play, so pick the region with the best ping for most of you. Groups form only within one mode, and Alliance and Horde cannot group in any mode. In PvP an account has only one faction, so agree on it before name reservation opens on 27.10.',
                         'Однакові для всіх. Регіони розділені, міжрегіональної гри немає, тож беріть регіон із найкращим пінгом для більшості. Група збирається лише в межах одного режиму, а Альянс і Орда не стають в одну групу в жодному режимі. У PvP на акаунті одна фракція, тож домовтеся про неї до бронювання імен 27.10.')]},
                {'id': 'servers', 'q': t('Какие серверы и есть ли русские?', 'Which servers are there, and are there language servers?', 'Які сервери і чи є окремі мовні?'),
                 'a': [t('Реалмов нет: в каждом регионе по одному серверу на режим (обычный, PvP, RP, RP-PvP), игроков разводят слои. Регионы: Америка и Океания, Европа, Корея, Тайвань. Отдельных русских серверов нет, русский язык выбирают в настройках клиента.',
                         'There are no realms: each region has one server per mode (Normal, PvP, RP, RP-PvP), and layers split the players. Regions: Americas and Oceania, Europe, Korea, Taiwan. There are no separate language servers: the language is set in the client.',
                         'Реалмів немає: у кожному регіоні по одному серверу на режим (звичайний, PvP, RP, RP-PvP), гравців розводять шари. Регіони: Америка й Океанія, Європа, Корея, Тайвань. Окремих мовних серверів немає, мову обирають у налаштуваннях клієнта.')]},
                {'id': 'where', 'q': t('Где найти группу?', 'Where do I find a group?', 'Де знайти групу?'),
                 'a': [t('На сайте и в Discord. Соберите группу в конструкторе и поделитесь ссылкой. На Discord-сервере Gabella собирают группы на старт 05.11 и договариваются о регионе, режиме и фракции.',
                         'On this site and on Discord. Build a party in the group builder and share the link. On the Gabella Discord server groups form for the Nov 4–5 launch, and players agree on region, mode and faction.',
                         'На сайті та в Discord. Зберіть групу в конструкторі й поділіться посиланням. На Discord-сервері Gabella збирають групи на старт 05.11 і домовляються про регіон, режим і фракцію.')],
                 'link': (t('Discord Gabella', 'Gabella Discord', 'Discord Gabella'), DISCORD_AT['faq'])},
                {'id': 'profile', 'q': t('Что такое ранг и рамки в профиле?', 'What are rank and frames in the profile?', 'Що таке ранг і рамки в профілі?'),
                 'a': [t('Это ваш профиль на сайте, к самой игре он не относится.',
                         'This is your profile on the site; it has nothing to do with the game itself.',
                         'Це ваш профіль на сайті, до самої гри він не стосується.'),
                       t('Ранг растёт от очков достижений и открывает рамки портрета. Особые рамки дают особые достижения.',
                         'Rank grows from achievement points and unlocks portrait frames. Special frames come from special achievements.',
                         'Ранг росте від очок досягнень і відкриває рамки портрета. Особливі рамки дають особливі досягнення.')]},
                {'id': 'raids', 'q': t('Когда откроются рейды?', 'When do raids open?', 'Коли відкриються рейди?'),
                 'a': [t('09.12: Barrow Deeps (10 игроков), Hyjal Summit (20), Onyxia’s Lair (40). До этого есть пять недель на прокачку и подземелья.',
                         '09.12: Barrow Deeps (10 players), Hyjal Summit (20), Onyxia’s Lair (40). Until then you have five weeks for leveling and dungeons.',
                         '09.12: Barrow Deeps (10 гравців), Hyjal Summit (20), Onyxia’s Lair (40). До цього є п’ять тижнів на прокачування та підземелля.')]},
                {'id': 'beta', 'q': t('Можно ли ещё попасть в бету?', 'Can I still get into the beta?', 'Чи можна ще потрапити в бету?'),
                 'a': [t('Нет. Доступ был у владельцев Epic и Collection. Бета завершилась 23.10 в 10:00 по тихоокеанскому времени.',
                         'No. Access was for Epic and Collection owners. The beta ended on 23.10 at 10:00 Pacific time.',
                         'Ні. Доступ мали власники Epic і Collection. Бета завершилася 23.10 о 10:00 за тихоокеанським часом.')]},
                {'id': 'classic-guides', 'q': t('Подойдут ли старые гайды по Classic?', 'Are old Classic guides still useful?', 'Чи підійдуть старі гайди по Classic?'),
                 'a': [t('Только частично. Характеристики и предметы изменены, поэтому старые списки добычи ненадёжны. Добавлены 9 новых подземелий, 2 новых рейда и Onyxia’s Lair, новые зоны и задания, у классов обновлены таланты.',
                         'Only partly. Stats and items were changed, so old loot lists are unreliable. There are 9 new dungeons, 2 new raids plus Onyxia’s Lair, new zones and quests, and class talents were updated.',
                         'Лише частково. Характеристики та предмети змінено, тому старі списки здобичі ненадійні. Додано 9 нових підземель, 2 нові рейди та Onyxia’s Lair, нові зони та завдання, у класів оновлено таланти.')]},
                {'id': 'visuals', 'q': t('Будет ли современная графика и геймпад?', 'Is there modern graphics and gamepad support?', 'Чи буде сучасна графіка та геймпад?'),
                 'a': [t('Да: при первом входе выбирают набор Classic или Enhanced (модели HD, цели заданий на карте, одна сумка, трансмогрификация), потом каждую настройку можно поменять. Есть официальная поддержка геймпада.',
                         'Yes: on first login you pick the Classic or Enhanced set (HD models, quest objectives on the map, one bag, transmog), and each setting can be changed later. There is official gamepad support.',
                         'Так: під час першого входу обирають набір Classic або Enhanced (моделі HD, цілі завдань на мапі, одна сумка, трансмогрифікація), потім кожне налаштування можна змінити. Є офіційна підтримка геймпада.')]},
                {'id': 'requirements', 'q': t('Какие системные требования?', 'What are the system requirements?', 'Які системні вимоги?'),
                 'a': [t('Минимум: Windows 10 64-bit, 4 ядра 3,0 ГГц, 8 ГБ ОЗУ, видеокарта DirectX 12 на 4 ГБ (GeForce GTX 10, RDNA 1) и 128 ГБ на SSD. На Mac — macOS 12 и Apple M2. Полная таблица — на странице требований.',
                         'Minimum: Windows 10 64-bit, 4 cores at 3.0 GHz, 8 GB RAM, a DirectX 12 GPU with 4 GB (GeForce GTX 10, RDNA 1) and 128 GB on an SSD. On Mac: macOS 12 and Apple M2. The full table is on the requirements page.',
                         'Мінімум: Windows 10 64-bit, 4 ядра 3,0 ГГц, 8 ГБ ОЗП, відеокарта DirectX 12 на 4 ГБ (GeForce GTX 10, RDNA 1) і 128 ГБ на SSD. На Mac — macOS 12 і Apple M2. Повна таблиця — на сторінці вимог.')],
                 'link': (t('Системные требования', 'System requirements', 'Системні вимоги'), '../requirements/')},
            ]),
        ]},
    ],
})

# ---------- Системные требования: по магазину Battle.net, видеокарты — по новости Blizzard ----------

SHOP = 'https://eu.shop.battle.net/en-gb/product/world-of-warcraft-forever'
SSD = t('SSD, 128 ГБ свободно', 'SSD, 128 GB free', 'SSD, 128 ГБ вільно')
RAM8, RAM16 = t('8 ГБ', '8 GB', '8 ГБ'), t('16 ГБ', '16 GB', '16 ГБ')
REQ_HEAD = ['', t('Минимум', 'Minimum', 'Мінімум'), t('Рекомендуется', 'Recommended', 'Рекомендовано')]

GUIDES.append({
    'slug': 'requirements', 'art': 'hero_requirements', 'hero': 'hero_requirements',
    'title': t('Системные требования', 'System requirements', 'Системні вимоги'),
    'lead': t('Минимальные и рекомендуемые требования WoW Forever для Windows и Mac по Battle.net Shop и какие видеокарты больше не поддерживаются.',
              'Minimum and recommended WoW Forever requirements for Windows and Mac from the Battle.net Shop, and which graphics cards are no longer supported.',
              'Мінімальні й рекомендовані вимоги WoW Forever для Windows і Mac за Battle.net Shop і які відеокарти більше не підтримуються.'),
    'tile': t('ПК и Mac: минимум, рекомендуемые, видеокарты', 'PC and Mac: minimum, recommended, graphics cards', 'ПК і Mac: мінімум, рекомендовані, відеокарти'),
    'pills': [t('SSD 128 ГБ', 'SSD 128 GB', 'SSD 128 ГБ'), t('Минимум 8 ГБ ОЗУ', '8 GB RAM minimum', 'Мінімум 8 ГБ ОЗП'),
              t('Windows и Mac', 'Windows and Mac', 'Windows і Mac')],
    'sources': [
        (t('Battle.net Shop: системные требования WoW Forever', 'Battle.net Shop: WoW Forever system requirements', 'Battle.net Shop: системні вимоги WoW Forever'), SHOP),
        (t('Blizzard: требования к видеокартам', 'Blizzard: graphics card requirements', 'Blizzard: вимоги до відеокарт'),
         'https://news.blizzard.com/en-us/article/24301512'),
        (t('Warcraft Tavern: установка Forever', 'Warcraft Tavern: installing Forever', 'Warcraft Tavern: встановлення Forever'),
         'https://www.warcrafttavern.com/forever/guides/beta/'),
        (t('esports.gg: системные требования', 'esports.gg: system requirements', 'esports.gg: системні вимоги'),
         'https://esports.gg/guides/world-of-warcraft/can-your-pc-or-mac-run-wow-forever-here-are-the-system-requirements/'),
        (t('System Requirements Lab: WoW Forever', 'System Requirements Lab: WoW Forever', 'System Requirements Lab: WoW Forever'),
         'https://www.systemrequirementslab.com/requirements/wow-forever/30743'),
    ],
    'sections': [
        {'id': 'windows', 'title': 'Windows', 'blocks': [
            ('table', {'head': REQ_HEAD, 'rows': [
                [t('Система', 'System', 'Система'),
                 t('Windows 10 64-bit (обновление May 2019 или новее)', 'Windows 10 64-bit (May 2019 Update or newer)', 'Windows 10 64-bit (оновлення May 2019 або новіше)'), 'Windows 11'],
                [t('Процессор', 'Processor', 'Процесор'),
                 t('4 ядра, 3,0 ГГц: Intel Core Haswell, AMD Ryzen Zen', '4 cores, 3.0 GHz: Intel Core Haswell, AMD Ryzen Zen', '4 ядра, 3,0 ГГц: Intel Core Haswell, AMD Ryzen Zen'),
                 t('8 производительных ядер до 5,2 ГГц: Intel Core Ultra (Series 2), AMD Ryzen Zen 5',
                   '8 performance cores, 5.2 GHz boost: Intel Core Ultra (Series 2), AMD Ryzen Zen 5',
                   '8 продуктивних ядер до 5,2 ГГц: Intel Core Ultra (Series 2), AMD Ryzen Zen 5')],
                [t('Видеокарта', 'Graphics', 'Відеокарта'),
                 t('DirectX 12, 4 ГБ: GeForce GTX 10, AMD RDNA 1, Intel Iris Xe2-LPG (Lunar Lake)', 'DirectX 12, 4 GB: GeForce GTX 10, AMD RDNA 1, Intel Iris Xe2-LPG (Lunar Lake)',
                   'DirectX 12, 4 ГБ: GeForce GTX 10, AMD RDNA 1, Intel Iris Xe2-LPG (Lunar Lake)'),
                 t('DirectX 12, 8 ГБ: GeForce RTX 40, AMD RDNA 3, Intel Arc B', 'DirectX 12, 8 GB: GeForce RTX 40, AMD RDNA 3, Intel Arc B',
                   'DirectX 12, 8 ГБ: GeForce RTX 40, AMD RDNA 3, Intel Arc B')],
                [t('Память', 'Memory', 'Пам’ять'), RAM8, RAM16],
                [t('Диск', 'Storage', 'Диск'), SSD, SSD],
                [t('Разрешение', 'Resolution', 'Роздільна здатність'), t('Не менее 1280 × 720', 'At least 1280 × 720', 'Не менше 1280 × 720'), t('Не менее 1280 × 720', 'At least 1280 × 720', 'Не менше 1280 × 720')],
                [t('Устройства ввода', 'Input devices', 'Пристрої введення'), t('Клавиатура и мышь', 'Keyboard and mouse', 'Клавіатура й миша'),
                 t('Клавиатура и мышь, рекомендуется многокнопочная мышь с колесом прокрутки', 'Keyboard and mouse, a multi-button mouse with a scroll wheel is recommended', 'Клавіатура й миша, рекомендовано багатокнопкову мишу з колесом прокрутки')],
            ]}),
        ]},
        {'id': 'mac', 'title': 'Mac', 'blocks': [
            ('table', {'head': REQ_HEAD, 'rows': [
                [t('Система', 'System', 'Система'), 'macOS 12', 'macOS 15'],
                [t('Процессор', 'Processor', 'Процесор'),
                 t('Apple M2 или Intel Core 9-го поколения (Coffee Lake)', 'Apple M2 or 9th generation Intel Core (Coffee Lake)', 'Apple M2 або Intel Core 9-го покоління (Coffee Lake)'), 'Apple M4'],
                [t('Видеокарта', 'Graphics', 'Відеокарта'), t('Metal, 4 ГБ; Apple M2 с 8 ГБ', 'Metal, 4 GB; Apple M2 with 8 GB', 'Metal, 4 ГБ; Apple M2 з 8 ГБ'),
                 t('Apple M4 с 16 ГБ', 'Apple M4 with 16 GB', 'Apple M4 з 16 ГБ')],
                [t('Память', 'Memory', 'Пам’ять'), RAM8, RAM16],
                [t('Диск', 'Storage', 'Диск'), SSD, SSD],
            ]}),
        ]},
        {'id': 'gpu', 'title': t('Старые видеокарты', 'Older graphics cards', 'Старі відеокарти'), 'blocks': [
            ('text', [t('Новому виду мира нужна функция, которой нет у старых видеокарт, поэтому с выходом Forever их поддержка закончилась. Видеокарта должна быть на одной из этих архитектур или новее:',
                        'The new look of the world needs a feature that older graphics cards lack, so their support ends with the Forever launch. Your card must be on one of these architectures or newer:',
                        'Новому вигляду світу потрібна функція, якої немає у старих відеокарт, тому з виходом Forever їх підтримка закінчується. Відеокарта має бути на одній із цих архітектур або новішій:')]),
            ('table', {'head': [t('Производитель', 'Maker', 'Виробник'), t('Не старше', 'This or newer', 'Не старша'), t('Запустится', 'Will start', 'Запуститься'),
                                t('Не запустится', 'Will not start', 'Не запуститься')], 'rows': [
                ['AMD', 'Graphics Core Next 1 (2012)', 'Radeon HD 7850', 'Radeon HD 6950'],
                ['NVIDIA', 'Maxwell (2014)', 'GeForce GTX 9xx, GTX 750 / 750 Ti', 'GeForce GTX 760, GTX 770 / 780, 8xxM'],
                ['Intel', 'Skylake (2015)', 'HD Graphics 530', 'Intel HD Graphics 6000'],
            ]}),
            ('tip', t('Такая видеокарта только запускает игру, до минимума выше ей далеко. Покупать железо стоит по столбцу «Минимум».',
                      'Such a card only starts the game and is still far below the minimum above. When buying hardware, go by the Minimum column.',
                      'Така відеокарта лише запускає гру, до мінімуму вище їй далеко. Купувати залізо варто за стовпцем «Мінімум».')),
            ('text', [t('Для игры нужны интернет, учётная запись и приложение Battle.net.',
                        'You need an internet connection, a Battle.net account and the Battle.net app.',
                        'Для гри потрібні інтернет, обліковий запис і застосунок Battle.net.')]),
        ]},
    ],
})

# ---------- Подземелья и рейды (переехали #dungeons и #group главной) ----------

def _dg_filter():
    """Filter bar + table shell for the dungeons list; rows are drawn by JS['dungeons'] from DUNGEONS."""
    out = {}
    for l, (flt, all_, mine, new, my, lo, hi, cols) in {
        'ru': ('Фильтр подземелий', 'Все', 'Мой уровень ±3', 'Новые', 'Мой уровень', 'Уровень ниже', 'Уровень выше', ('Подземелье', 'Уровни', 'Где вход')),
        'en': ('Dungeon filter', 'All', 'My level ±3', 'New', 'My level', 'Lower level', 'Higher level', ('Dungeon', 'Levels', 'Entrance')),
        'uk': ('Фільтр підземель', 'Усі', 'Мій рівень ±3', 'Нові', 'Мій рівень', 'Нижчий рівень', 'Вищий рівень', ('Підземелля', 'Рівні', 'Де вхід')),
    }.items():
        ths = ''.join(f'<th scope="col">{c}</th>' for c in cols)
        out[l] = (f'<div id="dgBox"><div class="filters" role="group" aria-label="{flt}">'
                  f'<div class="seg" id="segD"><button type="button" data-v="all" aria-pressed="true">{all_}</button>'
                  f'<button type="button" data-v="mine" aria-pressed="false">{mine}</button>'
                  f'<button type="button" data-v="new" aria-pressed="false">{new}</button></div>'
                  f'<div class="fgroup"><span class="flabel" id="ldgLvl">{my}</span><div class="stepper" role="group" aria-labelledby="ldgLvl">'
                  f'<button type="button" class="lvm" aria-label="{lo}">−</button>'
                  f'<input class="lvin" id="dgLvl" type="number" min="1" max="60" inputmode="numeric" aria-labelledby="ldgLvl" placeholder="—">'
                  f'<button type="button" class="lvp" aria-label="{hi}">+</button></div></div>'
                  f'<span class="small" id="dgCount" role="status"></span></div>'
                  f'<table class="gtable dgt"><thead><tr>{ths}</tr></thead>'
                  f'<tbody id="dgBody"></tbody></table></div>')
    return out


GUIDES.append({
    'slug': 'dungeons', 'art': 'warlock', 'hero': 'hero_dungeons', 'js': 'dungeons',
    'title': t('Подземелья и рейды', 'Dungeons and raids', 'Підземелля та рейди'),
    'lead': t('Все 35 подземелий по уровням с фильтром под вашего персонажа, три рейда и состав группы под любое число друзей.',
              'All 35 dungeons by level with a filter for your character, three raids and a group lineup for any number of friends.',
              'Усі 35 підземель за рівнями з фільтром під персонажа, три рейди та склад групи під будь-яку кількість друзів.'),
    'tile': t('35 подземелий по уровням, рейды, состав группы', '35 dungeons by level, raids, group lineup', '35 підземель за рівнями, рейди, склад групи'),
    'pills': [t('35 подземелий', '35 dungeons', '35 підземель'), t('9 новых', '9 new', '9 нових'),
              t('Рейды с 09.12', 'Raids from 09.12', 'Рейди з 09.12')],
    'sources': [
        (t('Warcraft Tavern: подземелья', 'Warcraft Tavern: dungeons', 'Warcraft Tavern: підземелля'), 'https://www.warcrafttavern.com/forever/guides/dungeons/'),
        (t('Sportskeeda: подземелья по уровням', 'Sportskeeda: dungeons by level', 'Sportskeeda: підземелля за рівнями'),
         'https://www.sportskeeda.com/mmo/world-warcraft-forever-all-dungeons-order-level-range'),
        (t('Icy Veins: обзор подземелий', 'Icy Veins: dungeons overview', 'Icy Veins: огляд підземель'), 'https://www.icy-veins.com/wow-forever/dungeons-overview'),
        (t('ClassicWoW.gg: подземелья', 'ClassicWoW.gg: dungeons', 'ClassicWoW.gg: підземелля'), 'https://classicwow.gg/forever/dungeons'),
        (t('Blizzard: заметки разработчиков беты Forever', 'Blizzard: WoW Forever beta development notes', 'Blizzard: нотатки розробників бети Forever'), 'https://us.forums.blizzard.com/en/wow/t/2360696/6'),
        (t('Warcraft Tavern: Legacy', 'Warcraft Tavern: Legacy', 'Warcraft Tavern: Legacy'), 'https://www.warcrafttavern.com/forever/guides/legacy/'),
        (t('LFCarry: классы и темп прокачки', 'LFCarry: classes and leveling pace', 'LFCarry: класи та темп прокачування'), 'https://lfcarry.com/guides/wow-forever-classes'),
    ],
    'sections': [
        {'id': 'list', 'title': t('Подземелья по уровням', 'Dungeons by level', 'Підземелля за рівнями'), 'blocks': [
            ('text', [t('Жёстких ограничений по уровню Blizzard не публиковала.', 'Blizzard has not published hard level limits.',
                        'Жорстких обмежень за рівнем Blizzard не публікувала.')]),   # sources: the list at the end; a differing range: under the level in the row
            ('raw', _dg_filter()),
            ('text', [t('Вход в [[Даларан|City of Dalaran]] Орде не закрыт. По заметкам беты Blizzard от 16.10 Орду в самом городе атакуют, едва заметив, но на доступ к подземелью это не влияет. Цепочка заданий Орды на Dalaran Sewer Key больше не даёт свободного прохода по городу.',
                        'The Horde is not locked out of City of Dalaran. Per the Blizzard beta notes of Oct 16, the Horde is attacked on sight in the city itself, but this does not affect access to the dungeon. The Horde questline for the Dalaran Sewer Key no longer grants free passage through the city.',
                        'Вхід у City of Dalaran для Орди не закритий. За нотатками бети Blizzard від 16.10 Орду в самому місті атакують, щойно помітять, але на доступ до підземелля це не впливає. Ланцюжок завдань Орди на Dalaran Sewer Key більше не дає вільного проходу містом.')]),
            ('text', [t('Основной опыт за подземелье дают его цепочки заданий, повторные заходы приносят заметно меньше. Любая выпавшая вещь открывает свой облик всем в группе, кто может её надеть. Ещё по два подземелья Blizzard обещает весной и летом.',
                        'Most dungeon experience comes from its quest chains, repeat runs give noticeably less. Every item that drops unlocks its appearance for everyone in the group who can wear it. Blizzard promises two more dungeons in spring and two in summer.',
                        'Основний досвід за підземелля дають його ланцюжки завдань, повторні заходи дають помітно менше. Будь-яка річ, що випала, відкриває свій вигляд усім у групі, хто може її вдягнути. Ще по два підземелля Blizzard обіцяє навесні та влітку.')]),
        ]},
        {'id': 'raids', 'title': t('Рейды (с 09.12.2026)', 'Raids (from 09.12.2026)', 'Рейди (з 09.12.2026)'), 'blocks': [
            ('steps', [
                {'t': 'Barrow Deeps', 'd': t('10 игроков', '10 players', '10 гравців')},
                {'t': 'Hyjal Summit', 'd': t('20 игроков', '20 players', '20 гравців')},
                {'t': 'Onyxia’s Lair', 'd': t('40 игроков, в [[Пылевых топях|Dustwallow Marsh]]', '40 players, in Dustwallow Marsh', '40 гравців, у Dustwallow Marsh')},
            ]),
            ('text', [t('За прохождение каждого из этих рейдов в Legacy даётся по очку.', 'Completing each of these raids gives one Legacy point.',
                        'За проходження кожного з цих рейдів у Legacy дається по одному очку.')]),
        ]},
        {'id': 'pvp', 'title': 'PvP', 'blocks': [
            ('steps', [
                {'t': 'Darkspear Islands', 'd': t('Новое поле боя 15 на 15 у побережья [[Пылевых топей|Dustwallow Marsh]].', 'New 15v15 battleground off the coast of Dustwallow Marsh.',
                                                  'Нове поле бою 15 на 15 біля узбережжя Dustwallow Marsh.')},
                {'t': t('Звания и Честь', 'Ranks and Honor', 'Звання та Честь'),
                 'd': t('Звания с недельным лимитом, улучшение экипировки за Честь, сезонные цели Legacy.', 'Ranks with a weekly limit, gear upgrades for Honor, seasonal Legacy goals.',
                        'Звання з тижневим лімітом, покращення екіпірування за Честь, сезонні цілі Legacy.')},
            ]),
            ('raw', t('<p><a class="more-l" href="../pvp/">PvP в WoW Forever: звания, награды и поля боя</a></p>',
                      '<p><a class="more-l" href="../pvp/">PvP in WoW Forever: ranks, rewards and battlegrounds</a></p>',
                      '<p><a class="more-l" href="../pvp/">PvP у WoW Forever: звання, нагороди й поля бою</a></p>')),
        ]},
        {'id': 'group', 'title': t('Состав группы', 'Group composition', 'Склад групи'), 'blocks': [
            ('steps', [
                {'t': t('Подземелья на 5', 'Dungeons for 5', 'Підземелля на 5'),
                 'd': t('Подземелья рассчитаны на 5 игроков: танк, лекарь, трое с уроном.', 'Dungeons are designed for 5 players: a tank, a healer and three damage dealers.',
                        'Підземелля розраховані на 5 гравців: танк, цілитель, троє зі шкодою.')},
                {'t': t('Рейды на 10, 20 и 40', 'Raids for 10, 20 and 40', 'Рейди на 10, 20 і 40'),
                 'd': t('Если своих меньше, недостающих добирают из гильдии.', 'If your own group is smaller, the rest are filled from a guild.',
                        'Якщо своїх менше, решту добирають із гільдії.')},
                {'t': t('Кто танкует и лечит', 'Who tanks and heals', 'Хто танкує й лікує'),
                 'd': t('Танковать могут Воин, Паладин и Друид, лечить Паладин, Жрец, Шаман и Друид.', 'Warriors, Paladins and Druids can tank; Paladins, Priests, Shamans and Druids can heal.',
                        'Танкувати можуть Воїн, Паладин і Друїд, лікувати Паладин, Жрець, Шаман і Друїд.')},
                {'t': t('Паладин и Друид', 'Paladin and Druid', 'Паладин і Друїд'),
                 'd': t('Паладин и Друид умеют все три роли. Это самые гибкие классы, когда игроков мало.', 'Paladins and Druids can do all three roles. They are the most flexible classes when players are few.',
                        'Паладин і Друїд вміють усі три ролі. Це найгнучкіші класи, коли гравців мало.')},
                {'t': t('Баффы классов', 'Class buffs', 'Баффи класів'),
                 'd': t('Группа и рейд получают баффы классов: Королей от паладина, тотемы шамана, Боевой крик воина, ауры охотника и друида. Порталы, еду и воду делает маг.',
                        'Groups and raids receive class buffs: Kings from the paladin, shaman totems, the warrior’s Battle Shout, hunter and druid auras. Portals, food and water come from the mage.',
                        'Група й рейд отримують баффи класів: Королів від паладина, тотеми шамана, Бойовий клич воїна, аури мисливця та друїда. Портали, їжу та воду робить маг.')},
            ]),
            ('tabs', [
                {'id': 'solo', 't': t('Соло', 'Solo', 'Соло'), 'blocks': [
                    ('tip', t('Легче всего Охотнику и Чернокнижнику, у них питомец держит врага. Паладин и Друид тоже живучи и в подземелье пойдут на любую роль.',
                              'Hunters and Warlocks have it easiest, their pet holds the enemy. Paladins and Druids are also sturdy and can fill any role in a dungeon.',
                              'Найлегше Мисливцю й Чорнокнижнику, у них вихованець тримає ворога. Паладин і Друїд теж живучі й у підземеллі підуть на будь-яку роль.'))]},
                {'id': 'p2-4', 't': t('2–4 игрока', '2–4 players', '2–4 гравці'), 'blocks': [
                    ('tip', t('Пусть хотя бы один умеет танковать или лечить (Воин, Паладин, Друид, Жрец, Шаман), остальных до пяти добирайте в подземелье.',
                              'Make sure at least one of you can tank or heal (Warrior, Paladin, Druid, Priest, Shaman), and fill the dungeon group up to five.',
                              'Нехай хоча б один уміє танкувати або лікувати (Воїн, Паладин, Друїд, Жрець, Шаман), решту до п’яти добирайте в підземелля.'))]},
                {'id': 'p5', 't': t('5 игроков', '5 players', '5 гравців'), 'blocks': [
                    ('tip', t('Танк, лекарь и трое в урон, например Воин, Жрец, Маг, Охотник и Разбойник.',
                              'A tank, a healer and three damage dealers, for example Warrior, Priest, Mage, Hunter and Rogue.',
                              'Танк, цілитель і троє в шкоду, наприклад Воїн, Жрець, Маг, Мисливець і Розбійник.'))]},
                {'id': 'p6-9', 't': t('6–9 игроков', '6–9 players', '6–9 гравців'), 'blocks': [
                    ('tip', t('Две группы для подземелий, в каждой нужны свой танк и лекарь. Тут особенно ценны гибриды: Паладин, Друид, Шаман.',
                              'Two dungeon groups, each needs its own tank and healer. Hybrids are especially valuable here: Paladin, Druid, Shaman.',
                              'Дві групи для підземель, у кожній потрібні свій танк і цілитель. Тут особливо цінні гібриди: Паладин, Друїд, Шаман.'))]},
                {'id': 'p10', 't': t('10 и больше', '10 or more', '10 і більше'), 'blocks': [
                    ('tip', t('Хватает на 10-местный рейд Barrow Deeps: два танка, два-три лекаря, остальные в урон.',
                              'Enough for the 10-player Barrow Deeps raid: two tanks, two or three healers, the rest on damage.',
                              'Вистачає на 10-місний рейд Barrow Deeps: два танки, два-три цілителі, решта в шкоду.'))]},
            ]),
            ('tip', t('Берите разные классы: баффы разных классов складываются, а одинаковые перекрываются. Кто-то в группе берёт Кулинарию ради костра на 10 объектов, остальные по профессии под баффы лагеря.',
                      'Take different classes: buffs of different classes stack, while identical ones overlap. Someone in the group takes Cooking for a campfire with 10 objects, the others pick professions for camp buffs.',
                      'Беріть різні класи: баффи різних класів складаються, а однакові перекриваються. Хтось у групі бере Кулінарію заради вогнища на 10 об’єктів, решта за професією під баффи табору.')),
        ]},
        {'id': 'together', 'title': t('Прокачка вместе', 'Leveling together', 'Прокачування разом'), 'blocks': [
            ('steps', [
                {'t': t('Темп классов', 'Class pace', 'Темп класів'),
                 'd': t('По оценке LFCarry Охотник и Маг прокачиваются быстрее всего (примерно на 8% быстрее среднего), Воин медленнее всех (около 12%), Друид и Жрец чуть медленнее среднего. Это оценки для беты, цифры могут измениться.',
                        'By LFCarry’s estimate, Hunter and Mage level fastest (about 8% faster than average), Warrior slowest (about 12%), Druid and Priest slightly slower than average. These are beta estimates, the figures may change.',
                        'За оцінкою LFCarry Мисливець і Маг прокачуються найшвидше (приблизно на 8% швидше за середнє), Воїн повільніше за всіх (близько 12%), Друїд і Жрець трохи повільніше за середнє. Це оцінки для бети, цифри можуть змінитися.')},
                {'t': t('Без масштабирования', 'No level scaling', 'Без масштабування'),
                 'd': t('Подземелья рассчитаны на свои уровни, а протаскивать отставшего друга Blizzard сделала невыгодным.', 'Dungeons are built for their own levels, and Blizzard made boosting a friend who lags behind unprofitable.',
                        'Підземелля розраховані на свої рівні, а протягувати друга, що відстав, Blizzard зробила невигідним.')},
                {'t': t('Копите отдых', 'Save up rest', 'Копіть відпочинок'),
                 'd': t('Спальник, Well Rested и еда с бонусом опыта складываются.', 'The bedroll, Well Rested and food with an experience bonus stack.',
                        'Спальник, Well Rested і їжа з бонусом досвіду складаються.')},
                {'t': t('Лагерь на прокачке', 'Camp while leveling', 'Табір на прокачуванні'),
                 'd': t('Лагерь можно ставить прямо на прокачке, пять минут на костёр окупаются баффами на группу.',
                        'You can set up camp right while leveling; five minutes for a campfire pays off with buffs for the group.',
                        'Табір можна ставити просто на прокачуванні, п’ять хвилин на вогнище окупаються баффами на групу.')},
            ]),
            ('tip', t('С 5 ноября по 9 декабря прокачайтесь вместе по подземельям и заранее решите, кто за какой класс, чтобы не дублироваться.',
                      'From launch (4–5 November) to 9 December, level up together through dungeons, and decide in advance who plays which class so you do not duplicate.',
                      'З 5 листопада по 9 грудня прокачайтеся разом по підземеллях і заздалегідь вирішіть, хто за який клас, щоб не дублюватися.')),
        ]},
    ],
})

# ---------- Прокачка 1–60 (переехали #legacy и #camp главной) ----------

KIT = {'id': 'kit', 'title': t('Что взять и сделать при прокачке', 'What to take and make while leveling', 'Що взяти й зробити на прокачуванні'), 'blocks': [
            ('text', [t('Здесь то, что игрок делает сам: еда, бинты, зелья, масла и зачарования. Данные беты до 30 уровня (Wowhead, 4–26 октября 2026); рецепты для 31–60 уровней станут известны после старта, где данных нет, так и написано.', 'What a player can make alone: food, bandages, potions, oils and enchants. The data comes from the beta up to level 30 (Wowhead, Oct 4–26, 2026); recipes for levels 31–60 will be known after launch, and where there is no data we say so.', 'Те, що гравець робить сам: їжа, бинти, зілля, олії та зачарування. Дані бети до 30 рівня (Wowhead, 4–26 жовтня 2026); рецепти для рівнів 31–60 стануть відомі після старту, де даних немає, так і написано.')]),
            ('text', [t('Цена — наша оценка по материалам: «дёшево», если они падают с врагов или продаются торговцем, «средне», если нужны травы, руда или Merchant’s Favor. Цен на аукционе до старта нет.', 'Price is our estimate from the materials: “cheap” if they drop from enemies or a vendor sells them, “medium” if you need herbs, ore or Merchant’s Favor. There are no auction prices before launch.', 'Ціна — наша оцінка за матеріалами: «дешево», якщо вони падають з ворогів або їх продає торговець, «середньо», якщо потрібні трави, руда чи Merchant’s Favor. Цін на аукціоні до старту немає.')]),
            ('tabs', [
                {'id': 'food', 't': t('Еда', 'Food', 'Їжа'), 'blocks': [('text', [t('Кулинария — вспомогательная профессия, основное место не занимает. Любая готовая еда даёт Well Fed XP Boost: +5% опыта за убийства на 15 минут (за задания нет). Варить нужно у огня: у своего костра или у очага в трактире. Приправы Mild Spices и Soothing Spices продают торговцы в городах.', 'Cooking is a secondary profession and takes no primary slot. Cooked food gives Well Fed XP Boost: +5% experience from kills for 15 minutes (not from quests). You cook at a fire: your own campfire or an inn hearth. Mild Spices and Soothing Spices are sold by vendors in cities.', 'Кулінарія — допоміжна професія, основний слот не займає. Будь-яка готова їжа дає Well Fed XP Boost: +5% досвіду за вбивства на 15 хвилин (за завдання ні). Варити треба біля вогню: біля власного вогнища чи каміна в таверні. Приправи Mild Spices і Soothing Spices продають торговці в містах.')]),
                ('table', {'head': [t('Навык', 'Skill', 'Навичка'), t('Блюдо', 'Dish', 'Страва'), t('Сколько', 'How many', 'Скільки'), t('Рецепт', 'Recipe', 'Рецепт'), t('Цена', 'Price', 'Ціна')], 'rows': [
                ['1–50', 'Brilliant Smallfish', '52', 'Stormwind / Thunder Bluff', t('дёшево', 'cheap', 'дешево')],
                ['50–100', 'Longjaw Mud Snapper', '55', 'Goldshire / Thunder Bluff', t('дёшево', 'cheap', 'дешево')],
                ['100–150', 'Bristle Whisker Catfish', '55', 'Stormwind / Thunder Bluff', t('дёшево', 'cheap', 'дешево')],
                ['150–175', 'Bristle Whisker Catfish', '65', 'Expert Cookbook', t('дёшево', 'cheap', 'дешево')],
                ['175–225', 'Mithril Head Trout', '55', 'Ironforge / Orgrimmar', t('дёшево', 'cheap', 'дешево')]]}),
                ('text', [t('Количество — сырая рыба; на деле выйдет чуть больше или меньше, как повезёт с прибавкой навыка. Сырая рыба на аукционе обычно недорога, а наловить её самому поможет Рыбалка. С навыка 150 нужна книга Expert Cookbook: Альянс покупает её в Ashenvale, Орда в Desolace (есть и на аукционе). Ступень Artisan (225–300) открывает квест Clamlette Surprise на 35 уровне при навыке 225.', 'The quantity is raw fish; in practice you need a little more or less, depending on luck with skill-ups. Raw fish is usually cheap at the auction house, and Fishing lets you catch it yourself. From skill 150 you need the Expert Cookbook: Alliance buys it in Ashenvale, Horde in Desolace (it is also at the auction house). The Artisan rank (225–300) opens with the Clamlette Surprise quest at level 35 and skill 225.', 'Кількість — сира риба; насправді вийде трохи більше чи менше, як пощастить із приростом навички. Сира риба на аукціоні зазвичай недорога, а наловити її самому допоможе Рибальство. З навички 150 потрібна книга Expert Cookbook: Альянс купує її в Ashenvale, Орда в Desolace (є й на аукціоні). Ступінь Artisan (225–300) відкриває завдання Clamlette Surprise на 35 рівні при навичці 225.')]),
                ('text', [t('Рецепты без вложений: часть блюд падает с врагов или даётся за задание, навык у них низкий.', 'Recipes that cost nothing: some dishes drop from enemies or come from a quest, and their skill requirement is low.', 'Рецепти без витрат: частина страв падає з ворогів або дається за завдання, навичка в них низька.')]),
                ('table', {'head': [t('Блюдо', 'Dish', 'Страва'), t('Навык', 'Skill', 'Навичка'), t('Откуда', 'Source', 'Звідки')], 'rows': [
                ['Venomous Smoothie', '25', t('Торговец, 30 Merchant’s Favor', 'Vendor, 30 Merchant’s Favor', 'Торговець, 30 Merchant’s Favor')],
                ['Skywall Souffle', '25', t('Задание: Restocking the Larders', 'Quest: Restocking the Larders', 'Завдання: Restocking the Larders')],
                ['Peace Tea', '25', t('Падает с: Frostmane Seer', 'Drop from: Frostmane Seer', 'Падає з: Frostmane Seer')],
                ['Tasty Raptor Bites', '25', t('Падает с: Sunscale Screecher, Mottled Raptor', 'Drop from: Sunscale Screecher, Mottled Raptor', 'Падає з: Sunscale Screecher, Mottled Raptor')],
                ['Pincer Bites', '35', t('Задание: Crab Season', 'Quest: Crab Season', 'Завдання: Crab Season')],
                ['Breakfast Omelette', '75', t('Падает с: Dire Condor', 'Drop from: Dire Condor', 'Падає з: Dire Condor')]]})]},
                {'id': 'aid', 't': t('Бинты и зелья', 'Bandages and potions', 'Бинти та зілля'), 'blocks': [('text', [t('Первая помощь — вспомогательная профессия. Бинты шьют из ткани, которая падает с гуманоидов; по Wowhead это обычно самый дешёвый способ поднять навык. В Forever зелья лечения делает Первая помощь, а не Алхимия, поэтому их может сделать любой.', 'First Aid is a secondary profession. Bandages are sewn from cloth that humanoids drop, and per Wowhead that is usually the cheapest way to raise the skill. In Forever, healing potions are made by First Aid, not Alchemy, so anyone can make them.', 'Перша допомога — допоміжна професія. Бинти шиють із тканини, що падає з гуманоїдів; за Wowhead це зазвичай найдешевший спосіб підняти навичку. У Forever зілля лікування робить Перша допомога, а не Алхімія, тож його може зробити будь-хто.')]),
                ('table', {'head': [t('Навык', 'Skill', 'Навичка'), t('Бинт', 'Bandage', 'Бинт'), t('Сколько', 'How many', 'Скільки'), t('Ткань', 'Cloth', 'Тканина'), t('Цена', 'Price', 'Ціна')], 'rows': [
                ['1–40', 'Linen Bandage', '45', '45 Linen Cloth', t('дёшево', 'cheap', 'дешево')],
                ['40–80', 'Heavy Linen Bandage', '65', '130 Linen Cloth', t('дёшево', 'cheap', 'дешево')],
                ['80–115', 'Wool Bandage', '50', '50 Wool Cloth', t('дёшево', 'cheap', 'дешево')],
                ['115–150', 'Heavy Wool Bandage', '50', '100 Wool Cloth', t('дёшево', 'cheap', 'дешево')],
                ['150–180', 'Silk Bandage', '45', '45 Silk Cloth', t('дёшево', 'cheap', 'дешево')],
                ['180–210', 'Heavy Silk Bandage', '45', '90 Silk Cloth', t('дёшево', 'cheap', 'дешево')],
                ['210–225', 'Mageweave Bandage', '20', '20 Mageweave Cloth', t('дёшево', 'cheap', 'дешево')]]}),
                ('text', [t('С навыка 150 нужны книга Expert First Aid - Under Wraps и руководства по Heavy Silk Bandage и Mageweave Bandage: Альянс покупает их в Stromgarde Keep (Arathi Highlands), Орда в Brackenwall Village (Dustwallow Marsh). Книги не привязаны, их можно взять на аукционе. Ступень Artisan (225–300) даёт квест Triage на 35 уровне при навыке 225.', 'From skill 150 you need the Expert First Aid - Under Wraps book and the manuals for Heavy Silk Bandage and Mageweave Bandage: Alliance buys them in Stromgarde Keep (Arathi Highlands), Horde in Brackenwall Village (Dustwallow Marsh). The books are not bound, so you can get them at the auction house. The Artisan rank (225–300) comes from the Triage quest at level 35 and skill 225.', 'З навички 150 потрібні книга Expert First Aid - Under Wraps і посібники з Heavy Silk Bandage та Mageweave Bandage: Альянс купує їх у Stromgarde Keep (Arathi Highlands), Орда в Brackenwall Village (Dustwallow Marsh). Книги не прив’язуються, їх можна взяти на аукціоні. Ступінь Artisan (225–300) дає завдання Triage на 35 рівні при навичці 225.')]),
                ('table', {'head': [t('Зелье', 'Potion', 'Зілля'), t('Навык', 'Skill', 'Навичка'), t('Откуда', 'Source', 'Звідки')], 'rows': [
                ['Minor Healing Potion', '1', t('Тренер', 'Trainer', 'Тренер')],
                ['Lesser Healing Potion', '55', t('Тренер', 'Trainer', 'Тренер')],
                ['Healing Potion', '110', t('Тренер', 'Trainer', 'Тренер')],
                ['Greater Healing Potion', '155', 'Manual: Greater Healing Potion'],
                ['Superior Healing Potion', '215', 'Manual: Superior Healing Potion'],
                ['Major Healing Potion', '275', 'Manual: Major Healing Potion']]})]},
                {'id': 'alch', 't': t('Эликсиры и масла', 'Elixirs and oils', 'Еліксири та олії'), 'blocks': [('text', [t('В Forever у Алхимии больше 50 новых рецептов, и она полезна уже на прокачке. Склянки (Empty Vial и другие) продают торговцы, травы собирает Травничество. Флаконы (Flask of Natural Accuracy, Aggression, Precision, Swiftness) требуют навыка 300: это уже конец прокачки. Часть рецептов продают за Merchant’s Favor, часть падает с врагов.', 'In Forever, Alchemy has more than 50 new recipes and is useful already while leveling. Vials (Empty Vial and others) are sold by vendors, herbs come from Herbalism. Flasks (Flask of Natural Accuracy, Aggression, Precision, Swiftness) need skill 300, which is the end of leveling. Some recipes are sold for Merchant’s Favor, some drop from enemies.', 'У Forever в Алхімії понад 50 нових рецептів, і вона корисна вже на прокачуванні. Колби (Empty Vial та інші) продають торговці, трави збирає Травництво. Флакони (Flask of Natural Accuracy, Aggression, Precision, Swiftness) вимагають навички 300: це вже кінець прокачування. Частину рецептів продають за Merchant’s Favor, частина падає з ворогів.')]),
                ('table', {'head': [t('Эликсир или масло', 'Elixir or oil', 'Еліксир або олія'), t('Навык', 'Skill', 'Навичка'), t('Откуда', 'Source', 'Звідки')], 'rows': [
                ['Minor Arcane Elixir', '1', t('Тренер', 'Trainer', 'Тренер')],
                ['Elixir of Minor Spirit', '15', t('Падает с: Gnarlpine Gardener', 'Drop from: Gnarlpine Gardener', 'Падає з: Gnarlpine Gardener')],
                ['Minor Mageblood Elixir', '25', t('Падает с: Young Wendigo', 'Drop from: Young Wendigo', 'Падає з: Young Wendigo')],
                ['Minor Cleric’s Elixir', '45', t('Падает с: Vile Fin Attacker', 'Drop from: Vile Fin Attacker', 'Падає з: Vile Fin Attacker')],
                ['Elixir of Lesser Spirit', '65', t('Торговец, 45 Merchant’s Favor', 'Vendor, 45 Merchant’s Favor', 'Торговець, 45 Merchant’s Favor')],
                ['Elixir of Lesser Intellect', '95', t('Торговец, 45 Merchant’s Favor', 'Vendor, 45 Merchant’s Favor', 'Торговець, 45 Merchant’s Favor')],
                ['Elixir of Spirit', '115', t('Падает с: Bloodfury Harpy', 'Drop from: Bloodfury Harpy', 'Падає з: Bloodfury Harpy')],
                ['Elixir of Intellect', '135', t('Падает с: Galak Mauler', 'Drop from: Galak Mauler', 'Падає з: Galak Mauler')],
                ['Minor Wizard Oil', 'Enchanting 5', t('Поставщик чар', 'Enchanting supplier', 'Постачальник чар')],
                ['Lesser Wizard Oil', 'Enchanting 200', t('Поставщик чар', 'Enchanting supplier', 'Постачальник чар')],
                ['Minor Mana Oil', 'Enchanting 150', t('Поставщик чар', 'Enchanting supplier', 'Постачальник чар')]]}),
                ('text', [t('Minor Wizard Oil даёт +8 к урону и лечению заклинаниями, Lesser Wizard Oil +16, Minor Mana Oil ускоряет восстановление маны; масла делает зачарователь. Самое доступное масло для заклинателя — Minor Wizard Oil: нужен навык чар 5.', 'Minor Wizard Oil gives +8 spell damage and healing, Lesser Wizard Oil +16, and Minor Mana Oil speeds up mana regeneration; an enchanter makes the oils. The most accessible oil for a caster is Minor Wizard Oil: it needs Enchanting skill 5.', 'Minor Wizard Oil дає +8 до шкоди й лікування закляттями, Lesser Wizard Oil +16, Minor Mana Oil пришвидшує відновлення мани; олії робить зачарувальник. Найдоступніша олія для заклинача — Minor Wizard Oil: потрібна навичка чар 5.')])]},
                {'id': 'ench', 't': t('Зачарования', 'Enchants', 'Зачарування'), 'blocks': [('text', [t('Список для заклинателей на уровне 30 (по гайду зачарователя на Wowhead от 14 октября 2026, он составлен для Чернокнижника и подходит магам, жрецам и другим заклинателям). Enchanting Vellum в Forever нет: зачаровывает зачарователь через нижнюю панель торговли, поэтому без профессии ищите такого игрока. Чары между собой не сравнивали.', 'A list for casters at level 30 (from the Wowhead enchanter guide of Oct 14, 2026, written for Warlocks and suiting mages, priests and other casters). There is no Enchanting Vellum in Forever: an enchanter applies enchants through the lower trade panel, so without the profession you look for such a player. The enchants were not compared against each other.', 'Список для заклиначів на рівні 30 (за гайдом зачарувальника на Wowhead від 14 жовтня 2026, він складений для Чорнокнижника й підходить магам, жерцям та іншим заклиначам). Enchanting Vellum у Forever немає: зачаровує зачарувальник через нижню панель торгівлі, тож без професії шукайте такого гравця. Чари між собою не порівнювали.')]),
                ('table', {'head': [t('Слот', 'Slot', 'Слот'), t('Зачарование', 'Enchant', 'Зачарування'), t('Что даёт', 'What it gives', 'Що дає'), t('Откуда', 'Source', 'Звідки')], 'rows': [
                [t('Шея', 'Neck', 'Шия'), 'Spell Power', t('+6 к силе заклинаний', '+6 spell power', '+6 до сили заклинань'), t('Формула за 120 Merchant’s Favor, чары 210', 'Formula for 120 Merchant’s Favor, Enchanting 210', 'Формула за 120 Merchant’s Favor, чари 210')],
                [t('Грудь', 'Chest', 'Груди'), 'Greater Intellect', t('+6 к интеллекту', '+6 Intellect', '+6 до інтелекту'), t('Тренер чар, 185', 'Enchanting trainer, 185', 'Тренер чар, 185')],
                [t('Запястья', 'Wrists', 'Зап’ястя'), 'Lesser Intellect', t('+5 к интеллекту', '+5 Intellect', '+5 до інтелекту'), t('Тренер чар, 150', 'Enchanting trainer, 150', 'Тренер чар, 150')],
                [t('Запястья', 'Wrists', 'Зап’ястя'), 'Lesser Healing Power', t('+6 к урону и +16 к лечению', '+6 spell damage, +16 healing', '+6 до шкоди й +16 до лікування'), t('Формула у кентавров (торговец или задание), чары 205', 'Formula from centaurs (vendor or quest), Enchanting 205', 'Формула в кентаврів (торговець або завдання), чари 205')],
                [t('Оружие, двуручное', 'Two-hand weapon', 'Зброя, дворучна'), 'Lesser Intellect', t('+5 к интеллекту', '+5 Intellect', '+5 до інтелекту'), t('Поставщик чар, 100', 'Enchanting supplier, 100', 'Постачальник чар, 100')],
                [t('Оружие', 'Weapon', 'Зброя'), 'Revelation', t('шанс критического удара заклинанием', 'a spell crit chance proc', 'шанс критичного удару закляттям'), t('Формула за 45 Merchant’s Favor, чары 140', 'Formula for 45 Merchant’s Favor, Enchanting 140', 'Формула за 45 Merchant’s Favor, чари 140')],
                [t('Ступни', 'Feet', 'Ступні'), 'Minor Speed', t('скорость бега', 'movement speed', 'швидкість бігу'), t('Тренер чар, 225', 'Enchanting trainer, 225', 'Тренер чар, 225')],
                [t('Грудь, руки, ноги, ступни', 'Chest, hands, legs, feet', 'Груди, руки, ноги, ступні'), 'Mystic Heavy Kit', t('+4 к силе заклинаний и +24 к броне', '+4 spell power, +24 armor', '+4 до сили заклинань і +24 до броні'), t('Выкройка у поставщика кожевника, навык 135', 'Pattern from a leatherworking supplier, skill 135', 'Викрійка в постачальника кожум’яки, навичка 135')]]}),
                ('text', [t('Для ближнего боя формулы шеи Agility и Strength продают за Merchant’s Favor (навык 210), перчаток Superior Strength (навык 300); подборки чар под ближний бой на 30 уровне пока нет, поэтому не пишем.', 'For melee, the Agility and Strength neck formulas are sold for Merchant’s Favor (skill 210), and Superior Strength gloves at skill 300; there is no list of melee enchants for level 30 yet, so we do not write one.', 'Для ближнього бою формули шиї Agility і Strength продають за Merchant’s Favor (навичка 210), рукавиць Superior Strength (навичка 300); добірки чарів для ближнього бою на 30 рівні поки немає, тому не пишемо.')])]},
                {'id': 'skill', 't': t('Навык профессий', 'Profession skill', 'Навичка професій'), 'blocks': [
                ('text', [t('Навык сборщиков качается в мире, а не в городе. Данные до навыка 225 (для Рыбалки до 300) из обзоров Wowhead Forever от 23–24 октября 2026; где лесенка не подтверждена, так и написано.', 'Skill for the gathering professions is raised in the world, not in a city. Data up to skill 225 (Fishing up to 300) from the Wowhead Forever overviews of Oct 23–24, 2026; where a ladder is not confirmed, it says so.', 'Навичка збирачів качається у світі, а не в місті. Дані до навички 225 (для Рибальства до 300) з оглядів Wowhead Forever від 23–24 жовтня 2026; де драбина не підтверджена, так і написано.')]),
                ('text', [t('Горное дело: до 185 навык растёт от плавки слитков, после 185 только от добычи в жилах. Одна жила даёт одно очко навыка. Нужна лишь кирка Mining Pick у торговцев хозтоварами; включите Find Minerals.', 'Mining: skill can be raised by smelting bars up to 185; past 185 only by mining nodes. One node gives one skill point. The only tool is a Mining Pick from Trade Goods vendors; turn on Find Minerals.', 'Гірництво: до 185 навичка росте від виплавки зливків, після 185 лише від видобутку в жилах. Одна жила дає одне очко навички. Потрібна лише кирка Mining Pick у торговців господарськими товарами; увімкніть Find Minerals.')]),
                ('table', {'head': [t('Навык', 'Skill', 'Навичка'), t('Слиток', 'Bar', 'Злиток'), t('Сколько', 'How many', 'Скільки'), t('Материалы', 'Materials', 'Матеріали')], 'rows': [
                ['1–65', 'Copper Bar', '130', '130 Copper Ore'],
                ['65–75', 'Tin Bar', '60', '60 Tin Ore'],
                ['75–100', 'Bronze Bar', '60', '60 Copper Bar, 60 Tin Bar'],
                ['100–125', 'Silver Bar', '70', '70 Silver Ore'],
                ['125–140', 'Iron Bar', '35', '35 Iron Ore'],
                ['140–155', t('Слитки навык не дают: копайте жилы', 'No bar gives skill here: mine nodes', 'Злитки навичку не дають: копайте жили'), '', ''],
                ['155–185', 'Gold Bar', '60', '60 Gold Ore']]}),
                ('table', {'head': [t('Навык', 'Skill', 'Навичка'), t('Жилы', 'Nodes', 'Жили'), t('Зоны', 'Zones', 'Зони')], 'rows': [
                ['1–65', 'Copper Vein', t('Любая стартовая зона', 'Any starting zone', 'Будь-яка стартова зона')],
                ['65–125', 'Copper Vein, Tin Vein, Silver Vein', 'Ashenvale, Redridge Mountains, The Barrens, Thousand Needles'],
                ['125–175', 'Tin Vein, Silver Vein, Iron Deposit, Gold Vein', 'Arathi Highlands, Desolace, Stranglethorn Vale, Thousand Needles'],
                ['175–225', 'Gold Vein, Mithril Deposit, Truesilver Deposit', 'Azshara, Tanaris, The Hinterlands']]}),
                ('text', [t('Оловянные жилы открываются с навыка 65, серебряные с 75, железные со 125, золотые со 155; олово перестаёт давать навык на 165, серебро на 175. Прибавки позволяют копать раньше: Miner’s Cape +2, Goblin Mining Helmet +5, Enchant Gloves - Mining +2, Enchant Gloves - Advanced Mining +5.', 'Tin Veins open at skill 65, Silver at 75, Iron at 125, Gold at 155; Tin stops giving skill at 165, Silver at 175. Boosts let you mine earlier: Miner’s Cape +2, Goblin Mining Helmet +5, Enchant Gloves - Mining +2, Enchant Gloves - Advanced Mining +5.', 'Олов’яні жили відкриваються з навички 65, срібні з 75, залізні зі 125, золоті зі 155; олово перестає давати навичку на 165, срібло на 175. Надбавки дозволяють копати раніше: Miner’s Cape +2, Goblin Mining Helmet +5, Enchant Gloves - Mining +2, Enchant Gloves - Advanced Mining +5.')]),
                ('text', [t('Травничеству инструменты не нужны: включите Find Herbs и идите к траве, на которую хватает навыка. Stranglekelp растёт только под водой, Wintersbite только в снегах Alterac Mountains. Earthroot появляется с навыка 15, Kingsblood со 125, Liferoot со 150, Khadgar’s Whisker со 185.', 'Herbalism needs no tools: turn on Find Herbs and go to a node you have the skill for. Stranglekelp grows only underwater, Wintersbite only in the snow of the Alterac Mountains. Earthroot appears from skill 15, Kingsblood from 125, Liferoot from 150, Khadgar’s Whisker from 185.', 'Травництву інструменти не потрібні: увімкніть Find Herbs і йдіть до трави, на яку вистачає навички. Stranglekelp росте лише під водою, Wintersbite лише в снігах Alterac Mountains. Earthroot з’являється з навички 15, Kingsblood зі 125, Liferoot зі 150, Khadgar’s Whisker зі 185.')]),
                ('table', {'head': [t('Навык', 'Skill', 'Навичка'), t('Травы', 'Herbs', 'Трави'), t('Зоны', 'Zones', 'Зони')], 'rows': [
                ['1–70', 'Peacebloom, Silverleaf, Earthroot', t('Любая стартовая зона', 'Any starting zone', 'Будь-яка стартова зона')],
                ['70–115', 'Mageroyal, Briarthorn, Stranglekelp', 'Darkshore, Loch Modan, Silverpine Forest'],
                ['115–170', 'Stranglekelp, Bruiseweed, Wild Steelbloom, Kingsblood, Liferoot', 'Hillsbrad Foothills, Wetlands, Stonetalon Mountains'],
                ['170–205', 'Kingsblood, Liferoot, Fadeleaf, Goldthorn, Khadgar’s Whisker', 'Stranglethorn Vale, Arathi Highlands'],
                ['205–225', 'Fadeleaf, Goldthorn, Khadgar’s Whisker, Wintersbite, Firebloom, Purple Lotus', 'Alterac Mountains, Tanaris, Searing Gorge']]}),
                ('text', [t('Снятие шкур: нужен нож Skinning Knife у торговцев хозтоварами и кожевенных поставщиков, надевать его не надо. Труп надо сначала обобрать; можно снимать шкуры с чужих жертв. Зверей в стартовых зонах тоже можно свежевать. В зонах ниже звери стоят гуще; если качаете персонажа по пути, просто идите в обычную следующую зону.', 'Skinning: you need a Skinning Knife from trade or Leatherworking vendors, no need to equip it. The corpse must be looted first, and you can skin mobs killed by other players. Beasts in starting zones can be skinned too. The zones below have dense beasts; if you level a character along the way, just go to the usual next zone.', 'Шкурництво: потрібен ніж Skinning Knife у торговців господарськими товарами й шкіряних постачальників, одягати його не треба. Труп треба спершу обшукати; можна знімати шкури з чужих жертв. Звірів у стартових зонах теж можна свежувати. У зонах нижче звірі стоять густіше; якщо качаєте персонажа дорогою, просто йдіть у звичайну наступну зону.')]),
                ('table', {'head': [t('Навык', 'Skill', 'Навичка'), t('Зоны', 'Zones', 'Зони')], 'rows': [
                ['1–75', t('Любая стартовая зона', 'Any starting zone', 'Будь-яка стартова зона')],
                ['75–125', 'The Barrens, Loch Modan, Darkshore'],
                ['125–175', 'Ashenvale, Duskwood, Hillsbrad Foothills, Wetlands'],
                ['175–225', 'Arathi Highlands, Stranglethorn Vale, Thousand Needles']]}),
                ('text', [t('Journeyman Skinning учит Thuwd в Orgrimmar (The Drag) на навыке 75. Expert Skinning учит Dranh в Camp Taurajo (The Barrens) до зон 125–175. Artisan Skinning можно выучить у учителя на навыке 200.', 'Journeyman Skinning is learned at 75 (Orgrimmar, The Drag: Thuwd). Expert Skinning is taught by Dranh in Camp Taurajo (The Barrens), before the 125–175 zones. Artisan Skinning can be learned from a trainer at skill 200.', 'Journeyman Skinning навчає Thuwd в Orgrimmar (The Drag) на навичці 75. Expert Skinning навчає Dranh у Camp Taurajo (The Barrens) до зон 125–175. Artisan Skinning можна вивчити в учителя на навичці 200.')]),
                ('text', [t('Навык Рыбалки зависит только от числа пойманных рыб, сложность зоны не важна. До навыка 25 используйте Shiny Bauble. Помогает удочка у торговцев рыболовным товаром: Strong Fishing Pole +5 (с навыка 10); Big Iron Fishing Pole +20 (с навыка 100, можно передавать).', 'Fishing skill depends only on the number of fish caught; the difficulty of the zone does not matter. Below skill 25 use a Shiny Bauble. A pole from fishing vendors helps: Strong Fishing Pole +5 (from skill 10); Big Iron Fishing Pole +20 (from skill 100, tradable).', 'Навичка Рибальства залежить лише від кількості впійманих риб, складність зони не важлива. До навички 25 використовуйте Shiny Bauble. Допомагає вудка в торговців рибальським краном: Strong Fishing Pole +5 (з навички 10); Big Iron Fishing Pole +20 (з навички 100, можна передавати).')]),
                ('table', {'head': [t('Навык', 'Skill', 'Навичка'), t('Зоны', 'Zones', 'Зони')], 'rows': [
                ['1–75', t('Любая стартовая зона', 'Any starting zone', 'Будь-яка стартова зона')],
                ['75–150', t('Столица: Darnassus, Ironforge или Stormwind City, Orgrimmar, Thunder Bluff или Undercity', 'A capital city: Darnassus, Ironforge or Stormwind City, Orgrimmar, Thunder Bluff or Undercity', 'Столиця: Darnassus, Ironforge або Stormwind City, Orgrimmar, Thunder Bluff або Undercity')],
                ['150–225', 'Dustwallow Marsh, Stranglethorn Vale'],
                ['225–300', 'Tanaris']]}),
                ('text', [t('Journeyman Fishing учат в столице на навыке 75. Expert открывает книга Expert Fishing - The Bass and You у Old Man Heming в Booty Bay. Artisan даёт задание в Dustwallow Marsh. В Dustwallow Marsh и Stranglethorn Vale улов гарантирован с 225, в Tanaris с 300: до этого берите наживку. Перк Legacy Luremaster даёт 25% шанса на лишнюю рыбу с наживкой.', 'Journeyman Fishing is learned in a capital at skill 75. Expert is taught by the book Expert Fishing - The Bass and You from Old Man Heming in Booty Bay. Artisan comes from a quest in Dustwallow Marsh. Dustwallow Marsh and Stranglethorn Vale give a 100% catch at 225, Tanaris at 300: use lures until then. The Luremaster Legacy perk gives a 25% chance of an extra fish with a lure.', 'Journeyman Fishing навчають у столиці на навичці 75. Expert відкриває книга Expert Fishing - The Bass and You в Old Man Heming у Booty Bay. Artisan дає завдання в Dustwallow Marsh. У Dustwallow Marsh і Stranglethorn Vale улов гарантований з 225, у Tanaris з 300: до цього беріть принаду. Перк Legacy Luremaster дає 25% шансу на зайву рибу з принадою.')]),
                ('text', [t('Алхимия: лесенка навыка от 1 до 225 пока не подтверждена, поэтому не выдумываем её (ждёт данных). Эликсиры и нужный для них навык есть во вкладке «Эликсиры и масла»; большую часть трав для них даёт Травничество.', 'Alchemy: a skill ladder from 1 to 225 is not confirmed yet, so we do not make one up (waiting for data). The elixirs and the skill they need are in the Elixirs and oils tab; most herbs for them come from Herbalism.', 'Алхімія: драбина навички від 1 до 225 поки не підтверджена, тому не вигадуємо її (чекає даних). Еліксири й потрібна для них навичка є у вкладці «Еліксири та олії»; більшість трав для них дає Травництво.')]),
                ('text', [t('Перки Legacy помогают любой профессии: Working Overtime (5 рангов) повышает шанс получить очко навыка на 4%; Dedicated Study поднимает вашу самую низкую основную или вторичную профессию на 1 (перезарядка 23 часа).', 'Legacy perks help every profession: Working Overtime (5 ranks) raises the chance of gaining a skill point by 4%; Dedicated Study raises your lowest primary or secondary profession by 1 (23 hour cooldown).', 'Перки Legacy допомагають будь-якій професії: Working Overtime (5 рангів) підвищує шанс отримати очко навички на 4%; Dedicated Study піднімає вашу найнижчу основну чи другорядну професію на 1 (перезарядка 23 години).')])]},
                {'id': 'gear', 't': t('Экипировка', 'Gear', 'Спорядження'), 'blocks': [('text', [t('По Wowhead, сделанная ремесленником экипировка в Forever заметно сильнее, чем в Classic, а многие новые схемы привязываются при получении: готовую вещь не купить на аукционе. Предметы из подземелий и наград за задания закрывают слабые места, особенно оружие. Поэтому пара профессий под ваш класс окупается с первых зон.', 'Per Wowhead, crafted gear in Forever is noticeably stronger than in Vanilla, and many new plans are bound when picked up, so the finished item cannot be bought at the auction house. Dungeon drops and quest rewards fill the weak spots, especially weapons. So a profession pair for your class pays off from the first zones.', 'За Wowhead, виготовлене ремісником спорядження у Forever помітно сильніше, ніж у Vanilla, а багато нових схем прив’язуються при отриманні: готову річ не купити на аукціоні. Предмети з підземель і нагороди за завдання закривають слабкі місця, особливо зброю. Тому пара професій під ваш клас окупається з перших зон.')]),
                ('text', [t('Пример для мага, Лёд, 30 уровень (Wowhead, 9 октября 2026): что падает в подземельях. Названия как в клиенте.', 'An example for a Frost mage at level 30 (Wowhead, Oct 9, 2026): what drops in dungeons. Names as in the client.', 'Приклад для мага, Крига, 30 рівень (Wowhead, 9 жовтня 2026): що падає в підземеллях. Назви як у клієнті.')]),
                ('table', {'head': [t('Подземелье', 'Dungeon', 'Підземелля'), t('Предмет', 'Item', 'Предмет')], 'rows': [
                ['Shadowfang Keep', 'Sorcerer Collar, Blade of Silverlaine, Feline Mantle, Belt of Arugal'],
                ['The Stockade', 'Dark Horde Band'],
                ['Blackfathom Deeps', 'Gaze Dreamer Pants, Leech Pants, Ghamoo-ra’s Bind'],
                ['Excavation Site: Wetlands', 'Raptor’s Gaze, Glinteye Slippers'],
                ['Razorfen Kraul', 'Thornweaver Drape, Death Speaker Mantle, Agamaggan’s Clutch, Vicar’s Robe'],
                ['Gnomeregan', 'Acidic Walkers, Spidertank Oilrag'],
                ['Scarlet Monastery: Graveyard', 'Bloodmage Mantle']]}),
                ('text', [t('Комплекты Silky и Azure Silk усиливают только урон Льда, и носить их может лишь сам портной. Предметы других спеков мы добавим поимённо после проверки в игре.', 'The Silky and Azure Silk pieces boost only Frost damage, and only the tailor who made them can wear them. We will add the items of other specs by name after checking in the game.', 'Комплекти Silky та Azure Silk підсилюють лише шкоду Криги, і носити їх може лише сам кравець. Предмети інших спеків ми додамо поіменно після перевірки в грі.')])]}]),
            ('tip', t('Кулинарию и Первую помощь стоит взять каждому: основные места они не занимают, а учителя стоят в столицах и городках у стартовых зон. Всё до 30 уровня сверено с бетой, остальное сверим после старта.', 'Everyone should take Cooking and First Aid: they use no primary slots, and trainers stand in capitals and in towns near the starting zones. Everything up to level 30 is checked against the beta; the rest we will check after launch.', 'Кулінарію та Першу допомогу варто взяти кожному: основні слоти вони не займають, а вчителі стоять у столицях і містечках біля стартових зон. Усе до 30 рівня звірено з бетою, решту звіримо після старту.')),
        ]}

GUIDES.append({
    'slug': 'leveling', 'art': 'hero_leveling', 'hero': 'hero_leveling',
    'title': t('Прокачка 1–60', 'Leveling 1–60', 'Прокачування 1–60'),
    'lead': t('Как дойти с 1 до 60 уровня: куда идти на каждом отрезке за Альянс и Орду, как копить отдых и когда качаться группой. Плюс Legacy и лагерь.',
              'How to get from level 1 to 60: where to go at each level range for Alliance and Horde, how to save up rest and when to level in a group. Plus Legacy and the camp.',
              'Як дійти з 1 до 60 рівня: куди йти на кожному відрізку за Альянс і Орду, як накопичувати відпочинок і коли качатися групою. Плюс Legacy і табір.'),
    'tile': t('Зоны по уровням, отдых, Legacy и лагерь', 'Zones by level, rest, Legacy and the camp', 'Зони за рівнями, відпочинок, Legacy і табір'),
    'pills': [t('Альянс и Орда', 'Alliance and Horde', 'Альянс і Орда'), t('Ездовое с 40', 'Mount at 40', 'Їздова тварина з 40'),
              t('4 084 700 опыта до 60', '4,084,700 XP to 60', '4 084 700 досвіду до 60')],
    'sources': [
        (t('Mobalytics: зоны по уровням и маршруты', 'Mobalytics: zones by level and routes', 'Mobalytics: зони за рівнями та маршрути'),
         'https://mobalytics.gg/wow-forever/guides/zone-map-level-ranges'),
        (t('Icy Veins: новые зоны', 'Icy Veins: new zones', 'Icy Veins: нові зони'), 'https://www.icy-veins.com/wow-forever/zones-and-maps'),
        (t('Warcraft Tavern: опыт и отдых', 'Warcraft Tavern: experience and rested XP', 'Warcraft Tavern: досвід і відпочинок'),
         'https://www.warcrafttavern.com/forever/guides/experience/'),
        (t('Warcraft Tavern: верховая езда', 'Warcraft Tavern: riding', 'Warcraft Tavern: верхова їзда'), 'https://www.warcrafttavern.com/forever/guides/riding/'),
        (t('Blizzard: Legacy', 'Blizzard: Legacy', 'Blizzard: Legacy'), 'https://news.blizzard.com/en-gb/article/24307383'),
        (t('Warcraft Tavern: Legacy', 'Warcraft Tavern: Legacy', 'Warcraft Tavern: Legacy'), 'https://www.warcrafttavern.com/forever/guides/legacy/'),
        (t('Warcraft Tavern: лагерь', 'Warcraft Tavern: camping', 'Warcraft Tavern: табір'), 'https://www.warcrafttavern.com/forever/guides/camping/'),
        (t('Wowhead: Кулинария (обновлено 24.10.2026)', 'Wowhead: Cooking (updated Oct 24, 2026)', 'Wowhead: Кулінарія (оновлено 24.10.2026)'), 'https://www.wowhead.com/forever/guide/professions/cooking/overview-leveling'),
        (t('Wowhead: Первая помощь (обновлено 23.10.2026)', 'Wowhead: First Aid (updated Oct 23, 2026)', 'Wowhead: Перша допомога (оновлено 23.10.2026)'), 'https://www.wowhead.com/forever/guide/professions/first-aid/overview'),
        (t('Wowhead: Горное дело (обновлено 23.10.2026)', 'Wowhead: Mining (updated Oct 23, 2026)', 'Wowhead: Гірництво (оновлено 23.10.2026)'), 'https://www.wowhead.com/forever/guide/professions/mining/overview-leveling'),
        (t('Wowhead: Травничество (обновлено 24.10.2026)', 'Wowhead: Herbalism (updated Oct 24, 2026)', 'Wowhead: Травництво (оновлено 24.10.2026)'), 'https://www.wowhead.com/forever/guide/professions/herbalism/overview-leveling'),
        (t('Wowhead: Снятие шкур (обновлено 24.10.2026)', 'Wowhead: Skinning (updated Oct 24, 2026)', 'Wowhead: Шкурництво (оновлено 24.10.2026)'), 'https://www.wowhead.com/forever/guide/professions/skinning/overview-leveling'),
        (t('Wowhead: Рыбалка (обновлено 24.10.2026)', 'Wowhead: Fishing (updated Oct 24, 2026)', 'Wowhead: Рибальство (оновлено 24.10.2026)'), 'https://www.wowhead.com/forever/guide/professions/fishing/overview-leveling'),
        (t('Wowhead: Алхимия (обновлено 24.10.2026)', 'Wowhead: Alchemy (updated Oct 24, 2026)', 'Wowhead: Алхімія (оновлено 24.10.2026)'), 'https://www.wowhead.com/forever/guide/professions/alchemy-overview-trainer-locations-recipes'),
        (t('Wowhead: чары на 30 уровне, составлено по данным беты 14.10.2026', 'Wowhead: level 30 enchant options, from beta data of Oct 14, 2026', 'Wowhead: чари на 30 рівні за даними бети від 14.10.2026'), 'https://www.wowhead.com/forever/guide/level-30-warlock-enchant-options-in-wow-forever-35073'),
        (t('Wowhead: Лёд, маг, 30 уровень (обновлено 09.10.2026)', 'Wowhead: Frost Mage, level 30 (updated Oct 9, 2026)', 'Wowhead: Крига, маг, 30 рівень (оновлено 09.10.2026)'), 'https://www.wowhead.com/forever/guide/classes/mage/frost/level-30-dps-overview'),
        (t('Wowhead: профессии по классам (обновлено 20.10.2026)', 'Wowhead: profession pairings by class (updated Oct 20, 2026)', 'Wowhead: професії за класами (оновлено 20.10.2026)'), 'https://www.wowhead.com/forever/guide/wow-forever-profession-pairings-by-class-35082'),
    ],
    'sections': [
        {'id': 'first', 'title': t('Первый час', 'First hour', 'Перша година'), 'blocks': [
            ('steps', [
                {'t': t('До старта', 'Before launch', 'До старту'),
                 'd': t('Решите с друзьями регион, режим и фракцию: группа собирается только внутри режима, регионы разделены. Владельцы наборов занимают имена с 27.10.',
                        'Agree on region, mode and faction with your friends: groups form only within a mode, and regions are separate. Pack owners can claim names from 27.10.',
                        'Вирішіть із друзями регіон, режим і фракцію: група збирається лише всередині режиму, регіони розділені. Власники наборів займають імена з 27.10.')},
                {'t': t('Старт', 'Launch', 'Старт'),
                 'd': t('В Европе 05.11, в Америке 04.11. Старт в 15:00 по тихоокеанскому, это 23:00 UTC.', '04.11 in the Americas, 05.11 in Europe. Launch is at 15:00 Pacific, which is 23:00 UTC.', 'У Європі 05.11, в Америці 04.11. Старт о 15:00 за тихоокеанським, це 23:00 UTC.')},
                {'t': t('Стартовая зона', 'Starting zone', 'Стартова зона'),
                 'd': t('Задания стартовой зоны своей расы до 10 уровня, дальше — маршрут ниже. Таланты открываются на 10 уровне.',
                        'Your race’s starting zone quests up to level 10, then the route below. Talents unlock at level 10.',
                        'Завдання стартової зони своєї раси до 10 рівня, далі — маршрут нижче. Таланти відкриваються на 10 рівні.')},
                {'t': t('Кулинария сразу', 'Cooking right away', 'Кулінарія одразу'),
                 'd': t('Костёр по Кулинарии становится лагерем: по Warcraft Tavern 140 навыка дают 5 мест, 220 — 10 (по Icy Veins 90 и 200, уточним на старте). Готовая еда даёт +5% опыта за врагов.',
                        'A Cooking campfire becomes a camp: per Warcraft Tavern, 140 skill gives 5 slots and 220 gives 10 (per Icy Veins 90 and 200; we’ll confirm at launch). Cooked food gives +5% experience from enemies.',
                        'Вогнище з Кулінарії стає табором: за Warcraft Tavern 140 навички дають 5 місць, 220 — 10 (за Icy Veins 90 і 200, уточнимо на старті). Готова їжа дає +5% досвіду за ворогів.')},
                {'t': t('Две профессии', 'Two professions', 'Дві професії'),
                 'd': t('Травничество, Горное дело и Снятие шкур кормят деньгами и ставят свои объекты в лагере. Пары под класс — в гайде по профессиям.',
                        'Herbalism, Mining and Skinning bring in money and place their own camp objects. Pairs for your class are in the professions guide.',
                        'Травництво, Гірництво та Знімання шкур дають гроші й ставлять свої об’єкти в таборі. Пари під клас — у гайді з професій.')},
                {'t': t('Выход из игры', 'Logging out', 'Вихід із гри'),
                 'd': t('В таверне или столице: копится отдых, и следующий вечер начнётся с двойного опыта за врагов.',
                        'In an inn or a capital: rest builds up, and the next evening starts with double experience from enemies.',
                        'У таверні чи столиці: накопичується відпочинок, і наступний вечір почнеться з подвійного досвіду за ворогів.')},
            ]),
        ]},
        {'id': 'route', 'title': t('Маршрут по зонам', 'Zone route', 'Маршрут зонами'), 'blocks': [
            ('play', {'h': t('Играете прямо сейчас?', 'Playing right now?', 'Граєте просто зараз?'),
                      'd': t('Откройте «В игре» на телефоне или втором мониторе: зоны под ваш уровень, подземелья, таймеры и радио.',
                             'Open “In game” on your phone or a second monitor: zones for your level, dungeons, timers and radio.',
                             'Відкрийте «У грі» на телефоні або другому моніторі: зони під ваш рівень, підземелля, таймери й радіо.'),
                      'go': t('Открыть «В игре»', 'Open “In game”', 'Відкрити «У грі»')}),
            ('text', [t('Диапазоны уровней по карте Mobalytics, новые зоны сверены с Icy Veins. Это ориентир для беты: Blizzard может сдвинуть уровни к релизу. Масштабирования нет, у каждой зоны свои уровни.',
                        'Level ranges are from the Mobalytics map, new zones checked against Icy Veins. This is a beta guideline: Blizzard may shift levels by release. There is no level scaling, each zone has its own levels.',
                        'Діапазони рівнів за мапою Mobalytics, нові зони звірені з Icy Veins. Це орієнтир для бети: Blizzard може зсунути рівні до релізу. Масштабування немає, кожна зона має свої рівні.')]),
            ('tabs', [
                {'id': 'alliance', 't': t('Альянс', 'Alliance', 'Альянс'), 'blocks': [
                    ('steps', [
                        {'t': '1–10', 'd': t('Люди: Elwynn Forest. Дворфы и гномы: Dun Morogh. Ночные эльфы: Teldrassil, до 11. Высшие скайборны: Zephras Isle, до 12.',
                                             'Human: Elwynn Forest. Dwarf and Gnome: Dun Morogh. Night Elf: Teldrassil (to 11). High Order Skyborne: Zephras Isle (to 12).',
                                             'Human: Elwynn Forest. Dwarf і Gnome: Dun Morogh. Night Elf: Teldrassil (до 11). High Order Skyborne: Zephras Isle (до 12).')},
                        {'t': '10–18', 'd': t('Westfall или Loch Modan, ночные эльфы обычно в [[Темных берегах|Darkshore]]. С 15 подходит Redridge Mountains.',
                                              'Westfall or Loch Modan, Night Elves usually go to Darkshore. From 15, Redridge Mountains fit.',
                                              'Westfall або Loch Modan, нічні ельфи зазвичай у Darkshore. З 15 підходять Redridge Mountains.')},
                        {'t': '18–30', 'd': t('Duskwood, Redridge Mountains и Wetlands, в [[Калимдоре|Kalimdor]] Stonetalon Mountains и Ashenvale.',
                                              'Duskwood, Redridge Mountains and Wetlands; in Kalimdor, Stonetalon Mountains and Ashenvale.',
                                              'Duskwood, Redridge Mountains і Wetlands, у Kalimdor Stonetalon Mountains і Ashenvale.')},
                        {'t': '30–45', 'd': t('Desolace или Arathi Highlands, Stranglethorn Vale. С 35: новая зона Riverglades между [[Красногорьем|Redridge Mountains]] и [[Пылающими степями|Burning Steppes]], Dustwallow Marsh, Badlands, Swamp of Sorrows.',
                                              'Desolace or Arathi Highlands, Stranglethorn Vale. From 35: the new Riverglades zone between Redridge and Burning Steppes, Dustwallow Marsh, Badlands, Swamp of Sorrows.',
                                              'Desolace або Arathi Highlands, Stranglethorn Vale. З 35: нова зона Riverglades між Redridge і Burning Steppes, Dustwallow Marsh, Badlands, Swamp of Sorrows.')},
                        {'t': '40–55', 'd': t('Tanaris, Feralas, The Hinterlands, затем Searing Gorge, Blasted Lands, Azshara, с 48 [[Кратер Ун’Горо|Un’Goro Crater]] и Felwood.',
                                              'Tanaris, Feralas, The Hinterlands, then Searing Gorge, Blasted Lands, Azshara, from 48 Un’Goro Crater and Felwood.',
                                              'Tanaris, Feralas, The Hinterlands, далі Searing Gorge, Blasted Lands, Azshara, з 48 Un’Goro Crater і Felwood.')},
                        {'t': '50–60', 'd': t('Burning Steppes, Western Plaguelands, Eastern Plaguelands, Winterspring, Silithus. На 60 открыта Mount Hyjal.',
                                              'Burning Steppes, Western and Eastern Plaguelands, Winterspring, Silithus. Mount Hyjal opens at 60.',
                                              'Burning Steppes, Western і Eastern Plaguelands, Winterspring, Silithus. На 60 відкритий Mount Hyjal.')},
                    ]),
                ]},
                {'id': 'horde', 't': t('Орда', 'Horde', 'Орда'), 'blocks': [
                    ('steps', [
                        {'t': '1–10', 'd': t('Орки и тролли: Durotar. Таурены: Mulgore. Нежить: Tirisfal Glades. Скайборны-ветрорезы: Zephras Isle, до 12.',
                                             'Orc and Troll: Durotar. Tauren: Mulgore. Undead: Tirisfal Glades. Windshaper Skyborne: Zephras Isle (to 12).',
                                             'Orc і Troll: Durotar. Tauren: Mulgore. Undead: Tirisfal Glades. Windshaper Skyborne: Zephras Isle (до 12).')},
                        {'t': '10–18', 'd': t('The Barrens или Silverpine Forest.', 'The Barrens or Silverpine Forest.', 'The Barrens або Silverpine Forest.')},
                        {'t': '18–30', 'd': t('Stonetalon Mountains и The Barrens, затем Ashenvale или Hillsbrad Foothills, с 25 Thousand Needles.',
                                              'Stonetalon Mountains and The Barrens, then Ashenvale or Hillsbrad Foothills, from 25 Thousand Needles.',
                                              'Stonetalon Mountains і The Barrens, далі Ashenvale або Hillsbrad Foothills, з 25 Thousand Needles.')},
                        {'t': '30–45', 'd': t('Desolace или Arathi Highlands, Stranglethorn Vale. С 35: новая зона Riverglades, Dustwallow Marsh, Badlands, Swamp of Sorrows.',
                                              'Desolace or Arathi Highlands, Stranglethorn Vale. From 35: the new Riverglades zone, Dustwallow Marsh, Badlands, Swamp of Sorrows.',
                                              'Desolace або Arathi Highlands, Stranglethorn Vale. З 35: нова зона Riverglades, Dustwallow Marsh, Badlands, Swamp of Sorrows.')},
                        {'t': '40–55', 'd': t('Tanaris, Feralas, The Hinterlands, затем Searing Gorge, Blasted Lands, Azshara, с 48 [[Кратер Ун’Горо|Un’Goro Crater]] и Felwood.',
                                              'Tanaris, Feralas, The Hinterlands, then Searing Gorge, Blasted Lands, Azshara, from 48 Un’Goro Crater and Felwood.',
                                              'Tanaris, Feralas, The Hinterlands, далі Searing Gorge, Blasted Lands, Azshara, з 48 Un’Goro Crater і Felwood.')},
                        {'t': '50–60', 'd': t('Burning Steppes, Western Plaguelands, Eastern Plaguelands, Winterspring, Silithus. На 60 открыта Mount Hyjal.',
                                              'Burning Steppes, Western and Eastern Plaguelands, Winterspring, Silithus. Mount Hyjal opens at 60.',
                                              'Burning Steppes, Western і Eastern Plaguelands, Winterspring, Silithus. На 60 відкритий Mount Hyjal.')},
                    ]),
                ]},
            ]),
            ('tip', t('Новая зона Shen’Dralas лежит между [[Пустошами|Desolace]] и [[Фераласом|Feralas]], в ней задания для [[Мародона|Maraudon]] и [[Курганов Иглошкурых|Razorfen Downs]]. Уровень зоны источники пока не называют.',
                      'The new Shen’Dralas zone lies between Desolace and Feralas and has quests for Maraudon and Razorfen Downs. Sources do not give its level yet.',
                      'Нова зона Shen’Dralas лежить між Desolace і Feralas, у ній завдання для Maraudon і Razorfen Downs. Рівень зони джерела поки не називають.')),
            ('tiles', [{'t': t('Аддоны и интерфейс', 'Addons and Interface', 'Аддони та інтерфейс'), 'd': t('Questie, RestedXP и карта для прокачки', 'Questie, RestedXP and maps for leveling', 'Questie, RestedXP і мапа для прокачування'), 'href': 'guides/addons/', 'art': 'hero_roster'}]),
        ]},
        {'id': 'pace', 'title': t('Темп и отдых', 'Pace and rest', 'Темп і відпочинок'), 'blocks': [
            ('steps', [
                {'t': t('Сколько опыта', 'How much experience', 'Скільки досвіду'),
                 'd': t('До 60 уровня нужно 4 084 700 опыта: 499 000 до 30 и 2 306 100 до 50.',
                        'Reaching level 60 takes 4,084,700 experience: 499,000 to 30 and 2,306,100 to 50.',
                        'До 60 рівня потрібно 4 084 700 досвіду: 499 000 до 30 і 2 306 100 до 50.')},
                {'t': t('Отдых', 'Rested XP', 'Відпочинок'),
                 'd': t('Отдых удваивает опыт за врагов, на задания он не действует. В таверне или столице копится 5% уровня за 8 часов, потолок 150% (около 10 дней вне игры).',
                        'Rested XP doubles experience from enemies and does not affect quests. In an inn or capital it builds 5% of a level per 8 hours, capped at 150% (about 10 days offline).',
                        'Відпочинок подвоює досвід за ворогів, на завдання він не діє. У таверні чи столиці накопичується 5% рівня за 8 годин, стеля 150% (близько 10 днів поза грою).')},
                {'t': t('Еда и спальник', 'Food and bedroll', 'Їжа і спальник'),
                 'd': t('Большая часть готовой еды даёт +5% опыта за врагов примерно на 15 минут. Cozy Sleeping Bag даёт до 3% и не пропадает после смерти, а лёжа на нём копится отдых даже вне игры.',
                        'Most cooked food gives +5% experience from enemies for about 15 minutes. The Cozy Sleeping Bag gives up to 3% and stays after death, and lying on it builds rest even while offline.',
                        'Більша частина готової їжі дає +5% досвіду за ворогів приблизно на 15 хвилин. Cozy Sleeping Bag дає до 3% і не зникає після смерті, а лежачи на ньому накопичується відпочинок навіть поза грою.')},
                {'t': t('Задания по уровню', 'Quests at your level', 'Завдання за рівнем'),
                 'd': t('Задания на 5 и больше уровней ниже теряют по 10–20% опыта за каждый лишний уровень, серые враги опыта не дают.',
                        'Quests 5 or more levels below you lose 10–20% experience per extra level, grey enemies give no experience.',
                        'Завдання на 5 і більше рівнів нижче втрачають по 10–20% досвіду за кожен зайвий рівень, сірі вороги досвіду не дають.')},
                {'t': t('Ездовое животное', 'Riding', 'Їздова тварина'),
                 'd': t('С 40 уровня: обучение 100 золотых и скакун 20 (скорость +60%). На 60: 1000 и 200 золотых (+100%). При Почёте у своей фракции скидка 10%. Паладин и Чернокнижник получают скакуна заданиями класса.',
                        'From level 40: training 100 gold and a mount 20 (+60% speed). At 60: 1,000 and 200 gold (+100%). Honored with your faction gives 10% off. Paladins and Warlocks get their mount through class quests.',
                        'З 40 рівня: навчання 100 золотих і скакун 20 (швидкість +60%). На 60: 1000 і 200 золотих (+100%). На Honored зі своєю фракцією знижка 10%. Паладин і Чорнокнижник отримують скакуна завданнями класу.')},
            ]),
            ('tip', t('Выходите из игры в таверне, столице или на спальнике: следующий вечер начнётся с двойного опыта за врагов. Еда, спальник и отдых складываются.',
                      'Log out in an inn, a capital or on the bedroll: the next evening starts with double experience from enemies. Food, the bedroll and rest stack.',
                      'Виходьте з гри в таверні, столиці або на спальнику: наступний вечір почнеться з подвійного досвіду за ворогів. Їжа, спальник і відпочинок складаються.')),
        ]},
        KIT,
        {'id': 'group', 'title': t('Соло, вдвоём или группой', 'Solo, duo or group', 'Соло, удвох чи групою'), 'blocks': [
            ('tabs', [
                {'id': 'solo', 't': t('Соло', 'Solo', 'Соло'), 'blocks': [
                    ('text', [t('Основа прокачки — задания: их опыт не зависит от группы. Отдых работает только на врагов, поэтому начинайте вечер с убийств, пока он есть.',
                                'Quests are the core of leveling: their experience does not depend on a group. Rest only works on enemies, so start the evening with kills while you have it.',
                                'Основа прокачування — завдання: їхній досвід не залежить від групи. Відпочинок працює лише на ворогів, тому починайте вечір із вбивств, поки він є.')]),
                    ('tip', t('Легче всего соло Охотнику и Чернокнижнику, у них питомец держит врага.',
                              'Hunters and Warlocks have the easiest time solo, their pet holds the enemy.',
                              'Найлегше соло Мисливцю й Чорнокнижнику, у них вихованець тримає ворога.')),
                ]},
                {'id': 'duo', 't': t('Вдвоём', 'Duo', 'Удвох'), 'blocks': [
                    ('text', [t('За сданное задание каждый получает полный опыт, а опыт за врагов делится. Держите уровни рядом: в Forever у игрока выше уровнем штраф к опыту в группе больше, а «протаскивать» друга Blizzard сделала невыгодным.',
                                'Each player gets full experience for a quest turn-in, while experience from enemies is shared. Keep your levels close: in Forever a higher-level group member gets a bigger experience penalty, and Blizzard made boosting a friend unprofitable.',
                                'За здане завдання кожен отримує повний досвід, а досвід за ворогів ділиться. Тримайте рівні поруч: у Forever у гравця з вищим рівнем штраф до досвіду в групі більший, а «протягувати» друга Blizzard зробила невигідним.')]),
                    ('tip', t('Берите задания вместе и сдавайте одновременно. Если один ушёл вперёд, пусть отстающий доберёт уровень соло.',
                              'Pick up quests together and turn them in at the same time. If one of you gets ahead, let the other catch up solo.',
                              'Беріть завдання разом і здавайте одночасно. Якщо один пішов уперед, нехай відсталий добере рівень соло.')),
                ]},
                {'id': 'party', 't': t('Группой', 'Group', 'Групою'), 'blocks': [
                    ('text', [t('Чем больше группа, тем меньше опыта за врага достаётся каждому, а задания по-прежнему дают полный опыт. Большой группой выгодно ходить в подземелья и на элитные задания, а между ними разбиваться на пары.',
                                'The bigger the group, the less experience each member gets per enemy, while quests still give full experience. A big group pays off in dungeons and on elite quests, and between them you can split into pairs.',
                                'Що більша група, то менше досвіду за ворога дістається кожному, а завдання й далі дають повний досвід. Великою групою вигідно ходити в підземелля та на елітні завдання, а між ними розбиватися на пари.')]),
                    ('tiles', [{'t': t('Подземелья и рейды', 'Dungeons and raids', 'Підземелля та рейди'),
                                'd': t('Какое подземелье под ваш уровень и кого взять в группу', 'Which dungeon fits your level and who to bring',
                                       'Яке підземелля під ваш рівень і кого взяти в групу'),
                                'href': 'guides/dungeons/', 'art': 'hero_dungeons'}]),
                ]},
            ]),
            ('tiles', [{'t': t('Тир-лист классов WoW Forever', 'WoW Forever Class Tier List', 'Тір-лист класів WoW Forever'), 'd': TL.tile(TL_STATUS), 'href': 'guides/tier-list/', 'art': 'hero_tierlist'}]),
        ]},
        {'id': 'legacy', 'title': t('Система Legacy', 'Legacy system', 'Система Legacy'), 'blocks': [
            ('text', [t('Legacy — прогресс на весь аккаунт Battle.net. Очки дают за испытания: уровни, профессии, PvP, подземелья и рейды. Тратите их на перки отдельно на каждом персонаже, на старте до 16 очков.', 'Legacy is progress shared across your whole Battle.net account. Challenges give you points: levels, professions, PvP, dungeons and raids. You spend them on perks separately on each character, up to 16 points at launch.', 'Legacy — прогрес на весь обліковий запис Battle.net. Очки дають за випробування: рівні, професії, PvP, підземелля та рейди. Витрачаєте їх на перки окремо на кожному персонажі, на старті до 16.')]),
            ('tiles', [{'t': t('Система Legacy', 'The Legacy System', 'Система Legacy'), 'd': t('Очки, испытания, перки и награды', 'Points, challenges, perks and rewards', 'Очки, випробування, перки та нагороди'), 'href': 'guides/legacy/', 'art': 'hero_guides'}]),
        ]},
        {'id': 'camp', 'title': t('Лагерь и профессии', 'Camp and professions', 'Табір і професії'), 'blocks': [
            ('text', [t('Костёр по профессии Кулинария превращается в общий лагерь: рядом можно отдыхать, получать баффы и ставить объекты своих профессий.',
                        'A campfire made with the Cooking profession becomes a shared camp: you can rest nearby, get buffs and place objects of your professions.',
                        'Вогнище за професією Кулінарія перетворюється на спільний табір: поруч можна відпочивати, отримувати баффи та ставити об’єкти своїх професій.')]),
            ('steps', [
                {'t': t('Костёр', 'Campfire', 'Вогнище'),
                 'd': t('Костёр одноразовый: строится несколько секунд, горит около 10 минут, откат на постановку 5 минут.',
                        'The campfire is single-use: it takes a few seconds to build, burns for about 10 minutes, with a 5 minute cooldown to place.',
                        'Вогнище одноразове: будується кілька секунд, горить близько 10 хвилин, відновлення на встановлення 5 хвилин.')},
                {'t': t('Места', 'Slots', 'Місця'),
                 'd': t('Для базового костра на 3 объекта нужна выученная Кулинария, прокачивать навык не обязательно. По Warcraft Tavern Кулинария 140 даёт 5 мест, 220 — 10 (по Icy Veins 90 и 200, уточним на старте).',
                        'A basic campfire with 3 objects needs the Cooking profession learned, but you don’t have to level the skill. Per Warcraft Tavern, Cooking 140 gives 5 slots and 220 gives 10 (per Icy Veins 90 and 200; we’ll confirm at launch).',
                        'Для базового вогнища на 3 об’єкти потрібна вивчена Кулінарія, прокачувати навичку не обов’язково. За Warcraft Tavern Кулінарія 140 дає 5 слотів, 220 дає 10 (за Icy Veins 90 і 200, уточнимо на старті).')},
                {'t': t('Общий лагерь', 'Shared camp', 'Спільний табір'),
                 'd': t('Каждый персонаж ставит один объект, откат на объект 1 час. Вместе делают общий лагерь.',
                        'Each character places one object, with a 1 hour cooldown per object. Together you make a shared camp.',
                        'Кожен персонаж ставить один об’єкт, відновлення на об’єкт 1 година. Разом роблять спільний табір.')},
                {'t': t('Баффы', 'Buffs', 'Баффи'),
                 'd': t('Чтобы получить баффы, сядьте (/sit) рядом минимум на 1 минуту. Они суммируются в один бафф «Camp Benefits». Баффы лагеря немного слабее классовых и не складываются с ними.',
                        'To get the buffs, sit (/sit) nearby for at least 1 minute. They stack into one buff, “Camp Benefits”. Camp buffs are slightly weaker than class buffs and do not stack with them.',
                        'Щоб отримати баффи, сядьте (/sit) поруч щонайменше на 1 хвилину. Вони підсумовуються в один бафф «Camp Benefits». Баффи табору трохи слабші за класові й не складаються з ними.')},
            ]),
            ('table', {'head': [t('Профессия', 'Profession', 'Професія'), t('Объект (1 уровень)', 'Object (level 1)', 'Об’єкт (1 рівень)'), t('Эффект', 'Effect', 'Ефект')], 'rows': [
                [t('Алхимия', 'Alchemy', 'Алхімія'), 'Mana Well', t('больше восстановление маны', 'more mana regeneration', 'більше відновлення мани')],
                [t('Кузнечное дело', 'Blacksmithing', 'Ковальство'), 'Sharpening Wheel', t('больше силы', 'more strength', 'більше сили')],
                [t('Наложение чар', 'Enchanting', 'Зачарування'), 'Enchanted Lute', t('больше основных характеристик и сопротивлений', 'more primary stats and resistances', 'більше основних характеристик і опорів')],
                [t('Первая помощь', 'First Aid', 'Перша допомога'), 'First Aid Kit', t('больше выносливости', 'more stamina', 'більше витривалості')],
                [t('Рыбалка', 'Fishing', 'Рибальство'), 'Fish Bowl', t('больше основных характеристик', 'more primary stats', 'більше основних характеристик')],
                [t('Травничество', 'Herbalism', 'Травництво'), 'Incense Candle', t('больше интеллекта', 'more intellect', 'більше інтелекту')],
                [t('Кожевничество', 'Leatherworking', 'Шкіряництво'), 'Camp Tent', t('отдых и опыт (Boosted Rest)', 'rest and experience (Boosted Rest)', 'відпочинок і досвід (Boosted Rest)')],
                [t('Горное дело', 'Mining', 'Гірництво'), 'Lodestone', t('больше силы атаки', 'more attack power', 'більше сили атаки')],
                [t('Снятие шкур', 'Skinning', 'Знімання шкур'), 'Camp Chair', t('больше шанс критического удара', 'higher critical strike chance', 'більший шанс критичного удару')],
                [t('Портняжное дело', 'Tailoring', 'Кравецтво'), 'Faction Banner', t('больше духа', 'more spirit', 'більше духу')],
                [t('Инженерное дело', 'Engineering', 'Інженерія'), 'Reagent Bot', t('торговец, на 2 уровне ремонт (Repair Bot)', 'a vendor, at level 2 repairs (Repair Bot)', 'торговець, на 2 рівні ремонт (Repair Bot)')],
                [t('Кулинария', 'Cooking', 'Кулінарія'), 'Basic Campfire', t('без баффа, добавляет места в лагере', 'no buff, adds camp slots', 'без баффа, додає слоти табору')],
            ]}),
            ('text', [t('Каждая профессия делает по три объекта, по одному на уровень. По Icy Veins навык для объектов 1, 2 и 3 уровня — 20, 140 и 300 (другие источники расходятся), поэтому сверяйте в игре.',
                        'Each profession makes three objects, one per level. Per Icy Veins the skill for level 1, 2 and 3 objects is 20, 140 and 300 (other sources differ), so check in the game.',
                        'Кожна професія робить по три об’єкти, по одному на рівень. За Icy Veins навичка для об’єктів 1, 2 і 3 рівня — 20, 140 і 300 (інші джерела розходяться), тому звіряйте в грі.')]),
            ('tip', t('Палатка Camp Tent от кожевника даёт отдых, как в таверне, на час и не пропадает после смерти. Перки Legacy Field Guide, Permanence и Reagent Economy улучшают лагерь.',
                      'The leatherworker’s Camp Tent gives rest like an inn for an hour and stays after death. The Legacy perks Field Guide, Permanence and Reagent Economy improve the camp.',
                      'Намет Camp Tent від шкіряника дає відпочинок, як у таверні, на годину й не зникає після смерті. Перки Legacy Field Guide, Permanence і Reagent Economy покращують табір.')),
        ]},
    ],
})

# ---------- Профессии ----------

# Пары по Warcraft Tavern, Icy Veins и Gfinity (25.10.2026): прокачка и 60 уровень. Пары для 60 уровня — прогноз гайдов по бете, на старте их никто не проверил
PAIR_HEAD = [t('Класс', 'Class', 'Клас'), t('Прокачка', 'Leveling', 'Прокачування'), t('60 уровень', 'Level 60', '60 рівень'), t('Почему', 'Why', 'Чому')]   # Класс · Прокачка · 60 уровень · Почему

CLASS_PAIRS = [   # (id, имя класса, прокачка, 60 уровень, почему); пара = (текст, профессии для объектов лагеря)
    ('warrior', t('Воин', 'Warrior', 'Воїн'),
     (t('Кузнечное дело + Горное дело', 'Blacksmithing + Mining', 'Ковальство + Гірництво'), ('blacksmithing', 'mining')),
     (t('Инженерное дело + Горное дело', 'Engineering + Mining', 'Інженерія + Гірництво'), ('engineering', 'mining')),
     t('Кузнец одевает себя в латы и оружие, многие рецепты персональные. Инженеру — гранаты и устройства, которых воину не хватает.', 'A blacksmith dresses in plate and weapons, and many recipes are personal. An engineer gets the grenades and devices a warrior lacks.', 'Коваль одягає себе в лати й зброю, багато рецептів персональні. Інженеру — гранати й пристрої, яких воїну бракує.')),
    ('paladin', t('Паладин', 'Paladin', 'Паладин'),
     (t('Кузнечное дело + Горное дело', 'Blacksmithing + Mining', 'Ковальство + Гірництво'), ('blacksmithing', 'mining')),
     (t('Защита, Воздаяние: Инженерное дело + Горное дело. Свет: Алхимия + Травничество', 'Protection, Retribution: Engineering + Mining. Holy: Alchemy + Herbalism', 'Захист, Відплата: Інженерія + Гірництво. Світло: Алхімія + Травництво'), ('engineering', 'mining', 'alchemy', 'herbalism')),
     t('Свет тратит много маны: зелья свои, а Mana Well в лагере заменяет Благословение мудрости.', 'Holy burns a lot of mana: you make your own potions, and the Mana Well in camp replaces Blessing of Wisdom.', 'Світло витрачає багато мани: зілля свої, а Mana Well у таборі замінює Благословення мудрості.')),
    ('hunter', t('Охотник', 'Hunter', 'Мисливець'),
     (t('Кожевничество + Снятие шкур', 'Leatherworking + Skinning', 'Шкіряництво + Знімання шкур'), ('leatherworking', 'skinning')),
     (t('Инженерное дело + Горное дело', 'Engineering + Mining', 'Інженерія + Гірництво'), ('engineering', 'mining')),
     t('Кожевник шьёт себе кожу и кольчугу и Armor Kit. Инженер делает прицелы и ружья.', 'A leatherworker makes their own leather and mail and Armor Kits. An engineer makes scopes and guns.', 'Шкіряник шиє собі шкіру й кольчугу та Armor Kit. Інженер робить приціли й рушниці.')),
    ('rogue', t('Разбойник', 'Rogue', 'Розбійник'),
     (t('Кожевничество + Снятие шкур', 'Leatherworking + Skinning', 'Шкіряництво + Знімання шкур'), ('leatherworking', 'skinning')),
     (t('Инженерное дело + Горное дело', 'Engineering + Mining', 'Інженерія + Гірництво'), ('engineering', 'mining')),
     t('Кожа своя, Camp Tent даёт отдых. Инженерное дело — главное для PvP.', 'You make your own leather, and the Camp Tent gives rest. Engineering is the main profession for PvP.', 'Шкіра своя, Camp Tent дає відпочинок. Інженерія — головна професія для PvP.')),
    ('priest', t('Жрец', 'Priest', 'Жрець'),
     (t('Портняжное дело + Наложение чар', 'Tailoring + Enchanting', 'Кравецтво + Зачарування'), ('tailoring', 'enchanting')),
     (t('Портняжное дело + Инженерное дело или Наложение чар', 'Tailoring + Engineering or Enchanting', 'Кравецтво + Інженерія або Зачарування'), ('tailoring', 'engineering', 'enchanting')),
     t('Портной делает пояса с силой заклинаний с 10 уровня, зачарователь — жезлы с силой заклинаний с 5. Сшитое распыляют на материалы.', 'A tailor makes belts with spell power from level 10, an enchanter makes wands with spell power from level 5. Tailored items get disenchanted into materials.', 'Кравець робить пояси із силою заклинань від 10 рівня, зачарувальник — жезли із силою заклинань від 5. Пошите розщеплюють на матеріали.')),
    ('shaman', t('Шаман', 'Shaman', 'Шаман'),
     (t('Кожевничество + Снятие шкур', 'Leatherworking + Skinning', 'Шкіряництво + Знімання шкур'), ('leatherworking', 'skinning')),
     (t('Алхимия + Травничество', 'Alchemy + Herbalism', 'Алхімія + Травництво'), ('alchemy', 'herbalism')),
     t('Кожевник делает вещи с силой заклинаний для Стихий и Исцеления и экипировку для Совершенствования. В рейде и группе нужны зелья.', 'A leatherworker makes spell power gear for Elemental and Restoration and gear for Enhancement. Raids and groups need potions.', 'Шкіряник робить речі із силою заклинань для Стихій і Зцілення та спорядження для Вдосконалення. У рейді й групі потрібні зілля.')),
    ('mage', t('Маг', 'Mage', 'Маг'),
     (t('Портняжное дело + Наложение чар', 'Tailoring + Enchanting', 'Кравецтво + Зачарування'), ('tailoring', 'enchanting')),
     (t('Портняжное дело + Наложение чар; для PvP и больших пулов Инженерное дело + Горное дело', 'Tailoring + Enchanting; for PvP and big pulls Engineering + Mining', 'Кравецтво + Зачарування; для PvP і великих пулів Інженерія + Гірництво'), ('tailoring', 'enchanting', 'engineering', 'mining')),
     t('Портной даёт раннюю экипировку с силой заклинаний, сшитое распыляют. Гранаты инженера держат на месте большие группы врагов.', 'A tailor provides early spell power gear, and tailored items get disenchanted. An engineer’s grenades hold big groups of enemies in place.', 'Кравець дає раннє спорядження із силою заклинань, пошите розщеплюють. Гранати інженера втримують на місці великі групи ворогів.')),
    ('warlock', t('Чернокнижник', 'Warlock', 'Чорнокнижник'),
     (t('Портняжное дело + Наложение чар', 'Tailoring + Enchanting', 'Кравецтво + Зачарування'), ('tailoring', 'enchanting')),
     (t('Портняжное дело + Алхимия', 'Tailoring + Alchemy', 'Кравецтво + Алхімія'), ('tailoring', 'alchemy')),
     t('Faction Banner портного даёт дух для Жизнеотвода. Алхимия — зелья и золото.', 'A tailor’s Faction Banner gives Spirit for Life Tap. Alchemy means potions and gold.', 'Faction Banner кравця дає дух для Life Tap. Алхімія — зілля й золото.')),
    ('druid', t('Друид', 'Druid', 'Друїд'),
     (t('Кожевничество + Снятие шкур или Травничество', 'Leatherworking + Skinning or Herbalism', 'Шкіряництво + Знімання шкур або Травництво'), ('leatherworking', 'skinning', 'herbalism')),
     (t('Алхимия + Травничество', 'Alchemy + Herbalism', 'Алхімія + Травництво'), ('alchemy', 'herbalism')),
     t('Травы собирают в Походном облике, зелья пьют в любом облике. Mana Well и Incense Candle — для Баланса и Исцеления.', 'You gather herbs in Travel Form and drink potions in any form. Mana Well and Incense Candle help Balance and Restoration.', 'Трави збирають у Travel Form, зілля п’ють у будь-якому вигляді. Mana Well і Incense Candle — для Балансу й Зцілення.')),
]


def _pairs_table():
    return {'head': PAIR_HEAD[:3], 'rows': [[name, lvl[0], cap[0]] for _c, name, lvl, cap, _w in CLASS_PAIRS]}


def _pair_tabs():
    return [{'id': cid, 't': name, 'blocks': [('steps', [{'t': PAIR_HEAD[1], 'd': lvl[0]}, {'t': PAIR_HEAD[2], 'd': cap[0]}]), ('text', [why])]}
            for cid, name, lvl, cap, why in CLASS_PAIRS]


GUIDES.append({
    'slug': 'professions', 'art': 'hero_campfire', 'hero': 'hero_professions', 'js': 'professions',
    'title': t('Профессии', 'Professions', 'Професії'),
    'lead': t('Какие две профессии взять под ваш класс на прокачке и на 60 уровне, на чём заработать золото, что каждая профессия ставит в лагерь и как прокачать навык до 300.', 'Which two professions to pick for your class while leveling and at level 60, how to make gold, what each profession places in camp and how to raise the skill to 300.', 'Які дві професії взяти під ваш клас на прокачуванні та на 60 рівні, на чому заробити золото, що кожна професія ставить у табір і як прокачати навичку до 300.'),
    'tile': t('Пары под класс, золото, объекты лагеря', 'Class pairs, gold, camp objects', 'Пари під клас, золото, об’єкти табору'),
    'pills': [t('9 классов', '9 classes', '9 класів'), t('Прокачка и 60 уровень', 'Leveling and level 60', 'Прокачування й 60 рівень'), t('36 объектов лагеря', '36 camp objects', '36 об’єктів табору')],
    'sources': [
        (t('Warcraft Tavern: профессии', 'Warcraft Tavern: professions', 'Warcraft Tavern: професії'), 'https://www.warcrafttavern.com/forever/guides/professions/'),
        (t('Warcraft Tavern: Алхимия', 'Warcraft Tavern: Alchemy', 'Warcraft Tavern: Алхімія'), 'https://www.warcrafttavern.com/forever/guides/alchemy/'),
        (t('Warcraft Tavern: объекты и баффы лагеря', 'Warcraft Tavern: camp objects and buffs', 'Warcraft Tavern: об’єкти та баффи табору'),
         'https://www.warcrafttavern.com/forever/guides/camping-objects-buffs/'),
        (t('Warcraft Tavern: лагерь', 'Warcraft Tavern: camping', 'Warcraft Tavern: табір'), 'https://www.warcrafttavern.com/forever/guides/camping/'),
        (t('Icy Veins: профессии', 'Icy Veins: professions', 'Icy Veins: професії'), 'https://www.icy-veins.com/wow-forever/professions-overview'),
        (t('Mobalytics: ящики Waylaid Crate', 'Mobalytics: Waylaid Crates', 'Mobalytics: ящики Waylaid Crate'), 'https://mobalytics.gg/wow-forever/guides/waylaid-crates-explained'),
    ],
    'sections': [
        {'id': 'pairs', 'title': t('Пары под класс', 'Pairs for your class', 'Пари під клас'), 'blocks': [
            ('text', [t('Основных профессий две. На прокачке ремесло берут вместе со сбором для него: материалы свои, а вещи с рецептов обновляют экипировку. На 60 уровне многие меняют одно из двух на Инженерное дело или Алхимию. Пары для 60 уровня — по гайдам на данных беты, до старта их никто не проверил. Если вы заполнили «Мой персонаж» на главной, сразу откроется ваш класс.', 'There are two primary professions. While leveling, take a craft together with the gathering profession that feeds it: you get the materials yourself, and recipe items refresh your gear. At level 60 many players swap one of the two for Engineering or Alchemy. The level 60 pairs come from guides based on beta data, and nobody has tested them before launch. If you filled in “My character” on the home page, your class opens right away.', 'Основних професій дві. На прокачуванні ремесло беруть разом зі збиранням для нього: матеріали свої, а речі з рецептів оновлюють спорядження. На 60 рівні багато хто міняє одну з двох на Інженерію або Алхімію. Пари для 60 рівня — за гайдами на даних бети, до старту їх ніхто не перевірив. Якщо ви заповнили «Мій персонаж» на головній, одразу відкриється ваш клас.')]),
            ('table', _pairs_table()),
            ('tabs', _pair_tabs()),
            ('tip', t('Кулинарию, Первую помощь и Рыбалку берут все: это вспомогательные профессии, можно взять все три, и забыть их нельзя. Пусть кто-то в группе прокачает Кулинарию ради 10 мест в лагере: порог навыка источники называют разный.', 'Everyone takes Cooking, First Aid and Fishing: they are secondary professions, you can have all three and they cannot be unlearned. Let someone in the group raise Cooking for 10 camp slots: sources give different skill thresholds.', 'Кулінарію, Першу допомогу та Рибальство беруть усі: це допоміжні професії, можна взяти всі три, і розучити їх не можна. Нехай хтось у групі прокачає Кулінарію заради 10 місць у таборі: поріг навички джерела називають різний.')),
            ('tiles', [{'t': t('Тир-лист классов WoW Forever', 'WoW Forever Class Tier List', 'Тір-лист класів WoW Forever'), 'd': TL.tile(TL_STATUS), 'href': 'guides/tier-list/', 'art': 'hero_tierlist'}]),
        ]},
        {'id': 'choose', 'title': t('Как выбрать пару', 'How to choose a pair', 'Як вибрати пару'), 'blocks': [
            ('steps', [
                {'t': t('Ремесло по броне', 'A craft for your armor', 'Ремесло за бронею'),
                 'd': t('Кузнечное дело для лат, Кожевничество для кожи и кольчуги, Портняжное дело для ткани.', 'Blacksmithing for plate, Leatherworking for leather and mail, Tailoring for cloth.', 'Ковальство для лат, Шкіряництво для шкіри й кольчуги, Кравецтво для тканини.')},
                {'t': t('Сбор к ремеслу', 'Gathering for the craft', 'Збирання до ремесла'),
                 'd': t('Горное дело кормит Кузнечное и Инженерное дело, Травничество — Алхимию, Снятие шкур — Кожевничество. Портняжному делу сбор не нужен: ткань падает с гуманоидов, поэтому его берут с Наложением чар.', 'Mining feeds Blacksmithing and Engineering, Herbalism feeds Alchemy, Skinning feeds Leatherworking. Tailoring needs no gathering: cloth drops from humanoids, which is why it is paired with Enchanting.', 'Гірництво живить Ковальство та Інженерію, Травництво — Алхімію, Знімання шкур — Шкіряництво. Кравецтву збирання не потрібне: тканина падає з гуманоїдів, тому його беруть із Зачаруванням.')},
                {'t': t('Рецепты для себя', 'Recipes for yourself', 'Рецепти для себе'),
                 'd': t('Многие вещи с рецептов персональные: они становятся вашими при создании, купить их на аукционе нельзя. Нужная вещь — повод взять профессию самому.', 'Many recipe items are personal: they become yours when crafted and cannot be bought at the auction house. An item you need is a reason to take the profession yourself.', 'Багато речей з рецептів персональні: вони стають вашими під час створення, купити їх на аукціоні не можна. Потрібна річ — привід узяти професію самому.')},
                {'t': t('PvP', 'PvP', 'PvP'),
                 'd': t('Инженерное дело: гранаты, бомбы, устройства и свои аксессуары. Специализацию Гоблинов или Гномов выбирают с 200 навыка.', 'Engineering: grenades, bombs, devices and its own trinkets. The Goblin or Gnome specialization is chosen at skill 200.', 'Інженерія: гранати, бомби, пристрої та власні аксесуари. Спеціалізацію Гоблінів або Гномів обирають з навички 200.')},
                {'t': t('Рейд', 'Raid', 'Рейд'),
                 'd': t('Алхимия: эликсиры, а флаконы теперь варят в переносной Alchemy Laboratory, без похода в [[Некроситет|Scholomance]].', 'Alchemy: elixirs, and flasks are now brewed in the portable Alchemy Laboratory, with no trip to Scholomance.', 'Алхімія: еліксири, а флакони тепер варять у переносній Alchemy Laboratory, без походу до Scholomance.')},
                {'t': t('Два ремесла', 'Two crafts', 'Два ремесла'),
                 'd': t('Когда персонажей несколько и золото есть, второе ремесло вместо сбора: материалы носит твинк или аукцион.', 'When you have several characters and some gold, take a second craft instead of gathering: an alt or the auction house supplies the materials.', 'Коли персонажів кілька і золото є, друге ремесло замість збирання: матеріали носить твінк або аукціон.')},
            ]),
            ('tip', t('Отказ от профессии стирает навык и рецепты, учить заново с нуля. Меняйте сбор на ремесло ближе к 60 уровню, когда сбор уже окупился.', 'Unlearning a profession wipes the skill and recipes, and you start over from zero. Swap gathering for a craft closer to level 60, once the gathering has paid off.', 'Відмова від професії стирає навичку й рецепти, вчити знову з нуля. Міняйте збирання на ремесло ближче до 60 рівня, коли збирання вже окупилося.')),
            ('tiles', [{'t': t('Прокачка 1–60', 'Leveling 1–60', 'Прокачування 1–60'), 'd': t('Маршрут и лагерь на прокачке', 'Route and camp while leveling', 'Маршрут і табір на прокачуванні'), 'href': 'guides/leveling/#camp', 'art': 'hero_leveling'}]),
        ]},
        {'id': 'gold', 'title': t('Профессии для золота', 'Professions for gold', 'Професії для золота'), 'blocks': [
            ('text', [t('WoW Token в Forever нет и пока не планируется (разработчики, сентябрь 2026): всё золото на сервере добывают игроки. Ремесло в основном одевает вас самого, а продают в первую очередь материалы.', 'There is no WoW Token in Forever and none is planned for now (developers, September 2026): all the gold on the server is earned by players. A craft mostly dresses you, so what sells first of all is materials.', 'WoW Token у Forever немає й поки не планується (розробники, вересень 2026): усе золото на сервері здобувають гравці. Ремесло здебільшого одягає вас самого, а продають насамперед матеріали.')]),
            ('table', {'head': [t('Профессия', 'Profession', 'Професія'), t('Что продают', 'What sells', 'Що продають'), t('Важно', 'Good to know', 'Важливо')], 'rows': [
                [t('Травничество', 'Herbalism', 'Травництво'), t('Травы, семена, редкие материалы', 'Herbs, seeds, rare materials', 'Трави, насіння, рідкісні матеріали'), t('Обычные травы быстро дешевеют, редкие держат цену.', 'Common herbs get cheap fast, rare ones hold their price.', 'Звичайні трави швидко дешевшають, рідкісні тримають ціну.')],
                [t('Горное дело', 'Mining', 'Гірництво'), t('Руда, слитки, редкие материалы', 'Ore, bars, rare materials', 'Руда, зливки, рідкісні матеріали'), t('Руду берут кузнецы и инженеры.', 'Blacksmiths and engineers buy the ore.', 'Руду беруть ковалі та інженери.')],
                [t('Снятие шкур', 'Skinning', 'Знімання шкур'), t('Кожа, шкуры, редкие материалы', 'Leather, hides, rare materials', 'Шкіра, шкури, рідкісні матеріали'), t('Одна из самых доходных профессий для золота, по Warcraft Tavern.', 'One of the most profitable professions for gold, according to Warcraft Tavern.', 'Одна з найприбутковіших професій для золота, за Warcraft Tavern.')],
                [t('Алхимия', 'Alchemy', 'Алхімія'), t('Эликсиры, флаконы, трансмутации', 'Elixirs, flasks, transmutations', 'Еліксири, флакони, трансмутації'), t('Лечебные зелья теперь у Первой помощи, их варит кто угодно.', 'Healing potions now belong to First Aid, so anyone can brew them.', 'Лікувальні зілля тепер у Першої допомоги, їх варить будь-хто.')],
                [t('Наложение чар', 'Enchanting', 'Зачарування'), t('Чары на чужие вещи', 'Enchants for other people’s gear', 'Чари на чужі речі'), t('Редкие чары дороже.', 'Rare enchants cost more.', 'Рідкісні чари дорожчі.')],
                [t('Инженерное дело', 'Engineering', 'Інженерія'), t('Мало', 'Little', 'Мало'), t('Польза в устройствах, а не в заработке.', 'Its value is in devices, not in income.', 'Користь у пристроях, а не в заробітку.')],
            ]}),
            ('steps', [
                {'t': t('Два сбора', 'Two gathering professions', 'Два збирання'),
                 'd': t('Самый простой заработок на старте: почти без вложений, всё, что собрали, идёт на аукцион.', 'The easiest income at the start: almost no investment, and everything you gather goes to the auction house.', 'Найпростіший заробіток на старті: майже без вкладень, усе, що зібрали, йде на аукціон.')},
                {'t': t('Редкие материалы', 'Rare materials', 'Рідкісні матеріали'),
                 'd': t('Сбор иногда даёт редкие материалы (Frilled Lichen, Rosecaps и другие) для красок и чар. Перк Legacy Bountiful Harvest помогает чаще находить дополнительные редкие ресурсы.', 'Gathering sometimes gives rare materials (Frilled Lichen, Rosecaps and others) for dyes and enchants. The Legacy Bountiful Harvest perk helps you find extra scarce resources more often.', 'Збирання іноді дає рідкісні матеріали (Frilled Lichen, Rosecaps та інші) для фарб і чар. Перк Legacy Bountiful Harvest допомагає частіше знаходити додаткові рідкісні ресурси.')},
                {'t': t('Ящики', 'Crates', 'Ящики'),
                 'd': t('Waylaid Crate падает с врагов и продаётся на аукционе. Ящик, который не будете сдавать, продайте.', 'Waylaid Crate drops from enemies and sells at the auction house. A crate you will not turn in, sell.', 'Waylaid Crate падає з ворогів і продається на аукціоні. Ящик, який не здаватимете, продайте.')},
                {'t': t('Не продавайте вслепую', 'Do not sell blindly', 'Не продавайте наосліп'),
                 'd': t('Сначала посмотрите, для чего предмет и сколько он стоит на аукционе. Дорогие покупки отложите до 60 уровня.', 'First check what an item is for and what it costs at the auction house. Put expensive purchases off until level 60.', 'Спершу подивіться, для чого предмет і скільки він коштує на аукціоні. Дорогі покупки відкладіть до 60 рівня.')},
            ]),
            ('tip', t('Цен по бете не пишем: на бете был лимит уровня, своя экономика на старте сложится заново.', 'We give no beta prices: the beta had a level cap, and the economy will form anew at launch.', 'Цін з бети не пишемо: на беті був ліміт рівня, власна економіка на старті складеться заново.')),
            ('tiles', [{'t': t('Система Legacy', 'The Legacy System', 'Система Legacy'), 'd': t('Перки профессий: Bountiful Harvest, Performance Bonus', 'Profession perks: Bountiful Harvest, Performance Bonus', 'Перки професій: Bountiful Harvest, Performance Bonus'), 'href': 'guides/legacy/', 'art': 'hero_guides'}]),
        ]},
        {'id': 'crates', 'title': t('Ящики и Merchant’s Favor', 'Crates and Merchant’s Favor', 'Ящики та Merchant’s Favor'), 'blocks': [
            ('text', [t('Новое в Forever: рецепты за валюту Merchant’s Favor. Её дают за ящики Waylaid Crate, заполненные материалами профессий.', 'New in Forever: recipes for the Merchant’s Favor currency. You earn it by turning in Waylaid Crates filled with profession materials.', 'Нове у Forever: рецепти за валюту Merchant’s Favor. Її дають за ящики Waylaid Crate, заповнені матеріалами професій.')]),
            ('steps', [
                {'t': t('Ящик', 'The crate', 'Ящик'),
                 'd': t('Waylaid Crate падает с врагов в открытом мире, его можно купить на аукционе. Заполнить нужно одну связку из списка ящика.', 'Waylaid Crate drops from enemies in the open world, and you can buy it at the auction house. You need to fill one bundle from the crate’s list.', 'Waylaid Crate падає з ворогів у відкритому світі, його можна купити на аукціоні. Заповнити потрібно один набір зі списку ящика.')},
                {'t': t('Куда сдавать', 'Where to turn it in', 'Куди здавати'),
                 'd': t('Орда: Dokimi у западных ворот Crossroads в [[Степях|The Barrens]]. Альянс: Marcy Baker на Three Corners, на западе [[Красногорья|Redridge Mountains]]. Рядом стоят продавцы рецептов.', 'Horde: Dokimi at the west gate of Crossroads in The Barrens. Alliance: Marcy Baker at Three Corners, in the west of Redridge Mountains. Recipe vendors stand nearby.', 'Орда: Dokimi біля західної брами Crossroads у The Barrens. Альянс: Marcy Baker на Three Corners, на заході Redridge Mountains. Поруч стоять продавці рецептів.')},
                {'t': t('Первый ящик', 'The first crate', 'Перший ящик'),
                 'd': t('Первая сдача даёт бонус 50 Merchant’s Favor: хватает на рецепт сразу.', 'The first turn-in gives a bonus of 50 Merchant’s Favor: enough for a recipe right away.', 'Перша здача дає бонус 50 Merchant’s Favor: вистачає на рецепт одразу.')},
                {'t': t('Репутация', 'Reputation', 'Репутація'),
                 'd': t('Сдача ящиков даёт репутацию у лагеря (Durotar Supply and Logistics у Орды, Azeroth Commerce Authority у Альянса). Рецепты выше 35 уровня требуют репутации.', 'Turning in crates earns reputation with the camp (Durotar Supply and Logistics for the Horde, Azeroth Commerce Authority for the Alliance). Recipes above level 35 require reputation.', 'Здача ящиків дає репутацію в таборі (Durotar Supply and Logistics в Орди, Azeroth Commerce Authority в Альянсу). Рецепти вище 35 рівня потребують репутації.')},
                {'t': t('Рецепты', 'Recipes', 'Рецепти'),
                 'd': t('Вещи с них персональные. Покупайте рецепт под самую слабую часть экипировки.', 'Items from them are personal. Buy a recipe for your weakest gear slot.', 'Речі з них персональні. Купуйте рецепт під найслабший слот спорядження.')},
            ]),
            ('tip', t('Merchant’s Favor у каждого персонажа свой. Перк Legacy Performance Bonus иногда даёт больше Favor.', 'Merchant’s Favor is separate for each character. The Legacy Performance Bonus perk sometimes gives more Favor.', 'Merchant’s Favor у кожного персонажа свій. Перк Legacy Performance Bonus іноді дає більше Favor.')),
        ]},
        {'id': 'camp', 'title': t('Объекты лагеря', 'Camp objects', 'Об’єкти табору'), 'blocks': [
            ('text', [t('У каждой профессии три объекта лагеря, по одному на уровень. Ниже объект первого уровня и бафф класса, на который похож его эффект.',
                        'Each profession has three camp objects, one per tier. Below is the tier 1 object and the class buff its effect resembles.',
                        'Кожна професія має три об’єкти табору, по одному на рівень. Нижче об’єкт першого рівня та бафф класу, на який схожий його ефект.')]),
            ('profs', None),
            ('tip', t('Баффы лагеря немного слабее классовых и не складываются с ними: Благословение королей даёт 10% ко всем характеристикам, а Fish Bowl в лагере 8%. Ставьте объекты, которых нет у классов вашей группы.',
                      'Camp buffs are slightly weaker than class buffs and do not stack with them: Blessing of Kings gives 10% to all stats, the camp Fish Bowl 8%. Place objects whose buffs no class in your group provides.',
                      'Баффи табору трохи слабші за класові й не складаються з ними: Благословення королів дає 10% до всіх характеристик, а Fish Bowl у таборі 8%. Ставте об’єкти, яких немає в класів вашої групи.')),
        ]},
        {'id': 'leveling', 'title': t('Прокачка навыка', 'Raising your skill', 'Прокачування навички'), 'blocks': [
            ('table', {'head': [t('Ступень', 'Rank', 'Ступінь'), t('С уровня персонажа', 'From character level', 'З рівня персонажа'), t('Навык до', 'Skill up to', 'Навичка до')], 'rows': [
                [t('Ученик', 'Apprentice', 'Apprentice'), t('1 для сбора, 5 для ремёсел', '1 for gathering, 5 for crafts', '1 для збирання, 5 для ремесел'), '75'],
                [t('Подмастерье', 'Journeyman', 'Journeyman'), '10', '150'],
                [t('Умелец', 'Expert', 'Expert'), '20', '225'],
                [t('Искусник', 'Artisan', 'Artisan'), '35', '300'],
            ]}),
            ('text', [t('Уровни персонажа для Умельца и Искусника даны по Warcraft Tavern. Для сбора Icy Veins пишет 10 и 25: источники расходятся, уточним на старте.',
                        'Character levels for Expert and Artisan follow Warcraft Tavern. For gathering, Icy Veins gives 10 and 25: sources differ, we will confirm at launch.',
                        'Рівні персонажа для Expert і Artisan за Warcraft Tavern. Для збирання Icy Veins пише 10 і 25: джерела розходяться, уточнимо на старті.')]),
            ('steps', [
                {'t': t('Первое задание', 'First quest', 'Перше завдання'),
                 'd': t('Стартовое задание предлагает Горное дело, Снятие шкур или Травничество, учит профессии и сразу даёт 2 очка навыка.',
                        'A starter quest offers Mining, Skinning or Herbalism, teaches the profession and gives 2 skill points right away.',
                        'Стартове завдання пропонує Гірництво, Знімання шкур або Травництво, вчить професії й одразу дає 2 очки навички.')},
                {'t': t('Цвет рецепта', 'Recipe colour', 'Колір рецепта'),
                 'd': t('Оранжевые рецепты и залежи всегда дают очко, жёлтые часто, зелёные редко, серые никогда.',
                        'Orange recipes and nodes always give a point, yellow often, green rarely, grey never.',
                        'Помаранчеві рецепти й поклади завжди дають очко, жовті часто, зелені рідко, сірі ніколи.')},
                {'t': t('Искусник', 'Artisan', 'Artisan'),
                 'd': t('Ступень Искусника даёт только особый учитель, а у вспомогательных профессий — особое задание.',
                        'Artisan comes only from special trainers, or from a special quest for secondary professions.',
                        'Ступінь Artisan дають лише особливі вчителі, а для допоміжних професій особливе завдання.')},
                {'t': t('Окно профессий', 'Professions window', 'Вікно професій'),
                 'd': t('Своё окно на клавише K: рецепты можно искать, фильтровать и отслеживать как список покупок. Для сумки с реагентами есть отдельная ячейка.',
                        'Its own window on the K key: recipes can be searched, filtered and tracked as a shopping list. Reagent bags have their own slot.',
                        'Своє вікно на клавіші K: рецепти можна шукати, фільтрувати й відстежувати як список покупок. Для сумки з реагентами є окремий слот.')},
            ]),
            ('tip', t('Если отказаться от профессии, весь её прогресс пропадёт, а игра просит подтвердить это вводом слова. Пассивных бонусов у профессий в Forever нет: польза в том, что вы делаете и собираете, и в баффах лагеря.',
                      'Unlearning a profession wipes all its progress, and the game asks you to type a confirmation. Professions in Forever have no passive bonuses: the value is in what you craft and gather, and in camp buffs.',
                      'Розучивши професію, ви втрачаєте весь її прогрес, а гра просить підтвердити це введенням слова. Пасивних бонусів у професій у Forever немає: користь у тому, що ви робите й збираєте, і в баффах табору.')),
        ]},
        {'id': 'changes', 'title': t('Что изменилось против Classic', 'What changed compared to Classic', 'Що змінилося проти Classic'), 'blocks': [
            ('table', {'head': [t('Что', 'What', 'Що'), t('В Forever', 'In Forever', 'У Forever')], 'rows': [
                [t('Лечебные зелья', 'Healing potions', 'Лікувальні зілля'), t('Перешли из Алхимии в Первую помощь', 'Moved from Alchemy to First Aid', 'Перейшли з Алхімії до Першої допомоги')],
                [t('Алхимия', 'Alchemy', 'Алхімія'), t('Переносная Alchemy Laboratory для флаконов, краски, Rage Potion теперь и для друидов', 'Portable Alchemy Laboratory for flasks, dyes, Rage Potion now for druids too', 'Переносна Alchemy Laboratory для флаконів, фарби, Rage Potion тепер і для друїдів')],
                [t('Наложение чар', 'Enchanting', 'Зачарування'), t('Делает посохи, реликвии, идолы и тотемы, новые чары на ожерелье, жезлы с силой заклинаний', 'Makes staves, relics, idols and totems, new enchants for the neck, wands with spell power', 'Робить посохи, реліквії, ідоли й тотеми, нові чари на намисто, жезли із силою заклинань')],
                [t('Кожевничество', 'Leatherworking', 'Шкіряництво'), t('Armor Kit для бойцов и для заклинателей отдельно', 'Armor Kit for fighters and, separately, for casters', 'Armor Kit для бійців і окремо для заклиначів')],
                [t('Инженерное дело', 'Engineering', 'Інженерія'), t('Безопасные для всех гранаты Saf T. Инженерная специализация гномов теперь снижает шанс сбоя устройств', 'Saf T grenades, safe for everyone. The gnome engineering specialization now lowers the chance of devices failing', 'Безпечні для всіх гранати Saf T. Інженерна спеціалізація гномів тепер знижує шанс збою пристроїв')],
                [t('Травничество', 'Herbalism', 'Травництво'), t('Семена и теплица в лагере', 'Seeds and a greenhouse in camp', 'Насіння й теплиця в таборі')],
                [t('Рецепты', 'Recipes', 'Рецепти'), t('Больше 600 новых, в основном из материалов Classic', 'Over 600 new ones, mostly from Classic materials', 'Понад 600 нових, здебільшого з матеріалів Classic')],
                [t('Сумки', 'Bags', 'Сумки'), t('Отдельная ячейка для сумки с реагентами', 'A separate slot for a reagent bag', 'Окрема комірка для сумки з реагентами')],
            ]}),
        ]},
        {'id': 'questions', 'title': t('Частые вопросы', 'Frequently asked questions', 'Часті питання'), 'blocks': [
            ('faq', [
                {'id': 'best-gold', 'q': t('Какие профессии лучше для золота в WoW Forever?', 'Which professions are best for gold in WoW Forever?', 'Які професії найкращі для золота у WoW Forever?'),
                 'a': [t('Два сбора: Травничество, Горное дело или Снятие шкур. Вложений почти нет, материалы нужны всем ремесленникам. Из ремёсел для золота советуют Алхимию в паре с Травничеством.', 'Two gathering professions: Herbalism, Mining or Skinning. There is almost no investment, and every crafter needs the materials. Of the crafts, players recommend Alchemy paired with Herbalism for gold.', 'Два збирання: Травництво, Гірництво або Знімання шкур. Вкладень майже немає, матеріали потрібні всім ремісникам. З ремесел для золота радять Алхімію в парі з Травництвом.')]},
                {'id': 'warrior', 'q': t('Какую профессию взять воину?', 'Which profession should a warrior take?', 'Яку професію взяти воїну?'),
                 'a': [t('Кузнечное дело и Горное дело на прокачке: кузнец сам делает себе латы и оружие. На 60 уровне Кузнечное дело часто меняют на Инженерное.', 'Blacksmithing and Mining while leveling: a blacksmith makes their own plate and weapons. At level 60 Blacksmithing is often swapped for Engineering.', 'Ковальство та Гірництво на прокачуванні: коваль сам робить собі лати й зброю. На 60 рівні Ковальство часто міняють на Інженерію.')]},
                {'id': 'pvp', 'q': t('Нужно ли Инженерное дело для PvP?', 'Do you need Engineering for PvP?', 'Чи потрібна Інженерія для PvP?'),
                 'a': [t('Да, для PvP его берут почти все классы: гранаты, бомбы и устройства дают контроль и подвижность, которых у класса нет.', 'Yes, almost every class takes it for PvP: grenades, bombs and devices give control and mobility the class lacks.', 'Так, для PvP її беруть майже всі класи: гранати, бомби та пристрої дають контроль і рухливість, яких у класу бракує.')]},
                {'id': 'potions', 'q': t('Кто теперь делает лечебные зелья?', 'Who makes healing potions now?', 'Хто тепер робить лікувальні зілля?'),
                 'a': [t('Первая помощь. Это вспомогательная профессия, её может взять любой персонаж без траты основного места. Алхимия оставила себе эликсиры, флаконы и трансмутации.', 'First Aid. It is a secondary profession that any character can take without using a primary slot. Alchemy kept elixirs, flasks and transmutations.', 'Перша допомога. Це допоміжна професія, її може взяти будь-який персонаж, не витрачаючи основне місце. Алхімія залишила собі еліксири, флакони й трансмутації.')]},
                {'id': 'change', 'q': t('Можно ли сменить профессию?', 'Can you change a profession?', 'Чи можна змінити професію?'),
                 'a': [t('Да, в любой момент, но навык и рецепты пропадут, прокачивать придётся с нуля. Вспомогательные профессии забыть нельзя.', 'Yes, at any time, but the skill and recipes are lost and you level from zero. Secondary professions cannot be unlearned.', 'Так, будь-коли, але навичка й рецепти зникнуть, прокачувати доведеться з нуля. Допоміжні професії розучити не можна.')]},
                {'id': 'favor', 'q': t('Что такое Merchant’s Favor?', 'What is Merchant’s Favor?', 'Що таке Merchant’s Favor?'),
                 'a': [t('Валюта за сданные ящики Waylaid Crate. На неё покупают рецепты, вещи с которых персональные. У каждого персонажа своя.', 'A currency for turned-in Waylaid Crates. You buy recipes with it, and items from them are personal. Each character has their own.', 'Валюта за здані ящики Waylaid Crate. За неї купують рецепти, речі з яких персональні. У кожного персонажа своя.')]},
            ]),
        ]},
    ],
})

# ---------- Новости: наши записи (новые сверху) + автолента Wowhead из assets/news.json ----------

NR_URL = 'https://news.blizzard.com/en-us/article/24303866/claim-your-world-of-warcraft-forever-character-names'   # name reservation 27.10 – 03.11

NEWS += [
    {'date': '2026-10-29', 'url': 'https://worldofwarcraft.blizzard.com/en-us/news/24315820/world-of-warcraft-forever-goes-live-globally-november-4',
     'title': t('WoW Forever выходит по всему миру в ноябре', 'WoW Forever goes live globally in November', 'WoW Forever виходить по всьому світу в листопаді'),
     'text': t('Blizzard объявила, что World of Warcraft: Forever запускается по всему миру в ноябре. В анонсе перечислено главное: более тысячи новых заданий на пути с уровня 1 до 60, новые и переработанные зоны (Mount Hyjal, Shen\'dralas, Riverglades, Zephras Isle), новая раса Skyborne: Windshapers Орды могут стать Shaman, High-Order Skyborne Альянса — Mage, девять новых подземелий на пять игроков для уровней 13–60, система Legacy, поле боя Darkspear Islands (15 на 15) и четыре режима. 9 декабря игроки 60-го уровня смогут войти в три рейда: Barrow Deeps, Hyjal Summit и Onyxia\'s Lair.',
               'Blizzard announced that World of Warcraft: Forever goes live globally in November. The announcement recaps the essentials: more than a thousand new quests across the level 1–60 journey, new and reimagined zones (Mount Hyjal, Shen\'dralas, the Riverglades, Zephras Isle), the new Skyborne race: Horde Windshapers can become Shaman, Alliance High-Order Skyborne can become Mages, nine new five-player dungeons for levels 13–60, the Legacy System, the Darkspear Islands battleground (15 versus 15) and four rulesets. On December 9, level 60 players can enter three raids: Barrow Deeps, Hyjal Summit and Onyxia\'s Lair.',
               'Blizzard оголосила, що World of Warcraft: Forever запускається по всьому світу в листопаді. В анонсі перелічено головне: понад тисячу нових завдань на шляху з рівня 1 до 60, нові та перероблені зони (Mount Hyjal, Shen\'dralas, Riverglades, Zephras Isle), нова раса Skyborne: Windshapers Орди можуть стати Shaman, High-Order Skyborne Альянсу — Mage, дев\'ять нових підземель на п\'ятьох гравців для рівнів 13–60, система Legacy, поле бою Darkspear Islands (15 на 15) і чотири режими. 9 грудня гравці 60-го рівня зможуть увійти до трьох рейдів: Barrow Deeps, Hyjal Summit та Onyxia\'s Lair.'),
     'so': t('Старт 05.11 в 01:00 по Киеву, рейды для 60-го уровня — с 09.12.',
             'Launch: 05.11 at 01:00 Kyiv time; raids for level 60 open on 09.12.',
             'Старт 05.11 о 01:00 за Києвом, рейди для 60-го рівня — з 09.12.')},
    {'date': '2026-10-29', 'url': 'https://worldofwarcraft.blizzard.com/en-us/news/24315643/return-to-azeroth-in-world-of-warcraft-forever',
     'title': t('Blizzard подвела итоги WoW Forever перед запуском', 'Blizzard sums up WoW Forever ahead of launch', 'Blizzard підсумувала WoW Forever перед запуском'),
     'text': t('В статье Return to Azeroth Blizzard собрала главное о WoW Forever. Игра начинается в раннем «Year 1» оригинального World of Warcraft и расширяет мир уровней 1–60 новыми и переработанными зонами (Mount Hyjal, Shen\'dralas, Riverglades, Zephras Isle). Девять новых подземелий на пять игроков охватывают уровни 13–60. Новая раса Skyborne доступна и Альянсу, и Орде, стартует на Zephras Isle (уровни 1–12) и требует Heroic Pack или выше. Также упомянуты аккаунтная система Legacy, поле боя Darkspear Islands (15 на 15, уровни 30–60) и четыре режима при запуске (Normal, PvP, Roleplay, Roleplay-PvP); Hardcore появится позже.',
               'In Return to Azeroth Blizzard gathers the key points about WoW Forever. The game begins in the early "Year 1" period of original World of Warcraft and expands the level 1–60 world with new and reimagined zones (Mount Hyjal, Shen\'dralas, the Riverglades, Zephras Isle). Nine new five-player dungeons span levels 13–60. The new Skyborne race can join either the Alliance or the Horde, starts on Zephras Isle (levels 1–12) and requires the Heroic Pack or higher. The article also covers the account-wide Legacy System, the Darkspear Islands battleground (15 versus 15, levels 30–60) and four rulesets at launch (Normal, PvP, Roleplay, Roleplay-PvP); Hardcore comes later.',
               'У статті Return to Azeroth Blizzard зібрала головне про WoW Forever. Гра починається в ранньому «Year 1» оригінального World of Warcraft і розширює світ рівнів 1–60 новими та переробленими зонами (Mount Hyjal, Shen\'dralas, Riverglades, Zephras Isle). Дев\'ять нових підземель на п\'ятьох гравців охоплюють рівні 13–60. Нова раса Skyborne доступна і Альянсу, і Орді, стартує на Zephras Isle (рівні 1–12) і потребує Heroic Pack або вище. Також згадано акаунтну систему Legacy, поле бою Darkspear Islands (15 на 15, рівні 30–60) і чотири режими на запуску (Normal, PvP, Roleplay, Roleplay-PvP); Hardcore з\'явиться пізніше.'),
     'so': t('Skyborne — только с Heroic Pack или выше. Hardcore на старте нет.',
             'Skyborne needs the Heroic Pack or higher. No Hardcore at launch.',
             'Skyborne — лише з Heroic Pack або вище. Hardcore на старті немає.')},
    {'date': '2026-10-22', 'url': 'https://worldofwarcraft.blizzard.com/en-us/news/24302070/choose-your-ruleset-in-world-of-warcraft-forever',
     'title': t('Blizzard описала четыре режима', 'Blizzard describes the four rulesets', 'Blizzard описала чотири режими'),
     'text': t('В статье Choose Your Ruleset Blizzard описывает четыре режима. Normal: приключения и бои с монстрами, бои с другими игроками по вашему желанию. PvP: упор на бои игрок против игрока, почти всегда есть риск нападения вражеских игроков. Roleplay: строгие правила имён и поведения для игроков, которые хотят погрузиться в роль персонажа. Roleplay PvP: те же правила с упором на бои игрок против игрока.',
               'Blizzard\'s article Choose Your Ruleset describes four rulesets. Normal: adventuring and fighting monsters, with fights against other players at your own discretion. PvP: a focus on player versus player combat, and you are almost always at risk of being attacked by opposing players. Roleplay: strict naming conventions and behavior rules for players who want to immerse themselves as a character. Roleplay PvP: the same rules with a focus on player versus player combat.',
               'У статті Choose Your Ruleset Blizzard описує чотири режими. Normal: пригоди та бої з монстрами, бої з іншими гравцями на ваш розсуд. PvP: акцент на боях гравець проти гравця, майже завжди є ризик нападу ворожих гравців. Roleplay: суворі правила імен і поведінки для гравців, які хочуть зануритися в роль персонажа. Roleplay PvP: ті самі правила з акцентом на боях гравець проти гравця.'),
     'so': t('На PvP и Roleplay PvP на вас почти всегда могут напасть, на Normal бой с игроками — по желанию.',
             'On PvP and Roleplay PvP you can almost always be attacked; on Normal, fighting players is your choice.',
             'На PvP і Roleplay PvP на вас майже завжди можуть напасти, на Normal бій із гравцями — за бажанням.')},
    {'date': '2026-10-28', 'url': 'https://worldofwarcraft.blizzard.com/en-us/news/24315280/new-players-starter-guide-welcome-to-world-of-warcraft-forever',
     'title': t('Стартовый гид Blizzard для новых игроков WoW Forever', 'New player\'s starter guide for WoW Forever', 'Стартовий гід Blizzard для нових гравців WoW Forever'),
     'text': t('Blizzard опубликовала стартовый гид для новых игроков WoW Forever. В нём: выбор режима (Ruleset) до создания персонажа (при запуске Normal, PvP, Roleplay и Roleplay-PvP, Hardcore позже), правило, что группы, гильдии, подземелья и рейды доступны только игрокам с тем же режимом и фракцией, система из двух имён, сбор ресурсов, ремёсла и вторичные профессии, а также что делать после смерти. Подробности и сроки Hardcore пока не объявлены. Roleplay-PvP: строгие правила имён и поведения для тех, кто хочет погрузиться в роль персонажа в фэнтезийном мире с упором на бои игрок против игрока; нападения вражеских персонажей почти всегда возможны.',
               'Blizzard published a starter guide for new WoW Forever players. It covers the choice of Ruleset before character creation (Normal, PvP, Roleplay and Roleplay-PvP at launch, Hardcore later), the rule that grouping, guilds, dungeons and raids work only with players of the same Ruleset and faction, the two-name system, gathering, crafting and secondary professions, and what to do after death. Hardcore details and timing are not yet announced. Roleplay-PvP has strict naming conventions and behavior rules for players who want to immerse themselves as a character in a fantasy world focused on player versus player combat; you are almost always at risk of being attacked by opposing characters.',
               'Blizzard опублікувала стартовий гід для нових гравців WoW Forever. У ньому: вибір режиму (Ruleset) до створення персонажа (на запуску Normal, PvP, Roleplay і Roleplay-PvP, Hardcore пізніше), правило, що групи, гільдії, підземелля та рейди доступні лише гравцям із тим самим режимом і фракцією, система з двох імен, збір ресурсів, ремесла та другорядні професії, а також що робити після смерті. Подробиці й терміни Hardcore поки не оголошено. Roleplay-PvP: суворі правила імен і поведінки для тих, хто хоче зануритися в роль персонажа у фентезійному світі з акцентом на боях гравець проти гравця; напади ворожих персонажів майже завжди можливі.'),
     'so': t('Группы, гильдии, подземелья и рейды — только с игроками вашего режима и фракции.',
             'Groups, guilds, dungeons and raids work only with players of your ruleset and faction.',
             'Групи, гільдії, підземелля та рейди — лише з гравцями вашого режиму і фракції.')},
    {'date': '2026-10-27', 'cls': 'all', 'url': NR_URL,
     'title': t('Резерв имён открыт до 03.11', 'Name reservation is open until 03.11', 'Резерв імен відкрито до 03.11'),
     'text': t('С 27.10 по 03.11 владельцы Skyborne Heroic Pack, Skyborne Epic Pack и Warcraft Forever Collection создают до трёх персонажей и занимают их имена. Лимит общий на все режимы. Резерв работает только на том аккаунте WoW, для которого куплен набор. Имена раздают по принципу «кто первый», нужное не гарантировано. Старт по Киеву: Европа 27.10 в 19:00, Америка 27.10 в 22:00, Корея 28.10 в 00:00, Тайвань 28.10 в 01:00. Источник: Blizzard.',
               'From 27.10 to 03.11 owners of the Skyborne Heroic Pack, Skyborne Epic Pack and Warcraft Forever Collection can create up to three characters and claim their names. The limit covers all modes together. The reservation works only on the WoW account the pack was bought for. Names are first come, first served, and no name is guaranteed. Start in Kyiv time: Europe 27.10 at 19:00, the Americas 27.10 at 22:00, Korea 28.10 at 00:00, Taiwan 28.10 at 01:00. Source: Blizzard.',
               'З 27.10 по 03.11 власники Skyborne Heroic Pack, Skyborne Epic Pack і Warcraft Forever Collection створюють до трьох персонажів і займають їхні імена. Ліміт спільний на всі режими. Резерв працює лише на тому акаунті WoW, для якого куплено набір. Імена роздають за принципом «хто перший», потрібне не гарантоване. Старт за Києвом: Європа 27.10 о 19:00, Америка 27.10 о 22:00, Корея 28.10 о 00:00, Тайвань 28.10 о 01:00. Джерело: Blizzard.'),
     'so': t('До 03.11 займите до трёх имён. Пошагово — в гиде «Как зарезервировать имя».',
             'Claim up to three names by 03.11. Steps are in our guide How to Reserve Your Name.',
             'До 03.11 займіть до трьох імен. Покроково — у гіді «Як зарезервувати ім’я».')},
    {'date': '2026-10-15', 'url': 'https://us.forums.blizzard.com/en/wow/t/beta-realm-maintenance-october-15/2383475/1',
     'title': t('Техработы на реалмах беты', 'Beta realm maintenance', 'Технічні роботи на реалмах бети'),
     'text': t('Blizzard написала на форуме о технических работах на реалмах беты. Подробностей, которые мы могли бы проверить, в сообщении нет: детали смотрите в самом сообщении.',
               'Blizzard posted on the forum about beta realm maintenance. The post gives no further details we could verify, so check the linked post.',
               'Blizzard написала на форумі про технічні роботи на реалмах бети. Подробиць, які ми могли б перевірити, у повідомленні немає: деталі дивіться в самому повідомленні.'),
     'so': t('Касалось только реалмов беты.',
             'Affected the beta realms only.',
             'Стосувалося лише реалмів бети.')},
    {'date': '2026-10-01', 'url': 'https://us.forums.blizzard.com/en/wow/t/actions-taken-against-botting-and-rmt/2368705/1',
     'title': t('Меры против ботов и RMT', 'Actions taken against botting and RMT', 'Заходи проти ботів і RMT'),
     'text': t('Blizzard написала на форуме о мерах против ботов и RMT (продажи игровых ценностей за реальные деньги). Подробностей, которые мы могли бы проверить, в сообщении нет: детали смотрите в самом сообщении.',
               'Blizzard posted on the forum about actions taken against botting and RMT (real-money trading). The post gives no further details we could verify, so check the linked post.',
               'Blizzard написала на форумі про заходи проти ботів і RMT (продаж ігрових цінностей за реальні гроші). Подробиць, які ми могли б перевірити, у повідомленні немає: деталі дивіться в самому повідомленні.'),
     'so': t('Не покупайте золото и не используйте ботов: Blizzard принимает меры.',
             'Do not buy gold or use bots: Blizzard takes action.',
             'Не купуйте золото й не користуйтеся ботами: Blizzard вживає заходів.')},
    {'date': '2026-10-22', 'url': 'https://us.forums.blizzard.com/en/wow/t/the-roleplay-pvp-ruleset-is-coming-to-wow-forever/2389502/1',
     'title': t('Режим Roleplay-PvP придёт в WoW Forever', 'Roleplay-PvP ruleset is coming to WoW Forever', 'Режим Roleplay-PvP прийде в WoW Forever'),
     'text': t('Blizzard объявила на форуме, что режим Roleplay-PvP появится в WoW Forever. Подробностей, которые мы могли бы проверить, в сообщении нет: правила смотрите в самом сообщении.',
               'Blizzard announced on the forum that the Roleplay-PvP ruleset is coming to WoW Forever. The post gives no further details we could verify, so check the linked post for the rules.',
               'Blizzard оголосила на форумі, що режим Roleplay-PvP з’явиться у WoW Forever. Подробиць, які ми могли б перевірити, у повідомленні немає: правила дивіться в самому повідомленні.'),
     'so': t('Roleplay-PvP — один из четырёх режимов на выбор.',
             'Roleplay-PvP is one of the four rulesets to pick from.',
             'Roleplay-PvP — один із чотирьох режимів на вибір.')},
    {'date': '2026-10-27', 'cls': 'all', 'url': 'https://news.blizzard.com/en-us/article/24303866',
     'title': t('Старт резерва в Европе задерживался', 'Name reservation start delayed in Europe', 'Старт резерву в Європі затримувався'),
     'text': t('27.10 Blizzard сообщила в лаунчере Battle.net, что старт резерва имён в Европе (по плану в 19:00 по Киеву) задерживается из-за технических проблем. Позже в тот же день резерв заработал в Европе и Америке. По уведомлению в лаунчере и обновлению Wowhead от 27.10.',
               'On 27.10 Blizzard said in the Battle.net launcher that the start of name reservation in Europe (planned for 19:00 Kyiv time) was delayed by technical issues. Later that day the reservation went live in Europe and the Americas. Based on the launcher notice and the Wowhead update of 27.10.',
               '27.10 Blizzard повідомила в лаунчері Battle.net, що старт резерву імен у Європі (за планом о 19:00 за Києвом) затримується через технічні проблеми. Пізніше того ж дня резерв запрацював у Європі та Америці. За повідомленням у лаунчері та оновленням Wowhead від 27.10.'),
     'so': t('Окно резерва прежнее: 27.10 – 03.11.',
             'The reservation window is still 27.10 – 03.11.',
             'Вікно резерву те саме: 27.10 – 03.11.')},
    {'date': '2026-10-26', 'cls': 'all', 'url': 'https://us.forums.blizzard.com/en/wow/t/2360696/7',
     'title': t('Последние правки рас перед стартом', 'Final racial changes before launch', 'Останні зміни рас перед стартом'),
     'text': t('Заметки разработчиков 26.10. Человек: Беспощадность +1% крита (было 2%), Человеческий дух +10% к духу (было 5%). Дворф: Ярость земли убрана, вместо неё Artisan’s Precision, +1% к меткости. Таурен: Бег по равнинам +2% скорости за заряд, до +60% (было 30%), на езду верхом больше не действует; Закалка — только +5% здоровья. Орк: Дикость убрана, вернулась Властность, +5% к урону питомцев чернокнижника и охотника. Скайборн: Благословение ветра +2% (было 3%), Чтение лей-линий +50% на 15 сек, Взгляд в небо +15% на 15 сек, у лей-линии и Elemental Convergence — сильнее на час. Оружейные специализации не вернутся.',
               'Developer notes, Oct 26. Human: Ruthless +1% crit (was 2%), The Human Spirit +10% Spirit (was 5%). Dwarf: Earth Fury removed, replaced by Artisan’s Precision, +1% hit chance. Tauren: Plainsrunning +2% speed per stack, up to +60% (was 30%), no longer affects mounted speed; Endurance is now only +5% health. Orc: Savage removed, Command returns, +5% Warlock and Hunter pet damage. Skyborne: Wind Blessed +2% (was 3%), Read Ley Line +50% for 15 sec, Skysight +15% for 15 sec, stronger for an hour at a Ley Line or Elemental Convergence. Weapon specializations are not coming back.',
               'Нотатки розробників 26.10. Людина: Ruthless +1% криту (було 2%), The Human Spirit +10% до духу (було 5%). Дворф: Earth Fury прибрали, замість неї Artisan’s Precision, +1% до влучності. Таурен: Plainsrunning +2% швидкості за заряд, до +60% (було 30%), на їзду верхи більше не діє; Endurance — лише +5% здоров’я. Орк: Savage прибрали, повернули Command, +5% шкоди улюбленців чорнокнижника й мисливця. Скайборн: Wind Blessed +2% (було 3%), Read Ley Line +50% на 15 сек, Skysight +15% на 15 сек, біля Ley Line та Elemental Convergence — сильніше на годину. Спеціалізації зброї не повернуть.'),
     'so': t('Таблицы рас и «Лучшая раса» на сайте уже по этим правкам.',
             'The race tables and Best Race on this site already follow these changes.',
             'Таблиці рас і «Найкраща раса» на сайті вже за цими змінами.')},
    {'date': '2026-10-23', 'url': 'https://worldofwarcraft.blizzard.com/en-us/news/24313106',
     'title': t('Резерв имён: время открытия по регионам', 'Name reservation: opening times by region', 'Резерв імен: час відкриття за регіонами'),
     'text': t('Резерв имён идёт с 27.10 по 03.11. Старт по Киеву: Европа — 27.10 в 19:00, Америка — 27.10 в 22:00, Корея — 28.10 в 00:00, Тайвань — 28.10 в 01:00. Резерв — для предзаказа Skyborne Heroic, Skyborne Epic или Warcraft Forever Collection: до трёх персонажей на аккаунт во всех режимах вместе.',
               'Name reservation runs from 27.10 to 03.11. Start in Kyiv time: Europe 27.10 at 19:00, the Americas 27.10 at 22:00, Korea 28.10 at 00:00, Taiwan 28.10 at 01:00. It is for Skyborne Heroic, Skyborne Epic or Warcraft Forever Collection pre-purchases: up to three characters per account across all rulesets.',
               'Резерв імен триває з 27.10 по 03.11. Старт за Києвом: Європа — 27.10 о 19:00, Америка — 27.10 о 22:00, Корея — 28.10 о 00:00, Тайвань — 28.10 о 01:00. Резерв — для передзамовлення Skyborne Heroic, Skyborne Epic або Warcraft Forever Collection: до трьох персонажів на акаунт у всіх режимах разом.'),
     'so': t('Имена раздают по принципу «кто первый»: редкое берите в первый час.',
             'Names go first come, first served: take a rare one in the first hour.',
             'Імена роздають за принципом «хто перший»: рідкісне беріть у першу годину.')},
    {'date': '2026-10-23', 'url': 'https://eu.forums.blizzard.com/en/wow/t/637228',
     'title': t('Бета закрыта, старт 04.11', 'Beta closed, launch on 04.11', 'Бету закрито, старт 04.11'),
     'text': t('Blizzard закрыла бету 23.10 в 10:00 по тихоокеанскому времени (17:00 UTC). До 27.10 команда чинит главные ошибки и серверы. С 27.10 открывается создание персонажей: режим и имя выбирают заранее. Старт игры — 04.11.',
               'Blizzard closed the beta on 23.10 at 10:00 Pacific time (17:00 UTC). Until 27.10 the team fixes priority issues and the game service. From 27.10 character creation opens: the ruleset and the name are chosen in advance. The game launches on 04.11.',
               'Blizzard закрила бету 23.10 о 10:00 за тихоокеанським часом (17:00 UTC). До 27.10 команда виправляє головні помилки й сервери. З 27.10 відкривається створення персонажів: режим та ім’я обирають заздалегідь. Старт гри — 04.11.'),
     'so': t('Режим и имя выбираются до старта, а не в день запуска.',
             'The ruleset and the name are chosen before launch, not on launch day.',
             'Режим та ім’я обирають до старту, а не в день запуску.')},
    {'date': '2026-10-15', 'cls': 'all', 'url': 'https://us.forums.blizzard.com/en/wow/t/2360696/6',
     'title': t('Крупный патч беты: расы и классы', 'Major beta patch: races and classes', 'Великий патч бети: раси та класи'),
     'text': t('Способности рас переделаны (оружейные специализации заменены критами), настроены почти все классы. Таблицы рас и классов на сайте уже по этому патчу.',
               'Racial abilities were reworked (weapon specializations replaced with crits), almost all classes were tuned. The race and class tables on this site already follow this patch.',
               'Здібності рас перероблено (спеціалізації зброї замінено критами), налаштовано майже всі класи. Таблиці рас і класів на сайті вже за цим патчем.'),
     'so': t('Таблицы рас и классов на сайте уже по этому патчу.',
             'The race and class tables on this site already follow this patch.',
             'Таблиці рас і класів на сайті вже за цим патчем.')},
    {'date': '2026-09-25', 'url': 'https://us.forums.blizzard.com/en/wow/t/what-insights-would-you-like-to-see-in-a-future-episode-of-the-wow-forever-podcast/2361993/1',
     'title': t('Подкаст WoW Forever: чего вы ждёте от следующего выпуска', 'What would you like to see in a future WoW: Forever Podcast episode', 'Подкаст WoW Forever: чого ви чекаєте від наступного випуску'),
     'text': t('Разработчик Blizzard спросил на форуме, какие темы игроки хотели бы увидеть в будущем выпуске подкаста WoW: Forever. Подробностей, которые мы могли бы проверить, в сообщении нет: детали смотрите в самом сообщении.',
               'A Blizzard developer asked on the forum which insights players would like to see in a future episode of the WoW: Forever Podcast. The post gives no further details we could verify, so check the linked post.',
               'Розробник Blizzard запитав на форумі, які теми гравці хотіли б побачити в майбутньому випуску подкасту WoW: Forever. Подробиць, які ми могли б перевірити, у повідомленні немає: деталі дивіться в самому повідомленні.'),
     'so': t('Темы для подкаста можно предложить в сообщении Blizzard.',
             'You can suggest podcast topics in the Blizzard post.',
             'Теми для подкасту можна запропонувати в повідомленні Blizzard.')},
    {'date': '2026-10-08', 'url': 'https://classicwow.gg/forever',
     'title': t('В бете Даларан и больше опыта в подземельях', 'Dalaran and more dungeon experience in the beta', 'У беті Даларан і більше досвіду в підземеллях'),
     'text': t('В бету добавили [[Даларан|City of Dalaran]] и примерно на 20% больше опыта за врагов в подземельях.',
               'The beta got City of Dalaran and about 20% more experience for enemies in dungeons.',
               'У бету додали City of Dalaran і приблизно на 20% більше досвіду за ворогів у підземеллях.')},
]

GUIDES.append({
    'slug': 'news', 'art': 'paladin', 'hero': 'hero_news', 'js': 'news',
    'title': t('Новости', 'News', 'Новини'),
    'lead': t('Главное о WoW Forever и свежая лента Wowhead.',
              'What matters for our game in WoW Forever, plus the latest Wowhead feed.',
              'Що важливо для нашої гри у WoW Forever, і свіжа стрічка Wowhead.'),
    'tile': t('Наши записи и лента Wowhead', 'Our notes and the Wowhead feed', 'Наші записи та стрічка Wowhead'),
    'pills': [t('Лента обновляется каждые 6 часов', 'Feed updates every 6 hours', 'Стрічка оновлюється кожні 6 годин')],
    'sources': [
        ('Wowhead News', 'https://www.wowhead.com/news'),
        (t('Blizzard: заметки разработчиков беты Forever', 'Blizzard: WoW Forever beta development notes', 'Blizzard: нотатки розробників бети Forever'), 'https://us.forums.blizzard.com/en/wow/t/2360696/7'),
        (t('Warcraft Tavern: изменения рас и классов', 'Warcraft Tavern: racial and class changes', 'Warcraft Tavern: зміни рас і класів'),
         'https://www.warcrafttavern.com/forever/news/racial-class-ability-changes-in-the-wow-forever-beta/'),
        ('ClassicWoW.gg', 'https://classicwow.gg/forever'),
        ('Blizzard: Claim Your World of Warcraft: Forever Character Names', NR_URL),
        (t('Blizzard: резерв имён по регионам', 'Blizzard: name reservation by region', 'Blizzard: резерв імен за регіонами'), 'https://worldofwarcraft.blizzard.com/en-us/news/24313106'),
        (t('Blizzard: бета закрыта', 'Blizzard: the beta is closed', 'Blizzard: бету закрито'), 'https://eu.forums.blizzard.com/en/wow/t/637228'),
        (t('Blizzard: меры против ботов и RMT', 'Blizzard: actions against botting and RMT', 'Blizzard: заходи проти ботів і RMT'), 'https://us.forums.blizzard.com/en/wow/t/actions-taken-against-botting-and-rmt/2368705/1'),
        (t('Blizzard: техработы на реалмах беты', 'Blizzard: beta realm maintenance', 'Blizzard: технічні роботи на реалмах бети'), 'https://us.forums.blizzard.com/en/wow/t/beta-realm-maintenance-october-15/2383475/1'),
        (t('Blizzard: Return to Azeroth', 'Blizzard: Return to Azeroth', 'Blizzard: Return to Azeroth'), 'https://worldofwarcraft.blizzard.com/en-us/news/24315643/return-to-azeroth-in-world-of-warcraft-forever'),
        (t('Blizzard: WoW Forever Goes Live Globally', 'Blizzard: WoW Forever Goes Live Globally', 'Blizzard: WoW Forever Goes Live Globally'), 'https://worldofwarcraft.blizzard.com/en-us/news/24315820/world-of-warcraft-forever-goes-live-globally-november-4'),
        (t('Blizzard: стартовый гид для новичков', 'Blizzard: new player\'s starter guide', 'Blizzard: стартовий гід для новачків'), 'https://worldofwarcraft.blizzard.com/en-us/news/24315280/new-players-starter-guide-welcome-to-world-of-warcraft-forever'),
        (t('Blizzard: выбор режима', 'Blizzard: choose your ruleset', 'Blizzard: вибір режиму'), 'https://worldofwarcraft.blizzard.com/en-us/news/24302070/choose-your-ruleset-in-world-of-warcraft-forever'),
        (t('Blizzard: подкаст WoW Forever', 'Blizzard: WoW Forever Podcast', 'Blizzard: подкаст WoW Forever'), 'https://us.forums.blizzard.com/en/wow/t/what-insights-would-you-like-to-see-in-a-future-episode-of-the-wow-forever-podcast/2361993/1'),
    ],
    'sections': [
        {'id': 'ours', 'title': t('Наши записи', 'Our notes', 'Наші записи'), 'blocks': [('news', None)]},
        {'id': 'feed', 'title': t('Лента Wowhead', 'Wowhead feed', 'Стрічка Wowhead'), 'blocks': [
            ('text', [t('Новости про Forever с Wowhead, на английском. Список обновляется сам.',
                        'Forever news from Wowhead, in English. The list updates by itself.',
                        'Новини про Forever з Wowhead, англійською. Список оновлюється сам.')]),
            ('raw', t('<div class="nlist" id="feedList" hidden></div><p><a class="more-l" href="https://www.wowhead.com/news" target="_blank" rel="noopener">Все новости Wowhead</a></p>',
                      '<div class="nlist" id="feedList" hidden></div><p><a class="more-l" href="https://www.wowhead.com/news" target="_blank" rel="noopener">All Wowhead news</a></p>',
                      '<div class="nlist" id="feedList" hidden></div><p><a class="more-l" href="https://www.wowhead.com/news" target="_blank" rel="noopener">Усі новини Wowhead</a></p>')),
        ]},
    ],
})


# ---------- Як грати українською: только uk ('only'), тексты — словари {'uk': …} ----------
# Факты: CurseForge и README аддонов (23.10.2026). Без версий и числа скачиваний — они быстро устаревают.

def u(s):
    return {'uk': s}


UAF = 'https://www.curseforge.com/wow/addons/ua-forever'
UALL = 'https://www.curseforge.com/wow/addons/uall-forever-ukrainian-localization'

GUIDES.append({
    'slug': 'ukrainian', 'only': 'uk', 'art': 'hero_ukrainian', 'hero': 'hero_ukrainian',
    'title': u('Як грати українською'),
    'lead': u('Української мови у WoW Forever немає, перекладає гру аддон. Який обрати, як встановити й налаштувати, де побачити оригінал.'),
    'tile': u('Аддони перекладу: який обрати й як встановити'),
    'pills': [u('UA_Forever'), u('UALL Forever'), u('Shift — оригінал')],
    'sources': [
        (u('CurseForge: UA_Forever'), UAF),
        (u('UA_Forever на GitHub: опис і команди'), 'https://github.com/sysrover/UA_Forever'),
        (u('CurseForge: UALL Forever'), UALL),
        (u('ClassicUA на GitHub'), 'https://github.com/greenya/ClassicUA'),
        (u('WoWGuide: мови WoW Forever'), 'https://wowguide.net/en/guides/wow-forever-supported-languages'),
    ],
    'sections': [
        {'id': 'short', 'title': u('Коротко'), 'blocks': [
            ('text', [u('Ставте UA_Forever. Він перекладає завдання, підказки, предмети, заклинання, імена NPC і вікна гри, а речення узгоджує з родом героя: «ви дав» чи «ви дала», залежно від персонажа.'),
                      u('Встановлення через CurseForge займає кілька хвилин. Оригінал англійською завжди під рукою: затисніть Shift.')]),
            ('raw', u(f'<p class="gbtns"><a class="btn" href="{UAF}" target="_blank" rel="noopener">UA_Forever на CurseForge ↗</a>'
                      '<a class="btn ghost" href="#install">Як встановити</a></p>')),
        ]},
        {'id': 'client', 'title': u('Мова гри'), 'blocks': [
            ('text', [u('Клієнт WoW Forever доступний десятьма мовами, серед них англійська та російська. Української серед них немає.'),
                      u('Аддон підміняє тексти лише на вашому екрані. Інші гравці бачать гру своєю мовою, на правила й бої переклад не впливає.'),
                      u('UALL Forever працює лише з англійським клієнтом. Мову змінюють у лаунчері Battle.net: налаштування гри, мова тексту.')]),
        ]},
        {'id': 'choose', 'title': u('UA_Forever чи UALL Forever'), 'blocks': [
            ('text', [u('На CurseForge два аддони українізації Forever з майже однаковою кількістю завантажень. Відрізняються вони сильно.')]),
            ('table', {'head': [u(''), u('UA_Forever'), u('UALL Forever')], 'rows': [
                [u('Основа'), u('ClassicUA: переклад спільноти, над ним працювали понад 30 перекладачів і редакторів'), u('Власний переклад автора')],
                [u('Обсяг'), u('Завдання, предмети, заклинання, аури, репліки NPC, книги, вікна'), u('Те саме, але предметів перекладено майже вчетверо менше')],
                [u('Рід героя'), u('Форми за статтю персонажа: «дав» або «дала»'), u('Завжди чоловічий рід')],
                [u('Назви'), u('Перекладені: Залізогарт, Підмістя, Молотобій'), u('Транслітерація: Айронфордж, Андерсіті, Гаммерфолл')],
                [u('Оригінал'), u('Shift у підказці, EN/UA у діалогах завдань'), u('Shift')],
                [u('Мова клієнта'), u('Вимог не вказано'), u('Лише англійська')],
                [u('Налаштування'), u('Налаштування → Додатки → UA Forever, команда /uaf'), u('Esc → Options → AddOns → UALLF, команда /uallfua')],
                [u('Код'), u('Відкритий, ліцензія GPLv3'), u('Закритий')],
            ]}),
            ('text', [u('UA_Forever перекладає більше й звучить природніше завдяки родам і перекладеним назвам. Слабкі місця: місцями дослівний текст, поодинокі помилки, у цілях завдань звертання на «ви» при «ти» в самому тексті.'),
                      u('UALL Forever читається рівніше, але назви транслітом, у предметах трапляються Англійські Великі Літери, а переклад і транслітерація змішуються: Пустограй поруч зі Срібноліссям.')]),
            ('tip', u('На цьому сайті ігрові назви англійською, як в оригінальному клієнті: так їх пишуть Wowhead, гайди й гравці в групі. Затисніть Shift на підказці, щоб звірити назву з аддоном.')),
        ]},
        {'id': 'install', 'title': u('Встановлення'), 'blocks': [
            ('steps', [
                {'t': u('CurseForge'), 'd': u('Встановіть застосунок CurseForge, оберіть World of Warcraft і версію Forever. Знайдіть UA_Forever і натисніть Install, оновлення застосунок ставитиме сам.')},
                {'t': u('Або вручну'), 'd': u('Завантажте архів зі сторінки аддона й розпакуйте так, щоб папка UA_Forever опинилася в Interface\\AddOns у теці гри Forever.')},
                {'t': u('Увімкнення'), 'd': u('На екрані вибору персонажа відкрийте AddOns і поставте позначку. Якщо аддон позначено застарілим, увімкніть Load out of date AddOns.')},
                {'t': u('Перевірка'), 'd': u('Якщо гра вже запущена, введіть /reload у чаті. Підказки й вікна завдань мають стати українськими.')},
            ]),
            ('tip', u('Вмикайте один аддон перекладу. Обидва підміняють ті самі вікна й заважають один одному.')),
            ('tiles', [{'t': u('Аддони та інтерфейс'), 'd': u('Що працює, що вбудовано, як ставити'), 'href': 'guides/addons/', 'art': 'hero_roster'}]),
        ]},
        {'id': 'setup', 'title': u('Налаштування й оригінал'), 'blocks': [
            ('table', {'head': [u(''), u('UA_Forever'), u('UALL Forever')], 'rows': [
                [u('Побачити оригінал'), u('Затиснути Shift на підказці'), u('Затиснути Shift')],
                [u('Діалог завдання англійською'), u('Перемикач EN/UA у вікні діалогу'), u('Shift')],
                [u('Увімкнути чи вимкнути переклад'), u('/uaf on, /uaf off'), u('Перемикачі в Esc → Options → AddOns → UALLF')],
                [u('Стан перекладу'), u('/uaf status'), u('/uallfua')],
                [u('Вимкнути окремі частини'), u('Налаштування → Додатки → UA Forever'), u('/uallfua list')],
            ]}),
        ]},
        {'id': 'help', 'title': u('Неперекладений текст'), 'blocks': [
            ('text', [u('Forever змінює частину класичних завдань і заклинань, тому старий переклад місцями відстає, а нові тексти з’являються з оновленнями аддона.'),
                      u('UA_Forever збирає неперекладене сам. У налаштуваннях аддона увімкніть автоскан і пограйте. Там само відкрийте зібрані дані, скопіюйте їх і надішліть через форму, посилання на яку є на сторінці аддона на GitHub. Без вас нічого не відправляється.')]),
        ]},
        {'id': 'questions', 'title': u('Часті питання'), 'blocks': [
            ('faq', [
                {'id': 'ban', 'q': u('Чи можуть заблокувати за аддон перекладу?'),
                 'a': [u('Аддони інтерфейсу Blizzard дозволяє. Перекладач лише змінює текст на вашому екрані й не автоматизує гру.')]},
                {'id': 'others', 'q': u('Чи побачать переклад інші гравці?'),
                 'a': [u('Ні, переклад працює тільки у вас. Назви в чаті групи пишіть англійською: так їх зрозуміють усі.')]},
                {'id': 'outdated', 'q': u('Після патча аддон позначено застарілим. Що робити?'),
                 'a': [u('Увімкніть Load out of date AddOns на екрані вибору персонажа й оновіть аддон через CurseForge, коли вийде нова версія.')]},
                {'id': 'russian', 'q': u('Чи працює UA_Forever з російським клієнтом?'),
                 'a': [u('Автор вимог до мови клієнта не вказує. Якщо частина тексту лишається неперекладеною, поставте англійську мову в лаунчері Battle.net.')]},
            ]),
        ]},
    ],
})

# ---------- Лучшая раса, тир-лист и Legacy (тексты 25.10.2026, переводы в i18n/*.json) ----------

# ---------- best-race ----------

GUIDES.append({
    'slug': 'best-race', 'art': 'hero_bestrace', 'hero': 'hero_bestrace',
    'title': t('Лучшая раса для каждого класса', 'Best Race for Every Class', 'Найкраща раса для кожного класу'),
    'crumb': t('Лучшая раса', 'Best race', 'Найкраща раса'),   # breadcrumb: the long title left «класса» alone on a 375 px line
    'lead': t('За Альянс чаще всего выигрывают Человек, Гном и Ночной эльф, за Орду — Орк в PvE и Нежить в PvP. Разница между расами — несколько процентов: класс, спек и экипировка важнее.', 'On the Alliance side Human, Gnome and Night Elf win most often; on the Horde side it is Orc in PvE and Undead in PvP. The gap between races is a few percent: class, spec and gear matter more.', 'За Альянс найчастіше перемагають Людина, Гном і Нічний ельф, за Орду — Орк у PvE та Нежить у PvP. Різниця між расами становить кілька відсотків: клас, спеціалізація й екіпірування важать більше.'),
    'tile': t('Какая раса сильнее для вашего класса', 'Which race is stronger for your class', 'Яка раса сильніша для вашого класу'),
    'pills': [t('56 пар класс и раса', '56 class and race pairs', '56 пар клас і раса'), t('PvE и PvP', 'PvE and PvP', 'PvE та PvP'), t('По бете', 'Beta data', 'За бетою')],
    'sources': [
        (t('Icy Veins: расы Forever', 'Icy Veins: Forever races', 'Icy Veins: раси Forever'), 'https://www.icy-veins.com/wow-forever/race-guide'),
        (t('Warcraft Tavern: расовые способности', 'Warcraft Tavern: racial abilities', 'Warcraft Tavern: расові здібності'), 'https://www.warcrafttavern.com/forever/guides/races/'),
        (t('Blizzard: заметки разработчиков беты Forever', 'Blizzard: WoW Forever beta development notes', 'Blizzard: нотатки розробників бети Forever'), 'https://us.forums.blizzard.com/en/wow/t/2360696/7'),
        (t('Warcraft Tavern: изменения беты от 15 октября', 'Warcraft Tavern: Oct 15 beta changes', 'Warcraft Tavern: зміни бети від 15 жовтня'), 'https://www.warcrafttavern.com/forever/news/racial-class-ability-changes-in-the-wow-forever-beta/'),
        (t('RankedBoost: расы по классам', 'RankedBoost: races by class', 'RankedBoost: раси за класами'), 'https://rankedboost.com/world-of-warcraft/forever/tier-list/'),
        (t('wowforevertierlist: лучшая раса для класса', 'wowforevertierlist: best race for each class', 'wowforevertierlist: найкраща раса для класу'), 'https://wowforevertierlist.com/races/best-race-for-each-class'),
        (t('ConquestCapped: тир-лист рас', 'ConquestCapped: race tier list', 'ConquestCapped: тір-лист рас'), 'https://conquestcapped.com/guides/wow-forever/wow-forever-race-tier-list/'),
        (t('mmonster: тир-лист рас', 'mmonster: race tier list', 'mmonster: тір-лист рас'), 'https://mmonster.co/wow-forever/guides/tier-lists/race-tier-list'),
        (t('GamesFuze: лучшая раса для класса', 'GamesFuze: best race for each class', 'GamesFuze: найкраща раса для класу'), 'https://gamesfuze.com/tier-list/world-of-warcraft-forever-best-race-for-every-class/'),
        (t('gamer-guides: тир-лист беты', 'gamer-guides: beta tier list', 'gamer-guides: тір-лист бети'), 'https://gamer-guides.com/warcraft-forever/tier-list-beta/'),
        (t('Wowhead Classic: Blood Fury (числа Classic)', 'Wowhead Classic: Blood Fury (Classic numbers)', 'Wowhead Classic: Blood Fury (числа Classic)'), 'https://www.wowhead.com/classic/spell=20572/blood-fury'),
        (t('Wowhead Classic: Hardiness (числа Classic)', 'Wowhead Classic: Hardiness (Classic numbers)', 'Wowhead Classic: Hardiness (числа Classic)'), 'https://www.wowhead.com/classic/spell=20573/hardiness'),
        (t('LFCarry: изменения классов', 'LFCarry: class changes', 'LFCarry: зміни класів'), 'https://lfcarry.com/guides/wow-forever-class-changes'),
    ],
    'sections': [
        {'id': 'table', 'title': t('Лучшие сочетания расы и класса', 'Best race and class combos', 'Найкращі комбінації раси й класу'), 'blocks': [
            ('text', [t('Данные по бете (уровень 30, сборки до 15.10). Полей боя на бете не было, поэтому PvP оценено по дуэлям и мировому PvP. «Или» — источники спорят, одного победителя нет.', 'Beta data (level 30, builds up to Oct 15). There were no battlegrounds in the beta, so PvP is judged by duels and world PvP. “Or” means the sources disagree and there is no single winner.', 'Дані за бетою (30 рівень, збірки до 15 жовтня). Полів бою в бета-версії не було, тож PvP оцінено за дуелями та світовим PvP. «Або» означає, що джерела сперечаються і єдиного переможця немає.'),
                      t('Рейтинги источников собраны до последних правок рас Blizzard 26.10: Орк потерял Дикость (+1% крита), Дворф — Ярость земли, Беспощадность Человека ослабла до +1% крита. Цифры способностей ниже уже по 26.10. Рейтинги обновим, когда их пересчитают источники.', 'The source rankings were made before Blizzard’s final racial changes on Oct 26: Orc lost Savage (+1% crit), Dwarf lost Earth Fury, and Human Ruthless dropped to +1% crit. The ability numbers below already follow Oct 26. We will update the rankings once the sources recalculate them.', 'Рейтинги джерел зібрано до останніх змін рас Blizzard 26.10: Орк втратив Savage (+1% криту), Дворф — Earth Fury, а Ruthless Людини послабили до +1% криту. Цифри здібностей нижче вже за 26.10. Рейтинги оновимо, коли їх перерахують джерела.')]),
            ('table', {'head': [t('Класс', 'Class', 'Клас'), t('Альянс, PvE', 'Alliance, PvE', 'Альянс, PvE'), t('Орда, PvE', 'Horde, PvE', 'Орда, PvE'), t('Альянс, PvP', 'Alliance, PvP', 'Альянс, PvP'), t('Орда, PvP', 'Horde, PvP', 'Орда, PvP')], 'rows': [
                [t('Воин', 'Warrior', 'Воїн'), t('Человек или Ночной эльф; танк — Дворф', 'Human or Night Elf; tank: Dwarf', 'Людина або Нічний ельф; танк — Дворф'), t('Орк; танк — Таурен', 'Orc; tank: Tauren', 'Орк; танк — Таурен'), t('Человек', 'Human', 'Людина'), t('Орк', 'Orc', 'Орк')],
                [t('Паладин', 'Paladin', 'Паладин'), t('Человек; танк — Дворф', 'Human; tank: Dwarf', 'Людина; танк — Дворф'), t('Нежить (единственная)', 'Undead (the only option)', 'Нежить (єдина)'), t('Человек или Дворф', 'Human or Dwarf', 'Людина або Дворф'), t('Нежить', 'Undead', 'Нежить')],
                [t('Охотник', 'Hunter', 'Мисливець'), t('Человек или Ночной эльф', 'Human or Night Elf', 'Людина або Нічний ельф'), t('Орк или Тролль', 'Orc or Troll', 'Орк або Троль'), t('Человек', 'Human', 'Людина'), t('Орк', 'Orc', 'Орк')],
                [t('Разбойник', 'Rogue', 'Розбійник'), t('Ночной эльф', 'Night Elf', 'Нічний ельф'), t('Орк', 'Orc', 'Орк'), t('Человек или Гном', 'Human or Gnome', 'Людина або Гном'), t('Нежить или Орк', 'Undead or Orc', 'Нежить або Орк')],
                [t('Жрец', 'Priest', 'Жрець'), t('Гном', 'Gnome', 'Гном'), t('Нежить или Тролль', 'Undead or Troll', 'Нежить або Троль'), t('Гном или Человек', 'Gnome or Human', 'Гном або Людина'), t('Нежить', 'Undead', 'Нежить')],
                [t('Шаман', 'Shaman', 'Шаман'), t('Дворф (единственный)', 'Dwarf (the only option)', 'Дворф (єдиний)'), t('Орк; лекарь — Тролль', 'Orc; healer: Troll', 'Орк; цілитель — Троль'), t('Дворф (единственный)', 'Dwarf (the only option)', 'Дворф (єдиний)'), t('Орк, Таурен или Тролль', 'Orc, Tauren or Troll', 'Орк, Таурен або Троль')],
                [t('Маг', 'Mage', 'Маг'), t('Гном', 'Gnome', 'Гном'), t('Орк', 'Orc', 'Орк'), t('Гном', 'Gnome', 'Гном'), t('Нежить', 'Undead', 'Нежить')],
                [t('Чернокнижник', 'Warlock', 'Чорнокнижник'), t('Гном или Человек', 'Gnome or Human', 'Гном або Людина'), t('Орк или Нежить', 'Orc or Undead', 'Орк або Нежить'), t('Человек', 'Human', 'Людина'), t('Нежить', 'Undead', 'Нежить')],
                [t('Друид', 'Druid', 'Друїд'), t('Ночной эльф', 'Night Elf', 'Нічний ельф'), t('Таурен', 'Tauren', 'Таурен'), t('Ночной эльф', 'Night Elf', 'Нічний ельф'), t('Таурен', 'Tauren', 'Таурен')],
            ]}),
            ('tip', t('Не можете выбрать — берите расу, которая нравится: несколько процентов урона не заменят персонажа, которым приятно играть до 60.', 'Can’t decide? Take the race you like: a few percent of damage won’t replace a character you enjoy playing all the way to 60.', 'Не можете обрати — беріть расу, яка подобається: кілька відсотків шкоди не замінять персонажа, за якого приємно грати до 60 рівня.')),
        ]},
        {'id': 'classes', 'title': t('Лучшая раса по классам', 'Best race by class', 'Найкраща раса за класами'), 'blocks': [
            ('steps', [
                {'id': 'warrior', 't': t('Лучшая раса для Воина', 'Best race for Warrior', 'Найкраща раса для Воїна'),
                 'd': t('Человек: Беспощадность даёт +1% крита любым оружием, Воля к жизни снимает оглушения. Ночной эльф: Свет Элуны, +10% крита на 15 сек. Источники делятся почти поровну. Танку — Дворф: Каменная форма снижает физический урон на 10% и снимает кровотечения. За Орду Орка ставят первым все источники: Кровавое неистовство (+10% силы атаки на 15 сек), Твердость (оглушения короче на 20%). Танку — Таурен: Закалка (+5% здоровья) и Громовая поступь.', 'Human: Ruthless gives +1% crit with any weapon, Will to Survive removes stuns. Night Elf: Elune’s Light, +10% crit for 15 sec. The sources are almost evenly split. For a tank, take Dwarf: Stoneform cuts physical damage by 10% and removes bleeds. On the Horde side every source puts Orc first: Blood Fury (+10% attack power for 15 sec), Hardiness (stuns 20% shorter). For a tank, take Tauren: Endurance (+5% health) and War Stomp.', 'Людина: Ruthless дає +1% криту будь-якою зброєю, Will to Survive знімає приголомшення. Нічний ельф: Elune’s Light, +10% криту на 15 с. Джерела розділилися майже порівну. Танку — Дворф: Stoneform зменшує фізичну шкоду на 10% і знімає кровотечі. За Орду всі джерела ставлять першим Орка: Blood Fury (+10% сили атаки на 15 с), Hardiness (приголомшення коротші на 20%). Танку — Таурен: Endurance (+5% здоров’я) і War Stomp.')},
                {'id': 'paladin', 't': t('Лучшая раса для Паладина', 'Best race for Paladin', 'Найкраща раса для Паладина'),
                 'd': t('Человек: Беспощадность усиливает и удары, и заклинания, Воля к жизни снимает оглушения. Для Защиты — Дворф: Каменная форма и Artisan’s Precision (+1% к меткости). В PvP один источник из четырёх выбирает Дворфа. За Орду паладином может быть только Нежить, это новое сочетание Forever. Каннибализм возвращает ману, Воля Отрекшихся снимает страх.', 'Human: Ruthless boosts both strikes and spells, Will to Survive removes stuns. For Protection, take Dwarf: Stoneform and Artisan’s Precision (+1% hit chance). In PvP one source out of four picks Dwarf. On the Horde side only Undead can be a paladin; this is a new Forever combination. Cannibalize restores mana, Will of the Forsaken removes fear.', 'Людина: Ruthless підсилює і удари, і закляття, Will to Survive знімає приголомшення. Для Захисту — Дворф: Stoneform і Artisan’s Precision (+1% до влучності). У PvP одне джерело з чотирьох обирає Дворфа. За Орду паладином може бути лише Нежить, це нова комбінація Forever. Cannibalize повертає ману, Will of the Forsaken знімає страх.')},
                {'id': 'hunter', 't': t('Лучшая раса для Охотника', 'Best race for Hunter', 'Найкраща раса для Мисливця'),
                 'd': t('Охотник-человек — новое сочетание Forever: Беспощадность даёт +1% крита, и питомец наследует крит. Ночной эльф отвечает Светом Элуны и Слиться с тенью. Один свежий источник (24.10) ставит первым Дворфа за Охотника на крупную дичь: +5% урона по зверям. За Орду — Орк (Кровавое неистовство, Властность: +5% к урону питомца) или Тролль (Убийство животных, +5% по зверям). В PvP Таурену помогает Громовая поступь.', 'The human hunter is a new Forever combination: Ruthless gives +1% crit, and the pet inherits the crit. Night Elf answers with Elune’s Light and Shadowmeld. One recent source (Oct 24) puts Dwarf first for its Big Game Hunter: +5% damage against beasts. On the Horde side it is Orc (Blood Fury, Command: +5% pet damage) or Troll (Beast Slaying, +5% against beasts). In PvP, War Stomp helps Tauren.', 'Мисливець-людина — нова комбінація Forever: Ruthless дає +1% криту, а улюбленець успадковує кріт. Нічний ельф відповідає Elune’s Light і Shadowmeld. Одне свіже джерело (24 жовтня) ставить першим Дворфа за Big Game Hunter: +5% шкоди по звірах. За Орду — Орк (Blood Fury, Command: +5% шкоди улюбленця) або Троль (Beast Slaying, +5% по звірах). У PvP Тауренові допомагає War Stomp.')},
                {'id': 'rogue', 't': t('Лучшая раса для Разбойника', 'Best race for Rogue', 'Найкраща раса для Розбійника'),
                 'd': t('Ночной эльф: Слиться с тенью теперь снижает угрозу и в бою, плюс Свет Элуны и Расторопность. Человек: крит любым оружием, Внимательность вскрывает чужих разбойников. В PvP Альянса единого ответа нет: Гном снимает корни и замедления Мастером побега. За Орду — Орк в PvE. В PvP чаще Нежить: Воля Отрекшихся снимает страх жрецов и чернокнижников.', 'Night Elf: Shadowmeld now lowers threat in combat too, plus Elune’s Light and Quickness. Human: crit with any weapon, and Perception reveals enemy rogues. In Alliance PvP there is no single answer: Gnome breaks roots and slows with Escape Artist. On the Horde side it is Orc in PvE. In PvP it is more often Undead: Will of the Forsaken removes fear from priests and warlocks.', 'Нічний ельф: Shadowmeld тепер знижує загрозу і в бою, плюс Elune’s Light і Quickness. Людина: кріт будь-якою зброєю, а Perception виявляє чужих розбійників. У PvP Альянсу єдиної відповіді немає: Гном знімає корені та уповільнення через Escape Artist. За Орду — Орк у PvE. У PvP частіше Нежить: Will of the Forsaken знімає страх жерців і чорнокнижників.')},
                {'id': 'priest', 't': t('Лучшая раса для Жреца', 'Best race for Priest', 'Найкраща раса для Жерця'),
                 'd': t('Жрец-гном — новое сочетание Forever и выбор всех источников в PvE: Эврика! усиливает и Слово силы: Щит, Пытливый ум даёт +5% маны, у гнома два своих заклинания: Confounding Flash и Contingency Plan. Для Темной магии один источник берёт Ночного эльфа. За Орду — Нежить или Тролль. Нежить сильнее в PvP: Воля Отрекшихся снимает страх, сон и очарование.', 'The gnome priest is a new Forever combination and the pick of every source in PvE: Eureka! also boosts Power Word: Shield, Expansive Mind gives +5% mana, and the gnome has two spells of its own (Confounding Flash, Contingency Plan). For Shadow, one source takes Night Elf. On the Horde side it is Undead or Troll. Undead is stronger in PvP: Will of the Forsaken removes fear, sleep and charm.', 'Жрець-гном — нова комбінація Forever і вибір усіх джерел у PvE: Eureka! підсилює й Power Word: Shield, Expansive Mind дає +5% мани, а в гнома є два власні закляття (Confounding Flash, Contingency Plan). Для Темряви одне джерело бере Нічного ельфа. За Орду — Нежить або Троль. Нежить сильніша в PvP: Will of the Forsaken знімає страх, сон і підкорення.')},
                {'id': 'shaman', 't': t('Лучшая раса для Шамана', 'Best race for Shaman', 'Найкраща раса для Шамана'),
                 'd': t('За Альянс шаманом может быть только Дворф, это новое сочетание Forever: Каменная форма и Artisan’s Precision (+1% к меткости). За Орду — Орк: Кровавое неистовство даёт и силу атаки, и силу заклинаний, поэтому подходит и Стихиям, и Совершенствованию. Лекарю один источник советует Тролля за Боевое исступление. В PvP три источника дают три разных ответа: Орк, Таурен, Тролль.', 'On the Alliance side only Dwarf can be a shaman; this is a new Forever combination: Stoneform and Artisan’s Precision (+1% hit chance). On the Horde side it is Orc: Blood Fury gives both attack power and spell power, so it suits Elemental and Enhancement alike. For a healer one source recommends Troll for Berserking. In PvP three sources give three different answers: Orc, Tauren, Troll.', 'За Альянс шаманом може бути лише Дворф, це нова комбінація Forever: Stoneform і Artisan’s Precision (+1% до влучності). За Орду — Орк: Blood Fury дає і силу атаки, і силу заклять, тож підходить і Стихіям, і Вдосконаленню. Цілителю одне джерело радить Троля за Berserking. У PvP три джерела дають три різні відповіді: Орк, Таурен, Троль.')},
                {'id': 'mage', 't': t('Лучшая раса для Мага', 'Best race for Mage', 'Найкраща раса для Мага'),
                 'd': t('Гном: Эврика! на 8 сек, Пытливый ум (+5% маны), Мастер побега от корней. Один источник ставил первым Высшего скайборна за Благословение ветра (+3% к скорости заклинаний, с 26.10 +2%), остальные — нет. Маг-орк — новое сочетание Forever: Кровавое неистовство теперь даёт силу заклинаний. В PvP — Нежить: Воля Отрекшихся снимает страх, сон и очарование.', 'Gnome: Eureka! for 8 sec, Expansive Mind (+5% mana), Escape Artist against roots. One source put High Order Skyborne first for Wind Blessed (+3% spell speed, +2% since Oct 26); the others don’t. The orc mage is a new Forever combination: Blood Fury now gives spell power. In PvP it is Undead: Will of the Forsaken removes fear, sleep and charm.', 'Гном: Eureka! на 8 с, Expansive Mind (+5% мани), Escape Artist від коренів. Одне джерело ставило першим Високого скайборна за Wind Blessed (+3% до швидкості заклять, з 26.10 +2%), решта — ні. Маг-орк — нова комбінація Forever: Blood Fury тепер дає силу заклять. У PvP — Нежить: Will of the Forsaken знімає страх, сон і підкорення.')},
                {'id': 'warlock', 't': t('Лучшая раса для Чернокнижника', 'Best race for Warlock', 'Найкраща раса для Чорнокнижника'),
                 'd': t('Гном (Эврика!, Пытливый ум) или Человек: периодический урон в Forever критует, а Беспощадность даёт +1% крита. В PvP чаще берут Человека: Воля к жизни снимает оглушения. За Орду — Орк в PvE (Кровавое неистовство даёт силу заклинаний) и Нежить в PvP. Тролль-чернокнижник — новое сочетание, но в лидеры не попадает.', 'Gnome (Eureka!, Expansive Mind) or Human: damage over time can crit in Forever, and Ruthless gives +1% crit. In PvP Human is the more common pick: Will to Survive removes stuns. On the Horde side it is Orc in PvE (Blood Fury gives spell power) and Undead in PvP. The troll warlock is a new combination but does not make the lead.', 'Гном (Eureka!, Expansive Mind) або Людина: періодична шкода у Forever може бути критичною, а Ruthless дає +1% криту. У PvP частіше беруть Людину: Will to Survive знімає приголомшення. За Орду — Орк у PvE (Blood Fury дає силу заклять) і Нежить у PvP. Чорнокнижник-троль — нова комбінація, але до лідерів не потрапляє.')},
                {'id': 'druid', 't': t('Лучшая раса для Друида', 'Best race for Druid', 'Найкраща раса для Друїда'),
                 'd': t('Ночной эльф: Свет Элуны (+10% крита) и Расторопность. Таурен: Закалка (+5% здоровья), Громовая поступь работает и в формах. Скайборн-друид — новое сочетание Forever: Благословение ветра даёт +2% к скорости заклинаний и ударов в облике кошки. Часть источников ставит его первым для Силы зверя и Баланса, другие — в середину. Для скайборна нужен платный набор Heroic Pack.', 'Night Elf: Elune’s Light (+10% crit) and Quickness. Tauren: Endurance (+5% health), and War Stomp works in forms too. The Skyborne druid is a new Forever combination: Wind Blessed gives +2% spell and melee speed in cat form. Some sources put it first for Feral and Balance, others in the middle. Skyborne needs the paid Heroic Pack.', 'Нічний ельф: Elune’s Light (+10% криту) і Quickness. Таурен: Endurance (+5% здоров’я), War Stomp працює й у формах. Скайборн-друїд — нова комбінація Forever: Wind Blessed дає +2% до швидкості заклять і ударів у подобі кота. Частина джерел ставить його першим для Сили звіра й Балансу, інші — в середину. Для скайборна потрібен платний набір Heroic Pack.')},
            ]),
        ]},
        {'id': 'forever', 'title': t('Что изменилось против Classic', 'What changed from Classic', 'Що змінилося порівняно з Classic'), 'blocks': [
            ('text', [t('Старые гайды Classic по расам устарели: у рас убраны оружейные специализации и сопротивления, часть способностей заменена.', 'Old Classic race guides are out of date: weapon specializations and resistances are gone from the races, and some abilities were replaced.', 'Старі гайди Classic з рас застаріли: у рас прибрали спеціалізації зброї та опір магії, частину здібностей замінили.')]),
            ('table', {'head': [t('Раса', 'Race', 'Раса'), t('В Classic', 'In Classic', 'У Classic'), t('В Forever', 'In Forever', 'У Forever')], 'rows': [
                [t('Все', 'All', 'Усі'), t('Специализации оружия, сопротивления', 'Weapon specializations, resistances', 'Спеціалізації зброї, опір магії'), t('Убраны, вместо них новые способности', 'Removed, replaced by new abilities', 'Прибрано, замість них нові здібності')],
                [t('Человек', 'Human', 'Людина'), t('Специализация на мечах и булавах', 'Sword and mace specialization', 'Спеціалізація на мечах і булавах'), t('Беспощадность: +1% крита всем умениям', 'Ruthless: +1% crit on all abilities', 'Ruthless: +1% криту всім умінням')],
                [t('Орк', 'Orc', 'Орк'), t('Кровавое неистовство: +25% базовой силы атаки на 15 сек, получаемое лечение −50% на 25 сек', 'Blood Fury: +25% base attack power for 15 sec, healing received −50% for 25 sec', 'Blood Fury: +25% базової сили атаки на 15 с, отримане лікування −50% на 25 с'), t('Даёт и силу заклинаний, штрафа к лечению нет, откат 3 мин', 'Gives spell power too, no healing penalty, 3 min cooldown', 'Дає й силу заклять, штрафу до лікування немає, відкат 3 хв')],
                [t('Орк', 'Orc', 'Орк'), t('Command: +5% урона питомцев', 'Command: +5% pet damage', 'Command: +5% шкоди улюбленців'), t('Тоже +5% урона питомцев чернокнижника и охотника: Властность вернулась 26.10 вместо Дикости', 'Also +5% Warlock and Hunter pet damage: Command returned on Oct 26 in place of Savage', 'Теж +5% шкоди улюбленців чорнокнижника й мисливця: Command повернули 26.10 замість Savage')],
                [t('Орк', 'Orc', 'Орк'), t('Твердость: +25% к шансу сопротивиться оглушению', 'Hardiness: +25% chance to resist stuns', 'Hardiness: +25% до шансу опиратися приголомшенню'), t('Оглушения короче на 20%', 'Stuns 20% shorter', 'Приголомшення коротші на 20%')],
                [t('Тролль', 'Troll', 'Троль'), t('Боевое исступление до +30% при низком здоровье', 'Berserking: up to +30% when at low health', 'Berserking: до +30% за низького здоров’я'), t('Ровно +10% скорости атак и заклинаний, на 12 сек, откат 3 мин', 'A flat +10% attack and spell speed for 12 sec, 3 min cooldown', 'Рівно +10% до швидкості атак і заклять на 12 с, відкат 3 хв')],
                [t('Дворф', 'Dwarf', 'Дворф'), t('Каменная форма: +10% брони', 'Stoneform: +10% armor', 'Stoneform: +10% броні'), t('−10% физического урона', '−10% physical damage', '−10% фізичної шкоди')],
                [t('Гном', 'Gnome', 'Гном'), '—', t('Эврика!: 8 сек, способности дешевле и на 10% сильнее', 'Eureka!: 8 sec, abilities cost less and are 10% stronger', 'Eureka!: 8 с, здібності дешевші й на 10% сильніші')],
                [t('Таурен', 'Tauren', 'Таурен'), t('Громовая поступь раз в 2 мин', 'War Stomp once every 2 min', 'War Stomp раз на 2 хв'), t('Раз в 90 сек, плюс Закалка и Бег по равнинам', 'Once every 90 sec, plus Endurance and Plainsrunning', 'Раз на 90 с, плюс Endurance і Plainsrunning')],
                [t('Нежить', 'Undead', 'Нежить'), '—', t('Могильное касание: шанс вытянуть здоровье', 'Touch of the Grave: chance to drain health', 'Touch of the Grave: шанс витягнути здоров’я')],
            ]}),
            ('text', [t('Новые сочетания: охотник-человек, шаман-дворф, жрец-гном, паладин-нежить, маг-орк, чернокнижник-тролль, друид-скайборн.', 'New combinations: human hunter, dwarf shaman, gnome priest, undead paladin, orc mage, troll warlock, Skyborne druid.', 'Нові комбінації: мисливець-людина, шаман-дворф, жрець-гном, паладин-нежить, маг-орк, чорнокнижник-троль, друїд-скайборн.')]),
        ]},
        {'id': 'disputed', 'title': t('Где источники спорят', 'Where the sources disagree', 'Де джерела сперечаються'), 'blocks': [
            ('steps', [
                {'t': t('Воин и Охотник за Альянс', 'Alliance Warrior and Hunter', 'Воїн і Мисливець за Альянс'),
                 'd': t('Человек или Ночной эльф, голоса делятся почти поровну. Охотнику один источник советует Дворфа.', 'Human or Night Elf, the votes are almost evenly split. For Hunter one source recommends Dwarf.', 'Людина або Нічний ельф, голоси розділилися майже порівну. Мисливцеві одне джерело радить Дворфа.')},
                {'t': t('Чернокнижник за Альянс', 'Alliance Warlock', 'Чорнокнижник за Альянс'),
                 'd': t('Гном или Человек.', 'Gnome or Human.', 'Гном або Людина.')},
                {'t': t('Шаман Орды в PvP', 'Horde Shaman in PvP', 'Шаман Орди в PvP'),
                 'd': t('три источника, три ответа.', 'three sources, three answers.', 'три джерела, три відповіді.')},
                {'t': t('Скайборн-друид и скайборн-маг', 'Skyborne druid and Skyborne mage', 'Скайборн-друїд і скайборн-маг'),
                 'd': t('от «лучшей расы» до «худшей в PvP» в разных списках.', 'from “best race” to “worst in PvP” depending on the list.', 'від «найкращої раси» до «найгіршої в PvP» залежно від списку.')},
                {'t': t('PvP целиком', 'PvP as a whole', 'PvP загалом'),
                 'd': t('полей боя на бете не было, уровни 31–60 никто не проверял. Обновим после старта 5 ноября.', 'there were no battlegrounds in the beta and nobody has tested levels 31–60. We’ll update after the Nov 4–5 launch.', 'полів бою в бета-версії не було, рівні 31–60 ніхто не перевіряв. Оновимо після старту 5 листопада.')},
            ]),
        ]},
        {'id': 'faq', 'title': t('Частые вопросы', 'Common questions', 'Часті питання'), 'blocks': [
            ('faq', [
                {'id': 'q1', 'q': t('Какая раса лучше для воина в WoW Forever?', 'Which race is best for a warrior in WoW Forever?', 'Яка раса найкраща для воїна у WoW Forever?'),
                 'a': [t('За Альянс — Человек или Ночной эльф, источники делятся почти поровну, танку — Дворф. За Орду — Орк, танку — Таурен.', 'On the Alliance side, Human or Night Elf; the sources are almost evenly split, and a tank should take Dwarf. On the Horde side, Orc; a tank should take Tauren.', 'За Альянс — Людина або Нічний ельф, джерела розділилися майже порівну, танку — Дворф. За Орду — Орк, танку — Таурен.')]},
                {'id': 'q2', 'q': t('Сильно ли раса влияет на игру?', 'Does race make a big difference?', 'Чи сильно раса впливає на гру?'),
                 'a': [t('Несколько процентов урона или живучести. Класс, спек и экипировка важнее, поэтому берите расу, которая нравится.', 'A few percent of damage or survivability. Class, spec and gear matter more, so take the race you like.', 'Це кілька відсотків шкоди або живучості. Клас, спеціалізація й екіпірування важать більше, тож беріть расу, яка подобається.')]},
                {'id': 'q3', 'q': t('Какие сочетания расы и класса новые в Forever?', 'Which race and class combinations are new in Forever?', 'Які поєднання раси й класу нові у Forever?'),
                 'a': [t('Охотник-человек, шаман-дворф, жрец-гном, паладин-нежить, маг-орк, чернокнижник-тролль и друид-скайборн.', 'Human hunter, dwarf shaman, gnome priest, undead paladin, orc mage, troll warlock and Skyborne druid.', 'Мисливець-людина, шаман-дворф, жрець-гном, паладин-нежить, маг-орк, чорнокнижник-троль і друїд-скайборн.')]},
                {'id': 'q4', 'q': t('Подходят ли гайды Classic по расам для Forever?', 'Do Classic race guides still apply to Forever?', 'Чи годяться гайди Classic з рас для Forever?'),
                 'a': [t('Нет. У рас убраны оружейные специализации и сопротивления, Кровавое неистовство, Боевое исступление и Каменная форма работают иначе.', 'No. Weapon specializations and resistances are gone from the races, and Blood Fury, Berserking and Stoneform work differently.', 'Ні. У рас прибрали спеціалізації зброї та опір магії, а Blood Fury, Berserking і Stoneform працюють інакше.')]},
                {'id': 'q5', 'q': t('Какую расу взять паладину за Орду?', 'Which race should a Horde paladin take?', 'Яку расу взяти паладину за Орду?'),
                 'a': [t('Только Нежить: другие расы Орды паладином быть не могут.', 'Only Undead: no other Horde race can be a paladin.', 'Лише Нежить: інші раси Орди паладинами бути не можуть.')]},
            ]),
        ]},
        {'id': 'related', 'title': t('Смотрите также', 'See also', 'Дивіться також'), 'blocks': [
            ('tiles', [{'t': t('Тир-лист классов WoW Forever', 'WoW Forever Class Tier List', 'Тір-лист класів WoW Forever'), 'd': t('Лучшие классы по данным беты', 'Best classes by beta data', 'Найкращі класи за даними бети'), 'href': 'guides/tier-list/', 'art': 'hero_tierlist'}, {'t': t('Классы', 'Classes', 'Класи'), 'd': t('Какой класс выбрать и сравнение', 'Which class to pick, compared', 'Який клас обрати й порівняння'), 'href': 'classes/', 'art': 'hero_classes'}, {'t': t('Расы', 'Races', 'Раси'), 'd': t('Сравнение всех рас', 'All races compared', 'Порівняння всіх рас'), 'href': 'races/', 'art': 'hero_races'}]),
        ]},
    ],
})


def _race_per_class(g):
    """best-race: an h2 with an anchor for every class («Best race for Warlock», #warlock), the query players type.
    The «Best race by class» section above keeps the toc entry and the jump links; the class sections light it up in the toc."""
    i = next(i for i, s in enumerate(g['sections']) if s['id'] == 'classes')
    steps = next(d for k, d in g['sections'][i]['blocks'] if k == 'steps')
    g['sections'][i]['blocks'] = [('anchors', [s['id'] for s in steps])]
    g['sections'][i + 1:i + 1] = [{'id': s['id'], 'title': s['t'], 'toc': 'classes', 'blocks': [('text', [s['d']])]} for s in steps]


_race_per_class(GUIDES[-1])

# ---------- tier-list ----------
# «по бете» / «по живой игре» и дата: один переключатель data/tierlist.json (content/tierlist_live.py) — title, лид, факты
# первого экрана, совет «Как читать», плитка и блок «Что изменилось». Порядок: docs/wow/TIERLIST-LIVE-RUNBOOK.md

GUIDES.append({
    'slug': 'tier-list', 'art': 'hero_tierlist', 'hero': 'hero_tierlist',
    'title': t('Тир-лист классов WoW Forever', 'WoW Forever Class Tier List', 'Тір-лист класів WoW Forever'),
    'crumb': t('Тир-лист', 'Tier list', 'Тір-лист'),
    # the content sentences; the status one (beta snapshot / live game, date) is added by TL.lead
    'lead': TL.lead(t('Тир-лист — рейтинг классов и спеков по силе, от S до C. На бете сильнее всех Паладин в PvE, Охотник и Маг на прокачке, Чернокнижник и Разбойник в PvP.', 'A tier list ranks classes and specs by strength, from S to C. In the beta the strongest picks are Paladin in PvE, Hunter and Mage for leveling, Warlock and Rogue in PvP.', 'Тір-лист — рейтинг класів і спеціалізацій за силою, від S до C. У бета-версії найсильніші Паладин у PvE, Мисливець і Маг на прокачуванні, Чорнокнижник і Розбійник у PvP.'), TL_STATUS),
    'tile': TL.tile(TL_STATUS),
    'pills': TL.pills(t('27 спеков', '27 specs', '27 спеціалізацій'), TL_STATUS),
    # one Alliance / Horde switch over the class grid (build_guides.side_switch): the site-wide side, races of that side in the table
    'side': {'label': t('Фракция', 'Faction', 'Фракція'),
             'alliance': t('Альянс', 'Alliance', 'Альянс'), 'horde': t('Орда', 'Horde', 'Орда'),
             'races': t('Расы', 'Races', 'Раси'),
             'note': t('Все 9 классов есть у обеих фракций, от фракции зависят расы.',
                       'All 9 classes are open to both factions; the faction decides the races.',
                       'Усі 9 класів є в обох фракцій, від фракції залежать раси.'),
             'star': t('★ — лучшая раса в PvE по гайду', '★ — the best race for PvE per the guide', '★ — найкраща раса в PvE за гайдом'),
             'guide': t('Лучшая раса для каждого класса', 'Best Race for Every Class', 'Найкраща раса для кожного класу')},
    'sources': [
        (t('RankedBoost: тир-лист Forever', 'RankedBoost: Forever tier list', 'RankedBoost: тір-лист Forever'), 'https://rankedboost.com/world-of-warcraft/forever/tier-list/'),
        (t('Noobtoboss: тир-лист', 'Noobtoboss: tier list', 'Noobtoboss: тір-лист'), 'https://noobtoboss.com/wowforever-tierlist/'),
        (t('Noobtoboss: прокачка', 'Noobtoboss: leveling', 'Noobtoboss: прокачування'), 'https://noobtoboss.com/wowforever-leveling-tierlist/'),
        (t('gamer-guides: тир-лист беты', 'gamer-guides: beta tier list', 'gamer-guides: тір-лист бети'), 'https://gamer-guides.com/warcraft-forever/tier-list-beta/'),
        (t('Kami-labs: все 9 классов', 'Kami-labs: all 9 classes', 'Kami-labs: усі 9 класів'), 'https://kami-labs.fr/en/wow-forever/quelle-classe-choisir-wow-forever/'),
        (t('Warcraft Tavern: итоги Forever Open', 'Warcraft Tavern: Forever Open results', 'Warcraft Tavern: підсумки Forever Open'), 'https://www.warcrafttavern.com/forever/news/warlockguy-wins-the-wow-forever-open-1v1-dueling-tournament/'),
        (t('LFCarry: изменения классов', 'LFCarry: class changes', 'LFCarry: зміни класів'), 'https://lfcarry.com/guides/wow-forever-class-changes'),
        (t('games.gg: какой класс выбрать', 'games.gg: which class to pick', 'games.gg: який клас обрати'), 'https://games.gg/news/wow-forever-best-class-returning-paladin/'),
        (t('LFCarry: классы и темп прокачки (оценка по Classic, перепроверена на бете)', 'LFCarry: classes and leveling pace (Classic-based estimate, rechecked on the beta)', 'LFCarry: класи й темп прокачування (оцінка за Classic, перевірена на бета-версії)'), 'https://lfcarry.com/guides/wow-forever-classes'),
    ],
    'sections': [
        {'id': 'how', 'title': t('Как читать', 'How to read it', 'Як читати'), 'blocks': [
            ('text', [t('Тир — сводка нескольких источников, а не оценка одного сайта. S — лучшие в своей роли, C — слабее, но играть можно. Звёздочка (*) — источники расходятся на две буквы и больше. Источники — сайты гайдов (RankedBoost, gamer-guides, Noobtoboss, Kami-labs и другие), список со ссылками — в конце страницы.', 'The tier is a summary of several sources, not one site’s rating. S is the best in its role, C is weaker but playable. An asterisk (*) means the sources differ by two letters or more. The sources are guide sites (RankedBoost, gamer-guides, Noobtoboss, Kami-labs and others); the full list with links is at the end of the page.', 'Тір — це зведення кількох джерел, а не оцінка одного сайту. S — найкращі у своїй ролі, C — слабші, але грати можна. Зірочка (*) означає, що джерела розходяться на дві літери й більше. Джерела — сайти гайдів (RankedBoost, gamer-guides, Noobtoboss, Kami-labs та інші), список із посиланнями — наприкінці сторінки.')]),
            ('tip', TL.tip(TL_STATUS)),
        ]},
        {'id': 'classes', 'title': t('Лучшие классы на 30 уровне', 'Best classes at level 30', 'Найкращі класи на 30 рівні'), 'blocks': [
            ('table', {'head': [t('Класс', 'Class', 'Клас'), t('Прокачка', 'Leveling', 'Прокачування'), 'PvE', 'PvP', t('Почему', 'Why', 'Чому')], 'rows': [
                [t('Паладин', 'Paladin', 'Паладин'), 'A', 'S', 'B', t('Защита — лучший танк беты, даже после ослабления 15.10.', 'Protection is the best tank of the beta, even after the Oct 15 nerf.', 'Захист — найкращий танк бети, навіть після послаблення 15 жовтня.')],
                [t('Охотник', 'Hunter', 'Мисливець'), 'S', 'A*', 'A', t('Самая быстрая прокачка и самый простой урон.', 'The fastest leveling and the simplest damage.', 'Найшвидше прокачування й найпростіша шкода.')],
                [t('Маг', 'Mage', 'Маг'), 'S', 'A', 'A*', t('Быстрая прокачка за Лёд, сильный бурст Тайной магии.', 'Fast leveling as Frost, strong Arcane burst.', 'Швидке прокачування за Лід, потужний бурст Тайної магії.')],
                [t('Чернокнижник', 'Warlock', 'Чорнокнижник'), 'A', 'A', 'S', t('Периодический урон критует; чернокнижники заняли два первых места на турнире Forever Open.', 'Damage over time can crit; warlocks took the top two places at the Forever Open tournament.', 'Періодична шкода може бути критичною; чорнокнижники зайняли два перші місця на турнірі Forever Open.')],
                [t('Разбойник', 'Rogue', 'Розбійник'), 'B', 'A', 'S', t('Скрытность и контроль: в PvP самый надёжный выбор.', 'Stealth and control: the most reliable pick in PvP.', 'Непомітність і контроль: у PvP найнадійніший вибір.')],
                [t('Жрец', 'Priest', 'Жрець'), 'C*', 'A', 'A*', t('Нужен любой группе; Послушание сильно и в PvP, Свет — нет.', 'Every group needs one; Discipline is strong in PvP too, Holy is not.', 'Потрібен будь-якій групі; Послух сильний і в PvP, Світло — ні.')],
                [t('Шаман', 'Shaman', 'Шаман'), 'B', 'A', 'B*', t('Исцеление и Совершенствование сильные, Стихии усилены 15.10 после слабого старта.', 'Restoration and Enhancement are strong, Elemental was buffed on Oct 15 after a weak start.', 'Зцілення та Вдосконалення сильні, Стихії підсилили 15 жовтня після слабкого старту.')],
                [t('Воин', 'Warrior', 'Воїн'), 'C', 'A', 'B', t('Самая медленная прокачка, зато Защита — сильный танк.', 'The slowest leveling, but Protection is a strong tank.', 'Найповільніше прокачування, зате Захист — сильний танк.')],
                [t('Друид', 'Druid', 'Друїд'), 'A*', 'B', 'B*', t('Нет ведущего спека, многие ключевые умения открываются после 30 уровня.', 'No leading spec; many key abilities unlock after level 30.', 'Провідної спеціалізації немає, багато ключових умінь відкривається після 30 рівня.')],
            ]}),
        ]},
        {'id': 'leveling', 'title': t('Тир-лист прокачки', 'Leveling tier list', 'Тір-лист прокачування'), 'blocks': [
            ('text', [t('Источники оценивают прокачку по классу, поэтому здесь один спек на класс. Проценты темпа — оценка LFCarry по Classic, перепроверенная на бете.', 'Sources rate leveling per class, so this table has one spec per class. The pace percentages are LFCarry’s estimate based on Classic, rechecked on the beta.', 'Джерела оцінюють прокачування за класом, тому тут одна спеціалізація на клас. Відсотки темпу — оцінка LFCarry за Classic, перевірена на бета-версії.')]),
            ('table', {'head': [t('Тир', 'Tier', 'Тір'), t('Класс · спек', 'Class · spec', 'Клас · спеціалізація'), t('Почему', 'Why', 'Чому'), t('Где расходятся', 'Where sources differ', 'Де розходяться')], 'rows': [
                ['S', (t('Охотник · Повелитель зверей', 'Hunter · Beast Mastery', 'Мисливець · Володіння звірами'), 'guides/leveling-hunter/'), t('Питомец танкует, примерно на 8% быстрее среднего.', 'The pet tanks; about 8% faster than average.', 'Улюбленець танкує, приблизно на 8% швидше за середнє.'), 'gamer-guides: A'],
                ['S', (t('Маг · Лёд', 'Mage · Frost', 'Маг · Лід'), 'guides/leveling-mage/'), t('Урон по площади, замедления, своя еда и вода, примерно на 8% быстрее среднего.', 'Area damage, slows, its own food and water; about 8% faster than average.', 'Шкода по площі, уповільнення, власні їжа й вода, приблизно на 8% швидше за середнє.'), t('gamer-guides берёт Тайную магию', 'gamer-guides picks Arcane', 'gamer-guides бере Тайну магію')],
                ['A', (t('Чернокнижник · Колдовство', 'Warlock · Affliction', 'Чорнокнижник · Прокляття'), 'guides/leveling-warlock/'), t('Питомец держит врага, пока работает периодический урон.', 'The pet holds the enemy while damage over time works.', 'Улюбленець тримає ворога, поки діє періодична шкода.'), 'gamer-guides: S'],
                ['A', (t('Паладин · Воздаяние', 'Paladin · Retribution', 'Паладин · Відплата'), 'guides/leveling-paladin/'), t('Легко фармит группы врагов по площади.', 'Farms groups of enemies easily with area damage.', 'Легко фармить групи ворогів шкодою по площі.'), 'gamer-guides: B'],
                ['A*', (t('Друид · Сила зверя', 'Druid · Feral', 'Друїд · Сила звіра'), 'guides/leveling-druid/'), t('Много ключевых умений открывается после 30, примерно на 5% медленнее среднего.', 'Many key abilities unlock after 30; about 5% slower than average.', 'Багато ключових умінь відкривається після 30, приблизно на 5% повільніше за середнє.'), 'gamer-guides: C'],
                ['B', (t('Шаман · Совершенствование', 'Shaman · Enhancement', 'Шаман · Вдосконалення'), 'guides/leveling-shaman/'), t('До 30 уровня не хватает маны; Призрачный волк с 20 уровня.', 'Short on mana until level 30; Ghost Wolf from level 20.', 'До 30 рівня не вистачає мани; Ghost Wolf з 20 рівня.'), '—'],
                ['B', (t('Разбойник · Ликвидация или Бой', 'Rogue · Assassination or Combat', 'Розбійник · Ліквідація або Бій'), 'guides/leveling-rogue/'), t('Средний темп.', 'Average pace.', 'Середній темп.'), 'gamer-guides: A'],
                ['C*', (t('Жрец · Темная магия', 'Priest · Shadow', 'Жрець · Темрява'), 'guides/leveling-priest/'), t('Примерно на 5% медленнее среднего.', 'About 5% slower than average.', 'Приблизно на 5% повільніше за середнє.'), t('gamer-guides: S для Послушания', 'gamer-guides: S for Discipline', 'gamer-guides: S для Послуху')],
                ['C', (t('Воин · Оружие или Неистовство', 'Warrior · Arms or Fury', 'Воїн · Зброя або Лють'), 'guides/leveling-warrior/'), t('Самый медленный, примерно на 12% дольше среднего.', 'The slowest, about 12% longer than average.', 'Найповільніший, приблизно на 12% довше за середнє.'), '—'],
            ]}),
        ]},
        {'id': 'pve', 'title': t('Тир-лист PvE по ролям', 'PvE tier list by role', 'Тір-лист PvE за ролями'), 'blocks': [
            ('text', [t('Сравнение внутри роли: танк с танками, лекарь с лекарями. Рейдовых логов нет, рейды откроются 09.12.', 'Comparison within a role: tank with tanks, healer with healers. There are no raid logs; raids open on Dec 9.', 'Порівняння всередині ролі: танк з танками, цілитель з цілителями. Рейдових логів немає, рейди відкриються 9 грудня.')]),
            ('tabs', [
                {'id': 'tank', 't': t('Танк', 'Tank', 'Танк'), 'blocks': [
                    ('table', {'head': [t('Тир', 'Tier', 'Тір'), t('Спек', 'Spec', 'Спеціалізація'), t('Почему', 'Why', 'Чому'), t('Где расходятся', 'Where sources differ', 'Де розходяться')], 'rows': [
                ['S', t('Паладин · Защита', 'Paladin · Protection', 'Паладин · Захист'), t('Лучший танк беты, Печать ярости даёт провокацию.', 'The best tank of the beta; Seal of Fury gives a taunt.', 'Найкращий танк бети, Seal of Fury дає провокацію.'), t('Ослаблен 15.10, RankedBoost (17.10) всё равно ставит S', 'Nerfed Oct 15, RankedBoost (Oct 17) still gives S', 'Послаблений 15 жовтня, RankedBoost (17 жовтня) усе одно ставить S')],
                ['A', t('Воин · Защита', 'Warrior · Protection', 'Воїн · Захист'), t('Сильный танк для подземелий.', 'A strong dungeon tank.', 'Сильний танк для підземель.'), '—'],
                ['B', t('Друид · Сила зверя (медведь)', 'Druid · Feral (bear)', 'Друїд · Сила звіра (ведмідь)'), t('Медведь танкует, но уступает Паладину и Воину.', 'The bear tanks, but trails Paladin and Warrior.', 'Ведмідь танкує, але поступається Паладину й Воїну.'), '—'],
            ]}),
                ]},
                {'id': 'healer', 't': t('Лекарь', 'Healer', 'Цілитель'), 'blocks': [
                    ('table', {'head': [t('Тир', 'Tier', 'Тір'), t('Спек', 'Spec', 'Спеціалізація'), t('Почему', 'Why', 'Чому'), t('Где расходятся', 'Where sources differ', 'Де розходяться')], 'rows': [
                ['S', t('Жрец · Послушание', 'Priest · Discipline', 'Жрець · Послух'), t('Покаяние и щиты: лучший лекарь беты по двум источникам.', 'Penance and shields: the best healer of the beta according to two sources.', 'Penance і щити: найкращий цілитель бети за двома джерелами.'), '—'],
                ['S', t('Шаман · Исцеление', 'Shaman · Restoration', 'Шаман · Зцілення'), t('Быстрина, первое место среди лекарей у RankedBoost.', 'Riptide; first among healers at RankedBoost.', 'Riptide; перше місце серед цілителів у RankedBoost.'), '—'],
                ['A', t('Паладин · Свет', 'Paladin · Holy', 'Паладин · Світло'), t('Сильное лечение по одной цели.', 'Strong single-target healing.', 'Сильне лікування однієї цілі.'), '—'],
                ['A', t('Друид · Исцеление', 'Druid · Restoration', 'Друїд · Зцілення'), t('Буйный рост; Kami-labs называет спек исключительным.', 'Wild Growth; Kami-labs calls the spec exceptional.', 'Wild Growth; Kami-labs називає спеціалізацію винятковою.'), 'gamer-guides: S'],
                ['B*', t('Жрец · Свет', 'Priest · Holy', 'Жрець · Світло'), t('Лучшее лечение по площади, раскрывается к 60 уровню.', 'The best area healing, comes into its own by level 60.', 'Найкраще лікування по площі, розкривається до 60 рівня.'), t('RankedBoost: B для лекаря; Noobtoboss и gamer-guides называют сильным рейдовым лекарем', 'RankedBoost: B as a healer; Noobtoboss and gamer-guides call it a strong raid healer', 'RankedBoost: B для цілителя; Noobtoboss і gamer-guides називають його сильним рейдовим цілителем')],
            ]}),
                ]},
                {'id': 'dps', 't': t('Урон', 'Damage', 'Шкода'), 'blocks': [
                    ('table', {'head': [t('Тир', 'Tier', 'Тір'), t('Спек', 'Spec', 'Спеціалізація'), t('Почему', 'Why', 'Чому'), t('Где расходятся', 'Where sources differ', 'Де розходяться')], 'rows': [
                ['A', t('Паладин · Воздаяние', 'Paladin · Retribution', 'Паладин · Відплата'), t('Сильный, хотя ослаблен 15.10.', 'Strong, though nerfed on Oct 15.', 'Сильний, хоч і послаблений 15 жовтня.'), '—'],
                ['A*', t('Охотник · Стрельба', 'Hunter · Marksmanship', 'Мисливець · Стрільба'), t('Лучший урон охотника, но источники спорят.', 'The hunter’s best damage, but the sources disagree.', 'Найкраща шкода мисливця, але джерела сперечаються.'), 'Noobtoboss: S, RankedBoost: A'],
                ['A*', t('Охотник · Повелитель зверей', 'Hunter · Beast Mastery', 'Мисливець · Володіння звірами'), t('Урон делит с питомцем.', 'Shares damage with the pet.', 'Ділить шкоду з улюбленцем.'), 'Noobtoboss: S, RankedBoost: A'],
                ['A', t('Охотник · Выживание', 'Hunter · Survival', 'Мисливець · Виживання'), t('Лидер по симуляциям, но его ждут выравнивать.', 'Leads in simulations, but a rebalance is expected.', 'Лідер за симуляціями, але його чекають вирівнювати.'), '—'],
                ['A', t('Разбойник · Ликвидация', 'Rogue · Assassination', 'Розбійник · Ліквідація'), t('Яды.', 'Poisons.', 'Отрути.'), '—'],
                ['A*', t('Разбойник · Бой', 'Rogue · Combat', 'Розбійник · Бій'), t('Хорош по одной цели.', 'Good against a single target.', 'Хороший по одній цілі.'), 'RankedBoost: B'],
                ['A', t('Воин · Неистовство', 'Warrior · Fury', 'Воїн · Лють'), t('Сильный урон по нескольким целям.', 'Strong damage against several targets.', 'Сильна шкода по кількох цілях.'), '—'],
                ['A*', t('Шаман · Совершенствование', 'Shaman · Enhancement', 'Шаман · Вдосконалення'), t('Один из лучших по урону у Noobtoboss.', 'One of the best for damage at Noobtoboss.', 'Один із найкращих за шкодою у Noobtoboss.'), 'RankedBoost: B'],
                ['A', t('Маг · Тайная магия', 'Mage · Arcane', 'Маг · Тайна магія'), t('Чародейская вспышка переработана 15.10.', 'Arcane Blast was reworked on Oct 15.', 'Arcane Blast переробили 15 жовтня.'), '—'],
                ['A*', t('Маг · Огонь', 'Mage · Fire', 'Маг · Вогонь'), t('Криты и поджоги.', 'Crits and ignites.', 'Криті та підпали.'), t('Noobtoboss: B для подземелий', 'Noobtoboss: B for dungeons', 'Noobtoboss: B для підземель')],
                ['A', t('Чернокнижник · Колдовство', 'Warlock · Affliction', 'Чорнокнижник · Прокляття'), t('Периодический урон, сильнее всех соло.', 'Damage over time, the strongest solo.', 'Періодична шкода, найсильніший наодинці.'), '—'],
                ['A', t('Чернокнижник · Демонология', 'Warlock · Demonology', 'Чорнокнижник · Демонологія'), t('Лучший спек подземелий по Noobtoboss.', 'The best dungeon spec according to Noobtoboss.', 'Найкраща спеціалізація підземель за Noobtoboss.'), '—'],
                ['A', t('Чернокнижник · Разрушение', 'Warlock · Destruction', 'Чорнокнижник · Руйнування'), t('Бурст, данных мало.', 'Burst, little data.', 'Бурст, даних мало.'), t('только RankedBoost', 'RankedBoost only', 'лише RankedBoost')],
                ['B', t('Воин · Оружие', 'Warrior · Arms', 'Воїн · Зброя'), t('Двуручное оружие, ветка под PvP.', 'Two-handed weapons, a PvP-oriented tree.', 'Дворучна зброя, гілка під PvP.'), '—'],
                ['B*', t('Жрец · Темная магия', 'Priest · Shadow', 'Жрець · Темрява'), t('Усилена 15.10.', 'Buffed on Oct 15.', 'Підсилена 15 жовтня.'), t('RankedBoost: A, Noobtoboss: отстаёт', 'RankedBoost: A, Noobtoboss: lags behind', 'RankedBoost: A, Noobtoboss: відстає')],
                ['B*', t('Шаман · Стихии', 'Shaman · Elemental', 'Шаман · Стихії'), t('Выброс лавы и Покорение стихий усилены 15.10.', 'Lava Burst and Elemental Mastery were buffed on Oct 15.', 'Lava Burst і Elemental Mastery підсилили 15 жовтня.'), 'RankedBoost: A'],
                ['B', t('Маг · Лёд', 'Mage · Frost', 'Маг · Лід'), t('Сильнее на прокачке, чем в подземельях.', 'Stronger for leveling than in dungeons.', 'Сильніший на прокачуванні, ніж у підземеллях.'), '—'],
                ['B', t('Друид · Сила зверя (кошка)', 'Druid · Feral (cat)', 'Друїд · Сила звіра (кіт)'), t('Масштабируется с оружием.', 'Scales with weapons.', 'Масштабується зі зброєю.'), '—'],
                ['C', t('Разбойник · Скрытность', 'Rogue · Subtlety', 'Розбійник · Непомітність'), t('Ветка для PvP.', 'A PvP tree.', 'Гілка для PvP.'), '—'],
                ['C', t('Друид · Баланс', 'Druid · Balance', 'Друїд · Баланс'), t('Затмение пока выглядит слабо.', 'Eclipse still looks weak.', 'Eclipse поки виглядає слабко.'), '—'],
            ]}),
                ]},
            ]),
        ]},
        {'id': 'pvp', 'title': t('Тир-лист PvP', 'PvP tier list', 'Тір-лист PvP'), 'blocks': [
            ('text', [t('Полей боя и арен на бете не было: оценки по дуэлям, мировому PvP и турниру Forever Open (18.10, только Орда, бой 1 на 1, уровень 30).', 'There were no battlegrounds or arenas in the beta: ratings come from duels, world PvP and the Forever Open tournament (Oct 18, Horde only, 1v1, level 30).', 'Полів бою й арен у бета-версії не було: оцінки за дуелями, світовим PvP і турніром Forever Open (18 жовтня, лише Орда, бій 1 на 1, 30 рівень).')]),
            ('table', {'head': [t('Тир', 'Tier', 'Тір'), t('Спек', 'Spec', 'Спеціалізація'), t('Почему', 'Why', 'Чому'), t('Где расходятся', 'Where sources differ', 'Де розходяться')], 'rows': [
                ['S', t('Разбойник · Ликвидация', 'Rogue · Assassination', 'Розбійник · Ліквідація'), t('Яды и контроль из скрытности.', 'Poisons and control from stealth.', 'Отрути й контроль із невидимості.'), '—'],
                ['S', t('Разбойник · Скрытность', 'Rogue · Subtlety', 'Розбійник · Непомітність'), t('Лучшая PvP-ветка разбойника.', 'The rogue’s best PvP tree.', 'Найкраща PvP-гілка розбійника.'), '—'],
                ['S', t('Жрец · Послушание', 'Priest · Discipline', 'Жрець · Послух'), t('Покаяние и щиты.', 'Penance and shields.', 'Penance і щити.'), '—'],
                ['S', t('Чернокнижник · Колдовство', 'Warlock · Affliction', 'Чорнокнижник · Прокляття'), t('Сильнее всех кастеров соло; Kami-labs ждёт его сильным на полях боя.', 'The strongest caster solo; Kami-labs expects it to be strong in battlegrounds.', 'Сильніший за всіх кастерів наодинці; Kami-labs чекає, що він буде сильним на полях бою.'), 'RankedBoost: A'],
                ['A', t('Паладин · Воздаяние', 'Paladin · Retribution', 'Паладин · Відплата'), '—', '—'],
                ['A', t('Охотник · Стрельба', 'Hunter · Marksmanship', 'Мисливець · Стрільба'), t('Kami-labs считает её очень сильной.', 'Kami-labs considers it very strong.', 'Kami-labs вважає її дуже сильною.'), '—'],
                ['A*', t('Охотник · Выживание', 'Hunter · Survival', 'Мисливець · Виживання'), t('Ближний бой у охотника слабее в PvP.', 'The hunter’s melee is weaker in PvP.', 'Ближній бій мисливця слабший у PvP.'), '—'],
                ['A*', t('Разбойник · Бой', 'Rogue · Combat', 'Розбійник · Бій'), '—', t('RankedBoost: S, Kami-labs: слабее в PvP', 'RankedBoost: S, Kami-labs: weaker in PvP', 'RankedBoost: S, Kami-labs: слабший у PvP')],
                ['A', t('Жрец · Темная магия', 'Priest · Shadow', 'Жрець · Темрява'), t('Переживает бой 1 на 1.', 'Survives a 1v1 fight.', 'Переживає бій 1 на 1.'), '—'],
                ['A*', t('Шаман · Совершенствование', 'Shaman · Enhancement', 'Шаман · Вдосконалення'), t('Мобильный, Призрачный волк.', 'Mobile, Ghost Wolf.', 'Мобільний, Ghost Wolf.'), '—'],
                ['A*', t('Маг · Тайная магия', 'Mage · Arcane', 'Маг · Тайна магія'), t('Бурст.', 'Burst.', 'Бурст.'), 'RankedBoost: S'],
                ['A', t('Маг · Лёд', 'Mage · Frost', 'Маг · Лід'), t('Контроль и замедления.', 'Control and slows.', 'Контроль і уповільнення.'), '—'],
                ['A*', t('Чернокнижник · Демонология', 'Warlock · Demonology', 'Чорнокнижник · Демонологія'), t('Kami-labs ждёт его сильным на полях боя.', 'Kami-labs expects it to be strong in battlegrounds.', 'Kami-labs чекає, що він буде сильним на полях бою.'), 'RankedBoost: B'],
                ['A', t('Чернокнижник · Разрушение', 'Warlock · Destruction', 'Чорнокнижник · Руйнування'), t('Бурст.', 'Burst.', 'Бурст.'), t('только RankedBoost', 'RankedBoost only', 'лише RankedBoost')],
                ['A', t('Друид · Баланс', 'Druid · Balance', 'Друїд · Баланс'), t('В PvP сильнее, чем в PvE.', 'Stronger in PvP than in PvE.', 'У PvP сильніший, ніж у PvE.'), '—'],
                ['A*', t('Друид · Сила зверя', 'Druid · Feral', 'Друїд · Сила звіра'), t('Берсерк, масштабируется с оружием.', 'Berserk, scales with weapons.', 'Berserk, масштабується зі зброєю.'), 'RankedBoost: S'],
                ['B', t('Воин · Оружие', 'Warrior · Arms', 'Воїн · Зброя'), t('В дуэлях беты слаб.', 'Weak in beta duels.', 'У дуелях бети слабкий.'), 'gamer-guides: A'],
                ['B*', t('Воин · Неистовство', 'Warrior · Fury', 'Воїн · Лють'), '—', 'RankedBoost: A'],
                ['B*', t('Паладин · Свет', 'Paladin · Holy', 'Паладин · Світло'), '—', 'RankedBoost: A'],
                ['B', t('Паладин · Защита', 'Paladin · Protection', 'Паладин · Захист'), '—', '—'],
                ['B', t('Охотник · Повелитель зверей', 'Hunter · Beast Mastery', 'Мисливець · Володіння звірами'), '—', '—'],
                ['B*', t('Шаман · Стихии', 'Shaman · Elemental', 'Шаман · Стихії'), t('Усилены 15.10.', 'Buffed on Oct 15.\xa0', 'Підсилені 15 жовтня.'), 'RankedBoost: A'],
                ['B', t('Шаман · Исцеление', 'Shaman · Restoration', 'Шаман · Зцілення'), '—', '—'],
                ['—', t('Маг · Огонь', 'Mage · Fire', 'Маг · Вогонь'), t('Нет PvP-оценок источников', 'No source PvP ratings', 'Немає PvP-оцінок джерел'), '—'],
                ['B*', t('Друид · Исцеление', 'Druid · Restoration', 'Друїд · Зцілення'), '—', 'gamer-guides: A'],
                ['C', t('Воин · Защита', 'Warrior · Protection', 'Воїн · Захист'), '—', '—'],
                ['C*', t('Жрец · Свет', 'Priest · Holy', 'Жрець · Світло'), t('Без иммунитетов.', 'No immunities.', 'Без імунітетів.'), 'RankedBoost: D'],
            ]}),
            ('tip', t('Воин в дуэлях беты внизу, но турнир 1 на 1 — не поле боя. Kami-labs ждёт, что на полях боя воин поднимется.', 'Warrior sits at the bottom in beta duels, but a 1v1 tournament is not a battleground. Kami-labs expects warriors to rise in battlegrounds.', 'Воїн у дуелях бети внизу, але турнір 1 на 1 — не поле бою. Kami-labs чекає, що на полях бою воїн підніметься.')),
            ('raw', t('<p><a class="more-l" href="../pvp/">PvP в WoW Forever: звания, награды и поля боя</a></p>',
                      '<p><a class="more-l" href="../pvp/">PvP in WoW Forever: ranks, rewards and battlegrounds</a></p>',
                      '<p><a class="more-l" href="../pvp/">PvP у WoW Forever: звання, нагороди й поля бою</a></p>')),
        ]},
        {'id': 'disputed', 'title': t('Где источники расходятся', 'Where sources disagree', 'Де джерела розходяться'), 'blocks': [
            ('steps', [
                {'t': t('Охотник в PvE', 'Hunter in PvE', 'Мисливець у PvE'),
                 'd': t('Noobtoboss ставит S, RankedBoost — A.', 'Noobtoboss gives S, RankedBoost gives A.', 'Noobtoboss ставить S, RankedBoost — A.')},
                {'t': t('Кто сильнее, Паладин или Охотник', 'Which is stronger, Paladin or Hunter', 'Хто сильніший, Паладин чи Мисливець'),
                 'd': t('В одном списке S только у Паладина, в другом у обоих.', 'One list gives S only to Paladin, another to both.', 'В одному списку S лише в Паладина, в іншому в обох.')},
                {'t': t('Жрец на прокачке', 'Priest while leveling', 'Жрець на прокачуванні'),
                 'd': t('Noobtoboss — C, gamer-guides — S для Послушания.', 'Noobtoboss says C, gamer-guides says S for Discipline.', 'Noobtoboss — C, gamer-guides — S для Послуху.')},
                {'t': t('Жрец, Свет', 'Priest, Holy', 'Жрець, Світло'),
                 'd': t('RankedBoost в одном списке ставит его в S, B и D.', 'RankedBoost puts it in S, B and D in a single list.', 'RankedBoost в одному списку ставить його в S, B і D.')},
                {'t': t('Маг в PvP', 'Mage in PvP', 'Маг у PvP'),
                 'd': t('RankedBoost ставит Тайную магию в S.', 'RankedBoost puts Arcane in S.', 'RankedBoost ставить Тайну магію в S.')},
            ]),
        ]},
        {'id': 'gabella', 'title': t('Оценка Gabella', 'Gabella’s view', 'Оцінка Gabella'), 'blocks': [
            ('text', [t('Мы сверили буквы источников со способностями спеков: контроль, баффы, лечение, живучесть. Урон не мерили, поэтому своих букв не ставим. Показываем только сдвиг: где по способностям спек выше или ниже, чем у источников.', 'We checked the sources’ letters against each spec’s abilities: control, buffs, healing, survivability. We haven’t measured damage, so we don’t give letters of our own. We only show the shift: where a spec’s abilities put it higher or lower than the sources do.', 'Ми звірили літери джерел зі здібностями спеціалізацій: контроль, бафи, лікування, живучість. Шкоду не міряли, тому власних літер не ставимо. Показуємо лише зсув: де за здібностями спеціалізація вища чи нижча, ніж у джерел.'),
                      t('Спеки, которых здесь нет, — без сдвига. Спеков урона в PvE здесь нет вовсе: их место решает урон.', 'Specs not listed here have no shift. Damage specs in PvE are left out entirely: damage decides their place.', 'Спеціалізації, яких тут немає, — без зсуву. Спеціалізацій шкоди в PvE тут немає взагалі: їхнє місце визначає шкода.')]),
            ('tip', t('По бете. После старта 5 ноября заменим живыми данными: логи, время прокачки, поля боя.', 'Beta data. After the Nov 4–5 launch we’ll replace it with live data: logs, leveling times, battlegrounds.', 'За бетою. Після старту 5 листопада замінимо живими даними: логи, час прокачування, поля бою.')),
            ('tabs', [
                {'id': 'g-leveling', 't': t('Прокачка соло', 'Solo leveling', 'Прокачування соло'), 'blocks': [
                    ('table', {'head': [t('Спек', 'Spec', 'Спеціалізація'), 'Gabella', t('Почему', 'Why', 'Чому')], 'rows': [
                [t('Охотник · Повелитель зверей', 'Hunter · Beast Mastery', 'Мисливець · Володіння звірами'), t('↓\xa0ниже', '↓\xa0lower', '↓\xa0нижче'), t('Нет самолечения; скорость убийства мы не мерили.', 'No self-healing; we haven’t measured kill speed.', 'Немає самолікування; швидкість убивства ми не міряли.')],
                [t('Маг · Лёд', 'Mage · Frost', 'Маг · Лід'), t('↓\xa0ниже', '↓\xa0lower', '↓\xa0нижче'), t('Урон по площади на прокачке ослаблен, мана — слабое место.', 'Area damage is nerfed for leveling, and mana is a weak spot.', 'Шкоду по площі на прокачуванні послаблено, мана — слабке місце.')],
                [t('Разбойник · Ликвидация или Бой', 'Rogue · Assassination or Combat', 'Розбійник · Ліквідація або Бій'), t('↓\xa0ниже', '↓\xa0lower', '↓\xa0нижче'), t('Нет самолечения: после каждого боя отдых.', 'No self-healing: rest after every fight.', 'Немає самолікування: після кожного бою відпочинок.')],
                [t('Жрец · Темная магия', 'Priest · Shadow', 'Жрець · Темрява'), t('↑\xa0выше', '↑\xa0higher', '↑\xa0вище'), t('Самолечение и дешёвые заклинания в Облике Тьмы.', 'Self-healing and cheap spells in Shadowform.', 'Самолікування й дешеві заклинання в Shadowform.')],
            ]}),
                ]},
                {'id': 'g-pve', 't': t('Танки и лекари', 'Tanks and healers', 'Танки й цілителі'), 'blocks': [
                    ('table', {'head': [t('Спек', 'Spec', 'Спеціалізація'), 'Gabella', t('Почему', 'Why', 'Чому')], 'rows': [
                [t('Воин · Защита', 'Warrior · Protection', 'Воїн · Захист'), t('↑\xa0выше в рейде', '↑\xa0higher in raids', '↑\xa0вище в рейді'), t('Полный набор танка, ярость не кончается в долгом бою.', 'A full tank toolkit; rage doesn’t run out in long fights.', 'Повний набір танка, ярість не закінчується в довгому бою.')],
                [t('Друид · Сила зверя (медведь)', 'Druid · Feral (bear)', 'Друїд · Сила звіра (ведмідь)'), t('↑\xa0выше в подземельях', '↑\xa0higher in dungeons', '↑\xa0вище в підземеллях'), t('Первый медведь в группе: Вожак стаи и воскрешение в бою.', 'The first bear in a group: Leader of the Pack and a combat resurrection.', 'Перший ведмідь у групі: Leader of the Pack і воскресіння в бою.')],
                [t('Друид · Исцеление', 'Druid · Restoration', 'Друїд · Зцілення'), t('↑\xa0выше', '↑\xa0higher', '↑\xa0вище'), t('Буйный рост, эффекты лечения складываются.', 'Wild Growth; healing effects stack.', 'Wild Growth, ефекти лікування складаються.')],
                [t('Жрец · Свет', 'Priest · Holy', 'Жрець · Світло'), t('↑\xa0выше', '↑\xa0higher', '↑\xa0вище'), t('Полный набор лекаря: лечение по площади и возврат маны.', 'A full healer toolkit: area healing and mana return.', 'Повний набір цілителя: лікування по площі й повернення мани.')],
            ]}),
                ]},
                {'id': 'g-pvp', 't': 'PvP', 'blocks': [
                    ('text', [t('Сдвиг считаем по контролю и бурсту. Живучесть — в колонке «Почему».', 'The shift is based on control and burst. Survivability is in the “Why” column.', 'Зсув рахуємо за контролем і бурстом. Живучість — у колонці «Чому».')]),
                    ('table', {'head': [t('Спек', 'Spec', 'Спеціалізація'), 'Gabella', t('Почему', 'Why', 'Чому')], 'rows': [
                [t('Охотник · Стрельба', 'Hunter · Marksmanship', 'Мисливець · Стрільба'), t('↑\xa0выше', '↑\xa0higher', '↑\xa0вище'), t('Ловушки в бою и сильное окно урона; живучесть низкая.', 'Traps in combat and a strong damage window; low survivability.', 'Пастки в бою й сильне вікно шкоди; живучість низька.')],
                [t('Охотник · Повелитель зверей', 'Hunter · Beast Mastery', 'Мисливець · Володіння звірами'), t('↑\xa0выше', '↑\xa0higher', '↑\xa0вище'), t('Ловушки в бою и Устрашение; живучесть низкая.', 'Traps in combat and Intimidation; low survivability.', 'Пастки в бою й Intimidation; живучість низька.')],
                [t('Маг · Тайная магия', 'Mage · Arcane', 'Маг · Тайна магія'), t('↑\xa0выше', '↑\xa0higher', '↑\xa0вище'), t('Контроль мага и сильный бурст.', 'Mage control and strong burst.', 'Контроль мага й потужний бурст.')],
                [t('Чернокнижник · Разрушение', 'Warlock · Destruction', 'Чорнокнижник · Руйнування'), t('↑\xa0выше', '↑\xa0higher', '↑\xa0вище'), t('Контроль и сильный бурст; живучесть низкая.', 'Control and strong burst; low survivability.', 'Контроль і потужний бурст; живучість низька.')],
                [t('Жрец · Свет', 'Priest · Holy', 'Жрець · Світло'), t('↑\xa0выше', '↑\xa0higher', '↑\xa0вище'), t('Контроль, урон и живучесть средние.', 'Average control, damage and survivability.', 'Контроль, шкода й живучість середні.')],
                [t('Жрец · Послушание', 'Priest · Discipline', 'Жрець · Послух'), t('↓\xa0ниже', '↓\xa0lower', '↓\xa0нижче'), t('Сила в щитах и Покаянии, а не в контроле; здесь источники, вероятно, точнее.', 'Its strength is shields and Penance, not control; here the sources are probably closer.', 'Сила в щитах і Penance, а не в контролі; тут джерела, імовірно, точніші.')],
                [t('Паладин · Воздаяние', 'Paladin · Retribution', 'Паладин · Відплата'), t('↓\xa0ниже', '↓\xa0lower', '↓\xa0нижче'), t('Контроль и бурст средние.', 'Average control and burst.', 'Контроль і бурст середні.')],
                [t('Жрец · Темная магия', 'Priest · Shadow', 'Жрець · Темрява'), t('↓\xa0ниже', '↓\xa0lower', '↓\xa0нижче'), t('Контроль и бурст средние, живучесть низкая.', 'Average control and burst; low survivability.', 'Контроль і бурст середні, живучість низька.')],
                [t('Шаман · Совершенствование', 'Shaman · Enhancement', 'Шаман · Вдосконалення'), t('↓\xa0ниже', '↓\xa0lower', '↓\xa0нижче'), t('Контроль и бурст средние; живучесть высокая.', 'Average control and burst; high survivability.', 'Контроль і бурст середні; живучість висока.')],
                [t('Друид · Баланс', 'Druid · Balance', 'Друїд · Баланс'), t('↓\xa0ниже', '↓\xa0lower', '↓\xa0нижче'), t('Контроль средний, одно окно урона; живучесть высокая.', 'Average control, one damage window; high survivability.', 'Контроль середній, одне вікно шкоди; живучість висока.')],
                [t('Друид · Сила зверя', 'Druid · Feral', 'Друїд · Сила звіра'), t('↓\xa0ниже', '↓\xa0lower', '↓\xa0нижче'), t('Контроль средний, одно окно урона; живучесть высокая.', 'Average control, one damage window; high survivability.', 'Контроль середній, одне вікно шкоди; живучість висока.')],
                [t('Воин · Неистовство', 'Warrior · Fury', 'Воїн · Лють'), t('↓\xa0ниже', '↓\xa0lower', '↓\xa0нижче'), t('Мало контроля, живучесть низкая.', 'Little control; low survivability.', 'Мало контролю, живучість низька.')],
                [t('Паладин · Свет', 'Paladin · Holy', 'Паладин · Світло'), t('↓\xa0ниже', '↓\xa0lower', '↓\xa0нижче'), t('Ветка лечения: урона мало, зато трудно убить.', 'A healing tree: little damage, but hard to kill.', 'Гілка лікування: шкоди мало, зате важко вбити.')],
                [t('Паладин · Защита', 'Paladin · Protection', 'Паладин · Захист'), t('↓\xa0ниже', '↓\xa0lower', '↓\xa0нижче'), t('Ветка танка: мало урона и контроля.', 'A tank tree: little damage and control.', 'Гілка танка: мало шкоди й контролю.')],
                [t('Шаман · Исцеление', 'Shaman · Restoration', 'Шаман · Зцілення'), t('↓\xa0ниже', '↓\xa0lower', '↓\xa0нижче'), t('Ветка лечения: урона мало, зато трудно убить.', 'A healing tree: little damage, but hard to kill.', 'Гілка лікування: шкоди мало, зате важко вбити.')],
                [t('Друид · Исцеление', 'Druid · Restoration', 'Друїд · Зцілення'), t('↓\xa0ниже', '↓\xa0lower', '↓\xa0нижче'), t('Ветка лечения: урона мало, зато трудно убить.', 'A healing tree: little damage, but hard to kill.', 'Гілка лікування: шкоди мало, зате важко вбити.')],
            ]}),
                ]},
            ]),
        ]},
        {'id': 'after', 'title': t('Что изменится после старта', 'What will change after launch', 'Що зміниться після старту'), 'blocks': [
            ('steps', [
                {'t': t('Уровни 31–60', 'Levels 31–60', 'Рівні 31–60'),
                 'd': t('на бете их не было, многие таланты и умения открываются выше 30.', 'they weren’t in the beta, and many talents and abilities unlock above 30.', 'у бета-версії їх не було, а багато талантів і умінь відкривається вище 30.')},
                {'t': t('Рейды с 09.12', 'Raids from Dec 9', 'Рейди з 9 грудня'),
                 'd': t('оценки рейдовых спеков пока без логов.', 'raid spec ratings have no logs yet.', 'оцінки рейдових спеціалізацій поки що без логів.')},
                {'t': t('Поля боя', 'Battlegrounds', 'Поля бою'),
                 'd': t('все PvP-оценки сейчас по дуэлям.', 'all PvP ratings are currently based on duels.', 'усі PvP-оцінки наразі за дуелями.')},
                {'t': t('Правки баланса', 'Balance changes', 'Правки балансу'),
                 'd': t('15.10 ослаблены Воздаяние и Защита паладина, усилены Стихии, Совершенствование и Темная магия. Noobtoboss ждёт ослабления Охотника и Паладина.', 'on Oct 15 Retribution and Paladin Protection were nerfed; Elemental, Enhancement and Shadow were buffed. Noobtoboss expects nerfs for Hunter and Paladin.', '15 жовтня послабили Відплату й Захист паладина, підсилили Стихії, Вдосконалення й Темряву. Noobtoboss чекає послаблення Мисливця та Паладина.')},
            ]),
        ]},
        {'id': 'faq', 'title': t('Частые вопросы', 'Common questions', 'Часті питання'), 'blocks': [
            ('faq', [
                {'id': 'q1', 'q': t('Какой класс самый сильный в WoW Forever?', 'Which class is the strongest in WoW Forever?', 'Який клас найсильніший у WoW Forever?'),
                 'a': [t('По бете — Паладин в PvE, Чернокнижник и Разбойник в PvP. Это данные 30 уровня, обновим после старта 5 ноября.', 'By beta data: Paladin in PvE, Warlock and Rogue in PvP. This is level 30 data; we’ll update it after the Nov 4–5 launch.', 'За бетою — Паладин у PvE, Чорнокнижник і Розбійник у PvP. Це дані 30 рівня, оновимо після старту 5 листопада.')]},
                {'id': 'q2', 'q': t('Какой класс быстрее всех качается?', 'Which class levels fastest?', 'Який клас прокачується найшвидше?'),
                 'a': [t('Охотник и Маг, примерно на 8% быстрее среднего. Медленнее всех Воин.', 'Hunter and Mage, about 8% faster than average. Warrior is the slowest.', 'Мисливець і Маг, приблизно на 8% швидше за середнє. Найповільніший — Воїн.')]},
                {'id': 'q3', 'q': t('Какой лекарь лучший?', 'Which healer is the best?', 'Який цілитель найкращий?'),
                 'a': [t('Жрец Послушания и Шаман Исцеления.', 'Discipline Priest and Restoration Shaman.', 'Жрець Послуху та Шаман Зцілення.')]},
                {'id': 'q4', 'q': t('Какой танк лучший?', 'Which tank is the best?', 'Який танк найкращий?'),
                 'a': [t('Паладин Защиты, следом Воин Защиты.', 'Protection Paladin, followed by Protection Warrior.', 'Паладин Захисту, далі Воїн Захисту.')]},
                {'id': 'q5', 'q': t('Можно ли верить тир-листу до релиза?', 'Can I trust the tier list before release?', 'Чи можна вірити тір-листу до релізу?'),
                 'a': [t('Как ориентиру: на бете не было уровней 31–60, рейдов и полей боя, к 60 уровню расклад может измениться.', 'As a guide: the beta had no levels 31–60, raids or battlegrounds, so the picture may change by level 60.', 'Як орієнтиру: у бета-версії не було рівнів 31–60, рейдів і полів бою, тож до 60 рівня розклад може змінитися.')]},
            ]),
        ]},
        {'id': 'related', 'title': t('Смотрите также', 'See also', 'Дивіться також'), 'blocks': [
            ('tiles', [{'t': t('Лучшая раса для каждого класса', 'Best Race for Every Class', 'Найкраща раса для кожного класу'), 'd': t('Какая раса сильнее для вашего класса', 'Which race is stronger for your class', 'Яка раса сильніша для вашого класу'), 'href': 'guides/best-race/', 'art': 'hero_bestrace'}, {'t': t('Классы', 'Classes', 'Класи'), 'd': t('Какой класс выбрать и сравнение', 'Which class to pick, compared', 'Який клас обрати й порівняння'), 'href': 'classes/', 'art': 'hero_classes'}]),
        ]},
    ],
})
if TL.changes_section(TL_STATUS):                                  # «Что изменилось» opens the page; no notes, no block
    GUIDES[-1]['sections'].insert(0, TL.changes_section(TL_STATUS))


# ---------- pvp: система PvP по официальным статьям Blizzard; спеки и расы — из тир-листа и «Лучшей расы» (одни данные) ----------

PVP_NEWS = 'https://news.blizzard.com/en-us/article/24303316/how-pvp-progression-in-world-of-warcraft-forever-works'
PVP_DSI = 'https://news.blizzard.com/en-us/article/24307308/battle-for-the-darkspear-islands-in-world-of-warcraft-forever'


def _pvp_classes():
    """PvP by class: the best-rated spec of each class in the tier list's PvP table (a tie goes to the letter without a star),
    its build anchor, and the PvP races of the Best Race table. The same dicts as on those pages: one source of truth."""
    def table(slug, sec):
        g = next(x for x in GUIDES if x['slug'] == slug)
        return next(d for k, d in next(s for s in g['sections'] if s['id'] == sec)['blocks'] if k == 'table')['rows']
    rank = {'S': 0, 'A': 1, 'B': 2, 'C': 3}
    tl, rows = table('tier-list', 'pvp'), []
    for r in table('best-race', 'table'):
        mine = [x for x in tl if x[1]['ru'].split(' · ')[0] == r[0]['ru'] and x[0].rstrip('*') in rank]
        best = min(mine, key=lambda x: (rank[x[0].rstrip('*')], x[0].endswith('*')))
        cid = r[0]['en'].lower()
        sid = best[1]['en'].split(' · ')[1].lower().replace(' ', '-')
        rows.append([(best[1], f'guides/builds-{cid}/#{sid}'), best[0], r[3], r[4]])
    return rows


GUIDES.append({
    'slug': 'pvp', 'art': 'hero_dusk', 'hero': 'hero_dusk', 'og': 'guides',
    'title': t('PvP в WoW Forever', 'PvP in WoW Forever', 'PvP у WoW Forever'),
    'crumb': 'PvP',
    'lead': t('PvP в Forever держится на Чести, очках звания и сезонах. Здесь всё, что Blizzard объявила официально: награды званий 1–14, наборы за Честь, новое поле боя Darkspear Islands. И честно о том, чего пока нет ни у кого: PvP-билдов по спекам на данных полей боя.',
              'PvP in Forever runs on Honor, Rank Points and seasons. This page has everything Blizzard has officially announced: rewards for ranks 1–14, Honor gear sets, the new Darkspear Islands battleground. It is also clear about what nobody has yet: PvP builds per spec based on battleground data.',
              'PvP у Forever тримається на Честі, очках звання та сезонах. Тут усе, що Blizzard оголосила офіційно: нагороди звань 1–14, набори за Честь, нове поле бою Darkspear Islands. І чесно про те, чого поки немає ні в кого: PvP-білдів за спеціалізаціями на даних полів бою.'),
    'tile': t('Звания 1–14, Честь, наборы и поля боя', 'Ranks 1–14, Honor, gear and battlegrounds', 'Звання 1–14, Честь, набори й поля бою'),
    'pills': [t('Звания 1–14', 'Ranks 1–14', 'Звання 1–14'), t('По данным Blizzard', 'Per Blizzard', 'За даними Blizzard'),
              t('Билды — после первой недели', 'Builds after the first week', 'Білди — після першого тижня')],
    'sources': [
        (t('Blizzard: как работает PvP в Forever (07.10)', 'Blizzard: How PvP Progression in Forever Works (Oct 7)', 'Blizzard: як працює PvP у Forever (07.10)'), PVP_NEWS),
        (t('Blizzard: поле боя Darkspear Islands', 'Blizzard: Battle for the Darkspear Islands', 'Blizzard: поле бою Darkspear Islands'), PVP_DSI),
        (t('Blizzard: система Legacy', 'Blizzard: Legacy system', 'Blizzard: система Legacy'), 'https://news.blizzard.com/en-gb/article/24307383'),
        (t('Blizzard: обзор панели Forever, 12.09', 'Blizzard: Forever panel recap, Sep 12', 'Blizzard: огляд панелі Forever, 12.09'), 'https://worldofwarcraft.blizzard.com/en-us/news/24303862'),
    ],
    'sections': [
        {'id': 'how', 'title': t('Как устроено', 'How it works', 'Як це влаштовано'), 'blocks': [
            ('steps', [
                {'t': t('Честь (Honor)', 'Honor', 'Честь (Honor)'),
                 'd': t('Валюта за PvP: победы над игроками, поля боя и PvP-задания. В праздничную неделю выделенное поле боя даёт больше Чести. Blizzard выровняла Честь между полями боя, чтобы не приходилось ходить только в Alterac Valley.',
                        'The PvP currency: defeating players, battlegrounds and PvP quests. During its holiday week a highlighted battleground gives more Honor. Blizzard evened out Honor across battlegrounds so you don’t have to queue for Alterac Valley alone.',
                        'Валюта за PvP: перемоги над гравцями, поля бою та PvP-завдання. У святковий тиждень виділене поле бою дає більше Честі. Blizzard вирівняла Честь між полями бою, щоб не доводилося ходити лише в Alterac Valley.')},
                {'t': t('Очки звания (Rank Points)', 'Rank Points', 'Очки звання (Rank Points)'),
                 'd': t('Даются за поля боя и PvP-задания, в праздничную неделю — с прибавкой. Ведут по званиям оригинальной игры к вершине: High Warlord у Орды, Grand Marshal у Альянса.',
                        'Earned from battlegrounds and PvP quests, with a boost in holiday weeks. They take you through the ranks of the original game to the top titles: High Warlord for the Horde, Grand Marshal for the Alliance.',
                        'Даються за поля бою та PvP-завдання, у святковий тиждень — із надбавкою. Ведуть званнями оригінальної гри до вершини: High Warlord в Орди, Grand Marshal в Альянсу.')},
                {'t': t('Недельный лимит', 'Weekly cap', 'Тижневий ліміт'),
                 'd': t('У званий есть недельный лимит, поэтому до 14 звания идут неделями, а не за один марафон. Само число Blizzard не назвала.',
                        'Ranks have a weekly cap, so rank 14 takes weeks rather than one marathon. Blizzard has not given the number.',
                        'Звання мають тижневий ліміт, тож до 14 звання йдуть тижнями, а не за один марафон. Саме число Blizzard не назвала.')},
                {'t': t('Где смотреть', 'Where to check', 'Де дивитися'),
                 'd': t('Окно персонажа (C), вкладка PvP справа: звание, очки звания и награды, которые уже можно купить.',
                        'Character pane (C), the PvP tab on the right: your rank, Rank Points and the rewards you can already buy.',
                        'Вікно персонажа (C), вкладка PvP праворуч: звання, очки звання й нагороди, які вже можна купити.')},
            ]),
            ('tip', t('Задачи сезонного пути дают и Честь, и очки звания, а три из них ещё и очко Legacy. Закрывайте их каждую неделю, пока не упёрлись в лимит.',
                      'Seasonal journey tasks give both Honor and Rank Points, and three of them also give a Legacy point. Clear them every week before you hit the cap.',
                      'Завдання сезонного шляху дають і Честь, і очки звання, а три з них ще й очко Legacy. Закривайте їх щотижня, доки не вперлися в ліміт.')),
        ]},
        {'id': 'ranks', 'title': t('Награды званий 1–14', 'Rank rewards 1–14', 'Нагороди звань 1–14'), 'blocks': [
            ('text', [t('Список наград — из статьи Blizzard 07.10. Колонка Legacy — из статьи о Legacy: пять званий дают по очку. Названия званий 1–13 для Forever Blizzard не публиковала.',
                        'The reward list is from Blizzard’s Oct 7 article. The Legacy column is from the Legacy article: five ranks give a point each. Blizzard has not published the names of ranks 1–13 for Forever.',
                        'Список нагород — зі статті Blizzard 07.10. Колонка Legacy — зі статті про Legacy: п’ять звань дають по очку. Назви звань 1–13 для Forever Blizzard не публікувала.')]),
            ('table', {'head': [t('Звание', 'Rank', 'Звання'), t('Награда', 'Reward', 'Нагорода'), 'Legacy'], 'rows': [
                ['1', t('Табард', 'Tabard', 'Табард'), '—'],
                ['2', t('PvP-аксессуар', 'PvP trinket', 'PvP-аксесуар'), '—'],
                ['3', t('Плащи', 'Cloaks', 'Плащі'), '+1'],
                ['4', t('Ожерелье', 'Necklace', 'Намисто'), '—'],
                ['5', t('Боевые зелья', 'Combat potions', 'Бойові зілля'), '—'],
                ['6', t('Табард', 'Tabard', 'Табард'), '—'],
                ['7', t('Боевой штандарт', 'Battle standard', 'Бойовий штандарт'), '+1'],
                ['8', t('Эпические наручи или пояс: жетон улучшения', 'Epic bracers or belt: upgrade token', 'Епічні наручі або пояс: жетон покращення'), '—'],
                ['9', t('Эпические сапоги: жетон улучшения', 'Epic boots: upgrade token', 'Епічні чоботи: жетон покращення'), '—'],
                ['10', t('Эпические перчатки: жетон улучшения', 'Epic gloves: upgrade token', 'Епічні рукавиці: жетон покращення'), '+1'],
                ['11', t('Скакуны', 'Mounts', 'Скакуни'), '—'],
                ['12', t('Эпические поножи или наплечники: жетон улучшения', 'Epic legs or shoulders: upgrade token', 'Епічні поножі або наплічники: жетон покращення'), '—'],
                ['13', t('Эпический нагрудник или шлем: жетон улучшения', 'Epic chest or helm: upgrade token', 'Епічний нагрудник або шолом: жетон покращення'), '+1'],
                ['14', t('Эпическое оружие', 'Epic weapons', 'Епічна зброя'), '+1'],
            ]}),
        ]},
        {'id': 'gear', 'title': t('Снаряжение за Честь', 'Honor gear', 'Спорядження за Честь'), 'blocks': [
            ('steps', [
                {'t': t('Синий набор', 'Blue set', 'Синій набір'),
                 'd': t('Покупается за Честь.', 'Bought with Honor.', 'Купується за Честь.')},
                {'t': t('Эпический набор', 'Epic set', 'Епічний набір'),
                 'd': t('Синяя вещь плюс Emboldened Seal превращаются в эпическую. Каждую печать можно купить только с нужным званием.',
                        'A blue piece plus an Emboldened Seal upgrades to the epic one. Each seal can only be bought once you reach its rank.',
                        'Синя річ плюс Emboldened Seal перетворюються на епічну. Кожну печатку можна купити лише з потрібним званням.')},
                {'t': t('Наборы под спеки', 'Sets for specs', 'Набори під спеціалізації'),
                 'd': t('Blizzard добавила и переделала вещи для спеков, которым раньше не было PvP-набора. Пример: у Шамана три набора — лекаря, ближнего боя и заклинателя.',
                        'Blizzard added and reworked items for specs that used to have no PvP set. For example, the Shaman now has three sets: healer, melee and caster.',
                        'Blizzard додала й переробила речі для спеціалізацій, у яких раніше не було PvP-набору. Приклад: у Шамана три набори — цілителя, ближнього бою та заклинача.')},
            ]),
            ('text', [t('Названия вещей, статы, цены в Чести и звания для печатей Blizzard не публиковала. Таблицу наборов по классам добавим, когда предметы появятся в игре.',
                        'Blizzard has not published item names, stats, Honor prices or the ranks required for seals. We will add a table of sets by class once the items are in the game.',
                        'Назви речей, стати, ціни в Честі та звання для печаток Blizzard не публікувала. Таблицю наборів за класами додамо, коли предмети з’являться в грі.')]),
        ]},
        {'id': 'seasons', 'title': t('Сезоны и Legacy', 'Seasons and Legacy', 'Сезони та Legacy'), 'blocks': [
            ('steps', [
                {'t': t('Сезонный путь', 'Seasonal journey', 'Сезонний шлях'),
                 'd': t('В каждом сезоне есть путь с недельными задачами. За задачи дают Честь и очки звания.',
                        'Each season has a journey of weekly tasks. Tasks give Honor and Rank Points.',
                        'У кожному сезоні є шлях із тижневими завданнями. За завдання дають Честь і очки звання.')},
                {'t': t('12 очков Legacy', '12 Legacy points', '12 очок Legacy'),
                 'd': t('Звания 3, 7, 10, 13 и 14 (5 очков); «Превознесение» (Exalted) с репутацией каждого поля боя (4 очка); задачи 4, 7 и 10 недели пути Field of Honor (3 очка).',
                        'Ranks 3, 7, 10, 13 and 14 (5 points); Exalted with each battleground reputation (4 points); the week 4, 7 and 10 tasks of the Field of Honor journey (3 points).',
                        'Звання 3, 7, 10, 13 і 14 (5 очок); Exalted із репутацією кожного поля бою (4 очки); завдання 4, 7 і 10 тижня шляху Field of Honor (3 очки).')},
                {'t': t('Не сгорают', 'They don’t expire', 'Не згорають'),
                 'd': t('Задачи с очком Legacy привязаны к Legacy, поэтому их можно закрыть и в следующих сезонах.',
                        'The tasks with a Legacy point are tied to Legacy, so you can still complete them in later seasons.',
                        'Завдання з очком Legacy прив’язані до Legacy, тож їх можна закрити й у наступних сезонах.')},
                {'t': t('Перк For Great Honor', 'For Great Honor perk', 'Перк For Great Honor'),
                 'd': t('Перк Legacy в дереве Находчивость: больше Чести в PvP, до 5 рангов.',
                        'A Legacy perk in the Resourcefulness tree: more Honor from PvP, up to 5 ranks.',
                        'Перк Legacy в дереві Винахідливість: більше Честі в PvP, до 5 рангів.')},
            ]),
            ('text', [t('Длительность сезона, дату первого сезона и то, сбрасывается ли звание между сезонами, Blizzard не объявила. PvP-испытания Legacy в Hardcore выполнить нельзя.',
                        'Blizzard has not announced the season length, the start of the first season or whether ranks reset between seasons. PvP Legacy challenges cannot be completed in Hardcore.',
                        'Тривалість сезону, дату першого сезону і те, чи скидається звання між сезонами, Blizzard не оголосила. PvP-випробування Legacy в Hardcore виконати не можна.')]),
        ]},
        {'id': 'battlegrounds', 'title': t('Поля боя', 'Battlegrounds', 'Поля бою'), 'blocks': [
            ('text', [t('Darkspear Islands — новое поле боя Forever. Полного списка полей боя на старте Blizzard не публиковала: Alterac Valley упомянута в статье о Чести, остальное сверим в игре 05.11.',
                        'Darkspear Islands is Forever’s new battleground. Blizzard has not published the full list of battlegrounds at launch: Alterac Valley is mentioned in the Honor article, and we will check the rest in the game on Nov 5.',
                        'Darkspear Islands — нове поле бою Forever. Повного списку полів бою на старті Blizzard не публікувала: Alterac Valley згадано в статті про Честь, решту звіримо в грі 05.11.')]),
            ('table', {'head': ['Darkspear Islands', t('По данным Blizzard', 'Per Blizzard', 'За даними Blizzard')], 'rows': [
                [t('Формат', 'Format', 'Формат'), t('15 на 15: захват точек и флаг', '15v15: capture points and a flag', '15 на 15: захоплення точок і прапор')],
                [t('Где', 'Where', 'Де'), t('У побережья [[Пылевых топей|Dustwallow Marsh]]', 'Off the coast of Dustwallow Marsh', 'Біля узбережжя Dustwallow Marsh')],
                [t('Уровни', 'Levels', 'Рівні'), '30–60'],
                [t('Победа', 'Victory', 'Перемога'), t('Первая команда, набравшая 2000 очков', 'The first team to 2000 points', 'Перша команда, що набрала 2000 очок')],
                [t('Как набирать очки', 'How to score', 'Як набирати очки'), t('Держать четыре точки: чем больше точек, тем быстрее идут очки. Флаг в центре карты отнести на базу, которую держит ваша команда.', 'Hold the four capture points: the more you hold, the faster points come. Take the flag in the middle of the map to a base your team controls.', 'Тримати чотири точки: що більше точок, то швидше йдуть очки. Прапор у центрі мапи віднести на базу, яку тримає ваша команда.')],
                [t('Очередь', 'Queue', 'Черга'), t('У распорядителя боя в любой столице или в [[Степях|The Barrens]]: база Darkspear Raiders (Орда) на Merchant Coast и Theramore Expeditionary Force (Альянс) в Northwatch, оттуда портал на поле боя.', 'At a battlemaster in any capital city, or in the Barrens: the Darkspear Raiders base (Horde) on the Merchant Coast and the Theramore Expeditionary Force base (Alliance) at Northwatch, with a portal into the battle.', 'У розпорядника бою в будь-якій столиці або в The Barrens: база Darkspear Raiders (Орда) на Merchant Coast і Theramore Expeditionary Force (Альянс) у Northwatch, звідти портал на поле бою.')],
                [t('Награды', 'Rewards', 'Нагороди'), t('Репутация своей стороны: аксессуары, кольца, плащи, оружие, броня и расходники у торговцев баз. Задания на репутацию сдаются за Marks of Honor, на «Превознесении» (Exalted) открывается короткая цепочка за табард.', 'Your side’s reputation: trinkets, rings, cloaks, weapons, armor and consumables from the base vendors. Reputation quests are turned in for Marks of Honor, and at Exalted a short questline unlocks the tabard.', 'Репутація своєї сторони: аксесуари, кільця, плащі, зброя, броня й витратні матеріали в торговців баз. Завдання на репутацію здаються за Marks of Honor, на Exalted відкривається короткий ланцюжок за табард.')],
            ]}),
        ]},
        {'id': 'classes', 'title': t('PvP по классам', 'PvP by class', 'PvP за класами'), 'blocks': [
            ('text', [t('PvP-билдов, снаряжения и расходников по спекам на данных полей боя пока нет ни у кого: бета шла на 30 уровне, а Darkspear Islands рассчитан на 30–60. Что есть сейчас: лучший спек класса в нашем тир-листе PvP (дуэли, мировое PvP и турнир Forever Open, 30 уровень) и раса для PvP из гайда «Лучшая раса». Спек ведёт на его билд, звёздочка (*) — источники расходятся.',
                        'Nobody has PvP builds, gear or consumables per spec based on battleground data yet: the beta ran at level 30, and Darkspear Islands is for levels 30–60. What exists now: the best spec of each class in our PvP tier list (duels, world PvP and the Forever Open tournament, level 30) and the PvP race from the Best Race guide. The spec links to its build; an asterisk (*) means the sources disagree.',
                        'PvP-білдів, спорядження й витратних матеріалів за спеціалізаціями на даних полів бою поки немає ні в кого: бета йшла на 30 рівні, а Darkspear Islands розраховане на 30–60. Що є зараз: найкраща спеціалізація класу в нашому тір-листі PvP (дуелі, світове PvP і турнір Forever Open, 30 рівень) і раса для PvP з гайду «Найкраща раса». Спеціалізація веде на свій білд, зірочка (*) — джерела розходяться.')]),
            ('table', {'head': [t('Класс · спек', 'Class · spec', 'Клас · спеціалізація'), t('Тир', 'Tier', 'Тір'), t('Альянс, PvP', 'Alliance, PvP', 'Альянс, PvP'), t('Орда, PvP', 'Horde, PvP', 'Орда, PvP')],
                       'rows': _pvp_classes()}),
            ('tip', t('Для PvP почти все классы берут Инженерное дело: гранаты, бомбы и устройства дают контроль и подвижность, которых у класса нет.',
                      'For PvP almost every class takes Engineering: grenades, bombs and devices give control and mobility the class lacks.',
                      'Для PvP майже всі класи беруть Інженерію: гранати, бомби та пристрої дають контроль і рухливість, яких класу бракує.')),
        ]},
        {'id': 'unknown', 'title': t('Чего пока нет', 'Not known yet', 'Чого поки немає'), 'blocks': [
            ('text', [t('Этого Blizzard не публиковала, а на бете проверить было нельзя. Каждую строку заполним по живым данным и подпишем дату.',
                        'Blizzard has not published these, and the beta could not show them. We will fill in each line from live data and date it.',
                        'Цього Blizzard не публікувала, а на беті перевірити було неможливо. Кожен рядок заповнимо за живими даними й підпишемо дату.')]),
            ('table', {'head': [t('Что', 'What', 'Що'), t('Когда узнаем', 'When we’ll know', 'Коли дізнаємося')], 'rows': [
                [t('Честь за бой и за победу над игроком', 'Honor per battleground and per kill', 'Честь за бій і за перемогу над гравцем'), t('В первые дни после старта', 'In the first days after launch', 'У перші дні після старту')],
                [t('Очки на каждое звание и недельный лимит', 'Rank Points per rank and the weekly cap', 'Очки на кожне звання й тижневий ліміт'), t('После первого недельного сброса', 'After the first weekly reset', 'Після першого тижневого скидання')],
                [t('Названия званий 1–13', 'Names of ranks 1–13', 'Назви звань 1–13'), t('В игре, во вкладке PvP', 'In the game, on the PvP tab', 'У грі, у вкладці PvP')],
                [t('Звание для каждой Emboldened Seal, статы и цены наборов', 'The rank for each Emboldened Seal, set stats and prices', 'Звання для кожної Emboldened Seal, стати й ціни наборів'), t('В игре, у торговцев', 'In the game, at the vendors', 'У грі, у торговців')],
                [t('Поля боя на старте, кроме Darkspear Islands', 'Battlegrounds at launch besides Darkspear Islands', 'Поля бою на старті, крім Darkspear Islands'), t('05.11, в окне очереди', 'Nov 5, in the queue window', '05.11, у вікні черги')],
                [t('Праздничные недели и длительность сезона', 'Holiday weeks and season length', 'Святкові тижні й тривалість сезону'), t('Когда Blizzard объявит', 'When Blizzard announces it', 'Коли Blizzard оголосить')],
                [t('PvP-билды, снаряжение и расы по спекам', 'PvP builds, gear and races per spec', 'PvP-білди, спорядження й раси за спеціалізаціями'), t('После первой недели полей боя', 'After the first week of battlegrounds', 'Після першого тижня полів бою')],
            ]}),
        ]},
        {'id': 'faq', 'title': t('Частые вопросы', 'Common questions', 'Часті питання'), 'blocks': [
            ('faq', [
                {'id': 'q1', 'q': t('Как работает PvP в WoW Forever?', 'How does PvP work in WoW Forever?', 'Як працює PvP у WoW Forever?'),
                 'a': [t('Вы получаете Честь и очки звания за поля боя, победы над игроками и PvP-задания. Очки поднимают звание до 14 с недельным лимитом, Честь тратится на наборы. Сезонный путь с недельными задачами даёт и то и другое.',
                         'You earn Honor and Rank Points from battlegrounds, defeating players and PvP quests. Rank Points raise your rank up to 14 with a weekly cap, and Honor buys gear sets. The seasonal journey with weekly tasks gives both.',
                         'Ви отримуєте Честь і очки звання за поля бою, перемоги над гравцями та PvP-завдання. Очки піднімають звання до 14 із тижневим лімітом, Честь витрачається на набори. Сезонний шлях із тижневими завданнями дає і те, і те.')]},
                {'id': 'q2', 'q': t('Что дают звания?', 'What do the ranks give?', 'Що дають звання?'),
                 'a': [t('С 1 по 7 звание — табарды, PvP-аксессуар, плащи, ожерелье, боевые зелья и штандарт. С 8 по 13 — жетоны улучшения эпических вещей и скакуны на 11. На 14 — эпическое оружие.',
                         'Ranks 1 to 7 give tabards, a PvP trinket, cloaks, a necklace, combat potions and a battle standard. Ranks 8 to 13 give epic upgrade tokens, with mounts at 11. Rank 14 gives epic weapons.',
                         'З 1 по 7 звання — табарди, PvP-аксесуар, плащі, намисто, бойові зілля й штандарт. З 8 по 13 — жетони покращення епічних речей і скакуни на 11. На 14 — епічна зброя.')]},
                {'id': 'q3', 'q': t('Где взять PvP-снаряжение?', 'Where do I get PvP gear?', 'Де взяти PvP-спорядження?'),
                 'a': [t('Синий набор — за Честь. Эпический — синяя вещь плюс Emboldened Seal, печать продают с нужного звания. Ещё вещи дают торговцы репутации Darkspear Islands и награды званий 8–14.',
                         'The blue set costs Honor. The epic one is a blue piece plus an Emboldened Seal, sold from the required rank. More items come from the Darkspear Islands reputation vendors and the rank 8–14 rewards.',
                         'Синій набір — за Честь. Епічний — синя річ плюс Emboldened Seal, печатку продають із потрібного звання. Ще речі дають торговці репутації Darkspear Islands і нагороди звань 8–14.')]},
                {'id': 'q4', 'q': t('Какой класс лучший для PvP?', 'Which class is best for PvP?', 'Який клас найкращий для PvP?'),
                 'a': [t('По бете в S — Разбойник (Ликвидация и Скрытность), Чернокнижник (Колдовство) и Жрец (Послушание). Это дуэли 30 уровня, на полях боя расклад может измениться.',
                         'In the beta the S tier is Rogue (Assassination and Subtlety), Warlock (Affliction) and Priest (Discipline). These are level 30 duels; battlegrounds may change the picture.',
                         'За бетою в S — Розбійник (Ліквідація й Непомітність), Чорнокнижник (Прокляття) і Жрець (Послух). Це дуелі 30 рівня, на полях бою розклад може змінитися.')],
                 'link': (t('Тир-лист PvP', 'PvP tier list', 'Тір-лист PvP'), '../tier-list/#pvp')},
                {'id': 'q5', 'q': t('Какая раса лучше для PvP?', 'Which race is best for PvP?', 'Яка раса найкраща для PvP?'),
                 'a': [t('Чаще всего за Альянс — Человек, за Орду — Нежить: Воля к жизни снимает оглушения, Воля Отрекшихся — страх. Но ответ зависит от класса, разница — несколько процентов.',
                         'Most often Human for the Alliance and Undead for the Horde: Will to Survive breaks stuns, Will of the Forsaken breaks fear. The answer depends on the class, and the gap is a few percent.',
                         'Найчастіше за Альянс — Людина, за Орду — Нежить: Will to Survive знімає приголомшення, Will of the Forsaken — страх. Але відповідь залежить від класу, різниця — кілька відсотків.')],
                 'link': (t('Лучшая раса для каждого класса', 'Best Race for Every Class', 'Найкраща раса для кожного класу'), '../best-race/')},
                {'id': 'q6', 'q': t('Есть ли PvP-билды для Forever?', 'Are there PvP builds for Forever?', 'Чи є PvP-білди для Forever?'),
                 'a': [t('На данных полей боя — пока нет ни у кого. Добавим PvP по спекам после первой недели боёв. Сейчас у нас билды спеков по бете 30 уровня.',
                         'Not based on battleground data, from anyone yet. We will add PvP per spec after the first week of battles. For now we have spec builds from the level 30 beta.',
                         'На даних полів бою — поки немає ні в кого. Додамо PvP за спеціалізаціями після першого тижня боїв. Зараз у нас білди спеціалізацій за бетою 30 рівня.')],
                 'link': (t('Билды всех классов', 'Builds for all classes', 'Білди всіх класів'), '../builds/')},
                {'id': 'q7', 'q': t('Какие профессии нужны для PvP?', 'Which professions are best for PvP?', 'Які професії потрібні для PvP?'),
                 'a': [t('Инженерное дело: гранаты, бомбы и устройства дают контроль и подвижность. Вторую профессию берите под золото или свой класс.',
                         'Engineering: grenades, bombs and devices give control and mobility. Pick the second profession for gold or for your class.',
                         'Інженерія: гранати, бомби та пристрої дають контроль і рухливість. Другу професію беріть під золото або свій клас.')],
                 'link': (t('Профессии под класс', 'Professions for your class', 'Професії під клас'), '../professions/')},
                {'id': 'q8', 'q': t('PvP-сервер или обычный?', 'PvP server or Normal?', 'PvP-сервер чи звичайний?'),
                 'a': [t('На PvP-сервере на вас почти всегда могут напасть игроки другой фракции, на обычном бой с игроками — по желанию. Режим выбирают до создания персонажа, группа собирается только внутри режима, в PvP на аккаунте одна фракция.',
                         'On a PvP server players of the other faction can almost always attack you; on Normal, fighting players is your choice. You pick the mode before creating a character, groups form only within a mode, and in PvP an account has one faction.',
                         'На PvP-сервері на вас майже завжди можуть напасти гравці іншої фракції, на звичайному бій із гравцями — за бажанням. Режим обирають до створення персонажа, група збирається лише в межах режиму, у PvP на акаунті одна фракція.')],
                 'link': (t('Режимы и серверы', 'Modes and servers', 'Режими та сервери'), '../faq/#modes')},
                {'id': 'q9', 'q': t('Был ли PvP-турнир по Forever?', 'Was there a Forever PvP tournament?', 'Чи був PvP-турнір із Forever?'),
                 'a': [t('Да, Forever Open 18.10: бой 1 на 1, 30 уровень, только Орда. Первые два места заняли чернокнижники. Его итоги учтены в нашем тир-листе PvP.',
                         'Yes, the Forever Open on Oct 18: 1v1, level 30, Horde only. Warlocks took the top two places. Its results are part of our PvP tier list.',
                         'Так, Forever Open 18.10: бій 1 на 1, 30 рівень, лише Орда. Перші два місця посіли чорнокнижники. Його підсумки враховано в нашому тір-листі PvP.')]},
            ]),
        ]},
    ],
})


# ---------- Счётчик Legacy: данные блока 'lgcalc' (разметка в build_guides.render_block, логика в JS['legacy']) ----------
# Порядок галочек = порядок битов в ссылке (#l=…): не менять, иначе старые ссылки покажут другое.
LGC = {
    'ui': {
        'intro': t('Отметьте выполненные испытания и расставьте ранги перков. Отметки хранятся в этом браузере, набор можно отправить ссылкой.',
                   'Tick the challenges you have done and set perk ranks. Your marks stay in this browser, and you can send the set as a link.',
                   'Позначте виконані випробування й розставте ранги перків. Позначки зберігаються в цьому браузері, набір можна надіслати посиланням.'),
        'earned': t('Очки за испытания', 'Points earned', 'Очки за випробування'),
        'spent': t('Потрачено на перки', 'Spent on perks', 'Витрачено на перки'),
        'cap': t('Лимит 16 очков на персонажа на старте: Blizzard.', 'The limit of 16 points per character at launch: Blizzard.', 'Ліміт 16 очок на персонажа на старті: Blizzard.'),
        'ch': t('Испытания', 'Challenges', 'Випробування'),
        'pk': t('Перки', 'Perks', 'Перки'),
        'rw': t('Награды', 'Rewards', 'Нагороди'),
        'src': t('Источник: Blizzard', 'Source: Blizzard', 'Джерело: Blizzard'),
        'pksrc': t('Ранги: Warcraft Tavern, Blizzard их не публиковала. Описания перков ниже, в разделе «Перки».',
                   'Ranks: Warcraft Tavern; Blizzard has not published them. Perk descriptions are in the Perks section below.',
                   'Ранги: Warcraft Tavern, Blizzard їх не публікувала. Описи перків нижче, у розділі «Перки».'),
        'rwsrc': t('Пороги очков: демо BlizzCon по сторонним сайтам, Blizzard их не публиковала. {beta}',
                   'Point thresholds: BlizzCon demo data from third-party sites; Blizzard has not published them. {beta}',
                   'Пороги очок: демо BlizzCon зі сторонніх сайтів, Blizzard їх не публікувала. {beta}'),
        'plist': t('Шесть основных профессий, кроме сбора; Blizzard их список не называет.', 'Six main professions except gathering; Blizzard names no list.', 'Шість основних професій, крім збирання; Blizzard їх список не називає.'),
        'link': t('Ссылка на набор', 'Link to this set', 'Посилання на набір'),
        'copy': t('Скопировать ссылку', 'Copy link', 'Скопіювати посилання'),
        'reset': t('Сбросить всё', 'Clear all', 'Скинути все'),
        'less': t('меньше', 'less', 'менше'),
        'more': t('больше', 'more', 'більше'),
    },
    'groups': [
        {'id': 'cls', 't': t('Классы', 'Classes', 'Класи'), 'rows': [{'classes': ['25', '45', '60']}]},
        {'id': 'prf', 't': t('Профессии', 'Professions', 'Професії'), 'note': 'plist', 'rows': [
            {'l': t('Навык', 'Skill', 'Навичка'), 'k': '150', 'chips': [None] * 6},
            {'l': t('Навык', 'Skill', 'Навичка'), 'k': '225', 'chips': [None] * 6},
            {'l': t('Навык', 'Skill', 'Навичка'), 'k': '300', 'chips': [None] * 6}]},
        {'id': 'pvp', 't': 'PvP', 'rows': [
            {'l': t('Звание', 'Rank', 'Звання'), 'chips': ['3', '7', '10', '13', '14']},
            {'l': t('Превознесение (Exalted) у полей боя', 'Exalted with battlegrounds', 'Exalted у полів бою'), 'chips': [None] * 4},
            {'l': t('Field of Honor, неделя', 'Field of Honor, week', 'Field of Honor, тиждень'), 'chips': ['4', '7', '10']}]},
        {'id': 'dng', 't': t('Подземелья', 'Dungeons', 'Підземелля'), 'rows': [
            {'l': t('Последний босс всех подземелий уровней', 'Final boss of all dungeons of levels', 'Останній бос усіх підземель рівнів'), 'chips': ['15–25', '26–45', '46–60']}]},
        {'id': 'rd', 't': t('Рейды', 'Raids', 'Рейди'), 'rows': [{'l': None, 'chips': ['Onyxia', 'Hyjal Summit', 'Barrow Deeps']}]},
        {'id': 'adv', 't': t('Приключения', 'Adventures', 'Пригоди'), 'rows': [{'l': None, 'chips': [
            t('Вся карта мира на одном персонаже', 'The whole world map on one character', 'Уся мапа світу на одному персонажі'),
            t('Цепочка на комплект Lord Valthalak', 'Lord Valthalak dungeon set questline', 'Ланцюжок на комплект Lord Valthalak')]}]},
    ],
    'trees': [
        {'id': 'pro', 't': t('Профессии', 'Professions', 'Професії'), 'perks': [('Working Overtime', 5), ('Bountiful Harvest', 5), ('Master Chef', 5), ('Luremaster', 2), ('Performance Bonus', 3), ('Bartering', 2), ('Dedicated Study', 1)]},
        {'id': 'adv', 't': t('Приключения', 'Adventure', 'Пригоди'), 'perks': [('Well Rested', 5), ('Thrill of Adventure', 5), ('Talented', 5), ('Field Guide', 3), ('High Alert', 2), ('Field Medicine', 2), ('Frequent Flier', 1)]},
        {'id': 'res', 't': t('Находчивость (Resourcefulness)', 'Resourcefulness', 'Винахідливість (Resourcefulness)'), 'perks': [('Gourmand', 3), ('Permanence', 2), ('Reagent Economy', 1), ('Reinforce', 5), ('Diplomat', 5), ('For Great Honor', 5), ('The Quick and the Dead', 2)]},
    ],
    'rewards': [
        (15, t('игрушка Replica Ironforge Air Rifle: оглушает других игроков и ведёт счёт', 'Toy: Replica Ironforge Air Rifle, which stuns other players and keeps score', 'іграшка Replica Ironforge Air Rifle: приголомшує інших гравців і веде лік')),
        (25, t('питомец Spectral Bear Cub', 'Pet: Spectral Bear Cub', 'улюбленець Spectral Bear Cub')),
        (40, t('табард Spectral Bear Tabard', 'Tabard: Spectral Bear Tabard', 'табард Spectral Bear Tabard')),
        (55, t('скакун Reins of the Spectral Bear', 'Mount: Reins of the Spectral Bear', 'скакун Reins of the Spectral Bear')),
    ],
}

# ---------- legacy ----------

GUIDES.append({
    'slug': 'legacy', 'art': 'hero_guides', 'hero': 'hero_guides',
    'title': t('Система Legacy', 'The Legacy System', 'Система Legacy'),
    'lead': t('Legacy — прогресс на весь аккаунт Battle.net. Очки дают за испытания: уровни, профессии, PvP, подземелья и рейды. Тратите их на перки отдельно на каждом персонаже, на старте до 16 очков.', 'Legacy is progress shared across your whole Battle.net account. Challenges give you points: levels, professions, PvP, dungeons and raids. You spend them on perks separately on each character, up to 16 points at launch.', 'Legacy — прогрес на весь обліковий запис Battle.net. Очки дають за випробування: рівні, професії, PvP, підземелля та рейди. Витрачаєте їх на перки окремо на кожному персонажі, на старті до 16.'),
    'tile': t('Очки, испытания, перки и награды', 'Points, challenges, perks and rewards', 'Очки, випробування, перки та нагороди'),
    'pills': [t('65 испытаний', '65 challenges', '65 випробувань'), t('До 16 очков на персонажа на старте', 'Up to 16 points per character at launch', 'До 16 очок на персонажа на старті'), t('Открывается с первым очком (обычно 25 уровень)', 'Unlocks with your first point (usually level 25)', 'Відкривається з першим очком (зазвичай 25 рівень)')],
    'sources': [
        (t('Blizzard: система Legacy', 'Blizzard: Legacy system', 'Blizzard: система Legacy'), 'https://news.blizzard.com/en-gb/article/24307383'),
        ('Warcraft Tavern: Legacy', 'https://www.warcrafttavern.com/forever/guides/legacy/'),
    ],
    'js': 'legacy',
    'sections': [
        {'id': 'about', 'title': t('Что это за раздел', 'What this section is', 'Що це за розділ'), 'blocks': [
            ('steps', [
                {'t': t('Очки за испытания', 'Points for challenges', 'Очки за випробування'),
                 'd': t('Испытание — задание вроде «достичь 25 уровня» или «победить Onyxia». Каждое даёт 1 очко Legacy, всего их 65. Очки общие для персонажей аккаунта, кроме Hardcore (на старте его нет).',
                        'A challenge is a task such as “reach level 25” or “defeat Onyxia”. Each one gives 1 Legacy point, and there are 65 in all. Points are shared by the characters on your account, except Hardcore (not available at launch).',
                        'Випробування — завдання на кшталт «досягти 25 рівня» або «перемогти Onyxia». Кожне дає 1 очко Legacy, усього їх 65. Очки спільні для персонажів облікового запису, крім Hardcore (на старті його немає).')},
                {'t': t('Перки на персонаже', 'Perks on a character', 'Перки на персонажі'),
                 'd': t('Перк — бонус, на который вы тратите очки: например, быстрее растут навыки ремёсел или выше потолок отдыха. Перки собраны в три дерева. На старте персонаж тратит до 16 очков, и каждый выбирает свои.',
                        'A perk is a bonus you spend points on, for example faster tradeskill gains or a higher rested experience cap. Perks sit in three trees. At launch a character can spend up to 16 points, and each character picks its own.',
                        'Перк — бонус, на який ви витрачаєте очки: наприклад, швидше зростають навички ремесел або вища стеля відпочинку. Перки зібрані в три дерева. На старті персонаж витрачає до 16 очок, і кожен обирає свої.')},
                {'t': t('Награды', 'Rewards', 'Нагороди'),
                 'd': t('Накопленные на аккаунте очки открывают награды: игрушку, питомца, табард и скакуна. Это косметика.',
                        'The points collected on your account unlock rewards: a toy, a pet, a tabard and a mount. They are cosmetic.',
                        'Накопичені на обліковому записі очки відкривають нагороди: іграшку, улюбленця, табард і скакуна. Це косметика.')},
                {'t': t('С чего начать', 'Where to start', 'З чого почати'),
                 'd': t('Альтов качать не нужно: один персонаж набирает до 29 очков, а потратить можно 16. Отметьте в разделе «Счётчик Legacy», что уже сделано. В игре окно Legacy открывается клавишей Y, когда появится первое очко, обычно на 25 уровне.',
                        'You don’t need alts: a single character can earn up to 29 points, and you can spend 16. Tick what you have already done in the “Legacy counter” section. In the game, the Legacy window opens with the Y key once you have your first point, usually at level 25.',
                        'Твінків качати не потрібно: один персонаж набирає до 29 очок, а витратити можна 16. Позначте в розділі «Лічильник Legacy», що вже зроблено. У грі вікно Legacy відкривається клавішею Y, коли з’явиться перше очко, зазвичай на 25 рівні.')},
            ]),
        ]},
        {'id': 'calc', 'title': t('Счётчик Legacy', 'Legacy counter', 'Лічильник Legacy'), 'blocks': [
            ('lgcalc', LGC),
        ]},
        {'id': 'start', 'title': t('Как открыть', 'How to unlock it', 'Як відкрити'), 'blocks': [
            ('steps', [
                {'t': t('Первое очко', 'First point', 'Перше очко'),
                 'd': t('Legacy открывается с первым очком: 25 уровень на персонаже, 150 в основной профессии (не сбор) или исследование всей карты.', 'Legacy unlocks with your first point: level 25 on a character, 150 in a main profession (not gathering) or exploring the entire map.', 'Legacy відкривається з першим очком: 25 рівень на персонажі, 150 в основній професії (не збирання) або дослідження всієї мапи.')},
                {'t': t('Окно', 'Window', 'Вікно'),
                 'd': t('Горячая клавиша Y или значок щита в меню.', 'Hotkey Y or the shield icon in the menu.', 'Гаряча клавіша Y або значок щита в меню.')},
                {'t': t('На весь аккаунт', 'Account-wide', 'На весь обліковий запис'),
                 'd': t('Очки общие для всех персонажей аккаунта не-Hardcore, тратит их каждый персонаж по-своему.', 'Points are shared by all non-Hardcore characters on the account; each character spends them its own way.', 'Очки спільні для всіх персонажів облікового запису, крім Hardcore, а витрачає їх кожен персонаж по-своєму.')},
                {'t': t('Лимит на старте', 'Limit at launch', 'Ліміт на старті'),
                 'd': t('На персонажа не больше 16 очков. Остальные копятся на аккаунте и открывают награды.', 'No more than 16 points per character. The rest pile up on the account and unlock rewards.', 'На персонажа не більше 16 очок. Решта накопичується на обліковому записі й відкриває нагороди.')},
            ]),
            ('tip', t('Альты не обязательны: один персонаж без твинков может набрать до 29 очков, а потратить нужно 16.', 'Alts aren’t required: a single character without alts can earn up to 29 points, and you only need to spend 16.', 'Твінки не обов’язкові: один персонаж без твінків може набрати до 29 очок, а витратити потрібно 16.')),
        ]},
        {'id': 'challenges', 'title': t('Испытания: где взять очки', 'Challenges: where to get points', 'Випробування: де брати очки'), 'blocks': [
            ('text', [t('Каждое испытание даёт 1 очко. Всего их 65 в шести категориях.', 'Each challenge gives 1 point. There are 65 of them in six categories.', 'Кожне випробування дає 1 очко. Усього їх 65 у шести категоріях.')]),
            ('table', {'head': [t('Категория', 'Category', 'Категорія'), t('Очки', 'Points', 'Очки'), t('За что', 'For what', 'За що')], 'rows': [
                [t('Классы', 'Classes', 'Класи'), '27', t('25, 45 и 60 уровень на каждом классе', 'Levels 25, 45 and 60 on each class', '25, 45 і 60 рівень на кожному класі')],
                [t('Профессии', 'Professions', 'Професії'), '18', t('150, 225 и 300 навыка в каждой основной профессии, кроме сбора', '150, 225 and 300 skill in each main profession except gathering', '150, 225 і 300 очок навички в кожній основній професії, крім збирання')],
                ['PvP', '12', t('звания 3, 7, 10, 13 и 14 (5 очков); «Превознесение» с репутацией каждого поля боя (4 очка); 4, 7 и 10 неделя сезонного пути Field of Honor (3 очка)', 'Ranks 3, 7, 10, 13 and 14 (5 points); Exalted reputation with each battleground (4 points); weeks 4, 7 and 10 of the seasonal Field of Honor path (3 points)', 'Звання 3, 7, 10, 13 і 14 (5 очок); репутація Exalted на кожному полі бою (4 очки); 4, 7 і 10 тиждень сезонного шляху Field of Honor (3 очки)')],
                [t('Подземелья', 'Dungeons', 'Підземелля'), '3', t('последний босс во всех подземельях 15–25, 26–45 и 46–60 уровня', 'The last boss in all dungeons of levels 15–25, 26–45 and 46–60', 'Останній бос у всіх підземеллях 15–25, 26–45 і 46–60 рівня')],
                [t('Рейды', 'Raids', 'Рейди'), '3', t('Onyxia; все 13 боссов Hyjal Summit; все 8 боссов Barrow Deeps', 'Onyxia; all 13 bosses of Hyjal Summit; all 8 bosses of Barrow Deeps', 'Onyxia; усі 13 босів Hyjal Summit; усі 8 босів Barrow Deeps')],
                [t('Приключения', 'Adventures', 'Пригоди'), '2', t('вся карта мира на одном персонаже; цепочка заданий на комплект подземелья Lord Valthalak', 'The whole world map on one character; the Lord Valthalak dungeon set questline', 'Уся мапа світу на одному персонажі; ланцюжок завдань на комплект підземелля Lord Valthalak')],
            ]}),
            ('tip', t('Если до 25 уровня далеко, доведите ремесло до 150: Legacy откроется раньше. Сбор (травы, руда, шкуры) очков не даёт, но кормит ремесло.', 'If level 25 is far off, get a craft to 150: Legacy will unlock sooner. Gathering (herbs, ore, hides) gives no points, but it feeds your craft.', 'Якщо до 25 рівня ще далеко, доведіть ремесло до 150: Legacy відкриється раніше. Збирання (трави, руда, шкури) очок не дає, але годує ремесло.')),
        ]},
        {'id': 'perks', 'title': t('Перки', 'Perks', 'Перки'), 'blocks': [
            ('text', [t('Три дерева: Профессии, Приключения, Находчивость (Resourcefulness). Описания перков — по Blizzard. Числа рангов — по Warcraft Tavern, Blizzard их не публиковала.', 'Three trees: Professions, Adventure, Resourcefulness. Perk descriptions are from Blizzard. Rank counts are from Warcraft Tavern; Blizzard has not published them.', 'Три дерева: Професії, Пригоди, Винахідливість (Resourcefulness). Описи перків — за Blizzard. Числа рангів — за Warcraft Tavern, Blizzard їх не публікувала.')]),
            ('table', {'head': [t('Дерево', 'Tree', 'Дерево'), t('Перки (рангов)', 'Perks (ranks)', 'Перки (рангів)')], 'rows': [
                [t('Профессии', 'Professions', 'Професії'), t('Working Overtime (5): чаще растут навыки всех ремёсел, включая классовые вроде Взлома замков. Bountiful Harvest (5): чаще находите дополнительные редкие ресурсы при добыче руды, сборе трав и снятии шкур. Master Chef (5): шанс лишнего блюда. Luremaster (2): шанс выловить лишнюю рыбу. Performance Bonus (3): иногда даёт больше Merchant’s Favor от Azeroth Commerce Authority или Durotar Supply and Logistics. Bartering (2): снижает цены у торговцев. Dedicated Study (1): раз в день ускоряет рост ремёсел; если все ремёсла на 300, даёт Elemental Essences.', 'Working Overtime (5): skills in all tradeskills improve more often, including class skills such as Lockpicking. Bountiful Harvest (5): you find additional scarce resources more often when mining, herbing or skinning. Master Chef (5): a chance for an extra dish. Luremaster (2): a chance to fish up extra fish. Performance Bonus (3): sometimes gives more Merchant’s Favor from the Azeroth Commerce Authority or Durotar Supply and Logistics. Bartering (2): reduces vendor prices. Dedicated Study (1): once a day, speeds up tradeskill gains; if all are at 300, gives free Elemental Essences.', 'Working Overtime (5): навички всіх ремесел зростають частіше, зокрема класові, як-от злом замків. Bountiful Harvest (5): частіше знаходите додаткові рідкісні ресурси під час видобутку руди, збирання трав і зняття шкур. Master Chef (5): шанс на зайву страву. Luremaster (2): шанс виловити зайву рибу. Performance Bonus (3): іноді дає більше Merchant’s Favor від Azeroth Commerce Authority або Durotar Supply and Logistics. Bartering (2): знижує ціни в торговців. Dedicated Study (1): раз на день пришвидшує зростання ремесел; якщо всі ремесла на 300, дає Elemental Essences.')],
                [t('Приключения', 'Adventure', 'Пригоди'), t('Well Rested (5): быстрее копится отдых и выше его потолок. Thrill of Adventure (5): немного здоровья и маны после каждого нетривиального убийства. Talented (5): очки талантов открываются раньше нормы, до 5 уровней. Field Guide (3): короче часовой откат установки объектов лагеря. High Alert (2): лучше видно врагов в незаметности, кроме полей боя. Field Medicine (2): короче дебафф «Недавно перевязан», кроме подземелий, рейдов и полей боя. Frequent Flier (1): перелёты дешевле и быстрее.', 'Well Rested (5): rest builds up faster and its cap is higher. Thrill of Adventure (5): a little health and mana after every non-trivial kill. Talented (5): talent points unlock earlier than normal, up to 5 levels. Field Guide (3): shorter 1-hour cooldown on placing camp objects. High Alert (2): enemies in stealth are easier to see, except in battlegrounds. Field Medicine (2): shorter Recently Bandaged debuff, except in dungeons, raids and battlegrounds. Frequent Flier (1): flights cost less and are faster.', 'Well Rested (5): швидше накопичується відпочинок і вища його стеля. Thrill of Adventure (5): трохи здоров’я та мани після кожного нетривіального вбивства. Talented (5): очки талантів відкриваються раніше за норму, до 5 рівнів. Field Guide (3): коротший годинний відкат встановлення об’єктів табору. High Alert (2): краще видно ворогів у невидимості, крім полів бою. Field Medicine (2): коротший дебаф «Нещодавно перев’язаний», крім підземель, рейдів і полів бою. Frequent Flier (1): перельоти дешевші й швидші.')],
                [t('Находчивость (Resourcefulness)', 'Resourcefulness', 'Винахідливість (Resourcefulness)'), t('Gourmand (3): баффы от еды действуют дольше. Permanence (2): баффы группы, рейда и лагеря действуют дольше. Reagent Economy (1): способностям класса не нужны покупные реагенты, объекты лагеря 1 уровня не требуют материалов. Reinforce (5): меньше потеря прочности при смерти. Diplomat (5): больше репутации. For Great Honor (5): больше Чести в PvP. The Quick and the Dead (2): мёртвые быстрее бегут к телу, а после воскрешения баффы группы и рейда бесплатны.', 'Gourmand (3): buffs from food last longer. Permanence (2): party, raid and camp buffs last longer. Reagent Economy (1): class abilities need no bought reagents, tier 1 camp objects need no materials. Reinforce (5): less durability loss on death. Diplomat (5): more reputation. For Great Honor (5): more Honor from PvP. The Quick and the Dead (2): dead players run faster to their body, and after resurrecting, party and raid buffs are free.', 'Gourmand (3): бафи від їжі діють довше. Permanence (2): бафи групи, рейду та табору діють довше. Reagent Economy (1): здібностям класу не потрібні куплені реагенти, об’єкти табору 1 рівня не потребують матеріалів. Reinforce (5): менша втрата міцності при смерті. Diplomat (5): більше репутації. For Great Honor (5): більше Честі в PvP. The Quick and the Dead (2): мертві швидше біжать до тіла, а після воскресіння бафи групи та рейду безкоштовні.')],
            ]}),
            ('tip', t('Первыми берите перки опыта и лагеря: Well Rested, Field Guide, Permanence. Reagent Economy ценен классам с реагентами, Talented — твинкам.', 'Take the experience and camp perks first: Well Rested, Field Guide, Permanence. Reagent Economy is worth it for classes with reagents, Talented for alts.', 'Першими беріть перки досвіду й табору: Well Rested, Field Guide, Permanence. Reagent Economy цінний класам із реагентами, Talented — твінкам.')),
            ('text', [t('Warcraft Tavern пишет про лимит 25 очков на дерево, Blizzard лимита на дерево не называет.', 'Warcraft Tavern mentions a limit of 25 points per tree; Blizzard names no per-tree limit.', 'Warcraft Tavern пише про ліміт 25 очок на дерево, Blizzard ліміту на дерево не називає.')]),
        ]},
        {'id': 'rewards', 'title': t('Награды', 'Rewards', 'Нагороди'), 'blocks': [
            ('text', [t('Награды открывает общее число очков на аккаунте, как бы вы их ни потратили. На старте наград четыре. Пороги очков Blizzard не опубликовала: ниже данные демо BlizzCon по сторонним сайтам, возможны изменения. По Warcraft Tavern, забирать у Innkeeper Wiley в Ratchet.', 'Rewards unlock by the total number of points on the account, however you spent them. There are four rewards at launch. Blizzard has not published point thresholds: the table shows BlizzCon demo data from third-party sites and may change. Per Warcraft Tavern, collect them from Innkeeper Wiley in Ratchet.', 'Нагороди відкриває загальна кількість очок на обліковому записі, як би ви їх не витратили. На старті нагород чотири. Пороги очок Blizzard не опублікувала: нижче дані демо BlizzCon зі сторонніх сайтів, можливі зміни. За Warcraft Tavern, забирати в Innkeeper Wiley у Ratchet.')]),
            ('table', {'head': [t('Очки (демо BlizzCon)', 'Points (BlizzCon demo)', 'Очки (демо BlizzCon)'), t('Награда', 'Reward', 'Нагорода')], 'rows': [
                ['15', t('игрушка Replica Ironforge Air Rifle: оглушает других игроков и ведёт счёт', 'Toy: Replica Ironforge Air Rifle, which stuns other players and keeps score', 'іграшка Replica Ironforge Air Rifle: приголомшує інших гравців і веде лік')],
                ['25', t('питомец Spectral Bear Cub', 'Pet: Spectral Bear Cub', 'улюбленець Spectral Bear Cub')],
                ['40', t('табард Spectral Bear Tabard', 'Tabard: Spectral Bear Tabard', 'табард Spectral Bear Tabard')],
                ['55', t('скакун Reins of the Spectral Bear', 'Mount: Reins of the Spectral Bear', 'скакун Reins of the Spectral Bear')],
            ]}),
            ('text', [t('Это косметика, преимуществ в игре она не даёт. Blizzard планирует новые испытания, перки и награды с каждым обновлением.', 'These are cosmetic and give no in-game advantage. Blizzard plans new challenges, perks and rewards with each update.', 'Це косметика, переваг у грі вона не дає. Blizzard планує нові випробування, перки та нагороди з кожним оновленням.')]),
        ]},
        {'id': 'hardcore', 'title': 'Hardcore', 'blocks': [
            ('text', [t('Hardcore на старте не будет. Когда он выйдет, испытания с обычных серверов в нём не засчитаются, а испытания из Hardcore засчитаются везде. PvP-испытания в Hardcore выполнить нельзя, зато к его старту добавят 12 новых испытаний, особых для Hardcore.', 'Hardcore won’t be available at launch. When it arrives, challenges from regular realms won’t count in it, while Hardcore challenges will count everywhere. PvP challenges can’t be completed in Hardcore, but 12 new challenges made for Hardcore will be added by its launch.', 'Hardcore на старті не буде. Коли він вийде, випробування зі звичайних серверів у ньому не зараховуватимуться, а випробування з Hardcore зараховуватимуться всюди. PvP-випробування в Hardcore виконати не можна, зате до його старту додадуть 12 нових випробувань, особливих для Hardcore.')]),
        ]},
        {'id': 'faq', 'title': t('Частые вопросы', 'Common questions', 'Часті питання'), 'blocks': [
            ('faq', [
                {'id': 'q1', 'q': t('Как открыть Legacy в WoW Forever?', 'How do I unlock Legacy in WoW Forever?', 'Як відкрити Legacy у WoW Forever?'),
                 'a': [t('Получите первое очко: 25 уровень, 150 в основной профессии (не сбор) или исследование всей карты. Окно открывается клавишей Y.', 'Earn your first point: level 25, 150 in a main profession (not gathering) or exploring the whole map. The window opens with the Y key.', 'Отримайте перше очко: 25 рівень, 150 в основній професії (не збирання) або дослідження всієї мапи. Вікно відкривається клавішею Y.')]},
                {'id': 'q2', 'q': t('Сколько очков Legacy можно потратить?', 'How many Legacy points can I spend?', 'Скільки очок Legacy можна витратити?'),
                 'a': [t('На старте до 16 на персонажа. Лишние копятся на аккаунте и открывают награды.', 'Up to 16 per character at launch. The extra points pile up on the account and unlock rewards.', 'На старті до 16 на персонажа. Зайві накопичуються на обліковому записі й відкривають нагороди.')]},
                {'id': 'q3', 'q': t('Нужно ли качать альтов ради Legacy?', 'Do I need to level alts for Legacy?', 'Чи потрібно качати твінків заради Legacy?'),
                 'a': [t('Нет. Один персонаж может набрать до 29 очков, а потратить нужно 16.', 'No. One character can earn up to 29 points, and you only need to spend 16.', 'Ні. Один персонаж може набрати до 29 очок, а витратити потрібно 16.')]},
                {'id': 'q4', 'q': t('Общие ли очки Legacy для всех персонажей?', 'Are Legacy points shared across all characters?', 'Чи спільні очки Legacy для всіх персонажів?'),
                 'a': [t('Да, на весь аккаунт Battle.net, кроме Hardcore. Перки каждый персонаж выбирает сам.', 'Yes, across the whole Battle.net account, except Hardcore. Each character picks its own perks.', 'Так, на весь обліковий запис Battle.net, крім Hardcore. Перки кожен персонаж обирає сам.')]},
                {'id': 'q5', 'q': t('Какие перки Legacy брать первыми?', 'Which Legacy perks should I take first?', 'Які перки Legacy брати першими?'),
                 'a': [t('Перки опыта и лагеря: Well Rested, Field Guide, Permanence. Классам с реагентами — Reagent Economy.', 'Experience and camp perks: Well Rested, Field Guide, Permanence. Reagent Economy for classes with reagents.', 'Перки досвіду й табору: Well Rested, Field Guide, Permanence. Класам із реагентами — Reagent Economy.')]},
            ]),
        ]},
    ],
})


# ---------- addons (текст 25.10.2026, переводы в i18n/*.json) ----------

def _tile(slug, href=None, d=None, art=None, title=None):
    g = next(x for x in GUIDES if x['slug'] == slug)
    return {'t': title or g['title'], 'd': d or g['tile'], 'href': href or f'guides/{slug}/', 'art': art or g.get('hero') or g['art']}


GUIDES.append({
    'slug': 'addons', 'art': 'hero_roster', 'hero': 'hero_roster',
    'title': t('Аддоны и интерфейс', 'Addons and Interface', 'Аддони та інтерфейс'),
    'lead': t('Аддоны в Forever есть, но работают по правилам современного WoW, а не Classic. Старые аддоны Classic не грузятся, нужен файл под Forever. Ниже — что уже встроено в игру, что ставить для прокачки и группы и как это установить.', 'Addons exist in Forever, but they follow the rules of modern WoW, not Classic. Old Classic addons won’t load: you need a file made for Forever. Below: what is already built into the game, what to install for leveling and groups, and how to install it.', 'Аддони у Forever є, але працюють за правилами сучасного WoW, а не Classic. Старі аддони Classic не завантажуються, потрібен файл під Forever. Нижче — що вже вбудовано в гру, що ставити для прокачування та групи і як це встановити.'),
    'tile': t('Что работает, что встроено, как ставить', 'What works, what is built in, how to install', 'Що працює, що вбудовано, як ставити'),
    'pills': [t('Нужна версия Forever', 'Forever version required', 'Потрібна версія Forever'), t('Боевой журнал закрыт', 'Combat log closed', 'Бойовий журнал закритий'), t('CurseForge и Wago', 'CurseForge and Wago', 'CurseForge і Wago')],
    'sources': [
        (t('Icy Veins: Blizzard об аддонах в Forever', 'Icy Veins: Blizzard on addons in Forever', 'Icy Veins: Blizzard про аддони у Forever'), 'https://www.icy-veins.com/wow-forever/news/addons-in-wow-forever-blizzard-devs-just-addressed-the-big-question/'),
        (t('Icy Veins: 9 аддонов для Forever', 'Icy Veins: 9 addons for Forever', 'Icy Veins: 9 аддонів для Forever'), 'https://www.icy-veins.com/wow-forever/news/set-up-your-wow-forever-ui-before-launch-with-these-9-addons/'),
        (t('Gfinity: интерфейс и аддоны Forever', 'Gfinity: Forever interface and addons', 'Gfinity: інтерфейс і аддони Forever'), 'https://www.gfinityesports.com/article/world-of-warcraft-forever-ui-addons-setup-guide'),
        (t('Kami Labs: аддоны WoW Forever', 'Kami Labs: WoW Forever addons', 'Kami Labs: аддони WoW Forever'), 'https://kami-labs.fr/en/addons-wow-forever/'),
        (t('LFCarry: аддоны WoW Forever', 'LFCarry: WoW Forever addons', 'LFCarry: аддони WoW Forever'), 'https://lfcarry.com/guides/wow-forever-addons'),
        (t('CurseForge: страницы аддонов, версия WoW Forever', 'CurseForge: addon pages, WoW Forever version', 'CurseForge: сторінки аддонів, версія WoW Forever'), 'https://www.curseforge.com/wow/addons'),
    ],
    'sections': [
        {'id': 'first', 'title': t('Поставьте первым делом', 'Install these first', 'Поставте насамперед'), 'blocks': [
            ('text', [t('С них удобно начать. У каждого на CurseForge есть файл «WoW Forever», ссылки проверены 04.11.2026.', 'A good set to start with. Each one has a “WoW Forever” file on CurseForge; links checked on November 4, 2026.', 'З них зручно почати. У кожного на CurseForge є файл «WoW Forever», посилання перевірено 4 листопада 2026 року.')]),
            ('addons', {'head': [t('Аддон', 'Addon', 'Аддон'), t('Что делает', 'What it does', 'Що робить'), ''], 'items': [
                {'n': 'Questie', 'url': 'https://www.curseforge.com/wow/addons/questie',
                 'd': t('Показывает на карте и миникарте, где цели заданий и кому их сдавать.', 'Shows quest objectives and turn-ins on the map and minimap.', 'Показує на мапі та мінімапі, де цілі завдань і кому їх здавати.')},
                {'n': 'Details!', 'url': 'https://www.curseforge.com/wow/addons/details',
                 'd': t('Урон, лечение и угроза всей группы.', 'Damage, healing and threat for the whole group.', 'Шкода, лікування та загроза всієї групи.')},
                {'n': 'DBM', 'url': 'https://www.curseforge.com/wow/addons/deadly-boss-mods',
                 'd': t('Предупреждения и таймеры на боссах.', 'Boss warnings and timers.', 'Попередження та таймери на босах.')},
                {'n': 'Auctionator', 'url': 'https://www.curseforge.com/wow/addons/auctionator',
                 'd': t('Быстрый поиск по аукциону, цены и выставление лотов.', 'Fast auction search, prices and posting items.', 'Швидкий пошук на аукціоні, ціни та виставлення лотів.')},
                {'n': 'Leatrix Plus', 'url': 'https://www.curseforge.com/wow/addons/leatrix-plus',
                 'd': t('Ремонт, продажа серого и приём приглашений без лишних кликов.', 'Repairs, selling grey items and accepting invites without extra clicks.', 'Ремонт, продаж сірого й прийом запрошень без зайвих кліків.')},
                {'n': 'RareScanner', 'url': 'https://www.curseforge.com/wow/addons/rarescanner',
                 'd': t('Сообщает, когда рядом редкий моб, сундук или событие, и отмечает их на карте мира.', 'Alerts you when a rare mob, treasure or event is nearby and marks them on the world map.', 'Повідомляє, коли поруч рідкісний моб, скриня чи подія, і позначає їх на мапі світу.')},
                {'n': 'Dialogue UI', 'url': 'https://www.curseforge.com/wow/addons/dialogueui',
                 'd': t('Задания в виде диалога: крупный текст, выбор ответа клавишей, камера на собеседнике.', 'Quests as a dialogue: large text, answers picked with a key, the camera on the speaker.', 'Завдання у вигляді діалогу: великий текст, вибір відповіді клавішею, камера на співрозмовнику.')},
                {'n': 'CatQuest', 'url': 'https://www.curseforge.com/wow/addons/catquest', 'langs': ('ru',),
                 'd': 'Русская озвучка заданий 1–60, книг и истории мест. Нужен русский клиент; после установки перезапустите игру целиком.'},
            ]}),
        ]},
        {'id': 'rules', 'title': t('Как работают аддоны в Forever', 'How addons work in Forever', 'Як працюють аддони у Forever'), 'blocks': [
            ('text', [t('Интерфейс Forever построен на клиенте современного WoW: по словам Blizzard, это архитектура Mainline и почти весь API версии 12.1.5, с теми же ограничениями, что в Midnight.', 'The Forever interface is built on the modern WoW client: according to Blizzard, it is the Mainline architecture and nearly the entire API of version 12.1.5, with the same restrictions as in Midnight.', 'Інтерфейс Forever побудований на клієнті сучасного WoW: за словами Blizzard, це архітектура Mainline і майже весь API версії 12.1.5, з тими самими обмеженнями, що й у Midnight.')]),
            ('table', {'head': ['', t('Можно', 'Allowed', 'Можна'), t('Нельзя', 'Not allowed', 'Не можна')], 'rows': [
                [t('Вид интерфейса', 'Look of the interface', 'Вигляд інтерфейсу'), t('Двигать и перерисовывать рамки, панели, сумки, карту', 'Move and redraw frames, panels, bags, the map', 'Рухати й перемальовувати рамки, панелі, сумки, мапу'), t('—', '—', '—')],
                [t('Информация', 'Information', 'Інформація'), t('Показывать то, что игра и так отдаёт: задания, координаты, цены, встроенный счётчик урона', 'Show what the game already provides: quests, coordinates, prices, the built-in damage meter', 'Показувати те, що гра й так віддає: завдання, координати, ціни, вбудований лічильник шкоди'), t('Читать боевой журнал', 'Read the combat log', 'Читати бойовий журнал')],
                [t('Бой', 'Combat', 'Бій'), t('Таймеры боссов, свои кулдауны и баффы', 'Boss timers, your own cooldowns and buffs', 'Таймери босів, власні кулдауни та баффи'), t('Видеть скрытые в бою значения: часть здоровья, угрозы и аур врагов', 'See values hidden in combat: part of enemy health, threat and auras', 'Бачити приховані в бою значення: частину здоров’я, загрози та аур ворогів')],
            ]}),
            ('tip', t('Ищите на CurseForge версию «WoW Forever». Файл для Classic даже со знакомым названием в Forever не загрузится.', 'Look on CurseForge for the “WoW Forever” version. A Classic file won’t load in Forever even if the name looks familiar.', 'Шукайте на CurseForge версію «WoW Forever». Файл для Classic навіть зі знайомою назвою у Forever не завантажиться.')),
        ]},
        {'id': 'builtin', 'title': t('Что уже есть в игре', 'What is already in the game', 'Що вже є в грі'), 'blocks': [
            ('text', [t('Часть того, ради чего раньше ставили аддоны, в Forever встроена. Начните с настроек, аддоны добавляйте под то, чего не хватает.', 'Some of the things people used to install addons for are built into Forever. Start with the settings and add addons for whatever is still missing.', 'Частину того, заради чого раніше ставили аддони, у Forever вбудовано. Почніть з налаштувань, аддони додавайте під те, чого бракує.')]),
            ('table', {'head': [t('Что', 'What', 'Що'), t('Где включить', 'Where to enable', 'Де ввімкнути'), t('Аддон нужен?', 'Addon needed?', 'Чи потрібен аддон?')], 'rows': [
                [t('Счётчик урона и лечения', 'Damage and healing meter', 'Лічильник шкоди та лікування'), t('Настройки, затем место на экране в Edit Mode', 'Settings, then place it on screen in Edit Mode', 'Налаштування, потім місце на екрані в Edit Mode'), t('Нет. Угроза и подробности — Details!', 'No. Threat and details: Details!', 'Ні. Загроза й подробиці — Details!')],
                [t('Cooldown Manager: свои кулдауны и баффы', 'Cooldown Manager: your own cooldowns and buffs', 'Cooldown Manager: власні кулдауни та баффи'), t('Options → Gameplay Enhancement, по умолчанию выключен', 'Options → Gameplay Enhancement, off by default', 'Options → Gameplay Enhancement, за замовчуванням вимкнено'), t('Нет. Свои индикаторы с условиями — ForeverAuras', 'No. Custom indicators with conditions: ForeverAuras', 'Ні. Власні індикатори з умовами — ForeverAuras')],
                [t('Перестановка панелей и рамок', 'Rearranging panels and frames', 'Перестановка панелей і рамок'), t('Esc → Edit Mode', 'Esc → Edit Mode', 'Esc → Edit Mode'), t('Нет. Старый рисунок Classic — только аддоны', 'No. The old Classic look comes only from addons', 'Ні. Старий вигляд Classic дають лише аддони')],
                [t('Цели заданий на карте', 'Quest objectives on the map', 'Цілі завдань на мапі'), t('Фильтр карты мира', 'World map filter', 'Фільтр мапи світу'), t('Для отметок на миникарте и сдачи заданий — Questie', 'For minimap markers and turning in quests: Questie', 'Для позначок на мінімапі та здавання завдань — Questie')],
                [t('Одна общая сумка', 'One shared bag', 'Одна спільна сумка'), t('Настройки управления', 'Controls settings', 'Налаштування керування'), t('Для категорий и сортировки — Baganator', 'For categories and sorting: Baganator', 'Для категорій і сортування — Baganator')],
                [t('Каст по клику на рамку', 'Click casting on a frame', 'Каст по кліку на рамку'), t('Назначение клавиш → Click Casting', 'Key Bindings → Click Casting', 'Призначення клавіш → Click Casting'), t('Нет', 'No', 'Ні')],
                [t('Таймер автоатаки, текст боя', 'Auto-attack timer, combat text', 'Таймер автоатаки, текст бою'), t('Настройки', 'Settings', 'Налаштування'), t('Нет', 'No', 'Ні')],
            ]}),
            ('tiles', [_tile('faq', 'guides/faq/#graphics', title=t('Частые вопросы: Classic или Enhanced', 'FAQ: Classic or Enhanced', 'FAQ: Classic чи Enhanced'))]),
        ]},
        {'id': 'list', 'title': t('Аддоны для прокачки и группы', 'Addons for leveling and groups', 'Аддони для прокачування та групи'), 'blocks': [
            ('text', [t('У всех аддонов ниже на CurseForge есть файл «WoW Forever» (проверено 04.11.2026). Ставьте три-четыре и добавляйте по мере надобности: каждый лишний аддон — ещё один источник ошибок после патча.', 'Every addon below has a “WoW Forever” file on CurseForge (checked on November 4, 2026). Install three or four and add more as you need them: every extra addon is one more source of errors after a patch.', 'У всіх аддонів нижче на CurseForge є файл «WoW Forever» (перевірено 4 листопада 2026 року). Ставте три-чотири й додавайте за потреби: кожен зайвий аддон — ще одне джерело помилок після патча.')]),
            ('tabs', [
                {'id': 'quests', 't': t('Задания и карта', 'Quests and map', 'Завдання та мапа'), 'blocks': [
                    ('table', {'head': [t('Аддон', 'Addon', 'Аддон'), t('Зачем', 'What for', 'Навіщо')], 'rows': [
                        [('Questie', 'https://www.curseforge.com/wow/addons/questie'), t('Задания, места целей и сдачи на карте и миникарте. Обновлён под новые зоны Forever.', 'Quests, objective and turn-in locations on the map and minimap. Updated for the new Forever zones.', 'Завдання, місця цілей і здавання на мапі та мінімапі. Оновлено під нові зони Forever.')],
                        [('RestedXP Guide', 'https://www.curseforge.com/wow/addons/restedxp-guide'), t('Маршрут прокачки по шагам, стрелка к цели, авто-приём и сдача заданий. Полный маршрут платный.', 'Step-by-step leveling route, arrow to the objective, auto-accept and turn-in of quests. The full route is paid.', 'Маршрут прокачування крок за кроком, стрілка до цілі, авто-прийом і здавання завдань. Повний маршрут платний.')],
                        [('Leatrix Maps', 'https://www.curseforge.com/wow/addons/leatrix-maps'), t('Координаты, значки подземелий и рейдов на карте мира.', 'Coordinates, dungeon and raid icons on the world map.', 'Координати, значки підземель і рейдів на мапі світу.')],
                        [('TomTom', 'https://www.curseforge.com/wow/addons/tomtom'), t('Стрелка к точке по координатам из гайдов (/way).', 'An arrow to a point from the coordinates in guides (/way).', 'Стрілка до точки за координатами з гайдів (/way).')],
                        [('RareScanner', 'https://www.curseforge.com/wow/addons/rarescanner'), t('Сигнал о редком мобе, сундуке или событии рядом, их места на карте мира.', 'An alert for a nearby rare mob, treasure or event, and their spots on the world map.', 'Сигнал про рідкісного моба, скриню чи подію поруч, їхні місця на мапі світу.')],
                        [('OpenMap', 'https://www.curseforge.com/wow/addons/openmap'), t('Сплошная карта мира в стиле Classic. Пока бета-версия.', 'A Classic-style continuous world map. Still a beta version.', 'Суцільна мапа світу в стилі Classic. Поки що бета-версія.')],
                    ]}),
                ]},
                {'id': 'bags', 't': t('Сумки и аукцион', 'Bags and auction', 'Сумки та аукціон'), 'blocks': [
                    ('table', {'head': [t('Аддон', 'Addon', 'Аддон'), t('Зачем', 'What for', 'Навіщо')], 'rows': [
                        [('Baganator', 'https://www.curseforge.com/wow/addons/baganator'), t('Сумки одним окном или по категориям, сортировка.', 'Bags in one window or by category, sorting.', 'Сумки одним вікном або за категоріями, сортування.')],
                        [('Bagnon', 'https://www.curseforge.com/wow/addons/bagnon'), t('Все сумки в одном окне. Выбирайте один из двух.', 'All bags in one window. Pick one of the two.', 'Усі сумки в одному вікні. Обирайте один із двох.')],
                        [('Auctionator', 'https://www.curseforge.com/wow/addons/auctionator'), t('Быстрый поиск по аукциону, цены и выставление лотов.', 'Fast auction search, prices and posting items.', 'Швидкий пошук на аукціоні, ціни та виставлення лотів.')],
                        [('Leatrix Plus', 'https://www.curseforge.com/wow/addons/leatrix-plus'), t('Мелкая автоматизация: ремонт, продажа серого, приём приглашений. Часть опций в Forever недоступна.', 'Small automations: repair, selling grey items, accepting invites. Some options are unavailable in Forever.', 'Дрібна автоматизація: ремонт, продаж сірого, прийом запрошень. Частина опцій у Forever недоступна.')],
                    ]}),
                ]},
                {'id': 'group', 't': t('Группа и бой', 'Group and combat', 'Група та бій'), 'blocks': [
                    ('table', {'head': [t('Аддон', 'Addon', 'Аддон'), t('Зачем', 'What for', 'Навіщо')], 'rows': [
                        [('Details! Damage Meter', 'https://www.curseforge.com/wow/addons/details'), t('Урон, лечение и угроза. В Classic-механике угроза важна танку и всей группе.', 'Damage, healing and threat. With Classic mechanics, threat matters to the tank and the whole group.', 'Шкода, лікування та загроза. У Classic-механіці загроза важлива танку й усій групі.')],
                        [('ThreatClassic2', 'https://www.curseforge.com/wow/addons/threatclassic2'), t('Отдельное окно угрозы. Режима «цель цели» для лекаря нет.', 'A separate threat window. There is no “target of target” mode for healers.', 'Окреме вікно загрози. Режиму «ціль цілі» для лікаря немає.')],
                        [('Forever Meter', 'https://www.curseforge.com/wow/addons/forever-meter'), t('Счётчик урона и угрозы, сделанный под Forever: берёт данные встроенного счётчика.', 'A damage and threat meter made for Forever: it takes its data from the built-in meter.', 'Лічильник шкоди й загрози, зроблений під Forever: бере дані вбудованого лічильника.')],
                        [('DBM - Deadly Boss Mods', 'https://www.curseforge.com/wow/addons/deadly-boss-mods'), t('Предупреждения и таймеры боссов.', 'Boss warnings and timers.', 'Попередження та таймери босів.')],
                        [('BigWigs', 'https://www.curseforge.com/wow/addons/bigwigs'), t('То же, что DBM. Ставьте один из двух.', 'The same as DBM. Install one of the two.', 'Те саме, що DBM. Ставте один із двох.')],
                        [('Platynator', 'https://www.curseforge.com/wow/addons/platynator'), t('Индикаторы над врагами; отмечает мобов, нужных для заданий.', 'Indicators over enemies; marks the mobs you need for quests.', 'Індикатори над ворогами; позначає мобів, потрібних для завдань.')],
                    ]}),
                ]},
                {'id': 'ui', 't': t('Интерфейс', 'Interface', 'Інтерфейс'), 'blocks': [
                    ('table', {'head': [t('Аддон', 'Addon', 'Аддон'), t('Зачем', 'What for', 'Навіщо')], 'rows': [
                        [('EllesmereUI', 'https://www.curseforge.com/wow/addons/ellesmereui'), t('Перерисовывает весь интерфейс, настройка правым кликом по элементу. Свой Cooldown Manager и карта.', 'Redraws the whole interface, set up by right-clicking an element. Its own Cooldown Manager and map.', 'Перемальовує весь інтерфейс, налаштування правим кліком по елементу. Власні Cooldown Manager і мапа.')],
                        [('ForeverAuras', 'https://www.curseforge.com/wow/addons/foreverauras'), t('Форк WeakAuras под Forever: свои значки баффов, дебаффов и кулдаунов с условиями. Настройки — /fa.', 'A WeakAuras fork for Forever: your own icons for buffs, debuffs and cooldowns, with conditions. Options: /fa.', 'Форк WeakAuras під Forever: власні значки баффів, дебаффів і кулдаунів з умовами. Налаштування — /fa.')],
                        [('Dialogue UI', 'https://www.curseforge.com/wow/addons/dialogueui'), t('Окно заданий в виде диалога, выбор ответа клавишей или геймпадом.', 'The quest window as a dialogue, answers picked with a key or a gamepad.', 'Вікно завдань у вигляді діалогу, вибір відповіді клавішею або геймпадом.')],
                        [('BugSack', 'https://www.curseforge.com/wow/addons/bugsack'), t('Ловит ошибки Lua и показывает, какой аддон сломался. Нужен вместе с BugGrabber.', 'Catches Lua errors and shows which addon broke. Needs BugGrabber alongside.', 'Ловить помилки Lua й показує, який аддон зламався. Потрібен разом із BugGrabber.')],
                    ]}),
                ]},
            ]),
            ('tiles', [_tile('leveling'), _tile('dungeons'), _tile('professions')]),
            ('tip', t('Модули DBM и BigWigs под рейды Forever проверьте ближе к открытию рейдов 09.12: на бете их наборы различались.', 'Check the DBM and BigWigs modules for Forever raids closer to the raids opening on December 9: their sets differed in the beta.', 'Модулі DBM і BigWigs під рейди Forever перевірте ближче до відкриття рейдів 9 грудня: на бета-тесті їхні набори різнилися.')),
        ]},
        {'id': 'broken', 'title': t('Что не работает', 'What doesn’t work', 'Що не працює'), 'blocks': [
            ('text', [t('Не ставьте аддоны, которые читают боевой журнал или живут только в Classic. На 04.11.2026 без версии Forever или бесполезны:', 'Don’t install addons that read the combat log or live only in Classic. As of November 4, 2026, these either have no Forever version or are useless:', 'Не ставте аддони, які читають бойовий журнал або живуть лише в Classic. На 4 листопада 2026 року без версії Forever або марні:')]),
            ('table', {'head': [t('Аддон', 'Addon', 'Аддон'), t('Почему', 'Why', 'Чому'), t('Чем заменить', 'What to use instead', 'Чим замінити')], 'rows': [
                [t('WeakAuras', 'WeakAuras', 'WeakAuras'), t('Нет версии Forever', 'No Forever version', 'Немає версії Forever'), t('ForeverAuras, Cooldown Manager', 'ForeverAuras, Cooldown Manager', 'ForeverAuras, Cooldown Manager')],
                [t('OmniCC, OmniCD, OmniBar, Hekili', 'OmniCC, OmniCD, OmniBar, Hekili', 'OmniCC, OmniCD, OmniBar, Hekili'), t('Боевой журнал и скрытые значения', 'Combat log and hidden values', 'Бойовий журнал і приховані значення'), t('Cooldown Manager', 'Cooldown Manager', 'Cooldown Manager')],
                [t('Skada, Recount', 'Skada, Recount', 'Skada, Recount'), t('Боевой журнал', 'Combat log', 'Бойовий журнал'), t('Встроенный счётчик, Details!', 'The built-in meter, Details!', 'Вбудований лічильник, Details!')],
                [t('AdiBags', 'AdiBags', 'AdiBags'), t('Нет версии Forever', 'No Forever version', 'Немає версії Forever'), t('Baganator, Bagnon', 'Baganator, Bagnon', 'Baganator, Bagnon')],
                [t('Auctioneer', 'Auctioneer', 'Auctioneer'), t('Только Classic', 'Classic only', 'Лише Classic'), t('Auctionator', 'Auctionator', 'Auctionator')],
                [t('Quartz, Postal, Nova World Buffs', 'Quartz, Postal, Nova World Buffs', 'Quartz, Postal, Nova World Buffs'), t('Нет версии Forever', 'No Forever version', 'Немає версії Forever'), t('—', '—', '—')],
            ]}),
            ('tip', t('Список меняется с каждым обновлением. Перед установкой смотрите на CurseForge, есть ли у аддона файл «WoW Forever».', 'The list changes with every update. Before installing, check on CurseForge whether the addon has a “WoW Forever” file.', 'Список змінюється з кожним оновленням. Перед встановленням дивіться на CurseForge, чи є в аддона файл «WoW Forever».')),
        ]},
        {'id': 'install', 'title': t('Как установить', 'How to install', 'Як встановити'), 'blocks': [
            ('steps', [
                {'t': t('Менеджер', 'Manager', 'Менеджер'),
                 'd': t('Поставьте приложение CurseForge или Wago App, выберите World of Warcraft и версию Forever. Нужную папку менеджер найдёт сам и будет обновлять аддоны. Пользуйтесь одним менеджером.', 'Install the CurseForge app or Wago App, choose World of Warcraft and the Forever version. The manager finds the right folder by itself and keeps your addons updated. Use only one manager.', 'Встановіть застосунок CurseForge або Wago App, оберіть World of Warcraft і версію Forever. Потрібну теку менеджер знайде сам і оновлюватиме аддони. Користуйтеся одним менеджером.')},
                {'t': t('Или вручную', 'Or manually', 'Або вручну'),
                 'd': t('На странице аддона скачайте архив (Download file manually) и распакуйте так, чтобы папка аддона лежала в Interface\\AddOns в папке Forever, не Classic и не Retail. Папку игры открывает Battle.net: шестерёнка у кнопки «Играть» → Show in Explorer.', 'On the addon page download the archive (Download file manually) and unpack it so the addon folder sits in Interface\\AddOns inside the Forever folder, not Classic and not Retail. Battle.net opens the game folder: the gear next to the Play button → Show in Explorer.', 'На сторінці аддона завантажте архів (Download file manually) і розпакуйте так, щоб тека аддона лежала в Interface\\AddOns у теці Forever, а не Classic чи Retail. Теку гри відкриває Battle.net: шестірня біля кнопки «Грати» → Show in Explorer.')},
                {'t': t('Включение', 'Enabling', 'Вмикання'),
                 'd': t('Esc → AddOns или кнопка AddOns на выборе персонажа. Поставьте галочку и нажмите Reload UI.', 'Esc → AddOns, or the AddOns button on the character screen. Tick the box and press Reload UI.', 'Esc → AddOns або кнопка AddOns на виборі персонажа. Поставте галочку й натисніть Reload UI.')},
                {'t': t('Если аддона нет в списке', 'If the addon is not in the list', 'Якщо аддона немає в списку'),
                 'd': t('Перезапустите игру полностью: новые папки она видит только при запуске.', 'Restart the game completely: it only sees new folders at launch.', 'Перезапустіть гру повністю: нові теки вона бачить лише під час запуску.')},
                {'t': t('Обновление', 'Updating', 'Оновлення'),
                 'd': t('После обновления аддона обычно хватает команды /reload.', 'After an addon update the /reload command is usually enough.', 'Після оновлення аддона зазвичай досить команди /reload.')},
            ]),
            ('tip', t('Load out of date AddOns загружает устаревшие файлы. Включайте только для аддонов, у которых есть файл Forever, но игра считает его старым.', 'Load out of date AddOns loads outdated files. Enable it only for addons that have a Forever file that the game considers old.', 'Load out of date AddOns завантажує застарілі файли. Вмикайте лише для аддонів, у яких є файл Forever, але гра вважає його старим.')),
            ('text', [t('На бете аддоны лежали в World of Warcraft\\_classic_beta_\\Interface\\AddOns. Папку для релиза Blizzard не называла: после 05.11 проверьте путь через Show in Explorer или доверьте его менеджеру.', 'In the beta, addons lived in World of Warcraft\\_classic_beta_\\Interface\\AddOns. Blizzard has not named the release folder: after November 4–5, check the path through Show in Explorer or leave it to the manager.', 'На бета-тесті аддони лежали в World of Warcraft\\_classic_beta_\\Interface\\AddOns. Теку для релізу Blizzard не назвала: після 5 листопада перевірте шлях через Show in Explorer або довірте його менеджеру.')]),
        ]},
        {'id': 'problems', 'title': t('Частые проблемы', 'Common problems', 'Часті проблеми'), 'blocks': [
            ('table', {'head': [t('Проблема', 'Problem', 'Проблема'), t('Что делать', 'What to do', 'Що робити')], 'rows': [
                [t('Ошибки Lua при входе', 'Lua errors on login', 'Помилки Lua під час входу'), t('Выключите все аддоны и включайте по одному. BugSack покажет, какой виноват.', 'Disable all addons and enable them one by one. BugSack shows which one is guilty.', 'Вимкніть усі аддони й вмикайте по одному. BugSack покаже, який винен.')],
                [t('Аддона нет в списке', 'The addon is not in the list', 'Аддона немає в списку'), t('Полный перезапуск игры. Проверьте, что папка аддона лежит прямо в Interface\\AddOns, а не во вложенной папке из архива.', 'Fully restart the game. Make sure the addon folder sits directly in Interface\\AddOns, not in a nested folder from the archive.', 'Повний перезапуск гри. Перевірте, що тека аддона лежить прямо в Interface\\AddOns, а не у вкладеній теці з архіву.')],
                [t('Аддон помечен устаревшим', 'The addon is marked out of date', 'Аддон позначено застарілим'), t('Нужен файл «WoW Forever». Load out of date AddOns — только если такой файл уже стоит.', 'You need the “WoW Forever” file. Load out of date AddOns only if such a file is already installed.', 'Потрібен файл «WoW Forever». Load out of date AddOns — лише якщо такий файл уже стоїть.')],
                [t('Счётчик урона или таймеры пустые', 'The damage meter or timers are empty', 'Лічильник шкоди або таймери порожні'), t('Аддон читает боевой журнал. Возьмите версию Forever или встроенный счётчик. Details! с пустыми окнами чинили альфа-версией.', 'The addon reads the combat log. Get the Forever version or use the built-in meter. Details! with empty windows was fixed with an alpha version.', 'Аддон читає бойовий журнал. Візьміть версію Forever або вбудований лічильник. Details! з порожніми вікнами лагодили альфа-версією.')],
                [t('Угроза босса пропадает в бою', 'Boss threat disappears in combat', 'Загроза боса зникає в бою'), t('Ограничение игры, не ошибка аддона. Пока вы не в списке угрозы врага, её не видно.', 'A game limitation, not an addon bug. Until you are on the enemy’s threat list, its threat is not visible.', 'Обмеження гри, не помилка аддона. Поки ви не в списку загрози ворога, її не видно.')],
                [t('Всё сломалось после патча', 'Everything broke after a patch', 'Усе зламалося після патча'), t('Сначала обновите аддоны, потом трогайте настройки.', 'Update your addons first, only then touch the settings.', 'Спершу оновіть аддони, потім чіпайте налаштування.')],
                [t('Две карты или две сумки конфликтуют', 'Two maps or two bag addons conflict', 'Дві мапи чи дві сумки конфліктують'), t('Оставьте один аддон карты мира и один аддон сумок.', 'Keep one world map addon and one bag addon.', 'Залиште один аддон мапи світу й один аддон сумок.')],
            ]}),
            ('tip', t('Раскладку Edit Mode экспортируйте строкой и храните вне папки игры: файлом она не переносится.', 'Export your Edit Mode layout as a string and keep it outside the game folder: it does not transfer as a file.', 'Розкладку Edit Mode експортуйте рядком і зберігайте поза текою гри: файлом вона не переноситься.')),
        ]},
        {'id': 'faq', 'title': t('Частые вопросы', 'Common questions', 'Часті питання'), 'blocks': [
            ('faq', [
                {'id': 'works', 'q': t('Работают ли аддоны в WoW Forever?', 'Do addons work in WoW Forever?', 'Чи працюють аддони у WoW Forever?'),
                 'a': [t('Да. Forever использует API современного WoW с ограничениями Midnight. Аддоны Classic не грузятся, нужен файл «WoW Forever» на CurseForge.', 'Yes. Forever uses the modern WoW API with the Midnight restrictions. Classic addons won’t load: you need a “WoW Forever” file on CurseForge.', 'Так. Forever використовує API сучасного WoW з обмеженнями Midnight. Аддони Classic не завантажуються, потрібен файл «WoW Forever» на CurseForge.')]},
                {'id': 'questie', 'q': t('Работает ли Questie в WoW Forever?', 'Does Questie work in WoW Forever?', 'Чи працює Questie у WoW Forever?'),
                 'a': [t('Да, у Questie есть версия для Forever, обновлённая под новые зоны. Цели заданий на карте есть и без аддона, в фильтре карты мира.', 'Yes, Questie has a Forever version, updated for the new zones. Quest objectives are on the map even without an addon, in the world map filter.', 'Так, у Questie є версія для Forever, оновлена під нові зони. Цілі завдань на мапі є й без аддона, у фільтрі мапи світу.')]},
                {'id': 'weakauras', 'q': t('Есть ли WeakAuras в WoW Forever?', 'Is there WeakAuras in WoW Forever?', 'Чи є WeakAuras у WoW Forever?'),
                 'a': [t('Самого WeakAuras нет: у него нет файла Forever. Есть ForeverAuras — форк WeakAuras, сделанный под Forever другим автором. Окно настроек открывает команда /fa.', 'Not WeakAuras itself: it has no Forever file. There is ForeverAuras, a WeakAuras fork made for Forever by another author. The /fa command opens its options.', 'Самого WeakAuras немає: у нього немає файлу Forever. Є ForeverAuras — форк WeakAuras, зроблений під Forever іншим автором. Вікно налаштувань відкриває команда /fa.'),
                       t('Свои кулдауны и баффы без аддонов показывает встроенный Cooldown Manager: Options → Gameplay Enhancement.', 'Your own cooldowns and buffs are shown without addons by the built-in Cooldown Manager: Options → Gameplay Enhancement.', 'Власні кулдауни та баффи без аддонів показує вбудований Cooldown Manager: Options → Gameplay Enhancement.')],
                 'link': (t('ForeverAuras на CurseForge', 'ForeverAuras on CurseForge', 'ForeverAuras на CurseForge'), 'https://www.curseforge.com/wow/addons/foreverauras')},
                {'id': 'meter', 'q': t('Нужен ли счётчик урона в WoW Forever?', 'Do I need a damage meter in WoW Forever?', 'Чи потрібен лічильник шкоди у WoW Forever?'),
                 'a': [t('Встроенный есть. Details! или Forever Meter добавляют угрозу и подробности. Аддоны, которые читают боевой журнал (Skada, Recount), не работают.', 'There is a built-in one. Details! or Forever Meter add threat and details. Addons that read the combat log (Skada, Recount) don’t work.', 'Вбудований є. Details! або Forever Meter додають загрозу й подробиці. Аддони, що читають бойовий журнал (Skada, Recount), не працюють.')]},
                {'id': 'where', 'q': t('Куда ставить аддоны WoW Forever?', 'Where do I install WoW Forever addons?', 'Куди ставити аддони WoW Forever?'),
                 'a': [t('В Interface\\AddOns в папке Forever. Проще всего через CurseForge или Wago App с выбранной версией Forever.', 'In Interface\\AddOns inside the Forever folder. The easiest way is through CurseForge or Wago App with the Forever version selected.', 'У Interface\\AddOns у теці Forever. Найпростіше через CurseForge або Wago App з обраною версією Forever.')]},
                {'id': 'missing', 'q': t('Почему аддон не появляется в игре?', 'Why doesn’t the addon show up in the game?', 'Чому аддон не з’являється в грі?'),
                 'a': [t('У него нет файла Forever, папка лежит не там или игра не перезапускалась. Новые аддоны видны только после полного перезапуска.', 'It has no Forever file, the folder is in the wrong place, or the game was not restarted. New addons appear only after a full restart.', 'У нього немає файлу Forever, тека лежить не там або гру не перезапускали. Нові аддони видно лише після повного перезапуску.')]},
            ]),
        ]},
    ],
})


# ---------- День 1: чек-лист старта (26.10). Только факты, которые уже есть в гайдах; отметки — localStorage gabella-day1 ----------
# Пункт = {'id', 't', 'd', 'href', 'go'}; 'langs' — пункт только на этих языках. Блок ('checks', [пункты]), счётчик ('ckbar', {...}).

def _ck(id_, title, d, href, go, langs=None):
    item = {'id': id_, 't': title, 'd': d, 'href': href, 'go': go}
    if langs:
        item['langs'] = langs
    return item


def _newbie():
    """Top of the Day 1 checklist for the «Я новичок» button of the home page: where to go next, with the main action."""
    from html import escape
    from content.spec_cheats import n9
    nxt = n9('Новичку, по порядку:', 'New player, in order:', 'Новачку, по порядку:', 'Als Neuling der Reihe nach:', 'Débutant, dans l’ordre :',
             'Si eres nuevo, en orden:', 'Para iniciantes, em ordem:', 'Se sei nuovo, in ordine:', 'Dla nowych, po kolei:')
    s1 = n9('Выбрать класс', 'Pick a class', 'Обрати клас', 'Klasse wählen', 'Choisir une classe', 'Elegir clase', 'Escolher classe', 'Scegli la classe', 'Wybierz klasę')
    s2 = n9('Взять билд', 'Take a build', 'Взяти білд', 'Build nehmen', 'Prendre un build', 'Coger un build', 'Pegar uma build', 'Prendi una build', 'Weź build')
    s3 = n9('Прокачка 1–60', 'Leveling 1–60', 'Прокачування 1–60', 'Leveln 1–60', 'Progression 1–60', 'Subida 1–60', 'Evolução 1–60', 'Salita 1–60', 'Levelowanie 1–60')
    return {l: (f'<p class="small">{escape(nxt[l])}</p>'
                f'<p class="nsteps"><a class="btn" href="../../classes/#choose">{escape(s1[l])}</a><span class="nr"><span aria-hidden="true">→</span>'
                f'<a href="../builds/">{escape(s2[l])}</a><span aria-hidden="true">→</span><a href="../leveling/">{escape(s3[l])}</a></span></p>')
            for l in nxt}


_NEWBIE = _newbie()


GUIDES.append({
    'slug': 'launch-checklist', 'art': 'hero_campfire', 'hero': 'hero_guides', 'tile_art': 'hero_campfire', 'og': 'guides', 'js': 'checklist',
    'title': t('День 1: чек-лист старта', 'Day 1: Launch Checklist', 'День 1: чек-лист старту'),
    'crumb': t('День 1', 'Day 1', 'День 1'),
    'lead': t('Что сделать до старта WoW Forever, в первые часы и в первый вечер. Отметки сохраняются в этом браузере.',
              'What to do before the WoW Forever launch, in the first hours and on the first evening. Your ticks are saved in this browser.',
              'Що зробити до старту WoW Forever, у перші години та першого вечора. Позначки зберігаються в цьому браузері.'),
    'tile': t('Что сделать до старта и в первый вечер', 'What to do before launch and on the first evening', 'Що зробити до старту й першого вечора'),
    'pills': [t('Старт 04.11.2026, 23:00 UTC (по Киеву 05.11, 01:00)', 'Launch 04.11.2026, 23:00 UTC (Kyiv: 05.11, 01:00)', 'Старт 04.11.2026, 23:00 UTC (за Києвом 05.11, 01:00)')],
    'sources': [
        (t('Blizzard: старт и коды Invite-A-Friend', 'Blizzard: launch and Invite-A-Friend codes', 'Blizzard: старт і коди Invite-A-Friend'),
         'https://news.blizzard.com/en-us/article/24301508'),
        (t('Blizzard: система Legacy', 'Blizzard: Legacy system', 'Blizzard: система Legacy'), 'https://news.blizzard.com/en-gb/article/24307383'),
        (t('Battle.net Shop: системные требования WoW Forever', 'Battle.net Shop: WoW Forever system requirements', 'Battle.net Shop: системні вимоги WoW Forever'), SHOP),
        (t('Icy Veins: Blizzard об аддонах в Forever', 'Icy Veins: Blizzard on addons in Forever', 'Icy Veins: Blizzard про аддони у Forever'),
         'https://www.icy-veins.com/wow-forever/news/addons-in-wow-forever-blizzard-devs-just-addressed-the-big-question/'),
        (t('Warcraft Tavern: опыт и отдых', 'Warcraft Tavern: experience and rested XP', 'Warcraft Tavern: досвід і відпочинок'),
         'https://www.warcrafttavern.com/forever/guides/experience/'),
    ],
    'sections': [
        {'id': 'before', 'title': t('До старта', 'Before launch', 'До старту'), 'blocks': [
            ('raw', _NEWBIE),
            ('ckbar', {'done': t('Отмечено', 'Ticked', 'Відмічено'), 'reset': t('Снять отметки', 'Clear ticks', 'Зняти позначки')}),
            ('checks', [
                _ck('time', t('Время старта', 'Launch time', 'Час старту'),
                    t('В Европе 05.11, в Америке 04.11. Старт в 23:00 UTC.', '04.11 in the Americas, 05.11 in Europe. Launch is at 23:00 UTC.', 'У Європі 05.11, в Америці 04.11. Старт о 23:00 UTC.'),
                    'guides/faq/#dates', t('Все даты старта', 'All launch dates', 'Усі дати старту')),
                _ck('sub', t('Подписка или игровое время', 'Subscription or game time', 'Підписка або ігровий час'),
                    t('Forever входит в подписку WoW, отдельно игру покупать не нужно. В Epic Pack и Collection есть 30 дней игрового времени, их начислят в день старта.',
                      'Forever is included in the WoW subscription, you do not buy the game separately. The Epic Pack and Collection include 30 days of game time, added on launch day.',
                      'Forever входить у підписку WoW, окремо гру купувати не потрібно. В Epic Pack і Collection є 30 днів ігрового часу, їх нарахують у день старту.'),
                    'guides/faq/#editions', t('Цены и подписка', 'Prices and subscription', 'Ціни та підписка')),
                _ck('pc', t('Battle.net и место на диске', 'Battle.net and disk space', 'Battle.net і місце на диску'),
                    t('Нужны приложение Battle.net и 128 ГБ на SSD. Старые видеокарты игру не запустят: сверьте свою с таблицей.',
                      'You need the Battle.net app and 128 GB on an SSD. Older graphics cards will not start the game: check yours against the table.',
                      'Потрібні застосунок Battle.net і 128 ГБ на SSD. Старі відеокарти гру не запустять: звірте свою з таблицею.'),
                    'guides/requirements/', t('Системные требования', 'System requirements', 'Системні вимоги')),
                _ck('mode', t('Регион, режим и фракция', 'Region, mode and faction', 'Регіон, режим і фракція'),
                    t('Решите с друзьями заранее. Режим выбирают один раз, группа собирается только внутри режима, в PvP на аккаунте одна фракция.',
                      'Agree with your friends in advance. The mode is chosen once, groups form only within a mode, and in PvP an account has one faction.',
                      'Вирішіть із друзями заздалегідь. Режим обирають один раз, група збирається лише в межах режиму, у PvP на акаунті одна фракція.'),
                    'guides/faq/#modes', t('Как выбрать режим', 'How to choose a mode', 'Як обрати режим')),
                _ck('ping', t('Пинг и очередь', 'Ping and queue', 'Пінг і черга'),
                    t('Узнайте свой регион, что делать при высоком пинге и как не потерять место в очереди на входе.',
                      'Find your region, what to do about high ping and how not to lose your place in the login queue.',
                      'Дізнайтеся свій регіон, що робити з високим пінгом і як не втратити місце в черзі на вхід.'),
                    'tools/#ping', t('Проверить пинг', 'Check your ping', 'Перевірити пінг')),
                _ck('class', t('Класс', 'Class', 'Клас'),
                    t('Тир-лист сравнивает классы и спеки для прокачки, подземелий и PvP по данным беты.',
                      'The tier list compares classes and specs for leveling, dungeons and PvP, based on beta data.',
                      'Тір-лист порівнює класи й спеціалізації для прокачування, підземель і PvP за даними бети.'),
                    'guides/tier-list/', t('Тир-лист', 'Tier list', 'Тір-лист')),
                _ck('race', t('Раса под класс', 'Race for your class', 'Раса під клас'),
                    t('Способности рас в Forever переделаны. Какую расу взять под класс за Альянс и Орду — в отдельном гайде.',
                      'Racial abilities were reworked in Forever. Which race to take for your class on the Alliance and Horde is in a separate guide.',
                      'Здібності рас у Forever перероблено. Яку расу взяти під клас за Альянс і Орду — в окремому гайді.'),
                    'guides/best-race/', t('Лучшая раса', 'Best race', 'Найкраща раса')),
                _ck('name', t('Имя и фамилия', 'First name and surname', 'Ім’я та прізвище'),
                    t('Полное имя уникально во всём регионе. Владельцы Heroic, Epic и Collection занимают до трёх имён с 27.10 по 03.11. Держите два-три запасных варианта.',
                      'The full name is unique across the whole region. Heroic, Epic and Collection owners can claim up to three names from 27.10 to 03.11. Keep two or three backups.',
                      'Повне ім’я унікальне в усьому регіоні. Власники Heroic, Epic і Collection займають до трьох імен з 27.10 по 03.11. Тримайте два-три запасні варіанти.'),
                    'guides/name-reservation/', t('Резерв имён', 'Name reservation', 'Резерв імен')),
                _ck('iaf', t('Код для друга', 'A code for a friend', 'Код для друга'),
                    t('С набором приходят коды Invite-A-Friend: по коду друг играет с 04.11 по 11.11 без подписки. Heroic даёт 1 код, Epic и Collection — 3. Коды приходят на почту.',
                      'Packs come with Invite-A-Friend codes: with one, a friend plays from 04.11 to 11.11 without a subscription. Heroic gives 1 code, Epic and Collection give 3. The codes arrive by email.',
                      'З набором приходять коди Invite-A-Friend: з кодом друг грає з 04.11 по 11.11 без підписки. Heroic дає 1 код, Epic і Collection — 3. Коди приходять на пошту.'),
                    'guides/faq/#editions', t('Наборы и коды', 'Packs and codes', 'Набори та коди')),
                _ck('group', t('Группа на старт', 'A group for launch', 'Група на старт'),
                    t('Соберите состав в конструкторе группы и отправьте ссылку друзьям.',
                      'Build the party in the group builder and send the link to your friends.',
                      'Зберіть склад у конструкторі групи й надішліть посилання друзям.'),
                    'tools/#raid', t('Конструктор группы', 'Group builder', 'Конструктор групи')),
                _ck('addons', t('Аддоны', 'Addons', 'Аддони'),
                    t('Поставьте CurseForge или Wago App и выберите версию Forever. Файлы для Classic в Forever не грузятся.',
                      'Install CurseForge or Wago App and choose the Forever version. Classic files will not load in Forever.',
                      'Встановіть CurseForge або Wago App і оберіть версію Forever. Файли для Classic у Forever не завантажуються.'),
                    'guides/addons/#list', t('Аддоны и интерфейс', 'Addons and Interface', 'Аддони та інтерфейс')),
                _ck('lang', {'ru': 'Русский клиент'},
                    {'ru': 'В Battle.net откройте настройки игры и выберите язык «Русский». Русификатор не нужен.'},
                    'guides/faq/#language', {'ru': 'Играть на русском'}, ('ru',)),
                _ck('lang', {'uk': 'Українська мова'},
                    {'uk': 'Українського клієнта у Forever немає. Українською грають з аддоном UA_Forever поверх клієнта.'},
                    'guides/ukrainian/', {'uk': 'Як грати українською'}, ('uk',)),
            ]),
        ]},
        {'id': 'hours', 'title': t('Первые часы', 'First hours', 'Перші години'), 'blocks': [
            ('checks', [
                _ck('look', t('Classic или Enhanced', 'Classic or Enhanced', 'Classic чи Enhanced'),
                    t('При первом входе игра предлагает набор настроек. Экран выбора больше не появится, но каждую настройку можно поменять отдельно.',
                      'On first login the game offers a set of settings. The choice screen will not come back, but every setting can be changed on its own.',
                      'Під час першого входу гра пропонує набір налаштувань. Екран вибору більше не з’явиться, але кожне налаштування можна змінити окремо.'),
                    'guides/faq/#graphics', t('Classic и Enhanced: разница', 'Classic and Enhanced: the difference', 'Classic і Enhanced: різниця')),
                _ck('start', t('Стартовая зона', 'Starting zone', 'Стартова зона'),
                    t('Задания стартовой зоны своей расы до 10 уровня. На 10 уровне открываются таланты.',
                      'Your race’s starting zone quests up to level 10. Talents unlock at level 10.',
                      'Завдання стартової зони своєї раси до 10 рівня. На 10 рівні відкриваються таланти.'),
                    'guides/leveling/#route', t('Маршрут по зонам', 'Zone route', 'Маршрут зонами')),
                _ck('cooking', t('Кулинария сразу', 'Cooking right away', 'Кулінарія одразу'),
                    t('Костёр по Кулинарии становится лагерем, а готовая еда даёт +5% опыта за врагов. Для базового костра хватит выученной профессии.',
                      'A Cooking campfire becomes a camp, and cooked food gives +5% experience from enemies. A basic campfire only needs the profession learned.',
                      'Вогнище з Кулінарії стає табором, а готова їжа дає +5% досвіду за ворогів. Для базового вогнища досить вивченої професії.'),
                    'guides/leveling/#camp', t('Лагерь и профессии', 'Camp and professions', 'Табір і професії')),
                _ck('profs', t('Две профессии', 'Two professions', 'Дві професії'),
                    t('Сбор кормит деньгами и ремеслом. Пары под ваш класс — в гайде по профессиям.',
                      'Gathering brings in money and feeds a craft. Pairs for your class are in the professions guide.',
                      'Збирання дає гроші й годує ремесло. Пари під ваш клас — у гайді з професій.'),
                    'guides/professions/#pairs', t('Пары под класс', 'Pairs for your class', 'Пари під клас')),
                _ck('cdm', 'Cooldown Manager',
                    t('Встроенная панель своих кулдаунов и баффов вместо WeakAuras. По умолчанию выключена: Options → Gameplay Enhancement.',
                      'The built-in panel for your own cooldowns and buffs instead of WeakAuras. Off by default: Options → Gameplay Enhancement.',
                      'Вбудована панель власних кулдаунів і баффів замість WeakAuras. За замовчуванням вимкнена: Options → Gameplay Enhancement.'),
                    'guides/addons/#builtin', t('Встроенные замены аддонов', 'Built-in addon replacements', 'Вбудовані заміни аддонів')),
                _ck('folder', t('Папка аддонов', 'Addon folder', 'Тека аддонів'),
                    t('Папку для релиза Blizzard не называла. Проверьте путь: шестерёнка у кнопки «Играть» в Battle.net → Show in Explorer, аддоны лежат в Interface\\AddOns.',
                      'Blizzard has not named the release folder. Check the path: the gear next to the Play button in Battle.net → Show in Explorer, addons go in Interface\\AddOns.',
                      'Теку для релізу Blizzard не назвала. Перевірте шлях: шестірня біля кнопки «Грати» в Battle.net → Show in Explorer, аддони лежать в Interface\\AddOns.'),
                    'guides/addons/#install', t('Установка аддонов', 'Installing addons', 'Встановлення аддонів')),
                _ck('play', t('В игре', 'In game', 'У грі'),
                    t('Откройте «В игре» на телефоне или втором мониторе: зоны под ваш уровень, подземелья, таймер еды и радио.',
                      'Open “In game” on your phone or a second monitor: zones for your level, dungeons, a food timer and radio.',
                      'Відкрийте «У грі» на телефоні або другому моніторі: зони під ваш рівень, підземелля, таймер їжі й радіо.'),
                    'play/', t('Открыть «В игре»', 'Open “In game”', 'Відкрити «У грі»')),
            ]),
        ]},
        {'id': 'evening', 'title': t('Первый вечер', 'First evening', 'Перший вечір'), 'blocks': [
            ('checks', [
                _ck('duo', t('Вдвоём — уровни рядом', 'Duo: keep levels close', 'Удвох — рівні поруч'),
                    t('Берите задания вместе и сдавайте одновременно: за задание каждый получает полный опыт, а опыт за врагов делится.',
                      'Pick up quests together and turn them in at the same time: each player gets full experience for a quest, while experience from enemies is shared.',
                      'Беріть завдання разом і здавайте одночасно: за завдання кожен отримує повний досвід, а досвід за ворогів ділиться.'),
                    'guides/leveling/#group', t('Соло, вдвоём или группой', 'Solo, duo or group', 'Соло, удвох чи групою')),
                _ck('dungeon', t('Первое подземелье', 'First dungeon', 'Перше підземелля'),
                    t('Подземелья рассчитаны на 5 игроков: танк, лекарь, трое с уроном. Фильтр покажет, что подходит вашему уровню.',
                      'Dungeons are designed for 5 players: a tank, a healer and three damage dealers. The filter shows what fits your level.',
                      'Підземелля розраховані на 5 гравців: танк, цілитель, троє зі шкодою. Фільтр покаже, що підходить вашому рівню.'),
                    'guides/dungeons/#list', t('Подземелья по уровням', 'Dungeons by level', 'Підземелля за рівнями')),
                _ck('legacy', t('Первое очко Legacy', 'First Legacy point', 'Перше очко Legacy'),
                    t('Legacy открывается с первым очком: 25 уровень, 150 в основной профессии (не сбор) или вся карта мира. Окно — клавиша Y.',
                      'Legacy unlocks with your first point: level 25, 150 in a main profession (not gathering) or the whole world map. The window opens with Y.',
                      'Legacy відкривається з першим очком: 25 рівень, 150 в основній професії (не збирання) або вся мапа світу. Вікно — клавіша Y.'),
                    'guides/legacy/#start', t('Система Legacy', 'The Legacy System', 'Система Legacy')),
                _ck('logout', t('Выход в таверне', 'Log out at an inn', 'Вихід у таверні'),
                    t('Выходите из игры в таверне, столице или на спальнике: следующий вечер начнётся с двойного опыта за врагов. Еда, спальник и отдых складываются.',
                      'Log out in an inn, a capital or on the bedroll: the next evening starts with double experience from enemies. Food, the bedroll and rest stack.',
                      'Виходьте з гри в таверні, столиці або на спальнику: наступний вечір почнеться з подвійного досвіду за ворогів. Їжа, спальник і відпочинок складаються.'),
                    'guides/leveling/#pace', t('Темп и отдых', 'Pace and rest', 'Темп і відпочинок')),
            ]),
        ]},
    ],
})


# ---------- День старта: время по часам читателя, очереди и слои, официальные каналы статуса. Чек-лист «День 1» не повторяет ----------

GUIDES.append({
    'slug': 'launch-day', 'art': 'hero_night', 'hero': 'hero_night', 'tile_art': 'hero_night', 'js': 'launchday',
    'title': t('День старта: время, очереди, статус', 'Launch Day: Time, Queues, Status', 'День старту: час, черги, статус'),
    'crumb': t('День старта', 'Launch day', 'День старту'),
    'lead': t('Когда открывается WoW Forever по вашему времени, чего ждать в первые часы и где Blizzard сообщает о сбоях.',
              'When WoW Forever opens in your time zone, what to expect in the first hours and where Blizzard reports outages.',
              'WoW Forever стартує 5 листопада о 01:00 за Києвом (04.11, 23:00 UTC). Чого чекати в перші години та де Blizzard повідомляє про збої.'),
    'tile': t('Время старта, очереди и где смотреть статус серверов', 'Launch time, queues and where to check server status', 'Час старту, черги та де дивитися статус серверів'),
    'pills': [t('Старт 04.11.2026, 23:00 UTC', 'Launch 04.11.2026, 23:00 UTC', 'Старт 04.11.2026, 23:00 UTC'),
              t('Статус — только каналы Blizzard', 'Status: Blizzard channels only', 'Статус — лише канали Blizzard')],
    'sources': [
        (t('Blizzard: дата и время старта', 'Blizzard: launch date and time', 'Blizzard: дата й час старту'), 'https://news.blizzard.com/en-us/article/24301508'),
        (t('Blizzard: время старта по Парижу (фр.)', 'Blizzard: launch time in Paris (French)', 'Blizzard: час старту за Парижем (фр.)'), 'https://news.blizzard.com/fr-fr/article/24301508'),
        (t('Blizzard: резерв имён и установка клиента', 'Blizzard: name reservation and client install', 'Blizzard: резерв імен і встановлення клієнта'), 'https://news.blizzard.com/en-us/article/24303866'),
        (t('Blizzard: режимы, язык и Hardcore', 'Blizzard: rulesets, language and Hardcore', 'Blizzard: режими, мова й Hardcore'), 'https://news.blizzard.com/en-gb/article/24302070'),
        (t('Правительство Британской Колумбии: постоянное летнее время', 'Government of British Columbia: permanent daylight time', 'Уряд Британської Колумбії: постійний літній час'),
         'https://www2.gov.bc.ca/gov/content/governments/celebrating-british-columbia/daylight-saving-time'),
        (t('GameSpot: заявление Blizzard о слоях', 'GameSpot: Blizzard statement on layering', 'GameSpot: заява Blizzard про шари'),
         'https://www.gamespot.com/articles/wow-forevers-divisive-layering-will-see-major-improvements-for-launch-blizzard-says/'),
        (t('Bolverk Games: очереди и отключения в бете', 'Bolverk Games: beta queues and disconnects', 'Bolverk Games: черги й відключення в беті'),
         'https://bolverkgames.com/wow/wow-forever-beta-hits-hour-long-queues-blizzard-scrambles-to-fix-disconnects/'),
        (t('Mein-MMO: слои в конце беты', 'Mein-MMO: layering at the end of the beta', 'Mein-MMO: шари наприкінці бети'),
         'https://mein-mmo.de/wow-forever-beta-endet-community-noch-sorgen/'),
    ],
    'sections': [
        {'id': 'time', 'title': t('Время старта', 'Launch time', 'Час старту'), 'blocks': [
            ('launch', {'left': t('до старта', 'until launch', 'до старту'), 'out': t('Игра вышла', 'The game is out', 'Гра вийшла'),
                        'your': t('по вашему времени', 'your time', 'за вашим часом'),
                        'd': t('дн', 'd', 'дн'), 'h': t('ч', 'h', 'год'), 'm': t('мин', 'min', 'хв'),
                        'cal': t('Добавить в календарь', 'Add to calendar', 'Додати в календар'),
                        'gcal': t('Google Календарь', 'Google Calendar', 'Google Календар'),
                        'ev': t('Старт WoW Forever', 'WoW Forever launch', 'Старт WoW Forever')}),
            ('text', [t('Blizzard: WoW Forever выходит во всём мире 04.11.2026 в 15:00 по тихоокеанскому времени (PST), это 23:00 UTC 04.11.',
                        'Blizzard: WoW Forever launches worldwide on 04.11.2026 at 15:00 Pacific time (PST), which is 23:00 UTC on 04.11.',
                        'Blizzard: WoW Forever виходить у всьому світі 04.11.2026 о 15:00 за тихоокеанським часом (PST), це 23:00 UTC 04.11.'),
                      t('В Европе это уже 5 ноября. Великобритания, Ирландия и Португалия встречают старт в 23:00 04.11.',
                        'In most of Europe it is already 5 November. The UK, Ireland and Portugal get the launch at 23:00 on 04.11.',
                        'У Європі це вже 5 листопада. Велика Британія, Ірландія та Португалія зустрічають старт о 23:00 04.11.'),
                      t('Время в таблице уже зимнее: Европа перевела часы 25.10, США и Канада — 01.11. Британская Колумбия с 01.11 часы не переводит и остаётся на UTC-7, поэтому в Ванкувере старт в 16:00, на час позже, чем в Лос-Анджелесе.',
                        'The table already uses winter time: Europe changed its clocks on 25.10, the US and Canada on 01.11. British Columbia stops changing clocks on 01.11 and stays on UTC-7, so in Vancouver the launch is at 16:00, an hour later than in Los Angeles.',
                        'Час у таблиці вже зимовий: Європа перевела годинники 25.10, США й Канада — 01.11. Британська Колумбія з 01.11 годинники не переводить і лишається на UTC-7, тому у Ванкувері старт о 16:00, на годину пізніше, ніж у Лос-Анджелесі.')]),
            ('table', {'head': [t('Город', 'City', 'Місто'), t('Часовой пояс', 'Time zone', 'Часовий пояс'), t('Старт по местному времени', 'Launch, local time', 'Старт за місцевим часом')], 'rows': [
                [t('Лос-Анджелес, Сиэтл', 'Los Angeles, Seattle', 'Лос-Анджелес, Сіетл'), t('PT (тихоокеанское), UTC-8', 'PT (Pacific), UTC-8', 'PT (тихоокеанський), UTC-8'), '04.11, 15:00'],
                [t('Денвер, Финикс, Ванкувер', 'Denver, Phoenix, Vancouver', 'Денвер, Фінікс, Ванкувер'), 'UTC-7', '04.11, 16:00'],
                [t('Чикаго, Мехико', 'Chicago, Mexico City', 'Чикаго, Мехіко'), 'UTC-6', '04.11, 17:00'],
                [t('Нью-Йорк, Торонто', 'New York, Toronto', 'Нью-Йорк, Торонто'), t('ET (восточное), UTC-5', 'ET (Eastern), UTC-5', 'ET (східний), UTC-5'), '04.11, 18:00'],
                [t('Сан-Паулу, Буэнос-Айрес', 'São Paulo, Buenos Aires', 'Сан-Паулу, Буенос-Айрес'), 'UTC-3', '04.11, 20:00'],
                [t('Лондон, Дублин, Лиссабон', 'London, Dublin, Lisbon', 'Лондон, Дублін, Лісабон'), 'UTC+0', '04.11, 23:00'],
                [t('Берлин, Париж, Мадрид, Рим, Варшава', 'Berlin, Paris, Madrid, Rome, Warsaw', 'Берлін, Париж, Мадрид, Рим, Варшава'), t('CET (центральноевропейское), UTC+1', 'CET (Central European), UTC+1', 'CET (центральноєвропейський), UTC+1'), '05.11, 00:00'],
                [t('Киев', 'Kyiv', 'Київ'), t('Киев (EET), UTC+2', 'Kyiv (EET), UTC+2', 'Київ (EET), UTC+2'), '05.11, 01:00'],
                [t('Тайбэй', 'Taipei', 'Тайбей'), 'UTC+8', '05.11, 07:00'],
                [t('Сеул', 'Seoul', 'Сеул'), 'UTC+9', '05.11, 08:00'],
                [t('Сидней', 'Sydney', 'Сідней'), 'UTC+11', '05.11, 10:00'],
                [t('Окленд', 'Auckland', 'Окленд'), 'UTC+13', '05.11, 12:00'],
            ]}),
        ]},
        {'id': 'before', 'title': t('Перед стартом', 'Before launch', 'Перед стартом'), 'blocks': [
            ('steps', [
                {'t': t('Клиент заранее', 'Install the client early', 'Клієнт заздалегідь'),
                 'd': t('Battle.net → World of Warcraft → меню версии над кнопкой «Играть» → World of Warcraft: Forever → «Установить». Так Blizzard описывает установку к резерву имён. Заодно обновите драйвер видеокарты.',
                        'Battle.net → World of Warcraft → the version menu above the Play button → World of Warcraft: Forever → Install. This is how Blizzard describes the install for name reservation. Update your graphics driver too.',
                        'Battle.net → World of Warcraft → меню версії над кнопкою «Грати» → World of Warcraft: Forever → Install. Так Blizzard описує встановлення до резерву імен. Заразом оновіть драйвер відеокарти.')},
                {'t': t('Подписка или игровое время', 'Subscription or game time', 'Підписка або ігровий час'),
                 'd': t('Forever входит в подписку WoW: без неё или игрового времени в момент старта не войти. Набор покупать не обязательно.',
                        'Forever comes with a WoW subscription: without one or game time you cannot log in at launch. A pack is not required.',
                        'Forever входить у підписку WoW: без неї або ігрового часу в момент старту не увійти. Набір купувати не обов’язково.')},
                {'t': t('Резерв имён до 03.11', 'Name reservation until 03.11', 'Резерв імен до 03.11'),
                 'd': t('Для владельцев наборов Heroic, Epic и Collection: до трёх персонажей на аккаунт во всех режимах вместе, кто первым пришёл, тот и занял. Режим выбирается при запуске клиента.',
                        'For Heroic, Epic and Collection owners: up to three characters per account across all modes, first come, first served. You pick the mode when you start the client.',
                        'Для власників наборів Heroic, Epic і Collection: до трьох персонажів на акаунт у всіх режимах разом, хто перший прийшов, той і зайняв. Режим обирають під час запуску клієнта.')},
                {'t': t('Invite-A-Friend', 'Invite-A-Friend', 'Invite-A-Friend'),
                 'd': t('Коды из наборов действуют в неделю старта: с 04.11 по 11.11 по тихоокеанскому времени, в Европе с 05.11 по 12.11.',
                        'Codes from the packs work during launch week: 04.11 to 11.11 Pacific time, 05.11 to 12.11 in Europe.',
                        'Коди з наборів діють у тиждень старту: з 04.11 по 11.11 за тихоокеанським часом, у Європі з 05.11 по 12.11.')},
            ]),
        ]},
        {'id': 'mode', 'title': t('Режим и реалм', 'Mode and realm', 'Режим і реалм'), 'blocks': [
            ('table', {'head': [t('Что', 'What', 'Що'), t('Что известно', 'What is known', 'Що відомо')], 'rows': [
                [t('Один сервер на режим', 'One server per mode', 'Один сервер на режим'),
                 t('Реалмов нет: в каждом регионе по одному большому серверу на режим, нагрузку делят слои. Регионы: Америка и Океания, Европа, Корея, Тайвань.',
                   'There are no realms: each region has one large server per mode, and layers share the load. Regions: Americas and Oceania, Europe, Korea, Taiwan.',
                   'Реалмів немає: у кожному регіоні по одному великому серверу на режим, навантаження ділять шари. Регіони: Америка й Океанія, Європа, Корея, Тайвань.')],
                [t('Режим выбирают один раз', 'The mode is chosen once', 'Режим обирають один раз'),
                 t('Перенести персонажа в другой режим нельзя. Исключение — погибший персонаж Hardcore: он продолжает в другом режиме.',
                   'You cannot move a character to another mode. The exception is a Hardcore character who has died: it carries on in another mode.',
                   'Перенести персонажа в інший режим не можна. Виняток — загиблий персонаж Hardcore: він продовжує в іншому режимі.')],
                [t('Группа только в одном режиме', 'Groups stay within one mode', 'Група лише в одному режимі'),
                 t('Группироваться можно только внутри одного режима. В PvP при создании доступна одна фракция.',
                   'You can only group within one mode. In PvP only one faction is available at character creation.',
                   'Групуватися можна лише в межах одного режиму. У PvP під час створення доступна одна фракція.')],
                [t('Язык', 'Language', 'Мова'),
                 t('Языковая настройка на весь аккаунт сводит игроков одного языка. Сменить её можно раз в 24 часа.',
                   'An account-wide language setting matches you with players of the same language. It can be changed once every 24 hours.',
                   'Мовне налаштування на весь акаунт зводить гравців однієї мови. Змінити його можна раз на 24 години.')],
                ['Hardcore',
                 t('Не на старте: Blizzard обещает его после запуска, даты нет. Поля боя общие для всех режимов, кроме Hardcore.',
                   'Not at launch: Blizzard promises it after release, with no date. Battlegrounds are shared by all modes except Hardcore.',
                   'Не на старті: Blizzard обіцяє його після запуску, дати немає. Поля бою спільні для всіх режимів, крім Hardcore.')],
                [(t('Режимы и серверы', 'Modes and servers', 'Режими та сервери'), 'guides/faq/#modes'),
                 t('Обычный, PvP, RP и RP-PvP, регионы и правила выше — подробно.', 'Normal, PvP, RP and RP-PvP, regions and the rules above, in full.', 'Звичайний, PvP, RP і RP-PvP, регіони та правила вище — докладно.')],
            ]}),
            ('tip', t('Договоритесь заранее: одна фракция, один режим, одни и те же дни на старт.',
                      'Agree in advance: one faction, one mode, the same days for launch.',
                      'Домовтеся заздалегідь: одна фракція, один режим, одні й ті самі дні на старт.')),
        ]},
        {'id': 'hour', 'title': t('Первый час', 'First hour', 'Перша година'), 'blocks': [
            ('steps', [
                {'t': t('Набор настроек', 'Settings set', 'Набір налаштувань'),
                 'd': t('При первом входе игра предлагает Classic или Enhanced. Экран выбора не повторится, но каждую настройку можно поменять позже. {beta}',
                        'On first login the game offers Classic or Enhanced. The choice screen will not repeat, but each setting can be changed later. {beta}',
                        'Під час першого входу гра пропонує Classic або Enhanced. Екран вибору не повториться, але кожне налаштування можна змінити пізніше. {beta}')},
                {'t': t('Стартовая зона', 'Starting zone', 'Стартова зона'),
                 'd': t('Задания зоны своей расы до 10 уровня. На 10 уровне открываются таланты.',
                        'Quests of your race’s zone up to level 10. Talents unlock at level 10.',
                        'Завдання зони своєї раси до 10 рівня. На 10 рівні відкриваються таланти.')},
                {'t': t('Кулинария', 'Cooking', 'Кулінарія'),
                 'd': t('Выучите её сразу: готовая еда даёт +5% опыта за врагов, а костёр по Кулинарии становится лагерем.',
                        'Learn it right away: cooked food gives +5% experience from enemies, and a Cooking campfire becomes a camp.',
                        'Вивчіть її одразу: готова їжа дає +5% досвіду за ворогів, а вогнище з Кулінарії стає табором.')},
                {'t': t('Две профессии', 'Two professions', 'Дві професії'),
                 'd': t('Сбор даёт деньги и кормит ремесло. Пары под ваш класс — в гайде по профессиям.',
                        'Gathering brings in money and feeds a craft. Pairs for your class are in the professions guide.',
                        'Збирання дає гроші й годує ремесло. Пари під ваш клас — у гайді з професій.')},
                {'t': t('Cooldown Manager', 'Cooldown Manager', 'Cooldown Manager'),
                 'd': t('Встроенная панель кулдаунов и баффов, по умолчанию выключена: Options → Gameplay Enhancement. {beta}',
                        'A built-in cooldown and buff panel, off by default: Options → Gameplay Enhancement. {beta}',
                        'Вбудована панель кулдаунів і баффів, за замовчуванням вимкнена: Options → Gameplay Enhancement. {beta}')},
                {'t': t('Папка аддонов', 'Addon folder', 'Тека аддонів'),
                 'd': t('Папку для релиза Blizzard не называла. Откройте её через шестерёнку у кнопки «Играть» в Battle.net → Show in Explorer: аддоны лежат в Interface\\AddOns.',
                        'Blizzard has not named the release folder. Open it via the gear next to the Play button in Battle.net → Show in Explorer: addons go in Interface\\AddOns.',
                        'Теку для релізу Blizzard не назвала. Відкрийте її через шестірню біля кнопки «Грати» в Battle.net → Show in Explorer: аддони лежать в Interface\\AddOns.')},
            ]),
            ('table', {'head': [t('Страница', 'Page', 'Сторінка'), t('Зачем', 'What for', 'Навіщо')], 'rows': [
                [(t('Чек-лист «День 1»', 'Day 1 checklist', 'Чек-лист «День 1»'), 'guides/launch-checklist/#hours'),
                 t('Те же первые часы с отметками, которые сохраняются в браузере.', 'The same first hours with ticks that are saved in your browser.', 'Ті самі перші години з позначками, які зберігаються в браузері.')],
            ]}),
        ]},
        {'id': 'expect', 'title': t('Чего ждать', 'What to expect', 'Чого чекати'), 'blocks': [
            ('table', {'head': [t('Что', 'What', 'Що'), t('Что известно', 'What is known', 'Що відомо')], 'rows': [
                [t('Очередь на вход', 'Login queue', 'Черга на вхід'),
                 t('Blizzard не называла ни вместимость, ни меры против очередей. В бете очередь доходила до часа и дольше. {beta}',
                   'Blizzard has named neither the capacity nor any measures against queues. In the beta the queue ran to an hour and longer. {beta}',
                   'Blizzard не називала ні місткість, ні заходи проти черг. У беті черга сягала години й довше. {beta}')],
                [t('Отключения', 'Disconnects', 'Відключення'),
                 t('В бете многих отключало сразу после очереди и ставило в конец новой. {beta}',
                   'In the beta many players were disconnected right after the queue and sent to the back of a new one. {beta}',
                   'У беті багатьох відключало одразу після черги й ставило в кінець нової. {beta}')],
                [t('Слои', 'Layering', 'Шари'),
                 t('Blizzard: слои останутся, полностью их не уберут. До старта чинят два случая: игроков разводит по разным слоям после загрузки на корабле или дирижабле, а большие группы — при входе в столицу и выходе из неё.',
                   'Blizzard: layering stays and will not go away completely. Before launch they are fixing two cases: players split into different layers after the loading screen on a boat or zeppelin, and large groups split when entering or leaving a capital.',
                   'Blizzard: шари залишаться, повністю їх не приберуть. До старту виправляють два випадки: гравців розводить по різних шарах після завантаження на кораблі чи дирижаблі, а великі групи — під час входу в столицю й виходу з неї.')],
                [t('Слои в бете', 'Layering in the beta', 'Шари в беті'),
                 t('На границах зон игроки пропадали из вида, группы раскидывало. {beta}',
                   'Players vanished from sight at zone borders and groups were split. {beta}',
                   'На межах зон гравці зникали з поля зору, групи розкидало. {beta}')],
            ]}),
            ('tip', t('Что делать в очереди и при высоком пинге — в советнике «Пинг и очередь» на странице инструментов.',
                      'What to do in the queue and with high ping is in the Ping and queue advisor on the tools page.',
                      'Що робити в черзі та з високим пінгом — у порадникові «Пінг і черга» на сторінці інструментів.')),
        ]},
        {'id': 'status', 'title': t('Где смотреть статус', 'Where to check status', 'Де дивитися статус'), 'blocks': [
            ('text', [t('Только официальные каналы Blizzard. Отдельной страницы статуса Forever Blizzard не объявляла.',
                        'Official Blizzard channels only. Blizzard has not announced a separate status page for Forever.',
                        'Лише офіційні канали Blizzard. Окремої сторінки статусу Forever Blizzard не оголошувала.')]),
            ('table', {'head': [t('Канал', 'Channel', 'Канал'), t('Что там', 'What is there', 'Що там')], 'rows': [
                [('@BlizzardCS', 'https://x.com/BlizzardCS'),
                 t('Поддержка Blizzard в X для Америки: сбои, работы на серверах, известные проблемы.',
                   'Blizzard support on X for the Americas: outages, server maintenance, known issues.',
                   'Підтримка Blizzard в X для Америки: збої, роботи на серверах, відомі проблеми.')],
                [('@BlizzardCSEU_EN', 'https://x.com/BlizzardCSEU_EN'),
                 t('Поддержка Blizzard в X для Европы, на английском.',
                   'Blizzard support on X for Europe, in English.',
                   'Підтримка Blizzard в X для Європи, англійською.')],
                [(t('Форум WoW: Forever, Европа', 'WoW: Forever forum, Europe', 'Форум WoW: Forever, Європа'), 'https://eu.forums.blizzard.com/en/wow/c/wow-forever/359'),
                 t('Официальный раздел Forever: объявления и ответы разработчиков.',
                   'The official Forever section: announcements and developer replies.',
                   'Офіційний розділ Forever: оголошення та відповіді розробників.')],
                [(t('Форум WoW: Forever, Америка', 'WoW: Forever forum, Americas', 'Форум WoW: Forever, Америка'), 'https://us.forums.blizzard.com/en/wow/c/wow-forever/346'),
                 t('То же для Америки и Океании.', 'The same for the Americas and Oceania.', 'Те саме для Америки та Океанії.')],
                [(t('Статус реалмов WoW', 'WoW realm status', 'Статус реалмів WoW'), 'https://worldofwarcraft.blizzard.com/en-gb/worldsoul/eu/server-status'),
                 t('Официальная страница статуса. На 26.10 Forever в ней нет: в Forever режимы вместо реалмов. Появится ли — уточним на старте.',
                   'The official status page. As of 26.10 Forever is not on it: Forever has modes instead of realms. Whether it appears, we will confirm at launch.',
                   'Офіційна сторінка статусу. На 26.10 Forever у ній немає: у Forever режими замість реалмів. Чи з’явиться — уточнимо на старті.')],
            ]}),
        ]},
        {'id': 'wait', 'title': t('Пока стоите в очереди', 'While you are in the queue', 'Поки стоїте в черзі'), 'blocks': [
            ('steps', [
                {'t': t('Не выходите', 'Do not leave', 'Не виходьте'),
                 'd': t('Повторный вход ставит в конец очереди. {beta}',
                        'Logging in again puts you at the back of the queue. {beta}',
                        'Повторний вхід ставить у кінець черги. {beta}')},
                {'t': t('Соберите персонажа', 'Build your character', 'Зберіть персонажа'),
                 'd': t('Класс, спек и раса в «Мой персонаж»: главная, таланты и чек-лист подстроятся под него, а на 10 уровне не придётся думать над первым очком.',
                        'Class, spec and race in My character: the home page, talents and checklist adapt to it, and at level 10 your first point is already planned.',
                        'Клас, спек і раса в «Мій персонаж»: головна, таланти й чек-лист підлаштуються під нього, а на 10 рівні перше очко вже сплановане.')},
                {'t': t('В игре', 'In game', 'У грі'),
                 'd': t('Откройте «В игре» на телефоне: маршрут прокачки вашей фракции, этапы и таймеры будут под рукой.',
                        'Open In game on your phone: the leveling route for your faction, milestones and timers stay at hand.',
                        'Відкрийте «У грі» на телефоні: маршрут прокачування вашої фракції, етапи й таймери будуть під рукою.')},
                {'t': t('Группа', 'Group', 'Група'),
                 'd': t('Соберите состав в конструкторе, отправьте ссылку друзьям и скопируйте текст для LFG заранее.',
                        'Build the party in the group builder, send the link to friends and copy the LFG text in advance.',
                        'Зберіть склад у конструкторі, надішліть посилання друзям і скопіюйте текст для LFG заздалегідь.')},
                {'t': t('Если выбило', 'If you get disconnected', 'Якщо вибило'),
                 'd': t('Сначала загляните в @BlizzardCS или @BlizzardCSEU_EN: об общем сбое Blizzard пишет там.',
                        'Check @BlizzardCS or @BlizzardCSEU_EN first: Blizzard posts outages for everyone there.',
                        'Спершу загляньте в @BlizzardCS або @BlizzardCSEU_EN: про загальний збій Blizzard пише там.')},
            ]),
            ('table', {'head': [t('Страница', 'Page', 'Сторінка'), t('Зачем', 'What for', 'Навіщо')], 'rows': [
                [(t('Мой персонаж', 'My character', 'Мій персонаж'), 'character/'),
                 t('Класс, спек и раса: главная, таланты и чек-лист подстраиваются под персонажа.', 'Class, spec and race: the home page, talents and checklist adapt to your character.', 'Клас, спек і раса: головна, таланти й чек-лист підлаштовуються під персонажа.')],
                [(t('В игре', 'In game', 'У грі'), 'play/'),
                 t('Второй экран во время игры: маршрут, этапы, таймеры, радио.', 'A second screen while you play: route, milestones, timers, radio.', 'Другий екран під час гри: маршрут, етапи, таймери, радіо.')],
                [(t('Чек-лист «День 1»', 'Day 1 checklist', 'Чек-лист «День 1»'), 'guides/launch-checklist/'),
                 t('Что сделать до старта, в первые часы и в первый вечер.', 'What to do before launch, in the first hours and on the first evening.', 'Що зробити до старту, у перші години та першого вечора.')],
                [(t('Пинг и очередь', 'Ping and queue', 'Пінг і черга'), 'tools/#ping'),
                 t('Ваш регион, что делать при высоком пинге и как не потерять место в очереди.', 'Your region, what to do about high ping and how not to lose your place in the queue.', 'Ваш регіон, що робити з високим пінгом і як не втратити місце в черзі.')],
                [(t('Конструктор группы', 'Group builder', 'Конструктор групи'), 'tools/#raid'),
                 t('Состав для друзей по ссылке.', 'A party to share with friends by link.', 'Склад для друзів за посиланням.')],
                [(t('Текст для LFG', 'LFG text', 'Текст для LFG'), 'tools/#lfg'),
                 t('Готовый текст для поиска группы в игре и короткая ссылка на состав.', 'A ready text for the in-game group finder list and a short link to the party.', 'Готовий текст для пошуку групи в грі та коротке посилання на склад.')],
                [(t('Подборщик расы и класса', 'Race and class picker', 'Підбір раси й класу'), 'tools/#picker'),
                 t('Все сочетания расы и класса в Forever и что умеет каждое.', 'Every race and class combination in Forever and what each can do.', 'Усі поєднання раси й класу у Forever і що вміє кожне.')],
                [(t('Тир-лист', 'Tier list', 'Тір-лист'), 'guides/tier-list/'),
                 t('Если класс ещё не выбран: классы и спеки по данным беты.', 'If you have not picked a class yet: classes and specs based on beta data.', 'Якщо клас ще не обрано: класи й спеціалізації за даними бети.')],
            ]}),
        ]},
        {'id': 'faq', 'title': t('Вопросы', 'Questions', 'Питання'), 'blocks': [
            ('faq', [
                {'id': 'when', 'q': t('Во сколько выходит WoW Forever?', 'What time does WoW Forever launch?', 'О котрій виходить WoW Forever?'),
                 'a': [t('04.11.2026 в 15:00 PST, это 23:00 UTC. В Киеве — 05.11 в 01:00, в Берлине и Варшаве — 05.11 в 00:00, в Нью-Йорке — 04.11 в 18:00.',
                         '04.11.2026 at 15:00 PST, which is 23:00 UTC. That is 23:00 on 04.11 in London, 00:00 on 05.11 in Berlin and Paris, and 18:00 on 04.11 in New York.',
                         '04.11.2026 о 15:00 PST, це 23:00 UTC. У Києві — 05.11 о 01:00, у Варшаві та Берліні — 05.11 о 00:00, у Нью-Йорку — 04.11 о 18:00.')]},
                {'id': 'regions', 'q': t('Европа и Америка стартуют в разное время?', 'Do Europe and the Americas launch at different times?', 'Європа й Америка стартують у різний час?'),
                 'a': [t('Нет. Blizzard открывает все регионы в одну минуту, разница только в местном времени.',
                         'No. Blizzard opens every region at the same minute; only the local time differs.',
                         'Ні. Blizzard відкриває всі регіони в одну хвилину, різниця лише в місцевому часі.')]},
                {'id': 'pst', 'q': t('Это PST или PDT?', 'Is it PST or PDT?', 'Це PST чи PDT?'),
                 'a': [t('PST, UTC-8: летнее время в США кончается 01.11. В одной английской статье Blizzard стоит PDT, но французская статья Blizzard называет полночь по Парижу, а это тоже 23:00 UTC.',
                         'PST, UTC-8: US daylight time ends on 01.11. One English Blizzard article says PDT, but the French Blizzard article gives midnight Paris time, which is also 23:00 UTC.',
                         'PST, UTC-8: літній час у США закінчується 01.11. В одній англійській статті Blizzard стоїть PDT, але французька стаття Blizzard називає північ за Парижем, а це теж 23:00 UTC.')]},
                {'id': 'early', 'q': t('Можно ли играть до старта?', 'Can I play before launch?', 'Чи можна грати до старту?'),
                 'a': [t('Нет. Бета закончилась 23.10. До 03.11 владельцы наборов могут только создать до трёх персонажей и занять имена.',
                         'No. The beta ended on 23.10. Until 03.11 pack owners can only create up to three characters and claim names.',
                         'Ні. Бета закінчилася 23.10. До 03.11 власники наборів можуть лише створити до трьох персонажів і зайняти імена.')]},
            ]),
        ]},
    ],
})

# ---------- server-status: where to check, the login queue, layering, maintenance (no invented numbers) ----------

_ld = next(g for g in GUIDES if g['slug'] == 'launch-day')
_ld_status = next(s for s in _ld['sections'] if s['id'] == 'status')
_ld_expect = next(s for s in _ld['sections'] if s['id'] == 'expect')
_ld_wait = next(s for s in _ld['sections'] if s['id'] == 'wait')
_tbl = lambda sec: next(b for k, b in sec['blocks'] if k == 'table')
_row = lambda sec, ru: next(r for r in _tbl(sec)['rows'] if (r[0][0] if isinstance(r[0], tuple) else r[0])['ru'] == ru)
_ST_HEAD = _tbl(_ld_expect)['head']

GUIDES.append({
    'slug': 'server-status', 'hub': False, 'art': 'hero_night', 'hero': 'hero_night', 'tile_art': 'hero_night', 'og': 'guides',
    'title': t('Статус серверов и очередь на вход', 'Server Status and Login Queue', 'Статус серверів і черга на вхід'),
    'crumb': t('Статус серверов', 'Server status', 'Статус серверів'),
    'lead': t('Где смотреть, работают ли серверы WoW Forever, как устроены очередь на вход и слои и что Blizzard об этом сообщила.',
              'Where to check whether WoW Forever servers are up, how the login queue and layers work and what Blizzard has said about them.',
              'Де дивитися, чи працюють сервери WoW Forever, як улаштовані черга на вхід і шари та що Blizzard про це повідомила.'),
    'tile': t('Статус, очередь на вход, слои, техработы', 'Status, login queue, layers, maintenance', 'Статус, черга на вхід, шари, техроботи'),
    'pills': [t('Статус — только каналы Blizzard', 'Status: Blizzard channels only', 'Статус — лише канали Blizzard'),
              t('Время очереди не объявлено', 'No queue times announced', 'Час черги не оголошено')],
    'sources': [s for s in _ld['sources'] if not any(x in s[1] for x in ('gov.bc.ca', 'fr-fr', '24303866', '24302070'))],
    'sections': [
        dict(_ld_status, title=t('Статус серверов', 'Server status', 'Статус серверів')),
        {'id': 'queue', 'title': t('Очередь на вход и её время', 'Login queue and queue times', 'Черга на вхід і її час'), 'blocks': [
            ('text', [t('Очередь на вход появляется, когда зайти пытается больше игроков, чем сервер принимает сразу. Blizzard не называла ни вместимость серверов Forever, ни ожидаемое время, поэтому времени очереди мы не публикуем.',
                        'A login queue appears when more players try to enter than the server accepts at once. Blizzard has not named the capacity of the Forever servers or the expected wait, so we publish no queue times.',
                        'Черга на вхід з’являється, коли зайти намагається більше гравців, ніж сервер приймає одразу. Blizzard не називала ні місткість серверів Forever, ні очікуваний час, тому часу черги ми не публікуємо.')]),
            ('table', {'head': _ST_HEAD, 'rows': [_row(_ld_expect, 'Очередь на вход'), _row(_ld_expect, 'Отключения')]}),
            ('tip', t('Не выходите из очереди: повторный вход ставит в её конец. {beta}',
                      'Do not leave the queue: logging in again puts you at the back. {beta}',
                      'Не виходьте з черги: повторний вхід ставить у її кінець. {beta}')),
        ]},
        {'id': 'layers', 'title': t('Слои', 'Layering', 'Шари'), 'blocks': [
            ('text', [t('Слои делят один сервер на несколько копий мира, и игроки из разных слоёв друг друга не видят. Blizzard заявила, что слои в Forever останутся и полностью их не уберут.',
                        'Layering splits one server into several copies of the world, and players on different layers do not see each other. Blizzard has said layering stays in Forever and will not go away completely.',
                        'Шари ділять один сервер на кілька копій світу, і гравці з різних шарів не бачать одне одного. Blizzard заявила, що шари у Forever залишаться й повністю їх не приберуть.')]),
            ('table', {'head': _ST_HEAD, 'rows': [_row(_ld_expect, 'Слои'), _row(_ld_expect, 'Слои в бете')]}),
        ]},
        {'id': 'maintenance', 'title': t('Техработы и сбои', 'Maintenance and outages', 'Техроботи та збої'), 'blocks': [
            ('text', [t('Расписание техработ Forever Blizzard не публиковала. О плановых работах и сбоях сообщают каналы выше. Если не можете зайти только вы, сначала проверьте соединение и пинг.',
                        'Blizzard has not published a maintenance schedule for Forever. Planned work and outages are posted in the channels above. If only you cannot log in, check your connection and ping first.',
                        'Розклад техробіт Forever Blizzard не публікувала. Про планові роботи та збої повідомляють канали вище. Якщо не можете зайти лише ви, спершу перевірте з’єднання й пінг.')]),
        ]},
        {'id': 'related', 'title': t('Смотрите также', 'See also', 'Дивіться також'), 'blocks': [
            ('table', {'head': _tbl(_ld_wait)['head'], 'rows': [
                [(_ld['title'], 'guides/launch-day/'), _ld['tile']],
                _row(_ld_wait, 'Пинг и очередь'),
                _row(_ld_wait, 'Чек-лист «День 1»'),
            ]}),
        ]},
    ],
})

# the Launch day page points to this one
_ss = next(g for g in GUIDES if g['slug'] == 'server-status')
_tbl(_ld_wait)['rows'].append([(_ss['title'], 'guides/server-status/'), _ss['tile']])
# and its status section ends with the same link (a new list: server-status shares the old one)
_ld_status['blocks'] = _ld_status['blocks'] + [('table', {'head': _tbl(_ld_wait)['head'], 'rows': [
    [(_ss['title'], 'guides/server-status/'),
     t('Очередь, слои и техработы подробно: что известно, а что нет.', 'The queue, layers and maintenance in full: what is known and what is not.', 'Черга, шари й техроботи докладно: що відомо, а що ні.')]]})]


# ---------- Резерв имён 27.10 – 03.11: только факты статьи Blizzard (NR_URL) и её справки об именах; время по Киеву ----------
# Киев после 25.10 = UTC+2: 18:00 CET = 19:00, 13:00 PDT = 22:00, 07:00 KST (28.10) = 00:00, 07:00 Тайвань (UTC+8) = 01:00.
# Океания и час конца окна в статье не указаны — так и пишем.

NR_HOW = t('Как занять имя', 'How to claim a name', 'Як зайняти ім’я')
GUIDES.append({
    'slug': 'name-reservation', 'art': 'hero_dusk', 'hero': 'hero_dusk', 'og': 'guides',
    'title': t('Как зарезервировать имя в WoW Forever', 'How to Reserve Your Name in WoW Forever', 'Як зарезервувати ім’я у WoW Forever'),
    'crumb': t('Резерв имён', 'Name reservation', 'Резерв імен'),
    'lead': t('Ранний резерв имён идёт с 27.10 по 03.11. Кому он доступен, когда стартует по Киеву, как занять имя за пять шагов и что делать, если не вышло.',
              'Early name reservation runs from 27.10 to 03.11. Who can use it, when it starts in Kyiv time, how to claim a name in five steps and what to do if it fails.',
              'Ранній резерв імен триває з 27.10 по 03.11. Кому він доступний, коли стартує за Києвом, як зайняти ім’я за п’ять кроків і що робити, якщо не вийшло.'),
    'tile': t('Сроки, условия, шаги и правила имён', 'Dates, conditions, steps and name rules', 'Строки, умови, кроки й правила імен'),
    'pills': ['27.10 – 03.11', t('До трёх персонажей', 'Up to three characters', 'До трьох персонажів'),
              t('Только с набором', 'Pack owners only', 'Лише з набором')],
    'sources': [
        ('Blizzard: Claim Your World of Warcraft: Forever Character Names', NR_URL),
        ('Blizzard: Create a Name of Your Own in WoW: Forever', 'https://worldofwarcraft.blizzard.com/news/24304161'),
        ('Battle.net: download', 'https://download.battle.net/desktop'),
        (t('Blizzard: старт и коды Invite-A-Friend', 'Blizzard: launch and Invite-A-Friend codes', 'Blizzard: старт і коди Invite-A-Friend'),
         'https://news.blizzard.com/en-us/article/24301508'),
        ('Wowhead: Name Reservations for WoW: Forever Now Live in EU, NA', 'https://www.wowhead.com/forever/news/name-reservations-for-wow-forever-delayed-383608'),
    ],
    'sections': [
        {'id': 'when', 'title': t('Когда и для кого', 'When and for whom', 'Коли й для кого'), 'blocks': [
            ('text', [t('Резерв открыт с 27.10 по 03.11 для всех, кто оформил предзаказ Skyborne Heroic Pack, Skyborne Epic Pack или Warcraft Forever Collection — в виде Digital Upgrade или Collector’s Edition. Он работает только на том аккаунте WoW, для которого куплен набор.',
                        'The reservation is open from 27.10 to 03.11 to anyone who pre-purchased the Skyborne Heroic Pack, Skyborne Epic Pack or Warcraft Forever Collection, as a Digital Upgrade or a Collector’s Edition. It works only on the WoW account the pack was bought for.',
                        'Резерв відкрито з 27.10 по 03.11 для всіх, хто оформив передзамовлення Skyborne Heroic Pack, Skyborne Epic Pack або Warcraft Forever Collection — як Digital Upgrade або Collector’s Edition. Він працює лише на тому акаунті WoW, для якого куплено набір.'),
                      t('Это не ранний доступ: сейчас вы только создаёте персонажей и занимаете имена. Играть можно со старта — 05.11 в 01:00 по Киеву.',
                        'This is not early access: for now you only create characters and claim names. You can play from launch, 05.11 at 01:00 Kyiv time.',
                        'Це не ранній доступ: зараз ви лише створюєте персонажів і займаєте імена. Грати можна від старту — 05.11 о 01:00 за Києвом.')]),
            ('table', {'head': [t('Регион', 'Region', 'Регіон'), t('Старт по Киеву', 'Start, Kyiv time', 'Старт за Києвом')], 'rows': [
                [t('Европа', 'Europe', 'Європа'), '27.10, 19:00'],
                [t('Америка', 'Americas', 'Америка'), '27.10, 22:00'],
                [t('Корея', 'Korea', 'Корея'), '28.10, 00:00'],
                [t('Тайвань', 'Taiwan', 'Тайвань'), '28.10, 01:00'],
                [t('Океания', 'Oceania', 'Океанія'), t('Время Blizzard не называла', 'Not given by Blizzard', 'Час Blizzard не називала')],
                [t('Конец резерва', 'Reservation ends', 'Кінець резерву'), t('03.11, время не указано', '03.11, time not given', '03.11, час не вказано')],
            ]}),
        ]},
        {'id': 'steps', 'title': NR_HOW, 'blocks': [
            ('steps', [
                {'t': t('Обновите драйверы', 'Update your drivers', 'Оновіть драйвери'),
                 'd': t('Blizzard советует начать со свежих драйверов видеокарты.', 'Blizzard recommends starting with up-to-date graphics drivers.',
                        'Blizzard радить почати зі свіжих драйверів відеокарти.')},
                {'t': t('Установите Battle.net', 'Install Battle.net', 'Встановіть Battle.net'),
                 'd': t('Скачайте приложение Battle.net на download.battle.net, откройте его и дайте обновиться.',
                        'Download the Battle.net app from download.battle.net, open it and let it update.',
                        'Завантажте застосунок Battle.net з download.battle.net, відкрийте його й дайте оновитися.')},
                {'t': t('Установите Forever', 'Install Forever', 'Встановіть Forever'),
                 'd': t('World of Warcraft в списке игр → меню Game Version → World of Warcraft: Forever → Install.',
                        'World of Warcraft in the game list → the Game Version menu → World of Warcraft: Forever → Install.',
                        'World of Warcraft у списку ігор → меню Game Version → World of Warcraft: Forever → Install.')},
                {'t': t('Выберите режим', 'Choose a mode', 'Оберіть режим'),
                 'd': t('Нажмите Play и выберите режим. Договоритесь с друзьями заранее: группа собирается только внутри одного режима.',
                        'Press Play and choose a mode. Agree with your friends first: groups form only within one mode.',
                        'Натисніть Play й оберіть режим. Домовтеся з друзями заздалегідь: група збирається лише в межах одного режиму.')},
                {'t': t('Создайте персонажей', 'Create your characters', 'Створіть персонажів'),
                 'd': t('До трёх персонажей с нужными именами. Созданный персонаж закрепляет имя за вами.',
                        'Up to three characters with the names you want. A created character keeps the name for you.',
                        'До трьох персонажів із потрібними іменами. Створений персонаж закріплює ім’я за вами.')},
            ]),
        ]},
        {'id': 'rules', 'title': t('Правила имён', 'Name rules', 'Правила імен'), 'blocks': [
            ('steps', [
                {'t': t('Три персонажа на все режимы', 'Three characters across all modes', 'Три персонажі на всі режими'),
                 'd': t('Лимит общий: два персонажа в PvP оставляют место только для одного в Normal или Role-Play. Лимит действует только на время раннего резерва.',
                        'The limit is shared: two PvP characters leave room for just one in Normal or Role-Play. The limit applies only to early name reservation.',
                        'Ліміт спільний: два персонажі в PvP залишають місце лише для одного в Normal або Role-Play. Ліміт діє лише на час раннього резерву.')},
                {'t': t('Уникально полное имя', 'The full name is unique', 'Унікальне повне ім’я'),
                 'd': t('У персонажа имя и фамилия. Сочетание должно быть свободно во всём регионе, а не на одном реалме. Имя может повторяться, если фамилия другая, а одну фамилию можно дать нескольким своим персонажам.',
                        'A character has a first name and a surname. The pair must be free across the whole region, not just one realm. A first name can repeat with a different surname, and you can give one surname to several of your characters.',
                        'Персонаж має ім’я та прізвище. Поєднання має бути вільним у всьому регіоні, а не на одному реалмі. Ім’я може повторюватися, якщо прізвище інше, а одне прізвище можна дати кільком своїм персонажам.')},
                {'t': t('Имя проверяют целиком', 'The name is checked as a whole', 'Ім’я перевіряють цілком'),
                 'd': t('Под запретом могут оказаться имена против правил поведения, похожие на Blizzard или команду WoW и с повторами символов. Запретное слово, разбитое на имя и фамилию, тоже не пройдёт.',
                        'Names may be blocked if they break the code of conduct, pose as Blizzard or the WoW team, or repeat characters. A banned word split between first name and surname will not pass either.',
                        'Під забороною можуть опинитися імена, що порушують правила поведінки, схожі на Blizzard чи команду WoW або з повторами символів. Заборонене слово, розбите на ім’я та прізвище, теж не пройде.')},
                {'t': t('Кто первый, тот и занял', 'First come, first served', 'Хто перший, той і зайняв'),
                 'd': t('Blizzard не гарантирует нужное имя. Редкое лучше занять сразу и держать запасную фамилию.',
                        'Blizzard does not guarantee any name. Claim a rare one right away and keep a backup surname.',
                        'Blizzard не гарантує потрібне ім’я. Рідкісне краще зайняти одразу й тримати запасне прізвище.')},
            ]),
        ]},
        {'id': 'fail', 'title': t('Если не получилось', 'If it does not work', 'Якщо не вийшло'), 'blocks': [
            ('table', {'head': [t('Что случилось', 'What happened', 'Що сталося'), t('Что делать', 'What to do', 'Що робити')], 'rows': [
                [t('Имя занято', 'The name is taken', 'Ім’я зайняте'),
                 t('Смените фамилию: уникальным должно быть только сочетание. Или возьмите запасной вариант.',
                   'Change the surname: only the pair has to be unique. Or use a backup.',
                   'Змініть прізвище: унікальним має бути лише поєднання. Або візьміть запасний варіант.')],
                [t('Имя не принимают', 'The name is rejected', 'Ім’я не приймають'),
                 t('Проверьте его по правилам выше: имя и фамилию оценивают вместе.',
                   'Check it against the rules above: the first name and surname are judged together.',
                   'Перевірте його за правилами вище: ім’я та прізвище оцінюють разом.')],
                [t('Нет доступа к резерву', 'No access to the reservation', 'Немає доступу до резерву'),
                 t('Убедитесь, что вошли в тот аккаунт WoW, для которого купили набор, и что в Battle.net выбран World of Warcraft: Forever. Без набора резерва нет: имя займёте на старте.',
                   'Make sure you are on the WoW account the pack was bought for and that World of Warcraft: Forever is selected in Battle.net. Without a pack there is no reservation: you claim your name at launch.',
                   'Переконайтеся, що ви в тому акаунті WoW, для якого купили набір, і що в Battle.net обрано World of Warcraft: Forever. Без набору резерву немає: ім’я займете на старті.')],
                [t('Лимит исчерпан', 'Limit reached', 'Ліміт вичерпано'),
                 t('Три персонажа на все режимы — это всё до 03.11. Остальные имена занимайте на старте.',
                   'Three characters across all modes is all you get until 03.11. Claim other names at launch.',
                   'Три персонажі на всі режими — це все до 03.11. Інші імена займайте на старті.')],
                [t('Резерв не открывается', 'The reservation does not open', 'Резерв не відкривається'),
                 t('27.10 старт в Европе задерживался из-за технических проблем, в тот же день резерв заработал. При новом сбое смотрите новости Blizzard и лаунчер Battle.net.',
                   'On 27.10 the start in Europe was delayed by technical issues and went live later that day. If it happens again, check Blizzard news and the Battle.net launcher.',
                   '27.10 старт у Європі затримувався через технічні проблеми, того ж дня резерв запрацював. Якщо збій повториться, дивіться новини Blizzard і лаунчер Battle.net.')],
            ]}),
            ('raw', t(f'<p><a class="more-l" href="{NR_URL}" target="_blank" rel="noopener">Статья Blizzard о резерве имён, на английском</a></p>',
                      f'<p><a class="more-l" href="{NR_URL}" target="_blank" rel="noopener">The Blizzard article on name reservation</a></p>',
                      f'<p><a class="more-l" href="{NR_URL}" target="_blank" rel="noopener">Стаття Blizzard про резерв імен, англійською</a></p>')),
        ]},
    ],
})


GUIDES.sort(key=lambda g: ORDER.index(g['slug']))


# ---------- glossary: короткий словарь терминов; термин поясняем там, где он встречается, и ссылаем сюда ----------

GUIDES.append({
    'slug': 'glossary', 'art': 'hero_guides', 'hero': 'hero_guides', 'og': 'guides',
    'title': t('Словарь терминов', 'Glossary', 'Словник термінів'),
    'lead': t('Что значат спек, билд, тир-лист, ротация, BiS, Legacy и перки: короткие определения, чтобы читать остальные гайды с первого раза.',
              'What spec, build, tier list, rotation, BiS, Legacy and perks mean: short definitions so you can read the other guides on the first pass.',
              'Що означають спек, білд, тир-лист, ротація, BiS, Legacy і перки: короткі визначення, щоб читати решту гайдів із першого разу.'),
    'tile': t('Спек, билд, тир-лист, BiS, Legacy и перки', 'Spec, build, tier list, BiS, Legacy and perks', 'Спек, білд, тир-лист, BiS, Legacy і перки'),
    'pills': [t('Игра и роли', 'Game and roles', 'Гра й ролі'), t('Билды', 'Builds', 'Білди'), t('Механики Forever', 'Forever mechanics', 'Механіки Forever')],
    'sources': [
        (t('Blizzard: система Legacy', 'Blizzard: Legacy system', 'Blizzard: система Legacy'), 'https://news.blizzard.com/en-gb/article/24307383'),
        (t('Warcraft Tavern: лагерь', 'Warcraft Tavern: camping', 'Warcraft Tavern: табір'), 'https://www.warcrafttavern.com/forever/guides/camping/'),
    ],
    'sections': [
        {'id': 'game', 'title': t('Игра, билд и силы классов', 'Game, builds and class strength', 'Гра, білд і сили класів'), 'blocks': [
            ('table', {'head': [t('Термин', 'Term', 'Термін'), t('Что это', 'What it means', 'Що це')], 'rows': [
                [t('Спек', 'Spec', 'Спек'), t('Ветка талантов, которую вы развиваете: у Мага это Тайная магия, Огонь или Лёд. От спека зависит роль в группе и то, какие умения вы нажимаете.', 'The talent tree you build up: for a Mage that is Arcane, Fire or Frost. The spec sets your role in a group and which abilities you press.', 'Гілка талантів, яку ви розвиваєте: у Мага це Тайна магія, Вогонь або Лід. Від спеку залежить роль у групі й те, які вміння ви натискаєте.')],
                [t('Билд', 'Build', 'Білд'), t('Набор талантов и порядок, в котором вы их берёте. Билд привязан к спеку: на странице класса он расписан по уровням.', 'A set of talents and the order you take them in. A build belongs to a spec; each class page lists it level by level.', 'Набір талантів і порядок, у якому ви їх берете. Білд прив’язаний до спеку: на сторінці класу він розписаний за рівнями.')],
                [t('Таланты', 'Talents', 'Таланти'), t('Очки, которые вы получаете с уровнем и вкладываете в дерево класса. Дерево открывает новые умения и усиливает старые.', 'Points you earn with levels and put into your class tree. The tree unlocks new abilities and strengthens old ones.', 'Очки, які ви отримуєте з рівнем і вкладаєте в дерево класу. Дерево відкриває нові вміння й підсилює старі.')],
                [t('Тир-лист', 'Tier list', 'Тір-лист'), t('Рейтинг классов и спеков по силе: S сильнее всех, дальше A, B, C. Это сравнение для выбора, а не приговор: играть можно любым.', 'A ranking of classes and specs by strength: S is strongest, then A, B, C. It is a guide for choosing, not a verdict: any spec is playable.', 'Рейтинг класів і спеків за силою: S найсильніший, далі A, B, C. Це порівняння для вибору, а не вирок: грати можна будь-яким.')],
                [t('PvE', 'PvE', 'PvE'), t('Игра против монстров: квесты, подземелья, рейды.', 'Playing against monsters: quests, dungeons, raids.', 'Гра проти монстрів: квести, підземелля, рейди.')],
                [t('PvP', 'PvP', 'PvP'), t('Игра против других игроков: поля боя и бои в открытом мире.', 'Playing against other players: battlegrounds and open-world fights.', 'Гра проти інших гравців: поля бою та бої у відкритому світі.')],
                [t('Прокачка', 'Leveling', 'Прокачування'), t('Путь от 1 до 60 уровня. После него начинается игра на максимальном уровне: подземелья, рейды, PvP.', 'The road from level 1 to 60. After it comes max-level play: dungeons, raids, PvP.', 'Шлях від 1 до 60 рівня. Після нього починається гра на максимальному рівні: підземелля, рейди, PvP.')],
                [t('Профессия', 'Profession', 'Професія'), t('Ремесло или сбор: Кузнечное дело, Алхимия, Травничество и другие. Даёт предметы, золото и баффы лагеря.', 'A craft or gathering skill: Blacksmithing, Alchemy, Herbalism and others. Gives items, gold and camp buffs.', 'Ремесло або збір: Ковальство, Алхімія, Травництво та інші. Дає предмети, золото й баффи табору.')],
                [t('Тренер', 'Trainer', 'Тренер'), t('NPC в городе, у которого за золото учат новым умениям класса и профессии. Заходите к нему каждые несколько уровней.', 'An NPC in town who teaches new class and profession abilities for gold. Visit one every few levels.', 'NPC у місті, який за золото навчає нових умінь класу й професії. Заходьте до нього кожні кілька рівнів.')],
            ]}),
        ]},
        {'id': 'group', 'title': t('Группа и бой', 'Group and combat', 'Група й бій'), 'blocks': [
            ('table', {'head': [t('Термин', 'Term', 'Термін'), t('Что это', 'What it means', 'Що це')], 'rows': [
                [t('Танк', 'Tank', 'Танк'), t('Держит врагов на себе и принимает удар. Без него в подземелье не справиться.', 'Holds enemies’ attention and takes the hits. A dungeon is hard without one.', 'Тримає ворогів на собі й приймає удар. Без нього в підземеллі важко.')],
                [t('Лекарь', 'Healer', 'Лікар'), t('Лечит группу. Работает на мане, поэтому следит за её запасом.', 'Heals the group. Runs on mana, so keeps an eye on it.', 'Лікує групу. Працює на мані, тому стежить за її запасом.')],
                [t('Урон (ДД)', 'Damage (DPS)', 'Шкода (ДД)'), t('Бьёт врагов. Бывает в ближнем бою и на расстоянии.', 'Kills enemies. Melee or ranged.', 'Б’є ворогів. Буває в ближньому бою й на відстані.')],
                [t('Агро', 'Aggro', 'Агро'), t('Чья очередь получать удары. Монстр бьёт того, кто создал больше угрозы. Урон не должен обгонять танка.', 'Whose turn it is to get hit. A monster attacks whoever built the most threat. Damage dealers must not outrun the tank.', 'Чия черга отримувати удари. Монстр б’є того, хто створив більше загрози. Шкода не повинна випереджати танка.')],
                [t('Кайт', 'Kite', 'Кайт'), t('Отступать от врага, не давая ему себя догнать, и бить на ходу. Привычный приём Охотника и Мага.', 'Backing away from an enemy while keeping out of reach and still hitting it. A usual Hunter and Mage trick.', 'Відступати від ворога, не даючи себе наздогнати, і бити на ходу. Звичний прийом Мисливця й Мага.')],
                [t('Бафф и дебафф', 'Buff and debuff', 'Бафф і дебафф'), t('Бафф усиливает вас или союзника на время, дебафф ослабляет врага или вас.', 'A buff strengthens you or an ally for a while, a debuff weakens an enemy or you.', 'Бафф посилює вас або союзника на час, дебафф послаблює ворога чи вас.')],
                [t('LFG', 'LFG', 'LFG'), t('Looking for group: поиск группы. В чате или в списке пишут, куда и кого ищут.', 'Looking for group. People post in chat or in the finder what they want and who they need.', 'Looking for group: пошук групи. У чаті або в списку пишуть, куди й кого шукають.')],
            ]}),
        ]},
        {'id': 'build', 'title': t('Как играть спеком', 'How to play a spec', 'Як грати спеком'), 'blocks': [
            ('table', {'head': [t('Термин', 'Term', 'Термін'), t('Что это', 'What it means', 'Що це')], 'rows': [
                [t('Ротация', 'Rotation', 'Ротація'), t('Порядок, в котором вы нажимаете умения, чтобы наносить максимум урона. Простая ротация — это 3–4 кнопки по очереди.', 'The order you press abilities in to deal the most damage. A simple rotation is 3–4 buttons in turn.', 'Порядок, у якому ви натискаєте вміння, щоб завдавати максимум шкоди. Проста ротація — це 3–4 кнопки по черзі.')],
                [t('Приоритет', 'Priority', 'Пріоритет'), t('Список умений по важности: когда несколько готовы, нажимаете то, что выше в списке. Ротация без жёсткой очерёдности.', 'A list of abilities by importance: when several are ready, press the highest one. A rotation without a fixed order.', 'Список умінь за важливістю: коли кілька готові, натискаєте те, що вище в списку. Ротація без жорсткої черги.')],
                [t('BiS', 'BiS', 'BiS'), t('Best in slot: лучший предмет для ячейки. Список BiS показывает, за какой экипировкой идти в подземелья и рейды.', 'Best in slot: the strongest item for a gear slot. A BiS list shows which gear to chase in dungeons and raids.', 'Best in slot: найкращий предмет для комірки. Список BiS показує, за яким екіпіруванням іти в підземелля та рейди.')],
                [t('Статы', 'Stats', 'Стати'), t('Характеристики: сила, ловкость, интеллект, выносливость. Каждому классу нужны свои, и спек уточняет, какие важнее.', 'Strength, agility, intellect, stamina. Every class needs its own, and the spec decides which matter most.', 'Характеристики: сила, спритність, інтелект, витривалість. Кожному класу потрібні свої, а спек уточнює, які важливіші.')],
                [t('Кулдаун', 'Cooldown', 'Кулдаун'), t('Время, пока умение нельзя применить снова. Сильные умения копят для сложных боёв.', 'The wait before an ability can be used again. Strong abilities are saved for hard fights.', 'Час, поки вміння не можна застосувати знову. Сильні вміння бережуть для складних боїв.')],
            ]}),
        ]},
        {'id': 'forever', 'title': t('Что есть только в Forever', 'Only in Forever', 'Що є лише у Forever'), 'blocks': [
            ('text', [t('Эти слова встречаются в Legacy, прокачке и профессиях. Подробности по каждому — в соответствующем гайде.',
                        'These words come up in Legacy, leveling and professions. Each has its own guide for details.',
                        'Ці слова трапляються в Legacy, прокачуванні та професіях. Подробиці щодо кожного — у відповідному гайді.')]),
            ('table', {'head': [t('Термин', 'Term', 'Термін'), t('Что это', 'What it means', 'Що це')], 'rows': [
                [t('Legacy', 'Legacy', 'Legacy'), t('Система наград на весь аккаунт Battle.net. Вы выполняете испытания, получаете очки и тратите их на перки персонажа.', 'A reward system for your whole Battle.net account. You complete challenges, earn points and spend them on character perks.', 'Система нагород на весь обліковий запис Battle.net. Ви виконуєте випробування, отримуєте очки й витрачаєте їх на перки персонажа.')],
                [t('Испытание', 'Challenge', 'Випробування'), t('Задание Legacy вроде «достичь 25 уровня». Каждое выполненное даёт 1 очко Legacy.', 'A Legacy task such as “reach level 25”. Each completed one gives 1 Legacy point.', 'Завдання Legacy на кшталт «досягти 25 рівня». Кожне виконане дає 1 очко Legacy.')],
                [t('Перк', 'Perk', 'Перк'), t('Бонус Legacy, на который вы тратите очки: например, быстрее растут навыки ремёсел. Перки у каждого персонажа свои.', 'A Legacy bonus you spend points on, for example faster tradeskill gains. Each character has its own perks.', 'Бонус Legacy, на який ви витрачаєте очки: наприклад, швидше зростають навички ремесел. Перки в кожного персонажа свої.')],
                [t('Отдых', 'Rested XP', 'Відпочинок'), t('Запас бонусного опыта: копится, пока вы отдыхаете, и тратится, когда вы убиваете монстров.', 'A pool of bonus experience: it builds while you rest and is spent as you kill monsters.', 'Запас бонусного досвіду: накопичується, поки ви відпочиваєте, і витрачається, коли ви вбиваєте монстрів.')],
                [t('Лагерь', 'Camp', 'Табір'), t('Общий костёр, который ставят с Кулинарией. Рядом отдыхают, получают баффы и ставят объекты своих профессий.', 'A shared campfire built with Cooking. Players rest nearby, get buffs and place their profession objects.', 'Спільне вогнище, яке ставлять із Кулінарією. Поруч відпочивають, отримують баффи й ставлять об’єкти своїх професій.')],
            ]}),
        ]},
    ],
    'next': [('guides/builds/', t('Выбрать билд своего класса', 'Pick a build for your class', 'Обрати білд свого класу')), ('guides/legacy/', t('Как работает Legacy', 'How Legacy works', 'Як працює Legacy')), ('guides/leveling/', t('Прокачка 1–60', 'Leveling 1–60', 'Прокачування 1–60'))],
})

# ---------- Разделы /classes/ и /races/: таблицы сравнения с главной (JS — из index.src.html, ref:start…ref:end) ----------

HUBS = [
    {'slug': 'classes', 'path': 'classes/', 'art': 'hero_classes', 'hero': 'hero_classes', 'js': 'classref',
     'title': t('Классы', 'Classes', 'Класи'),
     'lead': t('Какой класс выбрать в WoW Forever: короткий ответ под вашу цель, темп прокачки по бете и сравнение девяти классов.',
               'Which class to pick in WoW Forever: a short answer for your goal, leveling pace from the beta and all nine classes compared.',
               'Який клас обрати у WoW Forever: коротка відповідь під вашу мету, темп прокачки за бетою та порівняння дев’яти класів.'),
     'tile': t('Какой класс выбрать и сравнение', 'Which class to pick, compared', 'Який клас обрати й порівняння'),
     'sources': [('Warcraft Tavern', 'https://www.warcrafttavern.com/forever/guides/classes/'),
                 ('LFCarry', 'https://lfcarry.com/guides/wow-forever-classes')],
     'sections': [
        {'id': 'choose', 'title': t('Какой класс выбрать', 'Which class to pick', 'Який клас обрати'), 'blocks': [
            ('text', [t('Новичку в WoW — маг или охотник: они быстрее всех качаются, бьют издалека и уверенно играют одни. Дальше выбирайте по роли, которую хотите в группе.',
                        'New to WoW: mage or hunter. They level fastest, fight at range and do well solo. Beyond that, pick by the role you want in a group.',
                        'Новачку в WoW — маг або мисливець: вони найшвидше качаються, б’ють здалеку й упевнено грають самі. Далі обирайте за роллю, яку хочете в групі.')]),
            ('picks', {'head': [t('Что хотите', 'What you want', 'Що хочете'), t('Класс', 'Class', 'Клас'), t('Почему', 'Why', 'Чому')], 'rows': [
                (t('Быстрее до 60', 'Reach 60 fastest', 'Швидше до 60'), ['mage', 'hunter'],
                 t('Самая быстрая прокачка по оценке LFCarry, примерно на 8% быстрее среднего.',
                   'The fastest leveling by LFCarry’s estimate, about 8% faster than average.',
                   'Найшвидша прокачка за оцінкою LFCarry, приблизно на 8% швидше за середню.')),
                (t('Играть одному', 'Play solo', 'Грати самому'), ['hunter', 'warlock', 'mage'],
                 t('У охотника и чернокнижника питомец держит врага, у чернокнижника ещё Жизнеотвод. Маг сам делает еду и воду.',
                   'The hunter and warlock pet holds the enemy, and the warlock also has Life Tap. The mage conjures their own food and water.',
                   'У мисливця й чорнокнижника вихованець тримає ворога, у чорнокнижника ще Life Tap. Маг сам робить їжу та воду.')),
                (t('Лечить', 'Heal', 'Лікувати'), ['priest', 'paladin', 'druid', 'shaman'],
                 t('Жрец всегда нужен группе. Паладин и друид могут сменить роль, шаман лечит и ставит тотемы для группы.',
                   'A priest is always wanted in a group. The paladin and druid can switch roles, the shaman heals and drops totems for the group.',
                   'Жрець завжди потрібен групі. Паладин і друїд можуть змінити роль, шаман лікує й ставить тотеми для групи.')),
                (t('Танковать', 'Tank', 'Танкувати'), ['warrior', 'paladin', 'druid'],
                 t('Воин — лучший танк, но качается медленнее всех. Паладин и друид танкуют и могут лечить.',
                   'The warrior is the best tank but levels the slowest. The paladin and druid tank and can heal.',
                   'Воїн — найкращий танк, але качається найповільніше. Паладин і друїд танкують і можуть лікувати.')),
                (t('Урон в ближнем бою', 'Melee damage', 'Шкода в ближньому бою'), ['rogue', 'warrior', 'shaman'],
                 t('Разбойник: очень высокий урон, скрытность и контроль. Воин: ветки Оружие и Неистовство. Шаман: Совершенствование.',
                   'Rogue: very high damage, stealth and control. Warrior: the Arms and Fury trees. Shaman: Enhancement.',
                   'Розбійник: дуже висока шкода, скритність і контроль. Воїн: гілки Зброя і Лють. Шаман: Вдосконалення.')),
                (t('Урон издалека', 'Ranged damage', 'Шкода здалеку'), ['mage', 'warlock', 'hunter', 'priest'],
                 t('Маг: порталы и еда для всех. Чернокнижник: урон со временем. Жрец: ветка Темная магия.',
                   'Mage: portals and food for everyone. Warlock: damage over time. Priest: the Shadow tree.',
                   'Маг: портали та їжа для всіх. Чорнокнижник: шкода з часом. Жрець: гілка Темрява.')),
                (t('Все роли на одном персонаже', 'Every role on one character', 'Усі ролі на одному персонажі'), ['paladin', 'druid'],
                 t('Танк, лекарь и урон в одном классе.', 'Tank, healer and damage in one class.', 'Танк, лікар і шкода в одному класі.')),
            ]}),
            ('tip', t('Сначала класс, потом раса: раса даёт четыре способности, но не меняет роль. Строка таблицы ниже открывает страницу класса с подходящими расами.',
                      'Class first, race second: a race gives four abilities but does not change your role. A row of the table below opens the class page with the races that suit it.',
                      'Спершу клас, потім раса: раса дає чотири здібності, але не змінює роль. Рядок таблиці нижче відкриває сторінку класу з расами, що йому пасують.')),
        ]},
        {'id': 'pace', 'title': t('Темп прокачки', 'Leveling pace', 'Темп прокачки'), 'blocks': [
            ('text', [t('Оценка LFCarry: в бете был потолок 30 уровня, выше цифры проектные. Разница между самым быстрым и самым медленным классом — около 20% времени до 60.',
                        'LFCarry’s estimate: the beta was capped at level 30, figures above that are projections. The gap between the fastest and slowest class is about 20% of the time to 60.',
                        'Оцінка LFCarry: у беті була стеля 30 рівня, вище цифри проєктні. Різниця між найшвидшим і найповільнішим класом — близько 20% часу до 60.')]),
            ('picks', {'head': [t('Темп', 'Pace', 'Темп'), t('Классы', 'Classes', 'Класи')], 'rows': [
                (t('Быстрее среднего, около 8%', 'Faster than average, about 8%', 'Швидше за середній, близько 8%'), ['mage', 'hunter']),
                (t('Средний', 'Average', 'Середній'), ['paladin', 'rogue', 'shaman', 'warlock']),
                (t('Медленнее среднего, около 5%', 'Slower than average, about 5%', 'Повільніше за середній, близько 5%'), ['priest', 'druid']),
                (t('Медленнее всех, около 12%', 'Slowest, about 12%', 'Найповільніше, близько 12%'), ['warrior']),
            ]}),
        ]},
        {'id': 'compare', 'title': t('Сравнение', 'Comparison', 'Порівняння'), 'blocks': [
         ('text', [t('Темп прокачки взят из прогнозов по бете: в бете был потолок 30 уровня, выше оценки проектные. Строка открывает страницу класса.',
                     'Leveling pace comes from beta projections: the beta was capped at level 30, figures above that are estimates. A row opens the class page.',
                     'Темп прокачки взято з прогнозів по беті: у беті була стеля 30 рівня, вище оцінки проєктні. Рядок відкриває сторінку класу.')]),
         ('raw', '<div class="cmp cls" id="classRef"></div>'),
     ]}]},
    {'slug': 'races', 'path': 'races/', 'art': 'hero_races', 'hero': 'hero_races', 'js': 'raceref',
     'title': t('Расы', 'Races', 'Раси'),
     'lead': t('Пять рас за каждую фракцию: доступные классы и четыре расовые способности.',
               'Five races per faction: available classes and four racial abilities.',
               'П’ять рас за кожну фракцію: доступні класи та чотири расові здібності.'),
     'tile': t('Сравнение всех рас', 'All races compared', 'Порівняння всіх рас'),
     'sources': [('Method', 'https://www.method.gg/wow-forever/all-new-racial-abilities-in-world-of-warcraft-forever'),
                 ('Warcraft Tavern', 'https://www.warcrafttavern.com/forever/guides/races/')],
     'sections': [{'id': 'compare', 'title': t('Сравнение', 'Comparison', 'Порівняння'), 'blocks': [
         ('text', [t('У каждой расы по четыре способности: две активные и две пассивные. Часть старых способностей заменена новыми, сопротивления убраны.',
                     'Each race has four abilities: two active and two passive. Some old abilities were replaced with new ones, resistances were removed.',
                     'У кожної раси по чотири здібності: дві активні та дві пасивні. Частину старих здібностей замінено новими, опори прибрано.')]),
         ('raw', '<div class="cmp rac" id="raceRef"></div>'),
         ('tip', t('Скайборн доступна обеим фракциям, выбор фракции делается при создании. Обе ветки знают дарнасский, а стартовая зона Zephras Isle общая, враги там не встречаются из-за слоёв.',
                   'Skyborne is playable for both factions; the faction is chosen at creation. Both branches know Darnassian, and the Zephras Isle starting zone is shared, with no enemies meeting there because of layers.',
                   'Скайборн ігрова за обидві фракції, фракцію обирають під час створення. Обидві гілки знають дарнаську, а стартова зона Zephras Isle спільна, вороги там не зустрічаються через шари.')),
     ]}]},
]


# ---------- Служебные страницы: /privacy/ и 404.html. Не гайды: в список гайдов и плитки не попадают ----------
# Политика описывает то, что сайт делает на самом деле. Появится реклама, форма или новый сторонний скрипт — сначала поправить её.

from build import CONTACT  # noqa: E402  (адрес один на весь сайт, подвал берёт его оттуда же)
_mail = f'<a href="mailto:{CONTACT}">{CONTACT}</a>'
_cf = 'https://www.cloudflare.com/privacypolicy/'
_dc = 'https://discord.com/privacy'
_ways = (('Discord', _dc), ('Google', 'https://policies.google.com/privacy'),
         ('Blizzard', 'https://www.blizzard.com/en-us/legal/a4380ee5-5c8d-4e3b-83b7-ea26d01a9918/blizzard-entertainment-online-privacy-policy'),
         ('Telegram', 'https://telegram.org/privacy'), ('Resend', 'https://resend.com/legal/privacy-policy'),
         ('Cloudflare Turnstile', 'https://www.cloudflare.com/turnstile-privacy-policy/'))
_waylinks = ' · '.join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in _ways)
_lic = ', '.join(f'<a href="{u}" target="_blank" rel="noopener">Creative Commons {n}</a>' for n, u in (
    ('BY 4.0', 'https://creativecommons.org/licenses/by/4.0/'), ('BY 3.0', 'https://creativecommons.org/licenses/by/3.0/'),
    ('CC0', 'https://creativecommons.org/publicdomain/zero/1.0/')))
_gh = 'https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement'

PAGES = [
    {'slug': 'privacy', 'path': 'privacy/', 'og': 'guides', 'art': 'hero_campfire',
     'title': t('Конфиденциальность', 'Privacy', 'Конфіденційність'),
     'lead': t('Какие данные собирает сайт и что хранится у вас в браузере. Коротко: без входа мы о вас ничего не знаем, после входа храним только профиль.',
               'What data the site collects and what is stored in your browser. In short: without signing in we know nothing about you; after signing in we keep only your profile.',
               'Які дані збирає сайт і що зберігається у вашому браузері. Коротко: без входу ми нічого про вас не знаємо, після входу зберігаємо лише профіль.'),
     'pills': [t('Обновлено 26.10.2026', 'Updated 26.10.2026', 'Оновлено 26.10.2026')],
     'sections': [
         {'id': 'short', 'title': t('Коротко', 'In short', 'Коротко'), 'blocks': [
             ('text', [t('Сайт можно читать без входа: тогда он не ставит cookies и не знает, кто вы. Вход нужен только для профиля и «Состава». Рекламы и комментариев на сайте нет.',
                         'The guide works without signing in: then the site sets no cookies and does not know who you are. Signing in is only needed for a profile and the Roster. The site has no ads or comments.',
                         'Сайт можна читати без входу: тоді він не ставить cookies і не знає, хто ви. Вхід потрібен лише для профілю і «Складу». Реклами й коментарів на сайті немає.')])]},
         {'id': 'account', 'title': t('Профиль', 'Profile', 'Профіль'), 'blocks': [
             ('text', [t('Войти можно через Discord, Google, Battle.net, Telegram или по почте. Пароль мы не получаем, ключи доступа этих сервисов не храним. От каждого способа берём минимум:',
                         'You can sign in with Discord, Google, Battle.net, Telegram or by email. We never receive your password and do not keep these services’ access keys. From each way we take the minimum:',
                         'Увійти можна через Discord, Google, Battle.net, Telegram або поштою. Пароль ми не отримуємо, ключі доступу цих сервісів не зберігаємо. Від кожного способу беремо мінімум:')]),
             ('list', [t('Discord — ID и ник. Участникам сервера Gabella Team — ещё дату вступления: от неё значок команды и достижения за стаж.',
                         'Discord: ID and nickname. For members of the Gabella Team server, also the date they joined: it gives the team mark and the achievements for time on the server.',
                         'Discord — ID і нік. Учасникам сервера Gabella Team — ще дату вступу: від неї значок команди й досягнення за стаж.'),
                       t('Google — только номер аккаунта. Почту и имя не запрашиваем.',
                         'Google: only the account number. We ask for neither your email nor your name.',
                         'Google — лише номер акаунта. Пошту й ім’я не запитуємо.'),
                       t('Battle.net — номер аккаунта и BattleTag.',
                         'Battle.net: account number and BattleTag.',
                         'Battle.net — номер акаунта й BattleTag.'),
                       t('Telegram — ID и @username, если он есть. Имя не храним.',
                         'Telegram: ID and @username, if you have one. We do not keep your name.',
                         'Telegram — ID та @username, якщо він є. Ім’я не зберігаємо.'),
                       t('Почта — только отпечаток адреса, посчитанный с секретным ключом: по нему адрес не восстановить. Сам адрес не храним: письмо со ссылкой входа отправляет сервис Resend. Пока ссылка действует (15 минут), храним маску адреса вида li***@g***.com: её показываем, если ссылку откроют в другом браузере.',
                         'Email: only a fingerprint of the address computed with a secret key: the address cannot be recovered from it. We do not keep the address itself: the sign-in link is sent by the Resend service. While the link is valid (15 minutes) we keep a mask of the address like li***@g***.com and show it if the link is opened in another browser.',
                         'Пошта — лише відбиток адреси, обчислений із секретним ключем: за ним адресу не відновити. Саму адресу не зберігаємо: лист із посиланням для входу надсилає сервіс Resend. Поки посилання діє (15 хвилин), зберігаємо маску адреси на кшталт li***@g***.com: її показуємо, якщо посилання відкриють в іншому браузері.'),
                       t('Если вы подписались на письма — храним адрес (зашифрованным), язык и дату согласия; отписка удаляет их сразу. Письма отправляет Resend.',
                         'If you subscribed to emails, we keep the address (encrypted), the language and the date of consent; unsubscribing deletes them at once. Emails are sent by Resend.',
                         'Якщо ви підписалися на листи — зберігаємо адресу (зашифрованою), мову й дату згоди; відписка видаляє їх одразу. Листи надсилає Resend.')]),
             ('text', [t('Аккаунт один, а входов может быть несколько: привязать и отвязать их можно в кабинете, раздел «Аккаунт». Сами по себе входы не склеиваются: вход новым способом без привязки создаёт новый аккаунт.',
                         'One account can have several ways to sign in: link and unlink them in your profile, under Account. Ways are never merged on their own: signing in a new way without linking it creates a new account.',
                         'Акаунт один, а входів може бути кілька: прив’язати й відв’язати їх можна в кабінеті, розділ «Акаунт». Самі входи не склеюються: вхід новим способом без прив’язки створює новий акаунт.'),
                       t('Ещё храним то, что вы указали сами: персонажей (имя, раса, класс, роль, уровень, профессии, время игры, облик: пол и фон портрета), рамку профиля, отметку «Ищу группу» и того, кто вас пригласил, если вы пришли по его ссылке.',
                         'We also keep what you entered yourself: your characters (name, race, class, role, level, professions, play time, look: gender and portrait background), your profile frame, the Looking for group mark and who invited you, if you came by their link.',
                         'Також зберігаємо те, що ви вказали самі: персонажів (ім’я, раса, клас, роль, рівень, професії, час гри, вигляд: стать і тло портрета), рамку профілю, позначку «Шукаю групу» і того, хто вас запросив, якщо ви прийшли за його посиланням.'),
                       t('Для достижений сайт ведёт счётчики: какие разделы сайта вы открывали, сколько слушали радио, в какие дни заходили. Счётчики идут только после входа.',
                         'For achievements the site keeps counters: which guide sections you opened, how long you listened to the radio, which days you visited. Counters run only after you sign in.',
                         'Для досягнень сайт веде лічильники: які розділи сайту ви відкривали, скільки слухали радіо, в які дні заходили. Лічильники працюють лише після входу.'),
                       t('В списке игроков и на вашей странице всем видны персонажи, достижения и рамка. Ник виден, только если вы включили его показ: у новых профилей он скрыт. Ник берётся у первого способа входа (ник Discord, BattleTag, @username в Telegram) и потом сам не меняется. В ссылке на вашу страницу — внутренний номер профиля вида u_…, он не связан с Discord ID.',
                         'In the player list and on your page everyone can see your characters, achievements and frame. Your nickname is shown only if you turned it on: new profiles keep it hidden. The nickname comes from your first way to sign in (Discord nickname, BattleTag, Telegram @username) and never changes by itself later. The link to your page carries an internal profile number like u_…, unrelated to your Discord ID.',
                         'У списку гравців і на вашій сторінці всім видно персонажів, досягнення й рамку. Нік видно, лише якщо ви ввімкнули його показ: у нових профілів він прихований. Нік береться з першого способу входу (нік Discord, BattleTag, @username у Telegram) і потім сам не змінюється. У посиланні на вашу сторінку — внутрішній номер профілю на кшталт u_…, він не пов’язаний із Discord ID.'),
                       t('После входа сайт ставит cookie — ключ сессии на 30 дней. Её получает только сервер профилей api.gabella.site; в базе лежит не сам ключ, а его хэш. Выход удаляет сессию. На время входа добавляются короткие метки: при входе через Discord, Google или Battle.net — защитная на 10 минут, при входе по почте — «вход начат в этом браузере» на 15 минут.',
                         'After you sign in, the site sets a cookie: a session key for 30 days. Only the profile server api.gabella.site receives it; the database stores a hash of the key, not the key itself. Signing out deletes the session. While you sign in, short marks are added: a protective one for 10 minutes with Discord, Google or Battle.net, and “sign-in started in this browser” for 15 minutes with email.',
                         'Після входу сайт ставить cookie — ключ сесії на 30 днів. Її отримує лише сервер профілів api.gabella.site; у базі лежить не сам ключ, а його хеш. Вихід видаляє сесію. На час входу додаються короткі позначки: під час входу через Discord, Google або Battle.net — захисна на 10 хвилин, під час входу поштою — «вхід почато в цьому браузері» на 15 хвилин.'),
                       t('При входе по почте, создании первого персонажа и подписке на письма сайт загружает проверку «не робот» Cloudflare Turnstile: Cloudflare получает IP-адрес и сведения о браузере, чтобы отличить человека от программы.',
                         'When you sign in by email, create your first character or subscribe to emails, the site loads the Cloudflare Turnstile “not a robot” check: Cloudflare receives your IP address and browser details to tell a person from a program.',
                         'Під час входу поштою, створення першого персонажа та підписки на листи сайт завантажує перевірку «не робот» Cloudflare Turnstile: Cloudflare отримує IP-адресу й відомості про браузер, щоб відрізнити людину від програми.'),
                       t('Против спама и перегрузки сервер до часа помнит число попыток по отпечатку почты и по IP-адресу — писем входа, новых аккаунтов, частых изменений профиля, — потом стирает.',
                         'Against spam and overload the server remembers the number of attempts by email fingerprint and by IP address for up to an hour (sign-in emails, new accounts, frequent profile changes), then erases it.',
                         'Проти спаму й перевантаження сервер до години пам’ятає кількість спроб за відбитком пошти та за IP-адресою — листів входу, нових акаунтів, частих змін профілю, — потім стирає.')]),
             ('raw', t(f'<p>Политики конфиденциальности: {_waylinks}</p>',
                       f'<p>Privacy policies: {_waylinks}</p>',
                       f'<p>Політики конфіденційності: {_waylinks}</p>'))]},
         {'id': 'storage', 'title': t('Где и сколько хранится', 'Where and how long', 'Де й скільки зберігається'), 'blocks': [
             ('text', [t('Профили хранятся в Cloudflare (Workers и база D1): Cloudflare обрабатывает их по нашему поручению. Письма входа отправляет Resend (серверы в Ирландии) — тоже по нашему поручению. Храним, пока вы не удалите профиль. Не продаём и не передаём, кроме уведомления о жалобе в закрытый канал команды в Discord (см. ниже).',
                         'Profiles are stored with Cloudflare (Workers and the D1 database), which processes them on our behalf. Sign-in emails are sent by Resend (servers in Ireland), also on our behalf. We keep profiles until you delete them. We do not sell or share them, except a report notice sent to the team’s private Discord channel (see below).',
                         'Профілі зберігаються в Cloudflare (Workers і база D1): Cloudflare обробляє їх за нашим дорученням. Листи входу надсилає Resend (сервери в Ірландії) — теж за нашим дорученням. Зберігаємо, доки ви не видалите профіль. Не продаємо й не передаємо, окрім сповіщення про скаргу в закритий канал команди в Discord (див. нижче).'),
                       t('Администратор может скрыть персонажа, нарушающего правила, и закрыть вход аккаунту за спам или оскорбления.',
                         'An administrator can hide a character that breaks the rules and close sign-in for an account that spams or insults people.',
                         'Адміністратор може приховати персонажа, що порушує правила, і закрити вхід акаунту за спам чи образи.'),
                       t('Если вы пожаловались на игрока, мы храним, кто пожаловался, на кого, на что, причину и пояснение, если вы его написали. Запись остаётся со статусом решения и удаляется вместе с профилем любой из сторон. В закрытый канал команды в Discord уходит уведомление: что не так, причина и ссылка на игрока, без имени автора жалобы. Игрок не видит, кто пожаловался.',
                         'If you report a player, we keep who reported, whom, what about, the reason and the note, if you wrote one. The record stays with the decision status and is deleted together with the profile of either side. A notice goes to the team’s private Discord channel: what is wrong, the reason and a link to the player, without the reporter’s name. The player does not see who reported.',
                         'Якщо ви поскаржилися на гравця, ми зберігаємо, хто поскаржився, на кого, на що, причину й пояснення, якщо ви його написали. Запис лишається зі статусом рішення й видаляється разом із профілем будь-якої зі сторін. У закритий канал команди в Discord надходить сповіщення: що не так, причина й посилання на гравця, без імені автора скарги. Гравець не бачить, хто поскаржився.')])]},
         {'id': 'delete', 'title': t('Скачать и удалить', 'Download and delete', 'Завантажити й видалити'), 'blocks': [
             ('text', [t('В кабинете «Мой профиль», раздел «Аккаунт», можно скачать всё, что мы о вас храним, одним файлом — вместе со способами входа и сроками сессий — и удалить профиль. Вместе с ним сразу удаляются персонажи, достижения, счётчики, записи в ленте и сессии. Восстановить профиль нельзя.',
                         'In My profile, under Account, you can download everything we keep about you as one file, including your ways to sign in and session end dates, and delete your profile. Your characters, achievements, counters, feed entries and sessions are deleted with it at once. A deleted profile cannot be restored.',
                         'У кабінеті «Мій профіль», розділ «Акаунт», можна завантажити все, що ми про вас зберігаємо, одним файлом — разом зі способами входу й строками сесій — і видалити профіль. Разом із ним одразу видаляються персонажі, досягнення, лічильники, записи в стрічці й сесії. Відновити профіль не можна.')])]},
         {'id': 'analytics', 'title': t('Статистика посещений', 'Visit statistics', 'Статистика відвідувань'), 'blocks': [
             ('text', [t('Чтобы понимать, какие страницы читают, сайт использует Cloudflare Web Analytics. Он работает без cookies, не снимает отпечаток браузера и не следит за вами на других сайтах.',
                         'To see which pages people read, the site uses Cloudflare Web Analytics. It works without cookies, does not fingerprint your browser and does not track you across other sites.',
                         'Щоб розуміти, які сторінки читають, сайт використовує Cloudflare Web Analytics. Він працює без cookies, не знімає відбиток браузера і не стежить за вами на інших сайтах.'),
                       t('Мы видим только сводные цифры: сколько раз открывали страницу, из какой страны, с какого типа устройства и с какого сайта пришли. Отдельного посетителя в них не различить.',
                         'We only see totals: how many times a page was opened, from which country, on what kind of device and from which site. Individual visitors cannot be told apart.',
                         'Ми бачимо лише зведені цифри: скільки разів відкривали сторінку, з якої країни, з якого типу пристрою і з якого сайту прийшли. Окремого відвідувача в них не розрізнити.'),
                       t('Раз в сутки браузер отправляет анонимный счёт: «визит» и, если у вас сохранён персонаж, «визит с персонажем». Хранится только число за день: без IP, cookies, имени и данных персонажа. Отказаться: включите «Не отслеживать» (DNT) или Global Privacy Control; метка дня лежит в localStorage (gabella-cnt).',
                         'Once a day your browser sends an anonymous count: a “visit” and, if you have saved a character, a “visit with a character”. We keep only the daily total: no IP address, cookies, name or character data. To opt out, turn on Do Not Track (DNT) or Global Privacy Control. The browser keeps the date of the last count in localStorage (gabella-cnt).',
                         'Раз на добу браузер надсилає анонімний лічильник: «візит» і, якщо у вас збережено персонажа, «візит із персонажем». Зберігається лише число за день: без IP, cookies, імені й даних персонажа. Щоб відмовитися, увімкніть «Не відстежувати» (DNT) або Global Privacy Control; позначка дня лежить у localStorage (gabella-cnt).')]),
             ('raw', t(f'<p><a href="{_cf}" target="_blank" rel="noopener">Политика конфиденциальности Cloudflare</a></p>',
                       f'<p><a href="{_cf}" target="_blank" rel="noopener">Cloudflare privacy policy</a></p>',
                       f'<p><a href="{_cf}" target="_blank" rel="noopener">Політика конфіденційності Cloudflare</a></p>'))]},
         {'id': 'hosting', 'title': t('Хостинг', 'Hosting', 'Хостинг'), 'blocks': [
             ('text', [t('Сайт размещён на GitHub Pages. Как любой веб-сервер, GitHub получает IP-адрес вашего устройства, чтобы отдать страницу, и может хранить его в журналах для защиты от атак. У нас доступа к этим журналам нет.',
                         'The site is hosted on GitHub Pages. Like any web server, GitHub receives your device’s IP address to deliver the page and may keep it in logs to protect against attacks. We have no access to those logs.',
                         'Сайт розміщено на GitHub Pages. Як будь-який вебсервер, GitHub отримує IP-адресу вашого пристрою, щоб віддати сторінку, і може зберігати її в журналах для захисту від атак. Ми доступу до цих журналів не маємо.')]),
             ('raw', t(f'<p><a href="{_gh}" target="_blank" rel="noopener">Политика конфиденциальности GitHub</a></p>',
                       f'<p><a href="{_gh}" target="_blank" rel="noopener">GitHub privacy statement</a></p>',
                       f'<p><a href="{_gh}" target="_blank" rel="noopener">Політика конфіденційності GitHub</a></p>'))]},
         {'id': 'device', 'title': t('Что хранится у вас', 'Stored on your device', 'Що зберігається у вас'), 'blocks': [
             ('text', [t('В памяти браузера (localStorage) сайт запоминает выбранную тему, вашего персонажа — расу, класс, уровень и профессии, если вы их указали, — и настройки радио: станцию, трек, очередь треков, громкость, таймер сна и звуки вокруг, а на странице «В игре» — ваши таймеры, фракцию и выбранного персонажа. Чтобы сайт открывался без сети, браузер хранит копии страниц. После входа добавляются отметка о входе и выключатель звука достижений, а копия профиля для быстрой загрузки лежит в памяти вкладки (sessionStorage) и стирается с её закрытием. Ещё сайт помнит выбранный язык, кто вас пригласил, если вы пришли по ссылке, страницу, на которую вернуться после входа, и время начала входа через Telegram.',
                         'In browser storage (localStorage) the site remembers your chosen theme, your character (race, class, level and professions) if you entered them, and the radio settings: station, track, the queue of tracks, volume, sleep timer and ambient sounds, and on the In game page your timers, faction and chosen character. To open the guide offline, the browser keeps copies of the pages. After you sign in, it also keeps a signed-in mark and the achievement sound switch, while a copy of your profile for faster loading lives in the tab’s memory (sessionStorage) and is erased when you close it. The site also remembers your chosen language, who invited you if you came by their link, the page to return to after signing in, and when a Telegram sign-in was started.',
                         'У пам’яті браузера (localStorage) сайт запам’ятовує вибрану тему, персонажа — расу, клас, рівень і професії, якщо ви їх вказали, — і налаштування радіо: станцію, трек, чергу треків, гучність, таймер сну і звуки довкола, а на сторінці «У грі» — ваші таймери, фракцію та вибраного персонажа. Щоб сайт відкривався без мережі, браузер зберігає копії сторінок. Після входу додаються позначка входу й вимикач звуку досягнень, а копія профілю для швидкого завантаження лежить у пам’яті вкладки (sessionStorage) і стирається з її закриттям. Ще сайт пам’ятає вибрану мову, хто вас запросив, якщо ви прийшли за посиланням, сторінку, на яку повернутися після входу, і час початку входу через Telegram.'),
                       t('На странице «День 1» там же хранятся ваши отметки чек-листа.',
                         'On the Day 1 page, your checklist ticks are stored there too.',
                         'На сторінці «День 1» там само зберігаються ваші позначки чек-листа.'),
                       t('Эти данные остаются на вашем устройстве и никуда не отправляются. Удалить их можно, очистив данные сайта в настройках браузера.',
                         'This data stays on your device and is not sent anywhere. You can delete it by clearing the site data in your browser settings.',
                         'Ці дані залишаються на вашому пристрої й нікуди не надсилаються. Видалити їх можна, очистивши дані сайту в налаштуваннях браузера.'),
                       t('Раз в сутки браузер отправляет анонимный счёт: «визит» и, если у вас сохранён персонаж, «визит с персонажем». Хранится только число за день: без IP, cookies, имени и данных персонажа. Отказаться: включите «Не отслеживать» (DNT) или Global Privacy Control; метка дня лежит в localStorage (gabella-cnt).',
                         'Once a day your browser sends an anonymous count: a “visit” and, if you have saved a character, a “visit with a character”. We keep only the daily total: no IP address, cookies, name or character data. To opt out, turn on Do Not Track (DNT) or Global Privacy Control. The browser keeps the date of the last count in localStorage (gabella-cnt).',
                         'Раз на добу браузер надсилає анонімний лічильник: «візит» і, якщо у вас збережено персонажа, «візит із персонажем». Зберігається лише число за день: без IP, cookies, імені й даних персонажа. Щоб відмовитися, увімкніть «Не відстежувати» (DNT) або Global Privacy Control; позначка дня лежить у localStorage (gabella-cnt).')])]},
         {'id': 'links', 'title': t('Шрифты, музыка и ссылки', 'Fonts, music and links', 'Шрифти, музика та посилання'), 'blocks': [
             ('text', [t('Шрифты и картинки загружаются с нашего же сайта, без сторонних сервисов. Музыка радио лежит в хранилище Cloudflare R2 и загружается с нашего адреса media.gabella.site, только когда вы включили радио; как и при открытии страниц, Cloudflare получает IP-адрес вашего устройства. Звуки костра, дождя и ветра создаёт сам браузер. Ссылки на источники ведут на другие сайты, у них свои правила конфиденциальности.',
                         'Fonts and images load from this site, with no third-party services. Radio music is stored in Cloudflare R2 and loads from our address media.gabella.site, only when you turn the radio on; as with the pages, Cloudflare receives your device’s IP address. The campfire, rain and wind sounds are made by the browser itself. Links to sources lead to other sites, which have their own privacy rules.',
                         'Шрифти й зображення завантажуються з нашого ж сайту, без сторонніх сервісів. Музика радіо лежить у сховищі Cloudflare R2 і завантажується з нашої адреси media.gabella.site, лише коли ви ввімкнули радіо; як і під час відкриття сторінок, Cloudflare отримує IP-адресу вашого пристрою. Звуки багаття, дощу й вітру створює сам браузер. Посилання на джерела ведуть на інші сайти, у них свої правила конфіденційності.')]),
             ('raw', t(f'<p>Музыка радио: Kevin MacLeod (incompetech.com) и другие авторы с opengameart.org, лицензии {_lic}. Звук перекодирован и выровнен по громкости. Автор и лицензия каждого трека — в панели радио.</p>',
                       f'<p>Radio music: Kevin MacLeod (incompetech.com) and other authors from opengameart.org, licensed under {_lic}. The audio is re-encoded and levelled in loudness. The author and license of every track are in the radio panel.</p>',
                       f'<p>Музика радіо: Kevin MacLeod (incompetech.com) та інші автори з opengameart.org, ліцензії {_lic}. Звук перекодовано й вирівняно за гучністю. Автор і ліцензія кожного треку — у панелі радіо.</p>'))]},
         {'id': 'contact', 'title': t('Связь', 'Contact', 'Зв’язок'), 'blocks': [
             ('text', [t('С вопросами о данных, ошибками на сайте и претензиями правообладателей пишите на почту ниже. Если не можете войти, профиль удалим по письму: укажите имя основного персонажа и способ входа.',
                         'For questions about data, mistakes in the guide or copyright concerns, write to the address below. If you cannot sign in, we will delete your profile on request: include your main character’s name and how you signed in.',
                         'З питаннями про дані, помилками на сайті та претензіями правовласників пишіть на пошту нижче. Якщо не можете увійти, профіль видалимо за листом: вкажіть ім’я основного персонажа і спосіб входу.')]),
             ('raw', f'<p>{_mail}</p>'),
             ('text', [t('Если что-то изменится, например появится реклама, мы обновим эту страницу и дату вверху.',
                         'If anything changes, for example if ads appear, we will update this page and the date at the top.',
                         'Якщо щось зміниться, наприклад з’явиться реклама, ми оновимо цю сторінку й дату вгорі.')])]},
     ]},
]

from langs import AUTONYM, HREFLANG, LANGS  # noqa: E402

NF_FIND = {'ru': ('Поиск по сайту', 'Найти'), 'en': ('Search the site', 'Search'), 'uk': ('Пошук по сайту', 'Знайти'),
           'de': ('Seite durchsuchen', 'Suchen'), 'fr': ('Rechercher sur le site', 'Chercher'), 'es': ('Buscar en el sitio', 'Buscar'),
           'pt': ('Pesquisar no site', 'Buscar'), 'it': ('Cerca nel sito', 'Cerca'), 'pl': ('Szukaj w serwisie', 'Szukaj')}


def NF_SEARCH(lang):
    """404: a search box; the form opens tools/?q=, where the site search starts with the query."""
    label, go = NF_FIND[lang]
    return (f'<form class="nf-find" role="search" action="tools/" method="get"><input type="search" name="q" autocomplete="off" '
            f'aria-label="{label}" placeholder="{label}"><button class="btn" type="submit">{go}</button></form>')


# 404.html в корне гида: GitHub Pages отдаёт её на любой несуществующий адрес под /wow/. Одна страница на все языки.
NOT_FOUND = {
    'slug': '404', 'path': '', 'og': 'guides', 'art': 'hero_campfire', 'more': False,
    'title': t('Страница не найдена', 'Page not found', 'Сторінку не знайдено'),
    'lead': t('Такой страницы нет: ссылка устарела или в адресе опечатка. Разделы сайта ниже.',
              'This page does not exist: the link is outdated or the address has a typo. The site sections are below.',
              'Такої сторінки немає: посилання застаріло або в адресі помилка. Розділи сайту нижче.'),
    'sections': [{'id': 'where', 'title': t('Куда дальше', 'Where next', 'Куди далі'), 'blocks': [
        ('raw', {l: NF_SEARCH(l) for l in LANGS}),
        ('raw', '<p class="nf-langs">' + '<span aria-hidden="true"> · </span>'.join(   # the guide home in every language
            f'<a href="/wow/{"" if l == "ru" else l + "/"}" lang="{HREFLANG[l]}">{AUTONYM[l]}</a>' for l in LANGS) + '</p>'),
    ]}],
}

# ---------- /play/ «В игре»: второй экран на время игры. Сборка — build_guides.play_body + JS['play'] ----------
# Маршрут по зонам и совет про отдых страница берёт из гайда «Прокачка» (секции route и pace), тут только подписи и рубежи.
PLAY = {
    'slug': 'play', 'path': 'play/', 'og': 'guides', 'art': 'hero_campfire', 'compact': True, 'more': False, 'js': 'play',
    'title': t('В игре', 'In game', 'У грі'),
    'lead': t('Зоны и подземелья под ваш уровень, таймеры, радио.',
              'Zones and dungeons for your level, timers, radio.',
              'Зони й підземелля під ваш рівень, таймери, радіо.'),
    'sections': [],
}
# Рубежи по уровню — только факты из гайдов (ездовое — секция pace «Прокачки», Хиджал — маршрут, рейды — «Подземелья и рейды»)
PLAY_MILESTONES = [
    (40, t('Ездовое животное: обучение 100 золотых и скакун 20 (+60% скорости).',
           'Riding: training 100 gold and a mount 20 (+60% speed).',
           'Їздова тварина: навчання 100 золотих і скакун 20 (+60% швидкості).')),
    (60, t('Быстрое ездовое: 1000 и 200 золотых (+100%). Открыт Mount Hyjal, рейды — с 09.12.2026.',
           'Fast riding: 1,000 and 200 gold (+100%). Mount Hyjal opens, raids from 09.12.2026.',
           'Швидка їздова: 1000 і 200 золотих (+100%). Відкритий Mount Hyjal, рейди — з 09.12.2026.')),
]
PLAY_TX = {
    'radio': t('Радио', 'Radio', 'Радіо'),
    'lvl': t('Уровень', 'Level', 'Рівень'),
    'lvDown': t('Уровень ниже', 'Level down', 'Рівень нижче'),
    'lvUp': t('Уровень выше', 'Level up', 'Рівень вище'),
    'noHero': t('Персонаж не выбран', 'No character set', 'Персонажа не вибрано'),
    'edit': t('Настроить персонажа', 'Set up your character', 'Налаштувати персонажа'),
    'fac': t('Фракция', 'Faction', 'Фракція'),
    'alliance': t('Альянс', 'Alliance', 'Альянс'),
    'horde': t('Орда', 'Horde', 'Орда'),
    'needLvl': t('Выберите уровень — подскажем зоны и подземелья.',
                 'Pick your level to see zones and dungeons.',
                 'Оберіть рівень — підкажемо зони й підземелля.'),
    'lvQuick': t('Уровень одним нажатием', 'Level in one tap', 'Рівень одним натисканням'),
    'lvIn': t('Уровень от 1 до 60', 'Level from 1 to 60', 'Рівень від 1 до 60'),
    'myTal': t('Мои таланты', 'My talents', 'Мої таланти'),
    'clsGuide': t('Гайд класса', 'Class guide', 'Гайд класу'),
    'clsLvl': t('Прокачка класса', 'Class leveling', 'Прокачка класу'),
    'now': t('Сейчас', 'Now', 'Зараз'),
    'next': t('Дальше', 'Next', 'Далі'),
    'from': t('с', 'from', 'з'),
    'at': t('на', 'at', 'на'),
    'route': t('Весь маршрут', 'Full route', 'Весь маршрут'),
    'dung': t('Подземелья по уровню', 'Dungeons by level', 'Підземелля за рівнем'),
    'dungNone': t('Под этот уровень подземелий ещё нет. Ближайшие:', 'No dungeons at this level yet. The nearest:', 'Під цей рівень підземель ще немає. Найближчі:'),
    'all': t('Все подземелья', 'All dungeons', 'Усі підземелля'),
    'new': t('новое', 'new', 'нове'),
    'timers': t('Таймеры', 'Timers', 'Таймери'),
    'food': t('Еда', 'Food', 'Їжа'),
    'foodNote': t('+5% опыта за врагов', '+5% experience from enemies', '+5% досвіду за ворогів'),
    'min': t('мин', 'min', 'хв'),
    'custom': t('Своё', 'Custom', 'Своє'),
    'name': t('Название', 'Name', 'Назва'),
    'minutes': t('Минут', 'Minutes', 'Хвилин'),
    'start': t('Старт', 'Start', 'Старт'),
    'timer': t('Таймер', 'Timer', 'Таймер'),
    'done': t('Время вышло', 'Time is up', 'Час вийшов'),
    'again': t('Ещё раз', 'Again', 'Ще раз'),
    'remove': t('Убрать', 'Remove', 'Прибрати'),
    'noTimers': t('Нажмите на заготовку или задайте своё время. Таймеры идут и после перезагрузки страницы.',
                  'Tap a preset or set your own time. Timers keep running after the page reloads.',
                  'Натисніть заготовку або задайте свій час. Таймери йдуть і після перезавантаження сторінки.'),
    'notify': t('Уведомление, когда вкладка в фоне', 'Notify when the tab is in the background', 'Сповіщення, коли вкладка у фоні'),
    'guest': t('Войдите — уровень и персонажи сохранятся в профиле.',
               'Log in to keep your level and characters in your profile.',
               'Увійдіть — рівень і персонажі збережуться в профілі.'),
    'login': t('Войти', 'Log in', 'Увійти'),
    'profile': t('Профиль', 'Profile', 'Профіль'),
    'chars': t('Персонажи', 'Characters', 'Персонажі'),
    'addChar': t('Добавить персонажа', 'Add a character', 'Додати персонажа'),
    'day1': t('День 1', 'Day 1', 'День 1'),
    'day1d': t('Чек-лист: что сделать до старта, в первые часы и в первый вечер.',
               'Checklist: what to do before launch, in the first hours and on the first evening.',
               'Чек-лист: що зробити до старту, у перші години та першого вечора.'),
    'day1go': t('Открыть чек-лист', 'Open the checklist', 'Відкрити чек-лист'),
}
PAGES.append(PLAY)


# ---------- Гайды прокачки по классам: девять страниц, раздел «Прокачка по классам» в гайде прокачки, плитка хаба (content/class_guides.py) ----------

from content import class_guides  # noqa: E402

class_guides.attach(GUIDES, HUBS, ORDER)
CLASS_HUB_TILE = class_guides.HUB_TILE   # на хабе гайдов вместо девяти плиток: одна, ведёт на раздел «Прокачка по классам»


# ---------- Билды спеков: страницы builds-<класс>, раздел «Билды по классам» и ссылки спеков в тир-листе, плитка хаба (content/spec_builds.py) ----------

from content import spec_builds  # noqa: E402

spec_builds.attach(GUIDES, HUBS, ORDER)
from content import spec_cheats  # noqa: E402

spec_cheats.attach(GUIDES, HUBS, ORDER)   # шпоры четырёх спеков из готовых разделов; названия на всех языках — spec_cheats.finish() в build_guides
from content import dungeon_pages  # noqa: E402

dungeon_pages.attach(GUIDES, ORDER)   # страницы подземелий guides/dungeons/<slug>/ после «Подземелий» и ссылки на них в таблице
# /guides/builds/: девять плиток билдов на своей странице (хаб, «Ещё» и подвал ведут сюда, а не в середину тир-листа)
_tl = next(g for g in GUIDES if g['slug'] == 'tier-list')['sections']
# the talent calculator (talents/<class>/, build_guides.calc_*) above the nine builds; new strings, so all nine languages here
CALC_PLATE = {
    'h': {'ru': 'Калькулятор талантов', 'en': 'Talent calculator', 'uk': 'Калькулятор талантів', 'de': 'Talentrechner',
          'fr': 'Calculateur de talents', 'es': 'Calculadora de talentos', 'pt': 'Calculadora de talentos', 'it': 'Calcolatore di talenti',
          'pl': 'Kalkulator talentów'},
    'd': {'ru': 'Свой билд для любого из девяти классов: три ветки, 51 очко, ссылка на билд.',
          'en': 'Your own build for any of the nine classes: three trees, 51 points, a link to share.',
          'uk': 'Свій білд для будь-якого з дев’яти класів: три гілки, 51 очко, посилання на білд.',
          'de': 'Dein eigener Build für jede der neun Klassen: drei Bäume, 51 Punkte, Link zum Teilen.',
          'fr': 'Votre propre build pour chacune des neuf classes : trois arbres, 51 points, un lien à partager.',
          'es': 'Tu propia build para cualquiera de las nueve clases: tres árboles, 51 puntos y un enlace para compartir.',
          'pt': 'Sua própria build para qualquer uma das nove classes: três árvores, 51 pontos e um link para compartilhar.',
          'it': 'La tua build per ognuna delle nove classi: tre alberi, 51 punti e un link da condividere.',
          'pl': 'Własny build dla każdej z dziewięciu klas: trzy drzewka, 51 punktów i link do udostępnienia.'},
    'go': {'ru': 'Открыть', 'en': 'Open', 'uk': 'Відкрити', 'de': 'Öffnen', 'fr': 'Ouvrir', 'es': 'Abrir', 'pt': 'Abrir', 'it': 'Apri',
           'pl': 'Otwórz'},
}
GUIDES.append({
    'slug': 'builds', 'art': 'paladin', 'hub': False, 'footer': True,
    'title': spec_builds.BUILDS_TITLE, 'lead': spec_builds.BUILDS_LEAD, 'tile': spec_builds.BUILDS_TILE,
    'pills': [spec_builds.BETA, t('9 классов, 27 спеков', '9 classes, 27 specs', '9 класів, 27 спеціалізацій'), spec_builds.LATER],
    'sources': [('Wowhead: Forever Talent Calculator', 'https://www.wowhead.com/forever/talent-calc'),
                ('Wowhead: Forever Class Guides', 'https://www.wowhead.com/forever/guides/classes')]
               + [x for g in spec_builds.SPEC_BUILDS for x in g['sources'] if x[0].startswith('Icy Veins') and x[0].endswith('Talent Calculator')],
    'sections': [{'id': 'classes', 'title': t('Девять классов', 'Nine classes', 'Дев’ять класів'),
                  'blocks': [('calc', CALC_PLATE), next(s for s in _tl if s['id'] == 'builds')['blocks'][1]]}],
})
GUIDES.sort(key=lambda g: ORDER.index(g['slug']))
BUILDS_HUB_TILE = dict(spec_builds.HUB_TILE, href='guides/builds/')   # на хабе одна плитка «Билды по классам»


# ---------- «Мой персонаж» без входа: страница character/ (content/hero.py, сборка build_guides.hero_*) ----------

from content import hero  # noqa: E402

PAGES.append(hero.PAGE)


# ---------- «Следующий шаг» (поле next): 1–3 ссылки по сценарию новичка класс → билд → прокачка → профессии → подземелья ----------

NX = {
    'builds': ('guides/builds/', t('Выбрать билд своего класса', 'Pick a build for your class', 'Обрати білд свого класу')),
    'leveling': ('guides/leveling/', t('Прокачка 1–60 по зонам', 'Leveling 1–60 by zone', 'Прокачування 1–60 за зонами')),
    'classes': ('classes/', t('Какой класс выбрать', 'Which class to pick', 'Який клас обрати')),
    'professions': ('guides/professions/', t('Профессии под класс', 'Professions for your class', 'Професії під клас')),
    'dungeons': ('guides/dungeons/', t('Подземелья по уровням', 'Dungeons by level', 'Підземелля за рівнями')),
    'legacy': ('guides/legacy/', t('Как работает Legacy', 'How Legacy works', 'Як працює Legacy')),
    'glossary': ('guides/glossary/', t('Словарь терминов', 'Glossary', 'Словник термінів')),
    'tier-list': ('guides/tier-list/', t('Тир-лист: кто сильнее', 'Tier list: who is strongest', 'Тір-лист: хто сильніший')),
    'best-race': ('guides/best-race/', t('Лучшая раса для класса', 'Best race for your class', 'Найкраща раса для класу')),
    'pvp': ('guides/pvp/', t('PvP: звания, Честь и награды', 'PvP: ranks, Honor and rewards', 'PvP: звання, Честь і нагороди')),
    'launch-checklist': ('guides/launch-checklist/', t('Чек-лист к старту', 'Launch checklist', 'Чек-лист до старту')),
    'faq': ('guides/faq/', t('Даты и частые вопросы', 'Dates and common questions', 'Дати й часті питання')),
    'addons': ('guides/addons/', t('Аддоны для старта', 'Add-ons for launch', 'Аддони для старту')),
}
NX_BUILD = t('Билд и таланты по уровням', 'Build and talents level by level', 'Білд і таланти за рівнями')
NX_LVL = t('Прокачка этим классом 1–60', 'Leveling this class 1–60', 'Прокачування цим класом 1–60')
NEXT = {
    'name-reservation': ['launch-checklist', 'classes', 'faq'],
    'launch-checklist': ['leveling', 'classes', 'addons'],
    'launch-day': ['leveling', 'launch-checklist', 'faq'],
    'server-status': ['faq', 'launch-checklist', 'leveling'],
    'faq': ['launch-checklist', 'classes', 'glossary'],
    'requirements': ['launch-checklist', 'addons', 'faq'],
    'news': ['faq', 'launch-checklist', 'leveling'],
    'leveling': ['builds', 'professions', 'dungeons'],
    'builds': ['tier-list', 'leveling', 'glossary'],
    'best-race': ['classes', 'builds', 'leveling'],
    'tier-list': ['builds', 'best-race', 'pvp'],
    'pvp': ['tier-list', 'best-race', 'builds'],
    'legacy': ['leveling', 'professions', 'glossary'],
    'dungeons': ['builds', 'professions', 'glossary'],
    'professions': ['leveling', 'dungeons', 'legacy'],
    'addons': ['launch-checklist', 'leveling', 'glossary'],
    'classes': ['builds', 'best-race', 'leveling'],
    'races': ['classes', 'best-race', 'leveling'],
}
for _g in GUIDES + PAGES:
    _s = _g['slug']
    if 'next' in _g or _g.get('only'):
        continue
    if _s in NEXT:
        _g['next'] = [NX[k] for k in NEXT[_s]]
    elif _s.startswith(('leveling-', 'builds-', 'spec-')):
        _c = _s.split('-')[1]
        _b, _l = (f'guides/builds-{_c}/', NX_BUILD), (f'guides/leveling-{_c}/', NX_LVL)
        _g['next'] = [_l, NX['tier-list'], NX['professions']] if _s.startswith('builds-') else \
                     [_b, NX['professions'], NX['dungeons']] if _s.startswith('leveling-') else [_b, _l, NX['dungeons']]
