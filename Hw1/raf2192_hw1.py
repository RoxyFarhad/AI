"""
COMS W4701 Artificial Intelligence - Homework 0

In this assignment you will implement a few simple functions reviewing
basic Python operations and data structures.

@author: Roxanne Farhad / raf2192
"""



# Input: Two individual lists, each with at least two elements
def manip_list(list1, list2):
    #print last element of list1
    print(list1[-1])
    #remove last element of list1
    del list1[-1]

    #change second element of list2 to be identical to first element of list1

    list2[0] = list1[0]

    #print concatenation of list1 and list2 without modifying them

    print(list1 + list2)

    #return single list consisting of list1 and list2 as its two elements
    list3 = list1 + list2
    return list3

# Input: Two individual object parameters
def manip_tuple(obj1, obj2):
    #create a tuple of the two object parameters

    tup = (obj1, obj2)

    #attempt to modify the tuple by reassigning first item (should throw exception)

    tup[0] = obj1
    return None


# Input: Two lists and one object
def manip_set(list1, list2, obj):
    #create a set called set1 using list1
    set1 = set(list1)
     #create a set called set2 using list2
    set2 = set(list2)
    #add obj to set1
    set1.add(obj)
    #test if obj is in set2 (print True or False)
    if obj in set2:
        print("True")
    else: 
        print("False")
    #print the union of set1 and set2
    print(set1 | set2)
    #print the intersection of set1 and set2
    print(set1 & set2)
    #remove obj from set1
    set1.remove(obj); 
    return None

# Input: Two tuples and one object
def manip_dict(tuple1, tuple2, obj):
    #create a dictionary such that elements of tuple1 serve as keys for elements of tuple2
    dict1 = dict(zip(tuple1, tuple2))
    #print value of dictionary mapped by obj
    print(dict1.get(obj))
    #delete dictionary pairing with obj key
    dict1.pop(obj)
    #print length of dictionary
    print(len(dict1)) 
    #add new pairing to dictionary mapping from obj to the value 0
    dict1[obj] = 0
    #return a list in which each element is a two-tuple of the dictionary's key-value pairings
    
    tup_list = []

    for key in dict1: 
        tup_list.append((key, dict1.get(key)))
    
    return tup_list


if __name__ == "__main__":
    #Test case
    print(manip_list(["artificial", "intelligence", "rocks"], [4701, "is", "fun"]))

    try: manip_tuple("oh", "no")
    except TypeError: print("Can't modify a tuple!")

    manip_set(["sets", "have", "no", "duplicates"], ["sets", "operations", "are", "useful"], "yeah!")

    print(manip_dict(("list", "tuple", "set"), ("ordered, mutable", "ordered, immutable", "non-ordered, mutable"), "tuple"))