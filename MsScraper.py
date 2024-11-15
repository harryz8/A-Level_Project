#import modules
#python -m pip install requests
#python -m pip install beautifulsoup4
import requests
from bs4 import BeautifulSoup
def __init__(self):
    pass
class ms(BeautifulSoup):
    def __init__(self, search):
        #scrape page and make 'soup'
        self.page = requests.get("https://www.marksandspencer.com/MSFindItemsByKeyword?searchTerm="+search)
        super().__init__(self.page.content, "html.parser")
        #remove javascript
        for element in self.findAll('script'):
            element.extract()
        self.results = self.find("section", id="fesk-find")
        try:
            self.step1 = self.results.find("ul", class_="grid grid-4")
            #find items
            self.elements = self.step1.find_all("li")
        except AttributeError:
            pass
        self.links = []
        self.items = []
        self.prices = []
        self.out = []
        self.images = []
        self.reviews = []
        try:
            for self.element in self.elements:
                #find information
                self.title_element = self.element.find(class_="product__title")
                #print(self.title_element.get())
                self.firstreveiew = self.element.find("div", class_="product__details")
                try:
                    self.review_element = self.firstreveiew.find(class_="acc__text")
                except:
                    #self.review_element = None
                    pass
                try:
                    self.price_element = self.element.find(class_="price product__price--current")
                    curprice = self.price_element.text.strip("Current Price").strip("-").strip(" ").strip("£").strip("price£")
                except:
                    try:
                        self.price_element = self.element.find(class_="price price--reduced")
                        curprice = self.price_element.text.strip("Sale Price").strip("-").strip(" ").strip("£").strip("price£")
                    except AttributeError:
                        break
                #https://stackabuse.com/python-check-if-string-contains-substring/
                #format price so that just numbers remain
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
                self.link_element = self.element.find("a", class_="product__link")
                self.links.append(self.link_element.get("href"))
                self.items.append(self.title_element.text)
                #10 tries to get the picture from the item's page
                numResults = 0
                count = 0
                while numResults == 0:
                    self.page2 = requests.get("https://www.marksandspencer.com"+self.link_element.get("href"))
                    self.soup = BeautifulSoup(self.page2.content, "html.parser")
                    #print(self.soup)
                    for element in self.soup.findAll('script'):
                        element.extract()
                    self.do_first = self.soup.find("body")
                    self.do_second = self.do_first.find("div", id="sticky-header-after")
                    try:
                        self.do_third = self.do_second.find("ul", attrs={"tabindex":"0"})
                        self.results2 = self.do_third.find_all("li")
                        numResults = len(self.results2)
                    except:
                        numResults = 0
                    if numResults == 0:
                        try:
                            self.do_second = self.do_first.find("div", class_="container")
                            self.do_third = self.do_second.find("div", class_="image-grid__inner")
                            self.results3 = self.do_third.find_all("div", class_="image-grid__item")
                            self.results2 = self.results3[1:]
                            numResults = len(self.results2)
                        except:
                            numResults = 0
                    if numResults == 0:
                        try:
                            self.do_second = self.do_first.find("div", class_="container")
                            self.do_third = self.do_second.find("div", class_="image-grid__inner")
                            self.results3 = self.do_third.find_all("div", class_="image-grid__item")
                            self.results2 = self.results3
                            numResults = len(self.results2)
                        except:
                            numResults = 0
                    count = count+1
                    if count >= 10:
                        raise Exception("Maximum retries reached")
                if numResults > 0:
                    try:
                        self.image_element = self.results2[0].find("img", attrs={"data-tagg":"gallery-image"})
                        self.images.append(self.image_element.get("src").strip(" "))
                    except:
                        self.image_element = self.results2[0].find("img")
                        self.images.append(self.image_element.get("data-src").strip(" "))
                else:
                    self.images.append(None)
                if self.review_element == None:
                    self.reviews.append("N/A")
                else:
                    self.reviews.append(self.review_element.text[16:-9])
        except AttributeError and TypeError:
            pass
        for item in range(0, len(self.items)):
            #add item to results list
            self.out.append([self.items[item], self.prices[item], "https://www.marksandspencer.com"+self.links[item], "Marks and Spencer", self.images[item], self.reviews[item]])
    def outpt(self):
        return self.out
class update(BeautifulSoup):
    def __init__(self, itemList):
        #scrapes page and makes 'soup'
        self.page = requests.get(itemList[2])
        super().__init__(self.page.content, "html.parser")
        #removes javascript
        for element in self.findAll('script'):
            element.extract()
        self.results = self.find("div", id="detailsGrid")
        #find price and rating
        self.price_element = self.results.find("div", class_="price-container")
        #self.price_element = self.price1_element.find("span", class_="acc__text")
        self.review1_element = self.results.find("p", class_="star-rating")
        self.review_element = self.review1_element.find("span", class_="acc__text")
        #https://stackoverflow.com/questions/10993612/how-to-remove-xa0-from-string-in-python
        #format price correctly; just numbers
        curprice = self.price_element.text.strip("Sale Price")[:20].strip("-").strip(" ").strip("£").strip("price£").strip(" £").strip("  £").replace(u'\xa0', u' ').strip(" ")
        curResult = self.review_element.text[17:21]
        if "p" in curprice:
            curprice = "0."+curprice.strip("p")
        while True:
            try:
                float(curprice)
                break
            except:
                curprice = curprice.strip("\xa0")[:-1]
                if len(curprice) == 0:
                    break
        while " " in curprice:
            curprice = curprice[:-1]
        self.newItemList = itemList
        self.newItemList[1] = curprice
        self.newItemList[5] = curResult
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
        #gets details text
        detailsElement = soup.find("meta", attrs={"name":"description"})
        details = detailsElement.get("content")
    except:
        details = ""
    return details
