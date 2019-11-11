import random
import numpy as np

class MyGA2:
    
    def __init__(self, popsize, generations, mutProb, radius):
        self.popsize = popsize # Could be needed for random population generation
        self.generations = generations # Amount of generations to go / a stoping criterion in this case.
        #self.data = data # Original data and current generation are intialized
        #self.currGeneration = data
        self.bestIndividual = None # TBD as a result of GA execution
        self.mutProb = mutProb
        self.radius = radius # The Specified radius that we want to reach with our RRR open-chain
        
        self.data = [] 
        for i in range(0, self.popsize):
            arm = []
            for part in range(0,3):
                arm.append(random.randint(1,31)) 
            self.data.append(arm) 
        self.currGeneration = self.data

    def crossover(self, parent_1, parent_2):
        # Define crossover "masks" - it is problem specific, depends on the string length.
        # For example, for 5 bits-long string, for "after 3rd bit" crossover position the masks will be 11100 (28 decimal) and 00011 (3 decimal)
        mask_head = 28
        mask_tail = 3
        child_1 = []
        child_2 = []
        # Making the crossover
        for i in range(0,3):
            child_1.append((parent_1[i] & mask_head) + (parent_2[i] & mask_tail)) # head of parent 1, tail of parent 2
            child_2.append((parent_2[i] & mask_head) + (parent_1[i] & mask_tail)) # head of parent 2, tail of parent 1
        return child_1, child_2
        
        
    def fitness(self, individual, currGeneration): #change this later to prob. specific
        # Calculate fitness score of the individual w.r.t. the current generation
        # Problem specific: .
        # Sum up all the functions
        ind_score = 1/(5*(individual[1] + individual[2] - self.radius)**2 + (self.radius - individual[0])**2 + 2*(individual[1] - individual[2])**2 + 0.01234)
        sum = 0
        for x in range(0, len(currGeneration)):
            sum += 1/(5*(currGeneration[x][1] + currGeneration[x][2] - self.radius)**2 + (self.radius - currGeneration[x][0])**2 + 2*(currGeneration[x][1] - currGeneration[x][2])**2 + 0.01234)
        return ind_score/sum
        
    def selection(self, currGeneration):    #selection as defined in lecture slides
        # Problem specific. In this case - 2 pairs, the fittest - in both pairs and then the two next best ones - for one time.
        # Get position of the fittest

        selprobs = []
        currprob = 0
        for individual in range(0,self.popsize):
            #creating the cumulative probability for selection of each individual
            currprob += self.fitness(currGeneration[individual], currGeneration)
            selprobs.append(currprob) 
        
        newpop = currGeneration.copy()
        for i in range(0,self.popsize):
            # generates a new population from selected individuals
            r = random.random()     #float from 0 to 1
            selected = 0
            while r > selprobs[selected]:
                selected +=1
            newpop[i] = currGeneration[selected]

        return newpop


    # Mutation function example
    def mutate(self, population):
        # There are popsize # of individuals in the population. Each consist of three 4-bits-long binary string
        probNoMutations = (1-self.mutProb)**(self.popsize*5*3) 
        #Check if at least one bit mutation happened
        check = random.random() # Returns a random number in [0, 1]
        if check > probNoMutations:
            #Mutation happened - just selecting 1 random bit [1..20]
            theIndividual = random.randrange(0, self.popsize, 1)
            part = random.randrange(0,3)
            theBit = random.randrange(0, 5, 1) 
            #Get individual from the population
            ind = population[theIndividual]
            indpart = ind[part]
            #must transform to binary with right amount of bits
            bin_ind = format(indpart, '#07b')   #the bin represented as a string on the form '0b*****'
            #access the right bit 
            digit = bin_ind[theBit +2]
            #represent the binary number as a list of characters 
            listbi = list(bin_ind)

            if digit == '0':
                #turn 0 to 1
                listbi[theBit +2] ='1'
            else: 
                #turn 1 to 0
                listbi[theBit +2] ='0'
            #transform to decimal
            bin_mut = ''.join(listbi)   #binary list to binary string
            mutpart = int(bin_mut[2:], 2)  #binary string to decimal
            mutated = ind
            mutated[part] = mutpart

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
            selection = self.selection(currGeneration)
            nextGeneration = selection.copy()
            # Make the crossover
            for i in range(0, (self.popsize)//4, 2):       # Croosover on half of the population
                child1, child2 = self.crossover(selection[i],selection[i+1]) # Taking two selected parents to generate two children (just one of the ways to do it).
                nextGeneration[i] = child1 # Appending children to the next generation variable.
                nextGeneration[i+1] = child2
            
            # Mutation check before next iteration
            self.mutate(nextGeneration)
            
            #print(nextGeneration) #see result for each generation
            #print('bestFitnessScore: ', max(fitnessResults), ' on index ', fitnessResults.index(max(fitnessResults)))
            print('best arm: ', nextGeneration[fitnessResults.index(max(fitnessResults))])
            # Clearing fitnessResults
            fitnessResults.clear()
        
        # By this time, after the loop execution, the best individual was set via the selection function inside the loops.
        return    


# Test the class
"""data = [] 
for i in range 20:
    data.append(random.randint(1,16))"""
myga = MyGA2(15, 15, 0.05, 27)
#print("Fitness test", myga.fitness(13, )) # See slide 30 - http://lobov.biz/academia/kbe/191023
#print("Crossover test", myga.crossover(13, 24)[0]) # See slides 33 and 34 - http://lobov.biz/academia/kbe/191023

# Some useful operations
print("data", myga.data)
#print("Random selection test", random.choice(myga.data)) 

myga.run()
#print("Best individual:", myga.bestIndividual)
