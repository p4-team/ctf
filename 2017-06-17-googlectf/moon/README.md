# Moon (re, 246p)

> What's the password?

> moon.zip

In this challenge, we were given a Windows binary with a bunch of graphical libraries.
I solved the challenge without ever running it fully (not because it was so easy for me,
but because it didn't work out of the box on my virtual machine, and I didn't feel
like installing missing things). Knowing Gynvael, who created this task, it was likely 
a demo-like graphical effect with some password to be typed in.

After finding the main function, reversing the main logic was not too hard. The program
was loading a couple of resources from read-only section - some of them being PNGs,
some were random-looking hex strings, and there was even a shader program. One of the 
"random" strings was later decrypted to another shader program. I found it pretty suspicious,
so I decided to take a closer look at it:
```
#version 430
layout(local_size_x=8,local_size_y=8) in;
layout(std430,binding=0) buffer 
shaderExchangeProtocol{
	uint state[64];
	uint hash[64];
	uint password[32];
};
vec3 calc(uint p){
	float r=radians(p);
	float c=cos(r);
	float s=sin(r);
	mat3 m=mat3(c,-s,0.0,s,c,0.0,0.0,0.0,1.0);
	vec3 pt=vec3(1024.0,0.0,0.0);
	vec3 res=m*pt;
	res+=vec3(2048.0,2048.0,0.0);
	return res;
}
uint extend(uint e){
	uint i;
	uint r=e^0x5f208c26;
	for (i=15;i<31;i+=3){
		uint f=e<<i;
		r^=f;
	}
	return r;
}
uint hash_alpha(uint p){
	vec3 res=calc(p);
	return extend(uint(res[0]));
}
uint hash_beta(uint p){
	vec3 res=calc(p);
	return extend(uint(res[1]));
}
void main(){
	uint idx=gl_GlobalInvocationID.x+gl_GlobalInvocationID.y*8;
	uint final;
	if (state[idx]!=1){return;}
	if ((idx&1)==0){
		final=hash_alpha(password[idx/2]);
	}
	else{
		final=hash_beta(password[idx/2]);
	}
	uint i;
	for (i=0;i<32;i+=6){
		final^=idx<<i;
	}
	uint h=0x5a;
	for (i=0;i<32;i++){
		uint p=password[i];
		uint r=(i*3)&7;
		p=(p<<r)|(p>>(8-r));
		p&=0xff;
		h^=p;
	}
	final^=(h|(h<<8)|(h<<16)|(h<<24));
	hash[idx]=final;
	state[idx]=2;
	memoryBarrierShared();
}
```

Yep, it seems to be calculating a handmade hash of the password. It first calculates 
a `hash_alpha` or `hash_beta` of a single character, then makes some additional xors with
current character index, and then xors it with a simple 8-byte hash `h` of the whole password.
The final result is copied into the output buffer (`hash`).

The main binary runs this program and then compares the result to a hardcoded string. It seems
we need to reverse engineer the hash algorithm then. Fortunately, it's pretty simple.
We can brute force the 8-byte hash of the whole password, and then separately brute force 
each character, every time checking whether the corresponding hash bytes match up.

The whole code of the solver is in `sim.py`.
