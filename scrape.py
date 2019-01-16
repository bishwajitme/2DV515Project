import re
import threading
import requests
import schedule
from bs4 import BeautifulSoup


class wikipediaPage:
    name = ''
    link = ''
    nodes = []
    group = 1
    text = []

data = {}
data['nodes'] = []
data['links'] = []
currentNodes = 0
maxNodes = 220
termine = False

initialUrl = "/wiki/Music"

def scrape(aUrl):
    global currentNodes
    currentNodes = currentNodes + 1
    pageurl= "https://en.wikipedia.org/"+aUrl
    page = requests.get(pageurl).text
    soup = BeautifulSoup(page, 'lxml')

    newPage = wikipediaPage()
    newPage.link = pageurl
    newPage.name = aUrl.split('/').pop()
    pageLinks = soup.find('div',id="mw-content-text").find_all('a')
    pageHrefs = list(set(list( map( getLink, pageLinks))))


    words = []
    for texts in soup.find_all('p'):
       words = words + pureText(texts)
    writeTexts(words, newPage.name)

    filteredPageHrefs = list(set(list(filter( lambda s: s!=None ,pageHrefs))))
    writeLinks(filteredPageHrefs, newPage.name)
    newPage.nodes = filteredPageHrefs
    global termine
    if not termine:
        explore = list(map(lambda x: addThread(x), newPage.nodes))


def addThread(urlToScrape):
    global maxNodes
    if currentNodes < maxNodes:
        if threading.activeCount()<200:
            print( currentNodes, maxNodes, "page to scrape: " , urlToScrape)
            ts = threading.Thread(target=scrape, args=[urlToScrape])
            ts.start()
    else:
        global termine
        termine = True



def getLink(a):
    if a.get("href") != None and a.get("href").startswith("/wiki/") and not a.get("href").endswith(".jpg" or ".JPG" or ".svg" or ".jpeg" or ".JPEG" or ".ogg"):
        return str(a.get("href"))

def remove_tags(text):
    return re.sub(r'[^\w]','', text)

def pureText(cell):
    references = cell.findAll("sup", {"class": "reference"})
    if references:
        for ref in references:
            ref.extract()

    # Strip main references from the cell
    references = cell.findAll("ol", {"class": "references"})
    if references:
        for ref in references:
            ref.extract()


    # Strip sortkeys from the cell
    sortkeys = cell.findAll("span", {"class": "sortkey"})
    if sortkeys:
        for ref in sortkeys:
            ref.extract()

    # Strip footnotes from text and join into a single string
    text_items = cell.findAll(text=True)
    no_footnotes = [text for text in text_items if text[0] != '[']
    puretext = ''.join(no_footnotes)
    return puretext.split(" ")

def writeLinks(links, filename):
    f = open('data/Links/' + filename, "w+")
    for x in links:
        f.write(x + "\r\n")
    f.close()

def writeTexts(newwords, filename):
    wf = open('data/Words/' + filename, "w+")
    for sword in newwords:
        if(len(remove_tags(sword))>2):
            enWord = remove_tags(sword)
            wf.write(enWord + " ")
    wf.close()

def log():
    #print("number of active threads: ", threading.activeCount())
    #print("time: ", time.clock())
    print(termine)


scrape(initialUrl)


schedule.every(1).seconds.do(log)

while True:
    print "SCRAPING DONE"
    break

tsc = threading.Thread(target=scrape, args=[initialUrl])
tsc.start()