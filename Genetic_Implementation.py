

"""
    IN THIS FILE ARE INCLUDED ALL THE METHODS NEEDED FOR SOLVING THE TRAVELING SALESMAN PROBLEM AND THE
    VEHICLE ROUTING PROBLEM. A GENETIC ALGORITHM WILL BE USE TO SOLVE THESE PROBLEMS.
"""

import random


def partially_mapped_crossover(p1, p2):
    start = random.randint(0, len(p1) - 2)
    finish = random.randint(start + 1, len(p1) - 1)
    list_copy = p2[:start] + p1[start:finish] + p2[finish:len(p2)]  # We get a random slice of P1
    print 'List copy: ', list_copy
    print 'Corte: ', p1[start:finish]

    aux = list()

    for x1 in p2[start:finish]:
        if x1 not in list_copy:
            aux.append(x1)

    i = 0
    for x1 in p1[start:finish]:
        if x1 not in p2[start:finish]:
            list_copy[p2.index(x1)] = aux[i]
            i += 1

    return list_copy, p2


def create_table(p1, p2):
    dict = {}

    for x in p1:
        dict[str(x)] = list_create(x, p1, p2)

    return dict


def list_create(x, p1, p2):
    aux = []
    index1 = p1.index(x)
    index2 = p2.index(x)
    length = len(p1)

    if index1 == 0:
        aux.append(str(p1[index1 - 1]))
        aux.append(str(p1[1]))
    elif index1 == length - 1:
        aux.append(str(p1[0]))
        aux.append(str(p1[index1 - 1]))

    else:
        aux.append(str(p1[index1 - 1]))
        aux.append(str(p1[index1 + 1]))

    if index2 == 0:
        aux.append(str(p2[index2 - 1]))
        aux.append(str(p2[1]))
    elif index2 == length - 1:
        aux.append(str(p2[0]))
        aux.append(str(p2[index2 - 1]))
    else:
        aux.append(str(p2[index2 - 1]))
        aux.append(str(p2[index2 + 1]))

    count = 0
    for x in aux:
        for x2 in aux:
            if x == x2:
                count += 1
            if count == 2:
                aux.remove(x)
                aux.remove(x2)
                aux.append(str(x) + '+')
                break

        count = 0

    return aux


def edge_recombination(dict):
    candidates = dict.keys()  # Candidates to pick
    aux = list()  # list we should return
    l = list()  # list that we are checking
    isFirst = True
    element = None

    while candidates:

        if isFirst:
            number = random.randint(0, len(candidates) - 1)
            element = candidates[number]
            isFirst = False

        else:

            if contains_plus(l):
                #print 'contains plus'
                element = get_plus(l)

            elif not list:
                #print 'empty list'
                number = random.randint(0, len(candidates) - 1)
                element = candidates[number]

            elif are_equal(dict, l):
                #print 'equal'
                number = random.randint(0, len(candidates) - 1)
                element = candidates[number]

            else:
                #print 'choose shorter'
                element = choose_shorter(dict, l)

            #print 'candidates: ', candidates
            #print 'element: ', element
            #print 'list: ', l
            #print 'dictionary: ', dict

            aux.append(element)
            candidates.remove(element)
            l = dict[element]
            dict = remove_dict(dict, element)

    i = 0
    for x in aux:
        aux[i] = int(x)
        i += 1

    return aux


def choose_shorter(dict, l):
    element = None
    previous = None

    for x1 in l:
        previous = len(dict[x1])

        if len(dict[x1]) <= previous:
            element = x1

    return element


def remove_dict(dict, number):
    """Update the table"""

    dict.pop(number)

    for x in dict.values():
        if number in x:
            x.remove(number)

        if (number + '+') in x:
            x.remove(number + '+')

    return dict


def are_equal(dict, l):
    """  Look for a tie """

    state = True
    isFirst = True

    for x1 in l:
        if isFirst:
            previous = len(dict[x1])
            isFirst = False

        elif len(dict[x1]) != previous:
            state = False

    return state


def contains_plus(l):
    """   Look for + """

    state = False

    for s in l:
        if '+' in s:
            state = True

    return state


def get_plus(l):
    """  This method returns the element with + """

    element = None

    for s in l:
        if '+' in s:
            element = s.replace('+', '')

    return element.strip()


def order_crossover(p1, p2):
    """ This method implements a crossover that tries to mantain certain order """

    start = random.randint(0, len(p1) / 2)
    #print start
    finish = random.randint(start + 1, len(p1) - 1)
    #print finish

    list_copy = p1[:start] + p1[start:finish] + p1[finish:len(p1)]  # We get a random slice of P1
    aux = p1[:start] + p1[finish:len(p1)]
    aux2 = p2[finish:len(p2)] + p2[:finish]

    # print 'Output:', list_copy
    # print 'Cut: ', p1[start:finish]
    # print 'Aux: ', aux
    # print 'Aux2: ', aux2
    # print 'P1: ', p1
    # print 'P2: ', p2

    count = 0
    for x in aux2:
        for x1 in aux:
            if x == x1 and finish < len(p1):
                # print 'finish'
                list_copy[finish] = x
                finish += 1
                # print list_copy
            elif x == x1 and finish >= len(p1) - 1:
                # print 'beginning'
                list_copy[count] = x
                count += 1
                # print list_copy

    return list_copy, p2


def permutation_mutation(p1):
    c1 = random.randint(0, len(p1) / 2)
    c2 = random.randint(c1 + 1, len(p1) - 1)

    #print 'C1: ', c1, 'C2: ', c2

    aux = p1[:c1 + 1] + p1[c2:c2 + 1] + p1[c1 + 1:c2] + p1[c2 + 1:]

    return aux


def swap_mutation(p1):
    li = list(p1)
    c1 = random.randint(0, len(p1) / 2)
    c2 = random.randint(c1 + 1, len(p1) - 1)
    element = p1[c1]
    #print 'C1: ', c1, 'C2: ', c2

    li[c1] = li[c2]
    li[c2] = element

    return li


def inversion_mutation(p1):
    c1 = random.randint(0, len(p1) / 2)
    c2 = random.randint(c1 + 1, len(p1) - 1)
    #print 'C1: ', c1, 'C2: ', c2

    aux = p1[:c1] + list(reversed(p1[c1: c2 + 1])) + p1[c2 + 1:]

    return aux



p1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
p2 = [9, 3, 7, 8, 2, 6, 5, 1, 4]


#print partially_mapped_crossover(p1, p2)
#aux2 = create_table(p1, p2)
#print aux2
#print edge_recombination(aux2)
#print order_crossover(p1, p2)
#print permutation_mutation(p1)
#print swap_mutation(p1)
#print inversion_mutation(p1)
































































