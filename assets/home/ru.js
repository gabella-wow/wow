const HOME = '';   // language home, the classes/ and races/ pages set their own
/* ref:start — shared with the classes/ and races/ pages (build_guides.ref_js); no $ or esc here, every page defines its own */
const CLASSES = [
  { id:'warrior', n:'Воин', s:'Воин', roles:['tank','dps'],
    specs:[['Оружие','Урон в ближнем бою (двуручное оружие)',['dps']],['Неистовство','Урон в ближнем бою (два оружия)',['dps']],['Защита','Танк',['tank']]],
    lvl:'Самая медленная прокачка, примерно на 12% дольше среднего (оценка LFCarry)',
    lp:12,
    raid:'Боевой крик действует на весь рейд',
    forever:'Больше Ярости, лучше угроза по группе целей, талант Мастер оружия. Неистовство и Кровожадность ослаблены.' },
  { id:'paladin', n:'Паладин', roles:['tank','heal','dps'],
    specs:[['Свет','Лекарь',['heal']],['Защита','Танк',['tank']],['Воздаяние','Урон в ближнем бою',['dps']]],
    lvl:'Средний темп прокачки',
    lp:0,
    raid:'Благословение королей теперь базовое. По бета-спискам Защита среди сильнейших танков, Воздаяние просело после патча 15 октября.',
    forever:'Священный удар с 6 уровня, Правосудие не тратит печать. Нежить теперь может быть паладином, значит класс появился у Орды.' },
  { id:'hunter', n:'Охотник', roles:['dps'],
    specs:[['Повелитель зверей','Урон дальнего боя, много урона от питомца',['dps']],['Стрельба','Урон дальнего боя',['dps']],['Выживание','Ближний и дальний бой, ловушки',['dps']]],
    lvl:'Самая быстрая прокачка, примерно на 8% быстрее среднего (оценка LFCarry)',
    lp:-8,
    raid:'Аура меткого выстрела действует на весь рейд',
    forever:'Можно играть без питомца, ловушки работают в бою, появились лисы как семейство питомцев. Выживание может идти в ближний бой.' },
  { id:'rogue', n:'Разбойник', roles:['dps'],
    specs:[['Ликвидация','Урон ядами',['dps']],['Бой','Быстрые атаки оружием',['dps']],['Скрытность','Засады, кровотечения',['dps']]],
    lvl:'Средний темп прокачки',
    lp:0,
    raid:'Чистый урон в ближнем бою без баффов на весь рейд',
    forever:'Теперь можно использовать одноручные топоры. Ликвидация строится на ядах, Скрытность на кровотечениях и невидимости.' },
  { id:'priest', n:'Жрец', roles:['heal','dps'],
    specs:[['Послушание','Лекарь, щиты и поглощение',['heal']],['Свет','Лекарь',['heal']],['Темная магия','Урон дальнего боя',['dps']]],
    lvl:'Примерно на 5% медленнее среднего (оценка LFCarry)',
    lp:5,
    raid:'Божественный дух стал базовым. Урон Тьмы и «Всепожирающая чума» (откат 24 сек) усилены патчем 15 октября.',
    forever:'Защита от страха и «Всепожирающая чума» доступны с 20 уровня любой расе. У каждой расы по два своих заклинания жреца.' },
  { id:'shaman', n:'Шаман', roles:['heal','dps','tank?'],
    specs:[['Стихии','Урон дальнего боя',['dps']],['Совершенствование','Урон в ближнем бою. Возможность танковать пока под вопросом',['dps','tank?']],['Исцеление','Лекарь',['heal']]],
    lvl:'Средний темп прокачки',
    lp:0,
    raid:'Тотемы силы земли, неистовства ветра, языков пламени и грации воздуха усиливают свою группу',
    forever:'Дворфы теперь могут быть шаманами, значит класс появился у Альянса. Выброс лавы усилен, Стихии поднялись в списках урона.' },
  { id:'mage', n:'Маг', roles:['dps'],
    specs:[['Тайная магия','Бурст, много маны',['dps']],['Огонь','Криты и поджоги',['dps']],['Лёд','Урон и контроль',['dps']]],
    lvl:'Самая быстрая прокачка, примерно на 8% быстрее среднего, около 12 часов экономии (оценка LFCarry)',
    lp:-8,
    raid:'Порталы, еда и вода для группы',
    forever:'Огонь получил Путь огня, Тайная магия — Чародейскую вспышку, Лёд — Ледяное копьё. Огненно-ледяная стрела доступна с 40 уровня.' },
  { id:'warlock', n:'Чернокнижник', roles:['dps'],
    specs:[['Колдовство','Урон от проклятий и порчи',['dps']],['Демонология','Урон через демонов',['dps']],['Разрушение','Прямой урон огнём и тьмой',['dps']]],
    lvl:'Средний темп прокачки',
    lp:0,
    raid:'Мастерство тьмы даёт 2–10% урона от тьмы, как в Classic (в ранней бете было 1–5%)',
    forever:'У Колдовства новое направляемое заклинание, демон остаётся при Жертве демона, у Разрушения появились Испепеление и урон по площади.' },
  { id:'druid', n:'Друид', roles:['tank','heal','dps'],
    specs:[['Баланс','Урон дальнего боя',['dps']],['Сила зверя','Танк (медведь) и урон в ближнем бою (кошка)',['tank','dps']],['Исцеление','Лекарь, много лечения по времени',['heal']]],
    lvl:'Примерно на 5% медленнее среднего (оценка LFCarry)',
    lp:5,
    raid:'Вожак стаи и аура лунного совуха действуют на весь рейд и складываются',
    forever:'Каждая специализация получила чёткую роль, формы работают с зельями и чарами на оружии. Можно быть танком, лекарем и бойцом на одном персонаже.' }
];
const ROLE_RU = { tank:'Танк', heal:'Лекарь', dps:'Урон', 'tank?':'Танк (под вопросом)' };
const ri = r => `<svg class="ri" aria-hidden="true"><use href="#i-${r.replace('?','')}"/></svg>`;
const CCOL = { warrior:'#c79c6e', paladin:'#f58cba', hunter:'#abd473', rogue:'#fff569', priest:'#e8e8e8', shaman:'#2f8cf0', mage:'#40c7eb', warlock:'#8788ee', druid:'#ff7d0a' };
const BUFF = { warrior:'Боевой крик', paladin:'Благословение королей', hunter:'Аура меткого выстрела', priest:'Слово силы: Стойкость, Божественный дух', shaman:'Тотемы (сила земли, неистовство ветра, языки пламени, грация воздуха)', mage:'Чародейский интеллект, порталы, еда и вода', druid:'Знак дикой природы, Вожак стаи, аура лунного совуха' };

const RACES = [
  { id:'human', n:'Человек', f:'alliance',
    cls:['warrior','paladin','hunter*','rogue','priest','mage','warlock'],
    rac:[['a','Воля к жизни','Снимает оглушение'],['a','Внимательность','Показывает невидимых врагов на 20 сек'],['p','Беспощадность','+1% шанс крита'],['p','Человеческий дух','+10% к духу']],
    tip:'Дух идёт в лечение Жрецу Света, так что Человек-жрец хорош для лекаря.' },
  { id:'dwarf', n:'Дворф', f:'alliance',
    cls:['warrior','paladin','hunter','rogue','priest','shaman*'],
    rac:[['a','Каменная форма','Иммунитет к кровотечениям, ядам и болезням на 8 сек и снижение физического урона'],['a','Поиск сокровища','Показывает сундуки рядом и даёт шанс на лишние предметы в большинстве сундуков'],['p','Artisan’s Precision','+1% к меткости заклинаний и атак'],['p','Охотник на крупную дичь','+5% урона по зверям']],
    tip:'Каменная форма полезна танку и в PvP.' },
  { id:'nightelf', n:'Ночной эльф', f:'alliance',
    cls:['warrior','hunter','rogue','priest','druid'],
    rac:[['a','Свет Элуны','+10% к шансу крита на 15 сек'],['a','Слиться с тенью','Невидимость на месте'],['p','Расторопность','+2% к уклонению и скорости бега (у Warcraft Tavern уклонение 1%) {beta}'],['p','Дух огонька','+75% к скорости бега в виде духа (Warcraft Tavern пишет 25%) {beta}']],
    tip:'Единственная раса Альянса с друидом, если не брать Скайборн.' },
  { id:'gnome', n:'Гном', f:'alliance',
    cls:['warrior','rogue','mage','warlock','priest*'],
    rac:[['a','Мастер побега','Короткий иммунитет к замедлению и корням'],['a','Эврика!','На 8 сек способности дешевле и на 10% сильнее {beta}'],['p','Пытливый ум','+5% к максимуму маны, ярости или энергии'],['p','Инженерное дело, специализация','Инженерные устройства срабатывают надёжнее']],
    tip:'Пытливый ум особенно выручает классам на энергии.' },
  { id:'skyA', n:'Скайборн (Альянс)', f:'alliance', paid:true, name:'Высший скайборн',
    cls:['warrior','hunter','rogue','mage','druid'],
    rac:[['a','Хождение по воздуху','Планирование вниз 10 сек, нет урона от падения'],['a','Чтение лей-линий','Восстановление здоровья и маны +50% на 15 сек. У лей-линии ещё Attuned на 1 час: +100%, не спадает после смерти'],['p','Благословение ветра','+2% к скорости атаки и заклинаний'],['p','Прозрение стихий','+5% урона по элементалям']],
    tip:'Платная раса: набор Heroic Pack от $29.99. Старт в локации Zephras Isle (1–12 уровни).' },
  { id:'orc', n:'Орк', f:'horde',
    cls:['warrior','hunter','rogue','shaman','warlock','mage*'],
    rac:[['a','Кровавое неистовство','+10% к силе атаки и заклинаний на 15 сек'],['a','Разрушение проклятий','Снимает проклятия и порчи, магический урон по вам −5% на 8 сек'],['p','Властность','+5% к урону питомцев чернокнижника и охотника'],['p','Твердость','Оглушения короче на 20%']],
    tip:'Кровавое неистовство даёт мощное окно урона.' },
  { id:'undead', n:'Нежить', f:'horde',
    cls:['warrior','rogue','mage','priest','warlock','paladin*'],
    rac:[['a','Воля Отрекшихся','Снимает очарование, страх и сон'],['a','Каннибализм','Восстанавливает 35% здоровья и маны со временем'],['p','Подводное дыхание','Дыхание под водой дольше'],['p','Могильное касание','Шанс высосать здоровье при атаке']],
    tip:'Новая комбинация: паладин у Орды, где раньше этого класса не было.' },
  { id:'tauren', n:'Таурен', f:'horde',
    cls:['warrior','hunter','shaman','druid'],
    rac:[['a','Громовая поступь','Оглушает врагов рядом на 2 сек, откат 90 сек'],['a','Проращивание','Выращивает травы, которые можно собрать без травничества, откат 15 мин'],['p','Бег по равнинам','Пока вы движетесь, скорость бега растёт на 2% за заряд, до +60%. На езду верхом не действует'],['p','Закалка','+5% здоровья']],
    tip:'Единственная раса Орды с друидом, если не брать Скайборн.' },
  { id:'troll', n:'Тролль', f:'horde',
    cls:['warrior','hunter','rogue','priest','shaman','mage','warlock*'],
    rac:[['a','Боевое исступление','+10% к скорости атаки и заклинаний на 12 сек, откат 3 мин'],['a','Быстрая регенерация','Восстанавливает здоровье со временем'],['p','Убийство животных','+5% урона по зверям'],['p','Регенерация','Здоровье восстанавливается и в бою']],
    tip:'Больше всего вариантов классов в Орде: семь.' },
  { id:'skyH', n:'Скайборн (Орда)', f:'horde', paid:true, name:'Скайборн-ветрорез',
    cls:['warrior','hunter','rogue','shaman','druid'],
    rac:[['a','Хождение по воздуху','Планирование вниз 10 сек, нет урона от падения'],['a','Взгляд в небо','+15% к скорости бега на 15 сек. У Elemental Convergence ещё Charged на 1 час: +30%, не спадает после смерти'],['p','Благословение ветра','+2% к скорости атаки и заклинаний'],['p','Прозрение стихий','+5% урона по элементалям']],
    tip:'Платная раса: набор Heroic Pack от $29.99. Из скайборнов шаманом может быть только ветрорез (Орда), магом — только Высший орден (Альянс).' }
];
RACES.forEach(r => { r.can = {}; r.cls.forEach(c => { const isNew = c.endsWith('*'); r.can[isNew ? c.slice(0,-1) : c] = isNew ? 'new' : 'ok'; }); });
const CL = Object.fromEntries(CLASSES.map(c => [c.id, c]));
const BETA = '<span class="beta-note">по данным беты</span>';
const BMARK = '{' + 'beta}';   // split so the guide build (which swaps the marker for the span everywhere) leaves it alone
const racx = s => String(s).split(BETA).join(BMARK).split(BMARK).map(esc).join(BETA);
const RC = Object.fromEntries(RACES.map(r => [r.id, r]));
const RLEAD = {"human": "Самая многочисленная раса Альянса. Универсальна и сильна в PvP благодаря Воле к жизни.", "dwarf": "Крепкие горняки и стрелки Стальгорна. Впервые у Альянса есть шаманы, и это дворфы: в Classic такого не было.", "nightelf": "Древний народ лесов. Неуловимы: свой способ скрыться, уклонение и быстрый бег.", "gnome": "Изобретатели Гномрегана. Маленькие, хитрые и с лучшей способностью побега в игре.", "skyA": "Новая раса Forever. Высший орден: эльфы ветра, которые ищут утраченную тайную магию предков.", "orc": "Сердце Орды. Сильнейшие воины и мастера PvP благодаря Кровавому неистовству и Твердости.", "undead": "Отрекшиеся: бывшие люди, вырвавшиеся из-под власти Короля-лича. Не боятся страха и сна.", "tauren": "Мирные великаны равнин. Больше всех здоровья и свой массовый оглушающий удар.", "troll": "Племя Чёрного Копья. Больше всех классов в Орде и сильное Боевое исступление для урона.", "skyH": "Новая раса Forever. Ветрорезы: духовные лидеры скайборнов, близкие к стихиям."}; // race page leads and URL slugs, filled in by build.py
const RSLUG = {"human": "human", "dwarf": "dwarf", "nightelf": "night-elf", "gnome": "gnome", "skyA": "skyborne-alliance", "orc": "orc", "undead": "undead", "tauren": "tauren", "troll": "troll", "skyH": "skyborne-horde"};

const EN = {
  'Оружие':'Arms','Неистовство':'Fury','Защита':'Protection','Свет':'Holy','Воздаяние':'Retribution',
  'Повелитель зверей':'Beast Mastery','Стрельба':'Marksmanship','Выживание':'Survival',
  'Ликвидация':'Assassination','Бой':'Combat','Скрытность':'Subtlety',
  'Послушание':'Discipline','Темная магия':'Shadow','Стихии':'Elemental','Совершенствование':'Enhancement','Исцеление':'Restoration',
  'Тайная магия':'Arcane','Огонь':'Fire','Лёд':'Frost','Колдовство':'Affliction','Демонология':'Demonology','Разрушение':'Destruction',
  'Баланс':'Balance','Сила зверя':'Feral',
  'Воля к жизни':'Will to Survive','Внимательность':'Perception','Беспощадность':'Ruthless','Человеческий дух':'The Human Spirit',
  'Каменная форма':'Stoneform','Поиск сокровища':'Find Treasure','Ярость земли':'Earth Fury','Охотник на крупную дичь':'Big Game Hunter',
  'Свет Элуны':"Elune’s Light",'Слиться с тенью':'Shadowmeld','Расторопность':'Quickness','Дух огонька':'Wisp Spirit',
  'Мастер побега':'Escape Artist','Эврика!':'Eureka!','Пытливый ум':'Expansive Mind','Инженерное дело, специализация':'Engineering Specialization',
  'Хождение по воздуху':'Walk on Air','Чтение лей-линий':'Read Ley Line','Благословение ветра':'Wind Blessed','Прозрение стихий':'Elemental Insight','Взгляд в небо':'Skysight',
  'Кровавое неистовство':'Blood Fury','Разрушение проклятий':'Shatter Curse','Дикость':'Savage','Властность':'Command','Твердость':'Hardiness',
  'Воля Отрекшихся':'Will of the Forsaken','Каннибализм':'Cannibalize','Подводное дыхание':'Underwater Breathing','Могильное касание':'Touch of the Grave',
  'Громовая поступь':'War Stomp','Проращивание':'Cultivation','Бег по равнинам':'Plainsrunning','Закалка':'Endurance',
  'Боевое исступление':'Berserking','Быстрая регенерация':'Rapid Regeneration','Убийство животных':'Beast Slaying','Регенерация':'Regeneration'
};
RC.skyA.en = 'High Order Skyborne'; RC.skyH.en = 'Windshaper Skyborne';
const tipBox = h => `<div class="tipbox"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg><p><span class="tl">Совет</span>${h}</p></div>`;
function bi(ru) { return EN[ru] && EN[ru] !== ru ? `${esc(ru)} <span class="en">(${esc(EN[ru])})</span>` : esc(ru); }
function raceEn(r) { return r.en ? ` <span class="en">/ ${esc(r.en)}</span>` : ''; }
function facName(f) { return f === 'alliance' ? 'Альянс' : 'Орда'; }
const PV = /*PV*/'?v=03c9d4a0';   // ?v= of the class and race portraits, filled in by build.art_version (redrawn under the same names)
/* Round face avatar: assets/art/<id>-face.webp, ring colour cc */
/* A class face follows the reader's side (GabellaPor, build.por_js); f: a fixed side (the class faces of a race row) */
function face(id, cc, cls = '', title = '', f = '') { const P = window.GabellaPor, t = `./assets/art/{${id}}-face.webp${PV}`, live = P && P.map[id] && !f;
  return `<span class="av ${cls}" style="--cc:${cc}"${title ? ` title="${esc(title)}"` : ''}><img src="./assets/art/${P ? P.id(id, f) : id}-face.webp${PV}"${live ? ` data-por-src="${t}"` : ''} width="160" height="160" alt="" loading="lazy" decoding="async"></span>`; }
function lvlMeter(c) {
  const p = c.lp || 0, w = Math.min(Math.abs(p) / 12 * 46, 46);
  const label = p < 0 ? `Быстрее на ${-p}%` : p > 0 ? `Медленнее на ${p}%` : 'Средний темп';
  const bar = p ? `<i class="${p > 0 ? 'slow' : ''}" style="${p < 0 ? 'right' : 'left'}:50%;width:${w}%"></i>` : '';
  return `<span class="lvl"><span>${label}</span><span class="bar" role="img" aria-label="${label}">${bar}</span><span class="scale" aria-hidden="true"><span>быстрее</span><span>медленнее</span></span></span>`;
}
function renderClassRef() {
  const roles = ['tank', 'heal', 'dps'];
  const head = `<div class="cmp-h" aria-hidden="true"><span>Класс</span><span class="rdots">${roles.map(x => `<span title="${ROLE_RU[x]}">${ri(x)}</span>`).join('')}</span><span>Прокачка</span><span>В рейде</span><span></span></div>`;
  const box = $('#classRef');
  box.innerHTML = head + CLASSES.map(c => `<div class="cmp-row" style="--cc:${CCOL[c.id]};--art:url('./assets/art/${window.GabellaPor ? GabellaPor.id(c.id) : c.id}-360.webp${PV}')">
    <span class="cmp-id">${face(c.id, CCOL[c.id])}<span><b><a class="cmp-a" href="${HOME}classes/${c.id}/">${esc(c.n)}</a></b><small>${c.specs.map(s => esc(s[0])).join(' · ')}</small></span></span>
    <span class="rdots" role="img" aria-label="Роли: ${c.roles.map(x => ROLE_RU[x]).join(', ')}">${roles.map(x => { const on = c.roles.includes(x), q = c.roles.includes(x + '?'); return `<span class="rdot${on ? ' on' : q ? ' q' : ''}" title="${ROLE_RU[q ? x + '?' : x]}">${ri(x)}</span>`; }).join('')}</span>
    ${lvlMeter(c)}
    <span class="cmp-d"><span class="cmp-txt" id="crt-${c.id}">${esc(c.raid)}</span><button type="button" class="cmp-more" aria-expanded="false" aria-controls="crt-${c.id}" aria-label="Показать полностью" title="Показать полностью"></button></span>
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
  const head = `<div class="cmp-h" aria-hidden="true"><span>Раса</span><span>Классы</span><span class="abl">Способности <span class="abt">активная</span><span class="abt p">пассивная</span></span><span></span></div>`;
  $('#raceRef').innerHTML = ['alliance', 'horde'].map(f => `<div class="rgroup ${f}"><h3>${facName(f)}</h3>${head}` + RACES.filter(r => r.f === f).map(r => `<a class="cmp-row" href="${HOME}races/${RSLUG[r.id]}/" style="--cc:var(--${f});--art:url('./assets/art/${RSLUG[r.id]}-360.webp${PV}')">
    <span class="cmp-id">${face(RSLUG[r.id], `var(--${f})`)}<span><b>${esc(r.n)}${r.paid ? '<span class="paid">платная</span>' : ''}</b>${r.en ? `<small>${esc(r.en)}</small>` : ''}</span></span>
    <span class="ccl" role="img" aria-label="Классы: ${Object.keys(r.can).map(id => CL[id].n).join(', ')}">${CLASSES.map(c => { const v = r.can[c.id]; return face(c.id, CCOL[c.id], v ? (v === 'new' ? 'nw' : '') : 'off', c.n + (v === 'new' ? ', новое' : v ? '' : ', нельзя'), f); }).join('')}</span>
    <span class="abs">${r.rac.map(x => `<span><b class="${x[0] === 'a' ? '' : 'p'}">${bi(x[1])}</b><span>${racx(x[2])}</span></span>`).join('')}</span>
    <span class="go" aria-hidden="true"><svg class="ico"><use href="#i-arrow"/></svg></span>
  </a>`).join('') + '</div>').join('');
}
/* ref:end */
const $ = s => document.querySelector(s);
function esc(s) { return String(s).replace(/[&<>"]/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m])); }
const ROOT = './';
function raceName(r) { return r.name || r.n; }
/* Class roster: tall portraits, the hovered or focused one expands */
const DESC = {
  warrior: 'Латы, ярость и первый ряд. Держит удар как танк или рубит двуручным оружием.',
  paladin: 'Святой воин в латах: лечит, танкует и бьёт молотом. Теперь есть и у Орды.',
  hunter: 'Лук, ловушки и верный зверь рядом. Один из самых быстрых классов в прокачке.',
  rogue: 'Яды, клинки и тень. Чистый урон из засады и контроль врагов.',
  priest: 'Свет и Тьма в одних руках. Главный лекарь группы или тёмный заклинатель.',
  shaman: 'Тотемы и стихии: лечит, бьёт молнией или оружием. Теперь есть и у Альянса.',
  mage: 'Огонь, лёд и тайная магия. Порталы, еда и вода для группы.',
  warlock: 'Проклятия, демоны и огонь. Урон со временем и свой демон в помощь.',
  druid: 'Медведь, кошка, сова или лекарь: все три роли на одном персонаже.'
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
    <span class="info"><b>${esc(c.n)}</b><span class="roles">${c.roles.filter(r => !r.endsWith('?')).map(r => `<span>${ri(r)}${ROLE_RU[r]}</span>`).join('')}</span><span class="d">${esc(DESC[c.id])}</span><span class="more">Подробнее о классе</span></span>
  </a>`).join('');
}
renderRoster();
/* Race roster: one row of portraits per faction, links to the race pages */
function renderPeoples() {
  [['alliance', '#rosterA'], ['horde', '#rosterH']].forEach(([f, sel]) => {
    $(sel).innerHTML = RACES.filter(r => r.f === f).map((r, i) => `<a class="hc${i === 0 ? ' on' : ''}" href="races/${RSLUG[r.id]}/" style="--cc:var(--${f})">
    <picture><source type="image/avif" srcset="${artSet(RSLUG[r.id], 'avif')}" sizes="${ART_SIZES}"><source type="image/webp" srcset="${artSet(RSLUG[r.id], 'webp')}" sizes="${ART_SIZES}"><img src="${ROOT}assets/art/${RSLUG[r.id]}-600.webp${PV}" width="896" height="1200" alt="" loading="lazy" decoding="async"></picture>
    <span class="vn" aria-hidden="true">${esc(raceName(r))}</span>
    <span class="info"><b>${esc(raceName(r))}</b>${r.paid ? '<span class="tag paid">платная</span>' : ''}<span class="d">${esc(RLEAD[r.id])}</span><span class="more">Подробнее о расе</span></span>
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
    const wh = feed.slice(0, 2).map(x => ({ d: x.date, html: `<a class="nc" href="${esc(x.url)}" target="_blank" rel="noopener"><time datetime="${esc(x.date)}">${x.date.slice(8, 10)}.${x.date.slice(5, 7)}</time><b lang="en">${esc(x.title)}</b><span>${'Wowhead, на английском'}</span></a>` }));
    const all = ours.concat(bz, wh).sort((a, b) => (a.d < b.d ? 1 : a.d > b.d ? -1 : (b.o || 0) - (a.o || 0))).slice(0, 3);
    if (all.some(x => wh.includes(x) || bz.includes(x))) row.innerHTML = all.map(x => x.html).join('');
  });
})();
function hashTab() { if (location.hash === '#peoples') { showTab(TABS[1]); document.getElementById('classes').scrollIntoView(); } }
addEventListener('hashchange', hashTab);
hashTab();
