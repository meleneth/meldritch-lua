local capabilities = {
  ["graph.core"]="1.0.0", ["instrument.core"]="1.0.0",
  ["audio.modules"]="1.0.0", ["midi.routing"]="1.0.0",
  ["sequencer.core"]="1.0.0", ["sequencer.persistence.v2"]="1.0.0",
  ["events.subscription"]="1.0.0", ["samples.bank"]="1.0.0",
  ["vst3.host"]="1.0.0", ["web.performance"]="1.0.0",
  ["ui.control-surfaces"]="1.0.0", ["hardware.apc"]="1.0.0",
  ["hardware.stream-deck"]="1.0.0",
}

local function install()
  local host = {}
  function host.host_api_version() return "1.0.0" end
  function host.host_capabilities()
    local result = {}
    for id, version in pairs(capabilities) do
      result[#result + 1] = {id=id, version=version}
    end
    table.sort(result, function(left, right) return left.id < right.id end)
    return result
  end
  _G.meldritch = host
  return host
end

return {install=install, capabilities=capabilities}
