"""File containing the inventory allocater function, allocate()."""

def _backtrack(order, tot, idx, ind, solutions, wh):
    """Backtracking helper function that gathers possible shipments.

    This function takes in the amount of an item ordered and a list of stock of
    the item for every warehouse, and recursively gathers all possible subsets
    of indices from the list of stock such that the sum of the elements at those
    indices are at least the ordered amount, the that last index
    added is that of the element that made the total at least the ordered
    amount, and the indices are in increasing order.

    Example: Let's say we ordered 2 apples and had 3 warehouses whose apple
             stock were [1, 1, 2]

             Then the returned list of indices would be [[0, 1], [1, 2], [2]].
             [0, 2] is not included because while collecting [0, 1], we
             found that the elements at the indices [0, 1] sum to the ordered
             amount, Therefore we do not need to consider any other cases
             [0, i], as [0, 1] comes earlier than other indices.

    Args:
        order (int): The amount ordered for a particular item.
        tot (int): The current sum across the current subset of indices.
        idx (int): The current index in the passed in list of stock to start
                   considering to add to our current subset.
        ind (list): The current subset of indices.
        solutions (list): The list of subsets.
        wh (list): The list of stock of the item for every warehouse.
    """

    # Don't go out of bound.
    if idx >= len(wh):
        return

    for i in range(idx, len(wh)):

        # Don't consider any warehouses that don't have the item in stock.
        if wh[i] != 0:

            # Add the current warehouse's stock and update indices list.
            new_tot = tot + wh[i]
            ind.append(i)

            # If we've reached the order amount.
            if new_tot >= order:

                # Add this subset.
                solutions.append(list(ind))
                del ind[-1]

                # Don't need to consider any other indices at this level of
                # recursion. The current index comes earlier than the following
                # and therefore is more optimal.
                return

            _backtrack(order, new_tot, i + 1, ind, solutions, wh)

            # Remove the recently added index so we can try a subset
            # starting with the next index instead.
            del ind[-1]
   
def _combine_sets(item_idx, curr_set, item_solutions, final_solutions):
    """Recursively generates all possible combinations of the passed in sets.

    This function takes in a list of lists of sets. Each set in each list
    of sets will be unioned with another set from every other list of sets.

    Example: Given the following list:
             [
                [{1, 2}, {3, 4}],
                [{2, 3}, {4, 5}],
                [{3, 4}, {5, 6}]
             ]

             The function will generate the following list:
             [
                {1, 2, 3, 4},       # {1, 2} | {2, 3} | {3, 4}
                {1, 2, 3, 5, 6},    # {1, 2} | {2, 3} | {5, 6}
                {1, 2, 3, 4, 5},    # {1, 2} | {4, 5} | {3, 4}
                {1, 2, 4, 5, 6},    # {1, 2} | {4, 5} | {5, 6}
                {2, 3, 4},          # {3, 4} | {2, 3} | {3, 4}
                {2, 3, 4, 5, 6},    # {3, 4} | {2, 3} | {5, 6}
                {3, 4, 5},          # {3, 4} | {4, 5} | {3, 4}
                {3, 4, 5, 6}        # {3, 4} | {4, 5} | {5, 6}
            ]

    Args:
        item_idx (int): The index of our current list of sets we are taking a
                        set from and unioning to our current result set.
        curr_set (set): Our current result set.
        item_solutions (list): Our list of unioned sets.
        final_solutions (list): Our list of lists of sets to union.
    """

    # If we've recursed pass the last list of sets, then add the current result
    # to our results list.
    if item_idx == len(item_solutions):
        final_solutions.append(curr_set)
        return

    for item_sol in item_solutions[item_idx]:
        combined = curr_set | set(item_sol)
        _combine_sets(item_idx + 1, combined, item_solutions, final_solutions)
        

def allocate(order, warehouses):
    """Computes the optimal list of warehouses to ship an order.

    The optimal shipment is the cheapest shipment. A shipment is cheap
    if:
        1. The fewest number of warehouses are used.
        2. The closest warehouses are used.

    The passed in list of warehouses is sorted from closest to farthest.

    Args:
        order (dict): Mapping of items ordered to the amount ordered.
        warehouses (list): List of warehouses represented by dictionaries
                           containing the name of the warehouse and their
                           inventory.
    """

    # First compute the possible shipments for each individual item in
    # the order.
    item_solutions = []
    for item, count in order.items():

        # For the current item, gather the stock of the item in every warehouse.
        item_inventory = [wh['inventory'].get(item, 0) for wh in warehouses]
        item_sol = []

        # Compute the possible shipments for the current item.
        _backtrack(count, 0, 0, [], item_sol, item_inventory)
        item_solutions.append(list(item_sol))

    # Second, generate all possible shipments by combining
    # possible individual item solutions created from the previous step.
    final_solutions = []
    _combine_sets(0, set(), item_solutions, final_solutions)

    # Third, among the possible shipments, find that which uses the least
    # number of warehouses, and comes earliest in the list of shipments.
    solution_ind = final_solutions[0] if final_solutions else None
    for sol in final_solutions:
        solution_ind = sol if len(sol) < len(solution_ind) else solution_ind

    # What we have is a list of indices of warehouses. Here we get a list
    # of the warehouses themselves.
    res = list(map(lambda i: warehouses[i], solution_ind)) if solution_ind \
            else []

    # Finally, compute the number of items to be delivered from each warehouse.
    for warehouse in res:
        for item in order.keys():
            wh_stock = warehouse['inventory'].get(item, -1)

            # If we've already fulfilled our order for the current item,
            # we don't need to deliver any of the current item from this
            # warehouse.
            if order[item] == 0 and wh_stock >= 0:
                del warehouse['inventory'][item]

            # If this warehouse fulfills our order for the current item...
            elif wh_stock >= order[item]:

                # Assign this warehouse to deliver the remaining amount needed
                # of the current item.
                warehouse['inventory'][item] = order[item]
                order[item] = 0

            # Otherwise, we need more of the current item.
            # If this warehouse contains stock for our current item...
            elif wh_stock > 0:
                order[item] -= wh_stock
    return res
