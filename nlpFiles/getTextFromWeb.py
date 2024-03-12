import nltk
import transformers
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification, pipeline
from nltk.tokenize import sent_tokenize, word_tokenize
import urllib.request
from selenium import webdriver
import os
from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

tokenizer = AutoTokenizer.from_pretrained("d4data/bias-detection-model")
model = TFAutoModelForSequenceClassification.from_pretrained("d4data/bias-detection-model")
classifier = pipeline('text-classification', model=model, tokenizer=tokenizer)

#!!!!! IMPORTANT !!!!!
# GOING TO REWORK BIAS DETECTION TO ACTUALLY DETECT BIAS, CONCERNING WHERE IT IS IN THE TEXT AND IT'S TYPE(BIAS TOWARDS WHO?, WHAT KIND OF BIAS?, ETC)
#!!!!! IMPORTANT !!!!!

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
    avgBias = avgPol[0]
    avgNon = avgPol[1]
    for tupIndex in range(len(polarityList)):
        if polarityList[tupIndex][0] == "Bias" and polarityList[tupIndex][1] * 100 > avgBias:
            highList.append(str(round(polarityList[tupIndex][1] * 100, 1)) + "% Biased: " + paraList[tupIndex + 2] )
    return highList
def polarityRating(list, link):
    analyzer = SentimentIntensityAnalyzer()

    wantedText = webScrape(link)
    # Declare variables for average polarity
    count = 0
    polarityCount = 0
    temp=''
    totBias = 0
    totNon = 0
    totPos = 0
    totNeg = 0
    sentBiasList = []
    for para in wantedText:
        sentences = sent_tokenize(para.text.strip())
        sentInPara = ""
        for sent in sentences:
            if sent != "":
                list.append(sent)
                temp = classifier(sent)[0]
                if temp['label'] == "Non-biased":
                    sentBiasList.append(("Non-biased", temp["score"]))
                    totBias += 1 - temp["score"]
                    totNon += temp["score"]
                else:
                    tagged = analyzer.polarity_scores(sent)
                    if tagged["pos"] > tagged['neg']:
                        sentBiasList.append(("Bias", temp["score"], "pos"))
                    else:
                        sentBiasList.append(("Bias", temp["score"], "neg"))
    
                    totBias += temp["score"]
                    totNon += 1 - temp["score"]
                    totPos, totNeg = totPos + tagged["pos"], totNeg + tagged["neg"]
                    polarityCount += 1
                # Adds to the total polarity based on the key of the dictionary
                count += 1
    list.insert(0, sentBiasList)
    overallList = [str(round(totBias / count * 100, 1)) + "%", str(round(totNon / count * 100, 1)) + "%", str(round(totPos / polarityCount * 100, 1)) + "%", str(round(totNeg / polarityCount * 100, 1)) + "%"]
    if count != 0:
        list.insert(0,overallList)
