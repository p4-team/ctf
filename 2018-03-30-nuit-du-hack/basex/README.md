# BaseX, 300p, exploit

> BaseX stores datas from stdin into a buffer.

The binary was allowing us to write arbitrary data to arbitrary offset from
stack (simple buffer overflow). A complication was that we had no echo, which
made debugging the exploit harder. In the end, we ROP-ped to gadgets, overwriting
`fread` GOT entry to `system`'s, then jumped there with crafted command string.
