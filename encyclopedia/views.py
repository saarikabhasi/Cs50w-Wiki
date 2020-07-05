from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django import forms
from . import util



class NewSearchForm(forms.Form):
    search = forms.CharField(label="Search",required= False)
    # widget= forms.TextInput
    # (attrs={'placeholder':'Search Encyclopedia'}))
    
def index(request):
    form = NewSearchForm()
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form":form
    })

# redirect to page
def get_page(request,title):
    form = NewSearchForm()
    value = markdown_to_html(title)
    
    if value is None:
        return render(request,"encyclopedia/error.html",{
            "form":form
        })
        
    
    return render(request,"encyclopedia/titlepage.html",{
        'title': title, 
        'content': value,
        "form":form
    })

# markdown to html conversion
def markdown_to_html(title):
    value = util.get_entry(title)

    if value is None:
        return None
    return value

#search a query
def get_search_query(request):
    #import pdb; pdb.set_trace()
    if request.method == "GET":
        form = NewSearchForm(request.GET)
      
        if form.is_valid():
            searchquery = form.cleaned_data["search"].lower()
            all_entries = util.list_entries()
            
       
            files=[filename for filename in all_entries if searchquery in filename.lower()]
            
            if len(files)>1:
                return render(request,"encyclopedia/search_results.html",{
                    'results':files,
                    "form":form

                })
            elif len(files) == 0:
                return render(request,"encyclopedia/search_results.html",{
                    'error' : "No results found",
                    "form":form
                })
            else:
                title = files[0]
                
                value = markdown_to_html(title)
                if value is None:
                    return render(request,"encyclopedia/error.html",{
                    "form":form
                    })
        
                
                return render(request,"encyclopedia/titlepage.html",{
                    'title': title, 
                    'content': value,
                    "form":form
                })

        else:
            return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form":form
        })


    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form":form
    })

# new page

def new_page(request):
    return index()
#show random page
def random_page(request):
    return index()

