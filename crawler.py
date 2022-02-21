import requests
import time
import os

from bs4 import BeautifulSoup

def permits_link(url):
    resp = requests.get("{}/robots.txt".format(url))
    data = resp.text.split("\n")

    disallow_links = {}
    user_agent = False
    for line in data:
        if "User-agent" in line:
            agent = line.split(":")[1].strip()
            user_agent = True if agent == "*" else False
        
        if user_agent:
            if "Disallow" in line:
                link = line.split(":")[1].strip()
                value = False
                if link[-1] == "*": # if last character of link ends with *
                    value = True 
                disallow_links[link] = value
    return disallow_links

def get_links(html, base_url):
    links = []
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.find_all('a'):
        if link.has_attr("href"):
            url = link["href"]
            if url == '/' or url == "": # skip root
                continue
            if base_url in url:
                url = url.replace(base_url, "/") # get relative links
            elif base_url not in url and (url[0] != '/'): # skip links that take to other sites
                continue
            links.append(url)
    return links
    
def populate_frontier(frontier, disallow_links, links):
    disallowed = {}
    for disallow_link in disallow_links:
        for link in links:
            if link == disallow_link or (disallow_link in link and disallow_links[disallow_link]): # if absolute or relative
                disallowed[link] = None
    for link in links:
        if link not in disallowed:
            frontier.append(link)        
        
def store_document(html, site, url):
    site = site.replace("/", "").replace(":", "").replace(".", "").replace("https", "").replace("www", "").replace("com", "")
    if url == "/":
        url = "root"
    else:
        url = url.replace("/", "_").replace("?","_").replace("=", "_").replace("%", "").replace("$", "")
    path = "./repository/{}/".format(site)
    if not os.path.exists(path):
        os.makedirs(path)
        
    file = open("{}{}.html".format(path, url), 'w', encoding="utf-16")
    
    soup = BeautifulSoup(html, 'html.parser')
    file.write(soup.prettify()) 
    file.close()
    
def crawler():
    for site in seeds:
        frontier = ["/"]
        visited_links = {}
        disallowed_links = permits_link(site)
        
        print("Site {}".format(site))
        while len(frontier) > 0:
            curr_link = frontier.pop(0)
            if curr_link not in visited_links:
                res = requests.get("{}{}".format(site, curr_link))
                time.sleep(1) # to avoid timeout
                html = res.text
                links = get_links(html, site)
                store_document(html, site, curr_link)
                # process html page: 
                #   Word occurrences
                print("In {} Links: {}".format(curr_link, len(links)))
                populate_frontier(frontier, disallowed_links, links)
                visited_links[curr_link] = None
                if len(visited_links) >= MAX_LINKS:
                    break
        print("TOTAL VISITED LINKS: {}".format(len(visited_links)))
        print("-------------------------------------")   
if(__name__ == "__main__"):
    MAX_LINKS = 1000
    seeds = ["https://www.cbs.com/", "https://www.pokebip.com/", "https://ja.wikipedia.org/"]
    crawler()