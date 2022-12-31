from django.shortcuts import render
from django.http import HttpResponse
import re
import numpy as np
import random
from time import process_time
#from .. import ga
# Create your views here.

def index(request):
 print(request.POST)
 allO={}
 
 if(request.POST.get('poly')):
  for x in request.POST:
      allO[x]=request.POST[x]
  print(allO)
  """ 
  r2=allO['constraint2']
  r3="x+2*y+3*z<=200"
  """
  result=""
  t1_start = process_time()
  print(allO)
  ss=0
  constr=[]
  for x in request.POST:
    if(re.search('constraint', x)):
      ss+=1
      if(ss==2):
        continue
      else:
        constr.append(request.POST.get(x))
  print(ss,constr)
  fitness=[]
  def inputs(strs):
    l=re.findall("[A-Z a-z]",strs)
    dictStr=dict(map(lambda x:[x,"_[{i}]".format(i=l.index(x))],l));
    # for j in range(len(l)):
    #   x = strs.find(l[j])
    #   strs=strs.replace(strs[x],"_[{j}]".format(j=j))
    return dictStr
  
  def ch(_,L): #[h,h,h]
    #d=list(map(con,L))
    #d=[0,0,0]
    #def con (strr,dd):
    f=allO['poly']
    dd=inputs(f)
    for i in range(len(L)):
        c=re.findall('[A-Z a-z]', L[i])
        for k in range(len(c)):
            c1=L[i].find(c[k])
            c2=dd[c[k]]
            L[i]=L[i].replace(L[i][c1],c2)
    """c=re.findall('[A-Z a-z]', strr)
     for k in range(len(c)):
        c1=strr.find(c[k])
        c2=dd[c[k]]
        strr=strr.replace(strr[c1],c2)
     return strr"""
    """for o in L:
        d[o]=con(L,dd)"""
    """l3=re.findall("[A-Z a-z]",r3)
    for k in range(len(l3)):
      x3= r3.find(l3[k])
      r3=r3.replace(r3[x3],"_[{k}]".format(k=k))"""
    return eval(" and ".join(L))
  def findno(strr):
    no=len(re.findall("[A-Z a-z]",strr))
    return no
  def objective_function(pop):
    fitness = np.zeros(pop.shape[0])
    for i in range(pop.shape[0]):
        _= pop[i]
        
        r=allO['poly']
        l=re.findall("[A-Z a-z]",r)
        for j in range(len(l)):
          x = r.find(l[j])
          r=r.replace(r[x],"_[{j}]".format(j=j))
        if ch(_,constr):
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
  d=allO['poly']
  #d2=inputs(d)
  
  pop_size = 100
  crossover_rate = 110
  mutation_rate = 110
  rate = 10;
  no_variables = findno(allO['poly'])
  lower_bounds = [0, 0,0]
  upper_bounds = [100, 100,100]

  step_size = (upper_bounds[0]-lower_bounds[0]) * 0.02
  computing_time = 30
  no_generations = 100000000  # because we use computing time as termination criterion
  pop = np.zeros((pop_size, no_variables))
  for s in range(pop_size):
     #for h in range(no_variables):
         t=np.zeros(no_variables)
         for i in range(no_variables):
          t[i]=random.uniform(lower_bounds[i],upper_bounds[i])
         if ch(t,constr):
             #print("constrant")
             pop[s]=t
         else:
             continue
 
  extended_pop = np.zeros((pop_size + crossover_rate + mutation_rate + 2 * no_variables * rate, pop.shape[1]))

  A = []
  a = 5  # adaptive restart
  g = 0
  global_best = pop[0]
  k = 0

  while g <= no_generations:
    for i in range(no_generations):
        offspring1 = crossover(pop, crossover_rate)
        offspring2 = mutation(pop, mutation_rate)
        fitness = objective_function(pop)
        offspring3 = local_search(pop, fitness, lower_bounds,upper_bounds, step_size, rate)
        step_size = step_size * 0.98
        if step_size < (upper_bounds[0]-lower_bounds[0]) * 0.001:
            step_size = (upper_bounds[0]-lower_bounds[0]) * 0.001
        extended_pop[0:pop_size] = pop
        extended_pop[pop_size:pop_size + crossover_rate] = offspring1
        extended_pop[pop_size + crossover_rate:pop_size + crossover_rate + mutation_rate] = offspring2
        extended_pop[
        pop_size + crossover_rate + mutation_rate:pop_size + crossover_rate + mutation_rate + 2 * no_variables * rate] = offspring3
        fitness = objective_function(extended_pop)
        pop = selection(extended_pop, fitness, pop_size)
        print("Generation: ", g, ",Current Fitness value: ", max(fitness))
        result +="\nGeneration: "+str(g)+",Current Fitness value: "+ str(max(fitness))
              #,extended_pop[np.where(fitness == max(fitness))])
        A.append(max(fitness))
        g += 1
        if i >= a:
            if sum(abs(np.diff(A[g - a:g]))) <= 0:
                index = np.argmax(fitness)
                current_best = extended_pop[index]
                pop = np.zeros((pop_size, no_variables))
                for s in range(pop_size - 1):
                    for h in range(no_variables):
                        pop[s, h] = np.random.uniform(lower_bounds[h],upper_bounds[h])
                pop[pop_size - 1:pop_size] = current_best
                step_size = (upper_bounds[0]-lower_bounds[0]) * 0.02
                global_best = np.vstack((global_best, current_best))
                break

        t1_stop = process_time()
        time_elapsed = t1_stop - t1_start
        if time_elapsed >= computing_time:
            break
    if time_elapsed >= computing_time:
        break

  fitness = objective_function(global_best)
  index = np.argmax(fitness)
  print("Best Solution = ", global_best[index])
  result +="\nBest Solution = "+str(global_best[index])
  print("\nBest Fitness Value = ", max(fitness))
  result +="\nBest Fitness Value = "+str(max(fitness))
  return render(request, 'index.html',{"r":result})
 else:
     return render(request, 'index.html',{"r":""})