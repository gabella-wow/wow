const HOME = '';   // language home, the classes/ and races/ pages set their own
/* ref:start — shared with the classes/ and races/ pages (build_guides.ref_js); no $ or esc here, every page defines its own */
const CLASSES = [
  { id:'warrior', n:'Guerreiro', s:'Guerreiro', roles:['tank','dps'],
    specs:[['Armas','Dano corpo a corpo (arma de duas mãos)',['dps']],['Fúria','Dano corpo a corpo (duas armas)',['dps']],['Proteção','Tanque',['tank']]],
    lvl:'A evolução mais lenta, cerca de 12% mais longa que a média (estimativa do LFCarry)',
    lp:12,
    raid:'Brado de Batalha afeta a raide toda',
    forever:'Mais Raiva, melhor ameaça em grupos de alvos, o talento Weapon Master. Fúria e Sede de Sangue foram enfraquecidos.' },
  { id:'paladin', n:'Paladino', roles:['tank','heal','dps'],
    specs:[['Sagrado','Curador',['heal']],['Proteção','Tanque',['tank']],['Retribuição','Dano corpo a corpo',['dps']]],
    lvl:'Ritmo de evolução médio',
    lp:0,
    raid:'Bênção dos Reis agora é básica. Pelas listas do beta, Proteção está entre os tanques mais fortes, e Retribuição caiu depois do patch de 15 de outubro.',
    forever:'Golpe Sagrado a partir do nível 6, Julgamento não consome o selo. Mortos-vivos agora podem ser paladinos, então a classe chegou à Horda.' },
  { id:'hunter', n:'Caçador', roles:['dps'],
    specs:[['Domínio das Feras','Dano à distância, muito dano vindo do mascote',['dps']],['Precisão','Dano à distância',['dps']],['Sobrevivência','Corpo a corpo e à distância, armadilhas',['dps']]],
    lvl:'A evolução mais rápida, cerca de 8% mais rápida que a média (estimativa do LFCarry)',
    lp:-8,
    raid:'Aura de Tiro Certeiro afeta a raide toda',
    forever:'Dá para jogar sem mascote, armadilhas funcionam em combate, raposas surgiram como família de mascotes. Sobrevivência pode ir para o corpo a corpo.' },
  { id:'rogue', n:'Ladino', roles:['dps'],
    specs:[['Assassinato','Dano de venenos',['dps']],['Combate','Ataques rápidos com armas',['dps']],['Subterfúgio','Emboscadas, sangramentos',['dps']]],
    lvl:'Ritmo de evolução médio',
    lp:0,
    raid:'Dano corpo a corpo puro, sem bônus para a raide toda',
    forever:'Agora dá para usar machados de uma mão. Assassinato é construído em venenos, Subterfúgio em sangramentos e furtividade.' },
  { id:'priest', n:'Sacerdote', roles:['heal','dps'],
    specs:[['Disciplina','Curador, escudos e absorção',['heal']],['Sagrado','Curador',['heal']],['Sombra','Dano à distância',['dps']]],
    lvl:'Cerca de 5% mais lento que a média (estimativa do LFCarry)',
    lp:5,
    raid:'Espírito Divino agora é básico. O dano de Sombra e Peste Devoradora (recarga de 24 s) foram fortalecidos pelo patch de 15 de outubro.',
    forever:'Proteção contra Medo e Peste Devoradora ficam disponíveis a partir do nível 20 para qualquer raça. Cada raça tem dois feitiços de sacerdote próprios.' },
  { id:'shaman', n:'Xamã', roles:['heal','dps','tank?'],
    specs:[['Elemental','Dano à distância',['dps']],['Aperfeiçoamento','Dano corpo a corpo. A capacidade de tanquear ainda é incerta',['dps','tank?']],['Restauração','Curador',['heal']]],
    lvl:'Ritmo de evolução médio',
    lp:0,
    raid:'Os totens Força da Terra, Fúria dos Ventos, Labaredas e Graça do Ar dão bônus ao próprio grupo',
    forever:'Anões agora podem ser xamãs, então a classe chegou à Aliança. Estouro de Lava foi fortalecida, Elemental subiu no ranking de dano.' },
  { id:'mage', n:'Mago', roles:['dps'],
    specs:[['Arcano','Explosão de dano, muita mana',['dps']],['Fogo','Críticos e ignições',['dps']],['Gélido','Dano e controle',['dps']]],
    lvl:'A evolução mais rápida, cerca de 8% mais rápida que a média, cerca de 12 horas economizadas (estimativa do LFCarry)',
    lp:-8,
    raid:'Portais, comida e água para o grupo',
    forever:'Fogo ganhou Embalo de Fogo, Arcano ganhou Impacto Arcano, Gélido ganhou Lança de Gelo. Seta de Fogofrio fica disponível a partir do nível 40.' },
  { id:'warlock', n:'Bruxo', roles:['dps'],
    specs:[['Suplício','Dano de maldições e corrupção',['dps']],['Demonologia','Dano por meio de demônios',['dps']],['Destruição','Dano direto de fogo e de sombra',['dps']]],
    lvl:'Ritmo de evolução médio',
    lp:0,
    raid:'Maestria Sombria dá 2–10% de dano Sombrio, como no Classic (na beta inicial, 1–5%)',
    forever:'Suplício tem um novo feitiço canalizado, o demônio fica com Sacrifício Demoníaco, Destruição ganhou Incinerar e dano em área.' },
  { id:'druid', n:'Druida', roles:['tank','heal','dps'],
    specs:[['Equilíbrio','Dano à distância',['dps']],['Combate Feral','Tanque (urso) e dano corpo a corpo (gato)',['tank','dps']],['Restauração','Curador, muita cura ao longo do tempo',['heal']]],
    lvl:'Cerca de 5% mais lento que a média (estimativa do LFCarry)',
    lp:5,
    raid:'Líder do Bando e Aura de Luniscante afetam a raide toda e se acumulam',
    forever:'Cada especialização ganhou uma função clara, as formas funcionam com poções e encantamentos de arma. Você pode ser tanque, curador e lutador num só personagem.' }
];
const ROLE_RU = { tank:'Tanque', heal:'Curador', dps:'Dano', 'tank?':'Tanque (incerto)' };
const ri = r => `<svg class="ri" aria-hidden="true"><use href="#i-${r.replace('?','')}"/></svg>`;
const CCOL = { warrior:'#c79c6e', paladin:'#f58cba', hunter:'#abd473', rogue:'#fff569', priest:'#e8e8e8', shaman:'#2f8cf0', mage:'#40c7eb', warlock:'#8788ee', druid:'#ff7d0a' };
const BUFF = { warrior:'Brado de Batalha', paladin:'Bênção dos Reis', hunter:'Aura de Tiro Certeiro', priest:'Palavra de Poder: Fortitude, Espírito Divino', shaman:'Totens (Força da Terra, Fúria dos Ventos, Labaredas, Graça do Ar)', mage:'Inteligência Arcana, portais, comida e água', druid:'Marca do Indomado, Líder do Bando, Aura de Luniscante' };

const RACES = [
  { id:'human', n:'Humano', f:'alliance',
    cls:['warrior','paladin','hunter*','rogue','priest','mage','warlock'],
    rac:[['a','Desejo de Sobreviver','Remove atordoamento'],['a','Percepção','Revela inimigos invisíveis por 20 s'],['p','Ruthless','+1% de chance de crítico'],['p','O Espírito Humano','+10% de espírito']],
    tip:'O espírito vira cura para um Sacerdote Sagrado, então um sacerdote humano é bom para curar.' },
  { id:'dwarf', n:'Anão', f:'alliance',
    cls:['warrior','paladin','hunter','rogue','priest','shaman*'],
    rac:[['a','Forma de Pedra','Imunidade a sangramentos, venenos e doenças por 8 s e dano físico reduzido'],['a','Localizar Tesouros','Mostra baús por perto e dá chance de itens extras na maioria dos baús'],['p','Artisan’s Precision','+1% de chance de acerto com feitiços e ataques'],['p','Big Game Hunter','+5% de dano contra feras']],
    tip:'Forma de Pedra é útil para tanques e no PvP.' },
  { id:'nightelf', n:'Elfo Noturno', f:'alliance',
    cls:['warrior','hunter','rogue','priest','druid'],
    rac:[['a','Luz de Eluna','+10% de chance de crítico por 15 s'],['a','Fusão Sombria','Invisibilidade sem sair do lugar'],['p','Rapidez','+2% de esquiva e de velocidade de corrida (o Warcraft Tavern indica 1% de esquiva) {beta}'],['p','Espírito de Fogo-fátuo','+75% de velocidade de corrida como espírito (o Warcraft Tavern indica 25%) {beta}']],
    tip:'A única raça da Aliança com druida, a menos que você pegue Skyborne.' },
  { id:'gnome', n:'Gnomo', f:'alliance',
    cls:['warrior','rogue','mage','warlock','priest*'],
    rac:[['a','Artista da Fuga','Breve imunidade a lentidão e enraizamento'],['a','Eureca!','Por 8 s, as habilidades custam menos e ficam 10% mais fortes {beta}'],['p','Mente Expansiva','+5% de mana, raiva ou energia máxima'],['p','Especialização em Engenharia','Dispositivos de engenharia funcionam com mais confiabilidade']],
    tip:'Mente Expansiva ajuda especialmente as classes de energia.' },
  { id:'skyA', n:'Skyborne (Aliança)', f:'alliance', paid:true, name:'Skyborne da High Order',
    cls:['warrior','hunter','rogue','mage','druid'],
    rac:[['a','Walk on Air','Plana para baixo por 10 s, sem dano de queda'],['a','Read Ley Line','Regeneração de vida e mana +50% por 15 s. Numa Ley Line, também Attuned por 1 hora: +100%, continua após a morte'],['p','Wind Blessed','+2% de velocidade de ataque e de feitiços'],['p','Elemental Insight','+5% de dano contra elementais']],
    tip:'Raça paga: Heroic Pack a partir de $29.99. Começa na região de Zephras Isle (níveis 1–12).' },
  { id:'orc', n:'Orc', f:'horde',
    cls:['warrior','hunter','rogue','shaman','warlock','mage*'],
    rac:[['a','Fúria Sangrenta','+10% de poder de ataque e poder mágico por 15 s'],['a','Shatter Curse','Remove maldições e corrupção, −5% de dano mágico recebido por 8 s'],['p','Comando','+5% de dano dos mascotes de bruxo e caçador'],['p','Robustez','Atordoamentos duram 20% menos']],
    tip:'Fúria Sangrenta dá uma janela de dano poderosa.' },
  { id:'undead', n:'Morto-vivo', f:'horde',
    cls:['warrior','rogue','mage','priest','warlock','paladin*'],
    rac:[['a','Determinação dos Renegados','Remove enfeitiçamento, medo e sono'],['a','Canibalizar','Restaura 35% de vida e mana ao longo do tempo'],['p','Respiração Subaquática','Respira debaixo d’água por mais tempo'],['p','Toque do Túmulo','Chance de drenar vida ao atacar']],
    tip:'Nova combinação: um paladino para a Horda, onde essa classe não existia antes.' },
  { id:'tauren', n:'Taureno', f:'horde',
    cls:['warrior','hunter','shaman','druid'],
    rac:[['a','Pisada de Guerra','Atordoa inimigos próximos por 2 s, recarga de 90 s'],['a','Cultivo','Faz crescer ervas que podem ser colhidas sem Herborismo, recarga de 15 min'],['p','Vencer Planícies','Enquanto você se move, a velocidade de corrida sobe 2% por acúmulo, até +60%. Não afeta a velocidade montado'],['p','Resistência','+5% de vida']],
    tip:'A única raça da Horda com druida, a menos que você pegue Skyborne.' },
  { id:'troll', n:'Troll', f:'horde',
    cls:['warrior','hunter','rogue','priest','shaman','mage','warlock*'],
    rac:[['a','Berserk','+10% de velocidade de ataque e de feitiço por 12 s, recarga de 3 min'],['a','Regeneração Rápida','Restaura vida ao longo do tempo'],['p','Matança de Feras','+5% de dano contra feras'],['p','Regeneração','A vida se regenera também em combate']],
    tip:'O maior número de classes na Horda: sete.' },
  { id:'skyH', n:'Skyborne (Horda)', f:'horde', paid:true, name:'Skyborne Windshaper',
    cls:['warrior','hunter','rogue','shaman','druid'],
    rac:[['a','Walk on Air','Plana para baixo por 10 s, sem dano de queda'],['a','Skysight','+15% de velocidade por 15 s. Numa Elemental Convergence, também Charged por 1 hora: +30%, continua após a morte'],['p','Wind Blessed','+2% de velocidade de ataque e de feitiços'],['p','Elemental Insight','+5% de dano contra elementais']],
    tip:'Raça paga: Heroic Pack a partir de $29.99. Só a Horda pode ter xamã, só a Aliança, mago.' }
];
RACES.forEach(r => { r.can = {}; r.cls.forEach(c => { const isNew = c.endsWith('*'); r.can[isNew ? c.slice(0,-1) : c] = isNew ? 'new' : 'ok'; }); });
const CL = Object.fromEntries(CLASSES.map(c => [c.id, c]));
const BETA = '<span class="beta-note">segundo os dados da beta</span>';
const BMARK = '{' + 'beta}';   // split so the guide build (which swaps the marker for the span everywhere) leaves it alone
const racx = s => String(s).split(BETA).join(BMARK).split(BMARK).map(esc).join(BETA);
const RC = Object.fromEntries(RACES.map(r => [r.id, r]));
const RLEAD = {"human": "A raça mais numerosa da Aliança. Versátil e forte no PvP graças a Desejo de Sobreviver.", "dwarf": "Mineiros e fuzileiros robustos de Altoforno. Pela primeira vez a Aliança tem xamãs, e são anões: no Classic não havia.", "nightelf": "Um povo antigo das florestas. Esquivos: seu próprio jeito de se esconder, esquivar e correr rápido.", "gnome": "Os inventores de Gnomeregan. Pequenos, astutos e com a melhor habilidade de fuga do jogo.", "skyA": "Uma nova raça no Forever. A High Order: elfos do vento em busca da magia arcana perdida dos seus ancestrais.", "orc": "O coração da Horda. Os guerreiros mais fortes e mestres do PvP graças a Fúria Sangrenta e Robustez.", "undead": "Os Renegados: ex-humanos que se libertaram do Lich Rei. Imunes a medo e sono quando importa.", "tauren": "Gigantes pacíficos das planícies. A maior vida e seu próprio atordoamento em área.", "troll": "A tribo Lançanegra. O maior número de classes na Horda e um Berserk forte para dano.", "skyH": "Uma nova raça no Forever. Os Windshapers: líderes espirituais dos Skyborne, próximos aos elementos."}; // race page leads and URL slugs, filled in by build.py
const RSLUG = {"human": "human", "dwarf": "dwarf", "nightelf": "night-elf", "gnome": "gnome", "skyA": "skyborne-alliance", "orc": "orc", "undead": "undead", "tauren": "tauren", "troll": "troll", "skyH": "skyborne-horde"};

const EN = {
  'Armas':'Arms','Fúria':'Fury','Proteção':'Protection','Sagrado':'Holy','Retribuição':'Retribution',
  'Domínio das Feras':'Beast Mastery','Precisão':'Marksmanship','Sobrevivência':'Survival',
  'Assassinato':'Assassination','Combate':'Combat','Subterfúgio':'Subtlety',
  'Disciplina':'Discipline','Sombra':'Shadow','Elemental':'Elemental','Aperfeiçoamento':'Enhancement','Restauração':'Restoration',
  'Arcano':'Arcane','Fogo':'Fire','Gélido':'Frost','Suplício':'Affliction','Demonologia':'Demonology','Destruição':'Destruction',
  'Equilíbrio':'Balance','Combate Feral':'Feral',
  'Desejo de Sobreviver':'Will to Survive','Percepção':'Perception','Ruthless':'Ruthless','O Espírito Humano':'The Human Spirit',
  'Forma de Pedra':'Stoneform','Localizar Tesouros':'Find Treasure','Earth Fury':'Earth Fury','Big Game Hunter':'Big Game Hunter',
  'Luz de Eluna':"Elune’s Light",'Fusão Sombria':'Shadowmeld','Rapidez':'Quickness','Espírito de Fogo-fátuo':'Wisp Spirit',
  'Artista da Fuga':'Escape Artist','Eureca!':'Eureka!','Mente Expansiva':'Expansive Mind','Especialização em Engenharia':'Engineering Specialization',
  'Walk on Air':'Walk on Air','Read Ley Line':'Read Ley Line','Wind Blessed':'Wind Blessed','Elemental Insight':'Elemental Insight','Skysight':'Skysight',
  'Fúria Sangrenta':'Blood Fury','Shatter Curse':'Shatter Curse','Savage':'Savage','Comando':'Command','Robustez':'Hardiness',
  'Determinação dos Renegados':'Will of the Forsaken','Canibalizar':'Cannibalize','Respiração Subaquática':'Underwater Breathing','Toque do Túmulo':'Touch of the Grave',
  'Pisada de Guerra':'War Stomp','Cultivo':'Cultivation','Vencer Planícies':'Plainsrunning','Resistência':'Endurance',
  'Berserk':'Berserking','Regeneração Rápida':'Rapid Regeneration','Matança de Feras':'Beast Slaying','Regeneração':'Regeneration'
};
RC.skyA.en = 'High Order Skyborne'; RC.skyH.en = 'Windshaper Skyborne';
const tipBox = h => `<div class="tipbox"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg><p><span class="tl">Dica</span>${h}</p></div>`;
function bi(ru) { return EN[ru] && EN[ru] !== ru ? `${esc(ru)} <span class="en">(${esc(EN[ru])})</span>` : esc(ru); }
function raceEn(r) { return r.en ? ` <span class="en">/ ${esc(r.en)}</span>` : ''; }
function facName(f) { return f === 'alliance' ? 'Aliança' : 'Horda'; }
const PV = /*PV*/'?v=03c9d4a0';   // ?v= of the class and race portraits, filled in by build.art_version (redrawn under the same names)
/* Round face avatar: assets/art/<id>-face.webp, ring colour cc */
/* A class face follows the reader's side (GabellaPor, build.por_js); f: a fixed side (the class faces of a race row) */
function face(id, cc, cls = '', title = '', f = '') { const P = window.GabellaPor, t = `../assets/art/{${id}}-face.webp${PV}`, live = P && P.map[id] && !f;
  return `<span class="av ${cls}" style="--cc:${cc}"${title ? ` title="${esc(title)}"` : ''}><img src="../assets/art/${P ? P.id(id, f) : id}-face.webp${PV}"${live ? ` data-por-src="${t}"` : ''} width="160" height="160" alt="" loading="lazy" decoding="async"></span>`; }
function lvlMeter(c) {
  const p = c.lp || 0, w = Math.min(Math.abs(p) / 12 * 46, 46);
  const label = p < 0 ? `Mais rápido em ${-p}%` : p > 0 ? `Mais lento em ${p}%` : 'Ritmo médio';
  const bar = p ? `<i class="${p > 0 ? 'slow' : ''}" style="${p < 0 ? 'right' : 'left'}:50%;width:${w}%"></i>` : '';
  return `<span class="lvl"><span>${label}</span><span class="bar" role="img" aria-label="${label}">${bar}</span><span class="scale" aria-hidden="true"><span>mais rápido</span><span>mais lento</span></span></span>`;
}
function renderClassRef() {
  const roles = ['tank', 'heal', 'dps'];
  const head = `<div class="cmp-h" aria-hidden="true"><span>Classe</span><span class="rdots">${roles.map(x => `<span title="${ROLE_RU[x]}">${ri(x)}</span>`).join('')}</span><span>Evolução</span><span>Em raides</span><span></span></div>`;
  const box = $('#classRef');
  box.innerHTML = head + CLASSES.map(c => `<div class="cmp-row" style="--cc:${CCOL[c.id]};--art:url('../assets/art/${window.GabellaPor ? GabellaPor.id(c.id) : c.id}-360.webp${PV}')">
    <span class="cmp-id">${face(c.id, CCOL[c.id])}<span><b><a class="cmp-a" href="${HOME}classes/${c.id}/">${esc(c.n)}</a></b><small>${c.specs.map(s => esc(s[0])).join(' · ')}</small></span></span>
    <span class="rdots" role="img" aria-label="Funções: ${c.roles.map(x => ROLE_RU[x]).join(', ')}">${roles.map(x => { const on = c.roles.includes(x), q = c.roles.includes(x + '?'); return `<span class="rdot${on ? ' on' : q ? ' q' : ''}" title="${ROLE_RU[q ? x + '?' : x]}">${ri(x)}</span>`; }).join('')}</span>
    ${lvlMeter(c)}
    <span class="cmp-d"><span class="cmp-txt" id="crt-${c.id}">${esc(c.raid)}</span><button type="button" class="cmp-more" aria-expanded="false" aria-controls="crt-${c.id}" aria-label="Mostrar tudo" title="Mostrar tudo"></button></span>
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
  const head = `<div class="cmp-h" aria-hidden="true"><span>Raça</span><span>Classes</span><span class="abl">Habilidades <span class="abt">ativa</span><span class="abt p">passiva</span></span><span></span></div>`;
  $('#raceRef').innerHTML = ['alliance', 'horde'].map(f => `<div class="rgroup ${f}"><h3>${facName(f)}</h3>${head}` + RACES.filter(r => r.f === f).map(r => `<a class="cmp-row" href="${HOME}races/${RSLUG[r.id]}/" style="--cc:var(--${f});--art:url('../assets/art/${RSLUG[r.id]}-360.webp${PV}')">
    <span class="cmp-id">${face(RSLUG[r.id], `var(--${f})`)}<span><b>${esc(r.n)}${r.paid ? '<span class="paid">paga</span>' : ''}</b>${r.en ? `<small>${esc(r.en)}</small>` : ''}</span></span>
    <span class="ccl" role="img" aria-label="Classes: ${Object.keys(r.can).map(id => CL[id].n).join(', ')}">${CLASSES.map(c => { const v = r.can[c.id]; return face(c.id, CCOL[c.id], v ? (v === 'new' ? 'nw' : '') : 'off', c.n + (v === 'new' ? ', nova' : v ? '' : ', indisponível'), f); }).join('')}</span>
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
    const wh = feed.slice(0, 2).map(x => ({ d: x.date, html: `<a class="nc" href="${esc(x.url)}" target="_blank" rel="noopener"><time datetime="${esc(x.date)}">${x.date.slice(8, 10)}.${x.date.slice(5, 7)}</time><b lang="en">${esc(x.title)}</b><span>${'Wowhead, em inglês'}</span></a>` }));
    const all = ours.concat(bz, wh).sort((a, b) => (a.d < b.d ? 1 : a.d > b.d ? -1 : (b.o || 0) - (a.o || 0))).slice(0, 3);
    if (all.some(x => wh.includes(x) || bz.includes(x))) row.innerHTML = all.map(x => x.html).join('');
  });
})();
/* #peoples: the races block of the old home (old links) lives on the races page now */
if (location.hash === '#peoples') location.replace('races/');
