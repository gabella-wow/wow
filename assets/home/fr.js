const HOME = '';   // language home, the classes/ and races/ pages set their own
/* ref:start — shared with the classes/ and races/ pages (build_guides.ref_js); no $ or esc here, every page defines its own */
const CLASSES = [
  { id:'warrior', n:'Guerrier', s:'Guerrier', roles:['tank','dps'],
    specs:[['Armes','Dégâts en mêlée (arme à deux mains)',['dps']],['Fureur','Dégâts en mêlée (deux armes)',['dps']],['Protection','Tank',['tank']]],
    lvl:'La montée la plus lente, environ 12 % plus longue que la moyenne (estimation de LFCarry)',
    lp:12,
    raid:'Cri de guerre affecte tout le raid',
    forever:'Plus de rage, meilleure menace sur les groupes de cibles, le talent Weapon Master. Fureur et Sanguinaire sont affaiblis.' },
  { id:'paladin', n:'Paladin', roles:['tank','heal','dps'],
    specs:[['Sacré','Soigneur',['heal']],['Protection','Tank',['tank']],['Vindicte','Dégâts en mêlée',['dps']]],
    lvl:'Rythme de progression moyen',
    lp:0,
    raid:'Bénédiction des rois est désormais de base. Selon les classements de la bêta, Protection compte parmi les meilleurs tanks, et Vindicte a reculé après le patch du 15 octobre.',
    forever:'Frappe sacrée dès le niveau 6, Jugement ne consomme pas le sceau. Les morts-vivants peuvent désormais être paladins, la classe arrive donc dans la Horde.' },
  { id:'hunter', n:'Chasseur', roles:['dps'],
    specs:[['Maîtrise des bêtes','Dégâts à distance, beaucoup de dégâts du familier',['dps']],['Précision','Dégâts à distance',['dps']],['Survie','Mêlée et distance, pièges',['dps']]],
    lvl:'La montée la plus rapide, environ 8 % plus vite que la moyenne (estimation de LFCarry)',
    lp:-8,
    raid:'Aura de précision affecte tout le raid',
    forever:'Vous pouvez jouer sans familier, les pièges fonctionnent en combat, les renards arrivent comme famille de familiers. Survie peut jouer en mêlée.' },
  { id:'rogue', n:'Voleur', roles:['dps'],
    specs:[['Assassinat','Dégâts de poison',['dps']],['Combat','Attaques rapides à l’arme',['dps']],['Finesse','Embuscades, saignements',['dps']]],
    lvl:'Rythme de progression moyen',
    lp:0,
    raid:'Dégâts de mêlée purs, sans amélioration pour le raid',
    forever:'Les haches à une main sont désormais utilisables. Assassinat repose sur les poisons, Finesse sur les saignements et le camouflage.' },
  { id:'priest', n:'Prêtre', roles:['heal','dps'],
    specs:[['Discipline','Soigneur, boucliers et absorption',['heal']],['Sacré','Soigneur',['heal']],['Ombre','Dégâts à distance',['dps']]],
    lvl:'Environ 5 % plus lent que la moyenne (estimation de LFCarry)',
    lp:5,
    raid:'Esprit divin est désormais de base. Les dégâts d’ombre et Peste dévorante (24 s de temps de recharge) ont été renforcés par le patch du 15 octobre.',
    forever:'Gardien de peur et Peste dévorante sont disponibles dès le niveau 20 pour toutes les races. Chaque race a deux sorts de prêtre qui lui sont propres.' },
  { id:'shaman', n:'Chaman', roles:['heal','dps','tank?'],
    specs:[['Élémentaire','Dégâts à distance',['dps']],['Amélioration','Dégâts en mêlée. La capacité à tanker reste incertaine',['dps','tank?']],['Restauration','Soigneur',['heal']]],
    lvl:'Rythme de progression moyen',
    lp:0,
    raid:'Les totems Force de la Terre, Furie-des-vents, Langue de feu et Grâce aérienne améliorent leur groupe',
    forever:'Les nains peuvent désormais être chamans, la classe arrive donc dans l’Alliance. Explosion de lave a été renforcée, Élémentaire est monté dans les classements de dégâts.' },
  { id:'mage', n:'Mage', roles:['dps'],
    specs:[['Arcanes','Pics de dégâts, beaucoup de mana',['dps']],['Feu','Critiques et enflammer',['dps']],['Givre','Dégâts et contrôle',['dps']]],
    lvl:'La montée la plus rapide, environ 8 % plus vite que la moyenne, environ 12 heures gagnées (estimation de LFCarry)',
    lp:-8,
    raid:'Portails, nourriture et eau pour le groupe',
    forever:'Feu reçoit Chaleur continue, Arcanes Déflagration des arcanes, Givre Javelot de glace. Éclair de givrefeu est disponible dès le niveau 40.' },
  { id:'warlock', n:'Démoniste', roles:['dps'],
    specs:[['Affliction','Dégâts des malédictions et de la corruption',['dps']],['Démonologie','Dégâts par les démons',['dps']],['Destruction','Dégâts directs de feu et d’ombre',['dps']]],
    lvl:'Rythme de progression moyen',
    lp:0,
    raid:'Maîtrise des ténèbres donne 2–10 % de dégâts d’Ombre, comme dans Classic (1–5 % au début de la bêta)',
    forever:'Affliction a un nouveau sort canalisé, le démon reste avec Sacrifice démoniaque, Destruction gagne Incinérer et des dégâts de zone.' },
  { id:'druid', n:'Druide', roles:['tank','heal','dps'],
    specs:[['Équilibre','Dégâts à distance',['dps']],['Combat farouche','Tank (ours) et dégâts en mêlée (félin)',['tank','dps']],['Restauration','Soigneur, beaucoup de soins sur la durée',['heal']]],
    lvl:'Environ 5 % plus lent que la moyenne (estimation de LFCarry)',
    lp:5,
    raid:'Chef de la meute et Aura de sélénien affectent tout le raid et se cumulent',
    forever:'Chaque spécialisation a reçu un rôle clair, les formes fonctionnent avec les potions et les enchantements d’arme. Vous pouvez être tank, soigneur et combattant sur un seul personnage.' }
];
const ROLE_RU = { tank:'Tank', heal:'Soigneur', dps:'Dégâts', 'tank?':'Tank (incertain)' };
const ri = r => `<svg class="ri" aria-hidden="true"><use href="#i-${r.replace('?','')}"/></svg>`;
const CCOL = { warrior:'#c79c6e', paladin:'#f58cba', hunter:'#abd473', rogue:'#fff569', priest:'#e8e8e8', shaman:'#2f8cf0', mage:'#40c7eb', warlock:'#8788ee', druid:'#ff7d0a' };
const BUFF = { warrior:'Cri de guerre', paladin:'Bénédiction des rois', hunter:'Aura de précision', priest:'Mot de pouvoir : Robustesse, Esprit divin', shaman:'Totems (Force de la Terre, Furie-des-vents, Langue de feu, Grâce aérienne)', mage:'Intelligence des arcanes, portails, nourriture et eau', druid:'Marque du fauve, Chef de la meute, Aura de sélénien' };

const RACES = [
  { id:'human', n:'Humain', f:'alliance',
    cls:['warrior','paladin','hunter*','rogue','priest','mage','warlock'],
    rac:[['a','Volonté de survie','Supprime l’étourdissement'],['a','Perception','Révèle les ennemis invisibles pendant 20 s'],['p','Ruthless','+1% de chances de critique'],['p','L’esprit humain','+10% d’esprit']],
    tip:'L’esprit sert aux soins d’un prêtre Sacré, un prêtre humain est donc bon pour soigner.' },
  { id:'dwarf', n:'Nain', f:'alliance',
    cls:['warrior','paladin','hunter','rogue','priest','shaman*'],
    rac:[['a','Forme de pierre','Immunité aux saignements, poisons et maladies pendant 8 s et dégâts physiques réduits'],['a','Découverte de trésors','Affiche les coffres proches et donne une chance d’objets en plus dans la plupart des coffres'],['p','Artisan’s Precision','+1% de chances de toucher avec les sorts et les attaques'],['p','Big Game Hunter','+5% de dégâts contre les bêtes']],
    tip:'Forme de pierre est utile aux tanks et en JcJ.' },
  { id:'nightelf', n:'Elfe de la nuit', f:'alliance',
    cls:['warrior','hunter','rogue','priest','druid'],
    rac:[['a','Lumière d’Élune','+10% de chances de critique pendant 15 s'],['a','Camouflage dans l’ombre','Invisibilité sur place'],['p','Rapidité','+2 % d’esquive et de vitesse de course (Warcraft Tavern indique 1 % d’esquive) {beta}'],['p','Esprit feu follet','+75 % de vitesse de course sous forme d’esprit (Warcraft Tavern indique 25 %) {beta}']],
    tip:'La seule race de l’Alliance avec un druide, à moins de prendre un Skyborne.' },
  { id:'gnome', n:'Gnome', f:'alliance',
    cls:['warrior','rogue','mage','warlock','priest*'],
    rac:[['a','Maître de l’évasion','Brève immunité aux ralentissements et immobilisations'],['a','Eureka!','Pendant 8 s, les techniques coûtent moins cher et sont 10 % plus fortes {beta}'],['p','Pensée expansive','+5% de mana, rage ou énergie maximum'],['p','Spécialisation en ingénierie','Les appareils d’ingénierie fonctionnent de façon plus fiable']],
    tip:'Pensée expansive aide surtout les classes à énergie.' },
  { id:'skyA', n:'Skyborne (Alliance)', f:'alliance', paid:true, name:'Skyborne High Order',
    cls:['warrior','hunter','rogue','mage','druid'],
    rac:[['a','Walk on Air','Planez pendant 10 s, sans dégâts de chute'],['a','Read Ley Line','Régénération de vie et de mana +50% pendant 15 s. Près d’une Ley Line, Attuned en plus pendant 1 heure : +100%, conservé après la mort'],['p','Wind Blessed','+2% de vitesse d’attaque et d’incantation'],['p','Elemental Insight','+5% de dégâts contre les élémentaires']],
    tip:'Race payante : pack Héroïque dès $29.99. Débute sur Zephras Isle (niveaux 1–12).' },
  { id:'orc', n:'Orc', f:'horde',
    cls:['warrior','hunter','rogue','shaman','warlock','mage*'],
    rac:[['a','Fureur sanguinaire','+10% de puissance d’attaque et de puissance des sorts pendant 15 s'],['a','Shatter Curse','Retire malédictions et corruption, −5% de dégâts magiques subis pendant 8 s'],['p','Commandement','+5% de dégâts des familiers de démoniste et de chasseur'],['p','Solidité','Étourdissements 20% plus courts']],
    tip:'Fureur sanguinaire offre une puissante fenêtre de dégâts.' },
  { id:'undead', n:'Mort-vivant', f:'horde',
    cls:['warrior','rogue','mage','priest','warlock','paladin*'],
    rac:[['a','Volonté des Réprouvés','Supprime charme, peur et sommeil'],['a','Cannibalisme','Rend 35% de la vie et du mana sur la durée'],['p','Respiration aquatique','Respirez plus longtemps sous l’eau'],['p','Toucher du tombeau','Chance de drainer de la vie en attaquant']],
    tip:'Nouvelle combinaison : un paladin pour la Horde, où cette classe n’existait pas.' },
  { id:'tauren', n:'Tauren', f:'horde',
    cls:['warrior','hunter','shaman','druid'],
    rac:[['a','Choc martial','Étourdit les ennemis proches pendant 2 s, temps de recharge 90 s'],['a','Culture','Fait pousser des herbes récoltables sans Herboristerie, temps de recharge 15 min'],['p','Course dans les plaines','Tant que vous bougez, la vitesse de course augmente de 2% par cumul, jusqu’à +60%. Sans effet sur la vitesse en monture'],['p','Endurcissement','+5% de vie']],
    tip:'La seule race de la Horde avec un druide, à moins de prendre un Skyborne.' },
  { id:'troll', n:'Troll', f:'horde',
    cls:['warrior','hunter','rogue','priest','shaman','mage','warlock*'],
    rac:[['a','Berserker','+10 % de vitesse d’attaque et d’incantation pendant 12 s, récupération de 3 min'],['a','Régénération rapide','Rend de la vie sur la durée'],['p','Tueur de bêtes','+5% de dégâts contre les bêtes'],['p','Régénération','La vie se régénère aussi en combat']],
    tip:'Le plus de choix de classes dans la Horde : sept.' },
  { id:'skyH', n:'Skyborne (Horde)', f:'horde', paid:true, name:'Skyborne Windshaper',
    cls:['warrior','hunter','rogue','shaman','druid'],
    rac:[['a','Walk on Air','Planez pendant 10 s, sans dégâts de chute'],['a','Skysight','+15% de vitesse de course pendant 15 s. Près d’une Elemental Convergence, Charged en plus pendant 1 heure : +30%, conservé après la mort'],['p','Wind Blessed','+2% de vitesse d’attaque et d’incantation'],['p','Elemental Insight','+5% de dégâts contre les élémentaires']],
    tip:'Race payante : pack Héroïque dès $29.99. Seule la Horde peut avoir un chaman, seule l’Alliance un mage.' }
];
RACES.forEach(r => { r.can = {}; r.cls.forEach(c => { const isNew = c.endsWith('*'); r.can[isNew ? c.slice(0,-1) : c] = isNew ? 'new' : 'ok'; }); });
const CL = Object.fromEntries(CLASSES.map(c => [c.id, c]));
const BETA = '<span class="beta-note">d’après la bêta</span>';
const BMARK = '{' + 'beta}';   // split so the guide build (which swaps the marker for the span everywhere) leaves it alone
const racx = s => String(s).split(BETA).join(BMARK).split(BMARK).map(esc).join(BETA);
const RC = Object.fromEntries(RACES.map(r => [r.id, r]));
const RLEAD = {"human": "La race la plus nombreuse de l’Alliance. Polyvalente et forte en JcJ grâce à Volonté de survie.", "dwarf": "Robustes mineurs et fusiliers de Forgefer. Pour la première fois, l’Alliance a des chamans, et ce sont des nains : Classic n’en avait pas.", "nightelf": "Un peuple ancien des forêts. Insaisissables : leur propre façon de se cacher, d’esquiver et de courir vite.", "gnome": "Les inventeurs de Gnomeregan. Petits, rusés et avec la meilleure capacité d’évasion du jeu.", "skyA": "Une nouvelle race dans Forever. Le High Order : des elfes du vent en quête de la magie des arcanes perdue de leurs ancêtres.", "orc": "Le cœur de la Horde. Les meilleurs guerriers et maîtres du JcJ grâce à Fureur sanguinaire et Solidité.", "undead": "Les Réprouvés : d’anciens humains libérés du roi-liche. Immunisés contre la peur et le sommeil quand ça compte.", "tauren": "Paisibles géants des plaines. Le plus de vie et leur propre étourdissement de zone.", "troll": "La tribu Sombrelance. Le plus de classes de la Horde et un puissant Berserker pour les dégâts.", "skyH": "Une nouvelle race dans Forever. Les Windshapers : guides spirituels des Skyborne, proches des éléments."}; // race page leads and URL slugs, filled in by build.py
const RSLUG = {"human": "human", "dwarf": "dwarf", "nightelf": "night-elf", "gnome": "gnome", "skyA": "skyborne-alliance", "orc": "orc", "undead": "undead", "tauren": "tauren", "troll": "troll", "skyH": "skyborne-horde"};

const EN = {
  'Armes':'Arms','Fureur':'Fury','Protection':'Protection','Sacré':'Holy','Vindicte':'Retribution',
  'Maîtrise des bêtes':'Beast Mastery','Précision':'Marksmanship','Survie':'Survival',
  'Assassinat':'Assassination','Combat':'Combat','Finesse':'Subtlety',
  'Discipline':'Discipline','Ombre':'Shadow','Élémentaire':'Elemental','Amélioration':'Enhancement','Restauration':'Restoration',
  'Arcanes':'Arcane','Feu':'Fire','Givre':'Frost','Affliction':'Affliction','Démonologie':'Demonology','Destruction':'Destruction',
  'Équilibre':'Balance','Combat farouche':'Feral',
  'Volonté de survie':'Will to Survive','Perception':'Perception','Ruthless':'Ruthless','L’esprit humain':'The Human Spirit',
  'Forme de pierre':'Stoneform','Découverte de trésors':'Find Treasure','Earth Fury':'Earth Fury','Big Game Hunter':'Big Game Hunter',
  'Lumière d’Élune':"Elune’s Light",'Camouflage dans l’ombre':'Shadowmeld','Rapidité':'Quickness','Esprit feu follet':'Wisp Spirit',
  'Maître de l’évasion':'Escape Artist','Eureka!':'Eureka!','Pensée expansive':'Expansive Mind','Spécialisation en ingénierie':'Engineering Specialization',
  'Walk on Air':'Walk on Air','Read Ley Line':'Read Ley Line','Wind Blessed':'Wind Blessed','Elemental Insight':'Elemental Insight','Skysight':'Skysight',
  'Fureur sanguinaire':'Blood Fury','Shatter Curse':'Shatter Curse','Savage':'Savage','Commandement':'Command','Solidité':'Hardiness',
  'Volonté des Réprouvés':'Will of the Forsaken','Cannibalisme':'Cannibalize','Respiration aquatique':'Underwater Breathing','Toucher du tombeau':'Touch of the Grave',
  'Choc martial':'War Stomp','Culture':'Cultivation','Course dans les plaines':'Plainsrunning','Endurcissement':'Endurance',
  'Berserker':'Berserking','Régénération rapide':'Rapid Regeneration','Tueur de bêtes':'Beast Slaying','Régénération':'Regeneration'
};
RC.skyA.en = 'High Order Skyborne'; RC.skyH.en = 'Windshaper Skyborne';
const tipBox = h => `<div class="tipbox"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg><p><span class="tl">Conseil</span>${h}</p></div>`;
function bi(ru) { return EN[ru] && EN[ru] !== ru ? `${esc(ru)} <span class="en">(${esc(EN[ru])})</span>` : esc(ru); }
function raceEn(r) { return r.en ? ` <span class="en">/ ${esc(r.en)}</span>` : ''; }
function facName(f) { return f === 'alliance' ? 'Alliance' : 'Horde'; }
const PV = /*PV*/'?v=03c9d4a0';   // ?v= of the class and race portraits, filled in by build.art_version (redrawn under the same names)
/* Round face avatar: assets/art/<id>-face.webp, ring colour cc */
/* A class face follows the reader's side (GabellaPor, build.por_js); f: a fixed side (the class faces of a race row) */
function face(id, cc, cls = '', title = '', f = '') { const P = window.GabellaPor, t = `../assets/art/{${id}}-face.webp${PV}`, live = P && P.map[id] && !f;
  return `<span class="av ${cls}" style="--cc:${cc}"${title ? ` title="${esc(title)}"` : ''}><img src="../assets/art/${P ? P.id(id, f) : id}-face.webp${PV}"${live ? ` data-por-src="${t}"` : ''} width="160" height="160" alt="" loading="lazy" decoding="async"></span>`; }
function lvlMeter(c) {
  const p = c.lp || 0, w = Math.min(Math.abs(p) / 12 * 46, 46);
  const label = p < 0 ? `Plus rapide de ${-p}%` : p > 0 ? `Plus lent de ${p}%` : 'Rythme moyen';
  const bar = p ? `<i class="${p > 0 ? 'slow' : ''}" style="${p < 0 ? 'right' : 'left'}:50%;width:${w}%"></i>` : '';
  return `<span class="lvl"><span>${label}</span><span class="bar" role="img" aria-label="${label}">${bar}</span><span class="scale" aria-hidden="true"><span>plus rapide</span><span>plus lent</span></span></span>`;
}
function renderClassRef() {
  const roles = ['tank', 'heal', 'dps'];
  const head = `<div class="cmp-h" aria-hidden="true"><span>Classe</span><span class="rdots">${roles.map(x => `<span title="${ROLE_RU[x]}">${ri(x)}</span>`).join('')}</span><span>Progression</span><span>En raid</span><span></span></div>`;
  const box = $('#classRef');
  box.innerHTML = head + CLASSES.map(c => `<div class="cmp-row" style="--cc:${CCOL[c.id]};--art:url('../assets/art/${window.GabellaPor ? GabellaPor.id(c.id) : c.id}-360.webp${PV}')">
    <span class="cmp-id">${face(c.id, CCOL[c.id])}<span><b><a class="cmp-a" href="${HOME}classes/${c.id}/">${esc(c.n)}</a></b><small>${c.specs.map(s => esc(s[0])).join(' · ')}</small></span></span>
    <span class="rdots" role="img" aria-label="Rôles : ${c.roles.map(x => ROLE_RU[x]).join(', ')}">${roles.map(x => { const on = c.roles.includes(x), q = c.roles.includes(x + '?'); return `<span class="rdot${on ? ' on' : q ? ' q' : ''}" title="${ROLE_RU[q ? x + '?' : x]}">${ri(x)}</span>`; }).join('')}</span>
    ${lvlMeter(c)}
    <span class="cmp-d"><span class="cmp-txt" id="crt-${c.id}">${esc(c.raid)}</span><button type="button" class="cmp-more" aria-expanded="false" aria-controls="crt-${c.id}" aria-label="Afficher en entier" title="Afficher en entier"></button></span>
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
  const head = `<div class="cmp-h" aria-hidden="true"><span>Race</span><span>Classes</span><span class="abl">Capacités <span class="abt">active</span><span class="abt p">passive</span></span><span></span></div>`;
  $('#raceRef').innerHTML = ['alliance', 'horde'].map(f => `<div class="rgroup ${f}"><h3>${facName(f)}</h3>${head}` + RACES.filter(r => r.f === f).map(r => `<a class="cmp-row" href="${HOME}races/${RSLUG[r.id]}/" style="--cc:var(--${f});--art:url('../assets/art/${RSLUG[r.id]}-360.webp${PV}')">
    <span class="cmp-id">${face(RSLUG[r.id], `var(--${f})`)}<span><b>${esc(r.n)}${r.paid ? '<span class="paid">payant</span>' : ''}</b>${r.en ? `<small>${esc(r.en)}</small>` : ''}</span></span>
    <span class="ccl" role="img" aria-label="Classes : ${Object.keys(r.can).map(id => CL[id].n).join(', ')}">${CLASSES.map(c => { const v = r.can[c.id]; return face(c.id, CCOL[c.id], v ? (v === 'new' ? 'nw' : '') : 'off', c.n + (v === 'new' ? ', nouveau' : v ? '' : ', indisponible'), f); }).join('')}</span>
    <span class="abs">${r.rac.map(x => `<span><b class="${x[0] === 'a' ? '' : 'p'}">${bi(x[1])}</b><span>${racx(x[2])}</span></span>`).join('')}</span>
    <span class="go" aria-hidden="true"><svg class="ico"><use href="#i-arrow"/></svg></span>
  </a>`).join('') + '</div>').join('');
}
/* ref:end */
const $ = s => document.querySelector(s);
function esc(s) { return String(s).replace(/[&<>"]/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m])); }
const ROOT = '../';
function raceName(r) { return r.name || r.n; }
/* Class roster: tall portraits, the hovered or focused one expands */
const DESC = {
  warrior: 'Plaques, rage et première ligne. Encaisse les coups en tank ou fauche avec une arme à deux mains.',
  paladin: 'Un guerrier sacré en plaques : soigne, tanke et frappe au marteau. Désormais aussi dans la Horde.',
  hunter: 'Arc, pièges et une bête fidèle à vos côtés. L’une des classes les plus rapides à monter.',
  rogue: 'Poisons, lames et ombre. Dégâts purs depuis l’embuscade et contrôle des foules.',
  priest: 'La Lumière et l’Ombre dans les mêmes mains. Le soigneur principal du groupe ou un lanceur de sorts obscur.',
  shaman: 'Totems et éléments : soigne, frappe avec la foudre ou les armes. Désormais aussi dans l’Alliance.',
  mage: 'Magie du feu, du givre et des arcanes. Portails, nourriture et eau pour le groupe.',
  warlock: 'Malédictions, démons et feu. Dégâts sur la durée et votre propre démon pour vous aider.',
  druid: 'Ours, félin, sélénien ou soigneur : les trois rôles sur un seul personnage.'
};
const artSet = (id, ext) => [360, 600, 896].map(w => `${ROOT}assets/art/${id}-${w}.${ext}${PV} ${w}w`).join(', ');
/* A class portrait of the reader's side: the best race of that side (build.portraits), swapped by GabellaPor when the side changes */
const porPic = id => { const P = window.GabellaPor, u = s => (P ? P.url(s) : s.replace(/[{}]/g, '')), t = `{${id}}`, img = `${ROOT}assets/art/${t}-600.webp${PV}`;
  return `<picture>${['avif', 'webp'].map(e => `<source type="image/${e}" srcset="${u(artSet(t, e))}" data-por-srcset="${artSet(t, e)}" sizes="${CLS_SIZES}">`).join('')}<img src="${u(img)}" data-por-src="${img}" width="896" height="1200" alt="" loading="lazy" decoding="async"></picture>`; };
const ART_SIZES = '(max-width: 719px) 78vw, 440px';
const CLS_SIZES = '(max-width: 1023px) 34vw, 440px';   // class portraits are grid cells on a phone and a tablet
function renderRoster() {
  $('#roster').innerHTML = CLASSES.map((c, i) => `<a class="hc${i === 0 ? ' on' : ''}" href="classes/${c.id}/" style="--cc:${CCOL[c.id]}">
    ${porPic(c.id)}
    <span class="vn" aria-hidden="true">${esc(c.n)}</span>
    <span class="info"><b>${esc(c.n)}</b><span class="roles">${c.roles.filter(r => !r.endsWith('?')).map(r => `<span>${ri(r)}${ROLE_RU[r]}</span>`).join('')}</span><span class="d">${esc(DESC[c.id])}</span><span class="more">En savoir plus sur la classe</span></span>
  </a>`).join('');
}
renderRoster();
/* Race roster: one row of portraits per faction, links to the race pages */
function renderPeoples() {
  [['alliance', '#rosterA'], ['horde', '#rosterH']].forEach(([f, sel]) => {
    $(sel).innerHTML = RACES.filter(r => r.f === f).map((r, i) => `<a class="hc${i === 0 ? ' on' : ''}" href="races/${RSLUG[r.id]}/" style="--cc:var(--${f})">
    <picture><source type="image/avif" srcset="${artSet(RSLUG[r.id], 'avif')}" sizes="${ART_SIZES}"><source type="image/webp" srcset="${artSet(RSLUG[r.id], 'webp')}" sizes="${ART_SIZES}"><img src="${ROOT}assets/art/${RSLUG[r.id]}-600.webp${PV}" width="896" height="1200" alt="" loading="lazy" decoding="async"></picture>
    <span class="vn" aria-hidden="true">${esc(raceName(r))}</span>
    <span class="info"><b>${esc(raceName(r))}</b>${r.paid ? '<span class="tag paid">payant</span>' : ''}<span class="d">${esc(RLEAD[r.id])}</span><span class="more">En savoir plus sur la race</span></span>
  </a>`).join('');
  });
}
renderPeoples();
/* Card titles fit the card (CSS: font-size = room / --k). --k is the width in em of the longest word of the name, or of the whole vertical label, measured in the real font; the words are never broken. */
function fitCards() {
  const m = document.createElement('span');
  m.style.cssText = 'position:absolute;left:-9999px;top:0;visibility:hidden;white-space:pre;line-height:1;font-size:100px';
  document.body.append(m);
  const k = (t, v) => { m.textContent = t; m.style.writingMode = v ? 'vertical-rl' : 'horizontal-tb'; const r = m.getBoundingClientRect(); return (v ? r.height : r.width) / 100; };   // vertical labels are measured vertically: ’ and the like stand upright there
  const ks = new Map();   // one --k per roster and kind of label: the widest name sets the size of all, so no name is set smaller than the rest
  document.querySelectorAll('.hc .info b, .hc .vn').forEach(el => {
    const cs = getComputedStyle(el), whole = el.classList.contains('vn');
    m.style.fontFamily = cs.fontFamily; m.style.fontWeight = cs.fontWeight;
    m.style.letterSpacing = (parseFloat(cs.letterSpacing) || 0) / parseFloat(cs.fontSize) * 100 + 'px';
    const parts = whole ? [el.textContent] : el.textContent.match(/[^\s-]+-?/g) || [''];
    const g = el.closest('.roster, .rr') || document.body, key = g.dataset.fk || (g.dataset.fk = 'r' + ks.size + Math.random().toString(36).slice(2, 6));
    const id = key + whole; ks.set(id, Math.max(ks.get(id) || 0, ...parts.map(t => k(t, whole))));
    el.dataset.fid = id;
  });
  document.querySelectorAll('[data-fid]').forEach(el => el.style.setProperty('--k', ks.get(el.dataset.fid).toFixed(3)));
  m.remove();
}
fitCards();
if (document.fonts) { document.fonts.ready.then(fitCards); document.fonts.addEventListener('loadingdone', fitCards); }
function activate(card) { if (!card || card.classList.contains('on')) return; card.parentElement.querySelectorAll('.hc.on').forEach(x => x.classList.remove('on')); card.classList.add('on'); }
document.querySelectorAll('.roster').forEach(ro => {
  ro.addEventListener('mouseover', e => activate(e.target.closest('.hc')));
  ro.addEventListener('focusin', e => activate(e.target.closest('.hc')));
});

/* Side switch of the class portraits: GabellaPor is the one source (a hero's side, else a side chosen here, else the time of day) */
const SIDESW = $('#sidesw'), SIDEBTN = [...SIDESW.querySelectorAll('[role="radio"]')];
function syncSide() {
  const f = window.GabellaPor ? GabellaPor.fac() : 'alliance';
  SIDEBTN.forEach(b => { const on = b.dataset.f === f; b.setAttribute('aria-checked', on); b.tabIndex = on ? 0 : -1; });
}
if (window.GabellaPor) {
  SIDESW.classList.add('on'); syncSide();
  ['gabella-side', 'gabella-me'].forEach(n => addEventListener(n, syncSide)); document.addEventListener('gabella:tod', syncSide);
  SIDEBTN.forEach((b, i) => {
    b.addEventListener('click', () => { GabellaPor.set(b.dataset.f); syncSide(); });
    b.addEventListener('keydown', e => {
      const k = { ArrowRight: i + 1, ArrowDown: i + 1, ArrowLeft: i - 1, ArrowUp: i - 1, Home: 0, End: 1 }[e.key];
      if (k === undefined) return;
      e.preventDefault(); const n = SIDEBTN[(k + 2) % 2]; GabellaPor.set(n.dataset.f); syncSide(); n.focus();
    });
  });
}
/* Classes / races: one block, two tabs (arrow keys, Home, End); #peoples (menu, old links) opens the races */
const TABS = [...document.querySelectorAll('#classes [role="tab"]')];
function showTab(t, focus) {
  TABS.forEach(x => { const on = x === t; x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1; document.getElementById(x.getAttribute('aria-controls')).hidden = !on; });
  SIDESW.hidden = t !== TABS[0];   // the races show both sides: no switch there
  if (focus) t.focus();
}
TABS.forEach((t, i) => {
  t.addEventListener('click', () => showTab(t));
  t.addEventListener('keydown', e => {
    const k = { ArrowRight: i + 1, ArrowLeft: i - 1, Home: 0, End: TABS.length - 1 }[e.key];
    if (k === undefined) return;
    e.preventDefault(); showTab(TABS[(k + TABS.length) % TABS.length], true);
  });
});
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
    const wh = feed.slice(0, 2).map(x => ({ d: x.date, html: `<a class="nc" href="${esc(x.url)}" target="_blank" rel="noopener"><time datetime="${esc(x.date)}">${x.date.slice(8, 10)}.${x.date.slice(5, 7)}</time><b lang="en">${esc(x.title)}</b><span>${'Wowhead, en anglais'}</span></a>` }));
    const all = ours.concat(bz, wh).sort((a, b) => (a.d < b.d ? 1 : a.d > b.d ? -1 : (b.o || 0) - (a.o || 0))).slice(0, 3);
    if (all.some(x => wh.includes(x) || bz.includes(x))) row.innerHTML = all.map(x => x.html).join('');
  });
})();
function hashTab() { if (location.hash === '#peoples') { showTab(TABS[1]); document.getElementById('classes').scrollIntoView(); } }
addEventListener('hashchange', hashTab);
hashTab();
