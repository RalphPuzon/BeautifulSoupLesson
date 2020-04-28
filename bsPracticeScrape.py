#beautifulSoup scraping practice:
import sys
import csv 
from bs4 import BeautifulSoup
import requests

#fetch html via requests:
site = 'http://books.toscrape.com'
    
bulk_data = requests.get(site).text    

#make object
facade_soup = BeautifulSoup(bulk_data, "lxml")

#sidebar iteration:
#fetch the links and place them into a list

list_of_links = []

sidebar_soup_lists = facade_soup.find('div', class_="side_categories").ul.li.ul

for li in sidebar_soup_lists.find_all("li"):
    
    list_of_links.append(site + "/" + str(li.a['href']))
    
#iterate on each site and grab product pod. grab category, title, rating, and
#price. we will save this in a csv, for analytics later:
    
#csv prep:
csv_file = open('bookstore_scrape.csv', 'w') 

writer = csv.writer(csv_file) 

writer.writerow(['CATEGORY', 'TITLE', 'RATING', 'PRICE']) 

#fetching loop:
#for link in list_of_links:
    
for link in list_of_links: 
    templink = requests.get(link).text
    souptempo = BeautifulSoup(templink, 'html5') 
    
    #setting category for page loop
    bookCategory = souptempo.find('div', class_="page-header action").h1.text
    
    #page loop for title, rating, price:
    for pod in souptempo.find_all('article', class_='product_pod'):

        bookTitle = pod.h3.a.text.encode(sys.getdefaultencoding(),'replace')
        
        if "One" in pod.p["class"]:
            bookRating = 1
        elif "Two" in pod.p["class"]:
            bookRating = 2
        elif "Three" in pod.p["class"]:
            bookRating = 3
        elif "Four" in pod.p["class"]:
            bookRating = 4
        else:
            bookRating = 5
        
        bookPrice = pod.find('div', class_="product_price").find\
            ('p', class_= "price_color").text[2:]
            
        writer.writerow([bookCategory, bookTitle, bookRating, bookPrice])
        
csv_file.close() 

#TODO: fix title issue
    
    
    
    
    
    
    
    
    
    

