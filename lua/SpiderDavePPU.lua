-- fceux has fewer built-in routines for the PPU memory (wrt CPU memory).
-- here are some routines by SpiderDave and warmCabin
-- https://stackoverflow.com/questions/41954718/how-to-get-ppu-memory-from-fceux-in-lua
-- note: fceux 2.3.0 has more functionality than fceux 2.2.x.

-- -- For Rockman 2. Directly after all graphics update routines finish.
-- memory.registerexec(0xD031, function()
--     local paletteBase = 0x3F00
--     -- Make all BG colors pink
--     for i = 0x00, 0x0F do
--         memory.writebyteppu(paletteBase + i, 0x35)
--     end
-- end)


function memory.readbyteppu(a)
    memory.writebyte(0x2001,0x00) -- Turn off rendering
    memory.readbyte(0x2002) -- PPUSTATUS (reset address latch)
    memory.writebyte(0x2006,math.floor(a/0x100)) -- PPUADDR high byte
    memory.writebyte(0x2006,a % 0x100) -- PPUADDR low byte
    if a < 0x3f00 then
        dummy=memory.readbyte(0x2007) -- PPUDATA (discard contents of internal buffer if not reading palette area)
    end
    ret=memory.readbyte(0x2007) -- PPUDATA
    memory.writebyte(0x2001,0x1e) -- Turn on rendering
    return ret
end

function memory.readbytesppu(a,l)
    memory.writebyte(0x2001,0x00) -- Turn off rendering
    local ret
    local i
    ret=""
    for i=0,l-1 do
        memory.readbyte(0x2002) -- PPUSTATUS (reset address latch)
        memory.writebyte(0x2006,math.floor((a+i)/0x100)) -- PPUADDR high byte
        memory.writebyte(0x2006,(a+i) % 0x100) -- PPUADDR low byte
        if (a+i) < 0x3f00 then
            dummy=memory.readbyte(0x2007) -- PPUDATA (discard contents of internal buffer if not reading palette area)
        end
        ret=ret..string.char(memory.readbyte(0x2007)) -- PPUDATA
    end
    memory.writebyte(0x2001,0x1e) -- Turn on rendering
    return ret
end


function memory.writebyteppu(a,v)
    memory.writebyte(0x2001,0x00) -- Turn off rendering
    memory.readbyte(0x2002) -- PPUSTATUS (reset address latch)
    memory.writebyte(0x2006,math.floor(a/0x100)) -- PPUADDR high byte
    memory.writebyte(0x2006,a % 0x100) -- PPUADDR low byte
    memory.writebyte(0x2007,v) -- PPUDATA
    memory.writebyte(0x2001,0x1e) -- Turn on rendering
end

function memory.writebytesppu(a,str)
    memory.writebyte(0x2001,0x00) -- Turn off rendering

    local i
    for i = 0, #str-1 do
        memory.readbyte(0x2002) -- PPUSTATUS (reset address latch)
        memory.writebyte(0x2006,math.floor((a+i)/0x100)) -- PPUADDR high byte
        memory.writebyte(0x2006,(a+i) % 0x100) -- PPUADDR low byte
        memory.writebyte(0x2007,string.byte(str,i+1)) -- PPUDATA
    end

    memory.writebyte(0x2001,0x1e) -- Turn on rendering
end