function memChange(address, value)

    gui.text(0,10,"memory changed");
    gui.text(100,10,address);
    gui.text(200,10,value);

    -- memory.read

end

memory.registerwrite(0x0000, 4, memChange);

while (true) do

       -- gui.text(50,50,"Hello world!");

       emu.frameadvance();

end;


