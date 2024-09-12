from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

driver = webdriver.Chrome()
driver.maximize_window()

base_url = 'https://www.mcdonalds.com'
menu_url = 'https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html'
driver.get(menu_url)


wait = WebDriverWait(driver, 20)

product_links = driver.find_elements(By.CSS_SELECTOR, 'a.cmp-category__item-link')

menu_items = []


def extract_content(element):
    return element.text.strip() if element else ""


def get_element_text_or_default(driver, xpath, default_value="N/A"):
    try:
        element = driver.find_element(By.XPATH, xpath)
        return extract_content(element)
    except Exception as e:
        print(f"Element not found for xpath {xpath}: {e}")
        return default_value


for i in range(len(product_links)):
    product_links = driver.find_elements(By.CSS_SELECTOR, 'a.cmp-category__item-link')
    product_href = product_links[i].get_attribute('href')
    product_url = base_url + product_href if not product_href.startswith('http') else product_href

    driver.get(product_url)

    try:
        name = get_element_text_or_default(driver, '//*[@id="container-20012ecdca"]/div/div[1]/div/div[1]/div/div[3]/div[1]/h1/span[2]')

        description_element = driver.find_element(By.CSS_SELECTOR, 'div.cmp-text')
        description = extract_content(description_element)

        accordion_button = wait.until(EC.element_to_be_clickable((By.ID, 'accordion-29309a7a60-item-9ea8a10642-button')))
        accordion_button.click()

        calories = get_element_text_or_default(driver, '//*[@id="pdp-nutrition-summary"]/div/div[1]/div/ul/li[1]/span[1]/span[2]')
        fats = get_element_text_or_default(driver, "//span[contains(text(),'Жири')]")
        carbs = get_element_text_or_default(driver, "//span[contains(text(),'Вуглеводи')]")
        proteins = get_element_text_or_default(driver, "//span[contains(text(),'Білки')]")

        unsaturated_fats = get_element_text_or_default(driver, "//span[@class='metric' and contains(text(), 'НЖК')]/following-sibling::span//span", default_value="N/A")
        sugar = get_element_text_or_default(driver, "//span[@class='metric' and contains(text(), 'Цукор')]/following-sibling::span//span", default_value="N/A")
        salt = get_element_text_or_default(driver, "//span[@class='metric' and contains(text(), 'Сіль')]/following-sibling::span//span", default_value="N/A")
        portion = get_element_text_or_default(driver, "//span[@class='metric' and contains(text(), 'Порція')]/following-sibling::span//span", default_value="N/A")

        menu_items.append({
            "name": name,
            "description": description,
            "calories": calories,
            "fats": fats,
            "carbohydrates": carbs,
            "proteins": proteins,
            "unsaturated_fats": unsaturated_fats,
            "sugar": sugar,
            "salt": salt,
            "portion": portion
        })
    except Exception as e:
        print(f"Error processing {product_url}: {e}")
    driver.back()

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.cmp-category__item-link')))

with open('menu_items.json', 'w', encoding='utf-8') as f:
    json.dump(menu_items, f, ensure_ascii=False, indent=4)

driver.quit()
