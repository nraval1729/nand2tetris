class AsmWriter(object):
    def __init__(self, asm_file_name):
        self.asm_file_name = asm_file_name
        self.asm_file = open(asm_file_name, 'w')
        self.eq_counter, self.gt_counter, self.lt_counter = 0, 0, 0
        self.temp_segment_base_address = 5

    def write_arithmetic(self, vm_command):
        asm_commands = []

        # Add comment
        asm_commands.append("// {}".format(vm_command))

        if vm_command == "add":
            asm_commands += self._get_add_commands()
        elif vm_command == "sub":
            asm_commands += self._get_sub_commands()
        elif vm_command == "neg":
            asm_commands += self._get_neg_commands()
        elif vm_command == "eq":
            asm_commands += self._get_eq_commands()
        elif vm_command == "gt":
            asm_commands += self._get_gt_commands()
        elif vm_command == "lt":
            asm_commands += self._get_lt_commands()
        elif vm_command == "and":
            asm_commands += self._get_and_commands()
        elif vm_command == "or":
            asm_commands += self._get_or_commands()
        elif vm_command == "not":
            asm_commands += self._get_not_commands()
        else:
            print("invalid arithmetic/logical command!")
            return

        self.write_asm_commands(asm_commands)

    def write_push_pop(self, vm_command, memory_segment, arg):
        asm_commands = []

        # Add comment
        asm_commands.append("// {} {} {}".format(vm_command, memory_segment, arg))

        if vm_command == "push":
            if memory_segment == "constant":
                asm_commands += self._get_push_constant_commands(arg)
            elif memory_segment == "local":
                asm_commands += self._get_push_local_commands(arg)
            elif memory_segment == "argument":
                asm_commands += self._get_push_argument_commands(arg)
            elif memory_segment == "this":
                asm_commands += self._get_push_this_commands(arg)
            elif memory_segment == "that":
                asm_commands += self._get_push_that_commands(arg)
            elif memory_segment == "static":
                asm_commands += self._get_push_static_commands(arg)
            elif memory_segment == "temp":
                asm_commands += self._get_push_temp_commands(arg)
            elif memory_segment == "pointer":
                asm_commands += self._get_push_pointer_commands(arg)
            else:
                print("invalid memory access command!")
                return
        elif vm_command == "pop":
            if memory_segment == "local":
                asm_commands += self._get_pop_local_commands(arg)
            elif memory_segment == "argument":
                asm_commands += self._get_pop_argument_commands(arg)
            elif memory_segment == "this":
                asm_commands += self._get_pop_this_commands(arg)
            elif memory_segment == "that":
                asm_commands += self._get_pop_that_commands(arg)
            elif memory_segment == "static":
                asm_commands += self._get_pop_static_commands(arg)
            elif memory_segment == "temp":
                asm_commands += self._get_pop_temp_commands(arg)
            elif memory_segment == "pointer":
                asm_commands += self._get_pop_pointer_commands(arg)
            else:
                print("invalid memory access command!")
                return

        self.write_asm_commands(asm_commands)

    def _get_add_commands(self):
        cmds = []
        cmds.append("@SP")
        cmds.append("A=M-1")
        cmds.append("D=M")
        cmds.append("A=A-1")
        cmds.append("D=D+M")
        cmds.append("M=D")
        cmds.append("@SP")
        cmds.append("M=M-1")

        return cmds

    def _get_sub_commands(self):
        cmds = []
        cmds.append("@SP")
        cmds.append("A=M-1")
        cmds.append("D=-M")
        cmds.append("A=A-1")
        cmds.append("D=D+M")
        cmds.append("M=D")
        cmds.append("@SP")
        cmds.append("M=M-1")

        return cmds

    def _get_neg_commands(self):
        cmds = []
        cmds.append("@SP")
        cmds.append("A=M-1")
        cmds.append("M=-M")

        return cmds

    def _get_eq_commands(self):
        cmds = []
        cmds.append("@SP")
        cmds.append("A=M-1")
        cmds.append("D=-M")
        cmds.append("A=A-1")
        cmds.append("D=D+M")

        cmds.append("@X_EQUALS_Y_{}".format(self.eq_counter))
        cmds.append("D;JEQ")

        cmds.append("@SP")
        cmds.append("A=M-1")
        cmds.append("A=A-1")
        cmds.append("M=0")
        cmds.append("@DECREMENT_SP_EQ_{}".format(self.eq_counter))
        cmds.append("0;JMP")

        cmds.append("(X_EQUALS_Y_{})".format(self.eq_counter))
        cmds.append("@SP")
        cmds.append("A=M-1")
        cmds.append("A=A-1")
        cmds.append("M=-1")
        cmds.append("@DECREMENT_SP_EQ_{}".format(self.eq_counter))
        cmds.append("0;JMP")

        cmds.append("(DECREMENT_SP_EQ_{})".format(self.eq_counter))
        cmds.append("@SP")
        cmds.append("M=M-1")

        self.eq_counter += 1
        return cmds

    def _get_gt_commands(self):
        cmds = []
        cmds.append("@SP")
        cmds.append("A=M-1")
        cmds.append("D=-M")
        cmds.append("A=A-1")
        cmds.append("D=D+M")

        cmds.append("@X_GT_Y_{}".format(self.gt_counter))
        cmds.append("D;JGT")

        cmds.append("@SP")
        cmds.append("A=M-1")
        cmds.append("A=A-1")
        cmds.append("M=0")
        cmds.append("@DECREMENT_SP_GT_{}".format(self.gt_counter))
        cmds.append("0;JMP")

        cmds.append("(X_GT_Y_{})".format(self.gt_counter))
        cmds.append("@SP")
        cmds.append("A=M-1")
        cmds.append("A=A-1")
        cmds.append("M=-1")
        cmds.append("@DECREMENT_SP_GT_{}".format(self.gt_counter))
        cmds.append("0;JMP")

        cmds.append("(DECREMENT_SP_GT_{})".format(self.gt_counter))
        cmds.append("@SP")
        cmds.append("M=M-1")

        self.gt_counter += 1
        return cmds

    def _get_lt_commands(self):
        cmds = []
        cmds.append("@SP")
        cmds.append("A=M-1")
        cmds.append("D=-M")
        cmds.append("A=A-1")
        cmds.append("D=D+M")

        cmds.append("@X_LT_Y_{}".format(self.lt_counter))
        cmds.append("D;JLT")

        cmds.append("@SP")
        cmds.append("A=M-1")
        cmds.append("A=A-1")
        cmds.append("M=0")
        cmds.append("@DECREMENT_SP_LT_{}".format(self.lt_counter))
        cmds.append("0;JMP")

        cmds.append("(X_LT_Y_{})".format(self.lt_counter))
        cmds.append("@SP")
        cmds.append("A=M-1")
        cmds.append("A=A-1")
        cmds.append("M=-1")
        cmds.append("@DECREMENT_SP_LT_{}".format(self.lt_counter))
        cmds.append("0;JMP")

        cmds.append("(DECREMENT_SP_LT_{})".format(self.lt_counter))
        cmds.append("@SP")
        cmds.append("M=M-1")

        self.lt_counter += 1
        return cmds

    def _get_and_commands(self):
        cmds = []
        cmds.append("@SP")
        cmds.append("A=M-1")
        cmds.append("D=M")
        cmds.append("A=A-1")
        cmds.append("D=D&M")
        cmds.append("M=D")
        cmds.append("@SP")
        cmds.append("M=M-1")

        return cmds

    def _get_or_commands(self):
        cmds = []
        cmds.append("@SP")
        cmds.append("A=M-1")
        cmds.append("D=M")
        cmds.append("A=A-1")
        cmds.append("D=D|M")
        cmds.append("M=D")
        cmds.append("@SP")
        cmds.append("M=M-1")

        return cmds

    def _get_not_commands(self):
        cmds = []
        cmds.append("@SP")
        cmds.append("A=M-1")
        cmds.append("M=!M")

        return cmds

    # Memory access commands - PUSH
    def _get_push_constant_commands(self, arg):
        cmds = []
        cmds.append("@{}".format(arg))
        cmds.append("D=A")
        cmds.append("@SP")
        cmds.append("A=M")
        cmds.append("M=D")
        cmds.append("@SP")
        cmds.append("M=M+1")

        return cmds

    def _get_push_local_commands(self, arg):
        cmds = []

        # addr = LCL + i
        cmds.append("@LCL")
        cmds.append("D=M")
        cmds.append("@{}".format(arg))
        cmds.append("D=D+A")
        cmds.append("@addr")
        cmds.append("M=D")

        # *SP = *addr
        cmds.append("@addr")
        cmds.append("A=M")
        cmds.append("D=M")
        cmds.append("@SP")
        cmds.append("A=M")
        cmds.append("M=D")

        # SP++
        cmds.append("@SP")
        cmds.append("M=M+1")

        return cmds

    def _get_push_argument_commands(self, arg):
        cmds = []

        # addr = ARG + i
        cmds.append("@ARG")
        cmds.append("D=M")
        cmds.append("@{}".format(arg))
        cmds.append("D=D+A")
        cmds.append("@addr")
        cmds.append("M=D")

        # *SP = *addr
        cmds.append("@addr")
        cmds.append("A=M")
        cmds.append("D=M")
        cmds.append("@SP")
        cmds.append("A=M")
        cmds.append("M=D")

        # SP++
        cmds.append("@SP")
        cmds.append("M=M+1")

        return cmds

    def _get_push_this_commands(self, arg):
        cmds = []

        # addr = this + i
        cmds.append("@THIS")
        cmds.append("D=M")
        cmds.append("@{}".format(arg))
        cmds.append("D=D+A")
        cmds.append("@addr")
        cmds.append("M=D")

        # *SP = *addr
        cmds.append("@addr")
        cmds.append("A=M")
        cmds.append("D=M")
        cmds.append("@SP")
        cmds.append("A=M")
        cmds.append("M=D")

        # SP++
        cmds.append("@SP")
        cmds.append("M=M+1")

        return cmds

    def _get_push_that_commands(self, arg):
        cmds = []

        # addr = that + i
        cmds.append("@THAT")
        cmds.append("D=M")
        cmds.append("@{}".format(arg))
        cmds.append("D=D+A")
        cmds.append("@addr")
        cmds.append("M=D")

        # *SP = *addr
        cmds.append("@addr")
        cmds.append("A=M")
        cmds.append("D=M")
        cmds.append("@SP")
        cmds.append("A=M")
        cmds.append("M=D")

        # SP++
        cmds.append("@SP")
        cmds.append("M=M+1")

        return cmds

    def _get_push_static_commands(self, arg):
        static_variable_name = self.asm_file_name.split('.')[0]
        cmds = []

        # D = Filename.arg
        cmds.append("@{}.{}".format(static_variable_name, arg))
        cmds.append("D=M")

        # SP.push(D)
        cmds.append("@SP")
        cmds.append("A=M")
        cmds.append("M=D")

        # SP++
        cmds.append("@SP")
        cmds.append("M=M+1")

        return cmds

    def _get_push_temp_commands(self, arg):
        cmds = []

        # addr = TEMP_BASE_ADDRESS + i
        cmds.append("@{}".format(self.temp_segment_base_address))
        cmds.append("D=A")
        cmds.append("@{}".format(arg))
        cmds.append("D=D+A")
        cmds.append("@addr")
        cmds.append("M=D")

        # *SP = *addr
        cmds.append("@addr")
        cmds.append("A=M")
        cmds.append("D=M")
        cmds.append("@SP")
        cmds.append("A=M")
        cmds.append("M=D")

        # SP++
        cmds.append("@SP")
        cmds.append("M=M+1")

        return cmds

    def _get_push_pointer_commands(self, arg):
        should_access_this = arg == '0'

        cmds = []

        # D = THIS/THAT
        cmds.append("@{}".format("THIS")) if should_access_this else cmds.append("@{}".format("THAT"))
        cmds.append("D=M")

        # SP.push(THIS/THAT)
        cmds.append("@SP")
        cmds.append("A=M")
        cmds.append("M=D")

        # SP++
        cmds.append("@SP")
        cmds.append("M=M+1")

        return cmds

    # Memory access commands - POP
    def _get_pop_local_commands(self, arg):
        cmds = []

        # addr = LCL + i
        cmds.append("@LCL")
        cmds.append("D=M")
        cmds.append("@{}".format(arg))
        cmds.append("D=D+A")
        cmds.append("@addr")
        cmds.append("M=D")

        # SP--
        cmds.append("@SP")
        cmds.append("M=M-1")

        # *addr = *SP
        cmds.append("@SP")
        cmds.append("A=M")
        cmds.append("D=M")
        cmds.append("@addr")
        cmds.append("A=M")
        cmds.append("M=D")

        return cmds

    def _get_pop_argument_commands(self, arg):
        cmds = []

        # addr = ARG + i
        cmds.append("@ARG")
        cmds.append("D=M")
        cmds.append("@{}".format(arg))
        cmds.append("D=D+A")
        cmds.append("@addr")
        cmds.append("M=D")

        # SP--
        cmds.append("@SP")
        cmds.append("M=M-1")

        # *addr = *SP
        cmds.append("@SP")
        cmds.append("A=M")
        cmds.append("D=M")
        cmds.append("@addr")
        cmds.append("A=M")
        cmds.append("M=D")

        return cmds

    def _get_pop_this_commands(self, arg):
        cmds = []

        # addr = THIS + i
        cmds.append("@THIS")
        cmds.append("D=M")
        cmds.append("@{}".format(arg))
        cmds.append("D=D+A")
        cmds.append("@addr")
        cmds.append("M=D")

        # SP--
        cmds.append("@SP")
        cmds.append("M=M-1")

        # *addr = *SP
        cmds.append("@SP")
        cmds.append("A=M")
        cmds.append("D=M")
        cmds.append("@addr")
        cmds.append("A=M")
        cmds.append("M=D")

        return cmds

    def _get_pop_that_commands(self, arg):
        cmds = []

        # addr = THAT + i
        cmds.append("@THAT")
        cmds.append("D=M")
        cmds.append("@{}".format(arg))
        cmds.append("D=D+A")
        cmds.append("@addr")
        cmds.append("M=D")

        # SP--
        cmds.append("@SP")
        cmds.append("M=M-1")

        # *addr = *SP
        cmds.append("@SP")
        cmds.append("A=M")
        cmds.append("D=M")
        cmds.append("@addr")
        cmds.append("A=M")
        cmds.append("M=D")

        return cmds

    def _get_pop_static_commands(self, arg):
        static_variable_name = self.asm_file_name.split('.')[0]
        cmds = []

        # D = SP.pop()
        cmds.append("@SP")
        cmds.append("A=M-1")
        cmds.append("D=M")

        # SP--
        cmds.append("@SP")
        cmds.append("M=M-1")

        # Filename.arg=D
        cmds.append("@{}.{}".format(static_variable_name, arg))
        cmds.append("M=D")

        return cmds

    def _get_pop_temp_commands(self, arg):
        cmds = []

        # addr =  TEMP_BASE_ADDRESS + i
        cmds.append("@{}".format(self.temp_segment_base_address))
        cmds.append("D=A")
        cmds.append("@{}".format(arg))
        cmds.append("D=D+A")
        cmds.append("@addr")
        cmds.append("M=D")

        # SP--
        cmds.append("@SP")
        cmds.append("M=M-1")

        # *addr = *SP
        cmds.append("@SP")
        cmds.append("A=M")
        cmds.append("D=M")
        cmds.append("@addr")
        cmds.append("A=M")
        cmds.append("M=D")

        return cmds

    def _get_pop_pointer_commands(self, arg):
        should_access_this = arg == '0'

        cmds = []

        # SP--
        cmds.append("@SP")
        cmds.append("M=M-1")

        # D = *SP
        cmds.append("@SP")
        cmds.append("A=M")
        cmds.append("D=M")

        # THIS/THAT = *SP
        cmds.append("@{}".format("THIS")) if should_access_this else cmds.append("@{}".format("THAT"))
        cmds.append("M=D")

        return cmds

    def write_asm_commands(self, asm_commands):
        for asm_command in asm_commands:
            self.asm_file.write(asm_command)
            self.asm_file.write("\n")

    def close(self):
        self.asm_file.close()
