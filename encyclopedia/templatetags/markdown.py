from django import template
from django.template.defaultfilters import stringfilter

import re



class markdown(object):
  
    def __init__(self,value):
        self.results='' #Stores final result
        self.previous_ul_linespace = 0 # variable that stores previous line's space of un ordered list
        self.markdown_string = value # Markdown string to be converted to HTML
        self.ol_current_line_space = 0 # variable that stores current line's space of ordered list
        self.previous_ol_linespace  = 0 # variable that stores previous line's space of ordered list
        
        # variables used by lists
        self.list_variable = {
            "ul":{
                "ultag_is_open":False, # If True, a Unordered list is open. 
                "sub_ultag_is_open":False, # If True, Nested Unordered list is open.
                "number_of_list": 0 # Stores number of Sub Unordered List
                },
            "ol":{
                "ol_tag_is_open":False, # If True, a ordered list is open. 
                "sub_oltag_is_open":False, # If True, Nested ordered list is open.
                "number_of_list":0 # Stores number of Sub ordered List
            }
        }
    

        # Regex pattern 
        self.patterns = {
            "heading" :"#+\s", #heading
            "ul":r"^\s*(\-|\*|\+\s)([\w*\W*\d*\D*\s*\S*]+?)(?<=$)", #unordered list
            "ol":r"^\s*(\d+)(\.|\))\s*(.+?)(?<=$)",  # ordered list
            "hr":r"(?:\s*-{3,})+|(?:\s*\*{3,})+|(?:\s*_{3,})+", #HR
            "bold":r"(\*\*|__)(?=\S)(.+?[*_]*)(?<=\S)\1", #bold
            "italic" :r"(\*|_)(?=\S)(.+?[*_]*)(?<=\S)\1", #italic
            "bold_and_italic":r"\*\*\*(.+?)\*\*\*",
            "strikethrough" :r"(~~)(?=\S)(.+?[*_]*)(?<=\S)\1", #strikethrough
            "single_line_fenced_code":r"\s*(`{3})+([\w*\W*\d*\D*\s*\S*]+?)(`{3})+(?<=$)",#Single line fenced code block
            "multi_line_fenced_code": r"\s*(`{3})",#Muliple line fenced code block
            "link_text":r"(\[(.*?)\])(\((.*?)\))", #Links
            "image_links":r"(!\[(.*?)\])(\((.*?)\))", #images
            "inline_code":r"\`([\w*\W*\d*\D*\s*\S*]+?)\`", #inline-code
            "automatic_hyperlinks":r"(((http(s)*:\/\/){1}|(www\.{1}))(.*))", #web link

        }
        # HTML tags 
        self.substitute_patterns ={
            
            "ul_li_tag":r"\n<ul>\n<li>\2</li>\n", # new un ordered list tag
            "li_tag_of_ul":r"\n<li>\2</li>\n", #li tag of un-ordered list
            "ol_li_tag":r"\n<ol start = \1>\n<li>\3</li>\n",#new ordered list
            "li_tag_of_ol":r"\n<li>\3</li>\n",  #li tag of ordered list
            "hr_tag" : r"\n<hr>\n", #line break tag 
            "bold":r"<strong>\2</strong>", #bold
            "italic":r"<em>\2</em>", #italic
            "strikethrough":r"<s>\2</s>", #strikethrough
            "bold_and_italic":r"<strong><em>\1</em></strong>", #Bold and italic
            "single_line_fenced_code":r"<pre><code>\2</code></pre>",# Single line fenced code
            "link_text":r"<a href ='\4'>\2</a>", #links
            "image_links":r"<img src='\4' alt ='\2'>", #Images
            "inline":r"<code>\1</code>", #inline code
            "automatic_hyperlinks":r"<a href ='\1'>\1</a>", #web link
            

        }

    # close all the opened tags of list.The variable type, can be UL or OL
    def close_list(self,line,type):
        
        if type in self.list_variable.keys():
            for var in self.list_variable[type]:

                if self.list_variable[type][var]== True:    
                    line = "</" + type + ">"+'\n'+line
                    self.list_variable[type][var] = False

            if self.list_variable[type]["number_of_list"] >=1:
                for _ in range(int(self.list_variable[type][var])):
                    closingTags = "</" + type + ">"+'\n'


                line = closingTags + line
                self.list_variable[type]["number_of_list"] =0  
        return line   
        
         

    #ordered list
    def ol_list(self,line,ordered_list):
        
      # When a line matches the ol pattern,  
      # Calculate the preceeding space of the line.
       
        current_ol_line_space = len(line)-len(line.lstrip())

        # If the line space is same as previous ordered list line space . 
        # Then the line is considered as same level the previous ol list.

        if current_ol_line_space-self.previous_ol_linespace == 0 : 
            # First Ordered list
            if self.list_variable["ol"]["ol_tag_is_open"] == False:
                
                line = ordered_list.sub(self.substitute_patterns["ol_li_tag"],line)
                self.list_variable["ol"]["ol_tag_is_open"] = True
                self.previous_ol_linespace = current_ol_line_space

            else:
                line = ordered_list.sub(self.substitute_patterns["li_tag_of_ol"],line)

        # If the preceeding line space is between 3 and 6 (including) 
        # Then the line could be part of nested ol.
        # So this function checks if already a root ol tag and/ or sub ol is open, 
        # IF both are True then it checks for number of opened sub list
        # if there is atleast one sub list then a new ol is created, else it just appends to previous level ol list.

        elif 3<=current_ol_line_space-self.previous_ol_linespace <=6  : 

            if self.list_variable["ol"]["ol_tag_is_open"] == True: #not a first ordered list

                if self.list_variable["ol"]["sub_oltag_is_open"] :
                    if self.list_variable["ol"]["number_of_list"] >= 1:
                        line = ordered_list.sub(self.substitute_patterns["ol_li_tag"],line) 
                    line = ordered_list.sub(self.substitute_patterns["li_tag_of_ol"],line) 
                else:
                   
                    self.list_variable["ol"]["sub_oltag_is_open"] = True
                    self.list_variable["ol"]["number_of_list"] +=1
                    line = ordered_list.sub(self.substitute_patterns["ol_li_tag"],line)
            else:

                line = ordered_list.sub(self.substitute_patterns["ol_li_tag"],line)
                self.list_variable["ol"]["ol_tag_is_open"] = True 
            self.previous_ol_linespace = current_ol_line_space

        # if the line space between previous and current line is between -6 and -3, 
        # It could of same level as the root or a new ol list
        # before appending new ol, closes all the opened list and creates new ol tag
        elif -6<=current_ol_line_space-self.previous_ol_linespace<=-3:
            oltags =""
           
            if self.list_variable["ol"]["number_of_list"] >=1:

                for _ in range(int(self.list_variable["ol"]["number_of_list"])-1):
                    oltags = "</ol>"
  
                self.list_variable["ol"]["number_of_list"] =0  

            if self.list_variable["ol"]["ol_tag_is_open"] == True: #not a first ordered list

                if self.list_variable["ol"]["sub_oltag_is_open"] :

                    line = ordered_list.sub(self.substitute_patterns["li_tag_of_ol"],line) 

                else:
                   
                    self.list_variable["ol"]["sub_oltag_is_open"] = True
                    self.list_variable["ol"]["number_of_list"] +=1
                    line = ordered_list.sub(self.substitute_patterns["ol_li_tag"],line)
           
                    
                line =line+oltags
            else:

                line = ordered_list.sub(self.substitute_patterns["ol_li_tag"],line)
                self.list_variable["ol"]["ol_tag_is_open"] = True 
            self.previous_ol_linespace = current_ol_line_space

        else:
            # if the lines does not fall in any of the above categories , it is considered as a entirely new ol list
            if self.list_variable["ol"]["ol_tag_is_open"] == True: 
                line =self.close_list(line,"ol")

            line = ordered_list.sub(self.substitute_patterns["ol_li_tag"],line)
            self.list_variable["ol"]["ol_tag_is_open"] = True #set ol tag to open
            self.previous_ol_linespace = current_ol_line_space

        return line   

   


    #unordered list
    def list(self,line,unordered_list):
        
        # When a line matches the ul pattern,  
        # Calculate the preceeding space of the line.
        currentlinespace = len(line)-len(line.lstrip())

        # If the line space is same as previous unordered list line space . 
        # Then the line is considered as same level the previous ul list.
        if currentlinespace-self.previous_ul_linespace == 0: 
            
            if self.list_variable["ul"]["ultag_is_open"] == True:                       
                line = unordered_list.sub(self.substitute_patterns["li_tag_of_ul"],line)

            else:
                #first li in the list
                line = unordered_list.sub(self.substitute_patterns["ul_li_tag"],line)
                self.list_variable["ul"]["ultag_is_open"] = True #set ul tag to open
                self.previous_ul_linespace = currentlinespace

        #nested list  
        # if the line space between previous and current line is between 2 and 5, 
        # It could be a nested list
        # So this function checks if already a root ul tag and/ or sub ul is open, 
        # IF both are True then it checks for number of opened sub list
        # if there is atleast one sub list then a new ul is created, else it just appends to previous level ul list.
        elif 2<=currentlinespace-self.previous_ul_linespace <=5: 
           
            if self.list_variable["ul"]["ultag_is_open"] == True: #not a first li in the list

                if self.list_variable["ul"]["sub_ultag_is_open"] :
                    if self.list_variable["ul"]["number_of_list"] >= 1:
                        line = unordered_list.sub(self.substitute_patterns["ul_li_tag"],line) 
                    line = unordered_list.sub(self.substitute_patterns["li_tag_of_ul"],line) 
                else:
                   
                    self.list_variable["ul"]["sub_ultag_is_open"] = True
                    self.list_variable["ul"]["number_of_list"] +=1
                    line = unordered_list.sub(self.substitute_patterns["ul_li_tag"],line)
            else:

                line = unordered_list.sub(self.substitute_patterns["ul_li_tag"],line)
                self.list_variable["ul"]["ultag_is_open"] = True 
            self.previous_ul_linespace = currentlinespace

        # nested new list
        # if the lines does not fall in any of the above categories , it is considered as a entirely new ul list
        else: 

            #close all previous nested list
            line =self.close_list(line,"ul")

            line = unordered_list.sub(self.substitute_patterns["ul_li_tag"],line)
            self.list_variable["ul"]["ultag_is_open"] = True #set ul tag to open
            self.previous_ul_linespace = currentlinespace

        return line   
                         

    #heading
    def heading(self,heading_matches,line):
        
        tag = heading_matches.end()
        hashTagLen = heading_matches.end() - 1
        htmlTag = "h" + str(hashTagLen)
        content = line.strip()[(hashTagLen + 1):]
        line = "<" + htmlTag + ">" + content + "</" + htmlTag + ">"+'\n'
        return line
    
    #HR tag
    def hr(self,hr,line):
        line = hr.sub(self.substitute_patterns["hr_tag"] ,line)
        return line
    
    #Bold
    def bold(self,bold,line):
        line = bold.sub(self.substitute_patterns["bold"],line)
        return line

    #Italic
    def italic(self,italic,line):
        line = italic.sub(self.substitute_patterns["italic"],line)
        return line

    #Strikethrough
    def strikethrough(self,strikethrough,line):
        line = strikethrough.sub(self.substitute_patterns["strikethrough"],line)
        return line

    #Bold and italic
    def bold_and_italic(self,bold_and_italic,line):
        line = bold_and_italic.sub(self.substitute_patterns["bold_and_italic"],line )
        return line
    #code
    def single_line_code(self,code,line):
        line = code.sub(self.substitute_patterns["single_line_fenced_code"],line)
        return line

    #image links
    def image_links(self,img, line):
        line = img.sub(self.substitute_patterns["image_links"],line)
        return line

    #links
    def link_text(self,link, line):
        line = link.sub(self.substitute_patterns["link_text"],line)
        return line
    
   
    #inline code
    def inline(self,inline_code,line):
        line = inline_code.sub(self.substitute_patterns["inline"],line)
        return line

    #web links
    def automatic_hyperlinks(self,automatic_hyperlinks, line):
        line = automatic_hyperlinks.sub(self.substitute_patterns["automatic_hyperlinks"],line)
        return line

    # markdown to html main function
    def markdown_parser(self):
        codeline =""
        lines =""
        single_line_fenced_code_active = False
        multi_line_fenced_code_active = False
        line_tobe_checked_for_heading = ""
        heading_check =False
        
        
       
        for line in self.markdown_string.splitlines():
            multi_line_code_space = 0
            
            single_line_fenced_code = re.compile(self.patterns["single_line_fenced_code"],re.MULTILINE)

            #check if the line has single line code block
            if single_line_fenced_code.search(line) and multi_line_fenced_code_active ==False:
                single_line_fenced_code_active == True
                codeline = self.single_line_code(single_line_fenced_code,line)
            else:
                multiple_line_fenced_code = re.compile(self.patterns["multi_line_fenced_code"])
      
                if multi_line_fenced_code_active == True:

                    #keep appending code block line until the line matches another multi_line_fenced_code pattern
                    if multiple_line_fenced_code.search(line):
                    
                        # Close the multi line code block only if the line's space of first pattern match is equal to current line's space
                        if multi_line_code_space == len(line)-len(line.lstrip()):
                            multi_line_fenced_code_active = False
                            multi_line_code_space = 0
                            
                            codeline +="</code></pre>"
                        else:
               
                            codeline+='\n'+line+'\n'

                            continue    
 
                    else:
                        #appends until pattern is match
                        codeline+='\n'+line+'\n'

                        continue
                else:
                    # check if the line is multi-line code block, 
                    # if so, set multi_line_fenced_code_active variable as True
                    #if "```" in line:
                    if multiple_line_fenced_code.search(line):
                        multi_line_fenced_code_active = True
                        multi_line_code_space = len(line)-len(line.lstrip())
                        codeline += "<pre><code>"
                        continue
                    
            # It checks for other pattern only if its not a code block
            if multi_line_fenced_code_active ==False and len(codeline) == 0 and single_line_fenced_code_active ==False:

                #heading    
                heading = re.compile(self.patterns["heading"]) 
                heading_matches = heading.search(line.strip())

                if heading_matches != None:
                    
                    line = self.heading(heading_matches,line)
                
                #bold and italic
                bold_and_italic = re.compile(self.patterns["bold_and_italic"])
                if bold_and_italic.search(line):
                    line = self.bold_and_italic(bold_and_italic,line)
                        
                            

                #HR tag
                hr =  re.compile(self.patterns["hr"])
                hr_match = hr.search(line)
                if hr_match: 
                    line = self.hr(hr,line)

                #Bold tag
                bold = re.compile(self.patterns["bold"])
                if bold.search(line):
                    line = self.bold(bold,line)

                #italic tag
                italic = re.compile(self.patterns["italic"])
        
                if italic.search(line):
        
                    line = self.italic(italic,line)
                

                #Strikethrough
                strikethrough = re.compile(self.patterns["strikethrough"])
            
                if strikethrough.search(line):
                    line = self.strikethrough(strikethrough,line)

                #ordered list
                ordered_list = re.compile(self.patterns["ol"])
                if ordered_list.search(line):
                    
                    line = self.ol_list(line,ordered_list)

                else:
                    if self.list_variable["ol"]["ol_tag_is_open"] == True:
                        #if heading_matches or hr_match:
                            line = self.close_list(line,"ol")
                            self.ol_current_line_space = 0
                            self.previous_ol_linespace =0



                #unordered list
                unordered_list = re.compile(self.patterns["ul"],re.MULTILINE)

                if unordered_list.search(line):
                    line = self.list(line,unordered_list)
                else:
                    if self.list_variable["ul"]["ultag_is_open"] == True:
                        line = self.close_list(line,"ul") #close all opened list tags
                        self.previous_ul_linespace = 0
        

                #image
                #![Minion](https://octodex.github.com/images/minion.png)
                img = re.compile(self.patterns["image_links"])

                if img.search(line):
                    line = self.image_links(img,line)

                else:    
                    #links - example:[link text](https://www.google.com/)
                    link_text =  re.compile(self.patterns["link_text"])

                    if link_text.search(line):
                        line = self.link_text(link_text,line)

                    else:
    
                        # Autoconverted link example:https://www.google.com/
                        automatic_hyperlinks =  re.compile(self.patterns["automatic_hyperlinks"])

                        if automatic_hyperlinks.search(line):
                            line = self.automatic_hyperlinks(automatic_hyperlinks,line)

                #inline code
                inline_code = re.compile(self.patterns["inline_code"])
                if inline_code.search(line):
                    line = self.inline(inline_code,line)  

                #Making sure that an empty line is not added
                if line.strip() != "": #check if line is not empty
                    pat =re.compile(r"(</*ul>|</*li>|</*ol>|</*h[1-6]{1}|</*code>|</*pre>|</*img>|</*a>|<hr>)")
                    if pat.search(line):
                        self.results += '\n'+ line +'\n'
                    else:
                        self.results+='\n'+"<p>"+line +"</p>"+'\n'
            else:
                #fenced code block
                self.results += '\n'+ codeline +'\n'
                codeline =""

        
        return self.results
            


        
            
                



    