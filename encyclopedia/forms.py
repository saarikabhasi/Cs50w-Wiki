from django import forms

#search form
class NewSearchForm(forms.Form):
    search = forms.CharField(label="Search",required= False,
    widget= forms.TextInput
    (attrs={'placeholder':'Search Encyclopedia'}))

#new page
class NewPageForm(forms.Form):
    pagename = forms.CharField(label="Title",required= False,
    widget= forms.TextInput
    (attrs={'placeholder':'Enter Title','class':'col-sm-12','style':'bottom:1rem'}))

    heading = forms.CharField(label="Page Heading",disabled=True,required= False, 
        widget= forms.TextInput (attrs={'class':'col-sm-12','style':'bottom:1rem'}))

    body = forms.CharField(label="Content",required= False,
    widget= forms.Textarea
    (attrs={'placeholder':'Enter content','class':'col-sm-12','style':'top:2rem'}))

#edit page
class EditPageForm(forms.Form):
    pagename = forms.CharField(label="Title",
    widget= forms.TextInput
    (attrs={'class':'col-sm-12','style':'bottom:1rem'}))
   
    heading = forms.CharField(label="Page Heading",disabled=True,required= False,
    widget= forms.TextInput
    (attrs={'class':'col-sm-12','style':'bottom:1rem'}))

    body = forms.CharField(label="Content",
    widget= forms.Textarea
    (attrs={"rows":20, "cols":80,'class':'col-sm-12','style':'top:2rem'}))

