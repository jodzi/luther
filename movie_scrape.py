# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 19:50:58 2015

@author: josephdziados
"""
import urllib2
import re
from bs4 import BeautifulSoup
import pickle
import datetime
import pandas as pd
import json
import csv


def build_soup_page(page = "", url = "", use_url=False):
    """
    Returns a BeautifulSoup object by calling the server using a passed url if 
    use_url = True, otherwise takes in a string of html and returns a 
    BeautifulSoup object.
    
    page = string
    url = string
    use_url = boolean
    """
    if use_url:
        page = urllib2.urlopen(url)
        return BeautifulSoup(page, 'xml')
    else:
        return BeautifulSoup(page)
    
    
def build_index(soup, search_one, beg_url, search_two="", top=False, sub=False):
    """
    Returns a list of urls by using a soup object, a search term, and the 
    beginning of a particular url. Setting top builds the maing alpha pages, 
    sub builds the pages within those main alpha pages; search_two is used 
    when sub=True
    
    soup = soup object
    to_search = string
    beg_url = string
    search_two = string
    top = boolean
    sub = boolean
    """
    
    urls = []
    
    for a in soup.find_all('a', href=True):
        if top:        
            if a['href'].startswith(search_one):           
                urls.append(str(beg_url + a['href']))
        if sub:
            if a['href'].startswith(search_one) and re.search(search_two, a['href']) != None:
                urls.append(str(beg_url + a['href']))
    
    return sorted(list(set(urls)))
    
        
def build_single_movies(total_urls, box_url):
    """
    Returns a dictionary of every movie url as a key and its corresponding soup
    object as a string as the value. Takes in a list of urls and the beginning
    of a particular url.
    
    total_urls = list
    box_url = string
    """
    
    single_movie_url_html = {}

    for full_site in total_urls:
        soup = build_soup_page(full_site)
        for a in soup.find_all('a', href=True):
            if re.search('id', a['href']) != None and a['href'] not in \
                                single_movie_url_html.keys():
                single_movie_url_html[box_url + a['href']] = str(soup) 
    
    return single_movie_url_html
    
    
def store_pickles(filename, to_store):
    """Dumps information in to_store into a file named filename.
    
    filename = string
    to_store = list, dictionary, etc.    
    """  
    with open(filename, 'w') as f:
        pickle.dump(to_store, f)
        
        
def eat_pickles(filename):
    """Loads information from a pickle file.
    
    filename = string
    """
    
    with open(filename, 'r') as f:
        return pickle.load(f)
        
        
def get_movie_title(soup):
    """
    Returns a movie title given a soup object
    """
    return str(soup.find('title').text.split("(")[0].strip())
    
    
def get_movie_gross(soup):
    """
    Returns a domestic gross integer for a movie given a soup object.
    """
    obj = soup.find(text = re.compile('Domestic Total Gross'))
    if not obj:
        return None
    movie_gross = obj.findNextSibling().text
    if movie_gross:
        return int(movie_gross.replace(',','').replace('$', ''))
    else:
        return None 
        
        
def get_movie_release_date(soup):
    """
    Returns a datetime object of a release date for a movie given a soup object.
    """
    obj = soup.find(text = re.compile('Release Date'))
    if not obj:
        return None
    release_date = obj.findNextSibling().text
    if release_date != 'N/A':
        if release_date == 'TBD':
            return str(release_date)
        elif len(release_date.split()) == 3:
            return datetime.datetime.strptime(release_date, '%B %d, %Y').date()
        elif len(release_date.split()) == 1:
            return datetime.datetime.strptime(release_date, '%Y').date()
        
        else:
            return None
            

def get_movie_runtime(soup):
    """
    Returns a runtime as an integer in minutes for a movie given a soup object.
    """
    obj = soup.find(text = re.compile('Runtime'))
    if not obj:
        return None
    runtime = obj.findNextSibling().text
    if runtime and runtime != 'N/A':
        return int(runtime.split(' ')[0]) * 60 + int(runtime.split(' ')[2])      
    else:
        return None 
        
        
def get_movie_budget(soup):
    """
    Returns a movie budget as an integer given a soup object.
    """
    obj = soup.find(text = re.compile('Production Budget'))
    if not obj:
        return None
    budget = obj.findNextSibling().text
    if budget and budget != 'N/A':
        if '.' in budget:
            return int(budget.split()[0].split('.')[0].replace('$', '') + \
            budget.split()[0].split('.')[1] + '00000')
        elif ',' in budget:
            return int(budget.split(',')[0].replace('$', '') + budget.split(',')[1])
        else:
            return int(budget.split()[0].replace('$', '') + '000000')
    else:
        return None 
        
        
def get_movie_rating(soup):
    """
    Returns a movie rating given a soup object.
    """
    obj = soup.find(text = re.compile('Rating'))
    if not obj:
        return None
    rating = obj.findNextSibling().text
    if rating:
        return str(rating)
    else:
        return None 
        
        
def get_movie_foreign_gross(soup):
    """
    Returns total foreign gross as an int given a soup object.
    """
    obj = soup.find_all(width="35%")
    if not obj:
        return None
    if len(obj) > 1:
        foreign_tot_gross = obj[1].text.strip()
        if foreign_tot_gross != 'n/a':
            return int(''.join(foreign_tot_gross.replace('$','').split(',')))
    else:
        return None 
        
        
def get_movie_genre(soup):
    """
    Returns a movie genre given a soup object.
    """
    obj = soup.find(text = re.compile("Genre: "))
    if not obj:
        return None
    genre = obj.findNextSibling().text
    if genre:
        return str(genre)
    else:
        return None 
        
        
def get_movie_distributor(soup):
    """
    Returns the movie distributor given a soup object.
    """
    obj = soup.find(text = re.compile("Distributor"))
    if not obj:
        return None
    dist = obj.findNextSibling().text
    if dist:
        return str(dist)
    else:
        return None 
        
        
def get_movie_actors(soup):
    """
    Returns a list of non-duplicate actors in a movie given a soup object.
    """
    
    actor_list = []

    for a in soup.find_all('a', href=True):
        if a['href'].startswith('/people/chart/?view=Actor'):
            section = a.find_parent('font')
            for i in range(0, len(section), 2):
                try:
                    actor_list.append(str(section.contents[i].text))
                except:
                    try:
                        actor_list.append(str(section.contents[i]))
                    except:
                        actor_list.append(section.contents[i])
    return list(set(actor_list))
    
    
def get_actors_country(lst, actor=False, country=False):
    """
    Connects to the OMDB api to pull any actors for the movies that didn't have
    them as well as the movies country.  Passes in a list of movie titles and 
    either set actor to True or country to True, but not both.
    """
    
    actor_list = []
    country_list = []    
        
    for movie_title in lst: 
        title = movie_title.replace(" ", "+")
        base_url = 'http://www.omdbapi.com/?t='
        url = base_url + title + '&y=&plot=short&r=json'
        
        try:
            page = urllib2.urlopen(url).read()
            json_data = json.loads(page)
            if actor:        
                actors = json_data['Actors']
                actors = actors.split(',')
                try:
                    actor_list.append([str(actor).strip() for actor in actors])
                except:
                    actor_list.append([actor for actor in actors])
            if country:
                country = json_data['Country']
                countries = country.split(',')
                country_list.append([str(country).strip() for country in countries])
        except:
            if actor:
                actor_list.append([])
            if country:
                country_list.append([])
    if actor:
        return actor_list
    if country:
        return country_list
    
#==============================================================================
#     '''Start web scraping here'''
#     # Creates a soup object of the main movie page
#     main_page = build_soup_page(url="http://www.boxofficemojo.com/movies/", use_url=True)
#      
#     # Builds a list of each url ending for NUM and A-Z movie pages
#     az_urls = build_index(main_page, 'alphabetical', "http://www.boxofficemojo.com/movies/", top=True)
#                                                           
#     # Builds urls for all pages containing movies A-Z, NUM, and all sub-pages beneath those
#     total_urls = az_urls[:]
#      
#     for movie_page in az_urls:
#         soup = build_soup_page(movie_page)
#         sub_urls = build_index(soup, '/movies/', "http://www.boxofficemojo.com", search_two='page', sub=True)
#         if len(sub_urls) > 0:
#             for sub_url in sub_urls:
#                 if sub_url.count('id') == 0:
#                     total_urls.append(sub_url)  
#     single_movies = build_single_movies(total_urls, "http://www.boxofficemojo.com")
#     
#     foreign_pages = []
#      
#     '''Appends the urls of movies that have at least one foreign gross and is not of the
#     genre of Foreign'''    
#     for url, html in jar_of_pickles.iteritems():
#         movie_soup = build_soup_page(html)
#         if movie_soup.find(attrs={'href': re.compile('page=intl')}) != None and \
#         str(movie_soup.find(text = re.compile('Genre: ')).findNextSibling().text) != 'Foreign':
#             foreign_pages.append(url)
#              
#     '''Takes the main movie page urls and creates the url for the foreign gross page'''
#     foreign_urls = [str(foreign_pages[i]).split('?')[0] + '?page=intl&' + \
#     str(foreign_pages[i]).split('?')[1] for i in range(len(foreign_pages))]
#      
#     '''Get's pickeled foreign_url_pages'''
#     foreign_url_pages = eat_pickles('foreign_url_pages.pkl')
#      
#     foreign_movie_data = []
#      
#     '''Loop through pages that have foreign box office revenue and build a list 
#     of dictionaries with the url as the key and a dictionary as the value.  
#     The values contain a dictionary with keys as countries and values as gross.'''    
#     for url, html in foreign_url_pages.iteritems():
#         soup = build_soup_page(page=html)
#         foreign_movie_country = []
#         foreign_country_gross = []
#         for a in soup.find_all('a', href=True):
#             if a['href'].startswith('/movies/?page=intl&country'):
#                 table = a.find_parent('tr')
#                 foreign_movie_country.append(str(table.contents[0].text))
#                 try:
#                     foreign_country_gross.append(int(''.join(table.contents[10].text.replace('$', '').split(','))))
#                 except:
#                     continue
#         foreign_movie_data.append(dict(zip(foreign_movie_country, foreign_country_gross))) 
#      
#     '''Build a dictionary with the foreign urls as keys and the values as a dictionary of movie country and gross'''
#     foreign_movie_dict = dict(zip(foreign_url_pages.keys(), foreign_movie_data))
#      
#     '''Build a dictionary with url as keys and U.K. gross as values'''    
#     for k, v in foreign_movie_dict.iteritems():
#         if len(v) == 1:
#             soup = build_soup_page(foreign_url_pages[k])
#             if soup.find(text = re.compile('United Kingdom')):
#                 v['United Kingdom'] = v.pop('FOREIGN TOTAL')
#      
#     uk_movie_gross = {}
#     
#     for k, v in foreign_movie_dict.iteritems():
#          if 'United Kingdom' in v.keys():
#            uk_movie_gross[k] =  v['United Kingdom']
#==============================================================================
        

def main():
    '''Skip web scraping and use pickled movie data of website url and html data'''
    jar_of_pickles = eat_pickles('page_data.pkl')
    
    '''Deletes key that has odd characters in the movie title'''    
    del jar_of_pickles['http://www.boxofficemojo.com/movies/?id=lecombatdanslile.htm']
    
    uk_movie_gross = eat_pickles('uk_movie_gross_final.pkl') 
    
    '''Build a data structure of url, title, domestic gross, release date, actor list, 
    genre, budget, and uk total gross'''    
    title = []
    domestic_total_gross = []
    release_date = []
    budget = []
    genre = []
    uk_total_gross = []
    BOM_url = []
    actor_list_1 = []
    
    for url in uk_movie_gross.iterkeys():
        main_page = url[:37] + url[47:]
        main_html = jar_of_pickles[main_page]
        soup = build_soup_page(page=main_html)
        #Title
        title.append(get_movie_title(soup))
        #Domestic Total gross
        domestic_total_gross.append(get_movie_gross(soup))
        #Release Date
        release_date.append(get_movie_release_date(soup))
        #U.K. Total Gross
        uk_total_gross.append(uk_movie_gross[url])
        #Box office mojo URL
        BOM_url.append(main_page)
        #Actor lists
        actor_list_1.append(get_movie_actors(soup))
        #Genre
        genre.append(get_movie_genre(soup))
        #Budget
        budget.append(get_movie_budget(soup))
        
    feature_list = zip(BOM_url, title, domestic_total_gross, release_date, \
                        uk_total_gross, budget, actor_list_1, genre)
     
    '''Loop through list of movies and gather titles to get country info'''
    country_titles = []
    
    for movie in feature_list:
        country_titles.append(movie[1])  
        
    '''Loop through actor list and find movies that don't have a list of actors
    and create a list of movie titles to scrape for additional actors '''
    titles_to_scrape = []

    for i, actors in enumerate(actor_list_1):
        if len(actors) == 0:
            titles_to_scrape.append(title[i])

    actor_list_2 = get_actors_country(titles_to_scrape, actor=True)
    country_list = get_actors_country(country_titles, country=True)    

    '''Unpacks the title and actors to add to feature_list, then loops through 
    feature_list and adds it to the list for actors'''    
    add_actors_to_feature_list = zip(titles_to_scrape, actor_list_2)
    for el in add_actors_to_feature_list:
        for movie in feature_list:
            if el[0] in movie and len(movie[5]) == 0:
                movie[5].extend(el[1])
                
    '''Unpack country and movie title and append to final_4 '''
    add_country_to_feature_list = zip(country_titles, country_list)
    for el in add_country_to_feature_list:
        for movie in feature_list:
            if el[0] in movie:
                movie.append(el[1])
                
    with open('movie_features.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)

        i = 0
        for movie in feature_list:
            csvwriter.writerow(movie)
            print 'row %i written' % i
            i += 1
            print 'success'

        
if __name__ == '__main__':
    feature_list = main()
    print feature_list
    
    
    
    
    
    
    
    
