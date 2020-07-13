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
        self.ol_is_open =False
        self.previouslinespace = 0
        self.count =0
        self.markdown_string = value
        self.code_area = False

        # Regex pattern 
        self.patterns = {
            "heading" :"#+\s", #heading
            "ul": r"^\s*(\-\s|\*\s)([\w+(\[|\^&+\-.',%\(\/)=!\:>\'\"\*\s]+?)(?<=$)", #unordered list
            "ol":r"^\s*(\d+\.\s*)(.+?)(?<=$)",  # ordered list
            "pre":r"\s{4,}(\-\s|\*\s)([\w+(\[|\^&+\-.',%\(\/)=!\:>\'\"\s]+?)(?<=$)", #pre tag
            "hr":r"(?:\s*-{3,})+|(?:\s*\*{3,})+|(?:\s*_{3,})+", #HR
            "bold":r"(\*\*|__)(?=\S)(.+?[*_]*)(?<=\S)\1", #bold
            "italic" :r"(\*|_)(?=\S)(.+?[*_]*)(?<=\S)\1", #italic
            "bold_and_italic":r"\*\*\*(.+?)\*\*\*",
            "strikethrough" :r"(~~)(?=\S)(.+?[*_]*)(?<=\S)\1", #strikethrough
            "code":r"```((.+?\n)+)", #blocked code
            #code single line:(?:`{3})+(?<=\S)(\w*)(?:`{3})+

            
        }
        # HTML tags 
        self.substitute_patterns ={
            "li_tag":r"\n<li>\2</li>\n", #li tag
            "ul_li_tag":r"\n<ul>\n<li>\2</li>\n", # new un ordered list tag
            "hr_tag" : r"\n<hr>\n", #line break tag 
            "bold":r"<strong>\2</strong>", #bold
            "italic":r"<em>\2</em>", #italic
            "strikethrough":r"<s>\2</s>", #strikethrough
            "bold_and_italic":r"<strong><em>\2</em></strong>", #Bold and italic
            "code":r"<pre><code>\1</code></pre>",
        }

    # close all the opened tags of unordered list
    def close_list(self,line):

        if self.ultag_is_open == True:    

            line ="</ul>"+'\n'+line
            self.ultag_is_open = False

        if  self.sub_ultag_is_open ==True:

            line ="</ul>"+'\n'+line
            self.sub_ultag_is_open =False
                
        if self.count >=1:
            for _ in range(self.count):
                ultags ="</ul>"+'\n'

            line =ultags +line
            self.count =0  

        return line   

    #unordered list
    def list(self,line,unordered_list):
        self.currentlinespace = len(line)-len(line.lstrip())
        
        #non nested list
        if self.currentlinespace-self.previouslinespace == 0: 

            if self.ultag_is_open == True:                       
                line = unordered_list.sub(self.substitute_patterns["li_tag"],line)

            else:
                #first li in the list
                line = unordered_list.sub(self.substitute_patterns["ul_li_tag"],line)
                self.ultag_is_open = True #set ul tag to open
                self.previouslinespace = self.currentlinespace

        #nested list    
        elif 2<=self.currentlinespace-self.previouslinespace<=5: 
           
            if self.ultag_is_open == True: #not a first li in the list

                if self.sub_ultag_is_open :
                    if self.count >= 1:
                        line = unordered_list.sub(self.substitute_patterns["ul_li_tag"],line) 
                    line = unordered_list.sub(self.substitute_patterns["li_tag"],line) 
                else:
                   
                    self.sub_ultag_is_open = True
                    self.count +=1
                    line = unordered_list.sub(self.substitute_patterns["ul_li_tag"],line)
            else:

                line = unordered_list.sub(self.substitute_patterns["ul_li_tag"],line)
                self.ultag_is_open = True 
            self.previouslinespace = self.currentlinespace

        #nested new list
        else: #self.currentlinespace < self.previouslinespace:

            #close all previous nested list
            line =self.close_list(line)

            line = unordered_list.sub(self.substitute_patterns["ul_li_tag"],line)
            self.ultag_is_open = True #set ul tag to open
            self.previouslinespace = self.currentlinespace

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
    def code(self,code,line):
        line = code.sub(self.substitute_patterns["code"],line)
        print("After change pre-code",line)
        return line
    

    # markdown to html main function
    def markdown_parser(self,markdown_string):
        codeline =""
        for line in markdown_string.splitlines():
            print("LINE",line)
            print("self.code_area Before test",self.code_area )

            if self.code_area == True:
                if "```" in line:
                    self.code_area = False
                    line = codeline+"</code></pre>"
                    
                    codeline=""
                else:
                    codeline +=line+'\n'
                    print("line after change",codeline)
                    continue
            else:
                if "```" in line:
                    self.code_area = True
                    codeline = "<pre><code>"
            print("self.code_area After TEst",self.code_area )
            if self.code_area ==False:
                #heading    
                heading = re.compile(self.patterns["heading"]) 
                heading_matches = heading.search(line.strip())

                if heading_matches != None:
                    
                    line=self.heading(heading_matches,line)

                #unordered list
                unordered_list = re.compile(self.patterns["ul"],re.MULTILINE)

                if unordered_list.search(line):
                    line = self.list(line,unordered_list)
                else:
                    line = self.close_list(line) #close all opened list tags
                    self.previouslinespace = 0

                #HR tag
                hr =  re.compile(self.patterns["hr"])
                if hr.search(line): 
                    line = self.hr(hr,line)

                #bold and italic
                bold_and_italic = re.compile(self.patterns["bold_and_italic"])
                if bold_and_italic.search(line):
                    line = self.bold_and_italic(bold_and_italic,line)
                    
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

                # code
            

                # code = re.compile(self.patterns["code"])
                # print("Before change code",line)
                # if code.search(line):
                #     line =self.code(code,line)
                #     print("After change code",line)
            
                if line.strip() != "": #check if line is not empty
                    if "<ul>" not in line and "</ul>" not in line:
                        if "<li>" not in line and "</li>" not in line:
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
                        self.results += '\n'+ line+'\n'
            else:
                
                self.results += '\n'+ codeline +'\n'
 
            print("RESULTS",self.results)  
        return self.results
            


        
            
                



    