

s7 = [int(c, 16) for c in open("s7").read().split()]
s17 = [int(c, 16) for c in open("s17").read().split()]
s17 = s17[1::2]

inverse = [0] * 256
for i, j in enumerate(s17):
    inverse[j] = i

print(s7)
print(s17)
print(inverse)

for potential_sum in range(256*len(s7)):
    flag = []
    for ch in s7:
        for i in range(potential_sum):
            ch = inverse[ch]
        flag.append(ch)
    sm = sum(flag)
    if sm == potential_sum:
        print(flag)
    else:
        if potential_sum % 50 == 0:

            print(potential_sum, sm)
