# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 19:33:23 2022

@author: hemar
"""

import random
import math

class individu:
    def __init__(self, params=None):
        if params==None or len(params)!=6:
            self.params=[random.uniform(-100,100) for i in range(6)]
        else:
            self.params=params
        self.image_funcX = []
        self.image_funcY = []
        self.scoreX = 0
        self.scoreY = 0
        
    def __str__(self):
        sentence=""
        for param in self.params:
            sentence+=str(param) + " "
        return sentence
        
    def funct(self, t):
        return [self.params[0]*math.sin(self.params[1]*t + self.params[2]), self.params[3]*math.sin(self.params[4]*t + self.params[5])]
    
    def fitnessX(self, position_sample):
        self.image_funcX.clear()
        self.score = 0
        for i in range(len(position_sample)):
            self.image_funcX.append(self.funct(position_sample[i][0]))
            #self.score += math.sqrt((self.image_func[i][0] - position_sample[i][1])**2 + (self.image_func[i][1] - position_sample[i][2])**2)
            self.scoreX += abs(self.image_funcX[i][0] - position_sample[i][1])
        return self.scoreX
    
    def fitnessY(self, position_sample):
        self.image_funcY.clear()
        self.score = 0
        for i in range(len(position_sample)):
            self.image_funcY.append(self.funct(position_sample[i][0]))
            #self.score += math.sqrt((self.image_func[i][0] - position_sample[i][1])**2 + (self.image_func[i][1] - position_sample[i][2])**2)
            self.scoreY += abs(self.image_funcY[i][1] - position_sample[i][2]) 
        return self.scoreY

def create_rand_pop(count):
    ind_list = []
    for i in range(count):
        ind_list.append(individu())
    return ind_list

def evaluate(pop, position_sample, forX):
    if forX:
        pop.sort(key=lambda ind: int(ind.fitnessX(position_sample)))
    else:
        pop.sort(key=lambda ind: int(ind.fitnessY(position_sample)))
    return pop

def selection(pop, hcount, lcount):
    return pop[:hcount] + pop[len(pop)-lcount:]

def croisement(ind1,ind2):
    new_ind = individu()
    for i in range(6):
        new_ind.params[i] = (ind1.params[i] + ind2.params[i])/2
    return new_ind

def mutation(ind):
    new_ind=individu(list(ind.params))
    new_ind.params[random.randint(0, 5)] = random.uniform(-100,100)
    return new_ind


def loop():
    popX=create_rand_pop(10)
    popY=create_rand_pop(10)
    solutiontrouvee=False
    nbiteration=0
    while not solutiontrouvee and nbiteration < 5000:
        print("iteration numéro : ", nbiteration)
        nbiteration+=1
        evaluationX=evaluate(popX, position_sample, True)
        evaluationY=evaluate(popY, position_sample, False)
        if evaluationX[0].fitnessX(position_sample) + evaluationY[0].fitnessY(position_sample)<0:
            solutiontrouvee=True
        else:
            selectX=selection(evaluationX,5,2)+create_rand_pop(3)
            selectY=selection(evaluationY,5,2)+create_rand_pop(3)
            croisesX=[]
            croisesY=[]
            for i in range (len(selectX)//2):
                croisesX.append(croisement(selectX[random.randint(0, len(selectX)-1)], selectX[random.randint(0, len(selectX)-1)]))
                croisesY.append(croisement(selectY[random.randint(0, len(selectY)-1)], selectY[random.randint(0, len(selectY)-1)]))
            mutesX=[]
            mutesY=[]
            for i in selectX:
                if random.randint(-3, 7) > 0:
                    mutesX.append(mutation(i))
            for i in selectY:
                if random.randint(-3, 7) > 0:
                    mutesY.append(mutation(i))
            popX=selectX[:]+croisesX[:]+mutesX[:]
            popY=selectY[:]+croisesY[:]+mutesY[:]
        print("score fitness : ", evaluationX[0].fitnessX(position_sample) + evaluationY[0].fitnessY(position_sample))
    solution=[evaluationX[0].params[0], evaluationX[0].params[1], evaluationX[0].params[2], evaluationY[0].params[0], evaluationY[0].params[1], evaluationY[0].params[2]]
    return individu(solution)
       
            
if __name__ == "__main__":
    f=open(r'position_sample.csv', 'r')
    lines = f.readlines()
    position_sample = []
    for i in range(1,len(lines)):
        position_sample.append(lines[i].replace('\n','').split(";"))
        for j in range(3):
            position_sample[i-1][j] = float(position_sample[i-1][j])
            
    loop()

