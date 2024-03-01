from automaton import Automaton
def main():
    filename = input("Entrez le nom du fichier contenant l'automate : ")
    automaton1 = Automaton(filename)
    print(automaton1)

if __name__ == "__main__":
    main()