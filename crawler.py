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
    
if(__name__ == "__main__"):
    permits_link("https://www.pokebip.com")
    