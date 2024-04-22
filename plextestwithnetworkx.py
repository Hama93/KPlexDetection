# -*- coding: utf-8 -*-
"""plextestwithnetworkx.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1bIOIVdoWW4MD0pxf4vTd6TKw-olzYJ2_
"""

import networkx as nx
import matplotlib.pyplot as plt

def readGraph(f):
  G = nx.Graph()
  File = open(f, 'r')
  Lines = File.readlines()
  for line in Lines:
    vertices = line.split()
    if len(vertices) == 1:
      G.add_node(vertices[0])
    else:
      G.add_edge(vertices[0], vertices[1])
  return G

G = readGraph('karate.txt')
nx.draw_spring(G, with_labels = True)
plt.show()

def isKPlex(G, k):
  vertices = G.nodes()
  n = len(vertices)
  for vertex in vertices:
    if len(list(G.neighbors(vertex))) < (n - k):
      return False
  return True
def isMaximalKPlex(G, vertices, k):
    graph = G.subgraph(vertices)
    if not isKPlex(graph, k):
      return False
    nodes = list(G.nodes())
    for node in nodes:
      if not (node in vertices):
        graph = G.subgraph(list(vertices | {node}))
        if isKPlex(graph, k):
          return False
    return True
def listKPlexRecursive(G, k, candidate_set, listOfMaximals, memo=None):
  #print(candidate_set)
  """if len(candidate_set) <= (2 * k) - 1:
    return"""
  if memo is None:
    memo = set()
  key = (frozenset(candidate_set), k)  # Using frozenset for memoization
  if key in memo:
    return
  graph = G.subgraph(list(candidate_set))
  if isMaximalKPlex(graph, candidate_set, k) and (candidate_set not in listOfMaximals):
    listOfMaximals.append(candidate_set)
    memo.add(key)
    return
  else:
    if not isKPlex(graph, k) and nx.is_connected(graph):
      for vertex in candidate_set:
        #if graph.getDeg(vertex) <= len(candidate_set) - k:
        next_set = candidate_set - {vertex}
        #subgraph = G.getGraphInducedBy(next_set)
        #if subgraph.hasCycle():
        listKPlexRecursive(G, k, next_set, listOfMaximals, memo)
  memo.add(key)

def listKPlex(G, k):
  degeneracy_ordering = set(G.nodes())
  listOfMaximals = []
  listKPlexRecursive(G, k, degeneracy_ordering, listOfMaximals)
  return listOfMaximals

def buildMaximal(G, k, P, C, listOfMaximals, excluded):
  if P in listOfMaximals:
    return
  if isMaximalKPlex(G, P, k) and (P not in listOfMaximals):
    listOfMaximals.append(P)
    return
  if C:
    for c in C:
      graph = G.subgraph(list(P | {c}))
      if isKPlex(graph, k):
        buildMaximal(G, k, P | {c}, C - {c}, listOfMaximals, excluded)
      else:
        if P not in listOfMaximals:
          excluded.append(P)
  else:
    return listOfMaximals
def listEnum(G, k):
  if isKPlex(G,k):
    ll = list()
    P = set(G.nodes())
    ll.append(P)
    return ll
  else:
    C = set(G.nodes())
    n = len(C)
    listOfMaximals = list()
    excluded = list()
    for c in C:
      neighbors = set(G.neighbors(c))
      buildMaximal(G, k, neighbors | {c}, C - (neighbors | {c}), listOfMaximals, excluded)
    print("Excluded size = " + str(len(excluded)))
    return listOfMaximals

vertices = list(G.nodes())
n = len(vertices)
degree_dict = dict(G.degree())
min_degree = min(degree_dict.values())
kmax = n - min_degree
for k in range(kmax, 1, -1):
  print("List for k = " + str(k))
  ll = listEnum(G, k)
  print(ll)
  print(len(ll))
