#Standard imports
import os, discord, random, sys, asyncio
from discord.ext import commands
from datetime import datetime, timedelta
import tenma_storage
bot = commands.Bot(command_prefix=tenma_storage.PREFIX)

#Command modules
import tenma_utils
import moderation


#########################################
######### CHECKS ########################
#########################################

#Check if author is an admin
def _is_admin(ctx):
    return ctx.author.id == os.environ.get('ADMIN_ID')

#########################################
######### EVENTS ########################
#########################################

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

    await tenma_utils.set_status()

@bot.event
async def on_message(message):
    if moderation.is_muted(message.author.id):
        await tenma_utils.delete_message(message)

@bot.event
@bot.listen()
async def on_reaction_add(reaction,user):
    #Ignore bot's reaction add
    if user == bot.user:
        return

    msg = reaction.message
    embeds_reacted = msg.embeds
    emote = reaction.emoji


#########################################
######### COMMANDS ######################
#########################################

@bot.command(name='ping')
async def _ping(ctx):
    await tenma_utils.send_msg("Pong", ctx.channel)

#### ADMIN ONLY ####

@bot.command(name='exit')
@commands.check(_is_admin)
async def _exit(ctx):
    print("Exiting TenmaBot...")
    await bot.logout()


bot.run(os.environ.get('TOKEN'))
