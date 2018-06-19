# Encrypted espionage equipment, re, 468p

> Our agents have discovered this gadget in one of the conference rooms. It is now located at the organizers table. We managed to extract the firmware. Can you make sense of it?

In this task we got an ESP32 binary. It was actually an ELF with some symbols left, which heavily helped reversing it.
Nonetheless, being xtensa architecture, there is next to no good tooling for analyzing it. We compiled an official
toolchain from Espressif website, allowing us to use objdump and similar commands. Even then, analysis was hard, mostly
due to very frequent indirection. In fact, we wrote a simple script parsing objdump output, that would append
dereferenced address (sometimes twice...) to opcode's line. 

Before:
```
400d18db:       f9ecb1          l32r    a11, 400d008c <_flash_cache_start+0x74>
```
After:
```
400d18db:       f9ecb1          l32r    a11, 400d008c [0x3f401185-"%08x"] <_flash_cache_start+0x74>
```

After reversing, we found out that the chip was trying to connect to a certain SSID. The exact name and password
was changing every thirty seconds, and was generated using BLAKE2S hash in HMAC mode. If connection succeeded, it
would try to then connect to a certain IP and port, then listen for commands (in particular, `flag`, that would print
out the flag). We set up Wi-Fi hotspot using calculated credentials, set our laptop's IP appropriately. After
listening on the correct port, we eventually got the connection and the flag.
