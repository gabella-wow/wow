"""SEO-обвязка гида: последний шаг сборки (build.py зовёт seo.main() после всех страниц).
Шаблоны и контент не трогает: правит уже собранные index.html —
  * <title>, meta description, og:title/og:description/og:image:alt под поисковые запросы (тексты ниже, на трёх языках);
  * og:locale:alternate; JSON-LD (WebSite + Organization на главной, BreadcrumbList на разделах/классах/расах/гайдах,
    Article с датой обновления на гайдах, FAQPage на FAQ); метка подтверждения Bing (VERIFY);
  * сниппет Cloudflare Web Analytics, если задан CF_BEACON_TOKEN;
и пишет sitemap.xml со всеми страницами и hreflang-альтернативами.
robots.txt живёт в корне домена — репо gabella-wow/gabella-wow.github.io (gabella-hub), не здесь.
Если запускаете build_tools.py или build_guides.py отдельно, потом запустите и python seo.py.
Запуск: python seo.py"""
import json, os, re, sys
from html import escape

import build
from build import CLASSES, LANGS, RACES_PAGE, SITE, page_dir, tr
import langs
import live
import report
from langs import HREFLANG, LOCALE
from content.guides import GUIDES, HUB, HUBS

HERE = build.HERE

# Cloudflare Web Analytics: токен сайта gabella.site (Analytics → Web analytics → gabella.site → Manage site, режим «Enable with JS Snippet installation» — DNS only, автовставки нет).
# Пусто — сниппет не вставляется.
CF_BEACON_TOKEN = 'ee1d216e690040389063e8d72384c2c7'

# Подтверждение прав в поисковиках (Яндекс не используем — решение 23.10): значение content= из метатега, который выдаёт кабинет. Пусто — метатег не вставляется.
# Та же метка — в хабе (gabella-hub, content.VERIFY): кабинеты проверяют корень домена gabella.site.
# Bing Webmaster Tools подключён импортом из Search Console и метки не требует; msvalidate.01 — запасной путь.
VERIFY = {
    'msvalidate.01': '73FA74F8B7D415104D305A58E9706FE7',   # Bing Webmaster Tools → Settings → Verification → HTML Meta Tag
}

BRAND = 'Gabella'
HOME_NAME = {'ru': 'Главная', 'en': 'Home', 'uk': 'Головна'}
SITE_NAME = BRAND   # WebSite.name: the site name Google shows, the same on every language (the header says what the site is)
TOOLS_NAME = {'ru': 'Инструменты', 'en': 'Tools', 'uk': 'Інструменти'}
PRIVACY_NAME = {'ru': 'Конфиденциальность', 'en': 'Privacy', 'uk': 'Конфіденційність'}
PLAY_NAME = {'ru': 'В игре', 'en': 'In game', 'uk': 'У грі'}
ROSTER_NAME = {'ru': 'Игроки', 'en': 'Players', 'uk': 'Гравці'}
PROFILE_NAME = {'ru': 'Мой профиль', 'en': 'My profile', 'uk': 'Мій профіль'}
CHAR_NAME = {'ru': 'Мой персонаж', 'en': 'My character', 'uk': 'Мій персонаж'}
PLAYER_NAME = {'ru': 'Игрок WoW Forever', 'en': 'WoW Forever player', 'uk': 'Гравець WoW Forever'}
# Inner pages whose radio, search, profile and analytics files wait for the hero picture like on the home (build.late)
LATE_INNER = ('play/', 'guides/', 'classes/', 'races/', 'talents/')   # talents/: no picture, the files wake after the load
NOINDEX = {'profile/', 'u/', 'character/'} | (set() if build.SOCIAL else {'roster/'})   # personal pages: noindex in the page (build_me.py), left out of sitemap.xml


def t(ru, en, uk):
    return {'ru': ru, 'en': en, 'uk': uk}


# ---------- titles and descriptions: by page path (site-relative, without language prefix) ----------
# Под реальные запросы, по факту содержимого страницы. Длина: title до 60, description 120–155 символов (у переводов тоже: i18n/<lang>.json).

META = {
    '': (t('WoW Forever: таланты, тир-лист, Legacy, прокачка, подземелья',
           'WoW Forever Guide: Talents, Tier List, Legacy and Dungeons',
           'WoW Forever: таланти, тір-лист, Legacy, прокачка, підземелля'),
         t('Гайды и справочник по WoW Forever (ВоВ Форевер): таланты и тир-лист по бете, Legacy, прокачка 1–60, подземелья и сбор группы. У каждой цифры источник.',
           'WoW Forever guides and reference: talent builds and a tier list from beta data, Legacy, 1–60 leveling, dungeons and a group builder. Every number sourced.',
           'Гайди й довідник WoW Forever (ВоВ Форевер): таланти й тір-лист за бетою, Legacy, прокачка 1–60, підземелля і збір групи. У кожної цифри джерело.')),
    'classes/': (t('Классы WoW Forever: какой класс выбрать, сравнение всех 9',
                   'WoW Forever Classes: Best Class to Play, All 9 Compared',
                   'Класи WoW Forever: який клас обрати, порівняння всіх 9'),
                 t('Какой класс выбрать в WoW Forever: девять классов по три специализации, роли танк/лекарь/урон, кто качается быстрее и чем каждый полезен рейду.',
                   'Which class to pick in WoW Forever: nine classes with three specs each, tank/healer/DPS roles, which level fastest and what each brings to a raid.',
                   'Який клас обрати у WoW Forever: дев’ять класів по три спеціалізації, ролі танк/цілитель/шкода, хто качається швидше і чим кожен корисний рейду.')),
    'races/': (t('Расы и классы WoW Forever: все 10 рас и расовые способности',
                 'WoW Forever Races: Racials and Race/Class Combos for All 10',
                 'Раси й класи WoW Forever: усі 10 рас і расові здібності'),
               t('Пять рас за Альянс и пять за Орду, включая новых Скайборнов: какие классы доступны каждой расе и что дают её четыре расовые способности.',
                 'Five races per faction, including the new Skyborne: which classes each race can play and what its four racial abilities do.',
                 'П’ять рас за Альянс і п’ять за Орду, разом із новими Скайборнами: які класи доступні кожній расі та що дають її чотири расові здібності.')),
    'tools/': (t('Инструменты WoW Forever: сравнение классов и рас, группа',
                 'WoW Forever Tools: Class and Race Compare, Party Frames',
                 'Інструменти WoW Forever: порівняння класів і рас, група'),
               t('Сравнение классов и рас WoW Forever бок о бок, рамки группы и рейдовая сетка как в игре, поиск по всему сайту.',
                 'Compare WoW Forever classes and races side by side, in-game style party frames and raid grid, and search across the whole guide.',
                 'Порівняння класів і рас WoW Forever пліч-о-пліч, рамки групи та рейдова сітка як у грі, пошук по всьому сайту.')),
    'guides/': (t('Гайды WoW Forever: прокачка, подземелья, профессии, FAQ',
                  'WoW Forever Guides: Leveling, Dungeons, Professions, FAQ',
                  'Гайди WoW Forever: прокачка, підземелля, професії, FAQ'),
                t('Все гайды по WoW Forever в одном месте: маршрут прокачки 1–60, список подземелий и рейдов, профессии под класс, ответы на вопросы и новости.',
                  'All WoW Forever guides in one place: a 1–60 leveling route, the dungeon and raid list, professions for your class, answers to common questions and news.',
                  'Усі гайди по WoW Forever (ВоВ Форевер) в одному місці: маршрут прокачки 1–60, список підземель і рейдів, професії під клас, відповіді на питання та новини.')),
    'guides/leveling/': (t('Гайд по прокачке WoW Forever 1–60: зоны по уровням',
                           'WoW Forever Leveling Guide 1–60: Zones by Level',
                           'Гайд з прокачки WoW Forever 1–60: зони за рівнями'),
                         t('Прокачка в WoW Forever с 1 до 60: маршрут по зонам за Альянс и Орду, отдых и бонусы опыта, советы соло, вдвоём и группой, Legacy и лагерь.',
                           'Level 1 to 60 in WoW Forever: a zone-by-zone route for Alliance and Horde, rested XP and experience bonuses, solo, duo and group tips, Legacy and the camp.',
                           'Прокачка у WoW Forever з 1 до 60: маршрут зонами за Альянс і Орду, відпочинок і бонуси досвіду, поради соло, удвох і групою, Legacy та табір.')),
    'guides/leveling-warrior/': (t('Прокачка Воина в WoW Forever: таланты и спек 1–60', 'Warrior Leveling Guide 1–60 in WoW Forever: Protection', 'Гайд з прокачування Воїна 1–60 у WoW Forever: Захист'),
                                      t('Как качать Воина в WoW Forever: почему Защита, таланты по уровням 10–60, что брать у тренера, ротация соло и в группе, отличия от Classic. По данным беты.', 'How to level a Warrior in WoW Forever: Protection, talents by level 10–60, rotation, differences from Classic. Beta data.', 'Як прокачувати Воїна у WoW Forever: Захист, таланти за рівнями 10–60, ротація, відмінності від Classic. За бетою.')),
    'guides/leveling-paladin/': (t('Прокачка Паладина в WoW Forever: Воздаяние, таланты 1–60', 'Paladin Leveling Guide 1–60 in WoW Forever: Retribution', 'Гайд з прокачування Паладина 1–60 у WoW Forever: Відплата'),
                                      t('Как качать Паладина в WoW Forever: Воздаяние или Защита, таланты по уровням 10–60, печати и ротация, что брать у тренера, отличия от Classic. По бете.', 'How to level a Paladin in WoW Forever: Retribution, talents by level 10–60, seals, differences from Classic. Beta data.', 'Як прокачувати Паладина у WoW Forever: Відплата, таланти за рівнями 10–60, печатки, відмінності від Classic. За бетою.')),
    'guides/builds-paladin/': (t('Билды Паладина в WoW Forever: таланты и приоритет', 'WoW Forever Paladin Builds: Prot, Holy, Ret Talents', 'Білди Паладина у WoW Forever: таланти й пріоритет'),
                               t('Билды Паладина в WoW Forever: Защита, Свет и Воздаяние — ключевые таланты, приоритет в группе, характеристики. По бете, обновим после старта.',
                                 'WoW Forever Paladin builds for Protection, Holy and Retribution: key talents, group priorities and stats. Beta data, updated after launch.',
                                 'Білди Паладина у WoW Forever: Захист, Світло й Відплата — ключові таланти, пріоритет у групі, характеристики. За бетою, оновимо після старту.')),
    'guides/builds-warrior/': (t('Билды Воина в WoW Forever: таланты и приоритет', 'WoW Forever Warrior Builds: Prot, Fury, Arms Talents', 'Білди Воїна у WoW Forever: таланти й пріоритет'),
                               t('Билды Воина в WoW Forever: Защита, Неистовство и Оружие — ключевые таланты, приоритет в группе, характеристики. По бете, обновим после старта.',
                                 'WoW Forever Warrior builds for Protection, Fury and Arms: key talents, group priorities and stats. Beta data, updated after launch.',
                                 'Білди Воїна у WoW Forever: Захист, Лють і Зброя — ключові таланти, пріоритет у групі, характеристики. За бетою, оновимо після старту.')),
    'guides/builds-mage/': (t('Билды Мага в WoW Forever: таланты и приоритет', 'WoW Forever Mage Builds: Arcane, Fire, Frost Talents', 'Білди Мага у WoW Forever: таланти й пріоритет'),
                            t('Билды Мага в WoW Forever: Тайная магия, Огонь и Лёд — ключевые таланты, приоритет заклинаний, характеристики. По бете, обновим после старта.',
                              'WoW Forever Mage builds for Arcane, Fire and Frost: key talents, spell priorities and stats. Beta data, updated after launch.',
                              'Білди Мага у WoW Forever: Тайна магія, Вогонь і Лід — ключові таланти, пріоритет заклинань, характеристики. За бетою, оновимо після старту.')),
    'guides/builds-hunter/': (t('Билды Охотника в WoW Forever: таланты и приоритет', 'WoW Forever Hunter Builds: BM, MM, Survival Talents', 'Білди Мисливця у WoW Forever: таланти й пріоритет'),
                            t('Билды Охотника в WoW Forever: Повелитель зверей, Стрельба и Выживание — ключевые таланты, приоритет в группе, характеристики. По бете, обновим после старта.',
                              'WoW Forever Hunter builds for Beast Mastery, Marksmanship and Survival: key talents, group priorities and stats. Beta data, updated after launch.',
                              'Білди Мисливця у WoW Forever: Володіння звірами, Стрільба й Виживання — ключові таланти, пріоритет у групі, характеристики. За бетою, оновимо після старту.')),
    'guides/builds-rogue/': (t('Билды Разбойника в WoW Forever: таланты и приоритет', 'WoW Forever Rogue Builds: Assassination, Combat, Sub', 'Білди Розбійника у WoW Forever: таланти й пріоритет'),
                            t('Билды Разбойника в WoW Forever: Ликвидация, Бой и Скрытность — ключевые таланты, приоритет в группе, характеристики. По бете, обновим после старта.',
                              'WoW Forever Rogue builds for Assassination, Combat and Subtlety: key talents, group priorities and stats. Beta data, updated after launch.',
                              'Білди Розбійника у WoW Forever: Ліквідація, Бій і Непомітність — ключові таланти, пріоритет у групі, характеристики. За бетою, оновимо після старту.')),
    'guides/builds-priest/': (t('Билды Жреца в WoW Forever: таланты и приоритет', 'WoW Forever Priest Builds: Disc, Holy, Shadow Talents', 'Білди Жреця у WoW Forever: таланти й пріоритет'),
                            t('Билды Жреца в WoW Forever: Послушание, Свет и Темная магия — ключевые таланты, приоритет лечения и урона, характеристики. По бете, обновим после старта.',
                              'WoW Forever Priest builds for Discipline, Holy and Shadow: key talents, healing and damage priorities and stats. Beta data, updated after launch.',
                              'Білди Жреця у WoW Forever: Послух, Світло й Темрява — ключові таланти, пріоритет лікування й шкоди, характеристики. За бетою, оновимо після старту.')),
    'guides/builds-shaman/': (t('Билды Шамана в WoW Forever: таланты и приоритет', 'WoW Forever Shaman Builds: Ele, Enh, Resto Talents', 'Білди Шамана у WoW Forever: таланти й пріоритет'),
                            t('Билды Шамана в WoW Forever: Стихии, Совершенствование и Исцеление — ключевые таланты, приоритет в группе, характеристики. По бете, обновим после старта.',
                              'WoW Forever Shaman builds for Elemental, Enhancement and Restoration: key talents, group priorities and stats. Beta data, updated after launch.',
                              'Білди Шамана у WoW Forever: Стихії, Вдосконалення й Зцілення — ключові таланти, пріоритет у групі, характеристики. За бетою, оновимо після старту.')),
    'guides/builds-warlock/': (t('Билды Чернокнижника в WoW Forever: таланты и приоритет', 'WoW Forever Warlock Builds: Affliction, Demo, Destro', 'Білди Чорнокнижника у WoW Forever: таланти й пріоритет'),
                            t('Билды Чернокнижника в WoW Forever: Колдовство, Демонология и Разрушение — ключевые таланты, приоритет, характеристики. По бете, обновим после старта.',
                              'WoW Forever Warlock builds for Affliction, Demonology and Destruction: key talents, priorities and stats. Beta data, updated after launch.',
                              'Білди Чорнокнижника у WoW Forever: Прокляття, Демонологія й Руйнування — ключові таланти, пріоритет, характеристики. За бетою, оновимо після старту.')),
    'guides/builds-druid/': (t('Билды Друида в WoW Forever: таланты и приоритет', 'WoW Forever Druid Builds: Balance, Feral, Resto Talents', 'Білди Друїда у WoW Forever: таланти й пріоритет'),
                            t('Билды Друида в WoW Forever: Баланс, Сила зверя и Исцеление — ключевые таланты, приоритет в группе, характеристики. По бете, обновим после старта.',
                              'WoW Forever Druid builds for Balance, Feral and Restoration: key talents, group priorities and stats. Beta data, updated after launch.',
                              'Білди Друїда у WoW Forever: Баланс, Сила звіра й Зцілення — ключові таланти, пріоритет у групі, характеристики. За бетою, оновимо після старту.')),
    'guides/leveling-hunter/': (t('Прокачка Охотника в WoW Forever: таланты и питомец 1–60', 'Hunter Leveling Guide 1–60 in WoW Forever: Beast Mastery', 'Гайд з прокачування Мисливця 1–60 у WoW Forever'),
                                      t('Как качать Охотника в WoW Forever: Повелитель зверей, таланты по уровням 10–60, какого питомца приручить, ротация, ловушки и отличия от Classic. По бете.', 'How to level a Hunter in WoW Forever: Beast Mastery, talents by level 10–60, pets, differences from Classic. Beta data.', 'Як прокачувати Мисливця у WoW Forever: Володіння звірами, таланти за рівнями 10–60, улюбленці, відмінності від Classic. За бетою.')),
    'guides/leveling-rogue/': (t('Прокачка Разбойника в WoW Forever: Бой, таланты 1–60', 'Rogue Leveling Guide 1–60 in WoW Forever: Combat', 'Гайд з прокачування Розбійника 1–60 у WoW Forever: Бій'),
                                      t('Как качать Разбойника в WoW Forever: почему Бой, таланты по уровням 10–60, яды, очки серии, ротация соло и в группе, отличия от Classic. По данным беты.', 'How to level a Rogue in WoW Forever: Combat, talents by level 10–60, poisons, differences from Classic. Beta data.', 'Як прокачувати Розбійника у WoW Forever: Бій, таланти за рівнями 10–60, отрути, відмінності від Classic. За бетою.')),
    'guides/leveling-priest/': (t('Прокачка Жреца в WoW Forever: Темная магия, таланты 1–60', 'Priest Leveling Guide 1–60 in WoW Forever: Shadow', 'Гайд з прокачування Жерця 1–60 у WoW Forever: Темрява'),
                                      t('Как качать Жреца в WoW Forever: Темная магия или Послушание, таланты по уровням 10–60, жезл и мана, ротация соло и в группе, отличия от Classic. По бете.', 'How to level a Priest in WoW Forever: Shadow, talents by level 10–60, wand, differences from Classic. Beta data.', 'Як прокачувати Жерця у WoW Forever: Темрява, таланти за рівнями 10–60, паличка, відмінності від Classic. За бетою.')),
    'guides/leveling-shaman/': (t('Прокачка Шамана в WoW Forever: Совершенствование, таланты', 'Shaman Leveling Guide 1–60 in WoW Forever: Enhancement', 'Гайд з прокачування Шамана 1–60 у WoW Forever: Вдосконалення'),
                                      t('Как качать Шамана в WoW Forever: Совершенствование, таланты по уровням 10–60, тотемы и задания на них, мана и ротация, отличия от Classic. По данным беты.', 'How to level a Shaman in WoW Forever: Enhancement, talents by level 10–60, totems, differences from Classic. Beta data.', 'Як прокачувати Шамана у WoW Forever: Вдосконалення, таланти за рівнями 10–60, тотеми, відмінності від Classic. За бетою.')),
    'guides/leveling-mage/': (t('Прокачка Мага в WoW Forever: Лёд, таланты 1–60', 'Mage Leveling Guide 1–60 in WoW Forever: Frost', 'Гайд з прокачування Мага 1–60 у WoW Forever: Лід'),
                                      t('Как качать Мага в WoW Forever: почему Лёд, таланты по уровням 10–60, Ледяное копьё и Ледяные пальцы, ротация соло и по площади, отличия от Classic. По бете.', 'How to level a Mage in WoW Forever: Frost, talents by level 10–60, Ice Lance, differences from Classic. Beta data.', 'Як прокачувати Мага у WoW Forever: Лід, таланти за рівнями 10–60, Ice Lance, відмінності від Classic. За бетою.')),
    'guides/leveling-warlock/': (t('Прокачка Чернокнижника в WoW Forever: Колдовство, таланты', 'Warlock Leveling Guide 1–60 in WoW Forever: Affliction', 'Гайд з прокачування Чорнокнижника 1–60 у WoW Forever'),
                                      t('Как качать Чернокнижника в WoW Forever: Колдовство, таланты по уровням 10–60, демоны и задания, Жизнеотвод и Похищение жизни, отличия от Classic. По бете.', 'How to level a Warlock in WoW Forever: Affliction, talents by level 10–60, demons, differences from Classic. Beta data.', 'Як прокачувати Чорнокнижника у WoW Forever: Прокляття, таланти за рівнями 10–60, демони, відмінності від Classic. За бетою.')),
    'guides/leveling-druid/': (t('Прокачка Друида в WoW Forever: Сила зверя, таланты 1–60', 'Druid Leveling Guide 1–60 in WoW Forever: Feral', 'Гайд з прокачування Друїда 1–60 у WoW Forever: Сила звіра'),
                                      t('Как качать Друида в WoW Forever: кошка и медведь, таланты по уровням 10–60, облики и задания на них, ротация соло и в группе, отличия от Classic. По бете.', 'How to level a Druid in WoW Forever: Feral, talents by level 10–60, forms, differences from Classic. Beta data.', 'Як прокачувати Друїда у WoW Forever: Сила звіра, таланти за рівнями 10–60, форми, відмінності від Classic. За бетою.')),
    'guides/dungeons/': (t('Подземелья WoW Forever по уровням: все 35 и рейды',
                           'WoW Forever Dungeons by Level: All 35 Dungeons and Raids',
                           'Підземелля WoW Forever за рівнями: усі 35 і рейди'),
                         t('Все 35 подземелий WoW Forever по уровням и где вход, с фильтром под уровень вашего персонажа, три рейда с датами открытия и состав группы.',
                           'All 35 WoW Forever dungeons by level with entrance locations and a filter for your level, the three raids with opening dates, and group composition.',
                           'Усі 35 підземель WoW Forever за рівнями та де вхід, з фільтром під рівень персонажа, три рейди з датами відкриття та склад групи.')),
    'guides/professions/': (t('Лучшие профессии WoW Forever: пары под класс и для золота', 'Best WoW Forever Professions: Class Pairs and Gold', 'Найкращі професії WoW Forever: пари під клас і золото'),
                            t('Какие две профессии взять в WoW Forever: пары для прокачки и 60 уровня на 9 классов, что продавать на аукционе, ящики Waylaid Crate и Merchant’s Favor.', 'Which two professions to pick in WoW Forever: pairs for leveling and level 60 for 9 classes, what to sell, Waylaid Crates and Merchant’s Favor.', 'Які дві професії взяти в WoW Forever: пари для прокачування й 60 рівня на 9 класів, що продавати, ящики Waylaid Crate і Merchant’s Favor.')),
    'guides/transport/': (t('Корабли, дирижабли и полёты WoW Forever: маршруты', 'WoW Forever Boats, Zeppelins and Flight Paths', 'Кораблі, дирижаблі та польоти WoW Forever: маршрути'),
                          t('Все корабли и дирижабли WoW Forever: откуда, куда и где посадка за Альянс и Орду, новая гавань Штормграда, Zephras Isle, точки полёта 1–30.', 'Every WoW Forever boat and zeppelin: from where, to where and where to board for Alliance and Horde, the new Stormwind Harbor, Zephras Isle, flights 1–30.', 'Усі кораблі й дирижаблі WoW Forever: звідки, куди й де посадка за Альянс і Орду, нова гавань Stormwind, Zephras Isle, точки польоту 1–30.')),
    'guides/addons/': (t('Аддоны для WoW Forever: что работает и как установить', 'WoW Forever Addons: What Works and How to Install', 'Аддони для WoW Forever: що працює та як встановити'),
                       t('Какие аддоны работают в WoW Forever: Questie, Details!, DBM, Auctionator, Baganator. Что уже встроено в игру, как установить и почему аддон не грузится.', 'Which addons work in WoW Forever: Questie, Details!, DBM, Auctionator, Baganator. What is built in, how to install them and why an addon won’t load.', 'Які аддони працюють у WoW Forever: Questie, Details!, DBM, Auctionator, Baganator. Що вже вбудовано в гру, як встановити та чому аддон не завантажується.')),
    'guides/faq/': (t('WoW Forever FAQ: дата и время выхода, цена, подписка',
                      'WoW Forever FAQ: Release Date and Time, Price, Subscription',
                      'FAQ WoW Forever: коли вийде, ціна, підписка, чи безкоштовна'),
                    t('Когда выходит WoW Forever, нужна ли подписка, сколько стоят наборы, какие режимы игры, когда занимать имя и чем Forever отличается от Classic Era.',
                      'When WoW Forever launches, whether you need a subscription, pack prices, game modes, when to reserve a name and how Forever differs from Classic Era.',
                      'Коли виходить WoW Forever (5.11, 01:00 за Києвом), чи безкоштовна гра, ціна підписки й наборів, режими, резерв імен і відмінності від Classic Era.')),
    'guides/best-race/': (t('Лучшая раса для каждого класса в WoW Forever: PvE и PvP', 'Best Race for Every Class in WoW Forever: PvE and PvP', 'Найкраща раса для кожного класу у WoW Forever: PvE і PvP'),
                 t('Лучшая раса для каждого класса в WoW Forever: сочетания расы и класса за Альянс и Орду, выбор для PvE и PvP, расовые способности Forever и отличия от Classic.', 'Best race for every class in WoW Forever: race and class combos for Alliance and Horde, PvE and PvP picks, Forever racials and what changed from Classic.', 'Найкраща раса для кожного класу у WoW Forever: комбінації раси й класу для Альянсу та Орди, PvE та PvP, расові здібності Forever і відмінності від Classic.')),
    'guides/builds/': (t('Билды WoW Forever: таланты всех 9 классов', 'WoW Forever Builds: Talents for All 9 Classes', 'Білди WoW Forever: таланти всіх 9 класів'),
                 t('Билды WoW Forever для 9 классов и 27 спеков: таланты, приоритет, характеристики и полный калькулятор на 51 очко. Раскладку к 60 добавим после старта.',
                   'WoW Forever builds for all 9 classes and 27 specs: talents, priorities, stats and a full 51-point calculator. The level 60 layout follows after launch.',
                   'Білди WoW Forever для 9 класів і 27 спеціалізацій: таланти, пріоритет, характеристики й повний калькулятор на 51 очко. Розкладку до 60 додамо після старту.')),
    # 'guides/tier-list/': content.tierlist_live.meta() below (the status and the date of data/tierlist.json)
    'guides/pvp/': (t('PvP в WoW Forever: звания, Честь, награды и поля боя', 'WoW Forever PvP: Ranks, Honor, Rewards and Battlegrounds', 'PvP у WoW Forever: звання, Честь, нагороди й поля бою'),
                 t('Как устроено PvP в WoW Forever по данным Blizzard: Честь и очки звания, награды званий 1–14, наборы за Честь и Emboldened Seal, сезоны, Darkspear Islands.',
                   'How PvP works in WoW Forever per Blizzard: Honor and Rank Points, rewards for ranks 1–14, Honor gear and Emboldened Seals, seasons, Darkspear Islands.',
                   'Як влаштовано PvP у WoW Forever за даними Blizzard: Честь і очки звання, нагороди звань 1–14, набори за Честь і Emboldened Seal, сезони, Darkspear Islands.')),
    'guides/legacy/': (t('Система Legacy в WoW Forever: очки, перки и награды', 'WoW Forever Legacy System: Points, Perks and Rewards', 'Система Legacy у WoW Forever: очки, перки та нагороди'),
                 t('Как работает Legacy в WoW Forever: где взять очки Legacy, все 65 испытаний, перки трёх деревьев, лимит 16 очков на персонажа на старте и четыре награды.', 'How Legacy works in WoW Forever: where to get Legacy points, all 65 challenges, perks in three trees, the 16-point limit at launch and four rewards.', 'Як працює Legacy у WoW Forever: де брати очки Legacy, усі 65 випробувань, перки трьох дерев, ліміт 16 очок на персонажа на старті та чотири нагороди.')),
    'guides/launch-checklist/': (t('Чек-лист старта WoW Forever: что сделать в день 1', 'WoW Forever Launch Checklist: What to Do on Day 1', 'Чек-лист старту WoW Forever: що зробити в день 1'),
                 t('Чек-лист к старту WoW Forever 05.11: подписка, клиент, режим, класс и имя до старта, затем первые часы и первый вечер. Отметки хранятся в браузере.',
                   'WoW Forever launch checklist for Nov 4–5: subscription, client, mode, class and name before launch, then the first hours and evening. Ticks stay saved.',
                   'Чек-лист до старту WoW Forever 05.11: підписка, клієнт, режим, клас та ім’я до старту, далі перші години й перший вечір. Позначки зберігаються в браузері.')),
    'guides/launch-day/': (t('Старт WoW Forever: время, очереди и статус серверов', 'WoW Forever Launch Time, Queues and Server Status', 'Коли вийде WoW Forever: час старту за Києвом, черги'),
                 t('Во сколько старт WoW Forever: 04.11 в 15:00 PST (23:00 UTC), в Европе 5 ноября. Время по городам, отсчёт, очереди и где проверить, не упали ли серверы.',
                   'WoW Forever launch time in every time zone: Nov 4, 15:00 PST (23:00 UTC), Nov 5 in Europe. Countdown, login queues and where to check if servers are down.',
                   'WoW Forever виходить 5 листопада о 01:00 за Києвом (04.11, 23:00 UTC). Зворотний відлік, черги, шари й де перевірити, чи не впали сервери.')),
    'guides/name-reservation/': (t('Резерв имён WoW Forever закончился 03.11', 'WoW Forever Name Reservation Ended on 03.11', 'Резерв імен WoW Forever закінчився 03.11'),
                 t('Ранний резерв имён WoW Forever шёл с 27.10 по 03.11 и закончился. Кому был доступен, как работал, правила имён и что делать, если имя занято.',
                   'WoW Forever early name reservation ran from 27.10 to 03.11 and has ended. Who could use it, how it worked, name rules and what to do if a name is taken.',
                   'Ранній резерв імен WoW Forever тривав з 27.10 по 03.11 і закінчився. Кому був доступний, як працював, правила імен і що робити, якщо ім’я зайняте.')),
    'guides/server-status/': (t('Статус серверов WoW Forever: очередь и техработы', 'WoW Forever Server Status: Login Queue and Maintenance', 'Статус серверів WoW Forever: черга й техроботи'),
                 t('Статус серверов WoW Forever и очередь на вход: официальные каналы Blizzard, как работают очереди и слои, техработы и что известно о времени ожидания.',
                   'WoW Forever server status and login queue: official Blizzard channels, how queues and layers work, maintenance and what is known about wait times.',
                   'Статус серверів WoW Forever і черга на вхід: офіційні канали Blizzard, як працюють черги й шари, техроботи та що відомо про час очікування.')),
    'guides/requirements/': (t('Системные требования WoW Forever: ПК и Mac',
                               'WoW Forever System Requirements: PC and Mac',
                               'Системні вимоги WoW Forever: ПК і Mac'),
                             t('Минимальные и рекомендуемые системные требования WoW Forever для Windows и Mac: процессор, видеокарта, ОЗУ, SSD на 128 ГБ, старые видеокарты.',
                               'Minimum and recommended WoW Forever system requirements for Windows and Mac: CPU, graphics card, RAM, a 128 GB SSD, and older cards.',
                               'Мінімальні й рекомендовані системні вимоги WoW Forever (ВоВ Форевер) для Windows і Mac: процесор, відеокарта, ОЗП, SSD на 128 ГБ, старі відеокарти.')),
    'guides/news/': (t('Новости WoW Forever: бета, релиз и патчи',
                       'WoW Forever News: Beta, Launch and Patches',
                       'Новини WoW Forever: бета, реліз і патчі'),
                     t('Новости WoW Forever перед релизом: закрытие беты, конец резерва имён 03.11, изменения рас и классов в патчах беты, Даларан и свежая лента Wowhead.',
                       'WoW Forever news before launch: the beta closing, the end of name reservation on 03.11, race and class changes in beta patches, Dalaran and the Wowhead feed.',
                       'Новини WoW Forever перед релізом: закриття бети, кінець резерву імен 03.11, зміни рас і класів у патчах бети, Даларан і свіжа стрічка Wowhead.')),
    'guides/glossary/': (t('Словарь терминов WoW Forever: спек, билд, BiS, Legacy', 'WoW Forever Glossary: Spec, Build, BiS, Legacy', 'Словник термінів WoW Forever: спек, білд, BiS, Legacy'),
                         t('Что значат спек, билд, тир-лист, ротация, BiS, агро, Legacy, перки и лагерь в WoW Forever: короткие определения для новичка.',
                           'What spec, build, tier list, rotation, BiS, aggro, Legacy, perks and the camp mean in WoW Forever: short definitions for new players.',
                           'Що означають спек, білд, тир-лист, ротація, BiS, агро, Legacy, перки й табір у WoW Forever: короткі визначення для новачка.')),
    'guides/ukrainian/': ({'uk': 'WoW Forever українською: аддони UA_Forever і UALL Forever'},   # only uk
                          {'uk': 'Української мови у WoW Forever немає. Який аддон перекладу обрати, як встановити його через CurseForge чи вручну і як побачити оригінал.'}),
    'play/': (t('WoW Forever: второй экран — радио, зоны по уровню, таймеры',
                'WoW Forever Second Screen: Radio, Zones by Level, Timers',
                'WoW Forever: другий екран — радіо, зони за рівнем, таймери'),
              t('Держите открытым во время игры: фэнтези-радио, куда идти на вашем уровне за Альянс или Орду, подземелья под уровень и таймеры с сигналом.',
                'Keep it open while you play: fantasy radio, where to level next for Alliance or Horde, dungeons for your level and timers with an alert.',
                'Тримайте відкритим під час гри: фентезі-радіо, куди йти на вашому рівні за Альянс чи Орду, підземелля під рівень і таймери із сигналом.')),
    'roster/': (t('Игроки WoW Forever: найти группу и крафтера',
                  'WoW Forever Players: Find a Group or a Crafter',
                  'Гравці WoW Forever: знайти групу й крафтера'),
                t('Игроки WoW Forever: кто сейчас ищет группу, класс, роль, профессии и время игры. Нашли — напишите в игре через /w.',
                  'WoW Forever players: who is looking for a group now, class, role, professions and play time. Found someone? Whisper them in game with /w.',
                  'Гравці WoW Forever: хто зараз шукає групу, клас, роль, професії та час гри. Знайшли — напишіть у грі через /w.')),
    'profile/': (t('Мой профиль WoW Forever · Gabella', 'My Profile — WoW Forever Guide', 'Мій профіль WoW Forever · Gabella'),
                 t('Ваши персонажи, достижения, ранги и рамки портрета на Gabella. Вход через Discord, Google, Battle.net, Telegram или почту.',
                   'Your characters, achievements, ranks and portrait frames in the Gabella guide. Log in with Discord, Google, Battle.net, Telegram or email.',
                   'Ваші персонажі, досягнення, ранги й рамки портрета на Gabella. Вхід через Discord, Google, Battle.net, Telegram або пошту.')),
    'character/': (t('Мой персонаж WoW Forever · Gabella', 'My Character — WoW Forever Guide', 'Мій персонаж WoW Forever · Gabella'),
                   t('Персонаж без входа: класс, спек и раса со звездой лучшей по источникам. Сайт покажет сборку талантов, пары профессий, подземелья под уровень и сброс недели.',
                     'A character without a login: class, spec and race with the best one starred by the sources. The guide shows your talent build, profession pairs, dungeons for your level and the weekly reset.',
                     'Персонаж без входу: клас, спек і раса із зіркою найкращої за джерелами. Сайт покаже збірку талантів, пари професій, підземелля під рівень і скидання тижня.')),
    'u/': (t('Игрок WoW Forever · Gabella', 'Player — WoW Forever Guide', 'Гравець WoW Forever · Gabella'),
           t('Карточка игрока на Gabella: персонажи в WoW Forever, ранг, рамка и достижения.',
             'Player card in the Gabella guide: WoW Forever characters, rank, frame and achievements.',
             'Картка гравця на Gabella: персонажі у WoW Forever, ранг, рамка й досягнення.')),
    'privacy/': (t('Конфиденциальность WoW Forever · Gabella',
                   'Privacy — WoW Forever Guide',
                   'Конфіденційність WoW Forever · Gabella'),
                 t('Какие данные собирает Gabella, справочник WoW Forever: профиль после входа, статистика без cookies, что хранится в браузере, как скачать и удалить данные.',
                   'What data the Gabella WoW Forever guide collects: profile after sign-in, cookieless statistics, browser storage, and how to download and delete your data.',
                   'Які дані збирає Gabella, довідник WoW Forever: профіль після входу, статистика без cookies, що зберігається в браузері, як завантажити й видалити дані.')),
}

CLASS_T = t('{n} в WoW Forever: гайд, спеки и лучшая раса', 'WoW Forever {n} Guide: Specs, Best Race, Abilities', '{n} у WoW Forever: гайд, спеки й найкраща раса')   # «best race for warlock»: suggestions 27.10
CLASS_T_SHORT = t('{n} в WoW Forever: {specs}', 'WoW Forever {n}: {specs}', '{n} у WoW Forever: {specs}')   # when the full one is over 65
CLASS_D = t('{n} в WoW Forever: {specs} — ключевые способности, расы, польза в группе, плюсы, минусы и что нового.',
            'WoW Forever {n} guide: {specs} specs, key abilities, races, group value, pros and cons, and what is new.',
            '{n} у WoW Forever: {specs} — ключові здібності, раси, користь у групі, плюси, мінуси та що нового.')
RACE_T = t('{n} в WoW Forever: расовые способности и классы', 'WoW Forever {n} Racials and Classes Guide', '{n} у WoW Forever: расові здібності та класи')
RACE_T_SHORT = t('{n} в WoW Forever: расовые способности, классы', 'WoW Forever {n}: Racials and Classes', '{n} у WoW Forever: расові здібності, класи')   # when the full one is over 60
RACE_D = t('{n} в WoW Forever: четыре расовые способности, доступные и лучшие классы, столица {cap}, стартовая зона {zone}.',
           'WoW Forever {n} guide: four racial abilities, available and best classes, capital {cap}, starting zone {zone}.',
           '{n} у WoW Forever: чотири расові здібності, доступні та найкращі класи, столиця {cap}, стартова зона {zone}.')
AND = {'ru': ' и ', 'en': ' and ', 'uk': ' і '}
# Link previews (og:*, twitter:*) that differ from the search title and description: what a player sees in Discord and chats
OG = {
    'tools/': (t('Состав группы WoW Forever: пати и рейд по ролям',
                 'WoW Forever Group Builder: Party and Raid by Roles',
                 'Склад групи WoW Forever: паті й рейд за ролями'),
               t('Соберите группу на 5, 10, 20 или 40 игроков: танки, лекари и урон по классам и расам, со ссылкой, которую можно отправить.',
                 'Build a group of 5, 10, 20 or 40 players: tanks, healers and damage by class and race, with a link you can share.',
                 'Зберіть групу на 5, 10, 20 чи 40 гравців: танки, цілителі та шкода за класами й расами, з посиланням, яке можна надіслати.')),   # a group link (#t=) carries no title: the card speaks about the group builder
    '': (t('WoW Forever: Legacy, тир-лист, конструктор группы',
           'WoW Forever: Legacy, Tier List, Group Builder',
           'WoW Forever: Legacy, тір-лист, конструктор групи'),
         t('Legacy: 65 испытаний и перки трёх деревьев. Тир-лист классов по бете, конструктор группы и рейда, новости. Старт 04.11 в 23:00 UTC (по Киеву 5.11, 01:00).',
           'Legacy: 65 challenges and perks in three trees. Class tier list from beta data, group and raid builder, news. Launch Nov 4 at 23:00 UTC.',
           'Legacy: 65 випробувань і перки трьох дерев. Тір-лист класів за бетою, конструктор групи й рейду, новини. Старт 04.11 о 23:00 UTC (за Києвом 5.11, 01:00).')),
}
# ---------- Talent calculator: talents/ and talents/<class>/ (build_guides.calc_page, talents.render_calc) ----------
# Every text of these pages that a search engine reads is here, in all nine languages: the title, the h1, the lead, the description.
# Queries (suggestions 29.10): «WoW Forever <class> talent calculator», «<class> talents», «talent tree», «калькулятор талантов <класс>».
# {n} the class as the site names it, {g} its genitive (ru, uk), {s} the three trees of the class.
CALC_NAME = {'ru': 'Калькулятор талантов', 'en': 'Talent calculator', 'uk': 'Калькулятор талантів', 'de': 'Talentrechner',
             'fr': 'Calculateur de talents', 'es': 'Calculadora de talentos', 'pt': 'Calculadora de talentos',
             'it': 'Calcolatore di talenti', 'pl': 'Kalkulator talentów'}
CALC_GEN = {'ru': {'warrior': 'Воина', 'paladin': 'Паладина', 'hunter': 'Охотника', 'rogue': 'Разбойника', 'priest': 'Жреца',
                   'shaman': 'Шамана', 'mage': 'Мага', 'warlock': 'Чернокнижника', 'druid': 'Друида'},
            'uk': {'warrior': 'Воїна', 'paladin': 'Паладина', 'hunter': 'Мисливця', 'rogue': 'Розбійника', 'priest': 'Жреця',
                   'shaman': 'Шамана', 'mage': 'Мага', 'warlock': 'Чорнокнижника', 'druid': 'Друїда'}}
CALC_T = {'ru': 'Калькулятор талантов {g} WoW Forever', 'en': 'WoW Forever {n} Talent Calculator and Build Planner',
          'uk': 'Калькулятор талантів {g} у WoW Forever', 'de': 'WoW Forever Talentrechner: {n}, alle drei Bäume',
          'fr': 'Calculateur de talents {n} pour WoW Forever', 'es': 'Calculadora de talentos de {n} en WoW Forever',
          'pt': 'Calculadora de talentos de {n} no WoW Forever', 'it': '{n}: calcolatore di talenti per WoW Forever',
          'pl': '{n}: kalkulator talentów WoW Forever'}
CALC_H1 = {'ru': 'Калькулятор талантов {g}', 'en': '{n} Talent Calculator', 'uk': 'Калькулятор талантів {g}',
           'de': 'Talentrechner: {n}', 'fr': 'Calculateur de talents {n}', 'es': 'Calculadora de talentos de {n}',
           'pt': 'Calculadora de talentos de {n}', 'it': '{n}: calcolatore di talenti', 'pl': '{n}: kalkulator talentów'}
CALC_D = {'ru': 'Калькулятор талантов {g} в WoW Forever: ветки {s}, 51 очко к 60 уровню, ссылка на свой билд. Раскладка по бете.',
          'en': 'WoW Forever {n} talent calculator: {s} trees, 51 points by level 60, a shareable link to your build. Beta layout.',
          'uk': 'Калькулятор талантів {g} у WoW Forever: гілки {s}, 51 очко до 60 рівня, посилання на свій білд. Розкладка за бетою.',
          'de': 'Talentrechner {n} für WoW Forever: Bäume {s}, 51 Punkte bis Stufe 60, dein Build als Link. Stand der Beta.',
          'fr': 'Calculateur de talents {n} pour WoW Forever : arbres {s}, 51 points au niveau 60, build à partager. Données bêta.',
          'es': 'Calculadora de talentos de {n} en WoW Forever: árboles {s}, 51 puntos a nivel 60, build con enlace. Datos beta.',
          'pt': 'Calculadora de talentos de {n} no WoW Forever: árvores {s}, 51 pontos no nível 60, build por link. Dados da beta.',
          'it': 'Calcolatore di talenti {n} per WoW Forever: alberi {s}, 51 punti al livello 60, build in un link. Dati beta.',
          'pl': 'Kalkulator talentów {n} w WoW Forever: drzewka {s}, 51 punktów na 60 poziomie, twój build w linku. Dane z bety.'}
CALC_LEAD = {'ru': 'Три ветки, 51 очко к 60 уровню, ряды и требования как в игре. Билд сохраняется в браузере, ссылкой можно поделиться.',
             'en': 'Three trees, 51 points by level 60, row and prerequisite rules as in the game. Your build is saved in this browser and shared as a link.',
             'uk': 'Три гілки, 51 очко до 60 рівня, ряди й вимоги як у грі. Білд зберігається в браузері, посиланням можна поділитися.',
             'de': 'Drei Bäume, 51 Punkte bis Stufe 60, Reihen und Voraussetzungen wie im Spiel. Dein Build bleibt im Browser gespeichert und lässt sich als Link teilen.',
             'fr': 'Trois arbres, 51 points au niveau 60, rangées et prérequis comme en jeu. Votre build reste enregistré dans le navigateur et se partage par lien.',
             'es': 'Tres árboles, 51 puntos a nivel 60, filas y requisitos como en el juego. Tu build se guarda en el navegador y se comparte con un enlace.',
             'pt': 'Três árvores, 51 pontos no nível 60, linhas e pré-requisitos como no jogo. Sua build fica salva no navegador e pode ser compartilhada por link.',
             'it': 'Tre alberi, 51 punti al livello 60, file e requisiti come nel gioco. La build resta salvata nel browser e si condivide con un link.',
             'pl': 'Trzy drzewka, 51 punktów na 60 poziomie, rzędy i wymagania jak w grze. Build zapisuje się w przeglądarce, a linkiem można się podzielić.'}
CALC_HUB = {   # talents/: (title, h1, description, lead)
    'ru': ('Калькулятор талантов WoW Forever: все 9 классов', 'Калькулятор талантов WoW Forever',
           'Калькулятор талантов WoW Forever (ВоВ Форевер) для девяти классов: три ветки, 51 очко к 60 уровню, ряды и требования как в игре, ссылка на билд. По бете.',
           'Девять классов, у каждого три ветки и 51 очко к 60 уровню. Выберите класс.'),
    'en': ('WoW Forever Talent Calculator: All 9 Classes', 'WoW Forever Talent Calculator',
           'WoW Forever talent calculator for all nine classes: three trees each, 51 points by level 60, in-game row and prerequisite rules, a shareable build link.',
           'Nine classes, three trees each, 51 points by level 60. Pick a class.'),
    'uk': ('Калькулятор талантів WoW Forever: усі 9 класів', 'Калькулятор талантів WoW Forever',
           'Калькулятор талантів WoW Forever (ВоВ Форевер) для дев’яти класів: три гілки, 51 очко до 60 рівня, ряди й вимоги як у грі, посилання на білд. За бетою.',
           'Дев’ять класів, у кожного три гілки й 51 очко до 60 рівня. Оберіть клас.'),
    'de': ('WoW Forever Talentrechner: alle 9 Klassen', 'WoW Forever Talentrechner',
           'Talentrechner für WoW Forever, alle neun Klassen: je drei Bäume, 51 Punkte bis Stufe 60, Reihen und Voraussetzungen wie im Spiel, Build als Link.',
           'Neun Klassen, je drei Bäume und 51 Punkte bis Stufe 60. Wähle eine Klasse.'),
    'fr': ('Calculateur de talents WoW Forever : les 9 classes', 'Calculateur de talents WoW Forever',
           'Calculateur de talents WoW Forever pour les neuf classes : trois arbres chacune, 51 points au niveau 60, rangées et prérequis du jeu, build à partager.',
           'Neuf classes, trois arbres chacune, 51 points au niveau 60. Choisissez une classe.'),
    'es': ('Calculadora de talentos WoW Forever: las 9 clases', 'Calculadora de talentos WoW Forever',
           'Calculadora de talentos de WoW Forever para las nueve clases: tres árboles cada una, 51 puntos a nivel 60, filas y requisitos del juego, build con enlace.',
           'Nueve clases, tres árboles cada una, 51 puntos a nivel 60. Elige una clase.'),
    'pt': ('Calculadora de talentos WoW Forever: as 9 classes', 'Calculadora de talentos WoW Forever',
           'Calculadora de talentos do WoW Forever para as nove classes: três árvores cada, 51 pontos no nível 60, linhas e requisitos do jogo, build por link.',
           'Nove classes, três árvores cada, 51 pontos no nível 60. Escolha uma classe.'),
    'it': ('Calcolatore di talenti WoW Forever: tutte le 9 classi', 'Calcolatore di talenti WoW Forever',
           'Calcolatore di talenti di WoW Forever per tutte le nove classi: tre alberi ciascuna, 51 punti al livello 60, file e requisiti del gioco, build in un link.',
           'Nove classi, tre alberi ciascuna, 51 punti al livello 60. Scegli una classe.'),
    'pl': ('Kalkulator talentów WoW Forever: wszystkie 9 klas', 'Kalkulator talentów WoW Forever',
           'Kalkulator talentów WoW Forever dla dziewięciu klas: po trzy drzewka, 51 punktów na 60 poziomie, rzędy i wymagania jak w grze, build w linku.',
           'Dziewięć klas, każda ma trzy drzewka i 51 punktów na 60 poziomie. Wybierz klasę.'),
}


def calc_words(cid, lang):
    """{n}, {g}, {s} of a class calculator page in a language."""
    from content.guides import GUIDES as G
    c = next(x for x in CLASSES if x['id'] == cid)
    n = tr(c['n'], lang)
    import talents
    sec = {s['id']: s['title'] for s in next(x for x in G if x['slug'] == f'builds-{cid}')['sections']}
    trees = [langs.derive(dict(sec[t['key']]))[lang].split(':')[0].strip() for t in talents.load(cid)['trees']]   # the client's tab order
    return {'n': n, 'g': CALC_GEN.get(lang, {}).get(cid, n), 's': listing(trees, lang) if trees else ''}


def calc_meta():
    """talents/ and talents/<class>/ -> {lang: (title, description)}."""
    out = {'talents/': {l: (CALC_HUB[l][0], CALC_HUB[l][2]) for l in LANGS}}
    for c in CLASSES:
        out[f'talents/{c["id"]}/'] = {l: (CALC_T[l].format(**calc_words(c['id'], l)), CALC_D[l].format(**calc_words(c['id'], l))) for l in LANGS}
    return out


from content import dungeon_pages  # noqa: E402

import gear_planner  # noqa: E402

META[gear_planner.PATH] = ({l: v[0] for l, v in gear_planner.SEO.items()}, {l: v[1] for l, v in gear_planner.SEO.items()})   # character/gear/
META.update(dungeon_pages.SEO)   # pages of single dungeons: guides/dungeons/<slug>/
from content import tierlist_live  # noqa: E402

META['guides/tier-list/'] = tierlist_live.meta()   # «(Beta, Oct 23)» / «(Live, Nov 6)» in the title: one switch, data/tierlist.json
langs.fill([HOME_NAME, TOOLS_NAME, PRIVACY_NAME, PLAY_NAME, ROSTER_NAME, PROFILE_NAME, CHAR_NAME, PLAYER_NAME, META, CLASS_T, CLASS_T_SHORT, CLASS_D, RACE_T, RACE_T_SHORT, RACE_D, AND, OG])   # new languages: i18n/<lang>.json


def listing(xs, lang):
    return ', '.join(xs[:-1]) + AND[lang] + xs[-1]


def page_meta():
    """path -> {lang: (title, description)} for every page of the site."""
    out = {p: {l: (ti[l], de[l]) for l in LANGS if l in ti} for p, (ti, de) in META.items()}   # one-language page: its language
    for c in CLASSES:
        out[f'classes/{c["id"]}/'] = {}
        for l in LANGS:
            n = tr(c['n'], l)
            specs = [s['en'] if l == 'en' else tr(s['n'], l) for s in c['specs']]
            sp = ', '.join(specs) if l == 'en' else listing(specs, l)
            title = CLASS_T[l].format(n=n, specs=sp)
            if len(title) > 60:
                title = CLASS_T_SHORT[l].format(n=n, specs=sp)
            out[f'classes/{c["id"]}/'][l] = (title, CLASS_D[l].format(n=n, specs=listing(specs, l)))
    out.update(calc_meta())
    names = race_names()
    for rp in RACES_PAGE:
        facts = dict(rp['facts'])
        p = f'races/{rp["slug"]}/'
        out[p] = {}
        for l in LANGS:
            n = tr(names[rp['id']], l)
            fact = lambda k: build.ru_word(build.fact_ru(k, facts[k])) if l == 'ru' else tr(facts[k], l)   # places as the ruRU client shows them
            title = RACE_T[l].format(n=n)
            if len(title) > 60:
                title = RACE_T_SHORT[l].format(n=n)
            out[p][l] = (title, RACE_D[l].format(n=n, cap=fact('Столица'), zone=fact('Стартовая зона')))
    return out


# ---------- JSON-LD ----------

_RACES = None


def race_names():
    global _RACES
    if _RACES is None:
        src = open(os.path.join(HERE, 'index.src.html'), encoding='utf-8').read()
        _RACES = {r['id']: r['n'] for r in build.parse_races(src)}
    return _RACES


def crumbs(path, lang):
    """BreadcrumbList items [(name, url)] for a page path, or None for the home page."""
    if not path:
        return None
    base = SITE + page_dir(lang)
    items = [(HOME_NAME[lang], base)]
    sec = {'classes/': HUBS[0], 'races/': HUBS[1], 'guides/': HUB}
    parts = path.strip('/').split('/')
    top = parts[0] + '/'
    names = {'tools/': TOOLS_NAME, 'privacy/': PRIVACY_NAME, 'play/': PLAY_NAME, 'roster/': ROSTER_NAME, 'profile/': PROFILE_NAME, 'character/': CHAR_NAME}
    if top == 'u/':
        items += [(ROSTER_NAME[lang], base + 'roster/'), (PLAYER_NAME[lang], base + top)]
        return items
    if top in names:
        items.append((names[top][lang], base + top))
        if path == 'character/gear/':                              # the planner under «My character»
            import gear_planner
            items.append((gear_planner.TX['name'][lang], base + path))
        return items
    if top == 'talents/':                                          # the calculator: its class list, then the class
        items.append((CALC_NAME[lang], base + top))
        if len(parts) > 1:
            items.append((tr(next(c['n'] for c in CLASSES if c['id'] == parts[1]), lang), base + path))
        return items
    items.append((sec[top]['title'][lang], base + top))
    if len(parts) > 1:
        if top == 'guides/':
            g = next(x for x in GUIDES if x['slug'] == parts[1])
            name = g['title'][lang]
            if len(parts) > 2:                                     # guides/dungeons/<slug>/: the dungeon list, then the page
                items.append((name, base + top + parts[1] + '/'))
                name = next(x for x in GUIDES if x['slug'] == '/'.join(parts[1:]))['crumb'][lang]
        elif top == 'classes/':
            name = tr(next(c['n'] for c in CLASSES if c['id'] == parts[1]), lang)
        else:
            rid = next(r['id'] for r in RACES_PAGE if r['slug'] == parts[1])
            name = tr(race_names()[rid], lang)
        items.append((name, base + path))
    return items


def faq_ld(slug, lang):
    """FAQPage of a guide: every question of its ('faq', …) blocks; None when the guide has none."""
    guide = next(g for g in GUIDES if g['slug'] == slug)
    qs = [q for s in guide['sections'] for k, d in s['blocks'] if k == 'faq' for q in d]
    if not qs:
        return None
    text = build.ru_plain if lang == 'ru' else str                 # ru: game names as the ruRU client shows them
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'inLanguage': HREFLANG[lang],
            'mainEntity': [{'@type': 'Question', 'name': text(q['q'][lang]),
                            'acceptedAnswer': {'@type': 'Answer', 'text': ' '.join(text(a[lang]) for a in q['a'])}} for q in qs]}


ORG = {'@type': 'Organization', 'name': BRAND, 'url': 'https://gabella.site/', 'logo': SITE + 'assets/icons/icon-512.png',
       'sameAs': [build.DISCORD, build.TELEGRAM]}


def page_updated(path):
    """'2026-10-24' for a guide, class, race or tools page: the same date as its «Обновлено» line (build.page_updated), else None."""
    d = build.page_updated(path)
    return '-'.join(reversed(d.split('.'))) if d else None


# <lastmod> of the pages without an «Обновлено» line (home, news, play, privacy): the last change to their content sources,
# the same rule as build.src_date (today only while a source has uncommitted changes). Sitemap only: the pages show no date.
SITEMAP_SRC = {'': ('index.src.html', 'i18n/ru.txt', 'i18n/en.txt', 'i18n/uk.txt', 'content/guides.py'),   # «Свежее» = NEWS
               'guides/news/': ('content/guides.py', 'assets/news.json'),   # our notes + the Wowhead feed the page loads
               'play/': ('content/guides.py', 'journey.src.html'),   # PLAY texts and the game stages
               'privacy/': ('content/guides.py',),
               'character/gear/': ('gear_planner.py', 'assets/gear/planner.js', 'data/items_catalog.json', 'data/gear30.json')}   # the gear planner


def sitemap_lastmod(path):
    """'2026-10-24' for <lastmod>: the «Обновлено» date of the page, else the date of its SITEMAP_SRC sources, else None."""
    upd = page_updated(path)
    if upd or path not in SITEMAP_SRC:
        return upd
    return '-'.join(reversed(build.src_date(SITEMAP_SRC[path]).split('.')))


def json_ld(path, lang, desc, title='', image=''):
    blocks = []
    if not path:
        blocks.append({'@context': 'https://schema.org', '@type': 'WebSite', 'name': SITE_NAME,
                       'alternateName': 'gabella.site', 'url': SITE + page_dir(lang), 'inLanguage': HREFLANG[lang], 'description': desc,
                       'publisher': ORG})
        blocks.append({'@context': 'https://schema.org'} | ORG)
    else:
        items = crumbs(path, lang)
        blocks.append({'@context': 'https://schema.org', '@type': 'BreadcrumbList',
                       'itemListElement': [{'@type': 'ListItem', 'position': i, 'name': n, 'item': u}
                                           for i, (n, u) in enumerate(items, 1)]})
    updated = page_updated(path)
    if updated:
        art = {'@context': 'https://schema.org', '@type': 'Article', 'headline': title, 'description': desc,
               'inLanguage': HREFLANG[lang], 'url': SITE + page_dir(lang, path), 'dateModified': updated,
               'mainEntityOfPage': {'@type': 'WebPage', '@id': SITE + page_dir(lang, path)},
               'author': ORG, 'publisher': ORG, 'isPartOf': {'@type': 'WebSite', 'url': SITE + page_dir(lang)}}
        if image:
            art['image'] = image
        blocks.append(art)
    if path.startswith('guides/') and path != 'guides/' and (faq := faq_ld(path.split('/')[1], lang)):
        blocks.append(faq)
    dump = lambda b: json.dumps(b, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    return ''.join(f'<script type="application/ld+json">{dump(b)}</script>\n' for b in blocks)


# ---------- page rewrite ----------

def set_attr(html, rx, value, path):
    new, n = re.subn(rx, lambda m: m[1] + value + m[2], html, count=1)
    assert n == 1, (path, rx)
    return new


def undated(d):
    """After the launch night (live.py) the home description loses its last sentence when that one names the launch moment."""
    parts = re.split(r'(?<=[^\d][.!?])\s+', d)  # not after a digit: «5. Nov.»
    return ' '.join(parts[:-1]) if len(parts) > 1 and re.search(r'\d{1,2}[:.]\d{2}|UTC', parts[-1]) else d


def apply(html, path, lang, title, desc):
    a = escape(title, quote=True)
    d = escape(desc, quote=True)
    html = set_attr(html, r'(<title>).*?(</title>)', a, path)
    html = set_attr(html, r'(<meta name="description" content=")[^"]*(">)', d, path)
    if path in OG and lang in OG[path][0]:
        a, d = escape(OG[path][0][lang], quote=True), escape(undated(OG[path][1][lang]) if live.LIVE else OG[path][1][lang], quote=True)
    html = set_attr(html, r'(<meta property="og:title" content=")[^"]*(">)', a, path)
    html = set_attr(html, r'(<meta property="og:description" content=")[^"]*(">)', d, path)
    if 'og:image:alt' in html:
        html = set_attr(html, r'(<meta property="og:image:alt" content=")[^"]*(">)', a, path)
    else:
        html = html.replace('<meta name="twitter:card"', f'<meta property="og:image:alt" content="{a}">\n<meta name="twitter:card"', 1)
    if m := re.fullmatch(r'(?:classes|races)/([\w-]+)/', path):   # the card of a class or race is drawn per language (tools/make_og.py)
        html = re.sub(r'(assets/og/%s)\.jpg' % re.escape(m[1]), rf'\1-{lang}.jpg', html)
    img = re.search(r'<meta property="og:image" content="([^"]+)"', html)
    html = re.sub(r'<meta name="twitter:(?:title|description|image|image:alt)" content="[^"]*">\n', '', html)
    tw = f'<meta name="twitter:title" content="{a}">\n<meta name="twitter:description" content="{d}">\n'
    tw += f'<meta name="twitter:image" content="{img[1]}">\n<meta name="twitter:image:alt" content="{a}">\n' if img else ''
    html = re.sub(r'(<meta name="twitter:card"[^>]*>\n)', lambda m: m[1] + tw, html, count=1)
    alt = ''.join(f'<meta property="og:locale:alternate" content="{LOCALE[l]}">\n' for l in LANGS if l != lang and not build.only_lang(path))
    html = re.sub(r'<meta property="og:locale:alternate"[^>]*>\n', '', html)
    html = html.replace('<meta property="og:site_name"', alt + '<meta property="og:site_name"', 1)
    html = re.sub(r'<script type="application/ld\+json">.*?</script>\n', '', html, flags=re.S)
    html = re.sub(r'<meta name="(?:%s)" content="[^"]*">\n' % '|'.join(map(re.escape, VERIFY)), '', html)
    verify = ''.join(f'<meta name="{k}" content="{escape(v, quote=True)}">\n' for k, v in VERIFY.items() if v)
    og = re.search(r'<meta property="og:image" content="([^"]+)"', html)
    html = html.replace('</head>', verify + json_ld(path, lang, desc, title, og and og[1]) + '</head>', 1)
    html = re.sub(r'<script type="module" (?:data-)?src="https://static.cloudflareinsights.com/[^>]*></script>\n', '', html)
    if CF_BEACON_TOKEN:
        beacon = json.dumps({'token': CF_BEACON_TOKEN})
        html = html.replace('</body>', f'<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon=\'{beacon}\'></script>\n</body>', 1)
    if path == '':
        return build.late(build.late_fonts(html))
    if path.startswith('talents/'):                                # the calculator: a text heading, the display face comes late as on the home page
        return build.late(build.late_fonts(html), 'img[fetchpriority="high"]')
    return build.late(html, 'img[fetchpriority="high"]') if path.startswith(LATE_INNER) else html


def sitemap(paths):
    urls = []
    for p, by_lang in paths.items():
        ls = [l for l in LANGS if l in by_lang]
        alts = ''.join(f'<xhtml:link rel="alternate" hreflang="{HREFLANG[l]}" href="{SITE}{page_dir(l, p)}"/>' for l in ls)
        alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{p if len(ls) > 1 else page_dir(ls[0], p)}"/>'
        upd = sitemap_lastmod(p)
        lm = f'<lastmod>{upd}</lastmod>' if upd else ''
        urls += [f'<url><loc>{SITE}{page_dir(l, p)}</loc>{lm}{alts}</url>' for l in ls]
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + '\n'.join(urls) + '\n</urlset>\n')


def main():
    meta = page_meta()
    if '--list' in sys.argv:                 # build.py --list / --missing: texts collected, pages were not written
        return
    data_version = '-'.join(reversed(build.src_date(build.DATA_SRC).split('.')))   # the build version in a report: the date of the game data
    for path, by_lang in meta.items():
        for lang, (title, desc) in by_lang.items():
            if lang != 'ru':
                cyr = re.findall(r'[А-Яа-яЁё]', title + desc) if lang not in ('ru', 'uk') else []
                assert not cyr, (path, lang, title, desc)
            full = os.path.join(HERE, page_dir(lang, path), 'index.html')
            html = open(full, encoding='utf-8').read()
            html = apply(html, path, lang, title, desc)
            if lang == 'en':                     # dates added after localize (cards, JSON-LD): «Nov 4», not 04.11
                html = build.en_dates(html)
            if path.startswith('talents/'):     # a light page: only the styles its elements can use (build.prune_css)
                html = build.prune_css(html)
            html = build.min_css(html)
            html = report.inject(html, path, lang, data_version)   # «Нашёл ошибку» on the data pages (report.py)
            open(full, 'w', encoding='utf-8', newline='\n').write(html)
    with open(os.path.join(HERE, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(sitemap({p: v for p, v in meta.items() if p not in NOINDEX}))
    print(f'seo: {sum(map(len, meta.values()))} pages, sitemap.xml, analytics {"on" if CF_BEACON_TOKEN else "off (CF_BEACON_TOKEN empty)"}', file=sys.stderr)


if __name__ == '__main__':
    main()
