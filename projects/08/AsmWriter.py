class AsmWriter(object):
    def __init__(self, asm_file_name):
        self.asm_file_name = asm_file_name
        self.asm_file = open(asm_file_name, 'a')
        self.eq_counter, self.gt_counter, self.lt_counter = 0, 0, 0
        self.temp_segment_base_address = 5
        self.ret_idx = 0

    def set_file_name(self, name):
        self.current_vm_file_name = name.split("/")[-1]

    def write_init(self):
        cmds = []

        # Add comment
        cmds.append("// Bootstrap code")

        cmds.append("@256")
        cmds.append("D=A")
        cmds.append("@SP")
        cmds.append("M=D")
        cmds += self.write_call("Sys.init", 0)

        return cmds

    def write_arithmetic(self, vm_command):
        cmds = []

        # Add comment
        cmds.append("// {}".format(vm_command))

        if vm_command == "add":
            cmds += self._get_add_commands()
        elif vm_command == "sub":
            cmds += self._get_sub_commands()
        elif vm_command == "neg":
            cmds += self._get_neg_commands()
        elif vm_command == "eq":
            cmds += self._get_eq_commands()
        elif vm_command == "gt":
            cmds += self._get_gt_commands()
        elif vm_command == "lt":
            cmds += self._get_lt_commands()
        elif vm_command == "and":
            cmds += self._get_and_commands()
        elif vm_command == "or":
            cmds += self._get_or_commands()
        elif vm_command == "not":
            cmds += self._get_not_commands()
        else:
            print("invalid arithmetic/logical command!")
            return

        return cmds

    def write_push_pop(self, vm_command, memory_segment, arg):
        cmds = []

        # Add comment
        cmds.append("// {} {} {}".format(vm_command, memory_segment, arg))

        if vm_command == "push":
            if memory_segment == "constant":
                cmds += self._get_push_constant_commands(arg)
            elif memory_segment == "local":
                cmds += self._get_push_local_commands(arg)
            elif memory_segment == "argument":
                cmds += self._get_push_argument_commands(arg)
            elif memory_segment == "this":
                cmds += self._get_push_this_commands(arg)
            elif memory_segment == "that":
                cmds += self._get_push_that_commands(arg)
            elif memory_segment == "static":
                cmds += self._get_push_static_commands(arg)
            elif memory_segment == "temp":
                cmds += self._get_push_temp_commands(arg)
            elif memory_segment == "pointer":
                cmds += self._get_push_pointer_commands(arg)
            else:
                print("invalid memory access command!")
                return
        elif vm_command == "pop":
            if memory_segment == "local":
                cmds += self._get_pop_local_commands(arg)
            elif memory_segment == "argument":
                cmds += self._get_pop_argument_commands(arg)
            elif memory_segment == "this":
                cmds += self._get_pop_this_commands(arg)
            elif memory_segment == "that":
                cmds += self._get_pop_that_commands(arg)
            elif memory_segment == "static":
                cmds += self._get_pop_static_commands(arg)
            elif memory_segment == "temp":
                cmds += self._get_pop_temp_commands(arg)
            elif memory_segment == "pointer":
                cmds += self._get_pop_pointer_commands(arg)
            else:
                print("invalid memory access command!")
                return

        return cmds

    def write_label(self, label_name):
        cmds = []

        # Add comment
        cmds.append("// label {} ".format(label_name))
        cmds.append("({}${})".format(self.asm_file_name, label_name))

        return cmds

    def write_goto(self, label_name):
        cmds = []

        # Add comment
        cmds.append("// goto {} ".format(label_name))
        cmds.append("@{}${}".format(self.asm_file_name, label_name))
        cmds.append("0;JMP")

        return cmds

    def write_if_goto(self, label_name):
        cmds = []

        # Add comment
        cmds.append("// if-goto {} ".format(label_name))
        cmds.append("@SP")
        cmds.append("A=M-1")
        cmds.append("D=M")
        cmds.append("@SP")
        cmds.append("M=M-1")
        cmds.append("@{}${}".format(self.asm_file_name, label_name))
        cmds.append("D;JNE")

        return cmds

    def write_function(self, function_name, num_vars):
        cmds = []

        # Add comment
        cmds.append("// function {} {}".format(function_name, num_vars))
        cmds.append("({})".format(function_name))

        for i in range(int(num_vars)):
            cmds += self._get_push_constant_commands(0)

        return cmds

    def write_return(self):
        cmds = []

        # Add comment
        cmds.append("// return")

        # endFrame = LCL
        cmds.append("@LCL")
        cmds.append("D=M")
        cmds.append("@endFrame")
        cmds.append("M=D")

        # retAddr = *(endFrame - 5)
        cmds.append("@5")
        cmds.append("D=A")
        cmds.append("@endFrame")
        cmds.append("D=M-D")
        cmds.append("A=D")
        cmds.append("D=M")
        cmds.append("@retAddr")
        cmds.append("M=D")

        # *ARG = pop()
        cmds.append("@SP")
        cmds.append("M=M-1")
        cmds.append("@SP")
        cmds.append("A=M")
        cmds.append("D=M")
        cmds.append("@ARG")
        cmds.append("A=M")
        cmds.append("M=D")

        # SP = ARG + 1
        cmds.append("@ARG")
        cmds.append("D=M+1")
        cmds.append("@SP")
        cmds.append("M=D")

        # THAT = *(endFrame - 1)
        cmds.append("@1")
        cmds.append("D=A")
        cmds.append("@endFrame")
        cmds.append("D=M-D")
        cmds.append("A=D")
        cmds.append("D=M")
        cmds.append("@THAT")
        cmds.append("M=D")

        # THIS = *(endFrame - 2)
        cmds.append("@2")
        cmds.append("D=A")
        cmds.append("@endFrame")
        cmds.append("D=M-D")
        cmds.append("A=D")
        cmds.append("D=M")
        cmds.append("@THIS")
        cmds.append("M=D")

        # ARG = *(endFrame - 3)
        cmds.append("@3")
        cmds.append("D=A")
        cmds.append("@endFrame")
        cmds.append("D=M-D")
        cmds.append("A=D")
        cmds.append("D=M")
        cmds.append("@ARG")
        cmds.append("M=D")

        # LCL = *(endFrame - 4)
        cmds.append("@4")
        cmds.append("D=A")
        cmds.append("@endFrame")
        cmds.append("D=M-D")
        cmds.append("A=D")
        cmds.append("D=M")
        cmds.append("@LCL")
        cmds.append("M=D")

        # goto retAddr
        cmds.append("@retAddr")
        cmds.append("A=M")
        cmds.append("0;JMP")

        return cmds

    def write_call(self, function_name, n_args):
        #  We need to keep a running count of each time we hit a "call" instruction for a given function_name
        # if function_name in self.function_name_to_ret_idx:
        #     self.function_name_to_ret_idx[function_name] = self.function_name_to_ret_idx[function_name] + 1
        # else:
        #     self.function_name_to_ret_idx[function_name] = 1

        # ret_idx = self.function_name_to_ret_idx[function_name]
        self.ret_idx = self.ret_idx + 1
        ret_idx = self.ret_idx

        cmds = []

        # Add comment
        cmds.append("// call {} {}".format(function_name, n_args))

        # push return address
        return_address = "{}$ret{}".format(function_name, ret_idx)
        cmds.append("@{}".format(return_address))
        cmds.append("D=A")
        cmds.append("@SP")
        cmds.append("A=M")
        cmds.append("M=D")
        cmds.append("@SP")
        cmds.append("M=M+1")

        # push LCL
        cmds.append("@LCL")
        cmds.append("D=M")
        cmds.append("@SP")
        cmds.append("A=M")
        cmds.append("M=D")
        cmds.append("@SP")
        cmds.append("M=M+1")

        # push ARG
        cmds.append("@ARG")
        cmds.append("D=M")
        cmds.append("@SP")
        cmds.append("A=M")
        cmds.append("M=D")
        cmds.append("@SP")
        cmds.append("M=M+1")

        # push THIS
        cmds.append("@THIS")
        cmds.append("D=M")
        cmds.append("@SP")
        cmds.append("A=M")
        cmds.append("M=D")
        cmds.append("@SP")
        cmds.append("M=M+1")

        # push THAT
        cmds.append("@THAT")
        cmds.append("D=M")
        cmds.append("@SP")
        cmds.append("A=M")
        cmds.append("M=D")
        cmds.append("@SP")
        cmds.append("M=M+1")

        # ARG = SP - 5 - n_args
        cmds.append("@{}".format(n_args))
        cmds.append("D=A")
        cmds.append("@5")
        cmds.append("D=D+A")
        cmds.append("@SP")
        cmds.append("D=M-D")
        cmds.append("@ARG")
        cmds.append("M=D")

        # LCL = SP
        cmds.append("@SP")
        cmds.append("D=M")
        cmds.append("@LCL")
        cmds.append("M=D")

        # goto function_name
        cmds.append("@{}".format(function_name))
        cmds.append("0;JMP")

        # add returnAddress to cmds
        cmds.append("({})".format(return_address))

        return cmds

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
        static_variable_name = self.current_vm_file_name.split('.')[0]
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
        static_variable_name = self.current_vm_file_name.split('.')[0]
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
