import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import time

rank_limit = 10

url = 'http://gist.github.com/paulmillr/2657075'

my_token = ''
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

# Get top contributors
# param : String url, the webpage that lists the contributors
# returns : DataFrame df, a DataFrame that sums up the rankings
def getContributors(url):
    contr = 'tr'
    soup = getSoupFromURL(url)
    
    df = pd.DataFrame(index=range(1, rank_limit +1), columns=['Rank', 'Pseudo'])
    
    if soup:
        
        contributors = {int(contrib.select('th')[0].text.replace('#', '')) : contrib.select('a')[0].text for contrib in soup.find_all(contr) if contrib.select('th') and contrib.select('a')}
    
    s = pd.Series(contributors, index = contributors.keys())
    s = s.sort_index()
    return s

# Get the average number of stars for a contributor's set of repositories
# param : String contributor, the pseudo of the contributor
# return : Float avg, average number of stars
def getStarsContributor(contributor):
    # token needs to be regenerated each time : https://github.com/settings/tokens
    my_headers = {'Authorization': 'token {}'.format(my_token)}
    
    repo_url = 'https://api.github.com/users/' + contributor + '/repos'
    res = requests.get(repo_url, headers=my_headers)
    assert res.status_code == 200
    repositories = json.loads(res.text)
    
    nb_repos = len(repositories)

    nb_stars = 0

    nb_stars = sum([repo['stargazers_count'] for repo in repositories])

    if nb_repos != 0:
        avg = round(float(nb_stars) / float(nb_repos), 2)
    else :
        avg = 0
    return avg

# Get stars for all contributors
# param : DataFrame df, a DataFrame that contains the top contributors
# returns : DataFrame df_stars, a new DataFrame with rankings
def getStarsAll(s_contrib):
    contributors = s_contrib.tolist()

    contrib_stars = {contributor : getStarsContributor(contributor) for contributor in contributors}
    
    s = pd.Series(contrib_stars)
    s = s.sort_values(ascending=False)
    return s.to_frame()


if __name__ == "__main__":
    start_time = time.time()
    print('--------------- CONTRIBUTORS ---------------')
    contributors = getContributors(url)
    print(contributors)

    print('------------------- STARS ------------------')
    stars = getStarsAll(contributors)
    print(stars)

    print('------------------- RECAP ------------------')
    print("\nTime elapsed to get avg stargazer per user : {} s".format(time.time() - start_time))

    # Write in file
    stars.to_csv('average_number_stars.csv', header=None, index=True, sep=';')



