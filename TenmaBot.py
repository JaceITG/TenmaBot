#Standard imports
from ast import alias
import os, discord, random, sys, asyncio
from discord.ext import commands
from datetime import datetime, timedelta
import tenma_config
bot = commands.Bot(command_prefix=tenma_config.prefix)

bills = []

#Command modules
import tenma_utils


#########################################
######### CHECKS ########################
#########################################

#Check if author is an admin
def _is_admin(ctx):
    return ctx.author.id == int(os.environ.get('ADMIN_ID'))

#########################################
######### EVENTS ########################
#########################################

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

    await tenma_utils.set_status(bot)

    global bills
    bills = await tenma_utils.parse_bill(tenma_config.bill_fp)

# @bot.event
# async def on_message(message):
#     pass

@bot.event
@bot.listen()
async def on_reaction_add(reaction,user):

    #Ignore bot's reaction add
    if user == bot.user:
        return

    msg = reaction.message
    embeds_reacted = msg.embeds
    emote = reaction.emoji

    #Quote message 
    if emote == '💬' and msg.guild.id == tenma_config.riji_server:
        _quote_channel = msg.guild.get_channel(tenma_config.riji_quote_chan)
        _embed = await tenma_utils.embed_quote(msg)
        await tenma_utils.send_embed(_embed, msg.channel)



#########################################
######### COMMANDS ######################
#########################################

@bot.command(name='ping')
async def _ping(ctx):
    await tenma_utils.send_message("Pong", ctx.channel)

@bot.command(name='billquote', aliases=['bq','bill'])
async def _bill_quote(ctx):
    await tenma_utils.send_message(random.choice(bills), ctx.channel)

#### ADMIN ONLY ####

@bot.command(name='exit')
@commands.check(_is_admin)
async def _exit(ctx):
    print("Exiting TenmaBot...")
    await bot.logout()


def main():
    bot.run(os.environ.get('TOKEN'))

if __name__ == "__main__":
    main()