const HOME = '';   // language home, the classes/ and races/ pages set their own
/* ref:start — shared with the classes/ and races/ pages (build_guides.ref_js); no $ or esc here, every page defines its own */
const CLASSES = [
  { id:'warrior', n:'Guerriero', s:'Guerriero', roles:['tank','dps'],
    specs:[['Armi','Danni in mischia (arma a due mani)',['dps']],['Furia','Danni in mischia (due armi)',['dps']],['Protezione','Difensore',['tank']]],
    lvl:'Il livellamento più lento, circa il 12% più lungo della media (stima di LFCarry)',
    lp:12,
    raid:'Urlo di Battaglia agisce su tutta l’incursione',
    forever:'Più Rabbia, minaccia migliore su gruppi di bersagli, il talento Weapon Master. Furia e Sete di Sangue sono indebolite.' },
  { id:'paladin', n:'Paladino', roles:['tank','heal','dps'],
    specs:[['Sacro','Guaritore',['heal']],['Protezione','Difensore',['tank']],['Castigo','Danni in mischia',['dps']]],
    lvl:'Ritmo di livellamento nella media',
    lp:0,
    raid:'Benedizione dei Re ora è di base. Secondo le classifiche della beta, Protezione è tra i difensori più forti, mentre Castigo è sceso dopo la patch del 15 ottobre.',
    forever:'Assalto Sacro dal livello 6, Giudizio non consuma il sigillo. I Non Morti ora possono essere paladini, quindi la classe è arrivata nell’Orda.' },
  { id:'hunter', n:'Cacciatore', roles:['dps'],
    specs:[['Affinità Animale','Danni a distanza, molti danni dal famiglio',['dps']],['Precisione','Danni a distanza',['dps']],['Sopravvivenza','Mischia e distanza, trappole',['dps']]],
    lvl:'Il livellamento più veloce, circa l’8% più rapido della media (stima di LFCarry)',
    lp:-8,
    raid:'Aura di Precisione agisce su tutta l’incursione',
    forever:'Puoi giocare senza famiglio, le trappole funzionano in combattimento, le volpi sono arrivate come famiglia di famigli. Sopravvivenza può giocare in mischia.' },
  { id:'rogue', n:'Ladro', roles:['dps'],
    specs:[['Assassinio','Danni da veleno',['dps']],['Combattimento','Attacchi rapidi con l’arma',['dps']],['Scaltrezza','Imboscate, sanguinamenti',['dps']]],
    lvl:'Ritmo di livellamento nella media',
    lp:0,
    raid:'Puri danni in mischia, senza potenziamenti per l’incursione',
    forever:'Ora può usare asce a una mano. Assassinio si basa sui veleni, Scaltrezza su sanguinamenti e furtività.' },
  { id:'priest', n:'Sacerdote', roles:['heal','dps'],
    specs:[['Disciplina','Guaritore, scudi e assorbimento',['heal']],['Sacro','Guaritore',['heal']],['Ombra','Danni a distanza',['dps']]],
    lvl:'Circa il 5% più lento della media (stima di LFCarry)',
    lp:5,
    raid:'Spirito Divino ora è di base. I danni d’Ombra e Piaga Divoratrice (recupero di 24 s) sono stati potenziati dalla patch del 15 ottobre.',
    forever:'Protezione dalla Paura e Piaga Divoratrice sono disponibili dal livello 20 per tutte le razze. Ogni razza ha due incantesimi da sacerdote propri.' },
  { id:'shaman', n:'Sciamano', roles:['heal','dps','tank?'],
    specs:[['Elementale','Danni a distanza',['dps']],['Potenziamento','Danni in mischia. Il ruolo da difensore è ancora in dubbio',['dps','tank?']],['Rigenerazione','Guaritore',['heal']]],
    lvl:'Ritmo di livellamento nella media',
    lp:0,
    raid:'I totem Forza della Terra, Furia del Vento, Lingua di Fuoco e Grazia dell’Aria potenziano il proprio gruppo',
    forever:'I Nani ora possono essere sciamani, quindi la classe è arrivata nell’Alleanza. Getto di Lava è stata potenziata, Elementale è salito nelle classifiche dei danni.' },
  { id:'mage', n:'Mago', roles:['dps'],
    specs:[['Arcano','Danni esplosivi, molto mana',['dps']],['Fuoco','Critici e incendi',['dps']],['Gelo','Danni e controllo',['dps']]],
    lvl:'Il livellamento più veloce, circa l’8% più rapido della media, circa 12 ore risparmiate (stima di LFCarry)',
    lp:-8,
    raid:'Portali, cibo e acqua per il gruppo',
    forever:'Fuoco ha ottenuto Serie Bollente, Arcano Detonazione Arcana, Gelo Lancia di Ghiaccio. Palla di Fuocogelo è disponibile dal livello 40.' },
  { id:'warlock', n:'Stregone', roles:['dps'],
    specs:[['Afflizione','Danni da maledizioni e corruzione',['dps']],['Demonologia','Danni tramite demoni',['dps']],['Distruzione','Danni diretti da fuoco e ombra',['dps']]],
    lvl:'Ritmo di livellamento nella media',
    lp:0,
    raid:'Maestria oscura dà il 2–10% di danni Ombra, come in Classic (nella prima beta 1–5%)',
    forever:'Afflizione ha un nuovo incantesimo canalizzato, il demone resta con Sacrificio Demoniaco, Distruzione ha ottenuto Incenerimento e danni ad area.' },
  { id:'druid', n:'Druido', roles:['tank','heal','dps'],
    specs:[['Equilibrio','Danni a distanza',['dps']],['Aggressore Ferino','Difensore (orso) e danni in mischia (gatto)',['tank','dps']],['Rigenerazione','Guaritore, molte cure nel tempo',['heal']]],
    lvl:'Circa il 5% più lento della media (stima di LFCarry)',
    lp:5,
    raid:'Capobranco e Aura del Lunagufo agiscono su tutta l’incursione e si sommano',
    forever:'Ogni specializzazione ha un ruolo chiaro, le forme funzionano con pozioni e incantamenti delle armi. Puoi essere difensore, guaritore e combattente con un solo personaggio.' }
];
const ROLE_RU = { tank:'Difensore', heal:'Guaritore', dps:'Assaltatore', 'tank?':'Difensore (incerto)' };
const ri = r => `<svg class="ri" aria-hidden="true"><use href="#i-${r.replace('?','')}"/></svg>`;
const CCOL = { warrior:'#c79c6e', paladin:'#f58cba', hunter:'#abd473', rogue:'#fff569', priest:'#e8e8e8', shaman:'#2f8cf0', mage:'#40c7eb', warlock:'#8788ee', druid:'#ff7d0a' };
const BUFF = { warrior:'Urlo di Battaglia', paladin:'Benedizione dei Re', hunter:'Aura di Precisione', priest:'Parola del Potere: Fermezza, Spirito Divino', shaman:'Totem (Forza della Terra, Furia del Vento, Lingua di Fuoco, Grazia dell’Aria)', mage:'Intelletto Arcano, portali, cibo e acqua', druid:'Marchio Selvaggio, Capobranco, Aura del Lunagufo' };

const RACES = [
  { id:'human', n:'Umano', f:'alliance',
    cls:['warrior','paladin','hunter*','rogue','priest','mage','warlock'],
    rac:[['a','Volontà di Sopravvivenza','Rimuove lo stordimento'],['a','Percezione','Rivela i nemici invisibili per 20 s'],['p','Ruthless','+1% probabilità di critico'],['p','Spirito Umano','+10% spirito']],
    tip:'Per un Sacerdote Sacro lo spirito si traduce in cure, quindi un sacerdote Umano è ottimo per curare.' },
  { id:'dwarf', n:'Nano', f:'alliance',
    cls:['warrior','paladin','hunter','rogue','priest','shaman*'],
    rac:[['a','Forma di Pietra','Immunità a sanguinamenti, veleni e malattie per 8 s e danni fisici ridotti'],['a','Trova Tesori','Mostra i forzieri vicini e dà una probabilità di oggetti extra nella maggior parte dei forzieri'],['p','Artisan’s Precision','+1% di probabilità di colpire con incantesimi e attacchi'],['p','Big Game Hunter','+5% danni alle bestie']],
    tip:'Forma di Pietra è utile ai difensori e nel PvP.' },
  { id:'nightelf', n:'Elfo della Notte', f:'alliance',
    cls:['warrior','hunter','rogue','priest','druid'],
    rac:[['a','Luce di Elune','+10% probabilità di critico per 15 s'],['a','Fondersi nelle Ombre','Invisibilità sul posto'],['p','Rapidità','+2% di schivata e di velocità di corsa (Warcraft Tavern indica il 1% di schivata) {beta}'],['p','Spirito di Fuoco Fatuo','+75% di velocità di corsa da spirito (Warcraft Tavern indica il 25%) {beta}']],
    tip:'L’unica razza dell’Alleanza con il druido, a meno di scegliere gli Skyborne.' },
  { id:'gnome', n:'Gnomo', f:'alliance',
    cls:['warrior','rogue','mage','warlock','priest*'],
    rac:[['a','Artista della Fuga','Breve immunità a rallentamenti e immobilizzazioni'],['a','Eureka!','Per 8 s le abilità costano meno e sono più forti del 10% {beta}'],['p','Apertura Mentale','+5% mana, rabbia o energia massimi'],['p','Specializzazione: Ingegneria','I congegni d’ingegneria funzionano in modo più affidabile']],
    tip:'Apertura Mentale aiuta soprattutto le classi a energia.' },
  { id:'skyA', n:'Skyborne (Alleanza)', f:'alliance', paid:true, name:'Skyborne dell’High Order',
    cls:['warrior','hunter','rogue','mage','druid'],
    rac:[['a','Walk on Air','Plani per 10 s, senza danni da caduta'],['a','Read Ley Line','Rigenerazione di salute e mana +50% per 15 s. A una Ley Line anche Attuned per 1 ora: +100%, resta dopo la morte'],['p','Wind Blessed','+2% velocità d’attacco e degli incantesimi'],['p','Elemental Insight','+5% danni agli elementali']],
    tip:'Razza a pagamento: Heroic Pack da $29.99. Inizia nella zona di Zephras Isle (livelli 1–12).' },
  { id:'orc', n:'Orco', f:'horde',
    cls:['warrior','hunter','rogue','shaman','warlock','mage*'],
    rac:[['a','Furia Sanguinaria','+10% potenza d’attacco e potere magico per 15 s'],['a','Shatter Curse','Rimuove maledizioni e corruzione, −5% di danni magici subiti per 8 s'],['p','Command','+5% danni dei famigli di stregone e cacciatore'],['p','Audacia','Stordimenti più brevi del 20%']],
    tip:'Furia Sanguinaria offre una potente finestra di danni.' },
  { id:'undead', n:'Non Morto', f:'horde',
    cls:['warrior','rogue','mage','priest','warlock','paladin*'],
    rac:[['a','Volontà dei Reietti','Rimuove ammaliamento, paura e sonno'],['a','Cannibalismo','Ripristina nel tempo il 35% di salute e mana'],['p','Respiro Subacqueo','Respiri più a lungo sott’acqua'],['p','Tocco Tombale','Probabilità di sottrarre salute quando attacchi']],
    tip:'Nuova combinazione: un paladino per l’Orda, dove prima questa classe non esisteva.' },
  { id:'tauren', n:'Tauren', f:'horde',
    cls:['warrior','hunter','shaman','druid'],
    rac:[['a','Urto di Guerra','Stordisce i nemici vicini per 2 s, ricarica 90 s'],['a','Coltivazione','Fa crescere erbe raccoglibili senza Erbalismo, ricarica 15 min'],['p','Vagapianure','Finché ti muovi, la velocità di corsa sale del 2% per accumulo, fino a +60%. Non influisce sulla velocità in sella'],['p','Vigore','+5% salute']],
    tip:'L’unica razza dell’Orda con il druido, a meno di scegliere gli Skyborne.' },
  { id:'troll', n:'Troll', f:'horde',
    cls:['warrior','hunter','rogue','priest','shaman','mage','warlock*'],
    rac:[['a','Berserker','+10% di velocità di attacco e incantesimi per 12 s, ricarica di 3 min'],['a','Rapid Regeneration','Ripristina salute nel tempo'],['p','Cacciatore di Bestie','+5% danni alle bestie'],['p','Rigenerazione','La salute si rigenera anche in combattimento']],
    tip:'Più scelte di classe di tutta l’Orda: sette.' },
  { id:'skyH', n:'Skyborne (Orda)', f:'horde', paid:true, name:'Skyborne Windshaper',
    cls:['warrior','hunter','rogue','shaman','druid'],
    rac:[['a','Walk on Air','Plani per 10 s, senza danni da caduta'],['a','Skysight','+15% velocità di corsa per 15 s. A una Elemental Convergence anche Charged per 1 ora: +30%, resta dopo la morte'],['p','Wind Blessed','+2% velocità d’attacco e degli incantesimi'],['p','Elemental Insight','+5% danni agli elementali']],
    tip:'Razza a pagamento: Heroic Pack da $29.99. Solo nell’Orda può essere sciamano, solo nell’Alleanza mago.' }
];
RACES.forEach(r => { r.can = {}; r.cls.forEach(c => { const isNew = c.endsWith('*'); r.can[isNew ? c.slice(0,-1) : c] = isNew ? 'new' : 'ok'; }); });
const CL = Object.fromEntries(CLASSES.map(c => [c.id, c]));
const BETA = '<span class="beta-note">secondo i dati della beta</span>';
const BMARK = '{' + 'beta}';   // split so the guide build (which swaps the marker for the span everywhere) leaves it alone
const racx = s => String(s).split(BETA).join(BMARK).split(BMARK).map(esc).join(BETA);
const RC = Object.fromEntries(RACES.map(r => [r.id, r]));
const RLEAD = {"human": "La razza più numerosa dell’Alleanza. Versatile e forte nel PvP grazie a Volontà di Sopravvivenza.", "dwarf": "Robusti minatori e fucilieri di Forgiardente. Per la prima volta l’Alleanza ha degli sciamani, e sono nani: in Classic non c’erano.", "nightelf": "Un antico popolo delle foreste. Sfuggenti: un modo tutto loro per nascondersi, schivate e corsa veloce.", "gnome": "Gli inventori di Gnomeregan. Piccoli, astuti e con la migliore abilità di fuga del gioco.", "skyA": "Una nuova razza di Forever. L’High Order: elfi del vento in cerca della magia arcana perduta dei loro antenati.", "orc": "Il cuore dell’Orda. I guerrieri più forti e maestri del PvP grazie a Furia Sanguinaria e Audacia.", "undead": "I Reietti: ex umani liberatisi dal Re dei Lich. Immuni a paura e sonno quando conta.", "tauren": "Pacifici giganti delle pianure. La salute più alta e uno stordimento ad area tutto loro.", "troll": "La tribù Lanciascura. Più classi di tutta l’Orda e un potente Berserker per i danni.", "skyH": "Una nuova razza di Forever. I Windshaper: guide spirituali degli Skyborne, vicini agli elementi."}; // race page leads and URL slugs, filled in by build.py
const RSLUG = {"human": "human", "dwarf": "dwarf", "nightelf": "night-elf", "gnome": "gnome", "skyA": "skyborne-alliance", "orc": "orc", "undead": "undead", "tauren": "tauren", "troll": "troll", "skyH": "skyborne-horde"};

const EN = {
  'Armi':'Arms','Furia':'Fury','Protezione':'Protection','Sacro':'Holy','Castigo':'Retribution',
  'Affinità Animale':'Beast Mastery','Precisione':'Marksmanship','Sopravvivenza':'Survival',
  'Assassinio':'Assassination','Combattimento':'Combat','Scaltrezza':'Subtlety',
  'Disciplina':'Discipline','Ombra':'Shadow','Elementale':'Elemental','Potenziamento':'Enhancement','Rigenerazione':'Restoration',
  'Arcano':'Arcane','Fuoco':'Fire','Gelo':'Frost','Afflizione':'Affliction','Demonologia':'Demonology','Distruzione':'Destruction',
  'Equilibrio':'Balance','Aggressore Ferino':'Feral',
  'Volontà di Sopravvivenza':'Will to Survive','Percezione':'Perception','Ruthless':'Ruthless','Spirito Umano':'The Human Spirit',
  'Forma di Pietra':'Stoneform','Trova Tesori':'Find Treasure','Earth Fury':'Earth Fury','Big Game Hunter':'Big Game Hunter',
  'Luce di Elune':"Elune’s Light",'Fondersi nelle Ombre':'Shadowmeld','Rapidità':'Quickness','Spirito di Fuoco Fatuo':'Wisp Spirit',
  'Artista della Fuga':'Escape Artist','Eureka!':'Eureka!','Apertura Mentale':'Expansive Mind','Specializzazione: Ingegneria':'Engineering Specialization',
  'Walk on Air':'Walk on Air','Read Ley Line':'Read Ley Line','Wind Blessed':'Wind Blessed','Elemental Insight':'Elemental Insight','Skysight':'Skysight',
  'Furia Sanguinaria':'Blood Fury','Shatter Curse':'Shatter Curse','Savage':'Savage','Command':'Command','Audacia':'Hardiness',
  'Volontà dei Reietti':'Will of the Forsaken','Cannibalismo':'Cannibalize','Respiro Subacqueo':'Underwater Breathing','Tocco Tombale':'Touch of the Grave',
  'Urto di Guerra':'War Stomp','Coltivazione':'Cultivation','Vagapianure':'Plainsrunning','Vigore':'Endurance',
  'Berserker':'Berserking','Rapid Regeneration':'Rapid Regeneration','Cacciatore di Bestie':'Beast Slaying','Rigenerazione':'Regeneration'
};
RC.skyA.en = 'High Order Skyborne'; RC.skyH.en = 'Windshaper Skyborne';
const tipBox = h => `<div class="tipbox"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg><p><span class="tl">Consiglio</span>${h}</p></div>`;
function bi(ru) { return EN[ru] && EN[ru] !== ru ? `${esc(ru)} <span class="en">(${esc(EN[ru])})</span>` : esc(ru); }
function raceEn(r) { return r.en ? ` <span class="en">/ ${esc(r.en)}</span>` : ''; }
function facName(f) { return f === 'alliance' ? 'Alleanza' : 'Orda'; }
const PV = /*PV*/'?v=03c9d4a0';   // ?v= of the class and race portraits, filled in by build.art_version (redrawn under the same names)
/* Round face avatar: assets/art/<id>-face.webp, ring colour cc */
/* A class face follows the reader's side (GabellaPor, build.por_js); f: a fixed side (the class faces of a race row) */
function face(id, cc, cls = '', title = '', f = '') { const P = window.GabellaPor, t = `../assets/art/{${id}}-face.webp${PV}`, live = P && P.map[id] && !f;
  return `<span class="av ${cls}" style="--cc:${cc}"${title ? ` title="${esc(title)}"` : ''}><img src="../assets/art/${P ? P.id(id, f) : id}-face.webp${PV}"${live ? ` data-por-src="${t}"` : ''} width="160" height="160" alt="" loading="lazy" decoding="async"></span>`; }
function lvlMeter(c) {
  const p = c.lp || 0, w = Math.min(Math.abs(p) / 12 * 46, 46);
  const label = p < 0 ? `Più veloce del ${-p}%` : p > 0 ? `Più lento del ${p}%` : 'Ritmo nella media';
  const bar = p ? `<i class="${p > 0 ? 'slow' : ''}" style="${p < 0 ? 'right' : 'left'}:50%;width:${w}%"></i>` : '';
  return `<span class="lvl"><span>${label}</span><span class="bar" role="img" aria-label="${label}">${bar}</span><span class="scale" aria-hidden="true"><span>più veloce</span><span>più lento</span></span></span>`;
}
function renderClassRef() {
  const roles = ['tank', 'heal', 'dps'];
  const head = `<div class="cmp-h" aria-hidden="true"><span>Classe</span><span class="rdots">${roles.map(x => `<span title="${ROLE_RU[x]}">${ri(x)}</span>`).join('')}</span><span>Livellamento</span><span>In incursione</span><span></span></div>`;
  const box = $('#classRef');
  box.innerHTML = head + CLASSES.map(c => `<div class="cmp-row" style="--cc:${CCOL[c.id]};--art:url('../assets/art/${window.GabellaPor ? GabellaPor.id(c.id) : c.id}-360.webp${PV}')">
    <span class="cmp-id">${face(c.id, CCOL[c.id])}<span><b><a class="cmp-a" href="${HOME}classes/${c.id}/">${esc(c.n)}</a></b><small>${c.specs.map(s => esc(s[0])).join(' · ')}</small></span></span>
    <span class="rdots" role="img" aria-label="Ruoli: ${c.roles.map(x => ROLE_RU[x]).join(', ')}">${roles.map(x => { const on = c.roles.includes(x), q = c.roles.includes(x + '?'); return `<span class="rdot${on ? ' on' : q ? ' q' : ''}" title="${ROLE_RU[q ? x + '?' : x]}">${ri(x)}</span>`; }).join('')}</span>
    ${lvlMeter(c)}
    <span class="cmp-d"><span class="cmp-txt" id="crt-${c.id}">${esc(c.raid)}</span><button type="button" class="cmp-more" aria-expanded="false" aria-controls="crt-${c.id}" aria-label="Mostra tutto" title="Mostra tutto"></button></span>
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
  const head = `<div class="cmp-h" aria-hidden="true"><span>Razza</span><span>Classi</span><span class="abl">Abilità <span class="abt">attiva</span><span class="abt p">passiva</span></span><span></span></div>`;
  $('#raceRef').innerHTML = ['alliance', 'horde'].map(f => `<div class="rgroup ${f}"><h3>${facName(f)}</h3>${head}` + RACES.filter(r => r.f === f).map(r => `<a class="cmp-row" href="${HOME}races/${RSLUG[r.id]}/" style="--cc:var(--${f});--art:url('../assets/art/${RSLUG[r.id]}-360.webp${PV}')">
    <span class="cmp-id">${face(RSLUG[r.id], `var(--${f})`)}<span><b>${esc(r.n)}${r.paid ? '<span class="paid">a pagamento</span>' : ''}</b>${r.en ? `<small>${esc(r.en)}</small>` : ''}</span></span>
    <span class="ccl" role="img" aria-label="Classi: ${Object.keys(r.can).map(id => CL[id].n).join(', ')}">${CLASSES.map(c => { const v = r.can[c.id]; return face(c.id, CCOL[c.id], v ? (v === 'new' ? 'nw' : '') : 'off', c.n + (v === 'new' ? ', nuova' : v ? '' : ', non disponibile'), f); }).join('')}</span>
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
    const wh = feed.slice(0, 2).map(x => ({ d: x.date, html: `<a class="nc" href="${esc(x.url)}" target="_blank" rel="noopener"><time datetime="${esc(x.date)}">${x.date.slice(8, 10)}.${x.date.slice(5, 7)}</time><b lang="en">${esc(x.title)}</b><span>${'Wowhead, in inglese'}</span></a>` }));
    const all = ours.concat(bz, wh).sort((a, b) => (a.d < b.d ? 1 : a.d > b.d ? -1 : (b.o || 0) - (a.o || 0))).slice(0, 3);
    if (all.some(x => wh.includes(x) || bz.includes(x))) row.innerHTML = all.map(x => x.html).join('');
  });
})();
/* #peoples: the races block of the old home (old links) lives on the races page now */
if (location.hash === '#peoples') location.replace('races/');
