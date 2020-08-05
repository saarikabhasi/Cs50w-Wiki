from django import template
from django.template.defaultfilters import stringfilter
#from . import markdown2 as md
from . import markdown2html as md

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):

    md_object = md.markdown(value)
  
    return md_object.markdown_parser()

