# Baldi's RE Basics (re, 421p, 3 solved)

Sadly we run out of time on this challenge, because the client we wrote was quite unstable, so we missed the flag.
But the solver actually works, so we thought we can write about this task anyway.

## Overview

In the challenge we have to solve set of problems.
Initially there are some simple trivia questions, always the same, so we can simply hardcode the answers.
Once we're done with this part we get this view:


    ----------------------------------------
    |       |      |       |       |       |
    |  ???  |      |  ???  |       |  ???  |
    |       |      |       |       |       |
    |--   ---      ---   ---       ---   --|
    |                                      |
    |                                      |
    |--------                              |
    |       |                              |
    |  ???             😦                  |
    |       |                              |
    |--------                              |
    |                                      |
    |                                      |
    |--   ---      ---   ---       ---   --|
    |       |      |       |       |       |
    |  ???  |      |  ???  |       |  ???  |
    |       |      |       |       |       |
    ----------------------------------------

    w/a/s/d:


Once we start walking to one of the rooms a room challenge launches.
Each room has 3 problems to solve:

- assemble given assembly code to machine code
- disassemble given machine code to assembly
- evaluate given machine code and provide the result

Rooms are randomized, in each run rooms shift, but first 6 of the rooms are always one of:

- i386
- x86_64
- MIPS
- ARM
- PowerPC32
- aarch64

## Clearing first 6 rooms

Clearing a room looks like this:


          _       ______     ____    ____  
         / \     |_   __ \   |_   \  /   _| 
        / _ \      | |__) |    |   \/   |   
       / ___ \     |  __ /     | |\  /| |   
     _/ /   \ \_  _| |  \ \_  _| |_\/_| |_  
    |____| |____||____| |___||_____||_____|

```
Press the Enter key to start the challenge...
Give me the binary code of the following assembly ( in base64 encoded format ): 
sub sp, sp, #0x18
mov r0, #0
str r0, [sp, #0x14]
mov r0, #6
orr r0, r0, #0x9c00
str r0, [sp, #0x10]
mov r0, #0x93
orr r0, r0, #0x9200
str r0, [sp, #0xc]
mov r0, #0x77
orr r0, r0, #0x1900
str r0, [sp, #8]
mov r0, #0xd2
orr r0, r0, #0x400
str r0, [sp, #4]
mov r0, #0x28c
orr r0, r0, #0x9800
str r0, [sp]
ldr r0, [sp, #0x10]
mov r1, #0x7d
orr r1, r1, #0x4200
eor r0, r0, r1
ldr r1, [sp, #0xc]
and r0, r0, r1
ldr r1, [sp, #8]
orr r0, r0, r1
ldr r1, [sp, #4]
add r0, r0, r1
ldr r1, [sp]
add r0, r0, r1
add sp, sp, #0x18
bx lr
Answer:

GNBN4gAAoOMUAI3lBgCg4ycLgOMQAI3lkwCg45IMgOMMAI3ldwCg4xkMgOMIAI3l0gCg4wELgOMEAI3low+g4yYLgOMAAI3lEACd5X0QoONCHIHjAQAg4AwQneUBAADgCBCd5QEAgOEEEJ3lAQCA4AAQneUBAIDgGNCN4h7/L+E=

Give me the assembly of this binary code ( in base64 encoded format ): 

INBN4gAAoOMcAI3lEwCg488MgOMYAI3lFwCg454MgOMUAI3lSQCg4x0LgOMQAI3l2wCg4zkLgOMMAI3laQCg4x0LgOMIAI3l+QCg40cMgOMEAI3l9Q+g4zELgOMAAI3lGACd5RQQneUBAADgqhCg44ccgeMBAADgEBCd5QEAgOAMEJ3lAQCA4QgQneUBAADgBBCd5QEAIOAAEJ3lAQCA4CDQjeIe/y/h

Answer:

c3ViIHNwLCBzcCwgIzB4MjAKbW92IHIwLCAjMApzdHIgcjAsIFtzcCwgIzB4MWNdCm1vdiByMCwgIzB4MTMKb3JyIHIwLCByMCwgIzB4Y2YwMApzdHIgcjAsIFtzcCwgIzB4MThdCm1vdiByMCwgIzB4MTcKb3JyIHIwLCByMCwgIzB4OWUwMApzdHIgcjAsIFtzcCwgIzB4MTRdCm1vdiByMCwgIzB4NDkKb3JyIHIwLCByMCwgIzB4NzQwMApzdHIgcjAsIFtzcCwgIzB4MTBdCm1vdiByMCwgIzB4ZGIKb3JyIHIwLCByMCwgIzB4ZTQwMApzdHIgcjAsIFtzcCwgIzB4Y10KbW92IHIwLCAjMHg2OQpvcnIgcjAsIHIwLCAjMHg3NDAwCnN0ciByMCwgW3NwLCAjOF0KbW92IHIwLCAjMHhmOQpvcnIgcjAsIHIwLCAjMHg0NzAwCnN0ciByMCwgW3NwLCAjNF0KbW92IHIwLCAjMHgzZDQKb3JyIHIwLCByMCwgIzB4YzQwMApzdHIgcjAsIFtzcF0KbGRyIHIwLCBbc3AsICMweDE4XQpsZHIgcjEsIFtzcCwgIzB4MTRdCmFuZCByMCwgcjAsIHIxCm1vdiByMSwgIzB4YWEKb3JyIHIxLCByMSwgIzB4ODcwMAphbmQgcjAsIHIwLCByMQpsZHIgcjEsIFtzcCwgIzB4MTBdCmFkZCByMCwgcjAsIHIxCmxkciByMSwgW3NwLCAjMHhjXQpvcnIgcjAsIHIwLCByMQpsZHIgcjEsIFtzcCwgIzhdCmFuZCByMCwgcjAsIHIxCmxkciByMSwgW3NwLCAjNF0KZW9yIHIwLCByMCwgcjEKbGRyIHIxLCBbc3BdCmFkZCByMCwgcjAsIHIxCmFkZCBzcCwgc3AsICMweDIwCmJ4IGxy

'What is \x18\xd0M\xe2\x00\x00\xa0\xe3\x14\x00\x8d\xe5\xab\x0f\xa0\xe3\x10\x00\x8d\xe5\x99\x0f\xa0\xe3\x0e\x0b\x80\xe3\x0c\x00\x8d\xe5\xbb\x00\xa0\xe3\xde\x0c\x80\xe3\x08\x00\x8d\xe5\x92\x00\xa0\xe3g\x0c\x80\xe3\x04\x00\x8d\xe5\x9b\x00\xa0\xe3Z\x0c\x80\xe3\x00\x00\x8d\xe5\x10\x00\x9d\xe5+\x10\xa0\xe3\x92\x1c\x81\xe3\x01\x00 \xe0\x0c\x10\x9d\xe5\x01\x00\x00\xe0\x08\x10\x9d\xe5\x01\x00\x00\xe0\x04\x10\x9d\xe5\x01\x00@\xe0\x00\x10\x9d\xe5\x01\x00 \xe0\x18\xd0\x8d\xe2\x1e\xff/\xe1 ?'

Answer:

0xfffff2f5L
```

Those 6 rooms we managed to solve automatically using Keystone, Capstone and Unicorn.
Unicorn couldn't emulate PPC for us, so we wrote a very basic [interpreter](risclib.py).
This interpreter is very poor and lacks some opcodes, so it sometimes fail...

## 7th room

Once we reach 7th room it turns out there is yet another architecture to tackle:


      _____  _____  _____  _____   __      __
     |  __ \|_   _|/ ____|/ ____|  \ \    / /
     | |__) | | | | (___ | |   _____\ \  / / 
     |  _  /  | |  \___ \| |  |______\ \/ /  
     | | \ \ _| |_ ____) | |____      \  /   
     |_|  \_\_____|_____/ \_____|      \/ 


The problem is that neither of the tools we've been using support it, so we had to do it the hard way.
We found a very simple asembler/disasembler for RISC-V in Python on github: https://github.com/wueric/riscv_assembler/tree/master/assembler
We modified this to suit the challenges (some opcodes were missing, some were translated differently).
Finally we ended up with [assembler](riscv_asm.py) and [disasembler](riscv_dis.py) which work on the challenges.
Last part was the code evaluator, and for this we used the same approach as for PPC - we wrote it by hand getting another [interpreter](risclib.py). 
There is the same issue as for PPC - it doesn't work very well, but it can solve some of the challenges.

Once we pass the 7th room, we're faced with another view:


    ----------------------------------------
    |       |      |       |       |       |
    | EXIT6 |      | EXIT2 |       | EXIT1 |
    |       |      |       |       |       |
    |--   ---      ---   ---       ---   --|
    |                                      |
    |                                      |
    |--------                              |
    |       |                              |
    | EXIT3            😭                  |
    |       |                              |
    |--------                              |
    |                                      |
    |                                      |
    |--   ---      ---   ---       ---   --|
    |       |      |       |       |       |
    | EXIT0 |      | EXIT5 |       | EXIT4 |
    |       |      |       |       |       |
    ----------------------------------------


Now we can walk around the rooms again, collecting parts of the flag from each exit:
```
 __    __   __  .___________.
|  |  |  | |  | |           |
|  |__|  | |  | `---|  |----`
|   __   | |  |     |  |     
|  |  |  | |  |     |  |     
|__|  |__| |__|     |__|   


  ______   ______   .__   __.    ___
 /      | /  __  \  |  \ |  |   /  /
|  ,----'|  |  |  | |   \|  |  |  | 
|  |     |  |  |  | |  . `  | /  /  
|  `----.|  `--'  | |  |\   | \  \  
 \______| \______/  |__| \__|  |  | 
                                \__
 __    __        .______              
|  |  |  |       |   _  \             
|  |  |  |       |  |_)  |            
|  |  |  |       |      /             
|  `--'  |       |  |\  \----.        
 \______/   _____| _| `._____| ______ 
           |______|           |______|


 _______   _  _          .___  ___. 
|       \ | || |         |   \/   | 
|  .--.  || || |_        |  \  /  | 
|  |  |  ||__   _|       |  |\/|  | 
|  '--'  |   | |         |  |  |  | 
|_______/    |_|    _____|__|  |__| 
                   |______|         

     ___       _____  .___________.____   
    /   \     | ____| |           |___ \  
   /  ^  \    | |__   `---|  |----` __) | 
  /  /_\  \   |___ \      |  |     |__ <  
 /  _____  \   ___) |     |  |     ___) | 
/__/     \__\ |____/      |__|    |____/

.______             ___    _______ 
|   _  \           / _ \  |   ____|
|  |_)  |         | | | | |  |__   
|      /          | | | | |   __|  
|  |\  \----.     | |_| | |  |     
| _| `._____| _____\___/  |__|     
             |______|    

      .______      ____   
      |   _  \    |___ \  
      |  |_)  |     __) | 
      |      /     |__ <  
      |  |\  \----.___) | 
 _____| _| `._____|____/  
|______|                
```

But once we collect them, a secret door gets opened:

    
    ----------------------------------------
    |       |      |       |       |       |
    | EXIT6 |      | EXIT2 |       | EXIT1 |
    |       |      |       |       |       |
    |--------      ---------       --------|
    |   🤩                                 |
    |                                      |
    |--------                              ----
    |       |                               
    | EXIT3 |                               
    |       |                               
    |--------                              ----
    |                                      |
    |                                      |
    |--------      ---------       --------|
    |       |      |       |       |       |
    | EXIT0 |      | EXIT5 |       | EXIT4 |
    |       |      |       |       |       |
    ----------------------------------------


Once you walk there, you're faced with the final architecture:

```
 ▄█     █▄     ▄████████    ▄████████   ▄▄▄▄███▄▄▄▄   
███     ███   ███    ███   ███    ███ ▄██▀▀▀███▀▀▀██▄ 
███     ███   ███    ███   ███    █▀  ███   ███   ███ 
███     ███   ███    ███   ███        ███   ███   ███ 
███     ███ ▀███████████ ▀███████████ ███   ███   ███ 
███     ███   ███    ███          ███ ███   ███   ███ 
███ ▄█▄ ███   ███    ███    ▄█    ███ ███   ███   ███ 
 ▀███▀███▀    ███    █▀   ▄████████▀   ▀█   ███   █▀ 

```

For WASM we decided to use existing tools: https://github.com/WebAssembly/wabt
There is asembler, disasembler and interpter.
We decided to simply call those tools from python script and collect the outputs.
The only trick was that we get only code without the function header, so we have to place the code in proper structure in order to assemble/disassemble or evaluate.
For this we created a small [wrapper](wasmlib.py).

Once we pass the WASM stage we get the last chunk of the flag:

```
           ___      .__   __.  _______  
          /   \     |  \ |  | |       \ 
         /  ^  \    |   \|  | |  .--.  |
        /  /_\  \   |  . `  | |  |  |  |
       /  _____  \  |  |\   | |  '--'  |
 _____/__/     \__\ |__| \__| |_______/ 
|______|                                
      .______   .______     ______      
      |   _  \  |   _  \   /      |     
      |  |_)  | |  |_)  | |  ,----'     
      |   ___/  |   ___/  |  |          
      |  |      |  |      |  `----.     
 _____| _|      | _|       \______|     
|______|                                
       __     _  _    ____   ___        
      |  |  _| || |_ |___ \  \  \       
      |  | |_  __  _|  __) |  |  |      
      |  |  _| || |_  |__ <    \  \     
      |__| |_  __  _| ___) |   /  /     
 _____(__)   |_||_|  |____/   |  |      
|______|                     /__/  
```

The task was interesting, but the fact that last 2 architectures were "secret" until you reached them was very annoying.
It was kind of a honey-pot challenge.
It seemed doable initially, with Keystone, Capstone and Unicorn, but the further you go, the harder it got.
Entire solver script is [here](solver.py) but it's quite unstable so you might need to run it multiple times before you manage to win.
There is high probability of solver failing for PPC and RISC-V code evaluation.
