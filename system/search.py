from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def search_google_with_selenium(query):
    driver = webdriver.Chrome()

    driver.get("https://www.google.com")
    
    search_box = driver.find_element_by_name("q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    
    time.sleep(2) 

    results = driver.find_elements_by_css_selector('div.tF2Cxc')
    
    search_results = []
    for result in results:
        title = result.find_element_by_tag_name('h3').text
        link = result.find_element_by_tag_name('a').get_attribute('href')
        search_results.append({
            "title": title,
            "link": link
        })

    driver.quit()

    return search_results
