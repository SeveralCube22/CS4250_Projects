import requests
import time
import os
from collections import Counter
from bs4 import BeautifulSoup
import json
import re
import detect

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
            if base_url in url:
                url = url.replace(base_url, "/") # get relative links
            elif base_url not in url and (url == "" or url[0] != '/'): # skip links that take to other sites
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

def extract_words(text, word_list):
    words = text.lower().split()

    for word in words:
        word_list.append(word)

def create_word_dictionary(word_list):
    word_dictionary = {}

    for word in word_list:
        if word in word_dictionary:
            word_dictionary[word] += 1
        else:
            word_dictionary[word] = 1
            
    return word_dictionary

def clean_words(word_list):
    cleaned_list = []
    for word in word_list:
        symbols = "!@#$%^&*()_-+={[}]|\;:\"<>?/., "
 
        for i in range(len(symbols)):
            word = word.replace(symbols[i], '')
 
        if len(word) > 0:
            cleaned_list.append(word)
    return cleaned_list
        
def store_document(html, site, url):
    path = "./repository/{}/".format(site)
    if not os.path.exists(path):
        os.makedirs(path)
        
    file = open("{}{}.html".format(path, url), 'w', encoding="utf-16")
    
def store_out_links(site, url, outlinks):
    path = "./reports/links/"
    if not os.path.exists(path):
        os.makedirs(path)
    
    write_file = "{}{}-{}.csv".format(path, site, "report")
    mode = 'a' if os.path.exists(write_file) else 'w'
    
    file = open(write_file, mode, encoding="utf-16")
    if mode == 'w':
        file.write("LINKS, NUM OUT LINKS, OUT LINKS\n")
    
    formatted_links = ['"{}"'.format(l) for l in outlinks]
    file.write("{}, {}, {}\n".format(url, len(outlinks), "[" + ",".join(formatted_links) + "]"))
    
def store_word_report(site, word_dictionary):
    path = "./reports/words/"
    if not os.path.exists(path):
        os.makedirs(path)
    
    write_file = "{}{}-{}.csv".format(path, site, "report")
    mode = 'a' if os.path.exists(write_file) else 'w'
    
    file = open(write_file, mode, encoding="utf-16")
    if mode == 'w':
        file.write("\ufeff")
        file.write("WORDS, NUM OCCURENCES\n")
        file = open(write_file, 'a', encoding="utf-16")
        
    for word in word_dictionary:
        file.write("{}, {}\n".format(word, word_dictionary[word]))

def get_html_text_chunk(text):
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def crawler():
    for site in seeds:
        listofwords = []
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
                soup = BeautifulSoup(html, "html.parser")
                for script in soup(["script", "style"]):
                    script.extract()
                text = soup.get_text()  
                if(not detect.is_lang(seeds[site], get_html_text_chunk(text))):
                    continue
                links = get_links(html, site)
                formatted_site = site.replace("/", "").replace(":", "").replace(".", "").replace("https", "").replace("www", "").replace("com", "")
                if curr_link == "/":
                    formatted_link = "root"
                else:
                    formatted_link = curr_link.replace("/", "_").replace("?","_").replace("=", "_").replace("%", "").replace("$", "").replace(":", "")
                store_document(html, formatted_site, formatted_link)
                store_out_links(formatted_site, curr_link, links)
                extract_words(text, listofwords)
                # process html page: 
                #   Word occurrences
                print("In: {} Visited: {} Links: {}".format(curr_link, len(visited_links), len(links)))
                populate_frontier(frontier, disallowed_links, links)
                visited_links[curr_link] = None
                if len(visited_links) >= MAX_LINKS:
                    print("Finished crawling for domain")
                    listofwords = clean_words(listofwords)
                    break
        print("TOTAL VISITED LINKS: {}".format(len(visited_links)))
        print("-------------------------------------")   
        
if(__name__ == "__main__"):
    MAX_LINKS = 1000
    seeds = {"https://www.cbs.com/": "en", "https://www.pokebip.com/": "fr", "https://ja.wikipedia.org/": "ja"}
    crawler()
    