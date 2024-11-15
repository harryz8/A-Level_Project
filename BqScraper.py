#python -m pip install requests
#python -m pip install beautifulsoup4
#import modules
import requests
from bs4 import BeautifulSoup
def __init__(self):
    pass
class bq(BeautifulSoup):
    def __init__(self, search):
        #scrape page
        self.page = requests.get("https://www.diy.com/search?term="+search)
        #make it into a 'soup'
        super().__init__(self.page.content, "html.parser")
        for element in self.findAll('script'):
            element.extract()
        self.results = self.find("ul", class_="_40158784 _6b5bb6a7 _190cafcd")
        #find all results
        self.elements = self.results.find_all("li")
        #define variables
        self.links = []
        self.items = []
        self.prices = []
        self.images = []
        self.out = []
        self.reviews = []
        try:
            for self.element in self.elements:
                #find information
                self.title_element = self.element.find("p", attrs={"data-test-id":"productTitle"})
                self.price_element = self.element.find("div", attrs={"data-test-id":"product-primary-price"})
                self.image_element = self.element.find("img", attrs={"data-test-id":"image"})
                self.review_element = self.element.find("div", attrs={"data-test-id":"RatingStars"})
                curprice = self.price_element.text.strip().strip("-").strip(" ").strip("£")
                #https://stackabuse.com/python-check-if-string-contains-substring/
                #format price string just to numbers
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
                self.link_element = self.element.find("a", attrs={"data-test-id":"product-panel-main-section"})
                self.links.append(self.link_element.get("href"))
                self.items.append(self.title_element.text)
                self.images.append(self.image_element.get("src"))
                #count stars to make rating value
                try:
                    self.stardivs = self.review_element.find_all("div")
                    reviewtotal = 0
                    for stardiv in self.stardivs:
                        stardiv = str(stardiv)
                        if stardiv.find("Full star") != -1:
                            reviewtotal = reviewtotal + 1
                        elif stardiv.find("Half star") != -1:
                            reviewtotal = reviewtotal + 0.5
                    self.reviews.append(str(reviewtotal))
                except:
                    self.reviews.append("N/A")
        except AttributeError and TypeError:
            pass
        for item in range(0, len(self.items)):
            #add item to the results list
            self.out.append([self.items[item], self.prices[item], "https://www.diy.com"+self.links[item], "B & Q", self.images[item], self.reviews[item]])
    def outpt(self):
        return self.out
class update(BeautifulSoup):
    #updates the price and review elements of item passed
    def __init__(self, itemList):
        self.page = requests.get(itemList[2])
        super().__init__(self.page.content, "html.parser")
        #remove javascript
        for element in self.findAll('script'):
            element.extract()
        #find review and price elements
        self.results = self.find("main", attrs={"data-test-id":"PageContent"})
        self.step1 = self.results.find("div", attrs={"data-test-id":"product-primary-price"})
        self.price_element = self.step1.find("div", class_="_5d34bd7a")
        self.review_element = self.results.find("div", attrs={"data-test-id":"RatingStars"})
        curprice = self.price_element.text.strip("-").strip(" ").strip("£")
        #https://stackabuse.com/python-check-if-string-contains-substring/
        #https://www.techiedelight.com/find-index-character-python-string/#:~:text=Find%20index%20of%20a%20character%20in%20a%20Python,function%20...%204%204.%20Using%20more_itertools.locate%20%28%29%20function
        #format price to just numbers
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
        self.newItemList = itemList
        #count stars to get rating
        try:
            self.stardivs = self.review_element.find_all("div")
            reviewtotal = 0
            for stardiv in self.stardivs:
                stardiv = str(stardiv)
                if stardiv.find("Full star") != -1:
                    reviewtotal = reviewtotal + 1
                elif stardiv.find("Half star") != -1:
                    reviewtotal = reviewtotal + 0.5
            self.newItemList[5] = str(reviewtotal)
        except:
            self.newItemList[5] = "N/A"
        self.newItemList[1] = curprice
    def outpt(self):
        return self.newItemList
def getdetails(item):
    #gets description for specific item
    page = requests.get(item)
    soup = BeautifulSoup(page.content, "html.parser")
    #removes javascript
    for element in soup.findAll('script'):
        element.extract()
    try:
        detailsElement = soup.find("div", id="product-details")
        #https://stackoverflow.com/questions/1936466/how-to-scrape-only-visible-webpage-text-with-beautifulsoup
        #gets all visible text
        detailsAll = detailsElement.find_all(string=True)
        details = ""
        for element in detailsAll:
            #splits text with newlines
            details = details+element+"\n"
    except:
        details = ""
    return details
