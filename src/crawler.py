import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import re

def extractAndExport(html):
    #BeatifulSoup can parse the html using the tag 'html.parser'
    soup = bs(html, 'html.parser')

    #Now we use soup to scrape the data we want by using patterns in the html
    extracted_a = soup.find_all('a', attrs={'class': 'product-li'})

    for a in extracted_a:
        # Scraping product html by acessing its url
        req = requests.get(a.get('href'))
        product_html = bs(req.text, 'html.parser')
        product_header = product_html.find_all('div', attrs={'class': 'header-product'})
        for ph in product_header:
            print(ph.get))
        return
        #for ph in product_header:
        #    print(ph.get('data-product'))
    """   
    #Using pandas to create de tabular dataset and the export it to csv
    df = pd.DataFrame(frases, columns=['frase', 'gramatica'])

    #if the file does'nt exist create and write
    if not os.path.isfile('frases.csv'):
        #Exporting it to csv, index false indicates not to put the index in the csv
        df.to_csv('frases.csv', index=False, encoding='utf-8')
    else:
        #Appending it to csv, index false indicates not to put the index in the csv
        df.to_csv('frases.csv', mode='a', index=False, encoding='utf-8',header=False)

    words = open('words.in','w')

    #Writing the words in a file, for later loading in C
    for word in bagofwords:
        words.write("%s," % word)

    #To read the exported csv use the function below
    # df = pd.read_csv('frases.csv', encoding='utf-8')
    """

if __name__ == '__main__':
    n = 1
    html = ''

    while (n <= 1):
        #r is response object returned by the page resquest
        r = requests.get('https://www.magazineluiza.com.br/lavadora-de-roupas-lava-e-seca/eletrodomesticos/s/ed/ela1/' + n.__str__() + '/')

        #r.text has all the text from the html source
        html += r.text

        #Deleting all the html comments to facilitate the search
        html += re.sub(re.compile("<!--.*?-->", re.DOTALL), "", html)

        n += 1

    #print(len(html))
    extractAndExport(html)