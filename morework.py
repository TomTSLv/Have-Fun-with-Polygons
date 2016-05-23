from PositionalList import PositionalList 

def printlist(L,s):
    print(s,end=": ")
    for i in L:
        print(i,end=' ')
    print()

L1 = PositionalList()
L2 = PositionalList()
for i in range(5):
    L1.add_last(i)
    L2.add_last(i + 5)
if True:   #Once again, turn these on as you advance through this assignment.
            #Leave them all on when you hand in.
    #Task 1: Append the elements of a given list the end of a list.
    #The given list is basically destroyed.
    #¡Do this in constant time!
    L1.append(L2)
    printlist(L1, 'L1 after appending L2')
    printlist(L2, 'L2 after being appended L1')
    L2.add_last('seventeen')
    printlist(L1, 'L1 after adding \'seventeen\' to L2')
    printlist(L2, 'L2 after adding \'seventeen\' to it')
    # Output
    # L1 after appending L2: 0 1 2 3 4 5 6 7 8 9 
    # L2 after being appended L1:
    #
    # (so L2 is empty)
    # L1 after adding 'seventeen' to L2: 0 1 2 3 4 5 6 7 8 9 
    # L2 after adding 'seventeen' to it: seventeen 
if True:
    #Task 2: Given a Position p, return a new Positional List that contains all
    #the elements up to and including what is at p.
    #¡Do this in constant time!
    p = L1.first()
    for i in range(4):
        p = L1.after(p)
    print('L3\'s last element should be {0}'.format(p.element()))
    L3 = L1.split(p)
    printlist(L3, 'L3')
    printlist(L1, 'L1')
    print('Length of L1 is {0}'.format(len(L1)))
    print('Length of L3 is {0}'.format(len(L3)))
    # Output:
    # L3's last element should be 4
    # L3: 0 1 2 3 4 
    # L1: 5 6 7 8 9
    # Length of L1 is 5
    # Length of L3 is 5
if True:
    #Task 3: Reverse a list. Append and split should still work properly!
    #¡If you can do this in constant time, you will get an A on this homework!
    L1=PositionalList()
    for i in range(10):
        L1.add_last(i)
    L1.reverse()
    printlist(L1, 'L1 after reversing')
    L1.add_last('Right')
    printlist(L1, 'L1 after appending \'Right\'')
    p = L1.first()
    for i in range(4):
        p = L1.after(p)
    print('L4\'s last element should be {0}'.format(p.element()))
    L4 = L1.split(p)
    printlist(L4, 'L4')
    L4.append(L1)
    printlist(L4, 'jdasfklsdj')
    # Output:
    # L1 after reversing: 9 8 7 6 5 4 3 2 1 0
    # L1 after appending 'Right': 9 8 7 6 5 4 3 2 1 0 Right 
    # L4's last element should be 5
    # L4: 9 8 7 6 5 
