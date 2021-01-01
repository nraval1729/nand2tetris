// push argument 1
@ARG
D=M
@1
D=D+A
@addr
M=D
@addr
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1
@SP
M=M-1
@SP
A=M
D=M
@THAT
M=D
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop that 0
@THAT
D=M
@0
D=D+A
@addr
M=D
@SP
M=M-1
@SP
A=M
D=M
@addr
A=M
M=D
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop that 1
@THAT
D=M
@1
D=D+A
@addr
M=D
@SP
M=M-1
@SP
A=M
D=M
@addr
A=M
M=D
// push argument 0
@ARG
D=M
@0
D=D+A
@addr
M=D
@addr
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
A=M-1
D=-M
A=A-1
D=D+M
M=D
@SP
M=M-1
// pop argument 0
@ARG
D=M
@0
D=D+A
@addr
M=D
@SP
M=M-1
@SP
A=M
D=M
@addr
A=M
M=D
// label MAIN_LOOP_START 
(FibonacciSeries.asm$MAIN_LOOP_START)
// push argument 0
@ARG
D=M
@0
D=D+A
@addr
M=D
@addr
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// if-goto COMPUTE_ELEMENT 
@SP
A=M-1
D=M
@SP
M=M-1
@FibonacciSeries.asm$COMPUTE_ELEMENT
D;JNE
// goto END_PROGRAM 
@FibonacciSeries.asm$END_PROGRAM
0;JMP
// label COMPUTE_ELEMENT 
(FibonacciSeries.asm$COMPUTE_ELEMENT)
// push that 0
@THAT
D=M
@0
D=D+A
@addr
M=D
@addr
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// push that 1
@THAT
D=M
@1
D=D+A
@addr
M=D
@addr
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
A=M-1
D=M
A=A-1
D=D+M
M=D
@SP
M=M-1
// pop that 2
@THAT
D=M
@2
D=D+A
@addr
M=D
@SP
M=M-1
@SP
A=M
D=M
@addr
A=M
M=D
// push pointer 1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
A=M-1
D=M
A=A-1
D=D+M
M=D
@SP
M=M-1
// pop pointer 1
@SP
M=M-1
@SP
A=M
D=M
@THAT
M=D
// push argument 0
@ARG
D=M
@0
D=D+A
@addr
M=D
@addr
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
A=M-1
D=-M
A=A-1
D=D+M
M=D
@SP
M=M-1
// pop argument 0
@ARG
D=M
@0
D=D+A
@addr
M=D
@SP
M=M-1
@SP
A=M
D=M
@addr
A=M
M=D
// goto MAIN_LOOP_START 
@FibonacciSeries.asm$MAIN_LOOP_START
0;JMP
// label END_PROGRAM 
(FibonacciSeries.asm$END_PROGRAM)
