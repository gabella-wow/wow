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
const CX = {"warrior": {"armor": "Ткань, кожа, кольчуга; латы с 40 уровня {beta}", "weapons": "Всё, кроме жезлов; щит", "resource": "Ярость", "lvl": "Самая медленная прокачка, примерно на 12% дольше среднего (оценка LFCarry)", "group": ["Боевой крик действует на весь рейд", "Деморализующий крик и Раскол брони на боссе", "Размашистые удары и Вихрь для боёв с толпой"], "pros": ["Лучший танк и сильный урон в ближнем бою", "Подходит для PvP (Оружие)", "Мало кнопок, понятная игра"], "cons": ["Самая медленная прокачка", "Сильно зависит от экипировки", "Почти нет самолечения и контроля"], "specs": [{"n": "Оружие", "what": "Урон в ближнем бою (двуручное оружие)"}, {"n": "Неистовство", "what": "Урон в ближнем бою (два оружия)"}, {"n": "Защита", "what": "Танк"}]}, "paladin": {"armor": "Ткань, кожа, кольчуга; латы с 40 уровня; щит {beta}", "weapons": "Топоры, булавы, мечи, древковое с 20 уровня {beta}", "resource": "Мана", "lvl": "Средний темп прокачки", "group": ["Ауры на группу: благочестия, воздаяния, сосредоточенности", "Ауры сопротивления огню, льду и тьме на весь рейд", "Благословения на час, большие благословения на весь класс", "Печать справедливости не даёт врагам убегать"], "pros": ["Все три роли на одном персонаже", "Сильные баффы для группы", "Латы и крепкий персонаж"], "cons": ["Нет рывка, замедления и ускорения", "Мало контроля, кроме Молота правосудия", "Воздаяние просело после патча"], "specs": [{"n": "Свет", "what": "Лекарь"}, {"n": "Защита", "what": "Танк"}, {"n": "Воздаяние", "what": "Урон в ближнем бою"}]}, "hunter": {"armor": "Ткань, кожа; кольчуга с 40 уровня {beta}", "weapons": "Луки, арбалеты, ружья, топоры, мечи, древковое", "resource": "Мана; у питомца фокус", "lvl": "Самая быстрая прокачка, примерно на 8% быстрее среднего (оценка LFCarry)", "group": ["Аура меткого выстрела усиливает дальний бой группы", "Замораживающая ловушка: надёжный контроль", "Дезориентирующий выстрел прерывает заклинания", "Дух стаи ускоряет всю группу в пути"], "pros": ["Самая быстрая прокачка", "Отлично играет один", "Ловушки и контроль"], "cons": ["Мёртвая зона вблизи до 8 метров", "Нужно следить за питомцем", "На бете у талантов Выживания были ошибки"], "specs": [{"n": "Повелитель зверей", "what": "Урон дальнего боя, много урона от питомца"}, {"n": "Стрельба", "what": "Урон дальнего боя"}, {"n": "Выживание", "what": "Ближний и дальний бой, ловушки"}]}, "rogue": {"armor": "Ткань, кожа", "weapons": "Кинжалы, мечи, булавы, кистевое, одноручные топоры, метательное", "resource": "Энергия и приёмы серии", "lvl": "Средний темп прокачки", "group": ["Чистый урон в ближнем бою без баффов на весь рейд", "Ошеломление, Ослепление и Удар по почкам: много контроля", "Пинок прерывает опасные заклинания"], "pros": ["Очень высокий урон и рост с экипировкой", "Скрытность и много контроля", "Свобода выбора оружия"], "cons": ["Сильно зависит от экипировки", "Нет самолечения", "Спасают только Ускользание и Исчезновение"], "specs": [{"n": "Ликвидация", "what": "Урон ядами"}, {"n": "Бой", "what": "Быстрые атаки оружием"}, {"n": "Скрытность", "what": "Засады, кровотечения"}]}, "priest": {"armor": "Ткань", "weapons": "Кинжалы, булавы, посохи, жезлы", "resource": "Мана", "lvl": "Примерно на 5% медленнее среднего (оценка LFCarry)", "group": ["Божественный дух и Слово силы: Стойкость на весь рейд", "Придание сил усиливает союзника", "Главный лекарь группы"], "pros": ["Всегда нужен группе", "Лечение или урон тьмой", "Много сборок"], "cons": ["Только ткань, хрупкий", "Мало способов быстро двигаться", "Скорость почти не помогает заклинаниям"], "specs": [{"n": "Послушание", "what": "Лекарь, щиты и поглощение"}, {"n": "Свет", "what": "Лекарь"}, {"n": "Темная магия", "what": "Урон дальнего боя"}]}, "shaman": {"armor": "Ткань, кожа; кольчуга с 40 уровня; щит {beta}", "weapons": "Булавы, топоры, посохи, кистевое, кинжалы", "resource": "Мана", "lvl": "Средний темп прокачки", "group": ["Тотемы силы земли, неистовства ветра, языков пламени и грации воздуха усиливают свою группу", "Тотем трепета снимает страх, сон и очарование", "Тотемы очищения от ядов и болезней", "Развеивание магии снимает баффы с врагов"], "pros": ["Сильные тотемы для группы", "Мобильная прокачка", "Новые сильные таланты"], "cons": ["Нет жёсткого контроля", "Мана в долгих боях", "Танк пока под вопросом"], "specs": [{"n": "Стихии", "what": "Урон дальнего боя"}, {"n": "Совершенствование", "what": "Урон в ближнем бою. Возможность танковать пока под вопросом"}, {"n": "Исцеление", "what": "Лекарь"}]}, "mage": {"armor": "Ткань", "weapons": "Кинжалы, мечи, посохи, жезлы", "resource": "Мана", "lvl": "Самая быстрая прокачка, примерно на 8% быстрее среднего, около 12 часов экономии (оценка LFCarry)", "group": ["Порталы с 40 уровня, телепорт с 20", "Еда и вода для группы", "Превращение: надёжный контроль", "Снятие малого проклятия"], "pros": ["Самая быстрая прокачка", "Порталы и еда для всех", "Три сильные и разные ветки"], "cons": ["Только ткань, хрупкий", "Мана быстро кончается", "Урон по площади ослаблен"], "specs": [{"n": "Тайная магия", "what": "Бурст, много маны"}, {"n": "Огонь", "what": "Криты и поджоги"}, {"n": "Лёд", "what": "Урон и контроль"}]}, "warlock": {"armor": "Ткань", "weapons": "Кинжалы, мечи, посохи, жезлы", "resource": "Мана; Жизнеотвод меняет здоровье на ману", "lvl": "Средний темп прокачки", "group": ["Камень здоровья и Камень души", "Ритуал призыва: собирает группу", "Проклятие косноязычия замедляет заклинания на 60%", "Проклятие стихий: больше магического урона по цели"], "pros": ["Самостоятельный: демон и Жизнеотвод", "Много пользы группе", "Сильный урон со временем"], "cons": ["Хрупкий и неподвижный", "Урон раскачивается не сразу", "Нет рывка и ускорения"], "specs": [{"n": "Колдовство", "what": "Урон от проклятий и порчи"}, {"n": "Демонология", "what": "Урон через демонов"}, {"n": "Разрушение", "what": "Прямой урон огнём и тьмой"}]}, "druid": {"armor": "Ткань, кожа", "weapons": "Кинжалы, булавы, посохи, кистевое, древковое с 20 уровня {beta}", "resource": "Мана; ярость в облике медведя, энергия в облике кошки", "lvl": "Примерно на 5% медленнее среднего (оценка LFCarry)", "group": ["Вожак стаи и аура лунного совуха действуют на весь рейд и складываются", "Возрождение: воскрешение в бою", "Озарение возвращает ману лекарю", "Снимает проклятия и яды"], "pros": ["Все три роли на одном персонаже", "Отличная мобильность", "Воскрешение в бою"], "cons": ["Нет блока и парирования у медведя", "Сложнее следить за эффектами лечения", "Итоговые цифры в рейдах ещё неизвестны"], "specs": [{"n": "Баланс", "what": "Урон дальнего боя"}, {"n": "Сила зверя", "what": "Танк (медведь) и урон в ближнем бою (кошка)"}, {"n": "Исцеление", "what": "Лекарь, много лечения по времени"}]}};
const HC = {"tx":{"title":"Мой персонаж","lead":"Без входа и пароля: выберите класс, спек и расу, и сайт подстроится под вас.","local":"Сохраняется только в этом браузере.","none":"Персонаж ещё не создан","create":"Создать персонажа","edit":"Изменить","reset":"Удалить персонажа","resetQ":"Удалить персонажа из этого браузера?","steps":["Сторона","Класс и спек","Раса","Облик","Детали"],"side":"За кого играете?","cls":"Класс","spec":"Спек","race":"Раса","bestFor":"Лучшая раса для спека «%s»","best":"лучшая","paid":"платная","sex":"Пол","m":"Мужской","f":"Женский","bg":"Фон портрета","lvl":"Уровень","reg":"Регион","lvlReg":"Уровень и регион","regs":{"us":"Америка и Океания","eu":"Европа","kr":"Корея","tw":"Тайвань"},"p1":"Профессия 1","p2":"Профессия 2","secP":"Вспомогательные профессии","noP":"Нет","role":"Роль","back":"Назад","next":"Дальше","done":"Готово","cancel":"Отмена","later":"Можно заполнить позже.","levelN":"%n уровень","build":"Моя сборка талантов","buildD":"Таланты спека «%s» по уровням.","pairs":"Пары профессий","pairsD":"Какие профессии взять классу.","bestR":"Лучшие расы","bestRD":"Раса под класс за обе фракции.","lvlG":"Прокачка класса","lvlGD":"Маршрут и таланты 1–60.","day1":"День 1 под персонажа","day1D":"Чек-лист старта с вашим классом и расой.","play":"В игре","playD":"Зоны и подземелья под уровень, таймеры, радио.","dung":"Подземелья под уровень","dungNo":"Укажите уровень, и подберём подземелья.","dungFirst":"Первые подземелья с 13 уровня.","resetH":"Сброс недели","resetIn":"через %s","resetNote":"Время сброса Forever Blizzard ещё не объявила. Показано, как в других версиях WoW этого региона: сверим на старте.","resetUnk":"Для этого региона время сброса уточним на старте.","resetNoReg":"Укажите регион, и покажем сброс недели.","resetWhy":"Рейды открываются 09.12, у них недельное сохранение.","lfg":"Текст для поиска группы","lfgD":"Вставьте в чат LookingForGroup. Названия как в игре.","lfgP":{"tank":"%c-танк ищет группу","heal":"%c-лекарь ищет группу","dps":"%c ищет группу"},"lfgT":"%p: %d, %l уровень.","lfgT0":"%p.","allD":"Все подземелья","copy":"Скопировать","copied":"Скопировано","sync":"Синхронизировать между устройствами","syncD":"Вход нужен только для этого: персонаж будет на телефоне и на ПК, а письмо к старту придёт на почту, если подпишетесь.","yourCls":"Твой %s","bTalents":"Таланты","bSpec":"Билд: %s","bLevel":"Прокачка","bGroup":"Группа","bNews":"Новости","copiedT":"Скопировано: %s","profsL":"Профессии","day1n":"День 1: %n из %t","collect":"Собрать персонажа","collectD":"Класс, спек и раса: таланты, прокачка, группа и новости вашего класса.","change":"Сменить","allSet":"Все настройки","close":"Закрыть","mine":"Касается вашего класса","share":"Поделиться","linkCopied":"Ссылка скопирована","make":"Сделать моим персонажем","made":"Это ваш персонаж","plaqueH":"Мой персонаж","plaqueD":"Класс, спек и раса за минуту, а дальше ваша сборка, профессии и подземелья.","day1Mine":"Под вашего персонажа","ckClass":"Ваш спек «%s»: сборка талантов по уровням.","ckRaceOk":"%r — лучшая раса под ваш спек.","ckRaceAlt":"Лучшая раса под ваш спек: %r.","ckProfs":"Пары профессий для класса «%s».","ckStart":"Прокачка за класс «%s»: маршрут и первые таланты.","ckPing":"Ваш регион: %s.","or":"или"},"best":{"warrior":{"alliance":{"*":[["human","nightelf"],"Человек: +1% крита любым оружием. Ночной эльф: +10% крита на 15 сек. Источники делятся почти поровну."],"protection":[["dwarf"],"Каменная форма снижает физический урон на 10% и снимает кровотечения."]},"horde":{"*":[["orc"],"Кровавое неистовство: +10% силы атаки на 15 сек. До правок рас 26.10 его ставили первым все источники."],"protection":[["tauren"],"Закалка даёт +5% здоровья, Громовая поступь оглушает врагов рядом."]}},"paladin":{"alliance":{"*":[["human"],"Беспощадность усиливает и удары, и заклинания, Воля к жизни снимает оглушения."],"protection":[["dwarf"],"Каменная форма и Artisan’s Precision: +1% к меткости."]},"horde":{"*":[["undead"],"За Орду паладином может быть только Нежить. Каннибализм возвращает ману, Воля Отрекшихся снимает страх."]}},"hunter":{"alliance":{"*":[["human","nightelf"],"Человек: +1% крита, и питомец наследует крит. Ночной эльф: Свет Элуны и Слиться с тенью."]},"horde":{"*":[["orc","troll"],"Орк: Кровавое неистовство и Властность (+5% к урону питомца). Тролль: +5% урона по зверям."]}},"rogue":{"alliance":{"*":[["nightelf"],"Слиться с тенью снижает угрозу и в бою, плюс Свет Элуны и Расторопность."]},"horde":{"*":[["orc"],"Кровавое неистовство: +10% силы атаки на 15 сек."]}},"priest":{"alliance":{"*":[["gnome"],"Выбор всех источников: Эврика! усиливает и Слово силы: Щит, Пытливый ум даёт +5% маны."]},"horde":{"*":[["undead","troll"],"Источники делятся. Нежить сильнее в PvP: Воля Отрекшихся снимает страх, сон и очарование."]}},"shaman":{"alliance":{"*":[["dwarf"],"За Альянс шаманом может быть только Дворф: Каменная форма и Artisan’s Precision (+1% к меткости)."]},"horde":{"*":[["orc"],"Кровавое неистовство даёт и силу атаки, и силу заклинаний: подходит и Стихиям, и Совершенствованию."],"restoration":[["troll"],"Лекарю источник советует Тролля: Боевое исступление, +10% к скорости заклинаний на 12 сек."]}},"mage":{"alliance":{"*":[["gnome"],"Эврика! на 8 сек, Пытливый ум: +5% маны, Мастер побега снимает корни."]},"horde":{"*":[["orc"],"Маг-орк — новое сочетание Forever: Кровавое неистовство теперь даёт силу заклинаний."]}},"warlock":{"alliance":{"*":[["gnome","human"],"Гном: Эврика! и Пытливый ум. Человек: периодический урон критует, Беспощадность даёт +1% крита."]},"horde":{"*":[["orc","undead"],"Орк: Кровавое неистовство даёт силу заклинаний. Нежить чаще берут в PvP."]}},"druid":{"alliance":{"*":[["nightelf"],"Свет Элуны: +10% крита на 15 сек, и Расторопность."]},"horde":{"*":[["tauren"],"Закалка: +5% здоровья, Громовая поступь работает и в формах."]}}},"sid":{"warrior":["arms","fury","protection"],"paladin":["holy","protection","retribution"],"hunter":["beast-mastery","marksmanship","survival"],"rogue":["assassination","combat","subtlety"],"priest":["discipline","holy","shadow"],"shaman":["elemental","enhancement","restoration"],"mage":["arcane","fire","frost"],"warlock":["affliction","demonology","destruction"],"druid":["balance","feral","restoration"]},"sn":{"warrior":["Оружие","Неистовство","Защита"],"paladin":["Свет","Защита","Воздаяние"],"hunter":["Повелитель зверей","Стрельба","Выживание"],"rogue":["Ликвидация","Бой","Скрытность"],"priest":["Послушание","Свет","Темная магия"],"shaman":["Стихии","Совершенствование","Исцеление"],"mage":["Тайная магия","Огонь","Лёд"],"warlock":["Колдовство","Демонология","Разрушение"],"druid":["Баланс","Сила зверя","Исцеление"]},"fn":{"alliance":"Альянс","horde":"Орда"},"reset":{"us":[2,15],"eu":[3,4],"kr":null,"tw":null},"rn":{"human":"Человек","dwarf":"Дворф","nightelf":"Ночной эльф","gnome":"Гном","skyA":"Высший скайборн","orc":"Орк","undead":"Нежить","tauren":"Таурен","troll":"Тролль","skyH":"Скайборн-ветрорез"},"rf":{"human":"alliance","dwarf":"alliance","nightelf":"alliance","gnome":"alliance","skyA":"alliance","orc":"horde","undead":"horde","tauren":"horde","troll":"horde","skyH":"horde"},"cn":{"warrior":"Воин","paladin":"Паладин","hunter":"Охотник","rogue":"Разбойник","priest":"Жрец","shaman":"Шаман","mage":"Маг","warlock":"Чернокнижник","druid":"Друид"},"cen":{"warrior":"Warrior","paladin":"Paladin","hunter":"Hunter","rogue":"Rogue","priest":"Priest","shaman":"Shaman","mage":"Mage","warlock":"Warlock","druid":"Druid"}};
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

const CPROF = {"warrior": [["Прокачка: Кузнечное дело + Горное дело", ""], ["60 уровень: Инженерное дело + Горное дело", "Кузнец одевает себя в латы и оружие, многие рецепты персональные. Инженеру — гранаты и устройства, которых воину не хватает."]], "paladin": [["Прокачка: Кузнечное дело + Горное дело", ""], ["60 уровень: Защита, Воздаяние: Инженерное дело + Горное дело. Свет: Алхимия + Травничество", "Свет тратит много маны: зелья свои, а Mana Well в лагере заменяет Благословение мудрости."]], "hunter": [["Прокачка: Кожевничество + Снятие шкур", ""], ["60 уровень: Инженерное дело + Горное дело", "Кожевник шьёт себе кожу и кольчугу и Armor Kit. Инженер делает прицелы и ружья."]], "rogue": [["Прокачка: Кожевничество + Снятие шкур", ""], ["60 уровень: Инженерное дело + Горное дело", "Кожа своя, Camp Tent даёт отдых. Инженерное дело — главное для PvP."]], "priest": [["Прокачка: Портняжное дело + Наложение чар", ""], ["60 уровень: Портняжное дело + Инженерное дело или Наложение чар", "Портной делает пояса с силой заклинаний с 10 уровня, зачарователь — жезлы с силой заклинаний с 5. Сшитое распыляют на материалы."]], "shaman": [["Прокачка: Кожевничество + Снятие шкур", ""], ["60 уровень: Алхимия + Травничество", "Кожевник делает вещи с силой заклинаний для Стихий и Исцеления и экипировку для Совершенствования. В рейде и группе нужны зелья."]], "mage": [["Прокачка: Портняжное дело + Наложение чар", ""], ["60 уровень: Портняжное дело + Наложение чар; для PvP и больших пулов Инженерное дело + Горное дело", "Портной даёт раннюю экипировку с силой заклинаний, сшитое распыляют. Гранаты инженера держат на месте большие группы врагов."]], "warlock": [["Прокачка: Портняжное дело + Наложение чар", ""], ["60 уровень: Портняжное дело + Алхимия", "Faction Banner портного даёт дух для Жизнеотвода. Алхимия — зелья и золото."]], "druid": [["Прокачка: Кожевничество + Снятие шкур или Травничество", ""], ["60 уровень: Алхимия + Травничество", "Травы собирают в Походном облике, зелья пьют в любом облике. Mana Well и Incense Candle — для Баланса и Исцеления."]]};   /* recommended profession pairs per class, already in the page language (build.class_profs) */
const $ = s => document.querySelector(s);
const ROOT = '../', HOME = '../';
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
  try { await navigator.clipboard.writeText(text); msgEl.textContent = ok; } catch (e) { msgEl.textContent = 'Не удалось скопировать, выделите и нажмите Ctrl+C'; }
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
    out.push((groups > 1 ? `Группа ${g + 1}: ` : '') + part.map(p => `${p.name ? p.name + ' — ' : ''}${raceName(RC[p.race])} ${CL[p.cls].n} (${ROLE_RU[p.role]})`).join(', '));
  }
  return out.length ? out.join('\n') + `\n${FAC[R.f]}, ${R.size}` : '';
}

/* LFG line: the dungeon or raid, the missing roles, the play style and a short link (#t=); kept under the 255-byte chat limit */
const LFG = {"d": [["Огненная пропасть", 13, 18, "horde"], ["Hall of Thanes", 13, 18, 0], ["Руины Лордерона", 15, 20, 0], ["Мертвые копи", 15, 22, 0], ["Пещеры Стенаний", 17, 24, 0], ["Крепость Темного Клыка", 20, 26, 0], ["Непроглядная Пучина", 22, 28, 0], ["Тюрьма", 25, 29, "alliance"], ["Раскопки в Болотине", 26, 31, 0], ["City of Dalaran", 28, 33, 0], ["Гномреган", 29, 38, 0], ["Лабиринты Иглошкурых", 29, 38, 0], ["Монастырь Алого ордена: кладбище", 30, 38, 0], ["Монастырь Алого ордена: библиотека", 33, 41, 0], ["The Drowned City", 35, 40, 0], ["Монастырь Алого ордена: оружейная", 36, 44, 0], ["Ульдаман", 36, 45, 0], ["Курганы Иглошкурых", 37, 46, 0], ["Монастырь Алого ордена: собор", 38, 46, 0], ["Зул’Фаррак", 40, 47, 0], ["Krol'dok Stronghold", 40, 45, 0], ["Мародон", 45, 51, 0], ["Alcaz Island Prison", 48, 53, 0], ["Храм Атал’Хаккара", 50, 55, 0], ["Глубины Черной горы", 52, 60, 0], ["Blackmaw Hold", 55, 60, 0], ["Нижняя часть Вершины Черной горы", 57, 60, 0], ["Забытый Город: восток", 58, 60, 0], ["Shaper's Terrace", 58, 60, 0], ["Стратхольм: живые", 58, 60, 0], ["Стратхольм: нежить", 58, 60, 0], ["Некроситет", 58, 60, 0], ["Верхняя часть Вершины Черной горы", 60, 60, 0], ["Забытый Город: запад", 60, 60, 0], ["Забытый Город: север", 60, 60, 0]], "r": {"10": "Barrow Deeps", "20": "Вершина Хиджала", "40": "Логово Ониксии"}};   // dungeons [name, min, max, entrance faction] and raids {size: name} in the client's language (build_tools)
const CHAT_MAX = 255, CANON = 'https://gabella.site/wow/tools/'.replace(/^https?:\/\//, '');
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
  const head = (L.d ? '%d — нужны: %n.' : 'Нужны в группу: %n.').replace('%d', L.d).replace('%n', roles);
  const parts = [head, L.s ? 'Стиль: %s.'.replace('%s', L.s) : '', CANON + shortHash()].filter(Boolean);
  const bytes = t => new TextEncoder().encode(t).length;
  let text = parts.join(' ');
  if (bytes(text) > CHAT_MAX) text = parts.slice(0, -1).join(' ');   // a long raid code would not fit: the link goes first
  return text;
}
function renderLfg() {
  const places = lfgPlaces(), sel = $('#lfgD');
  if (!places.some(p => p[0] === L.d)) L.d = R.size === 5 ? '' : (places[0] || [''])[0];
  $('#lfgDL').textContent = R.size === 5 ? 'Подземелье' : 'Рейд';
  sel.innerHTML = (R.size === 5 ? '<option value="">Любое подземелье</option>' : '') + places.map(([v, t]) => `<option value="${esc(v)}"${v === L.d ? ' selected' : ''}>${esc(t)}</option>`).join('');
  syncSeg('lfgS', L.s);
  const text = lfgText();
  $('#rLfg').value = text;
  $('#rCopyLfg').disabled = !text;
  $('#rLfgMsg').textContent = text ? lfgLen(text) : R.s.some(Boolean) ? 'Все места заняты.' : 'Добавьте в состав хотя бы одного игрока.';
}
function lfgLen(t) { return 'Знаков: %n из %m (лимит строки чата).'.replace('%n', t.length).replace('%m', CHAT_MAX); }

function unitHTML(p, i) {
  const cls = R.moving === i ? ' src' : '';
  if (!p) return `<button type="button" class="unit empty${cls}" data-i="${i}"><span class="up" aria-hidden="true">+</span><span class="ub"><b>Свободное место</b><span>Нажмите, чтобы добавить игрока</span></span></button>`;
  const c = CL[p.cls], r = RC[p.race];
  return `<button type="button" class="unit${cls}" data-i="${i}" draggable="true" style="--cc:${CCOL[p.cls]};--pc:${power(p)}" aria-label="${esc((p.name || `Игрок ${i + 1}`) + ', ' + raceName(r) + ' ' + c.n + ', ' + ROLE_RU[p.role])}">
    <span class="up"><picture><source type="image/avif" srcset="${unitArt(p, 'avif')}"><img src="${unitArt(p, 'webp')}" width="360" height="482" alt="" loading="lazy" decoding="async"></picture></span>
    <span class="ub"><span class="un"><span class="ur" title="${ROLE_RU[p.role]}">${ri(p.role)}</span><b>${esc(p.name || c.n)}</b><small>${esc(raceName(r))} · ${esc(c.n)}</small></span><span class="hp"><i></i></span><span class="mp"></span></span></button>`;
}
function cellHTML(p, i) {
  const cls = R.moving === i ? ' src' : '';
  if (!p) return `<button type="button" class="rc empty${cls}" data-i="${i}" aria-label="Свободное место ${i + 1}"><span aria-hidden="true">+</span>Добавить</button>`;
  const c = CL[p.cls], r = RC[p.race];
  return `<button type="button" class="rc${cls}" data-i="${i}" draggable="true" style="--cc:${CCOL[p.cls]};--pc:${power(p)}" aria-label="${esc((p.name || `Игрок ${i + 1}`) + ', ' + raceName(r) + ' ' + c.n + ', ' + ROLE_RU[p.role])}" title="${esc(raceName(r) + ' · ' + c.n + ' · ' + ROLE_RU[p.role])}"><b>${esc(p.name || c.n)}</b><small>${esc(p.name ? c.n : raceName(r))}</small>${ri(p.role)}</button>`;
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
      const st = n && (!c.tank || !c.heal) ? `<span class="warn">${!c.tank ? 'нет танка' : 'нет лекаря'}</span>` : `<span>${n}/5</span>`;
      h += `<div class="rg"><div class="rg-h"><b>Группа ${g + 1}</b>${st}</div>${part.map((p, k) => cellHTML(p, g * PARTY + k)).join('')}</div>`;
    }
    $('#rview').innerHTML = `<div class="rgrid" style="--gc:${Math.min(groups, 8)}">${h}</div>`;
  }
  const hint = $('#rhint');
  hint.classList.toggle('on', R.moving >= 0);
  hint.innerHTML = R.moving >= 0 ? `Выберите место, куда переставить игрока ${R.moving + 1}. <button type="button" id="mvCancel">Отмена</button>` : '';

  const list = R.s.filter(Boolean), cnt = countRoles(list), rec = REC[R.size];
  $('#rRoles').innerHTML = RR.map((x, k) => `<span class="${list.length && cnt[x] < rec[k] ? 'low' : ''}">${ri(x)}${ROLE_RU[x]} <b>${cnt[x]}</b> / ${rec[k]}</span>`).join('');
  $('#rTip').textContent = R.size === 5 ? 'Для подземелья нужны танк, лекарь и три бойца урона.' : `Ориентир для рейда: танков ${rec[0]}, лекарей ${rec[1]}, остальные урон. Точное число зависит от боссов.`;
  const have = new Set(list.map(p => p.cls));
  $('#rBuffs').innerHTML = CLASSES.filter(c => BUFF[c.id]).map(c => `<li class="${have.has(c.id) ? '' : 'off'}" style="--cc:${CCOL[c.id]}"><span class="cdot"></span><span><b>${esc(c.n)}:</b> ${esc(BUFF[c.id])}</span></li>`).join('');
  const n = list.length;
  $('#rRaids').innerHTML = n ? RAIDS.map(([size, name]) => `<li class="${n >= size ? 'good' : ''}">${n >= size ? `Рейд на ${size} (${name}): людей хватает.` : `Рейд на ${size} (${name}): не хватает ${size - n}.`}</li>`).join('') : '<li>Пока никого нет. Нажмите «Моим персонажем», «Заполнить пустые» или на свободную рамку.</li>';

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
function myHero() {   // the hero of this browser (assets/hero/hero.js?v=b4acd02a83, localStorage gabella-wf-me)
  let h = null; try { h = JSON.parse(localStorage.getItem('gabella-wf-me')); } catch (e) {}
  return h && RC[h.race] && CL[h.cls] && RC[h.race].can[h.cls] ? h : null;
}
$('#rMine').onclick = () => {
  const h = myHero(), msg = $('#rMy');
  if (!h) {
    msg.innerHTML = 'Персонажа пока нет. <a href="../character/" id="rMake">Собрать персонажа</a>';
    $('#rMake').onclick = e => { if (window.GabellaHero) { e.preventDefault(); GabellaHero.open(); } };
    return;
  }
  const f = RC[h.race].f, role = RR.includes(h.role) ? h.role : roleOpts(CL[h.cls])[0];
  if (f !== R.f) {
    if (R.s.some(Boolean)) { msg.textContent = 'Ваш персонаж играет за другую фракцию: переключите фракцию над рамками.'; return; }
    R.f = f;
  }
  if (R.s.some(p => p && p.race === h.race && p.cls === h.cls && p.role === role && !p.name)) { msg.textContent = 'Ваш персонаж уже в составе.'; return; }
  let i = R.s.findIndex(p => !p); if (i < 0) i = 0;
  R.s[i] = { race: h.race, cls: h.cls, role, name: '' };
  msg.textContent = ''; R.moving = -1; renderRaid();
};
$('#rClear').onclick = () => { R.s = Array(R.size).fill(null); R.moving = -1; renderRaid(); };
$('#rCopyLink').onclick = () => copyTo(teamLink(), $('#rMsg'), 'Ссылка скопирована');
$('#rCopyText').onclick = () => copyTo(teamText(), $('#rMsg'), 'Состав скопирован');
$('#lfgD').onchange = e => { L.d = e.target.value; renderLfg(); };
$('#lfgS').addEventListener('click', e => { const b = e.target.closest('button'); if (b) { L.s = L.s === b.dataset.v ? '' : b.dataset.v; renderLfg(); } });
$('#rCopyLfg').onclick = () => { const t = lfgText(); copyTo(t, $('#rLfgMsg'), 'Текст скопирован. ' + lfgLen(t)); };

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
  $('#edT').textContent = `Игрок ${edI + 1}` + (R.size > 5 ? ` · Группа ${Math.floor(edI / PARTY) + 1}` : '');
  $('#edRace').innerHTML = RACES.filter(r => r.f === R.f).map(r => `<option value="${r.id}"${r.id === p.race ? ' selected' : ''}>${esc(raceName(r))}${r.paid ? ' (платная)' : ''}</option>`).join('');
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
  else box.innerHTML = ['alliance', 'horde'].map(f => `<div class="rside ${f}"><h3>${FAC[f]}</h3>${RACES.filter(r => r.f === f).map(r => { const k = sel.indexOf(r.id); return `<button type="button" class="rp" data-id="${r.id}" aria-pressed="${k >= 0}">${esc(raceName(r))}${r.paid ? '<span class="tag paid">платная</span>' : ''}<span class="no">${k + 1}</span></button>`; }).join('')}</div>`).join('');
  $('#cNote').textContent = `Выбрано ${sel.length} из 3`;
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
const ul = (items, cls) => items.length ? `<ul${cls ? ` class="${cls}"` : ''}>${items.map(x => `<li>${x}</li>`).join('')}</ul>` : '<span class="none">Нет</span>';
const row = (lab, vals, extra) => `<div class="crow${extra ? ' ' + extra : ''}"><div class="lab${extra === 'tiprow' ? ' tl' : ''}">${lab}</div>${vals.map(v => `<div class="val">${v}</div>`).join('')}</div>`;
function renderCmp() {
  const out = [];
  if (C.mode === 'class') {
    const ids = C.cls;
    out.push(`<div class="crow chead"><div class="lab"></div>${ids.map(id => `<div class="val" style="--cc:${CCOL[id]}"><picture><source type="image/avif" srcset="${art(id, 'avif')}"><img src="${art(id)}" width="360" height="482" alt="" loading="lazy" decoding="async"></picture><b>${esc(CL[id].n)}</b><a href="${classUrl(id)}">Страница класса<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>`).join('')}</div>`);
    out.push(row('Роли', ids.map(id => CL[id].roles.map(r => `<span class="role">${ri(r)}${ROLE_RU[r]}</span>`).join(''))));
    out.push(row('Броня', ids.map(id => racx(CX[id].armor))));
    out.push(row('Вооружение', ids.map(id => racx(CX[id].weapons))));
    out.push(row('Ресурс', ids.map(id => esc(CX[id].resource))));
    out.push(row('Прокачка', ids.map(id => esc(CX[id].lvl))));
    out.push(row('Специализации', ids.map(id => ul(CX[id].specs.map(s => `<b>${esc(s.n)}</b>${SPEC_SEP}<span class="sub">${esc(s.what)}</span>`)))));
    out.push(row('Бафф для рейда', ids.map(id => BUFF[id] ? esc(BUFF[id]) : '<span class="none">Нет</span>')));
    out.push(row('В группе', ids.map(id => ul(CX[id].group.map(esc)))));
    out.push(row('Профессии', ids.map(id => ul(CPROF[id].map(p => `<b>${esc(p[0])}</b>${p[1] ? `<br><span class="sub">${esc(p[1])}</span>` : ''}`)) + `<a class="cgo" href="${HOME}guides/professions/#pairs=${id}">Объекты лагеря и прокачка<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a>`)));
    out.push(row('Сильные стороны', ids.map(id => ul(CX[id].pros.map(esc), 'plus'))));
    out.push(row('Слабые стороны', ids.map(id => ul(CX[id].cons.map(esc), 'minus'))));
    ['alliance', 'horde'].forEach(f => out.push(row(`Расы: ${FAC[f]}`, ids.map(id => { const rs = RACES.filter(r => r.f === f && r.can[id]); return rs.length ? rs.map(r => `<a href="${raceUrl(r.id)}">${esc(raceName(r))}</a>`).join(', ') : '<span class="none">Нет</span>'; }))));
  } else {
    const ids = C.race;
    out.push(`<div class="crow chead"><div class="lab"></div>${ids.map(id => { const r = RC[id]; return `<div class="val race ${r.f}"><span class="fx">${FAC[r.f]}${r.paid ? ' · платная' : ''}</span><b>${esc(raceName(r))}</b><a href="${raceUrl(id)}">Страница расы<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>`; }).join('')}</div>`);
    out.push(row('Классы', ids.map(id => ul(Object.keys(RC[id].can).map(c => `<span style="color:${CCOL[c]}">●</span> ${esc(CL[c].n)}${RC[id].can[c] === 'new' ? ' <span class="tag new">новое</span>' : ''}`)))));
    out.push(row('Активные способности', ids.map(id => ul(RC[id].rac.filter(x => x[0] === 'a').map(x => `<b>${esc(x[1])}</b><br><span class="sub">${racx(x[2])}</span>`)))));
    out.push(row('Пассивные способности', ids.map(id => ul(RC[id].rac.filter(x => x[0] === 'p').map(x => `<b>${esc(x[1])}</b><br><span class="sub">${racx(x[2])}</span>`)))));
    out.push(row('Совет', ids.map(id => esc(RC[id].tip)), 'tiprow'));
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
const tipBox = h => `<div class="tipbox"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg><p><span class="tl">Совет</span>${h}</p></div>`;
function face(id, cc, cls = '', title = '', f) { return `<span class="av ${cls}" style="--cc:${cc}"${title ? ` title="${esc(title)}"` : ''}><img src="${ROOT}assets/art/${porId(id, f)}-face.webp${PV}" width="160" height="160" alt="" loading="lazy" decoding="async"></span>`; }
function lvlMeter(c) {
  const p = c.lp || 0, w = Math.min(Math.abs(p) / 12 * 46, 46);
  const label = p < 0 ? `Быстрее на ${-p}%` : p > 0 ? `Медленнее на ${p}%` : 'Средний темп';
  const bar = p ? `<i class="${p > 0 ? 'slow' : ''}" style="${p < 0 ? 'right' : 'left'}:50%;width:${w}%"></i>` : '';
  return `<span class="lvl"><span>${label}</span><span class="bar" role="img" aria-label="${label}">${bar}</span><span class="scale" aria-hidden="true"><span>быстрее</span><span>медленнее</span></span></span>`;
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
      h += `<tr class="${r.id === state.race ? 'rowsel' : ''}"><th scope="row"><span class="rn">${face(RSLUG[r.id], `var(--${r.f})`)}${esc(r.n)}${r.paid ? '<span class="paid">платная</span>' : ''}</span></th>`;
      CLASSES.forEach(c => {
        const v = r.can[c.id];
        const dim = roleMatch(c, state.r) ? '' : ' dim';
        if (!v) { h += `<td><span class="cell no${dim}" role="img" aria-label="${esc(r.n)} ${esc(c.n)}: нельзя"></span></td>`; return; }
        const sel = (r.id === state.race && c.id === state.cls) ? ' sel' : '';
        const label = `${r.n} ${c.n}${v === 'new' ? ', новая комбинация' : ''}`;
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
  const rac = r.rac.map(x => `<div class="card ab"><span class="abt${x[0] === 'a' ? '' : ' p'}">${x[0] === 'a' ? 'Активная' : 'Пассивная'}</span><b>${bi(x[1])}</b><span>${racx(x[2])}</span></div>`).join('');
  const text = `${r.name || r.n} ${c.n} (${facName(r.f)})${r.paid ? ', нужен набор Скайборн' : ''}`;
  $('#detail').innerHTML = `
    <div class="d-head">
      <div class="d-art" aria-hidden="true"><picture><source type="image/avif" srcset="${ROOT}assets/art/${RSLUG[r.id]}-600.avif${PV}"><img src="${ROOT}assets/art/${RSLUG[r.id]}-600.webp${PV}" width="600" height="804" alt="" loading="lazy" decoding="async"></picture></div>
      <div class="d-avs">${face(RSLUG[r.id], `var(--${r.f})`)}</div>
      <div class="d-title"><h3>${esc(r.n)}${raceEn(r)} · ${esc(c.n)}</h3>
        <div class="chips"><span class="tag ${r.f}">${facName(r.f)}</span>${isNew ? '<span class="tag new">Новая комбинация</span>' : ''}${r.paid ? '<span class="tag paid">Платная раса</span>' : ''}${roleChips(c)}</div></div>
    </div>
    <div class="d-body">
      <div class="d-cols">
        <div><h4>Специализации</h4><div class="cards">${specs}</div></div>
        <div><h4>Способности расы</h4><div class="cards two">${rac}</div></div>
      </div>
      <div class="facts3">
        <div class="fact"><h4>Прокачка</h4>${lvlMeter(c)}</div>
        <div class="fact"><h4>В рейде</h4><span>${esc(c.raid)}.</span></div>
        <div class="fact"><h4>Что нового</h4><span>${esc(c.forever)}</span></div>
      </div>
      ${tipBox(esc(r.tip))}
      ${pickLinks(r, c)}
      <div class="copyrow">
        <input id="pickText" readonly value="${esc(text)}" aria-label="Мой выбор">
        <button class="btn" id="copyBtn"><svg class="ico" aria-hidden="true"><use href="#i-copy"/></svg>Скопировать мой выбор</button>
        <button class="btn ghost" id="shareBtn">Поделиться</button>
        <span class="small" id="copyMsg" role="status"></span>
      </div>
    </div>`;
  $('#copyBtn').onclick = () => copyTo($('#pickText').value, $('#copyMsg'), 'Скопировано');
  $('#shareBtn').onclick = () => shareBuild(r.id, c.id, state.spec, text);
}
/* Share: the link of the card page b/<race>-<class>-<spec>/ (its preview is the card with the name); on a phone the share sheet, else the clipboard */
function shareBuild(race, cls, spec, text) {
  const url = new URL(`${HOME}b/${BSLUG[race] || race}-${cls}-${spec}/`, location.href).href, msg = $('#copyMsg');
  if (navigator.share && matchMedia('(pointer: coarse)').matches) navigator.share({ title: text, url }).catch(e => { if (e && e.name !== 'AbortError') copyTo(url, msg, 'Ссылка скопирована'); });
  else copyTo(url, msg, 'Ссылка скопирована');
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
  eu: ['Европа', ''],
  cas: ['Европа', 'Своего региона у Кавказа и Средней Азии нет, ближайший — Европа.'],
  mea: ['Европа', 'Своего региона у Ближнего Востока и Африки нет, ближайший — Европа.'],
  na: ['Америка и Океания', ''],
  la: ['Америка и Океания', 'Латинская Америка играет в американском регионе.'],
  oce: ['Америка и Океания', 'Blizzard объединяет Океанию с Америкой в один регион. Есть ли серверы в самой Океании, Blizzard не сообщала.'],
  kr: ['Корея', ''],
  tw: ['Тайвань', ''],
  asia: ['', 'Своего региона нет. Ближайшие по карте — Тайвань и Корея. Выберите тот, где задержка World ниже.'],
};
function renderPing() {
  const v = $('#pgW').value, r = PG[v];
  try { if (v) localStorage.setItem('gabella-ping', v); } catch (e) {}
  if (!r) { $('#pgOut').innerHTML = ''; return; }
  $('#pgOut').innerHTML = (r[0] ? `<p class="preg">Ваш регион: ${esc(r[0])}</p>` : '') + '<ul class="verdict">'
    + (r[1] ? `<li>${esc(r[1])}</li>` : '')
    + '<li>Реалмов нет: выбирают регион и режим, а не сервер. Регион выбирают в Battle.net перед запуском игры.</li>'
    + '<li>Персонажи и имена в каждом регионе свои. Играть вместе можно только в одном регионе.</li>'
    + '<li>Где стоят серверы регионов, Blizzard не сообщала.</li></ul>';
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
