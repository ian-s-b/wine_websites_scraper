#Watson's wine scraper

This folder contains the watson's wine scraper based on the BeautifulSoup library used on the https://www.watsonswine.com/ website.

Down below you will find a quick description of each file :

- **WatsonWineScrap.py:** 
	This file contains the script of a class that can be used to scrap data from the 
	watsonwine website. This class takes a keyword as a parameter that can filter
	the products on the website.

- **WWScrap_example.py:** 
	This file contains some lines of code that shows how can the class described on the 
	WatsonWineScrap.py file can be used. The "WW_champagne.csv" file is an output of this script.

- **WW_data_analysis.ipynb:**
	This file is a notebook that contains some data analysis of the output of the 
	WWScrap_example.py file. With this data analysis, we can extract the 
	"WW_champagne_plus.csv" file.
