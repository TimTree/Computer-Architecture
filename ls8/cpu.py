"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.program_filename = sys.argv[1]

        self.branchtable = {}
        self.branchtable[HLT] = self.handle_hlt
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[MUL] = self.handle_mul
        self.branchtable[PUSH] = self.handle_push
        self.branchtable[POP] = self.handle_pop

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
