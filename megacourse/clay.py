import requests
from bs4 import BeautifulSoup
import sqlite3
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
import time

url = 'https://claysheriff.policetocitizen.com/Inmates/Catalog'
html = requests.get(url)

with open("settings.json", "r") as f:
    settings = json.load(f)

s = BeautifulSoup(html.content, 'html.parser')

firstSection = first_inmate.find("td", class_ ="col-xs-11 col-sm-5 text-left")

first_inmate = table_of_imates.find("tr", class_= "raText")

inmates = s.find("div", class_= "ng-scope")

name = firstSection.find_all("span")[1].text


webhook = DiscordWebhook(url=settings['discordWebhook'])
embed = DiscordEmbed()
embed = DiscordEmbed()
embed.set_description(f"**Name:** {age[0]}\n\n")
embed.set_color(0xFFFFFF)    

webhook.add_embed(embed)
response = webhook.execute()