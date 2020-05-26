#Standard imports
import os, discord, random, sys, asyncio
from discord.ext import commands
from datetime import datetime, timedelta
import tenma_storage
bot = commands.Bot(command_prefix=tenma_storage.PREFIX)

#Command modules
import tenma_config, tenma_utils
import moderation


#########################################
######### CHECKS ########################
#########################################

#Check if author is an admin
def _is_admin(ctx):
    return ctx.author.id in tenma_storage.ADMIN_ID

#########################################
######### EVENTS ########################
#########################################

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

    await tenma_utils.set_status()

    #Get time until hour for rohil ping
    now = datetime.now()
    hr = tenma_storage.ROHIL_PING_TIME[0]
    min = tenma_storage.ROHIL_PING_TIME[1]
    secs_left = int((timedelta(hours=24) - (now - now.replace(hour=hr, minute=min, second=0, microsecond=0))).total_seconds() % (24 * 3600))

    await tenma_utils.ping_rohil(secs_left)

@bot.event
async def on_message(message):
    if moderation.is_muted(message.author.id):
        await tenma_utils.delete_message(message)

@bot.event
@bot.listen()
async def on_reaction_add(reaction,user):
    #Ignore bot's reaction add
    if user == client.user:
        return

    msg = reaction.message
    embeds_reacted = msg.embeds
    emote = reaction.emoji


#########################################
######### COMMANDS ######################
#########################################

@bot.command(name='ping')
async def _ping(ctx):
    await _send_msg("Pong", ctx.channel)

#### ADMIN ONLY ####

@bot.command(name='exit')
@commands.check(_is_admin)
async def _exit(ctx):
    print("Exiting TenmaBot...")
    await bot.logout()


bot.run(tenma_storage.TOKEN)
