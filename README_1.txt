This folder contains two web scraping projects based on two different libraries : 
BeautifulSoup (this library can be found in bs4) and selenium.

The BeautifulSoup library can be used to scrap simple HTML and XML based websites.
When we have dynamic websites, when the HTML and XML structure of the website changes
according to a script (based on javascript for example), we can use a headless browser
to automate some tasks (press buttons, fill forms, scroll pages, etc.) and retrieve 
the desired data.

The BeautifulSoup project can be found on the "scraping_with_bs4" folder and it was 
based on the https://www.watsonswine.com/ website.

The selenium project can be found on the "scraping_with_selenium" folder and it was
based on the https://www.instacart.com/ website.

The objective of these projects is to obtain data from two different websites with different
structures and to create dataframes containing information about the products of these sites.