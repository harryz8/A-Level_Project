#python -m pip install requests
#python -m pip install beautifulsoup4
import requests
from bs4 import BeautifulSoup
def __init__(self):
    pass
class jd(BeautifulSoup):
    def __init__(self, search):
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        #scrape webpage
        self.page = requests.get("https://www.jdsports.co.uk/search/"+search, headers=self.headers)
        #make 'soup'
        super().__init__(self.page.content, "html.parser")
        #for element in self.findAll('script'):
        #    element.extract()
        self.results = self.find("ul", id="productListMain")
        #find each item
        self.elements = self.results.find_all("li")
        self.links = []
        self.items = []
        self.prices = []
        self.images = []
        self.reviews = []
        #try:
        for self.element in self.elements:
            #print(self.element)
            #find information
            self.step1 = self.element.find("span", class_="itemTitle")
            self.title_element = self.step1.find("a")
            #two options to get the price element
            try:
                self.price_element = self.element.find("span", class_="pri")
                "" + self.price_element.text
                if self.price_element.text == "":
                    raise Exception
            except:
                self.step2 = self.element.find("span", class_="now")
                self.price_element = self.step2.find("span", attr={"data-oi-price"})
            self.link_element = self.step1.find("a")
            self.image_element = self.element.find("source")
            #print(self.review_element)
            self.items.append(self.title_element.text)
            curprice = self.price_element.text.strip("-").strip(" ").strip("£")
            #https://stackabuse.com/python-check-if-string-contains-substring/
            #https://www.techiedelight.com/find-index-character-python-string/#:~:text=Find%20index%20of%20a%20character%20in%20a%20Python,function%20...%204%204.%20Using%20more_itertools.locate%20%28%29%20function
            #format the price so just numbers
            if "p" in curprice:
                curprice = "0."+curprice.strip("p")
            if curprice[0] == "\n":
                curprice = curprice[7:-18]
            while True:
                try:
                    float(curprice)
                    break
                except:
                    curprice = curprice[:-1]
                    if len(curprice) == 0:
                        break
            self.prices.append(curprice)
            self.links.append(self.link_element.get("href"))
            #get picture as jpg
            origpic = self.image_element.get("data-srcset")
            origpic = origpic.split(" ")
            curpic = origpic[0][:-4]+"jpg"
            self.images.append(origpic[0])
            self.reviews.append("N/A")
        #except AttributeError:
        #    pass
        self.out = []
        for item in range(0, len(self.items)):
            #add item to results list
            self.out.append([self.items[item], self.prices[item], "https://www.jdsports.co.uk"+self.links[item], "JD Sports", self.images[item], self.reviews[item]])
    def outpt(self):
        return self.out
class update(BeautifulSoup):
    def __init__(self, itemList):
        #get page and make 'soup'
        self.page = requests.get(itemList[2])
        super().__init__(self.page.content, "html.parser")
        for element in self.findAll('script'):
            element.extract()
        self.results = self.find("div", class_="productPage")
        #get price
        self.price_element = self.results.find("span", class_="pri")
        curprice = self.price_element.text.strip("-").strip(" ").strip("£")
        #https://stackabuse.com/python-check-if-string-contains-substring/
        #https://www.techiedelight.com/find-index-character-python-string/#:~:text=Find%20index%20of%20a%20character%20in%20a%20Python,function%20...%204%204.%20Using%20more_itertools.locate%20%28%29%20function
        #format price correctly as just numbers
        if "p" in curprice:
            curprice = "0."+curprice.strip("p")
        if curprice[0] == "\n":
            curprice = curprice[7:-18]
        while True:
            try:
                float(curprice)
                break
            except:
                curprice = curprice[:-1]
                if len(curprice) == 0:
                    break
        self.newItemList = itemList
        self.newItemList[1] = curprice
    def outpt(self):
        return self.newItemList
def getdetails(item):
    #scrape page and make 'soup'
    page = requests.get(item)
    soup = BeautifulSoup(page.content, "html.parser")
    #removes javascript
    for element in soup.findAll('script'):
        element.extract()
    try:
        #get description by getting all visible text in this section
        detailsElement = soup.find("div", class_="tab-info")
        #https://stackoverflow.com/questions/1936466/how-to-scrape-only-visible-webpage-text-with-beautifulsoup
        detailsAll = detailsElement.find_all(string=True)
        #remove spare tabs and new lines
        detailsClean = []
        details = ""
        for element in detailsAll:
            element = element.strip("\n").strip("\t").strip("\n").strip("\n").strip("\n").strip("\n")
            detailsClean.append(element)
        #add newlines where needed
        for element in detailsClean:
            if element != "" and element != " ":
                details = details+element.strip("\t")+"\n"
    except:
        details = ""
    return details
