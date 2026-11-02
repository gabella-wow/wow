"""Профили: достижения, ранги и рамки (русский исходник; переводы — i18n/me.*.txt и i18n/<lang>.json).
Правила выдачи читает и сайт, и API (tools/export_game.py -> assets/game.json). Тексты в game.json не попадают.
kind: auto — выдаёт сервер по своим данным; progress — счётчик или набор из /progress (key, goal);
admin — выдаёт админ (события в игре, подтверждение в Discord). secret — скрыто до получения, видна подсказка.
Очки только 5, 10, 25, 50. Avoid ' and " inside strings: they split translation segments."""

CATS = [('community', 'Сообщество'), ('guide', 'Справочник'), ('radio', 'Радио'), ('tools', 'Инструменты'),
        ('rhythm', 'Ритм'), ('wow', 'WoW'), ('secrets', 'Секреты')]

# id, cat, pts, kind, rule, name, desc[, hint for secrets]
# rule: None | {'key': ..., 'goal': N} (счётчик) | {'key': ..., 'all': True} (весь набор) | {'key': ..., 'goal': N, 'set': True}
ACH = [
    # Сообщество
    ('founder', 'community', 25, 'auto', None, 'Основатель', 'Создать персонажа до 3 ноября, 21:00 UTC. Открывает рамку «Основатель».'),
    ('profile_full', 'community', 10, 'auto', None, 'Свой человек', 'Заполнить основного персонажа: роль, время игры и две профессии.'),
    ('three_chars', 'community', 10, 'auto', None, 'Три лица', 'Завести трёх персонажей.'),
    ('veteran3', 'community', 10, 'auto', {'days': 90}, 'Ветеран', 'Три месяца на сервере Gabella Team.'),
    ('veteran6', 'community', 25, 'auto', {'days': 182}, 'Старожил', 'Полгода на сервере Gabella Team.'),
    ('veteran12', 'community', 50, 'auto', {'days': 365}, 'Часть истории', 'Год на сервере Gabella Team. Открывает рамку «Часть истории».'),
    ('recruiter1', 'community', 10, 'auto', {'refs': 1}, 'Вербовщик', 'Позвать друга по своей ссылке: он вошёл на сайт.'),
    ('recruiter5', 'community', 50, 'auto', {'refs': 5}, 'Глава вербовки', 'Пять друзей вошли по вашей ссылке. Открывает рамку «Вербовщик».'),
    ('show_card', 'community', 5, 'progress', {'key': 'show_card', 'goal': 1}, 'Визитка', 'Скопировать ссылку на свою страницу.'),
    # Гид
    ('guides3', 'guide', 5, 'progress', {'key': 'guide', 'goal': 3, 'set': True}, 'Первые шаги', 'Открыть три гайда.'),
    ('guides_all', 'guide', 25, 'progress', {'key': 'guide', 'all': True}, 'Книжный червь', 'Открыть все гайды. Открывает рамку «Книжный червь».'),
    ('classes_all', 'guide', 10, 'progress', {'key': 'class', 'all': True}, 'Знаток классов', 'Открыть страницы всех девяти классов.'),
    ('races_all', 'guide', 10, 'progress', {'key': 'race', 'all': True}, 'Этнограф', 'Открыть страницы всех десяти рас.'),
    ('polyglot', 'guide', 10, 'progress', {'key': 'lang', 'goal': 3, 'set': True}, 'Полиглот', 'Открыть сайт на трёх языках.'),
    ('play_page', 'guide', 5, 'progress', {'key': 'play_page', 'goal': 1}, 'В игре', 'Открыть страницу «В игре».'),
    # Радио
    ('radio_on', 'radio', 5, 'progress', {'key': 'radio_on', 'goal': 1}, 'Первая нота', 'Включить радио Gabella.'),
    ('radio10h', 'radio', 25, 'progress', {'key': 'radio_min', 'goal': 600}, 'Меломан', 'Слушать радио 10 часов.'),
    ('radio100h', 'radio', 50, 'progress', {'key': 'radio_min', 'goal': 6000}, 'Вечный эфир', 'Слушать радио 100 часов. Открывает рамку «Вечный эфир».'),
    ('stations_all', 'radio', 10, 'progress', {'key': 'station', 'all': True}, 'Странник эфира', 'Послушать все восемь станций.'),
    ('sleep_timer', 'radio', 5, 'progress', {'key': 'sleep_timer', 'goal': 1}, 'Колыбельная', 'Уснуть под таймер сна.'),
    # Инструменты
    ('party5', 'tools', 5, 'progress', {'key': 'party5', 'goal': 1}, 'Квартирмейстер', 'Собрать полную группу на пятерых в инструментах.'),
    ('raid40', 'tools', 25, 'progress', {'key': 'raid40', 'goal': 1}, 'Рейд-лидер', 'Собрать полный рейд на сорок.'),
    ('share_team', 'tools', 5, 'progress', {'key': 'share_team', 'goal': 1}, 'Глашатай', 'Скопировать ссылку на состав группы.'),
    ('compare3', 'tools', 5, 'progress', {'key': 'compare3', 'goal': 1}, 'Взвесить всё', 'Сравнить три класса или расы.'),
    ('search25', 'tools', 10, 'progress', {'key': 'search', 'goal': 25}, 'Следопыт', 'Двадцать пять раз найти что-то поиском по сайту.'),
    # Ритм
    ('streak7', 'rhythm', 10, 'auto', {'streak': 7}, 'Завсегдатай', 'Заходить на сайт семь дней подряд.'),
    ('streak30', 'rhythm', 50, 'auto', {'streak': 30}, 'Свой за стойкой', 'Заходить на сайт тридцать дней подряд. Открывает рамку «Свой за стойкой».'),
    ('night_owl', 'rhythm', 10, 'progress', {'key': 'hour', 'items': [3, 4]}, 'Ночная смена', 'Зайти на сайт между тремя и пятью часами ночи.', 'Совы не спят.'),
    ('early_bird', 'rhythm', 10, 'progress', {'key': 'hour', 'items': [5, 6]}, 'Ранняя пташка', 'Зайти на сайт между пятью и семью утра.', 'Кто рано встаёт…'),
    # WoW (выдаёт админ; позже часть — через Battle.net)
    ('first60', 'wow', 50, 'admin', None, 'Первый шестидесятый', 'Первым в Gabella Team взять 60 уровень. Открывает рамку «Первый шестидесятый».'),
    ('lvl60', 'wow', 25, 'admin', None, 'Шестидесятый', 'Взять 60 уровень. Открывает рамку «Шестидесятый».'),
    ('dungeon_night', 'wow', 10, 'admin', None, 'Вечер в подземелье', 'Пройти подземелье группой Gabella Team.'),
    ('onyxia', 'wow', 50, 'admin', None, 'Убийца Ониксии', 'Победить Ониксию с Gabella Team. Открывает рамку «Драконоборец».'),
    ('molten_core', 'wow', 50, 'admin', None, 'Страж Хиджала', 'Победить всех 13 боссов Hyjal Summit с Gabella Team.'),
    ('raid_regular', 'wow', 25, 'admin', None, 'Костяк рейда', 'Пять рейдовых вечеров с Gabella Team. Открывает рамку «Костяк рейда».'),
    ('crafter', 'wow', 25, 'admin', None, 'Мастер', 'Довести профессию до 300. Открывает рамку «Мастер».'),
    ('helper', 'wow', 25, 'admin', None, 'Плечо друга', 'Помочь новичку пройти подземелье или задание. Открывает рамку «Плечо друга».'),
    ('event_winner', 'wow', 25, 'admin', None, 'Победитель', 'Победить в конкурсе Gabella Team. Открывает рамку «Победитель».'),
    # Секреты
    ('egg_griffin', 'secrets', 10, 'progress', {'key': 'egg', 'items': ['griffin']}, 'Гладить грифона', 'Десять раз нажать на грифона в шапке.', 'Грифон любит внимание.'),
    ('egg_leeroy', 'secrets', 10, 'progress', {'key': 'egg', 'items': ['leeroy']}, 'Ну хоть курицу взял', 'Найти в поиске самого известного паладина.', 'Время пошло!'),
    ('egg_konami', 'secrets', 10, 'progress', {'key': 'egg', 'items': ['konami']}, 'Старая школа', 'Ввести код из старых игр.', 'Вверх, вверх…'),
    ('egg_static', 'secrets', 10, 'progress', {'key': 'egg', 'items': ['static']}, 'Помехи в эфире', 'Переключить станцию радио десять раз за минуту.', 'Крути ручку.'),
    ('egg_404', 'secrets', 10, 'progress', {'key': 'egg', 'items': ['404']}, 'Не туда свернул', 'Попасть на страницу, которой нет.', 'Иногда полезно заблудиться.'),
    ('keeper', 'secrets', 25, 'auto', {'all_cat': 'secrets'}, 'Хранитель тайн', 'Найти все секреты. Открывает рамку «Хранитель тайн».', 'Найдите всё остальное.'),
]

# Ранги по очкам; у каждого своя рамка
RANKS = [('recruit', 0, 'Новобранец'), ('bronze', 25, 'Бронза'), ('silver', 100, 'Серебро'), ('gold', 200, 'Золото'),
         ('relite', 350, 'Редкая элита'), ('epic', 500, 'Эпический'), ('legend', 700, 'Легенда')]

# id, как открывается, название
FRAMES = [
    ('recruit', {'rank': 'recruit'}, 'Новобранец'), ('bronze', {'rank': 'bronze'}, 'Бронза'), ('silver', {'rank': 'silver'}, 'Серебро'),
    ('gold', {'rank': 'gold'}, 'Золото'), ('relite', {'rank': 'relite'}, 'Редкая элита'), ('epic', {'rank': 'epic'}, 'Эпический'),
    ('legend', {'rank': 'legend'}, 'Легенда'),
    ('founder', {'ach': 'founder'}, 'Основатель'), ('dragon', {'ach': 'onyxia'}, 'Драконоборец'),
    ('fire', {'ach': 'molten_core'}, 'Страж Хиджала'), ('secrets', {'ach': 'keeper'}, 'Хранитель тайн'),
    ('recruiter', {'ach': 'recruiter5'}, 'Вербовщик'),
    ('history', {'ach': 'veteran12'}, 'Часть истории'), ('ether', {'ach': 'radio100h'}, 'Вечный эфир'),
    ('tavern', {'ach': 'streak30'}, 'Свой за стойкой'), ('scholar', {'ach': 'guides_all'}, 'Книжный червь'),
    ('first60', {'ach': 'first60'}, 'Первый шестидесятый'), ('sixty', {'ach': 'lvl60'}, 'Шестидесятый'),
    ('raid', {'ach': 'raid_regular'}, 'Костяк рейда'), ('master', {'ach': 'crafter'}, 'Мастер'),
    ('friend', {'ach': 'helper'}, 'Плечо друга'), ('champion', {'ach': 'event_winner'}, 'Победитель'),
    ('boss', {'admin': True}, 'Босс'),
]


EGGS = ['griffin', 'leeroy', 'konami', 'static', '404']
