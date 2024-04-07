import re
from collections import Counter

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
            for line in lines:
                if "-2" in line:
                    self.states = [State(self, [i]) for i in range(int(lines[1]) - 1)]
                    self.states.append(State(self, [-2]))
                    self.states.sort(key=lambda x: x.values[0])
                else:
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
            temp_transitions = [re.match(r'([-+]?\d+)([a-zA-Z])([-+]?\d+)', t) for t in lines[5:]]
            self.transitions = [t[0] for t in temp_transitions]
            for t in temp_transitions:
                for state in self.states:
                    if state.get_value() == str(t.group(1)):
                        state.transitions[t.group(2)].append(t.group(3))


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
                if s.transitions[self.alphabet[i]] and not s.is_composed:
                    output += (",".join(map(str, s.transitions[self.alphabet[i]])).center(9) + "│")
                elif s.is_composed:
                    output += ("".join(s.transitions[self.alphabet[i]]).center(9) + "│")
                else:
                    output += ("-".center(9) + "│")

            output += "\n"

            # ligne de séparation
            if s != self.states[-1]:
                output += ("├─────────" + "┼─────────" * (len(self.alphabet) + 1) + "┤\n")



        # dernière ligne
        output += ("└─────────" + "┴─────────" * (len(self.alphabet) + 1) + "┘")

        return output


    # fonction pour mettre à jour les états initiaux et terminaux
    def update_initials_terminal(self):
        self.initals_states = [state for state in self.states if state.is_initial]
        self.terminal_states = [state for state in self.states if state.is_terminal]

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
                    if len(destinations) !=0:
                        for d in destinations:
                            if d not in new_initial_state.transitions[letter]:
                                new_initial_state.transitions[letter].append(d)


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

    # ----------------------------- Determinisation (Maryam) ----------------------------------- #
    def is_determinist(self):
        # On regarde si il y a plusieurs états initiaux
        if len(self.initals_states) != 1:
            return False
        # Vérifier si chaque état a exactement une transition pour chaque symbole de l'alphabet
        for state in self.states:
            for letter, destinations in state.transitions.items():
                if len(destinations) != 1:
                    return False
        return True

    # fonction pour remplir un tableau temporaire contenant les destinations des arretes de chaque état
    def fill_temp_tab(self):

        # initialisation des variables
        temp_tab = [[None for i in range(len(self.alphabet))] for j in range(len(self.states))]
        index, index_max = 0, len(self.states)

        # remplissage du tableau temporaire
        while index < index_max:
            for l in range(len(self.alphabet)):
                temp_tab[index][l] = self.states[index].transitions[self.alphabet[l]]
            index += 1
        return temp_tab

    # fonction pour remplir les transitions d'un nouvel état
    def fill_transitions(self, state):
        if state.value == "13":
            print("ok")
        for v in state.values:                        # on parcourt les valeurs de l'état
            for l in self.alphabet:                   # on parcourt les lettres de l'alphabet
                for s in self.states:                 # on parcourt les états existants
                    if s.value == v:                  # on vérifie si la valeur de l'état correspond à la valeur de l'état existant

                        union = set(state.transitions[l]).union(set(s.transitions[l]))         # on fait l'union des transitions de l'état existant et de la lettre de l'alphabet
                        if state.is_composed:                                                  # si l'état est composé on crée un etat composé avec les valeurrs des états de base
                            union = sorted(list(union))
                            union = "".join(union)
                            state.transitions[l] = [union]
                        else:                                                                  # sinon on ajoute la transition à l'état
                            state.transitions[l] = sorted(list(union))


    # fonction pour vérifier si il y a des doublons dans les transitions
    def check_doublons(self, tab):
        for e in tab:
            for i in tab:
                if e in i and e != i:
                    return True
        return False

    def determinize(self):

        # si l'automate est déjà déterminisé, on ne fait rien
        if self.is_determinist():
            return self


        # si il y a plusieurs états initiaux, on les fusionne
        if len(self.initals_states) > 1:
            temp_values = [str(s.values[0]) for s in self.initals_states]
            initial_state = State(self, temp_values)
            initial_state.is_initial = True
            for s in self.initals_states:
                if s.is_initial:
                    s.is_initial = False
            self.states.append(initial_state)
            self.fill_transitions(self.states[-1])

        # création d'un tableau temporaire contenant les destinations des arretes de chaque état
        temp_tab = self.fill_temp_tab()

        # déterminisation de l'automate
        for i, state in enumerate(self.states):                                                # on parcourt les états
            for l in range(len(self.alphabet)):                                                # on parcourt les lettres de l'alphabet
                if ''.join(temp_tab[i][l]) not in [s.get_value() for s in self.states]:        # on vérifie si la transition n'existe pas déjà
                    if(self.check_doublons(temp_tab[i][l])):                                   # si il y a des doublons dans les transitions on quitte la boucle
                        break
                    int_values = [int(x) for x in temp_tab[i][l]]                              # on convertit les valeurs en int
                    val = "".join(str(e) for e in int_values)                                  # on convertit les valeurs
                    print(temp_tab[i][l], val)
                    self.states[i].transitions[self.alphabet[l]] = [val]                       # on ajoute la transition à l'état
                    self.states.append(State(self, temp_tab[i][l], True, val))                 # on ajoute un nouvel état avec comme valeur les valeurs de la transition vers un état pas encore existant
                    self.fill_transitions(self.states[-1])                                     # on remplit les transitions de ce nouvel état
                    temp_tab = self.fill_temp_tab()                                            # on met à jour le tableau temporaire

        # on met à jour les entrées et sorties
        for state in self.states:
            if state.is_composed:
                for s in self.terminal_states:
                    if s.get_value() in state.values:
                        state.is_terminal = True
                        break

        # on met à jour les états initiaux et terminaux
        self.update_initials_terminal()




    # ------------------------------------------------------------------------------------------ #

    # ------------------------------- Minimisation (Thomas) ------------------------------------ #
    # -------------------------------- Completion (Camille) ------------------------------------ #


# --------------------------------- Class State ------------------------------------ #

class State():

    def __init__(self, automaton, values, composed=False, value=None):
        self.automaton = automaton
        self.values = values
        self.value = "".join(str(e) for e in values) if value is None else value
        self.is_composed = composed
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


