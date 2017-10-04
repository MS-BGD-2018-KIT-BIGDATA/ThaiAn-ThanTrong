import requests
import pandas as pd
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
import json

plt.style.use('ggplot')

rank_limit = 10

url = 'http://gist.github.com/paulmillr/2657075'
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
    
    df = pd.DataFrame(index=range(1, rank_limit + 1), columns=['Rank', 'Name'])
    
    if soup:
        for i in range(1, rank_limit + 1):
            contributor = soup.find_all(contr)[i]
            rank = contributor.select('th')[0].text
            name = contributor.select('a')[0].text
            df.loc[i, 'Rank'] = rank
            df.loc[i, 'Name'] = name
    df = df.set_index('Rank')
    return df

# Get the average number of stars for a contributor's set of repositories
# param : String contributor, the pseudo of the contributor
# return : Float avg, average number of stars
def getStarsContributor(contributor):
    repo_url = 'https://api.github.com/users/' + contributor + '/repos'
    res = requests.get(repo_url)
    repositories = json.loads(res.text)
    
    nb_repos = len(repositories)
    # print('Number of repositories : ' + str(nb_repos))
    nb_stars = 0

    for repo in repositories:
        try:
            nb_stars += repo['stargazers_count']
        except ValueError:
            print('Value is not int')
    avg = round(float(nb_stars) / float(nb_repos), 2)
    return avg

# Get stars for all contributors
# param : DataFrame df, a DataFrame that contains the top contributors
# returns : DataFrame df_stars, a new DataFrame with rankings
def getStarsAll(df):
    contributors = df['Name'].tolist()

    df_stars = df = pd.DataFrame(index=range(0, rank_limit), columns=['Name', 'Average number of stars'])
    for i in range(0, rank_limit):
        contributor = contributors[i]
        print(contributor)
        df_stars.loc[i, 'Name'] = contributor
        df_stars.loc[i, 'Average number of stars'] = getStarsContributor(contributor)
    df_stars = df_stars.sort('Average number of stars', ascending=False)
    return df_stars


if __name__ == "__main__":
    print('--------------- CONTRIBUTORS ---------------')
    df = getContributors(url)
    print(df)

    print('------------------- STARS ------------------')
    df_stars = getStarsAll(df)
    print(df_stars)

    print('------------------- RECAP ------------------')
    x = df_stars.index.values # ranks
    y = df_stars['Average number of stars'].tolist() # number of stars
    pseudos = df_stars['Name']
    print(x,y)
    plt.scatter(x, y, s=50)
    
    # Write pseudo for each point
    for ind in range(len(x)):
        plt.text(x[ind], y[ind], pseudos[x[ind]], horizontalalignment='center', verticalalignment='top')
    plt.show()



