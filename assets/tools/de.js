const CLASSES = [
  { id:'warrior', n:'Krieger', s:'Krieger', roles:['tank','dps'],
    specs:[['Waffen','Nahkampfschaden (Zweihandwaffe)',['dps']],['Furor','Nahkampfschaden (zwei Waffen)',['dps']],['Schutz','Tank',['tank']]],
    lvl:'Langsamstes Leveln, etwa 12 % länger als der Durchschnitt (Schätzung von LFCarry)',
    lp:12,
    raid:'Schlachtruf wirkt auf den ganzen Raid',
    forever:'Mehr Wut, bessere Bedrohung gegen mehrere Ziele, das Talent Weapon Master. Furor und Blutdurst wurden abgeschwächt.' },
  { id:'paladin', n:'Paladin', roles:['tank','heal','dps'],
    specs:[['Heilig','Heiler',['heal']],['Schutz','Tank',['tank']],['Vergeltung','Nahkampfschaden',['dps']]],
    lvl:'Durchschnittliches Leveltempo',
    lp:0,
    raid:'Segen der Könige ist jetzt Grundfähigkeit. Laut Beta-Listen gehört Schutz zu den stärksten Tanks, Vergeltung ist nach dem Patch vom 15. Oktober abgerutscht.',
    forever:'Heiliger Stoß ab Stufe 6, Richturteil verbraucht das Siegel nicht. Untote können jetzt Paladine sein, so kam die Klasse zur Horde.' },
  { id:'hunter', n:'Jäger', roles:['dps'],
    specs:[['Tierherrschaft','Fernkampfschaden, viel Schaden vom Begleiter',['dps']],['Treffsicherheit','Fernkampfschaden',['dps']],['Überleben','Nah- und Fernkampf, Fallen',['dps']]],
    lvl:'Schnellstes Leveln, etwa 8 % schneller als der Durchschnitt (Schätzung von LFCarry)',
    lp:-8,
    raid:'Aura des Volltreffers wirkt auf den ganzen Raid',
    forever:'Du kannst ohne Begleiter spielen, Fallen funktionieren im Kampf, Füchse sind als Begleiterfamilie dazugekommen. Überleben kann in den Nahkampf gehen.' },
  { id:'rogue', n:'Schurke', roles:['dps'],
    specs:[['Meucheln','Giftschaden',['dps']],['Kampf','Schnelle Waffenangriffe',['dps']],['Täuschung','Hinterhalte, Blutungen',['dps']]],
    lvl:'Durchschnittliches Leveltempo',
    lp:0,
    raid:'Reiner Nahkampfschaden ohne raidweite Buffs',
    forever:'Einhandäxte sind jetzt nutzbar. Meucheln baut auf Gifte, Täuschung auf Blutungen und Verstohlenheit.' },
  { id:'priest', n:'Priester', roles:['heal','dps'],
    specs:[['Disziplin','Heiler, Schilde und Absorption',['heal']],['Heilig','Heiler',['heal']],['Schatten','Fernkampfschaden',['dps']]],
    lvl:'Etwa 5 % langsamer als der Durchschnitt (Schätzung von LFCarry)',
    lp:5,
    raid:'Göttlicher Willen ist jetzt Grundfähigkeit. Schattenschaden und Verschlingende Seuche (24 Sek. Abklingzeit) wurden mit dem Patch vom 15. Oktober verstärkt.',
    forever:'Furchtzauberschutz und Verschlingende Seuche sind ab Stufe 20 für jedes Volk verfügbar. Jedes Volk hat zwei eigene Priesterzauber.' },
  { id:'shaman', n:'Schamane', roles:['heal','dps','tank?'],
    specs:[['Elementar','Fernkampfschaden',['dps']],['Verstärkung','Nahkampfschaden. Ob er tanken kann, ist noch offen',['dps','tank?']],['Wiederherstellung','Heiler',['heal']]],
    lvl:'Durchschnittliches Leveltempo',
    lp:0,
    raid:'Die Totems Erdstärke, Windzorn, Flammenzunge und Anmut der Luft buffen die eigene Gruppe',
    forever:'Zwerge können jetzt Schamanen sein, so kam die Klasse zur Allianz. Lavaexplosion wurde verstärkt, Elementar ist in den Schadensranglisten gestiegen.' },
  { id:'mage', n:'Magier', roles:['dps'],
    specs:[['Arkan','Burst, viel Mana',['dps']],['Feuer','Krits und Entzünden',['dps']],['Frost','Schaden und Kontrolle',['dps']]],
    lvl:'Schnellstes Leveln, etwa 8 % schneller als der Durchschnitt, rund 12 Stunden gespart (Schätzung von LFCarry)',
    lp:-8,
    raid:'Portale, Essen und Wasser für die Gruppe',
    forever:'Feuer bekam Kampfeshitze, Arkan den Arkanschlag, Frost die Eislanze. Frostfeuerblitz ist ab Stufe 40 verfügbar.' },
  { id:'warlock', n:'Hexenmeister', roles:['dps'],
    specs:[['Gebrechen','Schaden durch Flüche und Verderbnis',['dps']],['Dämonologie','Schaden durch Dämonen',['dps']],['Zerstörung','Direkter Feuer- und Schattenschaden',['dps']]],
    lvl:'Durchschnittliches Leveltempo',
    lp:0,
    raid:'Dunkle Meisterschaft gibt 2–10 % Schattenschaden, wie in Classic (in der frühen Beta 1–5 %)',
    forever:'Gebrechen hat einen neuen kanalisierten Zauber, der Dämon bleibt bei Dämonischer Opferung, Zerstörung bekam Verbrennen und Flächenschaden.' },
  { id:'druid', n:'Druide', roles:['tank','heal','dps'],
    specs:[['Gleichgewicht','Fernkampfschaden',['dps']],['Wilder Kampf','Tank (Bär) und Nahkampfschaden (Katze)',['tank','dps']],['Wiederherstellung','Heiler, viel Heilung über Zeit',['heal']]],
    lvl:'Etwa 5 % langsamer als der Durchschnitt (Schätzung von LFCarry)',
    lp:5,
    raid:'Rudelführer und Aura des Moonkin wirken auf den ganzen Raid und sind stapelbar',
    forever:'Jede Spezialisierung hat eine klare Rolle, Gestalten funktionieren mit Tränken und Waffenverzauberungen. Du kannst Tank, Heiler und Kämpfer auf einem Charakter sein.' }
];
const ROLE_RU = { tank:'Tank', heal:'Heiler', dps:'Schaden', 'tank?':'Tank (unsicher)' };
const ri = r => `<svg class="ri" aria-hidden="true"><use href="#i-${r.replace('?','')}"/></svg>`;
const CCOL = { warrior:'#c79c6e', paladin:'#f58cba', hunter:'#abd473', rogue:'#fff569', priest:'#e8e8e8', shaman:'#2f8cf0', mage:'#40c7eb', warlock:'#8788ee', druid:'#ff7d0a' };
const BUFF = { warrior:'Schlachtruf', paladin:'Segen der Könige', hunter:'Aura des Volltreffers', priest:'Machtwort: Seelenstärke, Göttlicher Willen', shaman:'Totems (Erdstärke, Windzorn, Flammenzunge, Anmut der Luft)', mage:'Arkane Intelligenz, Portale, Essen und Wasser', druid:'Mal der Wildnis, Rudelführer, Aura des Moonkin' };

const RACES = [
  { id:'human', n:'Mensch', f:'alliance',
    cls:['warrior','paladin','hunter*','rogue','priest','mage','warlock'],
    rac:[['a','Überlebenswille','Entfernt Betäubung'],['a','Wachsamkeit','Enthüllt unsichtbare Gegner für 20 Sek.'],['p','Ruthless','+1 % kritische Trefferchance'],['p','Unbeugsamkeit','+10 % Willenskraft']],
    tip:'Willenskraft fließt beim Heilig-Priester in die Heilung, deshalb ist ein menschlicher Priester gut zum Heilen.' },
  { id:'dwarf', n:'Zwerg', f:'alliance',
    cls:['warrior','paladin','hunter','rogue','priest','shaman*'],
    rac:[['a','Steingestalt','Immunität gegen Blutungen, Gifte und Krankheiten für 8 Sek. und weniger körperlicher Schaden'],['a','Schatzsucher','Zeigt Truhen in der Nähe und gibt in den meisten Truhen eine Chance auf zusätzliche Gegenstände'],['p','Artisan’s Precision','+1 % Trefferchance mit Zaubern und Angriffen'],['p','Big Game Hunter','+5 % Schaden gegen Wildtiere']],
    tip:'Steingestalt ist nützlich für Tanks und im PvP.' },
  { id:'nightelf', n:'Nachtelf', f:'alliance',
    cls:['warrior','hunter','rogue','priest','druid'],
    rac:[['a','Elunes Licht','+10 % kritische Trefferchance für 15 Sek.'],['a','Schattenmimik','Unsichtbarkeit auf der Stelle'],['p','Schnelligkeit','+2 % Ausweichen und Laufgeschwindigkeit (Warcraft Tavern nennt 1 % Ausweichen) {beta}'],['p','Irrwischgeist','+75 % Laufgeschwindigkeit als Geist (Warcraft Tavern nennt 25 %) {beta}']],
    tip:'Das einzige Allianzvolk mit Druiden, außer du nimmst Skyborne.' },
  { id:'gnome', n:'Gnom', f:'alliance',
    cls:['warrior','rogue','mage','warlock','priest*'],
    rac:[['a','Entfesselungskünstler','Kurze Immunität gegen Verlangsamung und Bewegungsunfähigkeit'],['a','Eureka!','Für 8 Sek. kosten Fähigkeiten weniger und sind 10 % stärker {beta}'],['p','Wacher Geist','+5 % maximales Mana, Wut oder Energie'],['p','Ingenieursspezialisierung','Ingenieursgeräte funktionieren zuverlässiger']],
    tip:'Wacher Geist hilft besonders Energieklassen.' },
  { id:'skyA', n:'Skyborne (Allianz)', f:'alliance', paid:true, name:'High Order Skyborne',
    cls:['warrior','hunter','rogue','mage','druid'],
    rac:[['a','Walk on Air','10 Sek. nach unten gleiten, kein Fallschaden'],['a','Read Ley Line','Gesundheits- und Manaregeneration +50 % für 15 Sek. An einer Ley Line zusätzlich Attuned für 1 Stunde: +100 %, bleibt nach dem Tod'],['p','Wind Blessed','+2 % Angriffs- und Zaubertempo'],['p','Elemental Insight','+5 % Schaden gegen Elementare']],
    tip:'Bezahltes Volk: Heroic Pack ab 29,99 $. Startet im Gebiet Zephras Isle (Stufen 1–12).' },
  { id:'orc', n:'Orc', f:'horde',
    cls:['warrior','hunter','rogue','shaman','warlock','mage*'],
    rac:[['a','Kochendes Blut','+10 % Angriffskraft und Zaubermacht für 15 Sek.'],['a','Shatter Curse','Entfernt Flüche und Verderbnis, −5 % erlittener Magieschaden für 8 Sek.'],['p','Befehlsgewalt','+5 % Schaden der Begleiter von Hexenmeistern und Jägern'],['p','Zähigkeit','Betäubungen sind 20 % kürzer']],
    tip:'Kochendes Blut gibt ein starkes Schadensfenster.' },
  { id:'undead', n:'Untoter', f:'horde',
    cls:['warrior','rogue','mage','priest','warlock','paladin*'],
    rac:[['a','Wille der Verlassenen','Entfernt Bezauberung, Furcht und Schlaf'],['a','Kannibalismus','Stellt über Zeit 35 % Gesundheit und Mana wieder her'],['p','Unterwasseratmung','Länger unter Wasser atmen'],['p','Berührung des Grabes','Chance, bei Angriffen Gesundheit zu entziehen']],
    tip:'Neue Kombination: ein Paladin für die Horde, wo es diese Klasse vorher nicht gab.' },
  { id:'tauren', n:'Tauren', f:'horde',
    cls:['warrior','hunter','shaman','druid'],
    rac:[['a','Kriegsdonner','Betäubt Gegner in der Nähe für 2 Sek., Abklingzeit 90 Sek.'],['a','Grüner Daumen','Lässt Kräuter wachsen, die man ohne Kräuterkunde sammeln kann, Abklingzeit 15 Min.'],['p','Ebenenlaufen','Solange du dich bewegst, steigt das Lauftempo um 2 % pro Stapel, bis +60 %. Wirkt nicht auf das Reittempo'],['p','Durchhaltevermögen','+5 % Gesundheit']],
    tip:'Das einzige Hordevolk mit Druiden, außer du nimmst Skyborne.' },
  { id:'troll', n:'Troll', f:'horde',
    cls:['warrior','hunter','rogue','priest','shaman','mage','warlock*'],
    rac:[['a','Berserker','+10 % Angriffs- und Zaubertempo für 12 Sek., 3 Min. Abklingzeit'],['a','Rasche Regeneration','Stellt über Zeit Gesundheit wieder her'],['p','Wildtierschlächter','+5 % Schaden gegen Wildtiere'],['p','Regeneration','Gesundheit regeneriert auch im Kampf']],
    tip:'Die meisten Klassenoptionen der Horde: sieben.' },
  { id:'skyH', n:'Skyborne (Horde)', f:'horde', paid:true, name:'Windshaper Skyborne',
    cls:['warrior','hunter','rogue','shaman','druid'],
    rac:[['a','Walk on Air','10 Sek. nach unten gleiten, kein Fallschaden'],['a','Skysight','+15 % Laufgeschwindigkeit für 15 Sek. An einer Elemental Convergence zusätzlich Charged für 1 Stunde: +30 %, bleibt nach dem Tod'],['p','Wind Blessed','+2 % Angriffs- und Zaubertempo'],['p','Elemental Insight','+5 % Schaden gegen Elementare']],
    tip:'Bezahltes Volk: Heroic Pack ab 29,99 $. Nur die Horde kann Schamanen haben, nur die Allianz Magier.' }
];
RACES.forEach(r => { r.can = {}; r.cls.forEach(c => { const isNew = c.endsWith('*'); r.can[isNew ? c.slice(0,-1) : c] = isNew ? 'new' : 'ok'; }); });
const CL = Object.fromEntries(CLASSES.map(c => [c.id, c]));
const BETA = '<span class="beta-note">laut Beta-Daten</span>';
const BMARK = '{' + 'beta}';   // split so the guide build (which swaps the marker for the span everywhere) leaves it alone
const racx = s => String(s).split(BETA).join(BMARK).split(BMARK).map(esc).join(BETA);
const RC = Object.fromEntries(RACES.map(r => [r.id, r]));
const EN = {
  'Waffen':'Waffen','Furor':'Furor','Schutz':'Schutz','Heilig':'Heilig','Vergeltung':'Vergeltung',
  'Tierherrschaft':'Tierherrschaft','Treffsicherheit':'Treffsicherheit','Überleben':'Überleben',
  'Meucheln':'Meucheln','Kampf':'Kampf','Täuschung':'Täuschung',
  'Disziplin':'Disziplin','Schatten':'Schatten','Elementar':'Elementar','Verstärkung':'Verstärkung','Wiederherstellung':'Wiederherstellung',
  'Arkan':'Arkan','Feuer':'Feuer','Frost':'Frost','Gebrechen':'Gebrechen','Dämonologie':'Dämonologie','Zerstörung':'Zerstörung',
  'Gleichgewicht':'Gleichgewicht','Wilder Kampf':'Wilder Kampf',
  'Überlebenswille':'Überlebenswille','Wachsamkeit':'Wachsamkeit','Ruthless':'Ruthless','Unbeugsamkeit':'Unbeugsamkeit',
  'Steingestalt':'Steingestalt','Schatzsucher':'Schatzsucher','Earth Fury':'Earth Fury','Big Game Hunter':'Big Game Hunter',
  'Elunes Licht':"Elunes Licht",'Schattenmimik':'Schattenmimik','Schnelligkeit':'Schnelligkeit','Irrwischgeist':'Irrwischgeist',
  'Entfesselungskünstler':'Entfesselungskünstler','Eureka!':'Heureka!','Wacher Geist':'Wacher Geist','Ingenieursspezialisierung':'Ingenieursspezialisierung',
  'Walk on Air':'Walk on Air','Read Ley Line':'Read Ley Line','Wind Blessed':'Wind Blessed','Elemental Insight':'Elemental Insight','Skysight':'Skysight',
  'Kochendes Blut':'Kochendes Blut','Shatter Curse':'Shatter Curse','Savage':'Savage','Befehlsgewalt':'Befehlsgewalt','Zähigkeit':'Zähigkeit',
  'Wille der Verlassenen':'Wille der Verlassenen','Kannibalismus':'Kannibalismus','Unterwasseratmung':'Unterwasseratmung','Berührung des Grabes':'Berührung des Grabes',
  'Kriegsdonner':'Kriegsdonner','Grüner Daumen':'Grüner Daumen','Ebenenlaufen':'Ebenenlaufen','Durchhaltevermögen':'Durchhaltevermögen',
  'Berserker':'Berserker','Rasche Regeneration':'Rasche Regeneration','Wildtierschlächter':'Wildtierschlächter','Regeneration':'Regeneration'
};
RC.skyA.en = 'High Order Skyborne'; RC.skyH.en = 'Windshaper Skyborne';
const CX = {"warrior": {"armor": "Stoff, Leder, Schwere Rüstung; Platte ab Stufe 40 {beta}", "weapons": "Alles außer Zauberstäben; Schild", "resource": "Wut", "lvl": "Langsamstes Leveln, etwa 12 % länger als der Durchschnitt (Schätzung von LFCarry)", "group": ["Schlachtruf wirkt auf den ganzen Raid", "Demoralisierungsruf und Rüstung zerreißen auf dem Boss", "Weitreichende Stöße und Wirbelwind für Kämpfe gegen mehrere Ziele"], "pros": ["Bester Tank und starker Nahkampfschaden", "Gut fürs PvP (Waffen)", "Wenige Tasten, leicht zu verstehen"], "cons": ["Langsamstes Leveln", "Stark von Ausrüstung abhängig", "Kaum Selbstheilung oder Gruppenkontrolle"], "specs": [{"n": "Waffen", "what": "Nahkampfschaden (Zweihandwaffe)"}, {"n": "Furor", "what": "Nahkampfschaden (zwei Waffen)"}, {"n": "Schutz", "what": "Tank"}]}, "paladin": {"armor": "Stoff, Leder, Schwere Rüstung; Platte ab Stufe 40; Schild {beta}", "weapons": "Äxte, Streitkolben, Schwerter, Stangenwaffen ab Stufe 20 {beta}", "resource": "Mana", "lvl": "Durchschnittliches Leveltempo", "group": ["Gruppenauren: Hingabe, Vergeltung, Konzentration", "Widerstandsauren gegen Feuer, Frost und Schatten für den ganzen Raid", "Segen für eine Stunde, große Segen für eine ganze Klasse", "Siegel der Gerechtigkeit hindert Gegner an der Flucht"], "pros": ["Alle drei Rollen auf einem Charakter", "Starke Gruppenbuffs", "Platte und ein zäher Charakter"], "cons": ["Kein Ranspringen, keine Verlangsamung, kein Tempoboost", "Wenig Kontrolle außer Hammer der Gerechtigkeit", "Vergeltung ist nach dem Patch abgerutscht"], "specs": [{"n": "Heilig", "what": "Heiler"}, {"n": "Schutz", "what": "Tank"}, {"n": "Vergeltung", "what": "Nahkampfschaden"}]}, "hunter": {"armor": "Stoff, Leder; Schwere Rüstung ab Stufe 40 {beta}", "weapons": "Bögen, Armbrüste, Schusswaffen, Äxte, Schwerter, Stangenwaffen", "resource": "Mana; der Begleiter nutzt Fokus", "lvl": "Schnellstes Leveln, etwa 8 % schneller als der Durchschnitt (Schätzung von LFCarry)", "group": ["Aura des Volltreffers erhöht den Fernkampfschaden der Gruppe", "Eiskältefalle: zuverlässige Kontrolle", "Streuschuss unterbricht Zauber", "Aspekt des Rudels macht die ganze Gruppe unterwegs schneller"], "pros": ["Schnellstes Leveln", "Super solo", "Fallen und Kontrolle"], "cons": ["Tote Zone im Nahbereich bis 8 Meter", "Du musst den Begleiter steuern", "Überleben-Talente waren in der Beta verbuggt"], "specs": [{"n": "Tierherrschaft", "what": "Fernkampfschaden, viel Schaden vom Begleiter"}, {"n": "Treffsicherheit", "what": "Fernkampfschaden"}, {"n": "Überleben", "what": "Nah- und Fernkampf, Fallen"}]}, "rogue": {"armor": "Stoff, Leder", "weapons": "Dolche, Schwerter, Streitkolben, Faustwaffen, Einhandäxte, Wurfwaffen", "resource": "Energie und Combopunkte", "lvl": "Durchschnittliches Leveltempo", "group": ["Reiner Nahkampfschaden ohne raidweite Buffs", "Kopfnuss, Blenden und Nierenhieb: viel Kontrolle", "Tritt unterbricht gefährliche Zauber"], "pros": ["Sehr hoher Schaden, der mit der Ausrüstung skaliert", "Verstohlenheit und viel Kontrolle", "Freie Waffenwahl"], "cons": ["Stark von Ausrüstung abhängig", "Keine Selbstheilung", "Nur Entrinnen und Verschwinden retten dich"], "specs": [{"n": "Meucheln", "what": "Giftschaden"}, {"n": "Kampf", "what": "Schnelle Waffenangriffe"}, {"n": "Täuschung", "what": "Hinterhalte, Blutungen"}]}, "priest": {"armor": "Stoff", "weapons": "Dolche, Streitkolben, Stäbe, Zauberstäbe", "resource": "Mana", "lvl": "Etwa 5 % langsamer als der Durchschnitt (Schätzung von LFCarry)", "group": ["Göttlicher Willen und Machtwort: Seelenstärke für den ganzen Raid", "Seele der Macht verstärkt einen Verbündeten", "Der Hauptheiler der Gruppe"], "pros": ["Wird von jeder Gruppe gebraucht", "Heilung oder Schattenschaden", "Viele Skillungen"], "cons": ["Nur Stoff, zerbrechlich", "Wenig Möglichkeiten, schnell zu sein", "Tempo hilft Zaubern kaum"], "specs": [{"n": "Disziplin", "what": "Heiler, Schilde und Absorption"}, {"n": "Heilig", "what": "Heiler"}, {"n": "Schatten", "what": "Fernkampfschaden"}]}, "shaman": {"armor": "Stoff, Leder; Schwere Rüstung ab Stufe 40; Schild {beta}", "weapons": "Streitkolben, Äxte, Stäbe, Faustwaffen, Dolche", "resource": "Mana", "lvl": "Durchschnittliches Leveltempo", "group": ["Die Totems Erdstärke, Windzorn, Flammenzunge und Anmut der Luft buffen die eigene Gruppe", "Totem des Erdstoßes entfernt Furcht, Schlaf und Bezauberung", "Totems gegen Gifte und Krankheiten", "Reinigen entfernt Buffs von Gegnern"], "pros": ["Starke Totems für die Gruppe", "Mobiles Leveln", "Starke neue Talente"], "cons": ["Keine harte Kontrolle", "Mana in langen Kämpfen", "Tanken noch unbestätigt"], "specs": [{"n": "Elementar", "what": "Fernkampfschaden"}, {"n": "Verstärkung", "what": "Nahkampfschaden. Ob er tanken kann, ist noch offen"}, {"n": "Wiederherstellung", "what": "Heiler"}]}, "mage": {"armor": "Stoff", "weapons": "Dolche, Schwerter, Stäbe, Zauberstäbe", "resource": "Mana", "lvl": "Schnellstes Leveln, etwa 8 % schneller als der Durchschnitt, rund 12 Stunden gespart (Schätzung von LFCarry)", "group": ["Portale ab Stufe 40, Teleports ab 20", "Essen und Wasser für die Gruppe", "Verwandlung: zuverlässige Kontrolle", "Geringen Fluch aufheben"], "pros": ["Schnellstes Leveln", "Portale und Essen für alle", "Drei starke und unterschiedliche Bäume"], "cons": ["Nur Stoff, zerbrechlich", "Mana geht schnell aus", "Flächenschaden abgeschwächt"], "specs": [{"n": "Arkan", "what": "Burst, viel Mana"}, {"n": "Feuer", "what": "Krits und Entzünden"}, {"n": "Frost", "what": "Schaden und Kontrolle"}]}, "warlock": {"armor": "Stoff", "weapons": "Dolche, Schwerter, Stäbe, Zauberstäbe", "resource": "Mana; Aderlass wandelt Gesundheit in Mana", "lvl": "Durchschnittliches Leveltempo", "group": ["Gesundheitsstein und Seelenstein", "Ritual der Beschwörung: holt die Gruppe zusammen", "Fluch der Sprachen verlangsamt das Zaubern um 60 %", "Fluch der Elemente: mehr Magieschaden am Ziel"], "pros": ["Selbstständig: ein Dämon und Aderlass", "Viel Nutzen für die Gruppe", "Starker Schaden über Zeit"], "cons": ["Zerbrechlich und unbeweglich", "Der Schaden braucht Zeit zum Anlaufen", "Kein Blinzeln, kein Sprint"], "specs": [{"n": "Gebrechen", "what": "Schaden durch Flüche und Verderbnis"}, {"n": "Dämonologie", "what": "Schaden durch Dämonen"}, {"n": "Zerstörung", "what": "Direkter Feuer- und Schattenschaden"}]}, "druid": {"armor": "Stoff, Leder", "weapons": "Dolche, Streitkolben, Stäbe, Faustwaffen, Stangenwaffen ab Stufe 20 {beta}", "resource": "Mana; Wut in Bärengestalt, Energie in Katzengestalt", "lvl": "Etwa 5 % langsamer als der Durchschnitt (Schätzung von LFCarry)", "group": ["Rudelführer und Aura des Moonkin wirken auf den ganzen Raid und sind stapelbar", "Wiedergeburt: Wiederbelebung im Kampf", "Anregen gibt einem Heiler Mana zurück", "Entfernt Flüche und Gifte"], "pros": ["Alle drei Rollen auf einem Charakter", "Super mobil", "Wiederbelebung im Kampf"], "cons": ["Kein Blocken oder Parieren für den Bären", "Heilung über Zeit ist schwerer im Blick zu behalten", "Endgültige Raidzahlen sind noch unbekannt"], "specs": [{"n": "Gleichgewicht", "what": "Fernkampfschaden"}, {"n": "Wilder Kampf", "what": "Tank (Bär) und Nahkampfschaden (Katze)"}, {"n": "Wiederherstellung", "what": "Heiler, viel Heilung über Zeit"}]}};
const HC = {"tx":{"title":"Mein Charakter","lead":"Ohne Login und Passwort: Wähle Klasse, Spezialisierung und Volk, und die Seite passt sich dir an.","local":"Nur in diesem Browser gespeichert.","none":"Noch kein Charakter","create":"Charakter erstellen","edit":"Bearbeiten","reset":"Charakter löschen","resetQ":"Charakter aus diesem Browser löschen?","steps":["Seite","Klasse und Spezialisierung","Volk","Aussehen","Details"],"side":"Für wen spielst du?","cls":"Klasse","spec":"Spezialisierung","race":"Volk","bestFor":"Bestes Volk für %s","best":"beste","paid":"bezahlt","sex":"Geschlecht","m":"Männlich","f":"Weiblich","bg":"Porträt-Hintergrund","lvl":"Stufe","reg":"Region","lvlReg":"Stufe und Region","regs":{"us":"Amerika und Ozeanien","eu":"Europa","kr":"Korea","tw":"Taiwan"},"p1":"Beruf 1","p2":"Beruf 2","secP":"Nebenberufe","noP":"Keine","role":"Rolle","back":"Zurück","next":"Weiter","done":"Fertig","cancel":"Abbrechen","later":"Kannst du auch später ausfüllen.","levelN":"Stufe %n","build":"Mein Talent-Build","buildD":"Talente für %s nach Stufe.","pairs":"Berufspaare","pairsD":"Welche Berufe zu deiner Klasse passen.","bestR":"Beste Völker","bestRD":"Volk für deine Klasse in beiden Fraktionen.","lvlG":"Klassen-Leveling","lvlGD":"Route und Talente 1–60.","day1":"Tag 1 für deinen Charakter","day1D":"Die Start-Checkliste mit deiner Klasse und deinem Volk.","play":"Im Spiel","playD":"Zonen und Dungeons für deine Stufe, Timer, Radio.","dung":"Dungeons für deine Stufe","dungNo":"Gib deine Stufe an, dann suchen wir Dungeons aus.","dungFirst":"Die ersten Dungeons öffnen ab Stufe 13.","resetH":"Wöchentlicher Reset","resetIn":"in %s","resetNote":"Blizzard hat die Reset-Zeit von Forever noch nicht bekannt gegeben. Angezeigt wie in anderen WoW-Versionen dieser Region: Wir prüfen es zum Start.","resetUnk":"Die Reset-Zeit für diese Region bestätigen wir zum Start.","resetNoReg":"Gib deine Region an, um den wöchentlichen Reset zu sehen.","resetWhy":"Schlachtzüge öffnen am 09.12 und haben eine wöchentliche ID.","lfg":"Text für die Gruppensuche","lfgD":"Füge ihn in den Chat LookingForGroup ein. Namen wie im Spiel.","lfgP":{"tank":"%c-Tank sucht Gruppe","heal":"%c-Heiler sucht Gruppe","dps":"%c sucht Gruppe"},"lfgT":"%p: %d, Stufe %l.","lfgT0":"%p.","allD":"Alle Dungeons","copy":"Kopieren","copied":"Kopiert","sync":"Zwischen Geräten synchronisieren","syncD":"Ein Login ist nur dafür nötig: Der Charakter ist dann auf Handy und PC, und die Start-Mail kommt per E-Mail, wenn du sie abonnierst.","yourCls":"Dein %s","bTalents":"Talente","bSpec":"Build: %s","bLevel":"Leveln","bGroup":"Gruppe","bNews":"News","copiedT":"Kopiert: %s","profsL":"Berufe","day1n":"Tag 1: %n von %t","collect":"Charakter zusammenstellen","collectD":"Klasse, Spezialisierung und Volk: Talente, Leveln, Gruppe und News deiner Klasse.","change":"Ändern","allSet":"Alle Einstellungen","close":"Schließen","mine":"Betrifft deine Klasse","share":"Teilen","linkCopied":"Link kopiert","make":"Zu meinem Charakter machen","made":"Das ist dein Charakter","plaqueH":"Mein Charakter","plaqueD":"Klasse, Spezialisierung und Volk in einer Minute, dann dein Build, deine Berufe und Dungeons.","day1Mine":"Für deinen Charakter","ckClass":"Deine Spezialisierung, %s: der Talent-Build nach Stufe.","ckRaceOk":"%r ist das beste Volk für deine Spezialisierung.","ckRaceAlt":"Bestes Volk für deine Spezialisierung: %r.","ckProfs":"Berufspaare für %s.","ckStart":"Leveln als %s: Route und erste Talente.","ckPing":"Deine Region: %s.","or":"oder"},"best":{"warrior":{"alliance":{"*":[["human","nightelf"],"Mensch: +1 % kritische Trefferchance mit jeder Waffe. Nachtelf: +10 % für 15 Sek. Die Quellen sind fast gleich verteilt."],"protection":[["dwarf"],"Steingestalt senkt körperlichen Schaden um 10 % und entfernt Blutungen."]},"horde":{"*":[["orc"],"Kochendes Blut: +10 % Angriffskraft für 15 Sek. Vor den Völker-Änderungen vom 26.10 setzten es alle Quellen an die Spitze."],"protection":[["tauren"],"Durchhaltevermögen gibt +5 % Gesundheit, Kriegsdonner betäubt Gegner in der Nähe."]}},"paladin":{"alliance":{"*":[["human"],"Ruthless verstärkt Schläge und Zauber, Überlebenswille entfernt Betäubungen."],"protection":[["dwarf"],"Steingestalt und Artisan’s Precision: +1 % Trefferchance."]},"horde":{"*":[["undead"],"In der Horde kann nur der Untote Paladin sein. Kannibalismus stellt Mana wieder her, Wille der Verlassenen entfernt Furcht."]}},"hunter":{"alliance":{"*":[["human","nightelf"],"Mensch: +1 % kritische Trefferchance, das Tier erbt sie. Nachtelf: Elunes Licht und Schattenmimik."]},"horde":{"*":[["orc","troll"],"Orc: Kochendes Blut und Befehlsgewalt (+5 % Begleiterschaden). Troll: +5 % Schaden gegen Wildtiere."]}},"rogue":{"alliance":{"*":[["nightelf"],"Schattenmimik senkt die Bedrohung jetzt auch im Kampf, dazu Elunes Anmut und Schnelligkeit."]},"horde":{"*":[["orc"],"Kochendes Blut: +10 % Angriffskraft für 15 Sek."]}},"priest":{"alliance":{"*":[["gnome"],"Alle Quellen wählen es: Heureka! verstärkt auch Machtwort: Schild, Inquisitive Mind gibt +5 % Mana."]},"horde":{"*":[["undead","troll"],"Die Quellen sind uneins. Untote sind im PvP stärker: Wille der Verlassenen entfernt Furcht, Schlaf und Bezauberung."]}},"shaman":{"alliance":{"*":[["dwarf"],"In der Allianz kann nur der Zwerg Schamane sein: Steingestalt und Artisan’s Precision (+1 % Trefferchance)."]},"horde":{"*":[["orc"],"Kochendes Blut gibt Angriffskraft und Zaubermacht: gut für Elementar und Verstärkung."],"restoration":[["troll"],"Für Heiler empfiehlt eine Quelle den Troll: Berserker, +10 % Zaubertempo für 12 Sek."]}},"mage":{"alliance":{"*":[["gnome"],"Heureka! für 8 Sek., Inquisitive Mind: +5 % Mana, Entfesselungskünstler löst Wurzeln."]},"horde":{"*":[["orc"],"Orc-Magier ist eine neue Kombination in Forever: Kochendes Blut gibt jetzt Zaubermacht."]}},"warlock":{"alliance":{"*":[["gnome","human"],"Gnom: Heureka! und Inquisitive Mind. Mensch: Schaden über Zeit kann kritisch treffen, Ruthless gibt +1 % kritische Trefferchance."]},"horde":{"*":[["orc","undead"],"Orc: Kochendes Blut gibt Zaubermacht. Untote werden im PvP öfter gewählt."]}},"druid":{"alliance":{"*":[["nightelf"],"Elunes Anmut: +10 % kritische Trefferchance für 15 Sek., dazu Schnelligkeit."]},"horde":{"*":[["tauren"],"Durchhaltevermögen: +5 % Gesundheit, Kriegsdonner wirkt auch in Gestalten."]}}},"sid":{"warrior":["arms","fury","protection"],"paladin":["holy","protection","retribution"],"hunter":["beast-mastery","marksmanship","survival"],"rogue":["assassination","combat","subtlety"],"priest":["discipline","holy","shadow"],"shaman":["elemental","enhancement","restoration"],"mage":["arcane","fire","frost"],"warlock":["affliction","demonology","destruction"],"druid":["balance","feral","restoration"]},"sn":{"warrior":["Waffen","Furor","Schutz"],"paladin":["Heilig","Schutz","Vergeltung"],"hunter":["Tierherrschaft","Treffsicherheit","Überleben"],"rogue":["Meucheln","Kampf","Täuschung"],"priest":["Disziplin","Heilig","Schatten"],"shaman":["Elementar","Verstärkung","Wiederherstellung"],"mage":["Arkan","Feuer","Frost"],"warlock":["Gebrechen","Dämonologie","Zerstörung"],"druid":["Gleichgewicht","Wilder Kampf","Wiederherstellung"]},"fn":{"alliance":"Allianz","horde":"Horde"},"reset":{"us":[2,15],"eu":[3,4],"kr":null,"tw":null},"rn":{"human":"Mensch","dwarf":"Zwerg","nightelf":"Nachtelf","gnome":"Gnom","skyA":"High Order Skyborne","orc":"Orc","undead":"Untoter","tauren":"Tauren","troll":"Troll","skyH":"Windshaper Skyborne"},"rf":{"human":"alliance","dwarf":"alliance","nightelf":"alliance","gnome":"alliance","skyA":"alliance","orc":"horde","undead":"horde","tauren":"horde","troll":"horde","skyH":"horde"},"cn":{"warrior":"Krieger","paladin":"Paladin","hunter":"Jäger","rogue":"Schurke","priest":"Priester","shaman":"Schamane","mage":"Magier","warlock":"Hexenmeister","druid":"Druide"},"cen":{"warrior":"Warrior","paladin":"Paladin","hunter":"Hunter","rogue":"Rogue","priest":"Priest","shaman":"Shaman","mage":"Mage","warlock":"Warlock","druid":"Druid"}};
function readHero() {
  let m = {};
  try { m = JSON.parse(localStorage.getItem('gabella-wf-me')) || {}; } catch (e) { m = {}; }
  if (!m || typeof m !== 'object' || !HC.cn[m.cls]) return null;
  const sid = HC.sid[m.cls], spec = sid.includes(m.spec) ? m.spec : '';
  return Object.assign({}, m, { spec, specN: spec ? HC.sn[m.cls][sid.indexOf(spec)] : '', clsN: HC.cn[m.cls], raceN: HC.rn[m.race] || '', fac: HC.rf[m.race] || '' });
}
function bestOf(cls, fac, spec) { const b = (HC.best[cls] || {})[fac]; return b ? (b[spec] || b['*']) : null; }
function nextReset(reg) {   // the region's weekly reset [weekday UTC, hour UTC] -> the next moment after now; null: not known
  const r = HC.reset[reg]; if (!r) return null;
  const now = new Date(), d = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate(), r[1]));
  d.setUTCDate(d.getUTCDate() + (r[0] - d.getUTCDay() + 7) % 7);
  if (d <= now) d.setUTCDate(d.getUTCDate() + 7);
  return d;
}
function leftTxt(ms) {
  const u = (n, k) => new Intl.NumberFormat(document.documentElement.lang, { style: 'unit', unit: k, unitDisplay: 'short', maximumFractionDigits: 0 }).format(n);
  const m = Math.max(1, Math.round(ms / 6e4)), d = Math.floor(m / 1440), h = Math.floor(m % 1440 / 60);
  return d ? `${u(d, 'day')} ${u(h, 'hour')}` : h ? `${u(h, 'hour')} ${u(m % 60, 'minute')}` : u(m, 'minute');
}

const CPROF = {"warrior": [["Leveln: Schmiedekunst + Bergbau", ""], ["Stufe 60: Ingenieurskunst + Bergbau", "Ein Schmied stattet sich mit Platte und Waffen aus, viele Rezepte sind persönlich. Der Ingenieur bekommt Granaten und Gadgets, die dem Krieger fehlen."]], "paladin": [["Leveln: Schmiedekunst + Bergbau", ""], ["Stufe 60: Schutz, Vergeltung: Ingenieurskunst + Bergbau. Heilig: Alchimie + Kräuterkunde", "Heilig verbraucht viel Mana: Die Tränke machst du selbst, und das Mana Well im Lager ersetzt Segen der Weisheit."]], "hunter": [["Leveln: Lederverarbeitung + Kürschnerei", ""], ["Stufe 60: Ingenieurskunst + Bergbau", "Ein Lederverarbeiter näht sich Leder und Kette und Armor Kits. Der Ingenieur baut Zielfernrohre und Gewehre."]], "rogue": [["Leveln: Lederverarbeitung + Kürschnerei", ""], ["Stufe 60: Ingenieurskunst + Bergbau", "Das Leder machst du selbst, das Camp Tent gibt Erholung. Ingenieurskunst ist der wichtigste Beruf fürs PvP."]], "priest": [["Leveln: Schneiderei + Verzauberkunst", ""], ["Stufe 60: Schneiderei + Ingenieurskunst oder Verzauberkunst", "Der Schneider näht ab Stufe 10 Gürtel mit Zaubermacht, der Verzauberer ab Stufe 5 Zauberstäbe mit Zaubermacht. Genähtes wird zu Materialien entzaubert."]], "shaman": [["Leveln: Lederverarbeitung + Kürschnerei", ""], ["Stufe 60: Alchimie + Kräuterkunde", "Der Lederverarbeiter macht Zaubermacht-Ausrüstung für Elementar und Wiederherstellung und Ausrüstung für Verstärkung. Im Raid und in der Gruppe braucht man Tränke."]], "mage": [["Leveln: Schneiderei + Verzauberkunst", ""], ["Stufe 60: Schneiderei + Verzauberkunst; fürs PvP und große Pulls Ingenieurskunst + Bergbau", "Der Schneider liefert frühe Ausrüstung mit Zaubermacht, Genähtes wird entzaubert. Die Granaten des Ingenieurs halten große Gegnergruppen an Ort und Stelle."]], "warlock": [["Leveln: Schneiderei + Verzauberkunst", ""], ["Stufe 60: Schneiderei + Alchimie", "Das Faction Banner des Schneiders gibt Willenskraft für Aderlass. Alchimie bedeutet Tränke und Gold."]], "druid": [["Leveln: Lederverarbeitung + Kürschnerei oder Kräuterkunde", ""], ["Stufe 60: Alchimie + Kräuterkunde", "Kräuter sammelst du in Reisegestalt, Tränke trinkst du in jeder Gestalt. Mana Well und Incense Candle helfen Gleichgewicht und Wiederherstellung."]]};   /* recommended profession pairs per class, already in the page language (build.class_profs) */
const $ = s => document.querySelector(s);
const ROOT = '../../', HOME = '../';
function esc(s) { return String(s).replace(/[&<>"]/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m])); }
function raceName(r) { return r.name || r.n; }
function syncSeg(id, v) { document.querySelectorAll(`#${id} button`).forEach(b => b.setAttribute('aria-pressed', b.dataset.v === String(v))); }
const FAC = { alliance: 'Allianz', horde: 'Horde' };
const BSLUG = { skyA: 'skyborne-a', skyH: 'skyborne-h' };   // race id -> url part of the share page (tools/make_build_cards.py SLUG)
const RSLUG = { human: 'human', dwarf: 'dwarf', nightelf: 'night-elf', gnome: 'gnome', skyA: 'skyborne-alliance', orc: 'orc', undead: 'undead', tauren: 'tauren', troll: 'troll', skyH: 'skyborne-horde' };
const PAINTED = ["druid-nightelf", "druid-tauren", "hunter-nightelf", "hunter-orc", "mage-gnome", "mage-orc", "paladin-human", "paladin-undead", "priest-gnome", "priest-undead", "rogue-nightelf", "rogue-orc", "shaman-dwarf", "shaman-orc", "warlock-gnome", "warlock-orc", "warrior-human", "warrior-orc"];   // class x race paintings that exist (build_tools.painted): the player's own race is drawn, never the best race of the side
const unitArt = (p, ext) => `${ROOT}assets/art/${PAINTED.includes(p.cls + '-' + p.race) ? p.cls + '-' + p.race : RSLUG[p.race]}-360.${ext}${PV}`;
const classUrl = id => `${HOME}classes/${id}/`, raceUrl = id => `${HOME}races/${RSLUG[id]}/`;
const PV = /*PV*/'?v=03c9d4a0';   // ?v= of the class and race portraits (build.art_version)
const porId = (id, f) => (window.GabellaPor ? GabellaPor.id(id, f) : id);   // a class: the portrait of side f, else of the reader's side (build.por_js)
const art = (id, ext = 'webp', f) => `${ROOT}assets/art/${porId(id, f)}-360.${ext}${PV}`;
async function copyTo(text, msgEl, ok) {
  try { await navigator.clipboard.writeText(text); msgEl.textContent = ok; } catch (e) { msgEl.textContent = 'Kopieren fehlgeschlagen, markiere den Text und drücke Strg+C'; }
}

/* ---------- Party and raid frames ---------- */
const SIZES = [5, 10, 20, 40], PARTY = 5, RR = ['tank', 'heal', 'dps'];
const POOL = { tank: ['paladin', 'warrior', 'druid'], heal: ['priest', 'shaman', 'paladin', 'druid'], dps: ['mage', 'hunter', 'warlock', 'rogue', 'shaman', 'druid', 'warrior'] };
const RAIDS = [[10, 'Barrow Deeps'], [20, 'Hyjal Summit'], [40, 'Onyxia’s Lair']];
const REC = { 5: [1, 1, 3], 10: [2, 3, 5], 20: [3, 5, 12], 40: [4, 10, 26] };
const RAGE = '#c8443a', ENERGY = '#e3c54b', MANA = '#3f7fe0';
const R = { f: window.GabellaPor ? GabellaPor.fac() : 'alliance', size: 5, s: Array(5).fill(null), moving: -1 };

function roleOpts(c) { return RR.filter(x => c.roles.includes(x) || (x === 'tank' && c.roles.includes('tank?'))); }
function power(p) { return p.cls === 'warrior' || (p.cls === 'druid' && p.role === 'tank') ? RAGE : p.cls === 'rogue' || (p.cls === 'druid' && p.role === 'dps') ? ENERGY : MANA; }
function slotRole(i) { const k = i % PARTY; return k === 0 ? 'tank' : k === 1 ? 'heal' : 'dps'; }
function raceFor(cls, k) {
  const free = RACES.filter(r => r.f === R.f && !r.paid && r.can[cls]);
  return free.length ? free[k % free.length].id : (RACES.find(r => r.f === R.f && r.can[cls]) || RACES.find(r => r.f === R.f)).id;
}
function fixPlayer(p) {
  const races = RACES.filter(r => r.f === R.f);
  let r = RC[p.race]; if (!r || r.f !== R.f) r = races.find(x => x.can[p.cls]) || races[0];
  p.race = r.id;
  if (!r.can[p.cls]) p.cls = Object.keys(r.can)[0];
  const ro = roleOpts(CL[p.cls]); if (!ro.includes(p.role)) p.role = ro[0];
}
function newPlayer(i, used) {
  const role = slotRole(i), pool = POOL[role].filter(c => RACES.some(r => r.f === R.f && r.can[c]));
  const k = used ? used[role]++ : i;
  const cls = pool[k % pool.length];
  return { race: raceFor(cls, i), cls, role, name: '' };
}
function cleanName(s) { return String(s || '').replace(/[.,;#&]/g, '').trim().slice(0, 16); }

function readHash() {
  const m = location.hash.match(/^#team=(alliance|horde);(?:(\d+);)?(.*)$/);
  if (!m) return;
  const items = m[3].split(',').map(x => {
    const p = x.split('.');
    if (p.length < 3 || !RC[p[0]] || !CL[p[1]] || !RR.includes(p[2])) return null;
    let name = ''; try { name = cleanName(decodeURIComponent(p[3] || '')); } catch (e) {}
    return { race: p[0], cls: p[1], role: p[2], name };
  });
  const want = +m[2], n = items.length;
  R.f = m[1];
  R.size = SIZES.includes(want) && want >= Math.min(n, 40) ? want : SIZES.find(x => x >= n) || 40;
  R.s = Array.from({ length: R.size }, (_, i) => items[i] || null);
}
function hashStr() {
  let last = R.s.length; while (last > 0 && !R.s[last - 1]) last--;
  const list = R.s.slice(0, last).map(p => p ? `${p.race}.${p.cls}.${p.role}${p.name ? '.' + encodeURIComponent(p.name) : ''}` : '-');
  return `#team=${R.f};${R.size};${list.join(',')}`;
}
function teamLink() { return location.origin + location.pathname + shortHash(); }   // the copied link is the short one (#t=); the address bar keeps #team= with the names
function teamText() {
  const groups = Math.ceil(R.size / PARTY), out = [];
  for (let g = 0; g < groups; g++) {
    const part = R.s.slice(g * PARTY, g * PARTY + PARTY).filter(Boolean);
    if (!part.length) continue;
    out.push((groups > 1 ? `Gruppe ${g + 1}: ` : '') + part.map(p => `${p.name ? p.name + ' — ' : ''}${raceName(RC[p.race])} ${CL[p.cls].n} (${ROLE_RU[p.role]})`).join(', '));
  }
  return out.length ? out.join('\n') + `\n${FAC[R.f]}, ${R.size}` : '';
}

/* LFG line: the dungeon or raid, the missing roles, the play style and a short link (#t=); kept under the 255-byte chat limit */
const LFG = {"d": [["Ragefireabgrund", 13, 18, "horde"], ["Hall of Thanes", 13, 18, 0], ["Ruinen von Lordaeron", 15, 20, 0], ["Die Todesminen", 15, 22, 0], ["Die Höhlen des Wehklagens", 17, 24, 0], ["Burg Shadowfang", 20, 26, 0], ["Blackfathom-Tiefe", 22, 28, 0], ["Das Verlies", 25, 29, "alliance"], ["Excavation Site: Wetlands", 26, 31, 0], ["City of Dalaran", 28, 33, 0], ["Gnomeregan", 29, 38, 0], ["Der Kral von Razorfen", 29, 38, 0], ["Das Scharlachrote Kloster: Friedhof", 30, 38, 0], ["Das Scharlachrote Kloster: Bibliothek", 33, 41, 0], ["The Drowned City", 35, 40, 0], ["Das Scharlachrote Kloster: Waffenkammer", 36, 44, 0], ["Uldaman", 36, 45, 0], ["Die Hügel von Razorfen", 37, 46, 0], ["Das Scharlachrote Kloster: Kathedrale", 38, 46, 0], ["Zul’Farrak", 40, 47, 0], ["Krol’dok Stronghold", 40, 45, 0], ["Maraudon", 45, 51, 0], ["Alcaz Island Prison", 48, 53, 0], ["Der Tempel von Atal’Hakkar", 50, 55, 0], ["Blackrocktiefen", 52, 60, 0], ["Blackmaw Hold", 55, 60, 0], ["Untere Blackrockspitze", 57, 60, 0], ["Düsterbruch: Ost", 58, 60, 0], ["Shaper’s Terrace", 58, 60, 0], ["Stratholme: Lebende", 58, 60, 0], ["Stratholme: Untote", 58, 60, 0], ["Scholomance", 58, 60, 0], ["Obere Blackrockspitze", 60, 60, 0], ["Düsterbruch: West", 60, 60, 0], ["Düsterbruch: Nord", 60, 60, 0]], "r": {"10": "Barrow Deeps", "20": "Hyjalgipfel", "40": "Onyxias Hort"}};   // dungeons [name, min, max, entrance faction] and raids {size: name} in the client's language (build_tools)
const CHAT_MAX = 255, CANON = 'https://gabella.site/wow/de/tools/'.replace(/^https?:\/\//, '');
const RK = ['human', 'dwarf', 'nightelf', 'gnome', 'skyA', 'orc', 'undead', 'tauren', 'troll', 'skyH'];
const CK = ['warrior', 'paladin', 'hunter', 'rogue', 'priest', 'shaman', 'mage', 'warlock', 'druid'];
const L = { d: '', s: '' };
function shortHash() {   // two base-36 characters a slot: race, class and role; names stay in the long link only
  let last = R.s.length; while (last > 0 && !R.s[last - 1]) last--;
  const code = R.s.slice(0, last).map(p => (p ? (RK.indexOf(p.race) * CK.length + CK.indexOf(p.cls)) * RR.length + RR.indexOf(p.role) + 1 : 0).toString(36).padStart(2, '0')).join('');
  return `#t=${R.f[0]}${SIZES.indexOf(R.size)}${code}`;
}
function readShort() {
  const m = location.hash.match(/^#t=([ah])([0-3])((?:[0-9a-z]{2})*)$/);
  if (!m) return false;
  const items = (m[3].match(/../g) || []).map(x => {
    let v = parseInt(x, 36) - 1; if (v < 0) return null;
    const role = RR[v % RR.length]; v = Math.floor(v / RR.length);
    const cls = CK[v % CK.length], race = RK[Math.floor(v / CK.length)];
    return RC[race] && CL[cls] ? { race, cls, role, name: '' } : null;
  });
  R.f = m[1] === 'h' ? 'horde' : 'alliance';
  R.size = Math.max(SIZES[+m[2]], SIZES.find(x => x >= items.length) || 40);
  R.s = Array.from({ length: R.size }, (_, i) => items[i] || null);
  return true;
}
function lfgPlaces() { return R.size === 5 ? LFG.d.filter(d => !d[3] || d[3] === R.f).map(d => [d[0], `${d[0]} (${d[1]}–${d[2]})`]) : (LFG.r[R.size] ? [[LFG.r[R.size], LFG.r[R.size]]] : []); }
function lfgNeed() {
  const list = R.s.filter(Boolean), cnt = countRoles(list), rec = REC[R.size];
  let free = R.size - list.length;
  const need = RR.map((x, k) => { const n = Math.min(Math.max(rec[k] - cnt[x], 0), free); free -= n; return n; });
  need[2] += free;   // places left once the roles are covered go to damage
  return need;
}
function lfgText() {
  const need = lfgNeed();
  if (!need.some(Boolean) || !R.s.some(Boolean)) return '';
  const roles = RR.map((x, k) => need[k] ? ROLE_RU[x] + (need[k] > 1 ? ` ×${need[k]}` : '') : '').filter(Boolean).join(', ');
  const head = (L.d ? '%d — gesucht: %n.' : 'Gruppe sucht: %n.').replace('%d', L.d).replace('%n', roles);
  const parts = [head, L.s ? 'Stil: %s.'.replace('%s', L.s) : '', CANON + shortHash()].filter(Boolean);
  const bytes = t => new TextEncoder().encode(t).length;
  let text = parts.join(' ');
  if (bytes(text) > CHAT_MAX) text = parts.slice(0, -1).join(' ');   // a long raid code would not fit: the link goes first
  return text;
}
function renderLfg() {
  const places = lfgPlaces(), sel = $('#lfgD');
  if (!places.some(p => p[0] === L.d)) L.d = R.size === 5 ? '' : (places[0] || [''])[0];
  $('#lfgDL').textContent = R.size === 5 ? 'Dungeon' : 'Schlachtzug';
  sel.innerHTML = (R.size === 5 ? '<option value="">Beliebiger Dungeon</option>' : '') + places.map(([v, t]) => `<option value="${esc(v)}"${v === L.d ? ' selected' : ''}>${esc(t)}</option>`).join('');
  syncSeg('lfgS', L.s);
  const text = lfgText();
  $('#rLfg').value = text;
  $('#rCopyLfg').disabled = !text;
  $('#rLfgMsg').textContent = text ? lfgLen(text) : R.s.some(Boolean) ? 'Alle Plätze sind belegt.' : 'Füge der Gruppe mindestens einen Spieler hinzu.';
}
function lfgLen(t) { return 'Zeichen: %n von %m (Limit einer Chatzeile).'.replace('%n', t.length).replace('%m', CHAT_MAX); }

function unitHTML(p, i) {
  const cls = R.moving === i ? ' src' : '';
  if (!p) return `<button type="button" class="unit empty${cls}" data-i="${i}"><span class="up" aria-hidden="true">+</span><span class="ub"><b>Freier Platz</b><span>Klicken, um Spieler hinzuzufügen</span></span></button>`;
  const c = CL[p.cls], r = RC[p.race];
  return `<button type="button" class="unit${cls}" data-i="${i}" draggable="true" style="--cc:${CCOL[p.cls]};--pc:${power(p)}" aria-label="${esc((p.name || `Spieler ${i + 1}`) + ', ' + raceName(r) + ' ' + c.n + ', ' + ROLE_RU[p.role])}">
    <span class="up"><picture><source type="image/avif" srcset="${unitArt(p, 'avif')}"><img src="${unitArt(p, 'webp')}" width="360" height="482" alt="" loading="lazy" decoding="async"></picture></span>
    <span class="ub"><span class="un"><span class="ur" title="${ROLE_RU[p.role]}">${ri(p.role)}</span><b>${esc(p.name || c.n)}</b><small>${esc(raceName(r))} · ${esc(c.n)}</small></span><span class="hp"><i></i></span><span class="mp"></span></span></button>`;
}
function cellHTML(p, i) {
  const cls = R.moving === i ? ' src' : '';
  if (!p) return `<button type="button" class="rc empty${cls}" data-i="${i}" aria-label="Freier Platz ${i + 1}"><span aria-hidden="true">+</span>Hinzufügen</button>`;
  const c = CL[p.cls], r = RC[p.race];
  return `<button type="button" class="rc${cls}" data-i="${i}" draggable="true" style="--cc:${CCOL[p.cls]};--pc:${power(p)}" aria-label="${esc((p.name || `Spieler ${i + 1}`) + ', ' + raceName(r) + ' ' + c.n + ', ' + ROLE_RU[p.role])}" title="${esc(raceName(r) + ' · ' + c.n + ' · ' + ROLE_RU[p.role])}"><b>${esc(p.name || c.n)}</b><small>${esc(p.name ? c.n : raceName(r))}</small>${ri(p.role)}</button>`;
}
function countRoles(list) { const c = { tank: 0, heal: 0, dps: 0 }; list.forEach(p => p && c[p.role]++); return c; }

function renderRaid(touched = true) {
  R.s.forEach(p => p && fixPlayer(p));
  syncSeg('rF', R.f); syncSeg('rS', R.size);
  const groups = R.size / PARTY;
  $('#rlay').classList.toggle('p5', R.size === 5);
  if (R.size === 5) $('#rview').innerHTML = `<div class="party5">${R.s.map(unitHTML).join('')}</div>`;
  else {
    let h = '';
    for (let g = 0; g < groups; g++) {
      const part = R.s.slice(g * PARTY, g * PARTY + PARTY), c = countRoles(part), n = part.filter(Boolean).length;
      const st = n && (!c.tank || !c.heal) ? `<span class="warn">${!c.tank ? 'kein Tank' : 'kein Heiler'}</span>` : `<span>${n}/5</span>`;
      h += `<div class="rg"><div class="rg-h"><b>Gruppe ${g + 1}</b>${st}</div>${part.map((p, k) => cellHTML(p, g * PARTY + k)).join('')}</div>`;
    }
    $('#rview').innerHTML = `<div class="rgrid" style="--gc:${Math.min(groups, 8)}">${h}</div>`;
  }
  const hint = $('#rhint');
  hint.classList.toggle('on', R.moving >= 0);
  hint.innerHTML = R.moving >= 0 ? `Neuen Platz wählen für Spieler ${R.moving + 1}. <button type="button" id="mvCancel">Abbrechen</button>` : '';

  const list = R.s.filter(Boolean), cnt = countRoles(list), rec = REC[R.size];
  $('#rRoles').innerHTML = RR.map((x, k) => `<span class="${list.length && cnt[x] < rec[k] ? 'low' : ''}">${ri(x)}${ROLE_RU[x]} <b>${cnt[x]}</b> / ${rec[k]}</span>`).join('');
  $('#rTip').textContent = R.size === 5 ? 'Ein Dungeon braucht einen Tank, einen Heiler und drei Schadensverursacher.' : `Faustregel für Raids: Tanks ${rec[0]}, Heiler ${rec[1]}, der Rest Schaden. Die genaue Zahl hängt von den Bossen ab.`;
  const have = new Set(list.map(p => p.cls));
  $('#rBuffs').innerHTML = CLASSES.filter(c => BUFF[c.id]).map(c => `<li class="${have.has(c.id) ? '' : 'off'}" style="--cc:${CCOL[c.id]}"><span class="cdot"></span><span><b>${esc(c.n)}:</b> ${esc(BUFF[c.id])}</span></li>`).join('');
  const n = list.length;
  $('#rRaids').innerHTML = n ? RAIDS.map(([size, name]) => `<li class="${n >= size ? 'good' : ''}">${n >= size ? `Raid für ${size} (${name}): genug Spieler.` : `Raid für ${size} (${name}): es fehlen ${size - n}.`}</li>`).join('') : '<li>Noch niemand da. Klicke auf „Mit meinem Charakter“, „Leere füllen“ oder einen freien Rahmen.</li>';

  const link = n ? teamLink() : '';
  $('#rLink').value = link;
  $('#rCopyLink').disabled = $('#rCopyText').disabled = !n;
  // the link follows the roster only once it has been edited, so #compare and other anchors keep working on load
  if (touched) try { history.replaceState(null, '', n ? hashStr() : location.pathname + location.search); } catch (e) {}
  renderLfg();
}

function setSize(size) {
  // keep slots in place; if some players would fall off the end, pack everyone to the front instead
  const lost = R.s.slice(size).some(Boolean), src = lost ? R.s.filter(Boolean) : R.s;
  R.s = Array.from({ length: size }, (_, i) => src[i] || null);
  R.size = size; R.moving = -1; renderRaid();
}
$('#rF').addEventListener('click', e => { const b = e.target.closest('button'); if (b) { R.f = b.dataset.v; renderRaid(); } });
$('#rS').addEventListener('click', e => { const b = e.target.closest('button'); if (b) setSize(+b.dataset.v); });
$('#rFill').onclick = () => {
  const used = { tank: 0, heal: 0, dps: 0 };
  R.s.forEach(p => p && used[p.role]++);
  R.s = R.s.map((p, i) => p || newPlayer(i, used)); R.moving = -1; renderRaid();
};
function myHero() {   // the hero of this browser (assets/hero/hero.js?v=56e9b73acd, localStorage gabella-wf-me)
  let h = null; try { h = JSON.parse(localStorage.getItem('gabella-wf-me')); } catch (e) {}
  return h && RC[h.race] && CL[h.cls] && RC[h.race].can[h.cls] ? h : null;
}
$('#rMine').onclick = () => {
  const h = myHero(), msg = $('#rMy');
  if (!h) {
    msg.innerHTML = 'Noch kein Charakter. <a href="../character/" id="rMake">Charakter zusammenstellen</a>';
    $('#rMake').onclick = e => { if (window.GabellaHero) { e.preventDefault(); GabellaHero.open(); } };
    return;
  }
  const f = RC[h.race].f, role = RR.includes(h.role) ? h.role : roleOpts(CL[h.cls])[0];
  if (f !== R.f) {
    if (R.s.some(Boolean)) { msg.textContent = 'Dein Charakter spielt für die andere Fraktion: Wechsle die Fraktion über den Rahmen.'; return; }
    R.f = f;
  }
  if (R.s.some(p => p && p.race === h.race && p.cls === h.cls && p.role === role && !p.name)) { msg.textContent = 'Dein Charakter ist schon in der Gruppe.'; return; }
  let i = R.s.findIndex(p => !p); if (i < 0) i = 0;
  R.s[i] = { race: h.race, cls: h.cls, role, name: '' };
  msg.textContent = ''; R.moving = -1; renderRaid();
};
$('#rClear').onclick = () => { R.s = Array(R.size).fill(null); R.moving = -1; renderRaid(); };
$('#rCopyLink').onclick = () => copyTo(teamLink(), $('#rMsg'), 'Link kopiert');
$('#rCopyText').onclick = () => copyTo(teamText(), $('#rMsg'), 'Gruppe kopiert');
$('#lfgD').onchange = e => { L.d = e.target.value; renderLfg(); };
$('#lfgS').addEventListener('click', e => { const b = e.target.closest('button'); if (b) { L.s = L.s === b.dataset.v ? '' : b.dataset.v; renderLfg(); } });
$('#rCopyLfg').onclick = () => { const t = lfgText(); copyTo(t, $('#rLfgMsg'), 'Text kopiert. ' + lfgLen(t)); };

function swap(a, b) { const t = R.s[a]; R.s[a] = R.s[b]; R.s[b] = t; }
$('#rview').addEventListener('click', e => {
  const b = e.target.closest('[data-i]'); if (!b) return;
  const i = +b.dataset.i;
  if (R.moving >= 0) { if (i !== R.moving) swap(R.moving, i); const to = i; R.moving = -1; renderRaid(); focusSlot(to); return; }
  if (!R.s[i]) { R.s[i] = newPlayer(i); fixPlayer(R.s[i]); renderRaid(); }
  openEditor(i);
});
$('#rhint').addEventListener('click', e => { if (e.target.id === 'mvCancel') { const i = R.moving; R.moving = -1; renderRaid(); focusSlot(i); } });
document.addEventListener('keydown', e => { if (e.key === 'Escape' && R.moving >= 0 && !$('#edDlg').open) { const i = R.moving; R.moving = -1; renderRaid(); focusSlot(i); } });
function focusSlot(i) { const el = document.querySelector(`#rview [data-i="${i}"]`); if (el) el.focus(); }

/* drag a frame onto another slot to swap them */
let dragFrom = -1;
$('#rview').addEventListener('dragstart', e => { const b = e.target.closest('[data-i]'); if (!b) return; dragFrom = +b.dataset.i; e.dataTransfer.effectAllowed = 'move'; try { e.dataTransfer.setData('text/plain', String(dragFrom)); } catch (x) {} b.classList.add('src'); });
$('#rview').addEventListener('dragover', e => { const b = e.target.closest('[data-i]'); if (b && dragFrom >= 0) { e.preventDefault(); document.querySelectorAll('#rview .over').forEach(x => x !== b && x.classList.remove('over')); b.classList.add('over'); } });
$('#rview').addEventListener('dragleave', e => { const b = e.target.closest('[data-i]'); if (b && !b.contains(e.relatedTarget)) b.classList.remove('over'); });
$('#rview').addEventListener('drop', e => { const b = e.target.closest('[data-i]'); if (!b || dragFrom < 0) return; e.preventDefault(); swap(dragFrom, +b.dataset.i); dragFrom = -1; renderRaid(); });
$('#rview').addEventListener('dragend', () => { dragFrom = -1; document.querySelectorAll('#rview .src, #rview .over').forEach(x => x.classList.remove('src', 'over')); });

/* frame editor */
const ed = $('#edDlg');
let edI = -1;
function fillEditor() {
  const p = R.s[edI];
  $('#edT').textContent = `Spieler ${edI + 1}` + (R.size > 5 ? ` · Gruppe ${Math.floor(edI / PARTY) + 1}` : '');
  $('#edRace').innerHTML = RACES.filter(r => r.f === R.f).map(r => `<option value="${r.id}"${r.id === p.race ? ' selected' : ''}>${esc(raceName(r))}${r.paid ? ' (bezahlt)' : ''}</option>`).join('');
  $('#edCls').innerHTML = Object.keys(RC[p.race].can).map(c => `<option value="${c}"${c === p.cls ? ' selected' : ''}>${esc(CL[c].n)}</option>`).join('');
  $('#edRole').innerHTML = roleOpts(CL[p.cls]).map(x => `<button type="button" data-v="${x}" aria-pressed="${x === p.role}">${ri(x)}${ROLE_RU[x]}</button>`).join('');
}
function openEditor(i) {
  edI = i; $('#edName').value = R.s[i].name || ''; fillEditor();
  if (ed.showModal) ed.showModal(); else ed.setAttribute('open', '');
}
const edP = () => ed.open && R.s[edI];   // the player in the open editor; autofill can fire input on the closed one
function edChanged() { fixPlayer(R.s[edI]); fillEditor(); renderRaid(); }
$('#edName').addEventListener('input', e => { const p = edP(); if (!p) return; p.name = cleanName(e.target.value); renderRaid(); });
$('#edRace').onchange = e => { const p = edP(); if (!p) return; p.race = e.target.value; edChanged(); };
$('#edCls').onchange = e => { const p = edP(); if (!p) return; p.cls = e.target.value; edChanged(); };
$('#edRole').addEventListener('click', e => { const b = e.target.closest('button'); const p = edP(); if (b && p) { p.role = b.dataset.v; edChanged(); } });
$('#edDel').onclick = () => { R.s[edI] = null; ed.close(); };
$('#edMove').onclick = () => { R.moving = edI; ed.close(); };
$('#edOk').onclick = $('#edClose').onclick = () => ed.close();
ed.addEventListener('close', () => { renderRaid(); focusSlot(R.moving >= 0 ? R.moving : edI); });
ed.addEventListener('click', e => { if (e.target === ed) ed.close(); });

/* ---------- Compare ---------- */
const C = { mode: 'class', cls: ['warrior', 'paladin'], race: ['human', 'orc'] };
const SPEC_SEP = ' — ';
function pickToggle(list, id) {
  const k = list.indexOf(id);
  if (k >= 0) { if (list.length > 1) list.splice(k, 1); }
  else { list.push(id); if (list.length > 3) list.shift(); }
}
function renderPick() {
  syncSeg('cMode', C.mode);
  const box = $('#cPick'), sel = C.mode === 'class' ? C.cls : C.race;
  box.classList.toggle('races', C.mode === 'race');
  if (C.mode === 'class') box.innerHTML = CLASSES.map(c => { const k = sel.indexOf(c.id); return `<button type="button" class="cp" data-id="${c.id}" aria-pressed="${k >= 0}"><picture><source type="image/avif" srcset="${art(c.id, 'avif')}"><img src="${art(c.id)}" width="360" height="482" alt="" loading="lazy" decoding="async"></picture><span class="no">${k + 1}</span><b>${esc(c.n)}</b></button>`; }).join('');
  else box.innerHTML = ['alliance', 'horde'].map(f => `<div class="rside ${f}"><h3>${FAC[f]}</h3>${RACES.filter(r => r.f === f).map(r => { const k = sel.indexOf(r.id); return `<button type="button" class="rp" data-id="${r.id}" aria-pressed="${k >= 0}">${esc(raceName(r))}${r.paid ? '<span class="tag paid">bezahlt</span>' : ''}<span class="no">${k + 1}</span></button>`; }).join('')}</div>`).join('');
  $('#cNote').textContent = `Gewählt ${sel.length} von 3`;
  fitCp();
}
/* Class names fit the picker card: --k is the width of the longest word in em, measured in the real font (the same idea as on the home page roster) */
function fitCp() {
  const els = document.querySelectorAll('#cPick .cp b');
  if (!els.length) return;
  const m = document.createElement('span');
  m.style.cssText = 'position:absolute;left:-9999px;top:0;visibility:hidden;white-space:pre;line-height:1;font-size:100px';
  document.body.append(m);
  let kmax = 0;   // the widest name sets the size of every card
  els.forEach(el => {
    const cs = getComputedStyle(el);
    m.style.fontFamily = cs.fontFamily; m.style.fontWeight = cs.fontWeight;
    kmax = Math.max(kmax, ...(el.textContent.match(/[^\s-]+-?/g) || ['']).map(t => (m.textContent = t, m.getBoundingClientRect().width / 100)));
  });
  els.forEach(el => el.style.setProperty('--k', kmax.toFixed(3)));
  m.remove();
}
if (document.fonts) document.fonts.addEventListener('loadingdone', fitCp);
const ul = (items, cls) => items.length ? `<ul${cls ? ` class="${cls}"` : ''}>${items.map(x => `<li>${x}</li>`).join('')}</ul>` : '<span class="none">Keine</span>';
const row = (lab, vals, extra) => `<div class="crow${extra ? ' ' + extra : ''}"><div class="lab${extra === 'tiprow' ? ' tl' : ''}">${lab}</div>${vals.map(v => `<div class="val">${v}</div>`).join('')}</div>`;
function renderCmp() {
  const out = [];
  if (C.mode === 'class') {
    const ids = C.cls;
    out.push(`<div class="crow chead"><div class="lab"></div>${ids.map(id => `<div class="val" style="--cc:${CCOL[id]}"><picture><source type="image/avif" srcset="${art(id, 'avif')}"><img src="${art(id)}" width="360" height="482" alt="" loading="lazy" decoding="async"></picture><b>${esc(CL[id].n)}</b><a href="${classUrl(id)}">Klassenseite<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>`).join('')}</div>`);
    out.push(row('Rollen', ids.map(id => CL[id].roles.map(r => `<span class="role">${ri(r)}${ROLE_RU[r]}</span>`).join(''))));
    out.push(row('Rüstung', ids.map(id => racx(CX[id].armor))));
    out.push(row('Waffen', ids.map(id => racx(CX[id].weapons))));
    out.push(row('Ressource', ids.map(id => esc(CX[id].resource))));
    out.push(row('Leveln', ids.map(id => esc(CX[id].lvl))));
    out.push(row('Spezialisierungen', ids.map(id => ul(CX[id].specs.map(s => `<b>${esc(s.n)}</b>${SPEC_SEP}<span class="sub">${esc(s.what)}</span>`)))));
    out.push(row('Raidbuff', ids.map(id => BUFF[id] ? esc(BUFF[id]) : '<span class="none">Keine</span>')));
    out.push(row('In der Gruppe', ids.map(id => ul(CX[id].group.map(esc)))));
    out.push(row('Berufe', ids.map(id => ul(CPROF[id].map(p => `<b>${esc(p[0])}</b>${p[1] ? `<br><span class="sub">${esc(p[1])}</span>` : ''}`)) + `<a class="cgo" href="${HOME}guides/professions/#pairs=${id}">Lagerobjekte und Skill<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a>`)));
    out.push(row('Stärken', ids.map(id => ul(CX[id].pros.map(esc), 'plus'))));
    out.push(row('Schwächen', ids.map(id => ul(CX[id].cons.map(esc), 'minus'))));
    ['alliance', 'horde'].forEach(f => out.push(row(`Völker: ${FAC[f]}`, ids.map(id => { const rs = RACES.filter(r => r.f === f && r.can[id]); return rs.length ? rs.map(r => `<a href="${raceUrl(r.id)}">${esc(raceName(r))}</a>`).join(', ') : '<span class="none">Keine</span>'; }))));
  } else {
    const ids = C.race;
    out.push(`<div class="crow chead"><div class="lab"></div>${ids.map(id => { const r = RC[id]; return `<div class="val race ${r.f}"><span class="fx">${FAC[r.f]}${r.paid ? ' · bezahlt' : ''}</span><b>${esc(raceName(r))}</b><a href="${raceUrl(id)}">Volksseite<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>`; }).join('')}</div>`);
    out.push(row('Klassen', ids.map(id => ul(Object.keys(RC[id].can).map(c => `<span style="color:${CCOL[c]}">●</span> ${esc(CL[c].n)}${RC[id].can[c] === 'new' ? ' <span class="tag new">neu</span>' : ''}`)))));
    out.push(row('Aktive Fähigkeiten', ids.map(id => ul(RC[id].rac.filter(x => x[0] === 'a').map(x => `<b>${esc(x[1])}</b><br><span class="sub">${racx(x[2])}</span>`)))));
    out.push(row('Passive Fähigkeiten', ids.map(id => ul(RC[id].rac.filter(x => x[0] === 'p').map(x => `<b>${esc(x[1])}</b><br><span class="sub">${racx(x[2])}</span>`)))));
    out.push(row('Tipp', ids.map(id => esc(RC[id].tip)), 'tiprow'));
  }
  const box = $('#cmp');
  box.style.setProperty('--n', C.mode === 'class' ? C.cls.length : C.race.length);
  box.innerHTML = out.join('');
}
$('#cMode').addEventListener('click', e => { const b = e.target.closest('button'); if (b) { C.mode = b.dataset.v; renderPick(); renderCmp(); } });
$('#cPick').addEventListener('click', e => {
  const b = e.target.closest('[data-id]'); if (!b) return;
  pickToggle(C.mode === 'class' ? C.cls : C.race, b.dataset.id);
  renderPick(); renderCmp();
  const nb = document.querySelector(`#cPick [data-id="${b.dataset.id}"]`); if (nb) nb.focus();
});

/* ---------- Page chrome ---------- */
const themeBtns = document.querySelectorAll('.themebtn');
function paintTheme() { const t = document.documentElement.getAttribute('data-theme'); themeBtns.forEach(b => b.querySelector('use').setAttribute('href', t === 'light' ? '#i-moon' : '#i-sun')); const m = document.querySelector('meta[name="theme-color"]'); if (m) m.setAttribute('content', t === 'light' ? '#fbfaf7' : '#050505'); }
themeBtns.forEach(b => b.onclick = () => { const t = document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light'; document.documentElement.setAttribute('data-theme', t); try { localStorage.setItem('wf-theme', t); } catch (e) {} paintTheme(); });
paintTheme();
const topbar = $('#topbar');
let barTick = false;
function paintBar() { topbar.classList.toggle('solid', window.scrollY > 24); barTick = false; }
window.addEventListener('scroll', () => { if (!barTick) { barTick = true; requestAnimationFrame(paintBar); } }, { passive: true });
paintBar();
const dlg = $('#moreDlg');
const moreX = on => document.querySelectorAll('[aria-controls="moreDlg"]').forEach(b => b.setAttribute('aria-expanded', on));
document.querySelectorAll('.menubtn, .morebtn').forEach(b => b.onclick = () => { if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', ''); moreX(true); });
dlg.addEventListener('close', () => moreX(false));
$('#moreClose').onclick = () => dlg.close();
dlg.addEventListener('click', e => { if (e.target === dlg || e.target.closest('.toc a')) dlg.close(); });

/* ---------- Picker: race and class (on the home page until 25.10; class and race pages link tools/#pick=…) ---------- */
function facName(f) { return f === 'alliance' ? 'Allianz' : 'Horde'; }
function bi(ru) { return EN[ru] && EN[ru] !== ru ? `${esc(ru)} <span class="en">(${esc(EN[ru])})</span>` : esc(ru); }
function raceEn(r) { return r.en ? ` <span class="en">/ ${esc(r.en)}</span>` : ''; }
const tipBox = h => `<div class="tipbox"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg><p><span class="tl">Tipp</span>${h}</p></div>`;
function face(id, cc, cls = '', title = '', f) { return `<span class="av ${cls}" style="--cc:${cc}"${title ? ` title="${esc(title)}"` : ''}><img src="${ROOT}assets/art/${porId(id, f)}-face.webp${PV}" width="160" height="160" alt="" loading="lazy" decoding="async"></span>`; }
function lvlMeter(c) {
  const p = c.lp || 0, w = Math.min(Math.abs(p) / 12 * 46, 46);
  const label = p < 0 ? `Schneller um ${-p}%` : p > 0 ? `Langsamer um ${p}%` : 'Durchschnittstempo';
  const bar = p ? `<i class="${p > 0 ? 'slow' : ''}" style="${p < 0 ? 'right' : 'left'}:50%;width:${w}%"></i>` : '';
  return `<span class="lvl"><span>${label}</span><span class="bar" role="img" aria-label="${label}">${bar}</span><span class="scale" aria-hidden="true"><span>schneller</span><span>langsamer</span></span></span>`;
}
const state = { f:'all', r:'all', race:'dwarf', cls:'shaman', spec:'elemental' };
function mySide() { if (window.GabellaPor && GabellaPor.side[state.race])GabellaPor.set(GabellaPor.side[state.race]); }   // the race the reader picks is his side for the whole site (GabellaPor)

function roleMatch(c, role) { return role === 'all' || c.roles.includes(role); }
function raceVisible(r) { return state.f === 'all' || r.f === state.f; }
function roleChips(c) { return c.roles.map(x => `<span class="chip ${state.r === x ? 'on' : ''} ${x.endsWith('?') ? 'q' : ''}">${ri(x)}${ROLE_RU[x]}</span>`).join(''); }

function pickValid() {
  let r = RC[state.race];
  if (!raceVisible(r)) { r = RACES.find(raceVisible); state.race = r.id; }
  if (!r.can[state.cls]) { state.cls = Object.keys(r.can).find(c => roleMatch(CL[c], state.r)) || Object.keys(r.can)[0]; }
  const sid = HC.sid[state.cls];   // the spec: kept when it is the class's, else the first one of the chosen role
  if (!sid.includes(state.spec)) state.spec = sid[CL[state.cls].specs.findIndex(s => state.r === 'all' || s[2].includes(state.r))] || sid[0];
}
/* Best race of the class and spec on a faction (the Best race guide): the picker stars it and says why in one line */
const pickBest = f => { const b = bestOf(state.cls, f, state.spec); return b ? b[0] : []; };
function pickClass(id) {
  state.cls = id;
  if (!HC.sid[id].includes(state.spec)) state.spec = '';
  if (!RC[state.race].can[id]) { const r = RACES.filter(raceVisible).find(x => x.can[id]) || RACES.find(x => x.can[id]); if (r) state.race = r.id; }
  pickRace();
  if (!raceVisible(RC[state.race])) { state.f = 'all'; syncSeg('segF', 'all'); }
}

function renderMatrix() {
  let h = '<thead><tr><th scope="col">Volk</th>';
  CLASSES.forEach(c => { h += `<th scope="col" class="${roleMatch(c, state.r) ? '' : 'dim'}${c.id === state.cls ? ' selc' : ''}">${face(c.id, CCOL[c.id])}${esc(c.n)}</th>`; });
  h += '</tr></thead><tbody>';
  ['alliance', 'horde'].forEach(f => {
    const rows = RACES.filter(r => r.f === f && raceVisible(r));
    if (!rows.length) return;
    h += `<tr class="fh ${f}"><th colspan="${CLASSES.length + 1}" scope="rowgroup"><span class="f ${f}"></span>${facName(f)}</th></tr>`;
    rows.forEach(r => {
      h += `<tr class="${r.id === state.race ? 'rowsel' : ''}"><th scope="row"><span class="rn">${face(RSLUG[r.id], `var(--${r.f})`)}${esc(r.n)}${r.paid ? '<span class="paid">bezahlt</span>' : ''}</span></th>`;
      CLASSES.forEach(c => {
        const v = r.can[c.id];
        const dim = roleMatch(c, state.r) ? '' : ' dim';
        if (!v) { h += `<td><span class="cell no${dim}" role="img" aria-label="${esc(r.n)} ${esc(c.n)}: nicht erlaubt"></span></td>`; return; }
        const sel = (r.id === state.race && c.id === state.cls) ? ' sel' : '';
        const label = `${r.n} ${c.n}${v === 'new' ? ', neue Kombination' : ''}`;
        const mark = '<i><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 12.5l4 4 8-9" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></i>';
        h += `<td><button class="cell ${v}${dim}${sel}" style="--cc:${CCOL[c.id]}" data-r="${r.id}" data-c="${c.id}" aria-label="${esc(label)}" aria-pressed="${sel ? 'true' : 'false'}">${mark}</button></td>`;
      });
      h += '</tr>';
    });
  });
  const mx = $('#matrix');
  mx.innerHTML = h + '</tbody>';
  mx._hc = -1;
}
/* Crosshair: the hovered cell lights up its row (CSS) and its column (here) */
(function () {
  const mx = document.getElementById('matrix');
  const mark = i => {
    if (i === mx._hc) return;
    mx._hc = i;
    mx.querySelectorAll('.hcol').forEach(x => x.classList.remove('hcol'));
    if (i > 0) mx.querySelectorAll(`thead th:nth-child(${i + 1}), tbody tr:not(.fh) > :nth-child(${i + 1})`).forEach(x => x.classList.add('hcol'));
  };
  mx.addEventListener('mouseover', e => { const td = e.target.closest('td'); mark(td ? td.cellIndex : -1); });
  mx.addEventListener('mouseleave', () => mark(-1));
})();

/* After a class or spec: the best race of the shown faction (of the current race's faction when both are shown) */
function pickRace() {
  pickValid();
  const f = state.f !== 'all' ? state.f : RC[state.race].f, best = pickBest(f);
  if (best.length && !best.includes(state.race)) state.race = best[0];
}
function renderPickM() {
  const TXH = HC.tx, c = CL[state.cls], sid = HC.sid[state.cls];
  const cls = CLASSES.filter(x => roleMatch(x, state.r)).map(x => `<button type="button" data-pc="${x.id}" aria-pressed="${x.id === state.cls}">${esc(x.n)}</button>`).join('');
  const specs = c.specs.map((s, i) => `<button type="button" data-ps="${sid[i]}" aria-pressed="${sid[i] === state.spec}">${esc(HC.sn[state.cls][i])}</button>`).join('');
  const races = RACES.filter(x => raceVisible(x) && x.can[state.cls]).map(x => { const b = pickBest(x.f).includes(x.id);
    return `<button type="button" data-pr="${x.id}" aria-pressed="${x.id === state.race}"><span class="f ${x.f}"></span>${esc(x.n)}${b ? ` <span class="pstar" title="${esc(TXH.best)}">★</span>` : ''}</button>`; }).join('');
  const f = RC[state.race].f, bo = bestOf(state.cls, f, state.spec), sn = HC.sn[state.cls][sid.indexOf(state.spec)];
  const why = bo ? `<p class="pwhy"><b>★ ${esc(TXH.bestFor.replace('%s', sn))}${state.f === 'all' ? ` (${esc(HC.fn[f])})` : ''}: ${esc(bo[0].map(x => HC.rn[x]).join(` ${TXH.or} `))}.</b> ${esc(bo[1])}</p>` : '';
  $('#pickm').innerHTML = `<div><div class="lbl">1. ${esc(TXH.cls)}</div><div class="chiprow">${cls}</div></div>
    <div><div class="lbl">2. ${esc(TXH.spec)}</div><div class="chiprow">${specs}</div></div>
    <div><div class="lbl">3. ${esc(TXH.race)}</div><div class="chiprow">${races}</div>${why}</div>`;
}

function renderDetail() {
  const r = RC[state.race], c = CL[state.cls], isNew = r.can[c.id] === 'new';
  const specs = c.specs.map(s => {
    const hit = state.r !== 'all' && s[2].includes(state.r) ? ' on' : '';
    return `<div class="card${hit}" style="--cc:${CCOL[c.id]}"><span class="rc">${ri(s[2][0])}</span><b>${bi(s[0])}</b><span>${esc(s[1])}</span></div>`;
  }).join('');
  const rac = r.rac.map(x => `<div class="card ab"><span class="abt${x[0] === 'a' ? '' : ' p'}">${x[0] === 'a' ? 'Aktiv' : 'Passiv'}</span><b>${bi(x[1])}</b><span>${racx(x[2])}</span></div>`).join('');
  const text = `${r.name || r.n} ${c.n} (${facName(r.f)})${r.paid ? ', Skyborne-Paket nötig' : ''}`;
  $('#detail').innerHTML = `
    <div class="d-head">
      <div class="d-art" aria-hidden="true"><picture><source type="image/avif" srcset="${ROOT}assets/art/${RSLUG[r.id]}-600.avif${PV}"><img src="${ROOT}assets/art/${RSLUG[r.id]}-600.webp${PV}" width="600" height="804" alt="" loading="lazy" decoding="async"></picture></div>
      <div class="d-avs">${face(RSLUG[r.id], `var(--${r.f})`)}</div>
      <div class="d-title"><h3>${esc(r.n)}${raceEn(r)} · ${esc(c.n)}</h3>
        <div class="chips"><span class="tag ${r.f}">${facName(r.f)}</span>${isNew ? '<span class="tag new">Neue Kombination</span>' : ''}${r.paid ? '<span class="tag paid">Bezahltes Volk</span>' : ''}${roleChips(c)}</div></div>
    </div>
    <div class="d-body">
      <div class="d-cols">
        <div><h4>Spezialisierungen</h4><div class="cards">${specs}</div></div>
        <div><h4>Volksfähigkeiten</h4><div class="cards two">${rac}</div></div>
      </div>
      <div class="facts3">
        <div class="fact"><h4>Leveln</h4>${lvlMeter(c)}</div>
        <div class="fact"><h4>In Raids</h4><span>${esc(c.raid)}.</span></div>
        <div class="fact"><h4>Was ist neu</h4><span>${esc(c.forever)}</span></div>
      </div>
      ${tipBox(esc(r.tip))}
      ${pickLinks(r, c)}
      <div class="copyrow">
        <input id="pickText" readonly value="${esc(text)}" aria-label="Meine Wahl">
        <button class="btn" id="copyBtn"><svg class="ico" aria-hidden="true"><use href="#i-copy"/></svg>Meine Wahl kopieren</button>
        <button class="btn ghost" id="shareBtn">Teilen</button>
        <span class="small" id="copyMsg" role="status"></span>
      </div>
    </div>`;
  $('#copyBtn').onclick = () => copyTo($('#pickText').value, $('#copyMsg'), 'Kopiert');
  $('#shareBtn').onclick = () => shareBuild(r.id, c.id, state.spec, text);
}
/* Share: the link of the card page b/<race>-<class>-<spec>/ (its preview is the card with the name); on a phone the share sheet, else the clipboard */
function shareBuild(race, cls, spec, text) {
  const url = new URL(`${HOME}b/${BSLUG[race] || race}-${cls}-${spec}/`, location.href).href, msg = $('#copyMsg');
  if (navigator.share && matchMedia('(pointer: coarse)').matches) navigator.share({ title: text, url }).catch(e => { if (e && e.name !== 'AbortError') copyTo(url, msg, 'Link kopiert'); });
  else copyTo(url, msg, 'Link kopiert');
}

/* Three ways on from the chosen combination and «make it my character» (character/#set=, the hero of this browser) */
function pickLinks(r, c) {
  const TXH = HC.tx, sn = HC.sn[c.id][HC.sid[c.id].indexOf(state.spec)], h = readHero();
  const mine = h && h.race === r.id && h.cls === c.id && h.spec === state.spec;
  const a = (href, t) => `<a class="btn ghost" href="${HOME}${href}">${esc(t)}</a>`;
  return `<div class="plinks">${a(`guides/best-race/#${c.id}`, TXH.bestR)}${a(`guides/professions/#pairs=${c.id}`, TXH.pairs)}${a(`guides/builds-${c.id}/#${state.spec}`, `${TXH.build}: ${sn}`)}`
    + (mine ? `<a class="btn" href="${HOME}character/">${esc(TXH.made)}</a>` : `<a class="btn" href="${HOME}character/#set=${r.id}.${c.id}.${state.spec}">${esc(TXH.make)}</a>`) + '</div>';
}
function render() { pickValid(); renderMatrix(); renderPickM(); renderDetail(); }
function toPicker() { $('#detail').scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'nearest' }); }

document.addEventListener('click', e => {
  const seg = e.target.closest('#segF button, #segR button');
  if (seg) {
    const which = seg.parentElement.id === 'segF' ? 'f' : 'r';
    state[which] = seg.dataset.v; syncSeg(seg.parentElement.id, seg.dataset.v);
    render(); return;
  }
  const cell = e.target.closest('button.cell');
  if (cell) { state.race = cell.dataset.r; state.cls = cell.dataset.c; mySide(); render(); toPicker(); return; }
  const pr = e.target.closest('[data-pr]');
  if (pr) { state.race = pr.dataset.pr; mySide(); render(); return; }
  const ps = e.target.closest('[data-ps]');
  if (ps) { state.spec = ps.dataset.ps; pickRace(); render(); return; }
  const pc = e.target.closest('[data-pc]');
  if (pc) { pickClass(pc.dataset.pc); render(); return; }
});
{ const h = readHero(); if (h && RC[h.race] && RC[h.race].can[h.cls]) Object.assign(state, { race: h.race, cls: h.cls, spec: h.spec || '' }); }
render();
/* ---------- Ping and queue advisor
: where the player is -> the WoW Forever region (Blizzard: Americas+Oceania, Europe, Korea, Taiwan) ---------- */
const PG = {
  eu: ['Europa', ''],
  cas: ['Europa', 'Kaukasus und Zentralasien haben keine eigene Region, am nächsten liegt Europa.'],
  mea: ['Europa', 'Naher Osten und Afrika haben keine eigene Region, am nächsten liegt Europa.'],
  na: ['Amerika und Ozeanien', ''],
  la: ['Amerika und Ozeanien', 'Lateinamerika spielt in der Region Amerika.'],
  oce: ['Amerika und Ozeanien', 'Blizzard fasst Ozeanien mit Amerika zu einer Region zusammen. Ob es Server in Ozeanien selbst gibt, hat Blizzard nicht gesagt.'],
  kr: ['Korea', ''],
  tw: ['Taiwan', ''],
  asia: ['', 'Eine eigene Region gibt es nicht. Am nächsten liegen Taiwan und Korea. Nimm die mit der geringeren World-Latenz.'],
};
function renderPing() {
  const v = $('#pgW').value, r = PG[v];
  try { if (v) localStorage.setItem('gabella-ping', v); } catch (e) {}
  if (!r) { $('#pgOut').innerHTML = ''; return; }
  $('#pgOut').innerHTML = (r[0] ? `<p class="preg">Deine Region: ${esc(r[0])}</p>` : '') + '<ul class="verdict">'
    + (r[1] ? `<li>${esc(r[1])}</li>` : '')
    + '<li>Es gibt keine Realms: Du wählst Region und Regelsatz, keinen Server. Die Region wählst du in Battle.net vor dem Spielstart.</li>'
    + '<li>Jede Region hat eigene Charaktere und Namen. Zusammen spielen geht nur innerhalb einer Region.</li>'
    + '<li>Wo die Server der Regionen stehen, hat Blizzard nicht gesagt.</li></ul>';
}
$('#pgW').onchange = renderPing;
try { const v = localStorage.getItem('gabella-ping'); if (v && PG[v]) $('#pgW').value = v; } catch (e) {}
renderPing();

/* Deep link from class pages: #pick=shaman or #pick=dwarf.shaman */
(function () {
  const m = location.hash.match(/^#pick=(?:(\w+)\.)?(\w+)(?:\.([\w-]+))?$/);   // class, race.class, race.class.spec (the share page b/<race>-<class>-<spec>/ sends the last)
  if (!m || !CL[m[2]]) return;
  if (m[1] && RC[m[1]] && RC[m[1]].can[m[2]]) { state.race = m[1]; state.cls = m[2]; if (m[3] && HC.sid[m[2]].includes(m[3])) state.spec = m[3]; } else pickClass(m[2]);
  state.f = 'all'; state.r = 'all'; syncSeg('segF', 'all'); syncSeg('segR', 'all'); render();
  setTimeout(() => document.getElementById('picker').scrollIntoView(), 0);
})();

const fromLink = /^#(team|t)=/.test(location.hash);
if (!readShort()) readHash();
renderRaid(fromLink); renderPick(); renderCmp();
if (fromLink) $('#raid').scrollIntoView();
addEventListener('hashchange', () => {   // a link pasted into an already open tab: load the group as on a fresh load
  if (!/^#(team|t)=/.test(location.hash)) return;
  if (!readShort()) readHash();
  renderRaid(true); $('#raid').scrollIntoView();
});
const openSearch = () => { const b = document.querySelector('.srchbtn'); if (b) b.click(); };   // the site search (assets/search/)
const q0 = new URLSearchParams(location.search).get('q');   // tools/?q=... opens it with the query, once search.js (deferred) is in
if (q0) addEventListener('DOMContentLoaded', () => {
  openSearch();
  const i = document.querySelector('dialog.srch input');
  if (i) { i.value = q0.slice(0, 60); i.dispatchEvent(new Event('input')); }
});
