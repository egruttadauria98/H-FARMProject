import pandas as pd
import numpy as np

path_data = 'data.nosync/CarrOutput.csv'
df = pd.read_csv(path_data, sep=';')


#print(df.head())
#print(df.columns)
#print(df.shape)


cols = ['ProductName', 'FullPath', 'BuyboxPricedf_cost_product']
df_cost_product = df[cols].copy()


#print(df_cost_product.head())
#print(df_cost_product.isnull().values.any())
#print(df_cost_product.dtypes)


# Drop the NAN values after converting the 'None' strings to actual NANs.
def remove_none(row):
    if row == 'None':
        return np.nan
    return row


df_cost_product['BuyboxPricedf_cost_product'] = df_cost_product.BuyboxPricedf_cost_product.apply(lambda x: remove_none(x))
df_cost_product.dropna(axis=0, inplace=True)


# Change string to make it convertible to number
df_cost_product['BuyboxPricedf_cost_product'] = df_cost_product.BuyboxPricedf_cost_product.apply(lambda x: x[:-2].replace(',', '.').strip())

#print(df_cost_product.shape)
#print(df_cost_product.head())
#print(df_cost_product.dtypes)

# Convert price column from string to number
df_cost_product.BuyboxPricedf_cost_product = df_cost_product.BuyboxPricedf_cost_product.astype(float)
#print(df_cost_product.head())
#print(df_cost_product.dtypes)

# Group by average price by path
#df_average_price = df_cost_product[cols[1:]].groupby(by=['FullPath']).mean()
df_low_price = df_cost_product[cols[1:]].groupby(by=['FullPath']).quantile(0.2)
df_high_price = df_cost_product[cols[1:]].groupby(by=['FullPath']).quantile(0.8)
                                                                           
#print(df_average_price.index)
#print(df_average_price.head())


def compare_price(row):

    # Limit the comparison to the second digit

    category = row[1]
    price = float("{:.2f}".format(row[2]))
    #avg_price = float("{:.2f}".format(df_average_price[df_average_price.index == category].iloc[0, 0]))
    low_price = float("{:.2f}".format(df_low_price[df_low_price.index == category].iloc[0, 0]))
    high_price = float("{:.2f}".format(df_high_price[df_high_price.index == category].iloc[0, 0]))

    #if price == avg_price:
    #    return 'Avg'
    #if price > avg_price:
    #    return 'Pos'
    #if price < avg_price:
    #    return 'Neg'
    
    if price <= low_price:
        return 'Low'
    if price >= high_price:
        return 'High'


df_cost_product['premium'] = df_cost_product.apply(lambda x: compare_price(x), axis=1)
#print(df_cost_product.columns)
#print(df_cost_product.head())

#df_cost_product['dummy_above_price'] = 0
#df_cost_product['dummy_above_price'][df_cost_product['premium'] == 'Pos'] = 1

#df_cost_product['dummy_below_price'] = 0
#df_cost_product['dummy_below_price'][df_cost_product['premium'] == 'Neg'] = 1

#df_cost_product['dummy_equal_average'] = 0
#df_cost_product['dummy_equal_average'][df_cost_product['premium'] == 'Avg'] = 1

df_cost_product['low'] = 0
df_cost_product.loc[df_cost_product['premium'] == 'Low', 'low'] = 1

df_cost_product['high'] = 0
df_cost_product.loc[df_cost_product['premium'] == 'High', 'high'] = 1


# These are the same operations done on the names of the products in original JSON from Carrefour
df_cost_product['ProductName'] = df_cost_product['ProductName'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
df_cost_product['ProductName'] = df_cost_product['ProductName'].str.lower()

print(df_cost_product.head())

df_cost_product.to_csv('data.nosync/premium_price_products_percentiles.csv')
