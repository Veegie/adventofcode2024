import re

sum = 0
mul_active = True
with open('input.txt') as file:
    for line in file:
        dont_cmds: list[re.Match] = [match for match in re.finditer(r'don\'t\(\)', line)]
        do_cmds: list[re.Match] = [match for match in re.finditer(r'do\(\)', line)]
        
        if mul_active:
            active_indices = [[0]]
        elif len(do_cmds) > 0:
            active_indices = [[do_cmds[0].end()]]
            del do_cmds[0]
        else:
            continue
        
        mul_active = True
        while len(dont_cmds) > 0:
            while len(dont_cmds) > 0 and dont_cmds[0].start() < active_indices[-1][0]:
                del dont_cmds[0]
            if len(dont_cmds) > 0:
                active_indices[-1].append(dont_cmds[0].start())
                del dont_cmds[0]
                while len(do_cmds) > 0 and do_cmds[0].start() < active_indices[-1][1]:
                    del do_cmds[0]
                if len(do_cmds) > 0:
                    active_indices.append([do_cmds[0].end()])
                    del do_cmds[0]
        
        if len(active_indices[-1]) == 1:
            active_indices[-1].append(len(line))
            mul_active = True
        elif active_indices[-1][1] != len(line):
            mul_active = False
        
        active_ranges = [range(i[0],i[1]+1) for i in active_indices]
        
        for mul in re.finditer(r'(?<=mul\()\d+,\d+(?=\))', line):
            while len(active_ranges) > 0 and mul.start() > active_ranges[0].stop:
                del active_ranges[0]
            if len(active_ranges) == 0:
                break
            if mul.start() > active_ranges[0].start:
                ops = mul[0].split(',')
                sum += int(ops[0]) * int(ops[1])
            
print(sum)