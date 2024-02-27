import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import urllib.request
from selenium import webdriver
import os
from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def percentToInt(list):
    # Remove '%' from strings and convert to float
    data_without_percentages = [float(item.strip('%')) if isinstance(item, str) else item for item in list]

    # Convert floats to integers
    data_as_integers = [int(float_value) if isinstance(float_value, float) else int(float_value) for float_value in data_without_percentages]

    return(data_as_integers)


def webScrape(webLink):
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
        
    driver.get(webLink)

    # Wait for a while to allow JavaScript to execute (adjust the time as needed)
    driver.implicitly_wait(1)

    pageSource = driver.page_source
    #Using BS and strip_tags to get wanted text

    soupText = BeautifulSoup(pageSource, 'html.parser')
    wantedText = soupText.findAll("p")
    return wantedText

# def highRatedSentences(paraLink):
def highRatedSent(paraList):
    highList = []
    polarityList = paraList[1]
    avgPol = percentToInt(paraList[0])
    avgNegative = avgPol[0]
    avgPositive = avgPol[2]
    for tupIndex in range(len(polarityList)):
        if polarityList[tupIndex][2] * 100 > avgPositive:
            highList.append("*" * 30 + "Above average positive text" + "*" * 80)
            highList.append(paraList[tupIndex + 2])
        elif polarityList[tupIndex][0] * 100 > avgNegative:
            highList.append("*" * 30 + "Above average negative text" + "*" * 80)
            highList.append(paraList[tupIndex + 2])
    return highList
def polarityRating(list, link):
    analyzer = SentimentIntensityAnalyzer()

    wantedText = webScrape(link)
    
    # Declare variables for average polarity
    totNegative = 0
    totNeutral = 0
    totPositive = 0
    count = 0
    sentPolarityList = []
    for para in wantedText:
        sentences = sent_tokenize(para.text.strip())
        sentInPara = ""
        for sent in sentences:
            # tagged = nltk.pos_tag(word_tokenize(sent))
            if sent != "":
                tagged = analyzer.polarity_scores(sent)
                list.append(sent)
                totNegative += tagged["neg"]
                totNeutral += tagged["neu"]
                totPositive += tagged["pos"]
                #Appends polarity of each sentence
                sentPolarityList.append((tagged["neg"], tagged["neu"], tagged["pos"]))
                # Adds to the total polarity based on the key of the dictionary
                count += 1
        #Will stop once reaches the end of the article (Reuters)
        if "Reporting by" in sentInPara or "Get all the stories you need" in sentInPara:
            break
        
    list.insert(0, sentPolarityList)
    #In the end, the average polarity score of the article is added (variables for polarity meter)
    list1 = [str(round(totNegative / count * 100, 1)) + "%",str(round(totNeutral / count * 100, 1)) + "%",str(round(totPositive / count * 100, 1)) + "%"]
    
    list1.append(round(totNegative/ count * 100, 1) / (round(totNegative / count * 100, 1) + round(totPositive / count * 100, 1)))
    if count != 0:
        list.insert(0,list1)
 