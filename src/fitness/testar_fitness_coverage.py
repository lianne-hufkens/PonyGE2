from fitness.base_ff_classes.base_ff import base_ff

from algorithm.parameters import params
import random, os, subprocess, csv, re
from . import testar

#https://stackoverflow.com/questions/431684/equivalent-of-shell-cd-command-to-change-the-working-directory
class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


class testar_fitness_coverage(base_ff):
    """
    Basic fitness function template for writing new fitness functions. This
    basic template inherits from the base fitness function class, which
    contains various checks and balances.
    
    Note that all fitness functions must be implemented as a class.
    
    Note that the class name must be the same as the file name.
    
    Important points to note about base fitness function class from which
    this template inherits:
    
      - Default Fitness values (can be referenced as "self.default_fitness")
        are set to NaN in the base class. While this can be over-written,
        PonyGE2 works best when it can filter solutions by NaN values.
    
      - The standard fitness objective of the base fitness function class is
        to minimise fitness. If the objective is to maximise fitness,
        this can be over-written by setting the flag "maximise = True".
    
    """

    # The base fitness function class is set up to minimise fitness.
    # However, if you wish to maximise fitness values, you only need to
    # change the "maximise" attribute here to True rather than False.
    # Note that if fitness is being minimised, it is not necessary to
    # re-define/overwrite the maximise attribute here, as it already exists
    # in the base fitness function class.
    maximise = True

    def __init__(self):
        """
        All fitness functions which inherit from the bass fitness function
        class must initialise the base class during their own initialisation.
        """

        # Initialise base fitness function class.
        super().__init__()

    def evaluate(self, ind, **kwargs):
        """
        Default fitness execution call for all fitness functions. When
        implementing a new fitness function, this is where code should be added
        to evaluate target phenotypes.
        
        There is no need to implement a __call__() method for new fitness
        functions which inherit from the base class; the "evaluate()" function
        provided here allows for this. Implementing a __call__() method for new
        fitness functions will over-write the __call__() method in the base
        class, removing much of the functionality and use of the base class.
                
        :param ind: An individual to be evaluated.
        :param kwargs: Optional extra arguments.
        :return: The fitness of the evaluated individual.
        """


        testar.call_testar(ind)
        
        # path r'C:\Users\testar\Desktop\TESTAR_dev\testar\output'
        path = r'C:\Users\testar\Desktop\TESTAR_dev\testar\target\install\testar\bin\output'
        if os.path.isdir(path):
            if "webformsut" in params['SUT']:
                with cd(path):
                    with open('_.csv') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=';')
                        for row in reader:                
                            fitness = abs((int(row['actions executed']) / int(row['number of fields'])) * int(row['successful submit'] == 'yes') - 1)
                            return fitness

                    return fitness
                except FileNotFoundError: #if file not found, default to standard fitness
                    return base_ff.default_fitness
