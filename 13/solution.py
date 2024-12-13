from scipy import optimize
import re

objective_coeff = [3, 1]
eq_coeff = [[0, 0], [0, 0]]
prize = [0, 0]
min_tokens = 0
min_tokens_part_2 = 0
with open('input.txt') as file:
    for line_num, line in enumerate(file):
        parts = re.split(',? ', line.rstrip('\n'))
        if len(parts) == 1:
            continue
        match(parts[0]):
            case'Button':
                if parts[1] == 'A:':
                    eq_coeff[0][0] = int(parts[2][2:])
                    eq_coeff[1][0] = int(parts[3][2:])
                else:
                    eq_coeff[0][1] = int(parts[2][2:])
                    eq_coeff[1][1] = int(parts[3][2:])
            case'Prize:':
                prize[0] = int(parts[1][2:])
                prize[1] = int(parts[2][2:])
                res: optimize.OptimizeResult = optimize.linprog(
                    objective_coeff, A_eq=eq_coeff, b_eq=prize, integrality=1)
                if res.success:
                    min_tokens += res.x[0] * 3 + res.x[1]
                prize[0] += 10000000000000
                prize[1] += 10000000000000
                res = optimize.linprog(objective_coeff, A_eq=eq_coeff, b_eq=prize, options={
                                       'presolve': False}, integrality=1)
                if res.success:
                    min_tokens_part_2 += res.x[0] * 3 + res.x[1]


print('Part 1:', min_tokens)
print('Part 2:', min_tokens_part_2)
