

class Automaton:

    def __init__(self, filename):
        self.filename = filename
        self.alphabet = None
        self.states = None
        self.initals_states = None
        self.terminal_states = None
        self.transitions = None
        self.initialize(filename)

    def initialize(self, filename):

        # ouverture du fichier et lecture des lignes
        with open(filename, 'r') as file:
            lines = file.readlines()

            # initialisation de l'alphabet
            self.alphabet = [chr(97+i) for i in range(int(lines[0]))]

            # initialisation des états
            self.states = [State(self, [i], [[] for _ in range(len(self.alphabet))]) for i in range(int(lines[1]))]

            # initialisation des états initiaux et terminaux
            self.initals_states = [int(x) for x in lines[2].split()[1:]]
            for i in self.initals_states:
                for j in self.states:
                    if j.get_value() == str(i):
                        j.is_initial = True

            self.terminal_states = [int(x) for x in lines[3].split()[1:]]
            for i in self.terminal_states:
                for j in self.states:
                    if j.get_value() == str(i):
                        j.is_terminal = True

            # initialisation des transitions
            self.transitions = [t[:3] for t in lines[5:]]
            for t in self.transitions:
                for state in self.states:
                    if state.get_value() == str(t[0]):
                        state.transitions[self.alphabet.index(t[1])].append(t[2])


    def __str__(self):
        # première ligne
        output = "┌─────────" + "┬─────────" * (len(self.alphabet) + 1) + "┐\n"

        # entêtes
        headers = ["E/S", "État"] + self.alphabet
        output += "│"
        for header in headers:
            output += (header.center(9) + "│")

        output += "\n"

        # ligne de séparation
        output += ("├─────────" + "┼─────────" * (len(self.alphabet) + 1) + "┤\n")

        # transitions
        for s in self.states:

            # entrées/sorties
            if s.is_initial and s.is_terminal:
                output += "│" + "E/S".center(9) + "│"
            elif s.is_initial:
                output += "│" + "E".center(9) + "│"
            elif s.is_terminal:
                output += "│" + "S".center(9) + "│"
            else:
                output += "│" + " ".center(9) + "│"

            # état
            output += str(s.get_value()).center(9) + "│"

            # transitions
            for i in range(len(self.alphabet)):
                if not all(not sublist for sublist in s.transitions[i]):
                    output += (",".join(map(str, s.transitions[i])).center(9) + "│")
                else:
                    output += ("-".center(9) + "│")

            output += "\n"

            # ligne de séparation
            if s != self.states[-1]:
                output += ("├─────────" + "┼─────────" * (len(self.alphabet) + 1) + "┤\n")



        # dernière ligne
        output += ("└─────────" + "┴─────────" * (len(self.alphabet) + 1) + "┘")

        return output


class State():

    def __init__(self, automaton, values, transitions):
        self.automaton = automaton
        self.values = values
        self.transitions = transitions
        self.is_initial = False
        self.is_terminal = False

    def get_value(self):
        return "".join(str(e) for e in self.values)

    def __str__(self):
        return "State (" + "".join(str(e) for e in self.values) + ")" + "".join("\n" + self.automaton.alphabet[i] + " : " + (", ".join(str(e) for e in self.transitions[i]) if not all(not sublist for sublist in self.transitions[i]) else "-") for i in range(len(self.automaton.alphabet)))

        """
        output = "State (" + "".join(str(e) for e in self.values) + ")"
        
        for i in range(len(self.automaton.alphabet)):
            output += "\n" + self.automaton.alphabet[i] + " : " + (", ".join(str(e) for e in self.transitions[i]) if not all(not sublist for sublist in self.transitions[i]) else "-")
            
        return output
        """



