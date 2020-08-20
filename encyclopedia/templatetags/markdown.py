from django import template
from django.template.defaultfilters import stringfilter

import re

#code patterns
class patterns():

    def __init__(self):
        # Regex pattern 
        core_patterns = {
            "heading" :"^#+\s", #heading 
            "se_text_h1":"^\s*[=]+(?<=$)", # setext h1
            "se_text_h2":"^\s*[-]+(?<=$)", # setext h2
            "ul":r"^\s*(\-|\*|\+)\s([\w*\W*\d*\D*\s*\S*]+?)(?<=$)", #unordered list
            "ol":r"^\s*(\d+)(\.|\))\s*(.+?)(?<=$)",  # ordered list
            "hr":r"(?:\s*-{3,})+|(?:\s*\*{3,})+|(?:\s*_{3,})+", #HR
            "bold":r"(\*\*|__)(?=\S)(.+?[*_]*)(?<=\S)\1", #bold
            "italic" :r"(\*|_)(?=\S)(.+?[*_]*)(?<=\S)\1", #italic
            "bold_and_italic":r"\*\*\*(.+?)\*\*\*", #combination of bold and italic
            "strikethrough" :r"(~~)(?=\S)(.+?[*_]*)(?<=\S)\1", #strikethrough
            "single_line_fenced_code":r"\s*(`{3})+([\w*\W*\d*\D*\s*\S*]+?)(`{3})+", #single line fenced code block
            "multi_line_fenced_code":r"\s*[`]+|[~]+",#multi line fenced code block
            "link_text":r"(\[(.*?)\])(\((.*?)\))", #links
            "image_links":r"(!\[(.*?)\])(\((.*?)\))", #images
            "inline_code":r"\`([\w*\W*\d*\D*\s*\S*]+?)\`", #inline-code
            "automatic_hyperlinks":r"(((http(s)*:\/\/){1}|(www\.{1}))(.*))", #web link

        }
        # HTML tags 
        substitute_patterns ={
            
            "ul_li_tag":r"\n<ul>\n<li>\2</li>\n", # new unordered list tag
            "li_tag_of_ul":r"\n<li>\2</li>\n", #li tag of unordered list
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
        #search patterns
        self.single_line_fenced_code = re.compile(core_patterns["single_line_fenced_code"],re.MULTILINE)
        self.multiple_line_fenced_code = re.compile(core_patterns["multi_line_fenced_code"])
        self.heading = re.compile(core_patterns["heading"])
        self.bold_and_italic = re.compile(core_patterns["bold_and_italic"])
        self.hr =  re.compile(core_patterns["hr"])
        self.bold = re.compile(core_patterns["bold"])
        self.italic = re.compile(core_patterns["italic"])
        self.strikethrough = re.compile(core_patterns["strikethrough"])
        self.ordered_list = re.compile(core_patterns["ol"])
        self.unordered_list = re.compile(core_patterns["ul"],re.MULTILINE)
        self.img = re.compile(core_patterns["image_links"])
        self.link_text =  re.compile(core_patterns["link_text"])
        self.automatic_hyperlinks =  re.compile(core_patterns["automatic_hyperlinks"])
        self.inline_code = re.compile(core_patterns["inline_code"])
        self.se_text_h1 = re.compile(core_patterns["se_text_h1"])
        self.se_text_h2 = re.compile(core_patterns["se_text_h2"])

        #substitute patterns
        self.single_line_fenced_code_SUB = substitute_patterns["single_line_fenced_code"]
        self.bold_and_italic_SUB = substitute_patterns["bold_and_italic"]
        self.hr_SUB =  substitute_patterns["hr_tag"] 
        self.bold_SUB = substitute_patterns["bold"]
        self.italic_SUB = substitute_patterns["italic"]
        self.strikethrough_SUB = substitute_patterns["strikethrough"]
        self.ordered_list_SUB = substitute_patterns["ol_li_tag"]
        self.li_OL_SUB = substitute_patterns["li_tag_of_ol"]
        self.unordered_list_SUB = substitute_patterns["ul_li_tag"]
        self.li_UL_SUB = substitute_patterns["li_tag_of_ul"]
        self.img_SUB = substitute_patterns["image_links"]
        self.link_text_SUB = substitute_patterns["link_text"]
        self.automatic_hyperlinks_SUB = substitute_patterns["automatic_hyperlinks"]
        self.inline_SUB = substitute_patterns["inline"]


RE = patterns()   

#variable used by code block 
class tag_variable():
    def __init__(self):
        self.codeBlock = {
            "line_with_code": "", # stores line inside code block. Used by multiple line code block and single line code block (only while inside list)
            "multi_code_active":False, #variable to make sure multi code block is active
            "start_space":0, #start space of multicode block
            "start_pattern": "", #starting pattern used to open multicode block
            "list_found":False, #if list is found while beginning the code block
            
        }
        '''
            the self.list variables are used while calculating the starting space for multi line code blocks.
            if the ul and/or ol list is active. calculate code block starting space space accordingly
        '''
        self.list = {
            
            "ul_list_active":False, 
            "ol_list_active":False,
            
        }

TagObj = tag_variable()

class markdown(object):
      
    def __init__(self,value):
        self.results='' #Stores final result
        self.previous_ul_linespace = 0 # variable that stores previous line's space of un ordered list
        self.markdown_string = value # Markdown string to be converted to HTML
        self.previous_ol_linespace  = 0 # variable that stores previous line's space of ordered list
        
        # variables used by lists
        self.list_variable = {
            "ul":{
                "ul_tag_is_open":False, # If True, a unordered list is open. 
                "sub_ultag_is_open":False, # If True, Nested Unordered list is open.
                "number_of_nested_list": 0 # Stores number of Nested Unordered List
                },
            "ol":{
                "ol_tag_is_open":False, # If True, a ordered list is open. 
                "sub_oltag_is_open":False, # If True, Nested ordered list is open.
                "number_of_nested_list":0 # Stores number of Nested ordered List
            }
        }
        self.last_opened_list_tag = "" # stores name of previous opened list tag, used when line is new list" 
    

    
    def close_list(self,line,list_type):
        '''
            This function calls close function. which closes the given list.
            if both list is given as argument, then it calls close function for ol and ul 
            else, calls close function for given list tag
             
            
        '''
        list_tags = ["ul","ol"]
        close_tags = ""
        if list_type == "both_list":
            #closes both the ul and ol list
            for i in list_tags :
                close_tags += self.close(line,i)
                
            line = close_tags +line
        else:
            
            line = self.close(line,list_type)+line

        return line

    def close(self,line,list_type):
        '''
            This function closes given list_type. 
            
        '''
        close_tags = ""
     
        if list_type in self.list_variable.keys():
            # unset all the boolean variable used by lists

            if list_type == "ul":
                TagObj.list["ul_list_active"] = False

            if list_type == "ol":
                TagObj.list["ol_list_active"] = False

            for var in self.list_variable[list_type]:
                
                if type(self.list_variable[list_type][var]) == bool and self.list_variable[list_type][var] == True:

                    close_tags += "</" + list_type + ">"+'\n'
                    self.list_variable[list_type][var] = False

            if self.list_variable[list_type]["number_of_nested_list"] >=1:
                # add close tag if number of nested list is more than one
                tags = ""

                for _ in range(int(self.list_variable[list_type][var])):
                    tags = "</" + list_type + ">"+'\n'
                close_tags += tags 

                self.list_variable[list_type]["number_of_nested_list"] = 0
                    
  
            if len(close_tags)>0:
                return close_tags
            
        return ""

    def list(self,line):
        '''
            List Rules:
                Accepts:
                    1. headers
                    2. bold(B), italic(I), B+I, Strikethrough, HR, Inline, auto-links, image, links
                    3. Single line code block
                        Example List:
                            * ``` ji ```
                    4. Multiple line code block
                        Example List:
                        
                                * Multiple line example
                                    ```
                                code
                                ```
                            * 
                                ```
                                code
                                ```            
            List levels:
                1. level 1
                a. level 2
                    b. level 3
                        ...
                2. level 1
                         
        '''

        if RE.unordered_list.search(line):
            # matched pattern of unordered list
            line = self.ul_list(line)
            
        else:
            # matched pattern of ordered list
            line = self.ol_list(line)
        
     
        return line

    #ordered list
    def ol_list(self,line):

        code_block_in_list = False
        current_ol_line_space = len(line)-len(line.lstrip())
        
        fenced_code_result = RE.multiple_line_fenced_code.findall(line)

        # if code block is found append only open tag to line
        # else substitute according to pattern.

        if len(fenced_code_result) > 0 and len(fenced_code_result[0].lstrip()) % 3 == 0 or RE.single_line_fenced_code.search(line):
            # multiple line code block 
            code_block_in_list = True


        if RE.single_line_fenced_code.search(line):

            # single line code block is found.
            TagObj.codeBlock["multi_code_active"] = False
            code_block_in_list = True


        if current_ol_line_space-self.previous_ol_linespace == 0 : 
            
            # level 1 ordered list

            if self.list_variable["ol"]["ol_tag_is_open"] == False:
                # first ol 
                
                if code_block_in_list:
                    TagObj.codeBlock["line_with_code"] += "<ol><li>"        
                line = RE.ordered_list.sub(RE.ordered_list_SUB,line)
     
                if self.last_opened_list_tag == "ul":
                    line = self.close_list(line,self.last_opened_list_tag)
                   
                self.last_opened_list_tag = "ol"
                self.list_variable["ol"]["ol_tag_is_open"] = True
                TagObj.list["ol_list_active"] = True
                self.previous_ol_linespace = current_ol_line_space


            else:
                #level 1 new li tag of ol list
                if code_block_in_list:
                    TagObj.codeBlock["line_with_code"] += "<li>"       
                
                line = RE.ordered_list.sub(RE.li_OL_SUB,line)
                if self.last_opened_list_tag == "ul":
                    line = self.close_list(line,self.last_opened_list_tag)

                


 

        elif 3<=current_ol_line_space-self.previous_ol_linespace <=6  : 
            # could be Level 2 nested ol                

            if self.list_variable["ol"]["ol_tag_is_open"] == True: 
                #Level 2 ol   
                if self.list_variable["ol"]["sub_oltag_is_open"] :
                    if self.list_variable["ol"]["number_of_nested_list"] >= 1:
                        if code_block_in_list:
                            TagObj.codeBlock["line_with_code"] += "<ol><li>"       
                        line = RE.ordered_list.sub(RE.ordered_list_SUB,line) 
                        self.last_opened_list_tag = "ol"
                    else:
                        if code_block_in_list:
                            TagObj.codeBlock["line_with_code"] += "<li>"       
                        line = RE.ordered_list.sub(RE.li_OL_SUB,line) 
                else:
                   
                    self.list_variable["ol"]["sub_oltag_is_open"] = True
                    self.list_variable["ol"]["number_of_nested_list"] +=1
                    if code_block_in_list:
                        TagObj.codeBlock["line_with_code"] += "<ol><li>"       
                    line = RE.ordered_list.sub(RE.ordered_list_SUB,line)
                    self.last_opened_list_tag = "ol"
            else:
                #first ordered list
                if code_block_in_list:
                    TagObj.codeBlock["line_with_code"] += "<ol><li>"       
                line = RE.ordered_list.sub(RE.ordered_list_SUB,line)
                self.list_variable["ol"]["ol_tag_is_open"] = True 
                TagObj.list["ol_list_active"] = True
                self.last_opened_list_tag = "ol"
            self.previous_ol_linespace = current_ol_line_space

   
        
        
        elif -6<=current_ol_line_space-self.previous_ol_linespace<=-3:
            # could be of level 1
            # before appending new ol, closes all the opened list and creates new ol tag

            oltags =""
            if self.list_variable["ol"]["number_of_nested_list"] >=1:

                for _ in range(int(self.list_variable["ol"]["number_of_nested_list"])-1):
                    oltags = "</ol>"
  
                self.list_variable["ol"]["number_of_nested_list"] =0  

            if self.list_variable["ol"]["ol_tag_is_open"] == True:

                if self.list_variable["ol"]["sub_oltag_is_open"] :
                    if code_block_in_list:
                        TagObj.codeBlock["line_with_code"] += "<li>"       
                    line = RE.ordered_list.sub(RE.li_OL_SUB,line) 

                else:
                   
                    self.list_variable["ol"]["sub_oltag_is_open"] = True
                    self.list_variable["ol"]["number_of_nested_list"] +=1
                    if code_block_in_list:
                        TagObj.codeBlock["line_with_code"] += "<ol><li>"       
                    line = RE.ordered_list.sub(RE.ordered_list_SUB,line)
                    self.last_opened_list_tag = "ol"
           
                    
                line =line+oltags
            else:
                 #first ordered list
                if code_block_in_list:
                    TagObj.codeBlock["line_with_code"] += "<ol><li>"       
                line = RE.ordered_list.sub(RE.ordered_list_SUB,line)
                self.list_variable["ol"]["ol_tag_is_open"] = True 
                TagObj.list["ol_list_active"] = True
                self.last_opened_list_tag = "ol"
            self.previous_ol_linespace = current_ol_line_space

        else:

            # if the lines does not fall in any of the above categories , it is considered as a entirely new ol list
            if self.list_variable["ol"]["ol_tag_is_open"] == True: 
                line = self.close_list(line,"ol")

            if code_block_in_list:
                TagObj.codeBlock["line_with_code"] += "<ol><li>"    

            line = RE.ordered_list.sub(RE.ordered_list_SUB,line)
            self.list_variable["ol"]["ol_tag_is_open"] = True #set ol tag to open
            TagObj.list["ol_list_active"] = True
            self.last_opened_list_tag = "ol"
            self.previous_ol_linespace = current_ol_line_space
        
        if code_block_in_list:
            #handle code block
            line = self.code_block_inlist(line)
           
        return line   



    #code block inside list
    def code_block_inlist(self,line):
        
        if RE.single_line_fenced_code.search(line) and TagObj.codeBlock["multi_code_active"] == False:
            
            line = self.single_line_code(line) 
            return line 
            
        else:
            fenced_code_result = RE.multiple_line_fenced_code.findall(line)

            if len(fenced_code_result) > 0 and len(fenced_code_result[0].lstrip()) % 3 == 0:
                
                self.multiple_line_fenced_code(fenced_code_result,line)
        return None
        
                
      
    #unordered list
    def ul_list(self,line):

        code_block_in_list = False
        currentlinespace = len(line)-len(line.lstrip())

        
        # if code block is found append only open tag to line
        # else substitute according to pattern.
        fenced_code_result = RE.multiple_line_fenced_code.findall(line)
        if len(fenced_code_result) > 0 and len(fenced_code_result[0].lstrip()) % 3 == 0 :
            code_block_in_list = True

        if RE.single_line_fenced_code.search(line):
            TagObj.codeBlock["multi_code_active"] = False
            code_block_in_list = True

        

        
        if currentlinespace-self.previous_ul_linespace == 0: 
            # level 1 list

            if self.list_variable["ul"]["ul_tag_is_open"] == True:    
                if code_block_in_list:
                    TagObj.codeBlock["line_with_code"] += "<li>"        
                line = RE.unordered_list.sub(RE.li_UL_SUB,line)
                if self.last_opened_list_tag == "ol":
                    line = self.close_list(line,self.last_opened_list_tag)

            else:
                # first ul 


                if code_block_in_list:
                    TagObj.codeBlock["line_with_code"] += "<ul><li>"    
                
                line = RE.unordered_list.sub(RE.unordered_list_SUB,line)
                if self.last_opened_list_tag == "ol":
                    line = self.close_list(line,self.last_opened_list_tag)
                
                self.list_variable["ul"]["ul_tag_is_open"] = True #set ul tag to open
                TagObj.list["ul_list_active"] = True
                self.previous_ul_linespace = currentlinespace
                self.last_opened_list_tag = "ul"

                

  
        # could be Level 2 nested ol     
        elif 2<=currentlinespace-self.previous_ul_linespace <=5: 

            if self.list_variable["ul"]["ul_tag_is_open"] == True: #not a first ul in the list

                if self.list_variable["ul"]["sub_ultag_is_open"] :
                    if self.list_variable["ul"]["number_of_nested_list"] >= 1:
                        
                        if code_block_in_list:
                            TagObj.codeBlock["line_with_code"]+= "<ul><li>"
                        line = RE.unordered_list.sub(RE.unordered_list_SUB,line) 
                        self.last_opened_list_tag = "ul"
                  
                    else:
                        if code_block_in_list:
                            TagObj.codeBlock["line_with_code"]+= "<li>"
                        line = RE.unordered_list.sub(RE.li_UL_SUB,line) 
                else:
                   
                    self.list_variable["ul"]["sub_ultag_is_open"] = True
                    self.list_variable["ul"]["number_of_nested_list"] +=1

                    if code_block_in_list:
                        TagObj.codeBlock["line_with_code"]+= "<ul><li>"
                    line = RE.unordered_list.sub(RE.unordered_list_SUB,line)
                    self.last_opened_list_tag = "ul"
            else:
                # first ul
                if code_block_in_list:
                    TagObj.codeBlock["line_with_code"]+= "<ul><li>"
                line = RE.unordered_list.sub(RE.unordered_list_SUB,line)
                self.list_variable["ul"]["ul_tag_is_open"] = True 
                TagObj.list["ul_list_active"] = True
                self.last_opened_list_tag = "ul"
            self.previous_ul_linespace = currentlinespace

        # nested new list
        # if the lines does not fall in any of the above categories , it is considered as a entirely new ul list
        else: 

            #close all previous nested list
           
            line =self.close_list(line,"ul")

            line = RE.unordered_list.sub(RE.unordered_list_SUB,line)
            TagObj.list["ul_list_active"] = True
            self.list_variable["ul"]["ul_tag_is_open"] = True #set ul tag to open
            self.previous_ul_linespace = currentlinespace
            self.last_opened_list_tag = "ul"
            
        #handle code block if true
        if code_block_in_list:
            
            line = self.code_block_inlist(line)
            
  
        return line   
                         

    #heading
    def heading(self,heading_matches,line):
        
        tag = heading_matches.end()
        hashTagLen = (heading_matches.end()- heading_matches.start())-1
       
        htmlTag = "h" + str(hashTagLen)
        content = line.strip()[(heading_matches.end() ):]
      
        line = line[0:heading_matches.start()]+"<" + htmlTag + ">" + content + "</" + htmlTag + ">"+'\n'
        return line
    
    #HR tag
    def hr(self,line):
        line = RE.hr.sub(RE.hr_SUB,line)
        return line
    
    #Bold
    def bold(self,line):
        line = RE.bold.sub(RE.bold_SUB,line)
        return line

    #Italic
    def italic(self,line):
        line = RE.italic.sub(RE.italic_SUB,line)
        return line

    #Strikethrough
    def strikethrough(self,line):
        line = RE.strikethrough.sub(RE.strikethrough_SUB,line)
        return line

    #Bold and italic
    def bold_and_italic(self,line):
        line = RE.bold_and_italic.sub(RE.bold_and_italic_SUB,line )
        return line

    #single line code 
    def single_line_code(self,line):
        #example: ``` hi ```
        line = RE.single_line_fenced_code.sub(RE.single_line_fenced_code_SUB,line)
        return line

    #image links
    def image_links(self, line):
        line = RE.img.sub(RE.img_SUB,line)
        return line

    #links
    def link_text(self, line):
        line = RE.link_text.sub(RE.link_text_SUB,line)
        return line
    
   
    #inline code
    def inline(self,line):
        line = RE.inline_code.sub(RE.inline_SUB,line)
        return line

    #web links
    def automatic_hyperlinks(self, line):
        line = RE.automatic_hyperlinks.sub(RE.automatic_hyperlinks_SUB,line)
        return line
    
    #multiple line code
    def multiple_line_fenced_code(self,results,line):

        '''

            example: 

                ``` 

                code 

                ```
            RULES of codeblock
        
            1. 
                Does not accept texts with headers, bold, italic, Bold and italic, Strikethrough, 
                link_text, automatic_hyperlinks, inline, image, lists,single line fenced code

            2. 
                code block can be inside list but list can not be inside code block.

        '''
        # list_found variable is changed from list function again which causes trouble
        add_space = 0
        

        space = len(line)-len(line.lstrip())

        if not TagObj.codeBlock["multi_code_active"]:   
            
            #new code block
            TagObj.codeBlock["start_pattern"] = results[0].lstrip()
            TagObj.codeBlock["start_space"] = space
 
            
            if TagObj.codeBlock["list_found"] ==True:
       
                # if list found in line, add space for each opened list tags to start space.
                list_type = ["ul","ol"]
                for i in list_type:
                
                    for var in self.list_variable[i]:
                    
                        if type(self.list_variable[i][var]) == bool and self.list_variable[i][var] == True:
                            add_space +=1 
                     

                
                add_space = add_space + self.list_variable["ul"]["number_of_nested_list"] +self.list_variable["ol"]["number_of_nested_list"]

                if TagObj.codeBlock["start_space"] == -1:
                    add_space = 0
    
            TagObj.codeBlock["multi_code_active"] = True
            
            if 0 <= len(results[0])-TagObj.codeBlock["start_space"]<= 3:
                TagObj.codeBlock["line_with_code"] += "<pre><code>"
                TagObj.codeBlock["start_space"] += add_space
                
            else:
                TagObj.codeBlock["line_with_code"] += "<pre><code>"+line
        
            TagObj.codeBlock["list_found"] = False
        else:
            
            # fence block is active so keep appending until close
            # close pattern must be same as pattern used to start code block
            # the left trailing space length must be from 0 till 3(inclusive)
            if len(results) > 0:
            
                find = line.find(TagObj.codeBlock["start_pattern"])


                current_pat = results[0][find::]
                # if list is open, remove space for each opened list tags from start space.
                if TagObj.list["ol_list_active"]:
                    find -=1 

                if TagObj.list["ul_list_active"]:
                    find -=1

                if  self.list_variable["ul"]["number_of_nested_list"]>0:
                    find -=self.list_variable["ul"]["number_of_nested_list"]
                if self.list_variable["ol"]["number_of_nested_list"]>0:
                    find -=self.list_variable["ol"]["number_of_nested_list"]
                if find == -1:
                    find = 0

                res = 0<=abs(find-TagObj.codeBlock["start_space"])<=3 and current_pat == TagObj.codeBlock["start_pattern"]
                
                    
                if  results[0].lstrip() == TagObj.codeBlock["start_pattern"] and res:
                    TagObj.codeBlock["multi_code_active"] = False
                    TagObj.codeBlock["start_space"]  = 0
                    if TagObj.list["ol_list_active"] or TagObj.list["ul_list_active"]:
                        
                        TagObj.codeBlock["line_with_code"]  += '\n'+"</pre></code></li>"+'\n'
                      
                    else:
                        TagObj.codeBlock["line_with_code"]  += '\n'+"</pre></code>"+'\n'
                    
                else:

                    TagObj.codeBlock["line_with_code"] +='\n'+line+'\n'


            else:
                TagObj.codeBlock["line_with_code"] +='\n'+line+'\n'

            

    def highlight_patterns(self,line):
        #heading
        heading_line_edit = ""

        for eachline in line.split("\n"):
            heading_matches = RE.heading.search(eachline.strip())

            if heading_matches != None:    
                heading_line_edit += self.heading(heading_matches,eachline)
            else:
                heading_line_edit += eachline

        if heading_line_edit != "":
            
            line = heading_line_edit

        #bold and italic
        if RE.bold_and_italic.search(line):
            line = self.bold_and_italic(line)

        #hr
        if RE.hr.search(line): 
            line = self.hr(line)

        #Bold tag
        if RE.bold.search(line):
            line = self.bold(line)

        #italic tag
        if RE.italic.search(line):                    
            line = self.italic(line)

        #Strikethrough
        if RE.strikethrough.search(line):
            line = self.strikethrough(line)

        #image
        #![Minion](https://octodex.github.com/images/minion.png)
        if RE.img.search(line):
            line = self.image_links(line)

        else:    
            #links - example:[link text](https://www.google.com/)
            if RE.link_text.search(line):
                line = self.link_text(line)

            else:
                # Autoconverted link example:https://www.google.com/
                if RE.automatic_hyperlinks.search(line):
                    line = self.automatic_hyperlinks(line)
    
        #inline code
        if RE.inline_code.search(line):
            line = self.inline(line)  

        return line


    # markdown to html main function
    def markdown_parser(self):

        
        tag ="" # if any html tags are found in md file. 
        imglines = "" # if any image is added to md file


        #process markdown string
        md_string = self.markdown_string.strip()
        md_string = md_string.replace("\r\n", "\n").replace("\r", "\n")
        md_string += "\n\n"
        md_string = md_string.expandtabs(4)

        #length of string
        md_len = len(md_string.split("\n"))
        index = 0 
        ignore_index = -1
       
        #main loop that process the string

        for index in range(0,md_len):

            
            add_br_tag = False #line break variable 
            line = md_string.split("\n")[index]

            if index == ignore_index:
                ignore_index = -1
                continue
            if line.strip() != "":
              
                #line break : yet to implement
                if not(RE.multiple_line_fenced_code.search(line) or RE.single_line_fenced_code.search(line) 
                or  TagObj.codeBlock["multi_code_active"]):
                    if (line[len(line)-1] == "\\") or len(line)-len(line.rstrip())>=2 :
                        '''
                        line break ( <br> ):
                            if line has more than 2 space
                            if line = "foo\(\ followed by 0 space)
                                    bar"
                            if line = "foo\  (\ followed by 2 or more space)
                                    bar"
                        '''
                        if index <= md_len-1:
                            # <br> has to be added for next line 
                            # if next line is not a blank line
                            md_string.split("\n")[index+1].strip!=""
                            add_br_tag = True
                       

                #single line fenced code
                if RE.single_line_fenced_code.search(line) and  TagObj.codeBlock["multi_code_active"] == False:

                    if RE.ordered_list.search(line) or RE.unordered_list.search(line):
                        # list is found , respective list handled single line code
                        TagObj.codeBlock["line_with_code"] += self.list(line)  
                    else:
                        line = self.single_line_code(line)  
                else:
                     #multiple line fenced code
                    fenced_code_result = RE.multiple_line_fenced_code.findall(line)
                    
                    if TagObj.codeBlock["multi_code_active"]== True: 
                        '''
                            The code block is active so do not check for other patterns 
                            just keep appending all the lines until close pattern
                        '''
                        
                        self.multiple_line_fenced_code(fenced_code_result,line)


                    else:
                        # new code block   
                        if len(fenced_code_result) > 0 and len(fenced_code_result[0].lstrip()) % 3 == 0:
                            if RE.ordered_list.search(line) or RE.unordered_list.search(line):
                                TagObj.codeBlock["list_found"] = True
                                line = self.list(line)
                                if line == None:
                                    continue
                            self.multiple_line_fenced_code(fenced_code_result,line)
                        else:
                            # Multiple or single line code block not found to check for all other patterns
                            pat =re.compile(r"(</*ul>|</*li>|</*ol>|</*h[1-6]{1}|</*code>|</*pre>|</*a>|<hr>|</*p>)")
                            imgpat = re.compile(r"(</*img)")
                            '''
                                if a html tag is found, check if next non empty line has a img tag
                                if img is found, save current line tag
                            '''
                            if pat.search(line):
                                for next_index in range(index,md_len-1):
                                    if md_string.split("\n")[next_index].strip():
                                        next_non_empty_line = md_string.split("\n")[next_index]
                                        break
                                if imgpat.search(next_non_empty_line):
                                    tag = line
                                continue

                            else:
                                # if img is found append image tag lines
                                if imgpat.search(line):
                                    
                                    if tag !="":
                                        imglines=tag+line
                                    else:
                                        imglines=line
                                  

                            # if image tag is found no need to check for other patterns. append image line to results
                            if len(imglines) <=0:
                                #list
                                if RE.ordered_list.search(line) or RE.unordered_list.search(line):
                                    
                                    line = self.list(line)  
                                else:
                                    # if current line is a list, check next non empty line. if next line is not a list, close all the opened list
                                    next_non_empty_line =""
                                    if self.list_variable["ul"]["ul_tag_is_open"] or self.list_variable["ol"]["ol_tag_is_open"] :
                                        
                                        for next_index in range(index,md_len-1):
                                            
                                            if md_string.split("\n")[next_index].strip():
                                                next_non_empty_line = md_string.split("\n")[next_index]
                                                
                                                break
                                        else:
                                            line = self.close_list(line,"both_list")
                                            
                                            #close lists. Since all the lines after current line is empty.
                                        
                                        if not(RE.ordered_list.search(next_non_empty_line) 
                                        or RE.unordered_list.search(next_non_empty_line) or RE.multiple_line_fenced_code.findall(line)):
                                            #close list. Since next line is not part of ul, ol or code block
                                            
                                            line = self.close_list(line,"both_list")
                                        
                               

                                if line == None:
                                    continue

                                line = self.highlight_patterns(line)

                                

            
                               
                
                if len(TagObj.codeBlock["line_with_code"]) > 0 :
                    #append lines which is either single or multiple line code block.
                    
                    self.results += '\n'+ TagObj.codeBlock["line_with_code"] +'\n'
                    TagObj.codeBlock["line_with_code"]  = ""

                elif len(imglines)>0:
                    # if image lines are found
                    self.results += imglines+"\n"
                    imglines =""                    
                else:
                    pat =re.compile(r"(</*ul>|</*li>|</*ol>|<ol|</*h[1-6]{1}|</*code>|</*pre>|</*img>|</*a|<hr>|<img|</*img>)")
                    
                    for line in line.split("\n"):
                        if line.strip()!="":
                            
                            ind = pat.search(line)  
                            pline ="" 
                            if ind:
                                # if there is combination of plain light with highlighting patterns
                                if ind.start()>0:
                                    pline = "<p>"+line[0:ind.start()]
                                    
                                    
                                if pline !="":
                                    self.results += '\n'+ pline+ line[ind.start()::] +'</p>'+'\n'
                    
                                else:
                                    self.results += '\n'+ line +'\n'
                            else:
                                # se text h1 and h2
                                for next_index in range(index+1,index+2):
                                  
                                    if md_string.split("\n")[next_index].strip():
                                                                
                                            next_line = md_string.split("\n")[next_index]

                                            if  RE.se_text_h1.search(next_line):  
                                                self.results+='\n'+"<h1>"+line +"</h1><hr>"+'\n'
                                                ignore_index = next_index
                                                next_line =""
                                                break
                                            else:
                                                if RE.se_text_h2.search(next_line): 
                                                    self.results+='\n'+"<h2>"+line +"</h2><hr>"+'\n' 
                                                    ignore_index =  next_index
                                                    next_line =""
                                                    break
                                            
                                else:
                                     
                                    self.results+='\n'+"<p>"+line +"</p>"+'\n'  
        if  TagObj.list["ul_list_active"]:
            list_close=self.close_list(TagObj.codeBlock["line_with_code"],"ul")   
            self.results += '\n'+ list_close +'\n'

        if  TagObj.list["ol_list_active"]:
            list_close=self.close_list(TagObj.codeBlock["line_with_code"],"ol")   
            self.results += '\n'+ list_close +'\n'   

        if TagObj.codeBlock["multi_code_active"]:
            # As we have reached end of string now, we have to check if multiple code block is active.
            # If active, we have to close the code block by ourselves
  
            TagObj.codeBlock["line_with_code"] += "</pre></code>"

            if  TagObj.list["ul_list_active"]:
                TagObj.codeBlock["line_with_code"]=self.close_list(TagObj.codeBlock["line_with_code"],"ul")  
            self.results += '\n'+ TagObj.codeBlock["line_with_code"] +'\n'
            TagObj.codeBlock["multi_code_active"] = False
            TagObj.codeBlock["start_space"]  = 0
            TagObj.codeBlock["line_with_code"]  = ""
 
   
        if len(TagObj.codeBlock["line_with_code"]) > 0:
 
            self.results += '\n'+ TagObj.codeBlock["line_with_code"] +'\n'
            TagObj.codeBlock["line_with_code"]  = ""

        
      

        return self.results
            


        
            
                



    