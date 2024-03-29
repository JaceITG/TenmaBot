import discord, asyncio, random
import tenma_config

local_client = discord.Client( )

# TODO: Finish documentation
async def handle_cline( command ):
    _arguments = command.split(' ')

    if _arguments[ 0 ] == "exit":
        print( "Exiting..." )
        await local_client.logout( )

    if _arguments[ 0 ] == "announce":
        if len( _arguments ) < 2:
            print( "Must pass message to announce" )
        else:
            try:
                _channel = local_client.get_channel( int( _arguments[ 1 ] ) )
                _message = ' '.join( _arguments[ 2: ] )
            except:
                _channel = local_client.get_channel( tenma_config.tenma_main )
                _message = ' '.join( _arguments[ 1: ] )
            await send_message( _message, _channel )

# ------------------------
# tenma_utils.send_message
# Purpose: Sends a message
# in a given channel
# ------------------------
async def send_message( message, channel ):
    try:
        m_sMessage = await channel.send( message )
        print(f"-Message sent to {channel.name}: \n\t-\"{message}\"")
        return m_sMessage
    except Exception as e:
        print(f"Error while attempting to send message to {channel.name}: \n{e}")
        
# -----------------------
# tenma_utils.embed_image
# Purpose: Sends an embed
# in a given channel
# -----------------------
async def send_embed( embed, channel, content=None ):
    try:
        m_fEmbed = await channel.send( content=content, embed=embed )
        print(f"-Embed sent to {channel.name}: {embed.title}")
        return m_fEmbed
    except Exception as e:
        print(f"Error while attempting to send embed to {channel.name}: \n{e}")

# -----------------------
# tenma_utils.send_file
# Purpose: Attaching a
# file to a message
# -----------------------
async def send_file( file_path, channel, content=None ):
    get_file = discord.File( file_path )
    try:
        await channel.send( content=content, file=get_file )
        print(f"-File attached in {channel.name}: {file_path}")
    except:
         print(f"Error while attempting to send {file_path} to {channel.name}")

#TODO: documentation
async def get_last_image(channel):
    async for message in channel.history(limit=100):
        if len(message.attachments) >= 1:
            return message.attachments[0].url
    return None

#TODO: documentation
async def delete_message(message):
    try:
        channel = message.channel.name
        await message.delete()
        print(f"Message deleted from {channel}")
    except:
        print(f"Error: could not delete message in {channel}")

#TODO: documentation
async def get_embed(url):
    embed = discord.Embed()
    embed.set_image(url=url)
    return embed

#TODO: documentation
async def set_status(bot, new=None):
    if new:
        activity_name = new
    else:
        activity_name = random.choice(tenma_config.activities)
    await bot.change_presence(activity=discord.Game(name=activity_name))

async def parse_bill(fp):
    cnt = ""
    with open(fp, 'r', encoding="utf-8") as f:
        cnt = f.read()
    
    return cnt.split('$%$%$%$%$%').strip()

# -----------------------
# tenma_utils.embed_quote
# Purpose: Create a visualization
# of a message sent in another channel
# -----------------------
async def embed_quote(message):
    return discord.Embed()

# NOTE: I'll clean the rest of this up later and finish documentation
# - software engineer
