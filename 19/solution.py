def pattern_index(pattern:str) -> int:
    match(pattern):
        case 'w':
            return 0
        case 'u':
            return 1
        case 'b':
            return 2
        case 'r':
            return 3
        case 'g':
            return 4

class TrieNode:
    def __init__(self):
        self.children = [None]*5
        self.end_of_word = False

def insert_word(root: TrieNode, word:str)-> None:
    cur_node: TrieNode = root

    for c in word:
        index = pattern_index(c)
        if cur_node.children[index] == None:
            cur_node.children[index] = TrieNode()
        cur_node = cur_node.children[index]
    cur_node.end_of_word = True

def word_exists(root: TrieNode, word:str) -> bool:
    cur_node = root
    for c in word:
        index = pattern_index(c)
        if cur_node.children[index] == None:
            return False
        cur_node = cur_node.children[index]
    return cur_node.end_of_word

trie_root = TrieNode()
trie_root.end_of_word = True
max_word_length: int = 0
min_word_length: int = 0
possible_patterns: int = 0
pattern_combinations: int = 0
memo_possible: dict[str, bool] = dict()
memo_combos: dict[str, int] = dict()

def is_pattern_possible(pattern:str) -> bool:
    if pattern in memo_possible:
        return memo_possible[pattern]
    if len(pattern) <= min_word_length and word_exists(trie_root, pattern):
        memo_possible[pattern] = True
        return True
    for chunk in range(min(max_word_length, len(pattern)), min_word_length - 1, -1):
        if word_exists(trie_root, pattern[:chunk]) and is_pattern_possible(pattern[chunk:]):
            memo_possible[pattern] = True
            return True
    memo_possible[pattern] = False
    return False

def pattern_combos(pattern:str) -> int:
    if pattern in memo_combos:
        return memo_combos[pattern]
    if len(pattern) == 0:
        return 0
    combos = 0
    if word_exists(trie_root, pattern):
        combos += 1
    if len(pattern) > min_word_length:
        for chunk in range(min(max_word_length, len(pattern)-1), min_word_length - 1, -1):
            if word_exists(trie_root, pattern[:chunk]):
                combos += pattern_combos(pattern[chunk:])
    memo_combos[pattern] = combos
    return combos

with open('input.txt') as file:
    for line in file.readlines(1):
        vocab = line.rstrip('\n').split(', ')
        max_word_length = max([len(w) for w in vocab])
        min_word_length = min([len(w) for w in vocab])
        for word in vocab:
            insert_word(trie_root, word)
    for line in file.readlines():
        pattern = line.rstrip('\n')
        if len(pattern) > 0 and is_pattern_possible(pattern):
            possible_patterns += 1
            pattern_combinations += pattern_combos(pattern)

print('Part 1: ', possible_patterns)
print('Part 2: ', pattern_combinations)