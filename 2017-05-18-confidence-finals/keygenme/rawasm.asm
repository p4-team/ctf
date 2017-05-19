mag_consts= dword ptr -84h
var_80= qword ptr -80h
anonymous_3= qword ptr -70h
anonymous_4= qword ptr -68h
var_60= byte ptr -60h
var_50= qword ptr -50h
anonymous_5= qword ptr -48h
var_40= qword ptr -40h
anonymous_2= qword ptr -38h
var_30= dword ptr -30h
anonymous_1= qword ptr -28h
var_20= qword ptr -20h
hi_arg= qword ptr -18h
a1= dword ptr  8

  ;; -0x90: III
  ;; -0x80: HHH
  ;; -0x70: GGG
  ;; -0x60: FFF
  ;; -0x50: EEE
  ;; -0x40: DDD
  ;; -0x30: CCC
  ;; -0x20: BBB
 	;; -0x10: AAA

push    ebp
mov     ebp, esp
sub     esp, 84h
mov     [ebp+mag_consts], offset magic_consts
lea     edi, [ebp+var_20]
mov     esi, [ebp+a1]

  ;; [BBB] == [ARG]
mov     eax, [esi]
mov     [edi], eax
mov     eax, [esi+4]
mov     [edi+4], eax
mov     eax, [esi+8]
mov     [edi+8], eax
mov     eax, [esi+0Ch]
mov     [edi+0Ch], eax

  ;; loc_F4102F:
loc_F4102F:                             ; CODE XREF: check_value+295j
lea     esi, [ebp+var_20]
lea     edi, [ebp+var_40]

  ;; [DDD] = [BBB]
mov     eax, [esi]
mov     [edi], eax
mov     eax, [esi+4]
mov     [edi+4], eax
mov     eax, [esi+8]
mov     [edi+8], eax
mov     eax, [esi+0Ch]
mov     [edi+0Ch], eax

  ;; [EEE] = 0
lea     edi, [ebp+var_50]
xor     eax, eax
mov     dword ptr [edi], 1
mov     [edi+4], eax
mov     [edi+8], eax
mov     [edi+0Ch], eax

  ;; [FFF] = [MAG[1]]
mov     esi, [ebp+mag_consts]
add     esi, 10h
lea     edi, [ebp+var_60]
mov     eax, [esi]
mov     [edi], eax
mov     eax, [esi+4]
mov     [edi+4], eax
mov     eax, [esi+8]
mov     [edi+8], eax
mov     eax, [esi+0Ch]
mov     [edi+0Ch], eax

  ;; loc_F41081:
loc_F41081:                             ; CODE XREF: check_value+262j
  ;; ZF = TEST [FFF] & 1
  ;; IF ZF GOTO loc_F4116A
test    [ebp+var_60], 1
jz      loc_F4116A

  ;; [HHH] = 0
lea     edx, [ebp+var_40]
lea     edi, [ebp+var_80]
xor     eax, eax
mov     [edi], eax
mov     [edi+4], eax
mov     [edi+8], eax
mov     [edi+0Ch], eax

  ;; [GGG] = [EEE]
lea     esi, [ebp+var_50]
mov     eax, [esi]
mov     [edi+10h], eax
mov     eax, [esi+4]
mov     [edi+14h], eax
mov     eax, [esi+8]
mov     [edi+18h], eax
mov     eax, [esi+0Ch]
mov     [edi+1Ch], eax

  ;;  ECX = 0x80
mov     ecx, 80h

  ;; loc_F410BD:
loc_F410BD:                             ; CODE XREF: check_value:loc_F410FCj
  ;; CF = SHL([GGG; HHH])
shl     dword ptr [edi], 1
rcl     dword ptr [edi+4], 1
rcl     dword ptr [edi+8], 1
rcl     dword ptr [edi+0Ch], 1
rcl     dword ptr [edi+10h], 1
rcl     dword ptr [edi+14h], 1
rcl     dword ptr [edi+18h], 1
rcl     dword ptr [edi+1Ch], 1

  ;; IF NOT CF GOTO loc_F410FC
jnb     short loc_F410FC

  ;;  [GGG; HHH] += [0; DDD]
mov     eax, [edx]
add     [edi], eax
mov     eax, [edx+4]
adc     [edi+4], eax
mov     eax, [edx+8]
adc     [edi+8], eax
mov     eax, [edx+0Ch]
adc     [edi+0Ch], eax
adc     dword ptr [edi+10h], 0
adc     dword ptr [edi+14h], 0
adc     dword ptr [edi+18h], 0
adc     dword ptr [edi+1Ch], 0

  ;; loc_F410FC:
loc_F410FC:                             ; CODE XREF: check_value+D4j
  ;; LOOP loc_F410BD
loop    loc_F410BD

  ;; [EEE] = 0
mov     edx, [ebp+mag_consts]
xor     eax, eax
mov     [esi], eax
mov     [esi+4], eax
mov     [esi+8], eax
mov     [esi+0Ch], eax

  ;;  ECX = 0x100
mov     ecx, 100h

  ;; loc_F41116:
loc_F41116:                             ; CODE XREF: check_value:loc_F41168j
  ;;  CF = SHL [EEE; GGG; HHH]
shl     dword ptr [edi], 1
rcl     dword ptr [edi+4], 1
rcl     dword ptr [edi+8], 1
rcl     dword ptr [edi+0Ch], 1
rcl     dword ptr [edi+10h], 1
rcl     dword ptr [edi+14h], 1
rcl     dword ptr [edi+18h], 1
rcl     dword ptr [edi+1Ch], 1
rcl     dword ptr [esi], 1
rcl     dword ptr [esi+4], 1
rcl     dword ptr [esi+8], 1
rcl     dword ptr [esi+0Ch], 1

  ;; IF CF GOTO	loc_F41152
jb      short loc_F41152

  ;; CF = CARRY [EEE] - [*MAG]
mov     eax, [esi]
sub     eax, [edx]
mov     eax, [esi+4]
sbb     eax, [edx+4]
mov     eax, [esi+8]
sbb     eax, [edx+8]
mov     eax, [esi+0Ch]
sbb     eax, [edx+0Ch]

  ;; IF CF GOTO loc_F41168
jb      short loc_F41168

  ;; loc_F41152;
loc_F41152:                             ; CODE XREF: check_value+138j
  ;; [EEE] -= [*MAG]
mov     eax, [edx]
sub     [esi], eax
mov     eax, [edx+4]
sbb     [esi+4], eax
mov     eax, [edx+8]
sbb     [esi+8], eax
mov     eax, [edx+0Ch]
sbb     [esi+0Ch], eax

  ;; loc_F41168
loc_F41168:                             ; CODE XREF: check_value+150j

  ;; LOOP	loc_F41116
loop    loc_F41116

  ;; loc_F4116A:
loc_F4116A:                             ; CODE XREF: check_value+85j
  ;; [HHH] = 0
lea     edx, [ebp+var_40]
lea     esi, [ebp+var_40]
lea     edi, [ebp+var_80]
xor     eax, eax
mov     [edi], eax
mov     [edi+4], eax
mov     [edi+8], eax
mov     [edi+0Ch], eax

  ;; [GGG] = [DDD]
mov     eax, [esi]
mov     [edi+10h], eax
mov     eax, [esi+4]
mov     [edi+14h], eax
mov     eax, [esi+8]
mov     [edi+18h], eax
mov     eax, [esi+0Ch]
mov     [edi+1Ch], eax

  ;; ECX = 0x80
mov     ecx, 80h

  ;; loc_F4119C:
loc_F4119C:                             ; CODE XREF: check_value:loc_F411DBj

  ;; CF = SHL [GGG; HHH]
shl     dword ptr [edi], 1
rcl     dword ptr [edi+4], 1
rcl     dword ptr [edi+8], 1
rcl     dword ptr [edi+0Ch], 1
rcl     dword ptr [edi+10h], 1
rcl     dword ptr [edi+14h], 1
rcl     dword ptr [edi+18h], 1
rcl     dword ptr [edi+1Ch], 1

  ;; IF NOT CF GOTO loc_F411DB
jnb     short loc_F411DB


  ;; [GGG; HHH] += [0; DDD]
mov     eax, [edx]
add     [edi], eax
mov     eax, [edx+4]
adc     [edi+4], eax
mov     eax, [edx+8]
adc     [edi+8], eax
mov     eax, [edx+0Ch]
adc     [edi+0Ch], eax
adc     dword ptr [edi+10h], 0
adc     dword ptr [edi+14h], 0
adc     dword ptr [edi+18h], 0
adc     dword ptr [edi+1Ch], 0

  ;; loc_F411DB
loc_F411DB:                             ; CODE XREF: check_value+1B3j

  ;; LOOP	loc_F4119C
loop    loc_F4119C

  ;; [DDD] = 0
mov     edx, [ebp+mag_consts]
xor     eax, eax
mov     [esi], eax
mov     [esi+4], eax
mov     [esi+8], eax
mov     [esi+0Ch], eax

  ;; ECX = 0x100
mov     ecx, 100h

  ;; loc_F411F5:
loc_F411F5:                             ; CODE XREF: check_value:loc_F41247j
  ;; CF = SHL [DDD; GGG; HHH]
shl     dword ptr [edi], 1
rcl     dword ptr [edi+4], 1
rcl     dword ptr [edi+8], 1
rcl     dword ptr [edi+0Ch], 1
rcl     dword ptr [edi+10h], 1
rcl     dword ptr [edi+14h], 1
rcl     dword ptr [edi+18h], 1
rcl     dword ptr [edi+1Ch], 1
rcl     dword ptr [esi], 1
rcl     dword ptr [esi+4], 1
rcl     dword ptr [esi+8], 1
rcl     dword ptr [esi+0Ch], 1

  ;; IF CF GOTO loc_F41231
jb      short loc_F41231

  ;; CF = [DDD] - [*MAG]
mov     eax, [esi]
sub     eax, [edx]
mov     eax, [esi+4]
sbb     eax, [edx+4]
mov     eax, [esi+8]
sbb     eax, [edx+8]
mov     eax, [esi+0Ch]
sbb     eax, [edx+0Ch]

  ;; IF CF GOTO loc_F41247
jb      short loc_F41247

  ;; loc_F41231
loc_F41231:                             ; CODE XREF: check_value+217j

  ;; [DDD] -= [*MAG]
mov     eax, [edx]
sub     [esi], eax
mov     eax, [edx+4]
sbb     [esi+4], eax
mov     eax, [edx+8]
sbb     [esi+8], eax
mov     eax, [edx+0Ch]
sbb     [esi+0Ch], eax

  ;; loc_F41247:
loc_F41247:                             ; CODE XREF: check_value+22Fj

  ;; LOOP loc_F411F5
loop    loc_F411F5

  ;; SHR [FFF]
lea     esi, [ebp+var_60]
shr     dword ptr [esi+0Ch], 1
rcr     dword ptr [esi+8], 1
rcr     dword ptr [esi+4], 1
rcr     dword ptr [esi], 1

  ;; ZF = [FFF] == 0
mov     eax, [esi]
or      eax, [esi+4]
or      eax, [esi+8]
or      eax, [esi+0Ch]

  ;; IF NOT ZF GOTO loc_F41081
jnz     loc_F41081

lea     esi, [ebp+var_50]
lea     edi, [ebp+var_20]

  ;; [BBB] = [EEE]
mov     eax, [esi]
mov     [edi], eax
mov     eax, [esi+4]
mov     [edi+4], eax
mov     eax, [esi+8]
mov     [edi+8], eax
mov     eax, [esi+0Ch]
mov     [edi+0Ch], eax

  ;; MAG++
add     [ebp+mag_consts], 20h
cmp     [ebp+mag_consts], offset aI3dragons ; "I<3Dragons"

  ;; CF = MAG < DRG
  ;; IF CF GOTO loc_F4102F
jb      loc_F4102F

  ;; [AAA] = 0
lea     esi, [ebp+var_20]
xor     eax, eax
mov     [esi+10h], eax
mov     [esi+14h], eax
mov     [esi+18h], eax
mov     [esi+1Ch], eax

  ;; [AAA; BBB] += 0x31337
add     dword ptr [esi], 31337h
adc     dword ptr [esi+4], 0
adc     dword ptr [esi+8], 0
adc     dword ptr [esi+0Ch], 0
adc     dword ptr [esi+10h], 0
adc     dword ptr [esi+14h], 0
adc     dword ptr [esi+18h], 0
adc     dword ptr [esi+1Ch], 0

lea     edx, aI3dragons                 ; "I<3Dragons"

  ;; [CCC] = 0
lea     edi, [ebp+var_30]
xor     eax, eax
mov     [edi], eax
mov     [edi+4], eax
mov     [edi+8], eax
mov     [edi+0Ch], eax

  ;; ECX = 0x100
mov     ecx, 100h

  ;; loc_F412E9:
loc_F412E9:                             ; CODE XREF: check_value:loc_F4133Bj

  ;; CF = SHL [CCC; AAA; BBB]
shl     dword ptr [esi], 1
rcl     dword ptr [esi+4], 1
rcl     dword ptr [esi+8], 1
rcl     dword ptr [esi+0Ch], 1
rcl     dword ptr [esi+10h], 1
rcl     dword ptr [esi+14h], 1
rcl     dword ptr [esi+18h], 1
rcl     dword ptr [esi+1Ch], 1
rcl     dword ptr [edi], 1
rcl     dword ptr [edi+4], 1
rcl     dword ptr [edi+8], 1
rcl     dword ptr [edi+0Ch], 1

  ;; IF CF GOTO loc_F41325
jb      short loc_F41325

  ;; CF = [CCC] - [DRG]
mov     eax, [edi]
sub     eax, [edx]
mov     eax, [edi+4]
sbb     eax, [edx+4]
mov     eax, [edi+8]
sbb     eax, [edx+8]
mov     eax, [edi+0Ch]
sbb     eax, [edx+0Ch]

  ;; IF CF GOTO loc_F4133B
jb      short loc_F4133B

  ;; loc_F41325:
loc_F41325:                             ; CODE XREF: check_value+30Bj

  ;; [CCC] -= [DRG]
mov     eax, [edx]
sub     [edi], eax
mov     eax, [edx+4]
sbb     [edi+4], eax
mov     eax, [edx+8]
sbb     [edi+8], eax
mov     eax, [edx+0Ch]
sbb     [edi+0Ch], eax

  ;; loc_F4133B:
loc_F4133B:                             ; CODE XREF: check_value+323j

  ;; LOOP	loc_F412E9
loop    loc_F412E9

  ;; RETURN [CCC] == 0
mov     eax, [edi]
or      eax, [edi+4]
or      eax, [edi+8]
or      eax, [edi+0Ch]
sub     eax, 1
sbb     eax, eax
mov     esp, ebp
pop     ebp
retn
