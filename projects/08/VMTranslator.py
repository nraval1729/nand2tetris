import sys
from os import listdir
from os.path import join

from AsmWriter import AsmWriter
from VMFileParser import VMFileParser, VMCommandType


def main():
    if len(sys.argv) != 2:
        print("Expected 1 argument (either the .vm file or a directory containing .vm files). Exiting!")
        return
    is_file_arg = sys.argv[1].endswith(".vm")
    asm_file_name = sys.argv[1].split('.')[0] + ".asm" if is_file_arg else sys.argv[1] + ".asm"

    asm_cmds = []
    asm_writer = AsmWriter(asm_file_name)
    if not is_file_arg:
        asm_cmds += asm_writer.write_init()

    if is_file_arg:
        vm_files = [sys.argv[1]]
    else:
        vm_files = [join(sys.argv[1], f) for f in listdir(sys.argv[1]) if f.endswith(".vm")]

    for vm_file in vm_files:
        vmf_parser = VMFileParser(vm_file)
        asm_writer.set_file_name(vm_file)
        while vmf_parser.has_more_lines():
            vmf_parser.advance()
            vm_command = vmf_parser.get_command_type()

            if vm_command != VMCommandType.C_RETURN:
                arg1 = vmf_parser.arg1()

                if vm_command == VMCommandType.C_ARITHMETIC:
                    asm_cmds += asm_writer.write_arithmetic(arg1)
                elif vm_command == VMCommandType.C_LABEL:
                    asm_cmds += asm_writer.write_label(arg1)
                elif vm_command == VMCommandType.C_GOTO:
                    asm_cmds += asm_writer.write_goto(arg1)
                elif vm_command == VMCommandType.C_IF_GOTO:
                    asm_cmds += asm_writer.write_if_goto(arg1)
                else:
                    arg2 = vmf_parser.arg2()

                    if vm_command in [VMCommandType.C_PUSH, VMCommandType.C_POP]:
                        asm_cmds += asm_writer.write_push_pop(vm_command.value, arg1, arg2)
                    elif vm_command == VMCommandType.C_FUNCTION:
                        asm_cmds += asm_writer.write_function(arg1, arg2)
                    elif vm_command == VMCommandType.C_CALL:
                        asm_cmds += asm_writer.write_call(arg1, arg2)
            else:
                asm_cmds += asm_writer.write_return()

        asm_writer.write_asm_commands(asm_cmds)


if __name__ == "__main__":
    main()
