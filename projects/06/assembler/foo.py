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

print(parse_c_instruction('MD=D+1+'))