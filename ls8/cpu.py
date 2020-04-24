"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
ADD = 0b10100000
RET = 0b00010001
CMP = 0b10100111
JNE = 0b01010110
JEQ = 0b01010101
JMP = 0b01010100


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.fl = 0b00000000
        self.program_filename = sys.argv[1]

        self.branchtable = {}
        self.branchtable[HLT] = self.handle_hlt
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[MUL] = self.handle_mul
        self.branchtable[PUSH] = self.handle_push
        self.branchtable[POP] = self.handle_pop
        self.branchtable[CALL] = self.handle_call
        self.branchtable[ADD] = self.handle_add
        self.branchtable[RET] = self.handle_ret
        self.branchtable[CMP] = self.handle_cmp
        self.branchtable[JEQ] = self.handle_jeq
        self.branchtable[JNE] = self.handle_jne
        self.branchtable[JMP] = self.handle_jmp

        # Stack pointer location is in position 7 of the register per the spec
        self.SP = 7

        # The stack by default points to address 0xF4
        self.reg[self.SP] = 0xF4

    def handle_hlt(self):
        sys.exit()

    def handle_ldi(self):
        reg_num = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.reg[reg_num] = value
        self.pc += 3

    def handle_prn(self):
        print(self.reg[self.ram_read(self.pc + 1)])
        self.pc += 2

    def handle_mul(self):
        value0 = self.reg[self.ram_read(self.pc + 1)]
        value1 = self.reg[self.ram_read(self.pc + 2)]
        self.reg[self.ram_read(self.pc + 1)] = value0 * value1
        self.pc += 3

    def handle_push(self):
        self.reg[self.SP] -= 1  # Decrement SP
        self.ram_write(self.reg[self.SP], self.reg[self.ram_read(self.pc + 1)])
        self.pc += 2

    def handle_pop(self):
        self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.reg[self.SP])
        self.reg[self.SP] += 1  # Increment SP
        self.pc += 2

    def handle_call(self):
        # The address of the ***instruction*** _directly after_ `CALL` is
        # pushed onto the stack.

        self.reg[self.SP] -= 1  # Decrement SP
        self.ram_write(self.reg[self.SP], (self.pc + 2))
        # The PC is set to the address stored in the given register.
        self.pc = self.reg[self.ram_read(self.pc + 1)]
        
        # self.pc += 2

    def handle_add(self):
        value0 = self.reg[self.ram_read(self.pc + 1)]
        value1 = self.reg[self.ram_read(self.pc + 2)]
        self.reg[self.ram_read(self.pc + 1)] = value0 + value1
        self.pc += 3

    def handle_ret(self):
        # Pop the value from the top of the stack and store it in the `PC`.
        self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.reg[self.SP])
        self.pc = self.ram_read(self.reg[self.SP])
        self.reg[self.SP] += 1  # Increment SP
    
    def handle_cmp(self):
        value0 = self.reg[self.ram_read(self.pc + 1)]
        value1 = self.reg[self.ram_read(self.pc + 2)]
        if value0 == value1:
            self.fl = 0b00000001
        elif value0 > value1:
            self.fl = 0b00000010
        else:
            self.fl = 0b00000100
        print(bin(self.fl))
        self.pc += 3

    def handle_jeq(self):
        if self.fl & 0b00000001 == 1:  # equal
            self.pc = self.reg[self.ram_read(self.pc + 1)]
        else:  # not equal
            self.pc += 2

    def handle_jne(self):
        if self.fl & 0b00000001 == 0:  # not equal
            self.pc = self.reg[self.ram_read(self.pc + 1)]
        else:  # equal
            self.pc += 2

    def handle_jmp(self):
        self.pc = self.reg[self.ram_read(self.pc + 1)]

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        with open(self.program_filename) as f:
            for line in f:
                line = line.split('#')
                line = line[0].strip()
                if line == '':
                    continue

                self.ram_write(address, int(line, 2))
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""

        while True:
            ir = self.ram_read(self.pc)
            try:
                self.branchtable[ir]()
            except KeyError:
                print("Unknown instruction")
                self.handle_hlt()
