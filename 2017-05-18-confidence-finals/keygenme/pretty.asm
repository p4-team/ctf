[BBB] == [ARG]

for MAG, MMM in CONSTS:
    [DDD] = [BBB]
    [EEE] = 0
    [FFF] = [MMM]

    while [FFF] != 0:
        IF [FFF] & 1:
            [HHH] = 0
            [GGG] = [EEE]
            for ECX in range(0x80):
                CF = SHL([GGG; HHH])
                IF CF:
                    continue
                [GGG; HHH] += [0; DDD]

            [EEE] = 0
            for ECX in range(0x100):
                CF = SHL [EEE; GGG; HHH]
                IF NOT CF:
                    IF [EEE] < [MAG]:
                        continue
                [EEE] -= [MAG]

        [HHH] = 0
        [GGG] = [DDD]
        for ECX in range(0x80):
            CF = SHL [GGG; HHH]
            IF CF:
                continue
            [GGG; HHH] += [0; DDD]

        [DDD] = 0
        for ECX in range(0x100):
            CF = SHL [DDD; GGG; HHH]
            IF NOT CF:
                IF [DDD] < [MAG]:
                    continue
            [DDD] -= [MAG]

        SHR [FFF]

    [BBB] = [EEE]

[AAA] = 0
[AAA; BBB] += 0x31337
[CCC] = 0

for ECX in range(0x100):
    CF = SHL [CCC; AAA; BBB]
    IF NOT CF:
        IF [CCC] < [DRG]:
            continue
    [CCC] -= [DRG]

RETURN [CCC] == 0
