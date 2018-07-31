exploit.exe: exploit.c zygote.idl
	x86_64-w64-mingw32-widl --win64 zygote.idl
	x86_64-w64-mingw32-gcc -s -o $@ exploit.c zygote_c.c -lrpcrt4
