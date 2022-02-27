from WatsonWineScrap import WWScrap

champagne = WWScrap("champagne")
champagne.findAllProducts()
champagne.scrapAll()
champagne.saveToCsv("WW_champagne.csv")