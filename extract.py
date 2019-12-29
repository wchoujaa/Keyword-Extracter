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

stop_words = []

f = open("french.txt", "r")

for x in f:
  stop_words.append(x.rstrip())

f.close()

root = Tk()
 

def openPdf(filename):
    pdfFileObj = open(filename, 'rb')  # open allows you to read the file
    # The pdfReader variable is a readable object that will be parsed
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    # discerning the number of pages will allow us to parse through all the pages
    num_pages = pdfReader.numPages
    count = 0
    global text 
    text = ""


    while count < num_pages:  # The while loop will read each page
        pageObj = pdfReader.getPage(count)
        count += 1
        text += pageObj.extractText()

    # Below if statement exists to check if the above library returned #words. It's done because PyPDF2 cannot read scanned files.

    if text != "":
        text = text
    # If the above returns as False, we run the OCR library textract to #convert scanned/image based PDF files into text

 
    for line in text:
        table.insert(END, line)
    warnings.filterwarnings("ignore")

 
 # This is where we lauch the file manager bar.
def OpenFile():
    name = askopenfilename(initialdir=" %UserProfile%/Desktop/",
                           filetypes=(("pdf", "*.pdf"), ("All Files", "*.*")),
                           title="Choose a file."
                           )
     # Using try in case user types in unknown file or closes without choosing a file.
    openPdf(name)
 



def onClick():
    table.delete(1.0, END)

def onKeywordClick():
    text = table.get("1.0",END)
    values = keywords(text=text, split='\n', scores=True)

    data = pd.DataFrame(values, columns=['keyword', 'score'])
    data = data.sort_values('score', ascending=False)
    table.delete(1.0, END)
    for x in values:
        if(x[0] not in stop_words):
            table.insert(END, x[0] + "\n")
    table.pack()

root.geometry("500x600")

## display title
Title = root.title("File Opener")
label = ttk.Label(root, text="Keyword Extractor",
                  foreground="red", font=("Helvetica", 16))
label.pack()

# Menu Bar
menu = Menu(root)
root.config(menu=menu)
file = Menu(menu)
file.add_command(label='Open', command=OpenFile)
file.add_command(label='Exit', command=lambda: exit())
menu.add_cascade(label='File', menu=file)

## display button
clearB = Button(root, text="clear", command=onClick)
clearB.pack(side=BOTTOM)
keywordB = Button(root, text="keyword", command=onKeywordClick)
keywordB.pack(side=BOTTOM)

## display text area
table = Text(root)
for x in range(10):
    table.insert(END,  "\n")
table.pack()


root.mainloop()
