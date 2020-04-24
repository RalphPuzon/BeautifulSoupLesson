# Beautiful soup scraper lesson by Corey Schafer:
    

# Practicing web scraping via bs4
#SETUP: change directory to where html file is:

import os
os.chdir("E:\\ProjectDataFolder\\python_web_scraping_practice")
    
from bs4 import BeautifulSoup
import requests
import csv #for a later section

#-----------------------------------------------------------------------------
# MAKING THE BS OBJECT:
# You can either pass a URL or an html file.

with open('simple.html') as html_file:
    soup = BeautifulSoup(html_file, 'lxml') # lxml is a parser, there's many
                                            # types of parsers
    
#test print the 'pretty'-fied html code:
print(soup.prettify())

#parts of the HTML can be accessed as attributes of the bs object

#print out visible text in title tag:
title = soup.title.text #.title prints w/ tags, .text removes the tags
print(title)

#fetch the first div + all children of div on the script:
div1 = soup.div
print(div1)

#find a div with included parameter "class=footer":
# we use "class_" since class is a keyword.
div_with_footer = soup.find('div', class_='footer')
print(div_with_footer)

#-----------------------------------------------------------------------------

#WORKING WITH MULTIPLE PIECES:
#we want all article headlines and summaries from object
#to get article (remember that articles are DIVs with class = article):
    
article = soup.find('div', class_='article')

#this prints the ff:
#<div class="article">
#<h2><a href="article_1.html">Article 1 Headline</a></h2>
#<p>This is a summary of article 1</p>
#</div>

#we want the text inside the anchor(<a>), which is inside the <h2>, inside the
#div. we can access these as attributes of the article object:

headline = article.h2.a.text #we dont want the tags, so add the .text
print(headline)

# we can get the summary in the <p> tah, in the same level as <h2>:

summary = article.p.text
print(summary)

#we can make lists of article searches via a find_all method for loop:
    
for article in soup.find_all('div', class_='article'):
    
    headline = article.h2.a.text #we dont want the tags, so add the .text
    print(headline)
    
    summary = article.p.text
    print(summary) 
    
    print() #to separate div groups via newline
    
# ----------------------------------------------------------------------------    
#USING REQUESTS:
    
source = requests.get('http://coreyms.com').text

#requests returns a request object, .text gives us just the text.

soup2 = BeautifulSoup(source, 'lxml')

#print(soup2.prettify())

#we can then perform what we've done above on this object.

summary = soup2.find('div', class_='entry-content').p.text

# remember, find will return all children. we drill down to get the text in the 
# <p> tag.

#more complex parsing:
#e.g. embedding videos are not as simple, since the src is not a direct link,
#but rather an embedding URL. we need to recreate the link

#example embed code:
    
# src="https://www.youtube.com/embed/06I63_p-2A4?version=3&amp;rel=1&amp;fs=1&\
#    amp;autohide=2&amp;showsearch=0&amp;showinfo=1&amp;iv_load_policy=1&amp;\
#        wmode=transparent" style="border:0;" type="text/html" width="640">    

# the "06I63_p-2A4" after the "embed/" and before the "?" is the video id, the 
# video would then be "http://youtube.com/06I63_p-2A4" would be the actual
#link. we need to extract this and join it to a blank youtube url as the video
#id to get the link.

# extract the correct div:
vid_src = soup2.find('iframe', class_="youtube-player")['src']

# the ['src'] returns the content of the src= parameter.
#let's split the url via the forward slashes, and fetch the 5th item

vid_id = vid_src.split('/')[4]

#we fetch the id by splitting on the "?", and returning the first item:
vid_id = vid_id.split("?")[0] #returns 'z0gguhEmWiY', which is the correct id.

# make the link:
yt_link = f'https://youtube.com/watch?v={vid_id}' #returns correct link

# use for loop to scrape all links:
"""
for souptempo in soup2.find_all('article'):
    headline = souptempo.h2.a.text
    print(headline)
    
    summary = souptempo.find('div', class_='entry-content').p.text
    
    #get entry-content source
    vid_src = souptempo.find('iframe', class_="youtube-player")['src']
    
    #fetch ID
    vid_id = vid_src.split('/')[4].split("?")[0] #combined the splits
    
    # make the link:
    yt_link = f'https://youtube.com/watch?v={vid_id}' 
    
    print(yt_link)
    print()
"""

# code is commented out since it encounters an error on the third iteration
# due to the object not having a video. we will fix this by placing the source
# search in a try/except, passing the value None for those without video. 

# we will also be writing the fetched headline, summary and link into a nice
# csv. 

csv_file = open('practice_scrape.csv', 'w') #make an open csv in environment

writer = csv.writer(csv_file) #writer object for the csv_file

writer.writerow(['headline', 'summary', 'link']) #write the column header row

for souptempo in soup2.find_all('article'):
    headline = souptempo.h2.a.text
    print(headline)
    
    summary = souptempo.find('div', class_='entry-content').p.text
    
    try:
        #get entry-content source
        vid_src = souptempo.find('iframe', class_="youtube-player")['src']
        
        #fetch ID
        vid_id = vid_src.split('/')[4].split("?")[0] #combined the splits
        
        # make the link:
        yt_link = f'https://youtube.com/watch?v={vid_id}' 
        
    except:
        yt_link = None
        
    print(yt_link)
    print()
    
    writer.writerow([headline, summary, yt_link]) #write row to build table

csv_file.close() #close the csv_file




