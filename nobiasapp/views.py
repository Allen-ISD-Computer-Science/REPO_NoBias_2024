from django.shortcuts import render
from nlpFiles.getTextFromWeb import polarityRating, highRatedSent, getTitle, webScrape
from nlpFiles.detectionInText import biasInText, justSents
from .forms import SubmitLinkForm, SubmitTextBoxForm
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
# def submitLink(request):
#     if request.method == 'POST':
#         form = SubmitLinkForm(request.POST)
#         if form.is_valid():
#             link_object = form.save()  # This saves the link to the database
#             thisVar = link_object.link  # Access the link and store it in thisVar
#             # You can now use thisVar for other Python code
#             paragraph = []
#             polarityRating(paragraph, thisVar)
#             highValuedList = highRatedSent(paragraph)
#             # Redirect or render a success page
#             return render(request, 'successPage.html', {'thisVar': paragraph, "highValuedList": highValuedList})
#     else:
#         form = SubmitLinkForm()

#     return render(request, 'submitLink.html', {'form': form})

def aboutus(request):
    return render(request, 'aboutus.html')
def tech(request):
    return render(request, 'tech.html')

def home(request):
    if request.method == 'POST':
        link_form = SubmitLinkForm(request.POST)
        text_form = SubmitTextBoxForm(request.POST)
        
        if link_form.is_valid():
            link_object = link_form.save()
            weblink = link_object.link
            paragraph = []
            pageSource = webScrape(weblink)
            title = getTitle(pageSource)
            polarityRating(paragraph, pageSource)
            return render(request, 'successPage.html', {'thisVar': paragraph, "sentences": zip(paragraph[2], paragraph[1]),'title': title, "biasperc": paragraph[0][0], }) #Redirects to successpage when a link is submitted
        
        elif text_form.is_valid():
            text_object = text_form.save()
            sentences = biasInText(str(text_object))
            justSent = justSents(str(text_object))
            combined = zip(sentences, justSent)
            # Do something with the text form submission
            return render(request, 'textPage.html', {'sentences': combined}) #Redirects to the successpage when text is submitted
        
    else:
        link_form = SubmitLinkForm()
        text_form = SubmitTextBoxForm()

    return render(request, './newPage.html', {'link_form': link_form, 'text_form': text_form})
