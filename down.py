
import urllib.request
import re

def download_page(pageUrl, anecdote):
    try:
        req = urllib.request.Request(pageUrl, headers={'User-Agent':user_agent})
        with urllib.request.urlopen(req) as response:
            page = response.read().decode('utf-8')
    except:
        print('Error at', pageUrl)
        return
    match = re.findall(anecdote, page)[1:]
    for i in match:
        i = re.sub('<br>', ' ', i)
        #print(i[18:-4])
        file.write(i[18:-4] + '\n\n')

file = open("corp.txt", 'a', encoding = "UTF-8")

commonUrl = 'http://vse-shutochki.ru/anekdoty/'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'

anecdote = re.compile("<div class=\"post\">.*?<hr", re.DOTALL)

for i in range(1, 1136):
    pageUrl = commonUrl + str(i)
    download_page(pageUrl, anecdote)  
file.close()