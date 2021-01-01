import sys

c_instruction_table = {
    'dest': {None: '000', 'M': '001', 'D': '010', 'MD': '011', 'A': '100', 'AM': '101', 'AD': '110', 'AMD': '111'},
    'jmp': {None: '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011', 'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'},
    'comp': {
        '0': '0101010',
        '1': '0111111',
        '-1': '0111010',
        'D': '0001100',
        'A': '0110000', 'M': '1110000',
        '!D': '0001101',
        '!A': '0110001', '!M': '1110001',
        '-D': '0001111',
        '-A': '0110011', '-M': '1110011',
        'D+1': '0011111',
        'A+1': '0110111', 'M+1': '1110111',
        'D-1': '0001110',
        'A-1': '0110010', 'M-1': '1110010',
        'D+A': '0000010', 'D+M': '1000010',
        'D-A': '0010011', 'D-M': '1010011',
        'A-D': '0000111', 'M-D': '1000111',
        'D&A': '0000000', 'D&M': '1000000',
        'D|A': '0010101', 'D|M': '1010101',
    }
}

symbol_table = {
    'R0': '0', 'R1': '1', 'R2': '2', 'R3': '3',
    'R4': '4', 'R5': '5', 'R6': '6', 'R7': '7',
    'R8': '8', 'R9': '9', 'R10': '10', 'R11': '11',
    'R12': '12', 'R13': '13', 'R14': '14', 'R15': '15',

    'SCREEN': '16384', 'KBD': '24576',

    'SP': '0', 'LCL': '1', 'ARG': '2', 'THIS': '3', 'THAT': '4'
}


def main():
    if len(sys.argv) != 2:
        print("Need name of assembly file to assemble!")
        return

    content = get_file_content(sys.argv[1])

    add_labels_in_symbol_table(content)
    generate_binary_code(content, sys.argv[1])


def add_labels_in_symbol_table(content):
    filtered_content = [l for l in content if not is_skippable_line(l)]

    instruction_no = 0
    for ins in filtered_content:
        ins = clean_ins(ins)
        if is_label_instruction(ins):
            label = get_label(ins)
            # print("Found label: ", label)
            symbol_table[label] = instruction_no
        else:
            instruction_no += 1


def is_label_instruction(ins):
    return ins.startswith('(') and ins.endswith(')')


def get_label(label_ins):
    return label_ins.split('(')[1].split(')')[0]


def is_skippable_line(l):
    return not l or l.startswith("//")


# Clean all leading whitespace and trailing whitespace and inline comments
def clean_ins(ins):
    return ins.strip().split(" ")[0]


def generate_binary_code(content, asm_file_name):
    filtered_content = [l for l in content if not is_skippable_line(l)]
    variable_address = 16

    binary = []
    for ins in filtered_content:
        print(ins)
        ins = clean_ins(ins)
        print(ins)
        # We ignore (LABEL) instructions while generating the binary
        if is_label_instruction(ins):
            continue
        elif is_a_instruction(ins):
            # print("A: ", ins)
            bin, variable_address = assemble_a_instruction(ins, variable_address)
            binary.append(bin)
        elif is_c_instruction(ins):
            binary.append(assemble_c_instruction(ins))
        else:
            print("invalid instruction: ", ins)
            return

    print(str.join("\n", binary))
    binary_file_name = asm_file_name.split('.')[0] + ".hack"
    with open(binary_file_name, 'w') as f:
        f.write(str.join("\n", binary))


def is_a_instruction(ins):
    return ins.startswith('@')


def is_c_instruction(ins):
    return '=' in ins or ';' in ins


def assemble_a_instruction(ins, curr_var_address):
    symbol = ins.split("@")[1]
    if symbol.isdigit():
        bin = convert_decimal_to_binary(int(symbol))
    elif symbol in symbol_table:
        bin = convert_decimal_to_binary(int(symbol_table[symbol]))
    else:
        symbol_table[symbol] = curr_var_address
        bin = convert_decimal_to_binary(curr_var_address)
        curr_var_address += 1

    return '0' + bin, curr_var_address


def assemble_c_instruction(ins):
    dest, comp, jmp = parse_c_instruction(ins)
    print(ins, dest, comp, jmp)
    return '111' + c_instruction_table['comp'][comp] + c_instruction_table['dest'][dest] + c_instruction_table['jmp'][jmp]


# Returns dest, comp, jmp in a given C instruction of the form dest=comp;jmp
def parse_c_instruction(c_ins):
    c_ins_split_on_equals = c_ins.split('=')

    if len(c_ins_split_on_equals) == 1:
        # no dest present
        dest = None
        c_ins_split_on_semi_colon_minus_equals = c_ins_split_on_equals[0].split(';')
        if len(c_ins_split_on_semi_colon_minus_equals) == 1:
            # no jmp present
            jmp = None
            comp = c_ins_split_on_semi_colon_minus_equals[0]
        else:
            # comp and jmp both present
            comp = c_ins_split_on_semi_colon_minus_equals[0]
            jmp = c_ins_split_on_semi_colon_minus_equals[1]
    else:
        # dest is present
        dest = c_ins_split_on_equals[0]
        c_ins_split_on_semi_colon_minus_equals = c_ins_split_on_equals[1].split(';')
        if len(c_ins_split_on_semi_colon_minus_equals) == 1:
            # no jmp present
            jmp = None
            comp = c_ins_split_on_semi_colon_minus_equals[0]
        else:
            # comp and jmp both present
            comp = c_ins_split_on_semi_colon_minus_equals[0]
            jmp = c_ins_split_on_semi_colon_minus_equals[1]

    return dest, comp, jmp


def get_file_content(filename):
    with open(filename, 'r') as f:
        content = f.read().splitlines()

    return content


# Return 15 bit binary representation of the given the_int
def convert_decimal_to_binary(the_int):
    return "{0:015b}".format(the_int)


if __name__ == "__main__":
    main()
