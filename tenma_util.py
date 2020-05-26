from TenmaBot import *

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
        rohil_mention = bot.get_user(463608962059862018).mention
        rohil_ping_chan = bot.get_channel(483289509941870595)
        await sendMsg(f"{rohil_mention} bitch", rohil_ping_chan)
        await asyncio.sleep(86400)

async def _set_status(new = None):
    if new:
        activity_name = new
    else:
        activity_name = random.choice(tenma_config.activities)
    await bot.change_presence(activity=discord.Game(name=activity_name))
