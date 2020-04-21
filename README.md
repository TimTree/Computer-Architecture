# Computer Architecture

## Project

* [Implement the LS-8 Emulator](ls8/)

## Task List: add this to the first comment of your Pull Request

call.ls8: Use the call command to run a subroutine that prints a number in a register multiplied by 2
interrupts.ls8: Prints the letter A once a second
keyboard.ls8: Program that tests the keyboard
mult.ls8: Multiplies 8 by 9 to get 72
print8.ls8: Prints the number 8
printstr.ls8: Prints the string, "Hello, world!"
sctest.ls8: Sprint challenge test
stack.ls8: Test stacks
stackoverflow.ls8: Test stack overflows
cpu.py: Our emulated CPU that can run programs from the ls8 (from the machine code)
ls8.py: Main script to run the emulated CPU

### Day 1: Get `print8.ls8` running

- [ ] Inventory what is here
- [ ] Implement the `CPU` constructor
- [ ] Add RAM functions `ram_read()` and `ram_write()`
- [ ] Implement the core of `run()`
- [ ] Implement the `HLT` instruction handler
- [ ] Add the `LDI` instruction
- [ ] Add the `PRN` instruction

### Day 2: Add the ability to load files dynamically, get `mult.ls8` running

- [ ] Un-hardcode the machine code
- [ ] Implement the `load()` function to load an `.ls8` file given the filename
      passed in as an argument
- [ ] Implement a Multiply instruction (run `mult.ls8`)

### Day 3: Stack

- [ ] Implement the System Stack and be able to run the `stack.ls8` program

### Day 4: Get `call.ls8` running

- [ ] Implement the CALL and RET instructions
- [ ] Implement Subroutine Calls and be able to run the `call.ls8` program

### Stretch

- [ ] Add the timer interrupt to the LS-8 emulator
- [ ] Add the keyboard interrupt to the LS-8 emulator
- [ ] Write an LS-8 assembly program to draw a curved histogram on the screen
