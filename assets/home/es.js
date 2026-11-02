const HOME = '';   // language home, the classes/ and races/ pages set their own
/* ref:start — shared with the classes/ and races/ pages (build_guides.ref_js); no $ or esc here, every page defines its own */
const CLASSES = [
  { id:'warrior', n:'Guerrero', s:'Guerrero', roles:['tank','dps'],
    specs:[['Armas','Daño cuerpo a cuerpo (arma de dos manos)',['dps']],['Furia','Daño cuerpo a cuerpo (dos armas)',['dps']],['Protección','Tanque',['tank']]],
    lvl:'La subida más lenta, cerca de un 12 % más larga que la media (estimación de LFCarry)',
    lp:12,
    raid:'Grito de guerra afecta a toda la banda',
    forever:'Más ira, mejor amenaza contra grupos de objetivos, el talento Weapon Master. Furia y Sed de sangre se han debilitado.' },
  { id:'paladin', n:'Paladín', roles:['tank','heal','dps'],
    specs:[['Sagrado','Sanador',['heal']],['Protección','Tanque',['tank']],['Reprensión','Daño cuerpo a cuerpo',['dps']]],
    lvl:'Ritmo de subida medio',
    lp:0,
    raid:'Bendición de los Reyes ahora es básica. Según las listas de la beta, Protección está entre los tanques más fuertes, y Reprensión bajó tras el parche del 15 de octubre.',
    forever:'Holy Strike desde el nivel 6, Sentencia no consume el sello. Los no-muertos ya pueden ser paladines, así que la clase llega a la Horda.' },
  { id:'hunter', n:'Cazador', roles:['dps'],
    specs:[['Bestias','Daño a distancia, mucho daño de la mascota',['dps']],['Puntería','Daño a distancia',['dps']],['Supervivencia','Cuerpo a cuerpo y a distancia, trampas',['dps']]],
    lvl:'La subida más rápida, cerca de un 8 % más rápida que la media (estimación de LFCarry)',
    lp:-8,
    raid:'Aura de disparo certero afecta a toda la banda',
    forever:'Puedes jugar sin mascota, las trampas funcionan en combate y llegan los zorros como familia de mascotas. Supervivencia puede ir cuerpo a cuerpo.' },
  { id:'rogue', n:'Pícaro', roles:['dps'],
    specs:[['Asesinato','Daño con venenos',['dps']],['Combate','Ataques rápidos con arma',['dps']],['Sutileza','Emboscadas, sangrados',['dps']]],
    lvl:'Ritmo de subida medio',
    lp:0,
    raid:'Daño cuerpo a cuerpo puro sin beneficios para la banda',
    forever:'Ya puede usar hachas de una mano. Asesinato se basa en venenos, Sutileza en sangrados y sigilo.' },
  { id:'priest', n:'Sacerdote', roles:['heal','dps'],
    specs:[['Disciplina','Sanador, escudos y absorción',['heal']],['Sagrado','Sanador',['heal']],['Sombras','Daño a distancia',['dps']]],
    lvl:'Cerca de un 5 % más lento que la media (estimación de LFCarry)',
    lp:5,
    raid:'Espíritu divino ahora es básico. El daño de Sombras y Peste devoradora (24 s de reutilización) se mejoraron con el parche del 15 de octubre.',
    forever:'Custodia de miedo y Peste devoradora están disponibles desde el nivel 20 para cualquier raza. Cada raza tiene dos hechizos de sacerdote propios.' },
  { id:'shaman', n:'Chamán', roles:['heal','dps','tank?'],
    specs:[['Elemental','Daño a distancia',['dps']],['Mejora','Daño cuerpo a cuerpo. Su capacidad de tanque aún está en duda',['dps','tank?']],['Restauración','Sanador',['heal']]],
    lvl:'Ritmo de subida medio',
    lp:0,
    raid:'Los tótems Fuerza de la tierra, Viento Furioso, Lengua de Fuego y Gracia del aire mejoran a su grupo',
    forever:'Los enanos ya pueden ser chamanes, así que la clase llega a la Alianza. Ráfaga de lava se mejoró y Elemental subió en las clasificaciones de daño.' },
  { id:'mage', n:'Mago', roles:['dps'],
    specs:[['Arcano','Ráfagas, mucho maná',['dps']],['Fuego','Críticos e igniciones',['dps']],['Escarcha','Daño y control',['dps']]],
    lvl:'La subida más rápida, cerca de un 8 % más rápida que la media, unas 12 horas ahorradas (estimación de LFCarry)',
    lp:-8,
    raid:'Portales, comida y agua para el grupo',
    forever:'Fuego recibió Buena racha, Arcano Explosión Arcana, Escarcha Lanza de hielo. Descarga de Pirofrío está disponible desde el nivel 40.' },
  { id:'warlock', n:'Brujo', roles:['dps'],
    specs:[['Aflicción','Daño con maldiciones y corrupción',['dps']],['Demonología','Daño a través de demonios',['dps']],['Destrucción','Daño directo de fuego y sombras',['dps']]],
    lvl:'Ritmo de subida medio',
    lp:0,
    raid:'Maestría oscura da un 2–10 % de daño de las Sombras, como en Classic (en la beta temprana, 1–5 %)',
    forever:'Aflicción tiene un nuevo hechizo canalizado, el demonio se queda con Sacrificio demoníaco, Destrucción gana Incinerar y daño en área.' },
  { id:'druid', n:'Druida', roles:['tank','heal','dps'],
    specs:[['Equilibrio','Daño a distancia',['dps']],['Combate feral','Tanque (oso) y daño cuerpo a cuerpo (gato)',['tank','dps']],['Restauración','Sanador, mucha sanación en el tiempo',['heal']]],
    lvl:'Cerca de un 5 % más lento que la media (estimación de LFCarry)',
    lp:5,
    raid:'Líder de la manada y Aura de lechúcico lunar afectan a toda la banda y se acumulan',
    forever:'Cada especialización tiene un rol claro, las formas funcionan con pociones y encantamientos de arma. Puedes ser tanque, sanador y luchador en un solo personaje.' }
];
const ROLE_RU = { tank:'Tanque', heal:'Sanador', dps:'Daño', 'tank?':'Tanque (dudoso)' };
const ri = r => `<svg class="ri" aria-hidden="true"><use href="#i-${r.replace('?','')}"/></svg>`;
const CCOL = { warrior:'#c79c6e', paladin:'#f58cba', hunter:'#abd473', rogue:'#fff569', priest:'#e8e8e8', shaman:'#2f8cf0', mage:'#40c7eb', warlock:'#8788ee', druid:'#ff7d0a' };
const BUFF = { warrior:'Grito de guerra', paladin:'Bendición de los Reyes', hunter:'Aura de disparo certero', priest:'Palabra de poder: entereza, Espíritu divino', shaman:'Tótems (Fuerza de la tierra, Viento Furioso, Lengua de Fuego, Gracia del aire)', mage:'Intelecto Arcano, portales, comida y agua', druid:'Marca de lo salvaje, Líder de la manada, Aura de lechúcico lunar' };

const RACES = [
  { id:'human', n:'Humano', f:'alliance',
    cls:['warrior','paladin','hunter*','rogue','priest','mage','warlock'],
    rac:[['a','Will to Survive','Elimina el aturdimiento'],['a','Percepción','Revela enemigos invisibles durante 20 s'],['p','Ruthless','+1% de probabilidad de crítico'],['p','El espíritu humano','+10% de espíritu']],
    tip:'El espíritu se convierte en sanación para un Sacerdote Sagrado, así que un sacerdote humano es bueno para sanar.' },
  { id:'dwarf', n:'Enano', f:'alliance',
    cls:['warrior','paladin','hunter','rogue','priest','shaman*'],
    rac:[['a','Petraforma','Inmunidad a sangrados, venenos y enfermedades durante 8 s y menos daño físico'],['a','Buscar tesoro','Muestra cofres cercanos y da probabilidad de objetos extra en la mayoría de cofres'],['p','Artisan’s Precision','+1% de probabilidad de golpe con hechizos y ataques'],['p','Big Game Hunter','+5% de daño contra bestias']],
    tip:'Petraforma es útil para tanques y en JcJ.' },
  { id:'nightelf', n:'Elfo de la noche', f:'alliance',
    cls:['warrior','hunter','rogue','priest','druid'],
    rac:[['a','Elune’s Light','+10% de probabilidad de crítico durante 15 s'],['a','Fusión de las Sombras','Invisibilidad en el sitio'],['p','Prontitud','+2 % de esquiva y de velocidad de carrera (Warcraft Tavern indica un 1 % de esquiva) {beta}'],['p','Espíritu de fuego fatuo','+75 % de velocidad de carrera como espíritu (Warcraft Tavern indica 25 %) {beta}']],
    tip:'La única raza de la Alianza con druida, salvo que elijas Skyborne.' },
  { id:'gnome', n:'Gnomo', f:'alliance',
    cls:['warrior','rogue','mage','warlock','priest*'],
    rac:[['a','Artista del escape','Breve inmunidad a ralentizaciones e inmovilizaciones'],['a','Eureka!','Durante 8 s, las habilidades cuestan menos y son un 10 % más fuertes {beta}'],['p','Mente expansiva','+5% de maná, ira o energía máximos'],['p','Especialización de ingeniería','Los artefactos de ingeniería funcionan de forma más fiable']],
    tip:'Mente expansiva ayuda sobre todo a las clases de energía.' },
  { id:'skyA', n:'Skyborne (Alianza)', f:'alliance', paid:true, name:'Skyborne High Order',
    cls:['warrior','hunter','rogue','mage','druid'],
    rac:[['a','Walk on Air','Planea hacia abajo durante 10 s, sin daño por caída'],['a','Read Ley Line','Regeneración de salud y maná +50% durante 15 s. En una Ley Line, además Attuned durante 1 hora: +100%, se mantiene tras morir'],['p','Wind Blessed','+2% de velocidad de ataque y de hechizos'],['p','Elemental Insight','+5% de daño contra elementales']],
    tip:'Raza de pago: Heroic Pack desde 29,99 $. Empieza en Zephras Isle (niveles 1–12).' },
  { id:'orc', n:'Orco', f:'horde',
    cls:['warrior','hunter','rogue','shaman','warlock','mage*'],
    rac:[['a','Furia sangrienta','+10% de poder de ataque y poder con hechizos durante 15 s'],['a','Shatter Curse','Elimina maldiciones y corrupción, −5% de daño mágico recibido durante 8 s'],['p','Comandar','+5% de daño de las mascotas de brujo y cazador'],['p','Firmeza','Los aturdimientos duran un 20% menos']],
    tip:'Furia sangrienta da una potente ventana de daño.' },
  { id:'undead', n:'No-muerto', f:'horde',
    cls:['warrior','rogue','mage','priest','warlock','paladin*'],
    rac:[['a','Voluntad de los Renegados','Elimina hechizos, miedo y sueño'],['a','Canibalizar','Restaura un 35% de salud y maná con el tiempo'],['p','Respiración subacuática','Respira bajo el agua más tiempo'],['p','Touch of the Grave','Probabilidad de drenar salud al atacar']],
    tip:'Combinación nueva: un paladín para la Horda, donde esta clase no existía antes.' },
  { id:'tauren', n:'Tauren', f:'horde',
    cls:['warrior','hunter','shaman','druid'],
    rac:[['a','Pisotón de guerra','Aturde a los enemigos cercanos durante 2 s, reutilización de 90 s'],['a','Cultivo','Cultiva hierbas que se pueden recoger sin Herboristería, reutilización de 15 min'],['p','Plainsrunning','Mientras te mueves, la velocidad de carrera sube un 2% por acumulación, hasta +60%. No afecta a la velocidad montado'],['p','Robustez','+5% de salud']],
    tip:'La única raza de la Horda con druida, salvo que elijas Skyborne.' },
  { id:'troll', n:'Trol', f:'horde',
    cls:['warrior','hunter','rogue','priest','shaman','mage','warlock*'],
    rac:[['a','Iracundia','+10 % de velocidad de ataque y de hechizo durante 12 s, reutilización de 3 min'],['a','Rapid Regeneration','Restaura salud con el tiempo'],['p','Matanza de bestias','+5% de daño contra bestias'],['p','Regeneración','La salud se regenera también en combate']],
    tip:'Más opciones de clase de la Horda: siete.' },
  { id:'skyH', n:'Skyborne (Horda)', f:'horde', paid:true, name:'Skyborne Windshaper',
    cls:['warrior','hunter','rogue','shaman','druid'],
    rac:[['a','Walk on Air','Planea hacia abajo durante 10 s, sin daño por caída'],['a','Skysight','+15% de velocidad de carrera durante 15 s. En una Elemental Convergence, además Charged durante 1 hora: +30%, se mantiene tras morir'],['p','Wind Blessed','+2% de velocidad de ataque y de hechizos'],['p','Elemental Insight','+5% de daño contra elementales']],
    tip:'Raza de pago: Heroic Pack desde 29,99 $. Solo la Horda puede tener chamán, solo la Alianza mago.' }
];
RACES.forEach(r => { r.can = {}; r.cls.forEach(c => { const isNew = c.endsWith('*'); r.can[isNew ? c.slice(0,-1) : c] = isNew ? 'new' : 'ok'; }); });
const CL = Object.fromEntries(CLASSES.map(c => [c.id, c]));
const BETA = '<span class="beta-note">según los datos de la beta</span>';
const BMARK = '{' + 'beta}';   // split so the guide build (which swaps the marker for the span everywhere) leaves it alone
const racx = s => String(s).split(BETA).join(BMARK).split(BMARK).map(esc).join(BETA);
const RC = Object.fromEntries(RACES.map(r => [r.id, r]));
const RLEAD = {"human": "La raza más numerosa de la Alianza. Versátil y fuerte en JcJ gracias a Will to Survive.", "dwarf": "Mineros y fusileros recios de Forjaz. Por primera vez la Alianza tiene chamanes, y son enanos: en Classic no los había.", "nightelf": "Un pueblo antiguo de los bosques. Escurridizos: su propia forma de esconderse, esquiva y carrera rápida.", "gnome": "Los inventores de Gnomeregan. Pequeños, astutos y con la mejor habilidad de escape del juego.", "skyA": "Una raza nueva en Forever. Los High Order: elfos del viento que buscan la magia arcana perdida de sus ancestros.", "orc": "El corazón de la Horda. Los guerreros más fuertes y maestros del JcJ gracias a Furia sangrienta y Firmeza.", "undead": "Los Renegados: antiguos humanos que se liberaron del Rey Exánime. Inmunes al miedo y al sueño cuando importa.", "tauren": "Gigantes pacíficos de las llanuras. La mayor salud y su propio aturdimiento en área.", "troll": "La tribu Lanza Negra. Más clases que nadie en la Horda y una potente Iracundia para el daño.", "skyH": "Una raza nueva en Forever. Los Windshaper: líderes espirituales de los Skyborne, cercanos a los elementos."}; // race page leads and URL slugs, filled in by build.py
const RSLUG = {"human": "human", "dwarf": "dwarf", "nightelf": "night-elf", "gnome": "gnome", "skyA": "skyborne-alliance", "orc": "orc", "undead": "undead", "tauren": "tauren", "troll": "troll", "skyH": "skyborne-horde"};

const EN = {
  'Armas':'Arms','Furia':'Fury','Protección':'Protection','Sagrado':'Holy','Reprensión':'Retribution',
  'Bestias':'Beast Mastery','Puntería':'Marksmanship','Supervivencia':'Survival',
  'Asesinato':'Assassination','Combate':'Combat','Sutileza':'Subtlety',
  'Disciplina':'Discipline','Sombras':'Shadow','Elemental':'Elemental','Mejora':'Enhancement','Restauración':'Restoration',
  'Arcano':'Arcane','Fuego':'Fire','Escarcha':'Frost','Aflicción':'Affliction','Demonología':'Demonology','Destrucción':'Destruction',
  'Equilibrio':'Balance','Combate feral':'Feral',
  'Will to Survive':'Will to Survive','Percepción':'Perception','Ruthless':'Ruthless','El espíritu humano':'The Human Spirit',
  'Petraforma':'Stoneform','Buscar tesoro':'Find Treasure','Earth Fury':'Earth Fury','Big Game Hunter':'Big Game Hunter',
  'Elune’s Light':"Elune’s Light",'Fusión de las Sombras':'Shadowmeld','Prontitud':'Quickness','Espíritu de fuego fatuo':'Wisp Spirit',
  'Artista del escape':'Escape Artist','Eureka!':'Eureka!','Mente expansiva':'Expansive Mind','Especialización de ingeniería':'Engineering Specialization',
  'Walk on Air':'Walk on Air','Read Ley Line':'Read Ley Line','Wind Blessed':'Wind Blessed','Elemental Insight':'Elemental Insight','Skysight':'Skysight',
  'Furia sangrienta':'Blood Fury','Shatter Curse':'Shatter Curse','Savage':'Savage','Comandar':'Command','Firmeza':'Hardiness',
  'Voluntad de los Renegados':'Will of the Forsaken','Canibalizar':'Cannibalize','Respiración subacuática':'Underwater Breathing','Touch of the Grave':'Touch of the Grave',
  'Pisotón de guerra':'War Stomp','Cultivo':'Cultivation','Plainsrunning':'Plainsrunning','Robustez':'Endurance',
  'Iracundia':'Berserking','Rapid Regeneration':'Rapid Regeneration','Matanza de bestias':'Beast Slaying','Regeneración':'Regeneration'
};
RC.skyA.en = 'High Order Skyborne'; RC.skyH.en = 'Windshaper Skyborne';
const tipBox = h => `<div class="tipbox"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg><p><span class="tl">Consejo</span>${h}</p></div>`;
function bi(ru) { return EN[ru] && EN[ru] !== ru ? `${esc(ru)} <span class="en">(${esc(EN[ru])})</span>` : esc(ru); }
function raceEn(r) { return r.en ? ` <span class="en">/ ${esc(r.en)}</span>` : ''; }
function facName(f) { return f === 'alliance' ? 'Alianza' : 'Horda'; }
const PV = /*PV*/'?v=03c9d4a0';   // ?v= of the class and race portraits, filled in by build.art_version (redrawn under the same names)
/* Round face avatar: assets/art/<id>-face.webp, ring colour cc */
/* A class face follows the reader's side (GabellaPor, build.por_js); f: a fixed side (the class faces of a race row) */
function face(id, cc, cls = '', title = '', f = '') { const P = window.GabellaPor, t = `../assets/art/{${id}}-face.webp${PV}`, live = P && P.map[id] && !f;
  return `<span class="av ${cls}" style="--cc:${cc}"${title ? ` title="${esc(title)}"` : ''}><img src="../assets/art/${P ? P.id(id, f) : id}-face.webp${PV}"${live ? ` data-por-src="${t}"` : ''} width="160" height="160" alt="" loading="lazy" decoding="async"></span>`; }
function lvlMeter(c) {
  const p = c.lp || 0, w = Math.min(Math.abs(p) / 12 * 46, 46);
  const label = p < 0 ? `Más rápido en ${-p}%` : p > 0 ? `Más lento en ${p}%` : 'Ritmo medio';
  const bar = p ? `<i class="${p > 0 ? 'slow' : ''}" style="${p < 0 ? 'right' : 'left'}:50%;width:${w}%"></i>` : '';
  return `<span class="lvl"><span>${label}</span><span class="bar" role="img" aria-label="${label}">${bar}</span><span class="scale" aria-hidden="true"><span>más rápido</span><span>más lento</span></span></span>`;
}
function renderClassRef() {
  const roles = ['tank', 'heal', 'dps'];
  const head = `<div class="cmp-h" aria-hidden="true"><span>Clase</span><span class="rdots">${roles.map(x => `<span title="${ROLE_RU[x]}">${ri(x)}</span>`).join('')}</span><span>Subida de nivel</span><span>En bandas</span><span></span></div>`;
  const box = $('#classRef');
  box.innerHTML = head + CLASSES.map(c => `<div class="cmp-row" style="--cc:${CCOL[c.id]};--art:url('../assets/art/${window.GabellaPor ? GabellaPor.id(c.id) : c.id}-360.webp${PV}')">
    <span class="cmp-id">${face(c.id, CCOL[c.id])}<span><b><a class="cmp-a" href="${HOME}classes/${c.id}/">${esc(c.n)}</a></b><small>${c.specs.map(s => esc(s[0])).join(' · ')}</small></span></span>
    <span class="rdots" role="img" aria-label="Roles: ${c.roles.map(x => ROLE_RU[x]).join(', ')}">${roles.map(x => { const on = c.roles.includes(x), q = c.roles.includes(x + '?'); return `<span class="rdot${on ? ' on' : q ? ' q' : ''}" title="${ROLE_RU[q ? x + '?' : x]}">${ri(x)}</span>`; }).join('')}</span>
    ${lvlMeter(c)}
    <span class="cmp-d"><span class="cmp-txt" id="crt-${c.id}">${esc(c.raid)}</span><button type="button" class="cmp-more" aria-expanded="false" aria-controls="crt-${c.id}" aria-label="Mostrar completo" title="Mostrar completo"></button></span>
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
  const head = `<div class="cmp-h" aria-hidden="true"><span>Raza</span><span>Clases</span><span class="abl">Habilidades <span class="abt">activa</span><span class="abt p">pasiva</span></span><span></span></div>`;
  $('#raceRef').innerHTML = ['alliance', 'horde'].map(f => `<div class="rgroup ${f}"><h3>${facName(f)}</h3>${head}` + RACES.filter(r => r.f === f).map(r => `<a class="cmp-row" href="${HOME}races/${RSLUG[r.id]}/" style="--cc:var(--${f});--art:url('../assets/art/${RSLUG[r.id]}-360.webp${PV}')">
    <span class="cmp-id">${face(RSLUG[r.id], `var(--${f})`)}<span><b>${esc(r.n)}${r.paid ? '<span class="paid">de pago</span>' : ''}</b>${r.en ? `<small>${esc(r.en)}</small>` : ''}</span></span>
    <span class="ccl" role="img" aria-label="Clases: ${Object.keys(r.can).map(id => CL[id].n).join(', ')}">${CLASSES.map(c => { const v = r.can[c.id]; return face(c.id, CCOL[c.id], v ? (v === 'new' ? 'nw' : '') : 'off', c.n + (v === 'new' ? ', nuevo' : v ? '' : ', no disponible'), f); }).join('')}</span>
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
    const wh = feed.slice(0, 2).map(x => ({ d: x.date, html: `<a class="nc" href="${esc(x.url)}" target="_blank" rel="noopener"><time datetime="${esc(x.date)}">${x.date.slice(8, 10)}.${x.date.slice(5, 7)}</time><b lang="en">${esc(x.title)}</b><span>${'Wowhead, en inglés'}</span></a>` }));
    const all = ours.concat(bz, wh).sort((a, b) => (a.d < b.d ? 1 : a.d > b.d ? -1 : (b.o || 0) - (a.o || 0))).slice(0, 3);
    if (all.some(x => wh.includes(x) || bz.includes(x))) row.innerHTML = all.map(x => x.html).join('');
  });
})();
/* #peoples: the races block of the old home (old links) lives on the races page now */
if (location.hash === '#peoples') location.replace('races/');
