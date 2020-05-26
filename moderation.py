from TenmaBot import bot
import tenma_config
from discord.ext import commands
global prev_muted

@bot.command(name="mute", aliases=["silence"])
@commands.has_permissions(kick_members=True)
async def _mute(ctx):
    #Warn if no users indicated to be muted
    if not ctx.message.mentions:
        await ctx.send("Must mention a member to mute")

    #Open file of muted users
    with open(tenma_config.muted_users_fp, "w") as f:
        #Get set of already muted users
        prev_muted = set(f.readlines())

        #Loop through each user mentioned in command
        for user in ctx.message.mentions:
            #Append id of muted user to set
            prev_muted.append(str(user.id))

        #Overwrite muted user cache with updated set
        for id in prev_muted:
            f.write(f"{id}\n")

def is_muted(id):
    return str(id) in prev_muted
