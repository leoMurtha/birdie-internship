import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import re
import json
import os

def extract(html):
    #BeatifulSoup can parse the html using the tag 'html.parser'
    soup = bs(html, 'html.parser')
    #Now we use soup to scrape the data we want by using patterns in the html
    extracted_a = soup.find_all('a', attrs={'class': 'product-li'})

    # .csv column order
    #cols = ['Titulo', 'Categoria', 'Preco', 'SKU', 'Marca', 'Modelo']
    # list containing products attributes in JSON(dictionary) format 
    product_json = []
    for a in extracted_a:
        # Scraping product html by acessing its url
        req = requests.get(a.get('href'))
        product_html = bs(req.text, 'html.parser')
        
        # Only one div with class header-product per product page
        product_header = product_html.find_all('div', attrs={'class': 'header-product'})
        if product_header:
            # In the div there's only one data-product tag
            data = json.loads(product_header[0].get('data-product'))
            # Filtering seller only allowing magazineluiza
            if data['seller'].upper() != 'MAGAZINELUIZA':
                continue # Go to the next product
            # New dictionary with product sku, fullTitle and the listPrice
            product_data = {k:data[k] for k in ('sku','fullTitle','listPrice') if k in data.keys()}
        
        # Extracting category from the breadcrumb element
        breadcrumb_itens = product_html.find_all('a', attrs={'class': 'breadcrumb__item'})
        if breadcrumb_itens: category = {'category' : breadcrumb_itens[1].text.strip()}
        
        # technical info start as a dict with empty values
        technical_info = {'Marca': '', 'Modelo': ''}
        # Getting technical info from the description box 
        description_box = product_html.find('td', attrs={'class' :'description__information-right'})
        # If exists a product description box then we can extract information from it
        # else the technical info dict remains with empty values = no technical information
        if description_box:
            # contains all of the types of technical information in the description box
            technical_type = description_box.find_all('td', attrs={'class': 'description__information-box-left'})
            # contains all values of technical information in the description box
            technical_value = description_box.find_all('td', attrs={'class': 'description__information-box-right'})
            # Dictionary that will only contain Marca and Modelo
            for type, value in zip(technical_type, technical_value):
                type = type.text.strip()
                value = value.text.strip()
                # Getting only Marca and Modelo as technical information
                if (type.upper() == 'MARCA') or (type.upper() == 'MODELO'):
                    technical_info[type] = value
        
        # Updating the product json adding category and technical information dictionary
        product_data.update(technical_info)
        product_data.update(category)
        # Sorting the dictionary to mantain consistency on the order of the keys
        product_data = {k:product_data[k] for k in sorted(product_data)}
        # Inserting new product data to the product json
        product_json.append(product_data)
       
    return product_json

def export(data):
    #Using pandas to create de tabular dataset and the export it to csv
    df = pd.DataFrame.from_dict(data)

    #if the file does'nt exist create and write
    if not os.path.isfile('magazine_products.csv'):
        #Exporting it to csv, index false indicates not to put the index in the csv
        df.to_csv('magazine_products.csv', index=False, encoding='utf-8')
    else:
        #Appending it to csv, index false indicates not to put the index in the csv
        df.to_csv('magazine_products.csv', mode='a', index=False, encoding='utf-8',header=False)

    #To read the exported csv use the function below
    # df = pd.read_csv('frases.csv', encoding='utf-8')

    
if __name__ == '__main__':
    n = 1
    html = ''
    url = 'https://www.magazineluiza.com.br/lavadora-de-roupas-lava-e-seca/eletrodomesticos/s/ed/ela1/'
    while (n <= 5):
        #r is response object returned by the page resquest
        r = requests.get(url + n.__str__() + '/')
        #r.text has all the text from the html source
        html += r.text
        n += 1
    n = 1
    
    url = 'https://www.magazineluiza.com.br/geladeira-refrigerador/eletrodomesticos/s/ed/refr/'
    while (n <= 6):
        #r is response object returned by the page resquest
        r = requests.get(url + n.__str__() + '/')
        #r.text has all the text from the html source
        html += r.text
        n += 1
    
    #Deleting all the html comments to facilitate the search
    html = re.sub(re.compile("<!--.*?-->", re.DOTALL), "", html)   

    product_data = extract(html)
    export(product_data)