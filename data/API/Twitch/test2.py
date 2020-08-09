#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 13:56:53 2020

@author: jonnyteronni
"""
from requests_oauthlib import OAuth2Session
import requests

url  = "https://id.twitch.tv/oauth2/validate"
client_id= '5cz0yhsd4m6yqrzcd5t62d09wdbtn7'
token= 'lvzyj81mvg770cz8ab4ttfcncwgqw2'
user_id = '74995207'
user_login = 'jonnyteronni'
response = requests.get(url)
# print(response)

client = OAuth2Session(client_id, token=token)

r = client.get(url)

# print(client)



curl -H 'Client-ID: uo6dggojyb8d6soh92zknwmi5ej1q2' \ -H 'Authorization: Bearer cfabdegwdoklmawdzdo98xt2fo512y' \ -X GET 'https://api.twitch.tv/helix/analytics/games?first=5'