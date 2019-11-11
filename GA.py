import random
import numpy as np

class MyGA:
    
    def __init__(self, popsize, generations, mutProb, radius):
        self.popsize = popsize # Needed for random population generation
        self.generations = generations # Amount of generations to go / a stoping criterion in this case.
        self.mutProb = mutProb
        self.radius = radius # The Specified radius that we want to reach with our RRR open-chain
        
        self.data = [] # random generized list of data. Each element in the list consist of a list with three integers: [r0, r1, r2]
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
        # Problem specific. For a 3-links RRR open chain represented as [r0, r1, r2] in a sphere with radius R we want:
        # 1. To minimize (R - r0)^2 and (r1 + r2 - R)^2. We want to reach the whole radius, and without diging in the ground
        # 2. To minimize (r1 - r2)^2. We want to reach to the inner points of the sphere, so r1 must be close to r2
        # Sum up all the functions
        ind_score = 1/(5*(individual[1] + individual[2] - self.radius)**2 + 2*(self.radius - individual[0])**2 + 2*(individual[1] - individual[2])**2 + 0.2)
        sum = 0
        for x in range(0, len(currGeneration)):
            sum += 1/(5*(currGeneration[x][1] + currGeneration[x][2] - self.radius)**2 + 2*(self.radius - currGeneration[x][0])**2 + 2*(currGeneration[x][1] - currGeneration[x][2])**2 + 0.2)
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
        while check > probNoMutations:
            check = check - probNoMutations
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
            #transform back to decimal
            bin_mut = ''.join(listbi)   #binary list to binary string
            mutpart = int(bin_mut[2:], 2)  #binary string to decimal
            mutated = ind
            #add mutated part to mutated arm
            mutated[part] = mutpart

            #check if mutated arm is better fitted
            fitNew = self.fitness(mutated, population)
            fitCurr = self.fitness(ind, population)
            if(fitNew > fitCurr):
                population[theIndividual] = mutated
				
        return
    
    def run(self):
        # Execute the algorithm
        nextGeneration = self.data # To populate as the next generation, in the beginning is set to data
        #Iterating via the # of generations defined.
        for i in range(1, self.generations):
            currGeneration = nextGeneration.copy() # Important to copy to create a new instance of the array object
            nextGeneration.clear()
            
            # Select the fittest parents for crossover
            selection = self.selection(currGeneration)
            nextGeneration = selection.copy()
            # Make the crossover
            for i in range(0, (self.popsize)//6, 2):       # Crossover on one third of the population
                child1, child2 = self.crossover(selection[i],selection[i+1]) # Taking two selected parents to generate two children (just one of the ways to do it).
                nextGeneration[i]     = child1 # Appending children to the next generation variable.
                nextGeneration[i + 1] = child2
            
            # Mutation check before next iteration
            self.mutate(nextGeneration)
        
        #return the best individual from the last 
        fitnessResults = [] #An empty array to store fitness results.
        for individual in nextGeneration:
            fitnessResults.append(self.fitness(individual, nextGeneration))
        print('final generation: ', nextGeneration)
        print('best arm: ', nextGeneration[fitnessResults.index(max(fitnessResults))])
        return nextGeneration[fitnessResults.index(max(fitnessResults))] 


# Test the class
myga = MyGA(15, 30, 0.01, 17)

# Some useful operations
print("data", myga.data)

myga.run()
#print("Best individual:", myga.bestIndividual)

