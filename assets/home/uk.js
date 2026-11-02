const HOME = '';   // language home, the classes/ and races/ pages set their own
/* ref:start — shared with the classes/ and races/ pages (build_guides.ref_js); no $ or esc here, every page defines its own */
const CLASSES = [
  { id:'warrior', n:'Воїн', s:'Воїн', roles:['tank','dps'],
    specs:[['Зброя','Шкода в ближньому бою (дворучна зброя)',['dps']],['Лють','Шкода в ближньому бою (дві зброї)',['dps']],['Захист','Танк',['tank']]],
    lvl:'Найповільніша прокачка, приблизно на 12% довше за середню (оцінка LFCarry)',
    lp:12,
    raid:'Бойовий клич діє на весь рейд',
    forever:'Більше Люті, краща загроза по групі цілей, талант Майстер зброї. Лють і Жага крові послаблені.' },
  { id:'paladin', n:'Паладин', roles:['tank','heal','dps'],
    specs:[['Світло','Цілитель',['heal']],['Захист','Танк',['tank']],['Відплата','Шкода в ближньому бою',['dps']]],
    lvl:'Середній темп прокачування',
    lp:0,
    raid:'Благословення королів тепер базове. За бета-списками Захист серед найсильніших танків, Відплата просіла після патча 15 жовтня.',
    forever:'Священний удар з 6 рівня, Правосуддя не витрачає печатку. Нежить тепер може бути паладином, отже клас з’явився в Орді.' },
  { id:'hunter', n:'Мисливець', roles:['dps'],
    specs:[['Володіння звірами','Шкода здалеку, багато шкоди від улюбленця',['dps']],['Стрільба','Шкода здалеку',['dps']],['Виживання','Ближній і дальній бій, пастки',['dps']]],
    lvl:'Найшвидша прокачка, приблизно на 8% швидше за середню (оцінка LFCarry)',
    lp:-8,
    raid:'Аура влучного стрільця діє на весь рейд',
    forever:'Можна грати без улюбленця, пастки працюють у бою, з’явилися лисиці як родина улюбленців. Виживання може йти в ближній бій.' },
  { id:'rogue', n:'Розбійник', roles:['dps'],
    specs:[['Ліквідація','Шкода отрутами',['dps']],['Бій','Швидкі атаки зброєю',['dps']],['Непомітність','Засідки, кровотечі',['dps']]],
    lvl:'Середній темп прокачування',
    lp:0,
    raid:'Чиста шкода в ближньому бою без баффів на весь рейд',
    forever:'Тепер можна використовувати одноручні сокири. Ліквідація будується на отрутах, Непомітність на кровотечах і невидимості.' },
  { id:'priest', n:'Жрець', roles:['heal','dps'],
    specs:[['Послух','Цілитель, щити та поглинання',['heal']],['Світло','Цілитель',['heal']],['Темрява','Шкода здалеку',['dps']]],
    lvl:'Приблизно на 5% повільніше за середню (оцінка LFCarry)',
    lp:5,
    raid:'Божественний дух став базовим. Шкоду Темряви та «Пожираючу чуму» (відновлення 24 сек) підсилено патчем 15 жовтня.',
    forever:'Захист від страху та «Пожираюча чума» доступні з 20 рівня будь-якій расі. У кожної раси по два своїх закляття жерця.' },
  { id:'shaman', n:'Шаман', roles:['heal','dps','tank?'],
    specs:[['Стихії','Шкода здалеку',['dps']],['Вдосконалення','Шкода в ближньому бою. Можливість танкувати поки під питанням',['dps','tank?']],['Зцілення','Цілитель',['heal']]],
    lvl:'Середній темп прокачування',
    lp:0,
    raid:'Тотеми сили землі, несамовитості вітру, язиків полум’я та грації повітря підсилюють свою групу',
    forever:'Дворфи тепер можуть бути шаманами, отже клас з’явився в Альянсі. Сплеск лави підсилено, Стихії піднялися в списках шкоди.' },
  { id:'mage', n:'Маг', roles:['dps'],
    specs:[['Тайна магія','Бурст, багато мани',['dps']],['Вогонь','Криті та підпали',['dps']],['Лід','Шкода і контроль',['dps']]],
    lvl:'Найшвидша прокачка, приблизно на 8% швидше за середню, близько 12 годин економії (оцінка LFCarry)',
    lp:-8,
    raid:'Портали, їжа й вода для групи',
    forever:'Вогонь отримав Hotstreak, Тайна магія — Arcane Blast, Лід — Крижаний спис. Вогняно-крижана стріла доступна з 40 рівня.' },
  { id:'warlock', n:'Чорнокнижник', roles:['dps'],
    specs:[['Прокляття','Шкода від прокляттів і псування',['dps']],['Демонологія','Шкода через демонів',['dps']],['Руйнування','Пряма шкода вогнем і темрявою',['dps']]],
    lvl:'Середній темп прокачування',
    lp:0,
    raid:'Мастерство тьмы дає 2–10% шкоди від темряви, як у Classic (у ранній беті було 1–5%)',
    forever:'У Прокляття нове закляття з наведенням, демон лишається при Жертві демона, у Руйнування з’явилися Спалення та AoE.' },
  { id:'druid', n:'Друїд', roles:['tank','heal','dps'],
    specs:[['Баланс','Шкода здалеку',['dps']],['Сила звіра','Танк (ведмідь) і шкода в ближньому бою (кішка)',['tank','dps']],['Зцілення','Цілитель, багато лікування з часом',['heal']]],
    lvl:'Приблизно на 5% повільніше за середню (оцінка LFCarry)',
    lp:5,
    raid:'Ватажок зграї та аура місячного совиця діють на весь рейд і складаються',
    forever:'Кожна спеціалізація отримала чітку роль, форми працюють із зіллями та чарами на зброї. Можна бути танком, цілителем і бійцем на одному персонажі.' }
];
const ROLE_RU = { tank:'Танк', heal:'Цілитель', dps:'Шкода', 'tank?':'Танк (під питанням)' };
const ri = r => `<svg class="ri" aria-hidden="true"><use href="#i-${r.replace('?','')}"/></svg>`;
const CCOL = { warrior:'#c79c6e', paladin:'#f58cba', hunter:'#abd473', rogue:'#fff569', priest:'#e8e8e8', shaman:'#2f8cf0', mage:'#40c7eb', warlock:'#8788ee', druid:'#ff7d0a' };
const BUFF = { warrior:'Бойовий клич', paladin:'Благословення королів', hunter:'Аура влучного стрільця', priest:'Power Word: Fortitude, Божественний дух', shaman:'Тотеми (сила землі, несамовитість вітру, язики полум’я, грація повітря)', mage:'Arcane Intellect, портали, їжа та вода', druid:'Mark of the Wild, Ватажок зграї, аура місячного совиця' };

const RACES = [
  { id:'human', n:'Людина', f:'alliance',
    cls:['warrior','paladin','hunter*','rogue','priest','mage','warlock'],
    rac:[['a','Воля до життя','Знімає приголомшення'],['a','Уважність','Показує невидимих ворогів на 20 сек'],['p','Безжальність','+1% шанс крита'],['p','Людський дух','+10% до духу']],
    tip:'Дух іде в лікування Жрецю Світла, тож Людина-жрець добра для цілителя.' },
  { id:'dwarf', n:'Дворф', f:'alliance',
    cls:['warrior','paladin','hunter','rogue','priest','shaman*'],
    rac:[['a','Кам’яна форма','Імунітет до кровотеч, отрут і хвороб на 8 сек і зниження фізичної шкоди'],['a','Пошук скарбів','Показує скрині поруч і дає шанс на додаткові предмети в більшості скринь'],['p','Artisan’s Precision','+1% до влучності заклять і атак'],['p','Мисливець на велику дичину','+5% шкоди по звірах']],
    tip:'Кам’яна форма корисна танку й у PvP.' },
  { id:'nightelf', n:'Нічний ельф', f:'alliance',
    cls:['warrior','hunter','rogue','priest','druid'],
    rac:[['a','Світло Елуни','+10% до шансу крита на 15 сек'],['a','Злиття з тінню','Невидимість на місці'],['p','Спритність','+2% до ухилення та швидкості бігу (у Warcraft Tavern ухилення 1%) {beta}'],['p','Дух-вогник','+75% до швидкості бігу у вигляді духу (Warcraft Tavern пише 25%) {beta}']],
    tip:'Єдина раса Альянсу з друїдом, якщо не брати Скайборн.' },
  { id:'gnome', n:'Гном', f:'alliance',
    cls:['warrior','rogue','mage','warlock','priest*'],
    rac:[['a','Майстер втечі','Короткий імунітет до уповільнення та коренів'],['a','Еврика!','На 8 с здібності дешевші й на 10% сильніші {beta}'],['p','Допитливий розум','+5% до максимуму мани, люті або енергії'],['p','Спеціалізація: інженерія','Інженерні пристрої спрацьовують надійніше']],
    tip:'Допитливий розум особливо виручає класам на енергії.' },
  { id:'skyA', n:'Скайборн (Альянс)', f:'alliance', paid:true, name:'Високий скайборн',
    cls:['warrior','hunter','rogue','mage','druid'],
    rac:[['a','Ходіння повітрям','Планування вниз 10 сек, немає шкоди від падіння'],['a','Читання лей-ліній','Відновлення здоров’я та мани +50% на 15 сек. Біля Ley Line ще Attuned на 1 годину: +100%, не спадає після смерті'],['p','Благословення вітру','+2% до швидкості атаки та заклять'],['p','Прозріння стихій','+5% шкоди по елементалях']],
    tip:'Платна раса: набір Heroic Pack від $29.99. Старт у локації Zephras Isle (1–12 рівні).' },
  { id:'orc', n:'Орк', f:'horde',
    cls:['warrior','hunter','rogue','shaman','warlock','mage*'],
    rac:[['a','Кривава лють','+10% до сили атаки та заклять на 15 сек'],['a','Руйнування прокляттів','Знімає прокляття і псування, магічна шкода по вас −5% на 8 сек'],['p','Command','+5% до шкоди улюбленців чорнокнижника й мисливця'],['p','Загартування','Приголомшення коротші на 20%']],
    tip:'Кривава лють дає потужне вікно шкоди.' },
  { id:'undead', n:'Нежить', f:'horde',
    cls:['warrior','rogue','mage','priest','warlock','paladin*'],
    rac:[['a','Воля Відрікшихся','Знімає зачарування, страх і сон'],['a','Канібалізм','Відновлює 35% здоров’я та мани з часом'],['p','Підводне дихання','Дихання під водою довше'],['p','Дотик могили','Шанс висмоктати здоров’я під час атаки']],
    tip:'Нова комбінація: паладин в Орді, де раніше цього класу не було.' },
  { id:'tauren', n:'Таурен', f:'horde',
    cls:['warrior','hunter','shaman','druid'],
    rac:[['a','Тупіт війни','Приголомшує ворогів поруч на 2 сек, відкат 90 сек'],['a','Культивація','Вирощує трави, які можна зібрати без травництва, відкат 15 хв'],['p','Біг рівнинами','Поки ви рухаєтеся, швидкість бігу росте на 2% за заряд, до +60%. На їзду верхи не діє'],['p','Витривалість','+5% здоров’я']],
    tip:'Єдина раса Орди з друїдом, якщо не брати Скайборн.' },
  { id:'troll', n:'Троль', f:'horde',
    cls:['warrior','hunter','rogue','priest','shaman','mage','warlock*'],
    rac:[['a','Берсерк','+10% до швидкості атаки й заклять на 12 с, відкат 3 хв'],['a','Швидке відновлення','Відновлює здоров’я з часом'],['p','Убивця звірів','+5% шкоди по звірах'],['p','Регенерація','Здоров’я відновлюється і в бою']],
    tip:'Найбільше варіантів класів в Орді: сім.' },
  { id:'skyH', n:'Скайборн (Орда)', f:'horde', paid:true, name:'Скайборн-вітрорізь',
    cls:['warrior','hunter','rogue','shaman','druid'],
    rac:[['a','Ходіння повітрям','Планування вниз 10 сек, немає шкоди від падіння'],['a','Погляд у небо','+15% до швидкості бігу на 15 сек. Біля Elemental Convergence ще Charged на 1 годину: +30%, не спадає після смерті'],['p','Благословення вітру','+2% до швидкості атаки та заклять'],['p','Прозріння стихій','+5% шкоди по елементалях']],
    tip:'Платна раса: набір Heroic Pack від $29.99. Шаманом може бути лише Орда, магом лише Альянс.' }
];
RACES.forEach(r => { r.can = {}; r.cls.forEach(c => { const isNew = c.endsWith('*'); r.can[isNew ? c.slice(0,-1) : c] = isNew ? 'new' : 'ok'; }); });
const CL = Object.fromEntries(CLASSES.map(c => [c.id, c]));
const BETA = '<span class="beta-note">за даними бети</span>';
const BMARK = '{' + 'beta}';   // split so the guide build (which swaps the marker for the span everywhere) leaves it alone
const racx = s => String(s).split(BETA).join(BMARK).split(BMARK).map(esc).join(BETA);
const RC = Object.fromEntries(RACES.map(r => [r.id, r]));
const RLEAD = {"human": "Найчисленніша раса Альянсу. Універсальна й сильна в PvP завдяки Will to Survive.", "dwarf": "Міцні гірники та стрільці Ironforge. Уперше Альянс має шаманів, і це дворфи: у Classic такого не було.", "nightelf": "Давній народ лісів. Невловимі: власний спосіб сховатися, ухилення та швидкий біг.", "gnome": "Винахідники Gnomeregan. Маленькі, хитрі й з найкращою здібністю втечі в грі.", "skyA": "Нова раса Forever. Вищий орден: ельфи вітру, які шукають втрачену таємну магію предків.", "orc": "Серце Орди. Найсильніші воїни та майстри PvP завдяки Blood Fury і Hardiness.", "undead": "Відреклі: колишні люди, що вирвалися з-під влади Короля-ліча. Не бояться страху та сну.", "tauren": "Мирні велетні рівнин. Найбільше здоров’я та власний масовий оглушливий удар.", "troll": "Плем’я Darkspear. Найбільше класів в Орді та сильний Berserking для шкоди.", "skyH": "Нова раса Forever. Вітрорізи: духовні лідери скайборнів, близькі до стихій."}; // race page leads and URL slugs, filled in by build.py
const RSLUG = {"human": "human", "dwarf": "dwarf", "nightelf": "night-elf", "gnome": "gnome", "skyA": "skyborne-alliance", "orc": "orc", "undead": "undead", "tauren": "tauren", "troll": "troll", "skyH": "skyborne-horde"};

const EN = {
  'Зброя':'Arms','Лють':'Fury','Захист':'Protection','Світло':'Holy','Відплата':'Retribution',
  'Володіння звірами':'Beast Mastery','Стрільба':'Marksmanship','Виживання':'Survival',
  'Ліквідація':'Assassination','Бій':'Combat','Непомітність':'Subtlety',
  'Послух':'Discipline','Темрява':'Shadow','Стихії':'Elemental','Вдосконалення':'Enhancement','Зцілення':'Restoration',
  'Тайна магія':'Arcane','Вогонь':'Fire','Лід':'Frost','Прокляття':'Affliction','Демонологія':'Demonology','Руйнування':'Destruction',
  'Баланс':'Balance','Сила звіра':'Feral',
  'Воля до життя':'Will to Survive','Уважність':'Perception','Безжальність':'Ruthless','Людський дух':'The Human Spirit',
  'Кам’яна форма':'Stoneform','Пошук скарбів':'Find Treasure','Лють землі':'Earth Fury','Мисливець на велику дичину':'Big Game Hunter',
  'Світло Елуни':"Elune’s Light",'Злиття з тінню':'Shadowmeld','Спритність':'Quickness','Дух-вогник':'Wisp Spirit',
  'Майстер втечі':'Escape Artist','Еврика!':'Eureka!','Допитливий розум':'Expansive Mind','Спеціалізація: інженерія':'Engineering Specialization',
  'Ходіння повітрям':'Walk on Air','Читання лей-ліній':'Read Ley Line','Благословення вітру':'Wind Blessed','Прозріння стихій':'Elemental Insight','Погляд у небо':'Skysight',
  'Кривава лють':'Blood Fury','Руйнування прокляттів':'Shatter Curse','Дикість':'Savage','Command':'Command','Загартування':'Hardiness',
  'Воля Відрікшихся':'Will of the Forsaken','Канібалізм':'Cannibalize','Підводне дихання':'Underwater Breathing','Дотик могили':'Touch of the Grave',
  'Тупіт війни':'War Stomp','Культивація':'Cultivation','Біг рівнинами':'Plainsrunning','Витривалість':'Endurance',
  'Берсерк':'Berserking','Швидке відновлення':'Rapid Regeneration','Убивця звірів':'Beast Slaying','Регенерація':'Regeneration'
};
RC.skyA.en = 'High Order Skyborne'; RC.skyH.en = 'Windshaper Skyborne';
const tipBox = h => `<div class="tipbox"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg><p><span class="tl">Порада</span>${h}</p></div>`;
function bi(ru) { return EN[ru] && EN[ru] !== ru ? `${esc(ru)} <span class="en">(${esc(EN[ru])})</span>` : esc(ru); }
function raceEn(r) { return r.en ? ` <span class="en">/ ${esc(r.en)}</span>` : ''; }
function facName(f) { return f === 'alliance' ? 'Альянс' : 'Орда'; }
const PV = /*PV*/'?v=03c9d4a0';   // ?v= of the class and race portraits, filled in by build.art_version (redrawn under the same names)
/* Round face avatar: assets/art/<id>-face.webp, ring colour cc */
/* A class face follows the reader's side (GabellaPor, build.por_js); f: a fixed side (the class faces of a race row) */
function face(id, cc, cls = '', title = '', f = '') { const P = window.GabellaPor, t = `../assets/art/{${id}}-face.webp${PV}`, live = P && P.map[id] && !f;
  return `<span class="av ${cls}" style="--cc:${cc}"${title ? ` title="${esc(title)}"` : ''}><img src="../assets/art/${P ? P.id(id, f) : id}-face.webp${PV}"${live ? ` data-por-src="${t}"` : ''} width="160" height="160" alt="" loading="lazy" decoding="async"></span>`; }
function lvlMeter(c) {
  const p = c.lp || 0, w = Math.min(Math.abs(p) / 12 * 46, 46);
  const label = p < 0 ? `Швидше на ${-p}%` : p > 0 ? `Повільніше на ${p}%` : 'Середній темп';
  const bar = p ? `<i class="${p > 0 ? 'slow' : ''}" style="${p < 0 ? 'right' : 'left'}:50%;width:${w}%"></i>` : '';
  return `<span class="lvl"><span>${label}</span><span class="bar" role="img" aria-label="${label}">${bar}</span><span class="scale" aria-hidden="true"><span>швидше</span><span>повільніше</span></span></span>`;
}
function renderClassRef() {
  const roles = ['tank', 'heal', 'dps'];
  const head = `<div class="cmp-h" aria-hidden="true"><span>Клас</span><span class="rdots">${roles.map(x => `<span title="${ROLE_RU[x]}">${ri(x)}</span>`).join('')}</span><span>Прокачування</span><span>У рейді</span><span></span></div>`;
  const box = $('#classRef');
  box.innerHTML = head + CLASSES.map(c => `<div class="cmp-row" style="--cc:${CCOL[c.id]};--art:url('../assets/art/${window.GabellaPor ? GabellaPor.id(c.id) : c.id}-360.webp${PV}')">
    <span class="cmp-id">${face(c.id, CCOL[c.id])}<span><b><a class="cmp-a" href="${HOME}classes/${c.id}/">${esc(c.n)}</a></b><small>${c.specs.map(s => esc(s[0])).join(' · ')}</small></span></span>
    <span class="rdots" role="img" aria-label="Ролі: ${c.roles.map(x => ROLE_RU[x]).join(', ')}">${roles.map(x => { const on = c.roles.includes(x), q = c.roles.includes(x + '?'); return `<span class="rdot${on ? ' on' : q ? ' q' : ''}" title="${ROLE_RU[q ? x + '?' : x]}">${ri(x)}</span>`; }).join('')}</span>
    ${lvlMeter(c)}
    <span class="cmp-d"><span class="cmp-txt" id="crt-${c.id}">${esc(c.raid)}</span><button type="button" class="cmp-more" aria-expanded="false" aria-controls="crt-${c.id}" aria-label="Показати повністю" title="Показати повністю"></button></span>
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
  const head = `<div class="cmp-h" aria-hidden="true"><span>Раса</span><span>Класи</span><span class="abl">Здібності <span class="abt">активна</span><span class="abt p">пасивна</span></span><span></span></div>`;
  $('#raceRef').innerHTML = ['alliance', 'horde'].map(f => `<div class="rgroup ${f}"><h3>${facName(f)}</h3>${head}` + RACES.filter(r => r.f === f).map(r => `<a class="cmp-row" href="${HOME}races/${RSLUG[r.id]}/" style="--cc:var(--${f});--art:url('../assets/art/${RSLUG[r.id]}-360.webp${PV}')">
    <span class="cmp-id">${face(RSLUG[r.id], `var(--${f})`)}<span><b>${esc(r.n)}${r.paid ? '<span class="paid">платна</span>' : ''}</b>${r.en ? `<small>${esc(r.en)}</small>` : ''}</span></span>
    <span class="ccl" role="img" aria-label="Класи: ${Object.keys(r.can).map(id => CL[id].n).join(', ')}">${CLASSES.map(c => { const v = r.can[c.id]; return face(c.id, CCOL[c.id], v ? (v === 'new' ? 'nw' : '') : 'off', c.n + (v === 'new' ? ', нове' : v ? '' : ', недоступно'), f); }).join('')}</span>
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
    const wh = feed.slice(0, 2).map(x => ({ d: x.date, html: `<a class="nc" href="${esc(x.url)}" target="_blank" rel="noopener"><time datetime="${esc(x.date)}">${x.date.slice(8, 10)}.${x.date.slice(5, 7)}</time><b lang="en">${esc(x.title)}</b><span>${'Wowhead, англійською'}</span></a>` }));
    const all = ours.concat(bz, wh).sort((a, b) => (a.d < b.d ? 1 : a.d > b.d ? -1 : (b.o || 0) - (a.o || 0))).slice(0, 3);
    if (all.some(x => wh.includes(x) || bz.includes(x))) row.innerHTML = all.map(x => x.html).join('');
  });
})();
/* #peoples: the races block of the old home (old links) lives on the races page now */
if (location.hash === '#peoples') location.replace('races/');
