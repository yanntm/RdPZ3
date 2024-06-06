# rdpz3/example_nets.py

from rdpz3.RdP import RdP

def net1():
    place = ['A1', 'B1', 'A2', 'B2']
    trans = ['t1', 't2']
    pre = [[(0, 1), (2, 1)], [(0, 1), (2, 1)]]
    post = [[(1, 1), (2, 1)], [(0, 1), (3, 1)]]
    m0 = [1, 0, 1, 0]
    return RdP(place, trans, pre, post, m0)

def net2():
    place = ['A1', 'B1', 'A2', 'B2', 'B3']
    trans = ['t1', 't2', 't3']
    pre = [[(0, 1), (2, 1)], [(0, 1), (2, 1)], [(1, 1), (3, 1)]]
    post = [[(1, 1), (2, 1)], [(0, 1), (3, 1)], [(1, 1), (4, 1)]]
    m0 = [1, 0, 1, 0, 0]
    return RdP(place, trans, pre, post, m0)

def net3():
    place = ['A1', 'B1', 'A2', 'B2', 'B3']
    trans = ['t1', 't2', 't3']
    pre = [[(0, 1), (2, 1)], [(0, 1), (2, 1)], [(1, 1), (3, 1)]]
    post = [[(1, 1), (2, 1)], [(0, 1), (3, 1)], [(1, 1), (3, 1), (4, 1)]]
    m0 = [1, 0, 1, 0, 0]
    return RdP(place, trans, pre, post, m0)
