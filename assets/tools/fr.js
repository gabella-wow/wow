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
const EN = {
  'Armes':'Armes','Fureur':'Fureur','Protection':'Protection','Sacré':'Sacré','Vindicte':'Vindicte',
  'Maîtrise des bêtes':'Maîtrise des bêtes','Précision':'Précision','Survie':'Survie',
  'Assassinat':'Assassinat','Combat':'Combat','Finesse':'Finesse',
  'Discipline':'Discipline','Ombre':'Ombre','Élémentaire':'Élémentaire','Amélioration':'Amélioration','Restauration':'Restauration',
  'Arcanes':'Arcanes','Feu':'Feu','Givre':'Givre','Affliction':'Affliction','Démonologie':'Démonologie','Destruction':'Destruction',
  'Équilibre':'Équilibre','Combat farouche':'Combat farouche',
  'Volonté de survie':'Volonté de survie','Perception':'Perception','Ruthless':'Ruthless','L’esprit humain':'L’esprit humain',
  'Forme de pierre':'Forme de pierre','Découverte de trésors':'Découverte de trésors','Earth Fury':'Earth Fury','Big Game Hunter':'Big Game Hunter',
  'Lumière d’Élune':"Lumière d’Élune",'Camouflage dans l’ombre':'Camouflage dans l’ombre','Rapidité':'Rapidité','Esprit feu follet':'Esprit feu follet',
  'Maître de l’évasion':'Maître de l’évasion','Eureka!':'Eurêka !','Pensée expansive':'Pensée expansive','Spécialisation en ingénierie':'Spécialisation en ingénierie',
  'Walk on Air':'Walk on Air','Read Ley Line':'Read Ley Line','Wind Blessed':'Wind Blessed','Elemental Insight':'Elemental Insight','Skysight':'Skysight',
  'Fureur sanguinaire':'Fureur sanguinaire','Shatter Curse':'Shatter Curse','Savage':'Savage','Commandement':'Commandement','Solidité':'Solidité',
  'Volonté des Réprouvés':'Volonté des Réprouvés','Cannibalisme':'Cannibalisme','Respiration aquatique':'Respiration aquatique','Toucher du tombeau':'Toucher du tombeau',
  'Choc martial':'Choc martial','Culture':'Culture','Course dans les plaines':'Course dans les plaines','Endurcissement':'Endurcissement',
  'Berserker':'Berserker','Régénération rapide':'Régénération rapide','Tueur de bêtes':'Tueur de bêtes','Régénération':'Régénération'
};
RC.skyA.en = 'High Order Skyborne'; RC.skyH.en = 'Windshaper Skyborne';
const CX = {"warrior": {"armor": "Tissu, cuir, mailles ; plaques dès le niveau 40 {beta}", "weapons": "Tout sauf les baguettes ; bouclier", "resource": "Rage", "lvl": "La montée la plus lente, environ 12 % plus longue que la moyenne (estimation de LFCarry)", "group": ["Cri de guerre affecte tout le raid", "Cri démoralisant et Fracasser armure sur le boss", "Attaques circulaires et Tourbillon pour les combats contre plusieurs cibles"], "pros": ["Meilleur tank et forts dégâts en mêlée", "Bon en JcJ (Armes)", "Peu de boutons, facile à comprendre"], "cons": ["Progression la plus lente", "Très dépendant de l’équipement", "Presque aucun soin personnel ni contrôle des foules"], "specs": [{"n": "Armes", "what": "Dégâts en mêlée (arme à deux mains)"}, {"n": "Fureur", "what": "Dégâts en mêlée (deux armes)"}, {"n": "Protection", "what": "Tank"}]}, "paladin": {"armor": "Tissu, cuir, mailles ; plaques dès le niveau 40 ; bouclier {beta}", "weapons": "Haches, masses, épées, armes d’hast dès le niveau 20 {beta}", "resource": "Mana", "lvl": "Rythme de progression moyen", "group": ["Auras de groupe : Dévotion, Vindicte, Concentration", "Auras de résistance au Feu, au Givre et à l’Ombre pour tout le raid", "Bénédictions d’une heure, bénédictions supérieures pour toute une classe", "Sceau de justice empêche les ennemis de fuir"], "pros": ["Les trois rôles sur un seul personnage", "Fortes améliorations de groupe", "Plaques et personnage solide"], "cons": ["Pas de rapprochement, de ralentissement ni d’accélération", "Peu de contrôle des foules en dehors de Marteau de la justice", "Vindicte en recul après le patch"], "specs": [{"n": "Sacré", "what": "Soigneur"}, {"n": "Protection", "what": "Tank"}, {"n": "Vindicte", "what": "Dégâts en mêlée"}]}, "hunter": {"armor": "Tissu, cuir ; mailles dès le niveau 40 {beta}", "weapons": "Arcs, arbalètes, armes à feu, haches, épées, armes d’hast", "resource": "Mana ; le familier utilise la Focalisation", "lvl": "La montée la plus rapide, environ 8 % plus vite que la moyenne (estimation de LFCarry)", "group": ["Aura de précision renforce les dégâts à distance du groupe", "Piège givrant : un contrôle des foules fiable", "Flèche de dispersion interrompt les incantations", "Aspect de la meute accélère tout le groupe sur la route"], "pros": ["Progression la plus rapide", "Excellent en solo", "Pièges et contrôle des foules"], "cons": ["Zone morte au contact jusqu’à 8 mètres", "Il faut gérer le familier", "Les talents Survie étaient buggés sur la bêta"], "specs": [{"n": "Maîtrise des bêtes", "what": "Dégâts à distance, beaucoup de dégâts du familier"}, {"n": "Précision", "what": "Dégâts à distance"}, {"n": "Survie", "what": "Mêlée et distance, pièges"}]}, "rogue": {"armor": "Tissu, cuir", "weapons": "Dagues, épées, masses, armes de pugilat, haches à une main, armes de jet", "resource": "Énergie et points de combo", "lvl": "Rythme de progression moyen", "group": ["Dégâts de mêlée purs, sans amélioration pour le raid", "Assommer, Cécité et Aiguillon perfide : beaucoup de contrôle des foules", "Coup de pied interrompt les incantations dangereuses"], "pros": ["Dégâts très élevés qui évoluent avec l’équipement", "Camouflage et beaucoup de contrôle des foules", "Liberté dans le choix d’arme"], "cons": ["Très dépendant de l’équipement", "Aucun soin personnel", "Seules Évasion et Disparition vous sauvent"], "specs": [{"n": "Assassinat", "what": "Dégâts de poison"}, {"n": "Combat", "what": "Attaques rapides à l’arme"}, {"n": "Finesse", "what": "Embuscades, saignements"}]}, "priest": {"armor": "Tissu", "weapons": "Dagues, masses, bâtons, baguettes", "resource": "Mana", "lvl": "Environ 5 % plus lent que la moyenne (estimation de LFCarry)", "group": ["Esprit divin et Mot de pouvoir : Robustesse pour tout le raid", "Infusion de puissance renforce un allié", "Le soigneur principal du groupe"], "pros": ["Toujours recherché par les groupes", "Soins ou dégâts d’ombre", "Nombreux builds"], "cons": ["Tissu uniquement, fragile", "Peu de moyens de se déplacer vite", "La hâte aide peu les sorts"], "specs": [{"n": "Discipline", "what": "Soigneur, boucliers et absorption"}, {"n": "Sacré", "what": "Soigneur"}, {"n": "Ombre", "what": "Dégâts à distance"}]}, "shaman": {"armor": "Tissu, cuir ; mailles dès le niveau 40 ; bouclier {beta}", "weapons": "Masses, haches, bâtons, armes de pugilat, dagues", "resource": "Mana", "lvl": "Rythme de progression moyen", "group": ["Les totems Force de la Terre, Furie-des-vents, Langue de feu et Grâce aérienne améliorent leur groupe", "Totem de Séisme supprime peur, sommeil et charme", "Totems de purification des poisons et des maladies", "Expiation retire les améliorations des ennemis"], "pros": ["Totems puissants pour le groupe", "Progression mobile", "Nouveaux talents puissants"], "cons": ["Pas de vrai contrôle des foules", "Le mana dans les combats longs", "Le rôle de tank reste non confirmé"], "specs": [{"n": "Élémentaire", "what": "Dégâts à distance"}, {"n": "Amélioration", "what": "Dégâts en mêlée. La capacité à tanker reste incertaine"}, {"n": "Restauration", "what": "Soigneur"}]}, "mage": {"armor": "Tissu", "weapons": "Dagues, épées, bâtons, baguettes", "resource": "Mana", "lvl": "La montée la plus rapide, environ 8 % plus vite que la moyenne, environ 12 heures gagnées (estimation de LFCarry)", "group": ["Portails dès le niveau 40, téléportations dès le 20", "Nourriture et eau pour le groupe", "Métamorphose : un contrôle des foules fiable", "Délivrance de la malédiction mineure"], "pros": ["Progression la plus rapide", "Portails et nourriture pour tous", "Trois arbres forts et différents"], "cons": ["Tissu uniquement, fragile", "Le mana s’épuise vite", "Dégâts de zone atténués"], "specs": [{"n": "Arcanes", "what": "Pics de dégâts, beaucoup de mana"}, {"n": "Feu", "what": "Critiques et enflammer"}, {"n": "Givre", "what": "Dégâts et contrôle"}]}, "warlock": {"armor": "Tissu", "weapons": "Dagues, épées, bâtons, baguettes", "resource": "Mana ; Connexion transforme la vie en mana", "lvl": "Rythme de progression moyen", "group": ["Pierre de soins et Pierre d’âme", "Rituel d’invocation : rassemble le groupe", "Malédiction des langages ralentit les incantations de 60%", "Malédiction des éléments : plus de dégâts magiques sur la cible"], "pros": ["Autonome : un démon et Connexion", "Beaucoup d’utilité pour le groupe", "Forts dégâts sur la durée"], "cons": ["Fragile et peu mobile", "Les dégâts mettent du temps à monter", "Ni transfert ni sprint"], "specs": [{"n": "Affliction", "what": "Dégâts des malédictions et de la corruption"}, {"n": "Démonologie", "what": "Dégâts par les démons"}, {"n": "Destruction", "what": "Dégâts directs de feu et d’ombre"}]}, "druid": {"armor": "Tissu, cuir", "weapons": "Dagues, masses, bâtons, armes de pugilat, armes d’hast dès le niveau 20 {beta}", "resource": "Mana ; rage en Forme d’ours, énergie en Forme de félin", "lvl": "Environ 5 % plus lent que la moyenne (estimation de LFCarry)", "group": ["Chef de la meute et Aura de sélénien affectent tout le raid et se cumulent", "Renaissance : résurrection en combat", "Innervation rend du mana à un soigneur", "Supprime malédictions et poisons"], "pros": ["Les trois rôles sur un seul personnage", "Excellente mobilité", "Résurrection en combat"], "cons": ["Ni blocage ni parade pour l’ours", "Les soins sur la durée sont plus difficiles à suivre", "Les chiffres finaux en raid sont encore inconnus"], "specs": [{"n": "Équilibre", "what": "Dégâts à distance"}, {"n": "Combat farouche", "what": "Tank (ours) et dégâts en mêlée (félin)"}, {"n": "Restauration", "what": "Soigneur, beaucoup de soins sur la durée"}]}};
const HC = {"tx":{"title":"Mon personnage","lead":"Sans compte ni mot de passe : choisissez une classe, une spécialisation et une race, et le site s’adapte à vous.","local":"Enregistré dans ce navigateur uniquement.","none":"Pas encore de personnage","create":"Créer un personnage","edit":"Modifier","reset":"Supprimer le personnage","resetQ":"Supprimer le personnage de ce navigateur ?","steps":["Camp","Classe et spécialisation","Race","Apparence","Détails"],"side":"Pour qui jouez-vous ?","cls":"Classe","spec":"Spécialisation","race":"Race","bestFor":"Meilleure race pour %s","best":"la meilleure","paid":"payant","sex":"Sexe","m":"Masculin","f":"Féminin","bg":"Arrière-plan du portrait","lvl":"Niveau","reg":"Région","lvlReg":"Niveau et région","regs":{"us":"Amériques et Océanie","eu":"Europe","kr":"Corée","tw":"Taïwan"},"p1":"Métier 1","p2":"Métier 2","secP":"Métiers secondaires","noP":"Aucun","role":"Rôle","back":"Retour","next":"Continuer","done":"OK","cancel":"Annuler","later":"Vous pouvez le remplir plus tard.","levelN":"Niveau %n","build":"Mon build de talents","buildD":"Talents %s par niveau.","pairs":"Paires de métiers","pairsD":"Quels métiers conviennent à votre classe.","bestR":"Meilleures races","bestRD":"Race pour votre classe dans les deux factions.","lvlG":"Montée en niveau de la classe","lvlGD":"Itinéraire et talents 1–60.","day1":"Jour 1 pour votre personnage","day1D":"La liste de lancement avec votre classe et votre race.","play":"En jeu","playD":"Zones et donjons pour votre niveau, minuteurs, radio.","dung":"Donjons pour votre niveau","dungNo":"Indiquez votre niveau et nous choisirons les donjons.","dungFirst":"Les premiers donjons ouvrent au niveau 13.","resetH":"Réinitialisation hebdomadaire","resetIn":"dans %s","resetNote":"Blizzard n’a pas encore annoncé l’heure de réinitialisation de Forever. Affiché comme dans les autres versions de WoW de cette région : nous vérifierons au lancement.","resetUnk":"Nous confirmerons l’heure de réinitialisation de cette région au lancement.","resetNoReg":"Indiquez votre région pour voir la réinitialisation hebdomadaire.","resetWhy":"Les raids ouvrent le 09.12 et ont un verrouillage hebdomadaire.","lfg":"Texte de recherche de groupe","lfgD":"Collez-le dans le canal LookingForGroup. Noms comme en jeu.","lfgP":{"tank":"%c tank cherche un groupe","heal":"%c soigneur cherche un groupe","dps":"%c cherche un groupe"},"lfgT":"%p : %d, niveau %l.","lfgT0":"%p.","allD":"Tous les donjons","copy":"Copier","copied":"Copié","sync":"Synchroniser entre appareils","syncD":"La connexion ne sert qu’à cela : le personnage sera sur votre téléphone et votre PC, et la lettre du lancement arrive par e-mail si vous vous abonnez.","yourCls":"Votre %s","bTalents":"Talents","bSpec":"Build : %s","bLevel":"Progression","bGroup":"Groupe","bNews":"Actualités","copiedT":"Copié : %s","profsL":"Métiers","day1n":"Jour 1 : %n sur %t","collect":"Créer mon personnage","collectD":"Classe, spécialisation et race : talents, montée en niveau, groupe et actualités de votre classe.","change":"Changer","allSet":"Tous les réglages","close":"Fermer","mine":"Concerne votre classe","share":"Partager","linkCopied":"Lien copié","make":"En faire mon personnage","made":"C’est votre personnage","plaqueH":"Mon personnage","plaqueD":"Classe, spécialisation et race en une minute, puis votre build, vos métiers et vos donjons.","day1Mine":"Pour votre personnage","ckClass":"Votre spécialisation, %s : le build de talents par niveau.","ckRaceOk":"%r est la meilleure race pour votre spécialisation.","ckRaceAlt":"Meilleure race pour votre spécialisation : %r.","ckProfs":"Paires de métiers pour %s.","ckStart":"Montée en niveau %s : itinéraire et premiers talents.","ckPing":"Votre région : %s.","or":"ou"},"best":{"warrior":{"alliance":{"*":[["human","nightelf"],"Humain : +1 % de critique avec toute arme. Elfe de la nuit : +10 % de critique pendant 15 s. Les sources sont presque partagées à égalité."],"protection":[["dwarf"],"Forme de pierre réduit les dégâts physiques de 10 % et dissipe les saignements."]},"horde":{"*":[["orc"],"Fureur sanguinaire : +10 % de puissance d’attaque pendant 15 s. Avant les changements des races du 26.10, toutes les sources la plaçaient en tête."],"protection":[["tauren"],"Endurcissement donne +5 % de points de vie, Choc martial étourdit les ennemis proches."]}},"paladin":{"alliance":{"*":[["human"],"Ruthless renforce les coups comme les sorts, Volonté de survie dissipe les étourdissements."],"protection":[["dwarf"],"Forme de pierre et Artisan’s Precision : +1 % de chances de toucher."]},"horde":{"*":[["undead"],"Dans la Horde, seul le Mort-vivant peut être paladin. Cannibalisme rend du mana, Volonté des Réprouvés dissipe la peur."]}},"hunter":{"alliance":{"*":[["human","nightelf"],"Humain : +1 % de critique, et le familier en hérite. Elfe de la nuit : Lumière d’Élune et Camouflage dans l’ombre."]},"horde":{"*":[["orc","troll"],"Orc : Fureur sanguinaire et Commandement (+5 % de dégâts du familier). Troll : +5 % de dégâts contre les bêtes."]}},"rogue":{"alliance":{"*":[["nightelf"],"Camouflage dans l’ombre réduit désormais la menace en combat aussi, plus Grâce d’Elune et Rapidité."]},"horde":{"*":[["orc"],"Fureur sanguinaire : +10 % de puissance d’attaque pendant 15 s."]}},"priest":{"alliance":{"*":[["gnome"],"Toutes les sources la choisissent : Eurêka ! renforce aussi Mot de pouvoir : Bouclier, Inquisitive Mind donne +5 % de mana."]},"horde":{"*":[["undead","troll"],"Les sources sont partagées. Le Mort-vivant est plus fort en PvP : Volonté des Réprouvés dissipe peur, sommeil et charme."]}},"shaman":{"alliance":{"*":[["dwarf"],"Dans l’Alliance, seul le Nain peut être chaman : Forme de pierre et Artisan’s Precision (+1 % de chances de toucher)."]},"horde":{"*":[["orc"],"Fureur sanguinaire donne puissance d’attaque et puissance des sorts : bonne pour Élémentaire comme pour Amélioration."],"restoration":[["troll"],"Pour un soigneur, une source conseille le Troll : Berserker, +10 % de vitesse d’incantation pendant 12 s."]}},"mage":{"alliance":{"*":[["gnome"],"Eurêka ! pendant 8 s, Inquisitive Mind : +5 % de mana, Maître de l’évasion brise les entraves."]},"horde":{"*":[["orc"],"L’orc mage est une nouvelle combinaison de Forever : Fureur sanguinaire donne désormais de la puissance des sorts."]}},"warlock":{"alliance":{"*":[["gnome","human"],"Gnome : Eurêka ! et Inquisitive Mind. Humain : les dégâts sur la durée peuvent être critiques, Ruthless donne +1 % de critique."]},"horde":{"*":[["orc","undead"],"Orc : Fureur sanguinaire donne de la puissance des sorts. Le Mort-vivant est plus souvent choisi en PvP."]}},"druid":{"alliance":{"*":[["nightelf"],"Grâce d’Elune : +10 % de critique pendant 15 s, et Rapidité."]},"horde":{"*":[["tauren"],"Endurcissement : +5 % de points de vie, Choc martial fonctionne aussi en forme."]}}},"sid":{"warrior":["arms","fury","protection"],"paladin":["holy","protection","retribution"],"hunter":["beast-mastery","marksmanship","survival"],"rogue":["assassination","combat","subtlety"],"priest":["discipline","holy","shadow"],"shaman":["elemental","enhancement","restoration"],"mage":["arcane","fire","frost"],"warlock":["affliction","demonology","destruction"],"druid":["balance","feral","restoration"]},"sn":{"warrior":["Armes","Fureur","Protection"],"paladin":["Sacré","Protection","Vindicte"],"hunter":["Maîtrise des bêtes","Précision","Survie"],"rogue":["Assassinat","Combat","Finesse"],"priest":["Discipline","Sacré","Ombre"],"shaman":["Élémentaire","Amélioration","Restauration"],"mage":["Arcanes","Feu","Givre"],"warlock":["Affliction","Démonologie","Destruction"],"druid":["Équilibre","Combat farouche","Restauration"]},"fn":{"alliance":"Alliance","horde":"Horde"},"reset":{"us":[2,15],"eu":[3,4],"kr":null,"tw":null},"rn":{"human":"Humain","dwarf":"Nain","nightelf":"Elfe de la nuit","gnome":"Gnome","skyA":"Skyborne High Order","orc":"Orc","undead":"Mort-vivant","tauren":"Tauren","troll":"Troll","skyH":"Skyborne Windshaper"},"rf":{"human":"alliance","dwarf":"alliance","nightelf":"alliance","gnome":"alliance","skyA":"alliance","orc":"horde","undead":"horde","tauren":"horde","troll":"horde","skyH":"horde"},"cn":{"warrior":"Guerrier","paladin":"Paladin","hunter":"Chasseur","rogue":"Voleur","priest":"Prêtre","shaman":"Chaman","mage":"Mage","warlock":"Démoniste","druid":"Druide"},"cen":{"warrior":"Warrior","paladin":"Paladin","hunter":"Hunter","rogue":"Rogue","priest":"Priest","shaman":"Shaman","mage":"Mage","warlock":"Warlock","druid":"Druid"}};
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

const CPROF = {"warrior": [["Progression: Forge + Minage", ""], ["Niveau 60: Ingénierie + Minage", "Le forgeron s’équipe en plaques et en armes, et beaucoup de recettes sont personnelles. L’ingénieur obtient des grenades et des gadgets qui manquent au guerrier."]], "paladin": [["Progression: Forge + Minage", ""], ["Niveau 60: Protection, Vindicte : Ingénierie + Minage. Sacré : Alchimie + Herboristerie", "Sacré consomme beaucoup de mana : les potions sont les vôtres, et le Mana Well du camp remplace Bénédiction de sagesse."]], "hunter": [["Progression: Travail du cuir + Dépeçage", ""], ["Niveau 60: Ingénierie + Minage", "Le travailleur du cuir se fait son cuir et ses mailles et des Armor Kits. L’ingénieur fabrique des viseurs et des armes à feu."]], "rogue": [["Progression: Travail du cuir + Dépeçage", ""], ["Niveau 60: Ingénierie + Minage", "Le cuir est à vous, et la Camp Tent donne du repos. L’Ingénierie est le métier principal pour le JcJ."]], "priest": [["Progression: Couture + Enchantement", ""], ["Niveau 60: Couture + Ingénierie ou Enchantement", "Le couturier fait des ceintures de puissance des sorts dès le niveau 10, l’enchanteur des baguettes de puissance des sorts dès le niveau 5. Ce qui est cousu se désenchante en matériaux."]], "shaman": [["Progression: Travail du cuir + Dépeçage", ""], ["Niveau 60: Alchimie + Herboristerie", "Le travailleur du cuir fait des objets de puissance des sorts pour Élémentaire et Restauration et de l’équipement pour Amélioration. En raid et en groupe, il faut des potions."]], "mage": [["Progression: Couture + Enchantement", ""], ["Niveau 60: Couture + Enchantement ; pour le JcJ et les gros groupes d’ennemis Ingénierie + Minage", "Le couturier donne un équipement précoce de puissance des sorts, et ce qui est cousu se désenchante. Les grenades de l’ingénieur immobilisent les gros groupes d’ennemis."]], "warlock": [["Progression: Couture + Enchantement", ""], ["Niveau 60: Couture + Alchimie", "La Faction Banner du couturier donne de l’Esprit pour Connexion. L’Alchimie, c’est des potions et de l’or."]], "druid": [["Progression: Travail du cuir + Dépeçage ou Herboristerie", ""], ["Niveau 60: Alchimie + Herboristerie", "Les herbes se récoltent en forme de voyage, les potions se boivent sous n’importe quelle forme. Mana Well et Incense Candle servent à Équilibre et Restauration."]]};   /* recommended profession pairs per class, already in the page language (build.class_profs) */
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
  try { await navigator.clipboard.writeText(text); msgEl.textContent = ok; } catch (e) { msgEl.textContent = 'Copie impossible, sélectionnez le texte et appuyez sur Ctrl+C'; }
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
    out.push((groups > 1 ? `Groupe ${g + 1}: ` : '') + part.map(p => `${p.name ? p.name + ' — ' : ''}${raceName(RC[p.race])} ${CL[p.cls].n} (${ROLE_RU[p.role]})`).join(', '));
  }
  return out.length ? out.join('\n') + `\n${FAC[R.f]}, ${R.size}` : '';
}

/* LFG line: the dungeon or raid, the missing roles, the play style and a short link (#t=); kept under the 255-byte chat limit */
const LFG = {"d": [["Gouffre de Ragefeu", 13, 18, "horde"], ["Hall of Thanes", 13, 18, 0], ["Ruines de Lordaeron", 15, 20, 0], ["Les Mortemines", 15, 22, 0], ["Cavernes des lamentations", 17, 24, 0], ["Donjon d’Ombrecroc", 20, 26, 0], ["Profondeurs de Brassenoire", 22, 28, 0], ["La Prison", 25, 29, "alliance"], ["Excavation Site: Wetlands", 26, 31, 0], ["City of Dalaran", 28, 33, 0], ["Gnomeregan", 29, 38, 0], ["Kraal de Tranchebauge", 29, 38, 0], ["Monastère écarlate : Cimetière", 30, 38, 0], ["Monastère écarlate : Bibliothèque", 33, 41, 0], ["The Drowned City", 35, 40, 0], ["Monastère écarlate : Armurerie", 36, 44, 0], ["Uldaman", 36, 45, 0], ["Souilles de Tranchebauge", 37, 46, 0], ["Monastère écarlate : Cathédrale", 38, 46, 0], ["Zul’Farrak", 40, 47, 0], ["Krol’dok Stronghold", 40, 45, 0], ["Maraudon", 45, 51, 0], ["Alcaz Island Prison", 48, 53, 0], ["Le temple d’Atal’Hakkar", 50, 55, 0], ["Profondeurs de Blackrock", 52, 60, 0], ["Blackmaw Hold", 55, 60, 0], ["Pic Blackrock inférieur", 57, 60, 0], ["Hache-tripes : Est", 58, 60, 0], ["Shaper’s Terrace", 58, 60, 0], ["Stratholme : vivants", 58, 60, 0], ["Stratholme : morts-vivants", 58, 60, 0], ["Scholomance", 58, 60, 0], ["Pic Blackrock supérieur", 60, 60, 0], ["Hache-tripes : Ouest", 60, 60, 0], ["Hache-tripes : Nord", 60, 60, 0]], "r": {"10": "Barrow Deeps", "20": "Sommet d’Hyjal", "40": "Repaire d’Onyxia"}};   // dungeons [name, min, max, entrance faction] and raids {size: name} in the client's language (build_tools)
const CHAT_MAX = 255, CANON = 'https://gabella.site/wow/fr/tools/'.replace(/^https?:\/\//, '');
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
  const head = (L.d ? '%d — on cherche : %n.' : 'Groupe cherche : %n.').replace('%d', L.d).replace('%n', roles);
  const parts = [head, L.s ? 'Style : %s.'.replace('%s', L.s) : '', CANON + shortHash()].filter(Boolean);
  const bytes = t => new TextEncoder().encode(t).length;
  let text = parts.join(' ');
  if (bytes(text) > CHAT_MAX) text = parts.slice(0, -1).join(' ');   // a long raid code would not fit: the link goes first
  return text;
}
function renderLfg() {
  const places = lfgPlaces(), sel = $('#lfgD');
  if (!places.some(p => p[0] === L.d)) L.d = R.size === 5 ? '' : (places[0] || [''])[0];
  $('#lfgDL').textContent = R.size === 5 ? 'Donjon' : 'Raid';
  sel.innerHTML = (R.size === 5 ? '<option value="">N’importe quel donjon</option>' : '') + places.map(([v, t]) => `<option value="${esc(v)}"${v === L.d ? ' selected' : ''}>${esc(t)}</option>`).join('');
  syncSeg('lfgS', L.s);
  const text = lfgText();
  $('#rLfg').value = text;
  $('#rCopyLfg').disabled = !text;
  $('#rLfgMsg').textContent = text ? lfgLen(text) : R.s.some(Boolean) ? 'Toutes les places sont prises.' : 'Ajoutez au moins un joueur au groupe.';
}
function lfgLen(t) { return 'Caractères : %n sur %m (limite d’une ligne de chat).'.replace('%n', t.length).replace('%m', CHAT_MAX); }

function unitHTML(p, i) {
  const cls = R.moving === i ? ' src' : '';
  if (!p) return `<button type="button" class="unit empty${cls}" data-i="${i}"><span class="up" aria-hidden="true">+</span><span class="ub"><b>Place libre</b><span>Cliquez pour ajouter un joueur</span></span></button>`;
  const c = CL[p.cls], r = RC[p.race];
  return `<button type="button" class="unit${cls}" data-i="${i}" draggable="true" style="--cc:${CCOL[p.cls]};--pc:${power(p)}" aria-label="${esc((p.name || `Joueur ${i + 1}`) + ', ' + raceName(r) + ' ' + c.n + ', ' + ROLE_RU[p.role])}">
    <span class="up"><picture><source type="image/avif" srcset="${unitArt(p, 'avif')}"><img src="${unitArt(p, 'webp')}" width="360" height="482" alt="" loading="lazy" decoding="async"></picture></span>
    <span class="ub"><span class="un"><span class="ur" title="${ROLE_RU[p.role]}">${ri(p.role)}</span><b>${esc(p.name || c.n)}</b><small>${esc(raceName(r))} · ${esc(c.n)}</small></span><span class="hp"><i></i></span><span class="mp"></span></span></button>`;
}
function cellHTML(p, i) {
  const cls = R.moving === i ? ' src' : '';
  if (!p) return `<button type="button" class="rc empty${cls}" data-i="${i}" aria-label="Place libre ${i + 1}"><span aria-hidden="true">+</span>Ajouter</button>`;
  const c = CL[p.cls], r = RC[p.race];
  return `<button type="button" class="rc${cls}" data-i="${i}" draggable="true" style="--cc:${CCOL[p.cls]};--pc:${power(p)}" aria-label="${esc((p.name || `Joueur ${i + 1}`) + ', ' + raceName(r) + ' ' + c.n + ', ' + ROLE_RU[p.role])}" title="${esc(raceName(r) + ' · ' + c.n + ' · ' + ROLE_RU[p.role])}"><b>${esc(p.name || c.n)}</b><small>${esc(p.name ? c.n : raceName(r))}</small>${ri(p.role)}</button>`;
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
      const st = n && (!c.tank || !c.heal) ? `<span class="warn">${!c.tank ? 'pas de tank' : 'pas de soigneur'}</span>` : `<span>${n}/5</span>`;
      h += `<div class="rg"><div class="rg-h"><b>Groupe ${g + 1}</b>${st}</div>${part.map((p, k) => cellHTML(p, g * PARTY + k)).join('')}</div>`;
    }
    $('#rview').innerHTML = `<div class="rgrid" style="--gc:${Math.min(groups, 8)}">${h}</div>`;
  }
  const hint = $('#rhint');
  hint.classList.toggle('on', R.moving >= 0);
  hint.innerHTML = R.moving >= 0 ? `Choisir une nouvelle place pour le joueur ${R.moving + 1}. <button type="button" id="mvCancel">Annuler</button>` : '';

  const list = R.s.filter(Boolean), cnt = countRoles(list), rec = REC[R.size];
  $('#rRoles').innerHTML = RR.map((x, k) => `<span class="${list.length && cnt[x] < rec[k] ? 'low' : ''}">${ri(x)}${ROLE_RU[x]} <b>${cnt[x]}</b> / ${rec[k]}</span>`).join('');
  $('#rTip').textContent = R.size === 5 ? 'Un donjon demande un tank, un soigneur et trois DPS.' : `Règle simple pour un raid : tanks ${rec[0]}, soigneurs ${rec[1]}, le reste en dégâts. Le nombre exact dépend des boss.`;
  const have = new Set(list.map(p => p.cls));
  $('#rBuffs').innerHTML = CLASSES.filter(c => BUFF[c.id]).map(c => `<li class="${have.has(c.id) ? '' : 'off'}" style="--cc:${CCOL[c.id]}"><span class="cdot"></span><span><b>${esc(c.n)}:</b> ${esc(BUFF[c.id])}</span></li>`).join('');
  const n = list.length;
  $('#rRaids').innerHTML = n ? RAIDS.map(([size, name]) => `<li class="${n >= size ? 'good' : ''}">${n >= size ? `Raid de ${size} (${name}) : assez de joueurs.` : `Raid de ${size} (${name}) : il en manque ${size - n}.`}</li>`).join('') : '<li>Personne pour l’instant. Cliquez sur « Mon personnage », « Remplir les vides » ou sur un cadre libre.</li>';

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
function myHero() {   // the hero of this browser (assets/hero/hero.js?v=c87ea2ee87, localStorage gabella-wf-me)
  let h = null; try { h = JSON.parse(localStorage.getItem('gabella-wf-me')); } catch (e) {}
  return h && RC[h.race] && CL[h.cls] && RC[h.race].can[h.cls] ? h : null;
}
$('#rMine').onclick = () => {
  const h = myHero(), msg = $('#rMy');
  if (!h) {
    msg.innerHTML = 'Pas encore de personnage. <a href="../character/" id="rMake">Créer mon personnage</a>';
    $('#rMake').onclick = e => { if (window.GabellaHero) { e.preventDefault(); GabellaHero.open(); } };
    return;
  }
  const f = RC[h.race].f, role = RR.includes(h.role) ? h.role : roleOpts(CL[h.cls])[0];
  if (f !== R.f) {
    if (R.s.some(Boolean)) { msg.textContent = 'Votre personnage est de l’autre faction : changez de faction au-dessus des cadres.'; return; }
    R.f = f;
  }
  if (R.s.some(p => p && p.race === h.race && p.cls === h.cls && p.role === role && !p.name)) { msg.textContent = 'Votre personnage est déjà dans la composition.'; return; }
  let i = R.s.findIndex(p => !p); if (i < 0) i = 0;
  R.s[i] = { race: h.race, cls: h.cls, role, name: '' };
  msg.textContent = ''; R.moving = -1; renderRaid();
};
$('#rClear').onclick = () => { R.s = Array(R.size).fill(null); R.moving = -1; renderRaid(); };
$('#rCopyLink').onclick = () => copyTo(teamLink(), $('#rMsg'), 'Lien copié');
$('#rCopyText').onclick = () => copyTo(teamText(), $('#rMsg'), 'Groupe copié');
$('#lfgD').onchange = e => { L.d = e.target.value; renderLfg(); };
$('#lfgS').addEventListener('click', e => { const b = e.target.closest('button'); if (b) { L.s = L.s === b.dataset.v ? '' : b.dataset.v; renderLfg(); } });
$('#rCopyLfg').onclick = () => { const t = lfgText(); copyTo(t, $('#rLfgMsg'), 'Texte copié. ' + lfgLen(t)); };

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
  $('#edT').textContent = `Joueur ${edI + 1}` + (R.size > 5 ? ` · Groupe ${Math.floor(edI / PARTY) + 1}` : '');
  $('#edRace').innerHTML = RACES.filter(r => r.f === R.f).map(r => `<option value="${r.id}"${r.id === p.race ? ' selected' : ''}>${esc(raceName(r))}${r.paid ? ' (payant)' : ''}</option>`).join('');
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
  else box.innerHTML = ['alliance', 'horde'].map(f => `<div class="rside ${f}"><h3>${FAC[f]}</h3>${RACES.filter(r => r.f === f).map(r => { const k = sel.indexOf(r.id); return `<button type="button" class="rp" data-id="${r.id}" aria-pressed="${k >= 0}">${esc(raceName(r))}${r.paid ? '<span class="tag paid">payant</span>' : ''}<span class="no">${k + 1}</span></button>`; }).join('')}</div>`).join('');
  $('#cNote').textContent = `Choisis ${sel.length} sur 3`;
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
const ul = (items, cls) => items.length ? `<ul${cls ? ` class="${cls}"` : ''}>${items.map(x => `<li>${x}</li>`).join('')}</ul>` : '<span class="none">Aucun</span>';
const row = (lab, vals, extra) => `<div class="crow${extra ? ' ' + extra : ''}"><div class="lab${extra === 'tiprow' ? ' tl' : ''}">${lab}</div>${vals.map(v => `<div class="val">${v}</div>`).join('')}</div>`;
function renderCmp() {
  const out = [];
  if (C.mode === 'class') {
    const ids = C.cls;
    out.push(`<div class="crow chead"><div class="lab"></div>${ids.map(id => `<div class="val" style="--cc:${CCOL[id]}"><picture><source type="image/avif" srcset="${art(id, 'avif')}"><img src="${art(id)}" width="360" height="482" alt="" loading="lazy" decoding="async"></picture><b>${esc(CL[id].n)}</b><a href="${classUrl(id)}">Page de la classe<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>`).join('')}</div>`);
    out.push(row('Rôles', ids.map(id => CL[id].roles.map(r => `<span class="role">${ri(r)}${ROLE_RU[r]}</span>`).join(''))));
    out.push(row('Armure', ids.map(id => racx(CX[id].armor))));
    out.push(row('Armes', ids.map(id => racx(CX[id].weapons))));
    out.push(row('Ressource', ids.map(id => esc(CX[id].resource))));
    out.push(row('Progression', ids.map(id => esc(CX[id].lvl))));
    out.push(row('Spécialisations', ids.map(id => ul(CX[id].specs.map(s => `<b>${esc(s.n)}</b>${SPEC_SEP}<span class="sub">${esc(s.what)}</span>`)))));
    out.push(row('Amélioration de raid', ids.map(id => BUFF[id] ? esc(BUFF[id]) : '<span class="none">Aucun</span>')));
    out.push(row('En groupe', ids.map(id => ul(CX[id].group.map(esc)))));
    out.push(row('Métiers', ids.map(id => ul(CPROF[id].map(p => `<b>${esc(p[0])}</b>${p[1] ? `<br><span class="sub">${esc(p[1])}</span>` : ''}`)) + `<a class="cgo" href="${HOME}guides/professions/#pairs=${id}">Objets de camp et compétence<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a>`)));
    out.push(row('Points forts', ids.map(id => ul(CX[id].pros.map(esc), 'plus'))));
    out.push(row('Points faibles', ids.map(id => ul(CX[id].cons.map(esc), 'minus'))));
    ['alliance', 'horde'].forEach(f => out.push(row(`Races : ${FAC[f]}`, ids.map(id => { const rs = RACES.filter(r => r.f === f && r.can[id]); return rs.length ? rs.map(r => `<a href="${raceUrl(r.id)}">${esc(raceName(r))}</a>`).join(', ') : '<span class="none">Aucun</span>'; }))));
  } else {
    const ids = C.race;
    out.push(`<div class="crow chead"><div class="lab"></div>${ids.map(id => { const r = RC[id]; return `<div class="val race ${r.f}"><span class="fx">${FAC[r.f]}${r.paid ? ' · payant' : ''}</span><b>${esc(raceName(r))}</b><a href="${raceUrl(id)}">Page de la race<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>`; }).join('')}</div>`);
    out.push(row('Classes', ids.map(id => ul(Object.keys(RC[id].can).map(c => `<span style="color:${CCOL[c]}">●</span> ${esc(CL[c].n)}${RC[id].can[c] === 'new' ? ' <span class="tag new">nouveau</span>' : ''}`)))));
    out.push(row('Capacités actives', ids.map(id => ul(RC[id].rac.filter(x => x[0] === 'a').map(x => `<b>${esc(x[1])}</b><br><span class="sub">${racx(x[2])}</span>`)))));
    out.push(row('Capacités passives', ids.map(id => ul(RC[id].rac.filter(x => x[0] === 'p').map(x => `<b>${esc(x[1])}</b><br><span class="sub">${racx(x[2])}</span>`)))));
    out.push(row('Conseil', ids.map(id => esc(RC[id].tip)), 'tiprow'));
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
function facName(f) { return f === 'alliance' ? 'Alliance' : 'Horde'; }
function bi(ru) { return EN[ru] && EN[ru] !== ru ? `${esc(ru)} <span class="en">(${esc(EN[ru])})</span>` : esc(ru); }
function raceEn(r) { return r.en ? ` <span class="en">/ ${esc(r.en)}</span>` : ''; }
const tipBox = h => `<div class="tipbox"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg><p><span class="tl">Conseil</span>${h}</p></div>`;
function face(id, cc, cls = '', title = '', f) { return `<span class="av ${cls}" style="--cc:${cc}"${title ? ` title="${esc(title)}"` : ''}><img src="${ROOT}assets/art/${porId(id, f)}-face.webp${PV}" width="160" height="160" alt="" loading="lazy" decoding="async"></span>`; }
function lvlMeter(c) {
  const p = c.lp || 0, w = Math.min(Math.abs(p) / 12 * 46, 46);
  const label = p < 0 ? `Plus rapide de ${-p}%` : p > 0 ? `Plus lent de ${p}%` : 'Rythme moyen';
  const bar = p ? `<i class="${p > 0 ? 'slow' : ''}" style="${p < 0 ? 'right' : 'left'}:50%;width:${w}%"></i>` : '';
  return `<span class="lvl"><span>${label}</span><span class="bar" role="img" aria-label="${label}">${bar}</span><span class="scale" aria-hidden="true"><span>plus rapide</span><span>plus lent</span></span></span>`;
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
      h += `<tr class="${r.id === state.race ? 'rowsel' : ''}"><th scope="row"><span class="rn">${face(RSLUG[r.id], `var(--${r.f})`)}${esc(r.n)}${r.paid ? '<span class="paid">payant</span>' : ''}</span></th>`;
      CLASSES.forEach(c => {
        const v = r.can[c.id];
        const dim = roleMatch(c, state.r) ? '' : ' dim';
        if (!v) { h += `<td><span class="cell no${dim}" role="img" aria-label="${esc(r.n)} ${esc(c.n)}: impossible"></span></td>`; return; }
        const sel = (r.id === state.race && c.id === state.cls) ? ' sel' : '';
        const label = `${r.n} ${c.n}${v === 'new' ? ', nouvelle combinaison' : ''}`;
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
  const text = `${r.name || r.n} ${c.n} (${facName(r.f)})${r.paid ? ', pack Skyborne requis' : ''}`;
  $('#detail').innerHTML = `
    <div class="d-head">
      <div class="d-art" aria-hidden="true"><picture><source type="image/avif" srcset="${ROOT}assets/art/${RSLUG[r.id]}-600.avif${PV}"><img src="${ROOT}assets/art/${RSLUG[r.id]}-600.webp${PV}" width="600" height="804" alt="" loading="lazy" decoding="async"></picture></div>
      <div class="d-avs">${face(RSLUG[r.id], `var(--${r.f})`)}</div>
      <div class="d-title"><h3>${esc(r.n)}${raceEn(r)} · ${esc(c.n)}</h3>
        <div class="chips"><span class="tag ${r.f}">${facName(r.f)}</span>${isNew ? '<span class="tag new">Nouvelle combinaison</span>' : ''}${r.paid ? '<span class="tag paid">Race payante</span>' : ''}${roleChips(c)}</div></div>
    </div>
    <div class="d-body">
      <div class="d-cols">
        <div><h4>Spécialisations</h4><div class="cards">${specs}</div></div>
        <div><h4>Capacités raciales</h4><div class="cards two">${rac}</div></div>
      </div>
      <div class="facts3">
        <div class="fact"><h4>Progression</h4>${lvlMeter(c)}</div>
        <div class="fact"><h4>En raid</h4><span>${esc(c.raid)}.</span></div>
        <div class="fact"><h4>Nouveautés</h4><span>${esc(c.forever)}</span></div>
      </div>
      ${tipBox(esc(r.tip))}
      ${pickLinks(r, c)}
      <div class="copyrow">
        <input id="pickText" readonly value="${esc(text)}" aria-label="Mon choix">
        <button class="btn" id="copyBtn"><svg class="ico" aria-hidden="true"><use href="#i-copy"/></svg>Copier mon choix</button>
        <button class="btn ghost" id="shareBtn">Partager</button>
        <span class="small" id="copyMsg" role="status"></span>
      </div>
    </div>`;
  $('#copyBtn').onclick = () => copyTo($('#pickText').value, $('#copyMsg'), 'Copié');
  $('#shareBtn').onclick = () => shareBuild(r.id, c.id, state.spec, text);
}
/* Share: the link of the card page b/<race>-<class>-<spec>/ (its preview is the card with the name); on a phone the share sheet, else the clipboard */
function shareBuild(race, cls, spec, text) {
  const url = new URL(`${HOME}b/${BSLUG[race] || race}-${cls}-${spec}/`, location.href).href, msg = $('#copyMsg');
  if (navigator.share && matchMedia('(pointer: coarse)').matches) navigator.share({ title: text, url }).catch(e => { if (e && e.name !== 'AbortError') copyTo(url, msg, 'Lien copié'); });
  else copyTo(url, msg, 'Lien copié');
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
  cas: ['Europe', 'Le Caucase et l’Asie centrale n’ont pas de région propre ; la plus proche est l’Europe.'],
  mea: ['Europe', 'Le Moyen-Orient et l’Afrique n’ont pas de région propre ; la plus proche est l’Europe.'],
  na: ['Amériques et Océanie', ''],
  la: ['Amériques et Océanie', 'L’Amérique latine joue dans la région Amériques.'],
  oce: ['Amériques et Océanie', 'Blizzard regroupe l’Océanie avec les Amériques dans une seule région. Blizzard n’a pas dit s’il y a des serveurs en Océanie même.'],
  kr: ['Corée', ''],
  tw: ['Taïwan', ''],
  asia: ['', 'Pas de région propre. Les plus proches sur la carte sont Taïwan et la Corée. Prenez celle où la latence World est la plus basse.'],
};
function renderPing() {
  const v = $('#pgW').value, r = PG[v];
  try { if (v) localStorage.setItem('gabella-ping', v); } catch (e) {}
  if (!r) { $('#pgOut').innerHTML = ''; return; }
  $('#pgOut').innerHTML = (r[0] ? `<p class="preg">Votre région : ${esc(r[0])}</p>` : '') + '<ul class="verdict">'
    + (r[1] ? `<li>${esc(r[1])}</li>` : '')
    + '<li>Pas de royaumes : on choisit une région et des règles, pas un serveur. La région se choisit dans Battle.net avant de lancer le jeu.</li>'
    + '<li>Chaque région a ses propres personnages et noms. On ne joue ensemble que dans une même région.</li>'
    + '<li>Blizzard n’a pas dit où se trouvent les serveurs des régions.</li></ul>';
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
