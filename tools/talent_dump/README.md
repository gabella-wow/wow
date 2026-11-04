# Деревья талантов из клиента Forever

Законный способ получить ряды, колонки, стрелки и значки: игровое API аддонов (то, чем пользуются все аддоны).

1. Скопировать папку `GabellaTalents` в `C:\Program Files (x86)\World of Warcraft\_forever_\Interface\AddOns\`.
2. В списке аддонов включить «Загружать устаревшие» (номер интерфейса Forever заранее неизвестен).
3. Каждым из 9 классов (друид, охотник, маг, паладин, жрец, разбойник, шаман, чернокнижник, воин; уровень 1 хватает): зайти в мир, набрать `/gtd` (или `/ggd all` вместе с GabellaGear), выйти. Один раз на ruRU, ещё раз с английским текстом клиента (Battle.net → настройки игры → язык текста English): имена для en/uk/pl.
4. Файл `_forever_\WTF\Account\<аккаунт>\SavedVariables\GabellaTalents.lua` — отдать в `python tools/talent_import.py <файл>` → `content/talents/<класс>.json`, затем `python tools/talent_icons.py` (иконки).

Значок: `GetTalentInfo` второе значение (file id), аддон пишет его в `icon` каждого таланта; `talent_import.py` кладёт его в `file`, `talent_icons.py` берёт картинку с render.worldofwarcraft.com по этому id. Ключ API для этого не нужен.

## Пробел сейчас: 95 из 464 талантов без значка (04.11)

Новые таланты Forever, которых нет ни в раскладке, ни в Game Data API. Закрываются только дампом своего класса:

- **druid** (9): balance: Genesis, Nature’s Majesty; feral: Shifting Power, Primal Bite, Improved Shifting Power, Natural Instinct, Natural Reaction; restoration: Gift of the Earthmother, Living Spirit
- **hunter** (16): beast-mastery: Deadly Aspects, Focused Fire, Summon Hawk; marksmanship: Lethal Attacks, Improved Stings, Rapid Killing, Lone Wolf, Rapid Recuperation, Sniper Shot; survival: Improved Tracking, Predator’s Edge, Resourcefulness, Expose Prey, Survivalist’s Discipline, Strider Kick, Lacerating Strikes
- **mage** (6): arcane: Improved Channeling, Missile Barrage, Arcane Geometry, Arcane Shielding, Arcane Wrath; fire: Heating Up
- **paladin** (15): holy: Voice of Truth, Reverence, Purifying Power, Divine Precision, Light’s Vigil; protection: Improved Seal of Fury, Swift Judgement, Templar’s Bulwark, Iron Creed; retribution: Holy Conduit, Sanctified Judgement, Sacred Arbiter, Champion of the Light, Instrument of Law, Twist of Light
- **priest** (12): discipline: Power in Light, Holy Precision, Soul Warding, Penance, Renewed Hope; holy: Twilight Focus, Binding Heal, Litany of Light; shadow: Improved Mind Flay, Dark Inspiration, Devouring Contagion, Early Demise
- **rogue** (7): assassination: Venom; combat: Puncturing Wounds, Flawless Execution, Hack and Slash; subtlety: Dirty Tricks, Quietus, Cutthroat
- **shaman** (8): elemental: Elemental Alacrity, Trial by Fire, Earthbound; enhancement: Mental Dexterity, Improved Stormstrike, Rage of the Farseer; restoration: Mindfulness, Natural Grace
- **warlock** (13): affliction: Soul Harvest, Improved Drains, Pandemic, Wrack; demonology: Demonic Aegis, Demonic Energies, Decimation, Demonic Brand, Demonic Pact; destruction: Molten Skin, Agonizing Flames, Bane of Havoc, Shadow and Flame
- **warrior** (9): arms: Spearing Strike, Bloodthrill, Weaponmaster; fury: Lingering Rage, Furious Precision, Raging Blows, Gore Drinker; protection: Master of Defense, Bastion

Проверка после импорта: `python tools/x2_verify.py --talents <файл>` (пункт «95 icons»: 0 без значка).
