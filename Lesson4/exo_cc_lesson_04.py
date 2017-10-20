# Labo | Qté principe actif | Année commercialisation | Mois | Prix | Restriction age | Restriction poids

import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import re
import numpy as np
import os

api = "https://open-medicaments.fr/api/v1/medicaments"


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

def getInfoMed():

    api_url = api + "?query=ibuprof%C3%A8ne"
    res = requests.get(api_url)
    assert res.status_code == 200
    all = json.loads(res.text)

    list = []

    for element in all:
        id = element['codeCIS']

        url_med = api + "/" + id
        res = requests.get(url_med)
        assert res.status_code == 200
        info_med = json.loads(res.text)

        cols = {}

        # LABO
        cols['Labo'] = info_med['titulaires'][0]

        # PRINCIPE ACTIF
        s_mg = re.search("(\d{1,3}) mg", info_med['compositions'][0]['substancesActives'][0]['dosageSubstance'])
        if s_mg is not None: # convert mg to g
            qty = float(s_mg.group(1)) / 10
        else:
            qty = float(info_med['compositions'][0]['substancesActives'][0]['dosageSubstance'].split()[0])

        cols['Qte principe actif (g)'] = qty

        # ANNEE COMMERCIALISATION
        cols['Annee commercialisation'] = info_med['presentations'][0]["dateDeclarationCommercialisation"].split("-")[0]

        # MOIS COMMERCIALISATION
        cols['Mois commercialisation'] = info_med['presentations'][0]["dateDeclarationCommercialisation"].split("-")[1]

        # PRIX
        cols['Prix'] = info_med['presentations'][0]["prix"]

        # RESTRICTION AGE
        s = re.search("(\d{1,2}) an", info_med['indicationsTherapeutiques'])
        if s is not None:
            cols['Restriction age'] = s.group(1)
        else :
            cols['Restriction age'] = np.NaN

        # RESTRICTION AGE
        s = re.search("(\d{1,2}) kg", info_med['indicationsTherapeutiques'])
        if s is not None:
            cols['Restriction poids (kg)'] = s.group(1)
        else:
            cols['Restriction poids (kg)'] = np.NaN

        list.append(cols)

    df = pd.DataFrame(list, columns=['Labo', 'Qte principe actif (g)', 'Annee commercialisation', 'Mois commercialisation', 'Restriction age', 'Restriction poids (kg)'])
    return df


# Main
if __name__ == "__main__":
    df = getInfoMed()
    print(df)

    if os.path.isfile("open_medicaments.csv"):
        os.remove("open_medicaments.csv")
    df.to_csv("open_medicaments.csv", sep=";")