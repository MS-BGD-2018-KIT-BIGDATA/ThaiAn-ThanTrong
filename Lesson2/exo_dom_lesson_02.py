import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


# Count results for Paris from 2010 to 2015

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


def get_soup_year(year):
    url_search = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=' + year

    class_results = "libellepetit G"  # look for A, B, C and D

    soup = getSoupFromURL(url_search)

    res = soup.find_all("td", class_=class_results)

    euros_par_hab = [int(r.parent.select_one("td:nth-of-type(2)").text.replace('\xa0', '').replace(' ', '')) for r in
                     res if
                     re.search('= [ABCD]\Z', r.text)]
    moyenne_par_strate = [int(r.parent.select_one("td:nth-of-type(3)").text.replace('\xa0', '').replace(' ', '')) for r
                          in res if
                          re.search('= [ABCD]\Z', r.text)]

    return euros_par_hab, moyenne_par_strate


# Reorganise the extracted data and create DataFrames
def get_soup_all(years):
    columns = ['A', 'B', 'C', 'D']

    df_euros_hab = pd.DataFrame(index=years, columns=columns)
    df_euros_hab.name = 'Euros par habitant'

    df_moyenne_strat = pd.DataFrame(index=years, columns=columns)
    df_moyenne_strat.name = 'Moyenne de la strate'

    for year in years:
        euros_par_hab, moyenne_par_strate = get_soup_year(year)
        df_euros_hab.loc[year, 'A':'D'] = euros_par_hab
        df_moyenne_strat.loc[year, 'A':'D'] = moyenne_par_strate

    return df_euros_hab, df_moyenne_strat


if __name__ == "__main__":
    years = ['2010', '2011', '2012', '2013', '2014', '2015']

    print('------ EUROS PAR HABITANT --------')
    df_euros_hab, df_moyenne_strat = get_soup_all(years)
    print(df_euros_hab)
    print()

    print('------ MOYENNE PAR STRATE --------')
    print(df_moyenne_strat)
    print('----------------------------------')
