const CLASSES = [
  { id:'warrior', n:'Guerriero', s:'Guerriero', roles:['tank','dps'],
    specs:[['Armi','Danni in mischia (arma a due mani)',['dps']],['Furia','Danni in mischia (due armi)',['dps']],['Protezione','Difensore',['tank']]],
    lvl:'Il livellamento più lento, circa il 12% più lungo della media (stima di LFCarry)',
    lp:12,
    raid:'Urlo di Battaglia agisce su tutta l’incursione',
    forever:'Più Rabbia, minaccia migliore su gruppi di bersagli, il talento Weapon Master. Furia e Sete di Sangue sono indebolite.' },
  { id:'paladin', n:'Paladino', roles:['tank','heal','dps'],
    specs:[['Sacro','Guaritore',['heal']],['Protezione','Difensore',['tank']],['Castigo','Danni in mischia',['dps']]],
    lvl:'Ritmo di livellamento nella media',
    lp:0,
    raid:'Benedizione dei Re ora è di base. Secondo le classifiche della beta, Protezione è tra i difensori più forti, mentre Castigo è sceso dopo la patch del 15 ottobre.',
    forever:'Assalto Sacro dal livello 6, Giudizio non consuma il sigillo. I Non Morti ora possono essere paladini, quindi la classe è arrivata nell’Orda.' },
  { id:'hunter', n:'Cacciatore', roles:['dps'],
    specs:[['Affinità Animale','Danni a distanza, molti danni dal famiglio',['dps']],['Precisione','Danni a distanza',['dps']],['Sopravvivenza','Mischia e distanza, trappole',['dps']]],
    lvl:'Il livellamento più veloce, circa l’8% più rapido della media (stima di LFCarry)',
    lp:-8,
    raid:'Aura di Precisione agisce su tutta l’incursione',
    forever:'Puoi giocare senza famiglio, le trappole funzionano in combattimento, le volpi sono arrivate come famiglia di famigli. Sopravvivenza può giocare in mischia.' },
  { id:'rogue', n:'Ladro', roles:['dps'],
    specs:[['Assassinio','Danni da veleno',['dps']],['Combattimento','Attacchi rapidi con l’arma',['dps']],['Scaltrezza','Imboscate, sanguinamenti',['dps']]],
    lvl:'Ritmo di livellamento nella media',
    lp:0,
    raid:'Puri danni in mischia, senza potenziamenti per l’incursione',
    forever:'Ora può usare asce a una mano. Assassinio si basa sui veleni, Scaltrezza su sanguinamenti e furtività.' },
  { id:'priest', n:'Sacerdote', roles:['heal','dps'],
    specs:[['Disciplina','Guaritore, scudi e assorbimento',['heal']],['Sacro','Guaritore',['heal']],['Ombra','Danni a distanza',['dps']]],
    lvl:'Circa il 5% più lento della media (stima di LFCarry)',
    lp:5,
    raid:'Spirito Divino ora è di base. I danni d’Ombra e Piaga Divoratrice (recupero di 24 s) sono stati potenziati dalla patch del 15 ottobre.',
    forever:'Protezione dalla Paura e Piaga Divoratrice sono disponibili dal livello 20 per tutte le razze. Ogni razza ha due incantesimi da sacerdote propri.' },
  { id:'shaman', n:'Sciamano', roles:['heal','dps','tank?'],
    specs:[['Elementale','Danni a distanza',['dps']],['Potenziamento','Danni in mischia. Il ruolo da difensore è ancora in dubbio',['dps','tank?']],['Rigenerazione','Guaritore',['heal']]],
    lvl:'Ritmo di livellamento nella media',
    lp:0,
    raid:'I totem Forza della Terra, Furia del Vento, Lingua di Fuoco e Grazia dell’Aria potenziano il proprio gruppo',
    forever:'I Nani ora possono essere sciamani, quindi la classe è arrivata nell’Alleanza. Getto di Lava è stata potenziata, Elementale è salito nelle classifiche dei danni.' },
  { id:'mage', n:'Mago', roles:['dps'],
    specs:[['Arcano','Danni esplosivi, molto mana',['dps']],['Fuoco','Critici e incendi',['dps']],['Gelo','Danni e controllo',['dps']]],
    lvl:'Il livellamento più veloce, circa l’8% più rapido della media, circa 12 ore risparmiate (stima di LFCarry)',
    lp:-8,
    raid:'Portali, cibo e acqua per il gruppo',
    forever:'Fuoco ha ottenuto Serie Bollente, Arcano Detonazione Arcana, Gelo Lancia di Ghiaccio. Palla di Fuocogelo è disponibile dal livello 40.' },
  { id:'warlock', n:'Stregone', roles:['dps'],
    specs:[['Afflizione','Danni da maledizioni e corruzione',['dps']],['Demonologia','Danni tramite demoni',['dps']],['Distruzione','Danni diretti da fuoco e ombra',['dps']]],
    lvl:'Ritmo di livellamento nella media',
    lp:0,
    raid:'Maestria oscura dà il 2–10% di danni Ombra, come in Classic (nella prima beta 1–5%)',
    forever:'Afflizione ha un nuovo incantesimo canalizzato, il demone resta con Sacrificio Demoniaco, Distruzione ha ottenuto Incenerimento e danni ad area.' },
  { id:'druid', n:'Druido', roles:['tank','heal','dps'],
    specs:[['Equilibrio','Danni a distanza',['dps']],['Aggressore Ferino','Difensore (orso) e danni in mischia (gatto)',['tank','dps']],['Rigenerazione','Guaritore, molte cure nel tempo',['heal']]],
    lvl:'Circa il 5% più lento della media (stima di LFCarry)',
    lp:5,
    raid:'Capobranco e Aura del Lunagufo agiscono su tutta l’incursione e si sommano',
    forever:'Ogni specializzazione ha un ruolo chiaro, le forme funzionano con pozioni e incantamenti delle armi. Puoi essere difensore, guaritore e combattente con un solo personaggio.' }
];
const ROLE_RU = { tank:'Difensore', heal:'Guaritore', dps:'Assaltatore', 'tank?':'Difensore (incerto)' };
const ri = r => `<svg class="ri" aria-hidden="true"><use href="#i-${r.replace('?','')}"/></svg>`;
const CCOL = { warrior:'#c79c6e', paladin:'#f58cba', hunter:'#abd473', rogue:'#fff569', priest:'#e8e8e8', shaman:'#2f8cf0', mage:'#40c7eb', warlock:'#8788ee', druid:'#ff7d0a' };
const BUFF = { warrior:'Urlo di Battaglia', paladin:'Benedizione dei Re', hunter:'Aura di Precisione', priest:'Parola del Potere: Fermezza, Spirito Divino', shaman:'Totem (Forza della Terra, Furia del Vento, Lingua di Fuoco, Grazia dell’Aria)', mage:'Intelletto Arcano, portali, cibo e acqua', druid:'Marchio Selvaggio, Capobranco, Aura del Lunagufo' };

const RACES = [
  { id:'human', n:'Umano', f:'alliance',
    cls:['warrior','paladin','hunter*','rogue','priest','mage','warlock'],
    rac:[['a','Volontà di Sopravvivenza','Rimuove lo stordimento'],['a','Percezione','Rivela i nemici invisibili per 20 s'],['p','Ruthless','+1% probabilità di critico'],['p','Spirito Umano','+10% spirito']],
    tip:'Per un Sacerdote Sacro lo spirito si traduce in cure, quindi un sacerdote Umano è ottimo per curare.' },
  { id:'dwarf', n:'Nano', f:'alliance',
    cls:['warrior','paladin','hunter','rogue','priest','shaman*'],
    rac:[['a','Forma di Pietra','Immunità a sanguinamenti, veleni e malattie per 8 s e danni fisici ridotti'],['a','Trova Tesori','Mostra i forzieri vicini e dà una probabilità di oggetti extra nella maggior parte dei forzieri'],['p','Artisan’s Precision','+1% di probabilità di colpire con incantesimi e attacchi'],['p','Big Game Hunter','+5% danni alle bestie']],
    tip:'Forma di Pietra è utile ai difensori e nel PvP.' },
  { id:'nightelf', n:'Elfo della Notte', f:'alliance',
    cls:['warrior','hunter','rogue','priest','druid'],
    rac:[['a','Luce di Elune','+10% probabilità di critico per 15 s'],['a','Fondersi nelle Ombre','Invisibilità sul posto'],['p','Rapidità','+2% di schivata e di velocità di corsa (Warcraft Tavern indica il 1% di schivata) {beta}'],['p','Spirito di Fuoco Fatuo','+75% di velocità di corsa da spirito (Warcraft Tavern indica il 25%) {beta}']],
    tip:'L’unica razza dell’Alleanza con il druido, a meno di scegliere gli Skyborne.' },
  { id:'gnome', n:'Gnomo', f:'alliance',
    cls:['warrior','rogue','mage','warlock','priest*'],
    rac:[['a','Artista della Fuga','Breve immunità a rallentamenti e immobilizzazioni'],['a','Eureka!','Per 8 s le abilità costano meno e sono più forti del 10% {beta}'],['p','Apertura Mentale','+5% mana, rabbia o energia massimi'],['p','Specializzazione: Ingegneria','I congegni d’ingegneria funzionano in modo più affidabile']],
    tip:'Apertura Mentale aiuta soprattutto le classi a energia.' },
  { id:'skyA', n:'Skyborne (Alleanza)', f:'alliance', paid:true, name:'Skyborne dell’High Order',
    cls:['warrior','hunter','rogue','mage','druid'],
    rac:[['a','Walk on Air','Plani per 10 s, senza danni da caduta'],['a','Read Ley Line','Rigenerazione di salute e mana +50% per 15 s. A una Ley Line anche Attuned per 1 ora: +100%, resta dopo la morte'],['p','Wind Blessed','+2% velocità d’attacco e degli incantesimi'],['p','Elemental Insight','+5% danni agli elementali']],
    tip:'Razza a pagamento: Heroic Pack da $29.99. Inizia nella zona di Zephras Isle (livelli 1–12).' },
  { id:'orc', n:'Orco', f:'horde',
    cls:['warrior','hunter','rogue','shaman','warlock','mage*'],
    rac:[['a','Furia Sanguinaria','+10% potenza d’attacco e potere magico per 15 s'],['a','Shatter Curse','Rimuove maledizioni e corruzione, −5% di danni magici subiti per 8 s'],['p','Command','+5% danni dei famigli di stregone e cacciatore'],['p','Audacia','Stordimenti più brevi del 20%']],
    tip:'Furia Sanguinaria offre una potente finestra di danni.' },
  { id:'undead', n:'Non Morto', f:'horde',
    cls:['warrior','rogue','mage','priest','warlock','paladin*'],
    rac:[['a','Volontà dei Reietti','Rimuove ammaliamento, paura e sonno'],['a','Cannibalismo','Ripristina nel tempo il 35% di salute e mana'],['p','Respiro Subacqueo','Respiri più a lungo sott’acqua'],['p','Tocco Tombale','Probabilità di sottrarre salute quando attacchi']],
    tip:'Nuova combinazione: un paladino per l’Orda, dove prima questa classe non esisteva.' },
  { id:'tauren', n:'Tauren', f:'horde',
    cls:['warrior','hunter','shaman','druid'],
    rac:[['a','Urto di Guerra','Stordisce i nemici vicini per 2 s, ricarica 90 s'],['a','Coltivazione','Fa crescere erbe raccoglibili senza Erbalismo, ricarica 15 min'],['p','Vagapianure','Finché ti muovi, la velocità di corsa sale del 2% per accumulo, fino a +60%. Non influisce sulla velocità in sella'],['p','Vigore','+5% salute']],
    tip:'L’unica razza dell’Orda con il druido, a meno di scegliere gli Skyborne.' },
  { id:'troll', n:'Troll', f:'horde',
    cls:['warrior','hunter','rogue','priest','shaman','mage','warlock*'],
    rac:[['a','Berserker','+10% di velocità di attacco e incantesimi per 12 s, ricarica di 3 min'],['a','Rapid Regeneration','Ripristina salute nel tempo'],['p','Cacciatore di Bestie','+5% danni alle bestie'],['p','Rigenerazione','La salute si rigenera anche in combattimento']],
    tip:'Più scelte di classe di tutta l’Orda: sette.' },
  { id:'skyH', n:'Skyborne (Orda)', f:'horde', paid:true, name:'Skyborne Windshaper',
    cls:['warrior','hunter','rogue','shaman','druid'],
    rac:[['a','Walk on Air','Plani per 10 s, senza danni da caduta'],['a','Skysight','+15% velocità di corsa per 15 s. A una Elemental Convergence anche Charged per 1 ora: +30%, resta dopo la morte'],['p','Wind Blessed','+2% velocità d’attacco e degli incantesimi'],['p','Elemental Insight','+5% danni agli elementali']],
    tip:'Razza a pagamento: Heroic Pack da $29.99. Solo nell’Orda può essere sciamano, solo nell’Alleanza mago.' }
];
RACES.forEach(r => { r.can = {}; r.cls.forEach(c => { const isNew = c.endsWith('*'); r.can[isNew ? c.slice(0,-1) : c] = isNew ? 'new' : 'ok'; }); });
const CL = Object.fromEntries(CLASSES.map(c => [c.id, c]));
const BETA = '<span class="beta-note">secondo i dati della beta</span>';
const BMARK = '{' + 'beta}';   // split so the guide build (which swaps the marker for the span everywhere) leaves it alone
const racx = s => String(s).split(BETA).join(BMARK).split(BMARK).map(esc).join(BETA);
const RC = Object.fromEntries(RACES.map(r => [r.id, r]));
const EN = {
  'Armi':'Armi','Furia':'Furia','Protezione':'Protezione','Sacro':'Sacro','Castigo':'Castigo',
  'Affinità Animale':'Affinità Animale','Precisione':'Precisione','Sopravvivenza':'Sopravvivenza',
  'Assassinio':'Assassinio','Combattimento':'Combattimento','Scaltrezza':'Scaltrezza',
  'Disciplina':'Disciplina','Ombra':'Ombra','Elementale':'Elementale','Potenziamento':'Potenziamento','Rigenerazione':'Rigenerazione',
  'Arcano':'Arcano','Fuoco':'Fuoco','Gelo':'Gelo','Afflizione':'Afflizione','Demonologia':'Demonologia','Distruzione':'Distruzione',
  'Equilibrio':'Equilibrio','Aggressore Ferino':'Aggressore Ferino',
  'Volontà di Sopravvivenza':'Volontà di Sopravvivenza','Percezione':'Percezione','Ruthless':'Ruthless','Spirito Umano':'Spirito Umano',
  'Forma di Pietra':'Forma di Pietra','Trova Tesori':'Trova Tesori','Earth Fury':'Earth Fury','Big Game Hunter':'Big Game Hunter',
  'Luce di Elune':"Luce di Elune",'Fondersi nelle Ombre':'Fondersi nelle Ombre','Rapidità':'Rapidità','Spirito di Fuoco Fatuo':'Spirito di Fuoco Fatuo',
  'Artista della Fuga':'Artista della Fuga','Eureka!':'Eureka!','Apertura Mentale':'Apertura Mentale','Specializzazione: Ingegneria':'Specializzazione: Ingegneria',
  'Walk on Air':'Walk on Air','Read Ley Line':'Read Ley Line','Wind Blessed':'Wind Blessed','Elemental Insight':'Elemental Insight','Skysight':'Skysight',
  'Furia Sanguinaria':'Furia Sanguinaria','Shatter Curse':'Shatter Curse','Savage':'Savage','Command':'Command','Audacia':'Audacia',
  'Volontà dei Reietti':'Volontà dei Reietti','Cannibalismo':'Cannibalismo','Respiro Subacqueo':'Respiro Subacqueo','Tocco Tombale':'Tocco Tombale',
  'Urto di Guerra':'Urto di Guerra','Coltivazione':'Coltivazione','Vagapianure':'Vagapianure','Vigore':'Vigore',
  'Berserker':'Berserker','Rapid Regeneration':'Rapid Regeneration','Cacciatore di Bestie':'Cacciatore di Bestie','Rigenerazione':'Rigenerazione'
};
RC.skyA.en = 'High Order Skyborne'; RC.skyH.en = 'Windshaper Skyborne';
const CX = {"warrior": {"armor": "Stoffa, cuoio, maglia; piastre dal livello 40 {beta}", "weapons": "Tutto tranne le bacchette; scudo", "resource": "Rabbia", "lvl": "Il livellamento più lento, circa il 12% più lungo della media (stima di LFCarry)", "group": ["Urlo di Battaglia agisce su tutta l’incursione", "Urlo Demoralizzante e Incrinatura sul boss", "Assalti Fendenti e Turbine per i combattimenti con più bersagli"], "pros": ["Miglior difensore e forti danni in mischia", "Buono per il PvP (Armi)", "Pochi tasti, facile da capire"], "cons": ["Livellamento più lento", "Molto dipendente dall’equipaggiamento", "Quasi niente autocure o controllo dei nemici"], "specs": [{"n": "Armi", "what": "Danni in mischia (arma a due mani)"}, {"n": "Furia", "what": "Danni in mischia (due armi)"}, {"n": "Protezione", "what": "Difensore"}]}, "paladin": {"armor": "Stoffa, cuoio, maglia; piastre dal livello 40; scudo {beta}", "weapons": "Asce, mazze, spade, armi ad asta dal livello 20 {beta}", "resource": "Mana", "lvl": "Ritmo di livellamento nella media", "group": ["Aure di gruppo: Devozione, Castigo, Concentrazione", "Aure di resistenza al Fuoco, al Gelo e all’Ombra per tutta l’incursione", "Benedizioni da un’ora, benedizioni superiori per un’intera classe", "Seal of Justice impedisce ai nemici di fuggire"], "pros": ["Tutti e tre i ruoli in un personaggio", "Forti potenziamenti di gruppo", "Piastre e un personaggio robusto"], "cons": ["Niente scatto, rallentamento o aumento di velocità", "Poco controllo oltre a Martello della Giustizia", "Castigo è sceso dopo la patch"], "specs": [{"n": "Sacro", "what": "Guaritore"}, {"n": "Protezione", "what": "Difensore"}, {"n": "Castigo", "what": "Danni in mischia"}]}, "hunter": {"armor": "Stoffa, cuoio; maglia dal livello 40 {beta}", "weapons": "Archi, balestre, armi da fuoco, asce, spade, armi ad asta", "resource": "Mana; il famiglio usa la Concentrazione", "lvl": "Il livellamento più veloce, circa l’8% più rapido della media (stima di LFCarry)", "group": ["Aura di Precisione aumenta i danni a distanza del gruppo", "Trappola Congelante: controllo affidabile", "Tiro Disorientante interrompe i lanci", "Aspetto del Branco velocizza tutto il gruppo in viaggio"], "pros": ["Livellamento più veloce", "Ottimo da solo", "Trappole e controllo dei nemici"], "cons": ["Zona morta ravvicinata fino a 8 metri", "Devi gestire il famiglio", "I talenti di Sopravvivenza avevano bug nella beta"], "specs": [{"n": "Affinità Animale", "what": "Danni a distanza, molti danni dal famiglio"}, {"n": "Precisione", "what": "Danni a distanza"}, {"n": "Sopravvivenza", "what": "Mischia e distanza, trappole"}]}, "rogue": {"armor": "Stoffa, cuoio", "weapons": "Pugnali, spade, mazze, armi da pugno, asce a una mano, da lancio", "resource": "Energia e punti combo", "lvl": "Ritmo di livellamento nella media", "group": ["Puri danni in mischia, senza potenziamenti per l’incursione", "Tramortimento, Accecamento e Colpo ai Reni: tanto controllo", "Calcio interrompe i lanci pericolosi"], "pros": ["Danni altissimi che crescono con l’equipaggiamento", "Furtività e tanto controllo dei nemici", "Libertà nella scelta dell’arma"], "cons": ["Molto dipendente dall’equipaggiamento", "Nessuna autocura", "Ti salvano solo Evasione e Sparizione"], "specs": [{"n": "Assassinio", "what": "Danni da veleno"}, {"n": "Combattimento", "what": "Attacchi rapidi con l’arma"}, {"n": "Scaltrezza", "what": "Imboscate, sanguinamenti"}]}, "priest": {"armor": "Stoffa", "weapons": "Pugnali, mazze, bastoni, bacchette", "resource": "Mana", "lvl": "Circa il 5% più lento della media (stima di LFCarry)", "group": ["Spirito Divino e Parola del Potere: Fermezza per tutta l’incursione", "Infusione di Potere potenzia un alleato", "Il guaritore principale del gruppo"], "pros": ["Sempre richiesto da un gruppo", "Cure o danni d’ombra", "Molte build"], "cons": ["Solo stoffa, fragile", "Pochi modi per muoversi in fretta", "La celerità aiuta poco gli incantesimi"], "specs": [{"n": "Disciplina", "what": "Guaritore, scudi e assorbimento"}, {"n": "Sacro", "what": "Guaritore"}, {"n": "Ombra", "what": "Danni a distanza"}]}, "shaman": {"armor": "Stoffa, cuoio; maglia dal livello 40; scudo {beta}", "weapons": "Mazze, asce, bastoni, armi da pugno, pugnali", "resource": "Mana", "lvl": "Ritmo di livellamento nella media", "group": ["I totem Forza della Terra, Furia del Vento, Lingua di Fuoco e Grazia dell’Aria potenziano il proprio gruppo", "Totem del Tremore rimuove paura, sonno e ammaliamento", "Totem che purificano veleni e malattie", "Epurazione rimuove i potenziamenti dai nemici"], "pros": ["Totem forti per il gruppo", "Livellamento mobile", "Nuovi talenti forti"], "cons": ["Nessun controllo forte", "Mana nei combattimenti lunghi", "Ruolo da difensore non ancora confermato"], "specs": [{"n": "Elementale", "what": "Danni a distanza"}, {"n": "Potenziamento", "what": "Danni in mischia. Il ruolo da difensore è ancora in dubbio"}, {"n": "Rigenerazione", "what": "Guaritore"}]}, "mage": {"armor": "Stoffa", "weapons": "Pugnali, spade, bastoni, bacchette", "resource": "Mana", "lvl": "Il livellamento più veloce, circa l’8% più rapido della media, circa 12 ore risparmiate (stima di LFCarry)", "group": ["Portali dal livello 40, teletrasporti dal 20", "Cibo e acqua per il gruppo", "Metamorfosi: controllo affidabile", "Remove Lesser Curse"], "pros": ["Livellamento più veloce", "Portali e cibo per tutti", "Tre alberi forti e diversi"], "cons": ["Solo stoffa, fragile", "Il mana finisce in fretta", "Danni ad area ridimensionati"], "specs": [{"n": "Arcano", "what": "Danni esplosivi, molto mana"}, {"n": "Fuoco", "what": "Critici e incendi"}, {"n": "Gelo", "what": "Danni e controllo"}]}, "warlock": {"armor": "Stoffa", "weapons": "Pugnali, spade, bastoni, bacchette", "resource": "Mana; Conversione Vitale trasforma la salute in mana", "lvl": "Ritmo di livellamento nella media", "group": ["Pietra della Salute e Pietra dell’Anima", "Rituale d’Evocazione: raduna il gruppo", "Maledizione delle Lingue rallenta i lanci del 60%", "Maledizione degli Elementi: più danni magici sul bersaglio"], "pros": ["Autosufficiente: un demone e Conversione Vitale", "Tanta utilità per il gruppo", "Forti danni nel tempo"], "cons": ["Fragile e poco mobile", "I danni impiegano tempo a salire", "Niente traslazione o scatto"], "specs": [{"n": "Afflizione", "what": "Danni da maledizioni e corruzione"}, {"n": "Demonologia", "what": "Danni tramite demoni"}, {"n": "Distruzione", "what": "Danni diretti da fuoco e ombra"}]}, "druid": {"armor": "Stoffa, cuoio", "weapons": "Pugnali, mazze, bastoni, armi da pugno, armi ad asta dal livello 20 {beta}", "resource": "Mana; Rabbia in Forma d’Orso, Energia in Forma Felina", "lvl": "Circa il 5% più lento della media (stima di LFCarry)", "group": ["Capobranco e Aura del Lunagufo agiscono su tutta l’incursione e si sommano", "Pronto Ritorno: resurrezione in combattimento", "Innervazione restituisce mana a un guaritore", "Rimuove maledizioni e veleni"], "pros": ["Tutti e tre i ruoli in un personaggio", "Ottima mobilità", "Resurrezione in combattimento"], "cons": ["Niente blocco né parata per l’orso", "Gli effetti di cura nel tempo sono più difficili da seguire", "I numeri finali in incursione non sono ancora noti"], "specs": [{"n": "Equilibrio", "what": "Danni a distanza"}, {"n": "Aggressore Ferino", "what": "Difensore (orso) e danni in mischia (gatto)"}, {"n": "Rigenerazione", "what": "Guaritore, molte cure nel tempo"}]}};
const HC = {"tx":{"title":"Il mio personaggio","lead":"Senza login né password: scegli classe, specializzazione e razza, e il sito si adatta a te.","local":"Salvato solo in questo browser.","none":"Ancora nessun personaggio","create":"Crea un personaggio","edit":"Modifica","reset":"Elimina personaggio","resetQ":"Eliminare il personaggio da questo browser?","steps":["Schieramento","Classe e specializzazione","Razza","Aspetto","Dettagli"],"side":"Per chi giochi?","cls":"Classe","spec":"Specializzazione","race":"Razza","bestFor":"Razza migliore per %s","best":"la migliore","paid":"a pagamento","sex":"Sesso","m":"Maschile","f":"Femminile","bg":"Sfondo del ritratto","lvl":"Livello","reg":"Regione","lvlReg":"Livello e regione","regs":{"us":"Americhe e Oceania","eu":"Europa","kr":"Corea","tw":"Taiwan"},"p1":"Professione 1","p2":"Professione 2","secP":"Professioni secondarie","noP":"Nessuna","role":"Ruolo","back":"Indietro","next":"Continua","done":"Fatto","cancel":"Annulla","later":"Puoi compilarlo più tardi.","levelN":"Livello %n","build":"La mia build di talenti","buildD":"Talenti %s per livello.","pairs":"Coppie di professioni","pairsD":"Quali professioni si addicono alla tua classe.","bestR":"Razze migliori","bestRD":"Razza per la tua classe in entrambe le fazioni.","lvlG":"Livellamento della classe","lvlGD":"Percorso e talenti 1–60.","day1":"Giorno 1 per il tuo personaggio","day1D":"La checklist del lancio con la tua classe e razza.","play":"In gioco","playD":"Zone e spedizioni per il tuo livello, timer, radio.","dung":"Spedizioni per il tuo livello","dungNo":"Indica il tuo livello e sceglieremo le spedizioni.","dungFirst":"Le prime spedizioni si aprono al livello 13.","resetH":"Reset settimanale","resetIn":"tra %s","resetNote":"Blizzard non ha ancora annunciato l’orario di reset di Forever. Mostrato come nelle altre versioni di WoW di questa regione: verificheremo al lancio.","resetUnk":"Confermeremo l’orario di reset di questa regione al lancio.","resetNoReg":"Indica la tua regione per vedere il reset settimanale.","resetWhy":"Le incursioni aprono il 09.12 e hanno un blocco settimanale.","lfg":"Testo per cercare un gruppo","lfgD":"Incollalo nella chat LookingForGroup. Nomi come nel gioco.","lfgP":{"tank":"%c difensore cerca gruppo","heal":"%c guaritore cerca gruppo","dps":"%c cerca gruppo"},"lfgT":"%p: %d, livello %l.","lfgT0":"%p.","allD":"Tutte le spedizioni","copy":"Copia","copied":"Copiato","sync":"Sincronizza tra dispositivi","syncD":"Il login serve solo a questo: il personaggio sarà sul telefono e sul PC, e la lettera del lancio arriva per e-mail se ti iscrivi.","yourCls":"Il tuo %s","bTalents":"Talenti","bSpec":"Build: %s","bLevel":"Livellamento","bGroup":"Gruppo","bNews":"Notizie","copiedT":"Copiato: %s","profsL":"Professioni","day1n":"Giorno 1: %n di %t","collect":"Crea il tuo personaggio","collectD":"Classe, specializzazione e razza: talenti, livellamento, gruppo e notizie della tua classe.","change":"Cambia","allSet":"Tutte le impostazioni","close":"Chiudi","mine":"Riguarda la tua classe","share":"Condividi","linkCopied":"Link copiato","make":"Rendilo il mio personaggio","made":"È il tuo personaggio","plaqueH":"Il mio personaggio","plaqueD":"Classe, specializzazione e razza in un minuto, poi la tua build, le professioni e le spedizioni.","day1Mine":"Per il tuo personaggio","ckClass":"La tua specializzazione, %s: la build di talenti per livello.","ckRaceOk":"%r è la razza migliore per la tua specializzazione.","ckRaceAlt":"Razza migliore per la tua specializzazione: %r.","ckProfs":"Coppie di professioni per %s.","ckStart":"Livellamento %s: percorso e primi talenti.","ckPing":"La tua regione: %s.","or":"o"},"best":{"warrior":{"alliance":{"*":[["human","nightelf"],"Umano: +1% di critico con qualsiasi arma. Elfo della Notte: +10% di critico per 15 s. Le fonti sono divise quasi a metà."],"protection":[["dwarf"],"Forma di Pietra riduce i danni fisici del 10% e rimuove i sanguinamenti."]},"horde":{"*":[["orc"],"Furia Sanguinaria: +10% di potere d’attacco per 15 s. Prima delle modifiche alle razze del 26.10 tutte le fonti la mettevano al primo posto."],"protection":[["tauren"],"Vigore dà +5% di salute, Urto di Guerra stordisce i nemici vicini."]}},"paladin":{"alliance":{"*":[["human"],"Ruthless potenzia colpi e incantesimi, Volontà di Sopravvivenza rimuove gli stordimenti."],"protection":[["dwarf"],"Forma di Pietra e Artisan’s Precision: +1% di probabilità di colpire."]},"horde":{"*":[["undead"],"Nell’Orda solo il Non Morto può essere paladino. Cannibalismo ripristina mana, Volontà dei Reietti rimuove la paura."]}},"hunter":{"alliance":{"*":[["human","nightelf"],"Umano: +1% di critico, e il famiglio lo eredita. Elfo della Notte: Luce di Elune e Fondersi nelle Ombre."]},"horde":{"*":[["orc","troll"],"Orco: Furia Sanguinaria e Command (+5% danni del famiglio). Troll: +5% di danni contro le bestie."]}},"rogue":{"alliance":{"*":[["nightelf"],"Fondersi nelle Ombre ora riduce la minaccia anche in combattimento, più Grazia di Elune e Rapidità."]},"horde":{"*":[["orc"],"Furia Sanguinaria: +10% di potere d’attacco per 15 s."]}},"priest":{"alliance":{"*":[["gnome"],"Tutte le fonti la scelgono: Eureka! potenzia anche Parola del Potere: Scudo, Inquisitive Mind dà +5% di mana."]},"horde":{"*":[["undead","troll"],"Le fonti sono divise. Il Non Morto è più forte nel PvP: Volontà dei Reietti rimuove paura, sonno e ammaliamento."]}},"shaman":{"alliance":{"*":[["dwarf"],"Nell’Alleanza solo il Nano può essere sciamano: Forma di Pietra e Artisan’s Precision (+1% di probabilità di colpire)."]},"horde":{"*":[["orc"],"Furia Sanguinaria dà potere d’attacco e potere magico: va bene sia per Elementale sia per Potenziamento."],"restoration":[["troll"],"Per un guaritore una fonte consiglia il Troll: Berserker, +10% di velocità di lancio per 12 s."]}},"mage":{"alliance":{"*":[["gnome"],"Eureka! per 8 s, Inquisitive Mind: +5% di mana, Artista della Fuga spezza le radici."]},"horde":{"*":[["orc"],"L’orco mago è una nuova combinazione di Forever: Furia Sanguinaria ora dà potere magico."]}},"warlock":{"alliance":{"*":[["gnome","human"],"Gnomo: Eureka! e Inquisitive Mind. Umano: i danni periodici possono essere critici e Ruthless dà +1% di critico."]},"horde":{"*":[["orc","undead"],"Orco: Furia Sanguinaria dà potere magico. Il Non Morto si sceglie più spesso nel PvP."]}},"druid":{"alliance":{"*":[["nightelf"],"Grazia di Elune: +10% di critico per 15 s, e Rapidità."]},"horde":{"*":[["tauren"],"Vigore: +5% di salute, Urto di Guerra funziona anche nelle forme."]}}},"sid":{"warrior":["arms","fury","protection"],"paladin":["holy","protection","retribution"],"hunter":["beast-mastery","marksmanship","survival"],"rogue":["assassination","combat","subtlety"],"priest":["discipline","holy","shadow"],"shaman":["elemental","enhancement","restoration"],"mage":["arcane","fire","frost"],"warlock":["affliction","demonology","destruction"],"druid":["balance","feral","restoration"]},"sn":{"warrior":["Armi","Furia","Protezione"],"paladin":["Sacro","Protezione","Castigo"],"hunter":["Affinità Animale","Precisione","Sopravvivenza"],"rogue":["Assassinio","Combattimento","Scaltrezza"],"priest":["Disciplina","Sacro","Ombra"],"shaman":["Elementale","Potenziamento","Rigenerazione"],"mage":["Arcano","Fuoco","Gelo"],"warlock":["Afflizione","Demonologia","Distruzione"],"druid":["Equilibrio","Aggressore Ferino","Rigenerazione"]},"fn":{"alliance":"Alleanza","horde":"Orda"},"reset":{"us":[2,15],"eu":[3,4],"kr":null,"tw":null},"rn":{"human":"Umano","dwarf":"Nano","nightelf":"Elfo della Notte","gnome":"Gnomo","skyA":"Skyborne dell’High Order","orc":"Orco","undead":"Non Morto","tauren":"Tauren","troll":"Troll","skyH":"Skyborne Windshaper"},"rf":{"human":"alliance","dwarf":"alliance","nightelf":"alliance","gnome":"alliance","skyA":"alliance","orc":"horde","undead":"horde","tauren":"horde","troll":"horde","skyH":"horde"},"cn":{"warrior":"Guerriero","paladin":"Paladino","hunter":"Cacciatore","rogue":"Ladro","priest":"Sacerdote","shaman":"Sciamano","mage":"Mago","warlock":"Stregone","druid":"Druido"},"cen":{"warrior":"Warrior","paladin":"Paladin","hunter":"Hunter","rogue":"Rogue","priest":"Priest","shaman":"Shaman","mage":"Mage","warlock":"Warlock","druid":"Druid"}};
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

const CPROF = {"warrior": [["Livellamento: Forgiatura + Estrazione", ""], ["Livello 60: Ingegneria + Estrazione", "Il fabbro si veste di piastre e armi, e molte ricette sono personali. L’ingegnere ottiene granate e congegni che al guerriero mancano."]], "paladin": [["Livellamento: Forgiatura + Estrazione", ""], ["Livello 60: Protezione, Castigo: Ingegneria + Estrazione. Sacro: Alchimia + Erbalismo", "Sacro consuma molto mana: le pozioni sono tue, e il Mana Well dell’accampamento sostituisce Benedizione della Saggezza."]], "hunter": [["Livellamento: Conciatura + Scuoiatura", ""], ["Livello 60: Ingegneria + Estrazione", "Il conciatore si cuce da solo cuoio e maglia e Armor Kit. L’ingegnere fa mirini e armi da fuoco."]], "rogue": [["Livellamento: Conciatura + Scuoiatura", ""], ["Livello 60: Ingegneria + Estrazione", "Il cuoio è tuo, e la Camp Tent dà riposo. L’Ingegneria è la professione principale per il PvP."]], "priest": [["Livellamento: Sartoria + Incantamento", ""], ["Livello 60: Sartoria + Ingegneria o Incantamento", "Il sarto fa cinture con potenza degli incantesimi dal livello 10, l’incantatore bacchette con potenza degli incantesimi dal livello 5. Ciò che è cucito si disincanta in materiali."]], "shaman": [["Livellamento: Conciatura + Scuoiatura", ""], ["Livello 60: Alchimia + Erbalismo", "Il conciatore fa oggetti con potenza degli incantesimi per Elementale e Rigenerazione e equipaggiamento per Potenziamento. In incursione e in gruppo servono pozioni."]], "mage": [["Livellamento: Sartoria + Incantamento", ""], ["Livello 60: Sartoria + Incantamento; per il PvP e i grandi gruppi di nemici Ingegneria + Estrazione", "Il sarto dà equipaggiamento precoce con potenza degli incantesimi, e ciò che è cucito si disincanta. Le granate dell’ingegnere tengono ferme le grandi folle di nemici."]], "warlock": [["Livellamento: Sartoria + Incantamento", ""], ["Livello 60: Sartoria + Alchimia", "La Faction Banner del sarto dà Spirito per Conversione Vitale. L’Alchimia sono pozioni e oro."]], "druid": [["Livellamento: Conciatura + Scuoiatura o Erbalismo", ""], ["Livello 60: Alchimia + Erbalismo", "Le erbe si raccolgono in Forma Celere, le pozioni si bevono in qualsiasi forma. Mana Well e Incense Candle servono per Equilibrio e Rigenerazione."]]};   /* recommended profession pairs per class, already in the page language (build.class_profs) */
const $ = s => document.querySelector(s);
const ROOT = '../../', HOME = '../';
function esc(s) { return String(s).replace(/[&<>"]/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m])); }
function raceName(r) { return r.name || r.n; }
function syncSeg(id, v) { document.querySelectorAll(`#${id} button`).forEach(b => b.setAttribute('aria-pressed', b.dataset.v === String(v))); }
const FAC = { alliance: 'Alleanza', horde: 'Orda' };
const BSLUG = { skyA: 'skyborne-a', skyH: 'skyborne-h' };   // race id -> url part of the share page (tools/make_build_cards.py SLUG)
const RSLUG = { human: 'human', dwarf: 'dwarf', nightelf: 'night-elf', gnome: 'gnome', skyA: 'skyborne-alliance', orc: 'orc', undead: 'undead', tauren: 'tauren', troll: 'troll', skyH: 'skyborne-horde' };
const PAINTED = ["druid-nightelf", "druid-tauren", "hunter-nightelf", "hunter-orc", "mage-gnome", "mage-orc", "paladin-human", "paladin-undead", "priest-gnome", "priest-undead", "rogue-nightelf", "rogue-orc", "shaman-dwarf", "shaman-orc", "warlock-gnome", "warlock-orc", "warrior-human", "warrior-orc"];   // class x race paintings that exist (build_tools.painted): the player's own race is drawn, never the best race of the side
const unitArt = (p, ext) => `${ROOT}assets/art/${PAINTED.includes(p.cls + '-' + p.race) ? p.cls + '-' + p.race : RSLUG[p.race]}-360.${ext}${PV}`;
const classUrl = id => `${HOME}classes/${id}/`, raceUrl = id => `${HOME}races/${RSLUG[id]}/`;
const PV = /*PV*/'?v=03c9d4a0';   // ?v= of the class and race portraits (build.art_version)
const porId = (id, f) => (window.GabellaPor ? GabellaPor.id(id, f) : id);   // a class: the portrait of side f, else of the reader's side (build.por_js)
const art = (id, ext = 'webp', f) => `${ROOT}assets/art/${porId(id, f)}-360.${ext}${PV}`;
async function copyTo(text, msgEl, ok) {
  try { await navigator.clipboard.writeText(text); msgEl.textContent = ok; } catch (e) { msgEl.textContent = 'Impossibile copiare, seleziona il testo e premi Ctrl+C'; }
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
    out.push((groups > 1 ? `Gruppo ${g + 1}: ` : '') + part.map(p => `${p.name ? p.name + ' — ' : ''}${raceName(RC[p.race])} ${CL[p.cls].n} (${ROLE_RU[p.role]})`).join(', '));
  }
  return out.length ? out.join('\n') + `\n${FAC[R.f]}, ${R.size}` : '';
}

/* LFG line: the dungeon or raid, the missing roles, the play style and a short link (#t=); kept under the 255-byte chat limit */
const LFG = {"d": [["Baratro di Fiamma Furente", 13, 18, "horde"], ["Hall of Thanes", 13, 18, 0], ["Rovine di Lordaeron", 15, 20, 0], ["Miniere della Morte", 15, 22, 0], ["Caverna dei Lamenti", 17, 24, 0], ["Forte di Zannascura", 20, 26, 0], ["Abissi di Fondocupo", 22, 28, 0], ["Segrete di Roccavento", 25, 29, "alliance"], ["Excavation Site: Wetlands", 26, 31, 0], ["City of Dalaran", 28, 33, 0], ["Gnomeregan", 29, 38, 0], ["Gallerie di Lamaspina", 29, 38, 0], ["Monastero Scarlatto: Cimitero", 30, 38, 0], ["Monastero Scarlatto: Biblioteca", 33, 41, 0], ["The Drowned City", 35, 40, 0], ["Monastero Scarlatto: Armeria", 36, 44, 0], ["Uldaman", 36, 45, 0], ["Sotterranei di Lamaspina", 37, 46, 0], ["Monastero Scarlatto: Cattedrale", 38, 46, 0], ["Zul’farrak", 40, 47, 0], ["Krol’dok Stronghold", 40, 45, 0], ["Maraudon", 45, 51, 0], ["Alcaz Island Prison", 48, 53, 0], ["Temple of Atal’Hakkar", 50, 55, 0], ["Sotterranei di Roccianera", 52, 60, 0], ["Blackmaw Hold", 55, 60, 0], ["Bastioni di Roccianera Inferiori", 57, 60, 0], ["Maglio Infausto: Est", 58, 60, 0], ["Shaper’s Terrace", 58, 60, 0], ["Stratholme: vivi", 58, 60, 0], ["Stratholme: non morti", 58, 60, 0], ["Scholomance", 58, 60, 0], ["Bastioni di Roccianera Superiori", 60, 60, 0], ["Maglio Infausto: Ovest", 60, 60, 0], ["Maglio Infausto: Nord", 60, 60, 0]], "r": {"10": "Barrow Deeps", "20": "Sommità di Hyjal", "40": "Antro di Onyxia"}};   // dungeons [name, min, max, entrance faction] and raids {size: name} in the client's language (build_tools)
const CHAT_MAX = 255, CANON = 'https://gabella.site/wow/it/tools/'.replace(/^https?:\/\//, '');
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
  const head = (L.d ? '%d — cerchiamo: %n.' : 'Gruppo cerca: %n.').replace('%d', L.d).replace('%n', roles);
  const parts = [head, L.s ? 'Stile: %s.'.replace('%s', L.s) : '', CANON + shortHash()].filter(Boolean);
  const bytes = t => new TextEncoder().encode(t).length;
  let text = parts.join(' ');
  if (bytes(text) > CHAT_MAX) text = parts.slice(0, -1).join(' ');   // a long raid code would not fit: the link goes first
  return text;
}
function renderLfg() {
  const places = lfgPlaces(), sel = $('#lfgD');
  if (!places.some(p => p[0] === L.d)) L.d = R.size === 5 ? '' : (places[0] || [''])[0];
  $('#lfgDL').textContent = R.size === 5 ? 'Spedizione' : 'Incursione';
  sel.innerHTML = (R.size === 5 ? '<option value="">Qualsiasi spedizione</option>' : '') + places.map(([v, t]) => `<option value="${esc(v)}"${v === L.d ? ' selected' : ''}>${esc(t)}</option>`).join('');
  syncSeg('lfgS', L.s);
  const text = lfgText();
  $('#rLfg').value = text;
  $('#rCopyLfg').disabled = !text;
  $('#rLfgMsg').textContent = text ? lfgLen(text) : R.s.some(Boolean) ? 'Tutti i posti sono occupati.' : 'Aggiungi almeno un giocatore al gruppo.';
}
function lfgLen(t) { return 'Caratteri: %n su %m (limite di una riga di chat).'.replace('%n', t.length).replace('%m', CHAT_MAX); }

function unitHTML(p, i) {
  const cls = R.moving === i ? ' src' : '';
  if (!p) return `<button type="button" class="unit empty${cls}" data-i="${i}"><span class="up" aria-hidden="true">+</span><span class="ub"><b>Posto libero</b><span>Clicca per aggiungere un giocatore</span></span></button>`;
  const c = CL[p.cls], r = RC[p.race];
  return `<button type="button" class="unit${cls}" data-i="${i}" draggable="true" style="--cc:${CCOL[p.cls]};--pc:${power(p)}" aria-label="${esc((p.name || `Giocatore ${i + 1}`) + ', ' + raceName(r) + ' ' + c.n + ', ' + ROLE_RU[p.role])}">
    <span class="up"><picture><source type="image/avif" srcset="${unitArt(p, 'avif')}"><img src="${unitArt(p, 'webp')}" width="360" height="482" alt="" loading="lazy" decoding="async"></picture></span>
    <span class="ub"><span class="un"><span class="ur" title="${ROLE_RU[p.role]}">${ri(p.role)}</span><b>${esc(p.name || c.n)}</b><small>${esc(raceName(r))} · ${esc(c.n)}</small></span><span class="hp"><i></i></span><span class="mp"></span></span></button>`;
}
function cellHTML(p, i) {
  const cls = R.moving === i ? ' src' : '';
  if (!p) return `<button type="button" class="rc empty${cls}" data-i="${i}" aria-label="Posto libero ${i + 1}"><span aria-hidden="true">+</span>Aggiungi</button>`;
  const c = CL[p.cls], r = RC[p.race];
  return `<button type="button" class="rc${cls}" data-i="${i}" draggable="true" style="--cc:${CCOL[p.cls]};--pc:${power(p)}" aria-label="${esc((p.name || `Giocatore ${i + 1}`) + ', ' + raceName(r) + ' ' + c.n + ', ' + ROLE_RU[p.role])}" title="${esc(raceName(r) + ' · ' + c.n + ' · ' + ROLE_RU[p.role])}"><b>${esc(p.name || c.n)}</b><small>${esc(p.name ? c.n : raceName(r))}</small>${ri(p.role)}</button>`;
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
      const st = n && (!c.tank || !c.heal) ? `<span class="warn">${!c.tank ? 'senza difensore' : 'senza guaritore'}</span>` : `<span>${n}/5</span>`;
      h += `<div class="rg"><div class="rg-h"><b>Gruppo ${g + 1}</b>${st}</div>${part.map((p, k) => cellHTML(p, g * PARTY + k)).join('')}</div>`;
    }
    $('#rview').innerHTML = `<div class="rgrid" style="--gc:${Math.min(groups, 8)}">${h}</div>`;
  }
  const hint = $('#rhint');
  hint.classList.toggle('on', R.moving >= 0);
  hint.innerHTML = R.moving >= 0 ? `Scegli un nuovo posto per il giocatore ${R.moving + 1}. <button type="button" id="mvCancel">Annulla</button>` : '';

  const list = R.s.filter(Boolean), cnt = countRoles(list), rec = REC[R.size];
  $('#rRoles').innerHTML = RR.map((x, k) => `<span class="${list.length && cnt[x] < rec[k] ? 'low' : ''}">${ri(x)}${ROLE_RU[x]} <b>${cnt[x]}</b> / ${rec[k]}</span>`).join('');
  $('#rTip').textContent = R.size === 5 ? 'Una spedizione richiede un difensore, un guaritore e tre assaltatori.' : `Regola pratica per le incursioni: difensori ${rec[0]}, guaritori ${rec[1]}, il resto danni. Il numero esatto dipende dai boss.`;
  const have = new Set(list.map(p => p.cls));
  $('#rBuffs').innerHTML = CLASSES.filter(c => BUFF[c.id]).map(c => `<li class="${have.has(c.id) ? '' : 'off'}" style="--cc:${CCOL[c.id]}"><span class="cdot"></span><span><b>${esc(c.n)}:</b> ${esc(BUFF[c.id])}</span></li>`).join('');
  const n = list.length;
  $('#rRaids').innerHTML = n ? RAIDS.map(([size, name]) => `<li class="${n >= size ? 'good' : ''}">${n >= size ? `Incursione da ${size} (${name}): giocatori sufficienti.` : `Incursione da ${size} (${name}): ne mancano ${size - n}.`}</li>`).join('') : '<li>Ancora nessuno. Premi «Il mio personaggio», «Riempi i vuoti» o un riquadro libero.</li>';

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
    msg.innerHTML = 'Nessun personaggio per ora. <a href="../character/" id="rMake">Crea il tuo personaggio</a>';
    $('#rMake').onclick = e => { if (window.GabellaHero) { e.preventDefault(); GabellaHero.open(); } };
    return;
  }
  const f = RC[h.race].f, role = RR.includes(h.role) ? h.role : roleOpts(CL[h.cls])[0];
  if (f !== R.f) {
    if (R.s.some(Boolean)) { msg.textContent = 'Il tuo personaggio è dell’altra fazione: cambia fazione sopra i riquadri.'; return; }
    R.f = f;
  }
  if (R.s.some(p => p && p.race === h.race && p.cls === h.cls && p.role === role && !p.name)) { msg.textContent = 'Il tuo personaggio è già nella composizione.'; return; }
  let i = R.s.findIndex(p => !p); if (i < 0) i = 0;
  R.s[i] = { race: h.race, cls: h.cls, role, name: '' };
  msg.textContent = ''; R.moving = -1; renderRaid();
};
$('#rClear').onclick = () => { R.s = Array(R.size).fill(null); R.moving = -1; renderRaid(); };
$('#rCopyLink').onclick = () => copyTo(teamLink(), $('#rMsg'), 'Link copiato');
$('#rCopyText').onclick = () => copyTo(teamText(), $('#rMsg'), 'Gruppo copiato');
$('#lfgD').onchange = e => { L.d = e.target.value; renderLfg(); };
$('#lfgS').addEventListener('click', e => { const b = e.target.closest('button'); if (b) { L.s = L.s === b.dataset.v ? '' : b.dataset.v; renderLfg(); } });
$('#rCopyLfg').onclick = () => { const t = lfgText(); copyTo(t, $('#rLfgMsg'), 'Testo copiato. ' + lfgLen(t)); };

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
  $('#edT').textContent = `Giocatore ${edI + 1}` + (R.size > 5 ? ` · Gruppo ${Math.floor(edI / PARTY) + 1}` : '');
  $('#edRace').innerHTML = RACES.filter(r => r.f === R.f).map(r => `<option value="${r.id}"${r.id === p.race ? ' selected' : ''}>${esc(raceName(r))}${r.paid ? ' (a pagamento)' : ''}</option>`).join('');
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
  else box.innerHTML = ['alliance', 'horde'].map(f => `<div class="rside ${f}"><h3>${FAC[f]}</h3>${RACES.filter(r => r.f === f).map(r => { const k = sel.indexOf(r.id); return `<button type="button" class="rp" data-id="${r.id}" aria-pressed="${k >= 0}">${esc(raceName(r))}${r.paid ? '<span class="tag paid">a pagamento</span>' : ''}<span class="no">${k + 1}</span></button>`; }).join('')}</div>`).join('');
  $('#cNote').textContent = `Selezionati ${sel.length} su 3`;
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
const ul = (items, cls) => items.length ? `<ul${cls ? ` class="${cls}"` : ''}>${items.map(x => `<li>${x}</li>`).join('')}</ul>` : '<span class="none">Nessuna</span>';
const row = (lab, vals, extra) => `<div class="crow${extra ? ' ' + extra : ''}"><div class="lab${extra === 'tiprow' ? ' tl' : ''}">${lab}</div>${vals.map(v => `<div class="val">${v}</div>`).join('')}</div>`;
function renderCmp() {
  const out = [];
  if (C.mode === 'class') {
    const ids = C.cls;
    out.push(`<div class="crow chead"><div class="lab"></div>${ids.map(id => `<div class="val" style="--cc:${CCOL[id]}"><picture><source type="image/avif" srcset="${art(id, 'avif')}"><img src="${art(id)}" width="360" height="482" alt="" loading="lazy" decoding="async"></picture><b>${esc(CL[id].n)}</b><a href="${classUrl(id)}">Pagina della classe<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>`).join('')}</div>`);
    out.push(row('Ruoli', ids.map(id => CL[id].roles.map(r => `<span class="role">${ri(r)}${ROLE_RU[r]}</span>`).join(''))));
    out.push(row('Armatura', ids.map(id => racx(CX[id].armor))));
    out.push(row('Armi', ids.map(id => racx(CX[id].weapons))));
    out.push(row('Risorsa', ids.map(id => esc(CX[id].resource))));
    out.push(row('Livellamento', ids.map(id => esc(CX[id].lvl))));
    out.push(row('Specializzazioni', ids.map(id => ul(CX[id].specs.map(s => `<b>${esc(s.n)}</b>${SPEC_SEP}<span class="sub">${esc(s.what)}</span>`)))));
    out.push(row('Buff d’incursione', ids.map(id => BUFF[id] ? esc(BUFF[id]) : '<span class="none">Nessuna</span>')));
    out.push(row('In gruppo', ids.map(id => ul(CX[id].group.map(esc)))));
    out.push(row('Professioni', ids.map(id => ul(CPROF[id].map(p => `<b>${esc(p[0])}</b>${p[1] ? `<br><span class="sub">${esc(p[1])}</span>` : ''}`)) + `<a class="cgo" href="${HOME}guides/professions/#pairs=${id}">Oggetti da accampamento e competenza<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a>`)));
    out.push(row('Punti di forza', ids.map(id => ul(CX[id].pros.map(esc), 'plus'))));
    out.push(row('Punti deboli', ids.map(id => ul(CX[id].cons.map(esc), 'minus'))));
    ['alliance', 'horde'].forEach(f => out.push(row(`Razze: ${FAC[f]}`, ids.map(id => { const rs = RACES.filter(r => r.f === f && r.can[id]); return rs.length ? rs.map(r => `<a href="${raceUrl(r.id)}">${esc(raceName(r))}</a>`).join(', ') : '<span class="none">Nessuna</span>'; }))));
  } else {
    const ids = C.race;
    out.push(`<div class="crow chead"><div class="lab"></div>${ids.map(id => { const r = RC[id]; return `<div class="val race ${r.f}"><span class="fx">${FAC[r.f]}${r.paid ? ' · a pagamento' : ''}</span><b>${esc(raceName(r))}</b><a href="${raceUrl(id)}">Pagina della razza<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>`; }).join('')}</div>`);
    out.push(row('Classi', ids.map(id => ul(Object.keys(RC[id].can).map(c => `<span style="color:${CCOL[c]}">●</span> ${esc(CL[c].n)}${RC[id].can[c] === 'new' ? ' <span class="tag new">nuova</span>' : ''}`)))));
    out.push(row('Abilità attive', ids.map(id => ul(RC[id].rac.filter(x => x[0] === 'a').map(x => `<b>${esc(x[1])}</b><br><span class="sub">${racx(x[2])}</span>`)))));
    out.push(row('Abilità passive', ids.map(id => ul(RC[id].rac.filter(x => x[0] === 'p').map(x => `<b>${esc(x[1])}</b><br><span class="sub">${racx(x[2])}</span>`)))));
    out.push(row('Consiglio', ids.map(id => esc(RC[id].tip)), 'tiprow'));
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
function facName(f) { return f === 'alliance' ? 'Alleanza' : 'Orda'; }
function bi(ru) { return EN[ru] && EN[ru] !== ru ? `${esc(ru)} <span class="en">(${esc(EN[ru])})</span>` : esc(ru); }
function raceEn(r) { return r.en ? ` <span class="en">/ ${esc(r.en)}</span>` : ''; }
const tipBox = h => `<div class="tipbox"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg><p><span class="tl">Consiglio</span>${h}</p></div>`;
function face(id, cc, cls = '', title = '', f) { return `<span class="av ${cls}" style="--cc:${cc}"${title ? ` title="${esc(title)}"` : ''}><img src="${ROOT}assets/art/${porId(id, f)}-face.webp${PV}" width="160" height="160" alt="" loading="lazy" decoding="async"></span>`; }
function lvlMeter(c) {
  const p = c.lp || 0, w = Math.min(Math.abs(p) / 12 * 46, 46);
  const label = p < 0 ? `Più veloce del ${-p}%` : p > 0 ? `Più lento del ${p}%` : 'Ritmo nella media';
  const bar = p ? `<i class="${p > 0 ? 'slow' : ''}" style="${p < 0 ? 'right' : 'left'}:50%;width:${w}%"></i>` : '';
  return `<span class="lvl"><span>${label}</span><span class="bar" role="img" aria-label="${label}">${bar}</span><span class="scale" aria-hidden="true"><span>più veloce</span><span>più lento</span></span></span>`;
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
  let h = '<thead><tr><th scope="col">Razza</th>';
  CLASSES.forEach(c => { h += `<th scope="col" class="${roleMatch(c, state.r) ? '' : 'dim'}${c.id === state.cls ? ' selc' : ''}">${face(c.id, CCOL[c.id])}${esc(c.n)}</th>`; });
  h += '</tr></thead><tbody>';
  ['alliance', 'horde'].forEach(f => {
    const rows = RACES.filter(r => r.f === f && raceVisible(r));
    if (!rows.length) return;
    h += `<tr class="fh ${f}"><th colspan="${CLASSES.length + 1}" scope="rowgroup"><span class="f ${f}"></span>${facName(f)}</th></tr>`;
    rows.forEach(r => {
      h += `<tr class="${r.id === state.race ? 'rowsel' : ''}"><th scope="row"><span class="rn">${face(RSLUG[r.id], `var(--${r.f})`)}${esc(r.n)}${r.paid ? '<span class="paid">a pagamento</span>' : ''}</span></th>`;
      CLASSES.forEach(c => {
        const v = r.can[c.id];
        const dim = roleMatch(c, state.r) ? '' : ' dim';
        if (!v) { h += `<td><span class="cell no${dim}" role="img" aria-label="${esc(r.n)} ${esc(c.n)}: non possibile"></span></td>`; return; }
        const sel = (r.id === state.race && c.id === state.cls) ? ' sel' : '';
        const label = `${r.n} ${c.n}${v === 'new' ? ', nuova combinazione' : ''}`;
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
  const rac = r.rac.map(x => `<div class="card ab"><span class="abt${x[0] === 'a' ? '' : ' p'}">${x[0] === 'a' ? 'Attive' : 'Passive'}</span><b>${bi(x[1])}</b><span>${racx(x[2])}</span></div>`).join('');
  const text = `${r.name || r.n} ${c.n} (${facName(r.f)})${r.paid ? ', serve il pacchetto Skyborne' : ''}`;
  $('#detail').innerHTML = `
    <div class="d-head">
      <div class="d-art" aria-hidden="true"><picture><source type="image/avif" srcset="${ROOT}assets/art/${RSLUG[r.id]}-600.avif${PV}"><img src="${ROOT}assets/art/${RSLUG[r.id]}-600.webp${PV}" width="600" height="804" alt="" loading="lazy" decoding="async"></picture></div>
      <div class="d-avs">${face(RSLUG[r.id], `var(--${r.f})`)}</div>
      <div class="d-title"><h3>${esc(r.n)}${raceEn(r)} · ${esc(c.n)}</h3>
        <div class="chips"><span class="tag ${r.f}">${facName(r.f)}</span>${isNew ? '<span class="tag new">Nuova combinazione</span>' : ''}${r.paid ? '<span class="tag paid">Razza a pagamento</span>' : ''}${roleChips(c)}</div></div>
    </div>
    <div class="d-body">
      <div class="d-cols">
        <div><h4>Specializzazioni</h4><div class="cards">${specs}</div></div>
        <div><h4>Abilità razziali</h4><div class="cards two">${rac}</div></div>
      </div>
      <div class="facts3">
        <div class="fact"><h4>Livellamento</h4>${lvlMeter(c)}</div>
        <div class="fact"><h4>In incursione</h4><span>${esc(c.raid)}.</span></div>
        <div class="fact"><h4>Novità</h4><span>${esc(c.forever)}</span></div>
      </div>
      ${tipBox(esc(r.tip))}
      ${pickLinks(r, c)}
      <div class="copyrow">
        <input id="pickText" readonly value="${esc(text)}" aria-label="La mia scelta">
        <button class="btn" id="copyBtn"><svg class="ico" aria-hidden="true"><use href="#i-copy"/></svg>Copia la mia scelta</button>
        <button class="btn ghost" id="shareBtn">Condividi</button>
        <span class="small" id="copyMsg" role="status"></span>
      </div>
    </div>`;
  $('#copyBtn').onclick = () => copyTo($('#pickText').value, $('#copyMsg'), 'Copiato');
  $('#shareBtn').onclick = () => shareBuild(r.id, c.id, state.spec, text);
}
/* Share: the link of the card page b/<race>-<class>-<spec>/ (its preview is the card with the name); on a phone the share sheet, else the clipboard */
function shareBuild(race, cls, spec, text) {
  const url = new URL(`${HOME}b/${BSLUG[race] || race}-${cls}-${spec}/`, location.href).href, msg = $('#copyMsg');
  if (navigator.share && matchMedia('(pointer: coarse)').matches) navigator.share({ title: text, url }).catch(e => { if (e && e.name !== 'AbortError') copyTo(url, msg, 'Link copiato'); });
  else copyTo(url, msg, 'Link copiato');
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
  eu: ['Europa', ''],
  cas: ['Europa', 'Caucaso e Asia centrale non hanno una regione propria; la più vicina è l’Europa.'],
  mea: ['Europa', 'Medio Oriente e Africa non hanno una regione propria; la più vicina è l’Europa.'],
  na: ['Americhe e Oceania', ''],
  la: ['Americhe e Oceania', 'L’America Latina gioca nella regione delle Americhe.'],
  oce: ['Americhe e Oceania', 'Blizzard unisce l’Oceania alle Americhe in un’unica regione. Blizzard non ha detto se ci sono server nella stessa Oceania.'],
  kr: ['Corea', ''],
  tw: ['Taiwan', ''],
  asia: ['', 'Non c’è una regione propria. Le più vicine sulla mappa sono Taiwan e Corea. Scegli quella con latenza World più bassa.'],
};
function renderPing() {
  const v = $('#pgW').value, r = PG[v];
  try { if (v) localStorage.setItem('gabella-ping', v); } catch (e) {}
  if (!r) { $('#pgOut').innerHTML = ''; return; }
  $('#pgOut').innerHTML = (r[0] ? `<p class="preg">La tua regione: ${esc(r[0])}</p>` : '') + '<ul class="verdict">'
    + (r[1] ? `<li>${esc(r[1])}</li>` : '')
    + '<li>Non ci sono reami: scegli regione e regole, non un server. La regione si sceglie in Battle.net prima di avviare il gioco.</li>'
    + '<li>Ogni regione ha i suoi personaggi e nomi. Si gioca insieme solo nella stessa regione.</li>'
    + '<li>Blizzard non ha detto dove si trovano i server delle regioni.</li></ul>';
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
