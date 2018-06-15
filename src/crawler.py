import pandas as pd
import math
import requests
from bs4 import BeautifulSoup as bs
import re
import json
import os
from time import sleep


def extract(html, status=''):
    """
        Given a HTML in text form returns a list of
        JSONs with the requested product features
        if @status:
            '' then it will extract all available products
            '--unavailable' then it will extract all unavailable products 
    """
    # BeatifulSoup can parse the html using the tag 'html.parser'
    soup = bs(html, 'html.parser')
    # Now we use soup to scrape the data we want by using patterns in the html
    extracted_a = soup.find_all('a', attrs={'class': 'product-li'})

    # list containing products attributes in JSON(dictionary) format
    product_json = []
    product_htmls = []

    for a in extracted_a:
        # Scraping product html by acessing its url
        try:
            req = requests.get(a.get('href'))
            product_htmls.append(req.text)
        except requests.exceptions.ConnectionError:
            print("Connection refused by the server..")
            # Sleeping so that the server don't refuse the request again
            sleep(3)
            continue

    print('Acessed every product link')

    # After extracting all available products pages html
    # Extract requested informations per product
    for product_html in product_htmls:
        product_html = bs(product_html, 'html.parser')
        # Only one div with class header-product per product page
        product_header = product_html.find_all('div', attrs={'class': 'header-product'+status})
        product_data = {}
        # If there is a product header so the extraction is valid otherwise continue
        if product_header:
            # In the div there's only one data-product tag
            data = json.loads(product_header[0].get('data-product'))
            # Filtering seller only allowing magazineluiza
            # Inspecting the site's HTML the default seller is magazineluiza
            # so when the key seller isn't in the JSON we still extract info from the product
            if 'seller' in data and data['seller'].upper() != 'MAGAZINELUIZA': 
                continue  # Go to the next product
            # New dictionary with product sku and the listPrice
            product_data = {k: data[k] for k in (
                'sku', 'listPrice') if k in data.keys()}
        else: continue

        # Extracting the title for available or unavailable products
        title = {'Titulo' : ''}
        title_html = product_html.find(
            'h1', attrs={'class': 'header-product__title'+status})
        title_text = title_html.text.strip().replace('"', '')
        title['Titulo'] = title_text
        
        # Extracting category from the breadcrumb element
        breadcrumb_itens = product_html.find_all(
            'a', attrs={'class': 'breadcrumb__item'})
        if breadcrumb_itens:
            category = {'category': breadcrumb_itens[1].text.strip()}

        # technical info start as a dict with empty values
        technical_info = {'Marca': '', 'Modelo': ''}
        # Getting technical info from the description box
        description_box = product_html.find(
            'td', attrs={'class': 'description__information-right'})
        # If exists a product description box then we can extract information from it
        # else the technical info dict remains with empty values = no technical information
        if description_box:
            # contains all of the types of technical information in the description box
            technical_type = description_box.find_all(
                'td', attrs={'class': 'description__information-box-left'})
            # contains all values of technical information in the description box
            technical_value = description_box.find_all(
                'td', attrs={'class': 'description__information-box-right'})
            # Dictionary that will only contain Marca and Modelo
            for type, value in zip(technical_type, technical_value):
                type = type.text.strip()
                value = value.text.strip()
                # Getting only Marca and Modelo as technical information
                if (type.upper() == 'MARCA') or (type.upper() == 'MODELO'):
                    technical_info[type] = value

        # Updating the product json adding title, category and technical information dictionary
        product_data.update(title)
        product_data.update(category)
        product_data.update(technical_info)
        # Sorting the dictionary to mantain consistency on the order of the keys
        product_data = {k: product_data[k] for k in sorted(product_data)}
        # Inserting new product data to the product json
        product_json.append(product_data)
        
    return product_json


def export(data, filename='file'):
    """
        Exports the data to file in csv format with the name filename.csv
    """    
    # Using pandas to create de tabular dataset and the export it to csv
    df = pd.DataFrame.from_dict(data)

    # if the file does'nt exist create and write
    if not os.path.isfile(filename + '.csv'):
        # Exporting it to csv, index false indicates not to put the index in the csv
        df.to_csv(filename + '.csv', index=False, encoding='utf-8')
    else:
        # Appending it to csv, index false indicates not to put the index in the csv
        df.to_csv(filename + '.csv', mode='a',
                  index=False, encoding='utf-8', header=False)

    # To read the exported csv use the function below
    # df = pd.read_csv('frases.csv', encoding='utf-8')

def main():
    n = 1
    html = ''
    
    url = 'https://www.magazineluiza.com.br/lavadora-de-roupas-lava-e-seca/eletrodomesticos/s/ed/ela1/'
    r = requests.get(url)
    
    # Getting number of pages by doing total product/product per page
    total = int(bs(r.text, 'html.parser').find('div', attrs={'class': 'product-showcase-bottom'}).find_all('span', attrs={})[1].text.split(' ')[-2])
    nEla = math.ceil(total/60.0)
    
    while (n <= nEla):
        # r is response object returned by the page resquest
        r = requests.get(url + n.__str__() + '/')
        print(url + n.__str__() + '/', r)
        # r.text has all the text from the html source
        html += r.text
        n += 1
    
    n = 1
    
    url = 'https://www.magazineluiza.com.br/geladeira-refrigerador/eletrodomesticos/s/ed/refr/'
    r = requests.get(url)
    
    # Getting number of pages by doing total product/product per page
    total = int(bs(r.text, 'html.parser').find('div', attrs={'class': 'product-showcase-bottom'}).find_all('span', attrs={})[1].text.split(' ')[-2])
    nRefr = math.ceil(total/60.0)
    
    while (n <= nRefr):
        # r is response object returned by the page resquest
        r = requests.get(url + n.__str__() + '/')
        print(url + n.__str__() + '/', r)
        # r.text has all the text from the html source
        html += r.text
        n += 1
    

    # Deleting all the html comments to facilitate the search
    html = re.sub(re.compile("<!--.*?-->", re.DOTALL), "", html)

    # Extracts both available and unavailable products
    product_data = extract(html, '--unavailable')
    product_data.extend(extract(html))

    # Saving the data to csv using pandas
    export(product_data, 'magazine_products')


if __name__ == '__main__':
    main()