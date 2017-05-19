[BBB] == [ARG]

for MAG, MMM in CONSTS:
    [DDD] = [BBB]
    [EEE] = 0
    [FFF] = [MMM]

    while [FFF] != 0:
        IF [FFF] & 1:
            [EEE] = ([DDD] * [EEE]) % [MAG]
        [DDD] = ([DDD] * DDD]) % [MAG]

        SHR [FFF]

    [BBB] = [EEE]

[AAA; BBB] = [0; BBB] + 0x31337
return [AAA; BBB] % DRG == 0
