import os

import discord
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument

from cogs.core.functions.functions import get_author, get_prefix_string, get_botc, get_colour
from main import client


class cog(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.group()
	@commands.is_owner()
	async def cog(self, ctx):
		user = ctx.author.name
		name = ctx.channel.name
		msg2 = ctx.message
		mention = ctx.author.mention
		botchannel = get_botc(message=ctx.message)
		if ctx.invoked_subcommand is None:
			if name == botchannel or botchannel == 'None':
				embed = discord.Embed(title='Fehler', colour=get_colour(ctx.message))
				embed.set_thumbnail(
					url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png'
						'?width=676&height=676')
				embed.add_field(name='‎', value='Bitte gib eines der unten angegebenen Argumente ein:\n'
											'`load <Name vom Cog>`\n`unload <Name vom Cog>`\n`reload <Name vom Cog>`\n'
											'`reloadall`\n', inline=False)
				embed.set_footer(
					text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
						message=ctx.message), icon_url='https://media.discordapp.net/attachments/645276319311200286'
													   '/803322491480178739/winging-easy.png?width=676&height=676')
				await ctx.send(embed=embed)
			else:
				await ctx.send(f'{mention}, dieser Befehl kann nur im Kanal #{botchannel} genutzt werden.',
							   delete_after=3)
				await msg2.delete()

	@cog.command()
	@commands.is_owner()
	async def load(self, ctx, cogname: str):
		user = ctx.author.name
		name = ctx.channel.name
		msg2 = ctx.message
		mention = ctx.author.mention
		botchannel = get_botc(message=ctx.message)
		if name == botchannel or botchannel == 'None':
			try:
				for directory in os.listdir('./cogs'):
					if directory != "Ignore":
						for directory2 in os.listdir(f'./cogs/{directory}'):
							for filename in os.listdir(f'./cogs/{directory}/{directory2}/'):
								if filename == f"{cogname}.py":
									extension = f"cogs.{directory}.{directory2}.{filename[:-3]}"
									client.load_extension(extension)
									embed = discord.Embed(title='Cog Load', colour=get_colour(ctx.message))
									embed.set_thumbnail(
										url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png'
											'?width=676&height=676')
									embed.add_field(name='‎',
													value=f'Der Cog ```{cogname}``` konnte erfolgreich geladen werden.'
													, inline=False)
									embed.set_footer(
										text='for ' + str(user) + ' | by ' + str(
											get_author()) + ' | Prefix ' + get_prefix_string(
											message=ctx.message),
										icon_url='https://media.discordapp.net/attachments/645276319311200286'
												 '/803322491480178739/winging-easy.png?width=676&height=676')
									await ctx.send(embed=embed)
									return
				else:
					embed = discord.Embed(title='Fehler', colour=get_colour(ctx.message))
					embed.set_thumbnail(
						url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png'
							'?width=676&height=676')
					embed.add_field(name='‎', value=f'Der Cog ```{cogname}``` konnte nicht geladen werden.'
									, inline=False)
					embed.set_footer(
						text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
							message=ctx.message), icon_url='https://media.discordapp.net/attachments/645276319311200286'
														   '/803322491480178739/winging-easy.png?width=676&height=676')
					await ctx.send(embed=embed)
			except Exception:
				embed = discord.Embed(title='Fehler', colour=get_colour(ctx.message))
				embed.set_thumbnail(
					url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png'
						'?width=676&height=676')
				embed.add_field(name='‎', value=f'Der Cog ```{cogname}``` konnte nicht geladen werden.'
								, inline=False)
				embed.set_footer(
					text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
						message=ctx.message), icon_url='https://media.discordapp.net/attachments/645276319311200286'
													   '/803322491480178739/winging-easy.png?width=676&height=676')
				await ctx.send(embed=embed)
				raise Exception
		else:
			await ctx.send(f'{mention}, dieser Befehl kann nur im Kanal #{botchannel} genutzt werden.',
						   delete_after=3)
			await msg2.delete()

	@load.error
	async def handle_error(self, ctx, error):
		user = ctx.author
		if isinstance(error, MissingRequiredArgument):
			embed = discord.Embed(title='**Fehler**', colour=get_colour(ctx.message))
			embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
				message=ctx.message),
							 icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
									  '/winging-easy.png?width=676&height=676')
			embed.add_field(name='‎',
							value='Du hast nicht alle erforderlichen Argumente angegeben, Nutzung: ```' +
								  get_prefix_string(ctx.message) + '```cog load <Name>```',
							inline=False)
			await ctx.send(embed=embed)

	@cog.command()
	@commands.is_owner()
	async def unload(self, ctx, cogname: str):
		user = ctx.author.name
		name = ctx.channel.name
		msg2 = ctx.message
		mention = ctx.author.mention
		botchannel = get_botc(message=ctx.message)
		if name == botchannel or botchannel == 'None':
			try:
				for directory in os.listdir('./cogs'):
					if directory != "Ignore":
						for directory2 in os.listdir(f'./cogs/{directory}'):
							for filename in os.listdir(f'./cogs/{directory}/{directory2}/'):
								if filename == f"{cogname}.py":
									extension = f"cogs.{directory}.{directory2}.{filename[:-3]}"
									client.unload_extension(extension)
									embed = discord.Embed(title='Cog Unload', colour=get_colour(ctx.message))
									embed.set_thumbnail(
										url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png'
											'?width=676&height=676')
									embed.add_field(name='‎',
													value=f'Der Cog ```{cogname}``` konnte erfolgreich entladen werden.'
													, inline=False)
									embed.set_footer(
										text='for ' + str(user) + ' | by ' + str(
											get_author()) + ' | Prefix ' + get_prefix_string(
											message=ctx.message),
										icon_url='https://media.discordapp.net/attachments/645276319311200286'
												 '/803322491480178739/winging-easy.png?width=676&height=676')
									await ctx.send(embed=embed)
									return
				else:
					embed = discord.Embed(title='Fehler', colour=get_colour(ctx.message))
					embed.set_thumbnail(
						url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png'
							'?width=676&height=676')
					embed.add_field(name='‎', value=f'Der Cog ```{cogname}``` konnte nicht entladen werden.'
									, inline=False)
					embed.set_footer(
						text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
							message=ctx.message), icon_url='https://media.discordapp.net/attachments/645276319311200286'
														   '/803322491480178739/winging-easy.png?width=676&height=676')
					await ctx.send(embed=embed)
			except Exception:
				embed = discord.Embed(title='Fehler', colour=get_colour(ctx.message))
				embed.set_thumbnail(
					url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png'
						'?width=676&height=676')
				embed.add_field(name='‎', value=f'Der Cog ```{cogname}``` konnte nicht entladen werden.'
								, inline=False)
				embed.set_footer(
					text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
						message=ctx.message), icon_url='https://media.discordapp.net/attachments/645276319311200286'
													   '/803322491480178739/winging-easy.png?width=676&height=676')
				await ctx.send(embed=embed)
		else:
			await ctx.send(f'{mention}, dieser Befehl kann nur im Kanal #{botchannel} genutzt werden.',
						   delete_after=3)
			await msg2.delete()

	@unload.error
	async def handle_error(self, ctx, error):
		user = ctx.author
		if isinstance(error, MissingRequiredArgument):
			embed = discord.Embed(title='**Fehler**', colour=get_colour(ctx.message))
			embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
				message=ctx.message),
							 icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
									  '/winging-easy.png?width=676&height=676')
			embed.add_field(name='‎',
							value='Du hast nicht alle erforderlichen Argumente angegeben, Nutzung: ```' +
								  get_prefix_string(ctx.message) + '```cog unload <Name>```',
							inline=False)
			await ctx.send(embed=embed)

	@cog.command()
	@commands.is_owner()
	async def reload(self, ctx, cogname: str):
		x = 0
		user = ctx.author.name
		name = ctx.channel.name
		msg2 = ctx.message
		mention = ctx.author.mention
		botchannel = get_botc(message=ctx.message)
		if name == botchannel or botchannel == 'None':
			try:
				for directory in os.listdir('./cogs'):
					if directory != "Ignore":
						for directory2 in os.listdir(f'./cogs/{directory}'):
							for filename in os.listdir(f'./cogs/{directory}/{directory2}/'):
								if filename == f"{cogname}.py":
									extension = f"cogs.{directory}.{directory2}.{filename[:-3]}"
									client.unload_extension(extension)
									client.load_extension(extension)
									embed = discord.Embed(title='Cog Reload', colour=get_colour(ctx.message))
									embed.set_thumbnail(
										url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png'
											'?width=676&height=676')
									embed.add_field(name='‎',
													value=f'Der Cog ```{cogname}``` konnte erfolgreich neu geladen werden.'
													, inline=False)
									embed.set_footer(
										text='for ' + str(user) + ' | by ' + str(
											get_author()) + ' | Prefix ' + get_prefix_string(
											message=ctx.message),
										icon_url='https://media.discordapp.net/attachments/645276319311200286'
												 '/803322491480178739/winging-easy.png?width=676&height=676')
									await ctx.send(embed=embed)
									return
				else:
					embed = discord.Embed(title='Fehler', colour=get_colour(ctx.message))
					embed.set_thumbnail(
						url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png'
							'?width=676&height=676')
					embed.add_field(name='‎', value=f'Der Cog ```{cogname}``` konnte nicht neu geladen werden.'
									, inline=False)
					embed.set_footer(
						text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
							message=ctx.message), icon_url='https://media.discordapp.net/attachments/645276319311200286'
														   '/803322491480178739/winging-easy.png?width=676&height=676')
					await ctx.send(embed=embed)
			except Exception:
				embed = discord.Embed(title='Fehler', colour=get_colour(ctx.message))
				embed.set_thumbnail(
					url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png'
						'?width=676&height=676')
				embed.add_field(name='‎', value=f'Der Cog ```{cogname}``` konnte nicht neu geladen werden.'
								, inline=False)
				embed.set_footer(
					text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
						message=ctx.message), icon_url='https://media.discordapp.net/attachments/645276319311200286'
													   '/803322491480178739/winging-easy.png?width=676&height=676')
				await ctx.send(embed=embed)
		else:
			await ctx.send(f'{mention}, dieser Befehl kann nur im Kanal #{botchannel} genutzt werden.',
						   delete_after=3)
			await msg2.delete()

	@reload.error
	async def handle_error(self, ctx, error):
		user = ctx.author
		if isinstance(error, MissingRequiredArgument):
			embed = discord.Embed(title='**Fehler**', colour=get_colour(ctx.message))
			embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
				message=ctx.message),
							 icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
									  '/winging-easy.png?width=676&height=676')
			embed.add_field(name='‎',
							value='Du hast nicht alle erforderlichen Argumente angegeben, Nutzung: ```' +
								  get_prefix_string(ctx.message) + '```cog reload <Name>```',
							inline=False)
			await ctx.send(embed=embed)

	@cog.command()
	@commands.is_owner()
	async def reloadall(self, ctx):
		global filename
		x = 0
		user = ctx.author.name
		name = ctx.channel.name
		msg2 = ctx.message
		mention = ctx.author.mention
		botchannel = get_botc(message=ctx.message)
		if name == botchannel or botchannel == 'None':
			try:
				for directory in os.listdir('./cogs'):
					if directory != "Ignore":
						for directory2 in os.listdir(f'./cogs/{directory}'):
							for filename in os.listdir(f'./cogs/{directory}/{directory2}/'):
								if filename.endswith(".py"):
									extension = f"cogs.{directory}.{directory2}.{filename[:-3]}"
									client.unload_extension(extension)
									client.load_extension(extension)

				embed = discord.Embed(title='Cog Reload', colour=get_colour(ctx.message))
				embed.set_thumbnail(
					url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png'
						'?width=676&height=676')
				embed.add_field(name='‎',
								value=f'Alle Cogs konnte erfolgreich neu geladen werden.'
								, inline=False)
				embed.set_footer(
					text='for ' + str(user) + ' | by ' + str(
						get_author()) + ' | Prefix ' + get_prefix_string(
						message=ctx.message),
					icon_url='https://media.discordapp.net/attachments/645276319311200286'
							 '/803322491480178739/winging-easy.png?width=676&height=676')
				await ctx.send(embed=embed)

			except Exception:
				embed = discord.Embed(title='Fehler', colour=get_colour(ctx.message))
				embed.set_thumbnail(
					url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png'
						'?width=676&height=676')
				embed.add_field(name='‎', value=f'Der Cog ```{filename}``` konnte nicht neu geladen werden.'
								, inline=False)
				embed.set_footer(
					text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
						message=ctx.message), icon_url='https://media.discordapp.net/attachments/645276319311200286'
													   '/803322491480178739/winging-easy.png?width=676&height=676')
				await ctx.send(embed=embed)
		else:
			await ctx.send(f'{mention}, dieser Befehl kann nur im Kanal #{botchannel} genutzt werden.',
						   delete_after=3)
			await msg2.delete()


########################################################################################################################


def setup(bot):
	bot.add_cog(cog(bot))
