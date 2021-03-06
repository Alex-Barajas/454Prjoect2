# Project 2 
# CS454 spring 2020
# NFAtoDFA.py :
# This is Python code for representing finite automata, DFAs and NFAs,
# and for converting from an NFA into a DFA.
#
#
from functools import reduce
import copy
import pprint


class DFA:
    """Class that encapsulates a DFA."""

    def __init__(self, transitionFunction, initialState, finalStates, stateSet):
        self.delta = transitionFunction
        self.q0 = initialState
        self.F = finalStates
        self.Q = stateSet

    def deltaHat(self, state, inputString):
        for a in inputString:
            state = self.delta[state][a]
        return state

    def inLanguage(self, inputString):
        return self.deltaHat(self.q0, inputString) in self.F


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
        Sigma = reduce(lambda a, b: set(a) | set(b), [x.keys() for x in self.delta.values()])
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
            if not nextStates in Q:
                Q.add(nextStates)
                unprocessedQ.add(nextStates)
    for qSet in Q:
        if len(qSet & N.F) > 0:
            F.append(qSet)
    M = DFA(delta, q0, F, Q)
    return M


def count(M, curr, next, n):
    for i in range(n):
        for q, v in curr.items():
            num = 0
            for sym in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                transition_state = frozenset(M.delta[frozenset(q)][sym])
                num += curr[transition_state]
            next[q] = num
        curr = copy.deepcopy(next)
    return next


def main():
    delta = {
        'q0': {
            '0': set(['q0', 'q7']),
            '1': set(['q1', 'q7']),
            '2': set(['q2', 'q7']),
            '3': set(['q3', 'q7']),
            '4': set(['q4', 'q7']),
            '5': set(['q5', 'q7']),
            '6': set(['q6', 'q7']),
            '7': set(['q0', 'q7']),
            '8': set(['q1', 'q7']),
            '9': set(['q2', 'q7'])
        },
        'q1': {
            '0': set(['q3', 'q8']),
            '1': set(['q4', 'q8']),
            '2': set(['q5', 'q8']),
            '3': set(['q6', 'q8']),
            '4': set(['q0', 'q8']),
            '5': set(['q1', 'q8']),
            '6': set(['q2', 'q8']),
            '7': set(['q3', 'q8']),
            '8': set(['q4', 'q8']),
            '9': set(['q5', 'q8'])
        },
        'q2': {
            '0': set(['q6', 'q9']),
            '1': set(['q0', 'q9']),
            '2': set(['q1', 'q9']),
            '3': set(['q2', 'q9']),
            '4': set(['q3', 'q9']),
            '5': set(['q4', 'q9']),
            '6': set(['q5', 'q9']),
            '7': set(['q6', 'q9']),
            '8': set(['q0', 'q9']),
            '9': set(['q1', 'q9'])
        },
        'q3': {
            '0': set(['q2', 'q10']),
            '1': set(['q3', 'q10']),
            '2': set(['q4', 'q10']),
            '3': set(['q5', 'q10']),
            '4': set(['q6', 'q10']),
            '5': set(['q0', 'q10']),
            '6': set(['q1', 'q10']),
            '7': set(['q2', 'q10']),
            '8': set(['q3', 'q10']),
            '9': set(['q4', 'q10'])
        },
        'q4': {
            '0': set(['q5', 'q11']),
            '1': set(['q6', 'q11']),
            '2': set(['q0', 'q11']),
            '3': set(['q1', 'q11']),
            '4': set(['q2', 'q11']),
            '5': set(['q3', 'q11']),
            '6': set(['q4', 'q11']),
            '7': set(['q5', 'q11']),
            '8': set(['q6', 'q11']),
            '9': set(['q0', 'q11'])
        },
        'q5': {
            '0': set(['q1', 'q12']),
            '1': set(['q2', 'q12']),
            '2': set(['q3', 'q12']),
            '3': set(['q4', 'q12']),
            '4': set(['q5', 'q12']),
            '5': set(['q6', 'q12']),
            '6': set(['q0', 'q12']),
            '7': set(['q1', 'q12']),
            '8': set(['q2', 'q12']),
            '9': set(['q3', 'q12'])
        },
        'q6': {
            '0': set(['q4', 'q13']),
            '1': set(['q5', 'q13']),
            '2': set(['q6', 'q13']),
            '3': set(['q0', 'q13']),
            '4': set(['q1', 'q13']),
            '5': set(['q2', 'q13']),
            '6': set(['q3', 'q13']),
            '7': set(['q4', 'q13']),
            '8': set(['q5', 'q13']),
            '9': set(['q6', 'q13'])
        },
        'q7': {
            '0': set(['q7']),
            '1': set(['q8']),
            '2': set(['q9']),
            '3': set(['q10']),
            '4': set(['q11']),
            '5': set(['q12']),
            '6': set(['q13']),
            '7': set(['q7']),
            '8': set(['q8']),
            '9': set(['q9'])
        },
        'q8': {
            '0': set(['q10']),
            '1': set(['q11']),
            '2': set(['q12']),
            '3': set(['q13']),
            '4': set(['q7']),
            '5': set(['q8']),
            '6': set(['q9']),
            '7': set(['q10']),
            '8': set(['q11']),
            '9': set(['q12'])
        },
        'q9': {
            '0': set(['q13']),
            '1': set(['q7']),
            '2': set(['q8']),
            '3': set(['q9']),
            '4': set(['q10']),
            '5': set(['q11']),
            '6': set(['q12']),
            '7': set(['q13']),
            '8': set(['q7']),
            '9': set(['q8'])
        },
        'q10': {
            '0': set(['q9']),
            '1': set(['q10']),
            '2': set(['q11']),
            '3': set(['q12']),
            '4': set(['q13']),
            '5': set(['q7']),
            '6': set(['q8']),
            '7': set(['q9']),
            '8': set(['q10']),
            '9': set(['q11'])
        },
        'q11': {
            '0': set(['q12']),
            '1': set(['q13']),
            '2': set(['q7']),
            '3': set(['q8']),
            '4': set(['q9']),
            '5': set(['q10']),
            '6': set(['q11']),
            '7': set(['q12']),
            '8': set(['q13']),
            '9': set(['q7'])
        },
        'q12': {
            '0': set(['q8']),
            '1': set(['q9']),
            '2': set(['q10']),
            '3': set(['q11']),
            '4': set(['q12']),
            '5': set(['q13']),
            '6': set(['q7']),
            '7': set(['q8']),
            '8': set(['q9']),
            '9': set(['q10'])
        },
        'q13': {
            '0': set(['q11']),
            '1': set(['q12']),
            '2': set(['q13']),
            '3': set(['q7']),
            '4': set(['q8']),
            '5': set(['q9']),
            '6': set(['q10']),
            '7': set(['q11']),
            '8': set(['q12']),
            '9': set(['q13'])
        },
        'q14': {
            '0': set(['q17']),
            '1': set(['q1', 'q8', 'q16']),
            '2': set(['q2', 'q16']),
            '3': set(['q3', 'q16']),
            '4': set(['q4', 'q16']),
            '5': set(['q5', 'q16']),
            '6': set(['q6', 'q16']),
            '7': set(['q15', 'q16']),
            '8': set(['q1', 'q16']),
            '9': set(['q2', 'q16'])
        },
        'q15': {
            '0': set(['q0', 'q7']),
            '1': set(['q1', 'q7']),
            '2': set(['q2', 'q7']),
            '3': set(['q3', 'q7']),
            '4': set(['q4', 'q7']),
            '5': set(['q5', 'q7']),
            '6': set(['q6', 'q7']),
            '7': set(['q0', 'q7']),
            '8': set(['q1', 'q7']),
            '9': set(['q2', 'q7'])
        },
        'q16': {
            '0': set(['q7']),
            '1': set(['q8']),
            '2': set(['q9']),
            '3': set(['q10']),
            '4': set(['q11']),
            '5': set(['q12']),
            '6': set(['q13']),
            '7': set(['q7']),
            '8': set(['q8']),
            '9': set(['q9'])
        },
        'q17': {
            '0': set(['q18']),
            '1': set(['q18']),
            '2': set(['q18']),
            '3': set(['q18']),
            '4': set(['q18']),
            '5': set(['q18']),
            '6': set(['q18']),
            '7': set(['q18']),
            '8': set(['q18']),
            '9': set(['q18'])
        },
        'q18': {
            '0': set(['q18']),
            '1': set(['q18']),
            '2': set(['q18']),
            '3': set(['q18']),
            '4': set(['q18']),
            '5': set(['q18']),
            '6': set(['q18']),
            '7': set(['q18']),
            '8': set(['q18']),
            '9': set(['q18'])
        }
    }

    N = NFA(delta, 'q14', ['q0', 'q7', 'q15', 'q17', ])
    # N.deltaHat('q0', '8')
    M = convertNFAtoDFA(N)
    # test = convertedDFA.delta

    curr = {}
    next = {}
    for q in M.Q:
        if q in M.F:
            curr[q] = 1
        else:
            curr[q] = 0
        next[q] = 0

    n = int(input("Enter a value for n or any negative value to exit: "))
    while n > 0:
        final = count(M, curr, next, n)
        print(final[M.q0])
        n = int(input("Enter a value for n or any negative value to exit: "))

main()
