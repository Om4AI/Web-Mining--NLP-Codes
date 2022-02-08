# Import libraries
import requests
import html5lib
from bs4 import BeautifulSoup
import csv
import pandas as pd

# Functions and dependencies
def init_csv(list):
    file = "ecom_data.csv"
    with open(file, 'w', newline='') as f:
        w = csv.DictWriter(f, list)
        w.writeheader()

# Scrap data from URL
def scrap_url(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    html_els = {}
    products = {}


    # Get elements (Product Name, Price, Discount, Image)
    pname = soup.find('span', attrs={'class':'B_NuCI'})
    html_els["Product_Name"] = pname
    
    pprice = soup.find('div', attrs={'class':"_30jeq3 _16Jk6d"})
    html_els["Product_Price"] = pprice

    pdisc = soup.find('div', attrs={'class':"_3Ay6Sb _31Dcoz"})
    html_els["Product_Discount"] = pdisc

    pimg = soup.find('div', attrs={'class':"CXW8mj _3nMexc"})
    html_els["Product_Image"] = pimg
    
    for k in html_els.keys():
        if(k=="Product_Image"):
            for row in html_els[k]:
                products[k] = row['src'];
        else:
            products[k] = html_els[k].text
            products[k] = products[k].replace(u'\xa0', u' ').title()
            
    # CSV file saving
    with open("ecom_data.csv", 'a', newline='', encoding="utf8") as f:
        wtr = csv.DictWriter(f, ["Product_Name", "Product_Price","Product_Discount", "Product_Image"])
        wtr.writerow(products)
