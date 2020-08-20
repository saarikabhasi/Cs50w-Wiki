from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.core.files import File
from . import util,forms
from random import choice


form = forms.NewSearchForm()


def index(request):

    '''
        display all the encyclopedia entries from disk

        steps:
        1. get all entries from list_entries() function of util.py
        2. redirect to index.html with entries for displaying the list. 
    '''
    entries =util.list_entries()

    return render(request, "encyclopedia/index.html", {
        "entries":entries ,
        "form":form
    })


def get_page(request,title):

    '''
        redirect to given title - encyclopedia page
        steps:
        1. get page contents from get_entry of util.py
        2. redirect to titlepage.html if content is found
        3. if content not found, redirect to error.html 

    '''
    page = util.get_entry(title)

    if page is None:
        # no page found 
        return render(request,"encyclopedia/error.html",{
            "form":form
        }) 
    
    # page found 
    return render(request,"encyclopedia/titlepage.html",{
        'title': title, 
        'content': page,
        "form":form,

    })




def get_search_query(request):
    '''
        this function handles the search request. 

        steps:
        1. get search query
        2. if exact match found for given query redirect to that page
        3. if not show list of all possible entries for that query

    '''
    if request.method == "GET":
        form = forms.NewSearchForm(request.GET)
      
        if form.is_valid():
            searchquery = form.cleaned_data["search"].lower()
            all_entries = util.list_entries()
            
       
            files=[filename for filename in all_entries if searchquery in filename.lower()]
    

            if len(files) == 0:

                '''
                    no matching filename found for the search query

                    So display "no results found"
                '''
                return render(request,"encyclopedia/search_results.html",{
                    'error' : "No results found",
                    "form":form
                })

            
            elif len(files) == 1 and files[0].lower() == searchquery:
                '''
                    found one matching filename for the search query 
                    and search query is same as entry page title. 

                    So redirect to get_page to display the page

                '''
                title = files[0]
                return get_page(request, title)

            
            else: 
                '''
                    multiple entry names found for query

                    steps:
                    1. traverse through the list of title names, 
                        and see if any title name is same search query 
                    2. if a match found redirect to get_page to display the page
                    3. if no match found redirect to search_results.html with list of all matching entries. 
                '''
                title = [filename for filename in files if searchquery == filename.lower()]

                if len(title)>0:
                    return get_page(request, title[0])
                else:
                    return render(request,"encyclopedia/search_results.html",{
                        'results':files,
                        "form":form

                    })

        else:
            # not a valid request
            return index(request)


    return index(request)


def new_page(request):
    '''
        create new page
        steps:

        1. get page title and body from NewPageForm
        2. check if the page title already exists in disk
        3. if page title exists- display error message
        4. if new page title - save new page and redirect to get_page with title name
    '''
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
            body = create_form.cleaned_data["body"]


            all_entries = util.list_entries()
            for filename in all_entries:
                if title.lower()== filename.lower():
                    create_form = forms.NewPageForm()
                    error_message="Page exists with the title '%s'. \n please try again with different title!" %filename
                    return render(request, "encyclopedia/create_page.html",{
                        "form":form,
                        "create_form":create_form,
                        "error":error_message
                        

                    })

            util.save_entry(title,body)
            return get_page(request, title)

        else:
            
            return render(request, "encyclopedia/create_page.html",{
            "form":form,
            "create_form":create_form

        })




def edit_page(request):
    '''
        edit page - pre-populate with page name and content
        
        steps:

        1. get page name from form and content from get_entry of util.py
        2. create a edit form object with initial value set as pagename and markdown content
        3. render to edit_page html file with pre-populated information.   

    '''
    pagename = request.POST.get("edit")

    content = util.get_entry(pagename)
    
    edit_form = forms.EditPageForm(initial={'pagename': pagename, 'body':content})
    if edit_form.is_valid():

        return render (request, "encyclopedia/edit_page.html",{
                "title": pagename,
                "form":form,
                "edit_form":edit_form
            
                

            })
    else:
        return render (request, "encyclopedia/edit_page.html",{
                "title": pagename,
                "form":form,
                "edit_form":edit_form        

        })
        

def save_page(request):
    '''
        save the edited page

        steps:
        1. get page name and markdown content from form
        2. save entry by calling save_entry function from util.py with page name and content.
        3. redirect to get_page function 

    '''
    edit_form = forms.EditPageForm(request.POST)

    if edit_form.is_valid():

        pagename = edit_form.cleaned_data["pagename"]
        content = edit_form.cleaned_data["body"]
        
        val = util.save_entry(pagename,content)

        return get_page(request, pagename)

    else:
        return render (request, "encyclopedia/edit_page.html",{
                "form":form,
                "edit_form":edit_form
            
        })


def random_page(request):

    '''
        display a random page from list_entries of util.py

    '''
    return get_page(request,choice( util.list_entries()))
