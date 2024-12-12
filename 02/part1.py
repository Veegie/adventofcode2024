def is_safe_report(report):
    if len(report) < 2:
        return True
    cur = int(report[1])
    prev = int(report[0])
    diff = cur - prev
    if diff == 0 or abs(diff) > 3:
        return False
    if diff > 0:
        ascending = True
    else:
        ascending = False
    for i in range(2, len(report)):
        prev = cur
        cur = int(report[i])
        diff = cur - prev
        if ascending and diff < 0:
            return False
        elif not ascending and diff > 0:
            return False
        if diff == 0 or abs(diff) > 3:
            return False
    return True

safe_count = 0
with open('input.txt') as file:
    for line in file:
        report = line.split()
        if is_safe_report(report):
            safe_count += 1

print(safe_count)