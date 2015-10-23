## XOR Crypter (crypto 200p)

	Description: The state of art on encryption, can you defeat it?
	CjBPewYGc2gdD3RpMRNfdDcQX3UGGmhpBxZhYhFlfQA= 

### PL
[ENG](#eng-version)

Cały kod szyfrujący jest [tutaj](shiftcrypt.py).
Szyfrowanie jest bardzo proste, aż dziwne że zadanie było za 200 punktów. Szyfrowanie polega na podzieleniu wejściowego tekstu na 4 bajtowe kawałki (po dodaniu paddingu jeśli to konieczne, aby rozmiar wejścia był wielokrotnością 4 bajtów), rzutowanie ich na inta a następnie wykonywana jest operacja `X xor X >>16`. Jeśli oznaczymy kolejnymi literami bajty tego inta uzyskujemy: 

`ABCD ^ ABCD >> 16 = ABCD ^ 00AB = (A^0)(B^0)(C^A)(D^B) = AB(C^A)(D^B)`

Jak widać dwa pierwsze bajty są zachowywane bez zmian a dwa pozostałe bajty są xorowane z tymi dwoma niezmienionymi. Wiemy także że xor jest operacją odwracalną i `(A^B)^B = A` możemy więc odwrócić szyfrowanie dwóch ostatnich bajtów xorując je jeszcze raz z pierwszym oraz drugim bajtem (pamiętając przy tym o kolejności bajtów)

```python
data = "CjBPewYGc2gdD3RpMRNfdDcQX3UGGmhpBxZhYhFlfQA="
decoded = base64.b64decode(data)
blocks = struct.unpack("I" * (len(decoded) / 4), decoded)
output = ''
for block in blocks:
	bytes = map(ord, struct.pack("I", block))
	result = [bytes[0] ^ bytes[2], bytes[1] ^ bytes[3],  bytes[2], bytes[3]]
	output += "".join(map(chr, result))
print(output)
```

W wyniku czego uzyskujemy flagę: `EKO{unshifting_the_unshiftable}`

### ENG version


Cipher code is [here](shiftcrypt.py).
The cipher is actually very simple, it was very strange that the task was worth 200 point. The cipher splits the input text in 4 byte blocks (after adding padding if necessary so that the input is a multiply of 4 bytes), casting each block to integer and the performing `X xor X >>16`. If we mark each byte of the single block with consecutive alphabet letters we get:

`ABCD ^ ABCD >> 16 = ABCD ^ 00AB = (A^0)(B^0)(C^A)(D^B) = AB(C^A)(D^B)`

As can be notices, first two bytes are unchanged and last two are xored with those two unchanged. We also know that xor is reversible and `(A^B)^B = A` so we can revert the cipher of the last two bytes by xoring them again with first and second byte (keeping in mind the byte order).

```python
data = "CjBPewYGc2gdD3RpMRNfdDcQX3UGGmhpBxZhYhFlfQA="
decoded = base64.b64decode(data)
blocks = struct.unpack("I" * (len(decoded) / 4), decoded)
output = ''
for block in blocks:
	bytes = map(ord, struct.pack("I", block))
	result = [bytes[0] ^ bytes[2], bytes[1] ^ bytes[3],  bytes[2], bytes[3]]
	output += "".join(map(chr, result))
print(output)
```

As a result we get: `EKO{unshifting_the_unshiftable}`
