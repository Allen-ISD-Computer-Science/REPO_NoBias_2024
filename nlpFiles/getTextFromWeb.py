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
    avgNegative = avgPol[0]
    avgPositive = avgPol[2]
    for tupIndex in range(len(polarityList)):
        if polarityList[tupIndex][2] * 100 > avgPositive:
            highList.append("+" + "Above average positive text")
            highList.append(paraList[tupIndex + 2])
        elif polarityList[tupIndex][0] * 100 > avgNegative:
            highList.append("-" + "Above average negative text")
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
    total = 0.00
    val = 0.00
    temp=''
    sentPolarityList = []
    for para in wantedText:
        sentences = sent_tokenize(para.text.strip())
        sentInPara = ""
        for sent in sentences:
            # tagged = nltk.pos_tag(word_tokenize(sent))
            if sent != "":
                # tagged = analyzer.polarity_scores(sent)
                tagged = {'pos': [], 'neu': [], 'neg': []}
                list.append(sent)
                temp = classifier(sent)[0]
                if temp["label"]=="Non-biased":
                    total += temp["score"]
                    val = temp["score"]
                else:
                    total += 1-temp["score"]
                    val = 1-temp["score"]
                if val < .40:
                    if 'pos' in tagged.keys():
                        tagged['pos'].append(0.00)
                    if 'neg' in tagged.keys():
                        tagged['neg'].append(val)
                    if 'neu' in tagged.keys():
                        tagged['neu'].append(0.00)
                elif val>=.40 and val<=.60:
                    if 'pos' in tagged.keys():
                        tagged['pos'].append(0.00)
                    if 'neg' in tagged.keys():
                        tagged['neg'].append(0.00)
                    if 'neu' in tagged.keys():
                        tagged['neu'].append(val)
                elif val>.60:
                    if 'pos' in tagged.keys():
                        tagged['pos'].append(val)
                    if 'neg' in tagged.keys():
                        tagged['neg'].append(0.00)
                    if 'neu' in tagged.keys():
                        tagged['neu'].append(0.00)
                totNegative += tagged["neg"][-1]
                totNeutral += tagged["neu"][-1]
                totPositive += tagged["pos"][-1]
                #Appends polarity of each sentence
                sentPolarityList.append((tagged["neg"][-1], tagged["neu"][-1], tagged["pos"][-1]))
                # Adds to the total polarity based on the key of the dictionary
                count += 1
        #Will stop once reaches the end of the article (Reuters)
        if "Reporting by" in sentInPara or "Get all the stories you need" in sentInPara:
            break
    
    rtotal = total/count
    list.insert(0, sentPolarityList)
    k=totPositive+totNegative+totNeutral
    scale_value=(2+(2*(100-k))/k)/2
    #In the end, the average polarity score of the article is added (variables for polarity meter)
    list1 = [str(round((totNegative*scale_value), 1)) + "%",str(round((totNeutral*scale_value), 1)) + "%",str(round((totPositive*scale_value), 1)) + "%"]
    #list1 = [str(l) + "%",str(k) + "%",str(m) + "%"]
    list1.append(round((1-rtotal),4))
    if count != 0:
        list.insert(0,list1)
 