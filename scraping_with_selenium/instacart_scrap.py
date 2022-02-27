from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import selenium.webdriver.support.expected_conditions as EC
import time
import re
from selenium.webdriver.support.wait import WebDriverWait

#Initializing parameters:
h = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

path = ChromeDriverManager().install()
s = Service(path)
o = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=s, options=o)

url = "https://www.instacart.com/"
driver.get(url)

#The url2 redirects to the safeway store page:
url2 = "https://www.instacart.com/store/safeway/storefront" 
driver.get(url2)

#Search for champagne keyword:
input_search_xpath='//*[@placeholder="Search Safeway..."]'
search_word = "champagne"
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, input_search_xpath))).send_keys(search_word)
driver.find_element(By.XPATH,input_search_xpath).submit()

time.sleep(5)

#Define the address :
btn_address_class="css-s3ybpu"
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, btn_address_class))).click()

address = "601 Diamond St, San Francisco"
input_address_xpath='//*[@id="streetAddress"]'
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, input_address_xpath))).send_keys(address)

btn_address_class2="css-1raxgv2"
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, btn_address_class2))).click()

postalcode="94114"
input_address_xpath2='//*[@id="postalCode"]'
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,input_address_xpath2))).send_keys(postalcode)
driver.find_element(By.XPATH,input_address_xpath2).submit()

time.sleep(5)

try:
    #Close the pop up at the bottom of the page (we need to close it to acces the "load more button"):
    btn_popup_xpath='//*[@class="rmq-b3bfb142"]/button'
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, btn_popup_xpath))).click()
except:
    pass

#Clik on the load more button:
btn_load_more_class="css-jqp6h0-LoadMore"
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, btn_load_more_class))).click()

#Scroll to the end of the page:
while True:
    previous_height = driver.execute_script('return document.body.scrollHeight')
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')

    time.sleep(2)

    new_height = driver.execute_script('return document.body.scrollHeight')

    if new_height == previous_height :
        break
        
time.sleep(2)

#We use the "search_result_class" to get all products and to avoid the section "People Also Purchased" located at the middle of the page:
search_result_class='//*[@class="css-c889c0-SearchResultsEngagementTracker"]'
products=driver.find_elements(By.XPATH,search_result_class)

#Functions to get scrap data:
def findProductUrl(product):
    product=product.find_element(By.TAG_NAME,"a")
    return product.get_attribute('href')

def findProductTitle(product):
    title_class="css-9vf613"
    product=product.find_element(By.CLASS_NAME,title_class)
    return '"'+product.text+'"'

def findImageUrl(product):
    url_picture_class="css-94dslt"
    product=product.find_element(By.CLASS_NAME,url_picture_class)
    url_picture=product.get_attribute('srcset')
    pattern = "3x,\ (.*?)\ 4x"
    return '"'+re.search(pattern,url_picture).group(1)+'"'

def findProductStock(product):
    product=product.text
    if "running low" in product.lower():
        return "running low"
    else :
        return ""

def findPrices(product):
    base_price_class="css-1kh7mkb"
    final_price_class="css-1sbaogi"
    unique_price_class="css-coqxwd"
    buyfor2_price_class="css-1sqinx7-ItemDynamicLabel"
    
    try:
        base_price = product.find_element(By.CLASS_NAME,base_price_class)
        final_price = product.find_element(By.CLASS_NAME,final_price_class)
        base_price=base_price.text.replace("reg. $","")
        final_price=final_price.text.replace("$","")
        reduction="yes"
    except:
        final_price = product.find_element(By.CLASS_NAME,unique_price_class)
        final_price = final_price.text.replace("$","")
        base_price = ""
        reduction="no"
    
    try:
        buy2for_price = product.find_element(By.CLASS_NAME,buyfor2_price_class)
        buy2for_price = buy2for_price.text.lower().replace("buy 2 for $","")
        reduction="yes"
    except:
        buy2for_price = ""
    
    return final_price,base_price,buy2for_price,reduction

#Extracting data and saving to a csv file:
with open("instacart.csv","w", encoding="utf-8") as csvFile :
    csvFile.write('Product Title,Final Price,Reduction?,Price Without Reduction,Buy 2 for,URL Product,URL Image,Stock Status\n')
    nproduct=0
    for product in products:
        print(f"Products saved to csv: {nproduct}",end="\r")
        
        title = findProductTitle(product)    
        finalPrice, originalPrice, buy2for, reduction = findPrices(product)
        productUrl = findProductUrl(product)
        imageUrl = findImageUrl(product)
        stock = findProductStock(product)

        csvFile.write(title+","+finalPrice+","+reduction+","+originalPrice+","+buy2for+","+productUrl+","+imageUrl+","+stock+"\n")

        nproduct+=1           
