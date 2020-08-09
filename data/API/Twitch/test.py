#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 23:50:03 2020

@author: jonnyteronni
"""


import twitch_integration

user_login = 'dota2ruhub'

query = twitch_integration.get_user_query(user_login)

response = twitch_integration.get_response(query)

twitch_integration.print_response(response)



