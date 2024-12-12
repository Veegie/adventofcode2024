def is_safe_report(report, secondary):
    if len(report) < 2:
        return True
    cur = int(report[1])
    prev = int(report[0])
    diff = cur - prev
    if diff == 0 or abs(diff) > 3:
        if secondary:
            return False
        else:
            return is_safe_report(report[1:], True) or is_safe_report(report[0:1] + report[2:], True)
    if diff > 0:
        ascending = True
    else:
        ascending = False
    for i in range(2, len(report)):
        prev = cur
        cur = int(report[i])
        diff = cur - prev
        if (ascending and diff < 0) or (not ascending and diff > 0) or (diff == 0 or abs(diff) > 3):
            if secondary:
                return False
            else:
                return is_safe_report(report[:i] + report[i+1:], True) or is_safe_report(report[:i-1] + report[i:], True)
    return True

safe_count = 0
with open('input.txt') as file:
    for line in file:
        report = line.split()
        if is_safe_report(report, False) or is_safe_report(report[1:], True):
            safe_count += 1

print(safe_count)