def seven_bit_cpu(a: int, b: int, c: int, ops: list[int]) -> str:
    registers: dict[str, int] = {'a': a, 'b': b, 'c': c}

    def dv(op: int, reg: str) -> None:
        """
        Divide A by 2^op. Store in specified register
        """
        if op < 4:
            registers[reg] = int(registers['a'] / 2**op)
        elif op == 4:
            registers[reg] = int(registers['a'] / 2**registers['a'])
        elif op == 5:
            registers[reg] = int(registers['a'] / 2**registers['b'])
        elif op == 6:
            registers[reg] = int(registers['a'] / 2**registers['c'])

    def bxl(lop: int) -> None:
        """
        B xor lop. store in B
        """
        registers['b'] = registers['b'] ^ lop

    def mod_8(op: int) -> int:
        if op < 4:
            return op % 8
        elif op == 4:
            return registers['a'] % 8
        elif op == 5:
            return registers['b'] % 8
        elif op == 6:
            return registers['c'] % 8

    def bst(op: int) -> None:
        """
        op mod 8, store in B
        """
        registers['b'] = mod_8(op)

    def bxc(_: int) -> None:
        """
        B xor C. store in B
        """
        registers['b'] = registers['b'] ^ registers['c']

    def out(op: int) -> str:
        """
        mod 8 op, then output
        """
        val = mod_8(op)
        if len(output) == 0:
            return str(val)
        else:
            return ',' + str(val)

    ip = 0
    output = ''
    while ip < len(ops) - 1:
        opcode = ops[ip]
        operand = ops[ip+1]
        match(opcode):
            case 0:
                dv(operand, 'a')
            case 1:
                bxl(operand)
            case 2:
                bst(operand)
            case 3:
                if registers['a'] != 0:
                    ip = operand-2
            case 4:
                bxc(operand)
            case 5:
                output += out(operand)
            case 6:
                dv(operand, 'b')
            case 7:
                dv(operand, 'c')
        ip += 2

    return output


a, b, c = 0, 0, 0

with open('input.txt') as file:
    for line_num, line in enumerate(file):
        if line_num == 0:
            a = int(line.rstrip('\n').split(': ')[1])
        if line_num == 1:
            b = int(line.rstrip('\n').split(': ')[1])
        if line_num == 2:
            c = int(line.rstrip('\n').split(': ')[1])
        if line_num == 4:
            input_program = line.rstrip('\n').split(': ')[1]
            ops = [int(o) for o in input_program if o != ',']

print('Part 1: ', seven_bit_cpu(a, b, c, ops))

a = 0
output = ''
next_op_index_to_match = len(ops)-1
while next_op_index_to_match > -1:
    output = seven_bit_cpu(a, b, c, ops)
    expected = ','.join(str(i) for i in ops[next_op_index_to_match:])
    while output != expected:
        back_steps = 0
        for i in range(2, len(output), 2):
            if output[i] != expected[i]:
                back_steps = i//2
        if back_steps > 0:
            for _ in range(0, back_steps):
                a -= a % 8
                a //= 8
                next_op_index_to_match += 1
            expected = ','.join(str(i) for i in ops[next_op_index_to_match:])
        else:
            a += 1
        output = seven_bit_cpu(a, b, c, ops)
    next_op_index_to_match -= 1
    if next_op_index_to_match > -1:
        a *= 8

print('Part 2: ', a)
