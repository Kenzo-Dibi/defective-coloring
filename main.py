import networkx as nx
import defectiveColoring as dc
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import argparse as ap

def main():
    graphParser = ap.ArgumentParser("Graph parsser")
    graphParser.add_argument("-i","--input", help="Fichier input")
    graphParser.add_argument("-c", help="Le nombre de sommets adjacent à tout sommet v du graphe pouvant posséder la même couleur que v.")
    graphParser.add_argument("-k", help="Permet de trouver le défaut minimal permettant d'obtenir un k-coloriage du graphe.")
    args = graphParser.parse_args()
    G = nx.Graph()
    noms = []
    som = []
    if args.input and args.c:
        fichier = args.input
        c = int(args.c)
        if c <= G.number_of_nodes():
            print(f"c doit être plus petit que le nombre de sommet ({G.number_of_nodes()}) dans le graphe.\n")
            return
        arbre = ET.parse(fichier)
        racine = arbre.getroot()
        #print(f"arbre: {arbre}, racine: {racine}")
        for names in racine:
            if names.tag == "sommet":
                som.append(names.text)
            elif names.tag == "arete":
                sommets = names.text.split(", ") #les sommets doit être séparer de la façon suivante:  x, y 
                noms.append(tuple(sommets))
        G.add_nodes_from(som)
        G.add_edges_from(noms)
        if len(som) <= 0 and len(noms) <= 0:
            print(f"Le graphique passé en arguement est vide. Veuillez ajouter des sommets et ou des arêtes.\n")
            return
        dc.coloriage_defectueux(G, c)

        couleur_sommets = [G.nodes[sommet]['couleur'] for sommet in G.nodes()]
        nx.draw(G,with_labels=True, node_color=couleur_sommets)
        plt.show()
    elif args.input and args.k: #check that k >= 1
        fichier = args.input
        k = int(args.k)
        if k < 1:
            print(f"Veuillez introduire une valeur plus grande ou égale à 1 pour l'arguemnt k (k choisi: {k}).\n")
        arbre = ET.parse(fichier)
        racine = arbre.getroot()
        for names in racine:
            if names.tag == "sommet":
                som.append(names.text)
            elif names.tag == "arete":
                sommets = names.text.split(", ") #les sommets doit être séparer de la façon suivante:  x, y 
                noms.append(tuple(sommets))
        G.add_nodes_from(som)
        G.add_edges_from(noms)
        if len(som) <= 0 and len(noms) <= 0:
            print(f"Le graphique passé en arguement est vide. Veuillez ajouter des sommets et ou des arêtes.\n")
            return
        print(f"Le graphe est k-colorable avec un défaut minimum valant {dc.degre_max(G)//k}.\n")
    elif (not args.input and args.k) or (not args.input and args.c):
        print(f"Argument manquant: -i/--input : S'il vous plait, veuillez utiliser l'arguement input (-i) suivi du fichier contenant votre graphe.\n")
    else:
        print(f"Arugment(s) manquant: Veuillez utiliser l'arguement help (-h) si vous souhaitez prendre connaissance des fonctionalités du programme.\n")
if __name__ == "__main__":
    main()

