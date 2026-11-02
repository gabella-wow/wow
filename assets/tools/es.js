const CLASSES = [
  { id:'warrior', n:'Guerrero', s:'Guerrero', roles:['tank','dps'],
    specs:[['Armas','Daño cuerpo a cuerpo (arma de dos manos)',['dps']],['Furia','Daño cuerpo a cuerpo (dos armas)',['dps']],['Protección','Tanque',['tank']]],
    lvl:'La subida más lenta, cerca de un 12 % más larga que la media (estimación de LFCarry)',
    lp:12,
    raid:'Grito de guerra afecta a toda la banda',
    forever:'Más ira, mejor amenaza contra grupos de objetivos, el talento Weapon Master. Furia y Sed de sangre se han debilitado.' },
  { id:'paladin', n:'Paladín', roles:['tank','heal','dps'],
    specs:[['Sagrado','Sanador',['heal']],['Protección','Tanque',['tank']],['Reprensión','Daño cuerpo a cuerpo',['dps']]],
    lvl:'Ritmo de subida medio',
    lp:0,
    raid:'Bendición de los Reyes ahora es básica. Según las listas de la beta, Protección está entre los tanques más fuertes, y Reprensión bajó tras el parche del 15 de octubre.',
    forever:'Holy Strike desde el nivel 6, Sentencia no consume el sello. Los no-muertos ya pueden ser paladines, así que la clase llega a la Horda.' },
  { id:'hunter', n:'Cazador', roles:['dps'],
    specs:[['Bestias','Daño a distancia, mucho daño de la mascota',['dps']],['Puntería','Daño a distancia',['dps']],['Supervivencia','Cuerpo a cuerpo y a distancia, trampas',['dps']]],
    lvl:'La subida más rápida, cerca de un 8 % más rápida que la media (estimación de LFCarry)',
    lp:-8,
    raid:'Aura de disparo certero afecta a toda la banda',
    forever:'Puedes jugar sin mascota, las trampas funcionan en combate y llegan los zorros como familia de mascotas. Supervivencia puede ir cuerpo a cuerpo.' },
  { id:'rogue', n:'Pícaro', roles:['dps'],
    specs:[['Asesinato','Daño con venenos',['dps']],['Combate','Ataques rápidos con arma',['dps']],['Sutileza','Emboscadas, sangrados',['dps']]],
    lvl:'Ritmo de subida medio',
    lp:0,
    raid:'Daño cuerpo a cuerpo puro sin beneficios para la banda',
    forever:'Ya puede usar hachas de una mano. Asesinato se basa en venenos, Sutileza en sangrados y sigilo.' },
  { id:'priest', n:'Sacerdote', roles:['heal','dps'],
    specs:[['Disciplina','Sanador, escudos y absorción',['heal']],['Sagrado','Sanador',['heal']],['Sombras','Daño a distancia',['dps']]],
    lvl:'Cerca de un 5 % más lento que la media (estimación de LFCarry)',
    lp:5,
    raid:'Espíritu divino ahora es básico. El daño de Sombras y Peste devoradora (24 s de reutilización) se mejoraron con el parche del 15 de octubre.',
    forever:'Custodia de miedo y Peste devoradora están disponibles desde el nivel 20 para cualquier raza. Cada raza tiene dos hechizos de sacerdote propios.' },
  { id:'shaman', n:'Chamán', roles:['heal','dps','tank?'],
    specs:[['Elemental','Daño a distancia',['dps']],['Mejora','Daño cuerpo a cuerpo. Su capacidad de tanque aún está en duda',['dps','tank?']],['Restauración','Sanador',['heal']]],
    lvl:'Ritmo de subida medio',
    lp:0,
    raid:'Los tótems Fuerza de la tierra, Viento Furioso, Lengua de Fuego y Gracia del aire mejoran a su grupo',
    forever:'Los enanos ya pueden ser chamanes, así que la clase llega a la Alianza. Ráfaga de lava se mejoró y Elemental subió en las clasificaciones de daño.' },
  { id:'mage', n:'Mago', roles:['dps'],
    specs:[['Arcano','Ráfagas, mucho maná',['dps']],['Fuego','Críticos e igniciones',['dps']],['Escarcha','Daño y control',['dps']]],
    lvl:'La subida más rápida, cerca de un 8 % más rápida que la media, unas 12 horas ahorradas (estimación de LFCarry)',
    lp:-8,
    raid:'Portales, comida y agua para el grupo',
    forever:'Fuego recibió Buena racha, Arcano Explosión Arcana, Escarcha Lanza de hielo. Descarga de Pirofrío está disponible desde el nivel 40.' },
  { id:'warlock', n:'Brujo', roles:['dps'],
    specs:[['Aflicción','Daño con maldiciones y corrupción',['dps']],['Demonología','Daño a través de demonios',['dps']],['Destrucción','Daño directo de fuego y sombras',['dps']]],
    lvl:'Ritmo de subida medio',
    lp:0,
    raid:'Maestría oscura da un 2–10 % de daño de las Sombras, como en Classic (en la beta temprana, 1–5 %)',
    forever:'Aflicción tiene un nuevo hechizo canalizado, el demonio se queda con Sacrificio demoníaco, Destrucción gana Incinerar y daño en área.' },
  { id:'druid', n:'Druida', roles:['tank','heal','dps'],
    specs:[['Equilibrio','Daño a distancia',['dps']],['Combate feral','Tanque (oso) y daño cuerpo a cuerpo (gato)',['tank','dps']],['Restauración','Sanador, mucha sanación en el tiempo',['heal']]],
    lvl:'Cerca de un 5 % más lento que la media (estimación de LFCarry)',
    lp:5,
    raid:'Líder de la manada y Aura de lechúcico lunar afectan a toda la banda y se acumulan',
    forever:'Cada especialización tiene un rol claro, las formas funcionan con pociones y encantamientos de arma. Puedes ser tanque, sanador y luchador en un solo personaje.' }
];
const ROLE_RU = { tank:'Tanque', heal:'Sanador', dps:'Daño', 'tank?':'Tanque (dudoso)' };
const ri = r => `<svg class="ri" aria-hidden="true"><use href="#i-${r.replace('?','')}"/></svg>`;
const CCOL = { warrior:'#c79c6e', paladin:'#f58cba', hunter:'#abd473', rogue:'#fff569', priest:'#e8e8e8', shaman:'#2f8cf0', mage:'#40c7eb', warlock:'#8788ee', druid:'#ff7d0a' };
const BUFF = { warrior:'Grito de guerra', paladin:'Bendición de los Reyes', hunter:'Aura de disparo certero', priest:'Palabra de poder: entereza, Espíritu divino', shaman:'Tótems (Fuerza de la tierra, Viento Furioso, Lengua de Fuego, Gracia del aire)', mage:'Intelecto Arcano, portales, comida y agua', druid:'Marca de lo salvaje, Líder de la manada, Aura de lechúcico lunar' };

const RACES = [
  { id:'human', n:'Humano', f:'alliance',
    cls:['warrior','paladin','hunter*','rogue','priest','mage','warlock'],
    rac:[['a','Will to Survive','Elimina el aturdimiento'],['a','Percepción','Revela enemigos invisibles durante 20 s'],['p','Ruthless','+1% de probabilidad de crítico'],['p','El espíritu humano','+10% de espíritu']],
    tip:'El espíritu se convierte en sanación para un Sacerdote Sagrado, así que un sacerdote humano es bueno para sanar.' },
  { id:'dwarf', n:'Enano', f:'alliance',
    cls:['warrior','paladin','hunter','rogue','priest','shaman*'],
    rac:[['a','Petraforma','Inmunidad a sangrados, venenos y enfermedades durante 8 s y menos daño físico'],['a','Buscar tesoro','Muestra cofres cercanos y da probabilidad de objetos extra en la mayoría de cofres'],['p','Artisan’s Precision','+1% de probabilidad de golpe con hechizos y ataques'],['p','Big Game Hunter','+5% de daño contra bestias']],
    tip:'Petraforma es útil para tanques y en JcJ.' },
  { id:'nightelf', n:'Elfo de la noche', f:'alliance',
    cls:['warrior','hunter','rogue','priest','druid'],
    rac:[['a','Elune’s Light','+10% de probabilidad de crítico durante 15 s'],['a','Fusión de las Sombras','Invisibilidad en el sitio'],['p','Prontitud','+2 % de esquiva y de velocidad de carrera (Warcraft Tavern indica un 1 % de esquiva) {beta}'],['p','Espíritu de fuego fatuo','+75 % de velocidad de carrera como espíritu (Warcraft Tavern indica 25 %) {beta}']],
    tip:'La única raza de la Alianza con druida, salvo que elijas Skyborne.' },
  { id:'gnome', n:'Gnomo', f:'alliance',
    cls:['warrior','rogue','mage','warlock','priest*'],
    rac:[['a','Artista del escape','Breve inmunidad a ralentizaciones e inmovilizaciones'],['a','Eureka!','Durante 8 s, las habilidades cuestan menos y son un 10 % más fuertes {beta}'],['p','Mente expansiva','+5% de maná, ira o energía máximos'],['p','Especialización de ingeniería','Los artefactos de ingeniería funcionan de forma más fiable']],
    tip:'Mente expansiva ayuda sobre todo a las clases de energía.' },
  { id:'skyA', n:'Skyborne (Alianza)', f:'alliance', paid:true, name:'Skyborne High Order',
    cls:['warrior','hunter','rogue','mage','druid'],
    rac:[['a','Walk on Air','Planea hacia abajo durante 10 s, sin daño por caída'],['a','Read Ley Line','Regeneración de salud y maná +50% durante 15 s. En una Ley Line, además Attuned durante 1 hora: +100%, se mantiene tras morir'],['p','Wind Blessed','+2% de velocidad de ataque y de hechizos'],['p','Elemental Insight','+5% de daño contra elementales']],
    tip:'Raza de pago: Heroic Pack desde 29,99 $. Empieza en Zephras Isle (niveles 1–12).' },
  { id:'orc', n:'Orco', f:'horde',
    cls:['warrior','hunter','rogue','shaman','warlock','mage*'],
    rac:[['a','Furia sangrienta','+10% de poder de ataque y poder con hechizos durante 15 s'],['a','Shatter Curse','Elimina maldiciones y corrupción, −5% de daño mágico recibido durante 8 s'],['p','Comandar','+5% de daño de las mascotas de brujo y cazador'],['p','Firmeza','Los aturdimientos duran un 20% menos']],
    tip:'Furia sangrienta da una potente ventana de daño.' },
  { id:'undead', n:'No-muerto', f:'horde',
    cls:['warrior','rogue','mage','priest','warlock','paladin*'],
    rac:[['a','Voluntad de los Renegados','Elimina hechizos, miedo y sueño'],['a','Canibalizar','Restaura un 35% de salud y maná con el tiempo'],['p','Respiración subacuática','Respira bajo el agua más tiempo'],['p','Touch of the Grave','Probabilidad de drenar salud al atacar']],
    tip:'Combinación nueva: un paladín para la Horda, donde esta clase no existía antes.' },
  { id:'tauren', n:'Tauren', f:'horde',
    cls:['warrior','hunter','shaman','druid'],
    rac:[['a','Pisotón de guerra','Aturde a los enemigos cercanos durante 2 s, reutilización de 90 s'],['a','Cultivo','Cultiva hierbas que se pueden recoger sin Herboristería, reutilización de 15 min'],['p','Plainsrunning','Mientras te mueves, la velocidad de carrera sube un 2% por acumulación, hasta +60%. No afecta a la velocidad montado'],['p','Robustez','+5% de salud']],
    tip:'La única raza de la Horda con druida, salvo que elijas Skyborne.' },
  { id:'troll', n:'Trol', f:'horde',
    cls:['warrior','hunter','rogue','priest','shaman','mage','warlock*'],
    rac:[['a','Iracundia','+10 % de velocidad de ataque y de hechizo durante 12 s, reutilización de 3 min'],['a','Rapid Regeneration','Restaura salud con el tiempo'],['p','Matanza de bestias','+5% de daño contra bestias'],['p','Regeneración','La salud se regenera también en combate']],
    tip:'Más opciones de clase de la Horda: siete.' },
  { id:'skyH', n:'Skyborne (Horda)', f:'horde', paid:true, name:'Skyborne Windshaper',
    cls:['warrior','hunter','rogue','shaman','druid'],
    rac:[['a','Walk on Air','Planea hacia abajo durante 10 s, sin daño por caída'],['a','Skysight','+15% de velocidad de carrera durante 15 s. En una Elemental Convergence, además Charged durante 1 hora: +30%, se mantiene tras morir'],['p','Wind Blessed','+2% de velocidad de ataque y de hechizos'],['p','Elemental Insight','+5% de daño contra elementales']],
    tip:'Raza de pago: Heroic Pack desde 29,99 $. Solo la Horda puede tener chamán, solo la Alianza mago.' }
];
RACES.forEach(r => { r.can = {}; r.cls.forEach(c => { const isNew = c.endsWith('*'); r.can[isNew ? c.slice(0,-1) : c] = isNew ? 'new' : 'ok'; }); });
const CL = Object.fromEntries(CLASSES.map(c => [c.id, c]));
const BETA = '<span class="beta-note">según los datos de la beta</span>';
const BMARK = '{' + 'beta}';   // split so the guide build (which swaps the marker for the span everywhere) leaves it alone
const racx = s => String(s).split(BETA).join(BMARK).split(BMARK).map(esc).join(BETA);
const RC = Object.fromEntries(RACES.map(r => [r.id, r]));
const EN = {
  'Armas':'Armas','Furia':'Furia','Protección':'Protección','Sagrado':'Sagrado','Reprensión':'Reprensión',
  'Bestias':'Bestias','Puntería':'Puntería','Supervivencia':'Supervivencia',
  'Asesinato':'Asesinato','Combate':'Combate','Sutileza':'Sutileza',
  'Disciplina':'Disciplina','Sombras':'Sombra','Elemental':'Elemental','Mejora':'Mejora','Restauración':'Restauración',
  'Arcano':'Arcano','Fuego':'Fuego','Escarcha':'Escarcha','Aflicción':'Aflicción','Demonología':'Demonología','Destrucción':'Destrucción',
  'Equilibrio':'Equilibrio','Combate feral':'Combate feral',
  'Will to Survive':'Lucha por la supervivencia','Percepción':'Percepción','Ruthless':'Ruthless','El espíritu humano':'El espíritu humano',
  'Petraforma':'Petraforma','Buscar tesoro':'Buscar tesoro','Earth Fury':'Earth Fury','Big Game Hunter':'Big Game Hunter',
  'Elune’s Light':"Luz de Elune",'Fusión de las Sombras':'Fusión de las Sombras','Prontitud':'Prontitud','Espíritu de fuego fatuo':'Espíritu de fuego fatuo',
  'Artista del escape':'Artista del escape','Eureka!':'¡Eureka!','Mente expansiva':'Mente expansiva','Especialización de ingeniería':'Especialización de ingeniería',
  'Walk on Air':'Walk on Air','Read Ley Line':'Read Ley Line','Wind Blessed':'Wind Blessed','Elemental Insight':'Elemental Insight','Skysight':'Skysight',
  'Furia sangrienta':'Furia sangrienta','Shatter Curse':'Shatter Curse','Savage':'Savage','Comandar':'Comandar','Firmeza':'Firmeza',
  'Voluntad de los Renegados':'Voluntad de los Renegados','Canibalizar':'Canibalizar','Respiración subacuática':'Respiración subacuática','Touch of the Grave':'Toque de la tumba',
  'Pisotón de guerra':'Pisotón de guerra','Cultivo':'Cultivo','Plainsrunning':'Correr planicies','Robustez':'Robustez',
  'Iracundia':'Iracundia','Rapid Regeneration':'Regeneración rápida','Matanza de bestias':'Matanza de bestias','Regeneración':'Regeneración'
};
RC.skyA.en = 'High Order Skyborne'; RC.skyH.en = 'Windshaper Skyborne';
const CX = {"warrior": {"armor": "Tela, cuero, malla; placas desde el nivel 40 {beta}", "weapons": "Todo excepto varitas; escudo", "resource": "Ira", "lvl": "La subida más lenta, cerca de un 12 % más larga que la media (estimación de LFCarry)", "group": ["Grito de guerra afecta a toda la banda", "Grito desmoralizador y Hender armadura en el jefe", "Golpes de barrido y Huracán para combates contra varios objetivos"], "pros": ["El mejor tanque y gran daño cuerpo a cuerpo", "Bueno para JcJ (Armas)", "Pocos botones, fácil de entender"], "cons": ["La subida más lenta", "Muy dependiente del equipo", "Casi sin autosanación ni control de masas"], "specs": [{"n": "Armas", "what": "Daño cuerpo a cuerpo (arma de dos manos)"}, {"n": "Furia", "what": "Daño cuerpo a cuerpo (dos armas)"}, {"n": "Protección", "what": "Tanque"}]}, "paladin": {"armor": "Tela, cuero, malla; placas desde el nivel 40; escudo {beta}", "weapons": "Hachas, mazas, espadas, armas de asta desde el nivel 20 {beta}", "resource": "Maná", "lvl": "Ritmo de subida medio", "group": ["Auras de grupo: Devoción, Reprensión, Concentración", "Auras de resistencia al Fuego, Escarcha y Sombras para toda la banda", "Bendiciones de una hora, bendiciones superiores para toda una clase", "Sello de justicia impide que los enemigos huyan"], "pros": ["Los tres roles en un solo personaje", "Fuertes beneficios de grupo", "Placas y un personaje resistente"], "cons": ["Sin acercamiento, ralentización ni aumento de velocidad", "Poco control de masas aparte de Martillo de justicia", "Reprensión bajó tras el parche"], "specs": [{"n": "Sagrado", "what": "Sanador"}, {"n": "Protección", "what": "Tanque"}, {"n": "Reprensión", "what": "Daño cuerpo a cuerpo"}]}, "hunter": {"armor": "Tela, cuero; malla desde el nivel 40 {beta}", "weapons": "Arcos, ballestas, armas de fuego, hachas, espadas, armas de asta", "resource": "Maná; la mascota usa Enfoque", "lvl": "La subida más rápida, cerca de un 8 % más rápida que la media (estimación de LFCarry)", "group": ["Aura de disparo certero aumenta el daño a distancia del grupo", "Trampa congelante: control de masas fiable", "Disparo disperso interrumpe lanzamientos", "Aspecto de la manada acelera a todo el grupo en el camino"], "pros": ["La subida más rápida", "Genial en solitario", "Trampas y control de masas"], "cons": ["Zona muerta a corta distancia de hasta 8 metros", "Tienes que gestionar la mascota", "Los talentos de Supervivencia tenían errores en la beta"], "specs": [{"n": "Bestias", "what": "Daño a distancia, mucho daño de la mascota"}, {"n": "Puntería", "what": "Daño a distancia"}, {"n": "Supervivencia", "what": "Cuerpo a cuerpo y a distancia, trampas"}]}, "rogue": {"armor": "Tela, cuero", "weapons": "Dagas, espadas, mazas, armas de puño, hachas de una mano, arrojadizas", "resource": "Energía y puntos de combo", "lvl": "Ritmo de subida medio", "group": ["Daño cuerpo a cuerpo puro sin beneficios para la banda", "Aporrear, Ceguera y Golpe a los riñones: mucho control de masas", "Patada interrumpe lanzamientos peligrosos"], "pros": ["Daño muy alto que escala con el equipo", "Sigilo y mucho control de masas", "Libertad para elegir arma"], "cons": ["Muy dependiente del equipo", "Sin autosanación", "Solo te salvan Evasión y Esfumarse"], "specs": [{"n": "Asesinato", "what": "Daño con venenos"}, {"n": "Combate", "what": "Ataques rápidos con arma"}, {"n": "Sutileza", "what": "Emboscadas, sangrados"}]}, "priest": {"armor": "Tela", "weapons": "Dagas, mazas, bastones, varitas", "resource": "Maná", "lvl": "Cerca de un 5 % más lento que la media (estimación de LFCarry)", "group": ["Espíritu divino y Palabra de poder: entereza para toda la banda", "Infusión de poder potencia a un aliado", "El sanador principal del grupo"], "pros": ["Un grupo siempre lo necesita", "Sanación o daño de sombras", "Muchas builds"], "cons": ["Solo tela, frágil", "Pocas formas de moverse rápido", "La celeridad apenas ayuda a los hechizos"], "specs": [{"n": "Disciplina", "what": "Sanador, escudos y absorción"}, {"n": "Sagrado", "what": "Sanador"}, {"n": "Sombras", "what": "Daño a distancia"}]}, "shaman": {"armor": "Tela, cuero; malla desde el nivel 40; escudo {beta}", "weapons": "Mazas, hachas, bastones, armas de puño, dagas", "resource": "Maná", "lvl": "Ritmo de subida medio", "group": ["Los tótems Fuerza de la tierra, Viento Furioso, Lengua de Fuego y Gracia del aire mejoran a su grupo", "Tótem de tremor elimina miedo, sueño y hechizos", "Tótems que limpian venenos y enfermedades", "Purgar quita beneficios a los enemigos"], "pros": ["Tótems potentes para el grupo", "Subida de nivel móvil", "Talentos nuevos potentes"], "cons": ["Sin control de masas duro", "Maná en combates largos", "El rol de tanque aún sin confirmar"], "specs": [{"n": "Elemental", "what": "Daño a distancia"}, {"n": "Mejora", "what": "Daño cuerpo a cuerpo. Su capacidad de tanque aún está en duda"}, {"n": "Restauración", "what": "Sanador"}]}, "mage": {"armor": "Tela", "weapons": "Dagas, espadas, bastones, varitas", "resource": "Maná", "lvl": "La subida más rápida, cerca de un 8 % más rápida que la media, unas 12 horas ahorradas (estimación de LFCarry)", "group": ["Portales desde el nivel 40, teletransportes desde el 20", "Comida y agua para el grupo", "Polimorfia: control de masas fiable", "Deshacer maldición inferior"], "pros": ["La subida más rápida", "Portales y comida para todos", "Tres árboles fuertes y distintos"], "cons": ["Solo tela, frágil", "El maná se acaba rápido", "Daño en área suavizado"], "specs": [{"n": "Arcano", "what": "Ráfagas, mucho maná"}, {"n": "Fuego", "what": "Críticos e igniciones"}, {"n": "Escarcha", "what": "Daño y control"}]}, "warlock": {"armor": "Tela", "weapons": "Dagas, espadas, bastones, varitas", "resource": "Maná; Transfusión de vida convierte salud en maná", "lvl": "Ritmo de subida medio", "group": ["Piedra de salud y Piedra de alma", "Ritual de invocación: reúne al grupo", "Maldición de la lengua ralentiza el lanzamiento un 60%", "Maldición de los Elementos: más daño mágico al objetivo"], "pros": ["Autosuficiente: un demonio y Transfusión de vida", "Mucha utilidad para el grupo", "Gran daño en el tiempo"], "cons": ["Frágil y poco móvil", "El daño tarda en arrancar", "Sin traslación ni sprint"], "specs": [{"n": "Aflicción", "what": "Daño con maldiciones y corrupción"}, {"n": "Demonología", "what": "Daño a través de demonios"}, {"n": "Destrucción", "what": "Daño directo de fuego y sombras"}]}, "druid": {"armor": "Tela, cuero", "weapons": "Dagas, mazas, bastones, armas de puño, armas de asta desde el nivel 20 {beta}", "resource": "Maná; ira en Forma de oso, energía en Forma felina", "lvl": "Cerca de un 5 % más lento que la media (estimación de LFCarry)", "group": ["Líder de la manada y Aura de lechúcico lunar afectan a toda la banda y se acumulan", "Renacer: resurrección en combate", "Enervar devuelve maná a un sanador", "Elimina maldiciones y venenos"], "pros": ["Los tres roles en un solo personaje", "Gran movilidad", "Resurrección en combate"], "cons": ["El oso no tiene bloqueo ni parada", "Los efectos de sanación en el tiempo cuestan más de controlar", "Las cifras finales en bandas aún se desconocen"], "specs": [{"n": "Equilibrio", "what": "Daño a distancia"}, {"n": "Combate feral", "what": "Tanque (oso) y daño cuerpo a cuerpo (gato)"}, {"n": "Restauración", "what": "Sanador, mucha sanación en el tiempo"}]}};
const HC = {"tx":{"title":"Mi personaje","lead":"Sin registro ni contraseña: elige clase, especialización y raza, y el sitio se adapta a ti.","local":"Se guarda solo en este navegador.","none":"Aún sin personaje","create":"Crear personaje","edit":"Editar","reset":"Eliminar personaje","resetQ":"¿Borrar el personaje de este navegador?","steps":["Bando","Clase y especialización","Raza","Aspecto","Detalles"],"side":"¿Con quién juegas?","cls":"Clase","spec":"Especialización","race":"Raza","bestFor":"Mejor raza para %s","best":"la mejor","paid":"de pago","sex":"Sexo","m":"Masculino","f":"Femenino","bg":"Fondo del retrato","lvl":"Nivel","reg":"Región","lvlReg":"Nivel y región","regs":{"us":"América y Oceanía","eu":"Europa","kr":"Corea","tw":"Taiwán"},"p1":"Profesión 1","p2":"Profesión 2","secP":"Profesiones secundarias","noP":"Ninguno","role":"Rol","back":"Atrás","next":"Continuar","done":"Listo","cancel":"Cancelar","later":"Puedes rellenarlo más tarde.","levelN":"Nivel %n","build":"Mi build de talentos","buildD":"Talentos de %s por nivel.","pairs":"Parejas de profesiones","pairsD":"Qué profesiones le van a tu clase.","bestR":"Mejores razas","bestRD":"Raza para tu clase en ambas facciones.","lvlG":"Subir de nivel la clase","lvlGD":"Ruta y talentos 1–60.","day1":"Día 1 para tu personaje","day1D":"La lista de lanzamiento con tu clase y raza.","play":"En el juego","playD":"Zonas y mazmorras para tu nivel, temporizadores, radio.","dung":"Mazmorras para tu nivel","dungNo":"Indica tu nivel y elegiremos mazmorras.","dungFirst":"Las primeras mazmorras abren al nivel 13.","resetH":"Reinicio semanal","resetIn":"en %s","resetNote":"Blizzard aún no ha anunciado la hora de reinicio de Forever. Se muestra como en otras versiones de WoW de esta región: lo comprobaremos en el lanzamiento.","resetUnk":"Confirmaremos la hora de reinicio de esta región en el lanzamiento.","resetNoReg":"Indica tu región para ver el reinicio semanal.","resetWhy":"Las bandas abren el 09.12 y tienen bloqueo semanal.","lfg":"Texto para buscar grupo","lfgD":"Pégalo en el chat LookingForGroup. Nombres como en el juego.","lfgP":{"tank":"%c tanque busca grupo","heal":"%c sanador busca grupo","dps":"%c busca grupo"},"lfgT":"%p: %d, nivel %l.","lfgT0":"%p.","allD":"Todas las mazmorras","copy":"Copiar","copied":"Copiado","sync":"Sincronizar entre dispositivos","syncD":"Solo necesitas iniciar sesión para esto: el personaje estará en tu móvil y tu PC, y el correo del lanzamiento te llegará si te suscribes.","yourCls":"Tu %s","bTalents":"Talentos","bSpec":"Build: %s","bLevel":"Subida de nivel","bGroup":"Grupo","bNews":"Noticias","copiedT":"Copiado: %s","profsL":"Profesiones","day1n":"Día 1: %n de %t","collect":"Arma tu personaje","collectD":"Clase, especialización y raza: talentos, subida de nivel, grupo y noticias de tu clase.","change":"Cambiar","allSet":"Todos los ajustes","close":"Cerrar","mine":"Afecta a tu clase","share":"Compartir","linkCopied":"Enlace copiado","make":"Hacerlo mi personaje","made":"Es tu personaje","plaqueH":"Mi personaje","plaqueD":"Clase, especialización y raza en un minuto, y luego tu build, profesiones y mazmorras.","day1Mine":"Para tu personaje","ckClass":"Tu especialización, %s: el build de talentos por nivel.","ckRaceOk":"%r es la mejor raza para tu especialización.","ckRaceAlt":"Mejor raza para tu especialización: %r.","ckProfs":"Parejas de profesiones para %s.","ckStart":"Subir de nivel con %s: ruta y primeros talentos.","ckPing":"Tu región: %s.","or":"o"},"best":{"warrior":{"alliance":{"*":[["human","nightelf"],"Humano: +1 % de crítico con cualquier arma. Elfo de la noche: +10 % de crítico durante 15 s. Las fuentes están casi a partes iguales."],"protection":[["dwarf"],"Petraforma reduce el daño físico un 10 % y quita sangrados."]},"horde":{"*":[["orc"],"Furia sangrienta: +10 % de poder de ataque durante 15 s. Antes de los cambios de razas del 26.10, todas las fuentes la ponían primera."],"protection":[["tauren"],"Robustez da +5 % de salud, Pisotón de guerra aturde a los enemigos cercanos."]}},"paladin":{"alliance":{"*":[["human"],"Ruthless refuerza golpes y hechizos, Lucha por la supervivencia quita aturdimientos."],"protection":[["dwarf"],"Petraforma y Artisan’s Precision: +1 % de probabilidad de golpe."]},"horde":{"*":[["undead"],"En la Horda solo el No-muerto puede ser paladín. Canibalizar recupera maná, Voluntad de los Renegados quita el miedo."]}},"hunter":{"alliance":{"*":[["human","nightelf"],"Humano: +1 % de crítico, y la mascota lo hereda. Elfo de la noche: Luz de Elune y Fusión de las Sombras."]},"horde":{"*":[["orc","troll"],"Orco: Furia sangrienta y Comandar (+5 % de daño de la mascota). Trol: +5 % de daño contra bestias."]}},"rogue":{"alliance":{"*":[["nightelf"],"Fusión de las Sombras ahora reduce la amenaza también en combate, además de Gracia de Elune y Prontitud."]},"horde":{"*":[["orc"],"Furia sangrienta: +10 % de poder de ataque durante 15 s."]}},"priest":{"alliance":{"*":[["gnome"],"Todas las fuentes la eligen: ¡Eureka! también refuerza Palabra de poder: escudo, Inquisitive Mind da +5 % de maná."]},"horde":{"*":[["undead","troll"],"Las fuentes están divididas. El No-muerto es más fuerte en JcJ: Voluntad de los Renegados quita miedo, sueño y hechizo."]}},"shaman":{"alliance":{"*":[["dwarf"],"En la Alianza solo el Enano puede ser chamán: Petraforma y Artisan’s Precision (+1 % de probabilidad de golpe)."]},"horde":{"*":[["orc"],"Furia sangrienta da poder de ataque y poder con hechizos: sirve a Elemental y a Mejora."],"restoration":[["troll"],"Para un sanador, una fuente recomienda Trol: Iracundia, +10 % de velocidad de lanzamiento durante 12 s."]}},"mage":{"alliance":{"*":[["gnome"],"¡Eureka! durante 8 s, Inquisitive Mind: +5 % de maná, Artista del escape rompe raíces."]},"horde":{"*":[["orc"],"El orco mago es una combinación nueva de Forever: Furia sangrienta ahora da poder con hechizos."]}},"warlock":{"alliance":{"*":[["gnome","human"],"Gnomo: ¡Eureka! e Inquisitive Mind. Humano: el daño periódico puede ser crítico y Ruthless da +1 % de crítico."]},"horde":{"*":[["orc","undead"],"Orco: Furia sangrienta da poder con hechizos. El No-muerto se elige más en JcJ."]}},"druid":{"alliance":{"*":[["nightelf"],"Gracia de Elune: +10 % de crítico durante 15 s, y Prontitud."]},"horde":{"*":[["tauren"],"Robustez: +5 % de salud, Pisotón de guerra funciona también en formas."]}}},"sid":{"warrior":["arms","fury","protection"],"paladin":["holy","protection","retribution"],"hunter":["beast-mastery","marksmanship","survival"],"rogue":["assassination","combat","subtlety"],"priest":["discipline","holy","shadow"],"shaman":["elemental","enhancement","restoration"],"mage":["arcane","fire","frost"],"warlock":["affliction","demonology","destruction"],"druid":["balance","feral","restoration"]},"sn":{"warrior":["Armas","Furia","Protección"],"paladin":["Sagrado","Protección","Reprensión"],"hunter":["Bestias","Puntería","Supervivencia"],"rogue":["Asesinato","Combate","Sutileza"],"priest":["Disciplina","Sagrado","Sombras"],"shaman":["Elemental","Mejora","Restauración"],"mage":["Arcano","Fuego","Escarcha"],"warlock":["Aflicción","Demonología","Destrucción"],"druid":["Equilibrio","Combate feral","Restauración"]},"fn":{"alliance":"Alianza","horde":"Horda"},"reset":{"us":[2,15],"eu":[3,4],"kr":null,"tw":null},"rn":{"human":"Humano","dwarf":"Enano","nightelf":"Elfo de la noche","gnome":"Gnomo","skyA":"Skyborne High Order","orc":"Orco","undead":"No-muerto","tauren":"Tauren","troll":"Trol","skyH":"Skyborne Windshaper"},"rf":{"human":"alliance","dwarf":"alliance","nightelf":"alliance","gnome":"alliance","skyA":"alliance","orc":"horde","undead":"horde","tauren":"horde","troll":"horde","skyH":"horde"},"cn":{"warrior":"Guerrero","paladin":"Paladín","hunter":"Cazador","rogue":"Pícaro","priest":"Sacerdote","shaman":"Chamán","mage":"Mago","warlock":"Brujo","druid":"Druida"},"cen":{"warrior":"Warrior","paladin":"Paladin","hunter":"Hunter","rogue":"Rogue","priest":"Priest","shaman":"Shaman","mage":"Mage","warlock":"Warlock","druid":"Druid"}};
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

const CPROF = {"warrior": [["Subida de nivel: Herrería + Minería", ""], ["Nivel 60: Ingeniería + Minería", "El herrero se viste con placas y armas, y muchas recetas son personales. El ingeniero consigue granadas y artilugios que al guerrero le faltan."]], "paladin": [["Subida de nivel: Herrería + Minería", ""], ["Nivel 60: Protección, Reprensión: Ingeniería + Minería. Sagrado: Alquimia + Herboristería", "Sagrado gasta mucho maná: las pociones son tuyas, y el Mana Well del campamento sustituye a Bendición de Sabiduría."]], "hunter": [["Subida de nivel: Peletería + Desollando", ""], ["Nivel 60: Ingeniería + Minería", "El peletero se hace su cuero y su malla y Armor Kits. El ingeniero fabrica miras y armas de fuego."]], "rogue": [["Subida de nivel: Peletería + Desollando", ""], ["Nivel 60: Ingeniería + Minería", "El cuero es tuyo, y la Camp Tent da descanso. La Ingeniería es la profesión principal para el PvP."]], "priest": [["Subida de nivel: Sastrería + Encantamiento", ""], ["Nivel 60: Sastrería + Ingeniería o Encantamiento", "El sastre hace cinturones con poder con hechizos desde el nivel 10, el encantador varitas con poder con hechizos desde el 5. Lo cosido se desencanta en materiales."]], "shaman": [["Subida de nivel: Peletería + Desollando", ""], ["Nivel 60: Alquimia + Herboristería", "El peletero hace objetos con poder con hechizos para Elemental y Restauración y equipo para Mejora. En banda y en grupo hacen falta pociones."]], "mage": [["Subida de nivel: Sastrería + Encantamiento", ""], ["Nivel 60: Sastrería + Encantamiento; para PvP y pulls grandes Ingeniería + Minería", "El sastre da equipo temprano con poder con hechizos, y lo cosido se desencanta. Las granadas del ingeniero retienen en su sitio a grupos grandes de enemigos."]], "warlock": [["Subida de nivel: Sastrería + Encantamiento", ""], ["Nivel 60: Sastrería + Alquimia", "La Faction Banner del sastre da Espíritu para Transfusión de vida. La Alquimia son pociones y oro."]], "druid": [["Subida de nivel: Peletería + Desollando o Herboristería", ""], ["Nivel 60: Alquimia + Herboristería", "Las hierbas se recogen en Forma de viaje, y las pociones se beben en cualquier forma. Mana Well e Incense Candle son para Equilibrio y Restauración."]]};   /* recommended profession pairs per class, already in the page language (build.class_profs) */
const $ = s => document.querySelector(s);
const ROOT = '../../', HOME = '../';
function esc(s) { return String(s).replace(/[&<>"]/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m])); }
function raceName(r) { return r.name || r.n; }
function syncSeg(id, v) { document.querySelectorAll(`#${id} button`).forEach(b => b.setAttribute('aria-pressed', b.dataset.v === String(v))); }
const FAC = { alliance: 'Alianza', horde: 'Horda' };
const BSLUG = { skyA: 'skyborne-a', skyH: 'skyborne-h' };   // race id -> url part of the share page (tools/make_build_cards.py SLUG)
const RSLUG = { human: 'human', dwarf: 'dwarf', nightelf: 'night-elf', gnome: 'gnome', skyA: 'skyborne-alliance', orc: 'orc', undead: 'undead', tauren: 'tauren', troll: 'troll', skyH: 'skyborne-horde' };
const PAINTED = ["druid-nightelf", "druid-tauren", "hunter-nightelf", "hunter-orc", "mage-gnome", "mage-orc", "paladin-human", "paladin-undead", "priest-gnome", "priest-undead", "rogue-nightelf", "rogue-orc", "shaman-dwarf", "shaman-orc", "warlock-gnome", "warlock-orc", "warrior-human", "warrior-orc"];   // class x race paintings that exist (build_tools.painted): the player's own race is drawn, never the best race of the side
const unitArt = (p, ext) => `${ROOT}assets/art/${PAINTED.includes(p.cls + '-' + p.race) ? p.cls + '-' + p.race : RSLUG[p.race]}-360.${ext}${PV}`;
const classUrl = id => `${HOME}classes/${id}/`, raceUrl = id => `${HOME}races/${RSLUG[id]}/`;
const PV = /*PV*/'?v=03c9d4a0';   // ?v= of the class and race portraits (build.art_version)
const porId = (id, f) => (window.GabellaPor ? GabellaPor.id(id, f) : id);   // a class: the portrait of side f, else of the reader's side (build.por_js)
const art = (id, ext = 'webp', f) => `${ROOT}assets/art/${porId(id, f)}-360.${ext}${PV}`;
async function copyTo(text, msgEl, ok) {
  try { await navigator.clipboard.writeText(text); msgEl.textContent = ok; } catch (e) { msgEl.textContent = 'No se pudo copiar, selecciona el texto y pulsa Ctrl+C'; }
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
    out.push((groups > 1 ? `Grupo ${g + 1}: ` : '') + part.map(p => `${p.name ? p.name + ' — ' : ''}${raceName(RC[p.race])} ${CL[p.cls].n} (${ROLE_RU[p.role]})`).join(', '));
  }
  return out.length ? out.join('\n') + `\n${FAC[R.f]}, ${R.size}` : '';
}

/* LFG line: the dungeon or raid, the missing roles, the play style and a short link (#t=); kept under the 255-byte chat limit */
const LFG = {"d": [["Sima Ígnea", 13, 18, "horde"], ["Hall of Thanes", 13, 18, 0], ["Ruinas de Lordaeron", 15, 20, 0], ["Las Minas de la Muerte", 15, 22, 0], ["Cuevas de los Lamentos", 17, 24, 0], ["Castillo de Colmillo Oscuro", 20, 26, 0], ["Cavernas de Brazanegra", 22, 28, 0], ["Las Mazmorras", 25, 29, "alliance"], ["Excavation Site: Wetlands", 26, 31, 0], ["City of Dalaran", 28, 33, 0], ["Gnomeregan", 29, 38, 0], ["Horado Rajacieno", 29, 38, 0], ["Monasterio Escarlata: Cementerio", 30, 38, 0], ["Monasterio Escarlata: Biblioteca", 33, 41, 0], ["The Drowned City", 35, 40, 0], ["Monasterio Escarlata: Armería", 36, 44, 0], ["Uldaman", 36, 45, 0], ["Zahúrda Rojocieno", 37, 46, 0], ["Monasterio Escarlata: Catedral", 38, 46, 0], ["Zul’Farrak", 40, 47, 0], ["Krol’dok Stronghold", 40, 45, 0], ["Maraudon", 45, 51, 0], ["Alcaz Island Prison", 48, 53, 0], ["El Templo de Atal’Hakkar", 50, 55, 0], ["Profundidades de Roca Negra", 52, 60, 0], ["Blackmaw Hold", 55, 60, 0], ["Cumbre de Roca Negra Inferior", 57, 60, 0], ["La Masacre: Este", 58, 60, 0], ["Shaper’s Terrace", 58, 60, 0], ["Stratholme: vivos", 58, 60, 0], ["Stratholme: no-muertos", 58, 60, 0], ["Scholomance", 58, 60, 0], ["Cumbre de Roca Negra Superior", 60, 60, 0], ["La Masacre: Oeste", 60, 60, 0], ["La Masacre: Norte", 60, 60, 0]], "r": {"10": "Barrow Deeps", "20": "La Cima Hyjal", "40": "Guarida de Onyxia"}};   // dungeons [name, min, max, entrance faction] and raids {size: name} in the client's language (build_tools)
const CHAT_MAX = 255, CANON = 'https://gabella.site/wow/es/tools/'.replace(/^https?:\/\//, '');
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
  const head = (L.d ? '%d — buscamos: %n.' : 'Grupo busca: %n.').replace('%d', L.d).replace('%n', roles);
  const parts = [head, L.s ? 'Estilo: %s.'.replace('%s', L.s) : '', CANON + shortHash()].filter(Boolean);
  const bytes = t => new TextEncoder().encode(t).length;
  let text = parts.join(' ');
  if (bytes(text) > CHAT_MAX) text = parts.slice(0, -1).join(' ');   // a long raid code would not fit: the link goes first
  return text;
}
function renderLfg() {
  const places = lfgPlaces(), sel = $('#lfgD');
  if (!places.some(p => p[0] === L.d)) L.d = R.size === 5 ? '' : (places[0] || [''])[0];
  $('#lfgDL').textContent = R.size === 5 ? 'Mazmorra' : 'Banda';
  sel.innerHTML = (R.size === 5 ? '<option value="">Cualquier mazmorra</option>' : '') + places.map(([v, t]) => `<option value="${esc(v)}"${v === L.d ? ' selected' : ''}>${esc(t)}</option>`).join('');
  syncSeg('lfgS', L.s);
  const text = lfgText();
  $('#rLfg').value = text;
  $('#rCopyLfg').disabled = !text;
  $('#rLfgMsg').textContent = text ? lfgLen(text) : R.s.some(Boolean) ? 'Todos los puestos están ocupados.' : 'Añade al menos un jugador al grupo.';
}
function lfgLen(t) { return 'Caracteres: %n de %m (límite de una línea de chat).'.replace('%n', t.length).replace('%m', CHAT_MAX); }

function unitHTML(p, i) {
  const cls = R.moving === i ? ' src' : '';
  if (!p) return `<button type="button" class="unit empty${cls}" data-i="${i}"><span class="up" aria-hidden="true">+</span><span class="ub"><b>Hueco libre</b><span>Haz clic para añadir un jugador</span></span></button>`;
  const c = CL[p.cls], r = RC[p.race];
  return `<button type="button" class="unit${cls}" data-i="${i}" draggable="true" style="--cc:${CCOL[p.cls]};--pc:${power(p)}" aria-label="${esc((p.name || `Jugador ${i + 1}`) + ', ' + raceName(r) + ' ' + c.n + ', ' + ROLE_RU[p.role])}">
    <span class="up"><picture><source type="image/avif" srcset="${unitArt(p, 'avif')}"><img src="${unitArt(p, 'webp')}" width="360" height="482" alt="" loading="lazy" decoding="async"></picture></span>
    <span class="ub"><span class="un"><span class="ur" title="${ROLE_RU[p.role]}">${ri(p.role)}</span><b>${esc(p.name || c.n)}</b><small>${esc(raceName(r))} · ${esc(c.n)}</small></span><span class="hp"><i></i></span><span class="mp"></span></span></button>`;
}
function cellHTML(p, i) {
  const cls = R.moving === i ? ' src' : '';
  if (!p) return `<button type="button" class="rc empty${cls}" data-i="${i}" aria-label="Hueco libre ${i + 1}"><span aria-hidden="true">+</span>Añadir</button>`;
  const c = CL[p.cls], r = RC[p.race];
  return `<button type="button" class="rc${cls}" data-i="${i}" draggable="true" style="--cc:${CCOL[p.cls]};--pc:${power(p)}" aria-label="${esc((p.name || `Jugador ${i + 1}`) + ', ' + raceName(r) + ' ' + c.n + ', ' + ROLE_RU[p.role])}" title="${esc(raceName(r) + ' · ' + c.n + ' · ' + ROLE_RU[p.role])}"><b>${esc(p.name || c.n)}</b><small>${esc(p.name ? c.n : raceName(r))}</small>${ri(p.role)}</button>`;
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
      const st = n && (!c.tank || !c.heal) ? `<span class="warn">${!c.tank ? 'sin tanque' : 'sin sanador'}</span>` : `<span>${n}/5</span>`;
      h += `<div class="rg"><div class="rg-h"><b>Grupo ${g + 1}</b>${st}</div>${part.map((p, k) => cellHTML(p, g * PARTY + k)).join('')}</div>`;
    }
    $('#rview').innerHTML = `<div class="rgrid" style="--gc:${Math.min(groups, 8)}">${h}</div>`;
  }
  const hint = $('#rhint');
  hint.classList.toggle('on', R.moving >= 0);
  hint.innerHTML = R.moving >= 0 ? `Elige un hueco nuevo para el jugador ${R.moving + 1}. <button type="button" id="mvCancel">Cancelar</button>` : '';

  const list = R.s.filter(Boolean), cnt = countRoles(list), rec = REC[R.size];
  $('#rRoles').innerHTML = RR.map((x, k) => `<span class="${list.length && cnt[x] < rec[k] ? 'low' : ''}">${ri(x)}${ROLE_RU[x]} <b>${cnt[x]}</b> / ${rec[k]}</span>`).join('');
  $('#rTip').textContent = R.size === 5 ? 'Una mazmorra necesita un tanque, un sanador y tres de daño.' : `Regla general para bandas: tanques ${rec[0]}, sanadores ${rec[1]}, el resto daño. El número exacto depende de los jefes.`;
  const have = new Set(list.map(p => p.cls));
  $('#rBuffs').innerHTML = CLASSES.filter(c => BUFF[c.id]).map(c => `<li class="${have.has(c.id) ? '' : 'off'}" style="--cc:${CCOL[c.id]}"><span class="cdot"></span><span><b>${esc(c.n)}:</b> ${esc(BUFF[c.id])}</span></li>`).join('');
  const n = list.length;
  $('#rRaids').innerHTML = n ? RAIDS.map(([size, name]) => `<li class="${n >= size ? 'good' : ''}">${n >= size ? `Banda de ${size} (${name}): jugadores suficientes.` : `Banda de ${size} (${name}): faltan ${size - n}.`}</li>`).join('') : '<li>Aún no hay nadie. Pulsa «Mi personaje», «Rellenar vacíos» o un marco libre.</li>';

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
function myHero() {   // the hero of this browser (assets/hero/hero.js?v=cc9d30bf3d, localStorage gabella-wf-me)
  let h = null; try { h = JSON.parse(localStorage.getItem('gabella-wf-me')); } catch (e) {}
  return h && RC[h.race] && CL[h.cls] && RC[h.race].can[h.cls] ? h : null;
}
$('#rMine').onclick = () => {
  const h = myHero(), msg = $('#rMy');
  if (!h) {
    msg.innerHTML = 'Aún no hay personaje. <a href="../character/" id="rMake">Arma tu personaje</a>';
    $('#rMake').onclick = e => { if (window.GabellaHero) { e.preventDefault(); GabellaHero.open(); } };
    return;
  }
  const f = RC[h.race].f, role = RR.includes(h.role) ? h.role : roleOpts(CL[h.cls])[0];
  if (f !== R.f) {
    if (R.s.some(Boolean)) { msg.textContent = 'Tu personaje es de la otra facción: cambia la facción sobre los marcos.'; return; }
    R.f = f;
  }
  if (R.s.some(p => p && p.race === h.race && p.cls === h.cls && p.role === role && !p.name)) { msg.textContent = 'Tu personaje ya está en la composición.'; return; }
  let i = R.s.findIndex(p => !p); if (i < 0) i = 0;
  R.s[i] = { race: h.race, cls: h.cls, role, name: '' };
  msg.textContent = ''; R.moving = -1; renderRaid();
};
$('#rClear').onclick = () => { R.s = Array(R.size).fill(null); R.moving = -1; renderRaid(); };
$('#rCopyLink').onclick = () => copyTo(teamLink(), $('#rMsg'), 'Enlace copiado');
$('#rCopyText').onclick = () => copyTo(teamText(), $('#rMsg'), 'Grupo copiado');
$('#lfgD').onchange = e => { L.d = e.target.value; renderLfg(); };
$('#lfgS').addEventListener('click', e => { const b = e.target.closest('button'); if (b) { L.s = L.s === b.dataset.v ? '' : b.dataset.v; renderLfg(); } });
$('#rCopyLfg').onclick = () => { const t = lfgText(); copyTo(t, $('#rLfgMsg'), 'Texto copiado. ' + lfgLen(t)); };

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
  $('#edT').textContent = `Jugador ${edI + 1}` + (R.size > 5 ? ` · Grupo ${Math.floor(edI / PARTY) + 1}` : '');
  $('#edRace').innerHTML = RACES.filter(r => r.f === R.f).map(r => `<option value="${r.id}"${r.id === p.race ? ' selected' : ''}>${esc(raceName(r))}${r.paid ? ' (de pago)' : ''}</option>`).join('');
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
  else box.innerHTML = ['alliance', 'horde'].map(f => `<div class="rside ${f}"><h3>${FAC[f]}</h3>${RACES.filter(r => r.f === f).map(r => { const k = sel.indexOf(r.id); return `<button type="button" class="rp" data-id="${r.id}" aria-pressed="${k >= 0}">${esc(raceName(r))}${r.paid ? '<span class="tag paid">de pago</span>' : ''}<span class="no">${k + 1}</span></button>`; }).join('')}</div>`).join('');
  $('#cNote').textContent = `Elegidos ${sel.length} de 3`;
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
const ul = (items, cls) => items.length ? `<ul${cls ? ` class="${cls}"` : ''}>${items.map(x => `<li>${x}</li>`).join('')}</ul>` : '<span class="none">Ninguno</span>';
const row = (lab, vals, extra) => `<div class="crow${extra ? ' ' + extra : ''}"><div class="lab${extra === 'tiprow' ? ' tl' : ''}">${lab}</div>${vals.map(v => `<div class="val">${v}</div>`).join('')}</div>`;
function renderCmp() {
  const out = [];
  if (C.mode === 'class') {
    const ids = C.cls;
    out.push(`<div class="crow chead"><div class="lab"></div>${ids.map(id => `<div class="val" style="--cc:${CCOL[id]}"><picture><source type="image/avif" srcset="${art(id, 'avif')}"><img src="${art(id)}" width="360" height="482" alt="" loading="lazy" decoding="async"></picture><b>${esc(CL[id].n)}</b><a href="${classUrl(id)}">Página de la clase<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>`).join('')}</div>`);
    out.push(row('Roles', ids.map(id => CL[id].roles.map(r => `<span class="role">${ri(r)}${ROLE_RU[r]}</span>`).join(''))));
    out.push(row('Armadura', ids.map(id => racx(CX[id].armor))));
    out.push(row('Armas', ids.map(id => racx(CX[id].weapons))));
    out.push(row('Recurso', ids.map(id => esc(CX[id].resource))));
    out.push(row('Subida de nivel', ids.map(id => esc(CX[id].lvl))));
    out.push(row('Especializaciones', ids.map(id => ul(CX[id].specs.map(s => `<b>${esc(s.n)}</b>${SPEC_SEP}<span class="sub">${esc(s.what)}</span>`)))));
    out.push(row('Beneficio de banda', ids.map(id => BUFF[id] ? esc(BUFF[id]) : '<span class="none">Ninguno</span>')));
    out.push(row('En grupo', ids.map(id => ul(CX[id].group.map(esc)))));
    out.push(row('Profesiones', ids.map(id => ul(CPROF[id].map(p => `<b>${esc(p[0])}</b>${p[1] ? `<br><span class="sub">${esc(p[1])}</span>` : ''}`)) + `<a class="cgo" href="${HOME}guides/professions/#pairs=${id}">Objetos de campamento y habilidad<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a>`)));
    out.push(row('Puntos fuertes', ids.map(id => ul(CX[id].pros.map(esc), 'plus'))));
    out.push(row('Puntos débiles', ids.map(id => ul(CX[id].cons.map(esc), 'minus'))));
    ['alliance', 'horde'].forEach(f => out.push(row(`Razas: ${FAC[f]}`, ids.map(id => { const rs = RACES.filter(r => r.f === f && r.can[id]); return rs.length ? rs.map(r => `<a href="${raceUrl(r.id)}">${esc(raceName(r))}</a>`).join(', ') : '<span class="none">Ninguno</span>'; }))));
  } else {
    const ids = C.race;
    out.push(`<div class="crow chead"><div class="lab"></div>${ids.map(id => { const r = RC[id]; return `<div class="val race ${r.f}"><span class="fx">${FAC[r.f]}${r.paid ? ' · de pago' : ''}</span><b>${esc(raceName(r))}</b><a href="${raceUrl(id)}">Página de la raza<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>`; }).join('')}</div>`);
    out.push(row('Clases', ids.map(id => ul(Object.keys(RC[id].can).map(c => `<span style="color:${CCOL[c]}">●</span> ${esc(CL[c].n)}${RC[id].can[c] === 'new' ? ' <span class="tag new">nuevo</span>' : ''}`)))));
    out.push(row('Habilidades activas', ids.map(id => ul(RC[id].rac.filter(x => x[0] === 'a').map(x => `<b>${esc(x[1])}</b><br><span class="sub">${racx(x[2])}</span>`)))));
    out.push(row('Habilidades pasivas', ids.map(id => ul(RC[id].rac.filter(x => x[0] === 'p').map(x => `<b>${esc(x[1])}</b><br><span class="sub">${racx(x[2])}</span>`)))));
    out.push(row('Consejo', ids.map(id => esc(RC[id].tip)), 'tiprow'));
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
function facName(f) { return f === 'alliance' ? 'Alianza' : 'Horda'; }
function bi(ru) { return EN[ru] && EN[ru] !== ru ? `${esc(ru)} <span class="en">(${esc(EN[ru])})</span>` : esc(ru); }
function raceEn(r) { return r.en ? ` <span class="en">/ ${esc(r.en)}</span>` : ''; }
const tipBox = h => `<div class="tipbox"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg><p><span class="tl">Consejo</span>${h}</p></div>`;
function face(id, cc, cls = '', title = '', f) { return `<span class="av ${cls}" style="--cc:${cc}"${title ? ` title="${esc(title)}"` : ''}><img src="${ROOT}assets/art/${porId(id, f)}-face.webp${PV}" width="160" height="160" alt="" loading="lazy" decoding="async"></span>`; }
function lvlMeter(c) {
  const p = c.lp || 0, w = Math.min(Math.abs(p) / 12 * 46, 46);
  const label = p < 0 ? `Más rápido en ${-p}%` : p > 0 ? `Más lento en ${p}%` : 'Ritmo medio';
  const bar = p ? `<i class="${p > 0 ? 'slow' : ''}" style="${p < 0 ? 'right' : 'left'}:50%;width:${w}%"></i>` : '';
  return `<span class="lvl"><span>${label}</span><span class="bar" role="img" aria-label="${label}">${bar}</span><span class="scale" aria-hidden="true"><span>más rápido</span><span>más lento</span></span></span>`;
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
  let h = '<thead><tr><th scope="col">Raza</th>';
  CLASSES.forEach(c => { h += `<th scope="col" class="${roleMatch(c, state.r) ? '' : 'dim'}${c.id === state.cls ? ' selc' : ''}">${face(c.id, CCOL[c.id])}${esc(c.n)}</th>`; });
  h += '</tr></thead><tbody>';
  ['alliance', 'horde'].forEach(f => {
    const rows = RACES.filter(r => r.f === f && raceVisible(r));
    if (!rows.length) return;
    h += `<tr class="fh ${f}"><th colspan="${CLASSES.length + 1}" scope="rowgroup"><span class="f ${f}"></span>${facName(f)}</th></tr>`;
    rows.forEach(r => {
      h += `<tr class="${r.id === state.race ? 'rowsel' : ''}"><th scope="row"><span class="rn">${face(RSLUG[r.id], `var(--${r.f})`)}${esc(r.n)}${r.paid ? '<span class="paid">de pago</span>' : ''}</span></th>`;
      CLASSES.forEach(c => {
        const v = r.can[c.id];
        const dim = roleMatch(c, state.r) ? '' : ' dim';
        if (!v) { h += `<td><span class="cell no${dim}" role="img" aria-label="${esc(r.n)} ${esc(c.n)}: no permitido"></span></td>`; return; }
        const sel = (r.id === state.race && c.id === state.cls) ? ' sel' : '';
        const label = `${r.n} ${c.n}${v === 'new' ? ', combinación nueva' : ''}`;
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
  const rac = r.rac.map(x => `<div class="card ab"><span class="abt${x[0] === 'a' ? '' : ' p'}">${x[0] === 'a' ? 'Activa' : 'Pasiva'}</span><b>${bi(x[1])}</b><span>${racx(x[2])}</span></div>`).join('');
  const text = `${r.name || r.n} ${c.n} (${facName(r.f)})${r.paid ? ', requiere el pack Skyborne' : ''}`;
  $('#detail').innerHTML = `
    <div class="d-head">
      <div class="d-art" aria-hidden="true"><picture><source type="image/avif" srcset="${ROOT}assets/art/${RSLUG[r.id]}-600.avif${PV}"><img src="${ROOT}assets/art/${RSLUG[r.id]}-600.webp${PV}" width="600" height="804" alt="" loading="lazy" decoding="async"></picture></div>
      <div class="d-avs">${face(RSLUG[r.id], `var(--${r.f})`)}</div>
      <div class="d-title"><h3>${esc(r.n)}${raceEn(r)} · ${esc(c.n)}</h3>
        <div class="chips"><span class="tag ${r.f}">${facName(r.f)}</span>${isNew ? '<span class="tag new">Combinación nueva</span>' : ''}${r.paid ? '<span class="tag paid">Raza de pago</span>' : ''}${roleChips(c)}</div></div>
    </div>
    <div class="d-body">
      <div class="d-cols">
        <div><h4>Especializaciones</h4><div class="cards">${specs}</div></div>
        <div><h4>Habilidades raciales</h4><div class="cards two">${rac}</div></div>
      </div>
      <div class="facts3">
        <div class="fact"><h4>Subida de nivel</h4>${lvlMeter(c)}</div>
        <div class="fact"><h4>En bandas</h4><span>${esc(c.raid)}.</span></div>
        <div class="fact"><h4>Novedades</h4><span>${esc(c.forever)}</span></div>
      </div>
      ${tipBox(esc(r.tip))}
      ${pickLinks(r, c)}
      <div class="copyrow">
        <input id="pickText" readonly value="${esc(text)}" aria-label="Mi elección">
        <button class="btn" id="copyBtn"><svg class="ico" aria-hidden="true"><use href="#i-copy"/></svg>Copiar mi elección</button>
        <button class="btn ghost" id="shareBtn">Compartir</button>
        <span class="small" id="copyMsg" role="status"></span>
      </div>
    </div>`;
  $('#copyBtn').onclick = () => copyTo($('#pickText').value, $('#copyMsg'), 'Copiado');
  $('#shareBtn').onclick = () => shareBuild(r.id, c.id, state.spec, text);
}
/* Share: the link of the card page b/<race>-<class>-<spec>/ (its preview is the card with the name); on a phone the share sheet, else the clipboard */
function shareBuild(race, cls, spec, text) {
  const url = new URL(`${HOME}b/${BSLUG[race] || race}-${cls}-${spec}/`, location.href).href, msg = $('#copyMsg');
  if (navigator.share && matchMedia('(pointer: coarse)').matches) navigator.share({ title: text, url }).catch(e => { if (e && e.name !== 'AbortError') copyTo(url, msg, 'Enlace copiado'); });
  else copyTo(url, msg, 'Enlace copiado');
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
  cas: ['Europa', 'El Cáucaso y Asia Central no tienen región propia; la más cercana es Europa.'],
  mea: ['Europa', 'Oriente Medio y África no tienen región propia; la más cercana es Europa.'],
  na: ['América y Oceanía', ''],
  la: ['América y Oceanía', 'Latinoamérica juega en la región de América.'],
  oce: ['América y Oceanía', 'Blizzard agrupa Oceanía con América en una sola región. Blizzard no ha dicho si hay servidores en la propia Oceanía.'],
  kr: ['Corea', ''],
  tw: ['Taiwán', ''],
  asia: ['', 'No hay región propia. Las más cercanas en el mapa son Taiwán y Corea. Elige la que tenga menos latencia World.'],
};
function renderPing() {
  const v = $('#pgW').value, r = PG[v];
  try { if (v) localStorage.setItem('gabella-ping', v); } catch (e) {}
  if (!r) { $('#pgOut').innerHTML = ''; return; }
  $('#pgOut').innerHTML = (r[0] ? `<p class="preg">Tu región: ${esc(r[0])}</p>` : '') + '<ul class="verdict">'
    + (r[1] ? `<li>${esc(r[1])}</li>` : '')
    + '<li>No hay reinos: eliges región y reglas, no un servidor. La región se elige en Battle.net antes de iniciar el juego.</li>'
    + '<li>Cada región tiene sus propios personajes y nombres. Solo se juega juntos dentro de una región.</li>'
    + '<li>Blizzard no ha dicho dónde están los servidores de las regiones.</li></ul>';
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
