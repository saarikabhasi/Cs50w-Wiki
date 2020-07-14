from django import template
from django.template.defaultfilters import stringfilter
from . import markdown_edit as md


register = template.Library()


@register.filter()
@stringfilter
def markdown1(value):

    md_object=md.markdown(value)
    return md_object.markdown_parser()

