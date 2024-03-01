#Lecture fichier automate

def get_alphabet (lignes) :
    alphabet = []
    for i in range(5, len(lignes)) :
        if lignes[i][1] not in alphabet :
            alphabet.append(lignes[i][1])
    alphabet = sorted(alphabet)
    return alphabet

def get_transition(matrice, lignes) :
    alphabet = get_alphabet(lignes)
    for i in range(5, len(lignes)):
        matrice[int(lignes[i][0])][alphabet.index(lignes[i][1])] = int(lignes[i][2])
    return matrice

def get_inital(lignes) :
    initial = []
    for i in range(0, len(lignes[2])-1, 2) :
        initial.append(int(lignes[2][i]))
    return initial

def get_final(lignes) :
    final = []
    for i in range(0, len(lignes[3])-1, 2) :
        final.append(int(lignes[3][i]))
    return final


with open ("Automates/bob.txt", "r") as fichier :
    lignes = fichier.readlines()
    table_transition_fichier = []

    for i in range (int(lignes[1])) :
        newline = []
        for j in range (int(lignes[0])) :
            newline.append(-1)
        table_transition_fichier.append(newline)

    table_transition_fichier = get_transition(table_transition_fichier, lignes)
    initial = get_inital(lignes)
    final = get_final(lignes)


for i in range(len(table_transition_fichier)) :
    for j in range(len(table_transition_fichier[i])) :
        if (table_transition_fichier[i][j]==-1) :
            print("-", end=" ")
        else :
            print(table_transition_fichier[i][j], end = " ")
    print()
print("Etat initiaux : ",end  = " ")
for i in range(len(initial)) :
    print(initial[i], end = " ")
print()
print("Etat finaux : ", end=" ")
for i in range(len(final)):
    print(final[i], end = " ")
