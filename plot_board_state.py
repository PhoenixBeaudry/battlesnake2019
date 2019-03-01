#tester code for kornislav BFS implementation

from logic import *
from strategies import *
import networkx as nx
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Data to be fed into the graph generator
# this can be changed to determine Kornislavs
# behaviour in certain conditions
defaultdata = {
  "game": {
    "id": "game-id-string"
  },
  "turn": 4,
  "board": {
    "height": 15,
    "width": 15,
    "food": [
      {
        "x": 9,
        "y": 8
      },
      {
        "x": 8,
        "y": 8
      }
    ],
    "snakes": [
      {
        "id": "snake-id-string",
        "name": "Sneky Snek",
        "health": 90,
        "body": [
          {
            "x": 1,
            "y": 3
          }
        ]
      },
      {
        "id": "othersnake",
        "name": "Emeny",
        "health": 90,
        "body": [
          {
            "x": 4,
            "y": 4
          },
          {
            "x": 5,
            "y": 4
          }
        ]
      }
    ]
  },
  "you": {
    "id": "snake-id-string",
    "name": "Sneky Snek",
    "health": 90,
    "body": [
      {
        "x": 1,
        "y": 3
      }
    ]
  }
}

testdata = defaultdata





#Setup board state
gameboard = Board(testdata)
graph = generate_graph(nothungry, gameboard)

print("Kornislav decided to go: ", next_direction(gameboard.myself[0], lightest_adjacent_edge(gameboard, graph)))


plot = True

if(plot):
  #Setup plot
  plt.figure(figsize=(15,15))
  pos = {}
  for node in graph:
  	pos[node] = node
  #Draw all nodes
  nx.draw_networkx(graph, pos, font_size=7)

  #Color food nodes
  nx.draw_networkx_nodes(graph, pos, nodelist=gameboard.food, node_color='green')

  #Color self nodes
  nx.draw_networkx_nodes(graph, pos, nodelist=gameboard.myself, node_color='blue')

  #Color enemy nodes
  enemylist = []
  for enemy in gameboard.enemies:
  	for enemypart in enemy:
  		enemylist.append(enemypart)

  nx.draw_networkx_nodes(graph, pos, nodelist=enemylist, node_color='black')

  edges = {}

  for edge in graph.edges:
  	edges[edge] = graph[edge[0]][edge[1]]['weight']

  nx.draw_networkx_edge_labels(graph, pos, edges, font_size=6, font_color='blue')

  plt.axis('off')
  plt.gca().invert_yaxis()
  plt.savefig("test")
