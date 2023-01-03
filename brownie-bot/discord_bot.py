import discord
import selenium.common.exceptions
from dotenv import load_dotenv

import os
import time
from uuid import uuid4
from threading import Thread
import asyncio

from brownie_retriever import get_brownie_code
from brownie_request import brownie_request

load_dotenv()  # load all the variables from the env file
bot = discord.Bot()

context_channel = None
requests = []


async def scan_for_codes():
    print("Scanning for codes...")
    global requests

    while context_channel is None:
        time.sleep(1.0)

    while True:
        for request in requests:
            try:
                await get_brownie_code(request)
            except TypeError:
                pass
            except (selenium.common.exceptions.NoSuchElementException, selenium.common.exceptions.ElementNotInteractableException):
                asyncio.run_coroutine_threadsafe(context_channel.send("There was an error processing your request!"), bot.loop)
            asyncio.run_coroutine_threadsafe(context_channel.send("Code: " + request.code), bot.loop)
            requests.remove(request)


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    global context_channel
    context_channel = bot.get_channel(1059632951022854204)


@bot.slash_command(name="get_brownie", description="Fill out online servey for free brownies!")
async def get_brownie(ctx, store_number: discord.Option(str), date: discord.Option(str), time: discord.Option(str),
                      order_id: discord.Option(str), receipt_location: discord.Option(str)):
    global requests

    requests.append(brownie_request(
        store_number=store_number,
        date=date,
        time=time,
        order_id=order_id,
        receipt_location=receipt_location,
        uuid=str(uuid4()),
        code=""
    ))
    await ctx.respond(f"Processing your request. Your uuid token is: {requests[-1].uuid}")


@bot.slash_command(name="help", description="This is the help command...bruh")
async def help(ctx):
    await ctx.respond(
        "Use /get_brownie <store number> <date (MM/DD/YY)> <time (HH:MM AM/PM)> <order id> <receipt location>\nWhen using receipt location: enter one of the following: Drive thru, Delivery, Dine in, Curbside Pickup, In-store pickup")


def middle_man():
    asyncio.run(scan_for_codes())


code_thread = Thread(target=middle_man, args=(), daemon=True)
code_thread.start()
bot.run(os.getenv("TOKEN"))
