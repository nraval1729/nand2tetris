import sys

from AsmWriter import AsmWriter
from VMFileParser import VMFileParser, VMCommandType


def main():
    if len(sys.argv) != 2:
        print("Expected 1 argument (the vm file). Exiting!")
        return

    vm_file_name = sys.argv[1]
    asm_file_name = vm_file_name.split('.')[0] + ".asm"

    vmf_parser = VMFileParser(vm_file_name)
    asm_writer = AsmWriter(asm_file_name)

    while vmf_parser.has_more_lines():
        vmf_parser.advance()
        vm_command = vmf_parser.get_command_type()

        if vm_command != VMCommandType.C_RETURN:
            arg1 = vmf_parser.arg1()

            if vm_command == VMCommandType.C_ARITHMETIC:
                asm_writer.write_arithmetic(arg1)
            else:
                # push, pop, function, call
                arg2 = vmf_parser.arg2()

                if vm_command in [VMCommandType.C_PUSH, VMCommandType.C_POP]:
                    asm_writer.write_push_pop(vm_command.value, arg1, arg2)


if __name__ == "__main__":
    main()
