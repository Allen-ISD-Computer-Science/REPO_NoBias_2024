import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import urllib.request
from selenium import webdriver
import os
from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def pasteText(list, link):

    analyzer = SentimentIntensityAnalyzer()

    #Detect the users browser

    BROWSER = os.environ.get('BROWSER', 'chrome')

    supported_browsers = ['chrome', 'firefox', 'safari', 'edge']

    if BROWSER.lower() in supported_browsers:
        if BROWSER.lower() == 'chrome':
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')  
            driver = webdriver.Chrome(options=chrome_options)       
        elif BROWSER.lower() == 'firefox':
            firefox_options = webdriver.FirefoxOptions()
            firefox_options.add_argument('--headless')  
            driver = webdriver.Firefox(options=firefox_options) 
        elif BROWSER.lower() == 'safari':
            driver = webdriver.Safari()
            safari_options = webdriver.SafariOptions()
            safari_options.add_argument('--headless')  
            driver = webdriver.Safari(options=safari_options) 
        elif BROWSER.lower() == 'edge':
            driver = webdriver.Edge()
            edge_options = webdriver.EdgeOptions()
            edge_options.add_argument('--headless')  #
            driver = webdriver.Edge(options=edge_options) 
    else:
        print(f"Invalid or unsupported browser specified: {BROWSER}. Using the default browser.")
        driver = webdriver.Chrome()
        
    driver.get(link)

    # Wait for a while to allow JavaScript to execute (adjust the time as needed)
    driver.implicitly_wait(1)

    pageSource = driver.page_source
    #Using BS and strip_tags to get wanted text

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
                count += 1
        #Will stop once reaches the end of the article (Reuters)
        if "Reporting by" in sentInPara or "Get all the stories you need" in sentInPara:
            break
            
        #Will only paste sentences in para and polarity score if sentence is not empty
        if sentInPara != "":
            list.append(sentInPara)
            list.append("|")
            list.append(tagged)
            list.append("----")

    #In the end, the average polarity score of the article is added (variables for polarity meter)
    list.append(totNegative / count * 100)
    list.append(totNeutral / count * 100)
    list.append(totPositive / count * 100)
    


            
           

    
        
            


    