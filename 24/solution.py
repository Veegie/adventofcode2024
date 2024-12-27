wires: dict[str, int] = dict()
ops_performed: dict[tuple[str, str, str], str] = dict()
ops_performed_reverse: dict[str, tuple[str, str, str]] = dict()


def do(op1: int, operation: str, op2: int) -> int:
    if operation == 'AND':
        return op1 & op2
    elif operation == 'OR':
        return op1 | op2
    elif operation == 'XOR':
        return op1 ^ op2


inputs_count = 0

z_wires: list[str] = list()
initializing = True
operations: dict[tuple[str, str, str], str] = dict()

with open('input.txt') as file:
    for line in file:
        if initializing:
            if len(line) == 1:
                initializing = False
            else:
                expr = line.rstrip('\n').split(': ')
                wires[expr[0]] = int(expr[1])
                inputs_count += 1
        else:
            expr = line.rstrip('\n').split(' ')
            op1 = expr[0]
            operation = expr[1]
            op2 = expr[2]
            output_wire = expr[4]
            operations[(op1, operation, op2)] = output_wire
            if output_wire.startswith('z'):
                z_wires.append(output_wire)

inputs_count //= 2


def run_simulation(w: dict[str, int], operations: dict[tuple[str, str, str], str]) -> dict[str, int]:
    while len(operations) > 0:
        to_remove = list()
        for exp, res in operations.items():
            if exp[0] in w and exp[2] in w:
                op = (exp[0], exp[1], exp[2])
                w[res] = do(w[op[0]], op[1], w[op[2]])
                ops_performed[op] = res
                ops_performed_reverse[res] = op
                to_remove.append(op)
        for rem in to_remove:
            del operations[rem]
    return w


result = run_simulation(wires.copy(), operations)

z_wires.sort(reverse=True)
z_val = ''
for z in z_wires:
    z_val += str(result[z])

print('Part 1:', int(z_val, base=2))


def get_op(ops, wire1, operation, wire2) -> tuple[str, str, str] | None:
    op = (wire1, operation, wire2)
    if op not in ops:
        op = (wire2, operation, wire1)
    if op not in ops:
        return None
    return op


def find_defective_digits(ops: dict[tuple[str, str, str], str], wire_to_op: dict[str, tuple[str, str, str]]) -> set[str]:
    swapped: set[tuple[str, str]] = set()
    wire_num = str(0).zfill(2)
    x_wire = 'x' + wire_num
    y_wire = 'y' + wire_num
    z_wire = 'z' + wire_num

    x_xor_y_op = get_op(ops, x_wire, 'XOR', y_wire)
    z_op = wire_to_op[z_wire]
    if z_op != x_xor_y_op:
        if x_xor_y_op not in ops:
            print(ops)
            print(x_wire, y_wire)
        wrong_wire = ops[x_xor_y_op]
        ops[z_op] = wrong_wire
        ops[x_xor_y_op] = z_wire
        wire_to_op[z_wire] = x_xor_y_op
        wire_to_op[wrong_wire] = z_op

    carry_out_op = get_op(ops, x_wire, 'AND', y_wire)
    carry_out_wire = ops[carry_out_op]

    for i in range(1, inputs_count):
        wire_num = str(i).zfill(2)
        x_wire = 'x' + wire_num
        y_wire = 'y' + wire_num
        z_wire = 'z' + wire_num

        a_op = get_op(ops, x_wire, 'XOR', y_wire)
        a_wire = ops[a_op]

        d_op = get_op(ops, x_wire, 'AND', y_wire)
        d_wire = ops[d_op]

        found = False
        z_op = wire_to_op[z_wire]
        for op in ops.keys():
            if a_wire in op and op[1] == 'XOR':
                found = True
                if a_wire == op[0]:
                    carry_out_wire = op[2]
                else:
                    carry_out_wire = op[0]
        if not found:
            swapped.add((a_wire, d_wire))
            continue

        expected_z_op = get_op(ops, carry_out_wire, 'XOR', a_wire)
        if expected_z_op == None:
            print(z_op)
            print(wire_num, ' - expected ', carry_out_wire, ' XOR ', a_wire)
            continue
        if z_op != expected_z_op:
            wrong_wire = ops[expected_z_op]
            swapped.add((z_wire, wrong_wire))
            continue

        b_op = get_op(ops, a_wire, 'AND', carry_out_wire)
        b_wire = ops[b_op]

        carry_out_op = get_op(ops, b_wire, 'OR', d_wire)
        carry_out_wire = ops[carry_out_op]

    return swapped


swapped = find_defective_digits(
    ops_performed.copy(), ops_performed_reverse.copy())

answer = list()
for pair in swapped:
    answer.extend(list(pair))
answer.sort()
print('Part 2:', ','.join(answer))
