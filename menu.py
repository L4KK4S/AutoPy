from automaton import Automaton
import file
import os

class Main:

    def __init__(self):
        self.run = True
        self.title_ascii = """
  __   _  _  ____  __  ____  _  _ 
 / _\ / )( \(_  _)/  \(  _ \( \/ )
/    \) \/ (  )( (  O )) __/ )  / 
\_/\_/\____/ (__) \__/(__)  (__/  
                                """
        self.commands = "0. Aide\n1. Liste des commandes\n2. Charger un automate\n3. Liste des automates\n4. Opérations sur les automates\n9. Quitter"
        self.automatons = []
        self.automaton = None

    def menu(self, with_title=False):

        if with_title:
            print(self.title_ascii)

        print(self.commands)

        while self.run:
            choice = input("\n>> ")

            if choice == "0":
                print("Aide")
            elif choice == "1":
                print("\n" + self.commands)
            elif choice == "2":
                self.load_automaton()
            elif choice == "3":
                self.display_automaton()
            elif choice == "4":
                self.select_automaton()
                self.operation_choice()
            elif choice == "8":
                pass
            elif choice == "9":
                print("Au revoir !")
                self.run = False
            else:
                print("Choix invalide. Veuillez réessayer.")

    def file_input(self):

        is_input_valid = False

        while not is_input_valid:
            input_text = input("Entrez le nom du fichier contenant l'automate : ")
            if not input_text.endswith('.txt') and '?' not in input_text and 'q' not in input_text:
                print("La saisie n'est pas valide. Veuillez réessayer.")
            elif input_text.endswith('.txt') and not os.path.exists(input_text):
                print("Le fichier spécifié n'existe pas. Veuillez réessayer.")
            else:
                is_input_valid = True

        if input_text == "?":

            file.root.mainloop()
            input_text = file.file

            if not input_text.endswith('.txt'):
                print("Le fichier spécifié n'est pas valide. Veuillez réessayer.")
                input_text = self.file_input()
            elif not os.path.exists(input_text):
                print("Le fichier spécifié n'existe pas. Veuillez réessayer.")
                input_text = self.file_input()

        if input_text == "q":
            return "q"

        return input_text

    def validate_input(self, input_text):

        if input_text == "q":
            return True

        is_input_valid = False

        while 1:
            validation_input = input("Voulez-vous valider l'automate ? (o/n) : ")
            if validation_input not in ["o", "n"]:
                print("La saisie n'est pas valide. Veuillez réessayer.")
            elif validation_input == "o":
                return True
            elif validation_input == "n":
                return False

    def load_automaton(self):

        print("")

        input_text = self.file_input()
        while not self.validate_input(input_text):
            input_text = self.file_input()

        if input_text == "q":
            print("Opération annulée.")
        else:
            self.automatons.append(Automaton(input_text))
            print("Automate chargé avec succès.")

    def display_automaton(self):

        if len(self.automatons) == 0:
            print("\nAucun automate n'est enregistré.")
            return

        print("\nListe des automates enregistrés :")
        for i, automaton in enumerate(self.automatons):
            print(f"Automate n°{i+1} : {automaton.filename}")

    def select_automaton(self):

        choice = input("\nEntrez le numéro de l'automate sur lequel vous souhaitez effectuer des opérations :\n>> ").rstrip()
        while int(choice) < 1 or int(choice) > len(self.automatons) or choice == 'q':
            print("Choix invalide. Veuillez réessayer.")
            choice = input("\nEntrez le numéro de l'automate sur lequel vous souhaitez effectuer des opérations :\n>> ").rstrip()

        if choice == "q":
            return

        self.automaton = self.automatons[int(choice)-1]

    def operation_choice(self):

        print("\n0. Afficher l'automate.\n1. Standardiser l'automate\n2. Complémenter l'automate\n3. Déterminiser l'automate\n4. Minimiser l'automate\n5. Vérifier si l'automate est standard\n6. Vérifier si l'automate est complet\n7. Vérifier si l'automate est déterministe\n8. Vérifier si l'automate est minimal\n9. Retour")
        choice = -1

        while choice != "9":

            choice = input("\n>> ")

            if choice == "0":
                print(self.automaton)

            elif choice == "1":
                self.automaton.standardize()
            elif choice == "2":
                pass
            elif choice == "3":
                pass
            elif choice == "4":
                pass
            elif choice == "5":
                print("L'automate est standard.") if self.automaton.is_standard() else print("L'automate n'est pas standard.")
            elif choice == "6":
                pass
            elif choice == "7":
                pass
            elif choice == "8":
                pass
            else:
                print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main = Main()
    main.menu(with_title=True)