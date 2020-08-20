from django import forms

#search form
class NewSearchForm(forms.Form):
    search = forms.CharField(label="Search",required= False,
    widget= forms.TextInput
    (attrs={'placeholder':'Search Encyclopedia'}))

#new page
class NewPageForm(forms.Form):
    pagename = forms.CharField(label="Title",required = True,help_text="<p class='text-secondary'>Please refer <a class='text-info' href = https://docs.github.com/en/github/writing-on-github/basic-writing-and-formatting-syntax> GitHub’s Markdown guide</a> </p>",
    widget= forms.TextInput
    (attrs={'placeholder':'Enter Title','class':'col-sm-11','style':'bottom:1rem'}))

    body = forms.CharField(label="Markdown content",required= False, 
    widget= forms.Textarea
    (attrs={'placeholder':'Enter markdown content','class':'col-sm-11','style':'top:2rem'}))

#edit page
class EditPageForm(forms.Form):
    pagename = forms.CharField(label="Title",disabled = False,required = False,
    widget= forms.HiddenInput
    (attrs={'class':'col-sm-12','style':'bottom:1rem'}))
   
    body = forms.CharField(label="Markdown content",help_text="<p class='text-secondary'>Please refer <a class='text-info' href = https://docs.github.com/en/github/writing-on-github/basic-writing-and-formatting-syntax> GitHub’s Markdown guide</a> </p>",
    widget= forms.Textarea
    (attrs={"rows":20, "cols":80,'class':'col-sm-11','style':'top:2rem'}))

