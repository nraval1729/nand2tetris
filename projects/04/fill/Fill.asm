// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
  (LOOP)
    @8191
    D = A

    @screenLimit
    M = D // screenLimit = 8191

    @SCREEN
    D = A

    @addr
    M = D // addr = SCREEN (16384)

    @KBD
    D = M

    @WHITENLOOP
    D; JEQ  // If KBD=0, that means no key is pressed which means we need to whiten screen

    (BLACKENLOOP)
      @screenLimit
      D = M

      @CONTINUE
      D; JLE  // If screenLimit <=0, All rows have been blackened, so now continue with the outer loop

      @addr
      A = M
      M = -1 // Blacken the row pointed by addr

      @screenLimit
      M = M - 1 // screenLimit -= 1

      @addr
      M = M + 1 // addr += 1

      @BLACKENLOOP
      0; JMP  // goto BLACKENLOOP


    (WHITENLOOP)
      @screenLimit
      D = M

      @CONTINUE
      D; JLE  // If screenLimit <=0, All rows have been whitened, so now continue with the outer loop

      @addr
      A = M
      M = 0 // Whiten the row pointed by addr

      @screenLimit
      M = M - 1 // screenLimit -= 1

      @addr
      M = M + 1 // addr += 1

      @WHITENLOOP
      0; JMP  // goto WHITENLOOP


  (CONTINUE)
    @LOOP
    0; JMP

@LOOP
0; JMP