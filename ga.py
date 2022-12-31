#https://www.youtube.com/watch?v=mSqZqvm7YUA&list=PLZgdMIFoNTxnfoBnUhHYb4FEeZrCW-2Iq
#https://learnwithpanda.com/2020/08/09/adaptive-re-start-hybrid-genetic-algorithm-for-global-optimization-python-code/
import re
import numpy as np
import random
fitness=[]
def inputs(strs):
    l=re.findall("[A-Z a-z]",r1)
    dictStr=dict(map(lambda x:[x,"_[{i}]".format(i=l.index(x))],l));
    # for j in range(len(l)):
    #   x = strs.find(l[j])
    #   strs=strs.replace(strs[x],"_[{j}]".format(j=j))
    return dictStr
def ch(_,L):
    d=list(map(inputs,L))
    """l3=re.findall("[A-Z a-z]",r3)
    for k in range(len(l3)):
      x3= r3.find(l3[k])
      r3=r3.replace(r3[x3],"_[{k}]".format(k=k))"""
    return eval(" and ".join(d))
r1="2*x+2*y+2*z<=300"
"""l=re.findall("[A-Z a-z]",r1)
for j in range(len(l)):
  x = r1.find(l[j])
  r1=r1.replace(r1[x],"_[{j}]".format(j=j))"""
#r1=inputs(r1)
r2="4*x+2*y<=400"
"""l2=re.findall("[A-Z a-z]",r2)
for f in range(len(l2)):
  x2 = r2.find(l2[f])
  r2=r2.replace(r2[x2],"_[{f}]".format(f=f))"""
#r2=inputs(r2)
r3="x+2*y+3*z<=200"
#r3=inputs(r3)
#print(ch([543534,75345,7435],[r1,r2,r3]))
def findno(strr):
    no=len(re.findall("[A-Z a-z]",strr))
    return no
def objective_function(pop):
    fitness = np.zeros(pop.shape[0])
    for i in range(pop.shape[0]):
        _= pop[i]
        r="10*x+15*y+20*z"
        l=re.findall("[A-Z a-z]",r)
        for j in range(len(l)):
          x = r.find(l[j])
          r=r.replace(r[x],"_[{j}]".format(j=j))
        if ch(_,[r1,r2,r3]):
          fitness[i] = eval(r)
    return fitness



def selection(pop, fitness, pop_size):
    next_generation = np.zeros((pop_size, pop.shape[1]))
    elite = np.argmax(fitness)
    next_generation[0] = pop[elite]  # keep the best
    fitness = np.delete(fitness, elite)
    pop = np.delete(pop, elite, axis=0)
    #if sum(fitness)!=0:
    #P = [f / sum(fitness) for f in fitness]  # selection probability
    #else:
     #   P=[ for f in fitness]
    index = list(range(pop.shape[0]))
    index_selected = np.random.choice(index, size=pop_size - 1, replace=False)
    s = 0
    for j in range(pop_size - 1):
        next_generation[j + 1] = pop[index_selected[s]]
        s += 1
    return next_generation


def crossover(pop, crossover_rate):
    offspring = np.zeros((crossover_rate, pop.shape[1]))
    for i in range(int(crossover_rate / 2)):
        r1 = random.randint(0, pop.shape[0] - 1)
        r2 = random.randint(0, pop.shape[0] - 1)
        while r1 == r2:
            r1 = random.randint(0, pop.shape[0] - 1)
            r2 = random.randint(0, pop.shape[0] - 1)
        cutting_point = random.randint(1, pop.shape[1] - 1)
        offspring[2 * i, 0:cutting_point] = pop[r1, 0:cutting_point]
        offspring[2 * i, cutting_point:] = pop[r2, cutting_point:]
        offspring[2 * i + 1, 0:cutting_point] = pop[r2, 0:cutting_point]
        offspring[2 * i + 1, cutting_point:] = pop[r1, cutting_point:]
    return offspring


def mutation(pop, mutation_rate):
    offspring = np.zeros((mutation_rate, pop.shape[1]))
    for i in range(int(mutation_rate / 2)):
        r1 = random.randint(0, pop.shape[0] - 1)
        r2 = random.randint(0, pop.shape[0] - 1)
        while r1 == r2:
            r1 = random.randint(0, pop.shape[0] - 1)
            r2 = random.randint(0, pop.shape[0] - 1)
        cutting_point = random.randint(0, pop.shape[1] - 1)
        offspring[2 * i] = pop[r1]
        offspring[2 * i, cutting_point] = pop[r2, cutting_point]
        offspring[2 * i + 1] = pop[r2]
        offspring[2 * i + 1, cutting_point] = pop[r1, cutting_point]
    return offspring



def local_search (pop,fitness ,lower_bounds, upper_bounds, step_size, rate):
    index = np.argmax(fitness)
    offspring = np.zeros ((rate *2 * pop.shape[1], pop.shape[1]))
    for r in range(rate):
        offspring1= np.zeros((pop.shape[1], pop.shape[1]))
        for i in range(int(pop.shape[1])):
            offspring1[i] = pop[index]
            offspring1[i, i] *= np.random.uniform(0, step_size)
            if offspring1[i, i] > upper_bounds[i]:
                offspring1[i, i] = upper_bounds[i]
        offspring2 = np.zeros ((pop.shape[1], pop.shape[1]))
        for i in range(int(pop.shape[1])):
            offspring2[i] = pop[index]
            offspring2[i, i] += np.random.uniform(-step_size,0)
            if offspring2[i, i] < lower_bounds[i]:
                offspring2[i, i]  = lower_bounds[i]
        offspring12 = np.zeros((2*pop.shape[1], pop.shape[1]))
        offspring12[0:pop.shape[1]] = offspring1
        offspring12[pop.shape[1] :2 * pop.shape[1]] = offspring2
        offspring[r * 2 * pop.shape[1]:r * 2 * pop.shape[1] + 2 * pop.shape[1]] = offspring12
    return offspring





