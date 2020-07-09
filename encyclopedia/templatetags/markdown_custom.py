from django import template
from django.template.defaultfilters import stringfilter

import re
import io

register = template.Library()


@register.filter()
@stringfilter



   
def markdown_parser(markdown):
    results=''
    print(markdown)
    count = 0
    print(type(markdown),markdown.strip())
    buf = io.StringIO(markdown)
    while True: 
        count += 1
  
        # Get next line from file 
        line = buf.readline() 
    
        # if line is empty 
        # end of file is reached 
        if not line: 
            break
        print("Current line is :",line)
        
        #heading    
        heading = re.compile("#+\s") 
        heading_matches = heading.search(line.strip())

        #hr dividing
        #hr = re.compile(r"(\*\*\*|___|---)(?=.?)") 
        hr =  re.compile(r"(?:\s*-{3,})+|(?:\s*\*{3,})+|(?:\s*_{3,})+")
        line=hr.sub(r"<hr>", line)

        #Bold
        #bold = re.compile("\*\*[\w+(\[|\^&+\-%\/=!\:>\'\"\])\s+]*\*\*")
        bold = re.compile(r"(\*\*|__)(?=\S)(.+?[*_]*)(?<=\S)\1")
        line= bold.sub(r"<p><strong>\2</strong><p>", line)
        print("Bold",line)
        
        #Italic
        italic = re.compile(r"(\*|_)(?=\S)(.+?[*_]*)(?<=\S)\1")
        line=italic.sub(r"<p><em>\2</em><p>", line)

        #Strikethrough
        strikethrough = re.compile(r"(~~)(?=\S)(.+?[*_]*)(?<=\S)\1")
        line=strikethrough.sub(r"<p><s>\2</s><p>", line)

        #list
        li = re.compile(r"(\-\s|\*\s)([\w+(\[|\^&+\-.',%\(/)=!\:>\'\"\s]*?)(?<=\n)",re.MULTILINE)
        #li =re.compile(r"^(\-\s|\*\s)([^.]*?)(?<=\n)")
        #li = re.compile(r"^\s*(\-\s|\*\s)([^.]*?)(?<=\n)")
        #li = re.compile(r"^\s*(\-\s|\*\s)([^\r]+?)(?<=\n)",re.m)
        #^\s*(\-\s|\*\s)([^\r]+?)(?<=\n)
        line= li.sub(r"<ul><li>\2</li></ul>",line)

        
        #Bold and italic
        
        
        

        if (heading_matches != None):
            tag = heading_matches.end()
            hashTagLen = heading_matches.end() - 1
            htmlTag = "h" + str(hashTagLen)
            content = line.strip()[(hashTagLen + 1):]
            results += "<" + htmlTag + ">" + content + "</" + htmlTag + ">"
        
        
        else:
            results+=line

    return results