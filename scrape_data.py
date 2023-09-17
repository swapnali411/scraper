import requests
from bs4 import BeautifulSoup as bs
import json


def crawl_data(search_term):
    """
    To crawl product data from given url
    """
    url = 'https://www.flipkart.com/search?marketplace=FLIPKART&q='+(search_term)
    result_list = []
    
    
    res = requests.get(url)
    soup = bs(res.text, 'html.parser')
    link_list = []
    all_a = soup.find('div',{'class':'_1YokD2 _3Mn1Gg'}).find_all('a',{'rel':'noopener noreferrer'})
    all_link = []
    for a in all_a:
        link = a['href']
        if 'https://www' not in link and link not in all_link:
            all_link.append(link)

    for product_link in all_link:

        product_details = {}
    
        product_link = 'https://www.flipkart.com'+ product_link
        product_res = requests.get(product_link)
        product_soup = bs(product_res.text, 'html.parser')
    
        product_name =  product_soup.find('h1', {'class':'yhB1nd'}).text.replace('\xa0\xa0','').strip()
        product_details['name'] = product_name
        product_details['link'] = product_link
        price_details = product_soup.find('div', {'class':'_25b18c'})

        current_price = price_details.find('div', {'class':'_30jeq3 _16Jk6d'})
        if current_price:
            product_details['current_price'] = current_price.text.replace('₹', '').strip()

        original_price = price_details.find('div', {'class':'_3I9_wc _2p6lqe'})
        if original_price:
            product_details['original_price'] = original_price.text.replace('₹', '').strip()

    
        discounted_str = price_details.find('div', {'class':'_3Ay6Sb _31Dcoz'})
        if discounted_str and 'off' in discounted_str.text:
            discounted = True
        else:
            discounted = False
        
        thumbnail = product_soup.find('div',{'class':'_3kidJX'}).find('img')['src']
        product_details['discounted'] = discounted
        product_details['thumbnail'] = thumbnail
    
        result_list.append(product_details)
    

        final_result = { 
            'total_result': len(result_list),
            'query': search_term,
            'fetch_from': url,
            'result' : result_list
            }
    
    with open("products.json", "w") as final:
        json.dump(final_result, final)
        
        
    
if __name__ == "__main__":
    search_term = input("Enter search term:")
    crawl_data(search_term)


    
