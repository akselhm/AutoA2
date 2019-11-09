import random
import numpy as np

class MyGA2:
    
    def __init__(self, popsize, generations, mutProb):
        self.popsize = popsize # Could be needed for random population generation
        self.generations = generations # Amount of generations to go / a stoping criterion in this case.
        #self.data = data # Original data and current generation are intialized
        #self.currGeneration = data
        self.bestIndividual = None # TBD as a result of GA execution
        self.mutProb = mutProb
        
        self.data = [] 
        for i in range(0, self.popsize-1):
            self.data.append(random.randint(1,16))
        self.currGeneration = self.data

    def crossover(self, parent_1, parent_2):
        # Define crossover "masks" - it is problem specific, depends on the string length.
        # For example, for 5 bits-long string, for "after 3rd bit" crossover position the masks will be 11100 (28 decimal) and 00011 (3 decimal)
        mask_head = 28
        mask_tail = 3
        # Making the crossover
        child_1 = (parent_1 & mask_head) + (parent_2 & mask_tail) # head of parent 1, tail of parent 2
        child_2 = (parent_2 & mask_head) + (parent_1 & mask_tail) # head of parent 2, tail of parent 1
        return child_1, child_2
        
        
    def fitness(self, individual, currGeneration):
        # Calculate fitness score of the individual w.r.t. the current generation
        # Problem specific - x*x.
        # Sum up all the functions
        sum = 0
        for x in currGeneration:
            sum += x*x
        return individual*individual/sum
    
    def selection(self, currGeneration, fitnessResults):
        # Problem specific. In this case - 2 pairs, the fittest - in both pairs and then the two next best ones - for one time.
        # Get position of the fittest

        selprobs = np.zeros(self.popsize)
        currprob = 0
        for individual in range(0,self.popsize-1):
            #creating the cumulative probability for selection of each individual
            currprob += self.fitness(individual, currGeneration)
            selprobs[individual] = currprob 
        
        newpop = currGeneration.copy()
        for i in range(0,self.popsize-1):
            # generates a new population from selected individuals
            r = random.random()     #float from 0 to 1
            selected = 0
            while r > selprobs[selected]:
                individual +=1
            newpop[i] = currGeneration[selected]

        return newpop


    # Mutation function example
    def mutate(self, population):
        # Problem specific.
        # There are 20 individuals in the population. Each is 4-bits-long binary string. So, in total, there are 800 bits.
        probNoMutations = (1-self.mutProb)**800 # Case specific '800'
        #Check if at least one bit mutation happened
        check = random.random() # Returns a random number in [0, 1]
        if check > probNoMutations:
            #Mutation happened - just selecting 1 random bit [1..20]
            theIndividual = random.randrange(0, len(self.data)-1, 1)
            theBit = random.randrange(0, 4, 1) #change 4 to 13 (5+4+4)
            #Get individual from the population
            ind = population[theIndividual]
            #must transform to binary with right amount of bits
            bin_ind = format(ind, '#06b')   #the bin represented as a string on the form '0b****'
            #access the right bit 
            digit = bin_ind[theBit +2]

            listbi = list(bin_ind)

            #change = bin(2^(len(self.data) - 1 - theBit)) # ether 1, 10, 100, 1000, ...
            if digit == 0:
                #turn 0 to 1
                listbi[theBit +2] ='1'
                bin_mut = ''.join(listbi)
            else: 
                #turn 1 to 0
                bin_mut = bin_ind - change
            #transform to decimal
            mutated = int(bin_mut[2:], 2)

            #check if mutated is better fitted
            fitNew = self.fitness(mutated, population)
            fitCurr = self.fitness(ind, population)
            if(fitNew > fitCurr):
                population[theIndividual] = mutated
				
        return
    
    def run(self):
        # Execute the algorithm - slide 10, http://lobov.biz/academia/kbe/191023
        nextGeneration = self.data # To populate as the next generation, in the beginning is set to data
        fitnessResults = [] #An empty array to store fitness results.
        #Iterating via the # of generations defined.
        for i in range(1, self.generations):
            currGeneration = nextGeneration.copy() # Important to copy to create a new instance of the array object
            nextGeneration.clear()
            # Fitness evaluation for the current generation
            for individual in currGeneration:
                fitnessResults.append(self.fitness(individual, currGeneration))
            
            # Select the fittest parents for crossover
            selection = self.selection(currGeneration, fitnessResults)
            
            # Make the crossover
            for pair in selection:
                child1, child2 = self.crossover(pair[0],pair[1]) # Taking two selected parents to generate two children (just one of the ways to do it).
                nextGeneration.append(child1) # Appending children to the next generation variable.
                nextGeneration.append(child1)
            
            # Mutation check before next iteration
            self.mutate(nextGeneration)
            
            
            # Clearing fitnessResults
            fitnessResults.clear()
        
        # By this time, after the loop execution, the best individual was set via the selection function inside the loops.
        return    


# Test the class
"""data = [] 
for i in range 20:
    data.append(random.randint(1,16))"""
myga = MyGA2(5, 5, 0.05)
#print("Fitness test", myga.fitness(13, )) # See slide 30 - http://lobov.biz/academia/kbe/191023
print("Crossover test", myga.crossover(13, 24)[0]) # See slides 33 and 34 - http://lobov.biz/academia/kbe/191023

# Some useful operations
print("data", myga.data)
print("Random selection test", random.choice(myga.data))
print("Max test", max(myga.data))
#print("Index of the element", myga.data.index(19))
#print("(1 - 0.05) in power 20", 0.95**20) 

myga.run()
print("Best individual:", myga.bestIndividual)
