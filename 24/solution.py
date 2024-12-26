wires: dict[str, int] = dict()
awaiting_operands: dict[str, tuple[str,str,str, list[str]]] = dict()
operations_performed: dict[tuple[str,str,str],str] = dict()
ops_performed_reverse: dict[str,tuple[str,str,str]] = dict()

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
            new_wire = expr[4]
            if op1 in wires and op2 in wires:
                wires[new_wire] = do(wires[op1], operation, wires[op2])
                operations_performed[(op1, operation, op2)] = new_wire
                ops_performed_reverse[new_wire] = (op1, operation, op2)
            else:
                missing_ops = [op for op in [op1, op2] if op not in wires]
                awaiting_operands[new_wire] = (op1, operation, op2, missing_ops)
            if new_wire.startswith('z'):
                z_wires.append(new_wire)

while len(awaiting_operands) > 0:
    to_remove = list()
    for res,exp in awaiting_operands.items():
        if exp[0] in wires and exp[2] in wires:
            wires[res] = do(wires[exp[0]], exp[1], wires[exp[2]])
            operations_performed[(exp[0], exp[1], exp[2])] = res
            ops_performed_reverse[res] = (exp[0], exp[1], exp[2])
            to_remove.append(res)
    for rem in to_remove:
        del awaiting_operands[rem]

z_wires.sort(reverse=True)
z_val = ''
for z in z_wires:
    z_val += str(wires[z])

inputs_count //= 2

def check_potential_swapped_wires() -> set[str]:
    potential_swapped_output_wires: set[str] = set()
    wire_num = str(0).zfill(2)
    x_wire = 'x' + wire_num
    y_wire = 'y' + wire_num
    z_wire = 'z' + wire_num

    expected_a_op = get_op(x_wire, 'XOR', y_wire)
    expected_d_op = get_op(x_wire, 'AND', y_wire)

    sum_op = ops_performed_reverse[z_wire]
    if sum_op[1] != 'XOR':
        potential_swapped_output_wires.add(z_wire)
    
    a_wire = sum_op[0]
    a_op = ops_performed_reverse[a_wire]
    if a_op != expected_a_op:
        a_wire = sum_op[2]
        a_op = ops_performed_reverse[a_wire]
        if a_op != expected_a_op:
            print('bluh')
            # NOW idk

    def get_op(wire1, operation, wire2) -> tuple[str,str,str] | None:
        op = (wire1, operation, wire2)
        if op not in operations_performed:
            op = (wire2, operation, wire1)
        if op not in operations_performed:
            return None
        return op

    a_op = get_op(x_wire, 'XOR', y_wire)
    a_wire = operations_performed[a_op]

    d_op = get_op(x_wire, 'AND', y_wire)
    d_wire = operations_performed[d_op]

    carry_in_wire = operations_performed[d_op]
    if operations_performed[a_op] != 'z' + wire_num:
        potential_swapped_output_wires.append('z' + wire_num)

    for i in range(1, inputs_count):
        wire_num = str(i).zfill(2)
        x_wire = 'x' + wire_num
        y_wire = 'y' + wire_num
        
        a_op = get_op(x_wire, 'XOR', y_wire)
        a_wire = operations_performed[a_op]
        
        d_op = get_op(x_wire, 'AND', y_wire)
        d_wire = operations_performed[d_op]

        sum_op = get_op(carry_in_wire, 'XOR', a_wire)
        if sum_op == None:
            potential_swapped_output_wires.add(a_wire)
            potential_swapped_output_wires.add(carry_in_wire)
        elif operations_performed[sum_op] != 'z' + wire_num:
            potential_swapped_output_wires.add('z' + wire_num)
        
        b_op = get_op(a_wire, 'AND', carry_in_wire)
        if b_op == None:
            potential_swapped_output_wires.add(a_wire)
            potential_swapped_output_wires.add(carry_in_wire)
        else:
            b_wire = operations_performed[b_op]
        
        carry_out_op = get_op(b_wire, 'OR', d_wire)
        if carry_out_op == None:
            potential_swapped_output_wires.add(a_wire)
            potential_swapped_output_wires.add(carry_in_wire)
        else:
            carry_in_wire = operations_performed[carry_out_op]
    
    return potential_swapped_output_wires

potential_swapped_wires = check_potential_swapped_wires()


print('Part 1:', int(z_val,base=2))