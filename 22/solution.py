bimillenial_secret_sum = 0

histories: dict[int, dict[int, int]] = dict()
sells_at: dict[int, dict[tuple[int, int, int, int], int]] = dict()
signals: set[tuple[int, int, int, int]] = set()

prune = 16777216
with open('input.txt') as file:
    for monkey, line in enumerate(file):
        histories[monkey] = dict()
        sells_at[monkey] = dict()
        num = int(line.rstrip('\n'))
        for i in range(2000):
            t = num * 64
            num ^= t
            num %= prune
            t = num // 32
            num ^= t
            num %= prune
            t = num * 2048
            num ^= t
            num %= prune
            histories[monkey][i] = num % 10
            if i > 3:
                m3 = histories[monkey][i-3] - histories[monkey][i-4]
                m2 = histories[monkey][i-2] - histories[monkey][i-3]
                m1 = histories[monkey][i-1] - histories[monkey][i-2]
                m0 = histories[monkey][i] - histories[monkey][i-1]
                signal = (m3, m2, m1, m0)
                if signal not in sells_at[monkey]:
                    sells_at[monkey][(m3, m2, m1, m0)] = histories[monkey][i]
                    signals.add((m3, m2, m1, m0))
        bimillenial_secret_sum += num

max_profit = 0
for signal in signals:
    profit = 0
    for monkey in range(len(histories)):
        if signal in sells_at[monkey]:
            profit += sells_at[monkey][signal]
    if profit > max_profit:
        max_profit = profit

print('Part 1: ', bimillenial_secret_sum)
print('Part 2: ', max_profit)
