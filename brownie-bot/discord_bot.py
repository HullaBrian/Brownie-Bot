import discord
import selenium.common.exceptions
from dotenv import load_dotenv
from loguru import logger

import os
import time
from threading import Thread
import asyncio
import json

from brownie_retriever import get_brownie_code
from brownie_retriever import init_browser
from brownie_request import brownie_request

load_dotenv()  # load all the variables from the env file
bot = discord.Bot()

context_channel = None
requests = []
run_thread = True
config = json.load(open("config.json"))


async def scan_for_codes():
    logger.info("[CODE SCANNER]: Started code scanner!")
    global requests

    while context_channel is None:
        time.sleep(1.0)
    logger.info("[CODE SCANNER]: Code scanner is ready to go!")

    while run_thread:
        for request in requests:
            logger.info("[CODE SCANNER]: Registered new request. Handling it...")
            try:
                await get_brownie_code(request)
                logger.success("[CODE SCANNER]: Got a new brownie!")
            except TypeError:
                logger.error("[CODE SCANNER]: Type error occured!")
                pass
            except (selenium.common.exceptions.NoSuchElementException, selenium.common.exceptions.ElementNotInteractableException):
                asyncio.run_coroutine_threadsafe(context_channel.send("There was an error processing your request!"), bot.loop)
                logger.error("[CODE SCANNER]: An error occurred while retrieving the brownie!")
            asyncio.run_coroutine_threadsafe(context_channel.send(file=discord.File(open(f"{request.code}", "rb"), filename=f"{request.code}")), bot.loop)
            logger.success("[CODE SCANNER]: Sent the screenshot in the discord channel!")

            time.sleep(5.0)
            try:
                os.remove(f"{request.code}")
                logger.success("[CODE SCANNER]: Cleaned up screenshot from history!")
            except PermissionError:
                logger.warning(f"[CODE SCANNER]: Could not delete '{request.code}'")
            requests.remove(request)
            logger.info("[CODE SCANNER]: Finished handling request!")


@bot.event
async def on_ready():
    logger.info(f"{bot.user} is ready and online!")
    global context_channel
    context_channel = bot.get_channel(config["context channel"])


@bot.slash_command(name="get_brownie", description="Fill out online servey for free brownies!")
async def get_brownie(ctx, store_number: discord.Option(str), date: discord.Option(str), time: discord.Option(str),
                      order_id: discord.Option(str), receipt_location: discord.Option(str)):
    global requests

    if not run_thread:
        await ctx.respond("The brownie factory is closed!")
    requests.append(brownie_request(
        store_number=store_number,
        date=date,
        time=time,
        order_id=order_id,
        receipt_location=receipt_location,
        code=""
    ))
    await ctx.respond(f"Processing your request. Please wait...")


@bot.slash_command(name="abuse_failsafe", description="Stop abusing stuff smh")
async def abuse_failsafe(ctx):
    global run_thread

    if ctx.author.id != config["admin user-id"]:
        await ctx.respond("You keep that up and you'll get banned...")
        return
    run_thread = False
    await ctx.respond("Putting a stop to the brownie thieves...")


@bot.slash_command(name="re-enable_factory", description="Re-enables the brownie functionality.")
async def enable(ctx):
    global run_thread

    if ctx.author.id != config["admin user-id"]:
        await ctx.respond("Bruh...")
        return
    run_thread = True
    await ctx.respond("Enabled da brownie factory!")


@bot.slash_command(name="help", description="This is the help command...bruh")
async def help(ctx):
    await ctx.respond(
        "Use /get_brownie <store number> <date (MM/DD/YY)> <time (HH:MM AM/PM)> <order id> <receipt location>\nWhen using receipt location: enter one of the following: Drive thru, Delivery, Dine in, Curbside Pickup, In-store pickup")


def middle_man():
    asyncio.run(scan_for_codes())


code_thread = Thread(target=middle_man, args=(), daemon=True)
code_thread.start()
init_browser()
bot.run(os.getenv("TOKEN"))
