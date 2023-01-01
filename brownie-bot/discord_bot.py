import asyncio

import discord
from discord.ext import tasks
import os
from uuid import uuid4
from dotenv import load_dotenv
from threading import Thread

from brownie_retriever import get_brownie


load_dotenv()  # load all the variables from the env file
bot = discord.Bot()

with open("codes.txt", "w") as file:  # Clear out codes
    file.write("")

store_num: str = ""
d: str = ""
t: str = ""
orderid: str = ""
receipt_loc = ""
codes = []


async def scan_for_codes():
    global codes
    print("Scanning for codes...")
    with open("codes.txt", "r") as codes:
        while True:
            for line in codes.readlines():
                codes.append(line)
                channel = bot.get_channel(1058441771438329987)  # channel ID goes here
                await channel.send("Code: " + line)


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name="get_brownie", description="Fill out online servey for free brownies!")
async def get_brownie(ctx, store_number: discord.Option(str), date: discord.Option(str), time: discord.Option(str), order_id: discord.Option(str), receipt_location: discord.Option(str)):
    request_id = str(uuid4())
    await ctx.respond(f"Processing your request. Your uuid token is: {request_id}")


@bot.slash_command(name="help", description="This is the help command...bruh")
async def help(ctx):
    await ctx.respond("Use /get_brownie <store number> <date (MM/DD/YY)> <time (HH:MM AM/PM)> <order id> <receipt location>\nWhen using receipt location: enter one of the following: Drive thru, Delivery, Dine in, Curbside Pickup, In-store pickup")


def run():
    bot.run(os.getenv("TOKEN"))


loop = asyncio.get_event_loop()
loop.call_later(3, run)
task = loop.create_task(scan_for_codes())

try:
    loop.run_until_complete(task)
except asyncio.CancelledError:
    pass
