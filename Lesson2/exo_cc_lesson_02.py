import requests
import pandas as pd
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt

plt.style.use('ggplot')

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

def getPrice(url, df, brand, rg):
    # TODO
    before_sales = 'prdtPrSt' # before price was changed (optional)
    current_price = 'price' # current price (compulsory)
    
    price = 'prdtPrice' # groups all
    soup = getSoupFromURL(url)
    if soup:

        price_content = soup.find_all(class_ = price)
        
        main_price_list = []
        sub_price_list = []
        diff_list = []
        
        for i in rg:
            main_price = float(price_content[i].parent.select("." + current_price)[0].text.replace('€', '.'))
            # print('Product price : ' +  str(main_price))
            
            main_price_list.append(main_price)
            
            # Case there are sales on the product
            if (len(price_content[i].parent.select("." + before_sales)) > 0):
                sub_price = float(price_content[i].parent.select("." + before_sales)[0].text.replace(',', '.'))
                # print('Before sales : ' + str(sub_price))
                sub_price_list.append(sub_price)
            
            else:
                # print('No sales on that product')
                sub_price = main_price
                sub_price_list.append(sub_price)
        
            diff = abs((main_price - sub_price) * 100 / sub_price)
            diff_list.append(diff)

        # Store everything in a DataFrame
        df.loc[:, brand] = diff_list
        return df


### IDEA : HISTOGRAM WITH ALL PERCENTAGES

if __name__ == "__main__":
    brands = ['dell', 'acer']
    
    range = range(22)
    df = pd.DataFrame(index=range, columns=brands)
    for brand in brands:
        url = 'https://www.cdiscount.com/informatique/ordinateurs-pc-portables/pc-portables/lf-228394_6-' + brand + '.html#_his_'

        df = getPrice(url, df, brand, range)
    print(df)

    df.plot.hist(alpha=0.5)

    plt.xlabel('Sales percentage')

    plt.show()
    plt.close()

	 
