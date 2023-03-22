#importing libraries
from bs4 import BeautifulSoup
import requests
import random

#getting the product name
def get_name(div):
    
    try:
        product_name = div.find('span', attrs={'class':'a-size-medium a-color-base a-text-normal'}).text
        
    except AttributeError:
        product_name = "NA"
    
     return product_name   
    
#getting the product url
def get_url(div):
    
    try:
        product_url = div.find('a', attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})['href']
        
    except AttributeError:
        product_url = "NA"
        
    return product_url

#getting the no. of ratings
def get_rating(div):
    
    try:
        product_rating = div.find('span', attrs={'class':'a-icon-alt'}).text
        
    except AttributeError:
        product_rating = "NA"
        
    return product_rating

#getting the user rating
def get_user_rating(div):
    
    try:
        users_rated = div.find('span', attrs={'class':'a-size-base s-underline-text'}).text
        
    except AttributeError:
        users_rated = "NA"
        
    return users_rated

#getting the product price
def get_price(div):
    
    try:
        price = div.find('span', attrs={'class':'a-price-whole'}).text
    
    except AttributeError:
        price = "NA" 
    
    return price

#getting the product asin
def get_asin(div):
    try:
        product_asin = product['data-asin']
    except AttributeError:
        product_asin = "NA" 
    return product_asin

#getting the product description
def get_description(soup):
    try:
        product_description =  soup.find('div', attrs={'id':'productDescription'})
        
    except AttributeError:
        product_description = "NA"
        
    return product_description

#getting the product manufacture name
def get_manufacture(soup):
    product_manufacturer = ''
    product_details = soup.find("div", attrs={'id':'detailBullets_feature_div'})
        if product_details is not None:
            for s in product_details.findAll("span", attrs={'class':'a-text-bold'}):
                if('Manufacturer' in s.text):
                    name = s.find_next_sibling("span").text
                    product_manufacturer = name
                    break

        elif product_details is None: 
            details_table = soup.find("table", attrs={'id':'productDetails_techSpec_section_1'})
            if details_table is not None:
                for row in details_table.findAll("th", attrs={'class':'a-color-secondary a-size-base prodDetSectionEntry'}):
                    if('Manufacturer' in row.text):
                        name = row.find_next_sibling("td").text.strip()
                        product_manufacturer = name
                        break
            else:
                product_manufacturer = 'NA'
                
    return product_manufacturer
    

if __name__ == '__main__':
    #header
    HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
    #proxies
    proxies_list = []
    #url
    base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{}.html"
    allProducts = []
    #for iterating in all the pages
    for n in range(1,21):
        #url of specific page
        url = base_url.format(n)
        proxies= {'https':random.choice(proxies_list)}
        #request
        res = requests.get(url,headers=Headers,proxies=proxies)
        #soup object
        soup = BeautifulSoup(res.content, "lxml")
        #fetching all the products in single page
        divs = soup.findAll("div",attrs={'class':"sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16"})
        single_prod = []
        
        #iterating through all the products
        for div in divs:
            # product name
            prod_name = get_name(div)
            single_prod.append(prod_name)
            
            #product url
            prod_url = get_url(div)
            single_prod.append(prod_url)
            
            #no. of ratings
            no_rating = get_rating(div)
            single_prod.append(no_rating)
            
            #user rating
            user_rating = get_user_rating(div)
            single_prod.append(user_rating)
            
            #product price
            price = get_price(div)
            single_prod.append(price)
            
            #product asin
            asin = get_asin(div)
            single_prod.append(asin)
            
            #redirecting to the each product page
            product_page = requests.get("https://www.amazon.in"+prod_url,headers=Headers)
            prod_soup = bs4.BeautifulSoup(product_page.content,'lxml')
            
            #product description
            prod_description = get_description(prod_soup)
            single_prod.append(prod_description)
            
            #product manufacture name
            manufacture = get_manufacture(prod_soup)
            single_prod.append(manufacture)
            
    allProducts.append(single_prod)
    distribute = lambda f:[item for sublist in f for item in sublist]
    df = pd.DataFrame(flatten(all_products_list),columns=['Product Name','Product URL','No,of Rating','Users Rated', 'Price', 'ASIN', 'Product Description', 'Product Manufacturer'])
    df.to_csv('amazon_things.csv', index=False, encoding='utf-8')
            
            
        
        
    