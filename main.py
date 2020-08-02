import yaml
import discord
from discord.ext import commands
from discord.ext.commands import bot
import re
from discord.utils import get
from discord.ext.commands import has_permissions, CheckFailure
import os.path
from os import path
import random

token = 'Token hidden for security reasons'

bot = commands.Bot(command_prefix="v!")
bot.remove_command('help')

#on ready
@bot.event
async def on_ready():
	print("Online and ready")
	for guild in bot.guilds:
		break

#hub command
@bot.command()
@has_permissions(administrator=True)
async def category_set(ctx, mute, *category):
	embed = discord.Embed(title="placeholder")
	if discord.utils.get(ctx.guild.categories, name=' '.join(category[:])) != None and discord.utils.get(ctx.guild.roles, id=int(re.sub('<', '', re.sub('>', '', re.sub('&', '', re.sub('@', '', mute)))))):
		catname = discord.utils.get(ctx.guild.categories, name=' '.join(category[:]))
		with open (r'/root/voicerooms/%s.yaml' % str(ctx.message.guild.id), 'a+') as file:
			yaml.dump([str(re.sub('<', '', re.sub('>', '', re.sub('&', '', re.sub('@', '', mute)))))], file)
			yaml.dump([str(' '.join(category[:]))], file)
			CategoryChannel = catname
			await CategoryChannel.create_voice_channel('AFK Room')
			VoiceChannel = discord.utils.get(ctx.guild.voice_channels, name="AFK Room")
			yaml.dump([str(VoiceChannel.id)], file)
			embed = discord.Embed(title="Category set: " + str(catname))
			await ctx.send(embed=embed)
			print("Category set: " + str(catname))
	else:
		embed = discord.Embed(title="Error", description="Invalid command usage. Try again")
		await ctx.send(embed=embed)
@category_set.error
async def hub_create_error(ctx, error):
	if isinstance(error, CheckFailure):
		embed = discord.Embed(title="Error", description="Only members with the Administrator permission can use this command.")
		await ctx.send(embed=embed)

#create command
@bot.command()
async def create(ctx, limit, type, *name):
	embed = discord.Embed(title="placeholder")
	if path.exists(r'/root/voicerooms/%s.yaml' % str(ctx.message.guild.id)):
		with open (r'/root/voicerooms/%s.yaml' % str(ctx.message.guild.id), 'r+') as file:
			if type == "public" or type == "private":
				if int(limit) <= 10 and int(limit) >= 0:
					truename = ' '.join(name[:])
					info = yaml.load(file, Loader=yaml.FullLoader)
					info.reverse()
					CategoryChannel = discord.utils.get(ctx.guild.categories, name=info[1])
					await CategoryChannel.create_voice_channel(str(truename), user_limit=int(limit))
					VoiceChannel = discord.utils.get(ctx.guild.voice_channels, name=str(truename))
					embed = discord.Embed(title="Channel successfully created.", description=f"Name = {truename} \nUser_limit = {str(limit)} \nType = {type}")
					await ctx.send(embed=embed)
					with open (r'/root/voicerooms/%s.yaml' % VoiceChannel.id, 'a+') as voice:
						print(ctx.author.id)
						list = []
						list.append(str(ctx.author.id))
						list.append("removed")
						list.append(str(type))
						list.append("not enabled")
						yaml.dump(list, voice)
						voice.close()
				else:
					embed = discord.Embed(title="Creation unsuccessful", description="Only a maximum of 10 can be set for the user limit.")
					await ctx.send(embed=embed)
			else:
				embed = discord.Embed(title="Creation unsuccessful", description="Invalid command usage. Try again")
				await ctx.send(embed=embed)
	else:
		embed = discord.Embed(title="Creation unsuccessful", description="Your server does not have a category set for voice chats yet.")
		await ctx.send(embed=embed)

#on join/leave
@bot.event
async def on_voice_state_update(member, before, after):
	with open (r'/root/voicerooms/%s.yaml' % str(member.guild.id), 'r+') as catfile3:
		afkid = yaml.load(catfile3, Loader=yaml.FullLoader)
		afkid.reverse()
		print(afkid[2])
		if after.channel:
			if str(after.channel.id) != str(afkid[0]):
				global VoiceChannel
				VoiceChannel = discord.utils.get(member.guild.voice_channels, id=after.channel.id)
				if path.exists(r'/root/voicerooms/%s.yaml' % VoiceChannel.id):
					with open (r'/root/voicerooms/%s.yaml' % VoiceChannel.id, 'r+') as file:
						info = yaml.load(file, Loader=yaml.FullLoader)
						if info[0] == str(member.id):
							embed = discord.Embed(title="placeholder")
							global isPrivate_
							isPrivate_ = False
							for i in info:
								if i == "not enabled":
									info[info.index(i)] = "enabled"
									with open (r'/root/voicerooms/%s.yaml' % VoiceChannel.id, 'w') as filewrite:
										yaml.dump(info, filewrite)
						if info[0] != str(member.id):
							for i in info:
								if i == "not enabled":
									with open (r'/root/voicerooms/%s.yaml' % str(member.guild.id), 'r+') as catfile:
										catinfo = yaml.load(catfile, Loader=yaml.FullLoader)
										catinfo.reverse()
										channel = discord.utils.get(member.guild.voice_channels, id=int(catinfo[0]))
										await member.move_to(channel)
										embed = discord.Embed(title="That voice channel is Locked.", description="When first created, voice channels are locked until their owners join them. This is to prevent others from joining and immediately leaving, thus deleting the channel before the owner can join.")
										await member.send(embed=embed)
								global enableindex
								global privateindex
								global removedindex
								if info.count("private") > 0:
									privateindex = info.index("private")
								if info.count("public") > 0:
								privateindex = info.index("public")
								if i == "not enabled":
									enableindex = info.index("not enabled")
								if i == "enabled":
									enableindex = info.index("enabled")
								removedindex = info.index("removed")
								print(privateindex)
								if i == "private":
									with open (r'/root/voicerooms/%s.yaml' % str(member.guild.id), 'r+') as catfile2:
										if i in info and info.index(i )> privateindex and info.index(i) < enableindex:
											isPrivate_ = True
										if isPrivate_ != True:
											catinfo = yaml.load(catfile2, Loader=yaml.FullLoader)
											catinfo.reverse()
											channel = discord.utils.get(member.guild.voice_channels, id=int(catinfo[0]))
											await member.move_to(channel)
											owner = bot.get_user(int(info[0]))
											embed= discord.Embed(title="That voice channel is Private.", description=f"You must get permission from the channel owner to join that channel.")
											await member.send(embed=embed)
								if i in info and info.index(i) > removedindex and info.index(i) < privateindex:
									with open (r'/root/voicerooms/%s.yaml' % str(member.guild.id), 'r+') as catfile2:
										catinfo = yaml.load(catfile2, Loader=yaml.FullLoader)
										catinfo.reverse()
										channel = discord.utils.get(member.guild.voice_channels, id=int(catinfo[0]))
										await member.move_to(channel)
										owner = bot.get_user(int(info[0]))
										embed = discord.Embed(title="The owner of that voice channel has removed you from the channel.", description="You cannot rejoin if you have been removed.")
										await member.send(embed=embed)
			if str(after.channel.id) == str(afkid[0]):
				await member.add_roles(discord.utils.get(member.guild.roles, id=int(afkid[2])))
	with open (r'/root/voicerooms/%s.yaml' % str(member.guild.id), 'r+') as catfile3:
		afkid = yaml.load(catfile3, Loader=yaml.FullLoader)
		afkid.reverse()
		if before.channel:
			if str(before.channel.id) != str(afkid[0]):
				VoiceChannel = discord.utils.get(member.guild.voice_channels, id=before.channel.id)
				with open (r'/root/voicerooms/%s.yaml' % VoiceChannel.id, 'r+') as file2:
					info = yaml.load(file2, Loader=yaml.FullLoader)
					if info[0] == str(member.id) and len(VoiceChannel.members) != 0:
						usercnt = len(VoiceChannel.members)
						randomuser = random.randint(0, int(usercnt) - 1)
						info[0] = VoiceChannel.members[int(randomuser)].id
						user = bot.get_user(int(info[0]))
						if path.exists(r'/root/voicerooms/%s.yaml' % VoiceChannel.id):
							with open (r'/root/voicerooms/%s.yaml' % VoiceChannel.id, 'w') as file2write:
								yaml.dump(info, file2write)
								embed = discord.Embed(title="The original owner of your voice room has left. You are now the new voice room owner.")
							await user.send(embed=embed)
					if len(VoiceChannel.members) == 0:
						await VoiceChannel.delete()
						file2.close()
			if str(before.channel.id) == str(afkid[0]):
				await member.remove_roles(discord.utils.get(member.guild.roles, id=int(afkid[2])))
		if len(VoiceChannel.members) == 0:
			if path.exists(r'/root/voicerooms/%s.yaml' % VoiceChannel.id):
				os.remove(r'/root/voicerooms/%s.yaml' % VoiceChannel.id)

#remove command
@bot.command()
async def remove(ctx, user):
	global afklocation
	member = re.sub(">", "", user)
	member = re.sub("<", "", member)
	member = re.sub("@", "", member)
	member = re.sub("!", "", member)
	print(member)
	isPrivate = False
	member = ctx.guild.get_member(int(member))
	if ctx.author.voice != None:
		with open (r'/root/voicerooms/%s.yaml' % ctx.author.voice.channel.id, 'r+') as listread:
			read = yaml.load(listread, Loader=yaml.FullLoader)
			if str(read[0]) == str(ctx.author.id):
				for i in read:
					if i == "removed":
						isOwner = True
						read.insert(read.index(i) + 1, member.id)
						print(read)
						listread.close()
						with open (r'/root/voicerooms/%s.yaml' % ctx.author.voice.channel.id, 'w') as listwrite:
							yaml.dump(read, listwrite)
							with open(r'/root/voicerooms/%s.yaml' % str(member.guild.id), 'r+') as afk:
								afkroom = yaml.load(afk, Loader=yaml.FullLoader)
								afkroom.reverse()
								if member.voice != None:
									afklocation = bot.get_channel(int(afkroom[2]))
									embed = discord.Embed(title="The owner of the voice channel has removed you from the channel.", description="You cannot rejoin if you are removed.")
									await member.send(embed=embed)
									await member.move_to(afklocation)
								embed = discord.Embed(title="Operation successful", description="User has been removed from your voice channel.")
								await ctx.send(embed=embed)
								afk.close()
			if str(read[0]) != str(ctx.author.id):
				embed = discord.Embed(title="Error", description="Only the owner of the voice channel can use that command.")
				await ctx.send(embed=embed)
	else:
		embed = discord.Embed(title="Error", description="You currently do not own a voice channel.")
		await ctx.send(embed=embed)

#allow command
@bot.command()
async def allow(ctx, user):
	member = re.sub(">", "", user)
	member = re.sub("<", "", member)
	member = re.sub("@", "", member)
	member = re.sub("!", "", member)
	member = ctx.guild.get_member(int(member))
	isPrivate = False
	if ctx.author.voice != None:
		with open (r'/root/voicerooms/%s.yaml' % ctx.author.voice.channel.id, 'r+') as listread:
			read = yaml.load(listread, Loader=yaml.FullLoader)
			if str(read[0]) == str(ctx.author.id):
				for i in read:
					if i == "private":
						isPrivate = True
						read.insert(read.index(i) + 1, member.id)
						listread.close()
				if isPrivate == False:
					embed = discord.Embed(title="Error", description="Your voice channel is public. This command can only be used with private channels.")
					await ctx.send(embed=embed)
				if isPrivate == True:
					with open (r'/root/voicerooms/%s.yaml' % ctx.author.voice.channel.id, 'w') as listwrite:
						yaml.dump(read, listwrite)
						embed = discord.Embed(title="Operation successful", description="User has been granted permission to join your private voice channel.")
						await ctx.send(embed=embed)
			else:
				embed = discord.Embed(title="Error", description="Only the owner of the voice channel can use that command.")
				await ctx.send(embed=embed)
	else:
		embed = discord.Embed(title="Error", description="You currently do not own a voice channel.")
		await ctx.send(embed=embed)

#owner command
@bot.command()
async def owner(ctx, *channel):
	voicechan = discord.utils.get(ctx.guild.voice_channels, name=' '.join(channel[:]))
	if voicechan:
		if path.exists(r'/root/voicerooms/%s.yaml' % str(voicechan.id)):
			with open(r'/root/voicerooms/%s.yaml' % str(voicechan.id), "r+") as file:
				fileread = yaml.load(file, Loader=yaml.FullLoader)
				user = bot.get_user(int(fileread[0]))
				await ctx.send(f"The owner of that channel is ``{user.name}``.")
		else:
			await ctx.send("Error: That channel isn't a user-created voice channel.")
	else:
		await ctx.send("Error: Not a valid channel.")

#help command
@bot.command()
async def help(ctx, *command):
	if len(command) == 0:
		embed = discord.Embed(title="List of commands", description="category_set \ncreate \nremove \nallow \nowner")
		await ctx.send(embed=embed)
	if len(command) > 0:
		if command[0] == "category_set":
			embed = discord.Embed(title="category_set <mute-role> <category>", description="Sets the category for future voice channels. **Only users with the administrator permission can use this** \n\nmute-role: Role to be set for muting users \ncategory: The category you want to set")
			await ctx.send(embed=embed)
		elif command[0] == "create":
			embed = discord.Embed(title="create <user_limit> <type> <name>", description="Creates a new voice channel. \n\nuser_limit: The limit on how many users can join \ntype: The type of voice channel. Typing \'public\' will allow all users to join. Typing \'private\' will require users to have permission from you to join \nname: The name of your channel")
			await ctx.send(embed=embed)
		elif command[0] == "remove":
			embed = discord.Embed(title="remove <user>", description="Removes a user from your channel and prevents them from rejoining. \n\nuser: The user you want to remove")
			await ctx.send(embed=embed)
		elif command[0] == "allow":
			embed = discord.Embed(title="allow <user>", description="Gives permission for a user to join your channel. *Only useable if your channel is private* \n\nuser: The user you would like to give permission to")
			await ctx.send(embed=embed)
		elif command[0] == "owner":
			embed = discord.Embed(title="owner <channel>", description="Returns the owner of the specified channel. \n\nchannel: The channel you want to check")
			await ctx.send(embed=embed)
		else:
			embed = discord.Embed(title="Error", description="Not a valid command.")
			await ctx.send(embed=embed)



bot.run(token)
