import pandas as pd

def createf_df(sold_list):
    # Create formatted dataframe of the sold properties
    houses_pd = pd.DataFrame(sold_list)
    houses_pd.date = pd.to_datetime(houses_pd.date, format="%d/%m/%y")
    houses_pd.price = houses_pd.price.str.replace('[\€\,\ **]', '').astype(int)
    return houses_pd