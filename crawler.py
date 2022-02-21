from bs4 import BeautifulSoup
import requests

def permits_link(url):
    resp = requests.get("{}/robots.txt".format(url))
    data = resp.text.split("\n")

    disallow_links = {}
    for line in data:
        if "Disallow" in line:
            link = line.split(":")[1].split()
            disallow_links[link[0]] = None
    return disallow_links

def get_links(html, base_url):
    links = []
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.find_all('a'):
        if link.has_attr("href"):
            url = link["href"]
            if url == '/' or url == '#': # skip root
                continue
            if base_url in url:
                url = url.replace(base_url, "/") # get relative links
            elif base_url not in url and (url[0] != '/' or url[0] != '#'): # skip links that take to other sites
                continue
            links.append(url)
    return links
    
def crawler():
    frontier = []
    for site in seeds:
        links = get_links(site)
        # add links to frontier
    
if(__name__ == "__main__"):
    seeds = ["https://www.cbs.com/", "https://www.pokebip.com/", "https://ja.wikipedia.org/"]
    print(get_links(requests.get(seeds[1]).text, seeds[1]))