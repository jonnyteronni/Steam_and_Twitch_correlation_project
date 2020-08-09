import requests, json

BASE_URL = 'https://api.twitch.tv/helix/'
HEADERS = {
    'Client-ID': '5cz0yhsd4m6yqrzcd5t62d09wdbtn7',
    'Authorization': 'Bearer lvzyj81mvg770cz8ab4ttfcncwgqw2'}
INDENT = 2


# get response from twitch API call
def get_response(query):
  url  = BASE_URL + query
  response = requests.get(url, headers=HEADERS)
  return response

# used for debugging the result
def print_response(response):
  response_json = response.json()
  print_response = json.dumps(response_json, indent=INDENT)
  print(print_response)

# get the current live stream info, given a username
def get_user_streams_query(user_login):
  return 'streams?user_login={0}'.format(user_login)

def get_user_query(user_login):
  return 'users?login={0}'.format(user_login)

def get_user_videos_query(user_id):
  return 'videos?user_id={0}&first=50'.format(user_id)

def get_games_query():
  return 'games/top'


# curl -H "Authorization: OAuth lvzyj81mvg770cz8ab4ttfcncwgqw2" https://id.twitch.tv/oauth2/validate
