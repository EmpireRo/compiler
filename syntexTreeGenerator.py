from collections import defaultdict
import copy
import json


def str2Dict(string, p_list):
    string = string.replace(' ', '')
    m_list = string.split('->')
    p_list.append((m_list[0], list(m_list[1])))
    return p_list


def firstConstructor(p_list, non_terminators):
    first_dict = defaultdict(set)
    for p in p_list:
        nonT = p[0]
        first_dict[nonT] = findFirst(nonT, p_list, non_terminators)
    return first_dict


def findFirst(symbol, p_list, non_terminators):
    first_set = set()
    if symbol not in non_terminators:
        first_set.add(symbol)
    else:
        first_set |= set([p[1][0] for p in p_list if p[0] == symbol and p[1][0] not in non_terminators])
        for p in p_list:
            if p[0] == symbol and p[1][0] in non_terminators:
                first_set |= findFirst(p[1][0], p_list, non_terminators) - set(('ε'))
        first_set -= set([None])
    return first_set


def findFirstString(symbols, p_list, non_terminators):
    first_set = set()
    for symbol in symbols:
        first_set |= findFirst(symbol, p_list, non_terminators) - set(('ε'))
        if 'ε' not in findFirst(symbol, p_list, non_terminators):
            break
        elif symbol is symbols[-1]:
            first_set.add('ε')
    return first_set


def followConstructor(p_list, non_terminators):
    follow_dict = defaultdict(set)
    for p in p_list:
        if p[0] is 'E':
            follow_dict[p[0]].add('#')
        for i, v in enumerate(p[1]):
            if v in non_terminators and v is not p[1][-1]:
                follow_dict[v] |= findFirst(p[1][i + 1], p_list, non_terminators) - set(('ε'))
        
    for p in p_list:
        for i, v in enumerate(p[1]):
            if v in non_terminators:
                if v is p[1][-1]:
                    follow_dict[v] |= follow_dict[p[0]]
                else:
                    if 'ε' in findFirstString(p[1][i + 1:], p_list, non_terminators):
                        follow_dict[v] |= follow_dict[p[0]]
    return follow_dict


def tableConstractor(follow_dict, p_list, terminators):
    parsing_table = defaultdict(tuple)
    for p in p_list:
        if 'ε' in findFirstString(p[1], p_list, non_terminators):
            for v in follow_dict[p[0]]:
                parsing_table[(p[0], v)] = p
            if '#' in follow_dict[p[0]]:
                parsing_table[(p[0], '#')]
        for v in terminators:
            if v in findFirstString(p[1], p_list, non_terminators):
                parsing_table[(p[0], v)] = p
    return parsing_table


if __name__ == '__main__':
    p_list = []
    rawP = ('E -> TR',
            'R -> +TR',
            'R -> -TR',
            'R -> ε',
            'T -> (E)',
            'T -> i',
            'T -> n')
    for p in rawP:
        p_list = str2Dict(p, p_list)

    non_terminators = ('E', 'T', 'R')
    terminators = ('i', 'n', '(', ')', '+', '-')
    print(p_list)

    first_dict = firstConstructor(p_list, non_terminators)
    print(firstConstructor(p_list, non_terminators))

    follow_dict = followConstructor(p_list, non_terminators)
    print(followConstructor(p_list, non_terminators))

    parsing_table = tableConstractor(follow_dict, p_list, terminators)
    print(parsing_table)
