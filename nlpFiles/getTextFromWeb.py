import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def pasteText(list, link):

    analyzer = SentimentIntensityAnalyzer()
    # Create a new instance of the Safari browser
    driver = webdriver.Safari()
    driver.get(link)

# Wait for a while to allow JavaScript to execute (adjust the time as needed)
    driver.implicitly_wait(1)

    # Now you can interact with the page using Selenium methods
    # For example, you can retrieve the page source
    pageSource = driver.page_source
    #Using BS and strip_tags to get the text I want

    soupText = BeautifulSoup(pageSource, 'html.parser')
    wantedText = soupText.findAll("p")
    
    # Declare variables for average polarity
    totNegative = 0
    totNeutral = 0
    totPositive = 0
    count = 0

    for para in wantedText:
        sentences = sent_tokenize(para.text.strip())
        sentInPara = ""
        for sent in sentences:
            # tagged = nltk.pos_tag(word_tokenize(sent))
            if sent != "":
                tagged = analyzer.polarity_scores(sent)
                sentInPara += " {0}".format(sent)
                # Adds to the total polarity based on the key of the dictionary
                totNegative += tagged["neg"]
                totNeutral += tagged["neu"]
                totPositive += tagged["pos"]
                count += 1

        #Will stop once reaches the end of the article (Reuters)
        if "Reporting by" in sentInPara:
            break
            
        #Will only paste sentences in para and polarity score if sentence is not empty
        if sentInPara != "":
            list.append(sentInPara)
            list.append("|")
            list.append(tagged)
            list.append("----")

    #In the end, the average polarity score of the article is added
    list.append(f"{totNegative / count * 100}% Negative, {totNeutral / count * 100}% Neutral, {totPositive / count * 100}% Positive")


            
           

    
        
            


    