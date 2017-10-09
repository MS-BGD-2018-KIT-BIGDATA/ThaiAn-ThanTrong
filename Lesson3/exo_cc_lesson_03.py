import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import numpy as np
import os
import time
from itertools import combinations
import googlemaps as gm

api_key = 'AIzaSyBjOYEcZSJVPnpkjxcn9dCEcqw4LDH0w1s '

url = 'https://lespoir.jimdo.com/2015/03/05/classement-des-plus-grandes-villes-de-france-source-insee/'

max_rank = 100

client = gm.Client(key=api_key)

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

# Get the 100 biggest cities in France
# param : String url, url that contains the ranking
# output : DataFrame rank_city, a DataFrame with rank and cities
def getCities(url):
    soup = getSoupFromURL(url)

    rk = "td"
    cl = "x165"
    
    if soup:
        all_cities = soup.find_all("tr")[:max_rank ]

        rank_city = pd.DataFrame.from_records(list(map(lambda x: (x.select(rk)[0].text.split()[0], x.select(rk)[1].text.split()[0]), all_cities)))

        # Header
        new_header = rank_city.iloc[0] #grab the first row for the header
        rank_city = rank_city[1:] #take the data less the header row
        rank_city.columns = new_header #set the header row as the df header
        
        return rank_city

# Compute distance matrix
# param : String origin, destination : cities of origin and destination respectively
# output : distance between the two cities
def getDistance(origin, destination):
    api_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?key={}&origins={}&destinations={}'.format(api_key, origin, destination)
    res = requests.get(api_url)
    assert res.status_code == 200
    all = json.loads(res.text)

    elements = all['rows'][0]['elements'][0]
    if 'distance' in elements.keys():
        distance = elements['distance']['value']
    else:
        distance = 0
    return distance

# Using gm
# param :  list cities, a list of cities
# output : DataFrame df, a DataFrame with distances between each cities
def getDistanceImproved(cities):
    pairs = list(combinations(cities, 2)) # compute all possible combination without any redondance : if we have (a,b) we don't need (b,a)
    
    # concatenate cities
    conc_cities = '|'.join(cities)
    destinations = conc_cities
    origins = conc_cities
    
    maps_matrix = gm.client.distance_matrix(client, origins, destinations)
    
    distances = [[maps_matrix['rows'][i]['elements'][j]['distance']['value'] \
                 for i in range(len(maps_matrix['rows'][j]['elements']))] \
                 for j in range(len(maps_matrix['rows']))]
    
    df = pd.DataFrame(distances, index = cities, columns = cities)
    return df

# Handle cases with no distance value
def catch(val):
    try:
        return val
    except KeyError:
        return 0

# Main
if __name__ == "__main__":
    start_time = time.time()
    rank_city = getCities(url)
    
    cities = rank_city.Ville.tolist()

    ## USING DATAFRAME
    final_matrix = getDistanceImproved(cities)
    filename = 'exo_cc_lesson_03_result_{}.csv'.format(str(max_rank))
    if os.path.exists(filename):
        os.remove(filename)
    final_matrix.to_csv(filename, sep=';')

    print(final_matrix)
    print("\nTime elapsed to get avg stargazer per user : {} s".format(time.time() - start_time))
