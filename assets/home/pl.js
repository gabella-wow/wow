const HOME = '';   // language home, the classes/ and races/ pages set their own
/* ref:start — shared with the classes/ and races/ pages (build_guides.ref_js); no $ or esc here, every page defines its own */
const CLASSES = [
  { id:'warrior', n:'Warrior', s:'Warrior', roles:['tank','dps'],
    specs:[['Arms','Obrażenia w zwarciu (broń dwuręczna)',['dps']],['Fury','Obrażenia w zwarciu (dual wield)',['dps']],['Protection','Tank',['tank']]],
    lvl:'Najwolniejszy leveling, około 12% dłużej niż średnia (szacunek LFCarry)',
    lp:12,
    raid:'Battle Shout działa na cały raid',
    forever:'Więcej Rage, lepsze aggro na grupach celów, talent Weapon Master. Fury i Bloodthirst osłabione.' },
  { id:'paladin', n:'Paladin', roles:['tank','heal','dps'],
    specs:[['Holy','Healer',['heal']],['Protection','Tank',['tank']],['Retribution','Obrażenia w zwarciu',['dps']]],
    lvl:'Średnie tempo levelowania',
    lp:0,
    raid:'Blessing of Kings jest teraz bazowe. Według list z bety Protection to jeden z najmocniejszych tanków, a Retribution spadł po patchu z 15 października.',
    forever:'Holy Strike od levelu 6, Judgement nie zużywa seala. Undead mogą teraz być paladynami, więc klasa pojawiła się w Horde.' },
  { id:'hunter', n:'Hunter', roles:['dps'],
    specs:[['Beast Mastery','Obrażenia dystansowe, dużo obrażeń od peta',['dps']],['Marksmanship','Obrażenia dystansowe',['dps']],['Survival','Zwarcie i dystans, pułapki',['dps']]],
    lvl:'Najszybszy leveling, około 8% szybciej niż średnia (szacunek LFCarry)',
    lp:-8,
    raid:'Trueshot Aura działa na cały raid',
    forever:'Można grać bez peta, pułapki działają w walce, pojawiła się rodzina petów lisy. Survival może grać w zwarciu.' },
  { id:'rogue', n:'Rogue', roles:['dps'],
    specs:[['Assassination','Obrażenia od trucizn',['dps']],['Combat','Szybkie ataki bronią',['dps']],['Subtlety','Zasadzki, krwawienia',['dps']]],
    lvl:'Średnie tempo levelowania',
    lp:0,
    raid:'Czyste obrażenia w zwarciu, bez buffów na cały raid',
    forever:'Można teraz używać jednoręcznych toporów. Assassination opiera się na truciznach, Subtlety na krwawieniach i stealthu.' },
  { id:'priest', n:'Priest', roles:['heal','dps'],
    specs:[['Discipline','Healer, tarcze i absorpcja',['heal']],['Holy','Healer',['heal']],['Shadow','Obrażenia dystansowe',['dps']]],
    lvl:'Około 5% wolniej niż średnia (szacunek LFCarry)',
    lp:5,
    raid:'Divine Spirit jest teraz bazowe. Obrażenia Shadow i Devouring Plague (24 sek. cooldownu) zostały wzmocnione w patchu z 15 października.',
    forever:'Fear Ward i Devouring Plague są dostępne od levelu 20 dla każdej rasy. Każda rasa ma dwa własne zaklęcia priesta.' },
  { id:'shaman', n:'Shaman', roles:['heal','dps','tank?'],
    specs:[['Elemental','Obrażenia dystansowe',['dps']],['Enhancement','Obrażenia w zwarciu. Możliwość tankowania wciąż pod znakiem zapytania',['dps','tank?']],['Restoration','Healer',['heal']]],
    lvl:'Średnie tempo levelowania',
    lp:0,
    raid:'Totemy Strength of Earth, Windfury, Flametongue i Grace of Air buffują swoją grupę',
    forever:'Krasnoludy mogą teraz być shamanami, więc klasa pojawiła się w Alliance. Lava Burst wzmocniony, Elemental poszedł w górę w rankingach obrażeń.' },
  { id:'mage', n:'Mage', roles:['dps'],
    specs:[['Arcane','Burst, dużo many',['dps']],['Fire','Kryty i ignite',['dps']],['Frost','Obrażenia i kontrola',['dps']]],
    lvl:'Najszybszy leveling, około 8% szybciej niż średnia, oszczędność około 12 godzin (szacunek LFCarry)',
    lp:-8,
    raid:'Portale, jedzenie i woda dla grupy',
    forever:'Fire dostał Hotstreak, Arcane Arcane Blast, Frost Ice Lance. Frostfire Bolt jest dostępny od levelu 40.' },
  { id:'warlock', n:'Warlock', roles:['dps'],
    specs:[['Affliction','Obrażenia od klątw i korupcji',['dps']],['Demonology','Obrażenia przez demony',['dps']],['Destruction','Bezpośrednie obrażenia od ognia i cienia',['dps']]],
    lvl:'Średnie tempo levelowania',
    lp:0,
    raid:'Mistrzostwo Mroku daje 2–10% obrażeń od Cienia, tak jak w Classic (we wczesnej becie 1–5%)',
    forever:'Affliction ma nowe zaklęcie channelowane, demon zostaje przy Demonic Sacrifice, Destruction dostał Incinerate i AoE.' },
  { id:'druid', n:'Druid', roles:['tank','heal','dps'],
    specs:[['Balance','Obrażenia dystansowe',['dps']],['Feral','Tank (miś) i obrażenia w zwarciu (kot)',['tank','dps']],['Restoration','Healer, dużo leczenia w czasie',['heal']]],
    lvl:'Około 5% wolniej niż średnia (szacunek LFCarry)',
    lp:5,
    raid:'Leader of the Pack i Moonkin Aura działają na cały raid i się stackują',
    forever:'Każda specjalizacja dostała jasną rolę, formy działają z miksturami i enchantami broni. Na jednej postaci możesz być tankiem, healerem i DPS-em.' }
];
const ROLE_RU = { tank:'Tank', heal:'Healer', dps:'DPS', 'tank?':'Tank (niepewne)' };
const ri = r => `<svg class="ri" aria-hidden="true"><use href="#i-${r.replace('?','')}"/></svg>`;
const CCOL = { warrior:'#c79c6e', paladin:'#f58cba', hunter:'#abd473', rogue:'#fff569', priest:'#e8e8e8', shaman:'#2f8cf0', mage:'#40c7eb', warlock:'#8788ee', druid:'#ff7d0a' };
const BUFF = { warrior:'Battle Shout', paladin:'Blessing of Kings', hunter:'Trueshot Aura', priest:'Power Word: Fortitude, Divine Spirit', shaman:'Totemy (Strength of Earth, Windfury, Flametongue, Grace of Air)', mage:'Arcane Intellect, portale, jedzenie i woda', druid:'Mark of the Wild, Leader of the Pack, Moonkin Aura' };

const RACES = [
  { id:'human', n:'Human', f:'alliance',
    cls:['warrior','paladin','hunter*','rogue','priest','mage','warlock'],
    rac:[['a','Will to Survive','Usuwa ogłuszenie'],['a','Perception','Ujawnia niewidzialnych wrogów na 20 sek.'],['p','Ruthless','+1% szansy na kryta'],['p','The Human Spirit','+10% spirit']],
    tip:'Spirit przekłada się na leczenie u Holy Priesta, więc Human priest dobrze sprawdza się w leczeniu.' },
  { id:'dwarf', n:'Dwarf', f:'alliance',
    cls:['warrior','paladin','hunter','rogue','priest','shaman*'],
    rac:[['a','Stoneform','Odporność na krwawienia, trucizny i choroby przez 8 sek. oraz mniejsze obrażenia fizyczne'],['a','Find Treasure','Pokazuje pobliskie skrzynie i daje szansę na dodatkowe przedmioty w większości skrzyń'],['p','Artisan’s Precision','+1% szansy na trafienie zaklęciami i atakami'],['p','Big Game Hunter','+5% obrażeń przeciw bestiom']],
    tip:'Stoneform przydaje się tankom i w PvP.' },
  { id:'nightelf', n:'Night Elf', f:'alliance',
    cls:['warrior','hunter','rogue','priest','druid'],
    rac:[['a','Elune’s Light','+10% szansy na kryta przez 15 sek.'],['a','Shadowmeld','Niewidzialność w miejscu'],['p','Quickness','+2% do uniku i do szybkości biegu (Warcraft Tavern podaje 1% uniku) {beta}'],['p','Wisp Spirit','+75% szybkości biegu jako duch (Warcraft Tavern podaje 25%) {beta}']],
    tip:'Jedyna rasa Alliance z druidem, chyba że weźmiesz Skyborne.' },
  { id:'gnome', n:'Gnome', f:'alliance',
    cls:['warrior','rogue','mage','warlock','priest*'],
    rac:[['a','Escape Artist','Krótka odporność na spowolnienia i unieruchomienia'],['a','Eureka!','Przez 8 s zdolności są tańsze i o 10% silniejsze {beta}'],['p','Expansive Mind','+5% maksymalnej many, rage lub energii'],['p','Engineering Specialization','Urządzenia inżynieryjne działają bardziej niezawodnie']],
    tip:'Expansive Mind szczególnie pomaga klasom na energii.' },
  { id:'skyA', n:'Skyborne (Alliance)', f:'alliance', paid:true, name:'High Order Skyborne',
    cls:['warrior','hunter','rogue','mage','druid'],
    rac:[['a','Walk on Air','Szybowanie w dół przez 10 sek., bez obrażeń od upadku'],['a','Read Ley Line','Regeneracja zdrowia i many +50% na 15 sek. Przy Ley Line dodatkowo Attuned na 1 godzinę: +100%, zostaje po śmierci'],['p','Wind Blessed','+2% szybkości ataku i rzucania zaklęć'],['p','Elemental Insight','+5% obrażeń przeciw żywiołakom']],
    tip:'Płatna rasa: Heroic Pack od $29.99. Start w lokacji Zephras Isle (levele 1–12).' },
  { id:'orc', n:'Orc', f:'horde',
    cls:['warrior','hunter','rogue','shaman','warlock','mage*'],
    rac:[['a','Blood Fury','+10% attack power i spell power przez 15 sek.'],['a','Shatter Curse','Usuwa klątwy i korupcję, −5% otrzymywanych obrażeń magicznych przez 8 sek.'],['p','Command','+5% obrażeń petów warlocka i huntera'],['p','Hardiness','Ogłuszenia są o 20% krótsze']],
    tip:'Blood Fury daje mocne okno na obrażenia.' },
  { id:'undead', n:'Undead', f:'horde',
    cls:['warrior','rogue','mage','priest','warlock','paladin*'],
    rac:[['a','Will of the Forsaken','Usuwa charm, fear i sen'],['a','Cannibalize','Przywraca 35% zdrowia i many w czasie'],['p','Underwater Breathing','Dłuższe oddychanie pod wodą'],['p','Touch of the Grave','Szansa na wyssanie zdrowia przy ataku']],
    tip:'Nowa kombinacja: paladyn dla Horde, w której tej klasy wcześniej nie było.' },
  { id:'tauren', n:'Tauren', f:'horde',
    cls:['warrior','hunter','shaman','druid'],
    rac:[['a','War Stomp','Ogłusza pobliskich wrogów na 2 sek., cooldown 90 sek.'],['a','Cultivation','Wyhodowane zioła można zbierać bez Herbalism, cooldown 15 min'],['p','Plainsrunning','Dopóki się ruszasz, szybkość biegu rośnie o 2% na stack, do +60%. Nie działa na szybkość na wierzchowcu'],['p','Endurance','+5% zdrowia']],
    tip:'Jedyna rasa Horde z druidem, chyba że weźmiesz Skyborne.' },
  { id:'troll', n:'Troll', f:'horde',
    cls:['warrior','hunter','rogue','priest','shaman','mage','warlock*'],
    rac:[['a','Berserking','+10% do szybkości ataku i czarów przez 12 s, cooldown 3 min'],['a','Rapid Regeneration','Przywraca zdrowie w czasie'],['p','Beast Slaying','+5% obrażeń przeciw bestiom'],['p','Regeneration','Zdrowie regeneruje się także w walce']],
    tip:'Najwięcej opcji klas w Horde: siedem.' },
  { id:'skyH', n:'Skyborne (Horde)', f:'horde', paid:true, name:'Windshaper Skyborne',
    cls:['warrior','hunter','rogue','shaman','druid'],
    rac:[['a','Walk on Air','Szybowanie w dół przez 10 sek., bez obrażeń od upadku'],['a','Skysight','+15% szybkości biegu na 15 sek. Przy Elemental Convergence dodatkowo Charged na 1 godzinę: +30%, zostaje po śmierci'],['p','Wind Blessed','+2% szybkości ataku i rzucania zaklęć'],['p','Elemental Insight','+5% obrażeń przeciw żywiołakom']],
    tip:'Płatna rasa: Heroic Pack od $29.99. Tylko Horde może mieć shamana, tylko Alliance maga.' }
];
RACES.forEach(r => { r.can = {}; r.cls.forEach(c => { const isNew = c.endsWith('*'); r.can[isNew ? c.slice(0,-1) : c] = isNew ? 'new' : 'ok'; }); });
const CL = Object.fromEntries(CLASSES.map(c => [c.id, c]));
const BETA = '<span class="beta-note">wg danych z bety</span>';
const BMARK = '{' + 'beta}';   // split so the guide build (which swaps the marker for the span everywhere) leaves it alone
const racx = s => String(s).split(BETA).join(BMARK).split(BMARK).map(esc).join(BETA);
const RC = Object.fromEntries(RACES.map(r => [r.id, r]));
const RLEAD = {"human": "Najliczniejsza rasa Alliance. Wszechstronna i mocna w PvP dzięki Will to Survive.", "dwarf": "Twardzi górnicy i strzelcy z Ironforge. Po raz pierwszy Alliance ma shamanów, i są to krasnoludy: w Classic ich nie było.", "nightelf": "Starożytny lud lasów. Nieuchwytni: własny sposób na ukrycie się, uniki i szybki bieg.", "gnome": "Wynalazcy z Gnomeregan. Mali, sprytni i z najlepszą zdolnością ucieczki w grze.", "skyA": "Nowa rasa w Forever. High Order: elfy wiatru szukające utraconej magii arkanów swoich przodków.", "orc": "Serce Horde. Najsilniejsi wojownicy i mistrzowie PvP dzięki Blood Fury i Hardiness.", "undead": "Forsaken: dawni ludzie, którzy wyrwali się spod władzy Lich Kinga. Odporni na fear i sen, kiedy to się liczy.", "tauren": "Pokojowe olbrzymy z równin. Najwięcej zdrowia i własne obszarowe ogłuszenie.", "troll": "Plemię Darkspear. Najwięcej klas w Horde i mocny Berserking na obrażenia.", "skyH": "Nowa rasa w Forever. Windshaper: duchowi przywódcy Skyborne, bliscy żywiołom."}; // race page leads and URL slugs, filled in by build.py
const RSLUG = {"human": "human", "dwarf": "dwarf", "nightelf": "night-elf", "gnome": "gnome", "skyA": "skyborne-alliance", "orc": "orc", "undead": "undead", "tauren": "tauren", "troll": "troll", "skyH": "skyborne-horde"};

const EN = {
  'Arms':'Arms','Fury':'Fury','Protection':'Protection','Holy':'Holy','Retribution':'Retribution',
  'Beast Mastery':'Beast Mastery','Marksmanship':'Marksmanship','Survival':'Survival',
  'Assassination':'Assassination','Combat':'Combat','Subtlety':'Subtlety',
  'Discipline':'Discipline','Shadow':'Shadow','Elemental':'Elemental','Enhancement':'Enhancement','Restoration':'Restoration',
  'Arcane':'Arcane','Fire':'Fire','Frost':'Frost','Affliction':'Affliction','Demonology':'Demonology','Destruction':'Destruction',
  'Balance':'Balance','Feral':'Feral',
  'Will to Survive':'Will to Survive','Perception':'Perception','Ruthless':'Ruthless','The Human Spirit':'The Human Spirit',
  'Stoneform':'Stoneform','Find Treasure':'Find Treasure','Earth Fury':'Earth Fury','Big Game Hunter':'Big Game Hunter',
  'Elune’s Light':"Elune’s Light",'Shadowmeld':'Shadowmeld','Quickness':'Quickness','Wisp Spirit':'Wisp Spirit',
  'Escape Artist':'Escape Artist','Eureka!':'Eureka!','Expansive Mind':'Expansive Mind','Engineering Specialization':'Engineering Specialization',
  'Walk on Air':'Walk on Air','Read Ley Line':'Read Ley Line','Wind Blessed':'Wind Blessed','Elemental Insight':'Elemental Insight','Skysight':'Skysight',
  'Blood Fury':'Blood Fury','Shatter Curse':'Shatter Curse','Savage':'Savage','Command':'Command','Hardiness':'Hardiness',
  'Will of the Forsaken':'Will of the Forsaken','Cannibalize':'Cannibalize','Underwater Breathing':'Underwater Breathing','Touch of the Grave':'Touch of the Grave',
  'War Stomp':'War Stomp','Cultivation':'Cultivation','Plainsrunning':'Plainsrunning','Endurance':'Endurance',
  'Berserking':'Berserking','Rapid Regeneration':'Rapid Regeneration','Beast Slaying':'Beast Slaying','Regeneration':'Regeneration'
};
RC.skyA.en = 'High Order Skyborne'; RC.skyH.en = 'Windshaper Skyborne';
const tipBox = h => `<div class="tipbox"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg><p><span class="tl">Porada</span>${h}</p></div>`;
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
  const label = p < 0 ? `Szybciej o ${-p}%` : p > 0 ? `Wolniej o ${p}%` : 'Średnie tempo';
  const bar = p ? `<i class="${p > 0 ? 'slow' : ''}" style="${p < 0 ? 'right' : 'left'}:50%;width:${w}%"></i>` : '';
  return `<span class="lvl"><span>${label}</span><span class="bar" role="img" aria-label="${label}">${bar}</span><span class="scale" aria-hidden="true"><span>szybciej</span><span>wolniej</span></span></span>`;
}
function renderClassRef() {
  const roles = ['tank', 'heal', 'dps'];
  const head = `<div class="cmp-h" aria-hidden="true"><span>Klasa</span><span class="rdots">${roles.map(x => `<span title="${ROLE_RU[x]}">${ri(x)}</span>`).join('')}</span><span>Levelowanie</span><span>Na raidach</span><span></span></div>`;
  const box = $('#classRef');
  box.innerHTML = head + CLASSES.map(c => `<div class="cmp-row" style="--cc:${CCOL[c.id]};--art:url('../assets/art/${window.GabellaPor ? GabellaPor.id(c.id) : c.id}-360.webp${PV}')">
    <span class="cmp-id">${face(c.id, CCOL[c.id])}<span><b><a class="cmp-a" href="${HOME}classes/${c.id}/">${esc(c.n)}</a></b><small>${c.specs.map(s => esc(s[0])).join(' · ')}</small></span></span>
    <span class="rdots" role="img" aria-label="Role: ${c.roles.map(x => ROLE_RU[x]).join(', ')}">${roles.map(x => { const on = c.roles.includes(x), q = c.roles.includes(x + '?'); return `<span class="rdot${on ? ' on' : q ? ' q' : ''}" title="${ROLE_RU[q ? x + '?' : x]}">${ri(x)}</span>`; }).join('')}</span>
    ${lvlMeter(c)}
    <span class="cmp-d"><span class="cmp-txt" id="crt-${c.id}">${esc(c.raid)}</span><button type="button" class="cmp-more" aria-expanded="false" aria-controls="crt-${c.id}" aria-label="Pokaż całość" title="Pokaż całość"></button></span>
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
  const head = `<div class="cmp-h" aria-hidden="true"><span>Rasa</span><span>Klasy</span><span class="abl">Zdolności <span class="abt">aktywna</span><span class="abt p">pasywna</span></span><span></span></div>`;
  $('#raceRef').innerHTML = ['alliance', 'horde'].map(f => `<div class="rgroup ${f}"><h3>${facName(f)}</h3>${head}` + RACES.filter(r => r.f === f).map(r => `<a class="cmp-row" href="${HOME}races/${RSLUG[r.id]}/" style="--cc:var(--${f});--art:url('../assets/art/${RSLUG[r.id]}-360.webp${PV}')">
    <span class="cmp-id">${face(RSLUG[r.id], `var(--${f})`)}<span><b>${esc(r.n)}${r.paid ? '<span class="paid">płatna</span>' : ''}</b>${r.en ? `<small>${esc(r.en)}</small>` : ''}</span></span>
    <span class="ccl" role="img" aria-label="Klasy: ${Object.keys(r.can).map(id => CL[id].n).join(', ')}">${CLASSES.map(c => { const v = r.can[c.id]; return face(c.id, CCOL[c.id], v ? (v === 'new' ? 'nw' : '') : 'off', c.n + (v === 'new' ? ', nowe' : v ? '' : ', niedostępne'), f); }).join('')}</span>
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
  warrior: 'Plate, rage i pierwsza linia. Przyjmuje ciosy jako tank albo kosi dwuręczniakiem.',
  paladin: 'Święty wojownik w plate: leczy, tankuje i wymachuje młotem. Teraz także w Horde.',
  hunter: 'Łuk, pułapki i wierna bestia u boku. Jedna z najszybciej levelujących klas.',
  rogue: 'Trucizny, ostrza i cień. Czyste obrażenia z zasadzki i kontrola tłumu.',
  priest: 'Światło i Cień w jednych rękach. Główny healer grupy albo mroczny caster.',
  shaman: 'Totemy i żywioły: leczy, uderza piorunami albo bronią. Teraz także w Alliance.',
  mage: 'Magia ognia, mrozu i arkanów. Portale, jedzenie i woda dla grupy.',
  warlock: 'Klątwy, demony i ogień. Obrażenia w czasie i własny demon do pomocy.',
  druid: 'Miś, kot, sowa albo healer: wszystkie trzy role na jednej postaci.'
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
    <span class="info"><b>${esc(c.n)}</b><span class="roles">${c.roles.filter(r => !r.endsWith('?')).map(r => `<span>${ri(r)}${ROLE_RU[r]}</span>`).join('')}</span><span class="d">${esc(DESC[c.id])}</span><span class="more">Więcej o klasie</span></span>
  </a>`).join('');
}
renderRoster();
/* Race roster: one row of portraits per faction, links to the race pages */
function renderPeoples() {
  [['alliance', '#rosterA'], ['horde', '#rosterH']].forEach(([f, sel]) => {
    $(sel).innerHTML = RACES.filter(r => r.f === f).map((r, i) => `<a class="hc${i === 0 ? ' on' : ''}" href="races/${RSLUG[r.id]}/" style="--cc:var(--${f})">
    <picture><source type="image/avif" srcset="${artSet(RSLUG[r.id], 'avif')}" sizes="${ART_SIZES}"><source type="image/webp" srcset="${artSet(RSLUG[r.id], 'webp')}" sizes="${ART_SIZES}"><img src="${ROOT}assets/art/${RSLUG[r.id]}-600.webp${PV}" width="896" height="1200" alt="" loading="lazy" decoding="async"></picture>
    <span class="vn" aria-hidden="true">${esc(raceName(r))}</span>
    <span class="info"><b>${esc(raceName(r))}</b>${r.paid ? '<span class="tag paid">płatna</span>' : ''}<span class="d">${esc(RLEAD[r.id])}</span><span class="more">Więcej o rasie</span></span>
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
    const wh = feed.slice(0, 2).map(x => ({ d: x.date, html: `<a class="nc" href="${esc(x.url)}" target="_blank" rel="noopener"><time datetime="${esc(x.date)}">${x.date.slice(8, 10)}.${x.date.slice(5, 7)}</time><b lang="en">${esc(x.title)}</b><span>${'Wowhead, po angielsku'}</span></a>` }));
    const all = ours.concat(bz, wh).sort((a, b) => (a.d < b.d ? 1 : a.d > b.d ? -1 : (b.o || 0) - (a.o || 0))).slice(0, 3);
    if (all.some(x => wh.includes(x) || bz.includes(x))) row.innerHTML = all.map(x => x.html).join('');
  });
})();
function hashTab() { if (location.hash === '#peoples') { showTab(TABS[1]); document.getElementById('classes').scrollIntoView(); } }
addEventListener('hashchange', hashTab);
hashTab();
