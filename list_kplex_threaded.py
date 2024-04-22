# -*- coding: utf-8 -*-
"""list-kplex.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Qr4o_cPTglolikTnbs5xRB-IiwdL7l_i
"""

# @title Class Graph
from collections import defaultdict
import sys
import copy
class Graph:
  __nodes = dict()
  """def __init__(self):
    self.__nodes = dict()"""
  def __init__(self):
    self.__nodes = defaultdict(set)
  def addEdges(self, edges):
    for edge in edges:
      vertices = edge.split()
      if len(vertices) == 1:
        self.__nodes[vertices[0]] = set()
      else:
        if self.__nodes.get(vertices[0]):
          self.__nodes[vertices[0]].add(vertices[1])
          if self.__nodes.get(vertices[1]):
            self.__nodes[vertices[1]].add(vertices[0])
          else:
            self.__nodes[vertices[1]] = set(vertices[0])
        else:
          self.__nodes[vertices[0]] = set(vertices[1])
          if self.__nodes.get(vertices[1]):
            self.__nodes[vertices[1]].add(vertices[0])
          else:
            self.__nodes[vertices[1]] = set(vertices[0])
  """def getNodes(self):
    return copy.deepcopy(dict(self.__nodes))"""
  def getNodes(self):
    return dict(self.__nodes)
  """def getNeighbors(self, vertex):
    vertex = str(vertex)
    if vertex in self.__nodes:
      return (self.__nodes[str(vertex)]).copy()
    else:
      return "null"""
  def getNeighbors(self, vertex):
    return self.__nodes.get(vertex, set())
  def get2HopNeighbors(self, vertex):
    neighbors = self.getNeighbors(vertex)
    thneighbors = set()
    for neighbor in neighbors:
      ns = self.getNeighbors(neighbor)
      for n in ns:
        if (n not in neighbors) and (n != str(vertex)):
          thneighbors.add(n)
    return thneighbors
  def getNonNeighbors(self, vertex):
    vertex = str(vertex)
    neighbors = self.getNeighbors(vertex)
    vertices = self.getNodes()
    nonNeighbors = set()
    for v in vertices:
      if (v not in neighbors) and (v != vertex):
        nonNeighbors.add(v)
    return nonNeighbors
  def getDeg(self, vertex):
    return len(self.getNeighbors(vertex))
  def getSize(self):
    return len(self.__nodes)
  """def addVertex(self, vertex):
    vertex = str(vertex)
    if vertex not in self.__nodes:
      self.__nodes[vertex] = set()
      return 0
    return 1"""
  def addVertex(self, vertex):
    if vertex not in self.__nodes:
      self.__nodes[vertex] = set()
  """def addEdge(self, vertex1, vertex2):
    vertex1 = str(vertex1)
    vertex2 = str(vertex2)
    if vertex1 not in self.__nodes:
      self.__nodes[vertex1] = set()
    if vertex2 not in self.__nodes:
      self.__nodes[vertex2] = set()
    self.__nodes[vertex1].add(vertex2)
    self.__nodes[vertex2].add(vertex1)"""
  def addEdge(self, vertex1, vertex2):
    self.__nodes[vertex1].add(vertex2)
    self.__nodes[vertex2].add(vertex1)
  """def getGraphInducedBy(self, setVertices):
    if setVertices is None:
      return None
    gg = Graph()
    # Add vertices to gg
    for vertex in setVertices:
      gg.addVertex(vertex)
    # Add edges only between vertices present in gg
    for vertex in gg.getNodes():
      neighbors_in_gg = set(self.getNeighbors(vertex)) & gg.getNodes().keys()  # Get neighbors present in gg
      for neighbor in neighbors_in_gg:
        gg.addEdge(vertex, neighbor)
    return gg"""
  def getGraphInducedBy(self, setVertices):
    if setVertices is None:
      return None
    gg = Graph()
    for vertex in setVertices:
      gg.addVertex(vertex)
    for vertex in self.__nodes:
      if vertex in setVertices:
        neighbors_in_gg = self.__nodes[vertex] & setVertices
        for neighbor in neighbors_in_gg:
          gg.addEdge(vertex, neighbor)
    return gg

  def getDegeneracyOrdering(self):
    gg = self.getNodes().copy()
    n = self.getSize()
    i = 0
    l = list()
    s = 0
    while i < n:
      min_size = sys.maxsize
      for e in gg:
        if min_size > len(gg[e]):
          min_size = len(gg[e])
      for e in gg:
        if min_size == len(gg[e]):
          l.append(e)
          s = e
          break
      if s != 0:
        gg.pop(s)
      i = i + 1
    return l
  def getDegeneracyOrderingWithEdgeRemoval(self):
    l = list()
    ss = copy.deepcopy(dict(self.getNodes()))
    n = len(ss)
    for i in range(n):
      s = 0
      min_size = sys.maxsize
      for e in ss:
        if min_size > len(ss[e]):
          min_size = len(ss[e])
      for e in ss:
        if min_size == len(ss[e]):
          l.append(e)
          s = str(e)
          break
      if s != 0:
        sss = ss[s].copy()
        ss.pop(s)
        if sss:
          for e in ss:
            for index in sss:
              if index == e:
                if s in ss[e]:
                  ss[e].remove(s)
    return l
  def getEdgesNumber(self):
    graph = self.getNodes()
    print(graph)
    s = 0
    for v in graph:
      s = s + len(graph[v])
    return (s / 2)
  def isConnected(self):
    if not self.__nodes:  # Check if the graph is empty
      return False
    visited = set()
    stack = []
    # pick any vertex and add it to visited and stack
    start = next(iter(self.__nodes))
    stack.append(start)
    visited.add(start)
    while stack:
      current_vertex = stack.pop()
      neighbors = self.__nodes[current_vertex]
      for neighbor in neighbors:
        if neighbor not in visited:
          stack.append(neighbor)
          visited.add(neighbor)
    return len(visited) == len(self.__nodes)
  def isKPlex(self, k):
    if not self.isConnected():
      return False
    vertices = set((self.getNodes()).keys())
    n = len(vertices)
    for vertex in vertices:
      if len(self.getNeighbors(vertex)) < (n - k):
        return False
    return True
  def isMaximalKPlex(self, vertices, k):
    graph = self.getGraphInducedBy(vertices)
    if not graph.isKPlex(k):
      return False
    nodes = (self.getNodes()).keys()
    for node in nodes:
      if not (node in vertices):
        graph = self.getGraphInducedBy(vertices.union({node}))
        if graph.isKPlex(k):
          return False
    return True
  def getMinimumDegree(self):
    minimum = sys.maxsize
    elems = self.__nodes.keys()
    for e in elems:
      size = self.getDeg(e)
      if minimum > size:
        minimum = size
    return minimum
  def getMaxK(self):
    size = len(self.__nodes.keys())
    minimum = self.getMinimumDegree()
    return (size - minimum)
  def getLargestCliqueContainingNode(self, node):
    max_clique_size = 0
    if node in self.__nodes:
      for neighbor in self.__nodes[node]:
        # Check if neighbor exists in the graph
        if neighbor in self.__nodes:
          common_neighbors = self.__nodes[node] & self.__nodes[neighbor]
          clique_size = len(common_neighbors) + 1  # Include the node itself
          max_clique_size = max(max_clique_size, clique_size)
    return max_clique_size
  def filterNodesForKplexes(self, k, m):
    filtered_nodes = set()
    min_clique_size = m // k  # Minimum size of a clique to be part of a k-plex
    for node in self.__nodes:
      # Check if the node belongs to a clique of size at least min_clique_size
      clique_size = self.getLargestCliqueContainingNode(node)
      if clique_size >= min_clique_size:
        filtered_nodes.add(node)
    return filtered_nodes
  def coreness(self, k):
    elements = self.__nodes.keys()
    n = len(elements)
    ss = set()
    for elem in elements:
      if self.getDeg(elem) >= (n - k):
        ss.add(elem)
    graph = self.getGraphInducedBy(ss)
    return graph

# @title Main functions

def listKPlexRecursive(G, k, candidate_set, listOfMaximals, memo=None):
  if memo is None:
    memo = set()
  key = (frozenset(candidate_set), k)  # Using frozenset for memoization
  if key in memo:
    return
  if G.isMaximalKPlex(candidate_set, k) and candidate_set not in listOfMaximals:
    listOfMaximals.append(candidate_set)
    memo.add(key)
    return
  else:
    graph = G.getGraphInducedBy(candidate_set)
    if not graph.isKPlex(k) and graph.isConnected():
      for vertex in candidate_set:
        #if graph.getDeg(vertex) <= len(candidate_set) - k:
        next_set = candidate_set - {vertex}
        listKPlexRecursive(G, k, next_set, listOfMaximals, memo)
  memo.add(key)

def listKPlex(G, k):
  degeneracy_ordering = set(G.getDegeneracyOrderingWithEdgeRemoval())
  listOfMaximals = []
  listKPlexRecursive(G, k, degeneracy_ordering, listOfMaximals)
  return listOfMaximals

# @title Main
"""File = open('/content/example3.txt', 'r')
Lines = File.readlines()
g = Graph()
g.addEdges(Lines)
P = g.getNodes().keys()
kmax = g.getMaxK()
for k in range(kmax, 1, -1):
  print("List for k = " + str(k))
  ll = listKPlex(g, k)
  print(ll)
  print(len(ll))"""

from multiprocessing import Pool

File = open('/content/karate.txt', 'r')
Lines = File.readlines()
g = Graph()
g.addEdges(Lines)
kmax = g.getMaxK()

# Compute maximal k-plexes for kmax initially
ll = list(listKPlex(g, kmax))  # Convert sets to lists

def compute_maximal_k_plex(k, g, ll):
    listOfMaximals = []
    for lls in ll:
        listKPlexRecursive(g, k, lls, listOfMaximals)
    return listOfMaximals

# Iterate over decreasing values of k
for k in range(kmax, 1, -1):
    print("Computing maximal k-plexes for k =", k)

    # Parallelize the computation for the current value of k
    with Pool() as pool:
        # Calculate chunk size ensuring it's at least 1
        chunk_size = max(len(ll) // pool._processes, 1)

        # Split ll into smaller chunks for parallel processing
        chunks = [ll[i:i+chunk_size] for i in range(0, len(ll), chunk_size)]

        # Compute maximal k-plexes in parallel
        results = pool.starmap(compute_maximal_k_plex, [(k, g, chunk) for chunk in chunks])

        # Combine the results
        listOfMaximals = [item for sublist in results for item in sublist]

    print("List for k =", k)
    print(listOfMaximals)
    print(len(listOfMaximals))

    # Update ll for the next iteration
    ll = list(listOfMaximals)  # Convert sets to lists