import pandas as pd
from os import listdir
from os.path import isfile, join, splitext
import matplotlib.pyplot as plt
import re


# Get all steam data to a dataframe
def get_steam_dataframe(categories):
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
        
    master_df.dropna(subset=['Players', 'Twitch Viewers'],how='all', inplace=True)
    #master_df.fillna(0, inplace=True)
    
    master_df['DateTime'] = pd.to_datetime(master_df['DateTime'])
    master_df['DateTime'] = master_df['DateTime'].astype('datetime64[D]')
    
    
    
    games_list = master_df['Game_name'].unique()
    
    return master_df,games_list



# Data cleaning for games names on stream dataframe
def clean_stream_games_names(games_unclean):
    result = re.split('\|',games_unclean)
    game_temp_list = []
    for number in range(len(result)):
        if number == 0 or number % 3 == 0:
            game_temp_list.append(result[number])
    return game_temp_list




# Get all streams to a dataframe
def get_streamers_dataframe(streamers):
    master_streams_df  = []
    file_number = 0
    for st in streamers:
        mypath = 'data/streamers/{}/'.format(st)
        files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    
        
        for file in files:
            path = 'data/streamers/{}/'.format(st) + file
            data = pd.read_csv(path, sep=',')
            if file_number == 0:
                master_streams_df = pd.read_csv(path, sep=',')
                master_streams_df['Streamer_name'] = st
            else:
                new_csv = pd.read_csv(path, sep=',')
                new_csv['Streamer_name']= st
                master_streams_df = pd.merge(master_streams_df,new_csv,how='outer')
            file_number = 1
        
    
    streamers_list = master_streams_df['Streamer_name'].unique()
    
    master_streams_df['Games_name'] = master_streams_df['Games'].apply(lambda x: clean_stream_games_names(x))
    
    master_streams_df['Stream start time'] = pd.to_datetime(master_streams_df['Stream start time'])
    master_streams_df['Stream start time'] = master_streams_df['Stream start time'].astype('datetime64[D]')
    master_streams_df.drop_duplicates(subset=['Stream start time'],keep='first', inplace=True)
    return master_streams_df, streamers_list



def corr_between_games(game_a,game_b,master_df):
    # Filter equal dates

    a_df = master_df[master_df['Game_name']==game_a]
    b_df = master_df[master_df['Game_name']==game_b]
    
    # If there are no comumn dates, function returns nothing
    test_df =a_df.where(a_df['DateTime'].isin(b_df['DateTime']))
    if test_df['DateTime'].count()==0:
        print('\nNo comumn date between {} and {}.'.format(game_a,game_b))
        return
    
    
    comum_df = a_df.merge(b_df, on = 'DateTime')

    comum_df['Moving_corr'] = comum_df['Players_x'].rolling(30).corr(comum_df['Players_y'])

    # Plotting dataframes
    fig = plt.figure()
    comum_df[['DateTime','Players_x','Players_y']].plot('DateTime')
    
    a_df.plot('DateTime','Players')
    b_df.plot('DateTime','Players')
    plt.show()

    # Quantiles
    lower_qt = comum_df['Moving_corr'].quantile(0.25)
    median = comum_df['Moving_corr'].quantile(0.5)
    upper_qt = comum_df['Moving_corr'].quantile(0.75)
    # Plotting
    comum_df.plot(x ='DateTime', y='Moving_corr',label="30 days moving correlation",color='black')
    #plt.annotate('Local Max',xy=('2019-07-05',df['Moving_corr'].tail(1).values))
    plt.axhline(y=lower_qt, color='red',xmin =0.02, xmax = 0.98, label="Lower quartile")
    plt.axhline(y=median, color='yellow',xmin =0.02, xmax = 0.98,label="Median")
    plt.axhline(y=upper_qt, color='green',xmin =0.02, xmax = 0.98,label="Upper quartile")
    plt.gca().set(title='Impact of {} in {}'.format(game_a,game_b))
    plt.show()
    

    

def corr_players_twitchviewers(df,games_list,graphs):
    for game in games_list:
        
        temp_df = df[df['Game_name']==game]
        temp_df['Twitch Viewers'].fillna(0, inplace=True)
        temp_df.dropna(subset=['Players', 'Twitch Viewers'],inplace=True)
        temp_df['Moving_corr'] = temp_df['Players'].rolling(30).corr(temp_df['Twitch Viewers'])
        temp_df.dropna(subset=['Moving_corr'])
        
        if graphs:
            # Quantiles
            lower_qt = temp_df['Moving_corr'].quantile(0.25)
            median = temp_df['Moving_corr'].quantile(0.5)
            upper_qt = temp_df['Moving_corr'].quantile(0.75)
            
            # Plotting
            temp_df.plot(x ='DateTime', y='Moving_corr',label="30 days moving correlation",color='black')
            #plt.annotate('Local Max',xy=('2019-07-05',df['Moving_corr'].tail(1).values))
            plt.axhline(y=lower_qt, color='red',xmin =0.02, xmax = 0.98, label="Lower quartile")
            plt.axhline(y=median, color='yellow',xmin =0.02, xmax = 0.98,label="Median")
            plt.axhline(y=upper_qt, color='green',xmin =0.02, xmax = 0.98,label="Upper quartile")
            plt.gca().set(title='Impact of Twitch viewers in game {} player base'.format(game))
            plt.show()
    
    return corr_list




def get_streamer_to_steam(date,game,streamer_df,streamer):
    temp_df = streamer_df[(streamer_df['Stream start time']==date) & (streamer_df['Games_name'].str.contains(game,regex=False))]
    if not temp_df.empty:
        return "{}|{}".format(streamer, temp_df['Stream length'].values)
        
   
   
def merge_streamer_steam(steam_df,streamer_df,streamer, graphs):
    
    streamer_df = streamer_df[streamer_df['Streamer_name']==streamer]
    
    steam_df['temp']  = steam_df[['DateTime','Game_name']].apply(lambda x:get_streamer_to_steam(x['DateTime'],x['Game_name'],streamer_df,streamer),axis = 1)
    
    steam_df['Streamer'] = None
    steam_df['Stream_length'] = None
    steam_df[['Streamer','Stream_length']] = steam_df['temp'].str.split('|',expand=True)
    steam_df['Stream_length'] = steam_df['Stream_length'].str.replace("[",'')
    steam_df['Stream_length'] = steam_df['Stream_length'].str.replace("]",'')
    steam_df['Stream_length'] = pd.to_numeric(steam_df['Stream_length'])
    
    return steam_df
    

def corr_streamer_steam(df,graphs,streamer,game):

    df = df[df['Game_name']==game]
    df['Stream_length'].fillna(0,inplace=True)
    df['Moving_corr'] = df['Players'].rolling(30).corr(df['Stream_length'])
    df.dropna(subset=['Moving_corr'])
    
    if graphs:
        # Quantiles
        lower_qt = df['Moving_corr'].quantile(0.25)
        median = df['Moving_corr'].quantile(0.5)
        upper_qt = df['Moving_corr'].quantile(0.75)
        
        # Plotting
        df.plot(x ='DateTime', y='Moving_corr',label="30 days moving correlation",color='black')
        #plt.annotate('Local Max',xy=('2019-07-05',df['Moving_corr'].tail(1).values))
        plt.axhline(y=lower_qt, color='red',xmin =0.02, xmax = 0.98, label="Lower quartile")
        plt.axhline(y=median, color='yellow',xmin =0.02, xmax = 0.98,label="Median")
        plt.axhline(y=upper_qt, color='green',xmin =0.02, xmax = 0.98,label="Upper quartile")
        plt.gca().set(title='Impact of streamer {} in game {}'.format(streamer,game))
        plt.show()
        
    return df

# Get all data

categories = ['singleplayer','multiplayer']

steam_df, games_steam_list = get_steam_dataframe(categories)


streamers = ['dota2ruhub','ESL_CSGO']#,'dota2ruhub'] 'summit1g','xQcOW'

streamer_df, streamers_list = get_streamers_dataframe(streamers)


# 1
# steam_corr_df = merge_streamer_steam(steam_df,streamer_df,streamer = 'dota2ruhub',graphs = False)
steam_corr_df = merge_streamer_steam(steam_df,streamer_df,streamer = 'ESL_CSGO',graphs = False)
# steam_streamer_corr_df = corr_streamer_steam(steam_corr_df,graphs=True,streamer = 'dota2ruhub', game = 'Dota 2')
steam_streamer_corr_df = corr_streamer_steam(steam_corr_df,graphs=True,streamer = 'ESL_CSGO', game = 'Counter-Strike: Global Offensive')


# 2
corr_between_games('PRO EVOLUTION SOCCER 2019','eFootball PES 2020',steam_df)


# 3 Correlation between player count and twitch viewers
corr_list = []
corr_list = corr_players_twitchviewers(steam_df,games_steam_list,graphs=True)

