local arp = assert(loadfile("libraries/arp.lua"))()
local engine = arp.new {mode="up", octaves=2, clock_division=2, gate=.5}
local events = engine:events(8, {60, 64})
assert(#events == 4)
assert(events[1].step == 1 and events[1].note == 60)
assert(events[2].step == 3 and events[2].note == 64)
assert(events[3].step == 5 and events[3].note == 72)
assert(events[4].step == 7 and events[4].note == 76)
engine:restart()
local again = engine:events(8, {60, 64})
for index, event in ipairs(events) do
  assert(event.step == again[index].step and event.note == again[index].note)
end
