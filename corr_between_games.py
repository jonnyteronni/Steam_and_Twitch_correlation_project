import pandas as pd
from os import listdir
from os.path import isfile, join, splitext
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose


categories = ['singleplayer','multiplayer']

master_df  = []
file_number = 0
for cat in categories:
    mypath = 'data/{}/'.format(cat)
    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    
    for file in files:
        path = 'data/{}/'.format(cat) + file
        data = pd.read_csv(path, sep=',')
        if file_number == 0:
            master_df = pd.read_csv(path, sep=',')
            master_df['Game_name'] = splitext(file)[0]
        else:
            new_csv = pd.read_csv(path, sep=',')
            new_csv['Game_name']= splitext(file)[0]
            master_df = pd.merge(master_df,new_csv,how='outer')
        file_number = 1
    

master_df.fillna(0, inplace=True)



def corr_between_games(game_a,game_b):
    # Filter equal dates
    #comum_df =  master_df[(master_df['Game_name']=='PUBG')|(master_df['Game_name']=='dayz')]
    
 
    a_df = master_df[master_df['Game_name']==game_a]
    b_df = master_df[master_df['Game_name']==game_b]
    
    # If there are no comumn dates, function returns nothing
    test_df =a_df.where(a_df['DateTime'].isin(b_df['DateTime']))
    if test_df['DateTime'].count()==0:
        print('\nNo comumn date between {} and {}.'.format(game_a,game_b))
        return
    
    
    comum_df = a_df.merge(b_df, on = 'DateTime')
    
    moving_corr_df = comum_df[['Players_x','Players_y']].rolling(30).corr()
    
    moving_corr_df.reset_index(inplace=True)
    
    # moving_corr_df.set_index('name', inplace = True)
    
    result = moving_corr_df[moving_corr_df['level_1']=='Players_x']['Players_y'].tail(360)
    
    
    
    #result = comum_df.corr()
     
    print(result)
    
    #result_2 = seasonal_decompose(result.dropna(), model='additive', freq=1)
    
    # Plotting dataframes
    fig = plt.figure()
    comum_df[['DateTime','Players_x','Players_y']].plot('DateTime')
    a_df.plot('DateTime','Players')
    b_df.plot('DateTime','Players')
    
    #result_2.plot()
    plt.show()
    
    result.plot()
    plt.show()

corr_between_games('dota2','poe')

print(master_df['Game_name'].unique())


