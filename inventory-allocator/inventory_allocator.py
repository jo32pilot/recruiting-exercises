# priorities
# 1. shipped by least number of warehouses
# 2. shipped by earliest warehouse
#
# doesn't matter if we have too much
#
# copy = order copy
# for each warehouse in list
#   for every item in order
#       if item in warehouse
#
# order 7 (optimal solution = 1 + 6, careful of 4 + 6 and 1 + 4 + 2)
# [1, 4, 2, 6, 5, 1, 3]
#
# only look at the direct previous solution
#
# (this sol doesn't take into account that there are some warehouses with none
# of the stock we're looking for)
#
# list_ind = 0
# dp[1] = 0
# for i = 2 ... order + 1: # assuming exclusive upper bound
#     if wh[list_ind] >= i:
#         dp[i] = list_ind
#         continue
#     else:
#         list_ind += 1
#
#     if wh[list_ind] >= i:
#         dp[i] = list_ind
#     else:
#         dp[i] = dp[i - 1].append(list_ind)
#
# order 1: solution = 0
# order 2: solution = 1
# order 3: solution = 1
# order 4: solution = 1
# order 5: solution = dp[4] + dp[5 - 4] (list combine)
# order 6: solution = dp
#
#
# order 7
# [1]: (-1, 1)
# [1, 4]: (-1, 5)
# [1, 4, 2]: ((0, 1, 2), 7)
# [1, 4, 2, 6]: 
#
# how about this: we have and n * m solution where n is the order number and m
# is the number of warehouses
#
# for i to n, go through list, compute solution for i
#
# order 1: solution = 0
# order 2: solution = 1
# order 3: solution = 1
# order 4: solution = 1
# order 5: solution = 4
# order 6: solution = 4
# order 7: solution = dp[6], dp[1]
# order 8: solution = (dp[7]: dp[6], dp[1]) , d
#

def backtrack(order, tot, idx, ind, solutions, wh):

    if idx >= len(wh):
        return

    if wh[idx] != 0:
        tot = tot + wh[idx]
        ind.append(idx)

        if tot >= order:
            solutions.append(list(ind))
            del ind[-1]
            return

    for i in range(idx + 1, len(wh)):
        backtrack(order, tot, i, ind, solutions, wh)
   
    if wh[idx] != 0:
        del ind[-1]

def combine_sets(item_idx, curr_set, item_solutions, final_solutions):
    
    if item_idx == len(item_solutions):
        final_solutions.append(curr_set)
        return

    for item_sol in item_solutions[item_idx]:
        combined = curr_set | set(item_sol)
        combine_sets(item_idx + 1, combined, item_solutions, final_solutions)
        

def allocate(order, warehouses):
    item_solutions = []
    for item, count in order.items():
        item_inventory = [wh['inventory'].get(item, 0) for wh in warehouses]
        item_sol = []
        backtrack(count, 0, 0, [], item_sol, item_inventory)
        item_solutions.append(list(item_sol))

    final_solutions = []
    combine_sets(0, set(), item_solutions, final_solutions)
    solution_ind = final_solutions[0] if final_solutions else None
    for sol in final_solutions:
        solution_ind = sol if len(sol) < len(solution_ind) else solution_ind

    return list(map(lambda i: warehouses[i], solution_ind)) if solution_ind \
            else []

# [1, 4, 2, 6, 5, 1, 3]
order = {
    'apple': 7,
    'orange': 1,
    'banana': 4
}

warehouses = [ 
    { 
        'name': 'owd', 
        'inventory': { 
            'apple': 1, 
            'orange': 1, 
        } 
    }, 
    { 
        'name': 'dm', 
        'inventory': { 
            'banana': 2, 
            'orange': 2,
        } 
    },
    {
        'name': 'wh',
        'inventory':{
            'apple':4,
            'orange': 3
            
        }
    },
    {
        'name': 'wh',
        'inventory':{
            'apple':2

            
        }
    },
    {
        'name': 'wh',
        'inventory':{
            'apple': 6,
            'banana': 4
            
        }
    },
    {
        'name': 'wh',
        'inventory':{
            'apple': 5
            
        }
    },
    {
        'name': 'wh',
        'inventory':{
            'apple': 1
            
        }
    },
    {
        'name': 'wh',
        'inventory':{
            'apple': 3
            
        }
    },
]

print(allocate(order, warehouses))
