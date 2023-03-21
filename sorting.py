from evo import Evo
import random as rnd
import pandas as pd
import numpy as np


class TAObjectives:

    def __init__(self):
        self.criteria = {}

    def overallocation(self, test):
        """
        Gets the total number of over-allocated sections for all rows
        Param: test: numpy array, one solution
        Param: max_assigned: list, max assignments requested
        Return: int, total over-allocated sections in solution
        """

        overallocated_lst = [sum(lst) - max for lst, max in zip(test.tolist(), self.criteria['max_assigned']) if
                             sum(lst) > max]

        return sum(overallocated_lst)

    def conflicts(self, test, times):
        """

        """

        conflict_combs = np.where(test == 1, times, 0).tolist()

        conflict_list = [[_ for _ in lst if _ != 0] for lst in conflict_combs]
        conflict_set = [set([_ for _ in lst if _ != 0]) for lst in conflict_list]

        num_conflicts = [1 for c_lst, c_set in zip(conflict_list, conflict_set) if len(c_lst) != len(c_set)]

        return sum(num_conflicts)

    def undersupport(self, test, minimum_support):
        undersupport_lst = [min - sum(lst) for lst, min in zip(test.T.tolist(), minimum_support) if sum(lst) < min]

        return sum(undersupport_lst)

    def unwilling(self, test, prefs):
        unwilling_lst = np.where((test == 1) & (prefs == 'U'), 1, 0).tolist()

        unwilling_count = [sum(lst) for lst in unwilling_lst]

        return sum(unwilling_count)

    def unpreferred(self, test, prefs):
        willing_lst = np.where((test == 1) & (prefs == 'W'), 1, 0).tolist()

        willing_count = [sum(lst) for lst in willing_lst]

        return sum(willing_count)

def swapper(solutions):
    """ Swap two random values """
    L = solutions[0]
    i = rnd.randrange(0, len(L))
    j = rnd.randrange(0, len(L))
    L[i], L[j] = L[j], L[i]
    return L

def main():
    preferences = pd.read_csv('sections_easy.csv')

    # Create framework
    E = Evo()

    # register ta criteria
    E.add_criteria('max_assigned', preferences['max_ta'].tolist())

    # Register objectives
    E.add_fitness_criteria("overallocation", overallocation)
    E.add_fitness_criteria("conflicts", conflicts)
    E.add_fitness_criteria("undersupport", undersupport)
    E.add_fitness_criteria("unwilling", unwilling)
    E.add_fitness_criteria("unpreferred", unpreferred)

    # Register some agents
    E.add_agent("swapper", swapper, k=1)

    # Seed the population with an initial random solution
    N = 50
    L = [rnd.randrange(1,99) for _ in range(N)]
    E.add_solution(L)
    print(E)

    # Run the evolver
    E.evolve(100000000, 100, 100000)

    # Print final results
    print(E)


if __name__ == '__main__':
    main()
