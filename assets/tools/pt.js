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
const EN = {
  'Armas':'Armas','Fúria':'Fúria','Proteção':'Proteção','Sagrado':'Sagrado','Retribuição':'Retribuição',
  'Domínio das Feras':'Domínio das Feras','Precisão':'Precisão','Sobrevivência':'Sobrevivência',
  'Assassinato':'Assassinato','Combate':'Combate','Subterfúgio':'Subterfúgio',
  'Disciplina':'Disciplina','Sombra':'Sombra','Elemental':'Elemental','Aperfeiçoamento':'Aperfeiçoamento','Restauração':'Restauração',
  'Arcano':'Arcano','Fogo':'Fogo','Gélido':'Gélido','Suplício':'Suplício','Demonologia':'Demonologia','Destruição':'Destruição',
  'Equilíbrio':'Equilíbrio','Combate Feral':'Combate Feral',
  'Desejo de Sobreviver':'Desejo de Sobreviver','Percepção':'Percepção','Ruthless':'Ruthless','O Espírito Humano':'O Espírito Humano',
  'Forma de Pedra':'Forma de Pedra','Localizar Tesouros':'Localizar Tesouros','Earth Fury':'Earth Fury','Big Game Hunter':'Big Game Hunter',
  'Luz de Eluna':"Luz de Eluna",'Fusão Sombria':'Fusão Sombria','Rapidez':'Rapidez','Espírito de Fogo-fátuo':'Espírito de Fogo-fátuo',
  'Artista da Fuga':'Artista da Fuga','Eureca!':'Eureca!','Mente Expansiva':'Mente Expansiva','Especialização em Engenharia':'Especialização em Engenharia',
  'Walk on Air':'Walk on Air','Read Ley Line':'Read Ley Line','Wind Blessed':'Wind Blessed','Elemental Insight':'Elemental Insight','Skysight':'Skysight',
  'Fúria Sangrenta':'Fúria Sangrenta','Shatter Curse':'Shatter Curse','Savage':'Savage','Comando':'Comando','Robustez':'Robustez',
  'Determinação dos Renegados':'Determinação dos Renegados','Canibalizar':'Canibalizar','Respiração Subaquática':'Respiração Subaquática','Toque do Túmulo':'Toque do Túmulo',
  'Pisada de Guerra':'Pisada de Guerra','Cultivo':'Cultivo','Vencer Planícies':'Vencer Planícies','Resistência':'Resistência',
  'Berserk':'Berserk','Regeneração Rápida':'Regeneração Rápida','Matança de Feras':'Matança de Feras','Regeneração':'Regeneração'
};
RC.skyA.en = 'High Order Skyborne'; RC.skyH.en = 'Windshaper Skyborne';
const CX = {"warrior": {"armor": "Tecido, couro, malha; placas a partir do nível 40 {beta}", "weapons": "Tudo exceto varinhas; escudo", "resource": "Raiva", "lvl": "A evolução mais lenta, cerca de 12% mais longa que a média (estimativa do LFCarry)", "group": ["Brado de Batalha afeta a raide toda", "Brado Desmoralizador e Fender Armadura no chefe", "Golpes a Esmo e Redemoinho para lutas com vários alvos"], "pros": ["Melhor tanque e dano corpo a corpo forte", "Bom para PvP (Armas)", "Poucos botões, fácil de entender"], "cons": ["Evolução mais lenta", "Depende muito do equipamento", "Quase sem autocura ou controle de grupo"], "specs": [{"n": "Armas", "what": "Dano corpo a corpo (arma de duas mãos)"}, {"n": "Fúria", "what": "Dano corpo a corpo (duas armas)"}, {"n": "Proteção", "what": "Tanque"}]}, "paladin": {"armor": "Tecido, couro, malha; placas a partir do nível 40; escudo {beta}", "weapons": "Machados, maças, espadas, armas de haste a partir do nível 20 {beta}", "resource": "Mana", "lvl": "Ritmo de evolução médio", "group": ["Auras de grupo: Devoção, Retribuição, Concentração", "Auras de resistência a Fogo, Gelo e Sombra para a raide toda", "Bênçãos de uma hora, bênçãos maiores para uma classe inteira", "Selo da Justiça impede os inimigos de fugir"], "pros": ["As três funções num só personagem", "Bônus de grupo fortes", "Placas e um personagem resistente"], "cons": ["Sem aproximação, lentidão ou aumento de velocidade", "Pouco controle de grupo além de Martelo da Justiça", "Retribuição caiu depois do patch"], "specs": [{"n": "Sagrado", "what": "Curador"}, {"n": "Proteção", "what": "Tanque"}, {"n": "Retribuição", "what": "Dano corpo a corpo"}]}, "hunter": {"armor": "Tecido, couro; malha a partir do nível 40 {beta}", "weapons": "Arcos, bestas, armas de fogo, machados, espadas, armas de haste", "resource": "Mana; o mascote usa Foco", "lvl": "A evolução mais rápida, cerca de 8% mais rápida que a média (estimativa do LFCarry)", "group": ["Aura de Tiro Certeiro aumenta o dano à distância do grupo", "Armadilha Congelante: controle de grupo confiável", "Tiro de Dispersão interrompe conjurações", "Aspecto da Matilha acelera o grupo todo na estrada"], "pros": ["Evolução mais rápida", "Ótimo sozinho", "Armadilhas e controle de grupo"], "cons": ["Zona morta de curta distância até 8 metros", "Você precisa gerenciar o mascote", "Os talentos de Sobrevivência tinham bugs no beta"], "specs": [{"n": "Domínio das Feras", "what": "Dano à distância, muito dano vindo do mascote"}, {"n": "Precisão", "what": "Dano à distância"}, {"n": "Sobrevivência", "what": "Corpo a corpo e à distância, armadilhas"}]}, "rogue": {"armor": "Tecido, couro", "weapons": "Adagas, espadas, maças, armas de punho, machados de uma mão, arremesso", "resource": "Energia e pontos de combo", "lvl": "Ritmo de evolução médio", "group": ["Dano corpo a corpo puro, sem bônus para a raide toda", "Aturdir, Cegar e Golpe no Rim: muito controle de grupo", "Chute interrompe conjurações perigosas"], "pros": ["Dano muito alto que escala com o equipamento", "Furtividade e muito controle de grupo", "Liberdade na escolha de armas"], "cons": ["Depende muito do equipamento", "Sem autocura", "Só Evasão e Sumir salvam você"], "specs": [{"n": "Assassinato", "what": "Dano de venenos"}, {"n": "Combate", "what": "Ataques rápidos com armas"}, {"n": "Subterfúgio", "what": "Emboscadas, sangramentos"}]}, "priest": {"armor": "Tecido", "weapons": "Adagas, maças, báculos, varinhas", "resource": "Mana", "lvl": "Cerca de 5% mais lento que a média (estimativa do LFCarry)", "group": ["Espírito Divino e Palavra de Poder: Fortitude para a raide toda", "Infusão de Poder fortalece um aliado", "O principal curador do grupo"], "pros": ["Um grupo sempre precisa", "Cura ou dano de sombra", "Muitas builds"], "cons": ["Só tecido, frágil", "Poucas formas de se mover rápido", "Aceleração quase não ajuda os feitiços"], "specs": [{"n": "Disciplina", "what": "Curador, escudos e absorção"}, {"n": "Sagrado", "what": "Curador"}, {"n": "Sombra", "what": "Dano à distância"}]}, "shaman": {"armor": "Tecido, couro; malha a partir do nível 40; escudo {beta}", "weapons": "Maças, machados, báculos, armas de punho, adagas", "resource": "Mana", "lvl": "Ritmo de evolução médio", "group": ["Os totens Força da Terra, Fúria dos Ventos, Labaredas e Graça do Ar dão bônus ao próprio grupo", "Totem Sísmico remove medo, sono e enfeitiçamento", "Totens que purificam venenos e doenças", "Expurgar remove bônus dos inimigos"], "pros": ["Totens fortes para o grupo", "Evolução com mobilidade", "Novos talentos fortes"], "cons": ["Sem controle de grupo forte", "Mana em lutas longas", "Tanquear ainda não confirmado"], "specs": [{"n": "Elemental", "what": "Dano à distância"}, {"n": "Aperfeiçoamento", "what": "Dano corpo a corpo. A capacidade de tanquear ainda é incerta"}, {"n": "Restauração", "what": "Curador"}]}, "mage": {"armor": "Tecido", "weapons": "Adagas, espadas, báculos, varinhas", "resource": "Mana", "lvl": "A evolução mais rápida, cerca de 8% mais rápida que a média, cerca de 12 horas economizadas (estimativa do LFCarry)", "group": ["Portais a partir do nível 40, teleportes a partir do 20", "Comida e água para o grupo", "Polimorfia: controle de grupo confiável", "Remover Maldição Inferior"], "pros": ["Evolução mais rápida", "Portais e comida para todos", "Três árvores fortes e diferentes"], "cons": ["Só tecido, frágil", "A mana acaba rápido", "Dano em área atenuado"], "specs": [{"n": "Arcano", "what": "Explosão de dano, muita mana"}, {"n": "Fogo", "what": "Críticos e ignições"}, {"n": "Gélido", "what": "Dano e controle"}]}, "warlock": {"armor": "Tecido", "weapons": "Adagas, espadas, báculos, varinhas", "resource": "Mana; Conversão de Vida transforma vida em mana", "lvl": "Ritmo de evolução médio", "group": ["Pedra de Vida e Pedra da Alma", "Ritual de Evocação: reúne o grupo", "Maldição de Línguas deixa a conjuração 60% mais lenta", "Maldição dos Elementos: mais dano mágico no alvo"], "pros": ["Autossuficiente: um demônio e Conversão de Vida", "Muita utilidade para o grupo", "Dano ao longo do tempo forte"], "cons": ["Frágil e pouco móvel", "O dano demora para engrenar", "Sem teleporte curto nem disparada"], "specs": [{"n": "Suplício", "what": "Dano de maldições e corrupção"}, {"n": "Demonologia", "what": "Dano por meio de demônios"}, {"n": "Destruição", "what": "Dano direto de fogo e de sombra"}]}, "druid": {"armor": "Tecido, couro", "weapons": "Adagas, maças, báculos, armas de punho, armas de haste a partir do nível 20 {beta}", "resource": "Mana; Raiva na Forma de Urso, Energia na Forma de Felino", "lvl": "Cerca de 5% mais lento que a média (estimativa do LFCarry)", "group": ["Líder do Bando e Aura de Luniscante afetam a raide toda e se acumulam", "Renascimento: ressurreição em combate", "Avivar devolve mana a um curador", "Remove maldições e venenos"], "pros": ["As três funções num só personagem", "Ótima mobilidade", "Ressurreição em combate"], "cons": ["Sem bloqueio nem aparo para o urso", "Efeitos de cura ao longo do tempo são mais difíceis de acompanhar", "Os números finais de raide ainda são desconhecidos"], "specs": [{"n": "Equilíbrio", "what": "Dano à distância"}, {"n": "Combate Feral", "what": "Tanque (urso) e dano corpo a corpo (gato)"}, {"n": "Restauração", "what": "Curador, muita cura ao longo do tempo"}]}};
const HC = {"tx":{"title":"Meu personagem","lead":"Sem login nem senha: escolha classe, especialização e raça, e o site se adapta a você.","local":"Salvo apenas neste navegador.","none":"Ainda sem personagem","create":"Criar personagem","edit":"Editar","reset":"Excluir personagem","resetQ":"Apagar o personagem deste navegador?","steps":["Lado","Classe e especialização","Raça","Aparência","Detalhes"],"side":"Por quem você joga?","cls":"Classe","spec":"Especialização","race":"Raça","bestFor":"Melhor raça para %s","best":"a melhor","paid":"paga","sex":"Sexo","m":"Masculino","f":"Feminino","bg":"Fundo do retrato","lvl":"Nível","reg":"Região","lvlReg":"Nível e região","regs":{"us":"Américas e Oceania","eu":"Europa","kr":"Coreia","tw":"Taiwan"},"p1":"Profissão 1","p2":"Profissão 2","secP":"Profissões secundárias","noP":"Nenhum","role":"Função","back":"Voltar","next":"Continuar","done":"Pronto","cancel":"Cancelar","later":"Você pode preencher depois.","levelN":"Nível %n","build":"Minha build de talentos","buildD":"Talentos de %s por nível.","pairs":"Pares de profissões","pairsD":"Quais profissões combinam com a sua classe.","bestR":"Melhores raças","bestRD":"Raça para a sua classe nas duas facções.","lvlG":"Evolução da classe","lvlGD":"Rota e talentos 1–60.","day1":"Dia 1 para o seu personagem","day1D":"O checklist de lançamento com a sua classe e raça.","play":"No jogo","playD":"Zonas e masmorras para o seu nível, timers, rádio.","dung":"Masmorras para o seu nível","dungNo":"Informe o seu nível e escolheremos masmorras.","dungFirst":"As primeiras masmorras abrem no nível 13.","resetH":"Reinício semanal","resetIn":"em %s","resetNote":"A Blizzard ainda não anunciou o horário de reinício do Forever. Mostrado como em outras versões de WoW desta região: vamos conferir no lançamento.","resetUnk":"Vamos confirmar o horário de reinício desta região no lançamento.","resetNoReg":"Informe a sua região para ver o reinício semanal.","resetWhy":"As raides abrem em 09.12 e têm bloqueio semanal.","lfg":"Texto para procurar grupo","lfgD":"Cole no chat LookingForGroup. Nomes como no jogo.","lfgP":{"tank":"%c tanque procura grupo","heal":"%c curador procura grupo","dps":"%c procura grupo"},"lfgT":"%p: %d, nível %l.","lfgT0":"%p.","allD":"Todas as masmorras","copy":"Copiar","copied":"Copiado","sync":"Sincronizar entre dispositivos","syncD":"Você só precisa entrar para isto: o personagem fica no celular e no PC, e a carta do lançamento chega por e-mail se você se inscrever.","yourCls":"Seu %s","bTalents":"Talentos","bSpec":"Build: %s","bLevel":"Evolução","bGroup":"Grupo","bNews":"Notícias","copiedT":"Copiado: %s","profsL":"Profissões","day1n":"Dia 1: %n de %t","collect":"Monte seu personagem","collectD":"Classe, especialização e raça: talentos, evolução, grupo e notícias da sua classe.","change":"Trocar","allSet":"Todas as configurações","close":"Fechar","mine":"Sobre a sua classe","share":"Compartilhar","linkCopied":"Link copiado","make":"Tornar meu personagem","made":"Este é o seu personagem","plaqueH":"Meu personagem","plaqueD":"Classe, especialização e raça em um minuto, e depois sua build, profissões e masmorras.","day1Mine":"Para o seu personagem","ckClass":"Sua especialização, %s: a build de talentos por nível.","ckRaceOk":"%r é a melhor raça para a sua especialização.","ckRaceAlt":"Melhor raça para a sua especialização: %r.","ckProfs":"Pares de profissões para %s.","ckStart":"Evolução de %s: rota e primeiros talentos.","ckPing":"Sua região: %s.","or":"ou"},"best":{"warrior":{"alliance":{"*":[["human","nightelf"],"Humano: +1% de crítico com qualquer arma. Elfo Noturno: +10% de crítico por 15 s. As fontes se dividem quase igualmente."],"protection":[["dwarf"],"Forma de Pedra reduz o dano físico em 10% e remove sangramentos."]},"horde":{"*":[["orc"],"Fúria Sangrenta: +10% de poder de ataque por 15 s. Antes das mudanças de raças de 26.10, todas as fontes a colocavam em primeiro."],"protection":[["tauren"],"Resistência dá +5% de vida, Pisada de Guerra atordoa inimigos próximos."]}},"paladin":{"alliance":{"*":[["human"],"Ruthless reforça golpes e feitiços, Desejo de Sobreviver remove atordoamentos."],"protection":[["dwarf"],"Forma de Pedra e Artisan’s Precision: +1% de chance de acerto."]},"horde":{"*":[["undead"],"Na Horda, só o Morto-vivo pode ser paladino. Canibalizar recupera mana, Determinação dos Renegados remove medo."]}},"hunter":{"alliance":{"*":[["human","nightelf"],"Humano: +1% de crítico, e o mascote herda o crítico. Elfo Noturno: Luz de Eluna e Fusão Sombria."]},"horde":{"*":[["orc","troll"],"Orc: Fúria Sangrenta e Comando (+5% de dano do mascote). Troll: +5% de dano contra feras."]}},"rogue":{"alliance":{"*":[["nightelf"],"Fusão Sombria agora reduz a ameaça também em combate, além de A graça de Eluna e Rapidez."]},"horde":{"*":[["orc"],"Fúria Sangrenta: +10% de poder de ataque por 15 s."]}},"priest":{"alliance":{"*":[["gnome"],"Todas as fontes a escolhem: Eureca! também reforça Palavra de Poder: Escudo, Inquisitive Mind dá +5% de mana."]},"horde":{"*":[["undead","troll"],"As fontes divergem. Morto-vivo é mais forte no PvP: Determinação dos Renegados remove medo, sono e encanto."]}},"shaman":{"alliance":{"*":[["dwarf"],"Na Aliança, só o Anão pode ser xamã: Forma de Pedra e Artisan’s Precision (+1% de chance de acerto)."]},"horde":{"*":[["orc"],"Fúria Sangrenta dá poder de ataque e poder mágico: serve para Elemental e Aperfeiçoamento."],"restoration":[["troll"],"Para curador, uma fonte recomenda Troll: Berserk, +10% de velocidade de conjuração por 12 s."]}},"mage":{"alliance":{"*":[["gnome"],"Eureca! por 8 s, Inquisitive Mind: +5% de mana, Artista da Fuga quebra raízes."]},"horde":{"*":[["orc"],"Orc mago é uma combinação nova do Forever: Fúria Sangrenta agora dá poder mágico."]}},"warlock":{"alliance":{"*":[["gnome","human"],"Gnomo: Eureca! e Inquisitive Mind. Humano: dano periódico pode ser crítico, e Ruthless dá +1% de crítico."]},"horde":{"*":[["orc","undead"],"Orc: Fúria Sangrenta dá poder mágico. Morto-vivo é mais escolhido no PvP."]}},"druid":{"alliance":{"*":[["nightelf"],"A graça de Eluna: +10% de crítico por 15 s, e Rapidez."]},"horde":{"*":[["tauren"],"Resistência: +5% de vida, Pisada de Guerra funciona também em formas."]}}},"sid":{"warrior":["arms","fury","protection"],"paladin":["holy","protection","retribution"],"hunter":["beast-mastery","marksmanship","survival"],"rogue":["assassination","combat","subtlety"],"priest":["discipline","holy","shadow"],"shaman":["elemental","enhancement","restoration"],"mage":["arcane","fire","frost"],"warlock":["affliction","demonology","destruction"],"druid":["balance","feral","restoration"]},"sn":{"warrior":["Armas","Fúria","Proteção"],"paladin":["Sagrado","Proteção","Retribuição"],"hunter":["Domínio das Feras","Precisão","Sobrevivência"],"rogue":["Assassinato","Combate","Subterfúgio"],"priest":["Disciplina","Sagrado","Sombra"],"shaman":["Elemental","Aperfeiçoamento","Restauração"],"mage":["Arcano","Fogo","Gélido"],"warlock":["Suplício","Demonologia","Destruição"],"druid":["Equilíbrio","Combate Feral","Restauração"]},"fn":{"alliance":"Aliança","horde":"Horda"},"reset":{"us":[2,15],"eu":[3,4],"kr":null,"tw":null},"rn":{"human":"Humano","dwarf":"Anão","nightelf":"Elfo Noturno","gnome":"Gnomo","skyA":"Skyborne da High Order","orc":"Orc","undead":"Morto-vivo","tauren":"Taureno","troll":"Troll","skyH":"Skyborne Windshaper"},"rf":{"human":"alliance","dwarf":"alliance","nightelf":"alliance","gnome":"alliance","skyA":"alliance","orc":"horde","undead":"horde","tauren":"horde","troll":"horde","skyH":"horde"},"cn":{"warrior":"Guerreiro","paladin":"Paladino","hunter":"Caçador","rogue":"Ladino","priest":"Sacerdote","shaman":"Xamã","mage":"Mago","warlock":"Bruxo","druid":"Druida"},"cen":{"warrior":"Warrior","paladin":"Paladin","hunter":"Hunter","rogue":"Rogue","priest":"Priest","shaman":"Shaman","mage":"Mage","warlock":"Warlock","druid":"Druid"}};
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

const CPROF = {"warrior": [["Evolução: Ferraria + Mineração", ""], ["Nível 60: Engenharia + Mineração", "O ferreiro se veste de placas e armas, e muitas receitas são pessoais. O engenheiro ganha granadas e engenhocas que faltam ao guerreiro."]], "paladin": [["Evolução: Ferraria + Mineração", ""], ["Nível 60: Proteção, Retribuição: Engenharia + Mineração. Sagrado: Alquimia + Herborismo", "Sagrado gasta muito mana: as poções são suas, e o Mana Well no acampamento substitui a Bênção de Sabedoria."]], "hunter": [["Evolução: Couraria + Esfolamento", ""], ["Nível 60: Engenharia + Mineração", "O coureiro faz o próprio couro e a própria malha e Armor Kits. O engenheiro faz miras e armas de fogo."]], "rogue": [["Evolução: Couraria + Esfolamento", ""], ["Nível 60: Engenharia + Mineração", "O couro é seu, e a Camp Tent dá descanso. A Engenharia é a profissão principal para PvP."]], "priest": [["Evolução: Alfaiataria + Encantamento", ""], ["Nível 60: Alfaiataria + Engenharia ou Encantamento", "O alfaiate faz cintos com poder mágico desde o nível 10, o encantador faz varinhas com poder mágico desde o 5. O que é costurado se desencanta em materiais."]], "shaman": [["Evolução: Couraria + Esfolamento", ""], ["Nível 60: Alquimia + Herborismo", "O coureiro faz itens com poder mágico para Elemental e Restauração e equipamento para Aperfeiçoamento. Em raide e em grupo, poções fazem falta."]], "mage": [["Evolução: Alfaiataria + Encantamento", ""], ["Nível 60: Alfaiataria + Encantamento; para PvP e grandes grupos de inimigos Engenharia + Mineração", "O alfaiate dá equipamento inicial com poder mágico, e o que é costurado se desencanta. As granadas do engenheiro seguram grandes grupos de inimigos no lugar."]], "warlock": [["Evolução: Alfaiataria + Encantamento", ""], ["Nível 60: Alfaiataria + Alquimia", "O Faction Banner do alfaiate dá Espírito para Conversão de Vida. Alquimia é poção e ouro."]], "druid": [["Evolução: Couraria + Esfolamento ou Herborismo", ""], ["Nível 60: Alquimia + Herborismo", "As ervas se coletam em Forma de Viagem, e as poções se bebem em qualquer forma. Mana Well e Incense Candle servem para Equilíbrio e Restauração."]]};   /* recommended profession pairs per class, already in the page language (build.class_profs) */
const $ = s => document.querySelector(s);
const ROOT = '../../', HOME = '../';
function esc(s) { return String(s).replace(/[&<>"]/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m])); }
function raceName(r) { return r.name || r.n; }
function syncSeg(id, v) { document.querySelectorAll(`#${id} button`).forEach(b => b.setAttribute('aria-pressed', b.dataset.v === String(v))); }
const FAC = { alliance: 'Aliança', horde: 'Horda' };
const BSLUG = { skyA: 'skyborne-a', skyH: 'skyborne-h' };   // race id -> url part of the share page (tools/make_build_cards.py SLUG)
const RSLUG = { human: 'human', dwarf: 'dwarf', nightelf: 'night-elf', gnome: 'gnome', skyA: 'skyborne-alliance', orc: 'orc', undead: 'undead', tauren: 'tauren', troll: 'troll', skyH: 'skyborne-horde' };
const PAINTED = ["druid-nightelf", "druid-tauren", "hunter-nightelf", "hunter-orc", "mage-gnome", "mage-orc", "paladin-human", "paladin-undead", "priest-gnome", "priest-undead", "rogue-nightelf", "rogue-orc", "shaman-dwarf", "shaman-orc", "warlock-gnome", "warlock-orc", "warrior-human", "warrior-orc"];   // class x race paintings that exist (build_tools.painted): the player's own race is drawn, never the best race of the side
const unitArt = (p, ext) => `${ROOT}assets/art/${PAINTED.includes(p.cls + '-' + p.race) ? p.cls + '-' + p.race : RSLUG[p.race]}-360.${ext}${PV}`;
const classUrl = id => `${HOME}classes/${id}/`, raceUrl = id => `${HOME}races/${RSLUG[id]}/`;
const PV = /*PV*/'?v=03c9d4a0';   // ?v= of the class and race portraits (build.art_version)
const porId = (id, f) => (window.GabellaPor ? GabellaPor.id(id, f) : id);   // a class: the portrait of side f, else of the reader's side (build.por_js)
const art = (id, ext = 'webp', f) => `${ROOT}assets/art/${porId(id, f)}-360.${ext}${PV}`;
async function copyTo(text, msgEl, ok) {
  try { await navigator.clipboard.writeText(text); msgEl.textContent = ok; } catch (e) { msgEl.textContent = 'Não foi possível copiar, selecione o texto e pressione Ctrl+C'; }
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
const LFG = {"d": [["Cavernas Ígneas", 13, 18, "horde"], ["Hall of Thanes", 13, 18, 0], ["Ruínas de Lordaeron", 15, 20, 0], ["Minas Mortas", 15, 22, 0], ["Caverna Ululante", 17, 24, 0], ["Bastilha da Presa Negra", 20, 26, 0], ["Profundezas Negras", 22, 28, 0], ["O Cárcere", 25, 29, "alliance"], ["Excavation Site: Wetlands", 26, 31, 0], ["City of Dalaran", 28, 33, 0], ["Gnomeregan", 29, 38, 0], ["Urzal dos Tuscos", 29, 38, 0], ["Monastério Escarlate: Cemitério", 30, 38, 0], ["Monastério Escarlate: Biblioteca", 33, 41, 0], ["The Drowned City", 35, 40, 0], ["Monastério Escarlate: Arsenal", 36, 44, 0], ["Uldaman", 36, 45, 0], ["Urzal dos Mortos", 37, 46, 0], ["Monastério Escarlate: Catedral", 38, 46, 0], ["Zul’Farrak", 40, 47, 0], ["Krol’dok Stronghold", 40, 45, 0], ["Maraudon", 45, 51, 0], ["Alcaz Island Prison", 48, 53, 0], ["Templo de Atal’Hakkar", 50, 55, 0], ["Abismo Rocha Negra", 52, 60, 0], ["Blackmaw Hold", 55, 60, 0], ["Pico da Rocha Negra Inferior", 57, 60, 0], ["Gládio Cruel: Leste", 58, 60, 0], ["Shaper’s Terrace", 58, 60, 0], ["Stratholme: vivos", 58, 60, 0], ["Stratholme: mortos-vivos", 58, 60, 0], ["Scolomântia", 58, 60, 0], ["Pico da Rocha Negra Superior", 60, 60, 0], ["Gládio Cruel: Oeste", 60, 60, 0], ["Gládio Cruel: Norte", 60, 60, 0]], "r": {"10": "Barrow Deeps", "20": "Pico Hyjal", "40": "Covil da Onyxia"}};   // dungeons [name, min, max, entrance faction] and raids {size: name} in the client's language (build_tools)
const CHAT_MAX = 255, CANON = 'https://gabella.site/wow/pt/tools/'.replace(/^https?:\/\//, '');
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
  const head = (L.d ? '%d — procuramos: %n.' : 'Grupo procura: %n.').replace('%d', L.d).replace('%n', roles);
  const parts = [head, L.s ? 'Estilo: %s.'.replace('%s', L.s) : '', CANON + shortHash()].filter(Boolean);
  const bytes = t => new TextEncoder().encode(t).length;
  let text = parts.join(' ');
  if (bytes(text) > CHAT_MAX) text = parts.slice(0, -1).join(' ');   // a long raid code would not fit: the link goes first
  return text;
}
function renderLfg() {
  const places = lfgPlaces(), sel = $('#lfgD');
  if (!places.some(p => p[0] === L.d)) L.d = R.size === 5 ? '' : (places[0] || [''])[0];
  $('#lfgDL').textContent = R.size === 5 ? 'Masmorra' : 'Raide';
  sel.innerHTML = (R.size === 5 ? '<option value="">Qualquer masmorra</option>' : '') + places.map(([v, t]) => `<option value="${esc(v)}"${v === L.d ? ' selected' : ''}>${esc(t)}</option>`).join('');
  syncSeg('lfgS', L.s);
  const text = lfgText();
  $('#rLfg').value = text;
  $('#rCopyLfg').disabled = !text;
  $('#rLfgMsg').textContent = text ? lfgLen(text) : R.s.some(Boolean) ? 'Todas as vagas estão ocupadas.' : 'Adicione pelo menos um jogador ao grupo.';
}
function lfgLen(t) { return 'Caracteres: %n de %m (limite de uma linha do chat).'.replace('%n', t.length).replace('%m', CHAT_MAX); }

function unitHTML(p, i) {
  const cls = R.moving === i ? ' src' : '';
  if (!p) return `<button type="button" class="unit empty${cls}" data-i="${i}"><span class="up" aria-hidden="true">+</span><span class="ub"><b>Vaga livre</b><span>Clique para adicionar um jogador</span></span></button>`;
  const c = CL[p.cls], r = RC[p.race];
  return `<button type="button" class="unit${cls}" data-i="${i}" draggable="true" style="--cc:${CCOL[p.cls]};--pc:${power(p)}" aria-label="${esc((p.name || `Jogador ${i + 1}`) + ', ' + raceName(r) + ' ' + c.n + ', ' + ROLE_RU[p.role])}">
    <span class="up"><picture><source type="image/avif" srcset="${unitArt(p, 'avif')}"><img src="${unitArt(p, 'webp')}" width="360" height="482" alt="" loading="lazy" decoding="async"></picture></span>
    <span class="ub"><span class="un"><span class="ur" title="${ROLE_RU[p.role]}">${ri(p.role)}</span><b>${esc(p.name || c.n)}</b><small>${esc(raceName(r))} · ${esc(c.n)}</small></span><span class="hp"><i></i></span><span class="mp"></span></span></button>`;
}
function cellHTML(p, i) {
  const cls = R.moving === i ? ' src' : '';
  if (!p) return `<button type="button" class="rc empty${cls}" data-i="${i}" aria-label="Vaga livre ${i + 1}"><span aria-hidden="true">+</span>Adicionar</button>`;
  const c = CL[p.cls], r = RC[p.race];
  return `<button type="button" class="rc${cls}" data-i="${i}" draggable="true" style="--cc:${CCOL[p.cls]};--pc:${power(p)}" aria-label="${esc((p.name || `Jogador ${i + 1}`) + ', ' + raceName(r) + ' ' + c.n + ', ' + ROLE_RU[p.role])}" title="${esc(raceName(r) + ' · ' + c.n + ' · ' + ROLE_RU[p.role])}"><b>${esc(p.name || c.n)}</b><small>${esc(p.name ? c.n : raceName(r))}</small>${ri(p.role)}</button>`;
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
      const st = n && (!c.tank || !c.heal) ? `<span class="warn">${!c.tank ? 'sem tanque' : 'sem curador'}</span>` : `<span>${n}/5</span>`;
      h += `<div class="rg"><div class="rg-h"><b>Grupo ${g + 1}</b>${st}</div>${part.map((p, k) => cellHTML(p, g * PARTY + k)).join('')}</div>`;
    }
    $('#rview').innerHTML = `<div class="rgrid" style="--gc:${Math.min(groups, 8)}">${h}</div>`;
  }
  const hint = $('#rhint');
  hint.classList.toggle('on', R.moving >= 0);
  hint.innerHTML = R.moving >= 0 ? `Escolha uma nova vaga para o jogador ${R.moving + 1}. <button type="button" id="mvCancel">Cancelar</button>` : '';

  const list = R.s.filter(Boolean), cnt = countRoles(list), rec = REC[R.size];
  $('#rRoles').innerHTML = RR.map((x, k) => `<span class="${list.length && cnt[x] < rec[k] ? 'low' : ''}">${ri(x)}${ROLE_RU[x]} <b>${cnt[x]}</b> / ${rec[k]}</span>`).join('');
  $('#rTip').textContent = R.size === 5 ? 'Uma masmorra precisa de um tanque, um curador e três de dano.' : `Regra geral para raide: tanques ${rec[0]}, curadores ${rec[1]}, o resto dano. O número exato depende dos chefes.`;
  const have = new Set(list.map(p => p.cls));
  $('#rBuffs').innerHTML = CLASSES.filter(c => BUFF[c.id]).map(c => `<li class="${have.has(c.id) ? '' : 'off'}" style="--cc:${CCOL[c.id]}"><span class="cdot"></span><span><b>${esc(c.n)}:</b> ${esc(BUFF[c.id])}</span></li>`).join('');
  const n = list.length;
  $('#rRaids').innerHTML = n ? RAIDS.map(([size, name]) => `<li class="${n >= size ? 'good' : ''}">${n >= size ? `Raide para ${size} (${name}): jogadores suficientes.` : `Raide para ${size} (${name}): faltam ${size - n}.`}</li>`).join('') : '<li>Ainda não há ninguém. Clique em “Meu personagem”, “Preencher vazios” ou num quadro livre.</li>';

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
    msg.innerHTML = 'Ainda não há personagem. <a href="../character/" id="rMake">Monte seu personagem</a>';
    $('#rMake').onclick = e => { if (window.GabellaHero) { e.preventDefault(); GabellaHero.open(); } };
    return;
  }
  const f = RC[h.race].f, role = RR.includes(h.role) ? h.role : roleOpts(CL[h.cls])[0];
  if (f !== R.f) {
    if (R.s.some(Boolean)) { msg.textContent = 'O seu personagem é da outra facção: troque a facção acima dos quadros.'; return; }
    R.f = f;
  }
  if (R.s.some(p => p && p.race === h.race && p.cls === h.cls && p.role === role && !p.name)) { msg.textContent = 'O seu personagem já está na composição.'; return; }
  let i = R.s.findIndex(p => !p); if (i < 0) i = 0;
  R.s[i] = { race: h.race, cls: h.cls, role, name: '' };
  msg.textContent = ''; R.moving = -1; renderRaid();
};
$('#rClear').onclick = () => { R.s = Array(R.size).fill(null); R.moving = -1; renderRaid(); };
$('#rCopyLink').onclick = () => copyTo(teamLink(), $('#rMsg'), 'Link copiado');
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
  $('#edT').textContent = `Jogador ${edI + 1}` + (R.size > 5 ? ` · Grupo ${Math.floor(edI / PARTY) + 1}` : '');
  $('#edRace').innerHTML = RACES.filter(r => r.f === R.f).map(r => `<option value="${r.id}"${r.id === p.race ? ' selected' : ''}>${esc(raceName(r))}${r.paid ? ' (paga)' : ''}</option>`).join('');
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
  else box.innerHTML = ['alliance', 'horde'].map(f => `<div class="rside ${f}"><h3>${FAC[f]}</h3>${RACES.filter(r => r.f === f).map(r => { const k = sel.indexOf(r.id); return `<button type="button" class="rp" data-id="${r.id}" aria-pressed="${k >= 0}">${esc(raceName(r))}${r.paid ? '<span class="tag paid">paga</span>' : ''}<span class="no">${k + 1}</span></button>`; }).join('')}</div>`).join('');
  $('#cNote').textContent = `Escolhido ${sel.length} de 3`;
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
const ul = (items, cls) => items.length ? `<ul${cls ? ` class="${cls}"` : ''}>${items.map(x => `<li>${x}</li>`).join('')}</ul>` : '<span class="none">Nenhum</span>';
const row = (lab, vals, extra) => `<div class="crow${extra ? ' ' + extra : ''}"><div class="lab${extra === 'tiprow' ? ' tl' : ''}">${lab}</div>${vals.map(v => `<div class="val">${v}</div>`).join('')}</div>`;
function renderCmp() {
  const out = [];
  if (C.mode === 'class') {
    const ids = C.cls;
    out.push(`<div class="crow chead"><div class="lab"></div>${ids.map(id => `<div class="val" style="--cc:${CCOL[id]}"><picture><source type="image/avif" srcset="${art(id, 'avif')}"><img src="${art(id)}" width="360" height="482" alt="" loading="lazy" decoding="async"></picture><b>${esc(CL[id].n)}</b><a href="${classUrl(id)}">Página da classe<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>`).join('')}</div>`);
    out.push(row('Funções', ids.map(id => CL[id].roles.map(r => `<span class="role">${ri(r)}${ROLE_RU[r]}</span>`).join(''))));
    out.push(row('Armadura', ids.map(id => racx(CX[id].armor))));
    out.push(row('Armas', ids.map(id => racx(CX[id].weapons))));
    out.push(row('Recurso', ids.map(id => esc(CX[id].resource))));
    out.push(row('Evolução', ids.map(id => esc(CX[id].lvl))));
    out.push(row('Especializações', ids.map(id => ul(CX[id].specs.map(s => `<b>${esc(s.n)}</b>${SPEC_SEP}<span class="sub">${esc(s.what)}</span>`)))));
    out.push(row('Bônus de raide', ids.map(id => BUFF[id] ? esc(BUFF[id]) : '<span class="none">Nenhum</span>')));
    out.push(row('Em grupo', ids.map(id => ul(CX[id].group.map(esc)))));
    out.push(row('Profissões', ids.map(id => ul(CPROF[id].map(p => `<b>${esc(p[0])}</b>${p[1] ? `<br><span class="sub">${esc(p[1])}</span>` : ''}`)) + `<a class="cgo" href="${HOME}guides/professions/#pairs=${id}">Objetos de acampamento e perícia<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a>`)));
    out.push(row('Pontos fortes', ids.map(id => ul(CX[id].pros.map(esc), 'plus'))));
    out.push(row('Pontos fracos', ids.map(id => ul(CX[id].cons.map(esc), 'minus'))));
    ['alliance', 'horde'].forEach(f => out.push(row(`Raças: ${FAC[f]}`, ids.map(id => { const rs = RACES.filter(r => r.f === f && r.can[id]); return rs.length ? rs.map(r => `<a href="${raceUrl(r.id)}">${esc(raceName(r))}</a>`).join(', ') : '<span class="none">Nenhum</span>'; }))));
  } else {
    const ids = C.race;
    out.push(`<div class="crow chead"><div class="lab"></div>${ids.map(id => { const r = RC[id]; return `<div class="val race ${r.f}"><span class="fx">${FAC[r.f]}${r.paid ? ' · paga' : ''}</span><b>${esc(raceName(r))}</b><a href="${raceUrl(id)}">Página da raça<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>`; }).join('')}</div>`);
    out.push(row('Classes', ids.map(id => ul(Object.keys(RC[id].can).map(c => `<span style="color:${CCOL[c]}">●</span> ${esc(CL[c].n)}${RC[id].can[c] === 'new' ? ' <span class="tag new">novo</span>' : ''}`)))));
    out.push(row('Habilidades ativas', ids.map(id => ul(RC[id].rac.filter(x => x[0] === 'a').map(x => `<b>${esc(x[1])}</b><br><span class="sub">${racx(x[2])}</span>`)))));
    out.push(row('Habilidades passivas', ids.map(id => ul(RC[id].rac.filter(x => x[0] === 'p').map(x => `<b>${esc(x[1])}</b><br><span class="sub">${racx(x[2])}</span>`)))));
    out.push(row('Dica', ids.map(id => esc(RC[id].tip)), 'tiprow'));
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
function facName(f) { return f === 'alliance' ? 'Aliança' : 'Horda'; }
function bi(ru) { return EN[ru] && EN[ru] !== ru ? `${esc(ru)} <span class="en">(${esc(EN[ru])})</span>` : esc(ru); }
function raceEn(r) { return r.en ? ` <span class="en">/ ${esc(r.en)}</span>` : ''; }
const tipBox = h => `<div class="tipbox"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg><p><span class="tl">Dica</span>${h}</p></div>`;
function face(id, cc, cls = '', title = '', f) { return `<span class="av ${cls}" style="--cc:${cc}"${title ? ` title="${esc(title)}"` : ''}><img src="${ROOT}assets/art/${porId(id, f)}-face.webp${PV}" width="160" height="160" alt="" loading="lazy" decoding="async"></span>`; }
function lvlMeter(c) {
  const p = c.lp || 0, w = Math.min(Math.abs(p) / 12 * 46, 46);
  const label = p < 0 ? `Mais rápido em ${-p}%` : p > 0 ? `Mais lento em ${p}%` : 'Ritmo médio';
  const bar = p ? `<i class="${p > 0 ? 'slow' : ''}" style="${p < 0 ? 'right' : 'left'}:50%;width:${w}%"></i>` : '';
  return `<span class="lvl"><span>${label}</span><span class="bar" role="img" aria-label="${label}">${bar}</span><span class="scale" aria-hidden="true"><span>mais rápido</span><span>mais lento</span></span></span>`;
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
  let h = '<thead><tr><th scope="col">Raça</th>';
  CLASSES.forEach(c => { h += `<th scope="col" class="${roleMatch(c, state.r) ? '' : 'dim'}${c.id === state.cls ? ' selc' : ''}">${face(c.id, CCOL[c.id])}${esc(c.n)}</th>`; });
  h += '</tr></thead><tbody>';
  ['alliance', 'horde'].forEach(f => {
    const rows = RACES.filter(r => r.f === f && raceVisible(r));
    if (!rows.length) return;
    h += `<tr class="fh ${f}"><th colspan="${CLASSES.length + 1}" scope="rowgroup"><span class="f ${f}"></span>${facName(f)}</th></tr>`;
    rows.forEach(r => {
      h += `<tr class="${r.id === state.race ? 'rowsel' : ''}"><th scope="row"><span class="rn">${face(RSLUG[r.id], `var(--${r.f})`)}${esc(r.n)}${r.paid ? '<span class="paid">paga</span>' : ''}</span></th>`;
      CLASSES.forEach(c => {
        const v = r.can[c.id];
        const dim = roleMatch(c, state.r) ? '' : ' dim';
        if (!v) { h += `<td><span class="cell no${dim}" role="img" aria-label="${esc(r.n)} ${esc(c.n)}: não permitido"></span></td>`; return; }
        const sel = (r.id === state.race && c.id === state.cls) ? ' sel' : '';
        const label = `${r.n} ${c.n}${v === 'new' ? ', nova combinação' : ''}`;
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
  const rac = r.rac.map(x => `<div class="card ab"><span class="abt${x[0] === 'a' ? '' : ' p'}">${x[0] === 'a' ? 'Ativa' : 'Passiva'}</span><b>${bi(x[1])}</b><span>${racx(x[2])}</span></div>`).join('');
  const text = `${r.name || r.n} ${c.n} (${facName(r.f)})${r.paid ? ', requer o pacote Skyborne' : ''}`;
  $('#detail').innerHTML = `
    <div class="d-head">
      <div class="d-art" aria-hidden="true"><picture><source type="image/avif" srcset="${ROOT}assets/art/${RSLUG[r.id]}-600.avif${PV}"><img src="${ROOT}assets/art/${RSLUG[r.id]}-600.webp${PV}" width="600" height="804" alt="" loading="lazy" decoding="async"></picture></div>
      <div class="d-avs">${face(RSLUG[r.id], `var(--${r.f})`)}</div>
      <div class="d-title"><h3>${esc(r.n)}${raceEn(r)} · ${esc(c.n)}</h3>
        <div class="chips"><span class="tag ${r.f}">${facName(r.f)}</span>${isNew ? '<span class="tag new">Nova combinação</span>' : ''}${r.paid ? '<span class="tag paid">Raça paga</span>' : ''}${roleChips(c)}</div></div>
    </div>
    <div class="d-body">
      <div class="d-cols">
        <div><h4>Especializações</h4><div class="cards">${specs}</div></div>
        <div><h4>Habilidades raciais</h4><div class="cards two">${rac}</div></div>
      </div>
      <div class="facts3">
        <div class="fact"><h4>Evolução</h4>${lvlMeter(c)}</div>
        <div class="fact"><h4>Em raides</h4><span>${esc(c.raid)}.</span></div>
        <div class="fact"><h4>Novidades</h4><span>${esc(c.forever)}</span></div>
      </div>
      ${tipBox(esc(r.tip))}
      ${pickLinks(r, c)}
      <div class="copyrow">
        <input id="pickText" readonly value="${esc(text)}" aria-label="Minha escolha">
        <button class="btn" id="copyBtn"><svg class="ico" aria-hidden="true"><use href="#i-copy"/></svg>Copiar minha escolha</button>
        <button class="btn ghost" id="shareBtn">Compartilhar</button>
        <span class="small" id="copyMsg" role="status"></span>
      </div>
    </div>`;
  $('#copyBtn').onclick = () => copyTo($('#pickText').value, $('#copyMsg'), 'Copiado');
  $('#shareBtn').onclick = () => shareBuild(r.id, c.id, state.spec, text);
}
/* Share: the link of the card page b/<race>-<class>-<spec>/ (its preview is the card with the name); on a phone the share sheet, else the clipboard */
function shareBuild(race, cls, spec, text) {
  const url = new URL(`${HOME}b/${BSLUG[race] || race}-${cls}-${spec}/`, location.href).href, msg = $('#copyMsg');
  if (navigator.share && matchMedia('(pointer: coarse)').matches) navigator.share({ title: text, url }).catch(e => { if (e && e.name !== 'AbortError') copyTo(url, msg, 'Link copiado'); });
  else copyTo(url, msg, 'Link copiado');
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
  cas: ['Europa', 'Cáucaso e Ásia Central não têm região própria; a mais próxima é a Europa.'],
  mea: ['Europa', 'Oriente Médio e África não têm região própria; a mais próxima é a Europa.'],
  na: ['Américas e Oceania', ''],
  la: ['Américas e Oceania', 'A América Latina joga na região das Américas.'],
  oce: ['Américas e Oceania', 'A Blizzard junta a Oceania às Américas em uma região. A Blizzard não disse se há servidores na própria Oceania.'],
  kr: ['Coreia', ''],
  tw: ['Taiwan', ''],
  asia: ['', 'Não há região própria. As mais próximas no mapa são Taiwan e Coreia. Escolha a que tiver menor latência World.'],
};
function renderPing() {
  const v = $('#pgW').value, r = PG[v];
  try { if (v) localStorage.setItem('gabella-ping', v); } catch (e) {}
  if (!r) { $('#pgOut').innerHTML = ''; return; }
  $('#pgOut').innerHTML = (r[0] ? `<p class="preg">Sua região: ${esc(r[0])}</p>` : '') + '<ul class="verdict">'
    + (r[1] ? `<li>${esc(r[1])}</li>` : '')
    + '<li>Não há reinos: você escolhe região e regras, não um servidor. A região é escolhida no Battle.net antes de iniciar o jogo.</li>'
    + '<li>Cada região tem seus próprios personagens e nomes. Só dá para jogar junto dentro de uma região.</li>'
    + '<li>A Blizzard não disse onde ficam os servidores das regiões.</li></ul>';
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
