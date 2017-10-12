#********************************************************************************
#                                                                               #
#    UCD-COMP41680 Machine Learning                                             #
#    Assignment 2:      Text Scraping & Clustering                              #
#    Author:            Wenrui.Shen                                             #
#    Student Number:    15210671                                                #
#    E-mail:            wenrui.shen@ucdconnect.ie                               #
#    Date:                2017-05-02                                            #
#    Description:        Web scraping for part-1                                #
#                  from http://mlg.ucd.ie/modules/COMP41680/news/index.html     #
#                                                                               #
#********************************************************************************

import io
import os
import sys
import urllib.request
import bs4
import codecs
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

news_content_subdir = "news/"
os.makedirs(os.path.dirname(news_content_subdir), exist_ok=True)

news_index_num = 0

news_index_link = "http://mlg.ucd.ie/modules/COMP41680/news/index.html"
news_main_link = "http://mlg.ucd.ie/modules/COMP41680/news/"
news_index_response = urllib.request.urlopen(news_index_link)
news_index_html = news_index_response.read().decode("utf-8")
#print(news_index_html)
print("**********************************************************************")

# Now start parsing index_html.
news_index_parser = bs4.BeautifulSoup(news_index_html,"html.parser")
for news_list_link_match in news_index_parser.find_all("li"):
    # Get a news' list for one month.
    news_index_text = news_list_link_match.get_text()
    for news_list_link in news_list_link_match.find_all('a'):
        # Get a news' list's link.
        news_list_link_str = news_main_link + news_list_link.get('href')
        print(news_index_text + ": " + news_list_link_str)
        
        # Get a news' list.
        news_list_response = urllib.request.urlopen(news_list_link_str)
        news_list_html = news_list_response.read().decode("utf-8")
        
        # Parse a news' list.
        news_list_parser = bs4.BeautifulSoup(news_list_html,"html.parser")
        
        for news_match in news_list_parser.find_all("li"):
            # Get a news' link.
            for news_link in news_match.find_all('a'):
                news_link_str = news_main_link + news_link.get('href')
                print("\t" + news_link_str)
                
                # Get a news.
                news_response = urllib.request.urlopen(news_link_str)
                news_html = news_response.read().decode("utf-8")
                #print(news_html)
                
                # Parse a news.
                news_text = ""
                news_parser = bs4.BeautifulSoup(news_html,"html.parser")
                # Extract the news' contents.
                for paragraph_match in news_parser.find_all("p"):
                    news_paragraph_text = paragraph_match.get_text()
                    news_text = news_text + news_paragraph_text
                print('\t' + news_text)
                
                file_name = news_content_subdir + str(news_index_num) + ".txt"
                news_index_num += 1
                news_file = codecs.open(file_name, 'w', "utf-8")
                news_file.write(news_text)
                news_file.close()
                
                print("***********")
                
        
        























