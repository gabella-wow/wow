-- Сохраняет деревья талантов своего класса через игровое API аддонов (GetTalentInfo / GetTalentPrereqs).
-- Нужен один персонаж каждого класса (уровень 1 хватает): зайти, набрать /gtd, выйти из игры; ещё раз с английским
-- текстом клиента (имена для en/uk/pl) —
-- данные лягут в WTF/Account/<аккаунт>/SavedVariables/GabellaTalents.lua.
GabellaTalentsDB = GabellaTalentsDB or {}

local tip = CreateFrame("GameTooltip", "GabellaTalentsTip", nil, "GameTooltipTemplate")
tip:SetOwner(WorldFrame, "ANCHOR_NONE")

local function tipLines()
  local out = {}
  for i = 1, tip:NumLines() do
    local l = _G["GabellaTalentsTipTextLeft" .. i]
    local t = l and l:GetText()
    if t and t ~= "" then out[#out + 1] = t end
  end
  return out
end

local spellName = (C_Spell and C_Spell.GetSpellName) or function(id) return (GetSpellInfo(id)) end
local spellIcon = (C_Spell and C_Spell.GetSpellTexture) or GetSpellTexture

local function byOrder(a, b) return (a.orderIndex or 0) < (b.orderIndex or 0) end

-- WoW Forever: the vanilla trees live in the trait system (one class tree, one trait group a vanilla tree).
-- Saved raw: node positions (posX/posY), ranks and edges; tools/talent_import.py turns positions into rows and columns.
local function dumpTraits(d)
  local configID = C_ClassTalents.GetActiveConfigID()
  local config = configID and C_Traits.GetConfigInfo(configID)
  local treeID = config and config.treeIDs and config.treeIDs[1]
  if not treeID then error("no talent config for this character yet (log in with a character that has a class tree)") end
  d.api, d.treeID = "traits", treeID
  local groups = C_Traits.GetGroupDisplayInfoByTreeID(treeID) or {}
  table.sort(groups, byOrder)
  local byGroup = {}
  for i, g in ipairs(groups) do
    d.trees[i] = { info = { g.displayName, nil, nil, nil, nil, g.groupID }, groupID = g.groupID, name = g.displayName, talents = {} }
    byGroup[g.groupID] = d.trees[i]
  end
  for _, nodeID in ipairs(C_Traits.GetTreeNodes(treeID) or {}) do
    local info = C_Traits.GetNodeInfo(configID, nodeID)
    if info and info.isVisible and info.entryIDs and info.entryIDs[1] then
      local t
      for _, gid in ipairs(info.groupIDs or {}) do t = t or byGroup[gid] end
      if t then
        local entry = C_Traits.GetEntryInfo(configID, info.entryIDs[1])
        local def = entry and entry.definitionID and C_Traits.GetDefinitionInfo(entry.definitionID)
        local sid = def and def.spellID
        local icon = def and def.overrideIcon
        if (not icon or icon == 0) and sid and spellIcon then icon = spellIcon(sid) end
        local edges = {}
        for _, e in ipairs(info.visibleEdges or {}) do edges[#edges + 1] = e.targetNode end
        local lines = {}
        if sid and tip.SetSpellByID then
          tip:ClearLines()
          if pcall(tip.SetSpellByID, tip, sid) then lines = tipLines() end
        end
        local getDesc = (C_Spell and C_Spell.GetSpellDescription) or GetSpellDescription
        local desc = sid and getDesc and getDesc(sid)
        if desc and desc ~= "" then lines[#lines + 1] = desc end   -- the tooltip of a talent not loaded yet has no text
        t.talents[#t.talents + 1] = { name = sid and spellName(sid), icon = icon, maxRank = info.maxRanks, talentID = nodeID,
                                      spellId = sid, posX = info.posX, posY = info.posY, edges = edges, tip = lines }
      end
    end
  end
  return #d.trees
end

local function dump()
  local _, class = UnitClass("player")
  local d = { class = class, locale = GetLocale(), build = select(1, GetBuildInfo()) .. "." .. select(2, GetBuildInfo()),
              interface = select(4, GetBuildInfo()), trees = {} }
  if not GetNumTalentTabs then
    if not (C_ClassTalents and C_Traits) then error("no talent API in this client (GetNumTalentTabs, C_Traits)") end
    local n = dumpTraits(d)
    GabellaTalentsDB[class] = GabellaTalentsDB[class] or {}
    GabellaTalentsDB[class][d.locale] = d
    local k = 0
    for _, t in ipairs(d.trees) do k = k + #t.talents end
    print("|cffc9a54aGabella|r: " .. class .. " (" .. d.locale .. ") saved (" .. n .. " trees, " .. k .. " talents). Log out to write the file.")
    return
  end
  for tab = 1, GetNumTalentTabs() do
    local a, b, c, e, f, g = GetTalentTabInfo(tab)
    local tree = { info = { a, b, c, e, f, g }, talents = {} }
    for i = 1, GetNumTalents(tab) do
      local r = { GetTalentInfo(tab, i) }
      local pt, pc
      if GetTalentPrereqs then pt, pc = GetTalentPrereqs(tab, i) end
      tip:ClearLines()
      local spellId
      if tip.SetTalent then                                    -- no tooltip API in this client: names and ranks still saved
        pcall(tip.SetTalent, tip, tab, i)
        if tip.GetSpell then
          local ok, _, sid = pcall(tip.GetSpell, tip)
          if ok then spellId = sid end
        end
      end
      tree.talents[i] = { name = r[1], icon = r[2], row = r[3], col = r[4], maxRank = r[6],
                          talentID = r[11], spellId = spellId, req = pt and { pt, pc } or nil, tip = tipLines() }
    end
    d.trees[tab] = tree
  end
  GabellaTalentsDB[class] = GabellaTalentsDB[class] or {}
  GabellaTalentsDB[class][d.locale] = d
  print("|cffc9a54aGabella|r: " .. class .. " (" .. d.locale .. ") saved (" .. GetNumTalentTabs() .. " trees). Log out to write the file.")
end

SLASH_GABELLATALENTS1 = "/gtd"
SlashCmdList.GABELLATALENTS = function()
  local ok, err = pcall(dump)
  if not ok then print("|cffc9a54aGabella|r: talents error: " .. tostring(err)) end
end
