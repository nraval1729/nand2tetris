// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

    @R0
    D = M

    @first
    M = D // first = R0

    @R1
    D = M

    @second
    M = D // second = R1

    @product
    M = 0 // product = 0


  (LOOP)
    @second
    D = M

    @STOP
    D; JLE // if second <=0 goto STOP

    @first
    D = M

    @product
    M = D + M // product += first

    @second
    M = M - 1 // second -= 1

    @LOOP
    0; JMP


  (STOP)
    @product
    D = M

    @R2
    M = D

    @END
    0; JMP

  (END)
    @END
    0; JMP
