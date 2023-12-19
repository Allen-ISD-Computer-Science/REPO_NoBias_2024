from django.shortcuts import render, redirect
from django.http import HttpResponse
from nlpFiles.getTextFromWeb import pasteText
from .forms import SubmitLinkForm
# Create your views here.

# def index(request):
#     this = []
#     pasteText(this)
#     return HttpResponse(this)
def submitLink(request):
    if request.method == 'POST':
        form = SubmitLinkForm(request.POST)
        if form.is_valid():
            
            link_object = form.save()  # This saves the link to the database
            thisVar = link_object.link  # Access the link and store it in thisVar
            # You can now use thisVar for other Python code
            this = []
            pasteText(this, thisVar)
            # Redirect or render a success page
            return render(request, 'successPage.html', {'thisVar': this})
    else:
        form = SubmitLinkForm()

    return render(request, 'submitLink.html', {'form': form})
def index(request):
    return render(request, 'index.html')