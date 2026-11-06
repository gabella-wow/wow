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

local function dump()
  local _, class = UnitClass("player")
  local d = { class = class, locale = GetLocale(), build = select(1, GetBuildInfo()) .. "." .. select(2, GetBuildInfo()),
              interface = select(4, GetBuildInfo()), trees = {} }
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
