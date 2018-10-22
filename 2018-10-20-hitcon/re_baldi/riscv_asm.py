import argparse
import re

from Crypto.Util.number import long_to_bytes

from crypto_commons.generic import chunk


def reverse_dict_with_iterable(dictionary):
    rev = {}
    for key, value in dictionary.items():
        for item in value:
            rev[item] = key
    return rev


TYPES_TO_INSTRUCTION = {
    'U_TYPE': set(['LUI', 'AUIPC']),
    'UJ_TYPE': set(['JAL']),
    'SB_TYPE': set(['BEQ', 'BNE', 'BLT', 'BGE', 'BLTU', 'BGEU']),
    'I_TYPE': set(
        ['JALR', 'LB', 'LH', 'LW', 'LBU', 'LHU', 'ADDI', 'SLTI', 'SLTIU', 'XORI', 'ORI', 'ANDI', 'SLLI', 'SRLI',
         'SRAI']),
    'S_TYPE': set(['SB', 'SH', 'SW']),
    'R_TYPE': set(['ADD', 'SUB', 'SLL', 'SLT', 'SLTU', 'XOR', 'SRL', 'SRA', 'OR', 'AND','MUL'])
}

LOAD_INSTRUCTION_NAMES = set([
    'LB', 'LH', 'LW', 'LBU', 'LHU'
])

STORE_INSTRUCTION_NAMES = set([
    'SB', 'SH', 'SW'
])

INSTRUCTION_TO_TYPE = reverse_dict_with_iterable(TYPES_TO_INSTRUCTION)

OPCODES = {
    'LUI': '0110111',
    'AUIPC': '0010111',
    'JAL': '1101111',
    'JALR': '1100111',
    'BEQ': '1100011',
    'BNE': '1100011',
    'BLT': '1100011',
    'BGE': '1100011',
    'BLTU': '1100011',
    'BGEU': '1100011',
    'LB': '0000011',
    'LH': '0000011',
    'LW': '0000011',
    'LBU': '0000011',
    'LHU': '0000011',
    'SB': '0100011',
    'SH': '0100011',
    'SW': '0100011',
    'ADDI': '0010011',
    'SLTI': '0010011',
    'SLTIU': '0010011',
    'XORI': '0010011',
    'ORI': '0010011',
    'ANDI': '0010011',
    'SLLI': '0010011',
    'SRLI': '0010011',
    'SRAI': '0010011',
    'ADD': '0110011',
    'SUB': '0110011',
    'SLL': '0110011',
    'SLT': '0110011',
    'SLTU': '0110011',
    'XOR': '0110011',
    'SRL': '0110011',
    'SRA': '0110011',
    'OR': '0110011',
    'AND': '0110011',
    'MUL':'0110011'
}

FUNCT_CODES = {
    'JALR': '000',
    'BEQ': '000',
    'BNE': '001',
    'BLT': '100',
    'BGE': '101',
    'BLTU': '110',
    'BGEU': '111',
    'LB': '000',
    'LH': '001',
    'LW': '010',
    'LBU': '100',
    'LHU': '101',
    'SB': '000',
    'SH': '001',
    'SW': '010',
    'ADDI': '000',
    'SLTI': '010',
    'SLTIU': '011',
    'XORI': '100',
    'ORI': '110',
    'ANDI': '111',
    'SLLI': '001',
    'SRLI': '101',
    'SRAI': '101',
    'ADD': '000',
    'SUB': '000',
    'SLL': '001',
    'SLT': '010',
    'SLTU': '011',
    'XOR': '100',
    'SRL': '101',
    'SRA': '101',
    'OR': '110',
    'AND': '111',
    'MUL': '000'
}

R_I_TYPE_UPPER_SEVEN_BITS_NORMAL = '0000000'
R_I_TYPE_UPPER_SEVEN_BITS_ALT = '0100000'


def generate_binary_from_instruction(instruction_text):
    '''
    >>> R_type_test = 'OR x10,x8,x31'
    >>> generate_binary_from_instruction(R_type_test)
    ('00000001111101000110010100110011', 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    >>> R_type_test = 'SUB x10,x8,x30'
    >>> generate_binary_from_instruction(R_type_test)
    ('01000001111001000000010100110011', 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    '''
    calculate_register_number_from_name = lambda x: int(x[1:])

    instruction_name, remainder = instruction_text.split()
    instruction_values = remainder.replace(" ", "").split(',')
    instruction_type = INSTRUCTION_TO_TYPE[instruction_name]

    if instruction_type == 'U_TYPE':
        # unpack u-type instruction
        assert len(instruction_values) == 2

        register_name = calculate_register_number_from_name(instruction_values[0])
        immediate_value = int(instruction_values[1], 0) & 0xFFFFFFFF  # convert immediate to integer

        immediate_bits = immediate_value

        instruction_binary = '{0:020b}{1:05b}{2}'.format(immediate_bits,
                                                         register_name,
                                                         OPCODES[instruction_name])

        immediate_real_pattern = '{0:032b}'.format(immediate_value)

        assert len(instruction_binary) == 32
        assert len(immediate_real_pattern) == 32
        return instruction_binary, immediate_real_pattern

    elif instruction_type == 'UJ_TYPE':
        # unpack uj-type instruction
        assert len(instruction_values) == 2

        register_name = calculate_register_number_from_name(instruction_values[0])
        immediate_value = int(instruction_values[1], 0)  # convert immediate to integer
        # get bottom 20 bits of immediate
        immediate_bottom_bits = immediate_value & 0x1FFFFF

        # pack immedate bits into binary string
        immediate_binary_string = '{0:01b}{1:010b}{2:01b}{3:08b}'.format(
            (immediate_bottom_bits >> 20) & 0x1,
            (immediate_bottom_bits >> 1) & 0x3FF,
            (immediate_bottom_bits >> 11) & 0x1,
            (immediate_bottom_bits >> 12) & 0xFF)

        instruction_binary = '{0}{1:05b}{2}'.format(immediate_binary_string,
                                                    register_name,
                                                    OPCODES[instruction_name])

        sign_extension_pattern = 11 * '{0}'.format(immediate_value >> 20)
        immediate_real_pattern = '{0}{1:021b}'.format(sign_extension_pattern, immediate_value)

        assert len(instruction_binary) == 32
        assert len(immediate_real_pattern) == 32
        return instruction_binary, immediate_real_pattern

    elif instruction_type == 'SB_TYPE':

        # unpack sb-type instruction

        assert len(instruction_values) == 3

        rs1_name = calculate_register_number_from_name(instruction_values[0])
        rs2_name = calculate_register_number_from_name(instruction_values[1])

        # get bottom 13 bits
        immediate_value = int(instruction_values[2], 0) & 0x1FFF

        # pack upper half of immediate
        immediate_upper_bits_string = '{0:01b}{1:06b}'.format(
            (immediate_value >> 12) & 0x1,
            (immediate_value >> 5) & 0x3F)

        # pack lower half of immediate
        immediate_lower_bits_string = '{0:04b}{1:01b}'.format(
            (immediate_value >> 1) & 0xF,
            (immediate_value >> 11) & 0x1)

        instruction_binary = '{0}{1:05b}{2:05b}{3}{4}{5}'.format(
            immediate_upper_bits_string,
            rs2_name,
            rs1_name,
            FUNCT_CODES[instruction_name],
            immediate_lower_bits_string,
            OPCODES[instruction_name]
        )

        sign_extension_pattern = 19 * '{0}'.format(immediate_value >> 12)
        immediate_real_pattern = '{0}{1:013b}'.format(sign_extension_pattern,
                                                      immediate_value & (0xFFF << 1))

        assert len(instruction_binary) == 32
        assert len(immediate_real_pattern) == 32
        return instruction_binary, immediate_real_pattern

    elif instruction_type == 'S_TYPE':

        rs2_name = calculate_register_number_from_name(instruction_values[0])
        second_piece = instruction_values[1].split('(')
        immediate_value = int(second_piece[0], base=0)
        rs1_name = calculate_register_number_from_name(second_piece[1][:-1])

        immediate_upper_half = '{0:07b}'.format(immediate_value >> 5)
        immediate_lower_half = '{0:05b}'.format(immediate_value & 0x1F)

        instruction_binary = '{0}{1:05b}{2:05b}{3}{4}{5}'.format(
            immediate_upper_half,
            rs2_name,
            rs1_name,
            FUNCT_CODES[instruction_name],
            immediate_lower_half,
            OPCODES[instruction_name]
        )

        sign_extension_pattern = 20 * '{0}'.format(immediate_value >> 11)
        immediate_real_pattern = '{0}{1:012b}'.format(sign_extension_pattern,
                                                      immediate_value)

        assert len(immediate_real_pattern) == 32
        assert len(instruction_binary) == 32

        return instruction_binary, immediate_real_pattern

    elif instruction_type == 'I_TYPE':
        # unpack i-type instruction
        rd_name = None
        rs1_name = None
        immediate_value = None

        if instruction_name in LOAD_INSTRUCTION_NAMES:
            rd_name = calculate_register_number_from_name(instruction_values[0])
            second_piece = instruction_values[1].split('(')
            immediate_value = int(second_piece[0], base=0)
            rs1_name = calculate_register_number_from_name(second_piece[1][:-1])

        else:
            assert len(instruction_values) == 3

            rd_name = calculate_register_number_from_name(instruction_values[0])
            rs1_name = calculate_register_number_from_name(instruction_values[1])

            immediate_value = int(instruction_values[2], base=0) & 0xFFF

        immediate_binary_string = ''
        if instruction_name == 'SLLI' or instruction_name == 'SRLI' \
                or instruction_name == 'SRAI':

            if instruction_name == 'SRAI':
                immediate_binary_string = '{0}{1:05b}'.format(
                    R_I_TYPE_UPPER_SEVEN_BITS_ALT,
                    immediate_value & 0x1F)
            else:
                immediate_binary_string = '{0}{1:05b}'.format(
                    R_I_TYPE_UPPER_SEVEN_BITS_NORMAL,
                    immediate_value & 0x1F)

        else:
            immediate_binary_string = '{0:012b}'.format(immediate_value)

        assert len(immediate_binary_string) == 12

        instruction_binary = '{0}{1:05b}{2}{3:05b}{4}'.format(
            immediate_binary_string,
            rs1_name,
            FUNCT_CODES[instruction_name],
            rd_name,
            OPCODES[instruction_name])

        sign_extension_pattern = 20 * '{0}'.format(immediate_value >> 11)
        immediate_real_pattern = '{0}{1:012b}'.format(sign_extension_pattern,
                                                      immediate_value)

        if instruction_name == 'SLLI' or instruction_name == 'SRLI' \
                or instruction_name == 'SRAI':
            immediate_real_pattern = '0' * 27 + '{0:05b}'.format(immediate_value & 0x1F)

        assert len(instruction_binary) == 32
        assert len(immediate_real_pattern) == 32

        return instruction_binary, immediate_real_pattern

    elif instruction_type == 'R_TYPE':
        # unpack r-type instruction
        assert len(instruction_values) == 3
        rd_name = calculate_register_number_from_name(instruction_values[0])
        rs1_name = calculate_register_number_from_name(instruction_values[1])
        rs2_name = calculate_register_number_from_name(instruction_values[2])

        special_instructions = set(['SUB', 'SRA'])
        upper_bit_pattern = R_I_TYPE_UPPER_SEVEN_BITS_ALT if instruction_name in special_instructions else R_I_TYPE_UPPER_SEVEN_BITS_NORMAL
        if instruction_name == 'MUL':
            upper_bit_pattern = '0000001'

        instruction_binary = '{0}{1:05b}{2:05b}{3}{4:05b}{5}'.format(
            upper_bit_pattern,
            rs2_name,
            rs1_name,
            FUNCT_CODES[instruction_name],
            rd_name,
            OPCODES[instruction_name]
        )

        assert len(instruction_binary) == 32
        return instruction_binary, (32 * 'x')


def asm(code):
    code = code.upper()
    code = code.replace("\nRET", "")
    code = re.sub("LI (.*?), (.*)", "ADDI \g<1>, X0, \g<2>", code)
    code = re.sub("J .*", "JAL X0, 0", code)
    code = code.replace(", ", ",")
    code = code.replace("SP", 'X2')
    code = code.replace("S0", 'X8')
    code = code.replace("S1", 'X9')
    code = code.replace("RA", 'X1')
    code = code.replace("A0", 'X10')
    code = code.replace("A1", 'X11')
    for i in range(2, 12):
        code = code.replace("S" + str(i), 'X' + str(i + 16))
    for i in range(2, 8):
        code = code.replace("A" + str(i), 'X' + str(i + 10))
    res = ''
    for line in code.split("\n"):
        line = line.strip('\n')
        instruction_as_binary, immediate = generate_binary_from_instruction(line)
        res += instruction_as_binary
    chunks = chunk(long_to_bytes(int(res, 2)), 4)
    return "".join(c[::-1] for c in chunks)+"g\x80\x00\x00"


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Convert RISC-V assembly to binary vectors')
    parser.add_argument('asmfile',
                        type=str,
                        help='asm file')
    parser.add_argument('-d',
                        '--debug',
                        action='store_true',
                        default=False,
                        help='enable printing additional stuff')
    parser.add_argument('-i',
                        '--inst',
                        action='store_true',
                        default=False,
                        help='print instruction text')
    parser.add_argument('-m',
                        '--imm',
                        action='store_true',
                        default=False,
                        help='print immediate binary')

    args = parser.parse_args()

    assembly_file_path = args.asmfile

    assembly_file_root_name = assembly_file_path.split('.')[0]

    with open(assembly_file_path, 'r') as assembly_file:
        assembly_lines = assembly_file.readlines()
        for line in assembly_lines:
            line = line.strip('\n')
            instruction_as_binary, immediate = generate_binary_from_instruction(line)

            if args.debug:
                if args.inst:
                    print 'inst: {0}'.format(line)
                if args.imm:
                    print 'immediate: {0}'.format(immediate)
                print 'bin: {0}\n\n'.format(instruction_as_binary)
            else:
                print '{0}'.format(instruction_as_binary)
