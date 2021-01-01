// Adds 1 + 2 + 3 + ... + n
// where n is stored in R0 and the output is stored in R1

    @R0
    D = M

    @i
    M = D // i = n

    @sum
    M = 0 // sum = 0

  (LOOP)
    @i
    D = M

    @STOP
    D; JLE // if i<=0 goto STOP

    @i
    D = M

    @sum
    M = D + M // sum += n

    @i
    M = M - 1 // i -= 1

    @LOOP
    0; JMP


  (STOP)
    @sum
    D = M

    @R1
    M = D // R1 = sum

    @END
    0; JMP

  (END)
    @END
    0; JMP