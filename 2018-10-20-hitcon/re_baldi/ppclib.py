code = '''
rlwinm r8, r27, 0xc, 5, 0x1a     
subfic r3, r9, 0x7320            
stwu r1, -0x30(r1)               
stw r31, 0x2c(r1)                
mr r31, r1                       
li r3, 0                         
stw r3, 0x28(r31)                
li r3, 0x78ea                    
stw r3, 0x24(r31)                
li r3, 0x15ec                    
stw r3, 0x20(r31)                
lis r3, 0                        
ori r4, r3, 0xf8a5               
stw r4, 0x1c(r31)                
li r4, 0x677f                    
stw r4, 0x18(r31)                
ori r3, r3, 0xc3fa               
stw r3, 0x14(r31)                
lwz r3, 0x24(r31)                
xori r3, r3, 0xfdd3              
lwz r4, 0x20(r31)                
add r3, r3, r4                   
lwz r4, 0x1c(r31)                
add r3, r3, r4                   
lwz r4, 0x18(r31)                
and r3, r3, r4                   
lwz r4, 0x14(r31)                
add r3, r3, r4                   
lwz r31, 0x2c(r1)                
addi r1, r1, 0x30                
blr                              
subfic r1, r31, 0xa41            
xoris r19, r19, 0x7765           
'''


def ppc_execute(code):
    code = code.split('\n')

    regs = {
        'r3': None,
        'r4': None,
        'r1': 0,
        'r2': None,
        'r31': None
    }
    mem = {}
    for insn in code:
        insn = insn.replace(',', ' ').split()
        if not insn:
            continue
        op = insn[0]
        args = insn[1:]
        if op == 'li':
            regs[args[0]] = int(args[1], 16)
        elif op == 'lis':
            regs[args[0]] = int(args[1], 16)
        elif op == 'ori':
            regs[args[0]] = regs[args[1]] | int(args[2], 16)
        elif op == 'xori':
            regs[args[0]] = regs[args[1]] ^ int(args[2], 16)
        elif op == 'andi':
            regs[args[0]] = regs[args[1]] & int(args[2], 16)
        elif op == 'and':
            regs[args[0]] = regs[args[1]] & regs[args[2]]
        elif op == 'or':
            regs[args[0]] = regs[args[1]] | regs[args[2]]
        elif op == 'xor':
            regs[args[0]] = regs[args[1]] ^ regs[args[2]]
        elif op == 'mr':
            regs[args[0]] = regs[args[1]]
        elif op == 'stw':
            mem[args[1]] = regs[args[0]]
        elif op == 'lwz':
            regs[args[0]] = mem[args[1]]
        elif op == 'addi':
            regs[args[0]] = (regs[args[1]] + int(args[2], 16)) % 2**32
        elif op == 'addis':
            regs[args[0]] = (regs[args[1]] + int(args[2], 16)) % 2**32
        elif op == 'add':
            regs[args[0]] = (regs[args[2]] + regs[args[1]]) % 2**32
        elif op == 'subf':
            regs[args[0]] = (regs[args[2]] - regs[args[1]]) % 2**32
        elif op == 'mullw':
            regs[args[0]] = (regs[args[2]] * regs[args[1]]) % 2**32
        elif op == 'mulli':
            regs[args[0]] = (regs[args[2]] * int(regs[args[1]], 16)) % 2**32
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
        else:
            print op
        print insn
    print regs
    return regs['r3']


if __name__ == '__main__':
    print hex(ppc_execute(code))