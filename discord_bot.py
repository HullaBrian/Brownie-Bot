import discord
import os
from dotenv import load_dotenv

load_dotenv()  # load all the variables from the env file
bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name="get_brownie", description="Fill out online servey for free brownies!")
async def get_brownie(ctx, order_id: discord.Option(int), teller_number: discord.Option(int)):
    await ctx.respond("Processing...")


bot.run(os.getenv('TOKEN'))  # run the bot with the token
