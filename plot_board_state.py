#tester code for kornislav BFS implementation

from logic import *
from strategies import *
import networkx as nx
import sys
import matplotlib
from matplotlib import cm
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

#testdata = {'game': {'id': 'f1d4600b-91ce-424b-b7b1-64505442de57'}, 'turn': 458, 'board': {'height': 7, 'width': 7, 'food': [{'x': 5, 'y': 2}, {'x': 5, 'y': 3}, {'x': 4, 'y': 3}, {'x': 3, 'y': 1}, {'x': 4, 'y': 1}, {'x': 3, 'y': 2}, {'x': 5, 'y': 1}, {'x': 4, 'y': 2}, {'x': 3, 'y': 3}], 'snakes': [{'id': 'gs_8fFRqghPjmQ3dd38TWPTCPhB', 'name': 'PhoenixBeaudry / NodeSlave', 'health': 95, 'body': [{'x': 0, 'y': 6}, {'x': 0, 'y': 5}, {'x': 0, 'y': 4}, {'x': 0, 'y': 3}, {'x': 0, 'y': 2}, {'x': 0, 'y': 1}, {'x': 0, 'y': 0}, {'x': 1, 'y': 0}, {'x': 2, 'y': 0}, {'x': 3, 'y': 0}, {'x': 4, 'y': 0}, {'x': 5, 'y': 0}, {'x': 6, 'y': 0}, {'x': 6, 'y': 1}, {'x': 6, 'y': 2}, {'x': 6, 'y': 3}, {'x': 6, 'y': 4}, {'x': 5, 'y': 4}, {'x': 4, 'y': 4}, {'x': 3, 'y': 4}, {'x': 2, 'y': 4}, {'x': 2, 'y': 3}, {'x': 2, 'y': 2}, {'x': 2, 'y': 1}, {'x': 1, 'y': 1}, {'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 1, 'y': 4}, {'x': 1, 'y': 5}, {'x': 2, 'y': 5}, {'x': 3, 'y': 5}, {'x': 4, 'y': 5}, {'x': 5, 'y': 5}, {'x': 6, 'y': 5}, {'x': 6, 'y': 6}, {'x': 5, 'y': 6}, {'x': 4, 'y': 6}, {'x': 3, 'y': 6}, {'x': 2, 'y': 6}, {'x': 1, 'y': 6}]}]}, 'you': {'id': 'gs_8fFRqghPjmQ3dd38TWPTCPhB', 'name': 'PhoenixBeaudry / NodeSlave', 'health': 95, 'body': [{'x': 0, 'y': 6}, {'x': 0, 'y': 5}, {'x': 0, 'y': 4}, {'x': 0, 'y': 3}, {'x': 0, 'y': 2}, {'x': 0, 'y': 1}, {'x': 0, 'y': 0}, {'x': 1, 'y': 0}, {'x': 2, 'y': 0}, {'x': 3, 'y': 0}, {'x': 4, 'y': 0}, {'x': 5, 'y': 0}, {'x': 6, 'y': 0}, {'x': 6, 'y': 1}, {'x': 6, 'y': 2}, {'x': 6, 'y': 3}, {'x': 6, 'y': 4}, {'x': 5, 'y': 4}, {'x': 4, 'y': 4}, {'x': 3, 'y': 4}, {'x': 2, 'y': 4}, {'x': 2, 'y': 3}, {'x': 2, 'y': 2}, {'x': 2, 'y': 1}, {'x': 1, 'y': 1}, {'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 1, 'y': 4}, {'x': 1, 'y': 5}, {'x': 2, 'y': 5}, {'x': 3, 'y': 5}, {'x': 4, 'y': 5}, {'x': 5, 'y': 5}, {'x': 6, 'y': 5}, {'x': 6, 'y': 6}, {'x': 5, 'y': 6}, {'x': 4, 'y': 6}, {'x': 3, 'y': 6}, {'x': 2, 'y': 6}, {'x': 1, 'y': 6}]}}

testdata = defaultdata

#Setup board state
gameboard = Board(testdata)

# Hungry/NotHungry Meta Strategy Implementation
if(gameboard.myhealth < 40):
    chosen_strategy = hungry
else:
    chosen_strategy = nothungry

foresight = 2
graph = generate_graph(nothungry, gameboard)

print("Kornislav decided to go: ", next_direction(gameboard.myself[0], determine_safest_move(gameboard, graph, foresight, nothungry)))


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

  edgeslist = []

  for edge in graph.edges:
    edges[edge] = graph[edge[0]][edge[1]]['weight']
    edgeslist.append(graph[edge[0]][edge[1]]['weight'])

  nx.draw_networkx_edge_labels(graph, pos, edges, font_size=6, font_color='blue')

  nx.draw_networkx_edges(graph, pos, edge_color=edgeslist, width=6, edge_vmin=-200, edge_vmax=200, edge_cmap=cm.get_cmap('seismic', 12))

  plt.axis('off')
  plt.gca().invert_yaxis()
  plt.savefig("test")
