# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 19:50:58 2015

@author: josephdziados
"""
import urllib2
import re
from bs4 import BeautifulSoup
#import string


def build_soup_page(url):
    """
    builds a beautifulsoup object from a url
    """
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    return soup
    
    
def build_top_index(soup, to_search, beg_url):
    """
    builds an index from a soup object with a search string
    """
    index = []
      
    for a in soup.find_all('a', href=True):
        if a['href'].startswith(to_search):
            index.append(beg_url + a['href'])
    end_index = len(index) / 2
      
    return index[:end_index]
    
    
def build_sub_index(soup, search_one, search_two, beg_url):
    """
    builds an index from a soup object with a search and count string
    """
    index = []
      
    for a in soup.find_all('a', href=True):
        if a['href'].startswith(search_one) and re.search(search_two, a['href']) != None:
            index.append(beg_url + a['href'])
    end_index = len(index) / 2
    
    return index[:end_index]
    
    
def build_single_movie_url_list(total_urls, box_url):
    """
    builds a list of every movies url
    """
    single_movie_url_tags = []

    #loops through each url and scrapes the page for all movies and appends the tags to the list    
    for full_site in total_urls:
        soup = build_soup_page(full_site)    
        for a in soup.find_all('a', href=True):
            if re.search('id', a['href']) != None and a['href'] not in single_movie_url_tags:
                single_movie_url_tags.append(box_url + a['href'])
    
    return set(single_movie_url_tags)
    
    
def main():
    
    # creates a soup object containing the href for all pages A-Z & NUM
    top_level = build_soup_page("http://www.boxofficemojo.com/movies")
    # builds a list of each url ending for NUM and A-Z movie pages
    top_level_urls = build_top_index(top_level, 'alphabetical', "http://www.boxofficemojo.com/movies/")
       
    total_urls = top_level_urls[:]

    for top_level_url in top_level_urls:
        top_level_soup = build_soup_page(top_level_url)
        sub_level = build_sub_index(top_level_soup, '/movies/', 'page', "http://www.boxofficemojo.com")
        if len(sub_level) > 0:
            for sub_level_url in sub_level:
                if sub_level_url.count('id') == 0:                  
                    total_urls.append(sub_level_url)    
                    
    single_movies = build_single_movie_url_list(total_urls, "http://www.boxofficemojo.com")
    print sorted(single_movies)
    
    
if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
