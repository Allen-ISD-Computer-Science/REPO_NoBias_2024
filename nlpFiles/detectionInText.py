from transformers import AutoTokenizer, TFAutoModelForSequenceClassification, pipeline
from nltk.tokenize import sent_tokenize
from selenium import webdriver
import os
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def biasInText(userText) -> list:
    # Get models
    tokenizer = AutoTokenizer.from_pretrained("d4data/bias-detection-model")
    model = TFAutoModelForSequenceClassification.from_pretrained("d4data/bias-detection-model")
    classifier = pipeline('text-classification', model=model, tokenizer=tokenizer)
    resultList = []
    # Separate user text by sentences
    sentences = sent_tokenize(userText)
    for sent in sentences:
        resultList.append(f"{classifier(sent)[0]}")
    return resultList
def justSents(userText):
    return sent_tokenize(userText)
# print(biasInText("My name is Omer. I am testing the new bias detection in text. Hopefully it works."))