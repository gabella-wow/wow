"""Шпоры спеков: guides/spec-<класс>-<спек>/, вкладки Билд · Таланты · Прокачка 1→60 · С кем играть · БиС · Ротация.
Страница не пишет новых фактов о игре: вкладки собираются из готовых разделов builds-<класс> и leveling-<класс>.
Вкладки БиС нет: пустая вкладка хуже отсутствия; строка «Экипировка» в ответе за 5 секунд говорит «ждёт данных», пока нет списка Forever.
Ссылка на билд b/<раса>-<класс>-<спек>/ у этих спеков ведёт сюда (build_cards.py), «Поделиться» на странице делится той же ссылкой.
Заготовка attach() кладёт страницы в GUIDES до langs.fill, finish() добавляет названия на всех языках (нужен hero_core из build_guides)."""
import json, os
from html import escape

# (класс, спек): самые частые по данным сайта — оба прокачиваемых «быстрых» спека (Охотник S и Маг S в тир-листе прокачки),
# лучший танк беты и лекарь (Послушание, S в PvE и PvP); роли: 2 урона, танк, лекарь. Выбор Вячеслава 28.10
CHEATS = [('hunter', 'beast-mastery'), ('mage', 'frost'), ('paladin', 'protection'), ('priest', 'discipline'), ('rogue', 'combat'),
          ('warrior', 'protection'), ('warrior', 'fury'), ('warrior', 'arms'), ('paladin', 'holy'), ('paladin', 'retribution'),
          ('hunter', 'marksmanship'), ('hunter', 'survival'), ('rogue', 'assassination'), ('rogue', 'subtlety'),
          ('priest', 'holy'), ('priest', 'shadow'), ('shaman', 'elemental'), ('shaman', 'enhancement'), ('shaman', 'restoration'),
          ('mage', 'arcane'), ('mage', 'fire'), ('warlock', 'affliction'), ('warlock', 'demonology'), ('warlock', 'destruction'),
          ('druid', 'balance'), ('druid', 'feral'), ('druid', 'restoration')]   # all 27 specs since 29.10; the first five came first
SLUGS = [f'spec-{c}-{s}' for c, s in CHEATS]
HAS_CHEAT = {f'{c}-{s}' for c, s in CHEATS}

LANGS9 = ('ru', 'en', 'uk', 'de', 'fr', 'es', 'pt', 'it', 'pl')


def n9(ru, en, uk, de, fr, es, pt, it, pl):
    return dict(zip(LANGS9, (ru, en, uk, de, fr, es, pt, it, pl)))


ANSWER = n9('Ответ за 5 секунд', 'The answer in 5 seconds', 'Відповідь за 5 секунд', 'Die Antwort in 5 Sekunden', 'La réponse en 5 secondes',
            'La respuesta en 5 segundos', 'A resposta em 5 segundos', 'La risposta in 5 secondi', 'Odpowiedź w 5 sekund')
BEST = n9('Лучшая раса', 'Best race', 'Найкраща раса', 'Beste Rasse', 'Meilleure race', 'Mejor raza', 'Melhor raça', 'Migliore razza', 'Najlepsza rasa')
SHEET = n9('Шпора', 'Cheat sheet', 'Шпора', 'Spickzettel', 'Fiche rapide', 'Guía rápida', 'Resumo', 'Scheda rapida', 'Ściąga')
TAB = {
    'build': n9('Билд', 'Build', 'Білд', 'Build', 'Build', 'Build', 'Build', 'Build', 'Build'),
    'talents': n9('Таланты', 'Talents', 'Таланти', 'Talente', 'Talents', 'Talentos', 'Talentos', 'Talenti', 'Talenty'),
    'leveling': n9('Прокачка 1→60', 'Leveling 1→60', 'Прокачування 1→60', 'Leveln 1→60', 'Progression 1→60', 'Subida 1→60',
                   'Evolução 1→60', 'Salita 1→60', 'Levelowanie 1→60'),
    'group': n9('С кем играть', 'Who to group with', 'З ким грати', 'Mit wem spielen', 'Avec qui jouer', 'Con quién jugar',
                'Com quem jogar', 'Con chi giocare', 'Z kim grać'),
    'rotation': n9('Ротация', 'Rotation', 'Ротація', 'Rotation', 'Rotation', 'Rotación', 'Rotação', 'Rotazione', 'Rotacja'),
}
PICK = n9('Подобрать свою расу', 'Pick your race', 'Підібрати свою расу', 'Eigene Rasse wählen', 'Choisir ma race', 'Elegir mi raza',
          'Escolher minha raça', 'Scegli la tua razza', 'Wybierz swoją rasę')
FROM_LINK = n9('Раса из ссылки', 'Race from the link', 'Раса з посилання', 'Rasse aus dem Link', 'Race du lien', 'Raza del enlace',
               'Raça do link', 'Razza dal link', 'Rasa z linku')
ROT_NOTE = n9(
    'Ротация на 60 уровне будет после старта 5 ноября. Пока здесь порядок действий на 30 уровне по бете, как у Icy Veins и Wowhead.',
    'The level 60 rotation will come after the Nov 5 launch. For now this is the level 30 order of actions from the beta, as given by Icy Veins and Wowhead.',
    'Ротація на 60 рівні буде після старту 5 листопада. Поки що тут порядок дій на 30 рівні за бетою, як в Icy Veins і Wowhead.',
    'Die Rotation für Stufe 60 folgt nach dem Start am 5. November. Bis dahin steht hier die Reihenfolge für Stufe 30 aus der Beta, wie bei Icy Veins und Wowhead.',
    'La rotation du niveau 60 viendra après le lancement du 5 novembre. En attendant, voici l’ordre des actions au niveau 30 d’après la bêta, comme chez Icy Veins et Wowhead.',
    'La rotación de nivel 60 llegará tras el lanzamiento del 5 de noviembre. De momento, aquí está el orden de acciones del nivel 30 según la beta, como en Icy Veins y Wowhead.',
    'A rotação do nível 60 virá após o lançamento de 5 de novembro. Por enquanto, aqui está a ordem das ações no nível 30 segundo a beta, como no Icy Veins e no Wowhead.',
    'La rotazione di livello 60 arriverà dopo il lancio del 5 novembre. Per ora qui c’è l’ordine delle azioni al livello 30 secondo la beta, come su Icy Veins e Wowhead.',
    'Rotacja na 60 level pojawi się po starcie 5 listopada. Na razie jest tu kolejność działań na 30 levelu z bety, jak u Icy Veins i Wowhead.')
GROUP_NOTE = n9(
    'Состав группы собирается в конструкторе: до 5, 10, 20 или 40 игроков, ссылка и текст для поиска группы.',
    'Build the group in the group builder: up to 5, 10, 20 or 40 players, with a link and a text for looking for a group.',
    'Склад групи збирається в конструкторі: до 5, 10, 20 або 40 гравців, посилання й текст для пошуку групи.',
    'Die Gruppe stellst du im Gruppenbauer zusammen: bis zu 5, 10, 20 oder 40 Spieler, mit Link und Text für die Gruppensuche.',
    'La composition du groupe se prépare dans le constructeur : jusqu’à 5, 10, 20 ou 40 joueurs, avec un lien et un texte pour chercher un groupe.',
    'El grupo se arma en el constructor: hasta 5, 10, 20 o 40 jugadores, con enlace y texto para buscar grupo.',
    'O grupo é montado no construtor: até 5, 10, 20 ou 40 jogadores, com link e texto para procurar grupo.',
    'Il gruppo si compone nel costruttore: fino a 5, 10, 20 o 40 giocatori, con link e testo per cercare un gruppo.',
    'Skład grupy ustawiasz w konstruktorze: do 5, 10, 20 lub 40 graczy, z linkiem i tekstem do szukania grupy.')
GROUP_TILE = n9('Сборщик группы', 'Group builder', 'Конструктор групи', 'Gruppenbauer', 'Constructeur de groupe', 'Constructor de grupo',
                'Construtor de grupo', 'Costruttore di gruppo', 'Konstruktor grupy')
FULL_LEVELING = n9('Полный гайд прокачки класса', 'Full class leveling guide', 'Повний гайд прокачування класу', 'Vollständiger Level-Guide der Klasse',
                   'Guide complet de progression de la classe', 'Guía completa de subida de la clase', 'Guia completo de evolução da classe',
                   'Guida completa alla salita della classe', 'Pełny poradnik levelowania klasy')
FULL_BUILDS = n9('Все спеки класса', 'All specs of the class', 'Усі спеки класу', 'Alle Skillungen der Klasse', 'Toutes les spécialisations de la classe',
                 'Todas las especializaciones de la clase', 'Todas as especializações da classe', 'Tutte le specializzazioni della classe',
                 'Wszystkie specjalizacje klasy')
SEE_ALSO = n9('Смотрите также', 'See also', 'Дивіться також', 'Siehe auch', 'À voir aussi', 'Véase también', 'Veja também', 'Vedi anche', 'Zobacz też')
SEO_TAIL = n9('шпора WoW Forever', 'WoW Forever cheat sheet', 'шпора WoW Forever', 'Spickzettel WoW Forever', 'fiche WoW Forever',
              'guía rápida WoW Forever', 'resumo WoW Forever', 'scheda WoW Forever', 'ściąga WoW Forever')
SEO = {}   # guides/<slug>/ -> (title, description) by language, for seo.META (build.py adds it before seo.main)
LEAD_TAIL = n9('Билд, таланты, прокачка и группа на одной странице.', 'Build, talents, leveling and group on one page.',
               'Білд, таланти, прокачування й група на одній сторінці.', 'Build, Talente, Leveln und Gruppe auf einer Seite.',
               'Build, talents, progression et groupe sur une seule page.', 'Build, talentos, subida y grupo en una sola página.',
               'Build, talentos, evolução e grupo em uma só página.', 'Build, talenti, salita e gruppo in una sola pagina.',
               'Build, talenty, levelowanie i grupa na jednej stronie.')

GOAL = n9('Цель', 'Goal', 'Мета', 'Ziel', 'Objectif', 'Objetivo', 'Objetivo', 'Obiettivo', 'Cel')
GOAL_LV = n9('Прокачка', 'Leveling', 'Прокачування', 'Leveln', 'Progression', 'Subida', 'Evolução', 'Salita', 'Levelowanie')
GOAL_DG = n9('Подземелья', 'Dungeons', 'Підземелля', 'Dungeons', 'Donjons', 'Mazmorras', 'Masmorras', 'Spedizioni', 'Lochy')
KEYT = n9('Ключевые таланты', 'Key talents', 'Ключові таланти', 'Wichtige Talente', 'Talents clés', 'Talentos clave', 'Talentos-chave',
          'Talenti chiave', 'Kluczowe talenty')
ORDER_L = n9('Порядок взятия по уровням', 'Order of points by level', 'Порядок вибору за рівнями', 'Reihenfolge nach Stufe', 'Ordre par niveau',
             'Orden por nivel', 'Ordem por nível', 'Ordine per livello', 'Kolejność wg poziomu')
GEAR_ROWS = [
    n9('Чары', 'Enchants', 'Чари', 'Verzauberungen', 'Enchantements', 'Encantamientos', 'Encantamentos', 'Incantamenti', 'Zaklęcia'),
    n9('Расходники', 'Consumables', 'Витратні', 'Verbrauchsgüter', 'Consommables', 'Consumibles', 'Consumíveis', 'Consumabili',
       'Materiały eksploatacyjne'),
    n9('Камни и материалы', 'Gems and materials', 'Камені й матеріали', 'Edelsteine und Materialien', 'Gemmes et matériaux',
       'Gemas y materiales', 'Gemas e materiais', 'Gemme e materiali', 'Kamienie i materiały')]
# Waiting lines per row: the reason is what the sources really lack, not "after launch"
WAIT = [
    n9('Ждёт данных: у Icy Veins и Wowhead по этому спеку чар нет.', 'Waiting for data: Icy Veins and Wowhead list no enchants for this spec.',
       'Чекає на дані: в Icy Veins і Wowhead для цього спеку чарів немає.', 'Wartet auf Daten: Icy Veins und Wowhead nennen für diese Skillung keine Verzauberungen.',
       'En attente de données : Icy Veins et Wowhead ne listent aucun enchantement pour cette spécialisation.',
       'A la espera de datos: Icy Veins y Wowhead no listan encantamientos para esta especialización.',
       'Aguardando dados: Icy Veins e Wowhead não listam encantamentos para esta especialização.',
       'In attesa di dati: Icy Veins e Wowhead non elencano incantamenti per questa specializzazione.',
       'Czeka na dane: Icy Veins i Wowhead nie podają zaklęć dla tej specjalizacji.'),
    n9('Ждёт данных: у Icy Veins и Wowhead по этому спеку расходников нет.', 'Waiting for data: Icy Veins and Wowhead list no consumables for this spec.',
       'Чекає на дані: в Icy Veins і Wowhead для цього спеку витратних немає.', 'Wartet auf Daten: Icy Veins und Wowhead nennen für diese Skillung keine Verbrauchsgüter.',
       'En attente de données : Icy Veins et Wowhead ne listent aucun consommable pour cette spécialisation.',
       'A la espera de datos: Icy Veins y Wowhead no listan consumibles para esta especialización.',
       'Aguardando dados: Icy Veins e Wowhead não listam consumíveis para esta especialização.',
       'In attesa di dati: Icy Veins e Wowhead non elencano consumabili per questa specializzazione.',
       'Czeka na dane: Icy Veins i Wowhead nie podają materiałów eksploatacyjnych dla tej specjalizacji.'),
    n9('Ждёт данных: у Icy Veins и Wowhead по этому спеку камней и материалов нет.', 'Waiting for data: Icy Veins and Wowhead list no gems or materials for this spec.',
       'Чекає на дані: в Icy Veins і Wowhead для цього спеку каменів і матеріалів немає.', 'Wartet auf Daten: Icy Veins und Wowhead nennen für diese Skillung keine Edelsteine oder Materialien.',
       'En attente de données : Icy Veins et Wowhead ne listent ni gemmes ni matériaux pour cette spécialisation.',
       'A la espera de datos: Icy Veins y Wowhead no listan gemas ni materiales para esta especialización.',
       'Aguardando dados: Icy Veins e Wowhead não listam gemas nem materiais para esta especialização.',
       'In attesa di dati: Icy Veins e Wowhead non elencano gemme né materiali per questa specializzazione.',
       'Czeka na dane: Icy Veins i Wowhead nie podają kamieni ani materiałów dla tej specjalizacji.')]


def _it(en, ru=None, de=None, fr=None, es=None, pt=None, it=None):
    """Item name: the client name where Wowhead Forever has one; uk, pl and the rest fall back to English."""
    return {'en': en, 'ru': ru or en, 'de': de or en, 'fr': fr or en, 'es': es or en, 'pt': pt or en, 'it': it or en}


I_POISON = _it('Instant Poison', 'Быстродействующий яд', 'Sofort wirkendes Gift', 'Poison instantané', 'Veneno instantáneo', 'Veneno Instantâneo')
I_STONE = _it('Rough Sharpening Stone', 'Грубое точило', 'Rauer Wetzstein', 'Pierre à aiguiser brute', 'Piedra de afilar férrea', 'Pedra de Afiar Rústica')
I_AGI = _it('Elixir of Agility', 'Эликсир Ловкости', 'Elixier der Beweglichkeit', 'Elixir d’Agilité', 'Elixir de agilidad', 'Elixir de Agilidade')
I_GHP = _it('Greater Healing Potion', 'Сильное лечебное зелье', 'Großer Heiltrank', 'Potion de soins supérieure', 'Poción de curación superior', 'Poção Maior de Cura')
E_POISON = n9('на оба оружия, лишний урон с каждым ударом', 'on both weapons, extra damage with each hit',
              'на обидві зброї, додаткова шкода з кожним ударом', 'auf beiden Waffen, zusätzlicher Schaden bei jedem Treffer',
              'sur les deux armes, dégâts supplémentaires à chaque coup', 'en ambas armas, daño adicional con cada golpe',
              'nas duas armas, dano extra a cada golpe', 'su entrambe le armi, danno extra a ogni colpo',
              'na obu broniach, dodatkowe obrażenia przy każdym trafieniu')
E_STONE = n9('ставится вместе с ядом: в Forever можно держать оба', 'goes on together with a poison: in Forever you can have both',
             'ставиться разом з отрутою: у Forever можна тримати обидва', 'zusammen mit einem Gift: in Forever sind beide gleichzeitig möglich',
             'avec un poison : dans Forever, les deux peuvent être actifs', 'junto con un veneno: en Forever puedes tener los dos',
             'junto com um veneno: no Forever dá para ter os dois', 'insieme a un veleno: in Forever si possono avere entrambi',
             'razem z trucizną: w Forever można mieć oba naraz')
E_AGI = n9('+15 ловкости на 1 час', '+15 Agility for 1 hour', '+15 спритності на 1 годину', '+15 Beweglichkeit für 1 Stunde',
           '+15 d’agilité pendant 1 heure', '+15 de agilidad durante 1 hora', '+15 de Agilidade por 1 hora', '+15 Agilità per 1 ora',
           '+15 zręczności na 1 godzinę')
E_GHP = n9('лечение в бою: разбойник сам не лечится', 'healing in combat: a Rogue has no self-heal', 'зцілення в бою: розбійник сам себе не лікує',
           'Heilung im Kampf: der Schurke kann sich nicht selbst heilen', 'soins en combat : le voleur ne peut pas se soigner seul',
           'curación en combate: el pícaro no se cura solo', 'cura em combate: o ladino não se cura sozinho',
           'cura in combattimento: il ladro non si cura da solo', 'leczenie w walce: łotrzyk sam się nie leczy')
STATS_T = n9('Приоритет статов', 'Stat priority', 'Пріоритет характеристик', 'Wertepriorität', 'Priorité des caractéristiques',
             'Prioridad de estadísticas', 'Prioridade de atributos', 'Priorità delle statistiche', 'Priorytet statystyk')
STAT = {
    'wd': n9('Урон оружия', 'Weapon damage', 'Шкода зброї', 'Waffenschaden', 'Dégâts de l’arme', 'Daño de arma', 'Dano da arma',
             'Danni dell’arma', 'Obrażenia broni'),
    'hit': n9('Меткость', 'Hit', 'Влучність', 'Trefferwertung', 'Toucher', 'Golpe', 'Acerto', 'Colpire', 'Trafienie'),
    'exp': n9('Мастерство', 'Expertise', 'Майстерність', 'Waffenkunde', 'Expertise', 'Pericia', 'Perícia', 'Maestria', 'Biegłość'),
    'agi': n9('Ловкость', 'Agility', 'Спритність', 'Beweglichkeit', 'Agilité', 'Agilidad', 'Agilidade', 'Agilità', 'Zręczność'),
    'crit': n9('Крит', 'Crit', 'Крит', 'Krit', 'Critique', 'Crítico', 'Crítico', 'Critico', 'Kryt'),
    'str': n9('Сила', 'Strength', 'Сила', 'Stärke', 'Force', 'Fuerza', 'Força', 'Forza', 'Siła'),
    'sp': n9('Сила заклинаний', 'Spell power', 'Сила заклинань', 'Zaubermacht', 'Puissance des sorts', 'Poder con hechizos', 'Poder mágico',
             'Potere magico', 'Moc zaklęć'),
    'hp': n9('Сила лечения', 'Healing power', 'Сила зцілення', 'Heilkraft', 'Puissance de soins', 'Poder de sanación', 'Poder de cura',
             'Potere di cura', 'Moc leczenia'),
    'int': n9('Интеллект', 'Intellect', 'Інтелект', 'Intelligenz', 'Intelligence', 'Intelecto', 'Intelecto', 'Intelletto', 'Intelekt'),
    'spi': n9('Дух', 'Spirit', 'Дух', 'Willenskraft', 'Esprit', 'Espíritu', 'Espírito', 'Spirito', 'Duch'),
    'mp5': n9('Мана раз в 5 с', 'Mana per 5 s', 'Мана раз на 5 с', 'Mana alle 5 Sek.', 'Mana toutes les 5 s', 'Maná cada 5 s',
              'Mana a cada 5 s', 'Mana ogni 5 s', 'Mana co 5 s'),
    'haste': n9('Скорость', 'Haste', 'Швидкість', 'Tempo', 'Hâte', 'Celeridad', 'Aceleração', 'Celerità', 'Szybkość'),
}
# The order from the spec's tip in spec_builds.py (Icy Veins for the beta; Fury also Warcraft Tavern). No key: the sources give no order;
# 'split': they disagree (Frost: Icy Veins hit first, Warcraft Tavern spell power). Arms, Protection (warrior), Arcane and Fire: the stat pages
# of the Icy Veins Forever guides, read 29.10 (Arcane is called a rough order there). Paladin Protection: Icy Veins has no order.
IV, IVT = 'Icy Veins', 'Icy Veins, Warcraft Tavern'
STATS = {
    'paladin-holy': ('hp int spi', IV), 'paladin-retribution': ('wd hit crit', IV), 'warrior-fury': ('hit crit str', IVT),
    'hunter-beast-mastery': ('wd hit agi crit', IV), 'hunter-marksmanship': ('wd hit agi crit', IV),
    'hunter-survival': ('wd hit agi crit str', IV), 'rogue-assassination': ('wd hit exp agi crit', IV),
    'rogue-combat': ('wd hit exp agi crit', IV), 'rogue-subtlety': ('wd hit exp agi crit', IV),
    'priest-discipline': ('hp mp5 spi int crit', IV), 'priest-holy': ('hp mp5 spi int crit', IV), 'priest-shadow': ('sp crit hit int', IV),
    'shaman-elemental': ('sp crit hit int', IV), 'shaman-enhancement': ('wd hit exp crit str int', IV),
    'shaman-restoration': ('hp crit int spi mp5', IV), 'warlock-affliction': ('sp hit crit int spi', IV),
    'warlock-demonology': ('sp hit int crit spi', IV), 'warlock-destruction': ('sp hit haste crit', IV),
    'druid-balance': ('int sp spi mp5 crit', IV), 'druid-feral': ('wd hit exp crit str agi', IV),
    'druid-restoration': ('int hp spi mp5 crit', IV), 'mage-frost': 'split',
    'warrior-arms': ('wd hit crit str agi sta', IV), 'warrior-protection': ('wd hit str agi armor sta crit', IV),
    'mage-arcane': ('hit spi int sp crit sta mp5', IV), 'mage-fire': ('hit sp crit spi int sta mp5', IV),
}
STATS_NONE = n9('Ждёт данных: в гайдах Icy Veins и Wowhead по бете порядка статов нет.',
                'Waiting for data: the Icy Veins and Wowhead beta guides give no stat order.',
                'Чекає на дані: у гайдах Icy Veins і Wowhead за бетою порядку характеристик немає.',
                'Wartet auf Daten: Die Beta-Guides von Icy Veins und Wowhead nennen keine Reihenfolge.',
                'En attente de données : les guides bêta d’Icy Veins et de Wowhead ne donnent pas d’ordre.',
                'A la espera de datos: las guías de la beta de Icy Veins y Wowhead no dan un orden.',
                'Aguardando dados: os guias da beta do Icy Veins e do Wowhead não dão uma ordem.',
                'In attesa di dati: le guide della beta di Icy Veins e Wowhead non danno un ordine.',
                'Czeka na dane: poradniki bety Icy Veins i Wowhead nie podają kolejności.')
STATS_SPLIT = n9('Ждёт данных: источники расходятся. Icy Veins ставит первой меткость, Warcraft Tavern — силу заклинаний.',
                 'Waiting for data: the sources disagree. Icy Veins puts hit first, Warcraft Tavern puts spell power first.',
                 'Чекає на дані: джерела розходяться. Icy Veins ставить першою влучність, Warcraft Tavern — силу заклинань.',
                 'Wartet auf Daten: Die Quellen sind uneins. Icy Veins setzt Trefferwertung zuerst, Warcraft Tavern Zaubermacht.',
                 'En attente de données : les sources divergent. Icy Veins place le toucher en premier, Warcraft Tavern la puissance des sorts.',
                 'A la espera de datos: las fuentes no coinciden. Icy Veins pone primero el golpe, Warcraft Tavern el poder con hechizos.',
                 'Aguardando dados: as fontes divergem. Icy Veins põe acerto primeiro, Warcraft Tavern põe poder mágico.',
                 'In attesa di dati: le fonti non concordano. Icy Veins mette prima colpire, Warcraft Tavern il potere magico.',
                 'Czeka na dane: źródła się różnią. Icy Veins stawia najpierw trafienie, Warcraft Tavern moc zaklęć.')
EXTRA = {
    'sta': n9('Выносливость', 'Stamina', 'Витривалість', 'Ausdauer', 'Endurance', 'Aguante', 'Vigor', 'Resistenza', 'Wytrzymałość'),
    'def': n9('Защита', 'Defense', 'Захист', 'Verteidigung', 'Défense', 'Defensa', 'Defesa', 'Difesa', 'Obrona'),
    'armor': n9('Броня', 'Armor', 'Броня', 'Rüstung', 'Armure', 'Armadura', 'Armadura', 'Armatura', 'Pancerz'),
    'thr': n9('угрозы', 'threat', 'загрози', 'Bedrohung', 'menace', 'amenaza', 'ameaça', 'minaccia', 'zagrożenia'),
    'dodge': n9('уклонения', 'dodge', 'ухилення', 'Ausweichen', 'esquive', 'esquiva', 'esquiva', 'schivata', 'uniku')}


def _low(w, lang):
    return w if lang == 'de' else w[:1].lower() + w[1:]   # mid-line stat names: lower case as in «+14 силы заклинаний»; German nouns keep it


# «+14 силы заклинаний», not «+14 сила заклинаний»: after a number ru, uk and pl take the genitive, es and pt a «de» (as in WELL_FED, E_AGI)
GEN = {
    'ru': {'sp': 'силы заклинаний', 'hp': 'силы лечения', 'int': 'интеллекта', 'agi': 'ловкости', 'str': 'силы', 'sta': 'выносливости',
           'def': 'защиты', 'mp5': 'маны раз в 5 с', 'spi': 'духа', 'crit': 'крита', 'hit': 'меткости', 'armor': 'брони', 'wd': 'урона оружия',
           'exp': 'мастерства', 'haste': 'скорости'},
    'uk': {'sp': 'сили заклинань', 'hp': 'сили зцілення', 'int': 'інтелекту', 'agi': 'спритності', 'str': 'сили', 'sta': 'витривалості',
           'def': 'захисту', 'mp5': 'мани раз на 5 с', 'spi': 'духу', 'crit': 'криту', 'hit': 'влучності', 'armor': 'броні', 'wd': 'шкоди зброї',
           'exp': 'майстерності', 'haste': 'швидкості'},
    'pl': {'sp': 'mocy zaklęć', 'hp': 'mocy leczenia', 'int': 'intelektu', 'agi': 'zręczności', 'str': 'siły', 'sta': 'wytrzymałości',
           'def': 'obrony', 'mp5': 'many co 5 s', 'spi': 'ducha', 'crit': 'kryta', 'hit': 'trafienia', 'armor': 'pancerza', 'wd': 'obrażeń broni',
           'exp': 'biegłości', 'haste': 'szybkości'}}


def _num(k, l):
    if k in GEN.get(l, {}):
        return GEN[l][k]
    w = _low((STAT.get(k) or EXTRA[k])[l], l)
    return f'de {w}' if l in ('es', 'pt') else w


def S(k, n):
    pct = '%' if k in ('thr', 'dodge') else ''
    return {l: f'+{n}{pct} {_num(k, l)}' for l in LANGS9}


def J(*ds):
    return {l: ', '.join(d[l] for d in ds) for l in LANGS9}


def U(n, u):
    return {l: f'{n} {UNIT[u][l]}' for l in LANGS9}


def W(word, a, b=None):
    return {l: f'{a}{"–" + str(b) if b else ""} {word[l]}' for l in LANGS9}


def NM(item, extra=None):
    d = {l: item.get(l) or item['en'] for l in LANGS9}
    return J(d, extra) if extra else d


UNIT = {'min': n9('мин', 'min', 'хв', 'Min.', 'min', 'min', 'min', 'min', 'min'), 's': n9('с', 's', 'с', 'Sek.', 's', 's', 's', 's', 's'),
        'h': n9('ч', 'h', 'год', 'Std.', 'h', 'h', 'h', 'h', 'godz.')}
MANA_W = n9('маны', 'mana', 'мани', 'Mana', 'de mana', 'de maná', 'de mana', 'di mana', 'many')
RAGE_W = n9('ярости', 'rage', 'люті', 'Wut', 'de rage', 'de ira', 'de raiva', 'di rabbia', 'wściekłości')
DMG_W = n9('урона', 'damage', 'шкоди', 'Schaden', 'de dégâts', 'de daño', 'de dano', 'di danno', 'obrażeń')
HP_W = n9('здоровья', 'health', 'здоров’я', 'Gesundheit', 'de vie', 'de salud', 'de vida', 'di salute', 'zdrowia')
SP_WEAPON = n9('сила заклинаний на оружие', 'spell power on the weapon', 'сила заклинань на зброю', 'Zaubermacht auf der Waffe',
               'puissance des sorts sur l’arme', 'poder con hechizos en el arma', 'poder mágico na arma', 'potere magico sull’arma',
               'moc zaklęć na broni')
WELL_FED = n9('сытость: +14 силы заклинаний', 'well fed: +14 spell power', 'ситість: +14 сили заклинань', 'gut genährt: +14 Zaubermacht',
              'bien nourri : +14 puissance des sorts', 'bien alimentado: +14 de poder con hechizos', 'bem alimentado: +14 de poder mágico',
              'ben nutrito: +14 potere magico', 'najedzenie: +14 mocy zaklęć')
SLOT = {
    'w': n9('Оружие', 'Weapon', 'Зброя', 'Waffe', 'Arme', 'Arma', 'Arma', 'Arma', 'Broń'),
    'neck': n9('Шея', 'Neck', 'Шия', 'Hals', 'Cou', 'Cuello', 'Pescoço', 'Collo', 'Szyja'),
    'chest': n9('Грудь', 'Chest', 'Груди', 'Brust', 'Torse', 'Pecho', 'Peitoral', 'Torace', 'Tors'),
    'legs': n9('Ноги', 'Legs', 'Ноги', 'Beine', 'Jambes', 'Piernas', 'Pernas', 'Gambe', 'Nogi'),
    'br': n9('Наручи', 'Bracers', 'Наручі', 'Armschienen', 'Brassards', 'Brazales', 'Braçadeiras', 'Bracciali', 'Karwasze'),
    'boots': n9('Сапоги', 'Boots', 'Чоботи', 'Stiefel', 'Bottes', 'Botas', 'Botas', 'Stivali', 'Buty'),
    'kit': n9('Грудь, ноги, перчатки', 'Chest, legs, hands', 'Груди, ноги, рукавиці', 'Brust, Beine, Hände', 'Torse, jambes, mains',
              'Pecho, piernas, manos', 'Peitoral, pernas, mãos', 'Torace, gambe, mani', 'Tors, nogi, dłonie'),
    'l60': n9('На 60 уровне', 'At level 60', 'На 60 рівні', 'Auf Stufe 60', 'Au niveau 60', 'En el nivel 60', 'No nível 60', 'Al livello 60',
              'Na 60 poziomie')}
REV = n9('после заклинания без крита следующее получает +100% к криту', 'a spell that fails to crit gives the next one +100% crit',
         'після заклинання без крита наступне отримує +100% до крита', 'nach einem Zauber ohne Krit hat der nächste +100 % Krit',
         'après un sort sans critique, le suivant a +100 % de critique', 'tras un hechizo sin crítico, el siguiente tiene +100 % de crítico',
         'após um feitiço sem crítico, o próximo tem +100% de crítico', 'dopo un incantesimo senza critico, il successivo ha +100% di critico',
         'po zaklęciu bez krytyka następne ma +100% do krytyka')
SPEED = n9('+8% скорости бега', '+8% run speed', '+8% швидкості бігу', '+8 % Lauftempo', '+8 % de vitesse de course', '+8 % de velocidad',
           '+8% de velocidade', '+8% velocità di corsa', '+8% szybkości biegu')
# Enchant names as the client shows them (Wowhead Forever, the spell's own page in each language); the effect stays after a comma, like the kit
E_REV = _it('Enchant Weapon - Revelation', 'Чары для оружия: откровение', 'Waffe - Offenbarung', 'Enchantement d’arme (Révélation)',
            'Encantar arma: revelación', 'Encantamento de Revelação - Arma')
E_NECK_SP = _it('Enchant Necklace - Spell Power', 'Чары для ожерелья: сила заклинаний', 'Halskette - Zaubermacht',
                'Enchantement de collier (Puissance des sorts)', 'Encantar collar: poder con hechizos', 'Encantamento de Poder Mágico - Colar')
E_BR_LHP = _it('Enchant Bracer - Lesser Healing Power', 'Чары для наручей: малая целительная сила', 'Armschiene - Geringere Heilkraft',
               'Enchantement de brassards (Pouvoir de guérison inférieur)', 'Encantar brazal: poder de sanación inferior',
               'Encantamento Inferior de Poder de Cura - Braçadeiras')
E_CH_INT = _it('Enchant Chest - Intellect', 'Чары для нагрудника: интеллект', 'Brust - Intelligenz', 'Enchantement de plastron (Intelligence)',
               'Encantar torso: intelecto', 'Encantamento de Intelecto - Torso')
E_CH_GINT = _it('Enchant Chest - Greater Intellect', 'Чары для нагрудника: сильный интеллект', 'Brust - Große Intelligenz',
                'Enchantement de plastron (Intelligence supérieure)', 'Encantar torso: intelecto superior', 'Encantamento Maior de Intelecto - Torso')
E_SPEED = _it('Enchant Boots - Minor Speed', 'Чары для обуви: малая скорость', 'Stiefel - Schwaches Tempo', 'Ench. de bottes (Vitesse mineure)',
              'Encantar botas: velocidad menor', 'Encantamento Menor de Velocidade - Botas')
E_GL_AGI = _it('Enchant Gloves - Agility', 'Чары для перчаток: ловкость', 'Handschuhe - Beweglichkeit', 'Ench. de gants (Agilité)',
               'Encantar guantes: agilidad', 'Encantamento de Agilidade – Luvas')
E_CL_AGI = _it('Enchant Cloak - Lesser Agility', 'Чары для плаща: малая ловкость', 'Umhang - Geringe Beweglichkeit', 'Ench. de cape (Agilité inférieure)',
               'Encantar capa: agilidad inferior', 'Encantamento Inferior de Agilidade - Manto')
E_BO_AGI = _it('Enchant Boots - Lesser Agility', 'Чары для обуви: малая ловкость', 'Stiefel - Geringe Beweglichkeit', 'Ench. de bottes (Agilité inférieure)',
               'Encantar botas: agilidad inferior', 'Encantamento Inferior de Agilidade - Botas')
E_BR_STR = _it('Enchant Bracer - Strength', 'Чары для браслетов: сила III', 'Armschiene - Stärke', 'Ench. de bracelets (Force)', 'Encantar brazal: fuerza',
               'Encantamento de Força - Braçadeiras')
E_GL_STR = _it('Enchant Gloves - Strength', 'Чары для перчаток: сила', 'Handschuhe - Stärke', 'Ench. de gants (Force)', 'Encantar guantes: fuerza',
               'Encantamento de Força - Luvas')
E_BR_STA = _it('Enchant Bracer - Stamina', 'Чары для браслетов: выносливость III', 'Armschiene - Ausdauer', 'Ench. de bracelets (Endurance)',
               'Encantar brazal: aguante', 'Encantamento de Vigor - Braçadeiras')
E_CH_STA = _it('Enchant Chest - Superior Stamina', 'Чары для нагрудника: высшая выносливость', 'Brust - Überragende Ausdauer',
               'Enchantement de plastron (Endurance excellente)', 'Encantar torso: aguante excelente', 'Encantamento Superior de Vigor – Torso')
E_BO_STA = _it('Enchant Boots - Stamina', 'Чары для обуви: выносливость III', 'Stiefel - Ausdauer', 'Ench. de bottes (Endurance)', 'Encantar botas: aguante',
               'Encantamento de Vigor - Botas')
E_SH_STA = _it('Enchant Shield - Stamina', 'Чары для щита: выносливость', 'Schild - Ausdauer', 'Ench. de bouclier (Endurance)', 'Encantar escudo: aguante',
               'Encantamento de Vigor - Escudo')


def EN(name, eff):
    return J(NM(name), eff)


REV = EN(E_REV, REV)
SPEED = EN(E_SPEED, SPEED)
NECK_SP = EN(E_NECK_SP, S('sp', 6))
BR_SP = EN(E_BR_LHP, S('sp', 6))       # the same enchant: +16 healing and +6 spell damage (Wowhead Forever)
I_KIT = _it('Mystic Heavy Armor Kit', 'Мистические накладки из толстой кожи', 'Mystisches schweres Rüstungsset', 'Renfort d’armure lourd mystique',
            'Complemento pesado para armadura místico', 'Kit de Armadura Pesada Mística')
I_SPELLB = _it('Spellblasting Potion', 'Зелье взрывных чар', 'Trank des Zauberschlags', 'Potion d’explosion de sorts',
               'Poción de explosión de hechizos', 'Poção de Impacto Mágico')
I_MANA = _it('Mana Potion', 'Зелье маны', 'Manatrank', 'Potion de mana', 'Poción de maná', 'Poção de Mana')
I_LAE = _it('Lesser Arcane Elixir', 'Малый чародейский эликсир', 'Geringes Arkanelixier', 'Élixir des arcanes inférieur', 'Elixir Arcano inferior',
            'Elixir Arcano Inferior')
I_MBLOOD = _it('Lesser Mageblood Elixir', 'Малый эликсир крови волшебника', 'Geringes Magierblutelixier', 'Élixir magesang inférieur',
               'Elixir de sangre de mago inferior', 'Elixir Inferior de Sangue de Mago')
I_WIZOIL = _it('Lesser Wizard Oil', 'Малое волшебное масло', 'Geringes Zauberöl', 'Huile de sorcier inférieure', 'Aceite de zahorí inferior',
               'Óleo Inferior de Teurgo')
I_STEW = _it('Briny Seafood Stew', 'Соленый суп из морепродуктов', 'Salziger Meeresfrüchteeintopf', 'Ragoût de fruits de mer saumâtre',
             'Estofado de marisco salobre', 'Ensopado Salgado de Frutos do Mar')
I_CLERIC = _it('Lesser Cleric’s Elixir', 'Малый эликсир священника', 'Geringes Klerikerelixier', 'Élixir des clercs inférieur',
               'Elixir de clérigo inferior', 'Elixir Inferior do Clérigo')
I_MENDER = _it('Mender’s Potion', 'Зелье целителя', 'Trank des Heilers', 'Potion de soigneur', 'Poción de ensalmador', 'Poção do Reparador')
I_OGRE = _it('Elixir of Ogre Strength', 'Эликсир силы огра', 'Elixier der Ogerstärke', 'Élixir de force d’ogre', 'Elixir de fuerza de ogro',
             'Elixir de Força de Ogro')
I_COARSE = _it('Coarse Sharpening Stone', 'Зернистое точило', 'Grober Wetzstein', 'Pierre à aiguiser grossière', 'Piedra de afilar burda',
               'Pedra de Afiar Grosseira')
I_SOLID = _it('Solid Sharpening Stone', 'Твердое точило', 'Robuster Wetzstein', 'Pierre à aiguiser solide', 'Piedra de afilar sólida',
              'Pedra de Afiar Maciça')
I_WEIGHT = _it('Solid Weightstone', 'Твердое грузило', 'Robuster Gewichtsstein', 'Caillou solide', 'Piedrafuerte sólida', 'Contrapeso Maciço')
I_RAGE = _it('Great Rage Potion', 'Сильнодействующее зелье ярости', 'Großer Wuttrank', 'Potion de Grande rage', 'Gran poción de ira',
             'Poção Grandiosa de Raiva')
X_GHP = n9('мгновенное лечение', 'instant healing', 'миттєве зцілення', 'Sofortheilung', 'soins instantanés', 'curación instantánea',
           'cura instantânea', 'cura istantanea', 'natychmiastowe leczenie')
X_LHP = {l: f'{X_GHP[l]}: 140–180 {HP_W[l]}' for l in LANGS9}
X_SHP = {l: f'{X_GHP[l]}: 700–900 {HP_W[l]}' for l in LANGS9}
X_GHP = {l: f'{X_GHP[l]}: 455–585 {HP_W[l]}' for l in LANGS9}
I_SHP = _it('Superior Healing Potion', 'Мощное лечебное зелье', 'Überragender Heiltrank', 'Potion de soins excellente', 'Poción de curación excelente',
            'Poção Superior de Cura')   # requires level 35 (Wowhead Forever, item 3928)
I_LMANA = _it('Lesser Mana Potion', 'Малое зелье маны', 'Geringer Manatrank', 'Potion de mana inférieure', 'Poción de maná inferior',
              'Poção Inferior de Mana')   # requires level 14 (Wowhead Forever, item 3385)
I_LHP = _it('Lesser Healing Potion', 'Простое лечебное зелье', 'Geringer Heiltrank', 'Potion de soins inférieure', 'Poción de Curación inferior',
            'Poção Inferior de Cura')
I_MELON = _it('Melon Juice', 'Дынный сок', 'Melonensaft', 'Jus de melon', 'Zumo de melón', 'Suco de Melão')
I_MMOIL = _it('Minor Mana Oil', 'Слабое масло маны', 'Schwaches Manaöl', 'Huile de mana mineure', 'Aceite de maná menor', 'Óleo Menor de Mana')
I_BUZZ = _it('Barbecued Buzzard Wing', 'Жареное крыло канюка', 'Gegrillter Bussardflügel', 'Aile de busard grillée', 'Ala de águila ratonera a la parrilla',
             'Asa de Urubu Grelhada')
P_SPELLB = J(S('sp', 16), U(30, 's'))
P_LAE = J(S('sp', 15), U(30, 'min'))
P_MBLOOD = J(S('mp5', 6), U(30, 'min'))
P_CLERIC = J(S('hp', 20), U(30, 'min'))
P_MENDER = J(S('hp', 31), U(30, 's'))
P_MANA = W(MANA_W, 455, 585)
P_LMANA = W(MANA_W, 280, 360)
P_AGI = J(S('agi', 15), U(1, 'h'))
P_OGRE = J(S('str', 8), U(1, 'h'))
P_RAGE = W(RAGE_W, 30, 60)
P_MELON = J(W(MANA_W, 835), U(24, 's'))
P_MMOIL = J(S('hp', 10), S('mp5', 5), U(30, 'min'))
P_BUZZ = J(S('int', 10), U(15, 'min'))


def P_STONE(n):
    return J(W(DMG_W, f'+{n}'), U(30, 'min'))


GHP = (I_GHP, X_GHP)
IV, WH, IVW = 'Icy Veins', 'Wowhead', 'Icy Veins, Wowhead'
CASTER = [(I_SPELLB, P_SPELLB), (I_LAE, P_LAE), (I_WIZOIL, SP_WEAPON), (I_MANA, P_MANA), GHP, (I_STEW, WELL_FED)]
WARRIOR = [GHP, (I_RAGE, P_RAGE), (I_OGRE, P_OGRE), (I_AGI, P_AGI), (I_SOLID, P_STONE(6)), (I_WEIGHT, P_STONE(6))]
HUNTER = [(I_AGI, P_AGI), GHP]
ROGUE = [(I_POISON, E_POISON), (I_STONE, E_STONE), (I_AGI, E_AGI), (I_GHP, E_GHP)]
LOCK = [(I_LAE, P_LAE), (I_MBLOOD, P_MBLOOD), (I_SPELLB, P_SPELLB), GHP]
HEALER = [(I_CLERIC, P_CLERIC), (I_MANA, P_MANA), GHP, (I_STEW, WELL_FED)]
KIT_SP = J(NM(I_KIT), S('sp', 4))
ARCANE_ENCH = [(SLOT['w'], REV), (SLOT['kit'], KIT_SP), (SLOT['neck'], NECK_SP), (SLOT['br'], BR_SP),
               (SLOT['l60'], J(S('sp', 30), {l: f'2H {S("sp", 55)[l]}' for l in LANGS9}))]
# Enchant Necklace - Spell Power: «spell damage and healing by up to 6» (Wowhead Forever, spell 1249057), the healer reads it as healing too
SP_HEAL6 = n9('+6 к урону и лечению заклинаниями', '+6 spell damage and healing', '+6 до шкоди й зцілення заклинаннями',
              '+6 Zauberschaden und Heilung', '+6 aux dégâts et aux soins des sorts', '+6 al daño y la sanación de hechizos',
              '+6 de dano e cura mágicos', '+6 a danni e cure magici', '+6 do obrażeń i leczenia zaklęciami')
HOLY_ENCH = [(SLOT['w'], REV), (SLOT['neck'], EN(E_NECK_SP, SP_HEAL6)), (SLOT['chest'], EN(E_CH_INT, S('int', 4))), (SLOT['legs'], KIT_SP), (SLOT['boots'], SPEED)]
HEAL_NECK = [(SLOT['neck'], S('hp', 11))]
DERIV = n9('Wowhead: база чар, подбор по статам', 'Wowhead: enchant database, picked by stats', 'Wowhead: база чарів, добір за характеристиками',
           'Wowhead: Verzauberungsdatenbank, nach Werten gewählt', 'Wowhead : base d’enchantements, choix selon les caractéristiques',
           'Wowhead: base de encantamientos, elegidos por estadísticas', 'Wowhead: base de encantamentos, escolha por atributos',
           'Wowhead: database degli incantamenti, scelti per statistiche', 'Wowhead: baza zaklęć, dobór według statystyk')
HEAL_ICY = n9('Icy Veins, Wowhead: подбор по статам', 'Icy Veins, Wowhead: picked by stats', 'Icy Veins, Wowhead: добір за характеристиками',
              'Icy Veins, Wowhead: nach Werten gewählt', 'Icy Veins, Wowhead : choix selon les caractéristiques',
              'Icy Veins, Wowhead: elegidos por estadísticas', 'Icy Veins, Wowhead: escolha por atributos',
              'Icy Veins, Wowhead: scelti per statistiche', 'Icy Veins, Wowhead: dobór według statystyk')
KIT_SLOTS = n9('Грудь, ноги, перчатки, сапоги', 'Chest, legs, hands, boots', 'Груди, ноги, рукавиці, чоботи', 'Brust, Beine, Hände, Stiefel',
               'Torse, jambes, mains, bottes', 'Pecho, piernas, manos, botas', 'Peitoral, pernas, mãos, botas', 'Torace, gambe, mani, stivali',
               'Tors, nogi, dłonie, buty')
SHIELD = n9('Щит', 'Shield', 'Щит', 'Schild', 'Bouclier', 'Escudo', 'Escudo', 'Scudo', 'Tarcza')
GLOVES = n9('Перчатки', 'Gloves', 'Рукавиці', 'Handschuhe', 'Handschuhe'.replace('Handschuhe', 'Gants'), 'Guantes', 'Luvas', 'Guanti', 'Rękawice')
CLOAK = n9('Плащ', 'Cloak', 'Плащ', 'Umhang', 'Cape', 'Capa', 'Capa', 'Mantello', 'Płaszcz')
KIT_ONLY_SP = J(NM(I_KIT), S('sp', 4))


SLOT['l60w'] = n9('Оружие на 60 уровне', 'Weapon at level 60', 'Зброя на 60 рівні', 'Waffe auf Stufe 60', 'Arme au niveau 60', 'Arma en el nivel 60',
                  'Arma no nível 60', 'Arma al livello 60', 'Broń na 60 poziomie')


def L60(*ds):
    return (SLOT['l60w'], J(*ds))


def TWOH(d):
    return {l: f'2H {d[l]}' for l in LANGS9}


CL_AGI, BO_AGI = EN(E_CL_AGI, S('agi', 3)), EN(E_BO_AGI, S('agi', 4))
AGI_ENCH = [(SLOT['br'], S('agi', 5)), (GLOVES, EN(E_GL_AGI, S('agi', 7))), (SLOT['neck'], S('agi', 5)), (CLOAK, CL_AGI), (SLOT['boots'], BO_AGI),
            L60(S('agi', 15), TWOH(S('agi', 25)))]
STR_ENCH = [(SLOT['br'], EN(E_BR_STR, S('str', 5))), (GLOVES, EN(E_GL_STR, S('str', 7))), (SLOT['neck'], S('str', 5)), (CLOAK, CL_AGI),
            (SLOT['boots'], BO_AGI),
            (SLOT['w'], TWOH(S('str', 15))), L60(S('str', 15), TWOH(S('str', 25)))]
TANK_ENCH = [(SLOT['br'], EN(E_BR_STA, S('sta', 5))), (SLOT['chest'], EN(E_CH_STA, S('sta', 8))), (SLOT['boots'], EN(E_BO_STA, S('sta', 5))),
             (SLOT['neck'], S('def', 5)), (SHIELD, EN(E_SH_STA, S('sta', 7))),
             (SLOT['l60'], J({l: f'{GLOVES[l]} {S("thr", 2)[l]}' for l in LANGS9}, {l: f'{CLOAK[l]} {S("dodge", 1)[l]}' for l in LANGS9}))]
CASTER_ENCH = [(KIT_SLOTS, KIT_ONLY_SP), (SLOT['neck'], NECK_SP), (SLOT['br'], BR_SP), L60(S('sp', 30), TWOH(S('sp', 55)))]
HEAL_ENCH = [(SLOT['neck'], S('hp', 11)), (SLOT['br'], EN(E_BR_LHP, S('hp', 16))), (SLOT['chest'], EN(E_CH_GINT, S('int', 6))), (SLOT['legs'], KIT_ONLY_SP), (SLOT['boots'], SPEED),
             L60(S('hp', 55), TWOH(S('hp', 100)))]
MAGE_ENCH = [(SLOT['w'], REV), (SLOT['kit'], KIT_SP), (SLOT['neck'], NECK_SP), (SLOT['br'], BR_SP), (SLOT['boots'], SPEED),
             L60(S('sp', 30), TWOH(S('sp', 55)))]
# Enhancement: Wowhead Forever's Enchants & Consumables page (29.10) names only the weapon, Revelation (procs from
# non-periodic spells); the rest of the slots are the strength picks of the other melee specs, picked by stats
ENH_ENCH = [(SLOT['w'], REV)] + STR_ENCH[:5]
ENH_SRC = n9('Wowhead: оружие — список спека, остальное — база чар, подбор по статам',
             'Wowhead: the weapon from the spec list, the rest from the enchant database, picked by stats',
             'Wowhead: зброя — список спеку, решта — база чарів, добір за характеристиками',
             'Wowhead: Waffe aus der Liste der Skillung, der Rest aus der Verzauberungsdatenbank, nach Werten gewählt',
             'Wowhead : l’arme d’après la liste de la spécialisation, le reste d’après la base d’enchantements, selon les caractéristiques',
             'Wowhead: el arma de la lista de la especialización, el resto de la base de encantamientos, elegidos por estadísticas',
             'Wowhead: a arma da lista da especialização, o resto da base de encantamentos, escolha por atributos',
             'Wowhead: l’arma dall’elenco della specializzazione, il resto dal database degli incantamenti, scelti per statistiche',
             'Wowhead: broń z listy specjalizacji, reszta z bazy zaklęć, dobór według statystyk')
ELE_ENCH = [(SLOT['w'], REV), (KIT_SLOTS, KIT_ONLY_SP), (SLOT['br'], S('sp', 12)), (SLOT['l60'], {l: f'{SLOT["br"][l]} {S("sp", 16)[l]}' for l in LANGS9})]

# (class-spec) -> row index (0 enchants, 1 consumables, 2 gems and materials) -> ([(label, effect)], source). No entry: the WAIT line of the row
GEAR = {
    'rogue-combat': {1: (ROGUE, IVW)}, 'rogue-assassination': {1: (ROGUE, IVW)}, 'rogue-subtlety': {1: (ROGUE, IVW)},
    'warrior-arms': {1: (WARRIOR, IVW)}, 'warrior-fury': {1: (WARRIOR, IVW)}, 'warrior-protection': {1: (WARRIOR, IVW)},
    'hunter-beast-mastery': {1: (HUNTER, IVW)}, 'hunter-marksmanship': {1: (HUNTER, IVW)}, 'hunter-survival': {1: (HUNTER, IVW)},
    'druid-feral': {1: ([GHP, (I_AGI, P_AGI), (I_OGRE, P_OGRE), (I_COARSE, P_STONE(3)), (I_WEIGHT, P_STONE(6))], IVW)},
    'druid-balance': {1: ([(I_LAE, P_LAE), GHP], IVW)},
    'mage-arcane': {0: (ARCANE_ENCH, WH), 1: (CASTER, IVW)}, 'mage-fire': {1: (CASTER, IVW)}, 'mage-frost': {1: (CASTER, IVW)},
    'warlock-affliction': {1: (LOCK, IVW)}, 'warlock-demonology': {1: (LOCK, IVW)}, 'warlock-destruction': {1: (LOCK, IVW)},
    'priest-shadow': {1: ([(I_WIZOIL, SP_WEAPON), (I_LAE, P_LAE), (I_STEW, WELL_FED), GHP], IVW)},
    'shaman-elemental': {1: ([(I_LAE, P_LAE), (I_SPELLB, P_SPELLB), (I_MANA, P_MANA), GHP], IVW)},
    'shaman-enhancement': {1: ([GHP, (I_LMANA, P_LMANA), (I_OGRE, P_OGRE), (I_MBLOOD, P_MBLOOD)], IVW)},   # Icy Veins: healing and Lesser Mana Potions, Mageblood, Ogre Strength
    'shaman-restoration': {1: ([(I_CLERIC, P_CLERIC), (I_MENDER, P_MENDER), (I_MANA, P_MANA), GHP], IVW)},
    'priest-discipline': {0: (HEAL_NECK, IVW), 1: (HEALER, IVW)}, 'priest-holy': {0: (HEAL_NECK, IVW), 1: (HEALER, IVW)},
    'paladin-holy': {0: (HOLY_ENCH, WH), 1: ([(I_MANA, P_MANA), (I_SHP, X_SHP), (I_MMOIL, P_MMOIL), (I_BUZZ, P_BUZZ)], WH)},   # Wowhead's list by type, the picks for level 20–39
    'druid-restoration': {1: ([(I_LAE, P_LAE), (I_LHP, X_LHP), (I_MANA, P_MANA), (I_MELON, P_MELON)], IV)},   # Icy Veins: Consumables
    'paladin-retribution': {1: ([GHP, (I_MANA, P_MANA), (I_LAE, P_LAE), (I_SPELLB, P_SPELLB)], IVW)},
}
ENCH_ADD = {
    'rogue-combat': (AGI_ENCH, DERIV),
    'rogue-assassination': (AGI_ENCH, DERIV),
    'rogue-subtlety': (AGI_ENCH, DERIV),
    'druid-feral': (AGI_ENCH, DERIV),
    'hunter-beast-mastery': (AGI_ENCH, DERIV),
    'hunter-marksmanship': (AGI_ENCH, DERIV),
    'hunter-survival': (AGI_ENCH, DERIV),
    'warrior-arms': (STR_ENCH, DERIV),
    'warrior-fury': (STR_ENCH, DERIV),
    'paladin-retribution': (STR_ENCH, DERIV),
    'warrior-protection': (TANK_ENCH, DERIV),
    'paladin-protection': (TANK_ENCH, DERIV),
    'warlock-affliction': (CASTER_ENCH, DERIV),
    'warlock-demonology': (CASTER_ENCH, DERIV),
    'warlock-destruction': (CASTER_ENCH, DERIV),
    'priest-shadow': (CASTER_ENCH, DERIV),
    'priest-discipline': (HEAL_ENCH, HEAL_ICY),
    'priest-holy': (HEAL_ENCH, HEAL_ICY),
    'shaman-restoration': (HEAL_ENCH, DERIV),
    'druid-restoration': (HEAL_ENCH, DERIV),
    'mage-fire': (MAGE_ENCH, WH),
    'mage-frost': (MAGE_ENCH, WH),
    'druid-balance': (MAGE_ENCH, WH),
    'shaman-elemental': (ELE_ENCH, WH),
    'shaman-enhancement': (ENH_ENCH, ENH_SRC),
}
for _k, (_lines, _src) in ENCH_ADD.items():
    GEAR.setdefault(_k, {})[0] = (_lines, _src)
GEAR['mage-arcane'][0] = (MAGE_ENCH, WH)
GEAR['paladin-holy'][0] = (HOLY_ENCH, WH)
ENCH_UNREAD = set()
WAIT_UNREAD = n9('Ждёт данных: у Wowhead есть список чар для этого спека, на сайт он ещё не перенесён.',
                 'Waiting for data: Wowhead has an enchant list for this spec, not yet on the site.',
                 'Чекає на дані: у Wowhead є список чарів для цього спеку, на сайт його ще не перенесено.',
                 'Wartet auf Daten: Wowhead hat eine Verzauberungsliste für diese Skillung, sie ist noch nicht auf der Seite.',
                 'En attente de données : Wowhead a une liste d’enchantements pour cette spécialisation, pas encore sur le site.',
                 'A la espera de datos: Wowhead tiene una lista de encantamientos para esta especialización, aún no está en el sitio.',
                 'Aguardando dados: o Wowhead tem uma lista de encantamentos para esta especialização, ainda não está no site.',
                 'In attesa di dati: Wowhead ha un elenco di incantamenti per questa specializzazione, non ancora sul sito.',
                 'Czeka na dane: Wowhead ma listę zaklęć dla tej specjalizacji, nie ma jej jeszcze na stronie.')

FAQ_T = n9('Вопросы', 'Questions', 'Питання', 'Fragen', 'Questions', 'Preguntas', 'Perguntas', 'Domande', 'Pytania')
# Button and tab names as talents.py shows them (ed, share, b_general, b_leveling)
FAQ = [
    {'id': 'copy-build',
     'q': n9('Как скопировать билд?', 'How do I copy the build?', 'Як скопіювати білд?', 'Wie kopiere ich den Build?', 'Comment copier le build ?',
             '¿Cómo copio la build?', 'Como copio a build?', 'Come copio la build?', 'Jak skopiować build?'),
     'a': [n9('В разделе «Таланты» нажмите «Собрать свой билд», расставьте очки и нажмите «Копировать билд»: очки сохранятся в ссылке. Кнопка наверху страницы делится ссылкой на эту шпору.',
              'In the Talents section, press “Make your own build”, place the points and press “Copy build”: the points are kept in the link. The button at the top of the page shares a link to this cheat sheet.',
              'У розділі «Таланти» натисніть «Зібрати свій білд», розставте очки й натисніть «Копіювати білд»: очки збережуться в посиланні. Кнопка вгорі сторінки ділиться посиланням на цю шпору.',
              'Im Abschnitt Talente auf „Eigenen Build erstellen“ tippen, Punkte setzen und „Build kopieren“ drücken: Die Punkte stehen im Link. Der Knopf oben teilt einen Link zu diesem Spickzettel.',
              'Dans la section Talents, appuyez sur « Créer votre build », placez les points puis sur « Copier le build » : les points restent dans le lien. Le bouton en haut de la page partage un lien vers cette fiche.',
              'En la sección Talentos, pulsa «Crear tu build», coloca los puntos y pulsa «Copiar build»: los puntos quedan en el enlace. El botón de arriba comparte un enlace a esta guía rápida.',
              'Na seção Talentos, toque em “Montar sua build”, distribua os pontos e toque em “Copiar build”: os pontos ficam no link. O botão no topo compartilha um link para este resumo.',
              'Nella sezione Talenti premi «Crea la tua build», assegna i punti e premi «Copia build»: i punti restano nel link. Il pulsante in alto condivide un link a questa scheda.',
              'W sekcji Talenty naciśnij „Złóż własny build”, rozdaj punkty i naciśnij „Kopiuj build”: punkty zostają w linku. Przycisk na górze strony udostępnia link do tej ściągi.')]},
    {'id': 'leveling-tab',
     'q': n9('Зачем вкладка «Прокачка» у талантов?', 'What is the “Leveling” tab in the talents for?', 'Навіщо вкладка «Прокачка» в талантах?',
             'Wozu dient der Reiter „Leveln“ bei den Talenten?', 'À quoi sert l’onglet « Progression » des talents ?',
             '¿Para qué sirve la pestaña «Subida de nivel» de los talentos?', 'Para que serve a aba “Evolução” dos talentos?',
             'A cosa serve la scheda «Livellamento» dei talenti?', 'Po co jest zakładka „Levelowanie” w talentach?'),
     'a': [n9('«Общая» — раскладка очков на 30 уровне по бете. «Прокачка» — порядок очков с 10 по 60 уровень; 31–60 взяты из гайда прокачки класса, после старта сверим их с игрой.',
              '“General” is the level 30 point layout from the beta. “Leveling” is the order of points from level 10 to 60; levels 31–60 come from the class leveling guide, and we will check them against the game after launch.',
              '«Загальна» — розкладка очок на 30 рівні за бетою. «Прокачка» — порядок очок з 10 по 60 рівень; 31–60 узяті з гайду прокачування класу, після старту звіримо їх із грою.',
              '„Allgemein“ ist die Punkteverteilung auf Stufe 30 aus der Beta. „Leveln“ ist die Reihenfolge der Punkte von Stufe 10 bis 60; 31–60 stammen aus dem Level-Guide der Klasse, nach dem Start gleichen wir sie mit dem Spiel ab.',
              '« Général » est la répartition des points au niveau 30 d’après la bêta. « Progression » est l’ordre des points du niveau 10 au 60 ; les niveaux 31–60 viennent du guide de progression de la classe, nous les vérifierons dans le jeu après le lancement.',
              '«General» es el reparto de puntos del nivel 30 según la beta. «Subida de nivel» es el orden de los puntos del nivel 10 al 60; del 31 al 60 sale de la guía de subida de la clase y lo comprobaremos en el juego tras el lanzamiento.',
              '“Geral” é a distribuição de pontos do nível 30 segundo a beta. “Evolução” é a ordem dos pontos do nível 10 ao 60; do 31 ao 60 vem do guia de evolução da classe e vamos conferir no jogo após o lançamento.',
              '«Generale» è la distribuzione dei punti al livello 30 secondo la beta. «Livellamento» è l’ordine dei punti dal livello 10 al 60; i livelli 31–60 vengono dalla guida al livellamento della classe e li verificheremo nel gioco dopo il lancio.',
              '„Ogólna” to rozkład punktów na 30 levelu z bety. „Levelowanie” to kolejność punktów od 10 do 60 levelu; poziomy 31–60 pochodzą z poradnika levelowania klasy, po starcie sprawdzimy je w grze.')]},
    {'id': 'legacy-points',
     'q': n9('Что с очками Legacy?', 'What about the Legacy points?', 'Що з очками Legacy?', 'Was ist mit den Legacy-Punkten?',
             'Et les points Legacy ?', '¿Qué pasa con los puntos de Legacy?', 'E os pontos de Legacy?', 'E i punti Legacy?', 'Co z punktami Legacy?'),
     'a': [n9('Перк Legacy Talented (до 5 рангов) открывает очки талантов раньше нормы, до 5 уровней. Куда их тратить, сказано в разделе «Таланты», если источники это называют. Все перки — в гайде Legacy.',
              'The Legacy perk Talented (up to 5 ranks) unlocks talent points earlier than normal, by up to 5 levels. Where to spend them is in the Talents section when the sources name it. All perks are in the Legacy guide.',
              'Перк Legacy Talented (до 5 рангів) відкриває очки талантів раніше за норму, до 5 рівнів. Куди їх витрачати, сказано в розділі «Таланти», якщо джерела це називають. Усі перки — в гайді Legacy.',
              'Der Legacy-Vorteil Talented (bis zu 5 Ränge) schaltet Talentpunkte früher frei, um bis zu 5 Stufen. Wohin damit, steht im Abschnitt Talente, wenn die Quellen es nennen. Alle Vorteile stehen im Legacy-Guide.',
              'L’avantage Legacy Talented (jusqu’à 5 rangs) débloque les points de talent plus tôt, jusqu’à 5 niveaux. Où les dépenser est indiqué dans la section Talents quand les sources le précisent. Tous les avantages sont dans le guide Legacy.',
              'La ventaja de Legacy Talented (hasta 5 rangos) desbloquea los puntos de talento antes, hasta 5 niveles. Dónde gastarlos se indica en la sección Talentos cuando las fuentes lo dicen. Todas las ventajas están en la guía de Legacy.',
              'O benefício de Legacy Talented (até 5 níveis) libera pontos de talento mais cedo, em até 5 níveis. Onde gastá-los está na seção Talentos quando as fontes dizem. Todos os benefícios estão no guia de Legacy.',
              'Il vantaggio Legacy Talented (fino a 5 gradi) sblocca i punti talento prima, fino a 5 livelli. Dove spenderli è indicato nella sezione Talenti quando le fonti lo dicono. Tutti i vantaggi sono nella guida Legacy.',
              'Atut Legacy Talented (do 5 rang) odblokowuje punkty talentów wcześniej, nawet o 5 leveli. Gdzie je wydać, podano w sekcji Talenty, jeśli źródła to mówią. Wszystkie atuty są w poradniku Legacy.')],
     'link': (n9('Гайд Legacy', 'Legacy guide', 'Гайд Legacy', 'Legacy-Guide', 'Guide Legacy', 'Guía de Legacy', 'Guia de Legacy', 'Guida Legacy',
                 'Poradnik Legacy'), '../legacy/')},
]
CHIPS_LEAD = n9('Шпора каждого спека: билд, таланты, прокачка и группа на одной странице.',
                'A cheat sheet for every spec: build, talents, leveling and group on one page.',
                'Шпора для кожного спека: білд, таланти, прокачування і група на одній сторінці.',
                'Ein Spickzettel für jede Skillung: Build, Talente, Leveln und Gruppe auf einer Seite.',
                'Une fiche pour chaque spécialisation : build, talents, progression et groupe sur une page.',
                'Una guía rápida por especialización: build, talentos, subida y grupo en una página.',
                'Um resumo para cada especialização: build, talentos, evolução e grupo em uma página.',
                'Una scheda per ogni specializzazione: build, talenti, salita e gruppo in una pagina.',
                'Ściąga dla każdej specjalizacji: build, talenty, levelowanie i grupa na jednej stronie.')
NEXT_PFX = n9('Дальше', 'Next', 'Далі', 'Weiter', 'Suite', 'Siguiente', 'Próximo', 'Avanti', 'Dalej')


# A row no spec has data for (now: gems and materials, none at the level 30 cap) is left out instead of 27 equal waiting lines
ROWS_ON = [i for i in range(len(GEAR_ROWS)) if any(i in g for g in GEAR.values())]


def _name(x, lang):
    return x if isinstance(x, str) else (x.get(lang) or x['en'])


# ---------- Gear 13–30: data/gear30.json (tools/gear_import.py), one table by slot. No items for a spec: no section, no answer row ----------
GEAR30_PATH = os.environ.get('GABELLA_GEAR30') or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'gear30.json')


def load_gear30(path=None):
    p = path or GEAR30_PATH
    try:
        with open(p, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError):
        return {'items': {}, 'specs': {}}


GEAR30_FILE = load_gear30()
# the build shows the section only for data Вячеслав accepted ("approved": true, tools/gear_import.py --approve);
# imported but not accepted: section and answer row stay hidden. The Wowhead level-30 import of 30.10 is accepted (31.10) for all 27 specs
# with the mark «temporary, beta data» until the addon dump, and «incomplete» on the specs listed in "partial" (fewer than GEAR_MIN_SLOTS slots)
GEAR30 = GEAR30_FILE if GEAR30_FILE.get('approved') else {'items': {}, 'specs': {}}
GEAR_MIN_SLOTS = 6
GSLOTS = ('head', 'neck', 'shoulder', 'back', 'chest', 'wrist', 'hands', 'waist', 'legs', 'feet', 'finger', 'trinket',
          'main', 'two', 'off', 'ranged')
GSLOT = {
    'head': n9('Голова', 'Head', 'Голова', 'Kopf', 'Tête', 'Cabeza', 'Cabeça', 'Testa', 'Głowa'), 'neck': SLOT['neck'],
    'shoulder': n9('Плечи', 'Shoulder', 'Плечі', 'Schultern', 'Épaules', 'Hombros', 'Ombros', 'Spalle', 'Ramiona'),
    'back': n9('Спина', 'Back', 'Спина', 'Rücken', 'Dos', 'Espalda', 'Costas', 'Schiena', 'Plecy'), 'chest': SLOT['chest'],
    'wrist': n9('Запястья', 'Wrist', 'Зап’ястя', 'Handgelenke', 'Poignets', 'Muñeca', 'Pulsos', 'Polsi', 'Nadgarstki'),
    'hands': n9('Кисти рук', 'Hands', 'Кисті рук', 'Hände', 'Mains', 'Manos', 'Mãos', 'Mani', 'Dłonie'),
    'waist': n9('Пояс', 'Waist', 'Пояс', 'Taille', 'Taille', 'Cintura', 'Cintura', 'Vita', 'Talia'), 'legs': SLOT['legs'],
    'feet': n9('Ступни', 'Feet', 'Ступні', 'Füße', 'Pieds', 'Pies', 'Pés', 'Piedi', 'Stopy'),
    'finger': n9('Палец', 'Finger', 'Палець', 'Finger', 'Doigt', 'Dedo', 'Dedo', 'Dito', 'Palec'),
    'trinket': n9('Аксессуар', 'Trinket', 'Аксесуар', 'Schmuck', 'Bijou', 'Abalorio', 'Berloque', 'Monile', 'Błyskotka'),
    'main': n9('Одноручное', 'One-hand', 'Одноручна', 'Einhändig', 'À une main', 'Una mano', 'Uma mão', 'Una mano', 'Jednoręczna'),
    'two': n9('Двуручное', 'Two-hand', 'Дворучна', 'Zweihändig', 'Deux mains', 'Dos manos', 'Duas mãos', 'Due mani', 'Dwuręczna'),
    'off': n9('Левая рука', 'Off hand', 'Ліва рука', 'Schildhand', 'Main gauche', 'Mano izquierda', 'Mão secundária', 'Mano secondaria',
              'Druga ręka'),
    'ranged': n9('Дальний бой', 'Ranged', 'Далекий бій', 'Distanz', 'À distance', 'A distancia', 'À distância', 'A distanza', 'Dystansowa')}
G_TITLE = n9('Экипировка 13–30', 'Gear 13–30', 'Екіпірування 13–30', 'Ausrüstung 13–30', 'Équipement 13–30', 'Equipo 13–30',
             'Equipamento 13–30', 'Equipaggiamento 13–30', 'Ekwipunek 13–30')
G_ROW = n9('Экипировка', 'Gear', 'Екіпірування', 'Ausrüstung', 'Équipement', 'Equipo', 'Equipamento', 'Equipaggiamento', 'Ekwipunek')
G_HEAD = [n9('Ячейка', 'Slot', 'Комірка', 'Platz', 'Emplacement', 'Ranura', 'Espaço', 'Slot', 'Miejsce'),
          n9('Предмет', 'Item', 'Предмет', 'Gegenstand', 'Objet', 'Objeto', 'Item', 'Oggetto', 'Przedmiot'),
          n9('Ур.', 'Lvl', 'Рів.', 'St.', 'Niv.', 'Nv.', 'Nv.', 'Liv.', 'Poz.'),
          n9('Где взять', 'Source', 'Де взяти', 'Quelle', 'Source', 'Origen', 'Origem', 'Fonte', 'Źródło')]
G_LEAD = n9('Предметы до 30 уровня по ячейкам экипировки и где их взять. В ячейке сверху предмет выше уровнем; «Мой уровень» скрывает то, что пока не надеть.',
            'Items up to level 30 by equipment slot, and where to get them. The higher-level item of a slot is on top; “My level” hides what you cannot wear yet.',
            'Предмети до 30 рівня за комірками екіпірування і де їх узяти. У комірці згори предмет вищого рівня; «Мій рівень» ховає те, що поки не вдягнути.',
            'Gegenstände bis Stufe 30 nach Ausrüstungsplatz und woher sie kommen. Oben steht jeweils der höherstufige; „Meine Stufe“ blendet aus, was du noch nicht tragen kannst.',
            'Objets jusqu’au niveau 30 par emplacement, et où les obtenir. L’objet de plus haut niveau est en haut ; « Mon niveau » masque ce que vous ne pouvez pas encore porter.',
            'Objetos hasta el nivel 30 por ranura y dónde conseguirlos. Arriba va el de mayor nivel; «Mi nivel» oculta lo que aún no puedes llevar.',
            'Itens até o nível 30 por espaço de equipamento e onde conseguir. O de nível mais alto fica em cima; “Meu nível” oculta o que você ainda não pode usar.',
            'Oggetti fino al livello 30 per slot e dove trovarli. In alto c’è quello di livello più alto; «Il mio livello» nasconde ciò che non puoi ancora indossare.',
            'Przedmioty do 30 poziomu według miejsca w ekwipunku i skąd je wziąć. Na górze jest przedmiot wyższego poziomu; „Mój poziom” ukrywa to, czego jeszcze nie założysz.')
G_ALL = n9('Все', 'All', 'Усі', 'Alle', 'Tous', 'Todos', 'Todos', 'Tutti', 'Wszystkie')
G_FAC = n9('Фракция', 'Faction', 'Фракція', 'Fraktion', 'Faction', 'Facción', 'Facção', 'Fazione', 'Frakcja')
G_MYLVL = n9('Мой уровень', 'My level', 'Мій рівень', 'Meine Stufe', 'Mon niveau', 'Mi nivel', 'Meu nível', 'Il mio livello', 'Mój poziom')
G_LO = n9('Уровень ниже', 'Lower level', 'Нижчий рівень', 'Niedrigere Stufe', 'Niveau inférieur', 'Nivel menor', 'Nível menor', 'Livello inferiore',
          'Niższy poziom')
G_HI = n9('Уровень выше', 'Higher level', 'Вищий рівень', 'Höhere Stufe', 'Niveau supérieur', 'Nivel mayor', 'Nível maior', 'Livello superiore',
          'Wyższy poziom')
G_MYPROF = n9('Только мои профессии', 'Only my professions', 'Лише мої професії', 'Nur meine Berufe', 'Mes métiers seulement',
              'Solo mis profesiones', 'Só minhas profissões', 'Solo le mie professioni', 'Tylko moje profesje')
G_SHOWN = n9('Показано %n из %t', 'Showing %n of %t', 'Показано %n з %t', '%n von %t angezeigt', '%n sur %t affichés', 'Se muestran %n de %t',
             'Mostrando %n de %t', 'Mostrati %n di %t', 'Pokazano %n z %t')
G_NONE = n9('Под этот уровень и фильтр предметов нет.', 'No items for this level and filter.', 'Під цей рівень і фільтр предметів немає.',
            'Keine Gegenstände für diese Stufe und diesen Filter.', 'Aucun objet pour ce niveau et ce filtre.', 'No hay objetos para este nivel y filtro.',
            'Nenhum item para este nível e filtro.', 'Nessun oggetto per questo livello e filtro.', 'Brak przedmiotów dla tego poziomu i filtra.')
G_QUEST = n9('Квест', 'Quest', 'Квест', 'Quest', 'Quête', 'Misión', 'Missão', 'Missione', 'Zadanie')
G_SRC = {
    'wowhead-forever-guide': n9(
        'Источник: гайды Wowhead Forever, данные беты на {d}.', 'Source: Wowhead Forever guides, beta data as of {d}.',
        'Джерело: гайди Wowhead Forever, дані бети на {d}.', 'Quelle: Wowhead-Forever-Guides, Beta-Daten vom {d}.',
        'Source : guides Wowhead Forever, données de la bêta au {d}.', 'Fuente: guías de Wowhead Forever, datos de la beta a {d}.',
        'Fonte: guias do Wowhead Forever, dados da beta de {d}.', 'Fonte: guide di Wowhead Forever, dati della beta al {d}.',
        'Źródło: poradniki Wowhead Forever, dane z bety na {d}.'),
    'client-dump': n9(
        'Источник: данные клиента Forever на {d}.', 'Source: Forever client data as of {d}.', 'Джерело: дані клієнта Forever на {d}.',
        'Quelle: Client-Daten von Forever vom {d}.', 'Source : données du client Forever au {d}.', 'Fuente: datos del cliente de Forever a {d}.',
        'Fonte: dados do cliente Forever de {d}.', 'Fonte: dati del client Forever al {d}.', 'Źródło: dane klienta Forever na {d}.')}
G_L60 = n9('Предметы 31–60 ждут данных: на бете их статы и добыча боссов закрыты.',
           'Items for levels 31–60 are waiting for data: their stats and boss loot were hidden in the beta.',
           'Предмети 31–60 чекають на дані: на беті їхні характеристики й здобич босів закриті.',
           'Gegenstände für Stufe 31–60 warten auf Daten: Werte und Bossbeute waren in der Beta verborgen.',
           'Les objets des niveaux 31–60 attendent des données : leurs caractéristiques et le butin des boss étaient masqués dans la bêta.',
           'Los objetos de nivel 31–60 esperan datos: sus estadísticas y el botín de jefes estaban ocultos en la beta.',
           'Os itens dos níveis 31–60 aguardam dados: atributos e saque de chefes estavam ocultos na beta.',
           'Gli oggetti dei livelli 31–60 attendono dati: statistiche e bottino dei boss erano nascosti nella beta.',
           'Przedmioty na poziomy 31–60 czekają na dane: w becie ich statystyki i łupy bossów były ukryte.')
G_TEST = n9('Тестовые данные: не для публикации.', 'Test data: not for publishing.', 'Тестові дані: не для публікації.',
            'Testdaten: nicht zur Veröffentlichung.', 'Données de test : ne pas publier.', 'Datos de prueba: no publicar.',
            'Dados de teste: não publicar.', 'Dati di prova: da non pubblicare.', 'Dane testowe: nie do publikacji.')
# the marks on top of the section: beta data (until the client dump replaces it) and a spec with not all slots filled
G_TEMP = n9('Временно: данные беты, обновим после старта игры.', 'Temporary: beta data, to be updated after the game launches.',
            'Тимчасово: дані бети, оновимо після старту гри.', 'Vorläufig: Beta-Daten, wir aktualisieren sie nach dem Spielstart.',
            'Provisoire : données de la bêta, mises à jour après le lancement du jeu.',
            'Provisional: datos de la beta, los actualizaremos tras el lanzamiento del juego.',
            'Provisório: dados da beta, atualizaremos após o lançamento do jogo.',
            'Provvisorio: dati della beta, li aggiorneremo dopo il lancio del gioco.',
            'Tymczasowo: dane z bety, zaktualizujemy je po starcie gry.')
G_PART = n9('Неполно: предметы есть только для {n} ячеек, остальные пока не заполнены.',
            'Incomplete: items for {n} slots only, the other slots are not filled yet.',
            'Неповно: предмети є лише для {n} комірок, решта поки не заповнені.',
            'Unvollständig: Gegenstände nur für {n} Plätze, die übrigen sind noch leer.',
            'Incomplet : des objets pour {n} emplacements seulement, les autres ne sont pas encore remplis.',
            'Incompleto: solo hay objetos para {n} ranuras, las demás aún están vacías.',
            'Incompleto: há itens só para {n} espaços, os demais ainda não foram preenchidos.',
            'Incompleto: oggetti solo per {n} slot, gli altri non sono ancora compilati.',
            'Niepełne: przedmioty tylko dla {n} miejsc, pozostałe nie są jeszcze uzupełnione.')
# items of tools/gear_fill.py ("pick": "stats"): not the advice of this spec's guide but our pick by its stat priority from the lists of
# other specs; a badge on each such row, a mark on top and a line next to the source, so a pick never reads as the guide's advice
G_PICK = n9('Подбор по статам', 'Picked by stats', 'Добір за характеристиками', 'Nach Werten gewählt', 'Choisi selon les stats',
            'Elegido por estadísticas', 'Escolhido por atributos', 'Scelto per statistiche', 'Dobór według statystyk')
G_PICK_NOTE = n9(
    'Подбор по статам: {n} из {t} предметов не из гайда этого спека, а подобраны по его приоритету статов из списков других спеков. В таблице они отмечены.',
    'Picked by stats: {n} of {t} items are not from this spec’s guide; we picked them by its stat priority from other specs’ lists. They are marked in the table.',
    'Добір за характеристиками: {n} з {t} предметів не з гайду цього спеку, а дібрані за його пріоритетом характеристик зі списків інших спеків. У таблиці вони позначені.',
    'Nach Werten gewählt: {n} von {t} Gegenständen stammen nicht aus dem Guide dieser Skillung, sondern sind nach ihrer Werte-Priorität aus Listen anderer Skillungen gewählt. Sie sind in der Tabelle markiert.',
    'Choisis selon les stats : {n} objets sur {t} ne viennent pas du guide de cette spécialisation, mais des listes d’autres, choisis selon sa priorité de caractéristiques. Ils sont signalés dans le tableau.',
    'Elegidos por estadísticas: {n} de {t} objetos no son de la guía de esta especialización, sino de listas de otras, elegidos por su prioridad de estadísticas. Están marcados en la tabla.',
    'Escolhidos por atributos: {n} de {t} itens não vêm do guia desta especialização, e sim de listas de outras, escolhidos pela prioridade de atributos dela. Estão marcados na tabela.',
    'Scelti per statistiche: {n} oggetti su {t} non vengono dalla guida di questa specializzazione, ma da elenchi di altre, scelti secondo la sua priorità di statistiche. Sono segnati nella tabella.',
    'Dobór według statystyk: {n} z {t} przedmiotów nie pochodzi z poradnika tej specjalizacji, tylko z list innych, dobranych według jej priorytetu statystyk. W tabeli są oznaczone.')
G_SRC_PICK = n9('Предметы «Подбор по статам» выбрали мы, по приоритету статов спека, из списков других спеков в тех же гайдах.',
                'Items marked “Picked by stats” were chosen by us, by the spec’s stat priority, from other specs’ lists in the same guides.',
                'Предмети «Добір за характеристиками» вибрали ми, за пріоритетом характеристик спеку, зі списків інших спеків у тих самих гайдах.',
                'Gegenstände mit „Nach Werten gewählt“ haben wir nach der Werte-Priorität der Skillung aus Listen anderer Skillungen derselben Guides gewählt.',
                'Les objets « Choisi selon les stats » ont été choisis par nous, selon la priorité de la spécialisation, dans les listes d’autres spécialisations des mêmes guides.',
                'Los objetos «Elegido por estadísticas» los elegimos nosotros, por la prioridad de la especialización, de listas de otras en las mismas guías.',
                'Os itens “Escolhido por atributos” foram escolhidos por nós, pela prioridade da especialização, de listas de outras nos mesmos guias.',
                'Gli oggetti «Scelto per statistiche» li abbiamo scelti noi, secondo la priorità della specializzazione, da elenchi di altre nelle stesse guide.',
                'Przedmioty „Dobór według statystyk” wybraliśmy my, według priorytetu specjalizacji, z list innych specjalizacji w tych samych poradnikach.')
G_WORLD = n9('Добыча в мире', 'World drop', 'Здобич у світі', 'Weltdrop', 'Butin du monde', 'Botín del mundo', 'Saque do mundo',
             'Bottino del mondo', 'Łup ze świata')   # a drop the guide lists as a world drop: no boss, no dungeon
G_TEMP_S = n9('данные беты', 'beta data', 'дані бети', 'Beta-Daten', 'données de la bêta', 'datos de la beta', 'dados da beta', 'dati della beta',
              'dane z bety')
G_PART_S = n9('неполно', 'incomplete', 'неповно', 'unvollständig', 'incomplet', 'incompleto', 'incompleto', 'incompleto', 'niepełne')
G_N = n9('Предметов', 'Items', 'Предметів', 'Gegenstände', 'Objets', 'Objetos', 'Itens', 'Oggetti', 'Przedmiotów')
G_LV = n9('ур.', 'lvl', 'рів.', 'St.', 'niv.', 'nv.', 'nv.', 'liv.', 'poz.')
G_GO = n9('Таблица по ячейкам', 'Table by slot', 'Таблиця за комірками', 'Tabelle nach Platz', 'Tableau par emplacement', 'Tabla por ranura',
          'Tabela por espaço', 'Tabella per slot', 'Tabela według miejsc')
G_PROF = {'blacksmithing': 'Кузнечное дело', 'leatherworking': 'Кожевничество', 'tailoring': 'Портняжное дело', 'engineering': 'Инженерное дело',
          'enchanting': 'Наложение чар', 'alchemy': 'Алхимия', 'firstaid': 'Первая помощь', 'cooking': 'Кулинария'}   # ru names of PROFS (index.src.html)
EXTRA['ap'] = n9('Сила атаки', 'Attack power', 'Сила атаки', 'Angriffskraft', 'Puissance d’attaque', 'Poder de ataque', 'Poder de ataque',
                 'Potere d’attacco', 'Moc ataku')
for _l, _w in (('ru', 'силы атаки'), ('uk', 'сили атаки'), ('pl', 'mocy ataku')):
    GEN[_l]['ap'] = _w
G_DPS = n9('урона в секунду', 'damage per second', 'шкоди за секунду', 'Schaden pro Sekunde', 'dégâts par seconde', 'de daño por segundo',
           'de dano por segundo', 'danni al secondo', 'obrażeń na sekundę')
G_SPHP = n9('+{n} к урону и лечению заклинаниями', '+{n} spell damage and healing', '+{n} до шкоди й зцілення заклинаннями',
            '+{n} Zauberschaden und Heilung', '+{n} aux dégâts et aux soins des sorts', '+{n} al daño y la sanación de hechizos',
            '+{n} de dano e cura mágicos', '+{n} a danni e cure magici', '+{n} do obrażeń i leczenia zaklęciami')
WH_LANG = {'ru': 'ru/', 'de': 'de/', 'fr': 'fr/', 'es': 'es/', 'pt': 'pt/', 'it': 'it/'}


def _fmt(v, lang):
    s = f'{v:g}'
    return s if lang == 'en' else s.replace('.', ',')


def gear_stats(st, lang):
    """«18,5 урона в секунду, +10 интеллекта, +6 выносливости»: weapon damage first, then armor, then the stats in a fixed order."""
    out = []
    if st.get('dps'):
        out.append(f'{_fmt(st["dps"], lang)} {G_DPS[lang]}')
    if st.get('armor'):
        out.append(f'{_fmt(st["armor"], lang)} {_num("armor", lang)}')
    for k in ('str', 'agi', 'int', 'spi', 'sta'):
        if st.get(k):
            out.append(f'+{_fmt(st[k], lang)} {_num(k, lang)}')
    if st.get('sp') and st.get('sp') == st.get('hp'):
        out.append(G_SPHP[lang].replace('{n}', _fmt(st['sp'], lang)))
    else:
        out += [f'+{_fmt(st[k], lang)} {_num(k, lang)}' for k in ('sp', 'hp') if st.get(k)]
    for k in ('mp5', 'hit', 'crit', 'def', 'ap'):
        if st.get(k):
            out.append(f'+{_fmt(st[k], lang)}{"%" if k in ("hit", "crit") else ""} {_num(k, lang)}')
    return ', '.join(out)


def gear_rows(key, data=None):
    """The items of a spec in table order: slot, then the higher required level first. [(entry, item)]"""
    data = data or GEAR30
    items = data.get('items', {})
    got = [(e, items[str(e['id'])]) for e in data.get('specs', {}).get(key, []) if str(e['id']) in items]
    return sorted(got, key=lambda x: (GSLOTS.index(x[1]['slot']), -(x[1].get('lvl') or 0), _name(x[1]['names'], 'en')))


def _src_html(src, lang, tr, fn):
    if src['kind'] == 'drop':
        boss, dg = (escape(_name(src[k], lang)) if src.get(k) else '' for k in ('boss', 'dungeon'))
        return ' · '.join(x for x in (boss, dg) if x) or (escape(G_WORLD[lang]) if src.get('world') else '')
    if src['kind'] == 'quest':
        q = escape(_name(src['quest'], lang)) if src.get('quest') else ''
        return f'{escape(G_QUEST[lang])}: {q}' + (f'<span class="alt">{escape(fn[src["faction"]])}</span>' if src.get('faction') else '')
    return escape(tr(G_PROF[src['prof']], lang)) if src.get('prof') in G_PROF else ''


def gear_beta(rows):
    """Beta data on the page: an item of the Wowhead import (not yet replaced by the client dump)."""
    return any(it.get('provenance') == 'wowhead-forever-guide' for _, it in rows)


def gear_partial(key, data=None):
    """A spec with fewer than GEAR_MIN_SLOTS slots, accepted as is and listed in "partial": the section says so."""
    return key in (data or GEAR30).get('partial', [])


def _mark(text):
    """«<b>Временно:</b> данные беты…»: the word before the first colon in bold."""
    head, tail = text.split(':', 1)
    return f'<b>{escape(head)}:</b>{escape(tail)}'


def gear_sprite_v():
    """?v=<hash> of the item icon sprite (tools/gear_api.py): one picture for the whole section, cached for days."""
    import hashlib
    f = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'gear', 'icons.webp')
    return '?v=' + hashlib.sha1(open(f, 'rb').read()).hexdigest()[:8] if os.path.isfile(f) else ''


def gear_html(key, lang, tr, fn, data=None):
    """The section: lead, filters (faction, my level, my professions; JS['cheat'] reads the hero of this browser), the table, the source."""
    data = data or GEAR30
    rows = gear_rows(key, data)
    if not rows:
        return ''
    head = [escape(h[lang]) for h in G_HEAD]
    body, last = '', ''
    for e, it in rows:
        srcs = e.get('src') or []
        quests = [s for s in srcs if s['kind'] == 'quest']
        f = (quests[0].get('faction') or '') if srcs and len(quests) == len(srcs) and len({s.get('faction') for s in quests}) == 1 else ''
        crafts = [s.get('prof') for s in srcs if s['kind'] == 'craft' and s.get('prof')]
        p = ' '.join(dict.fromkeys(crafts)) if srcs and len(crafts) == len(srcs) else ''
        name = _name(it['names'], lang)
        href = f'https://www.wowhead.com/forever/{WH_LANG.get(lang, "")}item={int(e["id"])}'
        stats = gear_stats(it.get('stats') or {}, lang)
        where = '<br>'.join(x for x in (_src_html(s, lang, tr, fn) for s in srcs) if x) or '—'
        lv = it.get('lvl') or 0
        lv = lv if lv > 1 else 0   # «1» from the API means no required level (quest rewards, goggles): «—», never a made-up level
        cont = ' class="cont"' if it['slot'] == last else ''
        last = it['slot']
        body += (f'<tr data-s="{it["slot"]}" data-lv="{lv}" data-f="{f}" data-p="{p}"{cont}>'
                 f'<td data-l="{head[0]}" class="k sl">{escape(GSLOT[it["slot"]][lang])}</td>'
                 f'<td data-l="{head[1]}" class="m">'
                 + (f'<i class="gic" style="--i:{int(it["ic"])}" aria-hidden="true"></i>' if it.get('ic') is not None else '<i class="gic no" aria-hidden="true"></i>')
                 + f'<a class="iq iq{int(it.get("q", 1))}" href="{href}" target="_blank" rel="noopener"'
                 + (f' title="{escape(it["names"]["en"])}"' if name != it['names'].get('en') else '') + f'>{escape(name)}</a>'
                 + (f'<span class="alt">{escape(stats)}</span>' if stats else '')
                 + (f'<span class="gpick">{escape(G_PICK[lang])}</span>' if e.get('pick') else '') + '</td>'
                 f'<td data-l="{head[2]}" class="s lv">{lv or "—"}</td>'
                 f'<td data-l="{head[3]}">{where}</td></tr>')
    prov = {it.get('provenance') for _, it in rows}
    slots = len({it['slot'] for _, it in rows})
    picks = sum(1 for e, _ in rows if e.get('pick'))
    marks = ([_mark(G_TEMP[lang])] if gear_beta(rows) else []) + ([_mark(G_PART[lang].replace('{n}', str(slots)))] if gear_partial(key, data) else [])
    marks += [_mark(G_PICK_NOTE[lang].replace('{n}', str(picks)).replace('{t}', str(len(rows))))] if picks else []
    day = '.'.join(reversed((data.get('date') or '').split('-')))
    src_line = ' '.join(G_SRC[p][lang].replace('{d}', day) for p in ('client-dump', 'wowhead-forever-guide') if p in prov)
    src_line += f' {G_SRC_PICK[lang]}' if picks else ''
    btns = (f'<button type="button" data-v="all" aria-pressed="true">{escape(G_ALL[lang])}</button>'
            + ''.join(f'<button type="button" data-v="{x}" aria-pressed="false">{escape(fn[x])}</button>' for x in ('alliance', 'horde')))
    ths = ''.join(f'<th scope="col">{h}</th>' for h in head)
    # the sprite waits for the section (JS['cheat'] sets --gsp near the viewport): fetched at once it took bandwidth from the first screen (LCP +0,3 s)
    sp = (f' style="--n:{max(int(data.get("sprite") or 0), 1)}" data-gsp="@@ROOT@@assets/gear/icons.webp{gear_sprite_v()}"'
          if data.get('sprite') else '')
    return (f'<div id="gearBox" data-shown="{escape(G_SHOWN[lang])}"{sp}>'
            + (f'<p class="gtest">{escape(G_TEST[lang])}</p>' if data.get('fixture') else '')
            + (f'<div class="gnote" role="note">' + ''.join(f'<p>{m}</p>' for m in marks) + '</div>' if marks else '')
            + f'<p>{escape(G_LEAD[lang])}</p>'
            f'<div class="filters" role="group" aria-label="{escape(G_ROW[lang])}">'
            f'<div class="seg" id="gearF" role="group" aria-label="{escape(G_FAC[lang])}">{btns}</div>'
            f'<div class="fgroup"><span class="flabel" id="lgearLvl">{escape(G_MYLVL[lang])}</span><div class="stepper" role="group" aria-labelledby="lgearLvl">'
            f'<button type="button" class="lvm" aria-label="{escape(G_LO[lang])}">−</button>'
            f'<input class="lvin" id="gearLvl" type="number" min="1" max="60" inputmode="numeric" aria-labelledby="lgearLvl" placeholder="—">'
            f'<button type="button" class="lvp" aria-label="{escape(G_HI[lang])}">+</button></div></div>'
            f'<button type="button" class="pill" id="gearProf" aria-pressed="false" hidden>{escape(G_MYPROF[lang])}</button>'
            f'<span class="small" id="gearCount" role="status"></span></div>'
            f'<table class="gtable geart"><thead><tr>{ths}</tr></thead><tbody>{body}'
            f'<tr id="gearNone" hidden><td colspan="4">{escape(G_NONE[lang])}</td></tr></tbody></table>'
            f'<p class="small">{escape(src_line)} {escape(G_L60[lang])}</p></div>')


def gear_answer(key, lang, data=None):
    """The «Gear» line of the answer in 5 seconds: how many items, their levels, a link to the table."""
    rows = gear_rows(key, data)
    lv = [it['lvl'] for _, it in rows if (it.get('lvl') or 0) > 1]   # level 1 = no requirement: not the low end of the span
    span = (f' · {G_LV[lang]} {min(lv)}–{max(lv)}' if min(lv) < max(lv) else f' · {G_LV[lang]} {lv[0]}') if lv else ''
    tags = ([G_TEMP_S[lang]] if gear_beta(rows) else []) + ([G_PART_S[lang]] if gear_partial(key, data) else [])
    tag = f' · {escape(", ".join(tags))}' if tags else ''
    return f'{escape(G_N[lang])}: {len(rows)}{span}{tag}. <a href="#gear">{escape(G_GO[lang])}</a>'


def _gear(key, i, lang):
    got = GEAR.get(key, {}).get(i)
    if not got:
        return escape((WAIT_UNREAD if i == 0 and key in ENCH_UNREAD else WAIT[i])[lang])
    items, src = got
    return '<br>'.join(f'{escape(_name(n, lang))} — {escape(e[lang])}' for n, e in items) + f'<br><span class="small">{escape(_name(src, lang))}</span>'


def _h(text):
    return {l: f'<h3>{escape(text[l])}</h3>' for l in text if l in LANGS9}


def _section(guide, sid):
    return next(s for s in guide['sections'] if s['id'] == sid)


def attach(guides, hubs, order):
    """The four pages with their texts; the titles come in finish() (they need the names of all languages)."""
    by = {g['slug']: g for g in guides}
    for (cid, spec), slug in zip(CHEATS, SLUGS):
        bg, lv = by[f'builds-{cid}'], by[f'leveling-{cid}']
        sec = next(s for s in bg['sections'] if s['id'] == spec)
        roles = next(d for k, d in next(s for s in bg['sections'] if s['id'] == 'roles')['blocks'] if k == 'table')   # finish() puts the chips above it
        rows = [r for r in roles['rows'] if sec['title']['ru'].startswith(r[0]['ru'].split(' (')[0])]   # Feral: cat and bear rows
        blocks = sec['blocks']
        texts = [d for k, d in blocks if k == 'text']
        tree = next(((k, d) for k, d in blocks if k == 'tree'), None)
        table = next((k, d) for k, d in blocks if k == 'table')
        steps = next((k, d) for k, d in blocks if k == 'steps')
        tip = next((k, d) for k, d in blocks if k == 'tip')
        lvl = lambda i: _section(lv, i)  # noqa: E731
        party = next(x for x in next(d for k, d in lvl('play')['blocks'] if k == 'tabs') if x['id'] == 'party')
        answer_table = (('table', {'head': roles['head'][1:4], 'rows': [rows[0][1:]]}) if len(rows) == 1 else
                        ('table', {'head': roles['head'], 'rows': rows}))
        roles_txt = [x for k, d in next(s for s in bg['sections'] if s['id'] == 'roles')['blocks'] if k == 'text' for x in d]
        star = [x for x in roles_txt if '*' in x['ru']] if any('*' in r[2] for r in rows) else []   # what A*/B* means, from builds-<class>
        answer = [('raw', {}), answer_table] + ([('text', star)] if star else [])
        tab_build = [('text', texts[0]), tip]
        tab_talents = ([tree] if tree else []) + [table] + [('text', x) for x in texts[1:]]
        tab_level = [('h3', lvl('spec')['title'])] + lvl('spec')['blocks'] + [('h3', lvl('talents')['title'])] + lvl('talents')['blocks']
        tab_group = party['blocks'] + [('text', [GROUP_NOTE])]
        guide = {
            'slug': slug, 'art': cid, 'hero': 'hero_leveling', 'hub': False, 'more': False, 'js': 'cheat', 'cheat': (cid, spec, rows, roles['head'][2], table[1]['rows']),
            'title': bg['title'], 'lead': bg['lead'], 'tile': sec['title'], 'pills': list(bg['pills'][:1]),
            'sources': [s for s in bg['sources'] if spec.split('-')[0].title() in s[0] or 'Calculator' in s[0]] or bg['sources'],
            'sections': [
                {'id': 'answer', 'title': ANSWER, 'blocks': answer},
                {'id': 'build', 'title': TAB['build'], 'blocks': tab_build},
                {'id': 'talents', 'title': TAB['talents'], 'blocks': tab_talents},
            ] + ([{'id': 'gear', 'title': G_TITLE, 'blocks': [('raw', {})]}] if gear_rows(f'{cid}-{spec}') else []) + [   # html in finish()
                {'id': 'leveling', 'title': TAB['leveling'], 'blocks': tab_level},
                {'id': 'group', 'title': TAB['group'], 'blocks': tab_group},
                {'id': 'rotation', 'title': TAB['rotation'], 'blocks': [('text', [ROT_NOTE]), steps]},
                {'id': 'faq', 'title': FAQ_T, 'blocks': [('faq', FAQ)]},
                {'id': 'related', 'title': SEE_ALSO, 'blocks': [('tiles', [
                    {'t': FULL_BUILDS, 'd': bg['tile'], 'href': f'guides/builds-{cid}/#{spec}', 'art': cid},
                    {'t': FULL_LEVELING, 'd': lv['tile'], 'href': f'guides/leveling-{cid}/', 'art': 'hero_dawn'},
                    {'t': GROUP_TILE, 'd': GROUP_NOTE, 'href': 'tools/#raid', 'art': 'hero_tierlist'}])]},
            ],
        }
        guides.append(guide)
    for slug in SLUGS:
        if slug not in order:
            order.append(slug)
    guides.sort(key=lambda g: order.index(g['slug']))


def finish(guides, hero_core, langs_mod):
    """Titles, leads and the bar with the buttons in every language, then langs.fill for what is still short."""
    got = {}
    for g in guides:
        if g['slug'] not in SLUGS:
            continue
        cid, spec, rows, tierh, trows = g.pop('cheat')
        got[(cid, spec)] = rows
        title, lead, bar = {}, {}, {}
        key = f'{cid}-{spec}'
        gear = next((s for s in g['sections'] if s['id'] == 'gear'), None)
        for lang in LANGS9:
            if lang not in langs_mod.LANGS:
                continue
            n = hero_core(lang)
            if gear:
                import build   # noqa: E402  the profession names of the site in every language (build.tr)
                gear['blocks'][0][1][lang] = gear_html(key, lang, build.tr, n['fn'])
            sn = n['sn'][cid][n['sid'][cid].index(spec)]
            title[lang] = f'{n["cn"][cid]} · {sn}'   # the dot stays with the class on a wrapped heading
            role = ' / '.join(r[1][lang] for r in rows)
            lead[lang] = f'{role} · {tierh[lang]}: {" / ".join(dict.fromkeys(r[2] for r in rows))}. {rows[0][3][lang]}. {LEAD_TAIL[lang]}'
            top = [trows[-1]] + sorted(trows[:-1], key=lambda r: -int(r[1]))[:4]   # the last row is the spec's main talent, then the most points
            keys = ' · '.join(f'{escape(_name(r[0], lang))} ×{r[1]}' for r in top)
            leveling_href = f'../leveling-{cid}/'
            st = STATS.get(f'{cid}-{spec}')
            stats = (escape(STATS_SPLIT[lang]) if st == 'split' else escape(STATS_NONE[lang]) if st is None else
                     ' › '.join(escape((STAT.get(k) or EXTRA[k])[lang]) for k in st[0].split()) + f'<br><span class="small">{escape(st[1])}</span>')
            bar[lang] = (f'<div id="cheat" data-cls="{cid}" data-spec="{spec}" data-from="{escape(FROM_LINK[lang])}">'
                         f'<p class="small" id="cheatRace" hidden></p>'
                         f'<p id="cheatBest" data-l="{escape(BEST[lang])}"></p>'
                         f'<dl class="cxrows">'
                         f'<div><dt>{escape(GOAL[lang])}</dt><dd><a href="#leveling">{escape(GOAL_LV[lang])}</a> · '
                         f'<a href="#group">{escape(GOAL_DG[lang])}: {escape(role)}</a></dd></div>'
                         f'<div><dt>{escape(KEYT[lang])}</dt><dd>{keys}. <a href="#talents">{escape(ORDER_L[lang])}</a></dd></div>'
                         f'<div><dt>{escape(STATS_T[lang])}</dt><dd>{stats}</dd></div>'
                         + (f'<div><dt>{escape(G_ROW[lang])}</dt><dd>{gear_answer(key, lang)}</dd></div>' if gear else '')
                         + ''.join(f'<div><dt>{escape(GEAR_ROWS[i][lang])}</dt><dd>{_gear(f"{cid}-{spec}", i, lang)}</dd></div>' for i in ROWS_ON) +
                         f'</dl>'
                         f'<p class="gbtns"><a class="btn cxnext" href="{leveling_href}">{escape(NEXT_PFX[lang])}: {escape(TAB["leveling"][lang])} →</a> '
                         f'<a class="btn ghost" id="cheatPick" href="../../tools/#pick={cid}">{escape(PICK[lang])}</a> '
                         f'<button type="button" class="btn ghost" id="cheatShare">{escape(n["tx"]["share"])}</button> '
                         f'<span class="small" role="status" id="cheatMsg"></span></p></div>')
        g['title'], g['lead'], g['crumb'] = title, lead, title
        SEO[f'guides/{g["slug"]}/'] = ({l: f'{title[l]}: {SEO_TAIL[l]}' for l in title}, dict(lead))
        g['sections'][0]['blocks'][0] = ('raw', bar)
        for sec in g['sections']:                                  # the headings of the borrowed sections: raw html, built after fill
            sec['blocks'] = [('raw', _h(d)) if k == 'h3' else (k, d) for k, d in sec['blocks']]
        g['tile'] = title
    by = {g['slug']: g for g in guides}
    chips = {}                                                     # (class, lang) -> the <li> of its three sheets
    for cid in dict.fromkeys(c for c, _ in CHEATS):                # builds-<class>: the chips of the class' sheets open the roles section
        html = {}
        for lang in LANGS9:
            if lang not in langs_mod.LANGS:
                continue
            n = hero_core(lang)
            chips[cid, lang] = ''.join(
                f'<li><a href="../spec-{cid}-{sp}/"><b>{escape(sn)}</b><span>{escape(" / ".join(r[1][lang] for r in got[(cid, sp)]))}</span></a></li>'
                for sp, sn in zip(n['sid'][cid], n['sn'][cid]))
            html[lang] = f'<p class="small">{escape(CHIPS_LEAD[lang])}</p><ul class="spchips">{chips[cid, lang]}</ul>'
        roles = next(sec for sec in by[f'builds-{cid}']['sections'] if sec['id'] == 'roles')
        roles['blocks'].insert(0, ('raw', html))                   # above the table: the next step is in the first screen of a phone
    hub = by.get('builds')                                         # /guides/builds/: the 27 sheets by class first, the calculator under them
    if hub:
        import build   # noqa: E402  the class order of the site
        html = {}
        for lang in LANGS9:
            if lang not in langs_mod.LANGS:
                continue
            n = hero_core(lang)
            html[lang] = (f'<p class="small">{escape(CHIPS_LEAD[lang])}</p><div class="spmx">' + ''.join(
                f'<div class="spcls"><a class="spn" href="../builds-{c["id"]}/">{escape(n["cn"][c["id"]])}</a><ul class="spchips">{chips[c["id"], lang]}</ul></div>'
                for c in build.CLASSES if (c['id'], lang) in chips) + '</div>')
        sec = hub['sections'][0]
        sec['blocks'] = [('raw', html)] + [(k, d) for k, d in sec['blocks'] if k == 'calc']
    langs_mod.fill([g for g in guides if g['slug'] in SLUGS])
