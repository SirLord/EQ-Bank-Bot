#python 3.6
# @abadrian @crisper andrewacropora@gmail.com
# bot to answer questions about a guild bank
# TODO: Add request, deposit, withdraw


token = ''

# Code to set up the bot, join channel, etc

import discord
from discord.ext.commands import Bot
from fuzzywuzzy import fuzz
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import asyncio

# Make a connection to a google sheet
id = ''
secret = ''


SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet. NOTE- DELETE PICKLE FILE IF CHANGING ANYTHING HERE
SPREADSHEET_ID = ''
SAMPLE_RANGE_NAME = 'Inventory!A:B'

def get_data():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        #print('Name, Amount') header already exists
        return values
        #for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            
            #print('%s, %s' % (row[0], row[1]))

def search_bank(query):
    data = get_data()
    results = []

    for row in data:
        if len(results) < 5:
            if fuzz.partial_ratio(row[0],query) > 70:
                results.append(row)
        else:
            return results
    return results

bot_channel = discord.Object("4")
#bot_channel = discord.Object("548905365")

BOT_PREFIX = ("?", "!")
client = Bot(command_prefix=BOT_PREFIX)


@client.event
async def on_message(message):  # event that happens per any message.
    # each message has a bunch of attributes. Here are a few.
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    if message.author == client.user:
        return
    if message.content.lower().startswith("!bank"):
        query = str(message.content.lower())[6::]
        matches = search_bank(query)
        if len(matches) == 0:
            await client.send_message(message.channel, "No matches for "+ query)
        else:
            await client.send_message(message.channel, "Matches for \""+ query+ "\" \n [ Name ,   Qty ]  \n")
            for line in matches:
                await client.send_message(message.channel, line )
    if message.content.lower().startswith("!help"):
         await client.send_message(message.channel, 'Use "!bank <item>" to query the guild bank')
    await asyncio.sleep(1)

@client.event  # event decorator/wrapper. More on decorators here: https://pythonprogramming.net/decorators-intermediate-python-tutorial/
async def on_ready():  # method expected by client. This runs once when connected
    print(f'We have logged in as {client.user}')  # notification of login.
    await client.send_message(bot_channel, 'Status: Online. \n Use "!bank <item>"" to query the guild bank')


# Retrieve the contents of the google sheet, parse it

# Answer Questions about bank contents
 
client.run(token) 