import discord
from pybooru import Danbooru
from tenma_storage import DAN_API_KEY, DAN_API_USER, HELP_EMBED, SEAL_DAN_API_USER, SEAL_DAN_API_KEY, SCH_DAN_API_USER, SCH_DAN_API_KEY, DAN_FAV_ID
import tenma_storage, tenma_config
badExts = ['mpg','mp4','wav','wmv','mkv','swf']

HELP_EMBED.add_field(name='`db [tags]*`',value="Fetch an image with the given tags from Danbooru\nOptions: `-s` - Begin a post stream of the given tags. Pass an integer as the first tag to set delay time between posts (defaults to 7 seconds)")

client = Danbooru(site_url='https://danbooru.donmai.us', username=DAN_API_USER, api_key=DAN_API_KEY)
clientSeals = Danbooru(site_url='https://danbooru.donmai.us', username=SEAL_DAN_API_USER, api_key=SEAL_DAN_API_KEY)
clientScheisse = Danbooru(site_url='https://danbooru.donmai.us', username=SCH_DAN_API_USER, api_key=SCH_DAN_API_KEY)
alreadySent = []

async def main(ctx):
    author = ctx.author
    text = ctx.content
    args = text[1:].split(' ')
    channel = ctx.channel
    guild = ctx.guild
    global looping_stream

    #Handle call to the db command
    if "-s" in args:
        #Set up post stream
        args.remove("-s")
        #If already streaming, end that one before starting new
        if looping_stream:
            looping_stream = False
            await asyncio.sleep(1)
        looping_stream = True
        #Check if delay time is defined
        if len(args)>1 and args[1].replace(".","").isdigit():
            delay = float(args[1])
            del args[1]
        else:
            delay = tenma_config.db_stream_delay
        streamEmb = discord.Embed(description=f"Starting post stream. Use `$stop` to end the stream.")
        await _send_embed(streamEmb,channel)
        await post_stream(args[1:], channel, delay)
    else:
        #Handle normally
        dbEmbed = await get_dan_img(args[1:])
        sentEmbed = await _send_embed(dbEmbed,channel)
        #Add reaction only to post images
        if dbEmbed.description.startswith("[Source]"):
            await sentEmbed.add_reaction("❤️")
            await sentEmbed.add_reaction("❌")

async def get_dan_img(tags):
    postList = client.post_list(tags=' '.join(tags),random=True)
    if len(postList)<1:
        return discord.Embed(description=f"Could not find posts tagged: {tags}")
    index = 0

    postUrl = postList[index]['large_file_url']
    ext = postList[index]['file_ext']
    while postUrl in alreadySent or ext in badExts:
        index += 1
        if index >= len(postList):
            return discord.Embed(description=f"No more posts with these tags could be found")
        postUrl = postList[index]['large_file_url']
        ext = postList[index]['file_ext']

    source = postList[index]['id']
    embed = discord.Embed(description=f"[Source](https://danbooru.donmai.us/posts/{source})")
    embed.set_image(url=postUrl)
    alreadySent.append(postUrl)
    return embed

async def favorite_id(favUrl, user):
    indexId = int(favUrl.find("posts/")) + 6
    postid = int(favUrl[indexId:-1])

    if user.id == tenma_storage.DAN_FAV_ID[0]:
        client.favorite_add(postid)
    elif user.id == tenma_storage.DAN_FAV_ID[1]:
        clientSeals.favorite_add(postid)
    elif user.id == tenma_storage.DAN_FAV_ID[2]:
        clientScheisse.favorite_add(postid)

#Loop for sending a continuous stream of images for given tags
async def post_stream(tags, channel, delay):
    global looping_stream
    while looping_stream:
        dbEmbed = await getDanImg(tags)
        sentEmbed = await sendEmbed(dbEmbed,channel)
        #Add reaction only to post images
        if dbEmbed.description.startswith("[Source]"):
            await sentEmbed.add_reaction("❤️")
            await sentEmbed.add_reaction("❌")
        else:
            looping_stream = False
        await asyncio.sleep(delay)

### Reaction add listener to check for image liked or deleted
@bot.listen('on_reaction_add')
async def reaction_handler(reaction, user):
    if user == client.user:
        return

    msg = reaction.message
    embeds_reacted = msg.embeds
    emote = reaction.emoji

    #Handle favorite db img
    if len(embeds_reacted)>0 and embeds_reacted[0].description.startswith("[Source](https://danbooru"):
        if user.id in DAN_FAV_ID and emote == "❤️":
            #Favorite image
            await favorite_id(embeds_reacted[0].description, user)
        elif emote == "❌":
            #Delete image
            await _delete_msg(msg)
