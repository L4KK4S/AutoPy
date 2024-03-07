from automaton import Automaton
import file
import os

def file_input():

    is_input_valid = False

    while not is_input_valid:
        input_text = input("Entrez le nom du fichier contenant l'automate : ")
        if not input_text.endswith('.txt') and '?' not in input_text:
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
            input_text = file_input()
        elif not os.path.exists(input_text):
            print("Le fichier spécifié n'existe pas. Veuillez réessayer.")
            input_text = file_input()


    return input_text

def validate_input(input_text):

    is_input_valid = False

    while 1:
        validation_input = input("Voulez-vous valider l'automate ? (o/n) : ")
        if validation_input not in ["o", "n"]:
            print("La saisie n'est pas valide. Veuillez réessayer.")
        elif validation_input == "o":
            return True
        elif validation_input == "n":
            return False


def main():


    input_text = file_input()
    while not validate_input(input_text):
        input_text = file_input()

    automaton1 = Automaton(input_text)
    print(automaton1)

    """automaton1 = Automaton("bob.txt")
    print(automaton1)"""

    automaton1.is_standard()
if __name__ == "__main__":
    main()
    print()