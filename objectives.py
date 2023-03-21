import pandas as pd
import csv
import numpy as np
from evo import Evo


def overallocation(test, max_assigned):
    """
    Gets the total number of over-allocated sections for all rows
    Param: test: numpy array, one solution
    Param: max_assigned: list, max assignments requested
    Return: int, total over-allocated sections in solution
    """

    overallocated_lst = [sum(lst) - max for lst, max in zip(test.tolist(), max_assigned) if sum(lst) > max]

    return sum(overallocated_lst)


def conflicts(test, times):
    """

    """

    conflict_combs = np.where(test == 1, times, 0).tolist()

    conflict_list = [[_ for _ in lst if _ != 0] for lst in conflict_combs]
    conflict_set = [set([_ for _ in lst if _ != 0]) for lst in conflict_list]

    num_conflicts = [1 for c_lst, c_set in zip(conflict_list, conflict_set) if len(c_lst) != len(c_set)]

    return sum(num_conflicts)


def undersupport(test, minimum_support):

    undersupport_lst = [min - sum(lst) for lst, min in zip(test.T.tolist(), minimum_support) if sum(lst) < min]

    return sum(undersupport_lst)


def unwilling(test, prefs):

    unwilling_lst = np.where((test == 1) & (prefs == 'U'), 1, 0).tolist()

    unwilling_count = [sum(lst) for lst in unwilling_lst]

    return sum(unwilling_count)


def unpreferred(test, prefs):

    willing_lst = np.where((test == 1) & (prefs == 'W'), 1, 0).tolist()

    willing_count = [sum(lst) for lst in willing_lst]

    return sum(willing_count)


test1, test2, test3 = pd.read_csv('tests/test1.csv', header=None).to_numpy(), \
                      pd.read_csv('tests/test2.csv', header=None).to_numpy(), pd.read_csv('tests/test3.csv', header=None).to_numpy()

ta = pd.read_csv('tas.csv')

sections = pd.read_csv('sections.csv')

max_assign = ta['max_assigned'].values

conflict_times = sections['daytime'].to_numpy()

min_support = sections['min_ta'].values

preferences = ta.loc[:, '0':].values

obj_df = pd.DataFrame([['Overallocation'], ['Conflicts'], ['Undersupport'], ['Unwilling'], ['Unpreferred']],
                      columns=['Objectives'])

for idx, test in enumerate([test1, test2, test3]):
    obj_df['Test' + str(idx + 1)] = [overallocation(test, max_assign), conflicts(test, conflict_times),
                                 undersupport(test, min_support), unwilling(test, preferences),
                                 unpreferred(test, preferences)]

print(obj_df)
