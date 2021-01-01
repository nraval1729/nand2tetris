// R0, R1 = R1, R0

    @R0
    D = M  // D = R0

    @temp
    M = D // temp = R0

    @R1
    D = M // D = R1

    @R0
    M = D // R0 = R1

    @temp
    D = M

    @R1
    M = D // R1 = temp

  (END)
    @END
    0; JMP