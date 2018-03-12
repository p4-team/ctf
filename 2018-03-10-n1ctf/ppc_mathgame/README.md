# Mathgame (PPC, 714p, 9 solved)

This was a very annoying task.
Conceptually it was actually pretty simple, but parsing the input was hard, and then it was randomly failing tests.
The idea was that we have a cube 7x7x7 with numbers on the walls.
There are 7 numbers which doesn't fit somehow.
We need to find them, then connect them via lines, and two of such lines will be perpendicular and cross an internal cube.
The task is to give coordinates of this internal cube.

It was not clear if the cube coordinates are counted from the middle or some other point, and also how to count intersection going through a wall.
There were also test cases which had multiple solutions, or no solutions at all.
Fortunately we had to solve only 5 examples to get the flag, so we simply run this in a loop for a while to get the flag.

The special numbers could be found with rules:
1. even/odd
2. even/odd
3. primes/non-primes
4. primes/non-primes
5. 3 divisors / 2 divisors

The input was in form:

```
=================================================================================
                                Question Five
=================================================================================

                                      A
------------------------------------------------------------------------------

|1328790233|2084499161|0696287693|1660138603|1157298553|2588563183|2357964443|
------------------------------------------------------------------------------
|3726747287|1521033083|3839283769|1661498821|1898692387|3135736403|1658923543|
------------------------------------------------------------------------------
|2326824881|2777671103|3099882481|2279475533|1765911347|2687755193|0339175751|
------------------------------------------------------------------------------
|1490623237|2618039657|1878850373|2081800027|1659998141|0532226311|1513689113|
------------------------------------------------------------------------------
|2003621209|3193816697|2664061769|3118907131|1743603311|1892309323|2909118241|
------------------------------------------------------------------------------
|2090511169|2726139389|2928378703|1563046193|2501788909|3227850023|3516251579|
------------------------------------------------------------------------------
|2331864553|1753491527|2239852117|2874087743|2656404403|2457493267|1891677913|
------------------------------------------------------------------------------

******************************************************************************
                                      B
------------------------------------------------------------------------------
|2357964443|3212428841|0432400201|1580443153|2362281367|2042152669|2248772021|
------------------------------------------------------------------------------
|1658923543|2238017741|2486241403|2087206861|3573698417|1884731227|2660729209|
------------------------------------------------------------------------------
|0339175751|1984116557|3212739667|1630709579|2630303411|1126220239|2723978393|
------------------------------------------------------------------------------
|1513689113|2379249491|2462656099|3278529689|3248454709|2452096897|1989718651|
------------------------------------------------------------------------------
|2909118241|2362922879|2319001897|3664496333|0287807791|2539914877|2944262089|
------------------------------------------------------------------------------
|3516251579|2069603141|2929374769|3001367287|3552535627|1737077239|2920954321|
------------------------------------------------------------------------------
|1891677913|1897008599|1607466241|2258608613|2605621531|2357919709|1621511029|
------------------------------------------------------------------------------

******************************************************************************
                                      C
------------------------------------------------------------------------------
|2248772021|2042152669|2362281367|1580443153|0432400201|3212428841|2357964443|
------------------------------------------------------------------------------
|2556179783|3083582137|2823299807|2982382943|2470982513|3766208269|2588563183|
------------------------------------------------------------------------------
|1279701343|1349891281|1631377337|2223472201|3043595761|3980677397|1157298553|
------------------------------------------------------------------------------
|2519143849|1332811691|3405530693|1462403983|3398349961|1933290613|1660138603|
------------------------------------------------------------------------------
|2881715209|2137626649|3365750909|1639321561|2501250923|1445581847|0696287693|
------------------------------------------------------------------------------
|3143410783|2063116669|3486766021|3058422299|3729039467|2252837863|2084499161|
------------------------------------------------------------------------------
|1338974471|4189292929|1755308323|3608715713|1160079631|3367242341|1328790233|
------------------------------------------------------------------------------

******************************************************************************
                                      D
------------------------------------------------------------------------------
|3235114681|2471203951|2709782587|1933809511|3129277721|2236589099|2331864553|
------------------------------------------------------------------------------
|2084508749|1206882367|1730418379|2182678481|1381552729|3469818697|1753491527|
------------------------------------------------------------------------------
|2832238313|2263125911|0480393457|2030207351|1893967217|2298743639|2239852117|
------------------------------------------------------------------------------
|1605350543|2398724927|2366655829|1861475303|1679976917|1588881649|2874087743|
------------------------------------------------------------------------------
|1949274161|3335731237|1715264021|2556690923|1572620113|1420979311|2656404403|
------------------------------------------------------------------------------
|1904118701|0809915627|1563823619|2756629699|4045257421|1755318067|2457493267|
------------------------------------------------------------------------------
|1621511029|2357919709|2605621531|2258608613|1607466241|1897008599|1891677913|
------------------------------------------------------------------------------

******************************************************************************
                                      E
------------------------------------------------------------------------------
|2248772021|2556179783|1279701343|2519143849|2881715209|3143410783|1338974471|
------------------------------------------------------------------------------
|2660729209|2208808709|2137179923|3467495971|2369408329|1417842847|2856461851|
------------------------------------------------------------------------------
|2723978393|2388231823|2931564319|3317731211|1993509377|2169053221|2057817481|
------------------------------------------------------------------------------
|1989718651|2251635973|1901557607|2165696801|3295570127|2353890053|2191693367|
------------------------------------------------------------------------------
|2944262089|2421919121|2310049853|3799873817|1785808949|2212685389|3431625541|
------------------------------------------------------------------------------
|2920954321|1548928189|1857980479|2371731689|2683816601|2536769041|3050435657|
------------------------------------------------------------------------------
|1621511029|1904118701|1949274161|1605350543|2832238313|2084508749|3235114681|
------------------------------------------------------------------------------

******************************************************************************
                                      F
------------------------------------------------------------------------------
|1338974471|4189292929|1755308323|3608715713|1160079631|3367242341|1328790233|
------------------------------------------------------------------------------
|2856461851|1830343831|2803179479|2540555291|1596370583|2428756193|3726747287|
------------------------------------------------------------------------------
|2057817481|1993397429|2212281713|2762599291|2213126341|2536883941|2326824881|
------------------------------------------------------------------------------
|2191693367|2253085969|2802701081|2338219649|1366065193|2054382947|1490623237|
------------------------------------------------------------------------------
|3431625541|2143610489|3419371091|2646546713|2317498357|2439885193|2003621209|
------------------------------------------------------------------------------
|3050435657|3676301219|3598318393|2810755349|3005050121|2401101617|2090511169|
------------------------------------------------------------------------------
|3235114681|2471203951|2709782587|1933809511|3129277721|2236589099|2331864553|
------------------------------------------------------------------------------

******************************************************************************
Use A to create a coordinate system(z == 0)

6^y
 |
 |
 |         x
 |__________>
0           6
```

The solver code:

```python
import hashlib
import itertools
import re
import string
from gmpy2 import is_prime

import numpy

from crypto_commons.generic import get_primes, factor_p
from crypto_commons.netcat.netcat_commons import nc, receive_until_match, send, interactive


def PoW(challenge):
    data = re.findall('"(.*?)"', challenge)
    prefix = data[0]
    result = data[1]
    for s in itertools.product(string.printable, repeat=4):
        st = "".join(s)
        if hashlib.sha256(prefix + st).hexdigest().startswith(result):
            return st
    return "dupa"


def parse_data(question_data):
    numbers = re.findall('\d+', question_data)
    numbers = map(int, numbers[:-4])

    def chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def find_match(a, b):
        for x1, x2 in enumerate(a):
            for y1, y2 in enumerate(b):
                if x2 == y2:
                    return (x1, y1)
        return None

    DIRECTIONS = {
        0: "UP",
        1: "RIGHT",
        2: "DOWN",
        3: "LEFT"
    }

    sides = chunks(numbers, len(numbers) / 6)

    class Face():

        def __init__(self, cubes):
            print("CONSTRUCTOR")
            self.cubes = list(reversed(list(chunks(cubes, 7))))
            self.hashes = []

            self.position = -1
            self.calculate_hashes()

        def calculate_hashes(self):
            self.hashes = []

            hash_up = 0
            for i in range(7):
                hash_up ^= self.cubes[0][i]

            hash_right = 0
            for i in range(7):
                hash_right ^= self.cubes[i][6]

            hash_down = 0
            for i in range(7):
                hash_down ^= self.cubes[6][i]

            hash_left = 0
            for i in range(7):
                hash_left ^= self.cubes[i][0]

            self.hashes.append(hash_up)
            self.hashes.append(hash_right)
            self.hashes.append(hash_down)
            self.hashes.append(hash_left)

        def turn_clockwise(self):
            print("Turn")
            length = len(self.cubes) - 1

            for i in range(length / 2):
                for j in range(i, length - i):
                    tmp = self.cubes[i][j]

                    self.cubes[i][j] = self.cubes[length - j][i]
                    self.cubes[length - j][i] = self.cubes[length - i][length - j]
                    self.cubes[length - i][length - j] = self.cubes[j][length - i]
                    self.cubes[j][length - i] = tmp

            self.calculate_hashes()

        def print_face(self):
            for i in range(len(self.cubes)):
                print(' '.join([str(x) for x in self.cubes[i]]))
            print()

    faces = []
    for side in sides:
        f = Face(side)
        faces.append(f)

    A = faces[0]
    SIDES = [None] * 4
    TOP = None

    for f in faces[1:]:
        print("new face")
        try:
            a_pos, f_pos = find_match(A.hashes, f.hashes)
            print(DIRECTIONS[a_pos], DIRECTIONS[f_pos])

            SIDES[a_pos] = f

            while a_pos != (f_pos + 2) % 4:
                f.turn_clockwise()
                a_pos, f_pos = find_match(A.hashes, f.hashes)
                print(DIRECTIONS[a_pos], DIRECTIONS[f_pos])

        except TypeError:
            print("bee")
            TOP = f

    # align top
    UP_POS, TOP_pos = find_match(SIDES[0].hashes, TOP.hashes)
    print(DIRECTIONS[UP_POS], DIRECTIONS[TOP_pos])

    while UP_POS != (TOP_pos + 2) % 4:
        TOP.turn_clockwise()
        UP_POS, TOP_pos = find_match(SIDES[0].hashes, TOP.hashes)
        print(DIRECTIONS[UP_POS], DIRECTIONS[TOP_pos])

    cubes = {}

    # process bottom
    BOTTOM = A
    print("Bottom")
    for i in range(7):
        for j in range(7):
            x = i
            y = j
            z = 0

            if (x, y, z) in cubes:
                assert cubes[(x, y, z)] == BOTTOM.cubes[j][i]
            cubes[(x, y, z)] = BOTTOM.cubes[j][i]

    ############################################################

    BACK = SIDES[0]
    print("Front")
    for i in range(7):
        for j in range(7):
            x = i
            y = 0
            z = 6 - j

            if (x, y, z) in cubes:
                assert cubes[(x, y, z)] == BACK.cubes[j][i]
            cubes[(x, y, z)] = BACK.cubes[j][i]

    ############################################################

    RIGHT = SIDES[1]
    print("Right")
    for i in range(7):
        for j in range(7):
            x = 6
            y = j
            z = i

            if (x, y, z) in cubes:
                assert cubes[(x, y, z)] == RIGHT.cubes[j][i]
            cubes[(x, y, z)] = RIGHT.cubes[j][i]

    ############################################################

    FRONT = SIDES[2]
    print("Back")
    for i in range(7):
        for j in range(7):
            x = i
            y = 6
            z = j

            if (x, y, z) in cubes:
                assert cubes[(x, y, z)] == FRONT.cubes[j][i]
            cubes[(x, y, z)] = FRONT.cubes[j][i]

    ############################################################

    LEFT = SIDES[3]
    print("Left")
    for i in range(7):
        for j in range(7):
            x = 0
            y = j
            z = 6 - i

            if (x, y, z) in cubes:
                assert cubes[(x, y, z)] == LEFT.cubes[j][i]
            cubes[(x, y, z)] = LEFT.cubes[j][i]

    ############################################################

    TOP = TOP
    print("Top")
    for i in range(7):
        for j in range(7):
            x = i
            y = 6 - j
            z = 6

            if (x, y, z) in cubes:
                assert cubes[(x, y, z)] == TOP.cubes[j][i]
            cubes[(x, y, z)] = TOP.cubes[j][i]

    print(len((filter(lambda x: x % 2 == 0, cubes.values()))))
    print(cubes)
    return cubes


def find_specials(matrix):
    odds = list(filter(lambda x: x[1] % 2 == 1, matrix.items()))
    print(len(odds))
    if len(odds) == 7:
        return odds
    evens = list(filter(lambda x: x[1] % 2 == 0, matrix.items()))
    print(len(evens))
    if len(evens) == 7:
        return evens
    primes = list(filter(lambda x: is_prime(x[1]), matrix.items()))
    print(len(primes))
    if len(primes) == 7:
        return primes
    non_primes = list(filter(lambda x: is_prime(x[1]) is False, matrix.items()))
    print(len(non_primes))
    if len(non_primes) == 7:
        return non_primes
    primes = get_primes(1000000)
    three_divisors = list(filter(lambda x: len(factor_p(x[1], primes, 100000)[0]) == 3, matrix.items()))
    print(len(three_divisors))
    if len(three_divisors) == 7:
        return three_divisors
    small = list(filter(lambda x: x[1] < 1000000000, matrix.items()))
    print(len(small))
    if len(small) == 7:
        return small


def calculate_vector(start, end):
    return end[0] - start[0], end[1] - start[1], end[2] - start[2]


def calculate_vectors(specials):
    return [((points_pair[0], points_pair[1]), calculate_vector(points_pair[0], points_pair[1])) for points_pair in itertools.combinations(specials, 2)]


def dot_product(vector1, vector2):
    return numpy.dot(vector1, vector2)


def find_intersection(line1, line2):
    from shapely.geometry import LineString
    A, B = line1
    C, D = line2
    line1 = LineString([A, B])
    line2 = LineString([C, D])
    result = line1.intersection(line2)
    print('intersection', str(result))
    if "POINT Z" in str(result):
        return tuple(map(int, map(numpy.round, map(float, re.findall("(\d+\.?\d*)", str(result))))))
    else:
        return ()


def is_internal_cube(intersection):
    return reduce(lambda x, y: x and y, [0 < intersection[i] < 6 for i in range(3)])


def find_perpendicular_crossing(points):
    vectors = calculate_vectors(points)
    intersections = set()
    for vector_pair in itertools.combinations(vectors, 2):
        vector1, vector2 = vector_pair
        line1, v1 = vector1
        line2, v2 = vector2
        if v1 != v2 and line1[0] not in line2 and line1[1] not in line2:
            product = dot_product(v1, v2)
            if product == 0:
                print('perpendicular vectors', line1, v1, line2, v2)
                intersection = find_intersection(line1, line2)
                if len(intersection) > 0 and intersection not in line1 and intersection not in line2 and is_internal_cube(intersection):
                    intersections.add(intersection)
    print('all internal intersections', intersections)
    return list(intersections)[0]


def main():
    while True:
        try:
            s = nc("47.75.60.212", 11011)
            data = receive_until_match(s, "Please give me str", None)
            p = PoW(data)
            send(s, p)
            print(receive_until_match(s, "you will get the flag.", None))
            while True:
                x = receive_until_match(s, "------------------------------------------------------------------------------", None)
                print(x)
                question_data = receive_until_match(s, "Please enter the coordinates of the answer:", None)
                print(question_data)
                if "N1CTF" in x or "N1CTF" in question_data:
                    interactive(s)
                matrix = parse_data(question_data)
                specials = find_specials(matrix)
                print('specials', specials)
                specials_coords = [x[0] for x in specials]
                intersection_point = find_perpendicular_crossing(specials_coords)
                print('intersection at', intersection_point)
                for i in range(3):
                    send(s, str(intersection_point[i]))
        except:
            pass


main()
```

In the end the hardest part was parsing the input data and assigning coordinates to numbers.
This was because the walls would have random rotations and random positions, so we had to match them by edges.
After that the calculations were pretty simple:

1. Find special points
2. Calculate vectors between each pair
3. Find perpendicular vectors (dot product of such vectors is 0)
4. Find intersection between two lines indicated by 4 points we have (2 points per vector)
5. If intersection crosses an internal cube then consider this a proper solution

It took a couple of minutes but we finally got: `N1CTF{This_1s_a_1j_Math_Game4!}`
