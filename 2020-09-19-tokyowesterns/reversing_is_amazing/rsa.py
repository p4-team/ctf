# We reverse the binary to obtain the parameters, then perform RSA:

from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes

data = """.rodata:0000000000001100       db 30h                  ; DATA XREF: main+3AE↑o
.rodata:0000000000001101                 db  82h
.rodata:0000000000001102                 db    2
.rodata:0000000000001103                 db  5Ch ; 
.rodata:0000000000001104                 db    2
.rodata:0000000000001105                 db    1
.rodata:0000000000001106                 db    0
.rodata:0000000000001107                 db    2
.rodata:0000000000001108                 db  81h
.rodata:0000000000001109                 db  81h
.rodata:000000000000110A                 db    0
.rodata:000000000000110B                 db 0AEh
.rodata:000000000000110C                 db  68h ; h
.rodata:000000000000110D                 db  61h ; a
.rodata:000000000000110E                 db 0D4h
.rodata:000000000000110F                 db  73h ; s
.rodata:0000000000001110                 db 0A6h
.rodata:0000000000001111                 db  33h ; 3
.rodata:0000000000001112                 db  31h ; 1
.rodata:0000000000001113                 db  33h ; 3
.rodata:0000000000001114                 db 0C2h
.rodata:0000000000001115                 db  1Ah
.rodata:0000000000001116                 db  5Eh ; ^
.rodata:0000000000001117                 db 0BEh
.rodata:0000000000001118                 db 0F5h
.rodata:0000000000001119                 db 0ECh
.rodata:000000000000111A                 db  90h
.rodata:000000000000111B                 db 0EAh
.rodata:000000000000111C                 db  85h
.rodata:000000000000111D                 db  77h ; w
.rodata:000000000000111E                 db 0EAh
.rodata:000000000000111F                 db 0C2h
.rodata:0000000000001120                 db 0DBh
.rodata:0000000000001121                 db  62h ; b
.rodata:0000000000001122                 db  73h ; s
.rodata:0000000000001123                 db 0B5h
.rodata:0000000000001124                 db  29h ; )
.rodata:0000000000001125                 db  5Dh ; ]
.rodata:0000000000001126                 db 0C2h
.rodata:0000000000001127                 db 0BBh
.rodata:0000000000001128                 db  3Ah ; :
.rodata:0000000000001129                 db  3Ch ; <
.rodata:000000000000112A                 db 0D1h
.rodata:000000000000112B                 db  50h ; P
.rodata:000000000000112C                 db 0BBh
.rodata:000000000000112D                 db 0D4h
.rodata:000000000000112E                 db 0D4h
.rodata:000000000000112F                 db  9Eh
.rodata:0000000000001130                 db 0EEh
.rodata:0000000000001131                 db  33h ; 3
.rodata:0000000000001132                 db 0DDh
.rodata:0000000000001133                 db  3Bh ; ;
.rodata:0000000000001134                 db  30h ; 0
.rodata:0000000000001135                 db  45h ; E
.rodata:0000000000001136                 db  3Ch ; <
.rodata:0000000000001137                 db 0EBh
.rodata:0000000000001138                 db 0BEh
.rodata:0000000000001139                 db 0F1h
.rodata:000000000000113A                 db  1Fh
.rodata:000000000000113B                 db  67h ; g
.rodata:000000000000113C                 db 0E4h
.rodata:000000000000113D                 db    5
.rodata:000000000000113E                 db  5Ch ; 
.rodata:000000000000113F                 db  8Bh
.rodata:0000000000001140                 db  9Ch
.rodata:0000000000001141                 db  6Fh ; o
.rodata:0000000000001142                 db  3Ah ; :
.rodata:0000000000001143                 db  56h ; V
.rodata:0000000000001144                 db 0BAh
.rodata:0000000000001145                 db 0E2h
.rodata:0000000000001146                 db 0BAh
.rodata:0000000000001147                 db 0ECh
.rodata:0000000000001148                 db  9Ah
.rodata:0000000000001149                 db 0A7h
.rodata:000000000000114A                 db 0D0h
.rodata:000000000000114B                 db  43h ; C
.rodata:000000000000114C                 db 0EDh
.rodata:000000000000114D                 db 0BCh
.rodata:000000000000114E                 db  27h ; '
.rodata:000000000000114F                 db  50h ; P
.rodata:0000000000001150                 db  46h ; F
.rodata:0000000000001151                 db 0C8h
.rodata:0000000000001152                 db  40h ; @
.rodata:0000000000001153                 db  92h
.rodata:0000000000001154                 db  2Eh ; .
.rodata:0000000000001155                 db  87h
.rodata:0000000000001156                 db 0B6h
.rodata:0000000000001157                 db  24h ; $
.rodata:0000000000001158                 db 0E3h
.rodata:0000000000001159                 db 0F4h
.rodata:000000000000115A                 db 0C3h
.rodata:000000000000115B                 db  1Bh
.rodata:000000000000115C                 db 0D6h
.rodata:000000000000115D                 db 0BDh
.rodata:000000000000115E                 db 0ADh
.rodata:000000000000115F                 db  55h ; U
.rodata:0000000000001160                 db 0A4h
.rodata:0000000000001161                 db  51h ; Q
.rodata:0000000000001162                 db  64h ; d
.rodata:0000000000001163                 db  23h ; #
.rodata:0000000000001164                 db  10h
.rodata:0000000000001165                 db 0D1h
.rodata:0000000000001166                 db  6Ch ; l
.rodata:0000000000001167                 db  14h
.rodata:0000000000001168                 db 0FDh
.rodata:0000000000001169                 db  35h ; 5
.rodata:000000000000116A                 db 0A8h
.rodata:000000000000116B                 db  18h
.rodata:000000000000116C                 db 0A1h
.rodata:000000000000116D                 db  9Fh
.rodata:000000000000116E                 db 0ABh
.rodata:000000000000116F                 db  33h ; 3
.rodata:0000000000001170                 db  14h
.rodata:0000000000001171                 db 0F9h
.rodata:0000000000001172                 db  3Eh ; >
.rodata:0000000000001173                 db  50h ; P
.rodata:0000000000001174                 db  34h ; 4
.rodata:0000000000001175                 db 0C4h
.rodata:0000000000001176                 db  3Ch ; <
.rodata:0000000000001177                 db  28h ; (
.rodata:0000000000001178                 db 0B6h
.rodata:0000000000001179                 db  10h
.rodata:000000000000117A                 db 0D2h
.rodata:000000000000117B                 db 0FCh
.rodata:000000000000117C                 db  90h
.rodata:000000000000117D                 db  9Bh
.rodata:000000000000117E                 db  97h
.rodata:000000000000117F                 db  60h ; `
.rodata:0000000000001180                 db 0D5h
.rodata:0000000000001181                 db  9Ah
.rodata:0000000000001182                 db  13h
.rodata:0000000000001183                 db 0E5h
.rodata:0000000000001184                 db  3Eh ; >
.rodata:0000000000001185                 db 0BFh
.rodata:0000000000001186                 db  38h ; 8
.rodata:0000000000001187                 db 0D0h
.rodata:0000000000001188                 db  52h ; R
.rodata:0000000000001189                 db  66h ; f
.rodata:000000000000118A                 db  7Dh ; }
.rodata:000000000000118B                 db    2
.rodata:000000000000118C                 db    3
.rodata:000000000000118D                 db    1
.rodata:000000000000118E                 db    0
.rodata:000000000000118F                 db    1
.rodata:0000000000001190                 db    2
.rodata:0000000000001191                 db  81h
.rodata:0000000000001192                 db  80h
.rodata:0000000000001193                 db    3
.rodata:0000000000001194                 db  7Eh ; ~
.rodata:0000000000001195                 db  81h
.rodata:0000000000001196                 db 0DFh
.rodata:0000000000001197                 db  40h ; @
.rodata:0000000000001198                 db 0C5h
.rodata:0000000000001199                 db 0E6h
.rodata:000000000000119A                 db 0A6h
.rodata:000000000000119B                 db 0A8h
.rodata:000000000000119C                 db 0B3h
.rodata:000000000000119D                 db 0CDh
.rodata:000000000000119E                 db 0D5h
.rodata:000000000000119F                 db  72h ; r
.rodata:00000000000011A0                 db  1Bh
.rodata:00000000000011A1                 db 0F9h
.rodata:00000000000011A2                 db  36h ; 6
.rodata:00000000000011A3                 db  5Ah ; Z
.rodata:00000000000011A4                 db  0Ch
.rodata:00000000000011A5                 db  7Ch ; |
.rodata:00000000000011A6                 db  7Fh ; 
.rodata:00000000000011A7                 db  8Eh
.rodata:00000000000011A8                 db  91h
.rodata:00000000000011A9                 db 0D8h
.rodata:00000000000011AA                 db 0A2h
.rodata:00000000000011AB                 db  1Ah
.rodata:00000000000011AC                 db 0D2h
.rodata:00000000000011AD                 db  0Eh
.rodata:00000000000011AE                 db  57h ; W
.rodata:00000000000011AF                 db 0D5h
.rodata:00000000000011B0                 db  6Ah ; j
.rodata:00000000000011B1                 db  70h ; p
.rodata:00000000000011B2                 db  47h ; G
.rodata:00000000000011B3                 db  7Dh ; }
.rodata:00000000000011B4                 db  47h ; G
.rodata:00000000000011B5                 db  96h
.rodata:00000000000011B6                 db  17h
.rodata:00000000000011B7                 db    0
.rodata:00000000000011B8                 db  6Ch ; l
.rodata:00000000000011B9                 db  23h ; #
.rodata:00000000000011BA                 db  4Bh ; K
.rodata:00000000000011BB                 db 0DEh
.rodata:00000000000011BC                 db  60h ; `
.rodata:00000000000011BD                 db 0B4h
.rodata:00000000000011BE                 db  32h ; 2
.rodata:00000000000011BF                 db  69h ; i
.rodata:00000000000011C0                 db  42h ; B
.rodata:00000000000011C1                 db 0B5h
.rodata:00000000000011C2                 db  0Fh
.rodata:00000000000011C3                 db 0FDh
.rodata:00000000000011C4                 db    3
.rodata:00000000000011C5                 db 0DBh
.rodata:00000000000011C6                 db  7Bh ; {
.rodata:00000000000011C7                 db 0A4h
.rodata:00000000000011C8                 db  2Ch ; ,
.rodata:00000000000011C9                 db  69h ; i
.rodata:00000000000011CA                 db  2Ah ; *
.rodata:00000000000011CB                 db  11h
.rodata:00000000000011CC                 db  0Ch
.rodata:00000000000011CD                 db 0C3h
.rodata:00000000000011CE                 db  78h ; x
.rodata:00000000000011CF                 db  1Dh
.rodata:00000000000011D0                 db  3Fh ; ?
.rodata:00000000000011D1                 db  67h ; g
.rodata:00000000000011D2                 db 0F7h
.rodata:00000000000011D3                 db  42h ; B
.rodata:00000000000011D4                 db 0BCh
.rodata:00000000000011D5                 db 0BAh
.rodata:00000000000011D6                 db  38h ; 8
.rodata:00000000000011D7                 db 0AEh
.rodata:00000000000011D8                 db 0CCh
.rodata:00000000000011D9                 db  26h ; &
.rodata:00000000000011DA                 db 0DBh
.rodata:00000000000011DB                 db 0CAh
.rodata:00000000000011DC                 db  81h
.rodata:00000000000011DD                 db  1Eh
.rodata:00000000000011DE                 db  49h ; I
.rodata:00000000000011DF                 db 0FDh
.rodata:00000000000011E0                 db 0FAh
.rodata:00000000000011E1                 db    6
.rodata:00000000000011E2                 db 0BDh
.rodata:00000000000011E3                 db  32h ; 2
.rodata:00000000000011E4                 db  83h
.rodata:00000000000011E5                 db  3Bh ; ;
.rodata:00000000000011E6                 db  9Eh
.rodata:00000000000011E7                 db  66h ; f
.rodata:00000000000011E8                 db  1Eh
.rodata:00000000000011E9                 db  9Bh
.rodata:00000000000011EA                 db  8Bh
.rodata:00000000000011EB                 db  4Fh ; O
.rodata:00000000000011EC                 db 0F5h
.rodata:00000000000011ED                 db    4
.rodata:00000000000011EE                 db  5Eh ; ^
.rodata:00000000000011EF                 db  81h
.rodata:00000000000011F0                 db 0DAh
.rodata:00000000000011F1                 db  69h ; i
.rodata:00000000000011F2                 db 0DBh
.rodata:00000000000011F3                 db  91h
.rodata:00000000000011F4                 db  7Eh ; ~
.rodata:00000000000011F5                 db  0Fh
.rodata:00000000000011F6                 db  96h
.rodata:00000000000011F7                 db  69h ; i
.rodata:00000000000011F8                 db 0A1h
.rodata:00000000000011F9                 db  51h ; Q
.rodata:00000000000011FA                 db  93h
.rodata:00000000000011FB                 db 0B3h
.rodata:00000000000011FC                 db  50h ; P
.rodata:00000000000011FD                 db 0F4h
.rodata:00000000000011FE                 db  84h
.rodata:00000000000011FF                 db  10h
.rodata:0000000000001200                 db 0D8h
.rodata:0000000000001201                 db  49h ; I
.rodata:0000000000001202                 db  24h ; $
.rodata:0000000000001203                 db 0C6h
.rodata:0000000000001204                 db 0B0h
.rodata:0000000000001205                 db  51h ; Q
.rodata:0000000000001206                 db  2Bh ; +
.rodata:0000000000001207                 db 0BCh
.rodata:0000000000001208                 db  7Ah ; z
.rodata:0000000000001209                 db 0E0h
.rodata:000000000000120A                 db  26h ; &
.rodata:000000000000120B                 db 0DFh
.rodata:000000000000120C                 db  42h ; B
.rodata:000000000000120D                 db 0EFh
.rodata:000000000000120E                 db 0BBh
.rodata:000000000000120F                 db  9Bh
.rodata:0000000000001210                 db  57h ; W
.rodata:0000000000001211                 db 0E2h
.rodata:0000000000001212                 db 0DDh
.rodata:0000000000001213                 db    2
.rodata:0000000000001214                 db  41h ; A
.rodata:0000000000001215                 db    0
.rodata:0000000000001216                 db 0D9h
.rodata:0000000000001217                 db  8Bh
.rodata:0000000000001218                 db  83h
.rodata:0000000000001219                 db 0A9h
.rodata:000000000000121A                 db 0F6h
.rodata:000000000000121B                 db 0BDh
.rodata:000000000000121C                 db  94h
.rodata:000000000000121D                 db 0CCh
.rodata:000000000000121E                 db 0EFh
.rodata:000000000000121F                 db  93h
.rodata:0000000000001220                 db  34h ; 4
.rodata:0000000000001221                 db  5Ah ; Z
.rodata:0000000000001222                 db  35h ; 5
.rodata:0000000000001223                 db 0EEh
.rodata:0000000000001224                 db  8Bh
.rodata:0000000000001225                 db 0B3h
.rodata:0000000000001226                 db  4Eh ; N
.rodata:0000000000001227                 db  32h ; 2
.rodata:0000000000001228                 db  41h ; A
.rodata:0000000000001229                 db  7Ch ; |
.rodata:000000000000122A                 db 0C6h
.rodata:000000000000122B                 db  9Ch
.rodata:000000000000122C                 db  2Ah ; *
.rodata:000000000000122D                 db  5Eh ; ^
.rodata:000000000000122E                 db 0F0h
.rodata:000000000000122F                 db  97h
.rodata:0000000000001230                 db 0C2h
.rodata:0000000000001231                 db  45h ; E
.rodata:0000000000001232                 db  3Dh ; =
.rodata:0000000000001233                 db  8Fh
.rodata:0000000000001234                 db  68h ; h
.rodata:0000000000001235                 db  1Eh
.rodata:0000000000001236                 db  34h ; 4
.rodata:0000000000001237                 db 0B7h
.rodata:0000000000001238                 db 0B0h
.rodata:0000000000001239                 db  5Fh ; _
.rodata:000000000000123A                 db 0AFh
.rodata:000000000000123B                 db  5Eh ; ^
.rodata:000000000000123C                 db  9Eh
.rodata:000000000000123D                 db 0FDh
.rodata:000000000000123E                 db  41h ; A
.rodata:000000000000123F                 db 0B8h
.rodata:0000000000001240                 db 0EEh
.rodata:0000000000001241                 db  5Ch ;
.rodata:0000000000001242                 db  8Bh
.rodata:0000000000001243                 db  5Ah ; Z
.rodata:0000000000001244                 db 0CAh
.rodata:0000000000001245                 db  4Eh ; N
.rodata:0000000000001246                 db 0B7h
.rodata:0000000000001247                 db  51h ; Q
.rodata:0000000000001248                 db  7Ah ; z
.rodata:0000000000001249                 db 0DEh
.rodata:000000000000124A                 db  57h ; W
.rodata:000000000000124B                 db  21h ; !
.rodata:000000000000124C                 db  37h ; 7
.rodata:000000000000124D                 db 0AAh
.rodata:000000000000124E                 db  40h ; @
.rodata:000000000000124F                 db  9Eh
.rodata:0000000000001250                 db  23h ; #
.rodata:0000000000001251                 db  0Ah
.rodata:0000000000001252                 db  51h ; Q
.rodata:0000000000001253                 db  1Dh
.rodata:0000000000001254                 db 0EDh
.rodata:0000000000001255                 db  6Bh ; k
.rodata:0000000000001256                 db    2
.rodata:0000000000001257                 db  41h ; A
.rodata:0000000000001258                 db    0
.rodata:0000000000001259                 db 0CDh
.rodata:000000000000125A                 db  3Ch ; <
.rodata:000000000000125B                 db 0CBh
.rodata:000000000000125C                 db  39h ; 9
.rodata:000000000000125D                 db  7Eh ; ~
.rodata:000000000000125E                 db 0CEh
.rodata:000000000000125F                 db 0DFh
.rodata:0000000000001260                 db  9Fh
.rodata:0000000000001261                 db 0D2h
.rodata:0000000000001262                 db 0C8h
.rodata:0000000000001263                 db  67h ; g
.rodata:0000000000001264                 db  9Dh
.rodata:0000000000001265                 db  64h ; d
.rodata:0000000000001266                 db  86h
.rodata:0000000000001267                 db  22h ; "
.rodata:0000000000001268                 db 0D3h
.rodata:0000000000001269                 db 0E5h
.rodata:000000000000126A                 db 0BCh
.rodata:000000000000126B                 db  3Fh ; ?
.rodata:000000000000126C                 db  0Ah
.rodata:000000000000126D                 db  33h ; 3
.rodata:000000000000126E                 db  32h ; 2
.rodata:000000000000126F                 db 0B8h
.rodata:0000000000001270                 db 0E0h
.rodata:0000000000001271                 db  3Fh ; ?
.rodata:0000000000001272                 db 0DCh
.rodata:0000000000001273                 db 0A0h
.rodata:0000000000001274                 db  7Fh ; 
.rodata:0000000000001275                 db 0E6h
.rodata:0000000000001276                 db 0A6h
.rodata:0000000000001277                 db 0FCh
.rodata:0000000000001278                 db  87h
.rodata:0000000000001279                 db 0DFh
.rodata:000000000000127A                 db  4Eh ; N
.rodata:000000000000127B                 db  86h
.rodata:000000000000127C                 db  80h
.rodata:000000000000127D                 db  81h
.rodata:000000000000127E                 db  3Ah ; :
.rodata:000000000000127F                 db 0E4h
.rodata:0000000000001280                 db 0E0h
.rodata:0000000000001281                 db  5Eh ; ^
.rodata:0000000000001282                 db 0E1h
.rodata:0000000000001283                 db  41h ; A
.rodata:0000000000001284                 db  1Ah
.rodata:0000000000001285                 db 0D0h
.rodata:0000000000001286                 db 0F4h
.rodata:0000000000001287                 db 0B8h
.rodata:0000000000001288                 db 0C2h
.rodata:0000000000001289                 db  4Eh ; N
.rodata:000000000000128A                 db    0
.rodata:000000000000128B                 db  91h
.rodata:000000000000128C                 db  9Ah
.rodata:000000000000128D                 db  1Ah
.rodata:000000000000128E                 db 0F0h
.rodata:000000000000128F                 db  1Eh
.rodata:0000000000001290                 db  38h ; 8
.rodata:0000000000001291                 db  9Fh
.rodata:0000000000001292                 db 0CAh
.rodata:0000000000001293                 db  55h ; U
.rodata:0000000000001294                 db 0E2h
.rodata:0000000000001295                 db 0A3h
.rodata:0000000000001296                 db  2Dh ; -
.rodata:0000000000001297                 db 0CDh
.rodata:0000000000001298                 db 0B7h
.rodata:0000000000001299                 db    2
.rodata:000000000000129A                 db  41h ; A
.rodata:000000000000129B                 db    0
.rodata:000000000000129C                 db  81h
.rodata:000000000000129D                 db  29h ; )
.rodata:000000000000129E                 db  7Bh ; {
.rodata:000000000000129F                 db  77h ; w
.rodata:00000000000012A0                 db 0EBh
.rodata:00000000000012A1                 db  5Eh ; ^
.rodata:00000000000012A2                 db 0AEh
.rodata:00000000000012A3                 db  3Dh ; =
.rodata:00000000000012A4                 db  6Bh ; k
.rodata:00000000000012A5                 db  35h ; 5
.rodata:00000000000012A6                 db  0Ch
.rodata:00000000000012A7                 db  4Dh ; M
.rodata:00000000000012A8                 db  4Fh ; O
.rodata:00000000000012A9                 db  5Eh ; ^
.rodata:00000000000012AA                 db  1Dh
.rodata:00000000000012AB                 db 0A5h
.rodata:00000000000012AC                 db 0CDh
.rodata:00000000000012AD                 db  14h
.rodata:00000000000012AE                 db 0BBh
.rodata:00000000000012AF                 db  9Bh
.rodata:00000000000012B0                 db  18h
.rodata:00000000000012B1                 db 0D4h
.rodata:00000000000012B2                 db 0D9h
.rodata:00000000000012B3                 db 0B7h
.rodata:00000000000012B4                 db  5Ah ; Z
.rodata:00000000000012B5                 db 0C3h
.rodata:00000000000012B6                 db 0CFh
.rodata:00000000000012B7                 db 0FDh
.rodata:00000000000012B8                 db  8Ah
.rodata:00000000000012B9                 db  4Ah ; J
.rodata:00000000000012BA                 db  5Dh ; ]
.rodata:00000000000012BB                 db 0F8h
.rodata:00000000000012BC                 db  29h ; )
.rodata:00000000000012BD                 db  36h ; 6
.rodata:00000000000012BE                 db 0B2h
.rodata:00000000000012BF                 db 0CAh
.rodata:00000000000012C0                 db  6Ch ; l
.rodata:00000000000012C1                 db 0F6h
.rodata:00000000000012C2                 db  12h
.rodata:00000000000012C3                 db  11h
.rodata:00000000000012C4                 db 0ADh
.rodata:00000000000012C5                 db 0F6h
.rodata:00000000000012C6                 db 0DDh
.rodata:00000000000012C7                 db 0D7h
.rodata:00000000000012C8                 db  26h ; &
.rodata:00000000000012C9                 db  8Ah
.rodata:00000000000012CA                 db  36h ; 6
.rodata:00000000000012CB                 db  39h ; 9
.rodata:00000000000012CC                 db 0BCh
.rodata:00000000000012CD                 db  4Fh ; O
.rodata:00000000000012CE                 db 0EDh
.rodata:00000000000012CF                 db  52h ; R
.rodata:00000000000012D0                 db  9Bh
.rodata:00000000000012D1                 db  8Ah
.rodata:00000000000012D2                 db 0C6h
.rodata:00000000000012D3                 db  61h ; a
.rodata:00000000000012D4                 db  18h
.rodata:00000000000012D5                 db  52h ; R
.rodata:00000000000012D6                 db  8Bh
.rodata:00000000000012D7                 db 0DDh
.rodata:00000000000012D8                 db  71h ; q
.rodata:00000000000012D9                 db  42h ; B
.rodata:00000000000012DA                 db    2
.rodata:00000000000012DB                 db  97h
.rodata:00000000000012DC                 db    2
.rodata:00000000000012DD                 db  40h ; @
.rodata:00000000000012DE                 db  12h
.rodata:00000000000012DF                 db 0ADh
.rodata:00000000000012E0                 db  51h ; Q
.rodata:00000000000012E1                 db 0A1h
.rodata:00000000000012E2                 db  2Dh ; -
.rodata:00000000000012E3                 db 0D5h
.rodata:00000000000012E4                 db  0Dh
.rodata:00000000000012E5                 db 0ACh
.rodata:00000000000012E6                 db 0B1h
.rodata:00000000000012E7                 db 0B5h
.rodata:00000000000012E8                 db 0E3h
.rodata:00000000000012E9                 db  18h
.rodata:00000000000012EA                 db    3
.rodata:00000000000012EB                 db 0A9h
.rodata:00000000000012EC                 db 0E1h
.rodata:00000000000012ED                 db  49h ; I
.rodata:00000000000012EE                 db  7Fh ; 
.rodata:00000000000012EF                 db  42h ; B
.rodata:00000000000012F0                 db  9Eh
.rodata:00000000000012F1                 db  4Ah ; J
.rodata:00000000000012F2                 db    3
.rodata:00000000000012F3                 db  56h ; V
.rodata:00000000000012F4                 db 0BEh
.rodata:00000000000012F5                 db  54h ; T
.rodata:00000000000012F6                 db  49h ; I
.rodata:00000000000012F7                 db 0FBh
.rodata:00000000000012F8                 db  7Dh ; }
.rodata:00000000000012F9                 db 0EFh
.rodata:00000000000012FA                 db 0A5h
.rodata:00000000000012FB                 db 0C1h
.rodata:00000000000012FC                 db 0D4h
.rodata:00000000000012FD                 db  81h
.rodata:00000000000012FE                 db  58h ; X
.rodata:00000000000012FF                 db 0E5h
.rodata:0000000000001300                 db    0
.rodata:0000000000001301                 db  80h
.rodata:0000000000001302                 db  79h ; y
.rodata:0000000000001303                 db  42h ; B
.rodata:0000000000001304                 db  2Eh ; .
.rodata:0000000000001305                 db 0C9h
.rodata:0000000000001306                 db 0ECh
.rodata:0000000000001307                 db  58h ; X
.rodata:0000000000001308                 db  7Bh ; {
.rodata:0000000000001309                 db  60h ; `
.rodata:000000000000130A                 db  41h ; A
.rodata:000000000000130B                 db  5Bh ; [
.rodata:000000000000130C                 db 0C3h
.rodata:000000000000130D                 db 0E4h
.rodata:000000000000130E                 db  8Ah
.rodata:000000000000130F                 db 0CCh
.rodata:0000000000001310                 db 0AAh
.rodata:0000000000001311                 db  73h ; s
.rodata:0000000000001312                 db  67h ; g
.rodata:0000000000001313                 db 0B8h
.rodata:0000000000001314                 db  2Ah ; *
.rodata:0000000000001315                 db  47h ; G
.rodata:0000000000001316                 db 0E4h
.rodata:0000000000001317                 db 0E2h
.rodata:0000000000001318                 db 0B8h
.rodata:0000000000001319                 db 0E6h
.rodata:000000000000131A                 db  23h ; #
.rodata:000000000000131B                 db  0Bh
.rodata:000000000000131C                 db  6Ch ; l
.rodata:000000000000131D                 db    9
.rodata:000000000000131E                 db    2
.rodata:000000000000131F                 db  40h ; @
.rodata:0000000000001320                 db  3Eh ; >
.rodata:0000000000001321                 db  76h ; v
.rodata:0000000000001322                 db  64h ; d
.rodata:0000000000001323                 db  63h ; c
.rodata:0000000000001324                 db 0D4h
.rodata:0000000000001325                 db  83h
.rodata:0000000000001326                 db 0B0h
.rodata:0000000000001327                 db  0Eh
.rodata:0000000000001328                 db  62h ; b
.rodata:0000000000001329                 db  46h ; F
.rodata:000000000000132A                 db 0B8h
.rodata:000000000000132B                 db  1Fh
.rodata:000000000000132C                 db  0Dh
.rodata:000000000000132D                 db 0E3h
.rodata:000000000000132E                 db  30h ; 0
.rodata:000000000000132F                 db  3Eh ; >
.rodata:0000000000001330                 db 0E9h
.rodata:0000000000001331                 db  16h
.rodata:0000000000001332                 db  40h ; @
.rodata:0000000000001333                 db  79h ; y
.rodata:0000000000001334                 db  8Fh
.rodata:0000000000001335                 db  8Ah
.rodata:0000000000001336                 db  77h ; w
.rodata:0000000000001337                 db  30h ; 0
.rodata:0000000000001338                 db  66h ; f
.rodata:0000000000001339                 db 0AEh
.rodata:000000000000133A                 db  25h ; %
.rodata:000000000000133B                 db 0E6h
.rodata:000000000000133C                 db 0C3h
.rodata:000000000000133D                 db  3Bh ; ;
.rodata:000000000000133E                 db  75h ; u
.rodata:000000000000133F                 db  7Eh ; ~
.rodata:0000000000001340                 db 0ABh
.rodata:0000000000001341                 db  7Eh ; ~
.rodata:0000000000001342                 db 0FFh
.rodata:0000000000001343                 db  4Ah ; J
.rodata:0000000000001344                 db    9
.rodata:0000000000001345                 db 0E0h
.rodata:0000000000001346                 db  38h ; 8
.rodata:0000000000001347                 db 0ECh
.rodata:0000000000001348                 db 0B6h
.rodata:0000000000001349                 db  5Dh ; ]
.rodata:000000000000134A                 db 0EBh
.rodata:000000000000134B                 db 0B3h
.rodata:000000000000134C                 db  85h
.rodata:000000000000134D                 db  59h ; Y
.rodata:000000000000134E                 db 0C0h
.rodata:000000000000134F                 db  6Dh ; m
.rodata:0000000000001350                 db  55h ; U
.rodata:0000000000001351                 db  4Eh ; N
.rodata:0000000000001352                 db 0A8h
.rodata:0000000000001353                 db    5
.rodata:0000000000001354                 db 0C3h
.rodata:0000000000001355                 db  71h ; q
.rodata:0000000000001356                 db 0EFh    
.rodata:0000000000001357                 db  60h ; `
.rodata:0000000000001358                 db  18h
.rodata:0000000000001359                 db 0DBh
.rodata:000000000000135A                 db  2Bh ; +
.rodata:000000000000135B                 db  6Dh ; m
.rodata:000000000000135C                 db 0CCh
.rodata:000000000000135D                 db  1Eh
.rodata:000000000000135E                 db  92h
.rodata:000000000000135F                 db 0FCh
"""

data = map(lambda x: int(x.split()[2].replace('h',''),16), list(data.split('\n'))[:-1])
key = RSA.importKey(bytearray(bytes(data)))

msg = """  msg[0] = 111;
  msg[1] = -122;
  msg[2] = -28;
  msg[3] = -106;
  msg[4] = 41;
  msg[5] = -66;
  msg[6] = -118;
  msg[7] = 94;
  msg[8] = 33;
  msg[9] = -30;
  msg[10] = -64;
  msg[11] = -38;
  msg[12] = 37;
  msg[13] = -73;
  msg[14] = -107;
  msg[15] = -32;
  msg[16] = 95;
  msg[17] = 10;
  msg[18] = 108;
  msg[19] = -23;
  msg[20] = 68;
  msg[21] = -37;
  msg[22] = 18;
  msg[23] = 76;
  msg[24] = 58;
  msg[25] = 108;
  msg[26] = 20;
  msg[27] = -121;
  msg[28] = -58;
  msg[29] = 54;
  msg[30] = 107;
  msg[31] = 109;
  msg[32] = -107;
  msg[33] = 6;
  msg[34] = 28;
  msg[35] = 45;
  msg[36] = 17;
  msg[37] = -98;
  msg[38] = -8;
  msg[39] = 114;
  msg[40] = -52;
  msg[41] = -101;
  msg[42] = 116;
  msg[43] = -121;
  msg[44] = 115;
  msg[45] = -89;
  msg[46] = 82;
  msg[47] = 114;
  msg[48] = 12;
  msg[49] = 91;
  msg[50] = 146;
  msg[51] = 141;
  msg[52] = 124;
  msg[53] = -87;
  msg[54] = 53;
  msg[55] = -21;
  msg[56] = -59;
  msg[57] = -42;
  msg[58] = 30;
  msg[59] = 28;
  msg[60] = -98;
  msg[61] = 126;
  msg[62] = -45;
  msg[63] = 110;
  msg[64] = 67;
  msg[65] = 53;
  msg[66] = -109;
  msg[67] = -48;
  msg[68] = 108;
  msg[69] = 38;
  msg[70] = -76;
  msg[71] = -107;
  msg[72] = -27;
  msg[73] = -103;
  msg[74] = 40;
  msg[75] = 99;
  msg[76] = 94;
  msg[77] = -21;
  msg[78] = -83;
  msg[79] = 64;
  msg[80] = -50;
  msg[81] = 38;
  msg[82] = 103;
  msg[83] = -9;
  msg[84] = 50;
  msg[85] = -78;
  msg[86] = 3;
  msg[87] = 13;
  msg[88] = 48;
  msg[89] = 36;
  msg[90] = -109;
  msg[91] = -124;
  msg[92] = 58;
  msg[93] = 25;
  msg[94] = -84;
  msg[95] = 111;
  msg[96] = 17;
  msg[97] = -69;
  msg[98] = 11;
  msg[99] = 91;
  msg[100] = 65;
  msg[101] = -115;
  msg[102] = -99;
  msg[103] = 73;
  msg[104] = 26;
  msg[105] = -79;
  msg[106] = 33;
  msg[107] = -39;
  msg[108] = 121;
  msg[109] = 67;
  msg[110] = -68;
  msg[111] = -125;
  msg[112] = 28;
  msg[113] = 54;
  msg[114] = -104;
  msg[115] = -71;
  msg[116] = 90;
  msg[117] = 83;
  msg[118] = -39;
  msg[119] = -12;
  msg[120] = -93;
  msg[121] = -103;
  msg[122] = 52;
  msg[123] = 103;
  msg[124] = -94;
  msg[125] = -117;
  msg[126] = -50;
  msg[127] = 6;""".split('\n')

msg = list(map(lambda x: int(x.split()[2][:-1]) & 0xff, msg))
msg = int.from_bytes(bytes(bytearray(msg)),'big')
print(long_to_bytes(pow(msg, key.e, key.n)))
