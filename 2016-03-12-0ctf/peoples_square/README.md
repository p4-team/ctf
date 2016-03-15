## People's Square (Crypto 6p)

	People's Square (A.K.A. shenmhin guangshan in Shanghai Dialect) 
	is a large public square in the Huangpu District of Shanghai, 
	China.
	We know Talent Yang is the king of People's Square. Now he 
	provides you a strange guessing game, and he also demonstrates 
	his talent by giving you the result of how he tackles this task. 
	Can you show your talent to decrypt the secret?	

###ENG
[PL](#pl-version)

###PL version

Najpierw analizujemy binarkę którą dostajemy w zadaniu. Coprawda nie działała ona na większości naszych komputerów za bardzo
(nie wszyscy mamy najnowsze laptopy), udało nam się ją zdekompilować.

Dekompilacja to dopiero pierwszy krok analizy, ponieważ jak to z automatyczną dekompilacją zawsze - kod był bardzo nieczytelny.
Ciężko o analizę z funkcjami takimi jak taka:

```cpp
const __m128i *__fastcall sub_4013C5(const __m128i *a1, __int64 a2)
{
  __m128i v2; // xmm0@1
  __m128i v3; // xmm0@2
  __m128i v6; // xmm0@4
  const __m128i *result; // rax@4
  signed __int64 i; // [sp+18h] [bp-98h]@1
  __int128 v11; // [sp+30h] [bp-80h]@1
  __int128 v12; // [sp+40h] [bp-70h]@1
  __int128 v13; // [sp+50h] [bp-60h]@1
  __int128 v14; // [sp+60h] [bp-50h]@2
  __int128 v15; // [sp+70h] [bp-40h]@2
  __int128 v16; // [sp+80h] [bp-30h]@4
  __int128 v17; // [sp+90h] [bp-20h]@4
  __int128 v18; // [sp+A0h] [bp-10h]@4

  v2 = _mm_load_si128((const __m128i *)a2);
  _mm_store_si128((__m128i *)&v12, _mm_loadu_si128(a1));
  _mm_store_si128((__m128i *)&v13, v2);
  _mm_store_si128(
    (__m128i *)&v11,
    _mm_xor_si128(_mm_load_si128((const __m128i *)&v13), _mm_load_si128((const __m128i *)&v12)));
  for ( i = 1LL; (unsigned __int64)i <= 3; ++i )
  {
    v3 = _mm_load_si128((const __m128i *)(16 * i + a2));
    _mm_store_si128((__m128i *)&v14, _mm_load_si128((const __m128i *)&v11));
    _mm_store_si128((__m128i *)&v15, v3);
    _XMM0 = _mm_load_si128((const __m128i *)&v14);
    __asm { aesenc  xmm0, [rbp+var_40] }
    _mm_store_si128((__m128i *)&v11, _XMM0);
  }
  v6 = _mm_load_si128((const __m128i *)(a2 + 64));
  _mm_store_si128((__m128i *)&v16, _mm_load_si128((const __m128i *)&v11));
  _mm_store_si128((__m128i *)&v17, v6);
  _XMM0 = _mm_load_si128((const __m128i *)&v16);
  __asm { aesenclast xmm0, [rbp+var_20] }
  _mm_store_si128((__m128i *)&v11, _XMM0);
  _mm_store_si128((__m128i *)&v18, _mm_load_si128((const __m128i *)&v11));
  result = a1;
  _mm_storeu_si128((__m128i *)a1, _mm_load_si128((const __m128i *)&v18));
  return result;
}
```

Zaczęliśmy od doprowadzania go do sensownej postaci
(ręcznie refaktoryzując dostarczony kod):

```cpp
__int64 realMain()
{
  char keyProbably;
  char ciphertextFor0[16];
  char ciphertextFor1[16];
  __int64 v14 = 0LL;
  __int64 v16 = 0LL;
  sub_400ABE(&v14); // put encrypted flag into buffer
  __int64 v10 = 0LL;
  sub_400A74(&v10);
  generateKey((const __m128i *)&v10, (__int64)&keyProbably);
  __int64 v6 = 0LL;
  __int64 initTime = time(0LL);
  for (__int64 i = 0LL; i <= 0x3FF; i++)
  {
    memsetAndEncrypt((__int64)&keyProbably, &ciphertextFor0, &ciphertextFor1, i, initTime);
    unsigned int v5 = rand() & 1;
    char *v1;
    if (v5) {
      v1 = &ciphertextFor0;
    } else {
      v1 = &ciphertextFor1;
    } 
    hexdump((__int64)v1, 0x10);
    puts("0 or 1?");
    user_bit = getchar() - 48;
    puts("ciphertext for 0 is: ");
    hexdump(&ciphertextFor0, 0x10);
    puts("ciphertext for 1 is: ");
    hexdump(&ciphertextFor1, 0x10);
    if ( user_bit == v5 )
    {
      puts("Correct!");
      ++v6;
    }
    else
    {
      puts("Incorrect!");
    }
  }
  if ( v6 == 1024 )
  {
    puts("Now I will give you the flag:");
    realEncrypt((const __m128i *)&v14, (__int64)&keyProbably); // decrypt flag
    realEncrypt((const __m128i *)&v16, (__int64)&keyProbably);
    hexdump((__int64)&v14, 0x20uLL);
  }
  return 0;
}

void memsetAndEncrypt(__int64 keyProbably, char ciphertext0[16], char ciphertext1[16], __int64 iter, __int64 initTime)
{
  memset(ciphertext0, 0, 0x10uLL);
  memset(ciphertext1, 1, 0x10uLL);
  memcpy((char *)ciphertext0 + 8,  &iter,     4uLL);
  memcpy((char *)ciphertext1 + 8,  &iter,     4uLL);
  memcpy((char *)ciphertext0 + 12, &initTime, 4uLL);
  memcpy((char *)ciphertext1 + 12, &initTime, 4uLL);
  realEncrypt((const __m128i *)ciphertext0, keyProbably);
  realEncrypt((const __m128i *)ciphertext1, keyProbably);
}

void realEncrypt(__m128i *a1, __m128i *key)
{
  __int128 state;

  *state = a1 ^ key[0];
  for (int i = 1LL; i <= 3; ++i) {
    *state = aesenc(state, key[i];
  }
  *a1 = aesenclast(state, key[4]);
}
```

W porównaniu do poprzedniego - 100 razy czytelniejsze (np. wklejona poprzednio funkcja przed refaktoryzacją to "realEncrypt" - skróciła się do 4 linijek!

Jak widać - cały ten program to po prostu AES szyfrujący jakieś dane. RealEncrypt to dokładnie implementacja "prawdziwego" AESa, ale zamiast pełnej liczby rund są tylko 4 (co pozwoli na nasz atak, swoją drogą).

Konkretnie, w pseudokodzie działanie programu można przedstawić tak:

```cpp
uint32_t initTime = time()

for (uint32_t i = 0; i < 1024; i++) {
    // 16 byte array: [ 8 ones ] [ i (4 bytes) ] [ initTime (4 bytes) ]
    uint8_t ones[16];
    memset(ones, 0, 16);
    memcpy(ones + 8, &i, 4);
    memcpy(ones + 12, &initTime, 4);

    // 16 byte array: [ 8 zeroes ] [ i (4 bytes) ] [ initTime (4 bytes) ]
    uint8_t zeroes[16];
    memset(zeroes, 0, 16);
    memcpy(zeroes + 8, &i, 4);
    memcpy(zeroes + 12, &initTime, 4);

    bool bit = rand() % 2;
    if (bit == 0) {
        print(encrypt(zeroes));
    } else {
        print(encrypt(zeroes));
    }
    
    print("guess?");
    bool guess = read();
    if (guess == bit) {
        goodGuesses++;
    }

    print(zeroes);
    print(ones);
}

if (goodGuesses == 1024) {
    print("you won");
    print encrypt(encryptedFlag); // will actually decrypt flag for us
}
```

Gdzie encrypt jest naszym zmodyfikowanym, czterorundowym AESem.

Jak się zabrać za taki atak? Otóż, możemy wykorzystać znaną technikę ataku kryptograficznego, czyli `square attack` albo `integral cryptanalysis`.

Żeby zrozumieć w jaki sposób ten atak będzie działać, trzeba najpierw wiedzieć (chociaż mniej-więcej) jak działa AES.

Otóż, AES działa na blokach rozmiaru 128 bitów (albo 192, albo 256, ale w naszym przypadku 128) traktowanych jako tablica 4x4 bajty, i robi na nich pewne operacje.

Te operacje to:

SubBytes - każdy bajt w macierzy jest zamieniany na inny wybrany bajt, korzystając z tablicy asocjacyjnej (tzw. substitution box). Czyli z macierzy:

    in_matrix:
     1  2  3  4
     6  7  8  5
    11 12  9 10
    16 13 14 15

robi się:

    out_matrix:
     S[1]  S[2]  S[3]  S[4]
     S[6]  S[7]  S[8]  S[5]
    S[11] S[12]  S[9] S[10]
    S[16] S[13] S[14] S[15]

ShiftRows - macierz jest przesuwana w wierszach. Czyli z macierzy:

    in_matrix:
     1  2  3  4
     5  6  7  8
     9 10 11 12
    13 14 15 16

robi się

    out_matrix:
     1  2  3  4
     6  7  8  5
    11 12  9 10
    16 13 14 15

MixColumns - wartości macierzy w kolumnach są mieszane (konkretnie, mnożone przez pewien wielomian w skończonym polu).
Ważne jest to, że ostateczne wartości w polu zależą tylko od innych pól w tej kolumnie:

    in_matrix:
    A  E  I  M
    B  F  J  N
    C  G  K  O
    D  H  L  P

    nA, nB, nC, nD = mix(A, B, C, D)
    nE, nF, nG, nH = mix(E, F, G, H)
    nI, nJ, nK, nL = mix(I, J, K, L)
    nM, nN, nO, nP = mix(M, N, O, P)

    out_matrix:
    nA nE nI nM
    nB nF nJ nN
    nC nG nK nO
    nD nH nL nP

AddRoundKey - każda wartość w macierzy jest xorowana z wartością z klucza rundy (round key)

    in_matrix:
    A  E  I  M
    B  F  J  N
    C  G  K  O
    D  H  L  P

    round_key:
    R0 R1 R2 R3
    R4 R5 R6 R7
    R8 R9 RA RB
    RC RD RE RF

    out_matrix:
    A^R0  E^R1  I^R2  M^R3
    B^R4  F^R5  J^R6  N^R7
    C^R8  G^R9  K^RA  O^RB
    D^RC  H^RD  L^RE  P^RF
    
Po co ten cały wstęp? Bo teraz przejdźmy do ataku właściwego.

Załóżmy, że możemy uzyskać ciphertexty dla 256 wybranych plaintextów - w taki sposób tak, że wszystkie bajty są stałe, poza jednym, który przyjmuje po kolei wszystkie możliwe wartości.

00 00 00 00 00 ... 00
01 00 00 00 00 ... 00
02 00 00 00 00 ... 00
03 00 00 00 00 ... 00
04 00 00 00 00 ... 00
..
FE 00 00 00 00 ... 00
FF 00 00 00 00 ... 00

Wtedy przy szyfrowaniu stan AES przyjmie takie wartości:

    X   C   C   C
    C   C   C   C
    C   C   C   C
    C   C   C   C

Gdzie C oznacza bajty które są stałe na danej pozycji dla każdego plaintextu, a X oznacza że bajt przyjmuje wszystkie możliwe wartości (od 0 do 255).
Co to dokładnie znaczy, będzie widoczne zaraz:


Początkowa wartość:

    X   C   C   C
    C   C   C   C
    C   C   C   C
    C   C   C   C

Po SubBytes:

    X   C   C   C
    C   C   C   C
    C   C   C   C
    C   C   C   C

No tak, wszystkie 'C' zostaną zamienione na tą samą wartość (więc dalej będą stałe). Co dalej?

Po ShiftRows:

    X   C   C   C
    C   C   C   C
    C   C   C   C
    C   C   C   C

Nic nie zostało przesunięte.

Po MixColumns:

    X   C   C   C
    X   C   C   C
    X   C   C   C
    X   C   C   C

Tutaj już wartości C nie będą de facto takie same, ale będą takie same dla każdego z 256 testowanych plaintextów na odpowiadających pozycjach - a to sie liczy.
Tak samo, bajty oznaczone jako X będą znowu przyjmowały wszystkie możliwe wartości (czyli np. pierwszy bajt w drugim wierszu przyjmie wartość 1 dokładnie dla
1 szyfrowanego plaintextu, wartość 2 dokładnie dla 1 szyfrowanego plaintextu, itd)

Po AddKey:

    X   C   C   C
    X   C   C   C
    X   C   C   C
    X   C   C   C

Następnie druga runda:

Po SubBytes:

    X   C   C   C
    X   C   C   C
    X   C   C   C
    X   C   C   C

Po ShiftRows:

    X   C   C   C
    C   C   C   X
    C   C   X   C
    C   X   C   C

Po MixColumns:

    X   X   X   X
    X   X   X   X
    X   X   X   X
    X   X   X   X

Po AddKey:

    X   X   X   X
    X   X   X   X
    X   X   X   X
    X   X   X   X

Uwaga, co się teraz stało? Wszystkie elementy klucza przyjmują wszystkie możliwe wartości!

Co to oznacza? Otóż uwaga - jeśli ustalimy dowolną pozycję stanu (np. 2 wiersz i 2 kolumna) i zrobimy:
(State_xx oznacza stan dla szyfrowania plaintextu mającego bajt xx na zmiennej pozycji na początku)

    state_01[2][2] ^ state_02[2][2] ^ state03_[2][2] ^ ... ^ stateFF[2][2]

To wynik zawsze wyjdzie równy zero! Bo skoro wiemy na pewno że każdy bajt przyjmuje wszystkie możliwe wartości, to xorujemy (w różnej kolejności) liczby:

    0 ^ 1 ^ 2 ^ 3 ... ^ 0xFE ^ 0xFF

Ok, i co z tego wynika? Nasz AES ma 4 rundy, a nie 3.

Ale możemy *zgadnąć* jeden bajt klucza, żeby *odszyfrować* jeden bajt zaszyfrowanych danych po czwartej rundzie! Z wyprowadzonej przed chwilą zależności
wynika że jeśli zgadniemy ten bajt dobrze, i odszyfrujemy nim wszystkie wybrane plaintexty, to po xorowaniu wszystkich wynikiem będzie zero.

Następnie możemy powtórzyć to 16 razy - dla wszystkich bajtów klucza. Średnio wyjdą dwie dobre wartości (jedna z nich poprawna) dla każdego bajta klucza - to daje nam złożoność ataku 2^16 - o niebo lepiej niż 2^128.

Czy ten atak możemy zastosować w tym zadaniu? Jak najbardziej - jeśli weźmiemy pierwsze 256 plaintextów, zauważymy że wszystkie różnią się tylko na jednym bajcie (tym zależnym od 'i').

Zaimplementujmy go więc w pythonie (implementacja AES pominięta, będzie w pełnym kodzie dostarczonym do zadania)
```python
def integrate(index):
    potential = []

    for candidateByte in range(256):
        sum = 0
        for ciph in ciphertexts:
            oneRoundDecr = backup(ciph, candidateByte, index)  # decrypt one round of one byte
            sum ^= oneRoundDecr     # xor result with sum
        if sum == 0:   # if sum is equal to 0 - candidateByte stays a candidate
            potential.append(candidateByte)
    return potential


from itertools import product
def integral():
    candidates = []
    for i in range(16):
        candidates.append(integrate(i))    # compute all possible candidate bytes for all positions
    print 'candidates', candidates
    for roundKey in product(*candidates):  # check all possibilities
        masterKey = round2master(roundKey)
        plain = ''.join(chr(c) for c in decrypt4rounds(ciphertexts[1], masterKey))
        if '\0\0\0\0' in plain:  # we know that plaintext contains 4 '0' bytes, and it's unlike to be accident
            print 'solved', masterKey
```

Po uruchomieniu kodu dla dostarczonych danych dostajemy taki oto wynik:

    candidates [[95, 246], [246], [1, 99], [78, 187], [123], [106], [98, 223], [96], [211], [44, 63, 102], [192, 234], [167], [9, 135, 234], [36], [146, 166], [107]]
    solved [23, 74, 34, 20, 64, 53, 100, 117, 220, 227, 160, 55, 163, 23, 237, 75]

Świetnie, teraz wystarczy zdeszyfrować flagę (zaszyfrowana flaga jest na samym końcu podanego outputu):

    0CTF{~R0MAN_l0VES_B10CK_C1PHER~}
