#from webserver import keep_alive
from dataclasses import replace
from turtle import back
from unicodedata import category
from urllib import response
import discord
import config
import datetime
import random
import json
import sqlite3
import time
import requests
from datetime import datetime
from config import TOKEN
from discord.ext import commands
import discord_components
from discord_components import DiscordComponents, Button, ButtonStyle
from discord.utils import get

PREFIX = "+"
bot = commands.Bot(command_prefix=PREFIX,intents=discord.Intents.all())
bot.remove_command("help")
connection = sqlite3.connect('Data/server.db')
cursor = connection.cursor()

@bot.event
async def on_ready():
	cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        name TEXT,
        id INT,
        cash BIGINT,
        pack INT,
        storage INT,
        xp INT,
        lvl INT,
        server_id INT
    )""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS shop (
		role_id INT,
		id INT,
		cost BIGINT
    )""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS inventory (
		id INT,
		copper INT,
		lead INT,
		coal INT,
		iron INT,
		tin INT,
		stone INT,
		trash INT,
		gold INT,
		diamond INT,
		chest INT
	)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS bank (
		cash BIGINT,
		server_id INT		
	)""")

	for guild in bot.guilds:
		for member in guild.members:
			if member.bot != True:
				if cursor.execute(f"SELECT server_id FROM bank WHERE server_id = {guild.id}").fetchone() is None:
					cursor.execute(f"INSERT INTO bank VALUES (15000,{guild.id})")
					print(f"Сервер {guild.name} был записан в БД bank")
				else:
					pass
				if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
					cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0, 0, 0, 0, {guild.id})")
					print(f"Пользователь {member} был записан в БД users")
				else:
					pass
				if cursor.execute(f"SELECT id FROM inventory WHERE id = {member.id}").fetchone() is None:
					cursor.execute(f"INSERT INTO inventory VALUES ({member.id}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")
					print(f"Пользователь {member} был записан в БД inventory")
				else:
					pass
	connection.commit()
	game = discord.Game(f"{PREFIX}help")
	await bot.change_presence(status=discord.Status.online, activity=game)
	print("BOT CONNECTED !")
	DiscordComponents(bot)
@bot.event
async def on_member_join(member):
	if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
		cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0, 0, 0, 0, {member.guild.id})")
		print(f"Пользователь {member} был записан в БД")
	else:
		pass
	if cursor.execute(f"SELECT id FROM inventory WHERE id = {member.id}").fetchone() is None:
		cursor.execute(f"INSERT INTO inventory VALUES ({member.id}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")
		print(f"Пользователь {member} был записан в БД inventory")
	else:
		pass
	print(f"{member} зашел на сервер")
	welcome = bot.get_channel(id=1003064023916494848)
	await welcome.send(f"***{member.mention} Добро пожаловать на сервер {member.guild.name}, скорей заходи в войс почиллить с ребятами. :heart:***")
@bot.event
async def on_message(message):
	if message.author.id == 574652751745777665:
		if f"Top 10 Levels in {message.guild.name}" in f"{message.content}":
			file = open("data/leaderboard.txt","w")
			file.write(message.content)
			file.close()
			file = open("data/leaderboard.txt","r")
			content = file.readlines()
			for member in message.guild.members:
				role = discord.utils.get(member.guild.roles,id=999040553025011812)
				role2 = discord.utils.get(member.guild.roles,id=1002203023633813584)
				if f"{member}" in f"{content[1]}" or f"{member}" in f"{content[2]}" or f"{member}" in f"{content[3]}" or f"{member}" in f"{content[4]}" or f"{member}" in f"{content[5]}":
					await member.add_roles(role)
				elif f"{member}" in f"{content[6]}" or f"{member}" in f"{content[7]}" or f"{member}" in f"{content[8]}" or f"{member}" in f"{content[9]}" or f"{member}" in f"{content[10]}":
					await member.add_roles(role2)
	await bot.process_commands(message)
@bot.command(aliases=["bal","$","bank","money","cash"])
async def balance(ctx,*,member: discord.Member = None):
	if member is None:
		embed=discord.Embed(title="Баланс", description=f"""**Баланс пользователя** ***{ctx.author}:*** ``{cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}``:coin:""", color=0x73d216)
		embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
		embed.set_footer(text="Laberty Team ",icon_url="https://cdn-icons-png.flaticon.com/512/1443/1443000.png")
		await ctx.reply(embed=embed,
				components=[
					Button(style=ButtonStyle.red,label="Выход", custom_id= "mine",emoji="↩")
				])
		button_balance = await bot.wait_for("button_click")
		if button_balance.component.label == "Выход":
				await button_balance.send(
				"Выхожу"
			)
				await menu(ctx)
		if cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0] > 50000:
			role = discord.utils.get(ctx.author.guild.roles, id = 1002494493695692900)
			await ctx.author.add_roles(role)
		else:
			role = discord.utils.get(ctx.author.guild.roles, id = 1002494493695692900)
			await ctx.author.remove_roles(role)
	else:
		embed=discord.Embed(title="Баланс", description=f"""**Баланс пользователя** ***{member}:*** ``{cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]}``:coin:""", color=0x73d216)
		embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
		embed.set_footer(text="Laberty Team ",icon_url="https://cdn-icons-png.flaticon.com/512/1443/1443000.png")
		await ctx.reply(embed=embed,
				components=[
					Button(style=ButtonStyle.red,label="Выход", custom_id= "mine",emoji="↩")
				])
		# button_balance = await bot.wait_for("button_click")
		if button_balance.component.label == "Выход":
				await button_balance.send(
				"Выхожу"
			)
				await menu(ctx)

@bot.command(aliases=["orelreshka","coin","monetka","moneta"])
async def flip(ctx,stavka,vibor):
	if int(stavka) < 10:
		await ctx.reply("Вы не можете ставить меньше чем 10:coin:")
	elif int(stavka) > 20000:
		await ctx.reply("Вы не можете ставить больше чем 20.000:coin:")
	else:
		money = cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
		if int(money) >= int(stavka):
			otvets = ["o","r"]
			otvet = random.choice(otvets)
			if vibor == otvet:
				stava = int(stavka)*2-111
				cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(stava,ctx.author.id))
				cursor.execute("UPDATE bank SET cash = cash - {} WHERE server_id = {}".format(stava,ctx.guild.id))
				connection.commit()
				embed=discord.Embed(title="Монета", description=f"""**Вы угадали! Вы выйграли:** ``{stava}``:coin:, ваш баланс теперь составляет: ``{int(money)+int(stava)}``:coin:""", color=0x73d216)
				embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
				embed.set_footer(text="Laberty Team ",icon_url="https://cdn-icons-png.flaticon.com/512/1443/1443000.png")
				await ctx.send(embed=embed)	
			
			elif vibor != otvet:
				cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(stavka,ctx.author.id))
				cursor.execute("UPDATE bank SET cash = cash + {} WHERE server_id = {}".format(round(result),ctx.guild.id))
				connection.commit()
				embed=discord.Embed(title="Монета", description=f"""**К сожалению вы не угадали( Вы потеряли:** ``{stavka}``:coin:, ваш баланс теперь составляет: ``{int(money)-int(stavka)}``:coin:""", color=0x73d216)
				embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
				embed.set_footer(text="Laberty Team ",icon_url="https://cdn-icons-png.flaticon.com/512/1443/1443000.png")	
				await ctx.send(embed=embed)	
			else:
				await ctx.reply("Такого аргумента нет! Выберите существующие: ( r - Решка, o - Орёл )")
		else:
			await ctx.reply("У вас недостаточно денег чтобы сделать ставку!")

@bot.command()
@commands.has_permissions(administrator=True)
async def givemoney(ctx, member:discord.Member = None, amount: int = None):
	cash = cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]
	cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(round(amount),member.id))
	connection.commit()
	await ctx.reply(f"Вы успешно выдали пользователю ***{member}*** ``{amount}``:coin:, его баланс теперь составляет: ``{int(cash)+amount}``:coin:")

@bot.command()
@commands.has_permissions(administrator=True)
async def setmoney(ctx, member:discord.Member = None, amount: int = None):
	cash = cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]
	cursor.execute("UPDATE users SET cash = {} WHERE id = {}".format(round(amount),member.id))
	connection.commit()
	await ctx.reply(f"Вы успешно установили пользователю ***{member}*** ``{amount}``:coin:, его баланс теперь составляет: ``{amount}``:coin:")

@bot.command()
async def pay(ctx,member:discord.Member,amount: int):
	if member.bot:
		await ctx.reply("Вы не можете перевести деньги боту!")
	elif member == ctx.author:
		await ctx.reply("Вы не можете перевести деньги самому себе!")
	else:
		cash = cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
		if int(cash) >= amount:
			if amount < 1:
				await ctx.reply("Минимальная сумма перевода денег 1:coin:")
			elif amount > 100000:
				await ctx.reply("Максимальная сумма перевода денег 100.000:coin:")
			else:
				await ctx.reply(embed = discord.Embed(title = "Подтверждение",description=f"Вы уверены что хотите перевести ``{amount}``:coin: пользователю ***{member}***? Коммисия **2%**"),
					components=[
						Button(style=ButtonStyle.green,label="Да",emoji="✅"),
						Button(style=ButtonStyle.red,label="Нет",emoji="⛔")
					]
				)		
				response = await bot.wait_for("button_click")
				if response.channel == ctx.channel:
					if response.component.label == "Да":
						if response.author != ctx.author:
							await response.respond(content=f"Для перевода денег введите ``{PREFIX}pay <@пользователь> <сумма>``")
						else:
							comm = amount/100*2
							cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(round(amount+comm),ctx.author.id))
							cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(round(amount),member.id))
							cursor.execute("UPDATE bank SET cash = cash + {} WHERE server_id = {}".format(round(comm),ctx.guild.id))
							connection.commit()
							embed=discord.Embed(title="Перевод денег", description=f"Вы успешно перевели пользователю ***{member}*** ``{amount}``:coin:", color=0x73d216)
							embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
							embed.set_footer(text="Laberty Team ",icon_url="https://cdn-icons-png.flaticon.com/512/1443/1443000.png")	
							await ctx.reply(embed=embed)
					elif response.component.label == "Нет":
						if response.author != ctx.author:
							await response.respond(content=f"Для перевода денег введите ``{PREFIX}pay <@пользователь> <сумма>``")
						else:
							embed=discord.Embed(title="Перевод денег", description=f"Операция отменена. ⛔", color=0x73d216)
							embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
							embed.set_footer(text="Laberty Team ",icon_url="https://cdn-icons-png.flaticon.com/512/1443/1443000.png")	
							await ctx.reply(embed=embed)
		else:
			await ctx.reply("У вас недостаточно денег для перевода!")
@bot.command()
async def wheel(ctx, stavka):
	if int(stavka) < 10:
		await ctx.reply("Вы не можете ставить меньше чем 10:coin:")
	elif int(stavka) > 20000:
		await ctx.reply("Вы не можете ставить больше чем 20.000:coin:")
	else:
		money = cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
		if int(money) >= int(stavka):
			emoji = [":arrow_right:",":arrow_left:",":arrow_up:",":arrow_down:",":arrow_upper_right:",":arrow_lower_right:",":arrow_upper_left:",":arrow_lower_left:"]
			strel = random.choice(emoji)
			if strel == ":arrow_upper_left:":
				win = 1.5
			elif strel == ":arrow_up:":
				win = 1.7
			elif strel == ":arrow_upper_right:":
				win = 2.4
			elif strel == ":arrow_left:":
				win = 0.2
			elif strel == ":arrow_right:":
				win = 1.2
			elif strel == ":arrow_lower_left:":
				win = 0.1
			elif strel == ":arrow_down:":
				win = 0.3
			elif strel == ":arrow_lower_right:":
				win = 0.5
			cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(round(int(stavka)),ctx.author.id))
			cursor.execute("UPDATE bank SET cash = cash + {} WHERE server_id = {}".format(round(int(stavka)),ctx.guild.id))
			cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(round(int(stavka))*win,ctx.author.id))
			connection.commit()
			win_ = int(stavka)*win
			money = cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
			embed=discord.Embed(title="Колесо фортуны", description=f"	『1.5』	『1.7』	『2.4』\n \n	『0.2』	{strel}  	『1.2』\n \n	『0.1』	 『0.3』	 『0.5』 \n \n**Вы выйграли:** ``{win_}``:coin:, ваш баланс теперь составляет: ``{int(money)}``:coin:", color=0x73d216)
			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			embed.set_footer(text="Laberty Team ",icon_url="https://cdn-icons-png.flaticon.com/512/1443/1443000.png")
			await ctx.reply(embed = embed)
		else:
			await ctx.reply("У вас недостаточно денег чтобы сделать ставку!")

@bot.command(aliases=["br","betroll"])
async def dice(ctx,stavka:int):
	money = cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
	if stavka < 10:
		await ctx.reply("Вы не можете ставить меньше чем 10:coin:")
	elif stavka > 20000:
		await ctx.reply("Вы не можете ставить больше чем 20.000:coin:")
	else:
		if money >= stavka:
			cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(round(stavka),ctx.author.id))
			cursor.execute("UPDATE bank SET cash = cash + {} WHERE server_id = {}".format(round(stavka),ctx.guild.id))
			number = random.randint(1,100)
			if number > 66:
				result = stavka*2
				desc = f"**{ctx.author}**``Вам выпало {number}.``Поздравляем!\nВы победили {result} :coin:, так как выбросили число больше 66"
				cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(round(result),ctx.author.id))
			elif number > 90:
				result = stavka*4
				desc = f"**{ctx.author}**``Вам выпало {number}.``Поздравляем!\nВы победили {result} :coin:, так как выбросили число больше 90"
				cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(round(result),ctx.author.id))
			else:
				desc = f"**{ctx.author}**``Вам выпало {number}.``Удачи в\nследующий раз :heart:"
			
			connection.commit()
			embed=discord.Embed(title="Кости", description=desc, color=0x73d216)	
			await ctx.reply(embed=embed,
				components=[
					Button(style=ButtonStyle.green, label="Еще раз",emoji="🔄"),
					Button(style=ButtonStyle.red, label="Выход",emoji="↩")
				]
			)
			response = await bot.wait_for("button_click")
			if response.channel == ctx.channel:
				if response.component.label == "Еще раз":
					await response.send(
						"Оки )"
					)
					await dice(ctx,stavka)
				if response.component.label == "Выход":
					await response.send(
						"Выхожу"
					)
					await menu(ctx)
		else:
			await ctx.reply("У вас недостаточно денег!")
@bot.command(aliases=["top","lb","leaders","servertop"])
async def leaderboard(ctx):
	embed=discord.Embed(title=f"Топ 10 богачей {ctx.guild.name} ",color=0x73d216)
	embed.set_footer(text="Laberty Team ",icon_url="https://cdn-icons-png.flaticon.com/512/1443/1443000.png")
	counter = 0
	for row in cursor.execute("SELECT name, cash FROM users WHERE server_id = {} ORDER BY cash DESC LIMIT 10".format(ctx.guild.id)):
		counter += 1
		embed.add_field(name=f"{counter}. {row[0]}",value=f"**{row[1]}** :coin:",inline=False)
	await ctx.reply(
		embed=embed,
				components=[
				Button(style=ButtonStyle.red,label="Выйти",emoji="↩")
				])
	button_leaderboards_top_users = await bot.wait_for("button_click")
	if button_leaderboards_top_users.channel == ctx.channel:
		if button_leaderboards_top_users.component.label == "Выйти":
			await button_leaderboards_top_users.send(
				"Выхожу"
			)
			await menu(ctx)

@bot.command()
async def mine(ctx):
	ores = ["iron","coal","copper","gold","diamond","tin","lead","trash","stone","chest","stone","stone","stone","stone","trash","trash","trash","lead","lead","tin","copper","copper","copper","iron","stone","trash","trash","trash","trash","trash","trash","trash","trash","trash","trash","trash","trash","trash","trash","trash","trash","trash","trash","trash","trash","trash","trash","trash","trash","trash","trash"]
	ore = random.choice(ores)
	count = random.randint(1,4)
	if ore == "iron":
		ore = "Железная руда"
		cursor.execute("UPDATE inventory SET iron = iron + {} WHERE id = {}".format(count,ctx.author.id))
	elif ore == "coal":
		ore = "Уголь"
		cursor.execute("UPDATE inventory SET coal = coal + {} WHERE id = {}".format(count,ctx.author.id))
	elif ore == "copper":
		ore = "Медь"
		cursor.execute("UPDATE inventory SET copper = copper + {} WHERE id = {}".format(count,ctx.author.id))
	elif ore == "gold":
		ore = "Золотая руда"
		cursor.execute("UPDATE inventory SET gold = gold + {} WHERE id = {}".format(count,ctx.author.id))
	elif ore == "diamond":
		ore = "Алмаз"
		cursor.execute("UPDATE inventory SET diamond = diamond + {} WHERE id = {}".format(count,ctx.author.id))
	elif ore == "tin":
		ore = "Оловянная руда"
		cursor.execute("UPDATE inventory SET tin = tin + {} WHERE id = {}".format(count,ctx.author.id))
	elif ore == "lead":
		ore = "Свинцовая руда"
		cursor.execute("UPDATE inventory SET lead = lead + {} WHERE id = {}".format(count,ctx.author.id))
	elif ore == "trash":
		ore = "Хлам"
		cursor.execute("UPDATE inventory SET trash = trash + {} WHERE id = {}".format(count,ctx.author.id))
	elif ore == "stone":
		ore = "Камень"
		cursor.execute("UPDATE inventory SET stone = stone + {} WHERE id = {}".format(count,ctx.author.id))
	elif ore == "chest":
		ore = "Сундук с драгоценностями"
		cursor.execute("UPDATE inventory SET chest = chest + {} WHERE id = {}".format(count,ctx.author.id))
	connection.commit()
	embed = discord.Embed(title="Шахта",description=f"Вы добыли: ***{ore} x{count}***")
	result = count/2*1.1
	cursor.execute("UPDATE users SET xp = xp + {} WHERE id = {}".format(round(result),ctx.author.id))
	connection.commit()
	await ctx.reply(embed = embed,
		components=[
			Button(style=ButtonStyle.green, label="Еще раз",emoji="🔄"),
			Button(style=ButtonStyle.red, label="Выход",emoji="↩")
		]
	)
	response = await bot.wait_for("button_click")
	if response.channel == ctx.channel:
		if response.component.label == "Еще раз":
			await response.send(
				"Оки )"
			)
			await mine(ctx)
		if response.component.label == "Выход":
			await response.send(
				"Выхожу"
			)
			await menu(ctx)

@bot.command(aliases=["inv","invent"])
async def inventory(ctx):
	embed = discord.Embed(title="Инвентарь")
	embed.add_field(name="Хлам",value=f"""{cursor.execute("SELECT trash FROM inventory WHERE id = {}".format(ctx.author.id)).fetchone()[0]} штуки""")
	embed.add_field(name="Камень",value=f"""{cursor.execute("SELECT stone FROM inventory WHERE id = {}".format(ctx.author.id)).fetchone()[0]} штуки""")
	embed.add_field(name="Медь",value=f"""{cursor.execute("SELECT copper FROM inventory WHERE id = {}".format(ctx.author.id)).fetchone()[0]} штуки""")
	embed.add_field(name="Свинцовая руда",value=f"""{cursor.execute("SELECT lead FROM inventory WHERE id = {}".format(ctx.author.id)).fetchone()[0]} штуки""")
	embed.add_field(name="Оловянная руда",value=f"""{cursor.execute("SELECT tin FROM inventory WHERE id = {}".format(ctx.author.id)).fetchone()[0]} штуки""")
	embed.add_field(name="Железная руда",value=f"""{cursor.execute("SELECT iron FROM inventory WHERE id = {}".format(ctx.author.id)).fetchone()[0]} штуки""")
	embed.add_field(name="Золотая руда",value=f"""{cursor.execute("SELECT gold FROM inventory WHERE id = {}".format(ctx.author.id)).fetchone()[0]} штуки""")
	embed.add_field(name="Алмаз",value=f"""{cursor.execute("SELECT diamond FROM inventory WHERE id = {}".format(ctx.author.id)).fetchone()[0]} штуки""")
	embed.add_field(name="Сундук с драгоценностями",value=f"""{cursor.execute("SELECT chest FROM inventory WHERE id = {}".format(ctx.author.id)).fetchone()[0]} штуки""")
	await ctx.reply(embed=embed,
				components=[
					Button(style=ButtonStyle.blue,label="Выход",emoji="↩", custom_id= "mine")
				])
	button_inventory = await bot.wait_for("button_click")
	if button_inventory.channel == ctx.channel:
		if button_inventory.component.label == "Выход":
			await button_inventory.send(
				"Выхожу"
			)
			await menu(ctx)



@bot.command()
async def sell(ctx,ore,count:int = None):
	trash = cursor.execute("SELECT trash FROM inventory WHERE id = {}".format(ctx.author.id)).fetchone()[0]
	stone = cursor.execute("SELECT stone FROM inventory WHERE id = {}".format(ctx.author.id)).fetchone()[0]
	copper = cursor.execute("SELECT copper FROM inventory WHERE id = {}".format(ctx.author.id)).fetchone()[0]
	lead = cursor.execute("SELECT lead FROM inventory WHERE id = {}".format(ctx.author.id)).fetchone()[0]
	tin = cursor.execute("SELECT tin FROM inventory WHERE id = {}".format(ctx.author.id)).fetchone()[0]
	iron = cursor.execute("SELECT iron FROM inventory WHERE id = {}".format(ctx.author.id)).fetchone()[0]
	gold = cursor.execute("SELECT gold FROM inventory WHERE id = {}".format(ctx.author.id)).fetchone()[0]
	diamond = cursor.execute("SELECT diamond FROM inventory WHERE id = {}".format(ctx.author.id)).fetchone()[0]
	chest = cursor.execute("SELECT chest FROM inventory WHERE id = {}".format(ctx.author.id)).fetchone()[0]
	All = trash+stone+copper+lead+tin+iron+gold+diamond+chest

	trash_cost = 0.01
	stone_cost = 0.1
	copper_cost = 1
	lead_cost = 1.5
	tin_cost = 3
	iron_cost = 5
	gold_cost = 7
	diamond_cost = 15
	chest_cost = random.randint(10,45)
	result = trash*trash_cost+stone*stone_cost+copper*copper_cost+lead*lead_cost+tin*tin_cost+iron*iron_cost+gold*gold_cost+diamond*diamond_cost+chest*chest_cost
	if ore == 'all':
		cursor.execute("UPDATE inventory SET trash = 0 WHERE id = {}".format(ctx.author.id))
		cursor.execute("UPDATE inventory SET stone = 0 WHERE id = {}".format(ctx.author.id))
		cursor.execute("UPDATE inventory SET copper = 0 WHERE id = {}".format(ctx.author.id))
		cursor.execute("UPDATE inventory SET lead = 0 WHERE id = {}".format(ctx.author.id))
		cursor.execute("UPDATE inventory SET tin = 0 WHERE id = {}".format(ctx.author.id))
		cursor.execute("UPDATE inventory SET iron = 0 WHERE id = {}".format(ctx.author.id))
		cursor.execute("UPDATE inventory SET gold = 0 WHERE id = {}".format(ctx.author.id))
		cursor.execute("UPDATE inventory SET diamond = 0 WHERE id = {}".format(ctx.author.id))
		cursor.execute("UPDATE inventory SET chest = 0 WHERE id = {}".format(ctx.author.id))
		cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(round(result),ctx.author.id))
		res = All/2*1.1
		cursor.execute("UPDATE users SET  = xp + {} WHERE id = {}".format(res,ctx.author.id))
		connection.commit()
		await ctx.reply(f"Вы успешно продали все предметы в сумме: ``{round(result)}``:coin:")
		connection.commit()
		
	if count != None:
		if count > 1:
			if ore == 'trash':
				if count is None:
					await ctx.reply(f"Введите количество предметов которые хотите продать (  Пример: {PREFIX}sell trash 5   )")
				else:
					if trash >= count:
						result = trash*trash_cost
						cursor.execute("UPDATE inventory SET trash = trash - {} WHERE id = {}".format(count,ctx.author.id))
						cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(round(result),ctx.author.id))
						cursor.execute("UPDATE bank SET cash = cash - {} WHERE server_id = {}".format(round(result),ctx.guild.id))
						await ctx.reply(f"Вы успешно продали предмет Хлам x{count} штуки за {round(result)}:coin:")
					else:
						await ctx.reply(f"У вас нету x{count} штуки хлама, у вас имеется только x{trash}")
			elif ore == 'stone':
				if count is None:
					await ctx.reply(f"Введите количество предметов которые хотите продать (  Пример: {PREFIX}sell stone 5   )")
				else:
					if stone >= count:
						result = stone*stone_cost
						cursor.execute("UPDATE inventory SET stone = stone - {} WHERE id = {}".format(count,ctx.author.id))
						cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(round(result),ctx.author.id))
						cursor.execute("UPDATE bank SET cash = cash - {} WHERE server_id = {}".format(round(result),ctx.guild.id))
						await ctx.reply(f"Вы успешно продали предмет Камень x{count} штуки за {round(result)}:coin:")
					else:
						await ctx.reply(f"У вас нету x{count} штуки камня, у вас имеется только x{stone}")
			elif ore == 'copper':
				if count is None:
					await ctx.reply(f"Введите количество предметов которые хотите продать (  Пример: {PREFIX}sell copper 5   )")
				else:
					if copper >= count:
						result = copper*copper_cost
						cursor.execute("UPDATE inventory SET copper = copper - {} WHERE id = {}".format(count,ctx.author.id))
						cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(round(result),ctx.author.id))
						cursor.execute("UPDATE bank SET cash = cash - {} WHERE server_id = {}".format(round(result),ctx.guild.id))
						await ctx.reply(f"Вы успешно продали предмет Медь x{count} штуки за {round(result)}:coin:")
					else:
						await ctx.reply(f"У вас нету x{count} штуки меди, у вас имеется только x{copper}")
			elif ore == 'lead':
				if count is None:
					await ctx.reply(f"Введите количество предметов которые хотите продать (  Пример: {PREFIX}sell lead 5   )")
				else:
					if lead >= count:
						result = lead*lead_cost
						cursor.execute("UPDATE inventory SET lead = lead - {} WHERE id = {}".format(count,ctx.author.id))
						cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(round(result),ctx.author.id))
						cursor.execute("UPDATE bank SET cash = cash - {} WHERE server_id = {}".format(round(result),ctx.guild.id))
						await ctx.reply(f"Вы успешно продали предмет Свинец x{count} штуки за {round(result)}:coin:")
					else:
						await ctx.reply(f"У вас нету x{count} штуки свинца, у вас имеется только x{lead}")
			elif ore == 'tin':
				if count is None:
					await ctx.reply(f"Введите количество предметов которые хотите продать (  Пример: {PREFIX}sell tin 5   )")
				else:
					if tin >= count:
						result = tin*tin_cost
						cursor.execute("UPDATE inventory SET tin = tin - {} WHERE id = {}".format(count,ctx.author.id))
						cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(round(result),ctx.author.id))
						cursor.execute("UPDATE bank SET cash = cash - {} WHERE server_id = {}".format(round(result),ctx.guild.id))
						await ctx.reply(f"Вы успешно продали предмет Оловянная руда x{count} штуки за {round(result)}:coin:")
					else:
						await ctx.reply(f"У вас нету x{count} оловянной руды, у вас имеется только x{tin}")
			elif ore == 'iron':
				if count is None:
					await ctx.reply(f"Введите количество предметов которые хотите продать (  Пример: {PREFIX}sell iron 5   )")
				else:
					if iron >= count:
						result = iron*iron_cost
						cursor.execute("UPDATE inventory SET iron = iron - {} WHERE id = {}".format(count,ctx.author.id))
						cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(round(result),ctx.author.id))
						cursor.execute("UPDATE bank SET cash = cash - {} WHERE server_id = {}".format(round(result),ctx.guild.id))
						await ctx.reply(f"Вы успешно продали предмет Железная руда x{count} штуки за {round(result)}:coin:")
					else:
						await ctx.reply(f"У вас нету x{count} железной руды, у вас имеется только x{iron}")
			elif ore == 'gold':
				if count is None:
					await ctx.reply(f"Введите количество предметов которые хотите продать (  Пример: {PREFIX}sell gold 5   )")
				else:
					if gold >= count:
						result = gold*gold_cost
						cursor.execute("UPDATE inventory SET gold = gold - {} WHERE id = {}".format(count,ctx.author.id))
						cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(round(result),ctx.author.id))
						cursor.execute("UPDATE bank SET cash = cash - {} WHERE server_id = {}".format(round(result),ctx.guild.id))
						await ctx.reply(f"Вы успешно продали предмет Золотая руда x{count} штуки за {round(result)}:coin:")
					else:
						await ctx.reply(f"У вас нету x{count} золотой руды, у вас имеется только x{gold}")
			elif ore == 'diamond':
				if count is None:
					await ctx.reply(f"Введите количество предметов которые хотите продать (  Пример: {PREFIX}sell diamond 5   )")
				else:
					if gold >= count:
						result = diamond*diamond_cost
						cursor.execute("UPDATE inventory SET diamond = diamond - {} WHERE id = {}".format(count,ctx.author.id))
						cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(round(result),ctx.author.id))
						cursor.execute("UPDATE bank SET cash = cash - {} WHERE server_id = {}".format(round(result),ctx.guild.id))
						await ctx.reply(f"Вы успешно продали предмет Алмаз x{count} штуки за {round(result)}:coin:")
					else:
						await ctx.reply(f"У вас нету x{count} алмазов, у вас имеется только x{diamond}")
			elif ore == 'chest':
				if count is None:
					await ctx.reply(f"Введите количество предметов которые хотите продать (  Пример: {PREFIX}sell chest 5   )")
				else:
					if chest >= count:
						result = chest*chest_cost
						cursor.execute("UPDATE inventory SET chest = chest - {} WHERE id = {}".format(count,ctx.author.id))
						cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(round(result),ctx.author.id))
						cursor.execute("UPDATE bank SET cash = cash - {} WHERE server_id = {}".format(round(result),ctx.guild.id))
						await ctx.reply(f"Вы успешно продали предмет Сундук с драгоценностями x{count} штуки за {round(result)}:coin:")
					else:
						await ctx.reply(f"У вас нету x{count} сундуков с драгоценностями, у вас имеется только x{chest}")
			else:
				await ctx.reply("Такого предмета не существует!")

@bot.command()
async def slot(ctx,stavka:int):
	if stavka is None:
		await ctx.reply(f"*Ты чё огурец?* ***Пиши так:*** ``{PREFIX}slot <ставка>``")
	else:
		if cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0] >= stavka:
			if stavka < 100:
				await ctx.reply("Ставка должна быть не меньше 100:coin:")
			elif stavka > 35000:
				await ctx.reply("Ставка должна быть не больше 35.000:coin:")
			else:
				fruits = [":strawberry:",":apple:",":watermelon:",":cherries:",":grapes:",":lemon:",":seven:"]
				one = random.choice(fruits)
				two = random.choice(fruits)
				three = random.choice(fruits)
				cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(stavka,ctx.author.id))
				if one == ":strawberry:" and two == ":strawberry:" and three == ":strawberry:":
					result = stavka*1.5
				elif one == ":apple:" and two == ":apple:" and three == ":apple:":
					result = stavka*2
				elif one == ":watermelon:" and two == ":watermelon:" and three == ":watermelon:":
					result = stavka*1.2
				elif one == ":cherries:" and two == ":cherries:" and three == ":cherries:":
					result = stavka*2.2
				elif one == ":grapes:" and two == ":grapes:" and three == ":grapes:":
					result = stavka*1.3
				elif one == ":lemon:" and two == ":lemon:" and three == ":lemon:":
					result = stavka*1.1
				elif one == ":seven:" and two == ":seven:" and three == ":seven:":
					result = stavka*5
				else:
					result = 0
				cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(round(result),ctx.author.id))
				cursor.execute("UPDATE bank SET cash = cash - {} WHERE server_id = {}".format(round(result),ctx.guild.id))
				embed = discord.Embed(title="Слоты",description=f"{one}{two}{three} \n **Вы выйграли:** ``{result}``:coin:")
				await ctx.reply(embed = embed)

@bot.command(aliases=["gift"])
@commands.cooldown(1, 60*60*4, commands.BucketType.user)
async def timely(ctx):
	prize = random.randint(65,120)
	embed = discord.Embed(title="Ежедневная награда",description=f"***Вы получили свою ежедневную награду!***")
	cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(prize,ctx.author.id))
	await ctx.reply(embed = embed)

@timely.error
async def timely_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="Ежедневная награда",description=f"""***Вы уже получили свою награду, до следующей награды ждите {error.retry_after:.2f} часов***""")
        await ctx.send(embed=embed)

@bot.command()
async def check_(ctx):
	await ctx.channel.purge(limit=1)
	if ctx.author.id == 890649916135833600:
		for guild in bot.guilds:
			guild_name = guild.name
		embed = discord.Embed(title="Статистика бота",description=f"Бот имеется на {len(bot.guilds)} сервере: \n {guild_name}")
		await ctx.send(embed=embed)
	
@bot.command()
async def menu(ctx):
		embed=discord.Embed(title="Меню", color=0x73d216)
		#embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
		embed.set_footer(text="Laberty Team ",icon_url="https://cdn-icons-png.flaticon.com/512/1443/1443000.png")
		await ctx.send(
			embed=embed,
			components=[
				Button(style=ButtonStyle.blue,label="Работа",emoji="🔧" , custom_id="work"),
				Button(style=ButtonStyle.blue,label="Казино",emoji="🎲"  , custom_id="casino"),
				Button(style=ButtonStyle.blue,label="Банк",emoji="💰" , custom_id="bank")
			]
		)


		category = await bot.wait_for("button_click")
		if category.component.label == "Работа":
				embed=discord.Embed(title="Работа", description=f"Выберите желаемую работу", color=0x73d216)
				embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
				embed.set_footer(text="Laberty Team ",icon_url="https://cdn-icons-png.flaticon.com/512/1443/1443000.png")
				await category.send(
						embed=embed,
						components=[
							Button(style=ButtonStyle.blue,label="Шахта",emoji="⚒"),
							Button(style=ButtonStyle.red,label="Назад",emoji="↩")
						]
				)
				response = await bot.wait_for("button_click")
				
				# backone = await bot.wait_for("button_click")
				if response.component.label == "Назад":
						await response.send(
								"Идем назад :)"
							)
						await menu(ctx)

				if response.component.label == "Шахта":
						embed=discord.Embed(title="Шахта", color=0x73d216)
						embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
						embed.set_footer(text="Laberty Team ",icon_url="https://cdn-icons-png.flaticon.com/512/1443/1443000.png")
						await response.send(
						embed=embed,
									components=[
											Button(style=ButtonStyle.blue,label="Добывать",emoji="🔨" , custom_id="mine_add"),
											Button(style=ButtonStyle.blue,label="Инвентарь",emoji="💼", custom_id="inventory"),
											Button(style=ButtonStyle.blue,label="Продать всё",emoji="💲",custom_id="sell_all"),
											Button(style=ButtonStyle.red,label="Назад",emoji="↩")
										]
						)

						response2 = await bot.wait_for("button_click")
						if response2.component.label == "Добывать":
								await response2.send(
									"Введите +mine для добычи!"
								)
								await mine(ctx)
						if response2.component.label == "Инвентарь":
									await response2.send(
									"Вот ваш инвентарь !"
								)
									await inventory(ctx)

						if response2.component.label == "Продать всё":
									await response2.send(
									"Всё успешно продано !"
								)
									await sell(ctx,"all")

						if response2.component.label == "Назад":
								await response2.send(
									"Идем назад :)"
								)
								await menu(ctx)
					
		if category.component.label == "Казино":
			embed=discord.Embed(title="Казино", description=f"Выберите желаемую игру", color=0x73d216)
			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			embed.set_footer(text="Laberty Team ",icon_url="https://cdn-icons-png.flaticon.com/512/1443/1443000.png")
			await category.send(
				embed=embed,
				components=[
					Button(style=ButtonStyle.blue,label="Колесо фортуны",emoji="☸"),
					Button(style=ButtonStyle.blue,label="Бросить монетку",emoji="🪙"),
					Button(style=ButtonStyle.blue,label="Слоты",emoji="🎰"),
					Button(style=ButtonStyle.red,label="Назад",emoji="↩")
				]
			)
			
			response3 = await bot.wait_for("button_click")
			if response3.component.label == "Колесо фортуны":
				embed=discord.Embed(title="Команда", description="Используйте: ``{}wheel <ставка>``".format(PREFIX), color=0x73d216)
				# 
				await response3.respond(embed=embed,
				components=[
				Button(style=ButtonStyle.red,label="Выйти",emoji="↩")
				])
				button_exit_wheel_of_fortune = await bot.wait_for("button_click")
				if button_exit_wheel_of_fortune.component.label == "Выйти":
					await button_exit_wheel_of_fortune.send(
				"Выхожу"
				)
					await menu(ctx)
		
			if response3.component.label == "Бросить монетку":
				embed=discord.Embed(title="Команда", description="Используйте: ``{}flip <ставка> <на что ставишь (o - Орёл, r - Решка)>``".format(PREFIX), color=0x73d216)
				# 
				await response3.respond(embed=embed,
				components=[
				Button(style=ButtonStyle.red,label="Выйти",emoji="↩")
				])
				button_exit_toss_a_coin = await bot.wait_for("button_click")
				if button_exit_toss_a_coin.component.label == "Выйти":
					await button_exit_toss_a_coin.send(
				"Выхожу"
				)
					await menu(ctx)

			if response3.component.label == "Слоты":
				embed=discord.Embed(title="Команда", description="Используйте: ``{}slot <ставка>``".format(PREFIX), color=0x73d216)
				# 
				await response3.respond(embed=embed,
				components=[
				Button(style=ButtonStyle.red,label="Выйти",emoji="↩")
				])
				button_exit_slots = await bot.wait_for("button_click")
				if button_exit_slots.component.label == "Выйти":
					await button_exit_slots.send(
				"Выхожу"
				)
					await menu(ctx)
			
			if response3.component.label == "Назад":
					await response3.send(
									"Идем назад :)"
								)
					await menu(ctx)

		if category.component.label == "Банк":
			embed=discord.Embed(title="Банк", description=f"Выберите желаемое действие", color=0x73d216)
			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			embed.set_footer(text="Laberty Team ",icon_url="https://cdn-icons-png.flaticon.com/512/1443/1443000.png")
			await category.send(
				embed=embed,
				components=[
					Button(style=ButtonStyle.blue,label="Баланс",emoji="💳"),
					Button(style=ButtonStyle.blue,label="Инвентарь",emoji="💼"),
					Button(style=ButtonStyle.blue,label="Список лидеров",emoji="🔝"),
					Button(style=ButtonStyle.red,label="Назад",emoji="↩")
				]
			)	

			response4 = await bot.wait_for("button_click")
			if response4.component.label == "Баланс":
					await response4.send("Показываю ваш баланс :)")
					await balance(ctx)
			if response4.component.label == "Инвентарь":
					await response4.send("Показываю ваш инвентарь :)")
					await inventory(ctx)
			if response4.component.label == "Список лидеров":
					await response4.send("Показываю таблицу лидеров :)")
					await leaderboard(ctx)
			if response4.component.label == "Назад":
					await response4.send(
									"Идем назад :)"
								)
					await menu(ctx)
		


@bot.command(aliases=["помощь","?"])
async def help(ctx,cmd=None):
	if cmd is None:
		embed = discord.Embed(title="Помощь",description="Чтобы не возникали лишние вопросы как? и что? Советуем для начала посмотреть как пользоваться командами, там всё понятно расписано, Удачи :heart:")
		embed.add_field(name="Информация по командам",value=f"``{PREFIX}help <команда>`` — показывает информацию о команде.")
		await ctx.reply(embed = embed,
			components=[
				Button(style=ButtonStyle.green,label="Список команд",emoji="📨")
			]
		)	
		response = await bot.wait_for("button_click")
		if response.channel == ctx.channel:
			if response.component.label == "Список команд":
				embed = discord.Embed(title=f"Список команд",description=f"``{PREFIX}balance`` ``{PREFIX}flip`` ``{PREFIX}wheel`` ``{PREFIX}pay`` ``{PREFIX}givemoney`` ``{PREFIX}setmoney`` ``{PREFIX}help`` ``{PREFIX}join`` ``{PREFIX}leave`` ``{PREFIX}activity`` ``{PREFIX}leaderboard`` ``{PREFIX}add-shop`` ``{PREFIX}remove-shop`` ``{PREFIX}shop`` ``{PREFIX}buy-role`` ``{PREFIX}pack`` ``{PREFIX}mine`` ``{PREFIX}sell`` ``{PREFIX}inventory`` ``{PREFIX}slot``")
				await response.respond(embed=embed)
	else:
		if cmd == 'help' or cmd == 'помощь' or cmd == '?':
			embed = discord.Embed(title=f"``{PREFIX}help``**/**``{PREFIX}помощь``**/**``{PREFIX}?``",description="Показывает информацию о командах")
			embed.add_field(name="Использование",value=f"``{PREFIX}help`` ``{PREFIX}help <команда>``")
			await ctx.reply(embed=embed)
		elif cmd == "flip" or cmd == 'coin' or cmd == 'moneta' or cmd == 'monetka':
			embed = discord.Embed(title=f"``{PREFIX}flip``**/**``{PREFIX}coin``**/**``{PREFIX}moneta``**/**``{PREFIX}monetka``",description="Ставьте ставку и угадывайте что выпадет орёл или решка, если вы угадаете то получите в двое больше чем ставили, а если проиграете то ваши деньги улетят в казну")
			embed.add_field(name="Использование",value=f"``{PREFIX}flip <ставка> <на кого ставишь (o - Орёл, r - Решка)>``")
			await ctx.reply(embed=embed)
		elif cmd == 'wheel':
			embed = discord.Embed(title=f"``{PREFIX}wheel``",description="Ставьте ставку и крутите колесо фортуны, какое число выпадет на такое и умножиться ваша ставка и вы заберете деньги себе")
			embed.add_field(name="Использование",value=f"``{PREFIX}wheel <ставка> ``")
			await ctx.reply(embed=embed)
		elif cmd == 'balance' or cmd == 'bal' or cmd == '$' or cmd == 'bank' or cmd == 'money' or cmd == 'cash':
			embed = discord.Embed(title=f"``{PREFIX}balance``**/**``{PREFIX}bal``**/**``{PREFIX}$``**/**``{PREFIX}bank``**/**``{PREFIX}money``**/**``{PREFIX}cash``",description="Проверяет ваш баланс/баланс других игроков")
			embed.add_field(name="Использование",value=f"``{PREFIX}balance`` ``{PREFIX}balance <@пользователь>``")
			await ctx.reply(embed=embed)
		elif cmd == 'pay':
			embed = discord.Embed(title=f"``{PREFIX}pay``",description="С этой командой вы можете перевести деньги со своего счета другому игроку")
			embed.add_field(name="Использование",value=f"``{PREFIX}pay <@пользователь> <сумма>``")
			await ctx.reply(embed=embed)
		elif cmd == 'givemoney':
			embed = discord.Embed(title=f"``{PREFIX}givemoney``",description="Админская команда с помощью которой можно выдавать игрокам деньги")
			embed.add_field(name="Использование",value=f"``{PREFIX}givemoney <@пользователь> <сумма>``")
			await ctx.reply(embed=embed)
		elif cmd == 'setmoney':
			embed = discord.Embed(title=f"``{PREFIX}setmoney``",description="Админская команда с помощью которой можно установить игрокам определенный баланс")
			embed.add_field(name="Использование",value=f"``{PREFIX}setmoney <@пользователь> <сумма>``")
			await ctx.reply(embed=embed)
		elif cmd == 'leaderboard' or cmd == 'lb' or cmd == 'servertop' or cmd == 'top' or cmd == 'leaders':
			embed = discord.Embed(title=f"``{PREFIX}leaderboard``**/**``{PREFIX}lb``**/**``{PREFIX}servertop``**/**``{PREFIX}top``**/**``{PREFIX}leaders``",description="Выводит топ 10 лидеров по балансу")
			embed.add_field(name="Использование",value=f"``{PREFIX}leaderboard``")
			await ctx.reply(embed=embed)
		elif cmd == 'mine':
			embed = discord.Embed(title=f"``{PREFIX}mine``",description=f"С помощью этой команды вы можете добывать разные ресурсы и продавать их с помощью команды {PREFIX}sell, а также с помощью команды {PREFIX}inventory вы можете чекнуть свой инвентарь <3")
			embed.add_field(name="Использование",value=f"``{PREFIX}mine``")
			await ctx.reply(embed=embed)
		elif cmd == 'inventory' or cmd == 'inv' or cmd == 'invent':
			embed = discord.Embed(title=f"``{PREFIX}inventory``**/**``{PREFIX}inv``**/**``{PREFIX}invent``",description=f"Ну тут и так всё понятно, с этой командой можно посмотреть что у тебя в инвентаре валяется)")
			embed.add_field(name="Использование",value=f"``{PREFIX}inventory``")
			await ctx.reply(embed=embed)
		elif cmd == 'sell':
			embed = discord.Embed(title=f"``{PREFIX}sell``",description=f"эх, с этой командой можно продавать ресурсы добытые при помощи {PREFIX}mine \n**Список ресурсов:**\n ***trash - Хлам,\n stone - Камень,\n copper - Медь,\n lead - Свинцовая руда,\n tin - Оловянная руда,\n iron - Железная руда,\n gold - Золотая руда,\n diamond - Алмаз,\n chest - Сундук с драгоценностями,\n all - Продать всё (при этом кол-во не надо писать) ***")
			embed.add_field(name="Использование",value=f"``{PREFIX}sell all`` ``{PREFIX}sell <ресурс> <кол-во>``")
			await ctx.reply(embed=embed)
		elif cmd == 'slot':
			embed = discord.Embed(title=f"``{PREFIX}slot``",description=f"Здесь всё просто: \n **3 яблока подряд - 100:coin:** \n **3 вишни подряд - 200:coin:** \n **3 семерки подряд - 10.000:coin:** \n \n Это абсолютный рандом, поэтому выйграть здесь очень сложно, но за то прибыльно!")
			embed.add_field(name="Использование",value=f"``{PREFIX}slot <ставка>``")
		else:
			await ctx.reply("Такой команды не существует!")

bot.run(TOKEN)