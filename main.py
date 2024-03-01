class Automate:
    def __init__(self, alphabet, etats, etats_initiaux, etats_terminaux, transitions):
        self.alphabet = alphabet
        self.etats = etats
        self.etats_initiaux = etats_initiaux
        self.etats_terminaux = etats_terminaux
        self.transitions = transitions

def lire_automate(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        alphabet_size = int(lines[0])
        etats_size = int(lines[1])
        etats = list(range(etats_size))  # Crée une liste d'états
        etats_initiaux = list(map(int, lines[2].split()[1:]))
        etats_terminaux = list(map(int, lines[3].split()[1:]))
        transitions = []
        for line in lines[5:]:
            transition_data = line.strip()
            etat_depart = int(transition_data[0])
            symbole = transition_data[1]
            etat_arrivee = int(transition_data[2])
            transitions.append((etat_depart, symbole, etat_arrivee))
        return Automate(alphabet_size, etats, etats_initiaux, etats_terminaux, transitions)

def afficher_automate(automate):
    # Collecte de tous les symboles uniques
    symboles = sorted(set(transition[1] for transition in automate.transitions))

    # Création des en-têtes de colonnes
    headers = ["État"] + symboles

    # Affichage de la première ligne
    print("┌─────────" + "┬─────────" * len(symboles) + "┐")

    # Affichage des en-têtes
    print("│", end="")
    for header in headers:
        print(header.center(9), end="│")
    print("")

    # Affichage de la ligne de séparation
    print("├─────────" + "┼─────────" * len(symboles) + "┤")

    # Affichage des lignes de transition
    for etat in automate.etats:
        print("│", end="")
        print(str(etat).center(9), end="│")
        for symbole in symboles:
            transitions = [transition[2] for transition in automate.transitions if transition[0] == etat and transition[1] == symbole]
            if transitions:
                print(",".join(map(str, transitions)).center(9), end="│")
            else:
                print("-".center(9), end="│")
        print("")

    # Affichage de la ligne de fin
    print("└─────────" + "┴─────────" * len(symboles) + "┘")

def main():
    filename = input("Entrez le nom du fichier contenant l'automate : ")
    automate = lire_automate(filename)
    afficher_automate(automate)

if __name__ == "__main__":
    main()

