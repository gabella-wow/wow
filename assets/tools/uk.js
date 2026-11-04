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
const CX = {"warrior": {"armor": "Тканина, шкіра, кольчуга; лати з 40 рівня {beta}", "weapons": "Усе, крім жезлів; щит", "resource": "Лють", "lvl": "Найповільніша прокачка, приблизно на 12% довше за середню (оцінка LFCarry)", "group": ["Бойовий клич діє на весь рейд", "Demoralizing Shout і Sunder Armor на босі", "Sweeping Strikes і Whirlwind для боїв із натовпом"], "pros": ["Найкращий танк і сильна шкода в ближньому бою", "Підходить для PvP (Arms)", "Мало кнопок, зрозуміла гра"], "cons": ["Найповільніша прокачка", "Сильно залежить від спорядження", "Майже немає самолікування й контролю"], "specs": [{"n": "Зброя", "what": "Шкода в ближньому бою (дворучна зброя)"}, {"n": "Лють", "what": "Шкода в ближньому бою (дві зброї)"}, {"n": "Захист", "what": "Танк"}]}, "paladin": {"armor": "Тканина, шкіра, кольчуга; лати з 40 рівня; щит {beta}", "weapons": "Сокири, булави, мечі, древкова з 20 рівня {beta}", "resource": "Мана", "lvl": "Середній темп прокачування", "group": ["Аури на групу: Devotion, Retribution, Concentration", "Аури опору вогню, льоду й темряві на весь рейд", "Благословення на годину, великі благословення на весь клас", "Seal of Justice не дає ворогам тікати"], "pros": ["Усі три ролі на одному персонажі", "Сильні бафи для групи", "Лати й міцний персонаж"], "cons": ["Немає ривка, сповільнення та прискорення", "Мало контролю, крім Hammer of Justice", "Retribution просіла після патча"], "specs": [{"n": "Світло", "what": "Цілитель"}, {"n": "Захист", "what": "Танк"}, {"n": "Відплата", "what": "Шкода в ближньому бою"}]}, "hunter": {"armor": "Тканина, шкіра; кольчуга з 40 рівня {beta}", "weapons": "Луки, арбалети, рушниці, сокири, мечі, древкова", "resource": "Мана; у вихованця фокус", "lvl": "Найшвидша прокачка, приблизно на 8% швидше за середню (оцінка LFCarry)", "group": ["Trueshot Aura підсилює дальній бій групи", "Freezing Trap: надійний контроль", "Scatter Shot перериває закляття", "Aspect of the Pack прискорює всю групу в дорозі"], "pros": ["Найшвидша прокачка", "Чудово грає сам", "Пастки й контроль"], "cons": ["Мертва зона зблизька до 8 метрів", "Треба стежити за вихованцем", "На беті таланти Survival мали помилки"], "specs": [{"n": "Володіння звірами", "what": "Шкода здалеку, багато шкоди від улюбленця"}, {"n": "Стрільба", "what": "Шкода здалеку"}, {"n": "Виживання", "what": "Ближній і дальній бій, пастки"}]}, "rogue": {"armor": "Тканина, шкіра", "weapons": "Кинджали, мечі, булави, кистьова, одноручні сокири, метальна", "resource": "Енергія та прийоми серії", "lvl": "Середній темп прокачування", "group": ["Чиста шкода в ближньому бою без баффів на весь рейд", "Sap, Blind і Kidney Shot: багато контролю", "Kick перериває небезпечні закляття"], "pros": ["Дуже висока шкода й ріст зі спорядженням", "Скритність і багато контролю", "Свобода вибору зброї"], "cons": ["Сильно залежить від спорядження", "Немає самолікування", "Рятують лише Evasion і Vanish"], "specs": [{"n": "Ліквідація", "what": "Шкода отрутами"}, {"n": "Бій", "what": "Швидкі атаки зброєю"}, {"n": "Непомітність", "what": "Засідки, кровотечі"}]}, "priest": {"armor": "Тканина", "weapons": "Кинджали, булави, посохи, жезли", "resource": "Мана", "lvl": "Приблизно на 5% повільніше за середню (оцінка LFCarry)", "group": ["Divine Spirit і Power Word: Fortitude на весь рейд", "Power Infusion підсилює союзника", "Головний цілитель групи"], "pros": ["Завжди потрібен групі", "Лікування або шкода темрявою", "Багато збірок"], "cons": ["Лише тканина, крихкий", "Мало способів швидко рухатися", "Швидкість майже не допомагає закляттям"], "specs": [{"n": "Послух", "what": "Цілитель, щити та поглинання"}, {"n": "Світло", "what": "Цілитель"}, {"n": "Темрява", "what": "Шкода здалеку"}]}, "shaman": {"armor": "Тканина, шкіра; кольчуга з 40 рівня; щит {beta}", "weapons": "Булави, сокири, посохи, кистьова, кинджали", "resource": "Мана", "lvl": "Середній темп прокачування", "group": ["Тотеми сили землі, несамовитості вітру, язиків полум’я та грації повітря підсилюють свою групу", "Tremor Totem знімає страх, сон і чарування", "Тотеми очищення від отрут і хвороб", "Purge знімає бафи з ворогів"], "pros": ["Сильні тотеми для групи", "Мобільна прокачка", "Нові сильні таланти"], "cons": ["Немає жорсткого контролю", "Мана в довгих боях", "Танк поки під питанням"], "specs": [{"n": "Стихії", "what": "Шкода здалеку"}, {"n": "Вдосконалення", "what": "Шкода в ближньому бою. Можливість танкувати поки під питанням"}, {"n": "Зцілення", "what": "Цілитель"}]}, "mage": {"armor": "Тканина", "weapons": "Кинджали, мечі, посохи, жезли", "resource": "Мана", "lvl": "Найшвидша прокачка, приблизно на 8% швидше за середню, близько 12 годин економії (оцінка LFCarry)", "group": ["Портали з 40 рівня, телепорт з 20", "Їжа й вода для групи", "Polymorph: надійний контроль", "Remove Lesser Curse"], "pros": ["Найшвидша прокачка", "Портали та їжа для всіх", "Три сильні й різні гілки"], "cons": ["Лише тканина, крихкий", "Мана швидко закінчується", "Шкоду по площі послаблено"], "specs": [{"n": "Тайна магія", "what": "Бурст, багато мани"}, {"n": "Вогонь", "what": "Криті та підпали"}, {"n": "Лід", "what": "Шкода і контроль"}]}, "warlock": {"armor": "Тканина", "weapons": "Кинджали, мечі, посохи, жезли", "resource": "Мана; Life Tap міняє здоров’я на ману", "lvl": "Середній темп прокачування", "group": ["Healthstone і Soulstone", "Ritual of Summoning: збирає групу", "Curse of Tongues сповільнює закляття на 60%", "Curse of the Elements: більше магічної шкоди по цілі"], "pros": ["Самостійний: демон і Life Tap", "Багато користі групі", "Сильна шкода з часом"], "cons": ["Крихкий і нерухливий", "Шкода розганяється не одразу", "Немає ривка й прискорення"], "specs": [{"n": "Прокляття", "what": "Шкода від прокляттів і псування"}, {"n": "Демонологія", "what": "Шкода через демонів"}, {"n": "Руйнування", "what": "Пряма шкода вогнем і темрявою"}]}, "druid": {"armor": "Тканина, шкіра", "weapons": "Кинджали, булави, посохи, кистьова, древкова з 20 рівня {beta}", "resource": "Мана; лють у формі ведмедя, енергія у формі кішки", "lvl": "Приблизно на 5% повільніше за середню (оцінка LFCarry)", "group": ["Ватажок зграї та аура місячного совиця діють на весь рейд і складаються", "Rebirth: воскресіння в бою", "Innervate повертає ману цілителю", "Знімає прокляття й отрути"], "pros": ["Усі три ролі на одному персонажі", "Чудова мобільність", "Воскресіння в бою"], "cons": ["Немає блоку й парирування у ведмедя", "Складніше стежити за ефектами лікування", "Підсумкові цифри в рейдах ще невідомі"], "specs": [{"n": "Баланс", "what": "Шкода здалеку"}, {"n": "Сила звіра", "what": "Танк (ведмідь) і шкода в ближньому бою (кішка)"}, {"n": "Зцілення", "what": "Цілитель, багато лікування з часом"}]}};
const HC = {"tx":{"title":"Мій персонаж","lead":"Без входу й пароля: виберіть клас, спек і расу, і сайт підлаштується під вас.","local":"Зберігається лише в цьому браузері.","none":"Персонажа ще не створено","create":"Створити персонажа","edit":"Змінити","reset":"Видалити персонажа","resetQ":"Видалити персонажа з цього браузера?","steps":["Сторона","Клас і спек","Раса","Вигляд","Деталі"],"side":"За кого граєте?","cls":"Клас","spec":"Спек","race":"Раса","bestFor":"Найкраща раса для спеку «%s»","best":"найкраща","paid":"платна","sex":"Стать","m":"Чоловіча","f":"Жіноча","bg":"Тло портрета","lvl":"Рівень","reg":"Регіон","lvlReg":"Рівень і регіон","regs":{"us":"Америка й Океанія","eu":"Європа","kr":"Корея","tw":"Тайвань"},"p1":"Професія 1","p2":"Професія 2","secP":"Допоміжні професії","noP":"Немає","role":"Роль","back":"Назад","next":"Далі","done":"Готово","cancel":"Скасувати","later":"Можна заповнити пізніше.","levelN":"%n рівень","build":"Моя збірка талантів","buildD":"Таланти спеку «%s» за рівнями.","pairs":"Пари професій","pairsD":"Які професії взяти класу.","bestR":"Найкращі раси","bestRD":"Раса під клас за обидві фракції.","lvlG":"Прокачування класу","lvlGD":"Маршрут і таланти 1–60.","day1":"День 1 під персонажа","day1D":"Чек-лист старту з вашим класом і расою.","play":"У грі","playD":"Зони й підземелля під рівень, таймери, радіо.","dung":"Підземелля під рівень","dungNo":"Вкажіть рівень, і доберемо підземелля.","dungFirst":"Перші підземелля з 13 рівня.","resetH":"Скидання тижня","resetIn":"через %s","resetNote":"Час скидання Forever Blizzard ще не оголосила. Показано, як в інших версіях WoW цього регіону: звіримо на старті.","resetUnk":"Для цього регіону час скидання уточнимо на старті.","resetNoReg":"Вкажіть регіон, і покажемо скидання тижня.","resetWhy":"Рейди відкриваються 09.12, у них тижневе збереження.","lfg":"Текст для пошуку групи","lfgD":"Вставте в чат LookingForGroup. Назви як у грі.","lfgP":{"tank":"%c-танк шукає групу","heal":"%c-цілитель шукає групу","dps":"%c шукає групу"},"lfgT":"%p: %d, %l рівень.","lfgT0":"%p.","allD":"Усі підземелля","copy":"Скопіювати","copied":"Скопійовано","sync":"Синхронізувати між пристроями","syncD":"Вхід потрібен лише для цього: персонаж буде на телефоні й на ПК, а лист до старту прийде на пошту, якщо підпишетеся.","yourCls":"Твій %s","bTalents":"Таланти","bSpec":"Білд: %s","bLevel":"Прокачка","bGroup":"Група","bNews":"Новини","copiedT":"Скопійовано: %s","profsL":"Професії","day1n":"День 1: %n з %t","collect":"Зібрати персонажа","collectD":"Клас, спек і раса: таланти, прокачка, група й новини вашого класу.","change":"Змінити","allSet":"Усі налаштування","close":"Закрити","mine":"Стосується вашого класу","share":"Поділитися","linkCopied":"Посилання скопійовано","make":"Зробити моїм персонажем","made":"Це ваш персонаж","plaqueH":"Мій персонаж","plaqueD":"Клас, спек і раса за хвилину, а далі ваша збірка, професії й підземелля.","day1Mine":"Під вашого персонажа","ckClass":"Ваш спек «%s»: збірка талантів за рівнями.","ckRaceOk":"%r — найкраща раса під ваш спек.","ckRaceAlt":"Найкраща раса під ваш спек: %r.","ckProfs":"Пари професій для класу «%s».","ckStart":"Прокачування за клас «%s»: маршрут і перші таланти.","ckPing":"Ваш регіон: %s.","or":"або"},"best":{"warrior":{"alliance":{"*":[["human","nightelf"],"Людина: +1% криту будь-якою зброєю. Нічний ельф: +10% криту на 15 сек. Джерела діляться майже порівну."],"protection":[["dwarf"],"Stoneform знижує фізичну шкоду на 10% і знімає кровотечі."]},"horde":{"*":[["orc"],"Blood Fury: +10% сили атаки на 15 сек. До змін рас 26.10 його ставили першим усі джерела."],"protection":[["tauren"],"Endurance дає +5% здоров’я, War Stomp оглушує ворогів поруч."]}},"paladin":{"alliance":{"*":[["human"],"Ruthless підсилює і удари, і заклинання, Will to Survive знімає оглушення."],"protection":[["dwarf"],"Stoneform і Artisan’s Precision: +1% до влучності."]},"horde":{"*":[["undead"],"За Орду паладином може бути лише Нежить. Cannibalize повертає ману, Will of the Forsaken знімає страх."]}},"hunter":{"alliance":{"*":[["human","nightelf"],"Людина: +1% криту, і улюбленець успадковує крит. Нічний ельф: Elune’s Light і Shadowmeld."]},"horde":{"*":[["orc","troll"],"Орк: Blood Fury і Command (+5% шкоди улюбленця). Троль: +5% шкоди по звірах."]}},"rogue":{"alliance":{"*":[["nightelf"],"Shadowmeld тепер знижує загрозу й у бою, плюс Elune’s Grace і Quickness."]},"horde":{"*":[["orc"],"Blood Fury: +10% сили атаки на 15 сек."]}},"priest":{"alliance":{"*":[["gnome"],"Вибір усіх джерел: Eureka! підсилює й Power Word: Shield, Inquisitive Mind дає +5% мани."]},"horde":{"*":[["undead","troll"],"Джерела діляться. Нежить сильніша в PvP: Will of the Forsaken знімає страх, сон і зачарування."]}},"shaman":{"alliance":{"*":[["dwarf"],"За Альянс шаманом може бути лише Дворф: Stoneform і Artisan’s Precision (+1% до влучності)."]},"horde":{"*":[["orc"],"Blood Fury дає і силу атаки, і силу заклинань: підходить і Стихіям, і Вдосконаленню."],"restoration":[["troll"],"Цілителю джерело радить Троля: Berserking, +10% до швидкості заклинань на 12 сек."]}},"mage":{"alliance":{"*":[["gnome"],"Eureka! на 8 сек, Inquisitive Mind: +5% мани, Escape Artist знімає корені."]},"horde":{"*":[["orc"],"Маг-орк — нове поєднання Forever: Blood Fury тепер дає силу заклинань."]}},"warlock":{"alliance":{"*":[["gnome","human"],"Гном: Eureka! та Inquisitive Mind. Людина: періодична шкода критує, Ruthless дає +1% криту."]},"horde":{"*":[["orc","undead"],"Орк: Blood Fury дає силу заклинань. Нежить частіше беруть у PvP."]}},"druid":{"alliance":{"*":[["nightelf"],"Elune’s Grace: +10% криту на 15 сек, і Quickness."]},"horde":{"*":[["tauren"],"Endurance: +5% здоров’я, War Stomp працює й у формах."]}}},"sid":{"warrior":["arms","fury","protection"],"paladin":["holy","protection","retribution"],"hunter":["beast-mastery","marksmanship","survival"],"rogue":["assassination","combat","subtlety"],"priest":["discipline","holy","shadow"],"shaman":["elemental","enhancement","restoration"],"mage":["arcane","fire","frost"],"warlock":["affliction","demonology","destruction"],"druid":["balance","feral","restoration"]},"sn":{"warrior":["Зброя","Лють","Захист"],"paladin":["Світло","Захист","Відплата"],"hunter":["Володіння звірами","Стрільба","Виживання"],"rogue":["Ліквідація","Бій","Непомітність"],"priest":["Послух","Світло","Темрява"],"shaman":["Стихії","Вдосконалення","Зцілення"],"mage":["Тайна магія","Вогонь","Лід"],"warlock":["Прокляття","Демонологія","Руйнування"],"druid":["Баланс","Сила звіра","Зцілення"]},"fn":{"alliance":"Альянс","horde":"Орда"},"reset":{"us":[2,15],"eu":[3,4],"kr":null,"tw":null},"rn":{"human":"Людина","dwarf":"Дворф","nightelf":"Нічний ельф","gnome":"Гном","skyA":"Високий скайборн","orc":"Орк","undead":"Нежить","tauren":"Таурен","troll":"Троль","skyH":"Скайборн-вітрорізь"},"rf":{"human":"alliance","dwarf":"alliance","nightelf":"alliance","gnome":"alliance","skyA":"alliance","orc":"horde","undead":"horde","tauren":"horde","troll":"horde","skyH":"horde"},"cn":{"warrior":"Воїн","paladin":"Паладин","hunter":"Мисливець","rogue":"Розбійник","priest":"Жрець","shaman":"Шаман","mage":"Маг","warlock":"Чорнокнижник","druid":"Друїд"},"cen":{"warrior":"Warrior","paladin":"Paladin","hunter":"Hunter","rogue":"Rogue","priest":"Priest","shaman":"Shaman","mage":"Mage","warlock":"Warlock","druid":"Druid"}};
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

const CPROF = {"warrior": [["Прокачування: Ковальство + Гірництво", ""], ["60 рівень: Інженерія + Гірництво", "Коваль одягає себе в лати й зброю, багато рецептів персональні. Інженеру — гранати й пристрої, яких воїну бракує."]], "paladin": [["Прокачування: Ковальство + Гірництво", ""], ["60 рівень: Захист, Відплата: Інженерія + Гірництво. Світло: Алхімія + Травництво", "Світло витрачає багато мани: зілля свої, а Mana Well у таборі замінює Благословення мудрості."]], "hunter": [["Прокачування: Шкіряництво + Знімання шкур", ""], ["60 рівень: Інженерія + Гірництво", "Шкіряник шиє собі шкіру й кольчугу та Armor Kit. Інженер робить приціли й рушниці."]], "rogue": [["Прокачування: Шкіряництво + Знімання шкур", ""], ["60 рівень: Інженерія + Гірництво", "Шкіра своя, Camp Tent дає відпочинок. Інженерія — головна професія для PvP."]], "priest": [["Прокачування: Кравецтво + Зачарування", ""], ["60 рівень: Кравецтво + Інженерія або Зачарування", "Кравець робить пояси із силою заклинань від 10 рівня, зачарувальник — жезли із силою заклинань від 5. Пошите розщеплюють на матеріали."]], "shaman": [["Прокачування: Шкіряництво + Знімання шкур", ""], ["60 рівень: Алхімія + Травництво", "Шкіряник робить речі із силою заклинань для Стихій і Зцілення та спорядження для Вдосконалення. У рейді й групі потрібні зілля."]], "mage": [["Прокачування: Кравецтво + Зачарування", ""], ["60 рівень: Кравецтво + Зачарування; для PvP і великих пулів Інженерія + Гірництво", "Кравець дає раннє спорядження із силою заклинань, пошите розщеплюють. Гранати інженера втримують на місці великі групи ворогів."]], "warlock": [["Прокачування: Кравецтво + Зачарування", ""], ["60 рівень: Кравецтво + Алхімія", "Faction Banner кравця дає дух для Life Tap. Алхімія — зілля й золото."]], "druid": [["Прокачування: Шкіряництво + Знімання шкур або Травництво", ""], ["60 рівень: Алхімія + Травництво", "Трави збирають у Travel Form, зілля п’ють у будь-якому вигляді. Mana Well і Incense Candle — для Балансу й Зцілення."]]};   /* recommended profession pairs per class, already in the page language (build.class_profs) */
const $ = s => document.querySelector(s);
const ROOT = '../../', HOME = '../';
function esc(s) { return String(s).replace(/[&<>"]/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m])); }
function raceName(r) { return r.name || r.n; }
function syncSeg(id, v) { document.querySelectorAll(`#${id} button`).forEach(b => b.setAttribute('aria-pressed', b.dataset.v === String(v))); }
const FAC = { alliance: 'Альянс', horde: 'Орда' };
const BSLUG = { skyA: 'skyborne-a', skyH: 'skyborne-h' };   // race id -> url part of the share page (tools/make_build_cards.py SLUG)
const RSLUG = { human: 'human', dwarf: 'dwarf', nightelf: 'night-elf', gnome: 'gnome', skyA: 'skyborne-alliance', orc: 'orc', undead: 'undead', tauren: 'tauren', troll: 'troll', skyH: 'skyborne-horde' };
const PAINTED = ["druid-nightelf", "druid-tauren", "hunter-nightelf", "hunter-orc", "mage-gnome", "mage-orc", "paladin-human", "paladin-undead", "priest-gnome", "priest-undead", "rogue-nightelf", "rogue-orc", "shaman-dwarf", "shaman-orc", "warlock-gnome", "warlock-orc", "warrior-human", "warrior-orc"];   // class x race paintings that exist (build_tools.painted): the player's own race is drawn, never the best race of the side
const unitArt = (p, ext) => `${ROOT}assets/art/${PAINTED.includes(p.cls + '-' + p.race) ? p.cls + '-' + p.race : RSLUG[p.race]}-360.${ext}${PV}`;
const classUrl = id => `${HOME}classes/${id}/`, raceUrl = id => `${HOME}races/${RSLUG[id]}/`;
const PV = /*PV*/'?v=03c9d4a0';   // ?v= of the class and race portraits (build.art_version)
const porId = (id, f) => (window.GabellaPor ? GabellaPor.id(id, f) : id);   // a class: the portrait of side f, else of the reader's side (build.por_js)
const art = (id, ext = 'webp', f) => `${ROOT}assets/art/${porId(id, f)}-360.${ext}${PV}`;
async function copyTo(text, msgEl, ok) {
  try { await navigator.clipboard.writeText(text); msgEl.textContent = ok; } catch (e) { msgEl.textContent = 'Не вдалося скопіювати, виділіть і натисніть Ctrl+C'; }
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
    out.push((groups > 1 ? `Група ${g + 1}: ` : '') + part.map(p => `${p.name ? p.name + ' — ' : ''}${raceName(RC[p.race])} ${CL[p.cls].n} (${ROLE_RU[p.role]})`).join(', '));
  }
  return out.length ? out.join('\n') + `\n${FAC[R.f]}, ${R.size}` : '';
}

/* LFG line: the dungeon or raid, the missing roles, the play style and a short link (#t=); kept under the 255-byte chat limit */
const LFG = {"d": [["Ragefire Chasm", 13, 18, "horde"], ["Hall of Thanes", 13, 18, 0], ["Ruins of Lordaeron", 15, 20, 0], ["The Deadmines", 15, 22, 0], ["Wailing Caverns", 17, 24, 0], ["Shadowfang Keep", 20, 26, 0], ["Blackfathom Deeps", 22, 28, 0], ["The Stockade", 25, 29, "alliance"], ["Excavation Site: Wetlands", 26, 31, 0], ["City of Dalaran", 28, 33, 0], ["Gnomeregan", 29, 38, 0], ["Razorfen Kraul", 29, 38, 0], ["Scarlet Monastery: Graveyard", 30, 38, 0], ["Scarlet Monastery: Library", 33, 41, 0], ["The Drowned City", 35, 40, 0], ["Scarlet Monastery: Armory", 36, 44, 0], ["Uldaman", 36, 45, 0], ["Razorfen Downs", 37, 46, 0], ["Scarlet Monastery: Cathedral", 38, 46, 0], ["Zul'Farrak", 40, 47, 0], ["Krol'dok Stronghold", 40, 45, 0], ["Maraudon", 45, 51, 0], ["Alcaz Island Prison", 48, 53, 0], ["Temple of Atal'Hakkar", 50, 55, 0], ["Blackrock Depths", 52, 60, 0], ["Blackmaw Hold", 55, 60, 0], ["Lower Blackrock Spire", 57, 60, 0], ["Dire Maul: East", 58, 60, 0], ["Shaper's Terrace", 58, 60, 0], ["Stratholme: Living", 58, 60, 0], ["Stratholme: Undead", 58, 60, 0], ["Scholomance", 58, 60, 0], ["Upper Blackrock Spire", 60, 60, 0], ["Dire Maul: West", 60, 60, 0], ["Dire Maul: North", 60, 60, 0]], "r": {"10": "Barrow Deeps", "20": "Hyjal Summit", "40": "Onyxia’s Lair"}};   // dungeons [name, min, max, entrance faction] and raids {size: name} in the client's language (build_tools)
const CHAT_MAX = 255, CANON = 'https://gabella.site/wow/uk/tools/'.replace(/^https?:\/\//, '');
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
  const head = (L.d ? '%d — потрібні: %n.' : 'Потрібні в групу: %n.').replace('%d', L.d).replace('%n', roles);
  const parts = [head, L.s ? 'Стиль: %s.'.replace('%s', L.s) : '', CANON + shortHash()].filter(Boolean);
  const bytes = t => new TextEncoder().encode(t).length;
  let text = parts.join(' ');
  if (bytes(text) > CHAT_MAX) text = parts.slice(0, -1).join(' ');   // a long raid code would not fit: the link goes first
  return text;
}
function renderLfg() {
  const places = lfgPlaces(), sel = $('#lfgD');
  if (!places.some(p => p[0] === L.d)) L.d = R.size === 5 ? '' : (places[0] || [''])[0];
  $('#lfgDL').textContent = R.size === 5 ? 'Підземелля' : 'Рейд';
  sel.innerHTML = (R.size === 5 ? '<option value="">Будь-яке підземелля</option>' : '') + places.map(([v, t]) => `<option value="${esc(v)}"${v === L.d ? ' selected' : ''}>${esc(t)}</option>`).join('');
  syncSeg('lfgS', L.s);
  const text = lfgText();
  $('#rLfg').value = text;
  $('#rCopyLfg').disabled = !text;
  $('#rLfgMsg').textContent = text ? lfgLen(text) : R.s.some(Boolean) ? 'Усі місця зайняті.' : 'Додайте до складу хоча б одного гравця.';
}
function lfgLen(t) { return 'Знаків: %n з %m (ліміт рядка чату).'.replace('%n', t.length).replace('%m', CHAT_MAX); }

function unitHTML(p, i) {
  const cls = R.moving === i ? ' src' : '';
  if (!p) return `<button type="button" class="unit empty${cls}" data-i="${i}"><span class="up" aria-hidden="true">+</span><span class="ub"><b>Вільне місце</b><span>Натисніть, щоб додати гравця</span></span></button>`;
  const c = CL[p.cls], r = RC[p.race];
  return `<button type="button" class="unit${cls}" data-i="${i}" draggable="true" style="--cc:${CCOL[p.cls]};--pc:${power(p)}" aria-label="${esc((p.name || `Гравець ${i + 1}`) + ', ' + raceName(r) + ' ' + c.n + ', ' + ROLE_RU[p.role])}">
    <span class="up"><picture><source type="image/avif" srcset="${unitArt(p, 'avif')}"><img src="${unitArt(p, 'webp')}" width="360" height="482" alt="" loading="lazy" decoding="async"></picture></span>
    <span class="ub"><span class="un"><span class="ur" title="${ROLE_RU[p.role]}">${ri(p.role)}</span><b>${esc(p.name || c.n)}</b><small>${esc(raceName(r))} · ${esc(c.n)}</small></span><span class="hp"><i></i></span><span class="mp"></span></span></button>`;
}
function cellHTML(p, i) {
  const cls = R.moving === i ? ' src' : '';
  if (!p) return `<button type="button" class="rc empty${cls}" data-i="${i}" aria-label="Вільне місце ${i + 1}"><span aria-hidden="true">+</span>Додати</button>`;
  const c = CL[p.cls], r = RC[p.race];
  return `<button type="button" class="rc${cls}" data-i="${i}" draggable="true" style="--cc:${CCOL[p.cls]};--pc:${power(p)}" aria-label="${esc((p.name || `Гравець ${i + 1}`) + ', ' + raceName(r) + ' ' + c.n + ', ' + ROLE_RU[p.role])}" title="${esc(raceName(r) + ' · ' + c.n + ' · ' + ROLE_RU[p.role])}"><b>${esc(p.name || c.n)}</b><small>${esc(p.name ? c.n : raceName(r))}</small>${ri(p.role)}</button>`;
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
      const st = n && (!c.tank || !c.heal) ? `<span class="warn">${!c.tank ? 'немає танка' : 'немає цілителя'}</span>` : `<span>${n}/5</span>`;
      h += `<div class="rg"><div class="rg-h"><b>Група ${g + 1}</b>${st}</div>${part.map((p, k) => cellHTML(p, g * PARTY + k)).join('')}</div>`;
    }
    $('#rview').innerHTML = `<div class="rgrid" style="--gc:${Math.min(groups, 8)}">${h}</div>`;
  }
  const hint = $('#rhint');
  hint.classList.toggle('on', R.moving >= 0);
  hint.innerHTML = R.moving >= 0 ? `Виберіть місце, куди переставити гравця ${R.moving + 1}. <button type="button" id="mvCancel">Скасувати</button>` : '';

  const list = R.s.filter(Boolean), cnt = countRoles(list), rec = REC[R.size];
  $('#rRoles').innerHTML = RR.map((x, k) => `<span class="${list.length && cnt[x] < rec[k] ? 'low' : ''}">${ri(x)}${ROLE_RU[x]} <b>${cnt[x]}</b> / ${rec[k]}</span>`).join('');
  $('#rTip').textContent = R.size === 5 ? 'Для підземелля потрібні танк, цілитель і три бійці шкоди.' : `Орієнтир для рейду: танків ${rec[0]}, цілителів ${rec[1]}, решта шкода. Точна кількість залежить від босів.`;
  const have = new Set(list.map(p => p.cls));
  $('#rBuffs').innerHTML = CLASSES.filter(c => BUFF[c.id]).map(c => `<li class="${have.has(c.id) ? '' : 'off'}" style="--cc:${CCOL[c.id]}"><span class="cdot"></span><span><b>${esc(c.n)}:</b> ${esc(BUFF[c.id])}</span></li>`).join('');
  const n = list.length;
  $('#rRaids').innerHTML = n ? RAIDS.map(([size, name]) => `<li class="${n >= size ? 'good' : ''}">${n >= size ? `Рейд на ${size} (${name}): людей вистачає.` : `Рейд на ${size} (${name}): бракує ${size - n}.`}</li>`).join('') : '<li>Поки нікого немає. Натисніть «Моїм персонажем», «Заповнити порожні» або на вільну рамку.</li>';

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
function myHero() {   // the hero of this browser (assets/hero/hero.js?v=f70745f9fb, localStorage gabella-wf-me)
  let h = null; try { h = JSON.parse(localStorage.getItem('gabella-wf-me')); } catch (e) {}
  return h && RC[h.race] && CL[h.cls] && RC[h.race].can[h.cls] ? h : null;
}
$('#rMine').onclick = () => {
  const h = myHero(), msg = $('#rMy');
  if (!h) {
    msg.innerHTML = 'Персонажа ще немає. <a href="../character/" id="rMake">Зібрати персонажа</a>';
    $('#rMake').onclick = e => { if (window.GabellaHero) { e.preventDefault(); GabellaHero.open(); } };
    return;
  }
  const f = RC[h.race].f, role = RR.includes(h.role) ? h.role : roleOpts(CL[h.cls])[0];
  if (f !== R.f) {
    if (R.s.some(Boolean)) { msg.textContent = 'Ваш персонаж грає за іншу фракцію: перемкніть фракцію над рамками.'; return; }
    R.f = f;
  }
  if (R.s.some(p => p && p.race === h.race && p.cls === h.cls && p.role === role && !p.name)) { msg.textContent = 'Ваш персонаж уже в складі.'; return; }
  let i = R.s.findIndex(p => !p); if (i < 0) i = 0;
  R.s[i] = { race: h.race, cls: h.cls, role, name: '' };
  msg.textContent = ''; R.moving = -1; renderRaid();
};
$('#rClear').onclick = () => { R.s = Array(R.size).fill(null); R.moving = -1; renderRaid(); };
$('#rCopyLink').onclick = () => copyTo(teamLink(), $('#rMsg'), 'Посилання скопійовано');
$('#rCopyText').onclick = () => copyTo(teamText(), $('#rMsg'), 'Склад скопійовано');
$('#lfgD').onchange = e => { L.d = e.target.value; renderLfg(); };
$('#lfgS').addEventListener('click', e => { const b = e.target.closest('button'); if (b) { L.s = L.s === b.dataset.v ? '' : b.dataset.v; renderLfg(); } });
$('#rCopyLfg').onclick = () => { const t = lfgText(); copyTo(t, $('#rLfgMsg'), 'Текст скопійовано. ' + lfgLen(t)); };

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
  $('#edT').textContent = `Гравець ${edI + 1}` + (R.size > 5 ? ` · Група ${Math.floor(edI / PARTY) + 1}` : '');
  $('#edRace').innerHTML = RACES.filter(r => r.f === R.f).map(r => `<option value="${r.id}"${r.id === p.race ? ' selected' : ''}>${esc(raceName(r))}${r.paid ? ' (платна)' : ''}</option>`).join('');
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
  else box.innerHTML = ['alliance', 'horde'].map(f => `<div class="rside ${f}"><h3>${FAC[f]}</h3>${RACES.filter(r => r.f === f).map(r => { const k = sel.indexOf(r.id); return `<button type="button" class="rp" data-id="${r.id}" aria-pressed="${k >= 0}">${esc(raceName(r))}${r.paid ? '<span class="tag paid">платна</span>' : ''}<span class="no">${k + 1}</span></button>`; }).join('')}</div>`).join('');
  $('#cNote').textContent = `Вибрано ${sel.length} з 3`;
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
const ul = (items, cls) => items.length ? `<ul${cls ? ` class="${cls}"` : ''}>${items.map(x => `<li>${x}</li>`).join('')}</ul>` : '<span class="none">Немає</span>';
const row = (lab, vals, extra) => `<div class="crow${extra ? ' ' + extra : ''}"><div class="lab${extra === 'tiprow' ? ' tl' : ''}">${lab}</div>${vals.map(v => `<div class="val">${v}</div>`).join('')}</div>`;
function renderCmp() {
  const out = [];
  if (C.mode === 'class') {
    const ids = C.cls;
    out.push(`<div class="crow chead"><div class="lab"></div>${ids.map(id => `<div class="val" style="--cc:${CCOL[id]}"><picture><source type="image/avif" srcset="${art(id, 'avif')}"><img src="${art(id)}" width="360" height="482" alt="" loading="lazy" decoding="async"></picture><b>${esc(CL[id].n)}</b><a href="${classUrl(id)}">Сторінка класу<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>`).join('')}</div>`);
    out.push(row('Ролі', ids.map(id => CL[id].roles.map(r => `<span class="role">${ri(r)}${ROLE_RU[r]}</span>`).join(''))));
    out.push(row('Броня', ids.map(id => racx(CX[id].armor))));
    out.push(row('Зброя', ids.map(id => racx(CX[id].weapons))));
    out.push(row('Ресурс', ids.map(id => esc(CX[id].resource))));
    out.push(row('Прокачування', ids.map(id => esc(CX[id].lvl))));
    out.push(row('Спеціалізації', ids.map(id => ul(CX[id].specs.map(s => `<b>${esc(s.n)}</b>${SPEC_SEP}<span class="sub">${esc(s.what)}</span>`)))));
    out.push(row('Баф для рейду', ids.map(id => BUFF[id] ? esc(BUFF[id]) : '<span class="none">Немає</span>')));
    out.push(row('У групі', ids.map(id => ul(CX[id].group.map(esc)))));
    out.push(row('Професії', ids.map(id => ul(CPROF[id].map(p => `<b>${esc(p[0])}</b>${p[1] ? `<br><span class="sub">${esc(p[1])}</span>` : ''}`)) + `<a class="cgo" href="${HOME}guides/professions/#pairs=${id}">Об’єкти табору й прокачування<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a>`)));
    out.push(row('Сильні сторони', ids.map(id => ul(CX[id].pros.map(esc), 'plus'))));
    out.push(row('Слабкі сторони', ids.map(id => ul(CX[id].cons.map(esc), 'minus'))));
    ['alliance', 'horde'].forEach(f => out.push(row(`Раси: ${FAC[f]}`, ids.map(id => { const rs = RACES.filter(r => r.f === f && r.can[id]); return rs.length ? rs.map(r => `<a href="${raceUrl(r.id)}">${esc(raceName(r))}</a>`).join(', ') : '<span class="none">Немає</span>'; }))));
  } else {
    const ids = C.race;
    out.push(`<div class="crow chead"><div class="lab"></div>${ids.map(id => { const r = RC[id]; return `<div class="val race ${r.f}"><span class="fx">${FAC[r.f]}${r.paid ? ' · платна' : ''}</span><b>${esc(raceName(r))}</b><a href="${raceUrl(id)}">Сторінка раси<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>`; }).join('')}</div>`);
    out.push(row('Класи', ids.map(id => ul(Object.keys(RC[id].can).map(c => `<span style="color:${CCOL[c]}">●</span> ${esc(CL[c].n)}${RC[id].can[c] === 'new' ? ' <span class="tag new">нове</span>' : ''}`)))));
    out.push(row('Активні здібності', ids.map(id => ul(RC[id].rac.filter(x => x[0] === 'a').map(x => `<b>${esc(x[1])}</b><br><span class="sub">${racx(x[2])}</span>`)))));
    out.push(row('Пасивні здібності', ids.map(id => ul(RC[id].rac.filter(x => x[0] === 'p').map(x => `<b>${esc(x[1])}</b><br><span class="sub">${racx(x[2])}</span>`)))));
    out.push(row('Порада', ids.map(id => esc(RC[id].tip)), 'tiprow'));
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
function facName(f) { return f === 'alliance' ? 'Альянс' : 'Орда'; }
function bi(ru) { return EN[ru] && EN[ru] !== ru ? `${esc(ru)} <span class="en">(${esc(EN[ru])})</span>` : esc(ru); }
function raceEn(r) { return r.en ? ` <span class="en">/ ${esc(r.en)}</span>` : ''; }
const tipBox = h => `<div class="tipbox"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg><p><span class="tl">Порада</span>${h}</p></div>`;
function face(id, cc, cls = '', title = '', f) { return `<span class="av ${cls}" style="--cc:${cc}"${title ? ` title="${esc(title)}"` : ''}><img src="${ROOT}assets/art/${porId(id, f)}-face.webp${PV}" width="160" height="160" alt="" loading="lazy" decoding="async"></span>`; }
function lvlMeter(c) {
  const p = c.lp || 0, w = Math.min(Math.abs(p) / 12 * 46, 46);
  const label = p < 0 ? `Швидше на ${-p}%` : p > 0 ? `Повільніше на ${p}%` : 'Середній темп';
  const bar = p ? `<i class="${p > 0 ? 'slow' : ''}" style="${p < 0 ? 'right' : 'left'}:50%;width:${w}%"></i>` : '';
  return `<span class="lvl"><span>${label}</span><span class="bar" role="img" aria-label="${label}">${bar}</span><span class="scale" aria-hidden="true"><span>швидше</span><span>повільніше</span></span></span>`;
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
  let h = '<thead><tr><th scope="col">Раса</th>';
  CLASSES.forEach(c => { h += `<th scope="col" class="${roleMatch(c, state.r) ? '' : 'dim'}${c.id === state.cls ? ' selc' : ''}">${face(c.id, CCOL[c.id])}${esc(c.n)}</th>`; });
  h += '</tr></thead><tbody>';
  ['alliance', 'horde'].forEach(f => {
    const rows = RACES.filter(r => r.f === f && raceVisible(r));
    if (!rows.length) return;
    h += `<tr class="fh ${f}"><th colspan="${CLASSES.length + 1}" scope="rowgroup"><span class="f ${f}"></span>${facName(f)}</th></tr>`;
    rows.forEach(r => {
      h += `<tr class="${r.id === state.race ? 'rowsel' : ''}"><th scope="row"><span class="rn">${face(RSLUG[r.id], `var(--${r.f})`)}${esc(r.n)}${r.paid ? '<span class="paid">платна</span>' : ''}</span></th>`;
      CLASSES.forEach(c => {
        const v = r.can[c.id];
        const dim = roleMatch(c, state.r) ? '' : ' dim';
        if (!v) { h += `<td><span class="cell no${dim}" role="img" aria-label="${esc(r.n)} ${esc(c.n)}: не можна"></span></td>`; return; }
        const sel = (r.id === state.race && c.id === state.cls) ? ' sel' : '';
        const label = `${r.n} ${c.n}${v === 'new' ? ', нова комбінація' : ''}`;
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
  const rac = r.rac.map(x => `<div class="card ab"><span class="abt${x[0] === 'a' ? '' : ' p'}">${x[0] === 'a' ? 'Активна' : 'Пасивна'}</span><b>${bi(x[1])}</b><span>${racx(x[2])}</span></div>`).join('');
  const text = `${r.name || r.n} ${c.n} (${facName(r.f)})${r.paid ? ', потрібен набір Скайборн' : ''}`;
  $('#detail').innerHTML = `
    <div class="d-head">
      <div class="d-art" aria-hidden="true"><picture><source type="image/avif" srcset="${ROOT}assets/art/${RSLUG[r.id]}-600.avif${PV}"><img src="${ROOT}assets/art/${RSLUG[r.id]}-600.webp${PV}" width="600" height="804" alt="" loading="lazy" decoding="async"></picture></div>
      <div class="d-avs">${face(RSLUG[r.id], `var(--${r.f})`)}</div>
      <div class="d-title"><h3>${esc(r.n)}${raceEn(r)} · ${esc(c.n)}</h3>
        <div class="chips"><span class="tag ${r.f}">${facName(r.f)}</span>${isNew ? '<span class="tag new">Нова комбінація</span>' : ''}${r.paid ? '<span class="tag paid">Платна раса</span>' : ''}${roleChips(c)}</div></div>
    </div>
    <div class="d-body">
      <div class="d-cols">
        <div><h4>Спеціалізації</h4><div class="cards">${specs}</div></div>
        <div><h4>Расові здібності</h4><div class="cards two">${rac}</div></div>
      </div>
      <div class="facts3">
        <div class="fact"><h4>Прокачування</h4>${lvlMeter(c)}</div>
        <div class="fact"><h4>У рейді</h4><span>${esc(c.raid)}.</span></div>
        <div class="fact"><h4>Що нового</h4><span>${esc(c.forever)}</span></div>
      </div>
      ${tipBox(esc(r.tip))}
      ${pickLinks(r, c)}
      <div class="copyrow">
        <input id="pickText" readonly value="${esc(text)}" aria-label="Мій вибір">
        <button class="btn" id="copyBtn"><svg class="ico" aria-hidden="true"><use href="#i-copy"/></svg>Скопіювати мій вибір</button>
        <button class="btn ghost" id="shareBtn">Поділитися</button>
        <span class="small" id="copyMsg" role="status"></span>
      </div>
    </div>`;
  $('#copyBtn').onclick = () => copyTo($('#pickText').value, $('#copyMsg'), 'Скопійовано');
  $('#shareBtn').onclick = () => shareBuild(r.id, c.id, state.spec, text);
}
/* Share: the link of the card page b/<race>-<class>-<spec>/ (its preview is the card with the name); on a phone the share sheet, else the clipboard */
function shareBuild(race, cls, spec, text) {
  const url = new URL(`${HOME}b/${BSLUG[race] || race}-${cls}-${spec}/`, location.href).href, msg = $('#copyMsg');
  if (navigator.share && matchMedia('(pointer: coarse)').matches) navigator.share({ title: text, url }).catch(e => { if (e && e.name !== 'AbortError') copyTo(url, msg, 'Посилання скопійовано'); });
  else copyTo(url, msg, 'Посилання скопійовано');
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
  eu: ['Європа', ''],
  cas: ['Європа', 'Свого регіону в Кавказу й Центральної Азії немає, найближчий — Європа.'],
  mea: ['Європа', 'Свого регіону в Близького Сходу й Африки немає, найближчий — Європа.'],
  na: ['Америка й Океанія', ''],
  la: ['Америка й Океанія', 'Латинська Америка грає в американському регіоні.'],
  oce: ['Америка й Океанія', 'Blizzard об’єднує Океанію з Америкою в один регіон. Чи є сервери в самій Океанії, Blizzard не повідомляла.'],
  kr: ['Корея', ''],
  tw: ['Тайвань', ''],
  asia: ['', 'Свого регіону немає. Найближчі на мапі — Тайвань і Корея. Оберіть той, де затримка World нижча.'],
};
function renderPing() {
  const v = $('#pgW').value, r = PG[v];
  try { if (v) localStorage.setItem('gabella-ping', v); } catch (e) {}
  if (!r) { $('#pgOut').innerHTML = ''; return; }
  $('#pgOut').innerHTML = (r[0] ? `<p class="preg">Ваш регіон: ${esc(r[0])}</p>` : '') + '<ul class="verdict">'
    + (r[1] ? `<li>${esc(r[1])}</li>` : '')
    + '<li>Реалмів немає: обирають регіон і режим, а не сервер. Регіон обирають у Battle.net перед запуском гри.</li>'
    + '<li>Персонажі та імена в кожному регіоні свої. Грати разом можна лише в одному регіоні.</li>'
    + '<li>Де стоять сервери регіонів, Blizzard не повідомляла.</li></ul>';
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
