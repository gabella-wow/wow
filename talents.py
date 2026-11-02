"""Talent trees in the spec guides (guides/builds-<class>/): the full class tree with our path in gold, a card under the tree
and the order by level. Decision 26.10 (variant B of docs/wow/audit/2026-10-26-talents).

Data: content/talents/<class>.json, written by tools/talent_import.py from the GabellaTalents addon (rows, columns, arrows and
icons straight from the Forever client through the addon API) and tools/talent_icons.py (icon names from the Blizzard Game Data
API, the pictures from Blizzard's render CDN into one sprite per class, assets/talents/<class>.webp). No file -> no tree: the
page keeps its table. The points come from the spec's talent table in content/spec_builds.py (one source for the numbers).
Rendered at build time: no fetch, no layout shift; the inline script only opens the card, switches tabs and wakes the sprite."""
import json, os, re
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'content', 'talents')
FIRST_LEVEL, CAP_LEVEL = 10, 30            # the first talent point, the beta cap the spec guides are written for
ROW_POINTS = 5                             # a row opens every 5 points spent in its tree

# The order of the talent tabs in the client, the same as the spec sections of guides/builds-<class>/
TREES = {'paladin': ['holy', 'protection', 'retribution'], 'warrior': ['arms', 'fury', 'protection'],
         'mage': ['arcane', 'fire', 'frost'], 'hunter': ['beast-mastery', 'marksmanship', 'survival'],
         'rogue': ['assassination', 'combat', 'subtlety'], 'priest': ['discipline', 'holy', 'shadow'],
         'shaman': ['elemental', 'enhancement', 'restoration'], 'warlock': ['affliction', 'demonology', 'destruction'],
         'druid': ['balance', 'feral', 'restoration']}

UI = {
    'hint': {'ru': 'Нажмите на значок: здесь откроется талант.', 'en': 'Tap an icon to see the talent here.',
             'uk': 'Натисніть на значок: тут відкриється талант.', 'de': 'Tippe auf ein Symbol, um das Talent hier zu sehen.',
             'es': 'Toca un icono para ver aquí el talento.', 'fr': 'Touchez une icône pour afficher le talent ici.',
             'it': 'Tocca un’icona per vedere qui il talento.', 'pl': 'Dotknij ikony, aby zobaczyć tu talent.',
             'pt': 'Toque num ícone para ver o talento aqui.'},
    'take': {'ru': 'Берём {p} из {m}', 'en': 'Take {p} of {m}', 'uk': 'Беремо {p} з {m}', 'de': '{p} von {m} nehmen',
             'es': 'Tomar {p} de {m}', 'fr': 'Prendre {p} sur {m}', 'it': 'Prendere {p} su {m}', 'pl': 'Bierzemy {p} z {m}',
             'pt': 'Pegar {p} de {m}'},
    'skip': {'ru': 'Не берём · рангов: {m}', 'en': 'Not taken · ranks: {m}', 'uk': 'Не беремо · рангів: {m}',
             'de': 'Nicht genommen · Ränge: {m}', 'es': 'No se toma · rangos: {m}', 'fr': 'Non pris · rangs : {m}',
             'it': 'Non preso · gradi: {m}', 'pl': 'Nie bierzemy · rangi: {m}', 'pt': 'Não pegar · níveis: {m}'},
    'lv': {'ru': 'ур. {a}', 'en': 'lvl {a}', 'uk': 'рів. {a}', 'de': 'Stufe {a}', 'es': 'nivel {a}', 'fr': 'niv. {a}',
           'it': 'liv. {a}', 'pl': 'poz. {a}', 'pt': 'nív. {a}'},
    'row': {'ru': 'Открыт с {n} очков в ветке', 'en': 'Opens at {n} points in the tree', 'uk': 'Відкривається з {n} очок у гілці',
            'de': 'Ab {n} Punkten im Baum', 'es': 'Desde {n} puntos en el árbol', 'fr': 'Dès {n} points dans l’arbre',
            'it': 'Da {n} punti nell’albero', 'pl': 'Od {n} punktów w drzewie', 'pt': 'A partir de {n} pontos na árvore'},
    'free': {'ru': 'На выбор', 'en': 'Your pick', 'uk': 'На вибір', 'de': 'Freie Wahl', 'es': 'A elegir', 'fr': 'Au choix',
             'it': 'A scelta', 'pl': 'Do wyboru', 'pt': 'À escolha'},
    'free_d': {'ru': 'Здесь Icy Veins и Wowhead расходятся: варианты — в тексте ниже.',
               'en': 'Icy Veins and Wowhead differ here: the options are in the text below.',
               'uk': 'Тут Icy Veins і Wowhead розходяться: варіанти — у тексті нижче.',
               'de': 'Hier gehen Icy Veins und Wowhead auseinander: Die Optionen stehen im Text unten.',
               'es': 'Aquí Icy Veins y Wowhead difieren: las opciones están en el texto de abajo.',
               'fr': 'Ici, Icy Veins et Wowhead divergent : les options sont dans le texte ci-dessous.',
               'it': 'Qui Icy Veins e Wowhead divergono: le opzioni sono nel testo qui sotto.',
               'pl': 'Tu Icy Veins i Wowhead się różnią: opcje są w tekście poniżej.',
               'pt': 'Aqui o Icy Veins e o Wowhead divergem: as opções estão no texto abaixo.'},
    'beta': {'ru': 'По данным беты Forever, уточним после старта', 'en': 'Forever beta data, we’ll update it after launch',
             'uk': 'За даними бети Forever, уточнимо після старту', 'de': 'Nach Daten der Forever-Beta, wir aktualisieren nach dem Start',
             'es': 'Según la beta de Forever, lo actualizaremos tras el lanzamiento',
             'fr': 'D’après la bêta de Forever, mis à jour après le lancement',
             'it': 'Secondo la beta di Forever, aggiorneremo dopo il lancio', 'pl': 'Według bety Forever, zaktualizujemy po starcie',
             'pt': 'Segundo a beta do Forever, atualizaremos após o lançamento'},
    'classic': {'ru': 'Как в Classic, Forever уточним после старта', 'en': 'As in Classic, we’ll update it for Forever after launch',
                'uk': 'Як у Classic, Forever уточнимо після старту', 'de': 'Wie in Classic, für Forever aktualisieren wir nach dem Start',
                'es': 'Como en Classic, lo actualizaremos para Forever tras el lanzamiento',
                'fr': 'Comme dans Classic, mis à jour pour Forever après le lancement',
                'it': 'Come in Classic, aggiorneremo per Forever dopo il lancio', 'pl': 'Jak w Classic, dla Forever zaktualizujemy po starcie',
                'pt': 'Como no Classic, atualizaremos para o Forever após o lançamento'},
    # The build leads to our calculator (a button); Wowhead is one small line under it to check against, rel="nofollow noopener"
    'go': {'ru': 'Открыть билд в калькуляторе', 'en': 'Open this build in the calculator', 'uk': 'Відкрити білд у калькуляторі',
           'de': 'Build im Talentrechner öffnen', 'es': 'Abrir la build en la calculadora', 'fr': 'Ouvrir le build dans le calculateur',
           'it': 'Apri la build nel calcolatore', 'pl': 'Otwórz build w kalkulatorze', 'pt': 'Abrir a build na calculadora'},
    'wh': {'ru': 'Сверить у Wowhead', 'en': 'Check on Wowhead', 'uk': 'Звірити на Wowhead', 'de': 'Bei Wowhead abgleichen',
           'es': 'Comparar en Wowhead', 'fr': 'Comparer sur Wowhead', 'it': 'Confronta su Wowhead', 'pl': 'Sprawdź na Wowhead',
           'pt': 'Conferir no Wowhead'},
    'perk': {'ru': 'с перком Legacy Talented ({n}/5)', 'en': 'with the Legacy Talented perk ({n}/5)',
             'uk': 'з перком Legacy Talented ({n}/5)', 'de': 'mit dem Legacy-Vorteil Talented ({n}/5)',
             'es': 'con la ventaja Legacy Talented ({n}/5)', 'fr': 'avec l’avantage Legacy Talented ({n}/5)',
             'it': 'con il vantaggio Legacy Talented ({n}/5)', 'pl': 'z atutem Legacy Talented ({n}/5)',
             'pt': 'com a vantagem Legacy Talented ({n}/5)'},
    'order': {'ru': 'Порядок по уровням', 'en': 'Order by level', 'uk': 'Порядок за рівнями', 'de': 'Reihenfolge nach Stufe',
              'es': 'Orden por nivel', 'fr': 'Ordre par niveau', 'it': 'Ordine per livello', 'pl': 'Kolejność wg poziomu',
              'pt': 'Ordem por nível'},
    # The build switcher (see BUILDS below): one button per build, shown only when the spec has data for it
    'bs': {'ru': 'Сборка', 'en': 'Build', 'uk': 'Збірка', 'de': 'Build', 'es': 'Build', 'fr': 'Build', 'it': 'Build',
           'pl': 'Build', 'pt': 'Build'},
    'b_general': {'ru': 'Общая', 'en': 'General', 'uk': 'Загальна', 'de': 'Allgemein', 'es': 'General', 'fr': 'Général',
                  'it': 'Generale', 'pl': 'Ogólna', 'pt': 'Geral'},
    'b_leveling': {'ru': 'Прокачка', 'en': 'Leveling', 'uk': 'Прокачка', 'de': 'Leveln', 'es': 'Subida de nivel',
                   'fr': 'Progression', 'it': 'Livellamento', 'pl': 'Levelowanie', 'pt': 'Evolução'},
    'b_dungeons': {'ru': 'Подземелья', 'en': 'Dungeons', 'uk': 'Підземелля', 'de': 'Dungeons', 'es': 'Mazmorras',
                   'fr': 'Donjons', 'it': 'Spedizioni', 'pl': 'Dungeony', 'pt': 'Masmorras'},
    'b_raid': {'ru': 'Рейд', 'en': 'Raid', 'uk': 'Рейд', 'de': 'Schlachtzug', 'es': 'Banda', 'fr': 'Raid', 'it': 'Incursione',
               'pl': 'Raid', 'pt': 'Raide'},
    'b_pvp': {'ru': 'PvP', 'en': 'PvP', 'uk': 'PvP', 'de': 'PvP', 'es': 'JcJ', 'fr': 'JcJ', 'it': 'PvP', 'pl': 'PvP', 'pt': 'PvP'},
    'lvh': {'ru': 'Порядок по уровням, 10–60', 'en': 'Order by level, 10–60', 'uk': 'Порядок за рівнями, 10–60',
            'de': 'Reihenfolge nach Stufe, 10–60', 'es': 'Orden por nivel, 10–60', 'fr': 'Ordre par niveau, 10–60',
            'it': 'Ordine per livello, 10–60', 'pl': 'Kolejność wg poziomu, 10–60', 'pt': 'Ordem por nível, 10–60'},
    'lvnote': {'ru': 'Порядок на уровни 31–60 взят из гайда прокачки класса; после старта сверим его с данными игры.',
               'en': 'The order for levels 31–60 comes from the class leveling guide; after launch we will check it against the game’s data.',
               'uk': 'Порядок на рівні 31–60 узято з гайда прокачування класу; після старту звіримо його з даними гри.',
               'de': 'Die Reihenfolge für die Stufen 31–60 stammt aus dem Level-Guide der Klasse; nach dem Start gleichen wir sie mit den Spieldaten ab.',
               'es': 'El orden de los niveles 31–60 viene de la guía de subida de la clase; tras el lanzamiento lo contrastaremos con los datos del juego.',
               'fr': 'L’ordre des niveaux 31–60 vient du guide de progression de la classe ; après le lancement, nous le comparerons aux données du jeu.',
               'it': 'L’ordine per i livelli 31–60 viene dalla guida al livellamento della classe; dopo il lancio lo confronteremo con i dati del gioco.',
               'pl': 'Kolejność na levele 31–60 pochodzi z poradnika levelowania klasy; po starcie porównamy ją z danymi z gry.',
               'pt': 'A ordem dos níveis 31–60 vem do guia de evolução da classe; após o lançamento, vamos compará-la com os dados do jogo.'},
    'lvwait': {'ru': 'Порядок 31–60 ждёт данных: в гайде прокачки последние три очка (58–60) не названы. До выгрузки деревьев из клиента идите по гайду, а три последних очка ставьте на свой выбор.', 'en': 'The 31–60 order is waiting for data: the leveling guide does not name the last three points (58–60). Until the trees are exported from the client, follow the guide and spend the last three points as you like.', 'uk': 'Порядок 31–60 чекає на дані: у гайді прокачування останні три очка (58–60) не названо. До вивантаження дерев із клієнта йдіть за гайдом, а три останні очка ставте на свій вибір.', 'de': 'Die Reihenfolge 31–60 wartet auf Daten: Der Level-Guide nennt die letzten drei Punkte (58–60) nicht. Bis die Talentbäume aus dem Client ausgelesen sind, folge dem Guide und setze die letzten drei Punkte nach Wahl.', 'es': 'El orden 31–60 espera datos: la guía de subida no nombra los tres últimos puntos (58–60). Hasta exportar los árboles del cliente, sigue la guía y reparte los tres últimos puntos a tu gusto.', 'fr': 'L’ordre 31–60 attend des données : le guide de progression ne nomme pas les trois derniers points (58–60). Tant que les arbres ne sont pas extraits du client, suivez le guide et placez les trois derniers points à votre guise.', 'it': 'L’ordine 31–60 attende i dati: la guida al livellamento non indica gli ultimi tre punti (58–60). Finché gli alberi non vengono estratti dal client, segui la guida e spendi gli ultimi tre punti a scelta.', 'pl': 'Kolejność 31–60 czeka na dane: poradnik levelowania nie wymienia trzech ostatnich punktów (58–60). Do czasu pobrania drzew z klienta idź za poradnikiem, a trzy ostatnie punkty wydaj według uznania.', 'pt': 'A ordem 31–60 aguarda dados: o guia de evolução não nomeia os três últimos pontos (58–60). Até exportar as árvores do cliente, siga o guia e gaste os três últimos pontos como preferir.'},
    'lvg': {'ru': 'Гайд по прокачке класса', 'en': 'Class leveling guide', 'uk': 'Гайд із прокачування класу',
            'de': 'Level-Guide der Klasse', 'es': 'Guía de subida de la clase', 'fr': 'Guide de progression de la classe',
            'it': 'Guida al livellamento della classe', 'pl': 'Poradnik levelowania klasy', 'pt': 'Guia de evolução da classe'},
    # The editor (your own build over the same tree): the bar under the switcher, the card lines, the reasons a point is refused
    'ed': {'ru': 'Собрать свой билд', 'en': 'Make your own build', 'uk': 'Зібрати свій білд', 'de': 'Eigenen Build erstellen',
           'es': 'Crear tu build', 'fr': 'Créer votre build', 'it': 'Crea la tua build', 'pl': 'Złóż własny build',
           'pt': 'Montar sua build'},
    'ed_x': {'ru': 'Вернуть нашу сборку', 'en': 'Back to our build', 'uk': 'Повернути нашу збірку', 'de': 'Zurück zu unserem Build',
             'es': 'Volver a nuestra build', 'fr': 'Revenir à notre build', 'it': 'Torna alla nostra build',
             'pl': 'Wróć do naszego buildu', 'pt': 'Voltar à nossa build'},
    'cnt': {'ru': 'Очки: {p} из {m}', 'en': 'Points: {p} of {m}', 'uk': 'Очки: {p} з {m}', 'de': 'Punkte: {p} von {m}',
            'es': 'Puntos: {p} de {m}', 'fr': 'Points : {p} sur {m}', 'it': 'Punti: {p} su {m}', 'pl': 'Punkty: {p} z {m}',
            'pt': 'Pontos: {p} de {m}'},
    'cm': {'ru': 'ЛКМ +, ПКМ −', 'en': 'Left-click +, right-click −', 'uk': 'ЛКМ +, ПКМ −', 'de': 'Linksklick +, Rechtsklick −', 'es': 'Clic izq. +, clic der. −', 'fr': 'Clic gauche +, clic droit −', 'it': 'Clic sinistro +, destro −', 'pl': 'LPM +, PPM −', 'pt': 'Clique esq. +, dir. −'},
    'cmt': {'ru': 'Тап +, долгое нажатие −', 'en': 'Tap +, long-press −', 'uk': 'Тап +, довге натискання −', 'de': 'Tippen +, lang drücken −', 'es': 'Toque +, pulsación larga −', 'fr': 'Appui +, appui long −', 'it': 'Tocco +, tocco lungo −', 'pl': 'Dotyk +, przytrzymanie −', 'pt': 'Toque +, toque longo −'},
    'add': {'ru': 'Ставить', 'en': 'Add', 'uk': 'Ставити', 'de': 'Setzen', 'es': 'Añadir', 'fr': 'Ajouter', 'it': 'Aggiungi',
            'pl': 'Dodaj', 'pt': 'Adicionar'},
    'del': {'ru': 'Снимать', 'en': 'Remove', 'uk': 'Знімати', 'de': 'Entfernen', 'es': 'Quitar', 'fr': 'Retirer', 'it': 'Togli',
            'pl': 'Usuń', 'pt': 'Remover'},
    'reset': {'ru': 'Сброс', 'en': 'Reset', 'uk': 'Скинути', 'de': 'Zurücksetzen', 'es': 'Reiniciar', 'fr': 'Réinitialiser',
              'it': 'Azzera', 'pl': 'Resetuj', 'pt': 'Zerar'},
    'share': {'ru': 'Скопировать ссылку на билд', 'en': 'Copy build link', 'uk': 'Скопіювати посилання на білд',
              'de': 'Build-Link kopieren', 'es': 'Copiar enlace de la build', 'fr': 'Copier le lien du build',
              'it': 'Copia il link della build', 'pl': 'Kopiuj link do buildu', 'pt': 'Copiar link da build'},
    'copied': {'ru': 'Ссылка скопирована', 'en': 'Link copied', 'uk': 'Посилання скопійовано', 'de': 'Link kopiert',
               'es': 'Enlace copiado', 'fr': 'Lien copié', 'it': 'Link copiato', 'pl': 'Link skopiowany', 'pt': 'Link copiado'},
    'nocopy': {'ru': 'Не удалось скопировать: ссылка в адресной строке', 'en': 'Could not copy: the link is in the address bar',
               'uk': 'Не вдалося скопіювати: посилання в адресному рядку',
               'de': 'Kopieren fehlgeschlagen: Der Link steht in der Adresszeile',
               'es': 'No se pudo copiar: el enlace está en la barra de direcciones',
               'fr': 'Copie impossible : le lien est dans la barre d’adresse',
               'it': 'Copia non riuscita: il link è nella barra degli indirizzi',
               'pl': 'Nie udało się skopiować: link jest w pasku adresu',
               'pt': 'Não foi possível copiar: o link está na barra de endereço'},
    'eh': {'ru': 'Нажатие ставит очко, правая кнопка мыши, Delete или «Снимать» убирают. Билд сохраняется в этом браузере.',
           'en': 'A tap adds a point; right-click, Delete or Remove takes it back. The build is saved in this browser.',
           'uk': 'Натискання ставить очко, права кнопка миші, Delete або «Знімати» прибирають. Білд зберігається в цьому браузері.',
           'de': 'Tippen setzt einen Punkt, Rechtsklick, Entf oder „Entfernen“ nimmt ihn zurück. Der Build bleibt in diesem Browser gespeichert.',
           'es': 'Un toque añade un punto; clic derecho, Supr o «Quitar» lo retira. La build se guarda en este navegador.',
           'fr': 'Un appui ajoute un point ; clic droit, Suppr ou « Retirer » l’enlève. Le build est enregistré dans ce navigateur.',
           'it': 'Un tocco aggiunge un punto; tasto destro, Canc o «Togli» lo rimuove. La build resta salvata in questo browser.',
           'pl': 'Dotknięcie dodaje punkt, prawy przycisk, Delete lub „Usuń” go zabiera. Build zapisuje się w tej przeglądarce.',
           'pt': 'Um toque adiciona um ponto; clique direito, Delete ou «Remover» o retira. A build fica salva neste navegador.'},
    'eht': {'ru': 'Нажатие ставит очко, долгое нажатие или «Снимать» убирают. Билд сохраняется в этом браузере.',
            'en': 'A tap adds a point; a long press or Remove takes it back. The build is saved in this browser.',
            'uk': 'Натискання ставить очко, довге натискання або «Знімати» прибирають. Білд зберігається в цьому браузері.',
            'de': 'Tippen setzt einen Punkt, langes Drücken oder „Entfernen“ nimmt ihn zurück. Der Build bleibt in diesem Browser gespeichert.',
            'es': 'Un toque añade un punto; una pulsación larga o «Quitar» lo retira. La build se guarda en este navegador.',
            'fr': 'Un appui ajoute un point ; un appui long ou « Retirer » l’enlève. Le build est enregistré dans ce navigateur.',
            'it': 'Un tocco aggiunge un punto; un tocco lungo o «Togli» lo rimuove. La build resta salvata in questo browser.',
            'pl': 'Dotknięcie dodaje punkt, przytrzymanie lub „Usuń” go zabiera. Build zapisuje się w tej przeglądarce.',
            'pt': 'Um toque adiciona um ponto; um toque longo ou «Remover» o retira. A build fica salva neste navegador.'},
    'rank': {'ru': 'Ранг {p} из {m}', 'en': 'Rank {p} of {m}', 'uk': 'Ранг {p} з {m}', 'de': 'Rang {p} von {m}',
             'es': 'Rango {p} de {m}', 'fr': 'Rang {p} sur {m}', 'it': 'Grado {p} su {m}', 'pl': 'Ranga {p} z {m}',
             'pt': 'Nível {p} de {m}'},
    'e_cap': {'ru': 'Очки закончились: {m} из {m}', 'en': 'All {m} points are spent', 'uk': 'Очки закінчились: {m} з {m}',
              'de': 'Alle {m} Punkte sind vergeben', 'es': 'Ya se usaron los {m} puntos', 'fr': 'Les {m} points sont tous placés',
              'it': 'Tutti i {m} punti sono già spesi', 'pl': 'Punkty się skończyły: {m} z {m}',
              'pt': 'Todos os {m} pontos já foram usados'},
    'e_row': {'ru': 'Сначала {n} очков в ветке выше этого ряда', 'en': 'First {n} points in the rows above',
              'uk': 'Спершу {n} очок у гілці вище цього ряду', 'de': 'Zuerst {n} Punkte in den Reihen darüber',
              'es': 'Primero {n} puntos en las filas de arriba', 'fr': 'D’abord {n} points dans les rangées au-dessus',
              'it': 'Prima {n} punti nelle file sopra', 'pl': 'Najpierw {n} punktów w rzędach powyżej',
              'pt': 'Primeiro {n} pontos nas linhas acima'},
    'e_req': {'ru': 'Сначала все ранги: {t}', 'en': 'First all ranks of {t}', 'uk': 'Спершу всі ранги: {t}',
              'de': 'Zuerst alle Ränge von {t}', 'es': 'Primero todos los rangos de {t}', 'fr': 'D’abord tous les rangs de {t}',
              'it': 'Prima tutti i gradi di {t}', 'pl': 'Najpierw wszystkie rangi: {t}', 'pt': 'Primeiro todos os níveis de {t}'},
    'e_keep': {'ru': 'Нельзя снять: на это очко опираются таланты ниже', 'en': 'Can’t remove: talents below rely on this point',
               'uk': 'Не можна зняти: на це очко спираються таланти нижче',
               'de': 'Nicht entfernbar: Talente darunter brauchen diesen Punkt',
               'es': 'No se puede quitar: los talentos de abajo dependen de este punto',
               'fr': 'Impossible de retirer : des talents plus bas dépendent de ce point',
               'it': 'Non si può togliere: i talenti sotto dipendono da questo punto',
               'pl': 'Nie można zdjąć: talenty niżej opierają się na tym punkcie',
               'pt': 'Não dá para remover: talentos abaixo dependem deste ponto'},
    # The calculator pages talents/<class>/ (render_calc): the link from a guide, the row of our builds under the tree
    'calc': {'ru': 'Калькулятор талантов', 'en': 'Talent calculator', 'uk': 'Калькулятор талантів', 'de': 'Talentrechner',
             'fr': 'Calculateur de talents', 'es': 'Calculadora de talentos', 'pt': 'Calculadora de talentos',
             'it': 'Calcolatore di talenti', 'pl': 'Kalkulator talentów'},
    'ours': {'ru': 'Начать с нашей сборки', 'en': 'Start from our build', 'uk': 'Почати з нашої збірки',
             'de': 'Mit unserem Build starten', 'fr': 'Partir de notre build', 'es': 'Empezar con nuestra build',
             'pt': 'Começar pela nossa build', 'it': 'Parti dalla nostra build', 'pl': 'Zacznij od naszego buildu'},
    'gd': {'ru': 'Разбор спеков', 'en': 'Spec guides', 'uk': 'Розбір спеків', 'de': 'Skillungen im Detail',
           'fr': 'Guides des spécialisations', 'es': 'Guías de especialización', 'pt': 'Guias de especialização',
           'it': 'Guide alle specializzazioni', 'pl': 'Poradniki specjalizacji'},
}
JS_SKIP = ('hint', 'beta', 'classic', 'wh', 'perk', 'bs', 'b_general', 'b_leveling', 'b_dungeons', 'b_raid', 'b_pvp', 'lvh', 'lvnote', 'lvg', 'lvwait',
           'add', 'del', 'reset', 'share', 'eh', 'eht', 'cm', 'cmt', 'calc', 'ours', 'gd', 'go')
EDIT_CAP = 51                              # points at level 60: one per level from 10 (the leveling build above checks the same 51)
EN_NAMES = ('en', 'uk', 'pl')              # the site keeps English talent names on these pages (content/spec_builds.py)
WH_LANGS = ('ru', 'de', 'es', 'fr', 'it', 'pt')            # Wowhead's own interface languages (www.wowhead.com/forever/<lang>/…)


def day(iso, lang):
    y, m, d = iso.split('-')
    if lang == 'en':
        return f'{("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec")[int(m) - 1]} {int(d)}, {y}'
    return f'{d}{"/" if lang in ("es", "fr", "it", "pt") else "."}{m}{"/" if lang in ("es", "fr", "it", "pt") else "."}{y}'


def wowhead(cid, data, rows, lang):
    """A link to the spec in the Wowhead Forever calculator (see wowhead_ids); rows: (table cell, points) of the general build."""
    return wowhead_ids(cid, data, table_picks(data, rows), lang, perk(data, rows))


def table_picks(data, rows):
    picks = []
    for cell, n in rows:
        tree, t = match(data, cell)
        if t:
            picks.append((tree, t, int(n)))
    return picks


def wh_base(cid, lang):
    return f'https://www.wowhead.com/forever/{lang + "/" if lang in WH_LANGS else ""}talent-calc/{cid}/v2'


def wowhead_ids(cid, data, picks, lang, pk):
    return f'{wh_base(cid, lang)}{build_code(data, picks)}_t{pk}'


WH_REL = 'nofollow noopener'               # Wowhead is a source to check against, not a page we pass readers and link weight to


def go_button(root, cid, code, lang):
    """The main action of a build: the same build opened in our calculator (talents/<class>/#<code>)."""
    return f'<p class="tt-go"><a class="btn" href="{root}talents/{cid}/#{code}">{UI["go"][lang]}</a></p>'


def wh_link(href, lang, cls=''):
    """The small «check on Wowhead» line at the bottom of a build (never a button)."""
    c = f' class="{cls}"' if cls else ''
    return f'<a{c} href="{escape(href)}" target="_blank" rel="{WH_REL}">{UI["wh"][lang]} ↗</a>'


def build_code(data, picks):
    """The calculator's own build format (also our editor's #<spec>/<code>): one digit per talent of each tree in row/column
    order, trees joined by '-', trailing zeros cut; the URL adds _t<n> = ranks of the Legacy perk. picks: (tree, talent, points).
    The calculator drops a talent whose row is not open yet, so a gap our table leaves (points the sources do not agree on) is put
    into the first free talent of an open row of that tree, the same «your pick» the order by level shows."""
    pts = {}
    spent = {}
    for tree, t, n in sorted(picks, key=lambda x: x[1]['r']):
        need = ROW_POINTS * (t['r'] - 1) - spent.get(tree['key'], 0)
        for f in sorted(tree['talents'], key=lambda x: (x['r'], x['c'])):
            if need <= 0:
                break
            if f['r'] < t['r'] and not f.get('req') and f['id'] not in {p[1]['id'] for p in picks}:
                k = min(need, f['m'] - pts.get(f['id'], 0))
                if k > 0 and spent.get(tree['key'], 0) >= ROW_POINTS * (f['r'] - 1):
                    pts[f['id']] = pts.get(f['id'], 0) + k
                    spent[tree['key']] = spent.get(tree['key'], 0) + k
                    need -= k
        pts[t['id']] = pts.get(t['id'], 0) + n
        spent[tree['key']] = spent.get(tree['key'], 0) + n
    code = [''.join(str(pts.get(t['id'], 0)) for t in sorted(tr['talents'], key=lambda x: (x['r'], x['c']))).rstrip('0')
            for tr in data['trees']]
    while code and not code[-1]:
        code.pop()
    return '-'.join(code)

_names = None


def names():
    """i18n/names.json: English name -> de/es/fr/it/pt/ru (the client names, the same file the guides use)."""
    global _names
    if _names is None:
        _names = json.load(open(os.path.join(HERE, 'i18n', 'names.json'), encoding='utf-8'))
    return _names


def load(cid):
    p = os.path.join(DATA, f'{cid}.json')
    return json.load(open(p, encoding='utf-8')) if os.path.isfile(p) else None


def tname(t, lang):
    """A talent name on a page: the client's own name in that language, else the guides' dictionary, else English."""
    n = t['n']
    if lang in EN_NAMES:
        return n.get('en') or n.get('ru', '')
    return n.get(lang) or names().get(n.get('en', ''), {}).get(lang) or n.get('en') or n.get('ru', '')


def desc(t, lang):
    """The client's tooltip text for the talent in that language (the longest line that is not the name, rank or requirement)."""
    lines = (t.get('tip') or {}).get('en' if lang in EN_NAMES else lang) or []
    body = [x for x in lines[1:] if not re.match(r'^(Rank|Ранг|Requires|Требует|Rang|Rango|Grado|Nível)\b', x)]
    return max(body, key=len) if body else ''


def _plain(x):
    return re.sub(r'\s*\(.*\)$', '', x).strip().lower()


def match(data, cell):
    """The talent of a table row: its English name (or the spell id from i18n/names_ids.json), else the Russian one."""
    en = cell['en'] if isinstance(cell, dict) else cell
    ru = _plain(cell['ru']) if isinstance(cell, dict) else ''
    ids = json.load(open(os.path.join(HERE, 'i18n', 'names_ids.json'), encoding='utf-8')).get(en) or {}
    for tree in data['trees']:
        for t in tree['talents']:
            if _plain(t['n'].get('en', '')) == en.lower() or (ids.get('id') and ids['id'] in t.get('spells', ())):
                return tree, t
    for tree in data['trees']:
        for t in tree['talents']:
            if ru and _plain(t['n'].get('ru', '')) == ru:
                return tree, t
    return None, None


def perk(data, rows):
    """Ranks of the Legacy Talented perk (one more point per rank, from level 9 down to 5) a table needs to fit level 30:
    some beta builds of the sources count those 5 points (21 + 5). 0 when the table fits the 21 points of level 30."""
    steps = plan(data, rows)[1]
    named_end = max((b for t, _, _, b in steps if t), default=FIRST_LEVEL)
    return max(0, min(5, named_end - CAP_LEVEL))


def plan(data, rows, first=FIRST_LEVEL):
    """Our points on the tree and the order by level. rows: (table cell, points) in table order.
    Returns ({talent id: points}, steps). A step is (talent or None, points, first level, last level); None is a run of points
    the sources do not agree on: a row of the tree needs 5 points per row spent in it first, and the tail up to level 30."""
    picks, unknown = [], []
    for cell, pts in rows:
        tree, t = match(data, cell)
        if t is None:
            unknown.append(cell)
            continue
        picks.append((tree['key'], t, int(pts)))
    order = sorted(range(len(picks)), key=lambda i: (picks[i][1]['r'], i))
    spent, steps, level = {}, [], first
    for i in order:
        key, t, pts = picks[i]
        need = ROW_POINTS * (t['r'] - 1) - spent.get(key, 0)
        if need > 0:                                               # the tree needs points we do not name
            steps.append((None, need, level, level + need - 1))
            spent[key] = spent.get(key, 0) + need
            level += need
        steps.append((t, pts, level, level + pts - 1))
        spent[key] = spent.get(key, 0) + pts
        level += pts
    if level <= CAP_LEVEL:
        steps.append((None, CAP_LEVEL - level + 1, level, CAP_LEVEL))
    return {t['id']: pts for _, t, pts in picks}, steps, spent, unknown


# ---- Build switcher: the general build (the table of the spec) plus one tab per extra build that has data -------------------------
# A build is a dict: picked {talent id: ranks}, steps [(talent, points, first level, last level)], spent {tree key: points},
# at {talent id: 'levels text'}, main (tree key shown first), picks [(tree, talent, ranks)] for the calculator link, pk,
# head/note/guide (UI keys). A provider returns None when the spec has no data: no data, no tab, never an empty tab.
# Leveling 10-60 comes from the leveling guides (content/class_guides.py, one spec per class); dungeons / raid / pvp get a provider
# once level 60 data with a source exists (after the launch).
BUILD_IDS = ('leveling', 'dungeons', 'raid', 'pvp')                  # tab order; the ids are also the URL anchors (#protection-leveling)
LEVEL_SPEC = {'warrior': 'protection', 'paladin': 'retribution', 'hunter': 'beast-mastery', 'rogue': 'combat',
              'priest': 'shadow', 'shaman': 'enhancement', 'mage': 'frost', 'warlock': 'affliction', 'druid': 'feral'}
LEVEL_CAP = 60


def _find(data, cell):
    """The talent of a leveling table row by its English name (apostrophes unified)."""
    def n(x):
        return re.sub(r'\s*\(.*\)$', '', x.replace('’', "'")).strip().lower()
    en = cell['en'] if isinstance(cell, dict) else cell
    for tree in data['trees']:
        for t in tree['talents']:
            if n(t['n'].get('en', '')) == n(en):
                return tree, t
    return None, None


def _level_rows(cid):
    from content import class_guides
    for g in class_guides.CLASS_GUIDES:
        if g['slug'] == f'leveling-{cid}':
            for s in g['sections']:
                if s['id'] == 'talents':
                    return next((b['rows'] for k, b in s['blocks'] if k == 'table'), [])
    return []


def leveling(cid, spec, data):
    """The order of the 51 points by level 10-60 from the class leveling guide. The table's number is the rank the talent has after
    the row. Every step is checked against the tree: the rows must follow each other from level 10 to 60, the ranks must add up
    to the levels, each talent's row must be open (5 points per row spent in the tree) and its prerequisite at full rank. Any
    break -> None: a spec whose source order cannot be taken in this tree gets no tab rather than a wrong one."""
    if LEVEL_SPEC.get(cid) != spec:
        return None
    rows = _level_rows(cid)
    by = {t['id']: t for tr in data['trees'] for t in tr['talents']}
    rank, spent, steps, spans, level = {}, {}, [], {}, FIRST_LEVEL
    for r in rows:
        m = re.match(r'^(\d+)(?:–(\d+))?$', str(r[0]))
        if not m:
            return None
        a, b = int(m.group(1)), int(m.group(2) or m.group(1))
        tree, t = _find(data, r[1])
        if a != level or t is None:
            return None
        level = b + 1
        goal = int(str(r[2]).split('/')[0])
        add = goal - rank.get(t['id'], 0)
        if add != b - a + 1 or goal > t['m'] or spent.get(tree['key'], 0) < ROW_POINTS * (t['r'] - 1):
            return None
        if t.get('req') and rank.get(t['req'], 0) < by[t['req']]['m']:
            return None
        rank[t['id']] = goal
        spent[tree['key']] = spent.get(tree['key'], 0) + add
        steps.append((t, add, a, b))
        spans.setdefault(t['id'], []).append(_span(a, b))
    if level - 1 != LEVEL_CAP or not steps:
        return None
    trees = {t['id']: tr for tr in data['trees'] for t in tr['talents']}
    return {'picked': rank, 'steps': steps, 'spent': spent, 'at': {k: ', '.join(v) for k, v in spans.items()},
            'main': max(spent, key=spent.get), 'pk': 0, 'picks': [(trees[k], by[k], n) for k, n in rank.items()],
            'head': 'lvh', 'note': 'lvnote', 'guide': 'lvg'}


PROVIDERS = {'leveling': leveling}


def extra_builds(cid, spec, data):
    return [(bid, b) for bid in BUILD_IDS if PROVIDERS.get(bid) for b in [PROVIDERS[bid](cid, spec, data)] if b]


def sprite_v(cid):
    """?v=<hash> of the class sprite: assets are cached for days by Cloudflare and the browser (gabella_site_tech)."""
    import hashlib
    f = os.path.join(HERE, 'assets', 'talents', f'{cid}.webp')
    return '?v=' + hashlib.sha1(open(f, 'rb').read()).hexdigest()[:8] if os.path.isfile(f) else ''


def lv(a, b, lang):
    return UI['lv'][lang].format(a=f'{a}–{b}' if b > a else a)


def _span(a, b):
    return f'{a}–{b}' if b > a else str(a)


def _icon(t, letters):
    """The sprite cell of a talent (--i on the button), or two letters on a plate when the icon is not known legally yet."""
    return '<i class="tt-ic"></i>' if t.get('icon') is not None else f'<i class="tt-ic no">{escape(letters)}</i>'


_SMALL = {'and', 'the', 'of', 'for', 'with', 'und', 'der', 'die', 'das', 'des', 'von', 'et', 'de', 'la', 'le', 'du', 'les', 'del',
          'el', 'los', 'las', 'do', 'da', 'dos', 'das', 'di', 'il', 'della', 'dei', 'na', 'ze', 'и', 'в', 'на', 'со', 'та', 'із'}


def _letters(name):
    """Two letters of the name the reader sees: the initials of the first two words that carry meaning ("Voice of Truth" -> VT,
    "Глас правды" -> ГП), or the start of a single word ("Reverence" -> Re)."""
    w = re.findall(r'\w+', name)
    big = [x for x in w if x.lower() not in _SMALL and (len(x) > 2 or x[:1].isupper())] or w
    if not big:
        return '?'
    return (big[0][0] + big[1][0]).upper() if len(big) > 1 else big[0][:2].capitalize()


def _arrows(tree, picked, ends=False):
    """Lines from a prerequisite to its talent: straight down, straight across, or across then down (an elbow).
    --r/--c: the row and the leftmost column of the line, --n: how many rows or columns it spans (the CSS does the rest)."""
    by = {t['id']: t for t in tree['talents']}
    out = []
    for t in tree['talents']:
        src = by.get(t.get('req'))
        if not src:
            continue
        on = ' on' if t['id'] in picked and src['id'] in picked else ''
        e = f' data-s="{src["id"]}" data-d="{t["id"]}"' if ends else ''      # the script re-colours the line for another build
        r1, c1, r2, c2 = src['r'], src['c'], t['r'], t['c']
        if c1 == c2:                                               # down
            out.append(f'<i class="tt-ar v{on}"{e} style="--r:{r1};--c:{c1};--n:{r2 - r1}"></i>')
            continue
        side = 'r' if c2 > c1 else 'l'
        if r1 == r2:                                               # across
            out.append(f'<i class="tt-ar h {side}{on}"{e} style="--r:{r1};--c:{min(c1, c2)};--n:{abs(c2 - c1)}"></i>')
            continue
        out.append(f'<i class="tt-ar e {side}{on}"{e} style="--r:{r1};--c:{min(c1, c2)};--n:{abs(c2 - c1)}"></i>'
                   f'<i class="tt-ar v m{on}"{e} style="--r:{r1};--c:{c2};--n:{r2 - r1}"></i>')
    return ''.join(out)


def _l(x, lang):
    return x.get(lang) or x.get('en', '') if isinstance(x, dict) else x


PAGE = {}   # (class, lang) -> the talents of the page for the card, written once per page by page()


def _rib(steps, lang, pre='f'):
    """The order by level: one cell per step (a run of points the sources do not agree on is a «?» cell)."""
    rib = []
    for i, (t, n, a, b) in enumerate(steps):
        if t is None:
            rib.append(f'<li><span>{_span(a, b)}</span><button type="button" class="tt-t free" data-k="{pre}{i}" aria-label="{UI["free"][lang]}" title="{UI["free"][lang]}">'
                       f'<i class="tt-ic no">?</i></button><b>×{n}</b><em class="tt-fr">{UI["free"][lang]}</em></li>')
            continue
        name = tname(t, lang)
        ic = f' style="--i:{t["icon"]}"' if t.get('icon') is not None else ''
        rib.append(f'<li><span>{_span(a, b)}</span><button type="button" class="tt-t on"{ic} data-k="{t["id"]}" aria-label="{escape(name)}">'
                   f'{_icon(t, _letters(name))}</button><b>×{n}</b></li>')
    return f'<ol class="tt-rib">{"".join(rib)}</ol>'


def tree_titles(titles, lang):
    """{tree key: name}: the spec sections are titled «Защита: танк», the tree is the part before the colon."""
    return {k: _l(v, lang).split(':')[0].strip() for k, v in titles.items()}


def page_data(data, lang):
    """#ttData of a page. q / o / cap / f: the rules the editor checks, read from the same data file as the drawn tree (nothing
    about the layout is written into the script, so the client data that replaces the beta layout on 05.11 changes the editor with it)."""
    return {'u': {k: v[lang] for k, v in UI.items() if k not in JS_SKIP},
            't': {t['id']: [tname(t, lang), t['m'], t['r'], desc(t, lang)] for tr in data['trees'] for t in tr['talents']},
            'q': {t['id']: t['req'] for tr in data['trees'] for t in tr['talents'] if t.get('req')},
            'o': [[t['id'] for t in sorted(tr['talents'], key=lambda x: (x['r'], x['c']))] for tr in data['trees']],
            'cap': EDIT_CAP, 'f': FIRST_LEVEL, 'rp': ROW_POINTS}


def _trees(data, titles, picked, main, lang):
    """The tabs (narrow screens) and the three drawn trees with the points of `picked` {talent id: points}."""
    tabs, trees = [], []
    for tree in data['trees']:
        key = tree['key']
        n = sum(picked.get(t['id'], 0) for t in tree['talents'])  # our named points; the runs «your pick» are not counted
        on = key == main
        title = escape(titles.get(key, key))
        tabs.append(f'<button type="button" role="tab" class="tt-tab" data-t="{key}" aria-selected="{"true" if on else "false"}">'
                    f'{title}<span>{n}</span></button>')
        cells = []
        for t in tree['talents']:
            name = tname(t, lang)
            p = picked.get(t['id'], 0)
            ic = f';--i:{t["icon"]}' if t.get('icon') is not None else ''
            cells.append(f'<button type="button" class="tt-t{" on" if p else ""}" style="--r:{t["r"]};--c:{t["c"]}{ic}" data-k="{t["id"]}" '
                         f'aria-label="{escape(name)}{f" {p}/{t["m"]}" if p else ""}">{_icon(t, _letters(name))}{f"<b>{p}</b>" if p else ""}</button>')
        rows_n = max(t['r'] for t in tree['talents'])
        trees.append(f'<div class="tt-tree{" on" if on else ""}" data-t="{key}" role="group" aria-label="{title}">'
                     f'<h3>{title}<span{" class=on" if n else ""}>{n}</span></h3>'
                     f'<div class="tt-grid" style="--rows:{rows_n}">{_arrows(tree, picked, True)}{"".join(cells)}</div></div>')
    return f'<div class="tt-tabs" role="tablist">{"".join(tabs)}</div>', f'<div class="tt-trees">{"".join(trees)}</div>'


def render(cid, spec, rows, titles, lang, root):
    """The tree block of one spec section. rows: the spec's talent table rows [name cell, points, why],
    titles: {tree key: name, a t() dict}. '' when the class has no data yet. The card texts live in one JSON per page
    (page()), the block carries only its points: data-p = {talent id: [points, first level, last level, our line]}.
    When the spec has data for more builds (extra_builds), a switcher sits on top: the tree is drawn once for the general build and
    the script re-colours it for the chosen build from data-b = {build id: {p: points, m: main tree}}; each build has its own order
    by level in the page (hidden until chosen), so nothing needs the script but the switch itself."""
    data = load(cid)
    if not data:
        return ''
    pk = perk(data, [(r[0], r[1]) for r in rows])
    picked, steps, spent, _ = plan(data, [(r[0], r[1]) for r in rows], FIRST_LEVEL - pk)
    why = {}
    for r in rows:
        _, t = match(data, r[0])
        if t:
            why[t['id']] = _l(r[2], lang)
    titles = tree_titles(titles, lang)
    PAGE[(cid, lang)] = page_data(data, lang)
    pts = {}
    for i, (t, n, a, b) in enumerate(steps):
        pts[t['id'] if t else f'f{i}'] = [n, a, b, why.get(t['id'], '')] if t else [n, a, b]
    main = spec if spec in spent or not spent else max(spent, key=spent.get)
    extra = extra_builds(cid, spec, data)
    tabs_html, trees_html = _trees(data, titles, picked, main, lang)
    p_attr = escape(json.dumps(pts, ensure_ascii=False, separators=(',', ':')))
    pk_html = f' <span class="tt-pk">{UI["perk"][lang].format(n=pk)}</span>' if pk else ''
    basis = data.get('basis')                                     # before launch: one line over the tree says where it comes from
    note = f'<p class="tt-note">{UI[basis][lang]} · {day(data["date"], lang)}</p>' if basis in ('beta', 'classic') else ''
    code = build_code(data, table_picks(data, [(r[0], r[1]) for r in rows]))
    link = wh_link(wowhead(cid, data, [(r[0], r[1]) for r in rows], lang), lang)
    head = (f'<h3 class="tt-oh">{UI["order"][lang]}{"" if basis else " @@BETA@@"}'
            f'{pk_html}</h3>{_rib(steps, lang)}{go_button(root, cid, code, lang)}<p class="tt-whc">{link}</p>')
    box = (f'<div class="tt" data-c="{cid}" data-l="{lang}" data-sp="{spec}" data-w="{code}" data-wh="{escape(wh_base(cid, lang))}" '
           f'data-sh="{root}t/{cid}-" '
           f'data-p="{p_attr}"@@B@@ style="--n:{max(data.get("sprite", 0), 2)};--sp:url(@@ROOT@@assets/talents/{cid}.webp{sprite_v(cid)})">')
    hint = f'<div class="tt-card" aria-live="polite"><p class="tt-hint">{UI["hint"][lang]}</p></div>'
    # in a <template>: no dead buttons without the script, and search.py leaves the bar out of the page text
    ed = (f'<template class="tt-edt"><div class="tt-ed"><div class="tt-er"><button type="button" class="btn tt-sh">{UI["share"][lang]}</button>'
          f'<button type="button" class="tt-eb" aria-expanded="false" aria-controls="tt-ec-{spec}">{UI["ed"][lang]}</button></div>'
          f'<p class="tt-st" role="status"></p><div class="tt-ec" id="tt-ec-{spec}" hidden><p class="tt-cnt"><span class="tt-cn"></span><span class="tt-cm"> · {UI["cm"][lang]}</span><span class="tt-ct"> · {UI["cmt"][lang]}</span></p>'
          f'<div class="tt-md"><button type="button" class="tt-mb" data-m="1" aria-pressed="true">+ {UI["add"][lang]}</button>'
          f'<button type="button" class="tt-mb" data-m="-1" aria-pressed="false">− {UI["del"][lang]}</button></div>'
          f'<button type="button" class="tt-rs">{UI["reset"][lang]}</button>'
          f'<a class="tt-cl" href="{root}talents/{cid}/">{UI["calc"][lang]}</a>'
          f'{wh_link(wh_base(cid, lang) + "_t0", lang, "tt-whl")}'
          f'<p class="tt-eh"><span class="tt-cm">{UI["eh"][lang]}</span><span class="tt-ct">{UI["eht"][lang]}</span></p></div></div></template>')
    if not extra and LEVEL_SPEC.get(cid) == spec and _level_rows(cid):      # the leveling guide of the class has rows but they do not fit the tree
        note += f'<p class="tt-note">{UI["lvwait"][lang]} <a href="{root}guides/leveling-{cid}/#talents">{UI["lvg"][lang]}</a></p>'
    if not extra:
        return (f'{box.replace("@@B@@", "")}{note}{ed}{tabs_html}{trees_html}{hint}'
                f'<div class="tt-ow" data-b="general">{head}</div></div>')
    # the switcher: a tablist (arrows, Home/End), the anchor of a tab is <spec>-<build id>, e.g. #protection-leveling
    ids = [('general', {'main': main})] + extra
    sw, ows, bdata = [], [f'<div class="tt-ow" data-b="general">{head}</div>'], {}
    for bid, b in ids:
        on = bid == 'general'
        sw.append(f'<button type="button" role="tab" class="tt-b" id="{spec}-{bid}" data-b="{bid}" data-m="{b["main"]}" '
                  f'aria-selected="{"true" if on else "false"}" aria-controls="tt-{spec}"{"" if on else " tabindex=-1"}>{UI["b_" + bid][lang]}</button>')
        if on:
            continue
        bp = {k: [n, 0, 0, '', b['at'][k]] for k, n in b['picked'].items()}
        for i, (t, n, a, z) in enumerate(b['steps']):
            if t is None:
                bp[f'f{bid}{i}'] = [n, a, z]
        bdata[bid] = {'p': bp, 'm': b['main'], 'w': build_code(data, b['picks'])}
        wh = wowhead_ids(cid, data, b['picks'], lang, b['pk'])
        ows.append(f'<div class="tt-ow" data-b="{bid}" hidden><p class="tt-note">{UI[b["note"]][lang]}</p>'
                   f'<h3 class="tt-oh">{UI[b["head"]][lang]}</h3>{_rib(b["steps"], lang, "f" + bid)}'
                   f'{go_button(root, cid, bdata[bid]["w"], lang)}'
                   f'<p class="tt-ext"><a href="{root}guides/leveling-{cid}/#talents">{UI[b["guide"]][lang]}</a></p>'
                   f'<p class="tt-whc">{wh_link(wh, lang)}</p></div>')
    b_attr = escape(json.dumps(bdata, ensure_ascii=False, separators=(',', ':')))
    return (f'{box.replace("@@B@@", " data-b=" + chr(34) + b_attr + chr(34))}'
            f'<div class="tt-bs" role="tablist" aria-label="{UI["bs"][lang]}">{"".join(sw)}</div>{note}{ed}'
            f'<div class="tt-pane" id="tt-{spec}" role="tabpanel" aria-labelledby="{spec}-general">'
            f'{tabs_html}{trees_html}{hint}{"".join(ows)}</div></div>')


def render_calc(cid, specs, titles, lang, root):
    """The calculator page talents/<class>/: the same tree and editor as the guides, open from the start, no build of ours drawn.
    specs: [(spec id, talent table rows)] of guides/builds-<class>/ for the row «start from our build». The bar is in the page
    (not in a <template>), so the first frame already has it and nothing moves when the script comes; without the script it is
    hidden (page()). The build lives in the hash as #<code> and in the same localStorage draft as the guide's editor."""
    data = load(cid)
    if not data:
        return ''
    titles = tree_titles(titles, lang)
    PAGE[(cid, lang)] = page_data(data, lang)
    tabs_html, trees_html = _trees(data, titles, {}, data['trees'][0]['key'], lang)
    basis = data.get('basis')
    note = f'<p class="tt-note">{UI[basis][lang]} · {day(data["date"], lang)}</p>' if basis in ('beta', 'classic') else ''
    box = (f'<div class="tt calc ed" id="calc" data-c="{cid}" data-l="{lang}" data-sp="{cid}" data-calc="1" data-w="" '
           f'data-wh="{escape(wh_base(cid, lang))}" data-sh="{root}t/{cid}-" data-p="{{}}" style="--n:{max(data.get("sprite", 0), 2)};'
           f'--sp:url(@@ROOT@@assets/talents/{cid}.webp{sprite_v(cid)})">')
    ed = (f'<div class="tt-ed"><div class="tt-er"><button type="button" class="btn tt-sh">{UI["share"][lang]}</button>'
          f'<button type="button" class="tt-eb" hidden>{UI["ed"][lang]}</button></div><p class="tt-st" role="status"></p><div class="tt-ec">'
          f'<p class="tt-cnt"><span class="tt-cn">{UI["cnt"][lang].format(p=0, m=EDIT_CAP)}</span><span class="tt-cm"> · {UI["cm"][lang]}</span>'
          f'<span class="tt-ct"> · {UI["cmt"][lang]}</span></p>'
          f'<div class="tt-md"><button type="button" class="tt-mb" data-m="1" aria-pressed="true">+ {UI["add"][lang]}</button>'
          f'<button type="button" class="tt-mb" data-m="-1" aria-pressed="false">− {UI["del"][lang]}</button></div>'
          f'<button type="button" class="tt-rs">{UI["reset"][lang]}</button></div></div>')
    hint = f'<div class="tt-card" aria-live="polite"><p class="tt-hint">{UI["hint"][lang]}</p></div>'
    ours = []
    for spec, rows in specs:
        code = build_code(data, table_picks(data, [(r[0], r[1]) for r in rows]))
        if code:
            ours.append(f'<a href="#{code}" data-t="{spec}">{escape(titles.get(spec, spec))}</a>')
    row = f'<nav class="tt-ours" aria-label="{UI["ours"][lang]}"><span>{UI["ours"][lang]}</span>{"".join(ours)}</nav>' if ours else ''
    # the links and the data line under the tree, not over it: on a phone the tree starts on the first screen
    ext = f'<p class="tt-ext"><a href="{root}guides/builds-{cid}/">{UI["gd"][lang]}</a></p>'
    eh = f'<p class="tt-eh"><span class="tt-cm">{UI["eh"][lang]}</span><span class="tt-ct">{UI["eht"][lang]}</span></p>'
    wh = f'<p class="tt-whc">{wh_link(wh_base(cid, lang) + "_t0", lang, "tt-whl")}</p>'      # the last line of the block
    return f'{box}{ed}{tabs_html}{trees_html}{hint}{row}{ext}{eh}{note}{wh}</div>'


CSS = """/* Talent trees (talents.py): three trees in a row when there is room, else the spec's tree and tabs; icons from one sprite */
.tt { container-type: inline-size; display: grid; gap: 14px; margin: 4px 0 6px; }
.tt-tabs { display: none; gap: 4px; flex-wrap: wrap; }
.tt-tab { min-height: 44px; padding: 0 14px; border: 0; border-radius: 6px; background: transparent; color: var(--muted); cursor: pointer; font: inherit; font-weight: 600; }
.tt-tab span { margin-left: 8px; color: var(--muted); font-variant-numeric: tabular-nums; }
.tt-tab:hover { background: var(--zebra); }
.tt-tab[aria-selected="true"] { background: var(--seg-on); color: var(--gold-2); }
.tt-trees { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }
.tt-tree { --s: 44px; --g: 20px; --u: calc(var(--s) + var(--g)); padding: 12px 12px 18px; border-radius: 8px; background: var(--panel-2); min-width: 0; }
.tt-tree h3 { color: var(--fg); display: flex; justify-content: space-between; margin: 0 0 14px; font-family: var(--font-body); font-size: var(--fs-14); font-weight: 600; line-height: 1.3; letter-spacing: 0; }
.tt-tree h3 span { color: var(--muted); font-variant-numeric: tabular-nums; }
.tt-tree h3 span.on { color: var(--gold-2); }
.tt-grid { position: relative; display: grid; grid-template-columns: repeat(4, var(--s)); grid-template-rows: repeat(var(--rows), var(--s)); gap: var(--g); width: max-content; margin: 0 auto; }
.tt-t { position: relative; grid-row: var(--r); grid-column: var(--c); width: var(--s); height: var(--s); padding: 0; border: 1px solid var(--line-2); border-radius: 6px; background: #101114; cursor: pointer; }
.tt-ic { position: absolute; inset: 1px; border-radius: 4px; background: #16181c no-repeat 0 0 / calc(var(--n) * 100%) 100%; background-position-x: calc(var(--i) / (var(--n) - 1) * 100%); }
.tt.ld .tt-ic:not(.no) { background-image: var(--sp); }
.tt-ic.no { display: grid; place-items: center; font: 600 12px/1 var(--serif, Georgia), serif; letter-spacing: .04em; color: #c9bfa8; font-style: normal;
  background: radial-gradient(circle at 50% 35%, #2b2d33, #15171b 75%); box-shadow: inset 0 0 0 1px rgba(201, 168, 92, .28), inset 0 0 8px rgba(0, 0, 0, .6); }
.tt-t:not(.on) { border-color: var(--line); }
.tt-t:not(.on) .tt-ic { filter: grayscale(1) brightness(.62); }
.tt-t.on { border-color: var(--gold); }
.tt-t.free { border-style: dashed; border-color: var(--line-2); }
.tt-t.free .tt-ic { filter: none; opacity: 1; }
.tt-t b { position: absolute; right: -7px; bottom: -7px; min-width: 16px; padding: 1px 3px; border: 1px solid var(--gold); border-radius: 4px; background: var(--bg); color: var(--gold-2); font: 600 11px/1.2 system-ui, sans-serif; font-variant-numeric: tabular-nums; }
.tt-t[aria-pressed="true"] { outline: 2px solid var(--fg); outline-offset: 2px; }
.tt-t:focus-visible { outline: 2px solid var(--gold-2); outline-offset: 2px; }
.tt-ar { position: absolute; background: var(--line-2); color: var(--line-2); }
.tt-ar.v { width: 2px; left: calc((var(--c) - 1) * var(--u) + var(--s) / 2 - 1px); top: calc((var(--r) - 1) * var(--u) + var(--s)); height: calc(var(--n) * var(--u) - var(--s)); }
.tt-ar.v.m { top: calc((var(--r) - 1) * var(--u) + var(--s) / 2); height: calc(var(--n) * var(--u) - var(--s) / 2); }
.tt-ar.h, .tt-ar.e { height: 2px; top: calc((var(--r) - 1) * var(--u) + var(--s) / 2 - 1px); }
.tt-ar.h { left: calc((var(--c) - 1) * var(--u) + var(--s)); width: calc(var(--n) * var(--u) - var(--s)); }
.tt-ar.e.r { left: calc((var(--c) - 1) * var(--u) + var(--s)); width: calc(var(--n) * var(--u) - var(--s) / 2 + 1px); }
.tt-ar.e.l { left: calc((var(--c) - 1) * var(--u) + var(--s) / 2 - 1px); width: calc(var(--n) * var(--u) - var(--s) / 2 + 1px); }
.tt-ar.on { background: var(--gold); color: var(--gold); }
.tt-ar.v::after { content: ""; position: absolute; left: -3px; bottom: -1px; border: 4px solid transparent; border-bottom: 0; border-top: 5px solid currentColor; }
.tt-ar.h.r::after { content: ""; position: absolute; right: -1px; top: -3px; border: 4px solid transparent; border-right: 0; border-left: 5px solid currentColor; }
.tt-ar.h.l::after { content: ""; position: absolute; left: -1px; top: -3px; border: 4px solid transparent; border-left: 0; border-right: 5px solid currentColor; }
.tt-note { margin: 0; color: var(--muted); font-size: var(--fs-13); }
.tt-pk { color: var(--muted); font-size: var(--fs-13); font-weight: 400; }
.tt-ext { display: flex; flex-wrap: wrap; gap: 4px 18px; margin: 0; font-size: var(--fs-14); }
.tt-go { margin: 0; }
.tt-go .btn { min-height: 48px; padding: 0 22px; font-size: var(--fs-16); white-space: normal; text-align: center; }
.tt-whc { margin: 0; font-size: var(--fs-13); }
.tt-whc a { color: var(--muted); }
.tt-whc a:hover { color: var(--fg); }
.tt-bs { display: flex; flex-wrap: wrap; gap: 4px; width: fit-content; max-width: 100%; padding: 4px; border: 1px solid var(--line); border-radius: 8px; }
.tt-b { min-height: 44px; padding: 0 16px; border: 0; border-radius: 6px; background: transparent; color: var(--muted); cursor: pointer; font: inherit; font-weight: 600; }
.tt-b:hover { background: var(--zebra); }
.tt-b[aria-selected="true"] { background: var(--seg-on); color: var(--gold-2); }
.tt-b:focus-visible { outline: 2px solid var(--gold-2); outline-offset: 2px; }
.tt-pane, .tt-ow { display: grid; gap: 14px; min-width: 0; }
.tt-ow[hidden] { display: none; }
.tt-ow .tt-oh { margin-top: 0; }
.tt-card { min-height: 48px; padding: 12px 14px; border: 1px solid var(--line); border-radius: 8px; }
.tt-card .h { display: block; margin: 0 0 2px; font-family: var(--font-body); font-size: var(--fs-16); font-weight: 600; line-height: 1.3; letter-spacing: 0; color: var(--fg); }
.tt-card .m { margin: 0 0 6px; font-size: var(--fs-13); color: var(--gold-2); }
.tt-card p { margin: 0; color: var(--fg); font-size: var(--fs-14); }
.tt-card .tt-hint { color: var(--muted); }
.tt-oh { margin: 6px 0 0; font-family: var(--font-body); font-size: var(--fs-14); font-weight: 600; line-height: 1.3; letter-spacing: 0; color: var(--fg); }
.tt-rib { display: flex; flex-wrap: wrap; align-items: flex-start; gap: 12px 18px; margin: 0; padding: 0; list-style: none; }
.tt-rib li { display: grid; grid-template-columns: auto auto; grid-template-rows: auto auto; column-gap: 6px; align-items: center; }
.tt-rib span { grid-column: 1 / -1; font-size: var(--fs-13); color: var(--gold-2); font-variant-numeric: tabular-nums; white-space: nowrap; }
.tt-rib .tt-t { --s: 36px; }
.tt-rib .tt-t::after { content: ""; position: absolute; inset: -4px; }   /* 44 x 44 to tap, the icon stays 36 px; the ribbon gaps are 12/18 px, no zone overlaps another (X6-05) */
.tt-rib .tt-fr { grid-column: 1 / -1; font-size: var(--fs-13); font-style: normal; color: var(--muted); white-space: nowrap; }
.tt-rib b { font-family: var(--font-body); font-size: var(--fs-14); font-weight: 600; line-height: 1; letter-spacing: 0; color: var(--muted); font-variant-numeric: tabular-nums; }
.tt-ed[hidden], .tt-ec[hidden], .tt.ed .tt-bs, .tt.ed .tt-ow { display: none; }
.tt-ed { display: grid; gap: 10px; }
.tt-ec { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 12px; }
.tt-er { display: flex; flex-wrap: wrap; gap: 8px 12px; }
.tt .tt-sh { min-height: 48px; padding: 0 22px; font: inherit; font-size: var(--fs-16); font-weight: 600; cursor: pointer; }
.tt .tt-sh:focus-visible { outline: 2px solid var(--gold-2); outline-offset: 2px; }
.tt-eb, .tt-mb, .tt-rs { min-height: 44px; padding: 0 16px; border: 1px solid var(--line-2); border-radius: 6px; background: transparent; color: var(--fg); cursor: pointer; font: inherit; font-weight: 600; }
.tt-eb { min-height: 48px; border-color: var(--gold); color: var(--gold-2); }
.tt-eb:hover, .tt-mb:hover, .tt-rs:hover { background: var(--zebra); }
.tt-eb:focus-visible, .tt-mb:focus-visible, .tt-rs:focus-visible { outline: 2px solid var(--gold-2); outline-offset: 2px; }
.tt .tt-cnt { flex-basis: 100%; max-width: none; margin: 0; color: var(--fg); font-weight: 600; font-variant-numeric: tabular-nums; }
.tt-ct { display: none; }
@media (pointer: coarse) { .tt-cm { display: none; } .tt-ct { display: inline; } }
.tt-cm, .tt-ct { color: var(--muted); font-weight: 400; }
.tt-md { display: flex; gap: 4px; padding: 4px; border: 1px solid var(--line); border-radius: 8px; }
.tt-md .tt-mb { border: 0; color: var(--muted); }
.tt-md .tt-mb[aria-pressed="true"] { background: var(--seg-on); color: var(--gold-2); }
.tt-cl { font-size: var(--fs-14); }
.tt-whl { font-size: var(--fs-13); color: var(--muted); }
.tt-eb[hidden] { display: none; }
/* The calculator page (render_calc): our builds of the class as a row of plain buttons under the tree, the spec guide at the end */
.tt-ours { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 10px; margin: 0; }
.tt-ours span { flex-basis: 100%; color: var(--muted); font-size: var(--fs-13); }
.tt-ours a[data-t] { display: inline-flex; align-items: center; min-height: 44px; padding: 0 16px; border: 1px solid var(--line-2); border-radius: 6px; color: var(--fg); font-weight: 600; text-decoration: none; }
.tt-ours a[data-t]:hover { border-color: var(--gold); }
.tt-ours a:focus-visible { outline: 2px solid var(--gold-2); outline-offset: 2px; }
.tt.calc > .tt-eh { max-width: 72ch; margin: 0; color: var(--muted); font-size: var(--fs-13); }
.tt-st:empty { display: none; }
.tt .tt-st, .tt .tt-eh { flex-basis: 100%; max-width: none; margin: 0; color: var(--muted); font-size: var(--fs-13); }
.tt.ed .tt-grid .tt-t.tt-op:not(.on) { border-color: var(--line-2); }
.tt.ed .tt-grid .tt-t.tt-op:not(.on) .tt-ic { filter: none; }
.tt.ed .tt-grid .tt-t { -webkit-touch-callout: none; user-select: none; touch-action: manipulation; }
.tt-card .e { color: var(--muted); }
@media (prefers-reduced-motion: no-preference) { .tt.ed .tt-t { transition: border-color .12s; } }
@container (max-width: 759px) {
  .tt-er > * { flex: 1 1 100%; }
  .tt-go .btn { width: 100%; }
  .tt-tabs { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .tt-tab { padding: 4px 2px; font-size: min(var(--fs-14), 3.5vw); line-height: 1.2; hyphens: auto; overflow-wrap: anywhere; }
  .tt-tab span { display: block; margin: 2px 0 0; white-space: nowrap; }
  .tt-trees { grid-template-columns: minmax(0, 1fr); }
  .tt-tree:not(.on) { display: none; }
  .tt-tree { --s: 44px; --g: min(26px, calc((100cqi - 24px - 4 * var(--s)) / 3)); }
  .tt-tree h3 { display: none; }
}
"""

JS = r"""<script>
/* Talent trees: the card under the tree on tap (and on hover with a mouse), the tabs on narrow screens, the sprite near the screen,
   and the editor (your own build over the same tree). #ttData: {u: texts, t: {id: [name, ranks, row, client text]},
   q: {id: prerequisite id}, o: [[ids of a tree in row/column order]], cap, f: first talent level, rp: points per row};
   a block's data-p: {id: [points, from, to, our line]}. The editor keeps the build as #<spec>/<code> and in localStorage. */
(function () {
  var D = JSON.parse(document.getElementById('ttData').textContent), U = D.u, KEY = 'gabella-tc-';
  var hover = window.matchMedia && matchMedia('(hover: hover)').matches;
  function hashCode() {                          /* the build code of the address (#<code> or #<spec>/<code>), else null */
    var h = ''; try { h = decodeURIComponent(location.hash.slice(1)); } catch (x) {}
    var m = /^(?:[a-z-]+\/)?([0-9-]+)$/.exec(h);
    return m ? m[1] : null;
  }
  var trOf = {};
  D.o.forEach(function (ids, i) { ids.forEach(function (k) { trOf[k] = i; }); });
  function f(s, o) { return s.replace(/\{(\w)\}/g, function (_, k) { return o[k]; }); }
  function lv(a, b) { return f(U.lv, { a: b > a ? a + '–' + b : a }); }
  /* The rules of the tree, all read from #ttData: a talent opens with rp points per row spent in the rows above it in its tree,
     its prerequisite must be at full rank, cap points in all. S: {id: points}. */
  function above(S, i, row) { var n = 0; D.o[i].forEach(function (k) { if (D.t[k][2] < row) n += S[k] || 0; }); return n; }
  function total(S) { var n = 0; for (var k in S) n += S[k]; return n; }
  function why(S, k) {
    var t = D.t[k], q = D.q[k];
    if ((S[k] || 0) >= t[1]) return 'max';
    if (total(S) >= D.cap) return f(U.e_cap, { m: D.cap });
    if (above(S, trOf[k], t[2]) < D.rp * (t[2] - 1)) return f(U.e_row, { n: D.rp * (t[2] - 1) });
    if (q && (S[q] || 0) < D.t[q][1]) return f(U.e_req, { t: D.t[q][0] });
    return '';
  }
  function legal(S, i) {
    return D.o[i].every(function (k) {
      var q = D.q[k];
      return !S[k] || (above(S, i, D.t[k][2]) >= D.rp * (D.t[k][2] - 1) && (!q || (S[q] || 0) >= D.t[q][1]));
    });
  }
  function encode(S) {
    var c = D.o.map(function (ids) { return ids.map(function (k) { return S[k] || 0; }).join('').replace(/0+$/, ''); });
    while (c.length && !c[c.length - 1]) c.pop();
    return c.join('-');
  }
  function decode(code) {
    var S = {}, want = {};
    String(code || '').split('-').forEach(function (s, i) {
      if (D.o[i]) s.split('').forEach(function (d, j) { var k = D.o[i][j]; if (k && +d) want[k] = Math.min(+d, D.t[k][1]); });
    });
    for (var pass = 0; pass < 2; pass++) {             /* a prerequisite may stand to the right in the same row */
      D.o.forEach(function (ids) { ids.forEach(function (k) { while ((S[k] || 0) < (want[k] || 0) && !why(S, k)) S[k] = (S[k] || 0) + 1; }); });
    }
    return S;
  }
  document.querySelectorAll('.tt').forEach(function (w) {
    var card = w.querySelector('.tt-card'), P0 = JSON.parse(w.dataset.p), P = P0, cur = null, hint = card.innerHTML;
    var B = w.dataset.b ? JSON.parse(w.dataset.b) : null, bs = w.querySelector('.tt-bs');
    var tp = w.querySelector('.tt-edt'), S = null, mode = 1, calc = !!w.dataset.calc;
    if (tp) tp.parentNode.replaceChild(tp.content.cloneNode(true), tp);   /* the calculator page has the bar in the page already */
    var ed = w.querySelector('.tt-ed');
    function line(cls, text) { var e = document.createElement(cls === 'h' ? 'b' : 'p'); e.className = cls; e.textContent = text; card.appendChild(e); }
    function show(b) {
      var k = b.dataset.k, p = P[k], t = D.t[k], meta = [];
      if (cur) cur.removeAttribute('aria-pressed');
      cur = b; b.setAttribute('aria-pressed', 'true');
      card.textContent = '';
      if (!t) { line('h', U.free); line('m', lv(p[1], p[2])); line('w', U.free_d); return; }
      if (S) meta.push(f(U.rank, { p: S[k] || 0, m: t[1] }));
      else {
        meta.push(p ? f(U.take, { p: p[0], m: t[1] }) : f(U.skip, { m: t[1] }));
        if (p) meta.push(p[4] ? f(U.lv, { a: p[4] }) : lv(p[1], p[2]));
      }
      if (t[2] > 1) meta.push(f(U.row, { n: D.rp * (t[2] - 1) }));
      line('h', t[0]); line('m', meta.join(' · '));
      var w2 = S ? t[3] : (p && p[3]) || t[3];
      if (w2) line('w', w2);
    }
    function pickTree(key) {
      w.querySelectorAll('.tt-tab').forEach(function (x) { x.setAttribute('aria-selected', x.dataset.t === key ? 'true' : 'false'); });
      w.querySelectorAll('.tt-tree').forEach(function (x) { x.classList.toggle('on', x.dataset.t === key); });
    }
    /* Colour the one drawn tree for a set of points (a build of ours or the editor's): points, golden lines, counts */
    function paint() {
      var sum = {};
      Object.keys(P).forEach(function (k) { if (D.t[k]) { var tr = k.replace(/-\d+$/, ''); sum[tr] = (sum[tr] || 0) + P[k][0]; } });
      w.querySelectorAll('.tt-grid [data-k]').forEach(function (b) {
        var k = b.dataset.k, n = P[k] ? P[k][0] : 0, nb = b.querySelector('b');
        b.classList.toggle('on', n > 0);
        b.setAttribute('aria-label', D.t[k][0] + (S ? ' ' + n + '/' + D.t[k][1] : n ? ' ' + n + '/' + D.t[k][1] : ''));
        if (n && !nb) { nb = document.createElement('b'); b.appendChild(nb); }
        if (nb) { if (n) nb.textContent = n; else nb.remove(); }
        b.classList.toggle('tt-op', !!S && !why(S, k));
      });
      w.querySelectorAll('.tt-ar').forEach(function (a) { a.classList.toggle('on', !!(P[a.dataset.s] && P[a.dataset.d])); });
      w.querySelectorAll('.tt-tab').forEach(function (x) { x.querySelector('span').textContent = sum[x.dataset.t] || 0; });
      w.querySelectorAll('.tt-tree h3 span').forEach(function (x) {
        var n = sum[x.parentNode.parentNode.dataset.t] || 0; x.textContent = n; x.classList.toggle('on', n > 0);
      });
    }
    /* Build switcher: re-colour the tree for the chosen build of ours, show that build's order */
    function setBuild(id, focus) {
      var tab = bs.querySelector('[data-b="' + id + '"]');
      if (!tab) return;
      P = id === 'general' ? P0 : B[id].p;
      paint();
      pickTree(tab.dataset.m);
      bs.querySelectorAll('.tt-b').forEach(function (x) {
        var on = x === tab; x.setAttribute('aria-selected', on ? 'true' : 'false'); x.tabIndex = on ? 0 : -1;
      });
      w.querySelector('.tt-pane').setAttribute('aria-labelledby', tab.id);
      w.querySelectorAll('.tt-ow').forEach(function (x) { x.hidden = x.dataset.b !== id; });
      cur = null; card.innerHTML = hint;
      if (focus) tab.focus();
    }
    if (bs) {
      var tabs = [].slice.call(bs.querySelectorAll('.tt-b'));
      var go = function (t, focus) {
        setBuild(t.dataset.b, focus);
        try { history.replaceState(null, '', t.dataset.b === 'general' ? '#' + t.id.replace(/-general$/, '') : '#' + t.id); } catch (x) {}
      };
      bs.addEventListener('click', function (e) { var t = e.target.closest('.tt-b'); if (t) go(t); });
      bs.addEventListener('keydown', function (e) {
        var i = tabs.indexOf(document.activeElement), j = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? i + 1
          : e.key === 'ArrowLeft' || e.key === 'ArrowUp' ? i - 1 : e.key === 'Home' ? 0 : e.key === 'End' ? tabs.length - 1 : -1;
        if (i < 0 || j < 0) return;
        e.preventDefault();
        go(tabs[(j + tabs.length) % tabs.length], true);
      });
      w.setBuildByHash = function (h) {
        var t = tabs.filter(function (x) { return x.id === h || x.id === h + '-general'; })[0];
        if (t && t.getAttribute('aria-selected') !== 'true') setBuild(t.dataset.b);
      };
    }
    /* Editor: starts from the build saved in this browser, else from the build of ours on screen */
    var eb = ed.querySelector('.tt-eb'), ec = ed.querySelector('.tt-ec'), cnt = ed.querySelector('.tt-cn');
    var st = ed.querySelector('.tt-st'), whl = w.querySelector('.tt-whl'), cl = ed.querySelector('.tt-cl');
    function saved() { try { return localStorage.getItem(KEY + w.dataset.c); } catch (x) { return null; } }
    /* the address of a build: #<spec>/<code> in a guide, #<code> on the calculator page (nothing for an empty build) */
    function addr(code) { return calc ? (code ? '#' + code : location.pathname + location.search) : '#' + w.dataset.sp + '/' + code; }
    function update(keep) {
      var n = total(S), code = encode(S);
      st.textContent = '';
      P = {};
      for (var k in S) if (S[k]) P[k] = [S[k]];
      paint();
      cnt.textContent = f(U.cnt, { p: n, m: D.cap }) + (n ? ' · ' + f(U.lv, { a: D.f - 1 + n }) : '');
      whl.href = w.dataset.wh + code + '_t0';
      if (cl) cl.href = cl.href.split('#')[0] + (code ? '#' + code : '');
      if (!keep) try { localStorage.setItem(KEY + w.dataset.c, code); } catch (x) {}
      try { history.replaceState(null, '', addr(code)); } catch (x) {}
    }
    function open(code) {
      S = decode(code);
      w.classList.add('ed'); ec.hidden = false; eb.textContent = U.ed_x; eb.setAttribute('aria-expanded', 'true');
      cur = null; card.innerHTML = hint;
      update(true);
    }
    function close() {
      S = null;
      w.classList.remove('ed'); ec.hidden = true; eb.textContent = U.ed; eb.setAttribute('aria-expanded', 'false');
      var t = bs && bs.querySelector('.tt-b[aria-selected="true"]');
      if (t) setBuild(t.dataset.b); else { P = P0; paint(); cur = null; card.innerHTML = hint; }
      try { history.replaceState(null, '', '#' + w.dataset.sp); } catch (x) {}
    }
    function step(b, d) {
      var k = b.dataset.k, r = '';
      if (d > 0) { r = why(S, k); if (!r) S[k] = (S[k] || 0) + 1; }
      else if (S[k]) { S[k]--; if (!legal(S, trOf[k])) { S[k]++; r = U.e_keep; } }
      if (!r) update();
      show(b);
      if (r && r !== 'max') line('e', r);
    }
    eb.addEventListener('click', function () {
      if (S) { close(); return; }
      var t = bs && bs.querySelector('.tt-b[aria-selected="true"]'), s = saved();
      open(s !== null ? s : t && t.dataset.b !== 'general' ? B[t.dataset.b].w : w.dataset.w);
    });
    ec.addEventListener('click', function (e) {
      var m = e.target.closest('.tt-mb');
      if (m) {
        mode = +m.dataset.m;
        ec.querySelectorAll('.tt-mb').forEach(function (x) { x.setAttribute('aria-pressed', x === m ? 'true' : 'false'); });
      } else if (e.target.closest('.tt-rs')) { S = {}; update(); cur = null; card.innerHTML = hint; }
    });
    /* the spec a build belongs to: the guide's section, on the calculator page the tree with most points */
    function specOf(code) {
      if (!calc) return w.dataset.sp;
      var P2 = decode(code), best = 0, at = -1;
      D.o.forEach(function (ids, i) { var n = 0; ids.forEach(function (k) { n += P2[k] || 0; }); if (n > best) { best = n; at = i; } });
      return at < 0 ? '' : w.querySelectorAll('.tt-tree')[at].dataset.t;
    }
    /* «Copy build link»: the build on screen (yours in the editor, else the build of ours chosen above the tree) as the share page
       t/<class>-<spec>/#<code>: a chat shows the class and spec in its card, a visitor lands in the calculator on the same build.
       An empty build keeps the page's own address; not location.href: replaceState can be throttled */
    ed.querySelector('.tt-sh').addEventListener('click', function () {
      var t = bs && bs.querySelector('.tt-b[aria-selected="true"]');
      var code = S ? encode(S) : t && t.dataset.b !== 'general' ? B[t.dataset.b].w : w.dataset.w;
      var sp = code && w.dataset.sh ? specOf(code) : '';
      var url = sp ? new URL(w.dataset.sh + sp + '/#' + code, location.href).href
        : location.href.split('#')[0] + (calc ? (code ? '#' + code : '') : '#' + w.dataset.sp + '/' + code);
      var ok = function () { st.textContent = U.copied; };
      var no = function () {                         /* old browsers and http: a hidden field and the copy command */
        var a = document.createElement('textarea'), done = false;
        a.value = url; a.setAttribute('readonly', ''); a.style.cssText = 'position:fixed;top:0;left:0;opacity:0';
        document.body.appendChild(a); a.select();
        try { done = document.execCommand('copy'); } catch (x) {}
        a.remove();
        if (done) ok(); else { st.textContent = U.nocopy; try { history.replaceState(null, '', url.slice(url.indexOf('#')) || location.pathname); } catch (x) {} }
      };
      try { navigator.clipboard.writeText(url).then(ok, no); } catch (x) { no(); }
    });
    w.openByHash = function (code) { if (S) { S = decode(code); update(true); } else open(code); };
    w.pickTree = pickTree;
    if (calc) {                        /* the calculator opens at once: a build from the address, else this browser's draft, else empty */
      var hc = hashCode(), sv = saved();
      open(hc !== null ? hc : sv !== null ? sv : '');
      var best = 0, at = 0;                  /* phones show one tree: the one with most points */
      D.o.forEach(function (ids, i) { var n = 0; ids.forEach(function (k) { n += S[k] || 0; }); if (n > best) { best = n; at = i; } });
      if (best) pickTree(w.querySelectorAll('.tt-tree')[at].dataset.t);
    }
    /* Touch has no right button: a long press on a talent takes the point back */
    var lpT = 0, lpDone = 0;
    w.addEventListener('pointerdown', function (e) {
      var b = S && e.pointerType !== 'mouse' && e.target.closest('.tt-grid [data-k]');
      clearTimeout(lpT);
      if (b) lpT = setTimeout(function () { lpDone = Date.now(); step(b, -1); }, 500);
    });
    ['pointerup', 'pointercancel', 'pointermove'].forEach(function (n) { w.addEventListener(n, function () { clearTimeout(lpT); }); });
    w.addEventListener('click', function (e) {
      if (Date.now() - lpDone < 700) return;
      var tab = e.target.closest('.tt-tab');
      if (tab) { pickTree(tab.dataset.t); return; }
      var our = e.target.closest('.tt-ours [data-t]');      /* «start from our build»: the hash opens it, the phone shows its tree */
      if (our) { pickTree(our.dataset.t); return; }
      var b = e.target.closest('[data-k]');
      if (b && S && b.closest('.tt-grid')) step(b, mode);
      else if (b) show(b);
    });
    w.addEventListener('contextmenu', function (e) {
      var b = S && e.target.closest('.tt-grid [data-k]');
      if (b) { e.preventDefault(); if (Date.now() - lpDone > 700) step(b, -1); }
    });
    w.addEventListener('keydown', function (e) {
      var b = S && e.target.closest && e.target.closest('.tt-grid [data-k]');
      if (!b) return;
      if (e.key === 'Delete' || e.key === 'Backspace' || e.key === '-') { e.preventDefault(); step(b, -1); }
      else if (e.key === '+' || e.key === '=') { e.preventDefault(); step(b, 1); }
    });
    if (hover) w.addEventListener('mouseover', function (e) { var b = e.target.closest('[data-k]'); if (b && b !== cur) show(b); });
  });
  function fromHash(e) {
    var h = ''; try { h = decodeURIComponent(location.hash.slice(1)); } catch (x) {}
    var m = /^([a-z-]+)\/([0-9-]*)$/.exec(h);
    document.querySelectorAll('.tt').forEach(function (w) {
      if (w.dataset.calc) {                     /* the calculator page: #<code>, or a guide's #<spec>/<code> */
        var c = hashCode();
        if (e && c !== null) { w.openByHash(c); w.scrollIntoView(); }
        return;
      }
      if (!m) { if (w.setBuildByHash) w.setBuildByHash(h); return; }
      if (w.dataset.sp !== m[1] || !w.openByHash) return;
      w.openByHash(m[2]);
      (document.getElementById(m[1]) || w).scrollIntoView();
    });
  }
  fromHash();
  window.addEventListener('hashchange', fromHash);
  /* The sprite: near the screen, and only after the first frame is painted (on the calculator page the tree is on the first
     screen: the picture of icons must not hold back the first paint of the heading) */
  var all = document.querySelectorAll('.tt');
  function wake() {
    if (!('IntersectionObserver' in window)) { all.forEach(function (w) { w.classList.add('ld'); }); return; }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('ld'); io.unobserve(e.target); } });
    }, { rootMargin: '300px 0px' });
    all.forEach(function (w) { io.observe(w); });
  }
  var woke = false;
  function go() { if (!woke) { woke = true; wake(); } }
  /* the browser reports a paint once the frame is on the screen; a tab in the background paints nothing: a timer then */
  var PO = window.PerformanceObserver, types = PO && PO.supportedEntryTypes || [];
  if (types.indexOf('paint') >= 0) new PO(function () { setTimeout(go, 0); }).observe({ type: 'paint', buffered: true });
  else addEventListener('load', function () { requestAnimationFrame(function () { setTimeout(go, 0); }); }, { once: true });
  setTimeout(go, 3000);
})();
</script>
"""


def page(html):
    """Adds the styles, the talents of the page (card texts) and the script once to a built page that has a tree."""
    m = re.search(r'<div class="tt(?: [a-z ]+)?"(?: id="\w+")? data-c="([a-z]+)" data-l="([a-z]+)"', html)
    if not m:
        return html
    data = json.dumps(PAGE[(m.group(1), m.group(2))], ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    html = html.replace('</style>', CSS + '</style>', 1)
    html = html.replace('</head>', '<noscript><style>.tt .tt-ic:not(.no){background-image:var(--sp)}.tt-bs,.tt.calc .tt-ed,.tt.calc .tt-ours{display:none}</style></noscript></head>', 1)
    return html.replace('</body>', f'<script type="application/json" id="ttData">{data}</script>\n' + JS + '</body>', 1)
