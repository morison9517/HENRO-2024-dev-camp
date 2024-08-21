from django import forms

from django.shortcuts import render

class NewNikkiForm(forms.Form):
    title = forms.CharField(label="New Nikki")

# Create your views here.
def index(request):
    return render(request, "nikki/index.html",{
        "form":NewNikkiForm
    })

def comp(request):
    return render(request, "nikki/comp.html",{
        "comp":"comp"
    })
