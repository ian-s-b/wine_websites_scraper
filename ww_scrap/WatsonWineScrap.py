from bs4 import BeautifulSoup
import requests
import csv

class WWScrap():
    """This class is intended to scrap the https://www.watsonswine.com/ website"""

    url = "https://www.watsonswine.com"
    h = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
    req='/wine-search?q='

    def __init__(self, search_word):
        self.search_word = search_word
        self.searchPage = WWScrap.url + WWScrap.req + self.search_word
        self.actualPage = self.findNextPage(self.searchPage)
        try:
            self.actualPage = self.actualPage.replace("page=1", "page=0")
        except:
            raise ValueError(f"{self.search_word} is not a valid keyword")
        self.products = []
        self.numberOfPages=0
        self.Titles=[]
        self.ProductsUrl=[]
        self.finalPrice=[]
        self.originalPrice=[] 
        self.reduction=[]
        self.ImagesUrl=[]
        self.ProductsStock=[]

    def r_soup(self,url):
        """This function is used to create a BeautifulSoup element:"""
        r = requests.get(url, headers=WWScrap.h)  
        return BeautifulSoup(r.text, 'lxml')

    def findNextPage(self, actualPage):
        """This funtion is used to find the next page to be scraped"""
        btn=self.r_soup(actualPage).find("input", {"id":"showMoreBtn"})
        if btn is None:
            return False
        else :
            return WWScrap.url+btn["onclick"].replace("loadNextPage('", "").replace("');", "")

    def findProductsinPage(self,actualPage):
        """This function is used to get all products in a single page."""
        soup=self.r_soup(actualPage)
        return soup.findAll("div", {"class": "items"})

    def findAllProducts(self):
        """This function is used to get all products in all pages."""
        while self.actualPage is not False:
            self.products.append(self.findProductsinPage(self.actualPage))
            NextPage = self.findNextPage(self.actualPage)
            self.actualPage = NextPage
            self.numberOfPages+=1
        self.products=sum(self.products,[])
        products_filter = []
        for product in self.products:
            try :
                product["data-code"]
            except:
                continue
            products_filter.append(product)
        self.products=products_filter

    def findProductTitle(self,product):
        """This function is used to find a single product title."""
        return product.find("a").find("img")["alt"]

    def findProductUrl(self,product): 
        """This function is used to find the url of a single product."""
        return WWScrap.url+product.find("div", {"class": "image-position"}).find("a")["href"]

    def findPrices(self,product):
        """This function is used to find all prices of a single product."""
        originalPrice=product.find("p", {"class": "original-price"})
        if originalPrice is not None:
            originalPrice=originalPrice.text.replace("$", "").replace("\n","").replace(" ","").replace(".0","") 
            reduction="yes" #Price with reduction
        else:
            originalPrice=""
            reduction="no" #Price without reduction

        finalPrice = product.find("input", {"id":"gtmBasePrice"})["value"].replace(".0","") 

        return finalPrice, originalPrice, reduction

    def findImageUrl(self,product):
        """This function is used to find the url of a single image."""
        soup=self.r_soup(self.findProductUrl(product))
        imageUrl = soup.find("div", {"class":"pdp-image-main image"})
        return WWScrap.url+imageUrl.find("img")["src"]

    def findProductStock(self,product):
        """This function is used to find the status of the stock of a single product."""
        stock=product.find("div", {"class": "actions"}).find("div", {"class":"out-of-stock"})
        if stock == None :
            status = "In Stock"
        else :
            status = "Out of Stock"
        return status

    def scrapAll(self):
        """This function is used to scrap all the data (title, urls, prices and stock) of all products."""
        for idx,product in enumerate(self.products):

            self.Titles.append(self.findProductTitle(product))

            finalPrice, originalPrice, reduction = self.findPrices(product)
            self.finalPrice.append(finalPrice)
            self.originalPrice.append(originalPrice)
            self.reduction.append(reduction)

            self.ProductsUrl.append(self.findProductUrl(product))

            self.ImagesUrl.append(self.findImageUrl(product))

            self.ProductsStock.append(self.findProductStock(product))

            print(f"Products scraped: {idx+1} of {len(self.products)}",end="\r")
        print(f"{idx+1} of {len(self.products)} products were scraped !")

    def saveToCsv(self,csvName):
        """This function is used to save the scraped data to a csv file."""
        rows = zip(self.Titles,self.finalPrice,self.reduction,self.originalPrice,self.ProductsUrl,self.ImagesUrl,self.ProductsStock)
        with open(csvName,"w", encoding="utf-8") as csvFile :
            w = csv.writer(csvFile)
            w.writerow(('Product Title','Final Price','Reduction?','Price Without Reduction','URL Product','URL Image','Stock Status'))
            for row in rows :
                w.writerow(row)