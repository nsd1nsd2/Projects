"""
Name: Roshan Peri/Freddy Elyas
File: alife.py
Description: Simulating an ecosystem with rabbits and foxes
"""

import random as rnd
import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
<<<<<<< HEAD
from matplotlib.colors import ListedColormap
=======
from matplotlib.colors import ListedColormap #ChatGPT code 
>>>>>>> fdae524a557c1d416830c241efdaf279eba4441e

CUSTOM_COLORS = ['black', 'green', 'white', 'red'] 
CUSTOM_CMAP = ListedColormap(CUSTOM_COLORS)
ARRSIZE = 200   # The dimensions of the field
FIGSIZE = 8     # The size of the animation (inches)
INIT_RABBITS = 30000 # Initial # of rabbits
INIT_FOXES = 10000 # Initial # of foxes 
GRASS_RATE = 0.15  # Probability that grass grows back at any given location
OFFSPRING = 2  # Maximum number of offspring



class Animal:
    """
    Creating the animal class to simulate both the foxes and the rabbits 
    """
    def __init__(self, species = 'rabbit', max_offspring=1, starvation_level=1, reproduction_level=1):
        """ Constructor """
        self.x = rnd.randrange(0, ARRSIZE)
        self.y = rnd.randrange(0, ARRSIZE)
        self.eaten = 0  # how much grass the rabbit has consumed
        
        self.species = species
        self.max_offspring = max_offspring
        self.starvation_level = starvation_level
        self.reproduction_level = reproduction_level

        self.hunger = 0
        self.alive = True

    def move(self):
        """ Moving up, down, left, right randomly
        In this world the field wraps around """
        self.x = (self.x + rnd.choice([-1, 0, 1])) % ARRSIZE
        self.y = (self.y + rnd.choice([-1, 0, 1])) % ARRSIZE

    def eat(self, amount):
        """
        How the animals eat
        """
        self.eaten += amount

    def reproduce(self):
        """
        How the animals reproduce 
        """
        self.eaten = 0
        return copy.deepcopy(self)


class Field:
    """ 
    Creating the field where the animals will interact with 
    """

    def __init__(self):
        self.animals = []   # a list of rabbit objects
        self.field = np.ones(shape=(ARRSIZE, ARRSIZE), dtype=int)
        self.rabbit_hist =[]
        self.fox_hist = []
        self.generation_count = 0 
    def add_animal(self, animal):
        """ A new rabbit is added to the field """
        self.animals.append(animal)

    def move(self):
        """ All the rabbits move! """
        for animal in self.animals:
            animal.move()

    def eat(self):
        """ Rabbits eat grass (if they find grass where they are) """
        rabbit_position = {

        }

        for animal in self.animals:
            if animal.species == 'rabbit' and animal.alive:
                animal.eat(self.field[animal.x, animal.y])
                self.field[animal.x, animal.y] = 0
                pos = (animal.x,animal.y)
                if pos not in rabbit_position:
                    rabbit_position[pos] = []
                rabbit_position[pos].append(animal)
        for animal in self.animals:
            if animal.species == 'fox' and animal.alive:
                pos = (animal.x,animal.y)
                if pos in rabbit_position and rabbit_position[pos]:
                    prey = rabbit_position[pos].pop()
                    prey.alive = False
                    animal.eat(1)



    def survive(self):
        """ Animals survive based on their hunger level """
        for animal in self.animals:
            if animal.eaten == 0:
                animal.hunger += 1
            else:
                animal.hunger = 0

            if animal.hunger >= animal.starvation_level:
                animal.alive = False
        self.animals = [animal for animal in self.animals if animal.alive]
        

    def grow(self):
        """ Grass grows back with some probability at each location """
        growloc = (np.random.rand(ARRSIZE, ARRSIZE) < GRASS_RATE) * 1
        self.field = np.maximum(self.field, growloc)

    def reproduce(self):
        """ Rabbits reproduce like rabbits """

        born = []
        for animal in self.animals:
            if animal.eaten >= animal.reproduction_level:
                for _ in range(rnd.randint(0, animal.max_offspring)):
                    born.append(animal.reproduce())
                animal.eaten = 0
        self.animals += born   # append the new rabbits to the field!


    def update_pop(self):
        """ Update population tracking """
        rabbit_count = sum(1 for animal in self.animals if animal.alive and animal.species == 'rabbit') #ChatGPT code
        fox_count = sum(1 for animal in self.animals if animal.alive and animal.species == 'fox' )
        self.fox_hist.append(fox_count)
        self.rabbit_hist.append(rabbit_count)
        self.generation_count += 1
            


    def generation(self):
        """ One generation of rabbits """
        self.move()
        self.eat()
        self.survive()
        self.reproduce()
        self.grow()
        self.update_pop()



    def field_display(self):
        """
        Creating the actual display of the field 
        """
        display = self.field.copy()
        for animal in self.animals:
            if animal.alive and animal.species == 'rabbit':
                display[animal.x,animal.y] = 2
        for animal in self.animals:
            if animal.alive and animal.species == 'fox':
                display[animal.x,animal.y] = 3 #ChatGPT code
        return display
    
    
    
    def pop_counts(self):
        """
        Counting the number of animals in each generation 
        """
        rabbit_num = sum(1 for a in self.animals if a.alive and a.species == 'rabbit') #ChatGPT code
        fox_num = sum(1 for a in self.animals if a.alive and a.species == 'fox')
        return rabbit_num, fox_num
    
    
    def plot_gen(self):
        """
        Creating the time series plot of the number of animals per generation 
        """
        generations = list(range(len(self.rabbit_hist)))
        plt.figure(figsize=(12,6))
        plt.plot(generations,self.rabbit_hist,'b-',label='Rabbits')
        plt.plot(generations,self.fox_hist,'r-',label='Foxes') 
        plt.xlabel('Generation')
        plt.ylabel('Population')
        plt.title('Predator-Prey Population Dynamics Over Time')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()




def animate(i, field, im):
    """
    Creating the animation function 
    """
    field.generation()
    im.set_array(field.field_display())   
    rabbit_count, fox_count = field.pop_counts()
    plt.title(f"Generation: {i}  Rabbits: {rabbit_count}  Foxes: {fox_count}")
    return im,


def main():

    # Create the field object (ecosystem)
    field = Field()

    # Add some rabbits at random locations
    for _ in range(INIT_RABBITS):
        field.add_animal(Animal(species= 'rabbit', starvation_level=2, reproduction_level=1, max_offspring=1))
    for _ in range(INIT_FOXES):
        field.add_animal(Animal(species='fox', starvation_level=8, reproduction_level=2, max_offspring=1))
    # Set up the animation with FuncAnimation
    fig = plt.figure(figsize=(FIGSIZE, FIGSIZE))
<<<<<<< HEAD

    # for the specific colors requested in the assignment
    colors = ['black', 'green', 'white', 'red']
    custom_cmap = ListedColormap(colors)

    im = plt.imshow(field.field_display(), cmap=custom_cmap, interpolation='nearest', vmin=0, vmax=3)
    # im = plt.imshow(field.field_display(), cmap='viridis', interpolation='nearest', vmin=0, vmax=3)
=======
    im = plt.imshow(field.field_display(), cmap=CUSTOM_CMAP, interpolation='nearest', vmin=0, vmax=3)
>>>>>>> fdae524a557c1d416830c241efdaf279eba4441e
    anim = animation.FuncAnimation(fig, animate, fargs=(field, im), frames=5000, interval=1)
    plt.show()
    field.plot_gen()

if __name__ == '__main__':
    main()