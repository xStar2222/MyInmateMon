import requests
from bs4 import BeautifulSoup
import sqlite3
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
import time

url = 'http://portal.sumtercountysheriff.org/smartwebclient/jail.aspx'
html = requests.get(url)

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'
}

with open("settings.json", "r") as f:
    settings = json.load(f)

s = BeautifulSoup(html.content, 'html.parser')



def main():
    response = requests.get(url, headers= headers)

    soup = BeautifulSoup(response.text, "html.parser")

    imatesDiv = soup.find("div", class_= "GridDIV")

    table_of_imates = imatesDiv.find("div", class_= "JailInfo")

    first_inmate = table_of_imates.find("tr", class_= "InmateRecordRow")

    inmates = s.find(id='grid')

    name = inmates.find_all('td', class_='SearchHeader')

    status = inmates.find_all('td', class_='InmateInfoGridTd')

    age = inmates.find()('td', class_='InmateInfoGridTd')

    webhook = DiscordWebhook(url=settings['discordWebhook'])
    embed = DiscordEmbed()
    embed = DiscordEmbed()
    embed.set_description(f"**Name:** {name[0]}\n\n**Status**{first_inmate[0]}\n\n**Age**{age[0]}")
    embed.set_color(0xFFFFFF)    

    webhook.add_embed(embed)
    response = webhook.execute()