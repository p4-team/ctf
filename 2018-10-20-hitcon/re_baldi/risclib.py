code = '''addi sp, sp, -64                                                                                                       
sw ra, 4(sp)                                                                                                           
sw s0, 0(sp)                                                                                                           
addi s0, sp, 8                                                                                                         
addi sp, sp, -32                                                                                                       
sw s1, 28(sp)                                              
sw s2, 24(sp)                                              
sw s3, 20(sp)                                              
sw s4, 16(sp)                                              
lui s1, 0x7                                                
addi s1, s1, -1534                                         
sw s1, 0(s0)                                               
lui s1, 0xc                                                
addi s1, s1, -133                                                                                                      
sw s1, 4(s0)                                                                                                                                                                                                                                  
lui s1, 0x1                                                                                                                                                                                                                                   
addi s1, s1, 1086                                                                                                                                                                                                                             
sw s1, 8(s0)                                                                                                                                                                                                                                  
lui s1, 0x6                                                                                                                                                                                                                                   
addi s1, s1, 1627                                                                                                      
sw s1, 12(s0)                                              
lui s1, 0xf                                                
addi s1, s1, -1242                                                                                                                                                                                                                            
sw s1, 16(s0)                                                                                                                                                                                                                                 
lui s1, 0x3                                                                                                                                                                                                                                   
addi s1, s1, -770                                                                                                                                                                                                                             
sw s1, 20(s0)                                              
lui s1, 0xe                                                                                                                                                                                                                                   
addi s1, s1, -719                                                                                                                                                                                                                             
sw s1, 24(s0)                                                                                                                                                                                                                                 
lui s1, 0x4                                                                                                            
addi s1, s1, -508                                                                                                      
sw s1, 28(s0)                                                                                                          
lui s1, 0x8                                                                                                            
addi s1, s1, 574                                                                                                       
sw s1, 32(s0)                                              
lui s1, 0x7                                                
addi s1, s1, 629                                           
sw s1, 36(s0)                                              
lui s1, 0x5                                                
addi s1, s1, -1394                                         
sw s1, 40(s0)                                              
lw a7, 0(s0)                                               
lw s3, 4(s0)                                                                                                           
lw s2, 8(s0)                                                                                                           
lw a6, 12(s0)                                                                                                          
lw a5, 16(s0)                                                                                                                                                                                                                                 
lw a4, 20(s0)                                                                                                          
lw a3, 24(s0)                                                                                                          
lw a2, 28(s0)                                                                                                          
lw a1, 32(s0)                                              
lw a0, 36(s0)                                              
lw s1, 40(s0)                                              
lui s4, 0x9                                                
addi s4, s4, 889                                           
mul a7, s4, a7                                             
or a7, a7, s3                                              
and a7, a7, s2                                                                                                         
xor a6, a7, a6                                                      
or a5, a6, a5                                                       
or a4, a5, a4                                                       
xor a3, a4, a3                                                      
or a2, a3, a2                                                       
mul a1, a2, a1                                                      
add a0, a1, a0                                                      
and a0, a0, s1                                                      
j 0x108                                                                        
lw s1, 28(sp)                                                                  
lw s2, 24(sp)                                                                  
lw s3, 20(sp)                                                                  
lw s4, 16(sp)                                                                  
addi sp, sp, 32                                                                                
lw ra, 4(sp)                                                                                   
lw s0, 0(sp)                                                                                   
addi sp, sp, 64                                                                                
ret                        
'''


def risc_execute(code):
    code = code.split('\n')

    regs = {
        'sp': 0,
        'ra': None,
        's0': None,
        's1': None,
        's2': None,
        's3': None,
        's4': None,
        's5': None,
        's6': None,
        's7': None,
        's8': None,
        's9': None,
        's10': None,
        'a0': None,
        'a1': None,
        'a2': None,
        'a3': None,
        'a4': None,
        'a5': None,
        'a6': None,
        'r3': None,
    }
    mem = {}
    for insn in code:
        insn = insn.replace(',', ' ').split()
        if not insn:
            continue
        op = insn[0]
        args = insn[1:]
        # print op, args
        if op == 'j':
            continue  # yolo
        elif op == 'lui':
            if '0x' in args[1]:
                regs[args[0]] = int(args[1], 16) * 2 ** 12
            else:
                regs[args[0]] = int(args[1]) * 2 ** 12
        elif op == 'li':
            regs[args[0]] = int(args[1], 16)
        elif op == 'addi':
            regs[args[0]] = regs[args[1]] + int(args[2])
        elif op == 'add':
            regs[args[0]] = (regs[args[2]] + regs[args[1]]) % 2 ** 32
        elif op == 'sub':
            regs[args[0]] = (regs[args[1]] - regs[args[2]]) % 2 ** 32
        elif op == 'ori':
            regs[args[0]] = regs[args[1]] | int(args[2])
        elif op == 'or':
            regs[args[0]] = (regs[args[2]] | regs[args[1]]) % 2 ** 32
        elif op == 'xori':
            regs[args[0]] = regs[args[1]] ^ int(args[2])
        elif op == 'and':
            regs[args[0]] = regs[args[1]] & regs[args[2]]
        elif op == 'or':
            regs[args[0]] = regs[args[1]] | regs[args[2]]
        elif op == 'xor':
            regs[args[0]] = regs[args[1]] ^ regs[args[2]]
        elif op == 'mr':
            regs[args[0]] = regs[args[1]]
        elif op == 'sw':
            mem[args[1]] = regs[args[0]]
        elif op == 'lw':
            regs[args[0]] = mem[args[1]]
        elif op == 'mul':
            regs[args[0]] = (regs[args[2]] * regs[args[1]]) % 2 ** 32
        elif op == 'rlwinm':
            continue
        elif op == 'subfic':
            continue
        elif op == 'stwu':
            continue
        elif op == 'xoris':
            continue
        elif op == 'blr':
            continue
        elif op == 'ret':
            continue
        else:
            print op
    print regs
    return regs['a0']


if __name__ == '__main__':
    print hex(risc_execute(code))
