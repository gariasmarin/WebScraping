# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 15:02:03 2022

@author: gabri
"""

# grab data : https://stackoverflow.com/questions/10556048/how-to-extract-tables-from-websites-in-python
# pickle : https://stackoverflow.com/questions/11218477/how-can-i-use-pickle-to-save-a-dict

import requests
import pandas as pd
import pickle
from matplotlib import pyplot as plt
import numpy as np

def grab_year(year):
    # Saves financial tables from a government website
    # The result is returned
    url = 'https://www.treasury.gov/resource-center/data-chart-center/interest-rates/pages/TextView.aspx?data=yieldYear&year='
    url_year = url + str(year)
    raw_html = requests.get(url_year).content
    df = pd.read_html(raw_html)[1]
    # df.to_csv('data_'+str(year)+'.csv') #another saving option
    return df

def scrape():
    # Collects the tables for a range of years
    # Saves the result as a pickle
    # Minimize the impact on the website by accessing the data only once
    # and saving it in a pickle file.
    data = [ grab_year(i) for i in range(2000,2022) ]
    with open('data.p', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

def load_data(fn):
    # Load the pickle file from a filename
    # Return that
    with open('data.p', 'rb') as handle:
        table_data = pickle.load(handle)
        
    #print (table_data)
    return table_data
    

def get_date_changes(dates):
    # Returns a list of tuples from the dataframe dates column
    # The tuple will be [index of change, last two digits of year]
    #   The type will be a List[int, string]
    dc_list= []
    for index, item in enumerate(dates):
        temp_list = []
        
        if index == 0:
            temp_list.append(index)
            temp_list.append(item[6:8])
            dc_list.append(temp_list)
        else:
            current_year = item[6:8]
            previous_index = dates[index-1]
            previous_year = previous_index[6:8]
            
            if current_year != previous_year:
               temp_list.append(index)
               temp_list.append(current_year)
               dc_list.append(temp_list)
    
    temp_list = [len(dates), '22']
    dc_list.append(temp_list)
    
    return dc_list


def plot_data(cols, r):
    # Plot each of the columns in a loop using plt
    # Add the column name as a label
    plt.figure(figsize=(16,9))   
    for i in range(len(cols)):
        if i == 0:
            continue
        
        plt.plot(r[cols[i]].values, label = cols[i])
    
    

def plot_finalize(dc, r):
    xticks = []
    xlabels = []
    for i in dc:
        xticks.append(i[0])
        xlabels.append(i[1])
    plt.xticks(xticks, xlabels)
    plt.xlim([0,5506])
    plt.ylim([0,7.5])
    plt.legend(loc= 'upper right') 
    
    plt.grid()
    plt.show()

def wrangle():
    # Load the pickle data
    data = load_data('data.p')
    
    # Concatenate data frames and set NaN values to -1 with fillna
    r = pd.concat(data).fillna(-1)
    
    # Get column names
    cols = data[0].columns
    # Get times the year changed
    dc = get_date_changes(r[cols[0]].values)

    # Plot 
    plot_data(cols, r)
    plot_finalize(dc, r)

    # Visually cross verify the 30 yr with the following link
    # https://www.macrotrends.net/2521/30-year-treasury-bond-rate-yield-chart

if __name__ == "__main__":
  
    scrape() 
    #load_data('data.p')

    wrangle()
