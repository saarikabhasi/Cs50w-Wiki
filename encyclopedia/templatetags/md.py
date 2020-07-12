from django import template
from django.template.defaultfilters import stringfilter
from . import markdown_edit as md


register = template.Library()


@register.filter()
@stringfilter
def markdown(value):

    mdp=md.markdown(value)
    return mdp.markdown_parser(value)

