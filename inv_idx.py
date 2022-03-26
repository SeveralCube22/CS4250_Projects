import glob
from bs4 import BeautifulSoup

def extract_words(text, word_list):
    words = text.lower().split()

    for word in words:
        word_list.append(word)

def inv_idx(dirname):
    files = glob.glob(dirname + '/*.html')
    idx = {}
    for fi in files:
        #print(fi)
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
                if word not in idx:
                    idx[word] = []
                if word not in idx[word]:
                    idx[word].append(fi)
    return idx

def search(dictionary):
    results = []
    userInput = input("Please enter your query: ")
    query = userInput.lower().split()
    for word in query:
        results.append(dictionary.get(word))
    print("Relevant results are: ", end="")
    print(results)
        
    

       
search(inv_idx("./repository/cbs"))
