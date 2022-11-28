import requests
from bs4 import BeautifulSoup
import sqlite3
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
import time

url = 'https://realpython.github.io/fake-jobs/'
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')

with open("settings.json", "r") as f:
    settings = json.load(f)

text_remove_tag=soup.find("h3").get_text()

inmates = soup.find(id='ResultsContainer')

name = inmates.find( class_='subtitle is-6 company')


webhook = DiscordWebhook(url=settings['discordWebhook'])
embed = DiscordEmbed()
embed = DiscordEmbed()
embed.set_description(f"**NAME:** {name}\n\n")
embed.set_color(0xFFFFFF)    

webhook.add_embed(embed)
response = webhook.execute()