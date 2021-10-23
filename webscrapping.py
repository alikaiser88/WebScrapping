# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 21:34:37 2021

@author: alika
"""


#Python program to scrape website 
#and save quotes from website
import requests
from bs4 import BeautifulSoup
import pandas as pd

# UPC Code scraping Function 
def scrap_upc_code(URL):
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    row = soup.find('div', attrs = {'class':'product__stat'}) 
    if row == None: 
        return ""
    row2 = row.find('span', attrs = {'class':'product__stat-desc'})
    #print(row2.text)  # UPC code
    if row2 == None: 
        return ""    
    return row2.text.strip('\n')


# URL scraping Function 
def scrap_url(URL, keyword):
    url_list=[]
    
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    #quotes=[]  # a list to store quotes
    table = soup.find('div', attrs = {'id':'product_listing'}) 
    if table == None: 
        #print("table Not found ")
        return None 
    
    nxt_page = soup.find('li', attrs = {'class':'rc-pagination-next'})
    #print(nxt_page)
    nxt_pagetag= nxt_page.find('a')
    if nxt_pagetag is not None:
        nxt_pagelink= nxt_pagetag.attrs["href"]
        print(nxt_pagelink)
    else :
        nxt_pagelink= None
    
    ret_obj = {}
    ret_obj['Next_url']= nxt_pagelink

    for row in table.findAll('div',
                              attrs = {'class':'ag-item gtm-product'}):
        item = {}
        details_tag= row.find('div', attrs = {'id':'details'})
        print(row.attrs["data-item-number"])  # SKU id
        item['sku'] = row.attrs["data-item-number"]
        a_tag= details_tag.find('a', attrs = {'class':'block'})
        #print(a_tag.text)  # Product description
        item['description'] = a_tag.text
        #print("https://www.webstaurantstore.com" + a_tag.attrs["href"])  # SKU id
        item['url'] =("https://www.webstaurantstore.com" + a_tag.attrs["href"])
        pricing_tag= row.find('div', attrs = {'class':'pricing'})
        a2_tag= pricing_tag.find('p')
        #print(a2_tag.text)  # price
        item['price'] = a2_tag.text
        item['UPC'] = scrap_upc_code(item['url'])
        item['keyword'] = keyword
        url_list.append(item)
    
    ret_obj['Product_list']= url_list
    return ret_obj




#word_List= ['Kitchen utensils','Food preparation tools','Tongs','Disposables','Restaurant dinnerware','Tabletop',
#               'Food storage containers','Spice storage containers','Kitchen spoons','Turners',
#               'Whisks and cooking whips','Pizza servers','Ice cream scoop and dippers','Measuring cups and spoons',
#               'Disposable food packaging supplies']

word_List =['Pizza servers','Ice cream scoop and dippers','Measuring cups and spoons',
              'Disposable food packaging supplies']
x = [word.replace(" ", "-").lower() for word in word_List ]
print(x)
word_List = list(set(x))
word_List.sort()

product_list=[]


for word in word_List :
    base_url ="https://www.webstaurantstore.com/search/"+word +".html"
    print(base_url)
    #break
    
    url = base_url

    while url is not None: 
        obj_list = scrap_url(url, word)

        if obj_list is None:
            url = None
        else:             
            product_list.extend(obj_list['Product_list'])

            url= obj_list['Next_url']
            #print(url)

            if url is not None :

                url_array = base_url.split('/')
                #print(url_array)
                new_url=url_array[0] +"//" + url_array[2]+ url
                print (new_url)
                url = new_url


# export data to CSV
df= pd.DataFrame(product_list)
df.to_csv("export.csv")   
print ( " Done ! ")