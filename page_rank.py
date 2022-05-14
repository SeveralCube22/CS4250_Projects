import json
from math import inf
from multiprocessing.sharedctypes import Value
import os
import re

class Node:
    def __init__(self, link):
        self.link = link
        self.rank = None
        
    def __eq__(self, other):
        return self.link == other.link
    
    def __hash__(self):
        return hash(self.link)

class Graph:
    def __init__(self, site, max_iterations=None, eps=None):
        self.nodes = {}
        self.create_graph(site)
        self.calculate_page_rank(max_iterations, eps)
        self.save_page_ranks(site)
        
    def create_graph(self, site):
        path = "./reports/links/"
        read_file = "{}{}-report.csv".format(path, site)
        file = open(read_file, "r", encoding="utf-16")
        next(file)
        num_pages = 0
        
        for line in file:
            (link, _, out_links) = re.split(',\s', line)
            out_nodes = [Node(l) for l in json.loads(out_links)]
            node = Node(link)
            self.nodes[node] = out_nodes
            num_pages += 1
                
        for node in self.nodes:
            node.rank = 1 / num_pages
       
    def get_in_nodes(self, node):
        in_nodes = []
        for pot in self.nodes:
            if node in self.nodes[pot]:
                in_nodes.append(pot) 
        return in_nodes
    
    def get_ranks(self):
        return {n: n.rank for n in self.nodes}
    
    def calculate_page_rank(self, max_iterations=None, eps=None):
        curr_ranks = self.get_ranks()
        curr_iter = 0
        curr_eps = inf
        
        max_iterations = inf if max_iterations == None else max_iterations
        eps = -inf if eps == None else eps
        
        while curr_iter < max_iterations and curr_eps >= eps:
            pot_ranks = {}
            for node in self.nodes:
                rank = sum([n.rank / len(self.nodes[n]) for n in self.get_in_nodes(node)])
                pot_ranks[node] = rank
            
            for node in self.nodes:
                node.rank = pot_ranks[node]
                
            curr_eps = abs(sum(pot_ranks.values()) / len(pot_ranks.values()) - sum(curr_ranks.values()) / len(curr_ranks.values()))
            curr_ranks = pot_ranks    
            curr_iter += 1
            
    def save_page_ranks(self, site):
        path = "./reports/page_ranks/"
        if not os.path.exists(path):
            os.makedirs(path)
        
        write_file = "{}{}-report.csv".format(path, site)
        mode = 'a' if os.path.exists(write_file) else 'w'
        
        file = open(write_file, mode, encoding="utf-16")
        if mode == 'w':
            file.write("Links, Page Ranks\n")
        
        for node in self.nodes:
            file.write("{}, {}\n".format(node.link, node.rank))
            
# This function converts the relative links in our page rank files to the correctly formatted html files in our repo
# The relative link '/' == root.html for a given site in our repo
def get_html_format_ranks(site):
    path = "./reports/page_ranks/"
    read_file = "{}{}-report.csv".format(path, site)
    file = open(read_file, 'r', encoding="utf-16")
    next(file)
     
    ranks = {}           
    for line in file:
        (link, rank) = re.split(",\s", line)
        
        if link == "/": formatted_link = "root"
        else:
            formatted_link = link.replace("/", "_").replace("?","_").replace("=", "_").replace("%", "").replace("$", "").replace(":", "")
        
        html_format = "{}{}.html".format(site, formatted_link) # These are the same files that are in the repo
        
        ranks[html_format] = rank
    
    #print(ranks)
    return ranks
                
if __name__ == "__main__":
    seeds = ["cbs", "jawikipediaorg", "pokebip"]
    html_ranks = {} # this is a dict that contains all the html_pages and their corresponding ranks for each site. e.g. {"cbs": {"root.html": .275}, "pokebip": {"root.html": .57879}, etc.}
    for seed in seeds:
        formatted_site = seed.replace("/", "").replace(":", "").replace(".", "").replace("https", "").replace("www", "").replace("com", "")
        
        g = Graph(formatted_site, max_iterations=1000, eps=.1) # constructor saves ranks to file
        html_ranks[formatted_site] = get_html_format_ranks(formatted_site)