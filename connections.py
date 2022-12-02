# HTTPS requests
import urllib, urllib.request
import feedparser

# graph construction/drawing
import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt

# string manipulation
import string
from unidecode import unidecode

# command line arguments
import argparse

cmdParser = argparse.ArgumentParser()
cmdParser.add_argument('author', help="Paper author to look into -- replace spaces with + please")
cmdParser.add_argument('field_of_study', default='cs', \
                       help="Author's field of study", \
                       choices=['cs',
                                'math',
                                'econ',
                                'eess (electrical engineering and systems science)',
                                'physics',
                                'q-bio',
                                'q-fin',
                                'stat'])
cmdParser.add_argument('breadth', type=int, default = 5, \
                       help="How many papers to look at per author")
cmdParser.add_argument('depth', type=int, default = 2, \
                       help="How many layers deep to look")

args = cmdParser.parse_args()

# parameters
author = args[0]
subject = args[1]
breadth = args[2]
depth = args[3]

# base querying functions
# Converts between a name's query form and normal form and turns an author
# into an API call
toQuery = lambda author : unidecode(author.replace(" ", "+"))
toNormal = lambda author : unidecode(string.capwords(author.replace("+", " ")))
toFilename = lambda author : author.replace(" ", "_").lower()
url = lambda author : "https://export.arxiv.org/api/query?search_query=au:%s&cat=%s&max_results=%i" % (author, subject, breadth)

graph = {toNormal(author) : set()} # author -> adjacent authors //// old author -> {adjacent authors -> num shared}
queue = [toNormal(author)]
nextQueue = []

# queries arxiv for papers by the author, then finds who
# the author worked with and queries those people
for i in range(depth):
    while(len(queue) != 0):
        a = queue.pop(0)
        data = urllib.request.urlopen(url(toQuery(a))).read()
        feed = feedparser.parse(data)

        for entry in feed.entries:
            authorSet = {toNormal(author.name) for author in entry.authors}
            authorSet.discard(a)
            graph[a] = graph.get(toNormal(a)).union(authorSet)

            for name in authorSet:
                if(graph.get(name) == None):
                    graph[toNormal(name)] = set()
                    nextQueue.append(toNormal(name))
    queue = nextQueue
    nextQueue = []

# contsructs the networkx graph
visG = nx.Graph()

edges = []
for a1 in graph.keys():
    for a2 in graph[a1]:
        edges.append([a1, a2])

visG.add_edges_from(edges)
nt = Network('500px', '500px')
nt.from_nx(visG)

# saves the graph and pulls it up in a web browser (browser part inconsistent)
nt.save_graph('%s_connections.html' % toFilename(author))