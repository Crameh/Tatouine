# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 17:33:40 2022

@author: hemar
"""

import random
import math
import time
import numpy as np
import matplotlib.pyplot as plt

#classe individu permettant de chercher les paramètres
class individu:
    def __init__(self, params=None):
        if params==None or len(params)!=6:
            self.params=[random.uniform(-100,100) for i in range(6)]
        else:
            self.params=params
        self.image_func = []
        self.score = 0
        
    def __str__(self):
        sentence=""
        for param in self.params:
            sentence+=str(param) + " "
        return sentence
        
    def funct(self, t):
        return [self.params[0]*math.sin(self.params[1]*t + self.params[2]), self.params[3]*math.sin(self.params[4]*t + self.params[5])]
    
    #renvoie la somme des erreurs
    def fitness(self, position_sample):
        self.image_func.clear()
        self.score = 0
        for i in range(len(position_sample)):
            self.image_func.append(self.funct(position_sample[i][0]))
            self.score += abs(self.image_func[i][0] - position_sample[i][1]) + abs(self.image_func[i][1] - position_sample[i][2])
        return self.score

#génère une liste d'individus aléatoirement
def create_rand_pop(count):
    ind_list = []
    for i in range(count):
        ind_list.append(individu())
    return ind_list

#trie une liste d'individus en fonction de leur score fitness
def evaluate(pop, position_sample):
    pop.sort(key=lambda ind: int(ind.fitness(position_sample)))
    return pop

#selectionne les hcount premiers individus et les lcount derniers individus
def selection(pop, hcount, lcount):
    return pop[:hcount] + pop[len(pop)-lcount:]

#fais la moyenne des paramètres de deux individus et retourne un individu enfant
def croisement(ind1,ind2):
    new_ind = individu()
    for i in range(6):
        new_ind.params[i] = (ind1.params[i] + ind2.params[i])/2
    return new_ind

#attribue une valeur aléatoire à un paramètre aléatoire d'un individu 
def mutation(ind):
    new_ind=individu(list(ind.params))
    r = random.randint(0, 5)
    if ind.fitness(position_sample) > 100:
        new_ind.params[r] = random.uniform(-100, 100)
    elif ind.fitness(position_sample) > 50:
        new_ind.params[r] += random.uniform(-5,5)
    elif ind.fitness(position_sample) > 10:
        new_ind.params[r] += random.uniform(-1,1)
    else:
        new_ind.params[r] += random.uniform (-0.2,0.2)
    return new_ind
   
def loop():
    start = time.time() #je lance le chronomètre
    pop=create_rand_pop(65) #je crée ma population
    solutiontrouvee=False
    nbiteration=0
    while not solutiontrouvee and nbiteration < 50000:
        nbiteration+=1
        evaluation=evaluate(pop, position_sample) #je trie ma population
        if evaluation[0].fitness(position_sample)<0:
            solutiontrouvee=True
        else:
            select=selection(evaluation,12,4)+create_rand_pop(10)
            croises=[]
            for i in range (len(select)//2):
                croises.append(croisement(select[random.randint(0, len(select)-1)], select[random.randint(0, len(select)-1)]))
            mutes=[]
            for i in select:
                mutes.append(mutation(i))
            pop=select[:]+croises[:]+mutes[:]
        print("score fitness : ", evaluation[0].fitness(position_sample), "| génération numéro : ", nbiteration, "| temps : ", format(time.time()-start))
    end = time.time()
    print(format(end-start))
    for i in range(6):
        print("p" + str(i + 1) + " = ", evaluation[0].params[i])
    return evaluation[0].params
                 
if __name__ == "__main__":
    f=open(r'position_sample.csv', 'r')
    lines = f.readlines()
    position_sample = []
    for i in range(1,len(lines)):
        position_sample.append(lines[i].replace('\n','').split(";"))
        for j in range(3):
            position_sample[i-1][j] = float(position_sample[i-1][j])
            
    solution = loop()
    file = open("He_Marc_groupeB.txt", "w")
    line = ""
    for i in range(6):
        line += str(solution[i]) + ";"
    
    file.write(line[:-1])
    file.close()
    
    # Cette partie du code sert simplement à avoir une représentation graphique
    # de ce que nous estimons. Plus les points verts sont proches de points rouges
    # plus notre solution est proche de ce que l'on recherche.    
    p1=solution[0]
    p2=solution[1]
    p3=solution[2]
    p4=solution[3]
    p5=solution[4]
    p6=solution[5]
    
    X = [x[1] for x in position_sample]
    Y = [y[2] for y in position_sample]
    T = [t[0] for t in position_sample]
    plt.scatter(X,Y, color = "red") #les points trouvés selon le fichier
    tps = np.arange(0,2*np.pi, 0.01)
    L_X = []
    L_Y = []
    for elt in tps:
        L_X.append(p1*np.sin(p2*elt+p3))
        L_Y.append(p4*np.sin(p5*elt+p6))
    ListeX = []
    ListeY = []
    for elt in T:
        ListeX.append(p1*np.sin(p2*elt+p3))
        ListeY.append(p4*np.sin(p5*elt+p6))

    plt.scatter(ListeX, ListeY, color = 'GREEN') #les points calculés par p1,p2,p3,p4,p5,p6 pour chaque T
    plt.plot(L_X,L_Y) #le graphe de la trajectoire avc les p1,p2,p3,p4,p5,p6 trouvés dans l'intervalle [0;2pi]
    plt.title("Trajectoire")
    plt.xlabel("x")
    plt.ylabel("y")
