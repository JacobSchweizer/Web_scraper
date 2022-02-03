#importing beautifulsoup and selenium
import csv
from json.tool import main
from bs4 import BeautifulSoup

from selenium import webdriver

#Startup the webdriver
driver = webdriver.Chrome("/Users/jacobschweizer/Documents/Programmering/drivers/chromedriver")

url = "https://www.amazon.com"
driver.get(url)

def get_url(search_term): 
    template = "https://www.amazon.com/s?k={}&ref=nb_sb_noss_1"

    search_term = search_term.replace(" ", "+" )
    return template.format(search_term)

url = get_url("ultrawide monitor")
print(url)

driver.get(url)

#Extracting the collection of data

soup = BeautifulSoup(driver.page_source, "html.parser")
results = soup.find_all("div", {"data-component-type": "s-search-result"})

len(results)

#Prototype the record

item = results[0]
atag = item.h2.a

description = atag.text.strip()
url = "https://www.amazon.com" + atag.get("href")

price_parent = item.find("span", "a-price")
price = price_parent.find("span", "a-offscreen").text

rating = item.i.text

review_count = item.find("span", {"class": "a-size-base"}).text

#Generalize the pattern

def extract_record(item): 

    #description and url
    atag = item.h2.a
    description = atag.text.strip()
    url = "https://www.amazon.com" + atag.get("href")

    #price
    price_parent = item.find("span", "a-price")
    price = price_parent.find("span", "a-offscreen").text

    #rank and rating
    rating = item.i.text
    review_count = item.find("span", {"class": "a-size-base"}).text

    result = (description, price, rating, review_count, url)

    return result

records = []
results = soup.find_all("div", {"data-component-type": "s-search-result"})

for item in results:
    records.append(extract_record(item))

#Error handling

def extract_record(item): 

    #description and url
    atag = item.h2.a
    description = atag.text.strip()
    url = "https://www.amazon.com" + atag.get("href")
    
    
    try: 

        #price
        price_parent = item.find("span", "a-price")
        price = price_parent.find("span", "a-offscreen").text

    except AttributeError:
        return

    try: 

        #rank and rating
        rating = item.i.text
        review_count = item.find("span", {"class": "a-size-base"}).text
    except AttributeError: 
        rating = ""
        review_count = ""

    result = (description, price, rating, review_count, url)

    return result

records = []
results = soup.find_all("div", {"data-component-type": "s-search-result"})

for item in results:
    record = extract_record(item)
    if record: 
        records.append(record)

records[0]

for row in records: 
    print(row[1])

#Getting the next page 

def get_url(search_term): 
    template = "https://www.amazon.com/s?k={}&ref=nb_sb_noss_1"

    search_term = search_term.replace(" ", "+" )

    #add term query to url 
    url = template.format(search_term)

    #add page query placeholder 

    url += "&page{}"
    return url








##Putting it all togheter

import csv
from json.tool import main
from bs4 import BeautifulSoup

from selenium import webdriver

#Startup the webdriver
##driver = webdriver.Chrome("/Users/jacobschweizer/Documents/Programmering/drivers/chromedriver")

def get_url(search_term): 
    template = "https://www.amazon.com/s?k={}&ref=nb_sb_noss_1"

    search_term = search_term.replace(" ", "+" )

    #add term query to url 
    url = template.format(search_term)

    #add page query placeholder 

    url += "&page{}"
    return url

def extract_record(item): 

    #description and url
    atag = item.h2.a
    description = atag.text.strip()
    url = "https://www.amazon.com" + atag.get("href")
    
    
    try: 

        #price
        price_parent = item.find("span", "a-price")
        price = price_parent.find("span", "a-offscreen").text

    except AttributeError:
        return

    try: 

        #rank and rating
        rating = item.i.text
        review_count = item.find("span", {"class": "a-size-base"}).text
    except AttributeError: 
        rating = ""
        review_count = ""

    result = (description, price, rating, review_count, url)

    return result

def main(search_term):
    
    driver = webdriver.Chrome("/Users/jacobschweizer/Documents/Programmering/drivers/chromedriver")

    record = []
    url = get_url(search_term)

    for page in range(1, 21):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        results = soup.find_all("div", {"data-component-type": "s-search-result"})

        for item in results: 
            record = extract_record(item)

            if record: 
                records.append(record)
    
    driver.close()

    with open("results.csv", "w", newline="", encoding="utf-8") as f: 
        writer = csv.writer(f)
        writer.writerow(["Despriction", "Price", "Rating", "Reviewcount", "url"])
        writer.writerows(records)


main("ultrawide monitor")






















