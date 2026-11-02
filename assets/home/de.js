const HOME = '';   // language home, the classes/ and races/ pages set their own
/* ref:start — shared with the classes/ and races/ pages (build_guides.ref_js); no $ or esc here, every page defines its own */
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
const RLEAD = {"human": "Das zahlreichste Volk der Allianz. Vielseitig und stark im PvP dank Überlebenswille.", "dwarf": "Robuste Bergleute und Schützen aus Eisenschmiede. Zum ersten Mal hat die Allianz Schamanen, und das sind Zwerge: In Classic gab es sie nicht.", "nightelf": "Ein uraltes Volk der Wälder. Schwer zu fassen: eigenes Verstecken, Ausweichen und schnelles Laufen.", "gnome": "Die Erfinder von Gnomeregan. Klein, gerissen und mit der besten Fluchtfähigkeit im Spiel.", "skyA": "Ein neues Volk in Forever. Der High Order: Windelfen auf der Suche nach der verlorenen Arkanmagie ihrer Vorfahren.", "orc": "Das Herz der Horde. Die stärksten Krieger und PvP-Meister dank Kochendem Blut und Zähigkeit.", "undead": "Die Verlassenen: ehemalige Menschen, die sich vom Lichkönig befreit haben. Immun gegen Furcht und Schlaf, wenn es darauf ankommt.", "tauren": "Friedliche Riesen der Ebenen. Die meiste Gesundheit und eine eigene Flächenbetäubung.", "troll": "Der Stamm der Dunkelspeere. Die meisten Klassen der Horde und ein starkes Berserker für Schaden.", "skyH": "Ein neues Volk in Forever. Die Windshapers: spirituelle Anführer der Skyborne, den Elementen nah."}; // race page leads and URL slugs, filled in by build.py
const RSLUG = {"human": "human", "dwarf": "dwarf", "nightelf": "night-elf", "gnome": "gnome", "skyA": "skyborne-alliance", "orc": "orc", "undead": "undead", "tauren": "tauren", "troll": "troll", "skyH": "skyborne-horde"};

const EN = {
  'Waffen':'Arms','Furor':'Fury','Schutz':'Protection','Heilig':'Holy','Vergeltung':'Retribution',
  'Tierherrschaft':'Beast Mastery','Treffsicherheit':'Marksmanship','Überleben':'Survival',
  'Meucheln':'Assassination','Kampf':'Combat','Täuschung':'Subtlety',
  'Disziplin':'Discipline','Schatten':'Shadow','Elementar':'Elemental','Verstärkung':'Enhancement','Wiederherstellung':'Restoration',
  'Arkan':'Arcane','Feuer':'Fire','Frost':'Frost','Gebrechen':'Affliction','Dämonologie':'Demonology','Zerstörung':'Destruction',
  'Gleichgewicht':'Balance','Wilder Kampf':'Feral',
  'Überlebenswille':'Will to Survive','Wachsamkeit':'Perception','Ruthless':'Ruthless','Unbeugsamkeit':'The Human Spirit',
  'Steingestalt':'Stoneform','Schatzsucher':'Find Treasure','Earth Fury':'Earth Fury','Big Game Hunter':'Big Game Hunter',
  'Elunes Licht':"Elune’s Light",'Schattenmimik':'Shadowmeld','Schnelligkeit':'Quickness','Irrwischgeist':'Wisp Spirit',
  'Entfesselungskünstler':'Escape Artist','Eureka!':'Eureka!','Wacher Geist':'Expansive Mind','Ingenieursspezialisierung':'Engineering Specialization',
  'Walk on Air':'Walk on Air','Read Ley Line':'Read Ley Line','Wind Blessed':'Wind Blessed','Elemental Insight':'Elemental Insight','Skysight':'Skysight',
  'Kochendes Blut':'Blood Fury','Shatter Curse':'Shatter Curse','Savage':'Savage','Befehlsgewalt':'Command','Zähigkeit':'Hardiness',
  'Wille der Verlassenen':'Will of the Forsaken','Kannibalismus':'Cannibalize','Unterwasseratmung':'Underwater Breathing','Berührung des Grabes':'Touch of the Grave',
  'Kriegsdonner':'War Stomp','Grüner Daumen':'Cultivation','Ebenenlaufen':'Plainsrunning','Durchhaltevermögen':'Endurance',
  'Berserker':'Berserking','Rasche Regeneration':'Rapid Regeneration','Wildtierschlächter':'Beast Slaying','Regeneration':'Regeneration'
};
RC.skyA.en = 'High Order Skyborne'; RC.skyH.en = 'Windshaper Skyborne';
const tipBox = h => `<div class="tipbox"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg><p><span class="tl">Tipp</span>${h}</p></div>`;
function bi(ru) { return EN[ru] && EN[ru] !== ru ? `${esc(ru)} <span class="en">(${esc(EN[ru])})</span>` : esc(ru); }
function raceEn(r) { return r.en ? ` <span class="en">/ ${esc(r.en)}</span>` : ''; }
function facName(f) { return f === 'alliance' ? 'Allianz' : 'Horde'; }
const PV = /*PV*/'?v=03c9d4a0';   // ?v= of the class and race portraits, filled in by build.art_version (redrawn under the same names)
/* Round face avatar: assets/art/<id>-face.webp, ring colour cc */
/* A class face follows the reader's side (GabellaPor, build.por_js); f: a fixed side (the class faces of a race row) */
function face(id, cc, cls = '', title = '', f = '') { const P = window.GabellaPor, t = `../assets/art/{${id}}-face.webp${PV}`, live = P && P.map[id] && !f;
  return `<span class="av ${cls}" style="--cc:${cc}"${title ? ` title="${esc(title)}"` : ''}><img src="../assets/art/${P ? P.id(id, f) : id}-face.webp${PV}"${live ? ` data-por-src="${t}"` : ''} width="160" height="160" alt="" loading="lazy" decoding="async"></span>`; }
function lvlMeter(c) {
  const p = c.lp || 0, w = Math.min(Math.abs(p) / 12 * 46, 46);
  const label = p < 0 ? `Schneller um ${-p}%` : p > 0 ? `Langsamer um ${p}%` : 'Durchschnittstempo';
  const bar = p ? `<i class="${p > 0 ? 'slow' : ''}" style="${p < 0 ? 'right' : 'left'}:50%;width:${w}%"></i>` : '';
  return `<span class="lvl"><span>${label}</span><span class="bar" role="img" aria-label="${label}">${bar}</span><span class="scale" aria-hidden="true"><span>schneller</span><span>langsamer</span></span></span>`;
}
function renderClassRef() {
  const roles = ['tank', 'heal', 'dps'];
  const head = `<div class="cmp-h" aria-hidden="true"><span>Klasse</span><span class="rdots">${roles.map(x => `<span title="${ROLE_RU[x]}">${ri(x)}</span>`).join('')}</span><span>Leveln</span><span>In Raids</span><span></span></div>`;
  const box = $('#classRef');
  box.innerHTML = head + CLASSES.map(c => `<div class="cmp-row" style="--cc:${CCOL[c.id]};--art:url('../assets/art/${window.GabellaPor ? GabellaPor.id(c.id) : c.id}-360.webp${PV}')">
    <span class="cmp-id">${face(c.id, CCOL[c.id])}<span><b><a class="cmp-a" href="${HOME}classes/${c.id}/">${esc(c.n)}</a></b><small>${c.specs.map(s => esc(s[0])).join(' · ')}</small></span></span>
    <span class="rdots" role="img" aria-label="Rollen: ${c.roles.map(x => ROLE_RU[x]).join(', ')}">${roles.map(x => { const on = c.roles.includes(x), q = c.roles.includes(x + '?'); return `<span class="rdot${on ? ' on' : q ? ' q' : ''}" title="${ROLE_RU[q ? x + '?' : x]}">${ri(x)}</span>`; }).join('')}</span>
    ${lvlMeter(c)}
    <span class="cmp-d"><span class="cmp-txt" id="crt-${c.id}">${esc(c.raid)}</span><button type="button" class="cmp-more" aria-expanded="false" aria-controls="crt-${c.id}" aria-label="Vollständig anzeigen" title="Vollständig anzeigen"></button></span>
    <span class="go" aria-hidden="true"><svg class="ico"><use href="#i-arrow"/></svg></span>
  </div>`).join('');
  /* the chevron: hidden (its place kept) where the note fits in 3 lines; checked again on resize and when the fonts arrive */
  const fit = () => box.querySelectorAll('.cmp-row:not(.open) .cmp-txt').forEach(t => t.nextElementSibling.classList.toggle('fits', t.scrollHeight <= t.clientHeight + 1));
  fit();
  if (!box.dataset.more) {
    box.dataset.more = '1';
    box.addEventListener('click', e => { const b = e.target.closest('.cmp-more'); if (!b) return;
      const open = b.getAttribute('aria-expanded') !== 'true'; b.setAttribute('aria-expanded', open); b.closest('.cmp-row').classList.toggle('open', open); });
    let q = 0; addEventListener('resize', () => { cancelAnimationFrame(q); q = requestAnimationFrame(fit); });
    if (document.fonts) document.fonts.ready.then(fit);
  }
}

function renderRaceRef() {
  const head = `<div class="cmp-h" aria-hidden="true"><span>Volk</span><span>Klassen</span><span class="abl">Fähigkeiten <span class="abt">aktiv</span><span class="abt p">passiv</span></span><span></span></div>`;
  $('#raceRef').innerHTML = ['alliance', 'horde'].map(f => `<div class="rgroup ${f}"><h3>${facName(f)}</h3>${head}` + RACES.filter(r => r.f === f).map(r => `<a class="cmp-row" href="${HOME}races/${RSLUG[r.id]}/" style="--cc:var(--${f});--art:url('../assets/art/${RSLUG[r.id]}-360.webp${PV}')">
    <span class="cmp-id">${face(RSLUG[r.id], `var(--${f})`)}<span><b>${esc(r.n)}${r.paid ? '<span class="paid">bezahlt</span>' : ''}</b>${r.en ? `<small>${esc(r.en)}</small>` : ''}</span></span>
    <span class="ccl" role="img" aria-label="Klassen: ${Object.keys(r.can).map(id => CL[id].n).join(', ')}">${CLASSES.map(c => { const v = r.can[c.id]; return face(c.id, CCOL[c.id], v ? (v === 'new' ? 'nw' : '') : 'off', c.n + (v === 'new' ? ', neu' : v ? '' : ', nicht verfügbar'), f); }).join('')}</span>
    <span class="abs">${r.rac.map(x => `<span><b class="${x[0] === 'a' ? '' : 'p'}">${bi(x[1])}</b><span>${racx(x[2])}</span></span>`).join('')}</span>
    <span class="go" aria-hidden="true"><svg class="ico"><use href="#i-arrow"/></svg></span>
  </a>`).join('') + '</div>').join('');
}
/* ref:end */
const $ = s => document.querySelector(s);
function esc(s) { return String(s).replace(/[&<>"]/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m])); }
const ROOT = '../';
document.addEventListener('click', e => {
  const a = e.target.closest('[data-q]');
  if (!a || e.ctrlKey || e.metaKey) return;
  e.preventDefault();
  const q = a.dataset.q, b = document.querySelector('.srchbtn');
  if (!globalThis.gabellaFind || !b) { location.href = a.getAttribute('href') + (q ? '?q=' + encodeURIComponent(q) : ''); return; }
  b.click();
  const i = document.querySelector('dialog.srch input');
  if (i && q) { i.value = q; i.dispatchEvent(new Event('input')); }
});
/* the search field: its index loads when the field comes into view or the pointer or focus reaches it, so that a tap
   opens the answers, not the loading line (phones have no hover) */
(() => {
  const f = document.querySelector('.hsrch');
  if (!f) return;
  let state = 0;   // 0 waiting, 1 waiting for search.js (it comes after this script), 2 loading
  const warm = () => {
    if (state === 2) return;
    if (globalThis.gabellaFind) { state = 2; globalThis.gabellaFind(''); return; }
    if (state === 0) { state = 1; let n = 0; const t = setInterval(() => { if (globalThis.gabellaFind || ++n > 40) { clearInterval(t); state = 0; if (globalThis.gabellaFind) warm(); } }, 250); }
  };
  ['pointerenter', 'pointerdown', 'focus'].forEach(t => f.addEventListener(t, warm, { passive: true }));
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => { if (es.some(x => x.isIntersecting)) { warm(); io.disconnect(); } });
    io.observe(f);
  }
})();
(() => {
  const row = document.querySelector('.hnews .row3');
  if (!row || !row.dataset.feed) return;
  const get = u => (u ? fetch(u).then(r => (r.ok ? r.json() : [])).catch(() => []) : Promise.resolve([]));
  /* official Blizzard notes first (data/official.json, level 1 of the news automation), then the Wowhead headlines */
  Promise.all([get(row.dataset.feed), get(row.dataset.off)]).then(([feed, off]) => {
    const ours = [...row.querySelectorAll('.nc')].map(n => ({ d: n.querySelector('time').getAttribute('datetime'), html: n.outerHTML }));
    const lang = (document.documentElement.lang || 'en').slice(0, 2);
    const pk = u => ((u || '').match(/\/t\/(?:[^/]+\/)?(\d+)\/(\d+)/) || []).slice(1).join('-') || u;   /* forum post: topic-post, any slug */
    const seen = new Set([...row.querySelectorAll('.nc[data-u]')].map(n => pk(n.dataset.u)));   /* a post we already wrote up is not repeated */
    const bz = (Array.isArray(off) ? off : []).filter(x => /^https:\/\//.test(x.url) && x.t && !seen.has(pk(x.url))).slice(0, 2).map(x => {
      const t = x.t[lang] || x.t.en;
      return { d: x.date, o: 1, html: `<a class="nc" href="${esc(x.url)}" target="_blank" rel="noopener"><time datetime="${esc(x.date)}">${x.date.slice(8, 10)}.${x.date.slice(5, 7)}</time><b${t.en ? ' lang="en"' : ''}>${esc(t.h)}</b><span>${esc(t.upd ? t.src + ' · ' + t.upd : t.src)}</span></a>` };
    });
    const wh = feed.slice(0, 2).map(x => ({ d: x.date, html: `<a class="nc" href="${esc(x.url)}" target="_blank" rel="noopener"><time datetime="${esc(x.date)}">${x.date.slice(8, 10)}.${x.date.slice(5, 7)}</time><b lang="en">${esc(x.title)}</b><span>${'Wowhead, auf Englisch'}</span></a>` }));
    const all = ours.concat(bz, wh).sort((a, b) => (a.d < b.d ? 1 : a.d > b.d ? -1 : (b.o || 0) - (a.o || 0))).slice(0, 3);
    if (all.some(x => wh.includes(x) || bz.includes(x))) row.innerHTML = all.map(x => x.html).join('');
  });
})();
/* #peoples: the races block of the old home (old links) lives on the races page now */
if (location.hash === '#peoples') location.replace('races/');
