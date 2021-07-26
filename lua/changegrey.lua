rep = { 0, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 13, 14, 15,
        16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 29, 30, 31,
        32, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 45, 46, 47,
        48, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 62, 63 }

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

function memory.writebyteppu(a,v)
    memory.writebyte(0x2001,0x00) -- Turn off rendering
    memory.readbyte(0x2002) -- PPUSTATUS (reset address latch)
    memory.writebyte(0x2006,math.floor(a/0x100)) -- PPUADDR high byte
    memory.writebyte(0x2006,a % 0x100) -- PPUADDR low byte
    memory.writebyte(0x2007,v) -- PPUDATA
    memory.writebyte(0x2001,0x1e) -- Turn on rendering
end

memory.register(0x2007, function()
  for i = 0x3f00, 0x3f1f do
    byte = memory.readbyteppu(i)
    print(byte)
    -- memory.writebyteppu(i, rep[byte])
  end
end)


























