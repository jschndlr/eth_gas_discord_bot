#! python3
# gaspricebot.py
import os
import discord
from PIL import Image
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

#Load environment variables
load_dotenv()
url = os.getenv('TARGET_URL')
path = os.getenv('TARGET_FILE')
TOKEN = os.getenv('DISCORD_TOKEN')

#Open driver and get gas page
driver = webdriver.Chrome()
driver.get(url)

#Grab image through chromedriver using selenium
async def getgas():
    driver.refresh()
    el = driver.find_element(By.ID, "body")
    el.screenshot(path)
    crop_image()

#Crop image and re-save
def crop_image():
    crop = Image.open(path).crop((0,168,919,709))
    crop.save('scrape.png')

#Discord bot and events
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.content.startswith('!gas'):
        await getgas()
        await message.channel.send(file=discord.File(path))

try:
    client.run(TOKEN)
except:
    print('client connect exception, check internet connection')
