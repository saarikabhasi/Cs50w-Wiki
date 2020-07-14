from django import template
from django.template.defaultfilters import stringfilter

import re,sys

# register = template.Library()
# pre inside a li 


# @register.filter()
# @stringfilter

class markdown(object):
  
    def __init__(self,value):
        self.results=''
        self.ultag_is_open = False
        self.sub_ultag_is_open =False    
        self.ol_tag_is_open =False
        self.sub_oltag_is_open = False
        self.previouslinespace = 0
        self.count =0
        self.markdown_string = value
        self.ol_current_line_space = 0
        self.number_of_ol_list = 0
        self.previous_ol_linespace  = 0
        self.tags = {
            "ul":["ultag_is_open","sub_ultag_is_open","count"],
            "ol":["ol_tag_is_open","sub_ultag_is_open","number_of_ol_list"]
        }
        
    

        # Regex pattern 
        self.patterns = {
            "heading" :"#+\s", #heading
            "ul":r"^\s*(\-\s|\*\s)([\w*\W*\d*\D*\s*\S*]+?)(?<=$)", #unordered list
            "ol":r"^\s*(\d+)(\.|\))\s*(.+?)(?<=$)",  # ordered list
            "hr":r"(?:\s*-{3,})+|(?:\s*\*{3,})+|(?:\s*_{3,})+", #HR
            "bold":r"(\*\*|__)(?=\S)(.+?[*_]*)(?<=\S)\1", #bold
            "italic" :r"(\*|_)(?=\S)(.+?[*_]*)(?<=\S)\1", #italic
            "bold_and_italic":r"\*\*\*(.+?)\*\*\*",
            "strikethrough" :r"(~~)(?=\S)(.+?[*_]*)(?<=\S)\1", #strikethrough
            "single_line_fenced_code":r"\s*(`{3})+([\w*\W*\d*\D*\s*\S*]+?)(`{3})+(?<=$)",#Single line fenced code block
            "multi_line_fenced_code": r"\s*(`{3})",#Muliple line fenced code block
            "a_links":r"(\[(.*?)\])(\((.*?)\))", #Links
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
            "a_links":r"<a href =\4>\2</a>", #links
 
            

        }

    # close all the opened tags of unordered list
    def close_list(self,line,type):
        
        # if type in tags.keys():
        #     for var in range(2):
        #         variable = tags[type][var]
        #         print("VAR",variable)
        #         if self.tags[type][var]== True:    
        #             line = "</" + type + ">"+'\n'+line
        #             #line ="</ul>"+'\n'+line
        #             self.variable = False
            
        #     # if  self.sub_ultag_is_open ==True:
        #     #     line = "</" + type + ">"+'\n'+line
        #     #     # line ="</ul>"+'\n'+line
        #     #     self.sub_ultag_is_open =False
        #     # if self.count >=1:
        #     sub_list = tags[type][2]
        #     if self.sub_list>= 1:
        #         for i in range(tags[type][2]):
        #             ultags = "</" + type + ">"+'\n'
        #             #ultags ="</ul>"+'\n'

        #         line =ultags +line
        #         self.sub_list =0  
        if type == "ul":
            if self.ultag_is_open == True:    
                line = "</" + type + ">"+'\n'+line
                #line ="</ul>"+'\n'+line
                self.ultag_is_open = False

            if self.sub_ultag_is_open == True:
                line = "</" + type + ">"+'\n'+line
                line ="</ul>"+'\n'+line
                self.sub_ultag_is_open =False
                    
            if self.count >=1:
                for _ in range(self.count):
                    ultags = "</" + type + ">"+'\n'
                    #ultags ="</ul>"+'\n'

                line =ultags +line
                self.count =0  
        else:
            if self.ol_tag_is_open == True: 
                line = "</" + type + ">"+'\n'+line
                self.ol_tag_is_open = False

            if  self.sub_oltag_is_open ==True:
                line = "</" + type + ">"+'\n'+line
                # line ="</ul>"+'\n'+line
                self.sub_oltag_is_open =False
                    
            if self.number_of_ol_list >=1:
                for _ in range(self.number_of_ol_list):
                    oltags = "</" + type + ">"+'\n'
                    #ultags ="</ul>"+'\n'

                line =oltags + line
                self.number_of_ol_list =0  
        
            

        return line   

    #ordered list
    def ol_list(self,line,ordered_list):
        
        #First Ordered list
        # 3 till 6
        current_ol_line_space = len(line)-len(line.lstrip())
        #non nested list

        if current_ol_line_space-self.previous_ol_linespace == 0 : 
      
            if self.ol_tag_is_open == False:
                
                line = ordered_list.sub(self.substitute_patterns["ol_li_tag"],line)
                self.ol_tag_is_open = True
                self.previous_ol_linespace = current_ol_line_space

            else:
                line = ordered_list.sub(self.substitute_patterns["li_tag_of_ol"],line)

        #nested list    
        elif 3<=current_ol_line_space-self.previous_ol_linespace <=6  : 

            if self.ol_tag_is_open == True: #not a first ordered list

                if self.sub_oltag_is_open :
                    if self.number_of_ol_list >= 1:
                        line = ordered_list.sub(self.substitute_patterns["ol_li_tag"],line) 
                    line = ordered_list.sub(self.substitute_patterns["li_tag_of_ol"],line) 
                else:
                   
                    self.sub_oltag_is_open = True
                    self.number_of_ol_list +=1
                    line = ordered_list.sub(self.substitute_patterns["ol_li_tag"],line)
            else:

                line = ordered_list.sub(self.substitute_patterns["ol_li_tag"],line)
                self.ol_tag_is_open = True 
            self.previous_ol_linespace = current_ol_line_space

        elif -6<=current_ol_line_space-self.previous_ol_linespace<=-3:
            oltags =""

            if self.number_of_ol_list >=1:
                for _ in range(self.number_of_ol_list):
                    oltags = "</ol>"
  
                self.number_of_ol_list =0  

            if self.ol_tag_is_open == True: #not a first ordered list

                if self.sub_oltag_is_open :
                    self.number_of_ol_list +=1
                    line = ordered_list.sub(self.substitute_patterns["li_tag_of_ol"],line) 

                else:
                   
                    self.sub_oltag_is_open = True
                    self.number_of_ol_list +=1
                    line = ordered_list.sub(self.substitute_patterns["ol_li_tag"],line)
           
                    
                line =oltags + line
            else:

                line = ordered_list.sub(self.substitute_patterns["ol_li_tag"],line)
                self.ol_tag_is_open = True 
            self.previous_ol_linespace = current_ol_line_space

        else:
           
       
            line =self.close_list(line,"ol")
            line = ordered_list.sub(self.substitute_patterns["ol_li_tag"],line)
            self.ol_tag_is_open = True #set ul tag to open
            self.previous_ol_linespace = current_ol_line_space

        return line   

   


    #unordered list
    def list(self,line,unordered_list):
        currentlinespace = len(line)-len(line.lstrip())
        
        #non nested list
        if currentlinespace-self.previouslinespace == 0: 

            if self.ultag_is_open == True:                       
                line = unordered_list.sub(self.substitute_patterns["li_tag_of_ul"],line)

            else:
                #first li in the list
                line = unordered_list.sub(self.substitute_patterns["ul_li_tag"],line)
                self.ultag_is_open = True #set ul tag to open
                self.previouslinespace = currentlinespace

        #nested list    
        elif 2<=currentlinespace-self.previouslinespace <=5: 
           
            if self.ultag_is_open == True: #not a first li in the list

                if self.sub_ultag_is_open :
                    if self.count >= 1:
                        line = unordered_list.sub(self.substitute_patterns["ul_li_tag"],line) 
                    line = unordered_list.sub(self.substitute_patterns["li_tag_of_ul"],line) 
                else:
                   
                    self.sub_ultag_is_open = True
                    self.count +=1
                    line = unordered_list.sub(self.substitute_patterns["ul_li_tag"],line)
            else:

                line = unordered_list.sub(self.substitute_patterns["ul_li_tag"],line)
                self.ultag_is_open = True 
            self.previouslinespace = currentlinespace

        #nested new list
        else: #currentlinespace < self.previouslinespace:

            #close all previous nested list
            line =self.close_list(line,"ul")

            line = unordered_list.sub(self.substitute_patterns["ul_li_tag"],line)
            self.ultag_is_open = True #set ul tag to open
            self.previouslinespace = currentlinespace

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
    
    #links
    def links(self,link, line):
        line = link.sub(self.substitute_patterns["a_links"],line)
        return line
    
    # markdown to html main function
    def markdown_parser(self,markdown_string):
        codeline =""
        lines =""
        single_line_fenced_code_active = False
        multi_line_fenced_code_active = False
        
       
        for line in markdown_string.splitlines():
            multi_line_code_space = 0
            single_line_fenced_code = re.compile(self.patterns["single_line_fenced_code"],re.MULTILINE)

            #check if the line has single line code block
            if single_line_fenced_code.search(line) and multi_line_fenced_code_active ==False:
                single_line_fenced_code_active ==True
                codeline = self.single_line_code(single_line_fenced_code,line)
            else:
                multiple_line_fenced_code = re.compile(self.patterns["multi_line_fenced_code"])
      
                if multi_line_fenced_code_active == True:
                
                    if multiple_line_fenced_code.search(line):
                        if multi_line_code_space == len(line)-len(line.lstrip()):
                            multi_line_fenced_code_active = False
                            multi_line_code_space = 0
                            
                            codeline +="</code></pre>"
                        else:
               
                            codeline+='\n'+line+'\n'

                            continue    
 
                    else:
                        #keep appending code block line until you get another ```

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
                    

            if multi_line_fenced_code_active ==False and len(codeline) == 0 and single_line_fenced_code_active ==False:
                #heading    
                heading = re.compile(self.patterns["heading"]) 
                heading_matches = heading.search(line.strip())

                if heading_matches != None:
                    
                    line=self.heading(heading_matches,line)
                
                #bold and italic
                bold_and_italic = re.compile(self.patterns["bold_and_italic"])
                if bold_and_italic.search(line):
                    line = self.bold_and_italic(bold_and_italic,line)
                  
                    

                #HR tag
                hr =  re.compile(self.patterns["hr"])
                hr_match = hr.search(line)
                if hr_match: 
                    line = self.hr(hr,line)
                

                #ordered list
                ordered_list = re.compile(self.patterns["ol"])
                if ordered_list.search(line):
                    
                    line = self.ol_list(line,ordered_list)

                else:
                    if self.ol_tag_is_open == True:
                        #if ordered_list.search(line).group(1)- self.number_of_ol_list !=1:

                        if len(line)-(len(line)-len(line.lstrip())) == self.previous_ol_linespace or heading_matches or hr_match:
                            line = self.close_list(line,"ol")
                            self.ol_current_line_space = 0
                            self.previous_ol_linespace =0



                #unordered list
                unordered_list = re.compile(self.patterns["ul"],re.MULTILINE)

                if unordered_list.search(line):
                    line = self.list(line,unordered_list)
                else:
                    line = self.close_list(line,"ul") #close all opened list tags
                    self.previouslinespace = 0
                
                
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

                
                #links
                link =  re.compile(self.patterns["a_links"])

                if link.search(line):
                    line = self.links(link,line)
                

    
                #Making sure that an empty line is not added
            
                if line.strip() != "": #check if line is not empty
                    if "<ul>" not in line and "</ul>" not in line:
                        if "<li>" not in line and "</li>" not in line:
                            if "<ol>" not in line and "</ol>" not in line:
                                if "<h" not in line and "<h" not in line:
                                    if "<code>" not in line and "</code>" not in line:
                                        if "<pre>" not in line and "</pre>" not in line:
                                            self.results+='\n'+"<p>"+line +"</p>"+'\n'
                                        else:
                                            self.results += '\n'+ codeline +'\n'
                                    else:
                                        self.results += '\n'+ codeline +'\n'
                                else:
                                    self.results += '\n'+ line +'\n'
                            else:
                                self.results += '\n'+ line +'\n'
                        else:
                            self.results += '\n'+ line +'\n'
                    else:
                        self.results += '\n'+ line+'\n'

            else:
                #Fenced Code block
                self.results += '\n'+ codeline +'\n'
                codeline =""


        return self.results
            


        
            
                



    