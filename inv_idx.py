import glob
import csv
import codecs
from page_rank import get_html_format_ranks
from bs4 import BeautifulSoup, ResultSet

def extract_words(text, word_list):
    words = text.lower().split()

    for word in words:
        word_list.append(word)

def inv_idx(dirname, idx):
    files = glob.glob(dirname + '/*.html')
    for fi in files:
        with open(fi, 'rb') as f:
            words = []
            content = f.read()
            content = content.decode('utf-16')
            content = content.encode('utf-8')
            #print(content)
            soup = BeautifulSoup(content, 'html.parser')
            for script in soup(["script", "style"]):
                script.extract()
            text = soup.get_text()
            extract_words(text, words)
            for word in words:
                """ if word in idx:
                    if len(idx[word]) == 0:
                        idx[word].append([fi, 1])
                    else:   
                        for file in idx[word]:
                            if fi == file[0]:
                                file[1] += 1
                            else:
                                idx[word].append([fi, 1]) """
                if word not in idx:
                    idx[word] = []
                if fi not in idx[word]:
                    idx[word].append(fi)


def handleQuery(query, text):
    logic = ["&", "|"]
    score = 0
    carry = False
    isSymbol = False
    for symbol in logic:
        for word in query:
            if symbol == word:
                isSymbol = True
                break

    if not isSymbol:
        for term in query:
            score += checkWordInstances(text, term)
    else:
        count = 0
        while count < len(query):
            if query[count] == "&":
                if not carry:
                    count1 = checkWordInstances(text, query[count - 1])
                    count2 = checkWordInstances(text, query[count + 1])
                    score = min(count1, count2)
                    carry = True
                else:
                    count1 = checkWordInstances(text, query[count + 1])
                    score = min(count1, score)
            elif query[count] == "|":
                if not carry:
                    count1 = checkWordInstances(text, query[count - 1])
                    count2 = checkWordInstances(text, query[count + 1])
                    score = count1 + count2
                    carry = True
                else:
                    count1 = checkWordInstances(text, query[count + 1])
                    score += count1
            count += 1
    return score

def rankedBooleanSearch(query):
    print("Loading...")
    seed_names = ["cbs", "jawikipediaorg", "pokebip"]
    repo_names = ["./repository/cbs", "./repository/jawikipediaorg", "./repository/pokebip"]
    results = []

    pageranks = {}
    
    for seed in seed_names:
        rank = get_html_format_ranks(seed)
        pageranks[seed] = rank

    for repo in repo_names:
        files = glob.glob(repo + '/*.html')
        for fi in files:
            with open(fi, 'rb') as f:
                words = []
                content = f.read()
                content = content.decode('utf-16')
                content = content.encode('utf-8')
                soup = BeautifulSoup(content, 'html.parser')
                for script in soup(["script", "style"]):
                    script.extract()
                text = soup.get_text()
                extract_words(text, words)
                multiplier = 1
                
                split_file_name = fi.split("/")
                page_rank = float(pageranks[fi[2]][fi[3]].rstrip())
                rbs = handleQuery(query, words)
                
                overall_score =  rbs * page_rank
                print("Page rank", page_rank, "Ranked Boolean Score", rbs, "Overall", overall_score)
                results.append((result, fi))

    return(results)

def checkWordInstances(text, query):
    count = 0
    for word in text:
        if query == word:
            count += 1

    return count

def search():
    userInput = input("Please enter your query (Use the symbols '&' for AND '|' for OR): ")
    query = userInput.lower().split()
    results = rankedBooleanSearch(query)
    print("Finished!")
    results.sort()
    results.reverse()
    print(results)

        
    


search()
