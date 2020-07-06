from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.core.files import File
from . import util,forms
from random import choice


form = forms.NewSearchForm()

def index(request):
    entries =util.list_entries()
    print(entries)
    return render(request, "encyclopedia/index.html", {
        "entries":entries ,
        "form":form
    })

# redirect to page
def get_page(request,title):
    value = util.get_entry(title)
    print("get page",title)
    if value is None:
        return render(request,"encyclopedia/error.html",{
            "form":form
        }) 
    
    return render(request,"encyclopedia/titlepage.html",{
        'title': title, 
        'content': value,
        "form":form
    })



#search a query
def get_search_query(request):
    #import pdb; pdb.set_trace()
    if request.method == "GET":
        form = forms.NewSearchForm(request.GET)
      
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
                return get_page(request, title)


        else:
            return index(request)


    return index(request)

# new page
def new_page(request):
    print(request.method)
    if request.method == "GET":
        create_form= forms.NewPageForm()
        return render(request, "encyclopedia/create_page.html",{
            "form":form,
            "create_form":create_form

        })
    else:
        create_form = forms.NewPageForm(request.POST)
        if create_form.is_valid():
            
            title = create_form.cleaned_data["pagename"]
            heading = "#" + title
            body = create_form.cleaned_data["body"]


            all_entries = util.list_entries()
            for filename in all_entries:
                if title.lower()== filename.lower():
                    create_form = forms.NewPageForm()
                    return render(request, "encyclopedia/create_page.html",{
                        "form":form,
                        "create_form":create_form,
                        "error":"page exists"
                        

                    })

            util.save_entry(title,body)
            return get_page(request, title)
        else:
            return render(request, "encyclopedia/create_page.html",{
            "form":form,
            "create_form":create_form

        })



#edit page
def edit_page(request):

    pagename = request.POST.get("edit")

    content = util.get_entry(pagename)
    
    print(request.POST)
    #request.POST.get("heading") = "#" + title
    heading = "#" + pagename

    edit_form = forms.EditPageForm(initial={'pagename': pagename, 'body':content, 'heading':heading})
    if edit_form.is_valid():
        print(edit_form.cleaned_data)
        return render (request, "encyclopedia/edit_page.html",{
                "form":form,
                "edit_form":edit_form
            
                

            })
    else:
        return render (request, "encyclopedia/edit_page.html",{
                "form":form,
                "edit_form":edit_form
            
                

        })
def save_page(request):
    edit_form = forms.EditPageForm(request.POST)
    if edit_form.is_valid():
        pagename = edit_form.cleaned_data["pagename"]
        content = edit_form.cleaned_data["body"]
        
        heading = "#" + pagename +'\n'

        val = util.save_entry(pagename,content)
        return get_page(request, pagename)
    else:
        return render (request, "encyclopedia/edit_page.html",{
                "form":form,
                "edit_form":edit_form
            
                

        })

#show random page
def random_page(request):
    return get_page(request, choice( util.list_entries()))
