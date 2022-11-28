import requests
from bs4 import BeautifulSoup
import sqlite3
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
import time

url = "https://www.lcso.org/inmates/"

with open("settings.json", "r") as f:
    settings = json.load(f)

if settings["discordWebhook"] == "":
    print("Please add a webhook to settings.json")
    exit()

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

#Create database for last inmate

conn = sqlite3.connect('inmate.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS inmate (name text)")
conn.commit()
conn.close()


def main():
    response = requests.get(url, headers= headers)

    soup = BeautifulSoup(response.text, "html.parser")

    imatesDiv = soup.find("div", class_= "GridDIV")

    table_of_imates = imatesDiv.find("div", class_= "JailInfo")

    first_inmate = table_of_imates.find("tr", class_= "InmateRecordRow")

    image = first_inmate.find("td", class_= "text-center col-xs-1").find("img")["src"]
    

    #Filter data from HTML:
    firstSection = first_inmate.find("td", class_ ="col-xs-11 col-sm-5 text-left")

    firstSectionMoreSpecified = firstSection.find("h4", {"style": "display: inline;"})


    name = firstSection.find_all("span")[1].text

    ageRaceGender = firstSectionMoreSpecified.find("span").next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()

    arrestingAgency = firstSectionMoreSpecified.find("span").next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()

    arrestedOn = firstSectionMoreSpecified.find("span").next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()

    img_url = f"https://www.lcso.org/inmates/{image}"

    
    secondSection = first_inmate.find("td", class_= "hidden-xs col-sm-5 text-left")

    dateOfBirth = secondSection.find_all("span")[1].text


    #Get last inmate from database

    conn = sqlite3.connect('inmate.db')
    c = conn.cursor()
    c.execute("SELECT * FROM inmate")
    last_inmate = c.fetchone()
    conn.close()


    #Check if theres a last inmate, if not, create one and send to discord
    if last_inmate == None:
        conn = sqlite3.connect('inmate.db')
        c = conn.cursor()
        c.execute("INSERT INTO inmate VALUES (?)", (name,))
        conn.commit()
        conn.close()


        webhook = DiscordWebhook(url=settings['discordWebhook'])
        embed = DiscordEmbed()
        embed.set_description(f"**Name:** {name}\n\n**Date Of Birth:** {dateOfBirth}\n\n**Age/Race/Gender:** {ageRaceGender}\n\n**Arresting Agency:** {arrestingAgency}\n\n**Arrested On:** {arrestedOn}")
        embed.set_image(url=img_url)
        embed.set_color(0xFFFFFF)
        
        webhook.add_embed(embed)
        response = webhook.execute()
        print('New inmate detected! Posting to discord')
        return


    #If last inmate is not the same as the current inmate, update the database and post to discord
    elif last_inmate[0] != name:

        conn = sqlite3.connect('inmate.db')
        c = conn.cursor()
        c.execute("UPDATE inmate SET name = (?)", (name,))
        conn.commit()
        conn.close()

        webhook = DiscordWebhook(url=settings['discordWebhook'])
        embed = DiscordEmbed()
        embed.set_title("**New Inmate Detected 🎉**")
        embed.set_description(f"**Name:** {name}\n\n**Date Of Birth:** {dateOfBirth}\n\n**Age/Race/Gender:** {ageRaceGender}\n\n**Arresting Agency:** {arrestingAgency}\n\n**Arrested On:** {arrestedOn}")
        embed.set_image(url=img_url)
        embed.set_color(0xFFFFFF)
        embed.set_footer
        webhook.add_embed(embed)
        response = webhook.execute()

        print('New inmate detected! Posting to discord')
        return
    
    else:
        print("Latest inmate is the same, sleeping for 1 minute...")
        return	



if __name__ == "__main__":
    print('\nStarting Inmates Monitor...')
    print()
    while True:
        main()
        time.sleep(60)

