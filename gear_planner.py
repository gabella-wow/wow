"""Gear planner (character/gear/): a paper doll with 17 slots, an item picker that opens on the reader's level, armor and spec,
the sum of the item stats, «Fill with our build» from data/gear30.json and the build in the address (#c=&s=&r=&l=&g=slot:id,…&t=).

Data: data/items_catalog.json (tools/item_catalog.py, Blizzard Game Data API static-classic1x-eu) -> assets/gear/planner-<lang>.json,
one file per language (item names of the page language; uk and pl have none in the catalog: English). Sources of an item and the
recommended lists come from data/gear30.json; nothing from Wowhead. Icons: the catalog sprite assets/gear/catalog.webp (36 px cells,
64 columns), set as a CSS variable only when an icon is drawn. The script is assets/gear/planner.js (its pure core is tested by
tests/test_gear_planner.py in node). The page shell is build_guides.build_page ('compact': 'gear').
Texts: n9() in every language, like content/spec_cheats.py and talents.py; item stat names come from spec_cheats."""
import hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import langs  # noqa: E402

LANGS9 = langs.ALL
CATALOG = os.path.join(HERE, 'data', 'items_catalog.json')
OUT = os.path.join(HERE, 'assets', 'gear')
SCRIPT = os.path.join(OUT, 'planner.js')
SPRITE = os.path.join(OUT, 'catalog.webp')
PATH = 'character/gear/'


def n9(ru, en, uk, de, fr, es, pt, it, pl):
    return dict(zip(LANGS9, (ru, en, uk, de, fr, es, pt, it, pl)))


# the slot codes of the data file (the catalog's slots, «two» = two-hand, «relic» = libram, idol, totem)
SL = ['head', 'neck', 'shoulder', 'back', 'chest', 'wrist', 'hands', 'waist', 'legs', 'feet', 'finger', 'trinket',
      'main', 'two', 'off', 'ranged', 'relic']
# the item stats the planner sums, in the order of the stats block
K = ['str', 'agi', 'sta', 'int', 'spi', 'armor', 'sp', 'hp', 'ap', 'crit', 'hit', 'mp5', 'def', 'dps']
# the doll: left column, right column, weapons (the in-game character window)
LEFT = ['head', 'neck', 'shoulder', 'back', 'chest', 'wrist']
RIGHT = ['hands', 'waist', 'legs', 'feet', 'finger1', 'finger2', 'trinket1', 'trinket2']
WEAP = ['main', 'off', 'ranged']
CELLS = LEFT + RIGHT + WEAP

TX = {
    'name': n9('Примерка экипировки', 'Gear planner', 'Приміряння екіпірування', 'Ausrüstungsplaner', 'Planificateur d’équipement',
               'Planificador de equipo', 'Planejador de equipamento', 'Pianificatore di equipaggiamento', 'Planer ekwipunku'),
    'lead': n9('Наденьте предметы по ячейкам: список сразу под ваш уровень, броню и спек. Сборка живёт в ссылке, без входа.',
               'Fill the slots item by item: the list opens on your level, armor and spec. The build lives in a link, no login.',
               'Вдягніть предмети за комірками: список одразу під ваш рівень, броню і спек. Збірка живе в посиланні, без входу.',
               'Belege die Plätze Stück für Stück: Die Liste öffnet sich passend zu Stufe, Rüstung und Skillung. Der Build steckt im Link, ohne Anmeldung.',
               'Remplissez les emplacements un à un : la liste s’ouvre sur votre niveau, votre armure et votre spé. Le build tient dans un lien, sans connexion.',
               'Llena las ranuras pieza a pieza: la lista se abre con tu nivel, armadura y especialización. El build vive en un enlace, sin iniciar sesión.',
               'Preencha os espaços item a item: a lista abre no seu nível, armadura e especialização. A build fica num link, sem login.',
               'Riempi gli slot pezzo per pezzo: l’elenco si apre sul tuo livello, armatura e specializzazione. La build sta in un link, senza accesso.',
               'Wypełniaj miejsca przedmiot po przedmiocie: lista otwiera się pod twój poziom, pancerz i specjalizację. Build żyje w linku, bez logowania.'),
    'go': n9('Примерить экипировку', 'Try on gear', 'Приміряти екіпірування', 'Ausrüstung anprobieren', 'Essayer l’équipement',
             'Probar equipo', 'Experimentar equipamento', 'Provare l’equipaggiamento', 'Przymierz ekwipunek'),
    'cls': n9('Класс', 'Class', 'Клас', 'Klasse', 'Classe', 'Clase', 'Classe', 'Classe', 'Klasa'),
    'spec': n9('Спек', 'Spec', 'Спек', 'Skillung', 'Spé', 'Especialización', 'Especialização', 'Specializzazione', 'Specjalizacja'),
    'nospec': n9('Без спека', 'No spec', 'Без спеку', 'Keine Skillung', 'Sans spé', 'Sin especialización', 'Sem especialização',
                 'Nessuna specializzazione', 'Bez specjalizacji'),
    'race': n9('Раса', 'Race', 'Раса', 'Volk', 'Race', 'Raza', 'Raça', 'Razza', 'Rasa'),
    'lvl': n9('Уровень', 'Level', 'Рівень', 'Stufe', 'Niveau', 'Nivel', 'Nível', 'Livello', 'Poziom'),
    'lvlDown': n9('Уровень ниже', 'Lower level', 'Нижчий рівень', 'Niedrigere Stufe', 'Niveau inférieur', 'Nivel menor', 'Nível menor',
                  'Livello inferiore', 'Niższy poziom'),
    'lvlUp': n9('Уровень выше', 'Higher level', 'Вищий рівень', 'Höhere Stufe', 'Niveau supérieur', 'Nivel mayor', 'Nível maior',
                'Livello superiore', 'Wyższy poziom'),
    'fill': n9('Заполнить нашей сборкой', 'Fill with our build', 'Заповнити нашою збіркою', 'Mit unserem Build füllen', 'Remplir avec notre build',
               'Llenar con nuestro build', 'Preencher com a nossa build', 'Riempi con la nostra build', 'Wypełnij naszym buildem'),
    'copy': n9('Скопировать ссылку', 'Copy link', 'Скопіювати посилання', 'Link kopieren', 'Copier le lien', 'Copiar enlace', 'Copiar link',
               'Copia link', 'Kopiuj link'),
    'copied': n9('Ссылка скопирована', 'Link copied', 'Посилання скопійовано', 'Link kopiert', 'Lien copié', 'Enlace copiado', 'Link copiado',
                 'Link copiato', 'Link skopiowany'),
    'nocopy': n9('Скопируйте адрес из строки браузера', 'Copy the address from the browser bar', 'Скопіюйте адресу з рядка браузера',
                 'Kopiere die Adresse aus der Browserleiste', 'Copiez l’adresse depuis la barre du navigateur', 'Copia la dirección de la barra del navegador',
                 'Copie o endereço da barra do navegador', 'Copia l’indirizzo dalla barra del browser', 'Skopiuj adres z paska przeglądarki'),
    'clear': n9('Снять всё', 'Unequip all', 'Зняти все', 'Alles ablegen', 'Tout retirer', 'Quitar todo', 'Remover tudo', 'Togli tutto', 'Zdejmij wszystko'),
    'cleared': n9('Всё снято', 'All unequipped', 'Усе знято', 'Alles abgelegt', 'Tout est retiré', 'Todo quitado', 'Tudo removido', 'Tutto tolto',
                  'Wszystko zdjęte'),
    'pick': n9('выбрать', 'choose', 'обрати', 'wählen', 'choisir', 'elegir', 'escolher', 'scegli', 'wybierz'),
    'change': n9('Сменить', 'Change', 'Змінити', 'Wechseln', 'Changer', 'Cambiar', 'Trocar', 'Cambia', 'Zmień'),
    'remove': n9('Снять', 'Unequip', 'Зняти', 'Ablegen', 'Retirer', 'Quitar', 'Remover', 'Togli', 'Zdejmij'),
    'locked': n9('Занято двуручным оружием', 'Taken by the two-hander', 'Зайнято дворучною зброєю', 'Belegt durch Zweihandwaffe',
                 'Prise par l’arme à deux mains', 'Ocupada por el arma a dos manos', 'Ocupada pela arma de duas mãos',
                 'Occupata dall’arma a due mani', 'Zajęte przez broń dwuręczną'),
    'doll': n9('Экипировка', 'Equipment', 'Екіпірування', 'Ausrüstung', 'Équipement', 'Equipo', 'Equipamento', 'Equipaggiamento', 'Ekwipunek'),
    'search': n9('Название предмета', 'Item name', 'Назва предмета', 'Name des Gegenstands', 'Nom de l’objet', 'Nombre del objeto', 'Nome do item',
                 'Nome dell’oggetto', 'Nazwa przedmiotu'),
    'filters': n9('Фильтры', 'Filters', 'Фільтри', 'Filter', 'Filtres', 'Filtros', 'Filtros', 'Filtri', 'Filtry'),
    'fLvl': n9('Мой уровень', 'My level', 'Мій рівень', 'Meine Stufe', 'Mon niveau', 'Mi nivel', 'Meu nível', 'Il mio livello', 'Mój poziom'),
    'fArm': n9('Моя броня', 'My armor', 'Моя броня', 'Meine Rüstung', 'Mon armure', 'Mi armadura', 'Minha armadura', 'La mia armatura', 'Mój pancerz'),
    'fRare': n9('Редкие+', 'Rare+', 'Рідкісні+', 'Selten+', 'Rares+', 'Raros+', 'Raros+', 'Rari+', 'Rzadkie+'),
    'fDrop': n9('Подземелья', 'Dungeons', 'Підземелля', 'Dungeons', 'Donjons', 'Mazmorras', 'Masmorras', 'Spedizioni', 'Lochy'),
    'fQuest': n9('Квесты', 'Quests', 'Квести', 'Quests', 'Quêtes', 'Misiones', 'Missões', 'Missioni', 'Zadania'),
    'fCraft': n9('Профессии', 'Professions', 'Професії', 'Berufe', 'Métiers', 'Profesiones', 'Profissões', 'Professioni', 'Profesje'),
    'count': n9('Предметов: {n}', 'Items: {n}', 'Предметів: {n}', 'Gegenstände: {n}', 'Objets : {n}', 'Objetos: {n}', 'Itens: {n}',
                'Oggetti: {n}', 'Przedmiotów: {n}'),
    'none': n9('Под этот фильтр предметов нет.', 'No items for this filter.', 'Під цей фільтр предметів немає.', 'Keine Gegenstände für diesen Filter.',
               'Aucun objet pour ce filtre.', 'No hay objetos para este filtro.', 'Nenhum item para este filtro.', 'Nessun oggetto per questo filtro.',
               'Brak przedmiotów dla tego filtra.'),
    'lv': n9('ур. {n}', 'lvl {n}', 'рів. {n}', 'St. {n}', 'niv. {n}', 'nv. {n}', 'nv. {n}', 'liv. {n}', 'poz. {n}'),
    'il': n9('Уровень предмета {n}', 'Item level {n}', 'Рівень предмета {n}', 'Gegenstandsstufe {n}', 'Niveau d’objet {n}', 'Nivel de objeto {n}',
             'Nível do item {n}', 'Livello oggetto {n}', 'Poziom przedmiotu {n}'),
    'better': n9('лучше', 'better', 'краще', 'besser', 'mieux', 'mejor', 'melhor', 'meglio', 'lepiej'),
    'worse': n9('хуже', 'worse', 'гірше', 'schlechter', 'moins bien', 'peor', 'pior', 'peggio', 'gorzej'),
    'worn': n9('надето', 'equipped', 'вдягнено', 'angelegt', 'équipé', 'equipado', 'equipado', 'indossato', 'założone'),
    'ours': n9('наша сборка', 'our build', 'наша збірка', 'unser Build', 'notre build', 'nuestro build', 'nossa build', 'nostra build', 'nasz build'),
    'sortSpec': n9('Сверху лучшее для спека «{s}» по приоритету статов.', 'Best for {s} on top, by its stat priority.',
                   'Згори найкраще для спеку «{s}» за пріоритетом характеристик.', 'Oben das Beste für {s}, nach Werte-Priorität.',
                   'En haut, le meilleur pour {s}, selon sa priorité de caractéristiques.', 'Arriba lo mejor para {s}, según su prioridad de estadísticas.',
                   'No topo, o melhor para {s}, pela prioridade de atributos.', 'In alto il meglio per {s}, secondo la priorità delle statistiche.',
                   'Na górze najlepsze dla {s}, według priorytetu statystyk.'),
    'sortIl': n9('Сверху предметы выше уровнем: у спека нет порядка статов в источниках.',
                 'Higher item levels on top: the sources give this spec no stat order.',
                 'Згори предмети вищого рівня: у джерелах для спеку немає порядку характеристик.',
                 'Oben höhere Gegenstandsstufen: Die Quellen nennen für diese Skillung keine Reihenfolge.',
                 'En haut les niveaux d’objet élevés : les sources ne donnent pas d’ordre pour cette spé.',
                 'Arriba los niveles de objeto más altos: las fuentes no dan un orden para esta especialización.',
                 'No topo os níveis de item mais altos: as fontes não dão uma ordem para esta especialização.',
                 'In alto i livelli oggetto più alti: le fonti non danno un ordine per questa specializzazione.',
                 'Na górze wyższe poziomy przedmiotów: źródła nie podają kolejności dla tej specjalizacji.'),
    'sortNone': n9('Сверху предметы выше уровнем. Выберите спек, чтобы сортировать по его статам.',
                   'Higher item levels on top. Pick a spec to sort by its stats.',
                   'Згори предмети вищого рівня. Оберіть спек, щоб сортувати за його характеристиками.',
                   'Oben höhere Gegenstandsstufen. Wähle eine Skillung, um nach ihren Werten zu sortieren.',
                   'En haut les niveaux d’objet élevés. Choisissez une spé pour trier selon ses caractéristiques.',
                   'Arriba los niveles de objeto más altos. Elige una especialización para ordenar por sus estadísticas.',
                   'No topo os níveis de item mais altos. Escolha uma especialização para ordenar pelos atributos dela.',
                   'In alto i livelli oggetto più alti. Scegli una specializzazione per ordinare secondo le sue statistiche.',
                   'Na górze wyższe poziomy przedmiotów. Wybierz specjalizację, aby sortować według jej statystyk.'),
    'stats': n9('Статы предметов', 'Item stats', 'Характеристики предметів', 'Gegenstandswerte', 'Caractéristiques des objets',
                'Estadísticas de objetos', 'Atributos dos itens', 'Statistiche degli oggetti', 'Statystyki przedmiotów'),
    'statsNote': n9('Сумма статов надетых предметов. Базовых статов класса и расы здесь нет: на сайте их данных пока нет.',
                    'The sum of the equipped items. No base stats of class and race: the site has no data for them yet.',
                    'Сума характеристик вдягнених предметів. Базових характеристик класу й раси тут немає: на сайті їхніх даних поки немає.',
                    'Summe der angelegten Gegenstände. Ohne Grundwerte von Klasse und Volk: Dafür hat die Seite noch keine Daten.',
                    'La somme des objets équipés. Sans les caractéristiques de base de la classe et de la race : le site n’a pas encore ces données.',
                    'La suma de los objetos equipados. Sin las estadísticas base de clase y raza: el sitio aún no tiene esos datos.',
                    'A soma dos itens equipados. Sem os atributos base de classe e raça: o site ainda não tem esses dados.',
                    'La somma degli oggetti indossati. Senza le statistiche base di classe e razza: il sito non ha ancora questi dati.',
                    'Suma założonych przedmiotów. Bez bazowych statystyk klasy i rasy: serwis nie ma jeszcze tych danych.'),
    'empty': n9('Пока ничего не надето.', 'Nothing equipped yet.', 'Поки нічого не вдягнено.', 'Noch nichts angelegt.', 'Rien d’équipé pour l’instant.',
                'Aún no hay nada equipado.', 'Nada equipado ainda.', 'Ancora nulla indossato.', 'Nic jeszcze nie założono.'),
    'filled': n9('Заполнено ячеек: {n}', 'Slots filled: {n}', 'Заповнено комірок: {n}', 'Plätze belegt: {n}', 'Emplacements remplis : {n}',
                 'Ranuras llenas: {n}', 'Espaços preenchidos: {n}', 'Slot riempiti: {n}', 'Wypełniono miejsc: {n}'),
    'fillNone': n9('В нашей сборке нет предметов под этот спек и уровень.', 'Our build has no items for this spec and level.',
                   'У нашій збірці немає предметів під цей спек і рівень.', 'Unser Build hat keine Gegenstände für diese Skillung und Stufe.',
                   'Notre build n’a pas d’objets pour cette spé et ce niveau.', 'Nuestro build no tiene objetos para esta especialización y nivel.',
                   'Nossa build não tem itens para esta especialização e nível.', 'La nostra build non ha oggetti per questa specializzazione e livello.',
                   'Nasz build nie ma przedmiotów dla tej specjalizacji i poziomu.'),
    'auto': n9('подбор по статам', 'stat pick', 'підбір за характеристиками', 'nach Werten gewählt', 'choisi selon les stats',
               'elegido por estadísticas', 'escolhido por atributos', 'scelto per statistiche', 'dobrane wg statystyk'),
    'fillMix': n9('Заполнено ячеек: {n}. Из нашей сборки: {a}, подбор по статам: {b}.', 'Slots filled: {n}. From our build: {a}, stat pick: {b}.',
                  'Заповнено комірок: {n}. З нашої збірки: {a}, підбір за характеристиками: {b}.',
                  'Plätze belegt: {n}. Aus unserem Build: {a}, nach Werten gewählt: {b}.',
                  'Emplacements remplis : {n}. De notre build : {a}, choisis selon les stats : {b}.',
                  'Ranuras llenas: {n}. De nuestro build: {a}, elegidas por estadísticas: {b}.',
                  'Espaços preenchidos: {n}. Da nossa build: {a}, escolhidos por atributos: {b}.',
                  'Slot riempiti: {n}. Dalla nostra build: {a}, scelti per statistiche: {b}.',
                  'Wypełniono miejsc: {n}. Z naszego buildu: {a}, dobrane wg statystyk: {b}.'),
    'fillOut': n9('Наша сборка — на {a}–{b} ур. Здесь всё подобрано по статам спека: ячеек {n}.',
                  'Our build covers levels {a}–{b}. Here every slot is a pick by the spec’s stats: {n} slots.',
                  'Наша збірка — на {a}–{b} рів. Тут усе підібрано за характеристиками спеку: комірок {n}.',
                  'Unser Build deckt Stufe {a}–{b} ab. Hier ist alles nach den Werten der Skillung gewählt: {n} Plätze.',
                  'Notre build couvre les niveaux {a} à {b}. Ici, tout est choisi selon les stats de la spé : {n} emplacements.',
                  'Nuestro build cubre los niveles {a}–{b}. Aquí todo se elige por las estadísticas de la especialización: {n} ranuras.',
                  'Nossa build cobre os níveis {a}–{b}. Aqui tudo é escolhido pelos atributos da especialização: {n} espaços.',
                  'La nostra build copre i livelli {a}–{b}. Qui tutto è scelto secondo le statistiche della specializzazione: {n} slot.',
                  'Nasz build obejmuje poziomy {a}–{b}. Tu wszystko dobrano wg statystyk specjalizacji: {n} miejsc.'),
    'needSpec': n9('Сначала выберите спек.', 'Pick a spec first.', 'Спершу оберіть спек.', 'Wähle zuerst eine Skillung.', 'Choisissez d’abord une spé.',
                   'Elige primero una especialización.', 'Escolha primeiro uma especialização.', 'Scegli prima una specializzazione.',
                   'Najpierw wybierz specjalizację.'),
    'loading': n9('Загружаем предметы…', 'Loading items…', 'Завантажуємо предмети…', 'Gegenstände werden geladen…', 'Chargement des objets…',
                  'Cargando objetos…', 'Carregando itens…', 'Caricamento oggetti…', 'Ładowanie przedmiotów…'),
    'loadErr': n9('Не получилось загрузить предметы. Обновите страницу.', 'Could not load the items. Reload the page.',
                  'Не вдалося завантажити предмети. Оновіть сторінку.', 'Gegenstände konnten nicht geladen werden. Lade die Seite neu.',
                  'Impossible de charger les objets. Rechargez la page.', 'No se pudieron cargar los objetos. Recarga la página.',
                  'Não foi possível carregar os itens. Recarregue a página.', 'Impossibile caricare gli oggetti. Ricarica la pagina.',
                  'Nie udało się wczytać przedmiotów. Odśwież stronę.'),
    'close': n9('Закрыть', 'Close', 'Закрити', 'Schließen', 'Fermer', 'Cerrar', 'Fechar', 'Chiudi', 'Zamknij'),
    'quest': n9('Квест', 'Quest', 'Квест', 'Quest', 'Quête', 'Misión', 'Missão', 'Missione', 'Zadanie'),
    'world': n9('Добыча в мире', 'World drop', 'Здобич у світі', 'Weltdrop', 'Butin du monde', 'Botín del mundo', 'Saque do mundo',
                'Bottino del mondo', 'Łup ze świata'),
    'rules': n9('Броня и оружие по правилам Classic: кольчуга у охотника и шамана и латы у воина и паладина с 40 уровня. '
                'Предметы и иконки из каталога Blizzard для Classic Era; правки Forever появятся после старта игры.',
                'Armor and weapons follow the Classic rules: mail for Hunters and Shamans and plate for Warriors and Paladins from level 40. '
                'Items and icons come from Blizzard’s Classic Era catalog; Forever changes will follow after launch.',
                'Броня і зброя за правилами Classic: кольчуга в мисливця й шамана та лати у воїна й паладина з 40 рівня. '
                'Предмети та іконки з каталогу Blizzard для Classic Era; зміни Forever з’являться після старту гри.',
                'Rüstung und Waffen nach Classic-Regeln: Kette für Jäger und Schamanen, Platte für Krieger und Paladine ab Stufe 40. '
                'Gegenstände und Symbole aus Blizzards Classic-Era-Katalog; Forever-Änderungen folgen nach dem Start.',
                'Armures et armes selon les règles Classic : mailles pour chasseurs et chamans, plaques pour guerriers et paladins dès le niveau 40. '
                'Objets et icônes du catalogue Classic Era de Blizzard ; les changements de Forever suivront après le lancement.',
                'Armadura y armas según las reglas de Classic: malla para cazadores y chamanes y placas para guerreros y paladines desde el nivel 40. '
                'Objetos e iconos del catálogo Classic Era de Blizzard; los cambios de Forever llegarán tras el lanzamiento.',
                'Armadura e armas pelas regras do Classic: malha para caçadores e xamãs e placa para guerreiros e paladinos a partir do nível 40. '
                'Itens e ícones do catálogo Classic Era da Blizzard; as mudanças do Forever virão após o lançamento.',
                'Armature e armi secondo le regole Classic: maglia per cacciatori e sciamani e piastre per guerrieri e paladini dal livello 40. '
                'Oggetti e icone dal catalogo Classic Era di Blizzard; le modifiche di Forever arriveranno dopo il lancio.',
                'Pancerz i broń według zasad Classic: kolczuga dla Huntera i Shamana, płyty dla Warriora i Paladina od 40 poziomu. '
                'Przedmioty i ikony z katalogu Blizzard dla Classic Era; zmiany Forever pojawią się po starcie gry.'),
    'right': n9('Правая рука', 'Main hand', 'Права рука', 'Waffenhand', 'Main droite', 'Mano derecha', 'Mão principal', 'Mano primaria',
                'Główna ręka'),
    'ring': n9('Кольцо', 'Ring', 'Каблучка', 'Ring', 'Anneau', 'Anillo', 'Anel', 'Anello', 'Pierścień'),
    'dps': n9('Урон оружия в секунду', 'Weapon damage per second', 'Шкода зброї за секунду', 'Waffenschaden pro Sekunde', 'Dégâts de l’arme par seconde',
              'Daño de arma por segundo', 'Dano da arma por segundo', 'Danni dell’arma al secondo', 'Obrażenia broni na sekundę'),
}
# short stat names of the item lines and the delta («+6 инт»)
SHORT = {
    'ru': {'str': 'сил', 'agi': 'лов', 'sta': 'вын', 'int': 'инт', 'spi': 'дух', 'armor': 'брони', 'sp': 'СЗ', 'hp': 'исц', 'ap': 'СА',
           'crit': 'крит', 'hit': 'метк', 'mp5': 'маны/5с', 'def': 'защ', 'dps': 'УВС'},
    'en': {'str': 'Str', 'agi': 'Agi', 'sta': 'Sta', 'int': 'Int', 'spi': 'Spi', 'armor': 'Armor', 'sp': 'SP', 'hp': 'Heal', 'ap': 'AP',
           'crit': 'Crit', 'hit': 'Hit', 'mp5': 'MP5', 'def': 'Def', 'dps': 'DPS'},
    'uk': {'str': 'сил', 'agi': 'спр', 'sta': 'вит', 'int': 'інт', 'spi': 'дух', 'armor': 'броні', 'sp': 'СЗ', 'hp': 'зціл', 'ap': 'СА',
           'crit': 'крит', 'hit': 'влуч', 'mp5': 'мани/5с', 'def': 'зах', 'dps': 'ШВС'},
    'de': {'str': 'Stä', 'agi': 'Bew', 'sta': 'Ausd', 'int': 'Int', 'spi': 'Wil', 'armor': 'Rüstung', 'sp': 'ZM', 'hp': 'Heil', 'ap': 'AK',
           'crit': 'Krit', 'hit': 'Treff', 'mp5': 'MP5', 'def': 'Vert', 'dps': 'DPS'},
    'fr': {'str': 'For', 'agi': 'Agi', 'sta': 'End', 'int': 'Int', 'spi': 'Esp', 'armor': 'Armure', 'sp': 'PS', 'hp': 'Soins', 'ap': 'PA',
           'crit': 'Crit', 'hit': 'Tou', 'mp5': 'PM5', 'def': 'Déf', 'dps': 'DPS'},
    'es': {'str': 'Fue', 'agi': 'Agi', 'sta': 'Agu', 'int': 'Int', 'spi': 'Esp', 'armor': 'Armadura', 'sp': 'PH', 'hp': 'Sana', 'ap': 'PA',
           'crit': 'Crít', 'hit': 'Golpe', 'mp5': 'MP5', 'def': 'Def', 'dps': 'DPS'},
    'pt': {'str': 'For', 'agi': 'Agi', 'sta': 'Vig', 'int': 'Int', 'spi': 'Esp', 'armor': 'Armadura', 'sp': 'PM', 'hp': 'Cura', 'ap': 'PA',
           'crit': 'Crít', 'hit': 'Acerto', 'mp5': 'MP5', 'def': 'Def', 'dps': 'DPS'},
    'it': {'str': 'For', 'agi': 'Agi', 'sta': 'Res', 'int': 'Int', 'spi': 'Spi', 'armor': 'Armatura', 'sp': 'PM', 'hp': 'Cura', 'ap': 'PA',
           'crit': 'Crit', 'hit': 'Imp', 'mp5': 'MP5', 'def': 'Dif', 'dps': 'DPS'},
    'pl': {'str': 'Sił', 'agi': 'Zr', 'sta': 'Wyt', 'int': 'Int', 'spi': 'Duch', 'armor': 'Panc', 'sp': 'MZ', 'hp': 'Lecz', 'ap': 'MA',
           'crit': 'Kryt', 'hit': 'Traf', 'mp5': 'MP5', 'def': 'Obr', 'dps': 'DPS'},
}
# the page heading, the search title and description (seo.py)
SEO = {
    'ru': ('Примерка экипировки WoW Forever: сборщик под уровень и спек', 'Сборщик экипировки WoW Forever под уровень, броню и спек: кукла из 17 ячеек, поиск предметов, сумма статов, наша сборка в один тап и ссылка на билд без входа.'),
    'en': ('WoW Forever Gear Planner: Items for Your Level and Spec', 'WoW Forever gear planner for your level, armor and spec: a 17-slot paper doll, item search, stat totals, our build in one tap and a build link with no login.'),
    'uk': ('Приміряння екіпірування WoW Forever: під рівень і спек', 'Збирач екіпірування WoW Forever під рівень, броню і спек: лялька з 17 комірок, пошук предметів, сума характеристик, наша збірка й посилання без входу.'),
    'de': ('WoW Forever Ausrüstungsplaner: für Stufe und Skillung', 'Ausrüstungsplaner für WoW Forever nach Stufe, Rüstung und Skillung: 17 Plätze, Suche, Wertesumme, unser Build mit einem Tipp und Build-Link ohne Anmeldung.'),
    'fr': ('Planificateur d’équipement WoW Forever : niveau et spé', 'Planificateur d’équipement WoW Forever selon niveau, armure et spé : 17 emplacements, recherche, total des stats, notre build en un clic et lien sans connexion.'),
    'es': ('Planificador de equipo WoW Forever: por nivel y spec', 'Planificador de equipo de WoW Forever por nivel, armadura y especialización: 17 ranuras, búsqueda, suma de estadísticas, nuestro build y enlace sin registro.'),
    'pt': ('Planejador de equipamento WoW Forever: nível e spec', 'Planejador de equipamento do WoW Forever por nível, armadura e especialização: 17 espaços, busca, soma de atributos, nossa build e link sem login.'),
    'it': ('Pianificatore equipaggiamento WoW Forever: livello e spec', 'Pianificatore di equipaggiamento di WoW Forever per livello, armatura e spec: 17 slot, ricerca, somma delle statistiche, nostra build e link senza accesso.'),
    'pl': ('Planer ekwipunku WoW Forever: pod poziom i specjalizację', 'Planer ekwipunku WoW Forever pod poziom, pancerz i specjalizację: 17 miejsc, wyszukiwarka, suma statystyk, nasz build jednym dotknięciem i link bez logowania.'),
}
# build_guides record: the page in the guide shell (build_page, 'compact': 'gear')
PAGE = {'slug': 'gear-planner', 'path': PATH, 'og': 'builds', 'art': 'hero_campfire', 'compact': 'gear', 'more': False,
        'title': TX['name'], 'lead': TX['lead'], 'sections': []}


# ---------- stat weights of a spec: the order of content/spec_cheats.STATS ----------

UNIT = {'str': 1, 'agi': 1, 'sta': 1, 'int': 1, 'spi': 1, 'sp': 1, 'hp': .6, 'ap': .5, 'crit': 12, 'hit': 12, 'mp5': 2.5, 'def': 1,
        'armor': .03, 'wd': 2.5}
BASE = {'sta': .15, 'armor': .004}   # unlisted: a little stamina and armor still beats nothing


def weights(order):
    """'sp crit hit int' -> {stat: weight per point}: the first stat 1.0 down to 0.5 for the last, times the size of a point (UNIT).
    «wd» (weapon damage) weighs the weapon's damage per second."""
    keys = order.split()
    w = dict(BASE)
    for i, k in enumerate(keys):
        if k not in UNIT:
            continue                                   # expertise, haste: the catalog has no such stat
        r = 1 - .5 * i / max(len(keys) - 1, 1)
        w['dps' if k == 'wd' else k] = round(r * UNIT[k], 4)
    return w


def spec_weights():
    from content import spec_cheats
    out = {}
    for key, v in spec_cheats.STATS.items():
        if isinstance(v, tuple):
            out[key] = weights(v[0])
    return out


# ---------- data files ----------

def _src_text(src, lang, tr):
    """One source of data/gear30.json in the page language: (kind 0 dungeon, 1 quest, 2 profession, text)."""
    from content import spec_cheats as sc
    def name(x):   # a boss, dungeon or quest: the official name of the language (i18n/names.json) when there is one
        en = x if isinstance(x, str) else (x.get(lang) or x.get('en') or '')
        return (langs.NAMES.get(en) or {}).get(lang) or en
    if src['kind'] == 'drop':
        txt = ' · '.join(x for x in (name(src.get('boss') or {}), name(src.get('dungeon') or {})) if x)
        return (0, txt or TX['world'][lang]) if src.get('dungeon') or txt else None
    if src['kind'] == 'quest':
        q = name(src.get('quest') or {})
        return 1, f'{TX["quest"][lang]}: {q}' if q else TX['quest'][lang]
    if src['kind'] == 'craft' and src.get('prof') in sc.G_PROF:
        return 2, tr(sc.G_PROF[src['prof']], lang)
    return None


# the side of an item the catalog does not mark: PvP rewards and city guards by the English name (Classic: Arathi Basin Highlander's /
# Defiler's, Warsong Gulch Sentinel's / Outrunner's and Outrider's, Alterac Valley Stormpike / Frostwolf, the honor ranks)
FACTION_RX = {
    'a': r"^(Highlander's|Sentinel's|Stormpike|Stormwind Guard|Knight-Lieutenant's|Knight-Captain's|Lieutenant Commander's|Sergeant Major's|"
         r"Master Sergeant's|(Field |Grand )?Marshal's (Chain|Dragonhide|Dreadweave|Lamellar|Leather|Mail|Plate|Satin|Silk))|^Talisman of Arathor$",
    'h': r"^(Defiler's|Outrunner's|Outrider's|Frostwolf|Legionnaire's|Blood Guard's|First Sergeant's|Senior Sergeant's|Stone Guard's|"
         r"(High )?Warlord's|(Lieutenant )?General's (Chain|Dragonhide|Dreadweave|Lamellar|Leather|Mail|Plate|Satin|Silk)|"
         r"Champion's (Chain|Dragonhide|Dreadweave|Lamellar|Leather|Mail|Plate|Satin|Silk))",
}


# items of the catalog no player gets: Blizzard's test and staff items
JUNK = __import__('re').compile(r"^\d|^The 1 Ring$|Gamemaster|\bTest\b|\[PH\]|Deprecated|^Monster ")
# the levels our build (data/gear30.json) is made for: as content/play_card.GEAR_LO, GEAR_HI; «Fill» above them picks by stats
COVER = [16, 30]


def faction_of(en, srcs):
    """'a', 'h' or '' (both sides): the item's English name (FACTION_RX), else its guide sources when every one is a quest of one side."""
    import re
    for f, rx in FACTION_RX.items():
        if re.search(rx, en or ''):
            return f
    fs = {(s.get('faction') or '') for s in srcs or []}
    if srcs and all(s.get('kind') == 'quest' for s in srcs) and len(fs) == 1 and '' not in fs:
        return fs.pop()[0]
    return ''


def planner_data(lang, tr=None, catalog=None, gear=None):
    """The data file of one language: items [id, slot, quality, item level, required level, class, subclass, icon, name, stats],
    sources of the items the guides list, our build per spec (data/gear30.json, the ids the catalog has) and the side of the items
    of one faction (fa: id -> 'a' | 'h')."""
    tr = tr or (lambda s, l: s)
    cat = catalog or json.load(open(CATALOG, encoding='utf-8'))
    li = cat['langs'].index(lang) if lang in cat['langs'] else 0
    if gear is None:
        from content import spec_cheats as sc
        gear = sc.GEAR30
    items = []
    for iid, it in sorted(cat['items'].items(), key=lambda x: int(x[0])):
        if it.get('c') != 'equip' or it.get('s') not in SL:
            continue
        if tuple(it['k']) == (2, 20):                  # fishing poles
            continue
        if (it.get('il') or 0) < 2 or JUNK.search(it['n'][0] or ''):   # Gamemaster gear, test items, festival trinkets of item level 1
            continue
        st = []
        for k, v in (it.get('st') or {}).items():
            if k in K and v:
                st += [K.index(k), v]
        nm = it['n'][li] or it['n'][0]
        items.append([int(iid), SL.index(it['s']), it.get('q', 1), it.get('il') or 0, it.get('lvl') or 0, it['k'][0], it['k'][1],
                      it.get('i', -1), nm, st])
    have = {x[0] for x in items}
    src = {}
    for key, rows in (gear.get('specs') or {}).items():
        for e in rows:
            if e['id'] in have and str(e['id']) not in src:
                got = [x for x in (_src_text(s, lang, tr) for s in e.get('src') or []) if x]
                if got:
                    src[str(e['id'])] = [got[0][0], ' / '.join(dict.fromkeys(t for _, t in got))]
    ours = {key: [e['id'] for e in rows if e['id'] in have] for key, rows in (gear.get('specs') or {}).items()}
    srcs = {}
    for rows in (gear.get('specs') or {}).values():
        for e in rows:
            srcs.setdefault(e['id'], []).extend(e.get('src') or [])
    fa = {}
    for iid, it in cat['items'].items():
        if int(iid) in have:
            f = faction_of(it['n'][0], srcs.get(int(iid)))
            if f:
                fa[iid] = f
    return {'v': 1, 'k': K, 'sl': SL, 'it': items, 'src': src, 'b': {k: v for k, v in ours.items() if v}, 'fa': fa, 'cv': COVER}


def vhash(path):
    return hashlib.sha1(open(path, 'rb').read()).hexdigest()[:8]


def write_data(tr=None):
    """assets/gear/planner-<lang>.json for every built language; {lang: '?v=<hash>'}."""
    cat = json.load(open(CATALOG, encoding='utf-8'))
    out = {}
    for lang in langs.LANGS:
        data = json.dumps(planner_data(lang, tr, cat), ensure_ascii=False, separators=(',', ':'))
        p = os.path.join(OUT, f'planner-{lang}.json')
        old = open(p, encoding='utf-8').read() if os.path.isfile(p) else None
        if old != data + '\n':
            open(p, 'w', encoding='utf-8', newline='\n').write(data + '\n')
        out[lang] = vhash(p)
    return out


_VER = {}


def data_v(lang):
    if not _VER:
        import build
        _VER.update(write_data(build.tr))
    return _VER[lang]


# ---------- the page ----------

ICONS = {   # simple outlines of the empty slots, 24 px grid, stroked with currentColor
    'head': 'M5 14a7 7 0 0 1 14 0v5h-4.5v-4h-5v4H5z',
    'neck': 'M6 4c0 5 2.7 8 6 8s6-3 6-8M12 12v2.5M9.5 17a2.5 2.5 0 1 0 5 0a2.5 2.5 0 1 0-5 0',
    'shoulder': 'M3 15c0-5.5 4-9 9-9s9 3.5 9 9l-4 1.5-2-3.5H9l-2 3.5z',
    'back': 'M8 4h8l3 16-7-3-7 3z',
    'chest': 'M9 4 4 7l2 5 2-1v9h8v-9l2 1 2-5-5-3-1.5 2h-3z',
    'wrist': 'M7 8h10v8H7zM7 12h10',
    'hands': 'M8 21v-6L5.5 11l1.2-1L9 12V5.5h1.6V11V4h1.6v7V4.6h1.6V11V6h1.6v9l-1.8 6z',
    'waist': 'M3 10h18v4H3zM10 8.5h4v7h-4z',
    'legs': 'M7 3h10l-1 18h-3l-1-11-1 11H8z',
    'feet': 'M8 3h5v10l6 3v4H6v-5l2-2z',
    'finger': 'M7 14a5 5 0 1 0 10 0a5 5 0 1 0-10 0M10 6l2-3 2 3-2 2z',
    'trinket': 'M12 3l6 6-6 12-6-12zM6 9h12',
    'main': 'M19 3v4l-9 9-3-3 9-9zM7.5 13.5l3 3M5 16l3 3-2 2-3-3z',
    'off': 'M12 3l8 3v6c0 5-4 8-8 9-4-1-8-4-8-9V6z',
    'ranged': 'M6 3c9 3 9 15 0 18M6 3v18M4 12h15M16 9.5l3 2.5-3 2.5',
}


def icon_of(cell):
    return cell.rstrip('12')


def slot_name(cell, lang):
    from content import spec_cheats as sc
    c = icon_of(cell)
    if c == 'main':
        return TX['right'][lang]
    if c == 'finger':
        return TX['ring'][lang]
    return sc.GSLOT[c][lang]


def stat_names(lang):
    from content import spec_cheats as sc
    long = {k: (sc.STAT.get(k) or sc.EXTRA.get(k))[lang] for k in K if k != 'dps'}
    long['dps'] = TX['dps'][lang]
    return long


CSS = r'''<style>
/* Gear planner (character/gear/, gear_planner.py + assets/gear/planner.js): the bar, the doll of 17 slots, the stats, the picker */
:root { --q0: #8f8f8f; --q1: var(--fg); --q2: #5cb84c; --q3: #4b97e3; --q4: #b07ce6; --q5: #e0913f; }
:root[data-theme="light"] { --q0: #6e6e6e; --q2: #2c7a21; --q3: #1d5fae; --q4: #7a40b0; --q5: #a65a17; }
.gp { display: grid; gap: 16px; }
.gpbar { display: flex; flex-wrap: wrap; align-items: end; gap: 12px 14px; padding: 14px 16px; }
.gpf { display: grid; gap: 4px; min-width: 0; font-size: var(--fs-13); color: var(--muted); font-weight: 600; }
.gpf select { min-height: 44px; max-width: 100%; padding: 0 34px 0 12px; border: 1px solid var(--fline); border-radius: 7px; background: var(--panel-2); color: var(--fg); font: inherit; font-size: var(--fs-16); font-weight: 600; }
.gpf select:focus-visible, .gp button:focus-visible, .gpk :is(button, input):focus-visible { outline: 2px solid var(--gold); outline-offset: 2px; }
.gpbar .stepper input { width: 48px; }
.gpact { display: flex; flex-wrap: wrap; gap: 8px; margin-left: auto; }
.gpact .btn { padding: 0 14px; }
.gpmain { display: grid; gap: 16px; grid-template-columns: minmax(0, 1fr); align-items: start; }
@media (min-width: 1100px) { .gpmain { grid-template-columns: minmax(0, 1fr) 300px; } }
.gpd { display: grid; gap: 8px; padding: 14px; grid-template-columns: minmax(0, 1fr); }
.gpd .gpc { display: grid; gap: 8px; align-content: start; min-width: 0; }
@media (min-width: 720px) {
  .gpd { grid-template-columns: repeat(2, minmax(0, 1fr)); column-gap: 14px; }
  .gpd .gpw { grid-column: 1 / -1; grid-template-columns: repeat(3, minmax(0, 1fr)); border-top: 1px solid var(--pline); padding-top: 10px; }
}
/* one slot: the picker button and the ✕ beside it */
.gpsw { position: relative; display: flex; min-width: 0; }
.gpsl { flex: 1; min-width: 0; display: grid; grid-template-columns: 56px minmax(0, 1fr); gap: 10px; align-items: center; min-height: 64px; padding: 4px 6px; border: 1px solid transparent; border-radius: 8px; background: none; color: var(--fg); font: inherit; text-align: left; cursor: pointer; }
.gpsl:hover { background: var(--zebra); border-color: var(--pline); }
.gpsl[disabled] { cursor: default; opacity: .6; }
.gpsl[disabled]:hover { background: none; border-color: transparent; }
.gpsw.on .gpsl { padding-right: 46px; }
.gpi { position: relative; width: 56px; height: 56px; border-radius: 6px; border: 2px solid var(--line-2); background: var(--panel-2); color: var(--muted); display: grid; place-items: center; }
.gpi svg { width: 28px; height: 28px; fill: none; stroke: currentColor; stroke-width: 1.4; stroke-linejoin: round; stroke-linecap: round; opacity: .75; }
.gpi.ic, .gpr .gpi { background: #16181c var(--gsp, none) no-repeat; --sz: 52px; background-size: calc(64 * var(--sz)) auto; background-position: calc(var(--ix) * var(--sz) * -1) calc(var(--iy) * var(--sz) * -1); background-clip: padding-box; }
.gpi.q0 { border-color: var(--q0); } .gpi.q1 { border-color: color-mix(in srgb, var(--fg) 55%, transparent); } .gpi.q2 { border-color: var(--q2); } .gpi.q3 { border-color: var(--q3); } .gpi.q4 { border-color: var(--q4); } .gpi.q5 { border-color: var(--q5); }
.gpi b { position: absolute; right: -2px; bottom: -2px; min-width: 22px; padding: 0 3px; border-radius: 5px 0 5px 0; background: rgba(5,5,5,.86); color: #f1ece0; font-size: 11px; line-height: 16px; font-weight: 700; text-align: center; font-variant-numeric: tabular-nums; }
.gptx { display: grid; gap: 1px; min-width: 0; line-height: 1.3; }
.gpkk { color: var(--muted); font-size: var(--fs-13); }
.gpn { font-weight: 600; overflow-wrap: anywhere; }
.gpsl.empty .gpn { font-weight: 500; color: var(--muted); }
.gpss { font-size: var(--fs-13); color: var(--fg); overflow-wrap: anywhere; }
.gpsr { font-size: var(--fs-13); color: var(--muted); overflow-wrap: anywhere; }
.iq0 { color: var(--q0); } .iq2 { color: var(--q2); } .iq3 { color: var(--q3); } .iq4 { color: var(--q4); } .iq5 { color: var(--q5); }
.gpx { position: absolute; top: 50%; right: 2px; transform: translateY(-50%); width: 44px; height: 44px; border: 0; border-radius: 7px; background: none; color: var(--muted); font-size: 18px; cursor: pointer; }
.gpx:hover { color: var(--fg); background: var(--zebra); }
/* stats */
.gpst { padding: 16px; display: grid; gap: 10px; }
.gpst h2 { margin: 0; font-size: var(--fs-22); }
.gpst dl { margin: 0; display: grid; }
.gpst dl > div { display: flex; justify-content: space-between; gap: 12px; padding: 6px 0; border-bottom: 1px solid var(--pline); }
.gpst dt { color: var(--muted); }
.gpst dd { margin: 0; font-weight: 600; font-variant-numeric: tabular-nums; }
.gpst p { margin: 0; }
.gpnote { margin: 0; }
/* the picker: a sheet from the bottom on phones, a box by the slot on wide screens */
dialog.gpk { border: 1px solid var(--line); padding: 0; background: var(--rail); color: var(--fg); width: min(440px, calc(100vw - 32px)); max-width: none; height: min(620px, calc(100dvh - 32px)); max-height: none; border-radius: 10px; margin: 0; position: fixed; inset: auto; overflow: hidden; }
dialog.gpk[open] { display: flex; flex-direction: column; }
dialog.gpk::backdrop { background: rgba(0,0,0,.45); }
@media (max-width: 719px) {
  dialog.gpk { inset: auto 0 0 0; width: 100%; height: 85dvh; border-radius: 10px 10px 0 0; border-width: 1px 0 0; padding-bottom: env(safe-area-inset-bottom, 0px); }
}
.gpkh { display: flex; align-items: center; gap: 8px; padding: 8px 8px 8px 16px; border-bottom: 1px solid var(--line); }
.gpkh h2 { flex: 1; margin: 0; font-size: var(--fs-18); }
.gpkh .iconbtn { flex: none; }
.gpks { padding: 10px 12px 6px; display: grid; gap: 8px; }
.gpks input { width: 100%; min-height: 44px; padding: 0 12px; border: 1px solid var(--fline); border-radius: 7px; background: var(--panel-2); color: var(--fg); font: inherit; font-size: var(--fs-16); }
.gpch { display: flex; flex-wrap: wrap; gap: 6px; }
.gpch button { min-height: 36px; padding: 0 12px; border: 1px solid var(--pline); border-radius: 999px; background: var(--panel-2); color: var(--fg); font: inherit; font-size: var(--fs-14); font-weight: 600; cursor: pointer; }
.gpch button[aria-pressed="true"] { border-color: var(--gold); background: var(--seg-on); color: var(--gold-2); }
.gpch button[aria-pressed="true"]::before { content: "✓ "; }
.gpkm { margin: 0; padding: 0 14px 6px; font-size: var(--fs-13); color: var(--muted); }
.gpl { position: relative; flex: 1; min-height: 0; overflow-y: auto; overscroll-behavior: contain; border-top: 1px solid var(--pline); }
.gplin { position: relative; }
.gpr { position: absolute; left: 0; right: 0; height: 56px; display: grid; grid-template-columns: 40px minmax(0, 1fr) auto; gap: 0 10px; align-items: center; padding: 0 12px; border: 0; border-bottom: 1px solid var(--pline); background: none; color: var(--fg); font: inherit; text-align: left; cursor: pointer; }
.gpr:hover, .gpr:focus-visible { background: var(--zebra); }
.gpr:focus-visible { outline-offset: -2px; }
.gpr.cur { background: var(--seg-on); }
.gpr .gpi { width: 40px; height: 40px; border-radius: 5px; --sz: 36px; }
.gpr .gpi.no { background-image: none; }
.gpr .gpt { display: grid; min-width: 0; line-height: 1.25; }
.gpr .gpn, .gpr .gpm { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.gpr .gpm { font-size: var(--fs-13); color: var(--muted); }
.gpr .gpdl { font-size: var(--fs-13); font-weight: 700; font-variant-numeric: tabular-nums; white-space: nowrap; max-width: 9.5em; overflow: hidden; text-overflow: ellipsis; }
.gpr.off { position: static; height: 48px; grid-template-columns: 40px minmax(0, 1fr); }
.gpdl.up { color: var(--new); } .gpdl.dn { color: var(--horde); }
.gpe { padding: 18px 16px; color: var(--muted); }
.gptoast { position: fixed; left: 50%; bottom: calc(84px + env(safe-area-inset-bottom, 0px)); z-index: 60; transform: translateX(-50%); max-width: calc(100vw - 32px); padding: 10px 16px; border-radius: 8px; background: var(--fg); color: var(--bg); font-weight: 600; box-shadow: 0 8px 24px rgba(0,0,0,.35); opacity: 0; pointer-events: none; transition: opacity .2s; }
.gptoast.on { opacity: 1; }
@media (min-width: 720px) { .gptoast { bottom: 24px; } }
@media (max-width: 719px) {
  .gpbar { padding: 12px; }
  .gpf { flex: 1 1 40%; }
  .gpf select { width: 100%; }
  .gpact { margin-left: 0; width: 100%; }
  .gpact .btn { flex: 1 1 auto; }
  .gpsl { grid-template-columns: 48px minmax(0, 1fr); min-height: 56px; }
  .gpi { width: 48px; height: 48px; }
  .gpsl .gpi.ic { --sz: 44px; }
  .gpd { padding: 8px; gap: 4px; }
  .gpr { padding: 0 10px; gap: 0 8px; align-content: center; }   /* phone: the name gets the full width, the delta sits under it */
  .gpr .gpt { display: contents; }
  .gpr .gpi { grid-row: 1 / 3; }
  .gpr .gpn { grid-column: 2 / 4; grid-row: 1; }
  .gpr .gpm { grid-column: 2; grid-row: 2; }
  .gpr .gpdl { grid-column: 3; grid-row: 2; max-width: 11em; }
  .gpr.off .gpn, .gpr.off .gpm { grid-column: 2; }
}
@media (prefers-reduced-motion: reduce) { .gptoast { transition: none; } }
</style>'''


def head(sec, lang):
    """The text heading: crumbs Home / My character / Gear planner, h1 and lead (like the calculator's chead)."""
    import seo
    from html import escape
    crumbs = __import__('re').search(r'<nav class="crumbs".*?<span aria-hidden="true">/</span>', sec, __import__('re').S)[0]
    return (f'<section class="chead" id="top"><div class="wrap">{crumbs}<a href="@@HOME@@character/">{escape(seo.CHAR_NAME[lang])}</a>'
            f'<span aria-hidden="true">/</span><span>{escape(TX["name"][lang])}</span></nav><h1>@@TITLE@@</h1>'
            f'<p class="glead">@@LEAD@@</p></div></section>')


def config(lang, core, races):
    """The script's data: texts, classes with specs, races, slot names, stat names, weights, file addresses."""
    tx = {k: v[lang] for k, v in TX.items() if k not in ('lead', 'rules', 'name')}
    import build
    slug = {r['id']: r['slug'] for r in build.RACES_PAGE}   # the race in the address as on the site (night-elf); the old ids still read
    cls = [[c['id'], core['cn'][c['id']], core['sid'][c['id']], core['sn'][c['id']]] for c in build.CLASSES]
    return {
        'tx': tx, 'cls': cls, 'color': build.COLOR,
        'races': [[r['id'], core['rn'][r['id']], r['f'], list(r['can']), slug.get(r['id'], r['id'])] for r in races],
        'cells': CELLS, 'icons': {c: ICONS[icon_of(c)] for c in CELLS}, 'slot': {c: slot_name(c, lang) for c in CELLS}, 'short': SHORT[lang], 'long': stat_names(lang),
        'w': spec_weights(), 'data': f'@@ROOT@@assets/gear/planner-{lang}.json?v={data_v(lang)}',
        'sprite': f'@@ROOT@@assets/gear/catalog.webp?v={vhash(SPRITE)}', 'dec': ',' if lang not in ('en',) else '.',
    }


def cell_html(cell, lang):
    from html import escape
    name = slot_name(cell, lang)
    return (f'<div class="gpsw" data-cell="{cell}"><button class="gpsl empty" type="button" aria-haspopup="dialog">'
            f'<span class="gpi" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="{ICONS[icon_of(cell)]}"/></svg></span>'
            f'<span class="gptx"><b class="gpn">{escape(name)} · {escape(TX["pick"][lang])}</b></span></button></div>')


def body(lang, root, core, races):
    """The page body: the bar, the doll, the stats, the picker dialog and the script."""
    from html import escape
    t = {k: escape(v[lang]) for k, v in TX.items()}
    cfg = json.dumps(config(lang, core, races), ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    col = lambda cells, cls: f'<div class="gpc {cls}">' + ''.join(cell_html(c, lang) for c in cells) + '</div>'  # noqa: E731
    stats = ''.join(f'<div data-k="{k}"><dt>{escape(v)}</dt><dd>0</dd></div>' for k, v in stat_names(lang).items() if k in ('str', 'agi', 'sta', 'int', 'spi', 'armor'))
    return (CSS + f'<div class="gp" id="gp">'
            f'<div class="frame gpbar" role="group" aria-label="{t["name"]}">'
            f'<label class="gpf">{t["cls"]}<select id="gpC"></select></label>'
            f'<label class="gpf">{t["spec"]}<select id="gpS"></select></label>'
            f'<label class="gpf">{t["race"]}<select id="gpR"></select></label>'
            f'<div class="gpf"><span id="gpLl">{t["lvl"]}</span><div class="stepper" role="group" aria-labelledby="gpLl">'
            f'<button type="button" id="gpLm" aria-label="{t["lvlDown"]}">−</button>'
            f'<input id="gpL" type="number" min="1" max="60" value="30" inputmode="numeric" aria-labelledby="gpLl">'
            f'<button type="button" id="gpLp" aria-label="{t["lvlUp"]}">+</button></div></div>'
            f'<div class="gpact"><button class="btn" type="button" id="gpFill">{t["fill"]}</button>'
            f'<button class="btn ghost" type="button" id="gpCopy">{t["copy"]}</button>'
            f'<button class="btn ghost" type="button" id="gpClear">{t["clear"]}</button></div></div>'
            f'<div class="gpmain"><section class="frame gpd" id="gpD" aria-label="{t["doll"]}">'
            + col(LEFT, 'l') + col(RIGHT, 'r') + col(WEAP, 'gpw') +
            f'</section><aside class="frame gpst" id="gpSt" aria-labelledby="gpStH"><h2 id="gpStH">{t["stats"]}</h2>'
            f'<dl id="gpStL">{stats}</dl><p class="small">{t["statsNote"]}</p></aside></div>'
            f'<p class="small gpnote">{t["rules"]}</p></div>'
            f'<dialog class="gpk" id="gpK" aria-labelledby="gpKh"><div class="gpkh"><h2 id="gpKh"></h2>'
            f'<button class="iconbtn" type="button" id="gpKx" aria-label="{t["close"]}"><svg class="ico" aria-hidden="true"><use href="#i-x"/></svg></button></div>'
            f'<div class="gpks"><input id="gpQ" type="search" autocomplete="off" placeholder="{t["search"]}" aria-label="{t["search"]}">'
            f'<div class="gpch" role="group" aria-label="{t["filters"]}">'
            + ''.join(f'<button type="button" data-f="{f}" aria-pressed="{"true" if f in ("lvl", "arm") else "false"}">{t["f" + f.title()]}</button>'
                      for f in ('lvl', 'arm', 'rare', 'drop', 'quest', 'craft')) +
            f'</div></div><p class="gpkm" id="gpKm" role="status"></p><div id="gpOff"></div>'
            f'<div class="gpl" id="gpList"><div class="gplin" id="gpIn"></div></div></dialog>'
            f'<p class="gptoast" id="gpT" role="status" aria-live="polite"></p>'
            f'<script type="application/json" id="gpData">{cfg}</script>'
            f'<script src="@@ROOT@@assets/gear/planner.js?v={vhash(SCRIPT)}" defer></script>')
