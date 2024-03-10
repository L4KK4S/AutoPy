from automaton import Automaton
import file
import os
import graph


def main():


    automaton1 = Automaton("bob.txt")



    print(automaton1)

    print(automaton1.transitions)
    for s in automaton1.states:
        print(s.transitions)

    print(automaton1.is_standard())

    automaton1.standardize()

    print(automaton1.transitions)
    for s in automaton1.states:
        print(s.transitions)

    print(automaton1.is_standard())

    print(automaton1.states[0])

    print(automaton1)

    print(automaton1.is_standard())

    graph.graph(automaton1)

if __name__ == "__main__":
    main()