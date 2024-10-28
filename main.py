# AuctionBot, a bot for fake auctions and as a test for developing discord applications.

# imports the discord.py library
import discord
from discord import app_commands

# for storing api key
import json

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

currentBid = 0
curPokemon = ''
bidUser = ''

guildId = 809484674518351982

with open('key.json', 'r') as file:
    key = json.load(file)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await tree.sync(guild=discord.Object(id=guildId))
    print("tree synced!")

@tree.command(
    name = "start-auction",
    description = "embed with button test",
    guild = discord.Object(id=guildId)
)

async def start_auction(interaction, bid: int, pokemon: str):
    global currentBid
    global curPokemon

    embed = discord.Embed(title='Auction', description='A new auction has started!', color=0xffffff)
    embed.add_field(name="Pokemon", value=f'{pokemon}', inline=True)
    embed.add_field(name="Current Bid", value=f'The auction has started with a bid of ${bid}', inline=False)

    currentBid = bid
    curPokemon = pokemon

    await interaction.response.send_message(embed=embed)

@tree.command(
    name = "bid",
    description = "allows you to bid your money",
    guild = discord.Object(id=guildId)
)

async def bid(interaction, money: int):
    global currentBid
    global bidUser

    if money > currentBid:
        currentBid = money
        bidUser = interaction.user.name
        await interaction.response.send_message(f'The current bid has been raised to {currentBid} by {bidUser}')
    else:
        await interaction.response.send_message('The bid you entered is not higher than the current one, brokeass')

@tree.command(
    name = "end-auction",
    description = "Ends the current auction at hand.",
    guild = discord.Object(id=guildId)
)

async def end_auction(interaction):
    global currentBid
    global curPokemon
    global bidUser

    await interaction.response.send_message(f'The auction ends with **{curPokemon}** being sold to **{bidUser}** for **{currentBid}**.')
    currentBid = 0

client.run(key["api_key"]) # note, you will have to make your own keys.json with a variable named "api_key" for this to work.