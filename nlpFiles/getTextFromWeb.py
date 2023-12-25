#################################################################################
#         FILE:
#           getTextFromWeb.py
#       AUTHOR:
#           Omer Erturk
#  DESCRIPTION:
#           
#           
# DEPENDENCIES:
#           Created with Python 3.12.0(Python version)
#           nltk, urllib.request, requests, bs4, wordnet
#################################################################################
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# nltk.download('averaged_perceptron_tagger')
# from app import input_data
# print(input_data)
#TODO Get link from user input

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
        
        if "Reporting by" in sentInPara or "Funding for the" in sentInPara:
            break
        if sentInPara != "":
            list.append(sentInPara)
            list.append("|")
            list.append(tagged)
            list.append("----")
    list.append(f"{totNegative / count * 100}% Negative, {totNeutral / count * 100}% Neutral, {totPositive / count * 100}% Positive")


            
           

    
        
            


    