from django import forms

#search form
class NewSearchForm(forms.Form):
    search = forms.CharField(label="Search",required= False,
    widget= forms.TextInput
    (attrs={'placeholder':'Search Encyclopedia'}))

#new page
class NewPageForm(forms.Form):
    title = forms.CharField(label="Title",required= False,
    widget= forms.TextInput
    (attrs={'placeholder':'Enter Title','class':'col-sm-12','style':'bottom:1rem'}))

    body = forms.CharField(label="Content",required= False,
    widget= forms.Textarea
    (attrs={'placeholder':'Enter content', "rows":20, "cols":80,'class':'col-sm-12','style':'top:2rem'}))