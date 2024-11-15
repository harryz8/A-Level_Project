class ro():
    def __init__(self, results):
        #create results object
        self.data = results
        self.current = "original"
        self.original = []
        for item in results:
            self.original.append(item)
    def outpt(self):
        return self.data
    def sort_price(self, startLow=True):
        #sort results by price
        if startLow == True:
            #insertion sort, low to high
            for pos in range(1, len(self.data)):
                currentValue = float(self.data[pos][1].strip("£"))
                while pos > 0 and float(self.data[pos-1][1].strip("£"))>currentValue:
                    oldval = self.data[pos]
                    self.data[pos] = self.data[pos-1]
                    pos = pos-1
                    self.data[pos] = oldval
            self.current = "PriceLow"
        elif startLow == False:
            #insertion sort, high to low
            for pos in range(1, len(self.data)):
                currentValue = float(self.data[pos][1].strip("£"))
                while pos > 0 and float(self.data[pos-1][1].strip("£"))<currentValue:
                    oldval = self.data[pos]
                    self.data[pos] = self.data[pos-1]
                    pos = pos-1
                    self.data[pos] = oldval
            self.current = "PriceHigh"
    def sort_rating(self, startLow=True):
        #sort results by rating
        if startLow == True:
            #insertion sort, low to high
            naListNums = []
            naList = []
            #add location of all N/As to naListNums
            for pos in range(0, len(self.data)):
                if self.data[pos][5] == "N/A":
                    naListNums.append(pos)
            #https://www.programiz.com/python-programming/methods/list/reverse
            naListNums.reverse()
            #remove N/As from results and add to naList, starting from the last N/A so to not disrupt the indexing of later ones
            for pos in naListNums:
                naList.append(self.data.pop(pos))
            for pos in range(1, len(self.data)):
                currentValue = float(self.data[pos][5])
                while pos > 0 and float(self.data[pos-1][5])>currentValue:
                    oldval = self.data[pos]
                    self.data[pos] = self.data[pos-1]
                    pos = pos-1
                    self.data[pos] = oldval
            self.data = self.data+naList
            self.current = "RatingLow"
        elif startLow == False:
            #insertion sort, high to low
            naListNums = []
            naList = []
            #add location of all N/As to naListNums
            for pos in range(0, len(self.data)):
                if self.data[pos][5] == "N/A":
                    naListNums.append(pos)
            #https://www.programiz.com/python-programming/methods/list/reverse
            naListNums.reverse()
            #remove N/As from results and add to naList, starting from the last N/A so to not disrupt the indexing of later ones
            for pos in naListNums:
                naList.append(self.data.pop(pos))
            for pos in range(1, len(self.data)):
                currentValue = float(self.data[pos][5])
                while pos > 0 and float(self.data[pos-1][5])<currentValue:
                    oldval = self.data[pos]
                    self.data[pos] = self.data[pos-1]
                    pos = pos-1
                    self.data[pos] = oldval
            self.data = self.data+naList
            self.current = "RatingHigh"
    def shop_only(self, shop):
        #sort results so only shows results of specified shop
        oldData = self.data
        self.data = []
        for item in oldData:
            if item[3] == shop:
                self.data.append(item)
    def alphabeticalShop(self):
        #sort results to alphebetical order on the store name
        oldData = self.data
        self.data = []
        for item in oldData:
            if item[3] == "B & Q":
                self.data.append(item)
        for item in oldData:
            if item[3] == "JD Sports":
                self.data.append(item)
        for item in oldData:
            if item[3] == "Marks and Spencer":
                self.data.append(item)
        for item in oldData:
            if item[3] == "Ocado":
                self.data.append(item)
    def reinstateOriginal(self):
        self.current = "Original"
        self.data = []
        for item in self.original:
            self.data.append(item)
