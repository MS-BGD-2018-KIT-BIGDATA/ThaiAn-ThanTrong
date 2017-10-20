## Generate a datafile with used Renault Zoe cars prices in IdF, PACA and Aquitaine
## File must contain :
## Car Version | Year | kms | Price | Telephone | Professional / Person

import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import numpy as np
import os
import time
import re
import itertools

# Regions
regions = ['ile_de_france', 'paca', 'acquitaine']
url = 'https://www.leboncoin.fr/voitures/offres/{}/?brd=Renault&mdl=Zoe&f=p'
max_rank = 5

versions = r'life|intens|zen'

# Using BeautifulSoup
def getSoupFromURL(url, method='get', data={}):
    
    if method == 'get':
        res = requests.get(url)
    elif method == 'post':
        res = requests.post(url, data=data)
    else:
        return None
    
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup
    else:
        return None

def getAllLinks(url):
    soup = getSoupFromURL(url)
    
    if soup:
        all_cars = soup.find_all("a", class_="list_item clearfix trackable")
        links = ["http:" + car['href'] for car in all_cars]

    return links

# Get info for a given car
def getInfoCar(link):
    soup = getSoupFromURL(link)

    car_info = {}
    classes = ['item_price clearfix', 'clearfix']
    if soup:
        
        ### COLLECT DATA ###
        # Properties - Values
        properties = list(map(lambda x: x.text.strip().lower(), soup.find_all("span", class_='property')))
        values = list(map(lambda x: x.text.strip().lower(), soup.find_all("span", class_='value')))
        
        car_info = {property : value for property, value in zip(properties, values)}
        
        # Version #
        description = soup.find_all('p', class_='value')[0].text.strip().lower()
        s = re.search(versions, description)
        if s :
            version = s.group(0)
        else:
            version = 'Unknown'
        car_info['version'] = version
        
        ### CLEANING ###
        # Remove currency sign
        car_info['prix'] = float(car_info['prix'].replace('\xa0€', '').replace(' ', ''))
        
        # Km
        car_info['kilométrage'] = float(car_info['kilométrage'].replace('km', '').replace(' ', ''))
        
        # Year
        car_info['année-modèle'] = int(car_info['année-modèle'])

        ### FIND SELLER ###
        seller = soup.find_all("p", class_="title")[0].text.strip()
        car_info['vendeur'] = seller
        
        return car_info

# Build dataframe with cars information
def buildDataFrame(list_cars):
    df = pd.DataFrame(list_cars)
    
    return df

# Get price from argus website
def getInfoArgus(version):
    url_argus = 'https://www.lacentrale.fr/cote-auto-renault-zoe-{}+charge+rapide-2013.html'.format(version)
    
    soup = getSoupFromURL(url_argus)
    
    if soup:
        price = soup.find_all("span", class_='jsRefinedQuot')[0].text.strip().replace(' ', '')
        return(float(price))

# Add to the previous dataframe
def buildArgusDataFrame(df):
    argus = {version : getInfoArgus(version) for version in versions.replace('r', '').split('|')}
    
    df['argus'] = df['version'].map(argus)
    return df

# Main
if __name__ == "__main__":
    start_time = time.time()
    
    lists = [getAllLinks(url.format(region)) for region in regions]
    links = list(itertools.chain.from_iterable(lists))
    
    list_cars = [getInfoCar(link) for link in links]
    
    df = buildDataFrame(list_cars)
    
    buildArgusDataFrame(df)
    
    print(df)

    print("\nTime elapsed to get avg stargazer per user : {} s".format(time.time() - start_time))


