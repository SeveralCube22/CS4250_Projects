import pandas as pd
import matplotlib.pyplot as plt

def create_data_frame(file):
    df = pd.read_csv(file, encoding="utf16")
    df.columns = df.columns.str.lstrip()
    df.sort_values(by=["NUM OCCURENCES"], ascending=False, inplace=True)
    return df

def create_ziph_data(df):
    rank = []
    pr = []
    currRank = 0
    N = 0
    for i, row in df.iterrows():
        N += row["NUM OCCURENCES"]
    
    prevOccur = -1
    for i, row in df.iterrows():
        currOccur = row["NUM OCCURENCES"]
        if prevOccur == -1:
            prevOccur = currOccur
        elif currOccur != prevOccur:    
            rank.append(currRank)
            pr.append(currOccur / N)
            currRank += 1 
            prevOccur = currOccur
    return rank, pr, "Rank", "Prob. of Occurences"

def create_heap_data(df):
    x, y = [], []
    tokens = 0
    unique_words = 0
    words = {}
    
    for i, row in df.iterrows():
        tokens += 1
        x.append(tokens)
        if row["WORDS"] not in words:
            unique_words += 1
            words[row["WORDS"]] = 0
        y.append(unique_words)
    return x, y, "Num Tokens", "Vocab. Size"

def graph(word_reports, titles, data):
    (fig, plots) = plt.subplots(1, 3, figsize=(15, 5))
    
    for i, file in enumerate(word_reports):
        df = create_data_frame(file)
        x, y, xlabel, ylabel = data(df)
        plots[i].plot(x, y)
        plots[i].title.set_text((titles[i]))
        plots[i].set_xlabel(xlabel)
        plots[i].set_ylabel(ylabel)
    plt.subplot_tool()
    plt.show()

if(__name__ == "__main__"):
    word_reports = ["./reports/words/cbs-report.csv", "./reports/words/pokebip-report.csv", "./reports/words/jawikipediaorg-report.csv"]
    titles = ["CBS", "Japanese Wiki", "PokeBip"]
    
    graph(word_reports, titles, create_ziph_data)
    graph(word_reports, titles, create_heap_data)
    
    
    