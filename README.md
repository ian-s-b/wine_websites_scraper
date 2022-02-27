# wine_websites_scraper
The objective of this projects is to scrap data from two different websites with different structures and to create dataframes containing information about the products of these sites.

The main libraries used on this project are BeautifulSoup and Selenium.

The BeautifulSoup library can be used to scrap simple HTML and XML based websites. 

Furthermore,when we have dynamic websites, when the HTML and XML structure of the website changes according to a script (based on javascript for example), we can use a headless browser to automate some tasks (press buttons, fill forms, scroll pages, etc.) and retrieve the desired data. For this project, we used the Selenium web browser controlling tool.

The scraped websites are the following:

-  <a href="https://www.watsonswine.com/">Watson's wine:</a>
Watson's Wine is a wine retailer based in Hong Kong and a member of the A.S. Watson Group (ASW). In order to scrap this website, the BeautifulSoup library was used. The code can be found on the "ww_scrap" folder.

- <a href="https://www.instacart.com/">Instacart:</a>
Instacart is an American company that operates a grocery delivery and pick-up service. In order to scrap this website, the selenium tool was used. The code can be found on the "instacart_scrap" folder


