import re

from Crypto.Util.number import bytes_to_long

from crypto_commons.generic import chunk
from riscv_asm import TYPES_TO_INSTRUCTION, INSTRUCTION_TO_TYPE, OPCODES, FUNCT_CODES, \
    R_I_TYPE_UPPER_SEVEN_BITS_NORMAL, R_I_TYPE_UPPER_SEVEN_BITS_ALT, LOAD_INSTRUCTION_NAMES, STORE_INSTRUCTION_NAMES
import argparse


def generate_lookup_to_set(dictionary):
    flipped = {}
    for key, value in dictionary.items():
        if value not in flipped:
            flipped[value] = set()
        flipped[value].add(key)
    return flipped


def generate_opcode_to_type(instruction_to_type, opcode_lookup):
    opcode_to_type = {}
    for opcode, instructions in opcode_lookup.items():
        opcode_to_type[opcode] = instruction_to_type[list(instructions)[0]]
    return opcode_to_type


OPCODE_LOOKUP = generate_lookup_to_set(OPCODES)
FUNCT_LOOKUP = generate_lookup_to_set(FUNCT_CODES)
OPCODE_TO_TYPE = generate_opcode_to_type(INSTRUCTION_TO_TYPE, OPCODE_LOOKUP)


def determine_instruction_name(opcode, funct):
    if opcode == '0000000':
        return 'NOOP'

    candidates = OPCODE_LOOKUP[opcode]
    if len(candidates) == 1:
        return list(candidates)[0]
    for candidate in candidates:
        if candidate in FUNCT_LOOKUP[funct]:
            return candidate
    raise Exception


def disassemble_from_binary(binary_vector, index):
    '''
    >>> u_test = '00000000000001000101000010110111'
    >>> disassemble_from_binary(u_test)
    'LUI x1,0x00045000'
    >>> uj_test = '01111111111100000000001001101111'
    >>> disassemble_from_binary(uj_test)
    'JAL x4,0x00000ffe'
    >>> sb_test = '00111110000100010000011111100011'
    >>> disassemble_from_binary(sb_test)
    'BEQ x2,x1,0x00000bee'
    >>> sb_test = '10101011011010011111111011100011'
    >>> disassemble_from_binary(sb_test)
    'BGEU x19,x22,0xfffffabc'
    >>> i_test = '11111111111101110000111110010011'
    >>> disassemble_from_binary(i_test)
    'ADDI x31,x14,0xffffffff'
    >>> i_test = '00000000010011100011111010010011'
    >>> disassemble_from_binary(i_test)
    'SLTIU x29,x28,0x00000004'
    >>> r_test = '00000000001100010101000010110011'
    >>> disassemble_from_binary(r_test)
    'SRL x1,x2,x3'
    >>> r_test = '01000000001100010101000010110011'
    >>> disassemble_from_binary(r_test)
    'SRA x1,x2,x3'
    '''
    get_opcode = lambda x: '{0:07b}'.format(x & 0x7F)
    get_functcode = lambda x: '{0:03b}'.format((x >> 12) & 0x7)
    get_rs1 = lambda x: (x >> 15) & 0x1F
    get_rs2 = lambda x: (x >> 20) & 0x1F
    get_rd = lambda x: (x >> 7) & 0x1F
    get_msb12 = lambda x: (x >> 20) & 0xFFF
    get_msb6 = lambda x: (x >> 25) & 0x3F

    def get_bitrange_exclusive(bitvector, msb, lsb):
        top_index = len(bitvector) - 1

        effective_low_index = top_index - msb
        effective_high_index = top_index - lsb + 1
        return bitvector[effective_low_index:effective_high_index]

    as_thirty_two_bit = int(binary_vector, 2)
    opcode = get_opcode(as_thirty_two_bit)
    funct = get_functcode(as_thirty_two_bit)

    instruction_name = determine_instruction_name(opcode, funct)  # could be wrong
    # for r-type instructions because ADD/SUB, or SRA/SRL
    # special case handled in R_TYPE code
    # this case also exists for I_TYPE instructions

    # if it's a known NOOP we can quit now
    if instruction_name == 'NOOP':
        return 'NOOP'

    instruction_type = OPCODE_TO_TYPE[opcode]

    if instruction_type == 'U_TYPE':
        rd = get_rd(as_thirty_two_bit)
        immediate_value = int(hex(as_thirty_two_bit & 0xFFFFF000)[2:][::-1], 16)
        return '{0} X{1},0x{2:x}'.format(instruction_name, rd, immediate_value)

    elif instruction_type == 'UJ_TYPE':
        rd = get_rd(as_thirty_two_bit)

        top_bit = '{0:01b}'.format((as_thirty_two_bit >> 31) & 0x1) * 12
        section_two = (as_thirty_two_bit >> 12) & 0xFF
        section_three = (as_thirty_two_bit >> 20) & 0x1
        section_four = (as_thirty_two_bit >> 25) & 0x3F
        section_five = (as_thirty_two_bit >> 21) & 0xF
        u_immediate = int('{0}{1:08b}{2:01b}{3:06b}{4:04b}0'.format(
            top_bit,
            section_two,
            section_three,
            section_four,
            section_five
        ), 2)

        return '{0} X{1},0x{2:x}'.format(instruction_name, rd, index*4)
    elif instruction_type == 'SB_TYPE':
        rs2 = get_rs2(as_thirty_two_bit)
        rs1 = get_rs1(as_thirty_two_bit)

        first_piece = '{0:01b}'.format((as_thirty_two_bit >> 31) & 0x1) * 20
        second_piece = (as_thirty_two_bit >> 7) & 0x1
        third_piece = (as_thirty_two_bit >> 25) & 0x3F
        fourth_piece = (as_thirty_two_bit >> 8) & 0xF
        sb_immediate = int('{0}{1:01b}{2:06b}{3:04b}0'.format(
            first_piece,
            second_piece,
            third_piece,
            fourth_piece
        ), 2)

        return '{0} X{1},X{2},{3}'.format(instruction_name,
                                          rs1,
                                          rs2,
                                          sb_immediate)

    elif instruction_type == 'I_TYPE':
        rd = get_rd(as_thirty_two_bit)
        rs1 = get_rs1(as_thirty_two_bit)

        first_piece = '{0}'.format((as_thirty_two_bit >> 31) & 0x1) * 21
        second_piece = (as_thirty_two_bit >> 20) & 0x7FF
        i_type_immediate = int('{0}{1:011b}'.format(
            first_piece,
            second_piece), 2)
        if i_type_immediate > 2 ** 30:
            i_type_immediate = -(4294967296 - i_type_immediate)

        if instruction_name in LOAD_INSTRUCTION_NAMES:
            # load instructions have a special format in text
            return '{0} X{1},{2}(X{3})'.format(instruction_name,
                                               rd,
                                               i_type_immediate,
                                               rs1)
        else:
            # all other types of I-TYPE instructions
            if opcode == OPCODES['SRLI'] and funct == FUNCT_CODES['SRLI']:
                decider = '{0:07b}'.format(get_msb6(as_thirty_two_bit))
                if decider == R_I_TYPE_UPPER_SEVEN_BITS_NORMAL:
                    instruction_name = 'SRLI'
                elif decider == R_I_TYPE_UPPER_SEVEN_BITS_ALT:
                    instruction_name = 'SRAI'
                else:
                    assert False, 'Could not disambiguate SRLI and SRAI, upper bits {0}'.format(decider)

            if instruction_name == 'SRLI' or instruction_name == 'SRAI' or \
                    instruction_name == 'SLLi':
                i_type_immediate = i_type_immediate & 0x1F

            return '{0} X{1},X{2},{3}'.format(instruction_name,
                                              rd,
                                              rs1,
                                              i_type_immediate)

    elif instruction_type == 'S_TYPE':
        rs2 = get_rs2(as_thirty_two_bit)
        rs1 = get_rs1(as_thirty_two_bit)

        first_piece = '{0:01b}'.format((as_thirty_two_bit >> 31) & 0x1) * 21
        second_piece = (as_thirty_two_bit >> 25) & 0x3F
        third_piece = (as_thirty_two_bit >> 8) & 0xF
        fourth_piece = (as_thirty_two_bit >> 7) & 0x1

        s_type_immediate = int('{0}{1:06b}{2:04b}{3:01b}'.format(
            first_piece,
            second_piece,
            third_piece,
            fourth_piece
        ), 2)

        return '{0} X{1},{2}(X{3})'.format(instruction_name,
                                           rs2,
                                           s_type_immediate,
                                           rs1)

    elif instruction_type == 'R_TYPE':
        rd = get_rd(as_thirty_two_bit)
        rs1 = get_rs1(as_thirty_two_bit)
        rs2 = get_rs2(as_thirty_two_bit)
        if opcode == OPCODES['ADD'] and funct == FUNCT_CODES['ADD']:
            decider = '{0:07b}'.format(get_msb6(as_thirty_two_bit))
            if decider == R_I_TYPE_UPPER_SEVEN_BITS_NORMAL:
                instruction_name = 'ADD'
            elif decider == R_I_TYPE_UPPER_SEVEN_BITS_ALT:
                instruction_name = 'SUB'
            elif decider == '0000001':
                instruction_name = 'MUL'
            else:
                assert False, 'Could not disambiguate ADD and SUB, upper bits {0}'.format(decider)

        elif opcode == OPCODES['SRL'] and funct == FUNCT_CODES['SRL']:
            decider = '{0:07b}'.format(get_msb6(as_thirty_two_bit))
            if decider == R_I_TYPE_UPPER_SEVEN_BITS_NORMAL:
                instruction_name = 'SRL'
            elif decider == R_I_TYPE_UPPER_SEVEN_BITS_ALT:
                instruction_name = 'SRA'
            else:
                assert False, 'Could not disambiguate SRL and SRA, upper bits {0}'.format(decider)

        return '{0} X{1},X{2},X{3}'.format(instruction_name, rd, rs1, rs2)


def dis(code):
    code = code[:-4]  # strip ret
    chunks = chunk(code, 4)
    result = ''
    i = 0
    for c in chunks:
        disassembled_instruction = disassemble_from_binary(bin(bytes_to_long(c[::-1]))[2:],i)
        result += disassembled_instruction + "\n"
        i += 1
    result = result + 'ret'
    code = result
    for i in range(2, 12):
        code = code.replace('X' + str(i + 16), "S" + str(i))
    for i in range(2, 8):
        code = code.replace('X' + str(i + 10), "A" + str(i))
    code = code.replace("X2", 'SP')
    code = code.replace("X8", 'S0')
    code = code.replace("X9", 'S1')
    code = code.replace("X1,", 'RA,')
    code = code.replace("X10", 'A0')
    code = code.replace("X11", 'A1')
    code = re.sub("ADDI (.*?),X0,(.*)", "LI \g<1>,\g<2>", code)
    code = re.sub("JAL X0,(.*)", "J \g<1>", code)
    code = code.replace(",", ", ")
    code = code.lower()
    return code


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Disassemble RISC-V binary vectors to assembly')
    parser.add_argument('binfile',
                        type=str,
                        help='binary vector file')
    args = parser.parse_args()

    binary_file_path = args.binfile

    with open(binary_file_path, 'r') as binary_file:
        binary_lines = binary_file.readlines()
        for line in binary_lines:
            line = line.strip('\n')
            disassembled_instruction = disassemble_from_binary(line)
            print '{0}'.format(disassembled_instruction)
