import re
import os
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

        # vérification de l'extension du fichier
        if filename[-4:] != '.txt':
            print("Erreur : le fichier doit être un fichier texte (.txt)")
            return

        # vérification de l'existence du fichier
        if not os.path.exists(filename):
            print("Erreur : le fichier n'existe pas")
            return


        # ouverture du fichier et lecture des lignes
        with open(filename, 'r') as file:
            lines = file.readlines()

            # vérification du nombre de lignes
            if len(lines) < 5:
                print("Erreur : le fichier doit contenir au moins 5 lignes")
                return

            # initialisation de l'alphabet
            self.alphabet = [chr(97+i) for i in range(int(lines[0]))]

            # initialisation des états
            for line in lines:
                if "-2" in line:
                    self.states = [State(self, [str(i)]) for i in range(int(lines[1]) - 1)]
                    self.states.append(State(self, [-2]))
                    self.states.sort(key=lambda x: x.values[0])
                else:
                    self.states = [State(self, [str(i)]) for i in range(int(lines[1]))]

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

        # nom du fichier de l'automate
        output = "\n" + self.filename + "\n"

        # haut de la table
        output += "┌─────────" + "┬─────────" * (len(self.alphabet) + 1) + "┐\n"

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
            output += (s.get_value().center(9) + "│")

            # transitions
            for i, letter in enumerate(self.alphabet):
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


    # méthode pour mettre à jour les états initiaux et terminaux
    def update_initials_terminal(self):
        self.initals_states = [state for state in self.states if state.is_initial]
        self.terminal_states = [state for state in self.states if state.is_terminal]

    # ------------------------------------------------------------------------------------------ #

    # ------------------------------ Standardisation (Anaelle) --------------------------------- #

    # méthode pour vérifier si l'automate est standard
    def is_standard(self):

        # vérification qu'on a un unique état initial
        if len(self.initals_states) != 1:  # on regarde si on a un nombre d'états initiaux différent de 1
            return False  # l'automate est non standard

        initial_state = self.initals_states[0]  # stock l'unique état initial dans la variable initial_state

        # vérification qu'il n'y a aucune transition menant à l'unique état initial
        for transition in self.transitions:  # on parcourt toutes les transitions
            if transition[2] == initial_state.get_value():  # on regarde si l'état d'arrivée de la transition correspond à l'état initial
                return False

        # si les deux conditions sont remplies, l'automate est standard
        return True

    # méthode pour standardiser l'automate
    def standardize(self):  # fonction qui standardise l'automate

        if self.is_standard():  # Si l'automate est déjà standard, on ne fait rien
            return False

        # stockage des anciens états
        old_states = self.states.copy()

        # ajout de l'état initial I qui aura pour valeur I
        new_initial_state = State(self, ["I"])

        # mettre la valeur is_initial de I initial à True
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


        for letter in self.alphabet:
            new_initial_state.transitions[letter].sort()


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
        self.states.sort(key=lambda x: x.value)


        return True

    # ------------------------------------------------------------------------------------------ #

    # -------------------------------- Completion (Camille) ------------------------------------ #

    # méthode pour vérifier si l'automate est complet
    def is_complete(self):

        # vérification que chaque état a une transition pour chaque symbole de l'alphabet
        for state in self.states:
            for symbol in self.alphabet:
                if state.transitions[symbol] == []:
                    print("Erreur : l'automate n'est pas complet car l'état " + state.get_value() + " n'a pas de transition pour le symbole " + symbol)
                    return False
        return True

    # méthode pour compléter l'automate
    def complete(self):

        if self.is_complete():
            return True

        else:

            P = State(self, ["P"])                                  # création d'un nouvel état P
            for symbol in self.alphabet:                           # on met P comme destination de chaque transition
                P.transitions[symbol] = [P.get_value()]

            for state in self.states:                              # on parcourt les états existants
                for symbol in self.alphabet:                       # on parcourt les symboles de l'alphabet
                    if state.transitions[symbol] == []:            # si l'état n'a pas de transition pour le symbole on ajoute P
                        state.transitions[symbol] = [P.get_value()]

            self.states.append(P)                                 # on ajoute P à la liste des états

            return self

    # ------------------------------------------------------------------------------------------ #

    # ----------------------------- Determinisation (Abdel-Waheb) ------------------------------ #

    # méthode pour vérifier si l'automate est déterministe
    def is_deterministic(self):
        # On regarde si il y a plusieurs états initiaux
        if len(self.initals_states) != 1:
            print("Erreur : l'automate n'est pas déterministe car il y a plusieurs états initiaux")
            return False
        # Vérifier si chaque état a exactement une transition pour chaque symbole de l'alphabet
        for state in self.states:
            for letter, destinations in state.transitions.items():
                if len(destinations) != 1:
                    print("Erreur : l'automate n'est pas déterministe car l'état " + state.get_value() + " a plusieurs transitions pour la lettre " + letter)
                    return False
        return True

    # méthode pour remplir un tableau temporaire contenant les destinations des arretes de chaque état
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

    # méthode pour vérifier si il y a des doublons dans une chaine de caractères
    def check_doublons_str(self, chaine):
        chaine = ''.join(sorted(chaine))
        resultat = ''
        i = 0
        while i < len(chaine):
            count = 0
            while i + 1 < len(chaine) and chaine[i] == chaine[i + 1]:
                i += 1
                count += 1
            if count < 2:
                resultat += chaine[i]
            i += 1
        return resultat

    # méthode pour remplir les transitions d'un nouvel état
    def fill_transitions(self, state):
        for v in state.values:                        # on parcourt les valeurs de l'état
            for l in self.alphabet:                   # on parcourt les lettres de l'alphabet
                for s in self.states:                 # on parcourt les états existants
                    if s.value == v:                  # on vérifie si la valeur de l'état correspond à la valeur de l'état existant
                        union = set(state.transitions[l]).union(set(s.transitions[l]))         # on fait l'union des transitions de l'état existant et de l'état courant
                        union = sorted(list(union))                                            # on trie l'union
                        union = "".join(union)                                                 # on convertit l'union en chaine de caractères
                        union = self.check_doublons_str(union)                                 # on vérifie si il y a des doublons dans l'union
                        state.transitions[l] = [union]                                         # on ajoute l'union à la transition de l'état



    # méthode pour vérifier si il y a des doublons dans les transitions
    def check_doublons_tab(self, tab):
        for e in tab:
            for i in tab:
                if e in i and e != i:
                    return True
        return False

    # méthode pour déterminiser l'automate
    def determine(self):

        # si l'automate n'est pas complet, on le complète
        if not self.is_complete():
            self.complete()

        # si l'automate est déjà déterminisé, on ne fait rien
        if self.is_deterministic():
            return False

        new_states = []  # initialisation de la liste des nouveaux états

        # si il y a plusieurs états initiaux, on les fusionne
        if len(self.initals_states) > 1:
            temp_values = [str(s.values[0]) for s in self.initals_states]
            initial_state = State(self, temp_values, True, "".join(temp_values))
            initial_state.is_initial = True
            for s in self.initals_states:
                if s.is_initial:
                    s.is_initial = False
            self.states.append(initial_state)
            new_states.append(initial_state)
            self.fill_transitions(self.states[-1])
            self.fill_transitions(new_states[-1])
        else:
            temp_state = State(self, self.initals_states[0].values, True, self.initals_states[0].get_value())
            new_states.append(temp_state)
            self.fill_transitions(temp_state)

        # création d'un tableau temporaire contenant les destinations des arretes de chaque état
        temp_tab = self.fill_temp_tab()


        # déterminisation de l'automate
        for i, state in enumerate(self.states):                                                # on parcourt les états
            for l in range(len(self.alphabet)):                                                # on parcourt les lettres de l'alphabet
                value = ''.join(temp_tab[i][l])                                                # on récupère la valeur de la transition
                value = ''.join(sorted(value))                                                 # on trie la valeur
                if value not in [s.get_value() for s in self.states]:                          # on vérifie si la transition n'existe pas déjà
                    if(self.check_doublons_tab(temp_tab[i][l])):                               # si il y a des doublons dans les transitions on quitte la boucle
                        break
                    values = re.split(r'(?<!-)', value)
                    values = [x for x in values if x]
                    self.states[i].transitions[self.alphabet[l]] = [value]                     # on ajoute la transition à l'état
                    self.states.append(State(self, values, True, value))                       # on ajoute un nouvel état avec comme valeur les valeurs de la transition vers un état pas encore existant
                    new_states.append(self.states[-1])                                         # on ajoute le nouvel état à la liste des nouveaux états
                    self.fill_transitions(self.states[-1])                                     # on remplit les transitions de ce nouvel état
                    self.fill_transitions(new_states[-1])                                      # on remplit les transitions de ce nouvel état
                    temp_tab = self.fill_temp_tab()                                            # on met à jour le tableau temporaire


        self.states = new_states.copy()                                                        # on met à jour les états

        for state in self.states:                                                               # on parcourt les états
            for letter in self.alphabet:                                                        # on parcourt les lettres de l'alphabet
                if len(state.transitions[letter]) > 1:                                          # si il y a plusieurs transitions
                    state.transitions[letter] = ["".join(state.transitions[letter])]            # on garde la première transition


        # on met à jour les transitions
        for letter in self.alphabet:
            for state in self.states:
                for destination in state.transitions[letter]:
                    if state.is_composed:
                        self.transitions.append(state.get_value() + letter + destination)

        # on met à jour les entrées et sorties
        for state in self.states:
            if state.is_composed:
                for s in self.terminal_states:
                    if s.get_value() in state.values:
                        state.is_terminal = True
                        break

        # on met à jour les états initiaux et terminaux
        self.update_initials_terminal()

        return True


    # ------------------------------------------------------------------------------------------ #


    # ------------------------------- Minimisation (Thomas) ------------------------------------ #

    # méthode pour vérifier si l'automate est minimisé
    def is_minimised(self):

        # Si l'automate à 1 seul état ou moins, alors il est minimisé
        if len(self.states) <= 1:
            return True

        # si l'automate n'est pas complet, on le complète
        if not self.is_complete():
            self.complete()

        # si l'automate n'est pas déterministe, on le déterminise
        if not self.is_deterministic():
            self.determine()

        # Initialisation de la partition 0
        P_prev = []
        P = [self.terminal_states, [state for state in self.states if state not in self.terminal_states]]

        # Si un des groupes est vide, alors l'automate est minimisé
        if P[0] == [] or P[1] == []:
            return True

        # Création du tableau de transitions
        cur_group = []

        # Création du tableau vide
        for i in range(len(self.states)):
            cur_group.append([])

        # Tableau d'alias de str pour pouvoir comparer les transitions
        P_str = []
        for i in range(len(P)):
            sub_group = []
            for j in range(len(P[i])):
                temp = [str(v) for v in P[i][j].values]
                temp_str = "".join(temp)
                sub_group.append(temp_str)
            P_str.append(sub_group)

        # Création d'un tableau d'alias int pour pouvoir avoir une correspondance dans le tab de transition sans convertir le str
        P_int = []
        for i in range(len(P)):
            sub_group = []
            for j in range(len(P[i])):
                sub_group.append(P[i][j].values[0])
            P_int.append(sub_group)

        # Parcours chaque état (lignes)
        for i in range(len(self.states)):
            # Parcours chaque transitions (colonnes)
            for j in range(len(self.alphabet)):
                # Regarde dans quel groupe de P appartient la transition actuelle
                for k in range(len(P)):
                    if (self.states[i].transitions.get(self.alphabet[j])[0] in P_str[k]):
                        cur_group[i].append(k)

        # Division des groupes
        P_new = []
        for group in range(len(P)):
            # Cas groupe indivisible car 1 seul membre
            if (len(P[group]) == 1):
                P_new.append(P[group])
            # Cas groupe à diviser
            else:
                # Création premier sous groupe, meilleur cas = tous les éléments dans mm sous groupe, sinon création d'autre sous groupes avec les autres états
                temp_list = [[P[group][0]]]
                temp_list_int = [[P_int[group][0]]]

                # Parcours de chaque état du groupe (groupe de plus de 1 élément car sinon indivisble, comme on à déjà ajouté le premier élément on commence par le 2ème)
                for state in range(1, len(P[group])):
                    # Identification d'une appartenance à un sous groupe existant
                    found = 0
                    # Parcours de chaque sous groupe pour voir appartenance
                    for k in range(len(temp_list)):
                        # Comparaison entre les transition du premier élément du groupe (même transition pour chaque élément du grp) à l'état que l'on veut insérer

                        # si l'état contient un P, on récupère l'index de l'état dans la liste des états
                        if 'P' in str(P_int[group][state]) or 'I' in str(P_int[group][state]):
                            temp = [s.get_value() for s in self.states]
                            p_index = temp.index(P_int[group][state])
                            to_compare = cur_group[p_index]
                        else:
                            to_compare = cur_group[int(P_int[group][state])]

                        if 'P' in temp_list_int[k][0] or 'I' in temp_list_int[k][0]:
                            temp = [s.get_value() for s in self.states]
                            p_index = temp.index(P_int[group][state])
                            to_compare2 = cur_group[p_index]
                        else:
                            to_compare2 = cur_group[int(temp_list_int[k][0])]

                        if to_compare2 == to_compare:
                            temp_list[k].append(P[group][state])
                            temp_list_int[k].append(P_int[group][state])
                            found = 1
                            break
                    # Si aucun match trouvé pour tout les groupes, alors on créer un nouveau groupe
                    if (found == 0):
                        temp_list.append([P[group][state]])
                        temp_list_int.append([P_int[group][state]])
                # Ajout de chaque nouveau sous groupe dans la nouvelle partition
                for l in range(len(temp_list)):
                    P_new.append(temp_list[l])

        # Mise à jour de la partition précédente et de la nouvelle partition
        return P == P_new


    # méthode pour minimiser l'automate
    def minimise(self):

        if self.is_minimised():
            return False

        # Initialisation de la partition 0
        P_prev = []
        P = [self.terminal_states, [state for state in self.states if state not in self.terminal_states]]

        while (P_prev != P) :

            # Création du tableau de transitions
            cur_group = []

            # Création du tableau vide
            for i in range(len(self.states)):
                cur_group.append([])

            # Tableau d'alias de str pour pouvoir comparer les transitions
            P_str = []
            for i in range(len(P)):
                sub_group = []
                for j in range(len(P[i])):
                    temp = [str(v) for v in P[i][j].values]
                    temp_str = "".join(temp)
                    sub_group.append(temp_str)
                P_str.append(sub_group)


            # Création d'un tableau d'alias int pour pouvoir avoir une correspondance dans le tab de transition sans convertir le str
            P_int = []
            for i in range(len(P)):
                sub_group = []
                for j in range(len(P[i])):
                    sub_group.append(P[i][j].values[0])
                P_int.append(sub_group)

            # Parcours chaque état (lignes)
            for i in range(len(self.states)):
                # Parcours chaque transitions (colonnes)
                for j in range(len(self.alphabet)) :
                    # Regarde dans quel groupe de P appartient la transition actuelle
                    for k in range(len(P)):
                        if (self.states[i].transitions.get(self.alphabet[j])[0] in P_str[k]) :
                            cur_group[i].append(k)

            # Division des groupes
            P_new = []
            for group in range(len(P)):
                # Cas groupe indivisible car 1 seul membre
                if (len(P[group])==1):
                    P_new.append(P[group])
                # Cas groupe à diviser
                else :
                    # Création premier sous groupe, meilleur cas = tous les éléments dans mm sous groupe, sinon création d'autre sous groupes avec les autres états
                    temp_list = [[P[group][0]]]
                    temp_list_int = [[P_int[group][0]]]

                    # Parcours de chaque état du groupe (groupe de plus de 1 élément car sinon indivisble, comme on à déjà ajouté le premier élément on commence par le 2ème)
                    for state in range(1, len(P[group])):
                        # Identification d'une appartenance à un sous groupe existant
                        found = 0
                        # Parcours de chaque sous groupe pour voir appartenance
                        for k in range(len(temp_list)):
                            # Comparaison entre les transition du premier élément du groupe (même transition pour chaque élément du grp) à l'état que l'on veut insérer

                            # si l'état contient un P, on récupère l'index de l'état dans la liste des états
                            if 'P' in str(P_int[group][state]) or 'I' in str(P_int[group][state]):
                                temp = [s.get_value() for s in self.states]
                                p_index = temp.index(P_int[group][state])
                                to_compare = cur_group[p_index]
                            else:
                                to_compare = cur_group[int(P_int[group][state])]

                            if 'P' in temp_list_int[k][0] or 'I' in temp_list_int[k][0]:
                                temp = [s.get_value() for s in self.states]
                                p_index = temp.index(P_int[group][state])
                                to_compare2 = cur_group[p_index]
                            else:
                                to_compare2 = cur_group[int(temp_list_int[k][0])]

                            if to_compare2 == to_compare:
                                temp_list[k].append(P[group][state])
                                temp_list_int[k].append(P_int[group][state])
                                found = 1
                                break
                        # Si aucun match trouvé pour tout les groupes, alors on créer un nouveau groupe
                        if (found==0) :
                            temp_list.append([P[group][state]])
                            temp_list_int.append([P_int[group][state]])
                    # Ajout de chaque nouveau sous groupe dans la nouvelle partition
                    for sub_groups in range(len(temp_list)):
                        P_new.append(temp_list[sub_groups])


            # Mise à jour de la partition précédente et de la nouvelle partition

            P_prev = P.copy()
            P = P_new.copy()

        # Initialisations des nouveaux éléments de l'automate
        new_states = []
        new_initial = []
        new_finals = []
        new_transitions = []

        # Création des nouveaux étatsenumerate
        for index, group in enumerate(P):

            # on crée un nouvel état
            new_state = State(self, str(index))

            # on parcourt les transitions du nouvel état pour les remplir
            for l in self.alphabet:

                # on parcourt les états des groupes
                for index2, group2 in enumerate(P):
                    for state2 in group2:

                        # si l'état correspond on ajoute la transition
                        if group[0].transitions[l] == [str(state2.get_value())]:
                            new_state.transitions[l] = [index2]

            for state in group:
                if state.is_initial:
                    new_state.is_initial = True
                if state.is_terminal:
                    new_state.is_terminal = True

            # on ajoute le nouvel état à la liste des nouveaux états
            new_states.append(new_state)


        # Création des nouvelles transitions
        for state in new_states:
            for l in self.alphabet:
                new_transitions.append(str(state.get_value()) + l + str(state.transitions[l][0]))


        # Mise à jour des champs de l'automate
        self.states = new_states.copy()
        self.transitions = new_transitions.copy()
        self.update_initials_terminal()

        return True


    # ------------------------------------------------------------------------------------------ #


    # ----------------------- Reconnaisance et Complémentaire (Maryam) ------------------------- #

    # méthode pour reconnaitre un mot
    def recognize(self, word):

        # vérifications: déterministe, mot dans l'alphabet
        if not self.is_deterministic():
            print("Erreur : l'automate n'est pas déterministe")
            return False

        for letter in word:
            if letter not in self.alphabet:
                print("Erreur : le mot contient des lettres qui ne sont pas dans l'alphabet")
                return False

        # initialisation de la liste des états actifs
        active_states = self.initals_states.copy()

        # parcours des lettres du mot
        for letter in word:

            # initialisation de la liste des états actifs temporaire
            temp_active_states = []

            # parcours des états actifs
            for state in active_states:

                # ajout des états de destination à la liste des états actifs temporaire
                temp_transition = [str(x) for x in state.transitions[letter]]
                temp_active_states += [s for s in self.states if s.get_value() in temp_transition]

            # mise à jour de la liste des états actifs
            active_states = temp_active_states.copy()

        # vérification si un des états actifs est terminal
        print("Le mot est reconnu") if any(state.is_terminal for state in active_states) else print("Le mot n'est pas reconnu")
        return any(state.is_terminal for state in active_states)

    # méthode pour donner le complémentaire de l'automate
    def completary(self):

        passerelle = []                                         # initialisation d'une liste passerelle

        for state in self.states:                               # parcours des états
            if not state.is_terminal:                           # si l'état n'est pas terminal on le rend terminal
                passerelle.append(state.get_value())
            state.is_terminal = not state.is_terminal           # on inverse la valeur de is_terminal

        self.terminal_states = passerelle                       # on met à jour les états terminaux

    # ------------------------------------------------------------------------------------------ #


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


