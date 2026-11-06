-- Saves items from the client (addon API: GetItemInfoInstant, GetItemInfo, GetItemStats, the item tooltip):
-- equipment (weapons, armor), consumables (potions, elixirs, flasks, food, drink, bandages, poisons), reagents and trade goods,
-- and where items come from while you play: dungeon boss loot, quest rewards, recipes of an open profession window.
-- /ggd all             scan + the talents of this character (GabellaTalents, /gtd) in one go
-- /ggd scan            scans item ids 1-30000 and 200000-300000 (3-5 minutes; stay in a city, nothing is sent anywhere);
--                      a stopped scan (reload, disconnect) goes on from where it was; /ggd scan new starts again
-- /ggd scan A B        scans ids A-B
-- /ggd max N           keeps items up to required level N (default 60)
-- /ggd status          what is saved and how far the scan is
-- Log out to write WTF/Account/<account>/SavedVariables/GabellaGear.lua -> python tools/gear_import.py --addon <file>
GabellaGearDB = GabellaGearDB or {}

local VERSION = 2
local STEP, TICK, REQ_TICK, SAVE_TICK, NOTE = 400, 0.1, 25, 150, 10000 -- ids, seconds, server requests, saves a tick; ids a message
local KEEP = { [0] = true, [2] = true, [4] = true, [5] = true, [7] = true } -- consumable, weapon, armor, reagent, trade goods
local EQUIP = { [2] = true, [4] = true }
local SKIP = { INVTYPE_BODY = true, INVTYPE_TABARD = true, INVTYPE_BAG = true, INVTYPE_AMMO = true, INVTYPE_QUIVER = true,
               INVTYPE_NON_EQUIP_IGNORE = true }
local DEFAULT_RANGES = { { 1, 30000 }, { 200000, 300000 } }
local P = "|cffc9a54aGabella|r: "

local tip = CreateFrame("GameTooltip", "GabellaGearTip", nil, "GameTooltipTemplate")
tip:SetOwner(WorldFrame, "ANCHOR_NONE")
-- The Forever client (1.60.x) has no global GetItemInfoInstant: every API call goes through a fallback.
local GII = GetItemInfoInstant or (C_Item and C_Item.GetItemInfoInstant)
local getInfo = GetItemInfo or (C_Item and C_Item.GetItemInfo)
local getStats = GetItemStats or (C_Item and C_Item.GetItemStats)
-- asking the server: the request API, or else GetItemInfo itself (it asks the server for an item the client does not have)
local request = (C_Item and C_Item.RequestLoadItemDataByID) or function(id) getInfo(id) end

local function newTicker(sec, fn)
  if C_Timer and C_Timer.NewTicker then return C_Timer.NewTicker(sec, fn) end
  local fr, acc = CreateFrame("Frame"), 0
  fr:SetScript("OnUpdate", function(_, e) acc = acc + e; if acc >= sec then acc = 0; fn() end end)
  return { Cancel = function() fr:SetScript("OnUpdate", nil) end }
end

-- what kind an id is: known (the client has it), class, equip slot. Without GetItemInfoInstant only cached items are known.
local function kind(id)
  if GII then
    local _, _, _, equip, _, cls = GII(id)
    return true, cls, equip
  end
  local name, _, _, _, _, _, _, _, equip, _, _, cls = getInfo(id)
  if name then return true, cls, equip end
  return false
end

local function db()
  GabellaGearDB.items = GabellaGearDB.items or {}
  GabellaGearDB.src = GabellaGearDB.src or {}
  GabellaGearDB.maxreq = GabellaGearDB.maxreq or 60
  GabellaGearDB.version = VERSION
  local v, b = GetBuildInfo()
  GabellaGearDB.build = tostring(v) .. "." .. tostring(b)
  return GabellaGearDB
end

local function tipLines(link)
  tip:ClearLines()
  tip:SetHyperlink(link)
  local out = {}
  for i = 1, tip:NumLines() do
    local l = _G["GabellaGearTipTextLeft" .. i]
    local t = l and l:GetText()
    if t and t ~= "" then out[#out + 1] = t end
  end
  return out
end

-- the kinds we keep, from what the client knows without asking the server
local function wanted(cls, equip)
  if not cls or not KEEP[cls] then return false end
  if EQUIP[cls] then return equip ~= nil and equip ~= "" and not SKIP[equip] end
  return true
end

local function save0(id)
  local name, link, q, ilvl, req, _, _, _, equip, icon, _, cls, sub = getInfo(id)
  if not name or not link then return false end
  local d = db()
  if not wanted(cls, equip) or (req or 0) > d.maxreq or (q or 0) < 1 then return false end
  local loc = GetLocale()
  local it = d.items[id] or {}
  it.name = it.name or {}
  it.tip = it.tip or {}
  it.name[loc] = name
  it.slot = (equip and equip ~= "") and equip or nil
  it.ilvl, it.req, it.q, it.icon = ilvl, req, q, icon
  it.cls, it.sub, it.iclass, it.isub = cls, sub, cls, sub          -- cls/sub: the v1 names, kept for old readers
  local st = getStats and getStats(link)
  it.stats = (st and next(st)) and st or nil
  it.tip[loc] = tipLines(link)
  d.items[id] = it
  return true
end

local function save(id)
  local ok, r = pcall(save0, id)
  return ok and r
end

local function itemId(link)
  return link and tonumber(link:match("item:(%d+)"))
end

local function addSrc(id, key, rec)
  if not id then return end
  local d = db()
  d.src[id] = d.src[id] or {}
  local loc, old = GetLocale(), d.src[id][key]
  if old then
    for _, f in ipairs({ "name", "zone" }) do
      if rec[f] then old[f] = old[f] or {}; old[f][loc] = rec[f][loc] end
    end
  else
    d.src[id][key] = rec
  end
  if not save(id) then request(id) end
end

-- the scan: every id of the ranges, STEP a tick; ids the client has to load are asked from the server (REQ_TICK a tick at most)
-- and saved by GET_ITEM_INFO_RECEIVED; ids still missing at the end are asked once more.
-- The state lives in GabellaGearDB.scan, so a reload or a new login goes on from there.
local ticker, found, waiting, seen, retry, idle = nil, 0, {}, 0, false, 0
local GRACE = 30                                              -- ticks to wait for the last answers (3 s)

local function total(ranges)
  local n = 0
  for _, r in ipairs(ranges) do n = n + (r[2] - r[1] + 1) end
  return n
end

local function finish()
  if ticker then ticker:Cancel(); ticker = nil end
  local s = db().scan
  if s then s.done = true end
  local n = 0
  for _ in pairs(db().items) do n = n + 1 end
  print(P .. "scan done, " .. found .. " new now, " .. n .. " saved in all. Log out to write the file.")
end

local function step0()
  local s = db().scan
  if not s or s.done then return finish() end
  local asked, saved = 0, 0
  for _ = 1, STEP do
    local r = s.ranges[s.r]
    if not r then
      idle = idle + 1
      if idle < GRACE then return end                            -- the answers to the last requests are still coming
      idle = 0
      if retry then return finish() end
      retry = true                                               -- second pass: what the server has not answered yet
      local again = {}
      for id in pairs(waiting) do if not db().items[id] then again[#again + 1] = id end end
      table.sort(again)
      waiting = {}
      if #again == 0 then return finish() end
      print(P .. "asking again for " .. #again .. " items...")
      s.ranges, s.r, s.n = {}, 1, 0
      for i, id in ipairs(again) do s.ranges[i] = { id, id } end
      return
    end
    local id = r[1] + s.n
    if id > r[2] then
      s.r, s.n = s.r + 1, 0
    else
      s.n = s.n + 1
      seen = seen + 1
      local known, cls, equip = kind(id)
      if not known or wanted(cls, equip) then
        if known and save(id) then found = found + 1; saved = saved + 1
        else                                                     -- not loaded yet: ask, GET_ITEM_INFO_RECEIVED saves it
          waiting[id] = true
          request(id)
          asked = asked + 1
        end
      end
      if seen % NOTE == 0 and not retry then
        print(P .. seen .. " / " .. s.all .. " ids, " .. found .. " items...")
      end
      if asked >= REQ_TICK or saved >= SAVE_TICK then return end -- do not flood the server, keep the frame rate
    end
  end
end

local function step()
  local ok, err = pcall(step0)
  if not ok then print(P .. "error, the scan goes on: " .. tostring(err)) end
end

local function start(ranges, fresh)
  local d = db()
  local s = d.scan
  if fresh or not s or s.done or s.locale ~= GetLocale() then
    s = { ranges = ranges, r = 1, n = 0, all = total(ranges), locale = GetLocale() }
    d.scan = s
    seen, found = 0, 0
    print(P .. "scanning items (" .. GetLocale() .. ", up to level " .. d.maxreq .. ")...")
  else
    seen = 0
    for i = 1, s.r - 1 do seen = seen + (s.ranges[i][2] - s.ranges[i][1] + 1) end
    seen = seen + s.n
    print(P .. "going on from " .. seen .. " / " .. s.all .. " ids (/ggd scan new starts again)...")
  end
  waiting, retry, idle = {}, false, 0
  if not ticker then ticker = newTicker(TICK, step) end
  if not GII then print(P .. "no GetItemInfoInstant in this client: every id is asked from the server (~10 minutes).") end
end

local function status()
  local d = db()
  local n, by, s = 0, {}, 0
  for _, it in pairs(d.items) do
    n = n + 1
    local c = it.iclass or it.cls or -1
    by[c] = (by[c] or 0) + 1
  end
  for _ in pairs(d.src) do s = s + 1 end
  print(P .. n .. " items (weapons " .. (by[2] or 0) .. ", armor " .. (by[4] or 0) .. ", consumables " .. (by[0] or 0) ..
        ", reagents " .. (by[5] or 0) .. ", trade goods " .. (by[7] or 0) .. "), " .. s .. " with a source, up to level " .. d.maxreq .. ".")
  local sc = d.scan
  if sc then
    local done = 0
    for i = 1, (sc.r or 1) - 1 do if sc.ranges[i] then done = done + (sc.ranges[i][2] - sc.ranges[i][1] + 1) end end
    print(P .. "scan " .. (sc.locale or "?") .. ": " .. (sc.done and "done" or ((ticker and "running, " or "stopped, ") ..
          (done + (sc.n or 0)) .. " / " .. (sc.all or 0) .. " ids")) .. ".")
  else
    print(P .. "no scan yet. /ggd all")
  end
end

local f = CreateFrame("Frame")
f:RegisterEvent("GET_ITEM_INFO_RECEIVED")
f:RegisterEvent("LOOT_READY")
f:RegisterEvent("QUEST_DETAIL")
f:RegisterEvent("QUEST_COMPLETE")
f:RegisterEvent("TRADE_SKILL_SHOW")
f:SetScript("OnEvent", function(_, ev, a1, a2)
  local ok, err = pcall(function()
    local loc = GetLocale()
    if ev == "GET_ITEM_INFO_RECEIVED" then
      if a1 and waiting[a1] then
        if a2 then                                                 -- answered: saved or not wanted (grey, too high), not asked again
          waiting[a1] = nil
          if save(a1) then found = found + 1 end
        end
      elseif a1 and a2 then
        save(a1)
      end
    elseif ev == "LOOT_READY" then                                 -- a dungeon boss: the corpse you loot is your target
      local zone, kind = GetInstanceInfo()
      if kind ~= "party" then return end
      local guid = UnitGUID("target")
      if not guid or not UnitIsDead("target") then return end
      local npc = select(6, strsplit("-", guid))
      for s = 1, GetNumLootItems() do
        addSrc(itemId(GetLootSlotLink(s)), "drop:" .. tostring(npc),
               { kind = "drop", npc = tonumber(npc), name = { [loc] = UnitName("target") }, zone = { [loc] = zone } })
      end
    elseif ev == "QUEST_DETAIL" or ev == "QUEST_COMPLETE" then     -- the rewards of the quest window, with your faction
      local qid, title = GetQuestID and GetQuestID() or 0, GetTitleText()
      local rec = function() return { kind = "quest", quest = qid, name = { [loc] = title }, faction = (UnitFactionGroup("player")) } end
      for i = 1, GetNumQuestChoices() do addSrc(itemId(GetQuestItemLink("choice", i)), "quest:" .. qid, rec()) end
      for i = 1, GetNumQuestRewards() do addSrc(itemId(GetQuestItemLink("reward", i)), "quest:" .. qid, rec()) end
    elseif ev == "TRADE_SKILL_SHOW" then                           -- what the open profession window makes
      local prof = GetTradeSkillLine()
      for i = 1, GetNumTradeSkills() do
        local _, kind = GetTradeSkillInfo(i)
        if kind ~= "header" then
          addSrc(itemId(GetTradeSkillItemLink(i)), "craft:" .. tostring(prof), { kind = "craft", name = { [loc] = prof } })
        end
      end
    end
  end)
  if not ok then print(P .. "error in " .. tostring(ev) .. ": " .. tostring(err)) end
end)

SLASH_GABELLAGEAR1 = "/ggd"
SlashCmdList.GABELLAGEAR = function(msg)
  msg = strtrim((msg or ""):lower())
  local cmd, rest = msg:match("^(%S*)%s*(.-)$")
  if cmd == "all" then
    start(DEFAULT_RANGES, rest == "new")
    if SlashCmdList.GABELLATALENTS then
      local ok, err = pcall(SlashCmdList.GABELLATALENTS, "")
      if not ok then print(P .. "talents failed: " .. tostring(err)) end
    else
      print(P .. "GabellaTalents is not loaded: turn it on in the AddOns list for the talents (/gtd).")
    end
  elseif cmd == "scan" then
    local a, b = rest:match("^(%d+)%s+(%d+)")
    if a then start({ { tonumber(a), tonumber(b) } }, true)
    else start(DEFAULT_RANGES, rest == "new") end
  elseif cmd == "max" then
    local n = tonumber(rest)
    if n and n >= 1 then db().maxreq = math.floor(n) end
    print(P .. "items up to required level " .. db().maxreq .. ".")
  elseif cmd == "stop" then
    if ticker then ticker:Cancel(); ticker = nil end
    print(P .. "scan stopped; /ggd scan goes on.")
  else
    status()
    print(P .. "/ggd all | scan [new] | scan A B | max N | status | stop")
  end
end
