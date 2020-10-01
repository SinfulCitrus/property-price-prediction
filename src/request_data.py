import requests
from bs4 import BeautifulSoup as bs
import pprint as pp
import re
import time
import pandas as pd

# Request and parse property data from https://www.daft.ie/price-register/

def extract_source(url):
    # User agent for the website
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    r = requests.get(url, headers=headers)
    return r


def get_sold_dict(source):
    # Get the dict with date, type of house and price
    page_content = bs(source.content, "lxml")
    sold_properties = [elem for elem in page_content.findAll(
        "div", {"class": "priceregister-searchresult"})]
    keys = ["date", "type", "price"]
    sold_dict = [dict(zip(keys, [x for x in elem.find("span", {"class": "priceregister-dwelling-details"})][2].replace(" ", "").replace("\n", "")[
                      1:].split("|")[:2] + [[x for x in elem.find("span", {"class": "priceregister-dwelling-details"})][1].contents[0]])) for elem in sold_properties]
    return sold_dict

def get_n_pages_as_list(n):
    try:
        pages = range(1,n+1)
        houses = list()
        for page_num in pages:
            url = f"https://www.daft.ie/price-register/dublin-city/?sortby=sold_date-desc&pagenum={page_num}"
            source = extract_source(url)
            data = get_sold_dict(source)
            houses += data
        return houses
    except:
        print("Ran out of pages")
        return []