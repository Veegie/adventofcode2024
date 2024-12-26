keys: list[tuple[int,int,int,int,int]] = list()
locks: list[tuple[int,int,int,int,int]] = list()

on_lock = False
with open('input.txt') as file:
    for ln, line in enumerate(file):
        if len(line) == 1:
            if on_lock:
                locks.append(tuple(cur_list))
            else:
                keys.append(tuple(cur_list))
        elif (ln % 8 == 0 or ln == 0):
            on_lock = line[0] == '#'
            cur_list = [0]*5 if on_lock else [-1]*5
        else:
            for i, c in enumerate(line.rstrip('\n')):
                if c == '#':
                    cur_list[i] += 1

if on_lock:
    locks.append(tuple(cur_list))
else:
    keys.append(tuple(cur_list))

def fits(a: tuple[int], b: tuple[int]) -> bool:
    for i in range(5):
        if a[i] + b[i] > 5:
            return False
    return True

def count_fits(a: set[tuple[int,int,int,int,int]], b: set[tuple[int,int,int,int,int]]) -> int:
    fit_count = 0
    for entry in a:
        for other in b:
            if fits(entry, other):
                fit_count += 1
    return fit_count

print(keys)
print(locks)
fit_count = count_fits(keys, locks) if len(keys) < len(locks) else count_fits(locks, keys)

print('Part 1:', fit_count)