import pants as p
from math import *
import math as math
import random as r
import csv
import matplotlib.pyplot as mt
import networkx as network
import os


#Correspondance pour faciliter la lecture
CATEGORIE = 0
LIBELLE = 1
MOT_DIRECTEUR = 2
STATUT = 3
COMMUNE = 4
RIVOLI = 5
TENANT = 6
ABOUTISSANT = 7
BI_MIN = 8
BP_MIN = 9
BI_MAX = 10
BP_MAX = 11
DATE_CREATION = 11
DATE_MODIFICATION = 12

#Creation d'une fourmi
def create_fourmi(numero_fourmi, rue_depart, rues_livraisons):
	fourmi = {}
	fourmi["numero"] = numero_fourmi
	fourmi["rue_depart"] = rue_depart
	fourmi["rues_livraisons"] = rues_livraisons
	fourmi["rues_empruntés"] = ""
	fourmi["distance"] = 0

	return fourmi

#Méthode de travail d'une fourmi
def au_boulot(graph, fourmi):
	#Tant que on est pas passé par toutes les rues
	while(count(list(set(fourmi["rues_empruntés"]).intersection(set(fourmi["rues_livraisons"])))) != count(fourmi["rues_livraisons"])):
		#On considère que la rue de départ est une arrête

		#On prend un noeud aléatoire sur les deux noeuds existants
		noeud = graph.edges()[fourmi["rue_depart"]][r.randint(0,1)]
		
		#On va dans un nouvel rue / on récupère la données et ses propriétés
		#Ici, on prend un random, mais pour que les fourmis
		nouvelle_rue = graph.nodes()[noeud["label"]][r.randint(0,(len(noeud["label"])-1))]

		#On ajout une marque à la rue
		graph.edges()[nouvelle_rue[TENANT]][nouvelle_rue[ABOUTISSANT]]["pheromone"] += 1

		fourmi["rues_empruntés"] += nouvelle_rue
	
	return fourmi

#Toutes les 5 fourmis, le phéromone s'évapore/se dissipe
def fitness(graph, fourmi, i):
	if (i % 5 == 0):
		for u,v,d in graph.edges(data=True):
			if (d["pheromone"] > 0):
	 			d["pheromone"] - 1

	return graph

#Initialisation du graph
graph = network.Graph()

#Import du fichier CSV contenant l'ensemble des rues de la métropole de Nantes
with open("VOIES_NM.csv") as csv_file:
	reader_file = csv.reader(csv_file)

	count = 0
	for line in reader_file:
		#Initialisation d'un count pour garder le fichier original
		count += 1
		if count > 1:
			#Ce if count est là pour limiter le nombre de rues/de
			if count < 100:
				#Pour avoir un jeu de données cohérant, on évite les rues n'ayant pas de tenant ou d'aboutissant
				if (line[TENANT] != "" and line[ABOUTISSANT] != ""):

					# print(line)
					#On initialise les boîtes postales avec un min, pour que la rue ait toujours un poids minimum
					if (line[BI_MIN] == ""):
						line[BI_MIN] = 1
					else:
						line[BI_MIN] = int(line[BI_MIN])
					if (line[BP_MIN] == ""):
						line[BP_MIN] = 2
					else:
						line[BP_MIN] = int(line[BP_MIN])
					if (line[BI_MAX] == ""):
						line[BI_MAX] = line[BI_MIN]
					else:
						line[BI_MAX] = int(line[BI_MAX])
					if (line[BP_MAX] == ""):
						line[BP_MAX] = line[BP_MIN]
					else:
						line[BP_MAX] = int(line[BP_MAX])
		
					#Calcul du poids des rues, doit servir lors du calcul de la fonction de fitness
					POIDS = max(((line[BI_MAX] - line[BI_MIN])/2)+1, ((line[BP_MAX] - line[BP_MIN])/2)+1)

					NOM_COMPLET = line[COMMUNE] + " " + line[LIBELLE]

					#Ajout d'une arrête et des liens entre les noeuds
					graph.add_edge(line[TENANT], line[ABOUTISSANT], weight=POIDS, label=NOM_COMPLET, pheromone=0)

#Choix de la forme du graph
pos = network.spring_layout(graph)

#Permet de dessiner les arrêtes, les noeuds et les informations associés 
network.draw_networkx_edges(graph, pos)
network.draw_networkx_labels(graph, pos)
network.draw_networkx_nodes(graph, pos)
network.draw_networkx_edge_labels(graph, pos)

#Affiche le graph. (si des "draw_xxx" ont été réalisés)
mt.show()

#Initialisation des rues de départ et de livraison
print("Indiquer une rue de départ")
rue_depart = input()
print("Indiquer le nombre de points de livraison")
nombre_rue_livraison = input()
rues_livraisons = []

#On fait confiance à l'utilisateur pour rentrer un chiffre
for i in range(int(nombre_rue_livraison)):
	print("Indiquer une rue de livraison")
	rues_livraisons.append(input())


#Création de X fourmis
print("Indiquer le nombre de fourmi à envoyer")
nbr_fourmi = r.randint(1,10)

for i in range(nbr_fourmi):
	fourmi = create_fourmi(i, rue_depart, rues_livraisons)
	fourmi = au_boulot(graph, fourmi)
	graph = fitness(graph, fourmi, i)

#On redessine le graph
network.draw_networkx_edge_labels(graph, pos)

os.system("pause")


