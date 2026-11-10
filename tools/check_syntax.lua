for _, path in ipairs(arg) do
  local chunk, error_message = loadfile(path)
  if not chunk then
    io.stderr:write(path .. ": " .. error_message .. "\n")
    os.exit(1)
  end
end
