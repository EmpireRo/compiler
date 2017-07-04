from collections import defaultdict
import copy
import json


def str2Dict(string, p_list):
    string = string.replace(' ', '')
    m_list = string.split('->')
    p_list.append((m_list[0], list(m_list[1])))
    return p_list


def firstConstructor(p_list, nonTs):
    first_dict = defaultdict(set)
    for p in p_list:
        nonT = p[0]
        first_dict[nonT] = findFirstWrapper(nonT, p_list, nonTs)
    return first_dict


def findFirstWrapper(symbol, p_list, nonTs):
    first_set = set()
    if symbol not in nonTs:
        first_set.add(symbol)
    else:
        first_set |= set([p[1][0] for p in p_list if p[0] == symbol and p[1][0] not in nonTs])
        for p in p_list:
            if p[0] == symbol and p[1][0] in nonTs:
                first_set |= findFirstWrapper(p[1][0], p_list, nonTs) - set(('ε'))
        first_set -= set([None])
    return first_set


def followConstructor(p_list, nonTs):
    follow_dict = defaultdict(set)
    for nonT in p_list.keys():
        if nonT is 'E':
            follow_dict[nonT].add('#')
        for p in p_list[nonT]:
            for i, v in enumerate(p):
                if v in nonTs and v is not p[-1]:
                    follow_dict[v] |= findFirstWrapper(p[i + 1], p_list, nonTs)
                    follow_dict[v] -= set(('ε'))
        
    for nonT in p_list.keys():
        for p in p_list[nonT]:
            for i, v in enumerate(p):
                if v in nonTs:
                    if v is p[-1]:
                        follow_dict[v] |= follow_dict[nonT]
                    else:
                        t_p_list = copy.deepcopy(p_list)
                        t_p_list['S'] = p[i + 1:]
                        if 'ε' in findFirstWrapper('S', t_p_list, nonTs, True):
                            follow_dict[v] |= follow_dict[nonT]
                            break
    return follow_dict


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

    nonTs = ('E', 'T', 'R')
    print(p_list)

    first_dict = firstConstructor(p_list, nonTs)
    print(firstConstructor(p_list, nonTs))

    # follow_dict = followConstructor(p_list, nonTs)
    # print(followConstructor(p_list, nonTs))
