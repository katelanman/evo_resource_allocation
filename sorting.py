from evo import Evo
import random as rnd
import pandas as pd
import numpy as np
import time

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
    conflict_combs = np.where(test == 1, sections['daytime'].to_numpy(), 0)

    conflict_list = [[_ for _ in lst if _ != 0] for lst in conflict_combs]
    conflict_set = [set([_ for _ in lst if _ != 0]) for lst in conflict_list]

    num_conflicts = [1 for c_lst, c_set in zip(conflict_list, conflict_set) if len(c_lst) != len(c_set)]

    return sum(num_conflicts)


def undersupport(test):
    undersupport_lst = [min - sum(lst) for lst, min in zip(test.T.tolist(), sections['min_ta'].values) if
                        sum(lst) < min]

    return sum(undersupport_lst)


def unwilling(test):
    unwilling_lst = np.where((test == 1) & (section_prefs == 'U'), 1, 0)

    unwilling_count = [sum(lst) for lst in unwilling_lst]

    return sum(unwilling_count)


def unpreferred(test):
    willing_lst = np.where((test == 1) & (section_prefs == 'W'), 1, 0)

    willing_count = [sum(lst) for lst in willing_lst]

    return sum(willing_count)


def swapper(solutions):
    """ Swap two random rows """
    new = solutions[0]
    i = rnd.randrange(0, len(new))
    j = rnd.randrange(0, len(new))
    new[i], new[j] = new[j], new[i]
    return new


def reallocate(solutions):
    new = solutions[0]

    # list of position in sol of each ta who is overallocated
    over = [i for ta, max, i in zip(new, allo_prefs, range(len(new))) if sum(ta) > max]

    # if no tas overallocated
    if not over:
        return new

    # choose random overallocated ta
    ta = rnd.choice(over)

    while True:
        i = rnd.randrange(0, len(new[ta]))

        # if section assigned, unassign
        if new[ta][i] == 1:
            new[ta][i] = 0
            return new


def trade_rows(solutions):
    sol1 = solutions[0]
    sol2 = solutions[1]
    i = rnd.randrange(0, len(sol1))

    sol1[i] = sol2[i]
    return sol1


def zero_unwill(solutions):
    new = solutions[0]

    unwilling = np.where((new == 1) & (section_prefs == 'U'), 1, 0)
    willing = np.where((new == 0) & (section_prefs != 'U'), 1, 0)

    tas_unwilling = [i for assigned, i in zip(unwilling, range(len(unwilling))) if 1 in assigned]

    if not tas_unwilling:
        return new

    # choose random unwilling ta
    ta = rnd.choice(tas_unwilling)
    unassign = rnd.choice([_ for _ in unwilling[ta] if ])


    new[ta] = [0 if unwilling_lst[ta][i] == 1 else new[ta][i] for i in range(len(new[ta]))]

    # take unwilling assignment and move to unpreferred section

    return new


def min_under(solutions):
    new = solutions[0]

    under = [i for ta, min, i in zip(new, sections['min_ta'].values, range(len(new))) if sum(ta) < min]

    if not under:
        return new

    # choose random overallocated ta
    ta = rnd.choice(under)

    while True:
        i = rnd.randrange(0, len(new[ta]))

        # if section unassigned, assign
        if new[ta][i] == 0:
            new[ta][i] = 1
            return new


def change_assigned(solutions):
    new = solutions[0]
    i = rnd.randrange(0, len(new))
    j = rnd.randrange(0, len(new[0]))

    new[i][j] = (new[i][j] + 1) % 2
    return new


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
    E.add_agent("trader", trade_rows, k=2)
    E.add_agent("eliminate_unwilling", zero_unwill, k=1)
    E.add_agent("reallocate", reallocate, k=1)
    E.add_agent("change_assigned", change_assigned)
    E.add_agent("min_under", min_under)

    # Seed the population with an initial random solution
    L = np.array([[rnd.choice([0, 0, 0, 0, 0, 1]) for _ in range(17)] for _ in range(43)])
    E.add_solution(L)
    print(E)


    # Run the evolver
    E.evolve(100000, 100, 100, 120)

    # Print final results
    print(E)


if __name__ == '__main__':
    main()
