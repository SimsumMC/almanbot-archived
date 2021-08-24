import discord 
from discord import commands

class broadcast(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
  @commands.command(name="broadcast", aliases=["ankündigung", "ownermsg"])
  async def broadcast(self, ctx, *, message):
    user = ctx.author
    name = ctx.channel.name
    msg2 = ctx.message
    if botchannel_check(ctx):
      ...
    else:
      embed = discord.Embed(
                    title="**Fehler**", colour=get_embedcolour(ctx.message)
                )
      embed.set_footer(
                    text=FOOTER[0]
                    + str(user)
                    + FOOTER[1]
                    + str(get_author())
                    + FOOTER[2]
                    + str(get_prefix_string(ctx.message)),
                    icon_url=ICON_URL,
                )
      embed.add_field(
                    name="‎",
                    value="Es existiert noch kein Log deines Servers, da dass hier anscheinend dein erster "
                    "Befehl ist!",
                    inline=False,
                )
                await ctx.send(embed=embed)
                log(
                    input=str(time)
                    + ": Der Spieler "
                    + str(user)
                    + ' hat sich probiert den noch nicht existierenden Log mit der ID "'
                    + str(ctx.guild.id)
                    + '" ausgeben zu lassen!',
                    id=ctx.guild.id,
                )



###############################################################################################################

def setup(bot):
  bot.add_cog(broadcast(bot))
