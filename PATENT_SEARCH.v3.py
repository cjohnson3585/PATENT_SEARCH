# 01/30/20 Added target_* prefix to output files when only searching for a specific patent number
# 01/30/20 Created CREATE_RECOMMENDER_DATA_FILE.py and RECOMMENDER.py
# 10/25/19 Added in output file .csv for patent history
# 10/23/19 Added in ability to create directory (./PATENT_DIR/) which stores all frequency plots (.pdf) and csv file of keyword and frequency (.csv)
# 10/23/19 Added in get_pdf_reader function to read and display keyword frequency if pdf is supplied
# 10/23/19 Added in input.txt file for changing variables
# 10/07/19 Added in functions for scraping and tokenizing. Scrapes Patentsview,tokenizes USPTO
# 10/02/19 Updated with requests
# 03/11/19 Script to scrape patentsview.org API for fields, adopted from previous work
#
#
import json
import requests
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
from bs4 import BeautifulSoup as bs
import sys
import PyPDF2
import os

#function for scraping article w/ patent number on the USPTO website                                                                                                                                               
def get_url_content(patnum):
    url2 = "http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO1&Sect2=HITOFF&d=PALL&p=1&u=%2Fnetahtml%2FPTO%2Fsrchnum.htm&r=1&f=G&l=50&s1="+patnum+".PN.&OS=PN/"+patnum+"&RS=PN/"+patnum
    wordss = [] #--> ARRAY TO RETURN CONTENT                                                                                                                             
    page = requests.get(url2)
    soup = bs(page.text,features='html.parser')
    txt = soup.find_all(string=True)
    for l in range(len(txt)):
        wordss.append(txt[l])
        aa = ' '.join(wordss)
    return aa


#Function for tokenizing and plot keyword frequency
def get_token_plot(ff,pnum):
    tokens = word_tokenize(ff)
    punctuations = ['(',')',';',':','[',']',',','said']
    stop_words = stopwords.words('english')#We initialize the stopwords variable                                                                                          
    keywords = [word for word in tokens if not word in stop_words and not word in punctuations and len(word) >= 4]
    
    counts = Counter(keywords)
    kw = [];cnt = []
    for li in counts.most_common(25):
        kw.append(li[0]),cnt.append(li[1])
    pos = nltk.pos_tag(kw)
    d = {'KEYWORD':kw, 'COUNT':cnt, 'POS':pos}
    df = pd.DataFrame(data=d)
#    print(df)
#    for k in range(25):
#        print(df['KEYWORD'][k],df['COUNT'][k])
    fig,ax = plt.subplots(figsize=(25,15))
    fig.suptitle("Patent Number:"+str(pnum), fontsize=16)
    fig.autofmt_xdate()
    ax.bar(df['KEYWORD'], df['COUNT'])
#create pdf and log file for keyword frequency with format <patent_num>.pdf and <patent_num>.txt
    if patent_number:
        m = open('./PATENT_DIR/target_'+str(pnum)+'.csv','w')
    else:
        m = open('./PATENT_DIR/'+str(pnum)+'.csv','w')#--> name of file for output
    m.write('KEYWORD,COUNT'+'\n')
    for l in range(25):
        m.write(str(df['KEYWORD'][l])+','+str(df['COUNT'][l])+'\n')
    m.close()
    if patent_number:
        plt.savefig('./PATENT_DIR/target_'+str(pnum)+'.pdf', format='pdf')
    else:
        plt.savefig('./PATENT_DIR/'+str(pnum)+'.pdf', format='pdf')
        
    





#function for reading a pdf and plotting keyword frequency
def get_pdf_reader(filename1):
    stemmer = filename1.strip('"')
    stem = stemmer.rstrip('.pdf')

    #open allows you to read the file                                                                                                                                       
    pdfFileObj = open(filename1.strip('"'),'rb')

#The pdfReader variable is a readable object that will be parsed                                                                                                           
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

#discerning the number of pages will allow us to parse through all pages                                                                                                    
    num_pages = pdfReader.numPages
    count = 0
    text = ""

#The while loop will read each page                                                                                                                                        
    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count +=1
        text += pageObj.extractText()

    tokens = word_tokenize(text)
    punctuations = ['(',')',';',':','[',']',',']

#We initialize the stopwords variable                                                                                                                                       
    stop_words = stopwords.words('english')

#We create a list comprehension which only returns a list of words #that are #NOT IN stop_words                                                                          
    keywords = [word for word in tokens\
            if not word in stop_words\
            and not word in punctuations and len(word)\
            >= 4]

#count and itemize the keywords                                                                                                                                           
    counts = Counter(keywords)
    kw = [];cnt = []
    for li in counts.most_common(25):
        kw.append(li[0]),cnt.append(li[1])
    pos = nltk.pos_tag(kw)
    d = {'KEYWORD':kw, 'COUNT':cnt, 'POS':pos}
    df = pd.DataFrame(data=d)
#    print(df)
#    print(stem)
    fig,ax = plt.subplots(figsize=(25,15))
    fig.autofmt_xdate()
    ax.bar(df['KEYWORD'], df['COUNT'])
    m = open('./PATENT_DIR/'+str(stem)+'.csv','w')
    for l in range(25):
        m.write(str(df['KEYWORD'][l])+','+str(df['COUNT'][l])+'\n')
    m.close()
    plt.savefig('./PATENT_DIR/'+str(stem)+'_kw_plot.pdf', format='pdf')



#----------------------------------------------------------------------------------------------------------------------------------------------------------
#READ IN INPUT FILE VARIABLES. DO NOT CHANGE THINGS BELOW, ONLY IN INPUT FILE (input.txt)
#----------------------------------------------------------------------------------------------------------------------------------------------------------
print('')
print('PATENT_SEARCH.py-------------------')
myvars = {}
with open("./input.txt") as myfile:
    for line in myfile:
        if line and not line.startswith('#'):
            name, var = line.partition("=")[::2]
            myvars[name.strip()] = str(var.strip())
myfile.close()
#----------------------------------------------------------------------------------------------------------------------------------------------------------


#Create directory to hold pdfs and .txt for patents
direc = "./PATENT_DIR"
if not os.path.exists(direc):
    os.makedirs(direc)
    print("Created: ./PATENT_DIR/...")

#OUTPUT FILE PREFIX
try:
    prefix = myvars['PREFIX']
except:
    prefix = 'output_search'

#SEARCH WORD for TITLE
try:
    search_title = myvars['SEARCH_TITLE']
except:
    search_title = '"dog"'

#SEARCH WORD for ABSTRACT
try:
    search_abs = myvars['SEARCH_ABS']
except:
    search_abs = '"wheel"'


#PATENT NUMBER INPUT (IF USED)
try:
    patent_number = myvars['PATENT_NUMBER']
except:
    patent_number = ""

#PDF to read (IF USED)
try:
    pdf_to_read = myvars['PDF_TO_READ']
except:
    pdf_to_read = ""

#MAX patents to return and plot when using abstract/title method
try:
    max_patents = myvars['MAX_PATENTS']
except:
    max_patents = 2


if len(pdf_to_read) > 4:
    try:
        get_pdf_reader(pdf_to_read)
    except:
        print("ERROR: Can not find pdf with file name "+pdf_to_read+"...")
    sys.exit()


fields = ['"patent_number"','"patent_title"','"patent_date"','"inventor_last_name"']
fields = ",".join(fields)


if patent_number:
    query = '"patent_number"'+":"+patent_number
else:
    query = '"_and"'+":[{"+'"_text_any"'+":{"+'"patent_title"'+":"+search_title+"}}"+",{"+'"_text_any"'+":{"+'"patent_abstract"'+":"+search_abs+"}}]"



#option parameters
k = 1
opt1 = ['"page"',str(k)]
opt1 = ":".join(opt1)
opt2 = ['"per_page"','1000']      #-->set this for the amount of records per page you want back
opt2 = ":".join(opt2)
options = opt1+","+opt2

#Get the data from the url in json format
url = "http://www.patentsview.org/api/patents/query?q={"+query+"}&f=["+fields+"]&o={"+options+"}"
f = open(direc+'/'+prefix+'.json','w')     #--> name of file for output.json
q = open(direc+'/'+prefix+'.csv','w')     #--> name of file for output.csv
r = requests.get(url)

#print it out to a file
f.write(r.text)
f.close()
print('Created: ',direc+'/'+prefix+'.json as a logfile for results...')
print('Created: ',direc+'/'+prefix+'.csv as a logfile for results...')

df = pd.read_json(direc+'/'+prefix+'.json')


if patent_number:
    print(df['patents'][0]['patent_number'],df['patents'][0]['patent_date'],df['patents'][0]['patent_title'])
    q.write(str(df['patents'][0]['patent_number'])+','+str(df['patents'][0]['patent_date'])+','+str(df['patents'][0]['patent_title']))
    q.close()
    patnum = df['patents'][0]['patent_number']
    ff = get_url_content(patnum)
    get_token_plot(ff,patnum)
else:
    for j in range(int(max_patents)):#len(df)):
        print(df['patents'][j]['patent_number'],df['patents'][j]['patent_date'],df['patents'][j]['patent_title'])
        q.write(str(df['patents'][j]['patent_number'])+','+str(df['patents'][j]['patent_date'])+','+str(df['patents'][j]['patent_title'])+'\n')
        patnum = df['patents'][j]['patent_number']
        ff = get_url_content(patnum)
        get_token_plot(ff,patnum)
    q.close()

#----------------------------------------------------------------------------------------------------------------------------------------------------------
