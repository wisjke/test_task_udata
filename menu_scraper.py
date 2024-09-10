import requests
from bs4 import BeautifulSoup
import json
base_url = 'https://www.mcdonalds.com'
menu_url = 'https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html'

page = requests.get(menu_url)

soup = BeautifulSoup(page.content, 'html.parser')

menu_items = []


def extract_content(element):
    return element.get_text(strip=True) if element else ""

product_links = soup.find_all('a', class_='cmp-category__item-link')

for product_link in product_links:

    product_href = product_link.get('href')
    product_url = base_url + product_href
    product_response = requests.get(product_url)
    product_soup = BeautifulSoup(product_response.content, 'html.parser')

    name = extract_content(product_soup.find('span', class_='cmp-product-details-main__heading-title'))
    description = extract_content(product_soup.find('div', class_='cmp-text'))



    menu_items.append({
        "name": name,
        "description": description,
    })

print(json.dumps(menu_items, ensure_ascii=False, indent=4))