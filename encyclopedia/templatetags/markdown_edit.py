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

            
        }
        # self.substitute_patterns ={
        #     "li_opentag":"\n<li>\n",
        #     "li_closetag":"\n</li>\n",
        #     "ul_li_tag":"\n<ul>\n<li>\2</li>\n",
        #     "hr_tag" : "\n<hr>\n",
        #     "bold":"<strong>\2</strong>",
        #     "italic":"<em>\2</em>",
        #     "strikethrough":"<s>\2</s>",
        # }

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
                line = unordered_list.sub(r"\n<li>\2</li>\n",line)

            else:
                #first li in the list
                line = unordered_list.sub(r"\n<ul>\n<li>\2</li>\n",line)
                self.ultag_is_open = True #set ul tag to open
                self.previouslinespace = self.currentlinespace

        #nested list    
        elif 2<=self.currentlinespace-self.previouslinespace<=5: 
           
            if self.ultag_is_open == True: #not a first li in the list

                if self.sub_ultag_is_open :
                    if self.count >= 1:
                        line = unordered_list.sub(r"\n<ul>\n<li>\2</li>\n",line) 
                    line = unordered_list.sub(r"\n<li>\2</li>\n",line) 
                else:
                   
                    self.sub_ultag_is_open = True
                    self.count +=1
                    line = unordered_list.sub(r"\n<ul>\n<li>\2</li>\n",line)
            else:

                line = unordered_list.sub(r"\n<ul>\n<li>\2</li>\n",line)
                self.ultag_is_open = True 
            self.previouslinespace = self.currentlinespace

        #nested new list
        else: #self.currentlinespace < self.previouslinespace:

            #close all previous nested list
            line =self.close_list(line)

            line = unordered_list.sub(r"<ul>\n<li>\2</li>",line)
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
        line = hr.sub("\n<hr>\n",line)
        return line
    
    #Bold
    def bold(self,bold,line):
        line = bold.sub(r"\n<strong>\2</strong>\n",line)
        return line

    #Italic
    def italic(self,italic,line):
        line = italic.sub(r"\n<em>\2</em>\n",line)
        return line

    #Strikethrough
    def strikethrough(self,strikethrough,line):
        line = strikethrough.sub(r"\n<s>\2</s>\n",line)
        return line

    #Bold and italic
    def bold_and_italic(self,bold_and_italic,line):
        line = bold_and_italic.sub(r"\n<strong><em>\2</em></strong>\n")
        return line
    #code
    def code(self,code,line):
        line = code.sub(r"\n<pre><code>\1</code></pre>\n",line)
        print("After change pre-code",line)
        return line
    

    # markdown to html main function
    def markdown_parser(self,markdown_string):
        print("Coming inside of markdown_parser")
        for line in markdown_string.splitlines():
            print("LINE",line)
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


            code = re.compile(self.patterns["code"])
            print("Before change code",line)
            if code.search(line):
                line =self.code(code,line)
            print("After change code",line)
            
            if line.strip() != "": #check if line is not empty
                if "<ul>" not in line and "</ul>" not in line:
                    if "<li>" not in line and "</li>" not in line:
                        if "<h" not in line and "<h" not in line:
                            if "<code>" and "</code>" not in line:
                                self.results+='\n'+"<p>"+line +"</p>"+'\n'
                            else:
                                self.results += '\n'+ line +'\n'
                        else:
                            self.results += '\n'+ line +'\n'
                    else:
                        self.results += '\n'+ line +'\n'
                else:
                    self.results += '\n'+ line+'\n'
 
            print("RESULTS",self.results)  
        return self.results
            


        
            
                



    