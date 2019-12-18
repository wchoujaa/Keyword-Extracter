from gensim.summarization import keywords
import warnings
import pandas as pd
import numpy as np
import PyPDF2
import textract
import re
from tkinter import *  # from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import wikipedia

root = Tk()
root.geometry("500x600")
Title = root.title( "File Opener")
label = ttk.Label(root, text ="Keyword Extractor",foreground="red",font=("Helvetica", 16))
label.pack()

def openPdf(filename):
    pdfFileObj = open(filename,'rb')               #open allows you to read the file
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)   #The pdfReader variable is a readable object that will be parsed
    num_pages = pdfReader.numPages                 #discerning the number of pages will allow us to parse through all the pages


    count = 0
    text = ""
                                                            
    while count < num_pages:                       #The while loop will read each page
        pageObj = pdfReader.getPage(count)
        count +=1
        text += pageObj.extractText()
    
    #Below if statement exists to check if the above library returned #words. It's done because PyPDF2 cannot read scanned files.

    if text != "":
        text = text
    #If the above returns as False, we run the OCR library textract to #convert scanned/image based PDF files into text

    else:
        text = textract.process('http://bit.ly/epo_keyword_extraction_document', method='tesseract', language='eng')

    warnings.filterwarnings("ignore")

    filename ='JavaBasics-notes.pdf' 

    values = keywords(text=text,split='\n',scores=True)

    data = pd.DataFrame(values,columns=['keyword','score'])
    data = data.sort_values('score',ascending=False)

    t = Text(root)
    for x in values:
        t.insert(END, x[0] + ', ')
    t.pack()   

    t = Text(root)
    for x in values:
        query = []
        try: 
            query = wikipedia.search(x[0], results=5)
        except:
            print("An exception occurred")
        print(x, query)
        if(len(query) > 0):
            t.insert(END, x[0] + '\n')
    t.pack()
    

#This is where we lauch the file manager bar.
def OpenFile():
    name = askopenfilename(initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
                           filetypes =(("pdf", "*.pdf"),("All Files","*.*")),
                           title = "Choose a file."
                           )
    print (name)
    #Using try in case user types in unknown file or closes without choosing a file.
    openPdf(name)



#Menu Bar

menu = Menu(root)
root.config(menu=menu)

file = Menu(menu)

file.add_command(label = 'Open', command = OpenFile)
file.add_command(label = 'Exit', command = lambda:exit())

menu.add_cascade(label = 'File', menu = file)

 
root.mainloop()