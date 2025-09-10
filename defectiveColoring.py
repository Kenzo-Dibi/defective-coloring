import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

COULEURS = {"red", "blue", "green", "cyan", "magenta", "yellow", "black", "purple", "orange", "olive", "gray", "pink", "brown",}

#chaque sommet possede un attribut couleur
#une fois finis faire l'exception handling
#on a besoin de combien de couleur ?
#adapter les fonctions accédant au voisinage d'un sommet de manière à ce que si le sommet n'a pas de voisin. le programme continue
#le fais qu'on utilise des set peut poser  problème lors de l'assignation des couleurs -> trouver sol

#degree function(defined in networkx)
def degre_max(G: nx.Graph) -> int:
    if G is None or not isinstance(G, nx.Graph):
        raise ValueError(f"Le graphe doit être de type nx.Graph et ne peut être égal à None.")
    
    return max([degre for v, degre in G.degree()])
#neighbors function (defined in networkx)

#mixed edge edge it a tuple
def arete_melange(G: nx.Graph, edge) -> list:
    assert not G is None and not edge is None
    if G is None or not isinstance(G, nx.Graph):
        raise ValueError(f"Le graphe doit être de type nx.Graph et ne peut être égal à None.")
    elif edge is None or len(edge) <= 0:
        raise ValueError(f"La liste passé en argument ne peut pas être égal à None ni être vide")
    
    return not (quelle_couleur(G, edge[0]) == quelle_couleur(G, edge[1]))

def aretes_melange(G: nx.Graph):
    if G is None or not isinstance(G, nx.Graph):
        raise ValueError(f"Le graphe doit être de type nx.Graph et ne peut être égal à None.")
    
    return [(v1, v2) for v1, v2 in G.edges() if quelle_couleur(G, v1) != quelle_couleur(G, v2)]

#mixing number
def nombre_de_melange(G: nx.Graph)-> int:
    if G is None or not isinstance(G, nx.Graph):
        raise ValueError(f"Le graphe doit être de type nx.Graph et ne peut être égal à None.")
    
    return len(aretes_melange(G))

#secureVertex returns a list of bool
def sommet_securise(G: nx.Graph, sommet, k: int) -> bool:
    if G is None or not isinstance(G, nx.Graph):
        raise ValueError(f"Le graphe doit être de type nx.Graph et ne peut être égal à None.")
    elif k <= 0 or not isinstance(k, int):
        raise ValueError(f"k doit être un entier plus grand ou égal à 1.")
    
    return len([couleur for couleur in couleur_voisins(G, sommet) if couleur == quelle_couleur(G, sommet)]) > (1/k) * G.degree(sommet)

#secureVertices (maybe return a set since the order of the elements doesn't matter)
def sommets_securise(G: nx.Graph, k: int) -> list:
    if G is None or not isinstance(G, nx.Graph):
        raise ValueError(f"Le graphe doit être de type nx.Graph et ne peut être égal à None.")
    elif k <= 0 or not isinstance(k, int):
        raise ValueError(f"k doit être un entier plus grand ou égal à 1.")
    
    return [sommet for sommet in G.nodes() if sommet_securise(G, sommet, k)]

#whatColor
def quelle_couleur(G: nx.Graph, sommet) -> str:
    if G is None or not isinstance(G, nx.Graph):
        raise ValueError(f"Le graphe doit être de type nx.Graph et ne peut être égal à None.")
    elif sommet is None:
        raise ValueError(f"Le sommet en argument ne peut valoir None.")
    elif sommet not in G.nodes():
        return None
    else:
        return G.nodes[sommet]['couleur']

def couleur_voisins(G: nx.Graph, sommet) -> list:
    if G is None or not isinstance(G, nx.Graph):
        raise ValueError(f"Le graphe doit être de type nx.Graph et ne peut être égal à None.")
    elif sommet is None:
        raise ValueError(f"Le sommet en argument ne peut valoir None.")
    elif sommet not in G.nodes():
        return None
    
    return [quelle_couleur(G, voisins) for voisins in G.neighbors(sommet)]

#renvoie une list de tuple de la formule (couleur, occurence)
def decompte(couleurs: list) -> set:
    if couleurs is None or not isinstance(couleurs, list):
        raise ValueError(f"couleurs doit être une liste et ne peut valoir None.")
    elif len(couleurs) <= 0:
        raise ValueError(f"La liste des couleur a pour taille {len(couleurs)} alors qu'elle doit être plus grand ou égal à 1.")
    
    return {(couleur, couleurs.count(couleur)) for couleur in couleurs}

#COULEURS contient également des couleurs pas utilisé dans le graphe (TROP DE COULEURS MANQUANTE A RESOUDRE) 
def couleurs_manquante(G: nx.Graph, sommet) -> set:
    if G is None or not isinstance(G, nx.Graph):
        raise ValueError(f"Le graphe doit être de type nx.Graph et ne peut être égal à None.")
    if sommet is None:
        raise ValueError(f"Le sommet en argument ne peut valoir None.")
    
    return COULEURS - set(couleur_voisins(G, sommet))

def couleurs_moins_frequente(G: nx.Graph, sommet) -> set:
    if G is None or not isinstance(G, nx.Graph):
        raise ValueError(f"Le graphe doit être de type nx.Graph et ne peut être égal à None.")
    if sommet is None:
        raise ValueError(f"Le sommet en argument ne peut valoir None.")
    
    couleurVoisins = decompte(couleur_voisins(G, sommet))
    return min(couleurVoisins, key=lambda item: item[1])[0]

def premiere_couleurs_moins_frequente(G: nx.Graph, sommet) -> str:
    if G is None or not isinstance(G, nx.Graph):
        raise ValueError(f"Le graphe doit être de type nx.Graph et ne peut être égal à None.")
    if sommet is None:
        raise ValueError(f"Le sommet en argument ne peut valoir None.")
    
    couleursManquante = couleurs_manquante(G, sommet)
    if len(couleursManquante) > 0:
        return couleursManquante.pop()
    else:
        return couleurs_moins_frequente(G, sommet)

def change_couleur(G: nx.Graph, sommet) -> None:
    if G is None or not isinstance(G, nx.Graph):
        raise ValueError(f"Le graphe doit être de type nx.Graph et ne peut être égal à None.")
    if sommet is None:
        raise ValueError(f"Le sommet en argument ne peut valoir None.")
    
    G.nodes[sommet]["couleur"] = premiere_couleurs_moins_frequente(G, sommet)

#insecure graph coloring renvoie une liste contenant des listes de sommets (une liste = une couleur)

def initialise(G: nx.Graph, k: int, couleurs: list) -> None:
    if G is None or not isinstance(G, nx.Graph):
        raise ValueError(f"Le graphe doit être de type nx.Graph et ne peut être égal à None.")
    if k <= 0 or not isinstance(k, int):
        raise ValueError(f"k doit être un entier plus grand ou égal à 1.")
    if couleurs is None or not isinstance(couleurs, list):
        raise ValueError(f"couleurs doit être une liste et ne peut valoir None.")
    if len(couleurs) <= 0:
        raise ValueError(f"La liste des couleur a pour taille {len(couleurs)} alors qu'elle doit être plus grand ou égal à 1.")
    
    nb_sommet = len(G.nodes())
    sommets_par_couleur = nb_sommet // k
    #check if k is not smaller than len couleurs
    idx_couleur = 0
    sommet_colorie = 0
    for node in G.nodes():
        if sommet_colorie >= sommets_par_couleur:
            idx_couleur = (idx_couleur + 1) % k
            sommet_colorie = 0

        couleur = couleurs[idx_couleur]

        idx_couleur = (idx_couleur + 1) % k
        sommet_colorie += 1
        nx.set_node_attributes(G, {node: couleur}, "couleur")

def coloriage_non_securise(G: nx.Graph, k: int) -> list:
    if G is None or not isinstance(G, nx.Graph):
        raise ValueError(f"Le graphe doit être de type nx.Graph et ne peut être égal à None.")
    if k <= 0 or not isinstance(k, int):
        raise ValueError(f"k doit être un entier plus grand ou égal à 1.")
    
    sv = sommets_securise(G, k)
    while(sv != []):
        v = sv[0]
        change_couleur(G, v)
        sv = sommets_securise(G, k)

    return [G.nodes[sommet]['couleur'] for sommet in G.nodes()] 

#defective graph coloring 
def coloriage_defectueux(G: nx.Graph, c: int) -> None:
    if G is None or not isinstance(G, nx.Graph):
        raise ValueError(f"Le graphe doit être de type nx.Graph et ne peut être égal à None.")
    if c <= 0:
        raise ValueError(f"Le défaut du graphe est égal à {c} alors qu'il doit être plus grand ou égal à 0.")
    
    k = degre_max(G) // c
    if k < 1:
        k = 1
    if k > len(COULEURS):
        print(f"Il n'y a pas assez de couleurs que pour que le graphe soit k-colorier.\n")
        return
    couleurs = list(COULEURS)[0: k]
    #initialisé le graphe
    initialise(G, k, couleurs)
    #rajouter un coloriage
    coloriage_non_securise(G, k)