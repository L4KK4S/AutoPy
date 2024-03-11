
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
        print("L'automate est standard")
        return True

    def standardize_automaton(self): #fonction qui standardise l'automate
        new_initial_state = max(self.states) + 1 #Ajout de l'état initial qui au lieu de s'appeler i ça sera notre nombre d'étas + 1
        self.states.append(new_initial_state)  # Ajouter le nouvel état initial à la liste des états

        old_initial_states = self.initals_states.copy() #Sauvegarde des anciens états initiaux

        self.initals_states = [new_initial_state] #L'état initial devient l'unique état initial

        # Déterminer si le nouvel état initial est terminal ou non-terminal en regardant dans la liste des états terminaux
        is_terminal = any(state in self.terminal_states for state in old_initial_states)

        new_transitions = []  # Liste pour stocker les nouvelles transitions

        # Ajout des nouvelles transitions depuis le nouvel état initial
        for initial_state in old_initial_states:
            for transition in self.transitions:
                if transition[0] == initial_state:
                    new_transitions.append((new_initial_state, transition[1], transition[2]))


        # Ajouter les nouvelles transitions à la liste self.transitions
        self.transitions.extend(new_transitions)

        print("etats", self.states)

        # Si i est terminal, on l'ajoute dans la liste des états terminaux
        if is_terminal:
            self.terminal_states.append(new_initial_state)

        return self

