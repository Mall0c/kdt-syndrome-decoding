import numpy as np
import sys

# Author: Richard Steinbrecht (richardsteinbrecht@hotmail.de)

# Generatormatrix aufstellen. Hier sind als kleiner Test die beiden Generatormatrizen aus Zettel 5 angegeben.
G = np.array([[1, 1, 1, 0, 0], [1, 0, 0, 1, 0], [0, 1, 0, 0, 1]])
#G = np.array([[0, 1, 1, 1, 0, 1, 0], [1, 0, 1, 0, 0, 1, 1], [0, 1, 0, 0, 1, 1, 1]])

# Mit True werden zusätzlich alle Nebenklassen in der Konsole ausgegeben
printClasses = False

# Der Nullvektor ist immer enthalten. Falls er in G nicht angegeben ist, wird er hinzugefügt.
zero_vector = [np.zeros((np.size(G, 1),), dtype=int)]
is_zero_vector_in_G = (zero_vector == G).all(1).any()
if not is_zero_vector_in_G:
    G = np.append(G, zero_vector, axis = 0)

# Code C definieren: alle linear abhängigen Vektoren aus den Zeilenvektoren der Generatormatrix.
def generateCode(G):
    # Äußere Schleife durchläuft G komplett
    for i in range(np.size(G, 0) - 1):
        # Innere Schleife startet erst bei i + 1. Effizienter Weg, um alle Summen über einer Liste zu bilden.
        # Würde die innere Schleife ebenfalls bei 0 anfangen, würde man jede Summe 2x bilden,
        # sprich bei zwei beliebigen Vektoren y und z: (y+z und z+y); so aber nur 1x (nämlich y+z).
        for j in range(i + 1, np.size(G, 0) - 1):
            vector = [(G[i] + G[j]) % 2]
            # Prüfen, ob der berechnete, linear abhängige Vektor bereits in G enthalten ist. Wenn nicht, wird er hinzugefügt
            # und die gesamte Funktion wird erneut aufgerufen, um die Summen ebenfalls mit dem neuen Vektor zu bilden.
            is_vector_in_G = (vector == G).all(1).any()
            if not is_vector_in_G:
                G = np.append(G, vector, axis = 0)
                G = generateCode(G)
                return G
    return G

# Nimmt eine Zahl x, und gibt ein numpy Array in Binärdarstellung der Zahl zurück.
def unpackbits(x, num_bits):
    xshape = list(x.shape)
    x = x.reshape([-1, 1])
    to_and = 2**np.arange(num_bits).reshape([1, num_bits])
    return (x & to_and).astype(bool).astype(int).reshape(xshape + [num_bits])

# Nimmt einen Code und liefert alle Nebenklassen samt deren Vertreter zurück.
def generateClasses(G):
    # Anzahl disjunkter Nebenklassen.
    number_of_disjunct_classes = int(pow(2, np.size(G, 1)) / np.size(G, 0))
    # Die erste Klasse ist C selber.
    classes = np.array([G])
    # Vektoren werden aus der Binärdarstellung von Zahlen gebildet, beginnend mit 1 = [1 0 0 0 . . .]
    # und mit den bereits gebildeten Nebenklassen abgeglichen.
    number = 1
    while(np.size(classes, 0) < number_of_disjunct_classes):
        number_in_array = np.array([number])
        bits_of_number = unpackbits(number_in_array, np.size(G, 1))
        is_vector_in_G = False
        for klasse in classes:
            is_vector_in_G = (bits_of_number == klasse).all(1).any()
            if is_vector_in_G:
                break
        if not is_vector_in_G:
            classes = np.append(classes, (classes[0] + bits_of_number[:, None]) % 2, axis = 0)
        number += 1
    return classes

# Berechnet aus den Nebenklassen den jeweiligen Führer und dessen Gewicht.
def generateClassLeaders(classes):
    leaders = []
    # "klasse" ist ausnahmsweise ein deutscher Variablenname, da "class" in Python ein reserviertes Schlüsselwort ist...
    for klasse in classes:
        least_weight = sys.maxsize
        idx_of_least_weight = sys.maxsize
        for idx, vector in enumerate(klasse):
            weight = np.sum(vector)
            if weight < least_weight:
                least_weight = weight
                idx_of_least_weight = idx
        leaders.append((least_weight, klasse[idx_of_least_weight]))
    return leaders

def printLeaders(leaders):
    for idx, x in enumerate(leaders):
        print("{}: {}".format(idx, x))
            

# Code C definieren.
G = generateCode(G)
# Nebenklassen von C generieren.
classes = generateClasses(G)
# Nebenklassenführer und deren Gewicht berechnen.
leaders = generateClassLeaders(classes)
printLeaders(leaders)

if printClasses:
    print(classes)