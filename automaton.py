
class Automaton:

    def __init__(self, filename):
        self.alphabet = None
        self.states = None
        self.initals_states = None
        self.terminal_states = None
        self.transitions = None
        self.initialize(filename)

    def initialize(self, filename):
        
        with open(filename, 'r') as file:
            lines = file.readlines()
            alphabet_size = int(lines[0])
            nb_states = int(lines[1])
            states = list(range(nb_states))  # Crée une liste d'états
            self.initals_states = list(map(int, lines[2].split()[1:]))
            self.terminal_states = list(map(int, lines[3].split()[1:]))
            transitions = []
            for line in lines[5:]:
                transition_data = line.strip()
                start_state = int(transition_data[0])
                symbol = transition_data[1]
                terminal_state = int(transition_data[2])
                transitions.append((start_state, symbol, terminal_state))

            self.alphabet = alphabet_size
            self.states = states
            self.transitions = transitions


    def __str__(self):

        output_text = ""

        # Collecte de tous les symboles uniques
        symbols = sorted(set(transition[1] for transition in self.transitions))

        # Création des en-têtes de colonnes
        headers = ["État"] + symbols

        # Affichage de la première ligne
        output_text += ("┌─────────" + "┬─────────" * len(symbols) + "┐\n")

        # Affichage des en-têtes
        output_text += "│"
        for header in headers:
                output_text += (header.center(9) + "│")
        output_text += "\n"

        # Affichage de la ligne de séparation
        output_text += ("├─────────" + "┼─────────" * len(symbols) + "┤\n")

        # Affichage des lignes de transition
        for etat in self.states:
            output_text += "│"
            output_text += (str(etat).center(9) + "│")
            for symbol in symbols:
                transitions = [transition[2] for transition in self.transitions if transition[0] == etat and transition[1] == symbol]
                if transitions:
                    output_text += (",".join(map(str, transitions)).center(9) + "│")
                else:
                    output_text += ("-".center(9) + "│")
            output_text += "\n"

        # Affichage de la ligne de fin
        output_text += ("└─────────" + "┴─────────" * len(symbols) + "┘")

        return output_text

    def is_standard(self):
        #Vérification qu'on a un unique état initial
        if len(self.initals_states) != 1: #on regarde si on a un nombre d'états initiaux différent de 1
            return False # L'automate est non standard

        initial_state = self.initals_states[0] #stock l'unique état initial dans la variable initial_state

        # Vérification qu'il n'y a aucune transition menant à l'unique état initial
        for transition in self.transitions: #on parcourt toutes les transitions
            if transition[2] == initial_state: #on regarde si l'état d'arrivée de la transition correspond à l'état initial
                return False

        # Si les deux conditions sont remplies, l'automate est standard
        return True
