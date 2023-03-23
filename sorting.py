from evo import Evo
import random as rnd
import pandas as pd
import numpy as np


sections = pd.read_csv("sections.csv")
prefs = pd.read_csv("tas.csv")
section_prefs = prefs.loc[:, '0':].values
allo_prefs = prefs["max_assigned"].values

def overallocation(test):
    """
    Gets the total number of over-allocated sections for all rows
    Param: test: numpy array, one solution
    Param: max_assigned: list, max assignments requested
    Return: int, total over-allocated sections in solution
    """

    overallocated_lst = [sum(lst) - max for lst, max in zip(test, allo_prefs) if
                         sum(lst) > max]

    return sum(overallocated_lst)


def conflicts(test):
    """
    """

    conflict_combs = np.where(test == 1, sections['daytime'].values, 0).tolist()

    conflict_list = [[_ for _ in lst if _ != 0] for lst in conflict_combs]
    conflict_set = [set([_ for _ in lst if _ != 0]) for lst in conflict_list]

    num_conflicts = [1 for c_lst, c_set in zip(conflict_list, conflict_set) if len(c_lst) != len(c_set)]

    return sum(num_conflicts)


def undersupport(test):
    undersupport_lst = [min - sum(lst) for lst, min in zip(test.T.tolist(), sections['min_ta'].values) if sum(lst) < min]

    return sum(undersupport_lst)


def unwilling(test):
    unwilling_lst = np.where((test == 1) & (section_prefs == 'U'), 1, 0).tolist()

    unwilling_count = [sum(lst) for lst in unwilling_lst]

    return sum(unwilling_count)


def unpreferred(test):
    willing_lst = np.where((test == 1) & (section_prefs == 'W'), 1, 0).tolist()

    willing_count = [sum(lst) for lst in willing_lst]

    return sum(willing_count)


def swapper(solutions):
    """ Swap two random rows """
    new = solutions[0]
    i = rnd.randrange(0, len(new))
    j = rnd.randrange(0, len(new))
    new[i], new[j] = new[j], new[i]
    return new


def transpose(solutions):
    new = solutions[0]
    return [list(a) for a in list[zip(*new)]]


def trade_rows(solutions):
    sol1 = solutions[0]
    sol2 = solutions[1]
    i = rnd.randrange(0, len(sol1))

    sol1[i] = sol2[i]
    return sol1



def main():
    preferences = pd.read_csv('sections_easy.csv')

    # Create framework
    E = Evo()

    # Register objectives
    E.add_fitness_criteria("overallocation", overallocation)
    E.add_fitness_criteria("conflicts", conflicts)
    E.add_fitness_criteria("undersupport", undersupport)
    E.add_fitness_criteria("unwilling", unwilling)
    E.add_fitness_criteria("unpreferred", unpreferred)

    # Register some agents
    E.add_agent("swapper", swapper, k=1)
    E.add_agent("transpose", transpose, k=1)
    E.add_agent("trader", trade_rows, k=2)

    # Seed the population with an initial random solution
    L = [[rnd.choice([0, 1]) for _ in range(42)] for _ in range(20)]
    E.add_solution(L)

    # Run the evolver
    E.evolve(100000000, 100, 100000)

    # Print final results
    print(E)


if __name__ == '__main__':
    main()
