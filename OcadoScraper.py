#import modules
#python -m pip install requests
#python -m pip install beautifulsoup4
import requests
from bs4 import BeautifulSoup
def __init__(self):
    pass
class os(BeautifulSoup):
    def __init__(self, search):
        #scrape page and create 'soup'
        self.page = requests.get("https://www.ocado.com/search?entry="+search)
        super().__init__(self.page.content, "html.parser")
        #remove javascript
        for element in self.findAll('script'):
            element.extract()
        #self.results = self.find(class_="fops fops-regular fops-shelf")
        #find all items
        self.elements = self.find_all(class_="fops-item fops-item--cluster")
        self.links = []
        self.items = []
        self.prices = []
        self.images = []
        self.reviews = []
        try:
            for self.element in self.elements:
                #find information
                self.title_element = self.element.find(class_="fop-title")
                self.step1 = self.element.find(class_="fop-contentWrapper")
                self.link_element = self.step1.find("a")
                self.image_element = self.element.find("img", class_="fop-img")
                self.review_element = self.element.find("span", class_="fop-rating-inner")
                #3 different places the price may be found
                try:
                    self.price_element = self.element.find(class_="fop-price price-offer")
                    "" + self.price_element.text
                except:
                    try:
                        self.price_element = self.element.find(class_="fop-price fop-value-delivered price-offer")
                        "" + self.price_element.text
                    except:
                        self.price_element = self.element.find(class_="fop-price")
                        #print("yes")
                #print(self.title_element.text+"\n"+self.price_element.text)
                self.items.append(self.title_element.text)
                curprice = self.price_element.text.strip("-").strip(" ").strip("£")
                #https://stackabuse.com/python-check-if-string-contains-substring/
                #format price correctly; just numbers
                if "p" in curprice:
                    curprice = "0."+curprice.strip("p")
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
                self.images.append(self.image_element.get("src"))
                try:
                    self.reviews.append(self.review_element.get("title")[8:-9])
                except:
                    self.reviews.append("N/A")
        except AttributeError:
            pass
        self.out = []
        for item in range(0, len(self.items)):
            #add each item to list of results
            self.out.append([self.items[item], self.prices[item], "https://www.ocado.com"+self.links[item], "Ocado", "https://www.ocado.com"+self.images[item], self.reviews[item]])
    def outpt(self):
        return self.out
class update(BeautifulSoup):
    #gets latest values for price and rating for an item
    def __init__(self, itemList):
        #get item's page
        self.page = requests.get(itemList[2])
        super().__init__(self.page.content, "html.parser")
        #remove javascrpt
        for element in self.findAll('script'):
            element.extract()
        #get result, price
        self.results = self.find("div", class_="main-app-view")
        self.price_element = self.results.find("meta", attrs={"itemprop":"price"})
        self.review_element = self.results.find("meta", attrs={"itemprop":"ratingValue"})
        curprice = self.price_element.get("content")
        curReview = self.review_element.get("content")
        #make sure price is properly formatted
        dotloc = curprice.find(".")
        if len(curprice) < dotloc+3:
            curprice = curprice+"0"
        self.newItemList = itemList
        self.newItemList[1] = curprice
        self.newItemList[5] = curReview
    def outpt(self):
        #output item with updated price and rating
        return self.newItemList
def getdetails(item):
    #scrape page and create 'soup'
    page = requests.get(item)
    soup = BeautifulSoup(page.content, "html.parser")
    #removes javascript
    for element in soup.findAll('script'):
        element.extract()
    try:
        #get description content by getting all text from the info-content div
        detailsElement = soup.find("div", class_="bop-info__content")
        #https://stackoverflow.com/questions/1936466/how-to-scrape-only-visible-webpage-text-with-beautifulsoup
        detailsAll = detailsElement.find_all(string=True)
        details = ""
        #split paragraphs
        for element in detailsAll:
            details = details+element+"\n"
    except:
        details = ""
    return details
