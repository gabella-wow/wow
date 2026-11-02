const CLASSES = [
  { id:'warrior', n:'Warrior', s:'Warrior', roles:['tank','dps'],
    specs:[['Arms','Melee damage (two-handed weapon)',['dps']],['Fury','Melee damage (dual wield)',['dps']],['Protection','Tank',['tank']]],
    lvl:'Slowest leveling, about 12% longer than average (LFCarry estimate)',
    lp:12,
    raid:'Battle Shout affects the whole raid',
    forever:'More Rage, better threat on groups of targets, the Weapon Master talent. Fury and Bloodthirst are weakened.' },
  { id:'paladin', n:'Paladin', roles:['tank','heal','dps'],
    specs:[['Holy','Healer',['heal']],['Protection','Tank',['tank']],['Retribution','Melee damage',['dps']]],
    lvl:'Average leveling pace',
    lp:0,
    raid:'Blessing of Kings is now baseline. Per beta lists, Protection is among the strongest tanks, and Retribution dropped after the 15 October patch.',
    forever:'Holy Strike from level 6, Judgement does not consume the seal. Undead can now be paladins, so the class appeared for the Horde.' },
  { id:'hunter', n:'Hunter', roles:['dps'],
    specs:[['Beast Mastery','Ranged damage, a lot of damage from the pet',['dps']],['Marksmanship','Ranged damage',['dps']],['Survival','Melee and ranged, traps',['dps']]],
    lvl:'Fastest leveling, about 8% faster than average (LFCarry estimate)',
    lp:-8,
    raid:'Trueshot Aura affects the whole raid',
    forever:'You can play without a pet, traps work in combat, foxes appeared as a pet family. Survival can go melee.' },
  { id:'rogue', n:'Rogue', roles:['dps'],
    specs:[['Assassination','Poison damage',['dps']],['Combat','Fast weapon attacks',['dps']],['Subtlety','Ambushes, bleeds',['dps']]],
    lvl:'Average leveling pace',
    lp:0,
    raid:'Pure melee damage with no raid-wide buffs',
    forever:'One-handed axes can now be used. Assassination is built on poisons, Subtlety on bleeds and stealth.' },
  { id:'priest', n:'Priest', roles:['heal','dps'],
    specs:[['Discipline','Healer, shields and absorption',['heal']],['Holy','Healer',['heal']],['Shadow','Ranged damage',['dps']]],
    lvl:'About 5% slower than average (LFCarry estimate)',
    lp:5,
    raid:'Divine Spirit is now baseline. Shadow damage and Devouring Plague (24 sec cooldown) were buffed by the 15 October patch.',
    forever:'Fear Ward and Devouring Plague are available from level 20 to any race. Each race has two of its own priest spells.' },
  { id:'shaman', n:'Shaman', roles:['heal','dps','tank?'],
    specs:[['Elemental','Ranged damage',['dps']],['Enhancement','Melee damage. Tanking ability is still in question',['dps','tank?']],['Restoration','Healer',['heal']]],
    lvl:'Average leveling pace',
    lp:0,
    raid:'Strength of Earth, Windfury, Flametongue and Grace of Air totems buff their own party',
    forever:'Dwarves can now be shamans, so the class appeared for the Alliance. Lava Burst was buffed, Elemental rose in the damage rankings.' },
  { id:'mage', n:'Mage', roles:['dps'],
    specs:[['Arcane','Burst, lots of mana',['dps']],['Fire','Crits and ignites',['dps']],['Frost','Damage and control',['dps']]],
    lvl:'Fastest leveling, about 8% faster than average, around 12 hours saved (LFCarry estimate)',
    lp:-8,
    raid:'Portals, food and water for the group',
    forever:'Fire got Hotstreak, Arcane got Arcane Blast, Frost got Ice Lance. Frostfire Bolt is available from level 40.' },
  { id:'warlock', n:'Warlock', roles:['dps'],
    specs:[['Affliction','Damage from curses and corruption',['dps']],['Demonology','Damage through demons',['dps']],['Destruction','Direct fire and shadow damage',['dps']]],
    lvl:'Average leveling pace',
    lp:0,
    raid:'Dark Mastery gives 2–10% shadow damage, same as in Classic (1–5% in the early beta)',
    forever:'Affliction has a new channeled spell, the demon stays with Demonic Sacrifice, Destruction gained Incinerate and AoE.' },
  { id:'druid', n:'Druid', roles:['tank','heal','dps'],
    specs:[['Balance','Ranged damage',['dps']],['Feral','Tank (bear) and melee damage (cat)',['tank','dps']],['Restoration','Healer, lots of healing over time',['heal']]],
    lvl:'About 5% slower than average (LFCarry estimate)',
    lp:5,
    raid:'Leader of the Pack and Moonkin Aura affect the whole raid and stack',
    forever:'Each specialization got a clear role, forms work with potions and weapon enchants. You can be a tank, healer and fighter on one character.' }
];
const ROLE_RU = { tank:'Tank', heal:'Healer', dps:'Damage', 'tank?':'Tank (uncertain)' };
const ri = r => `<svg class="ri" aria-hidden="true"><use href="#i-${r.replace('?','')}"/></svg>`;
const CCOL = { warrior:'#c79c6e', paladin:'#f58cba', hunter:'#abd473', rogue:'#fff569', priest:'#e8e8e8', shaman:'#2f8cf0', mage:'#40c7eb', warlock:'#8788ee', druid:'#ff7d0a' };
const BUFF = { warrior:'Battle Shout', paladin:'Blessing of Kings', hunter:'Trueshot Aura', priest:'Power Word: Fortitude, Divine Spirit', shaman:'Totems (Strength of Earth, Windfury, Flametongue, Grace of Air)', mage:'Arcane Intellect, portals, food and water', druid:'Mark of the Wild, Leader of the Pack, Moonkin Aura' };

const RACES = [
  { id:'human', n:'Human', f:'alliance',
    cls:['warrior','paladin','hunter*','rogue','priest','mage','warlock'],
    rac:[['a','Will to Survive','Removes stun'],['a','Perception','Reveals invisible enemies for 20 sec'],['p','Ruthless','+1% crit chance'],['p','The Human Spirit','+10% spirit']],
    tip:'Spirit goes into healing for a Holy Priest, so a Human priest is good for healing.' },
  { id:'dwarf', n:'Dwarf', f:'alliance',
    cls:['warrior','paladin','hunter','rogue','priest','shaman*'],
    rac:[['a','Stoneform','Immunity to bleeds, poisons and diseases for 8 sec and reduced physical damage'],['a','Find Treasure','Shows nearby chests and gives a chance at extra items in most chests'],['p','Artisan’s Precision','+1% hit chance with spells and attacks'],['p','Big Game Hunter','+5% damage to beasts']],
    tip:'Stoneform is useful for tanks and in PvP.' },
  { id:'nightelf', n:'Night Elf', f:'alliance',
    cls:['warrior','hunter','rogue','priest','druid'],
    rac:[['a','Elune’s Light','+10% crit chance for 15 sec'],['a','Shadowmeld','Invisibility on the spot'],['p','Quickness','+2% dodge and run speed (Warcraft Tavern gives 1% dodge) {beta}'],['p','Wisp Spirit','+75% run speed as a spirit (Warcraft Tavern says 25%) {beta}']],
    tip:'The only Alliance race with a druid, unless you take Skyborne.' },
  { id:'gnome', n:'Gnome', f:'alliance',
    cls:['warrior','rogue','mage','warlock','priest*'],
    rac:[['a','Escape Artist','Brief immunity to slows and roots'],['a','Eureka!','For 8 sec, abilities cost less and are 10% stronger {beta}'],['p','Expansive Mind','+5% maximum mana, rage or energy'],['p','Engineering Specialization','Engineering devices work more reliably']],
    tip:'Expansive Mind especially helps energy classes.' },
  { id:'skyA', n:'Skyborne (Alliance)', f:'alliance', paid:true, name:'High Order Skyborne',
    cls:['warrior','hunter','rogue','mage','druid'],
    rac:[['a','Walk on Air','Glide down for 10 sec, no fall damage'],['a','Read Ley Line','Health and mana regeneration +50% for 15 sec. At a Ley Line you also get Attuned for 1 hour: +100%, kept through death'],['p','Wind Blessed','+2% attack and spell speed'],['p','Elemental Insight','+5% damage to elementals']],
    tip:'Paid race: Heroic Pack from $29.99. Starts in the Zephras Isle location (levels 1–12).' },
  { id:'orc', n:'Orc', f:'horde',
    cls:['warrior','hunter','rogue','shaman','warlock','mage*'],
    rac:[['a','Blood Fury','+10% attack power and spell power for 15 sec'],['a','Shatter Curse','Removes curses and corruption, −5% magic damage taken for 8 sec'],['p','Command','+5% Warlock and Hunter pet damage'],['p','Hardiness','Stuns are 20% shorter']],
    tip:'Blood Fury gives a powerful damage window.' },
  { id:'undead', n:'Undead', f:'horde',
    cls:['warrior','rogue','mage','priest','warlock','paladin*'],
    rac:[['a','Will of the Forsaken','Removes charm, fear and sleep'],['a','Cannibalize','Restores 35% health and mana over time'],['p','Underwater Breathing','Breathe underwater longer'],['p','Touch of the Grave','Chance to drain health on attack']],
    tip:'New combination: a paladin for the Horde, where this class did not exist before.' },
  { id:'tauren', n:'Tauren', f:'horde',
    cls:['warrior','hunter','shaman','druid'],
    rac:[['a','War Stomp','Stuns nearby enemies for 2 sec, 90 sec cooldown'],['a','Cultivation','Grows herbs that can be gathered without Herbalism, 15 min cooldown'],['p','Plainsrunning','While you keep moving, run speed grows by 2% per stack, up to +60%. Does not affect mounted speed'],['p','Endurance','+5% health']],
    tip:'The only Horde race with a druid, unless you take Skyborne.' },
  { id:'troll', n:'Troll', f:'horde',
    cls:['warrior','hunter','rogue','priest','shaman','mage','warlock*'],
    rac:[['a','Berserking','+10% attack and spell speed for 12 sec, 3 min cooldown'],['a','Rapid Regeneration','Restores health over time'],['p','Beast Slaying','+5% damage to beasts'],['p','Regeneration','Health regenerates in combat too']],
    tip:'The most class options in the Horde: seven.' },
  { id:'skyH', n:'Skyborne (Horde)', f:'horde', paid:true, name:'Windshaper Skyborne',
    cls:['warrior','hunter','rogue','shaman','druid'],
    rac:[['a','Walk on Air','Glide down for 10 sec, no fall damage'],['a','Skysight','+15% run speed for 15 sec. At an Elemental Convergence you also get Charged for 1 hour: +30%, kept through death'],['p','Wind Blessed','+2% attack and spell speed'],['p','Elemental Insight','+5% damage to elementals']],
    tip:'Paid race: Heroic Pack from $29.99. Only the Horde can have a shaman, only the Alliance a mage.' }
];
RACES.forEach(r => { r.can = {}; r.cls.forEach(c => { const isNew = c.endsWith('*'); r.can[isNew ? c.slice(0,-1) : c] = isNew ? 'new' : 'ok'; }); });
const CL = Object.fromEntries(CLASSES.map(c => [c.id, c]));
const BETA = '<span class="beta-note">per beta data</span>';
const BMARK = '{' + 'beta}';   // split so the guide build (which swaps the marker for the span everywhere) leaves it alone
const racx = s => String(s).split(BETA).join(BMARK).split(BMARK).map(esc).join(BETA);
const RC = Object.fromEntries(RACES.map(r => [r.id, r]));
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
const CX = {"warrior": {"armor": "Cloth, leather, mail; plate from level 40 {beta}", "weapons": "Everything except wands; shield", "resource": "Rage", "lvl": "Slowest leveling, about 12% longer than average (LFCarry estimate)", "group": ["Battle Shout affects the whole raid", "Demoralizing Shout and Sunder Armor on the boss", "Sweeping Strikes and Whirlwind for multi-target fights"], "pros": ["Best tank and strong melee damage", "Good for PvP (Arms)", "Few buttons, easy to understand"], "cons": ["Slowest leveling", "Heavily gear dependent", "Almost no self-healing or crowd control"], "specs": [{"n": "Arms", "what": "Melee damage (two-handed weapon)"}, {"n": "Fury", "what": "Melee damage (dual wield)"}, {"n": "Protection", "what": "Tank"}]}, "paladin": {"armor": "Cloth, leather, mail; plate from level 40; shield {beta}", "weapons": "Axes, maces, swords, polearms from level 20 {beta}", "resource": "Mana", "lvl": "Average leveling pace", "group": ["Party auras: Devotion, Retribution, Concentration", "Fire, Frost and Shadow resistance auras for the whole raid", "One-hour blessings, greater blessings for a whole class", "Seal of Justice stops enemies from fleeing"], "pros": ["All three roles on one character", "Strong group buffs", "Plate and a sturdy character"], "cons": ["No gap closer, slow or speed boost", "Little crowd control beyond Hammer of Justice", "Retribution dropped after the patch"], "specs": [{"n": "Holy", "what": "Healer"}, {"n": "Protection", "what": "Tank"}, {"n": "Retribution", "what": "Melee damage"}]}, "hunter": {"armor": "Cloth, leather; mail from level 40 {beta}", "weapons": "Bows, crossbows, guns, axes, swords, polearms", "resource": "Mana; the pet uses Focus", "lvl": "Fastest leveling, about 8% faster than average (LFCarry estimate)", "group": ["Trueshot Aura boosts the group ranged damage", "Freezing Trap: reliable crowd control", "Scatter Shot interrupts casts", "Aspect of the Pack speeds up the whole group on the road"], "pros": ["Fastest leveling", "Great solo", "Traps and crowd control"], "cons": ["Close-range deadzone up to 8 yards", "You have to manage the pet", "Survival talents were buggy on the beta"], "specs": [{"n": "Beast Mastery", "what": "Ranged damage, a lot of damage from the pet"}, {"n": "Marksmanship", "what": "Ranged damage"}, {"n": "Survival", "what": "Melee and ranged, traps"}]}, "rogue": {"armor": "Cloth, leather", "weapons": "Daggers, swords, maces, fist weapons, one-handed axes, thrown", "resource": "Energy and combo points", "lvl": "Average leveling pace", "group": ["Pure melee damage with no raid-wide buffs", "Sap, Blind and Kidney Shot: lots of crowd control", "Kick interrupts dangerous casts"], "pros": ["Very high damage that scales with gear", "Stealth and lots of crowd control", "Freedom of weapon choice"], "cons": ["Heavily gear dependent", "No self-healing", "Only Evasion and Vanish save you"], "specs": [{"n": "Assassination", "what": "Poison damage"}, {"n": "Combat", "what": "Fast weapon attacks"}, {"n": "Subtlety", "what": "Ambushes, bleeds"}]}, "priest": {"armor": "Cloth", "weapons": "Daggers, maces, staves, wands", "resource": "Mana", "lvl": "About 5% slower than average (LFCarry estimate)", "group": ["Divine Spirit and Power Word: Fortitude for the whole raid", "Power Infusion empowers an ally", "The group main healer"], "pros": ["Always needed by a group", "Healing or shadow damage", "Many builds"], "cons": ["Cloth only, fragile", "Few ways to move fast", "Haste barely helps spells"], "specs": [{"n": "Discipline", "what": "Healer, shields and absorption"}, {"n": "Holy", "what": "Healer"}, {"n": "Shadow", "what": "Ranged damage"}]}, "shaman": {"armor": "Cloth, leather; mail from level 40; shield {beta}", "weapons": "Maces, axes, staves, fist weapons, daggers", "resource": "Mana", "lvl": "Average leveling pace", "group": ["Strength of Earth, Windfury, Flametongue and Grace of Air totems buff their own party", "Tremor Totem removes fear, sleep and charm", "Poison and disease cleansing totems", "Purge removes buffs from enemies"], "pros": ["Strong totems for the group", "Mobile leveling", "Strong new talents"], "cons": ["No hard crowd control", "Mana in long fights", "Tanking still unconfirmed"], "specs": [{"n": "Elemental", "what": "Ranged damage"}, {"n": "Enhancement", "what": "Melee damage. Tanking ability is still in question"}, {"n": "Restoration", "what": "Healer"}]}, "mage": {"armor": "Cloth", "weapons": "Daggers, swords, staves, wands", "resource": "Mana", "lvl": "Fastest leveling, about 8% faster than average, around 12 hours saved (LFCarry estimate)", "group": ["Portals from level 40, teleports from 20", "Food and water for the group", "Polymorph: reliable crowd control", "Remove Lesser Curse"], "pros": ["Fastest leveling", "Portals and food for everyone", "Three strong and different trees"], "cons": ["Cloth only, fragile", "Mana runs out fast", "Area damage toned down"], "specs": [{"n": "Arcane", "what": "Burst, lots of mana"}, {"n": "Fire", "what": "Crits and ignites"}, {"n": "Frost", "what": "Damage and control"}]}, "warlock": {"armor": "Cloth", "weapons": "Daggers, swords, staves, wands", "resource": "Mana; Life Tap turns health into mana", "lvl": "Average leveling pace", "group": ["Healthstone and Soulstone", "Ritual of Summoning: gathers the group", "Curse of Tongues slows casting by 60%", "Curse of the Elements: more magic damage on the target"], "pros": ["Self-sufficient: a demon and Life Tap", "Lots of group utility", "Strong damage over time"], "cons": ["Fragile and immobile", "Damage takes time to ramp up", "No blink or sprint"], "specs": [{"n": "Affliction", "what": "Damage from curses and corruption"}, {"n": "Demonology", "what": "Damage through demons"}, {"n": "Destruction", "what": "Direct fire and shadow damage"}]}, "druid": {"armor": "Cloth, leather", "weapons": "Daggers, maces, staves, fist weapons, polearms from level 20 {beta}", "resource": "Mana; Rage in Bear Form, Energy in Cat Form", "lvl": "About 5% slower than average (LFCarry estimate)", "group": ["Leader of the Pack and Moonkin Aura affect the whole raid and stack", "Rebirth: combat resurrection", "Innervate returns mana to a healer", "Removes curses and poisons"], "pros": ["All three roles on one character", "Great mobility", "Combat resurrection"], "cons": ["No block or parry for the bear", "Heal over time effects are harder to track", "Final raid numbers are still unknown"], "specs": [{"n": "Balance", "what": "Ranged damage"}, {"n": "Feral", "what": "Tank (bear) and melee damage (cat)"}, {"n": "Restoration", "what": "Healer, lots of healing over time"}]}};
const HC = {"tx":{"title":"My character","lead":"No login, no password: pick a class, spec and race, and the site adjusts to you.","local":"Saved in this browser only.","none":"No character yet","create":"Create a character","edit":"Edit","reset":"Delete character","resetQ":"Delete the character from this browser?","steps":["Side","Class and spec","Race","Look","Details"],"side":"Who do you play for?","cls":"Class","spec":"Spec","race":"Race","bestFor":"Best race for %s","best":"best","paid":"paid","sex":"Sex","m":"Male","f":"Female","bg":"Portrait background","lvl":"Level","reg":"Region","lvlReg":"Level and region","regs":{"us":"Americas and Oceania","eu":"Europe","kr":"Korea","tw":"Taiwan"},"p1":"Profession 1","p2":"Profession 2","secP":"Secondary professions","noP":"None","role":"Role","back":"Back","next":"Continue","done":"Done","cancel":"Cancel","later":"You can fill this in later.","levelN":"Level %n","build":"My talent build","buildD":"%s talents by level.","pairs":"Profession pairs","pairsD":"Which professions suit your class.","bestR":"Best races","bestRD":"Race for your class on both factions.","lvlG":"Class leveling","lvlGD":"Route and talents 1–60.","day1":"Day 1 for your character","day1D":"The launch checklist with your class and race.","play":"In game","playD":"Zones and dungeons for your level, timers, radio.","dung":"Dungeons for your level","dungNo":"Set your level and we will pick dungeons.","dungFirst":"The first dungeons open at level 13.","resetH":"Weekly reset","resetIn":"in %s","resetNote":"Blizzard has not announced the Forever reset time yet. Shown as in other WoW versions of this region: we will check at launch.","resetUnk":"We will confirm the reset time for this region at launch.","resetNoReg":"Set your region to see the weekly reset.","resetWhy":"Raids open on Dec 9 and have a weekly lockout.","lfg":"Looking for group text","lfgD":"Paste it into the LookingForGroup chat. Names as in the game.","lfgP":{"tank":"%c tank LFG","heal":"%c healer LFG","dps":"%c DPS LFG"},"lfgT":"%p: %d, level %l.","lfgT0":"%p.","allD":"All dungeons","copy":"Copy","copied":"Copied","sync":"Sync across devices","syncD":"You only need to log in for this: the character will be on your phone and PC, and the launch letter comes by email if you subscribe.","yourCls":"Your %s","bTalents":"Talents","bSpec":"Build: %s","bLevel":"Leveling","bGroup":"Group","bNews":"News","copiedT":"Copied: %s","profsL":"Professions","day1n":"Day 1: %n of %t","collect":"Build a character","collectD":"Class, spec and race: talents, leveling, group and news for your class.","change":"Change","allSet":"All settings","close":"Close","mine":"About your class","share":"Share","linkCopied":"Link copied","make":"Make it my character","made":"This is your character","plaqueH":"My character","plaqueD":"Class, spec and race in a minute, then your build, professions and dungeons.","day1Mine":"For your character","ckClass":"Your spec, %s: the talent build by level.","ckRaceOk":"%r is the best race for your spec.","ckRaceAlt":"Best race for your spec: %r.","ckProfs":"Profession pairs for %s.","ckStart":"%s leveling: route and first talents.","ckPing":"Your region: %s.","or":"or"},"best":{"warrior":{"alliance":{"*":[["human","nightelf"],"Human: +1% crit with any weapon. Night Elf: +10% crit for 15 sec. The sources are almost evenly split."],"protection":[["dwarf"],"Stoneform cuts physical damage by 10% and removes bleeds."]},"horde":{"*":[["orc"],"Blood Fury: +10% attack power for 15 sec. Before the Oct 26 racial changes every source put it first."],"protection":[["tauren"],"Endurance gives +5% health, War Stomp stuns nearby enemies."]}},"paladin":{"alliance":{"*":[["human"],"Ruthless boosts both strikes and spells, Will to Survive removes stuns."],"protection":[["dwarf"],"Stoneform and Artisan’s Precision: +1% hit chance."]},"horde":{"*":[["undead"],"On the Horde only Undead can be a Paladin. Cannibalize restores mana, Will of the Forsaken removes fear."]}},"hunter":{"alliance":{"*":[["human","nightelf"],"Human: +1% crit, and the pet inherits crit. Night Elf: Elune’s Light and Shadowmeld."]},"horde":{"*":[["orc","troll"],"Orc: Blood Fury and Command (+5% pet damage). Troll: +5% damage against beasts."]}},"rogue":{"alliance":{"*":[["nightelf"],"Shadowmeld now drops threat in combat too, plus Elune’s Grace and Quickness."]},"horde":{"*":[["orc"],"Blood Fury: +10% attack power for 15 sec."]}},"priest":{"alliance":{"*":[["gnome"],"Every source picks it: Eureka! also boosts Power Word: Shield, Inquisitive Mind gives +5% mana."]},"horde":{"*":[["undead","troll"],"The sources are split. Undead is stronger in PvP: Will of the Forsaken removes fear, sleep and charm."]}},"shaman":{"alliance":{"*":[["dwarf"],"On the Alliance only Dwarf can be a Shaman: Stoneform and Artisan’s Precision (+1% hit chance)."]},"horde":{"*":[["orc"],"Blood Fury gives both attack power and spell power: good for Elemental and Enhancement alike."],"restoration":[["troll"],"For a healer a source recommends Troll: Berserking, +10% casting speed for 12 sec."]}},"mage":{"alliance":{"*":[["gnome"],"Eureka! for 8 sec, Inquisitive Mind: +5% mana, Escape Artist breaks roots."]},"horde":{"*":[["orc"],"Orc Mage is a new Forever combination: Blood Fury now gives spell power."]}},"warlock":{"alliance":{"*":[["gnome","human"],"Gnome: Eureka! and Inquisitive Mind. Human: damage over time can crit, and Ruthless gives +1% crit."]},"horde":{"*":[["orc","undead"],"Orc: Blood Fury gives spell power. Undead is picked more often for PvP."]}},"druid":{"alliance":{"*":[["nightelf"],"Elune’s Grace: +10% crit for 15 sec, and Quickness."]},"horde":{"*":[["tauren"],"Endurance: +5% health, War Stomp works in forms too."]}}},"sid":{"warrior":["arms","fury","protection"],"paladin":["holy","protection","retribution"],"hunter":["beast-mastery","marksmanship","survival"],"rogue":["assassination","combat","subtlety"],"priest":["discipline","holy","shadow"],"shaman":["elemental","enhancement","restoration"],"mage":["arcane","fire","frost"],"warlock":["affliction","demonology","destruction"],"druid":["balance","feral","restoration"]},"sn":{"warrior":["Arms","Fury","Protection"],"paladin":["Holy","Protection","Retribution"],"hunter":["Beast Mastery","Marksmanship","Survival"],"rogue":["Assassination","Combat","Subtlety"],"priest":["Discipline","Holy","Shadow"],"shaman":["Elemental","Enhancement","Restoration"],"mage":["Arcane","Fire","Frost"],"warlock":["Affliction","Demonology","Destruction"],"druid":["Balance","Feral","Restoration"]},"fn":{"alliance":"Alliance","horde":"Horde"},"reset":{"us":[2,15],"eu":[3,4],"kr":null,"tw":null},"rn":{"human":"Human","dwarf":"Dwarf","nightelf":"Night Elf","gnome":"Gnome","skyA":"High Order Skyborne","orc":"Orc","undead":"Undead","tauren":"Tauren","troll":"Troll","skyH":"Windshaper Skyborne"},"rf":{"human":"alliance","dwarf":"alliance","nightelf":"alliance","gnome":"alliance","skyA":"alliance","orc":"horde","undead":"horde","tauren":"horde","troll":"horde","skyH":"horde"},"cn":{"warrior":"Warrior","paladin":"Paladin","hunter":"Hunter","rogue":"Rogue","priest":"Priest","shaman":"Shaman","mage":"Mage","warlock":"Warlock","druid":"Druid"},"cen":{"warrior":"Warrior","paladin":"Paladin","hunter":"Hunter","rogue":"Rogue","priest":"Priest","shaman":"Shaman","mage":"Mage","warlock":"Warlock","druid":"Druid"}};
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

const CPROF = {"warrior": [["Leveling: Blacksmithing + Mining", ""], ["Level 60: Engineering + Mining", "A blacksmith dresses in plate and weapons, and many recipes are personal. An engineer gets the grenades and devices a warrior lacks."]], "paladin": [["Leveling: Blacksmithing + Mining", ""], ["Level 60: Protection, Retribution: Engineering + Mining. Holy: Alchemy + Herbalism", "Holy burns a lot of mana: you make your own potions, and the Mana Well in camp replaces Blessing of Wisdom."]], "hunter": [["Leveling: Leatherworking + Skinning", ""], ["Level 60: Engineering + Mining", "A leatherworker makes their own leather and mail and Armor Kits. An engineer makes scopes and guns."]], "rogue": [["Leveling: Leatherworking + Skinning", ""], ["Level 60: Engineering + Mining", "You make your own leather, and the Camp Tent gives rest. Engineering is the main profession for PvP."]], "priest": [["Leveling: Tailoring + Enchanting", ""], ["Level 60: Tailoring + Engineering or Enchanting", "A tailor makes belts with spell power from level 10, an enchanter makes wands with spell power from level 5. Tailored items get disenchanted into materials."]], "shaman": [["Leveling: Leatherworking + Skinning", ""], ["Level 60: Alchemy + Herbalism", "A leatherworker makes spell power gear for Elemental and Restoration and gear for Enhancement. Raids and groups need potions."]], "mage": [["Leveling: Tailoring + Enchanting", ""], ["Level 60: Tailoring + Enchanting; for PvP and big pulls Engineering + Mining", "A tailor provides early spell power gear, and tailored items get disenchanted. An engineer’s grenades hold big groups of enemies in place."]], "warlock": [["Leveling: Tailoring + Enchanting", ""], ["Level 60: Tailoring + Alchemy", "A tailor’s Faction Banner gives Spirit for Life Tap. Alchemy means potions and gold."]], "druid": [["Leveling: Leatherworking + Skinning or Herbalism", ""], ["Level 60: Alchemy + Herbalism", "You gather herbs in Travel Form and drink potions in any form. Mana Well and Incense Candle help Balance and Restoration."]]};   /* recommended profession pairs per class, already in the page language (build.class_profs) */
const $ = s => document.querySelector(s);
const ROOT = '../../', HOME = '../';
function esc(s) { return String(s).replace(/[&<>"]/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m])); }
function raceName(r) { return r.name || r.n; }
function syncSeg(id, v) { document.querySelectorAll(`#${id} button`).forEach(b => b.setAttribute('aria-pressed', b.dataset.v === String(v))); }
const FAC = { alliance: 'Alliance', horde: 'Horde' };
const BSLUG = { skyA: 'skyborne-a', skyH: 'skyborne-h' };   // race id -> url part of the share page (tools/make_build_cards.py SLUG)
const RSLUG = { human: 'human', dwarf: 'dwarf', nightelf: 'night-elf', gnome: 'gnome', skyA: 'skyborne-alliance', orc: 'orc', undead: 'undead', tauren: 'tauren', troll: 'troll', skyH: 'skyborne-horde' };
const PAINTED = ["druid-nightelf", "druid-tauren", "hunter-nightelf", "hunter-orc", "mage-gnome", "mage-orc", "paladin-human", "paladin-undead", "priest-gnome", "priest-undead", "rogue-nightelf", "rogue-orc", "shaman-dwarf", "shaman-orc", "warlock-gnome", "warlock-orc", "warrior-human", "warrior-orc"];   // class x race paintings that exist (build_tools.painted): the player's own race is drawn, never the best race of the side
const unitArt = (p, ext) => `${ROOT}assets/art/${PAINTED.includes(p.cls + '-' + p.race) ? p.cls + '-' + p.race : RSLUG[p.race]}-360.${ext}${PV}`;
const classUrl = id => `${HOME}classes/${id}/`, raceUrl = id => `${HOME}races/${RSLUG[id]}/`;
const PV = /*PV*/'?v=03c9d4a0';   // ?v= of the class and race portraits (build.art_version)
const porId = (id, f) => (window.GabellaPor ? GabellaPor.id(id, f) : id);   // a class: the portrait of side f, else of the reader's side (build.por_js)
const art = (id, ext = 'webp', f) => `${ROOT}assets/art/${porId(id, f)}-360.${ext}${PV}`;
async function copyTo(text, msgEl, ok) {
  try { await navigator.clipboard.writeText(text); msgEl.textContent = ok; } catch (e) { msgEl.textContent = 'Could not copy, select the text and press Ctrl+C'; }
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
    out.push((groups > 1 ? `Group ${g + 1}: ` : '') + part.map(p => `${p.name ? p.name + ' — ' : ''}${raceName(RC[p.race])} ${CL[p.cls].n} (${ROLE_RU[p.role]})`).join(', '));
  }
  return out.length ? out.join('\n') + `\n${FAC[R.f]}, ${R.size}` : '';
}

/* LFG line: the dungeon or raid, the missing roles, the play style and a short link (#t=); kept under the 255-byte chat limit */
const LFG = {"d": [["Ragefire Chasm", 13, 18, "horde"], ["Hall of Thanes", 13, 18, 0], ["Ruins of Lordaeron", 15, 20, 0], ["The Deadmines", 15, 22, 0], ["Wailing Caverns", 17, 24, 0], ["Shadowfang Keep", 20, 26, 0], ["Blackfathom Deeps", 22, 28, 0], ["The Stockade", 25, 29, "alliance"], ["Excavation Site: Wetlands", 26, 31, 0], ["City of Dalaran", 28, 33, 0], ["Gnomeregan", 29, 38, 0], ["Razorfen Kraul", 29, 38, 0], ["Scarlet Monastery: Graveyard", 30, 38, 0], ["Scarlet Monastery: Library", 33, 41, 0], ["The Drowned City", 35, 40, 0], ["Scarlet Monastery: Armory", 36, 44, 0], ["Uldaman", 36, 45, 0], ["Razorfen Downs", 37, 46, 0], ["Scarlet Monastery: Cathedral", 38, 46, 0], ["Zul'Farrak", 40, 47, 0], ["Krol'dok Stronghold", 40, 45, 0], ["Maraudon", 45, 51, 0], ["Alcaz Island Prison", 48, 53, 0], ["Temple of Atal'Hakkar", 50, 55, 0], ["Blackrock Depths", 52, 60, 0], ["Blackmaw Hold", 55, 60, 0], ["Lower Blackrock Spire", 57, 60, 0], ["Dire Maul: East", 58, 60, 0], ["Shaper's Terrace", 58, 60, 0], ["Stratholme: Living", 58, 60, 0], ["Stratholme: Undead", 58, 60, 0], ["Scholomance", 58, 60, 0], ["Upper Blackrock Spire", 60, 60, 0], ["Dire Maul: West", 60, 60, 0], ["Dire Maul: North", 60, 60, 0]], "r": {"10": "Barrow Deeps", "20": "Hyjal Summit", "40": "Onyxia’s Lair"}};   // dungeons [name, min, max, entrance faction] and raids {size: name} in the client's language (build_tools)
const CHAT_MAX = 255, CANON = 'https://gabella.site/wow/en/tools/'.replace(/^https?:\/\//, '');
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
  const head = (L.d ? 'LFM %d: %n.' : 'LFM: %n.').replace('%d', L.d).replace('%n', roles);
  const parts = [head, L.s ? 'Style: %s.'.replace('%s', L.s) : '', CANON + shortHash()].filter(Boolean);
  const bytes = t => new TextEncoder().encode(t).length;
  let text = parts.join(' ');
  if (bytes(text) > CHAT_MAX) text = parts.slice(0, -1).join(' ');   // a long raid code would not fit: the link goes first
  return text;
}
function renderLfg() {
  const places = lfgPlaces(), sel = $('#lfgD');
  if (!places.some(p => p[0] === L.d)) L.d = R.size === 5 ? '' : (places[0] || [''])[0];
  $('#lfgDL').textContent = R.size === 5 ? 'Dungeon' : 'Raid';
  sel.innerHTML = (R.size === 5 ? '<option value="">Any dungeon</option>' : '') + places.map(([v, t]) => `<option value="${esc(v)}"${v === L.d ? ' selected' : ''}>${esc(t)}</option>`).join('');
  syncSeg('lfgS', L.s);
  const text = lfgText();
  $('#rLfg').value = text;
  $('#rCopyLfg').disabled = !text;
  $('#rLfgMsg').textContent = text ? lfgLen(text) : R.s.some(Boolean) ? 'All places are taken.' : 'Add at least one player to the group.';
}
function lfgLen(t) { return 'Characters: %n of %m (the chat line limit).'.replace('%n', t.length).replace('%m', CHAT_MAX); }

function unitHTML(p, i) {
  const cls = R.moving === i ? ' src' : '';
  if (!p) return `<button type="button" class="unit empty${cls}" data-i="${i}"><span class="up" aria-hidden="true">+</span><span class="ub"><b>Free slot</b><span>Click to add a player</span></span></button>`;
  const c = CL[p.cls], r = RC[p.race];
  return `<button type="button" class="unit${cls}" data-i="${i}" draggable="true" style="--cc:${CCOL[p.cls]};--pc:${power(p)}" aria-label="${esc((p.name || `Player ${i + 1}`) + ', ' + raceName(r) + ' ' + c.n + ', ' + ROLE_RU[p.role])}">
    <span class="up"><picture><source type="image/avif" srcset="${unitArt(p, 'avif')}"><img src="${unitArt(p, 'webp')}" width="360" height="482" alt="" loading="lazy" decoding="async"></picture></span>
    <span class="ub"><span class="un"><span class="ur" title="${ROLE_RU[p.role]}">${ri(p.role)}</span><b>${esc(p.name || c.n)}</b><small>${esc(raceName(r))} · ${esc(c.n)}</small></span><span class="hp"><i></i></span><span class="mp"></span></span></button>`;
}
function cellHTML(p, i) {
  const cls = R.moving === i ? ' src' : '';
  if (!p) return `<button type="button" class="rc empty${cls}" data-i="${i}" aria-label="Free slot ${i + 1}"><span aria-hidden="true">+</span>Add</button>`;
  const c = CL[p.cls], r = RC[p.race];
  return `<button type="button" class="rc${cls}" data-i="${i}" draggable="true" style="--cc:${CCOL[p.cls]};--pc:${power(p)}" aria-label="${esc((p.name || `Player ${i + 1}`) + ', ' + raceName(r) + ' ' + c.n + ', ' + ROLE_RU[p.role])}" title="${esc(raceName(r) + ' · ' + c.n + ' · ' + ROLE_RU[p.role])}"><b>${esc(p.name || c.n)}</b><small>${esc(p.name ? c.n : raceName(r))}</small>${ri(p.role)}</button>`;
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
      const st = n && (!c.tank || !c.heal) ? `<span class="warn">${!c.tank ? 'no tank' : 'no healer'}</span>` : `<span>${n}/5</span>`;
      h += `<div class="rg"><div class="rg-h"><b>Group ${g + 1}</b>${st}</div>${part.map((p, k) => cellHTML(p, g * PARTY + k)).join('')}</div>`;
    }
    $('#rview').innerHTML = `<div class="rgrid" style="--gc:${Math.min(groups, 8)}">${h}</div>`;
  }
  const hint = $('#rhint');
  hint.classList.toggle('on', R.moving >= 0);
  hint.innerHTML = R.moving >= 0 ? `Pick a new slot for player ${R.moving + 1}. <button type="button" id="mvCancel">Cancel</button>` : '';

  const list = R.s.filter(Boolean), cnt = countRoles(list), rec = REC[R.size];
  $('#rRoles').innerHTML = RR.map((x, k) => `<span class="${list.length && cnt[x] < rec[k] ? 'low' : ''}">${ri(x)}${ROLE_RU[x]} <b>${cnt[x]}</b> / ${rec[k]}</span>`).join('');
  $('#rTip').textContent = R.size === 5 ? 'A dungeon needs a tank, a healer and three damage dealers.' : `Raid rule of thumb: tanks ${rec[0]}, healers ${rec[1]}, the rest damage. The exact number depends on the bosses.`;
  const have = new Set(list.map(p => p.cls));
  $('#rBuffs').innerHTML = CLASSES.filter(c => BUFF[c.id]).map(c => `<li class="${have.has(c.id) ? '' : 'off'}" style="--cc:${CCOL[c.id]}"><span class="cdot"></span><span><b>${esc(c.n)}:</b> ${esc(BUFF[c.id])}</span></li>`).join('');
  const n = list.length;
  $('#rRaids').innerHTML = n ? RAIDS.map(([size, name]) => `<li class="${n >= size ? 'good' : ''}">${n >= size ? `Raid for ${size} (${name}): enough players.` : `Raid for ${size} (${name}): short by ${size - n}.`}</li>`).join('') : '<li>Nobody here yet. Press “My character”, “Fill empty” or an empty frame.</li>';

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
function myHero() {   // the hero of this browser (assets/hero/hero.js?v=ddf7d65dcc, localStorage gabella-wf-me)
  let h = null; try { h = JSON.parse(localStorage.getItem('gabella-wf-me')); } catch (e) {}
  return h && RC[h.race] && CL[h.cls] && RC[h.race].can[h.cls] ? h : null;
}
$('#rMine').onclick = () => {
  const h = myHero(), msg = $('#rMy');
  if (!h) {
    msg.innerHTML = 'No character yet. <a href="../character/" id="rMake">Build a character</a>';
    $('#rMake').onclick = e => { if (window.GabellaHero) { e.preventDefault(); GabellaHero.open(); } };
    return;
  }
  const f = RC[h.race].f, role = RR.includes(h.role) ? h.role : roleOpts(CL[h.cls])[0];
  if (f !== R.f) {
    if (R.s.some(Boolean)) { msg.textContent = 'Your character is on the other faction: switch the faction above the frames.'; return; }
    R.f = f;
  }
  if (R.s.some(p => p && p.race === h.race && p.cls === h.cls && p.role === role && !p.name)) { msg.textContent = 'Your character is already in the roster.'; return; }
  let i = R.s.findIndex(p => !p); if (i < 0) i = 0;
  R.s[i] = { race: h.race, cls: h.cls, role, name: '' };
  msg.textContent = ''; R.moving = -1; renderRaid();
};
$('#rClear').onclick = () => { R.s = Array(R.size).fill(null); R.moving = -1; renderRaid(); };
$('#rCopyLink').onclick = () => copyTo(teamLink(), $('#rMsg'), 'Link copied');
$('#rCopyText').onclick = () => copyTo(teamText(), $('#rMsg'), 'Group copied');
$('#lfgD').onchange = e => { L.d = e.target.value; renderLfg(); };
$('#lfgS').addEventListener('click', e => { const b = e.target.closest('button'); if (b) { L.s = L.s === b.dataset.v ? '' : b.dataset.v; renderLfg(); } });
$('#rCopyLfg').onclick = () => { const t = lfgText(); copyTo(t, $('#rLfgMsg'), 'Text copied. ' + lfgLen(t)); };

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
  $('#edT').textContent = `Player ${edI + 1}` + (R.size > 5 ? ` · Group ${Math.floor(edI / PARTY) + 1}` : '');
  $('#edRace').innerHTML = RACES.filter(r => r.f === R.f).map(r => `<option value="${r.id}"${r.id === p.race ? ' selected' : ''}>${esc(raceName(r))}${r.paid ? ' (paid)' : ''}</option>`).join('');
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
  else box.innerHTML = ['alliance', 'horde'].map(f => `<div class="rside ${f}"><h3>${FAC[f]}</h3>${RACES.filter(r => r.f === f).map(r => { const k = sel.indexOf(r.id); return `<button type="button" class="rp" data-id="${r.id}" aria-pressed="${k >= 0}">${esc(raceName(r))}${r.paid ? '<span class="tag paid">paid</span>' : ''}<span class="no">${k + 1}</span></button>`; }).join('')}</div>`).join('');
  $('#cNote').textContent = `Selected ${sel.length} of 3`;
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
const ul = (items, cls) => items.length ? `<ul${cls ? ` class="${cls}"` : ''}>${items.map(x => `<li>${x}</li>`).join('')}</ul>` : '<span class="none">None</span>';
const row = (lab, vals, extra) => `<div class="crow${extra ? ' ' + extra : ''}"><div class="lab${extra === 'tiprow' ? ' tl' : ''}">${lab}</div>${vals.map(v => `<div class="val">${v}</div>`).join('')}</div>`;
function renderCmp() {
  const out = [];
  if (C.mode === 'class') {
    const ids = C.cls;
    out.push(`<div class="crow chead"><div class="lab"></div>${ids.map(id => `<div class="val" style="--cc:${CCOL[id]}"><picture><source type="image/avif" srcset="${art(id, 'avif')}"><img src="${art(id)}" width="360" height="482" alt="" loading="lazy" decoding="async"></picture><b>${esc(CL[id].n)}</b><a href="${classUrl(id)}">Class page<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>`).join('')}</div>`);
    out.push(row('Roles', ids.map(id => CL[id].roles.map(r => `<span class="role">${ri(r)}${ROLE_RU[r]}</span>`).join(''))));
    out.push(row('Armor', ids.map(id => racx(CX[id].armor))));
    out.push(row('Weapons', ids.map(id => racx(CX[id].weapons))));
    out.push(row('Resource', ids.map(id => esc(CX[id].resource))));
    out.push(row('Leveling', ids.map(id => esc(CX[id].lvl))));
    out.push(row('Specializations', ids.map(id => ul(CX[id].specs.map(s => `<b>${esc(s.n)}</b>${SPEC_SEP}<span class="sub">${esc(s.what)}</span>`)))));
    out.push(row('Raid buff', ids.map(id => BUFF[id] ? esc(BUFF[id]) : '<span class="none">None</span>')));
    out.push(row('In a group', ids.map(id => ul(CX[id].group.map(esc)))));
    out.push(row('Professions', ids.map(id => ul(CPROF[id].map(p => `<b>${esc(p[0])}</b>${p[1] ? `<br><span class="sub">${esc(p[1])}</span>` : ''}`)) + `<a class="cgo" href="${HOME}guides/professions/#pairs=${id}">Camp objects and leveling<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a>`)));
    out.push(row('Strengths', ids.map(id => ul(CX[id].pros.map(esc), 'plus'))));
    out.push(row('Weaknesses', ids.map(id => ul(CX[id].cons.map(esc), 'minus'))));
    ['alliance', 'horde'].forEach(f => out.push(row(`Races: ${FAC[f]}`, ids.map(id => { const rs = RACES.filter(r => r.f === f && r.can[id]); return rs.length ? rs.map(r => `<a href="${raceUrl(r.id)}">${esc(raceName(r))}</a>`).join(', ') : '<span class="none">None</span>'; }))));
  } else {
    const ids = C.race;
    out.push(`<div class="crow chead"><div class="lab"></div>${ids.map(id => { const r = RC[id]; return `<div class="val race ${r.f}"><span class="fx">${FAC[r.f]}${r.paid ? ' · paid' : ''}</span><b>${esc(raceName(r))}</b><a href="${raceUrl(id)}">Race page<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>`; }).join('')}</div>`);
    out.push(row('Classes', ids.map(id => ul(Object.keys(RC[id].can).map(c => `<span style="color:${CCOL[c]}">●</span> ${esc(CL[c].n)}${RC[id].can[c] === 'new' ? ' <span class="tag new">new</span>' : ''}`)))));
    out.push(row('Active abilities', ids.map(id => ul(RC[id].rac.filter(x => x[0] === 'a').map(x => `<b>${esc(x[1])}</b><br><span class="sub">${racx(x[2])}</span>`)))));
    out.push(row('Passive abilities', ids.map(id => ul(RC[id].rac.filter(x => x[0] === 'p').map(x => `<b>${esc(x[1])}</b><br><span class="sub">${racx(x[2])}</span>`)))));
    out.push(row('Tip', ids.map(id => esc(RC[id].tip)), 'tiprow'));
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

/* ---------- Picker: race and class (on the home page until Oct 25; class and race pages link tools/#pick=…) ---------- */
function facName(f) { return f === 'alliance' ? 'Alliance' : 'Horde'; }
function bi(ru) { return EN[ru] && EN[ru] !== ru ? `${esc(ru)} <span class="en">(${esc(EN[ru])})</span>` : esc(ru); }
function raceEn(r) { return r.en ? ` <span class="en">/ ${esc(r.en)}</span>` : ''; }
const tipBox = h => `<div class="tipbox"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg><p><span class="tl">Tip</span>${h}</p></div>`;
function face(id, cc, cls = '', title = '', f) { return `<span class="av ${cls}" style="--cc:${cc}"${title ? ` title="${esc(title)}"` : ''}><img src="${ROOT}assets/art/${porId(id, f)}-face.webp${PV}" width="160" height="160" alt="" loading="lazy" decoding="async"></span>`; }
function lvlMeter(c) {
  const p = c.lp || 0, w = Math.min(Math.abs(p) / 12 * 46, 46);
  const label = p < 0 ? `Faster by ${-p}%` : p > 0 ? `Slower by ${p}%` : 'Average pace';
  const bar = p ? `<i class="${p > 0 ? 'slow' : ''}" style="${p < 0 ? 'right' : 'left'}:50%;width:${w}%"></i>` : '';
  return `<span class="lvl"><span>${label}</span><span class="bar" role="img" aria-label="${label}">${bar}</span><span class="scale" aria-hidden="true"><span>faster</span><span>slower</span></span></span>`;
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
  let h = '<thead><tr><th scope="col">Race</th>';
  CLASSES.forEach(c => { h += `<th scope="col" class="${roleMatch(c, state.r) ? '' : 'dim'}${c.id === state.cls ? ' selc' : ''}">${face(c.id, CCOL[c.id])}${esc(c.n)}</th>`; });
  h += '</tr></thead><tbody>';
  ['alliance', 'horde'].forEach(f => {
    const rows = RACES.filter(r => r.f === f && raceVisible(r));
    if (!rows.length) return;
    h += `<tr class="fh ${f}"><th colspan="${CLASSES.length + 1}" scope="rowgroup"><span class="f ${f}"></span>${facName(f)}</th></tr>`;
    rows.forEach(r => {
      h += `<tr class="${r.id === state.race ? 'rowsel' : ''}"><th scope="row"><span class="rn">${face(RSLUG[r.id], `var(--${r.f})`)}${esc(r.n)}${r.paid ? '<span class="paid">paid</span>' : ''}</span></th>`;
      CLASSES.forEach(c => {
        const v = r.can[c.id];
        const dim = roleMatch(c, state.r) ? '' : ' dim';
        if (!v) { h += `<td><span class="cell no${dim}" role="img" aria-label="${esc(r.n)} ${esc(c.n)}: not allowed"></span></td>`; return; }
        const sel = (r.id === state.race && c.id === state.cls) ? ' sel' : '';
        const label = `${r.n} ${c.n}${v === 'new' ? ', new combination' : ''}`;
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
  const rac = r.rac.map(x => `<div class="card ab"><span class="abt${x[0] === 'a' ? '' : ' p'}">${x[0] === 'a' ? 'Active' : 'Passive'}</span><b>${bi(x[1])}</b><span>${racx(x[2])}</span></div>`).join('');
  const text = `${r.name || r.n} ${c.n} (${facName(r.f)})${r.paid ? ', Skyborne pack required' : ''}`;
  $('#detail').innerHTML = `
    <div class="d-head">
      <div class="d-art" aria-hidden="true"><picture><source type="image/avif" srcset="${ROOT}assets/art/${RSLUG[r.id]}-600.avif${PV}"><img src="${ROOT}assets/art/${RSLUG[r.id]}-600.webp${PV}" width="600" height="804" alt="" loading="lazy" decoding="async"></picture></div>
      <div class="d-avs">${face(RSLUG[r.id], `var(--${r.f})`)}</div>
      <div class="d-title"><h3>${esc(r.n)}${raceEn(r)} · ${esc(c.n)}</h3>
        <div class="chips"><span class="tag ${r.f}">${facName(r.f)}</span>${isNew ? '<span class="tag new">New combination</span>' : ''}${r.paid ? '<span class="tag paid">Paid race</span>' : ''}${roleChips(c)}</div></div>
    </div>
    <div class="d-body">
      <div class="d-cols">
        <div><h4>Specializations</h4><div class="cards">${specs}</div></div>
        <div><h4>Racial abilities</h4><div class="cards two">${rac}</div></div>
      </div>
      <div class="facts3">
        <div class="fact"><h4>Leveling</h4>${lvlMeter(c)}</div>
        <div class="fact"><h4>In raids</h4><span>${esc(c.raid)}.</span></div>
        <div class="fact"><h4>What’s new</h4><span>${esc(c.forever)}</span></div>
      </div>
      ${tipBox(esc(r.tip))}
      ${pickLinks(r, c)}
      <div class="copyrow">
        <input id="pickText" readonly value="${esc(text)}" aria-label="My choice">
        <button class="btn" id="copyBtn"><svg class="ico" aria-hidden="true"><use href="#i-copy"/></svg>Copy my choice</button>
        <button class="btn ghost" id="shareBtn">Share</button>
        <span class="small" id="copyMsg" role="status"></span>
      </div>
    </div>`;
  $('#copyBtn').onclick = () => copyTo($('#pickText').value, $('#copyMsg'), 'Copied');
  $('#shareBtn').onclick = () => shareBuild(r.id, c.id, state.spec, text);
}
/* Share: the link of the card page b/<race>-<class>-<spec>/ (its preview is the card with the name); on a phone the share sheet, else the clipboard */
function shareBuild(race, cls, spec, text) {
  const url = new URL(`${HOME}b/${BSLUG[race] || race}-${cls}-${spec}/`, location.href).href, msg = $('#copyMsg');
  if (navigator.share && matchMedia('(pointer: coarse)').matches) navigator.share({ title: text, url }).catch(e => { if (e && e.name !== 'AbortError') copyTo(url, msg, 'Link copied'); });
  else copyTo(url, msg, 'Link copied');
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
  eu: ['Europe', ''],
  cas: ['Europe', 'The Caucasus and Central Asia have no region of their own; the nearest is Europe.'],
  mea: ['Europe', 'The Middle East and Africa have no region of their own; the nearest is Europe.'],
  na: ['Americas and Oceania', ''],
  la: ['Americas and Oceania', 'Latin America plays in the Americas region.'],
  oce: ['Americas and Oceania', 'Blizzard groups Oceania with the Americas in one region. Blizzard has not said whether there are servers in Oceania itself.'],
  kr: ['Korea', ''],
  tw: ['Taiwan', ''],
  asia: ['', 'There is no region of your own. The nearest on the map are Taiwan and Korea. Pick the one with lower World latency.'],
};
function renderPing() {
  const v = $('#pgW').value, r = PG[v];
  try { if (v) localStorage.setItem('gabella-ping', v); } catch (e) {}
  if (!r) { $('#pgOut').innerHTML = ''; return; }
  $('#pgOut').innerHTML = (r[0] ? `<p class="preg">Your region: ${esc(r[0])}</p>` : '') + '<ul class="verdict">'
    + (r[1] ? `<li>${esc(r[1])}</li>` : '')
    + '<li>There are no realms: you choose a region and a ruleset, not a server. The region is chosen in Battle.net before you start the game.</li>'
    + '<li>Each region has its own characters and names. You can only play together within one region.</li>'
    + '<li>Blizzard has not said where the region servers are located.</li></ul>';
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
