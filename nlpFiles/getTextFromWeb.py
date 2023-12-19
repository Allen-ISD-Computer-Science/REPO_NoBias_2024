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
# from app import input_data
# print(input_data)
#TODO Get link from user input

def pasteText(list, link):
    # Create a new instance of the Safari browser
    driver = webdriver.Safari()
    driver.get(link)

# Wait for a while to allow JavaScript to execute (adjust the time as needed)
    driver.implicitly_wait(2)

    # Now you can interact with the page using Selenium methods
    # For example, you can retrieve the page source
    pageSource = driver.page_source
    #Using BS and strip_tags to get the text I want

    soupText = BeautifulSoup(pageSource, 'html.parser')
    wantedText = soupText.findAll("p")
    for para in wantedText:
        sentences = sent_tokenize(para.text.strip())
        sentInPara = ""
        for sent in sentences:
            sentInPara += " {0}".format(sent)
        list.append(sentInPara)
        list.append("----")
            
           

    
        
            


    