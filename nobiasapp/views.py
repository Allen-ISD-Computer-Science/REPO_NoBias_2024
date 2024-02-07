from django.shortcuts import render
from nlpFiles.getTextFromWeb import pasteText
from .forms import SubmitLinkForm

def submitLink(request):
    if request.method == 'POST':
        form = SubmitLinkForm(request.POST)
        if form.is_valid():
            link_object = form.save()  # This saves the link to the database
            thisVar = link_object.link  # Access the link and store it in thisVar
            # You can now use thisVar for other Python code
            paragraph = []
            pasteText(paragraph, thisVar)
            # Redirect or render a success page
            return render(request, 'successPage.html', {'thisVar': paragraph})
    else:
        form = SubmitLinkForm()

    return render(request, 'submitLink.html', {'form': form})

def aboutus(request):
    return render(request, 'aboutus.html')
