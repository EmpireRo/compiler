from collections import defaultdict
import copy
import json


class ParsingTableGenerator(object):
    """
    class for generate predicting parsing table.
    """

    def __init__(self, grammar, terminators, non_terminators):
        self.p_list = self.str2Dict(grammar)
        self.terminators = terminators
        self.non_terminators = non_terminators
        self.first_dict = self.firstConstructor()
        self.follow_dict = self.followConstructor()

    @classmethod
    def str2Dict(self, grammar):
        self.p_list = list()
        for p in grammar:
            p = p.replace(' ', '')
            m_list = p.split('->')
            self.p_list.append((m_list[0], list(m_list[1])))
        return self.p_list

    def firstConstructor(self):
        first_dict = defaultdict(set)
        for p in self.p_list:
            nonT = p[0]
            first_dict[nonT] = self.findFirst(nonT)
        return first_dict

    def findFirst(self, symbol):
        first_set = set()
        if symbol not in self.non_terminators:
            first_set.add(symbol)
        else:
            first_set |= set([p[1][0] for p in self.p_list if p[0] == symbol and p[1][0] not in self.non_terminators])
            for p in self.p_list:
                if p[0] == symbol and p[1][0] in self.non_terminators:
                    first_set |= self.findFirst(p[1][0]) - set(('ε'))
            first_set -= set([None])
        return first_set

    def findFirstString(self, symbols):
        first_set = set()
        for symbol in symbols:
            first_set |= self.findFirst(symbol) - set(('ε'))
            if 'ε' not in self.findFirst(symbol):
                break
            elif symbol is symbols[-1]:
                first_set.add('ε')
        return first_set

    def followConstructor(self):
        follow_dict = defaultdict(set)
        for p in self.p_list:
            if p[0] is 'E':
                follow_dict[p[0]].add('#')
            for i, v in enumerate(p[1]):
                if v in self.non_terminators and v is not p[1][-1]:
                    follow_dict[v] |= self.findFirst(p[1][i + 1]) - set(('ε'))
            
        for p in self.p_list:
            for i, v in enumerate(p[1]):
                if v in self.non_terminators:
                    if v is p[1][-1]:
                        follow_dict[v] |= follow_dict[p[0]]
                    else:
                        if 'ε' in self.findFirstString(p[1][i + 1:]):
                            follow_dict[v] |= follow_dict[p[0]]
        return follow_dict

    def tableConstractor(self):
        self.parsing_table = defaultdict(tuple)
        for p in self.p_list:
            if 'ε' in self.findFirstString(p[1]):
                for v in self.follow_dict[p[0]]:
                    self.parsing_table[(p[0], v)] = p
                if '#' in self.follow_dict[p[0]]:
                    self.parsing_table[(p[0], '#')]
            for v in terminators:
                if v in self.findFirstString(p[1]):
                    self.parsing_table[(p[0], v)] = p
        return self.parsing_table


if __name__ == '__main__':
    grammar = ('E -> TR',
            'R -> +TR',
            'R -> -TR',
            'R -> ε',
            'T -> (E)',
            'T -> i',
            'T -> n')

    non_terminators = ('E', 'T', 'R')
    terminators = ('i', 'n', '(', ')', '+', '-')

    parsingTableGenerator = ParsingTableGenerator(grammar, terminators, non_terminators)

    parsing_table = parsingTableGenerator.tableConstractor()
    print(parsingTableGenerator.p_list)
    print(parsingTableGenerator.first_dict)
    print(parsingTableGenerator.follow_dict)
    print(parsing_table)
