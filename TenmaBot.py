#Standard imports
import os, discord, random, sys, asyncio
from discord.ext import commands
from datetime import datetime, timedelta
#Command modules
import tenma_storage
from danbooru_new import get_dan_img,favorite_id

bot = commands.Bot(command_prefix=tenma_storage.PREFIX)

#########################################
######### UTIL FUNCTIONS ################
#########################################

#Sends text message to a channel
async def _send_msg(text, channel):
    try:
        msg = await channel.send(text)
        print(f"-Message sent to {channel.name}: \n\t-\"{text}\"")
        return msg
    except:
        print(f"Error while attempting to send message to {channel.name}")

#Sends embed message to a channel
async def _send_embed(embed, channel, content=None):
    try:
        embed = await channel.send(content=content,embed=embed)
        print(f"-Embed sent to {channel.name}: {embed.title}")
        return embed
    except:
        print(f"Error while attempting to send embed to {channel.name}")

#Sends file from given absolute path
async def _send_file(fp, channel, cntnt=None):
    img_file = discord.File(fp)
    try:
        await channel.send(content=cntnt,file=img_file)
        print(f"-Image sent to {channel.name}: {fp}")
    except:
        print(f"Error while attempting to send {fp} to {channel.name}")

#Return url string of most recently posted image
async def _last_image(channel):
    async for message in channel.history(limit=100):
        if len(message.attachments) >= 1:
            return message.attachments[0].url
    return None

#Delete passed message
async def _delete_msg(message):
    try:
        channel = message.channel.name
        await message.delete()
        print(f"Message deleted from {channel}")
    except:
        print(f"Error: could not delete message in {channel}")

#Return an embedded image
async def _embed_image(url):
    embed = discord.Embed()
    embed.set_image(url=url)
    return embed

#Loop to ping rohil on 24 hour interval
async def _ping_rohil(secs):
    await asyncio.sleep(secs)
    while True:
        rohil_mention = client.get_user(463608962059862018).mention
        rohil_ping_chan = client.get_channel(483289509941870595)
        await sendMsg(f"{rohil_mention} bitch", rohil_ping_chan)
        await asyncio.sleep(86400)

async def _set_status(new = None):
    if new:
        activity_name = new
    else:
        activities = ["mobile games", "HOW", "POGGER", "$db toddlercon", "with little girls", "pee.com","keta is a pedophile", "rijihuudu.ahlamontada.com"]
        activity_name = random.choice(activities)
    await bot.change_presence(activity=discord.Game(name=activity_name))

#Check if author is an admin
def _is_admin(ctx):
    return ctx.author in tenma_storage.ADMIN_ID


#########################################
######### EVENTS ########################
#########################################

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await _set_status()

    #Get time until hour for rohil ping
    now = datetime.now()
    hr = tenma_storage.ROHIL_PING_TIME[0]
    min = tenma_storage.ROHIL_PING_TIME[1]
    secs_left = int((timedelta(hours=24) - (now - now.replace(hour=hr, minute=min, second=0, microsecond=0))).total_seconds() % (24 * 3600))

    await _ping_rohil(secs_left)

@bot.event
async def on_reaction_add(reaction,user):
    #Ignore bot's reaction add
    if user == client.user:
        return

    msg = reaction.message
    embeds_reacted = msg.embeds
    emote = reaction.emoji

    #Handle favorite db img
    if len(embeds_reacted)>0 and embeds_reacted[0].description.startswith("[Source](https://danbooru"):
        if user.id in tenma_storage.DAN_FAV_ID and emote == "❤️":
            #Favorite image FIXMEEEE
            await favorite_id(embedsReacted[0].description, user)
        elif emote == "❌":
            await _delete_msg(msg)
            
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
