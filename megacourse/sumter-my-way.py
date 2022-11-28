import requests
from bs4 import BeautifulSoup
import sqlite3
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
import time

url = 'http://portal.sumtercountysheriff.org/smartwebclient/jail.aspx'
html = requests.get(url)

with open("settings.json", "r") as f:
    settings = json.load(f)

s = BeautifulSoup(html.content, 'html.parser')

inmates = s.find(id='JailInfo')

name = inmates.find_all('td', class_='SearchHeader')

status = inmates.find_all('td', class_='InmateInfoGridTd')

age = inmates.find()('td', class_='InmateInfoGridTd')

webhook = DiscordWebhook(url=settings['discordWebhook'])
embed = DiscordEmbed()
embed = DiscordEmbed()
embed.set_description(f"**Name:** {name[0]}\n\n**Status**{status[0]}\n\n**Age**{age[0]}")
embed.set_color(0xFFFFFF)    

webhook.add_embed(embed)
response = webhook.execute()