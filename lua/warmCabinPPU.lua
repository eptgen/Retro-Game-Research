-- For Rockman 2. Directly after all graphics update routines finish.

memory.registerexec(0xD031, function()
    local paletteBase = 0x3F00
    -- Make all BG colors pink
    for i = 0x00, 0x0F do
        memory.writebyteppu(paletteBase + i, 0x35)
    end
end)
