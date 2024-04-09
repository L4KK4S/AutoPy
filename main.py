from automaton import Automaton
import os
import graph

class Main:

    def __init__(self):
        self.run = True
        self.title_ascii = """
  __   _  _  ____  __  ____  _  _ 
 / _\ / )( \(_  _)/  \(  _ \( \/ )
/    \) \/ (  )( (  O )) __/ )  / 
\_/\_/\____/ (__) \__/(__)  (__/  
                                """
        self.help_text = "\nBienvenue sur Autopy, un programme permettant de gérer les automates finis, voici la liste des commandes et leurs fonctionalités:\n\n" \
                         "     help: permet d'afficher l'aide\n" \
                         "     list <option>: liste les différents automates chargés\n" \
                         "     load <fichier>.txt <option>: charge un automate à partir d'un fichier texte\n" \
                         "          -c: sélectionne l'automate chargé\n" \
                         "     select <numéro>: sélectionne un automate parmi la liste des automates enregistrés\n" \
                         "     current: affiche l'automate actuellement sélectionné\n" \
                         "     show: affiche le tableau des transitions de l'automate actuellement sélectionné\n" \
                         "     graph: affiche un gaphe de l'automate actuellement sélectionné\n" \
                         "     save <fichier>.txt: enregistre l'automate actuellement sélectionné dans un fichier texte\n" \
                         "     standard -<option>: opérations sur la standardisation\n" \
                         "         -v: vérifie si l'automate est standard\n" \
                         "         -a: standardise l'automate\n"\
                         "     determine -<option>: opérations sur la déterminisation\n"\
                         "         -v: vérifie si l'automate est déterministe\n" \
                         "         -a: détermine l'automate\n" \
                         "     minimise -<option>: opérations sur la minimisation\n" \
                         "         -v: vérifie si l'automate est miniminal\n" \
                         "         -a: minimise l'automate\n"
        self.automatons = []
        self.automaton = None

    # fonction principale
    def loop(self):

        print(self.title_ascii)
        print("Tapez 'help' pour afficher l'aide")

        while self.run:

            command_input = input("\n>> ")
            command = command_input.split(" ")
            #print(command)

            # commande help: affiche l'aide
            if command[0] == "help":
                print(self.help_text)

            # commande list: affiche la liste des automates enregistrés
            elif command[0] == "list":
                self.display_automaton()

            # commande load: charge un automate à partir d'un fichier texte
            elif command[0] == "load":
                if len(command) not in [2, 3]:
                    print("Erreur: nombre d'arguments invalide")
                elif len(command) == 3:
                    if command[2] != "-c":
                        print("Erreur: deuxième argument invalide")
                    else:
                        if self.input_automaton(command[1]):
                            self.automatons.append(Automaton(command[1]))
                            self.automaton = self.automatons[-1]
                            print("Automate chargé avec succès")
                else:
                    if self.input_automaton(command[1]):
                        self.automatons.append(Automaton(command[1]))
                        print("Automate chargé avec succès")

            # commande select: sélectionne un automate parmi la liste des automates enregistrés
            elif command[0] == "select":
                if len(command) != 2:
                    print("Erreur: nombre d'arguments invalide")
                elif not command[1].isdigit():
                    print("Erreur: argument invalide, ce n'est pas un nombre entier")
                elif len(self.automatons) == 0:
                    print("Erreur: aucun automate n'est enregistré")
                elif int(command[1]) < 1 or int(command[1]) > len(self.automatons):
                    print("Erreur: numéro d'automate invalide")
                else:
                    self.automaton = self.automatons[int(command[1])-1]
                    print(f"Automate n°{command[1]} sélectionné")

            # commande current: affiche l'automate actuellement sélectionné
            elif command[0] == "current":
                if self.automaton is None:
                    print("Aucun automate n'est sélectionné")
                else:
                    print(f"Automate actuel : {self.automaton.filename} - n°{self.automatons.index(self.automaton)+1}")

            # commande show: affiche l'automate actuellement sélectionné
            elif command[0] == "show":
                if self.automaton is None:
                    print("Aucun automate n'est sélectionné")
                else:
                    print(self.automaton)

            # commande graph: affiche le graphe de l'automate actuellement sélectionné
            elif command[0] == "graph":
                if self.automaton is None:
                    print("Erreur: aucun automate n'est sélectionné")
                else:
                    graph.graph(self.automaton)

            # commande standard: opérations sur la standardisation
            elif command[0] == "standard":
                if len(command) != 2:
                    print("Erreur: nombre d'arguments invalide")
                elif self.automaton is None:
                    print("Erreur: aucun automate n'est sélectionné")
                else:
                    if command[1] == "-v":
                        print("L'automate est standard") if self.automaton.is_standard() else print("L'automate n'est pas standard")
                    elif command[1] == "-a":
                        print("Automate standardisé avec succès") if self.automaton.standardize() else print("Erreur: l'automate est déjà standard")
                    else:
                        print("Erreur: argument invalide")

            # commande determine: opérations sur la déterminisation
            elif command[0] == "determine":
                if len(command) != 2:
                    print("Erreur: nombre d'arguments invalide")
                elif self.automaton is None:
                    print("Erreur: aucun automate n'est sélectionné")
                else:
                    if command[1] == "-v":
                        print("L'automate est déterministe") if self.automaton.is_deterministic() else print("L'automate n'est pas déterministe")
                    elif command[1] == "-a":
                        print("Automate déterminisé avec succès") if self.automaton.determine() else print("Erreur: l'automate est déjà déterministe")
                    else:
                        print("Erreur: argument invalide")

            # commande minimize: opérations sur la minimisation
            elif command[0] == "minimise":
                if len(command) != 2:
                    print("Erreur: nombre d'arguments invalide")
                elif self.automaton is None:
                    print("Erreur: aucun automate n'est sélectionné")
                else:
                    if command[1] == "-v":
                        print("L'automate est minimal") if self.automaton.is_minimised() else print("L'automate n'est pas minimal")
                    elif command[1] == "-a":
                        print("Automate minimisé avec succès") if self.automaton.minimise() else print("Erreur: l'automate est déjà minimal")
                    else:
                        print("Erreur: argument invalide")

            # commande save: enregistre l'automate actuellement sélectionné dans un fichier texte
            elif command[0] == "save":
                if len(command) != 2:
                    print("Erreur: nombre d'arguments invalide")
                elif self.automaton is None:
                    print("Erreur: aucun automate n'est sélectionné")
                elif not command[1].endswith('.txt'):
                    print("Erreur: ce n'est pas un fichier texte")
                elif os.path.exists(command[1]):
                    print("Erreur: le fichier spécifié existe déjà")
                else:
                    self.save_automaton(command[1])
                    print(f"Automate enregistré avec succès dans le fichier {command[1]}")



            # commande clear: efface la console
            elif command[0] == "clear":
                os.system('cls' if os.name == 'nt' else 'clear')

            # commande quit: quitte le programme
            elif command[0] == "quit" or command[0] == "exit":
                self.run = False

            # commande inconnue
            else:
                print("Commande invalide")

    # fonction pour afficher la liste des automates enregistrés
    def display_automaton(self):

        if len(self.automatons) == 0:
            print("\nAucun automate n'est enregistré.")
            return

        print("\nListe des automates enregistrés :")
        for i, automaton in enumerate(self.automatons):
            print(f"    Automate n°{i+1} : {automaton.filename}")

    # fonction pour vérifier si le fichier texte est valide
    def input_automaton(self, input_text):

        is_input_valid = False

        if not input_text.endswith('.txt') and '?' not in input_text and 'q' not in input_text:
            print("Erreur: ce n'est pas un fichier texte")
        elif input_text.endswith('.txt') and not os.path.exists(input_text):
            print("Erreur: Le fichier spécifié n'existe pas ou est introuvable")
        else:
            is_input_valid = True

        return is_input_valid

    def save_automaton(self, filename):

            with open(filename, "w") as file:

                # taille alphabet et états
                file.write(str(len(self.automaton.alphabet)) + "\n")
                file.write(str(len(self.automaton.states)) + "\n")

                # etats initiaux
                file.write(str(len(self.automaton.initals_states)) + " ")
                for state in self.automaton.initals_states:
                    file.write(state.get_value() + " ")
                file.write("\n")

                # etats terminaux
                file.write(str(len(self.automaton.terminal_states)) + " ")
                for state in self.automaton.terminal_states:
                    file.write(state.get_value() + " ")
                file.write("\n")

                # nombres de transitions
                file.write(str(len(self.automaton.transitions)) + "\n")

                # transitions
                for transition in self.automaton.transitions:
                    file.write(transition)
                    file.write("\n")


if __name__ == "__main__":
    main = Main()

    for i in range(10):
        main.automatons.append(Automaton(f"automatons/B1-{i+1}.txt"))
        main.automaton = main.automatons[i]

    main.automatons.append(Automaton("trash/test2.txt"))
    main.automaton = main.automatons[-1]

    """print(main.automaton)
    print(main.automaton.is_minimised())
    print(main.automaton.minimise())

    print(main.automaton)
    print(main.automaton.is_minimised())
"""

    main.loop()