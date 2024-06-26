# -*- coding: utf-8 -*-
"""listEnum.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oElGoQOwVEcFtlbyq4kVi2GINd0yWm3S
"""

# @title Class Graph
import sys
import copy
from collections import deque
import time
class Graph:
  __nodes = dict()
  def __init__(self):
    self.__nodes = dict()
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
  def getNodes(self):
    return copy.deepcopy(dict(self.__nodes))
  def getNeighbors(self, vertex):
    vertex = str(vertex)
    if vertex in self.__nodes:
      return (self.__nodes[str(vertex)]).copy()
    else:
      return "null"
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
  def addVertex(self, vertex):
    vertex = str(vertex)
    if vertex not in self.__nodes:
      self.__nodes[vertex] = set()
      return 0
    return 1
  def addEdge(self, vertex1, vertex2):
    vertex1 = str(vertex1)
    vertex2 = str(vertex2)
    if vertex1 not in self.__nodes:
      self.__nodes[vertex1] = set()
    if vertex2 not in self.__nodes:
      self.__nodes[vertex2] = set()
    self.__nodes[vertex1].add(vertex2)
    self.__nodes[vertex2].add(vertex1)
  def getGraphInducedBy(self, setVertices):
    if setVertices is None:
      return None
    gg = Graph()
    # add the set of vertices to an empty graph gg
    for vertex in setVertices:
      gg.addVertex(vertex)
    # get the Vertices of gg
    nv = gg.getNodes()
    for vertex in nv:
      # For every vertex in gg get the neighbors of the same vertex is self
      vs = self.getNeighbors(vertex)
      if vs != "null":
        for vv in vs:
          if vv in nv:
            gg.addEdge(vertex, vv)
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
    if not self.__nodes:
      return False

    visited = set()
    stack = []
    # Pick any vertex and add it to visited and stack
    start = next(iter(self.__nodes))
    if start is None:  # If no vertex is found
      return False

    stack.append(start)
    visited.add(start)
    while stack:
      current_vertex = stack.pop()
      neighbors = self.__nodes.get(current_vertex, set())  # Use .get() to handle missing keys
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
  def shortestDistance(self, start, end):
    if start not in self.__nodes or end not in self.__nodes:
      return -1  # Assuming -1 denotes that the vertices are not in the graph
    visited = set()
    queue = deque([(start, 0)])  # (vertex, distance)
    while queue:
      current_vertex, distance = queue.popleft()
      if current_vertex == end:
        return distance
      if current_vertex not in visited:
        visited.add(current_vertex)
        neighbors = self.__nodes[current_vertex]
        for neighbor in neighbors:
          queue.append((neighbor, distance + 1))
    return -1  # If end vertex is unreachable from start
  def areNeighbors(self, vertex, neighbor):
    neighbors = self.getNeighbors(vertex)
    if neighbor in neighbors:
      return True
    else:
      return False

# @title Main functions
def getX(G, k, C, P):
  X = set()
  for c in C:
    graph = G.getGraphInducedBy(P | {c})
    if graph.isKPlex(k):
      X.add(c)
  return X
def buildMaximal(G, k, P, C, listOfMaximals, excluded):
  if P in listOfMaximals:
    return
  if G.isMaximalKPlex(P, k) and (P not in listOfMaximals):
    listOfMaximals.append(P)
    return
  if C:
    X = getX(G, k, C, P)
    for c in X:
      graph = G.getGraphInducedBy(P | {c})
      if graph.isKPlex(k):
        buildMaximal(G, k, P | {c}, X - {c}, listOfMaximals, excluded)
      else:
        if P not in listOfMaximals:
          excluded.append(P)
  else:
    return listOfMaximals
def listEnum(G, k):
  if G.isKPlex(k):
    P = G.getDegeneracyOrderingWithEdgeRemoval()
    return P
  else:
    C = set(G.getDegeneracyOrderingWithEdgeRemoval())
    listOfMaximals = list()
    excluded = list()
    for c in C:
      buildMaximal(G, k, {c}, C - {c}, listOfMaximals, excluded)
      neighbors = G.getNeighbors(c)
      buildMaximal(G, k, neighbors | {c}, C - (neighbors | {c}), listOfMaximals, excluded)
      #neighbors2h = G.get2HopNeighbors(c)
      #buildMaximal(G, k, neighbors2h | (neighbors | {c}), C - (neighbors2h | (neighbors | {c})), listOfMaximals, excluded)
    print("Excluded size = " + str(len(excluded)))
    return listOfMaximals

# @title Main
File = open('example.txt', 'r')
Lines = File.readlines()
g = Graph()
g.addEdges(Lines)
ll = listEnum(g, 3)
print(ll)
print(len(ll))