#program to download files on web page and get the count of words in each PDF file
#
# Author: Shravani Ramisetty
# Dated: 11/13/2017
#
from bs4 import BeautifulSoup
import urllib2
import urlparse
import os
import io
import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import nltk
reload(sys)
sys.setdefaultencoding('utf8')


#function to get text from PDF files
def getWordCount(file_name):
    output = io.BytesIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)
    inFile = open(file_name, 'rb')
    for page in PDFPage.get_pages(inFile, set()):
        interpreter.process_page(page)
        fileContent = output.getvalue()
        output.flush
    inFile.close()
    converter.close()
    output.close
    words= nltk.word_tokenize(fileContent)
    fdist1 = nltk.FreqDist(words)
    total= fdist1['travel'] + fdist1['Travel']+ fdist1['TRAVEL']
    totalList['File Name']= fileName
    totalList['Word Count']=total

url = "http://ir.expediainc.com/annuals.cfm"
request = urllib2.Request(url)
response = urllib2.urlopen(request)
soup = BeautifulSoup(response)
for i in soup.findAll('div', {'class': 'post-content'}):
    soupVar = BeautifulSoup(str(i), "html.parser")
    # print(soupVar)
    filesList= soupVar.find('table', {'class': 'dataTable'})
    soupFilesList = BeautifulSoup(str(filesList), "html.parser")
    # print(soupfilesList)
    files = soupFilesList.find('a', {'class': 'docList'})
    fileName= files.string.strip()
    print(fileName)
    processingFileURLs = set()
    response=[]
    totalList={}
    for node in soup.findAll('a', href=True):
        node['href'] = urlparse.urljoin(url, node['href'])
        urlSplit = os.path.splitext(os.path.basename(node['href']))

        if urlSplit[1].lower() == '.pdf' and node['href'] not in processingFileURLs:
            parsed = urlparse.urlparse(node['href'])
            fileName = urlparse.parse_qs(parsed.query)['filename'][0]
            with open(fileName, 'wb') as f:
                current = urllib2.urlopen(node['href'])
                f.write(current.read())
            print("Downloaded ", fileName)
            getWordCount(fileName)
response.append(totalList)
print(response)


