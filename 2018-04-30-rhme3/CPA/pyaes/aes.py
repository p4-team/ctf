#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ---------------------------------------------------
# Copyright (c) 2013 Pablo Caro. All Rights Reserved.
# Pablo Caro <me@pcaro.es> - http://pcaro.es/
# AES.py
# ---------------------------------------------------

import sys
import os.path
from AES_base import sbox, isbox, gfp2, gfp3, gfp9, gfp11, gfp13, gfp14, Rcon

if sys.version_info[0] == 3:
    raw_input = input


def RotWord(word):
    return word[1:] + word[0:1]


def SubWord(word):
    return [sbox[byte] for byte in word]


def SubBytes(state):
    return [[sbox[byte] for byte in word] for word in state]


def InvSubBytes(state):
    return [[isbox[byte] for byte in word] for word in state]


def ShiftRows(state):
    Nb = len(state)
    n = [word[:] for word in state]

    for i in range(Nb):
        for j in range(4):
            n[i][j] = state[(i+j) % Nb][j]

    return n


def InvShiftRows(state):
    Nb = len(state)
    n = [word[:] for word in state]

    for i in range(Nb):
        for j in range(4):
            n[i][j] = state[(i-j) % Nb][j]

    return n


def MixColumns(state):
    Nb = len(state)
    n = [word[:] for word in state]

    for i in range(Nb):
        n[i][0] = (gfp2[state[i][0]] ^ gfp3[state[i][1]]
                   ^ state[i][2] ^ state[i][3])
        n[i][1] = (state[i][0] ^ gfp2[state[i][1]]
                   ^ gfp3[state[i][2]] ^ state[i][3])
        n[i][2] = (state[i][0] ^ state[i][1]
                   ^ gfp2[state[i][2]] ^ gfp3[state[i][3]])
        n[i][3] = (gfp3[state[i][0]] ^ state[i][1]
                   ^ state[i][2] ^ gfp2[state[i][3]])

    return n


def InvMixColumns(state):
    Nb = len(state)
    n = [word[:] for word in state]

    for i in range(Nb):
        n[i][0] = (gfp14[state[i][0]] ^ gfp11[state[i][1]]
                   ^ gfp13[state[i][2]] ^ gfp9[state[i][3]])
        n[i][1] = (gfp9[state[i][0]] ^ gfp14[state[i][1]]
                   ^ gfp11[state[i][2]] ^ gfp13[state[i][3]])
        n[i][2] = (gfp13[state[i][0]] ^ gfp9[state[i][1]]
                   ^ gfp14[state[i][2]] ^ gfp11[state[i][3]])
        n[i][3] = (gfp11[state[i][0]] ^ gfp13[state[i][1]]
                   ^ gfp9[state[i][2]] ^ gfp14[state[i][3]])

    return n


def AddRoundKey(state, key):
    Nb = len(state)
    new_state = [[None for j in range(4)] for i in range(Nb)]

    for i, word in enumerate(state):
        for j, byte in enumerate(word):
            new_state[i][j] = byte ^ key[i][j]

    return new_state
