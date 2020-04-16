# Project 2 
# CS454 spring 2020
# NFAtoDFA.py :
# This is Python code for representing finite automata, DFAs and NFAs,
# and for converting from an NFA into a DFA.
#
# Ben Reichardt, 1/17/2011
#
from functools import reduce


class DFA:
    """Class that encapsulates a DFA."""

    def __init__(self, transitionFunction, initialState, finalStates):
        self.delta = transitionFunction
        self.q0 = initialState
        self.F = finalStates

    def deltaHat(self, state, inputString):
        for a in inputString:
            state = self.delta[state][a]
        return state

    def inLanguage(self, inputString):
        return self.deltaHat(self.q0, inputString) in self.F


# comments:
# 	* python dictionary keys must be immutable
#	* it is a KeyError to extract an entry using a non-existent key

class NFA:
    """Class that encapsulates an NFA."""

    def __init__(self, transitionFunction, initialState, finalStates):
        self.delta = transitionFunction
        self.q0 = initialState
        self.F = set(finalStates)

    def deltaHat(self, state, inputString):
        """deltaHat is smart enough to return the empty set if no transition is defined."""
        states = set([state])
        for a in inputString:
            newStates = set([])
            for state in states:
                try:
                    newStates = newStates | self.delta[state][a]
                except KeyError:
                    pass
            states = newStates
        return states

    def inLanguage(self, inputString):
        return len(self.deltaHat(self.q0, inputString) & self.F) > 0

    def alphabet(self):
        """Returns the NFA's input alphabet, generated on the fly."""
        Sigma = reduce(lambda a, b: set(a) | set(b), [x.keys() for x in N.delta.values()])
        return Sigma

    def states(self):
        """Returns the NFA's set of states, generated on the fly."""
        Q = set([self.q0]) | set(self.delta.keys()) | reduce(lambda a, b: a | b, reduce(lambda a, b: a + b,
                                                                                        [x.values() for x in
                                                                                         self.delta.values()]))  # {q0, all states with outgoing arrows, all with incoming arrows}
        return Q


def convertNFAtoDFA(N):
    """Converts the input NFA into a DFA.

    The output DFA has a state for every *reachable* subset of states in the input NFA.
    In the worst case, there will be an exponential increase in the number of states.
    """
    q0 = frozenset([N.q0])  # frozensets are hashable, so can key the delta dictionary
    Q = set([q0])
    unprocessedQ = Q.copy()  # unprocessedQ tracks states for which delta is not yet defined
    delta = {}
    F = []
    Sigma = N.alphabet()

    while len(unprocessedQ) > 0:
        qSet = unprocessedQ.pop()
        delta[qSet] = {}
        for a in Sigma:
            nextStates = reduce(lambda x, y: x | y, [N.deltaHat(q, a) for q in qSet])
            nextStates = frozenset(nextStates)
            delta[qSet][a] = nextStates
            if nextStates not in Q:
                Q.add(nextStates)
                unprocessedQ.add(nextStates)
    for qSet in Q:
        if len(qSet & N.F) > 0:
            F.append(qSet)
    M = DFA(delta, q0, F)
    return M



delta = {'q0': {'0': set(['q0']),
                '1': set(['q1']),
                '2': set(['q2']),
                '3': set(['q3']),
                '4': set(['q4']),
                '5': set(['q5']),
                '6': set(['q6']),
                '7': set(['q0']),
                '8': set(['q1']),
                '9': set(['q2'])
                },
        'q1': {'0': set(['q3']),
                '1': set(['q4']),
                '2': set(['q5']),
                '3': set(['q6']),
                '4': set(['q0']),
                '5': set(['q1']),
                '6': set(['q2']),
                '7': set(['q3']),
                '8': set(['q4']),
                '9': set(['q5'])
                 },
        'q2': {'0': set(['q6']),
                '1': set(['q0']),
                '2': set(['q1']),
                '3': set(['q2']),
                '4': set(['q3']),
                '5': set(['q4']),
                '6': set(['q5']),
                '7': set(['q6']),
                '8': set(['q0']),
                '9': set(['q1'])
                },
        'q3': {'0': set(['q2']),
                '1': set(['q3']),
                '2': set(['q4']),
                '3': set(['q5']),
                '4': set(['q6']),
                '5': set(['q0']),
                '6': set(['q1']),
                '7': set(['q2']),
                '8': set(['q3']),
                '9': set(['q4'])
                },
        'q4': {'0': set(['q5']),
                '1': set(['q6']),
                '2': set(['q0']),
                '3': set(['q1']),
                '4': set(['q2']),
                '5': set(['q3']),
                '6': set(['q4']),
                '7': set(['q5']),
                '8': set(['q6']),
                '9': set(['q0'])
                },
        'q5': {'0': set(['q1']),
                '1': set(['q2']),
                '2': set(['q3']),
                '3': set(['q4']),
                '4': set(['q5']),
                '5': set(['q6']),
                '6': set(['q0']),
                '7': set(['q1']),
                '8': set(['q2']),
                '9': set(['q3'])
                },
        'q6': {'0': set(['q4']),
                '1': set(['q5']),
                '2': set(['q6']),
                '3': set(['q0']),
                '4': set(['q1']),
                '5': set(['q2']),
                '6': set(['q3']),
                '7': set(['q4']),
                '8': set(['q5']),
                '9': set(['q6'])
                }
    }
N = NFA(delta, 'q0', ['q0'])
N.deltaHat('q0', '0123456789')
example = ['7', '54', '49', '77', '4326']
for x in example:
    print(x, N.inLanguage(x))
M = convertNFAtoDFA(N)
for x in example:
    print(x, M.inLanguage(x))

# # both the above lines should return [('0001', True), ('00010', False), ('100101', True)]

# to run the doctests, run python or python -v directly on this script
#if __name__ == "__main__":
    #import doctest

    #doctest.testmod()
