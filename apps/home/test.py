import requests
import bl
import scraper
import json

response=bl.get_station_weather(43279)
print(((json.dumps(response, indent = 4))))
print(type((json.dumps(response, indent = 4))))
