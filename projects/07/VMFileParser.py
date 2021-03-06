from enum import Enum

arithmetic_commands = ["add", "sub", "neg"]
logical_commands = ["eq", "gt", "lt", "and", "or", "not"]


class VMCommandType(Enum):
    C_ARITHMETIC = 'arithmetic'
    C_PUSH = 'push'
    C_POP = 'pop'
    C_FUNCTION = 'function'
    C_CALL = 'call'
    C_RETURN = 'return'


class VMFileParser(object):
    def __init__(self, vm_file_name):
        self.vm_file = open(vm_file_name, 'r')

        self.lines = self.vm_file.read().splitlines()
        self._filter_out_comments()
        self._filter_out_newlines()

        self.current_line_index = 0
        self.current_line = self.lines[self.current_line_index]

    def has_more_lines(self):
        return self.current_line_index < len(self.lines)

    def advance(self):
        self.current_line = self.lines[self.current_line_index]
        self.current_line_index += 1

    def get_command_type(self):
        if self.current_line in arithmetic_commands or self.current_line in logical_commands:
            return VMCommandType.C_ARITHMETIC
        elif self.current_line.startswith("push"):
            return VMCommandType.C_PUSH
        elif self.current_line.startswith("pop"):
            return VMCommandType.C_POP
        # TODO: Add more commands in next project

    def arg1(self):
        # current line is the command in case of all arithmetic and logical commands
        if self.get_command_type() == VMCommandType.C_ARITHMETIC:
            return self.current_line
        else:
            return self.current_line.split(" ")[1]

    def arg2(self):
        return self.current_line.split(" ")[2]

    def close(self):
        self.vm_file.close()

    # Remove comments
    def _filter_out_comments(self):
        self.lines = [line for line in self.lines if not line.startswith("//")]

    # Remove newlines
    def _filter_out_newlines(self):
        self.lines = [line for line in self.lines if line]
