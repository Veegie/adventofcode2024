import re
bad_orderings: dict[int, dict[int, bool]] = dict()
rule_regex: re.Pattern = re.compile(r'\d+\|\d+')


def is_bad_order(order: list[int]) -> bool:
    for i in range(len(order)-1, -1, -1):
        page = order[i]
        if page in bad_orderings:
            if any([p for p in order[i+1:] if p in bad_orderings[page]]):
                return True
    return False


def repair_bad_order(order: list[int]) -> None:
    for i in range(len(order)-1, -1, -1):
        page = order[i]
        if page in bad_orderings:
            for j in range(len(order)-1, i, -1):
                if order[j] in bad_orderings[page]:
                    order[i], order[j] = order[j], order[i]

sum_middles = 0
fixed_order_middles = 0
with open('input.txt') as file:
    for line in file:
        if rule_regex.match(line):
            rule = line.split('|')
            first_page = int(rule[0])
            second_page = int(rule[1])
            if second_page not in bad_orderings:
                bad_orderings[second_page] = dict()
            bad_orderings[second_page][first_page] = True
        else:
            order = line.rstrip('\n').split(',')
            if (len(order) > 1):
                parsed_order: list[int] = [int(page) for page in order]
                if is_bad_order(parsed_order):
                    repair_bad_order(parsed_order)
                    fixed_order_middles += parsed_order[len(parsed_order) // 2]
                else:
                    sum_middles += parsed_order[len(parsed_order) // 2]

print('Part 1: ', sum_middles)
print('Part 2: ', fixed_order_middles)
