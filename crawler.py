from bs4 import BeautifulSoup
import requests

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
            if url == '/': # skip root
                continue
            if base_url in url:
                url = url.replace(base_url, "/") # get relative links
            elif base_url not in url and (url[0] != '/'): # skip links that take to other sites
                continue
            links.append(url)
    return links
    
def populate_frontier(frontier, disallow_links, links):
    for disallow_link in disallow_links:
        for link in links:
            if disallow_links[disallow_link]: # not absolute
                pass
        

def store_document(html, url):
    pass

def crawler():
    for site in seeds:
        res = requests.get(site).text
        links = get_links(res, site)
        frontier = []
        visited_links = {"/"}
        # store text from base site
        
        # process each link in frontier
        
        
    
if(__name__ == "__main__"):
    seeds = ["https://www.cbs.com/", "https://www.pokebip.com/", "https://ja.wikipedia.org/"]
    print(permits_link(seeds[0]))