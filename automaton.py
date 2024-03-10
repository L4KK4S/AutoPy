
# --------------------------------- Class Automaton ------------------------------------ #

class Automaton:


    # -------------------------------- Initialisation de l'automate -------------------------------- #

    def __init__(self, filename):
        self.filename = filename
        self.alphabet = None
        self.states = None
        self.initals_states = None
        self.terminal_states = None
        self.transitions = None
        self.initialize(self.filename)

    def initialize(self, filename):

        # ouverture du fichier et lecture des lignes
        with open(filename, 'r') as file:
            lines = file.readlines()

            # initialisation de l'alphabet
            self.alphabet = [chr(97+i) for i in range(int(lines[0]))]

            # initialisation des états
            self.states = [State(self, [i]) for i in range(int(lines[1]))]

            # initialisation des états initiaux et terminaux
            self.initals_states = [int(x) for x in lines[2].split()[1:]]
            for i in self.initals_states:
                for j in self.states:
                    if j.get_value() == str(i):
                        j.is_initial = True
            self.initals_states = [state for state in self.states if state.is_initial]


            self.terminal_states = [int(x) for x in lines[3].split()[1:]]
            for i in self.terminal_states:
                for j in self.states:
                    if j.get_value() == str(i):
                        j.is_terminal = True
            self.terminal_states = [state for state in self.states if state.is_terminal]

            # initialisation des transitions
            self.transitions = [t[:3] for t in lines[5:]]
            for t in self.transitions:
                for state in self.states:
                    if state.get_value() == str(t[0]):
                        state.transitions[t[1]].append(t[2])


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
            if s.get_value() == "-2":
                output += "I".center(9) + "│"
            else:
                output += (s.get_value().center(9) + "│")

            # transitions
            for i in range(len(self.alphabet)):
                if s.transitions[self.alphabet[i]]:
                    output += (",".join(map(str, s.transitions[self.alphabet[i]])).center(9) + "│")
                else:
                    output += ("-".center(9) + "│")

            output += "\n"

            # ligne de séparation
            if s != self.states[-1]:
                output += ("├─────────" + "┼─────────" * (len(self.alphabet) + 1) + "┤\n")



        # dernière ligne
        output += ("└─────────" + "┴─────────" * (len(self.alphabet) + 1) + "┘")

        return output

    # ------------------------------------------------------------------------------------------ #

    # ------------------------------ Standardisation (Anaelle) --------------------------------- #

    def is_standard(self):

        # vérification qu'on a un unique état initial
        if len(self.initals_states) != 1:  # on regarde si on a un nombre d'états initiaux différent de 1
            return False  # l'automate est non standard

        initial_state = self.initals_states[0]  # stock l'unique état initial dans la variable initial_state

        # vérification qu'il n'y a aucune transition menant à l'unique état initial
        for transition in self.transitions:  # on parcourt toutes les transitions
            if transition[2] == initial_state:  # on regarde si l'état d'arrivée de la transition correspond à l'état initial
                return False

        # si les deux conditions sont remplies, l'automate est standard
        return True

    def standardize(self):  # fonction qui standardise l'automate

        if self.is_standard():  # Si l'automate est déjà standard, on ne fait rien
            return self

        # stockage des anciens états
        old_states = self.states.copy()

        # ajout de l'état initial I qui aura pour valeur -2
        new_initial_state = State(self, [-2])

        # mettre la valeur is_initial de I initial à False
        new_initial_state.is_initial = True

        # mettre la valeur is_terminal de I initial à True si un des états initiaux de l'automate est terminal
        for state in self.initals_states:
            if state.is_terminal:
                new_initial_state.is_terminal = True
                break

        # ajouter le nouvel état initial à la liste des états
        self.states.append(new_initial_state)

        # l'état initial devient l'unique état initial
        self.initals_states = [new_initial_state]

        # ajout des nouvelles transitions depuis le nouvel état initial
        for state in old_states:
            if state.is_initial:
                for letter, destinations in state.transitions.items():
                    new_initial_state.transitions[letter].extend(destinations)

        # ajout des transition du nouvel état initial à l'automate
        for letter in self.alphabet:
            for destination in new_initial_state.transitions[letter]:
                self.transitions.append(new_initial_state.get_value() + letter + destination)

        # mettre à jour is_initial pour les anciens états
        for state in self.states:
            for old_state in old_states:
                if old_state.get_value() == state.get_value():
                    if old_state.is_initial:
                        state.is_initial = False


        # trier les états par valeur croissante
        self.states.sort(key=lambda x: x.values[0])


        return self

    # ------------------------------------------------------------------------------------------ #

    # -------------------------------- Completion (Camille) ------------------------------------ #
    # ------------------------------------------------------------------------------------------ #

    # ----------------------------- Determinisation (Thomas) ----------------------------------- #
    # ------------------------------------------------------------------------------------------ #

    # ------------------------------- Minimisation (Maryam) ------------------------------------ #
    # -------------------------------- Completion (Camille) ------------------------------------ #


# --------------------------------- Class State ------------------------------------ #

class State():

    def __init__(self, automaton, values):
        self.automaton = automaton
        self.values = values
        self.transitions = {letter: [] for letter in automaton.alphabet}
        self.is_initial = False
        self.is_terminal = False

    def get_value(self):
        return "".join(str(e) for e in self.values)

    def __str__(self):
        output = "State (" + "".join(str(e) for e in self.values) + ")"

        for letter, destinations in self.transitions.items():
            output += "\n" + letter + " : " + (", ".join(str(dest) for dest in destinations) if destinations else "-")

        return output

# ------------------------------------------------------------------------------------------ #


