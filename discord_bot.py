import discord
import os
from dotenv import load_dotenv

from brownie_retriever import get_brownie


load_dotenv()  # load all the variables from the env file
bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name="get_brownie", description="Fill out online servey for free brownies!")
async def get_brownie(ctx, store_number: discord.Option(str), date: discord.Option(str), time: discord.Option(str), order_id: discord.Option(str), receipt_location: discord.Option(str)):
    await ctx.respond("Code:" + str(get_brownie(store_number=store_number, date=date, time=time, order_id=order_id, receipt_location=receipt_location)))


@bot.slash_command(name="help", description="This is the help command...bruh")
async def help(ctx):
    await ctx.respond("Use /get_brownie <store number> <date (MM/DD/YY)> <time (HH:MM AM/PM)> <order id> <receipt location>\nWhen using receipt location: enter one of the following: Drive thru, Delivery, Dine in, Curbside Pickup, In-store pickup")

bot.run(os.getenv('TOKEN'))  # run the bot with the token
