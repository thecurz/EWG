import graphviz as gv
import matplotlib.pyplot as plt
from math import *
from collections import deque
import os
from pathlib import Path


def check_path():
  CWD = f'{os.getcwd()}'
  if Path(CWD).name == 'english-words-graph':
    os.chdir(r'./project/')
    return f'{os.getcwd()}'
  if Path(CWD).name == 'data_generation':
    os.chdir(r'../')
    return f'{os.getcwd()}'
  return CWD

CWD = check_path()
DATASET1 = CWD + r'/datasets/SimVerb-3500.txt'
DATASET2 = CWD + r'/datasets/wordsim_relatedness_goldstandard.txt'
DATASET3 = CWD + r'/datasets/men.txt'

def normalize(n, top, c):
  return c*(n)/top

def read_data():
  word_list = []
  relations = []
  with open(DATASET1) as file:
    lines = file.readlines()
    for line in lines:
      line = line.split('	')
      first_word = line[0]
      second_word = line[1]
      relatedness = line[3]
      word_list.append(first_word)
      word_list.append(second_word)
      relations.append([first_word,[second_word,relatedness]])

  with open(DATASET2) as file:
    lines = file.readlines()
    for line in lines:
      line = line.split('	')
      first_word = line[0]
      second_word = line[1]
      relatedness = line[2]
      word_list.append(first_word)
      word_list.append(second_word)
      w = [second_word,relatedness[:-2]]
      relations.append([first_word, w])

  with open(DATASET3) as file:
    lines = file.readlines()
    for line in lines:
      line = line.split(' ')
      first_word = line[0]
      second_word = line[1]
      relatedness = normalize(float(line[2]), 9.96, 1)
      word_list.append(first_word)
      word_list.append(second_word)
      w = [second_word,relatedness]
      relations.append([first_word, w])
  return list(set(word_list)), relations

def build_graph(G):
  words_dict = dict()
  for u in range(len(G)):
    word = G[u][0]
    related = G[u][1][0]
    if word in words_dict:
      existing = words_dict[word]
      existing.append(G[u][1])
      words_dict[word] = existing
    else:
      words_dict[word] = [G[u][1]]
    if related in words_dict:
      existing = words_dict[related]
      existing.append([G[u][0], G[u][1][1]])
      words_dict[related] = existing
    else:
      words_dict[related] = [[G[u][0], G[u][1][1]]]
  return words_dict


def BFS_findsubgraph(G, source = ''):
  newG = dict()
  explored = set()
  lengths = []
  if source == '':
    source = list(G.keys())[0]
  queue = deque([])
  queue.extend(G[source])

  while(len(queue) > 0):
    current = queue.popleft()
    newG[current[0]] = G[current[0]]
    for neighbor in G[current[0]]:
      if neighbor[0] not in explored:
        queue.append(neighbor)
        explored.add(neighbor[0])
  keys = list(newG.keys())
  print(f'Number of nodes: {len(newG)}. \nExample node and edge ([node] - [adjacent node, weight]) [{keys[100]}] - [{G[keys[100]][0][0]}, {G[keys[100]][0][1]}]')
  return newG

def convert(G):
  new_G = []
  keys = list(G.keys())
  for i in range(len(G)):
    for j in range(len(G[keys[i]])):
      new_G.append([keys[i], G[keys[i]][j]])
  return new_G
word_list, relations = read_data()
relations = BFS_findsubgraph(build_graph(relations))

max = 0
for k in relations.keys():
  for i in range(len(relations[k])):
    if float(relations[k][i][1]) > max:
        max = float(relations[k][1][1])
from importlib.abc import TraversableResources
from operator import indexOf


def calculate_position(adj: dict):
    prevx = 0
    prevy = 0
    points_x = []
    points_y = []
    annotations = []
    x=0
    y=0
    #relu
    check = 0
    for k in adj.keys():  
      grade = 0 
      num_adj_nodes = len(adj[k])
      #adjacent_words = [adjacents[0] for adjacents in adj[k]]
      for n in range(num_adj_nodes):
        if adj[k][n][0] not in annotations:
          grade += 1
        else:
          index = annotations.index(adj[k][n][0])
          points_x.append(points_x[index])
          points_y.append(points_y[index])
      if grade == 0:
        continue
      angle_div = pi/grade
      angle = pi/4
      for n in range(num_adj_nodes):
        if adj[k][n][0] in annotations:
          continue
        angle += n*angle_div
        radiusx = float(adj[k][n][1]) if float(adj[k][n][1]) > 0 else 0.1
        radiusy = float(adj[k][n][1]) if float(adj[k][n][1]) > 0 else 0.1

        #is x really prevx

        x = prevx + cos(angle)/normalize(radiusx, max, 10)
        y = prevy + sin(angle)/normalize(radiusy, max, 10)
        points_x.append(x)
        points_y.append(y)
        annotations.append(adj[k][n][0])
      prevx = x
      prevy = y
    return points_x, points_y, annotations
for _ in range(100):
    print("HELLO")

X, Y, annotations = calculate_position(relations)

#points1, points2 = draw_lines(relations)

plt.figure(figsize=(100,100))
plt.scatter(X,Y,s=100,color="red")
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Scatter Plot with annotations",fontsize=15)
traversed = set()
label_index = 0

for i in range(len(X)):
    if X[i] in traversed:
      continue
    plt.annotate(annotations[label_index], (X[i], Y[i]))
    traversed.add(X[i])
    label_index += 1
    x_values = [X[i], X[i+1]]
    y_values = [Y[i], Y[i+1]]
    plt.plot(x_values, y_values, 'bo', linestyle="-")
plt.savefig("./client/src/test.png")
